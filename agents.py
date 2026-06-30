"""
Three agents that power the self-improvement loop:

  extractor  — answers wealth-manager questions using the current prompt
  judge      — scores each answer on 4 dimensions (0–25 each, total 0–100)
  optimizer  — analyzes failure patterns and rewrites the extraction prompt
"""
import json

import anthropic

_client = anthropic.Anthropic()
MODEL = "claude-opus-4-8"

# Approximate token pricing for claude-opus-4-8 ($/million tokens)
_PRICE_INPUT = 15.0
_PRICE_OUTPUT = 75.0


def _call(system: str, user: str, max_tokens: int = 512) -> tuple[str, dict]:
    """Call the API and return (text, usage_dict)."""
    msg = _client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    usage = {
        "input_tokens": msg.usage.input_tokens,
        "output_tokens": msg.usage.output_tokens,
        "cost_usd": (
            msg.usage.input_tokens * _PRICE_INPUT / 1_000_000
            + msg.usage.output_tokens * _PRICE_OUTPUT / 1_000_000
        ),
    }
    return msg.content[0].text, usage


def extract(document: str, question: str, prompt: str) -> tuple[str, dict]:
    """
    Extractor agent: answers a question about the document using `prompt` as its system instruction.
    Returns (answer_text, usage).
    """
    return _call(
        system=prompt,
        user=f"Document:\n{document}\n\nQuestion: {question}",
        max_tokens=300,
    )


def judge(document: str, question: str, answer: str) -> tuple[dict, dict]:
    """
    Judge agent: scores an answer on four dimensions.
    Returns (score_dict, usage).

    score_dict keys:
      specificity   0–25   cites specific numbers/names from the document
      completeness  0–25   covers all key points, nothing material omitted
      accuracy      0–25   factually correct per the document
      utility       0–25   actionable for a wealth manager
      score         0–100  sum of above
      feedback      str    what was missing or wrong
    """
    system = """You are a senior financial analyst evaluating AI-generated responses to wealth management questions.

Score the answer on four dimensions (each 0–25):
- specificity:   Does it cite specific numbers, names, or dates from the document?
- completeness:  Does it cover all key points without omitting material information?
- accuracy:      Is every claim factually correct based on the document?
- utility:       Is it directly actionable for a wealth manager making investment decisions?

You must respond with valid JSON only — no prose before or after:
{"specificity": <int>, "completeness": <int>, "accuracy": <int>, "utility": <int>, "feedback": "<one sentence on what was missing or wrong>"}"""

    user = (
        f"Document:\n{document}\n\n"
        f"Question: {question}\n\n"
        f"Answer to evaluate:\n{answer}"
    )

    text, usage = _call(system=system, user=user, max_tokens=256)

    # Strip markdown fences if the model wraps JSON
    cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    data = json.loads(cleaned)
    data["score"] = data["specificity"] + data["completeness"] + data["accuracy"] + data["utility"]
    return data, usage


def optimize(current_prompt: str, failures: dict[str, dict], answers: dict[str, str]) -> tuple[str, dict]:
    """
    Optimizer agent: given the current prompt and the questions it failed on,
    returns an improved prompt.
    Returns (new_prompt_text, usage).
    """
    failure_block = "\n\n".join(
        f"QUESTION: {q}\n"
        f"SCORE: {s['score']}/100\n"
        f"FEEDBACK: {s['feedback']}\n"
        f"ANSWER PRODUCED:\n{answers[q][:300]}"
        for q, s in failures.items()
    )

    system = "You are an expert prompt engineer specializing in financial document analysis."
    user = f"""The current extraction prompt is:
---
{current_prompt}
---

It scored below 80/100 on these questions:

{failure_block}

Analyze the failure patterns across all questions. Then rewrite the extraction prompt so that:
- Answers cite specific data (numbers, names, dates) from the document
- All material aspects of each question are covered
- Responses are factually precise and investment-actionable
- Format is concise (under 150 words per answer)

Return ONLY the new prompt text. No explanation, no preamble."""

    return _call(system=system, user=user, max_tokens=600)
