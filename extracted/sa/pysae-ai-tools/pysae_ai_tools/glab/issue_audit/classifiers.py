"""Classifiers and generators that may call external services (LLM, glab API)."""

import re

from ...common.glab.models import GitLabIssue
from ...common.llm import get_llm_client
from ...common.project_config import ProjectConfigError, load_project_config_for
from ...common.references.gitlab_labels import (
    TypeLabel,
)
from .diagnostic import DetectionMethod

CLASSIFIER_MODEL = "claude-haiku-4-5"
_MAX_TOKENS = 200

# ---------------------------------------------------------------------------
# Type classification
# ---------------------------------------------------------------------------

TYPE_KEYWORDS: dict[str, list[str]] = {
    "type::bug": [
        r"\bbug\b",
        r"\bfix\b",
        r"\bbroken\b",
        r"\bregression\b",
        r"\bcrash",
        r"\berror\b",
        r"\bfail",
        r"\b500\b",
        r"\b404\b",
        r"\bcorrect",
        r"\bincorrect\b",
        r"\bwrong\b",
        r"\bissue\b",
        r"\bproblem\b",
    ],
    "type::feature": [
        r"\badd\b",
        r"\bimplement",
        r"\bnew\b",
        r"\bfeature\b",
        r"\buser story\b",
        r"\benable\b",
        r"\bintroduce\b",
        r"\bsupport\b",
        r"\ballow\b",
        r"\bajouter\b",
        r"\bnouveau\b",
        r"\bnouvelle\b",
    ],
    "type::technical": [
        r"\btech\b",
        r"\bmigrat",
        r"\btooling\b",
        r"\bscript\b",
        r"\bci\b",
        r"\bcd\b",
        r"\binfra\b",
        r"\bdeploy",
        r"\bpipeline\b",
        r"\bdevops\b",
        r"\bdocker\b",
        r"\bhelm\b",
        r"\bterraform\b",
        r"\bsecurity\b",
        r"\baws\b",
        r"\beks\b",
        r"\bs3\b",
        r"\becr\b",
        r"\bnat\b",
        r"\bvpc\b",
        r"\bgateway\b",
        r"\belastic\b",
        r"\bargo",
        r"\bkubernetes\b",
        r"\bk8s\b",
        r"\brefactor",
        r"\brename\b",
        r"\bcleanup\b",
        r"\brestructure\b",
        r"\breorganiz",
        r"\bsimplif",
        r"\bextract\b",
        r"\bsplit\b",
    ],
    "type::debt": [
        r"\bdebt\b",
        r"\bdeprecat",
        r"\bdependenc",
        r"\bupgrade\b",
        r"\bbump\b",
        r"\bcve\b",
        r"\beol\b",
        r"\bend of life\b",
    ],
}

VALID_TYPE_LABELS = {str(t) for t in TypeLabel}


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------


