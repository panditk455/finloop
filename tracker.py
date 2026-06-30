"""
Observability layer: records every iteration in full detail.
Saves to output/history.json so you can inspect the full improvement arc after the run.
"""
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class Iteration:
    iteration: int
    prompt: str
    answers: dict          # question → answer text
    scores: dict           # question → score dict (specificity, completeness, ...)
    avg_score: float
    total_tokens: int
    total_cost_usd: float


@dataclass
class Tracker:
    iterations: list[Iteration] = field(default_factory=list)
    _cumulative_cost: float = field(default=0.0, repr=False)
    _cumulative_tokens: int = field(default=0, repr=False)

    def record(
        self,
        iteration: int,
        prompt: str,
        answers: dict,
        scores: dict,
        avg_score: float,
        tokens: int,
        cost: float,
    ):
        self._cumulative_cost += cost
        self._cumulative_tokens += tokens
        self.iterations.append(
            Iteration(
                iteration=iteration,
                prompt=prompt,
                answers=answers,
                scores=scores,
                avg_score=avg_score,
                total_tokens=tokens,
                total_cost_usd=cost,
            )
        )

    @property
    def cumulative_cost(self) -> float:
        return self._cumulative_cost

    @property
    def cumulative_tokens(self) -> int:
        return self._cumulative_tokens

    def score_history(self) -> list[float]:
        return [it.avg_score for it in self.iterations]

    def ascii_chart(self) -> str:
        scores = self.score_history()
        if not scores:
            return ""
        max_score = 100
        height = 8
        lines = []
        for row in range(height, 0, -1):
            threshold = (row / height) * max_score
            cells = []
            for s in scores:
                cells.append("█" if s >= threshold else " ")
            label = f"{threshold:>3.0f} │"
            lines.append(label + " ".join(cells))
        axis = "    └" + "──".join(["─"] * len(scores))
        labels = "      " + "  ".join(str(it.iteration) for it in self.iterations)
        lines.append(axis)
        lines.append(labels + "  ← iteration")
        return "\n".join(lines)

    def save(self, path: str = "output/history.json"):
        out = Path(path)
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            json.dumps(
                {
                    "summary": {
                        "iterations": len(self.iterations),
                        "initial_score": self.iterations[0].avg_score if self.iterations else 0,
                        "final_score": self.iterations[-1].avg_score if self.iterations else 0,
                        "cumulative_tokens": self._cumulative_tokens,
                        "cumulative_cost_usd": round(self._cumulative_cost, 4),
                    },
                    "iterations": [asdict(it) for it in self.iterations],
                },
                indent=2,
            )
        )
        return out
