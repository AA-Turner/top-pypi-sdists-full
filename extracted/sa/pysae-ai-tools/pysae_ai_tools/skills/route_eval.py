"""Behavioural oracle for natural-language skill triggering.

The deterministic lint (``internal scan-skill``) checks the *form* of a description; this
harness checks the *behaviour*: given a real user phrasing, does the right skill win? It
measures **recall@1** (the expected skill is picked) and **collisions** (which wrong skill
stole the phrasing — the actionable list of pairs to disambiguate), over a versioned corpus.

The routing itself is done OUTSIDE this script so it needs **no API key**: the
``clawd-route-eval`` skill fans out sub-agents *of the active Claude Code session* to route
each utterance, then feeds their predictions back here. The flow is three pure, deterministic
pieces:

- ``prompts`` — emit the router system prompt (the skill catalogue) + the utterances to route.
  Carries NO expected answer, so the routing agents are blind.
- ``score`` — read a predictions file, compare against the corpus, print recall + collisions.
- ``api`` — optional: route via a direct Anthropic API call (for CI, needs ANTHROPIC_API_KEY).

``evaluate`` takes an injected ``predict_fn`` so the metrics are unit-tested without any LLM.
"""

import importlib.resources
import json
import os
import sys
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated

import typer
import yaml

from ..common.llm import get_llm_client
from ..internal.scan_skill import _bundled_skills_root, _extract_description

ROUTER_MODEL = "claude-haiku-4-5-20251001"
_MAX_TOKENS = 32

app = typer.Typer(no_args_is_help=True, help="Measure natural-language skill-routing recall + collisions.")


@dataclass(frozen=True)
class Utterance:
    """One corpus entry: a phrasing and the skill it should route to."""

    text: str
    expected: str
    lang: str = ""
    register: str = ""


@dataclass
class EvalReport:
    """Aggregate routing metrics over a corpus run."""

    total: int
    correct: int
    misroutes: list[tuple[Utterance, str]] = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.correct / self.total if self.total else 0.0

    @property
    def collisions(self) -> dict[tuple[str, str], int]:
        """``(expected, predicted) -> count`` for every wrong prediction — what to disambiguate."""
        c: Counter[tuple[str, str]] = Counter()
        for utt, predicted in self.misroutes:
            c[(utt.expected, predicted)] += 1
        return dict(c)

    def to_dict(self) -> dict[str, object]:
        return {
            "total": self.total,
            "correct": self.correct,
            "recall": round(self.recall, 4),
            "misroutes": [
                {"text": u.text, "expected": u.expected, "predicted": p, "lang": u.lang, "register": u.register}
                for u, p in self.misroutes
            ],
            "collisions": [{"expected": e, "predicted": p, "count": n} for (e, p), n in self.collisions.items()],
        }


def load_skills(root: Path | None = None) -> dict[str, str]:
    """Map each bundled skill name to its description (empty string if absent)."""
    root = root or _bundled_skills_root()
    skills: dict[str, str] = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()):
        desc = _extract_description((d / "SKILL.md").read_text(encoding="utf-8", errors="replace"))
        skills[d.name] = desc or ""
    return skills


def load_corpus(path: Path | None = None) -> list[Utterance]:
    """Load the routing corpus (bundled ``route_corpus.yaml`` unless ``path`` is given)."""
    if path is not None:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raw = yaml.safe_load(
            importlib.resources.files("pysae_ai_tools.skills").joinpath("route_corpus.yaml").read_text(encoding="utf-8")
        )
    return [
        Utterance(
            text=str(e["text"]),
            expected=str(e["expected"]),
            lang=str(e.get("lang", "")),
            register=str(e.get("register", "")),
        )
        for e in (raw or [])
    ]


def build_router_system_prompt(skills: dict[str, str]) -> str:
    """System prompt: list the skills and instruct the router to return exactly one name."""
    catalogue = "\n".join(f"- {name}: {desc}" for name, desc in sorted(skills.items()))
    return (
        "You are a router. Given a user message, pick the SINGLE most appropriate skill from the "
        "catalogue below. Reply with ONLY the skill name (the token before the colon), nothing else — "
        "no punctuation, no explanation. If none fits, reply 'none'.\n\n"
        f"Skills:\n{catalogue}"
    )


def evaluate(corpus: Iterable[Utterance], predict_fn: Callable[[Utterance], str]) -> EvalReport:
    """Run ``predict_fn`` over the corpus and aggregate recall + misroutes.

    ``predict_fn`` maps an utterance to the predicted skill name; injecting it keeps the
    metrics testable without any API call.
    """
    corpus = list(corpus)
    correct = 0
    misroutes: list[tuple[Utterance, str]] = []
    for utt in corpus:
        predicted = predict_fn(utt).strip()
        if predicted == utt.expected:
            correct += 1
        else:
            misroutes.append((utt, predicted))
    return EvalReport(total=len(corpus), correct=correct, misroutes=misroutes)