def _complete(prompt: str) -> str | None:
    """Run a single haiku completion through the shared LLM layer.

    Routes through :func:`common.llm.get_llm_client` (mockable, usage tracked)
    instead of shelling out to the ``claude`` binary. Non-blocking: returns
    ``None`` on any failure (no API key, provider CLI missing, API down, …).
    """
    try:
        response = get_llm_client().complete(
            model=CLASSIFIER_MODEL,
            max_tokens=_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:  # noqa: BLE001  # non-blocking on any provider failure
        return None
    answer = response.text.strip().strip('"').strip("'")
    return answer or None


# ---------------------------------------------------------------------------
# Type classification
# ---------------------------------------------------------------------------


def classify_type_with_claude(title: str, description: str, labels: list[str]) -> str | None:
    """Use an LLM to classify an issue into a type label."""
    prompt = (
        "You are classifying a GitLab issue into exactly one type. Rules:\n"
        "- Output ONLY the type label, nothing else (no quotes, no explanation)\n"
        "- Choose from: type::bug, type::feature, type::technical, type::debt\n\n"
        "Definitions:\n"
        "- type::bug — Defect, regression, incorrect behavior, crash, error\n"
        "- type::feature — New user-facing functionality, user story\n"
        "- type::technical — Tooling, scripts, CLI, migrations, infra, CI/CD, security, refactoring\n"
        "- type::debt — Technical debt: dependency upgrades, deprecations, cleanup with no behavior change\n\n"
        f"Title: {title}\n"
        f"Labels: {', '.join(labels)}\n"
        f"Description (first 500 chars):\n{description[:500]}\n"
    )
    answer = _complete(prompt)
    if answer and answer in VALID_TYPE_LABELS:
        return answer
    return None


def _project_path_from_issue(issue: GitLabIssue) -> str:
    """Extract ``group/repo`` from an issue web URL (``""`` if it has no path)."""
    # https://gitlab.com/<group>/<repo>/-/issues/N → "<group>/<repo>"
    after_host = issue.web_url.split("//", 1)[-1].split("/", 1)[-1]
    return after_host.split("/-/", 1)[0].strip("/")


def guess_type_label(issue: GitLabIssue) -> tuple[str | None, DetectionMethod]:
    """Guess the type label from the repo config, keywords, then Claude as fallback.

    Returns ``(label, method)`` where ``method`` is the :class:`DetectionMethod` that
    produced the guess.
    """
    # 1. Strong signal: a repo can declare a default type in its config (e.g. infra/tooling
    #    repos → type::technical). No hardcoded repo→type table — the policy lives per-repo.
    project_path = _project_path_from_issue(issue)
    if project_path:
        try:
            config = load_project_config_for(project_path)
        except (RuntimeError, ProjectConfigError):
            config = None
        if config and config.issues.default_type in VALID_TYPE_LABELS:
            return config.issues.default_type, DetectionMethod.PROJECT

    title = issue.title
    description = (issue.description or "")[:1000]
    text = f"{title} {description}".lower()

    # 2. Keyword scoring
    scores: dict[str, int] = {}
    for type_label, patterns in TYPE_KEYWORDS.items():
        score = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
        if score > 0:
            scores[type_label] = score

    if scores:
        best = max(scores, key=lambda k: scores[k])
        second = sorted(scores.values(), reverse=True)
        if scores[best] >= 2 and (len(second) < 2 or second[0] > second[1]):
            return best, DetectionMethod.KEYWORDS

    # 3. Claude fallback
    labels = issue.labels
    result = classify_type_with_claude(title, description, labels)
    if result:
        return result, DetectionMethod.CLAUDE
    return None, DetectionMethod.NONE


def guess_domain_label(issue: GitLabIssue) -> str | None:
    """Guess the domain label from the issue's repo **config** (`project.labels`).

    Loads the repo's `.pysae-ai-tools.yaml` (cached) and returns its first declared
    domain label. A repo with no config — or that can't be reached — yields ``None``
    (ai-tools holds no hardcoded repo→domain table).
    """
    project_path = _project_path_from_issue(issue)
    if not project_path:
        return None
    try:
        config = load_project_config_for(project_path)
    except (RuntimeError, ProjectConfigError):
        return None
    return config.project.domain_label() if config else None


# ---------------------------------------------------------------------------
# Title generation
# ---------------------------------------------------------------------------


def generate_title_with_claude(title: str, description: str, labels: list[str]) -> str | None:
    """Use an LLM to generate a proper English title."""
    prompt = (
        "You are rewriting a GitLab issue title. Rules:\n"
        "- Output ONLY the new title, nothing else (no quotes, no explanation)\n"
        "- English only\n"
        "- Action-oriented (start with a verb: Add, Fix, Implement, Update, Remove, etc.)\n"
        "- No prefix like [API], tech:, scope:, feat:, fix:, etc. (labels handle scoping)\n"
        "- Concise: under 80 characters\n"
        "- Summarize the issue well based on the description\n\n"
        f"Current title: {title}\n"
        f"Labels: {', '.join(labels)}\n"
        f"Description (first 500 chars):\n{description[:500]}\n"
    )
    new_title = _complete(prompt)
    if new_title and len(new_title) < 120:
        return new_title
    return None
