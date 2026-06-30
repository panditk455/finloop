"""
FinLoop: Self-Improving Financial Analysis Agent

An agentic loop that iteratively improves a financial document analysis prompt.
Three agents collaborate:
  1. Extractor  — answers wealth-manager questions using the current prompt
  2. Judge      — scores each answer on specificity, completeness, accuracy, utility
  3. Optimizer  — rewrites the prompt to address failure patterns

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 main.py

Output:
    - Live score table printed each iteration
    - ASCII improvement chart at the end
    - Full history saved to output/history.json
"""
from pathlib import Path

from agents import extract, judge, optimize
from data import DOCUMENT, QUESTIONS
from tracker import Tracker

PROMPT_FILE = Path(__file__).parent / "prompts" / "v0.txt"
OUTPUT_DIR = Path(__file__).parent / "output"
MAX_ITERATIONS = 6
TARGET_SCORE = 88          # stop early if we hit this
FAILURE_THRESHOLD = 78     # below this = a "failed" question that the optimizer addresses


def load_prompt() -> str:
    return PROMPT_FILE.read_text().strip()


def header(text: str):
    bar = "=" * 64
    print(f"\n{bar}")
    print(f"  {text}")
    print(bar)


def score_bar(score: float, width: int = 20) -> str:
    filled = int(score / 100 * width)
    return f"[{'█' * filled}{'░' * (width - filled)}] {score:.0f}/100"


def main():
    tracker = Tracker()
    prompt = load_prompt()

    header("FinLoop: Self-Improving Financial Analysis Agent")
    print(f"  Document : WealthTech Corp 10-K excerpt")
    print(f"  Questions: {len(QUESTIONS)}")
    print(f"  Max iters: {MAX_ITERATIONS}  |  Target score: {TARGET_SCORE}/100")

    for i in range(MAX_ITERATIONS + 1):
        print(f"\n{'─' * 64}")
        print(f"  ITERATION {i}  {'(baseline — weak prompt)' if i == 0 else ''}")
        print(f"{'─' * 64}")

        answers = {}
        scores = {}
        iter_tokens = 0
        iter_cost = 0.0

        # ── Extract + Judge each question ───────────────────────────────────
        for q in QUESTIONS:
            answer, ex_usage = extract(DOCUMENT, q, prompt)
            score, jd_usage = judge(DOCUMENT, q, answer)

            answers[q] = answer
            scores[q] = score

            iter_tokens += ex_usage["input_tokens"] + ex_usage["output_tokens"]
            iter_tokens += jd_usage["input_tokens"] + jd_usage["output_tokens"]
            iter_cost += ex_usage["cost_usd"] + jd_usage["cost_usd"]

            short_q = q[:52] + "…" if len(q) > 52 else q
            print(f"\n  Q: {short_q}")
            print(f"     {score_bar(score['score'])}")
            print(f"     Feedback: {score['feedback']}")

        avg_score = sum(s["score"] for s in scores.values()) / len(scores)
        print(f"\n  ── Average: {score_bar(avg_score)}  |  ${iter_cost:.3f}  |  {iter_tokens:,} tokens")

        tracker.record(i, prompt, answers, scores, avg_score, iter_tokens, iter_cost)

        # ── Check stopping conditions ───────────────────────────────────────
        if avg_score >= TARGET_SCORE:
            print(f"\n  Target score reached. Loop complete.")
            break
        if i == MAX_ITERATIONS:
            break

        # ── Optimize: focus on questions that underperformed ────────────────
        failures = {q: scores[q] for q in scores if scores[q]["score"] < FAILURE_THRESHOLD}
        if not failures:
            print(f"\n  All questions above {FAILURE_THRESHOLD}. Optimizing for marginal gains.")
            failures = scores  # optimize everything if nothing is badly broken

        print(f"\n  Optimizer analyzing {len(failures)} question(s) to improve…")
        new_prompt, opt_usage = optimize(prompt, failures, answers)
        prompt = new_prompt
        tracker._cumulative_cost += opt_usage["cost_usd"]
        tracker._cumulative_tokens += opt_usage["input_tokens"] + opt_usage["output_tokens"]

    # ── Final summary ───────────────────────────────────────────────────────
    history = tracker.score_history()
    gain = history[-1] - history[0]

    header("RESULTS")
    print(f"  Iterations run : {len(history)}")
    print(f"  Initial score  : {history[0]:.1f}/100")
    print(f"  Final score    : {history[-1]:.1f}/100")
    print(f"  Score gain     : +{gain:.1f} points")
    print(f"  Total tokens   : {tracker.cumulative_tokens:,}")
    print(f"  Total cost     : ${tracker.cumulative_cost:.3f}")

    print(f"\n  Score over iterations:\n")
    for line in tracker.ascii_chart().split("\n"):
        print(f"  {line}")

    saved = tracker.save(str(OUTPUT_DIR / "history.json"))
    print(f"\n  Full history → {saved}")

    header("WHAT THE AGENT LEARNED")
    print("  The prompt evolved from a generic assistant instruction to a structured")
    print("  financial analyst persona with explicit requirements for:")
    print("    • Specific data citation (numbers, names, dates)")
    print("    • Completeness across all material points")
    print("    • Investment-actionable framing")
    print()
    print("  This is the core of agentic self-improvement: the system knows")
    print("  how to evaluate itself, and uses that evaluation to rewrite its own")
    print("  instructions — without human intervention each iteration.")
    print()
    print("  Inspect output/history.json to see every prompt version,")
    print("  every answer, and every score breakdown.")
    print("=" * 64)


if __name__ == "__main__":
    main()