def load_predictions(path: Path, corpus: list[Utterance]) -> dict[int, str]:
    """Parse a predictions file into ``{corpus_index: predicted_skill}``.

    Accepts either a mapping ``{"0": "ci-deploy", ...}`` or a list of objects
    ``[{"id": 0, "predicted": "ci-deploy"}, ...]`` — whichever the routing step wrote.
    Indices are positions in the corpus the matching ``prompts`` run emitted.
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[int, str] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            out[int(k)] = str(v)
    elif isinstance(raw, list):
        for item in raw:
            out[int(item["id"])] = str(item["predicted"])
    else:
        raise ValueError("predictions must be a JSON object {id: skill} or a list of {id, predicted}")
    valid = range(len(corpus))
    unknown = sorted(i for i in out if i not in valid)
    if unknown:
        raise ValueError(f"predictions reference unknown corpus indices (not in 0..{len(corpus) - 1}): {unknown}")
    missing = [i for i in valid if i not in out]
    if missing:
        raise ValueError(f"predictions missing for corpus indices: {missing}")
    return out


@app.command()
def prompts(
    corpus_path: Annotated[
        Path | None, typer.Option("--corpus", help="Corpus YAML (defaults to the bundled one).")
    ] = None,
    out: Annotated[Path | None, typer.Option("--out", help="Write the prompt bundle here (default: stdout).")] = None,
) -> None:
    """Emit the routing tasks for the session's sub-agents — the catalogue prompt + utterances.

    Carries NO expected answers, so the routing agents stay blind. The orchestrating skill
    (``clawd-route-eval``) feeds each utterance + this system prompt to a sub-agent, collects
    ``{id: skill}`` predictions, then calls ``score``.
    """
    skills = load_skills()
    corpus = load_corpus(corpus_path)
    bundle = {
        "system": build_router_system_prompt(skills),
        "utterances": [{"id": i, "text": u.text} for i, u in enumerate(corpus)],
    }
    text = json.dumps(bundle, indent=2, ensure_ascii=False)
    if out is not None:
        out.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {len(corpus)} routing tasks to {out}", file=sys.stderr)
    else:
        sys.stdout.write(text + "\n")


@app.command()
def score(
    predictions: Annotated[
        Path, typer.Option("--predictions", help="Predictions file ({id: skill} or [{id, predicted}]).")
    ],
    corpus_path: Annotated[
        Path | None, typer.Option("--corpus", help="Corpus YAML (defaults to the bundled one).")
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the full report as JSON.")] = False,
    min_recall: Annotated[
        float, typer.Option("--min-recall", help="Exit non-zero if recall falls below this (0 = never fail).")
    ] = 0.0,
) -> None:
    """Score a predictions file against the corpus — recall@1 + collisions. No API key needed."""
    corpus = load_corpus(corpus_path)
    if not corpus:
        print("Empty corpus — nothing to score.", file=sys.stderr)
        raise typer.Exit(code=1)
    preds = load_predictions(predictions, corpus)
    # Predictions are keyed by corpus position; feed them in order (evaluate iterates in order),
    # which is robust to duplicate utterances that a value-based lookup would conflate.
    ordered = iter(preds[i] for i in range(len(corpus)))
    report = evaluate(corpus, lambda u: next(ordered))
    _emit(report, as_json=as_json)
    if min_recall > 0 and report.recall < min_recall:
        print(f"FAIL: recall {report.recall:.1%} < min {min_recall:.1%}", file=sys.stderr)
        raise typer.Exit(code=1)


@app.command()
def api(
    model: Annotated[str, typer.Option("--model", help="Router model id.")] = ROUTER_MODEL,
    corpus_path: Annotated[
        Path | None, typer.Option("--corpus", help="Corpus YAML (defaults to the bundled one).")
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the full report as JSON.")] = False,
    min_recall: Annotated[
        float, typer.Option("--min-recall", help="Exit non-zero if recall falls below this (0 = never fail).")
    ] = 0.0,
) -> None:
    """Route via a direct Anthropic API call and score — optional, for CI (needs ANTHROPIC_API_KEY).

    The default, key-free path is ``prompts`` + session sub-agents + ``score`` (see the
    ``clawd-route-eval`` skill). This command exists only for an automated CI run with a real key.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set — use the key-free 'clawd-route-eval' skill instead.", file=sys.stderr)
        raise typer.Exit(code=0)
    skills = load_skills()
    corpus = load_corpus(corpus_path)
    if not corpus:
        print("Empty corpus — nothing to evaluate.", file=sys.stderr)
        raise typer.Exit(code=1)
    report = evaluate(corpus, _llm_predictor(model, skills))
    _emit(report, as_json=as_json)
    if min_recall > 0 and report.recall < min_recall:
        print(f"FAIL: recall {report.recall:.1%} < min {min_recall:.1%}", file=sys.stderr)
        raise typer.Exit(code=1)


def _emit(report: EvalReport, *, as_json: bool) -> None:
    """Print a report either as JSON or as a human-readable recall + collision summary."""
    if as_json:
        json.dump(report.to_dict(), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return
    print(f"Routing recall@1: {report.correct}/{report.total} = {report.recall:.1%}\n")
    if report.misroutes:
        print("Collisions (expected → predicted):")
        for (expected, predicted), n in sorted(report.collisions.items(), key=lambda kv: -kv[1]):
            print(f"  {expected:32} → {predicted:32} ×{n}")
        print("\nMisrouted utterances:")
        for utt, predicted in report.misroutes:
            print(f"  [{utt.expected} → {predicted}] {utt.text!r}")
    else:
        print("No collisions — every utterance routed to its expected skill.")


def _llm_predictor(model: str, skills: dict[str, str]) -> Callable[[Utterance], str]:
    """Build a predict_fn backed by a direct Anthropic API call.

    This CI-oriented mode is pinned to the ``anthropic`` provider (it exists
    precisely to exercise the direct API path) and requires ``ANTHROPIC_API_KEY``
    regardless of the global default provider.
    """
    client = get_llm_client(provider="anthropic", api_key=os.environ.get("ANTHROPIC_API_KEY"))
    system = build_router_system_prompt(skills)

    def predict(utt: Utterance) -> str:
        response = client.complete(
            model=model,
            max_tokens=_MAX_TOKENS,
            system=system,
            messages=[{"role": "user", "content": utt.text}],
        )
        text = response.text
        return text.strip().strip("/").splitlines()[0].strip() if text else "none"

    return predict


if __name__ == "__main__":
    app()
