"""Find orphan issues (no parent epic) and score them against open epics.

Outputs a JSON report with two sections:
- ``matches``: issues grouped by best-matching epic (with confidence score)
- ``orphans``: issues that could not be matched to any epic

The SKILL.md orchestrates user validation on top of this output.

Usage:
    pysae-ai-tools glab issue-find-epic [OPTIONS]
"""

import functools
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Annotated, Any

import typer

from ..common.glab.fetch_issues import (
    CommonAllProjects,
    CommonIssueFilters,
    CommonMe,
    CommonProject,
    CommonSearch,
    CommonUser,
    glab_api_paginated,
    resolve_issue_filters,
    run_glab,
)
from ..common.glab.models import GitLabIssue
from ..common.group import resolve_group_id
from ..common.project_config import domain_labels
from ..common.references.gitlab_labels import BoardLabel


@functools.lru_cache(maxsize=1)
def _domain_vocab() -> frozenset[str]:
    """Domain-label vocabulary, live from the repo configs (cached once per process).

    Replaces the former hardcoded ``DOMAIN_LABELS`` set: which labels count as a
    *domain* (vs workflow/meta) is whatever the ``.pysae-ai-tools.yaml`` configs declare.
    Degrades to an empty set when the group listing can't be reached.
    """
    return frozenset(domain_labels())


# Issues with these labels are excluded from epic matching (bugs, support, cancelled)
EXCLUDED_LABELS = {"type::bug", "Support 📞", "ANNULE"}

# Board column labels — issues must have at least one to be considered "in workflow"
BOARD_LABELS: set[str] = set(BoardLabel)

# Stop-words excluded from keyword extraction (English + French common terms)
_STOP_WORDS = frozenset(
    "a an the and or but in on of to for is it this that with from by at as be are was were "
    "not no can will do does did has have had been would should could may might shall into "
    "le la les un une des du de et ou en à par pour est ce qui que dans sur avec se ne pas".split()
)

HIGH_CONFIDENCE = 0.7
MEDIUM_CONFIDENCE = 0.4


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class GitLabEpic:
    """A GitLab group epic."""

    iid: int = 0
    title: str = ""
    description: str = ""
    labels: list[str] = field(default_factory=list)
    web_url: str = ""
    child_issue_titles: list[str] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "GitLabEpic":
        return cls(
            iid=data.get("iid", 0),
            title=data.get("title", ""),
            description=(data.get("description") or "")[:500],
            labels=data.get("labels", []),
            web_url=data.get("web_url", ""),
        )


@dataclass
class IssueMatch:
    """An issue matched to an epic with a confidence score."""

    issue: GitLabIssue
    score: float
    confidence: str  # "high" | "medium"
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "iid": self.issue.iid,
            "project_id": self.issue.project_id,
            "title": self.issue.title,
            "web_url": self.issue.web_url,
            "labels": self.issue.labels,
            "score": round(self.score, 3),
            "confidence": self.confidence,
            "reasons": self.reasons,
        }


@dataclass
class EpicGroup:
    """An epic with its matched issues."""

    epic: GitLabEpic
    matches: list[IssueMatch] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "epic_iid": self.epic.iid,
            "epic_title": self.epic.title,
            "epic_url": self.epic.web_url,
            "issues": [m.to_dict() for m in sorted(self.matches, key=lambda m: -m.score)],
        }


@dataclass
class ThemeCluster:
    """A group of orphan issues sharing a common theme."""

    theme: str
    keywords: list[str]
    issues: list[GitLabIssue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "keywords": self.keywords,
            "issues": [
                {
                    "iid": i.iid,
                    "project_id": i.project_id,
                    "title": i.title,
                    "web_url": i.web_url,
                    "labels": i.labels,
                }
                for i in self.issues
            ],
        }


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------


def _tokenize(text: str) -> set[str]:
    """Extract meaningful lowercase tokens from text."""
    words = re.findall(r"[a-zA-ZÀ-ÿ]{3,}", text.lower())
    return {w for w in words if w not in _STOP_WORDS}


def _keyword_overlap(tokens_a: set[str], tokens_b: set[str]) -> float:
    """Jaccard-like overlap between two token sets, returns 0-1."""
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def _label_overlap(labels_a: list[str], labels_b: list[str]) -> float:
    """Score based on shared domain labels, returns 0-1."""
    vocab = _domain_vocab()
    domain_a = {lbl for lbl in labels_a if lbl in vocab}
    domain_b = {lbl for lbl in labels_b if lbl in vocab}
    if not domain_a or not domain_b:
        return 0.0
    return len(domain_a & domain_b) / len(domain_a | domain_b)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _score_issue_epic(issue: GitLabIssue, epic: GitLabEpic) -> tuple[float, list[str]]:
    """Score how well an issue matches an epic. Returns (score, reasons)."""
    score = 0.0
    reasons: list[str] = []

    # 1. Title keyword overlap (weight: 0.4)
    issue_title_tokens = _tokenize(issue.title)
    epic_title_tokens = _tokenize(epic.title)
    title_score = _keyword_overlap(issue_title_tokens, epic_title_tokens)
    if title_score > 0:
        score += title_score * 0.4
        reasons.append(f"title overlap: {title_score:.2f}")

    # 2. Label overlap (weight: 0.3)
    label_score = _label_overlap(issue.labels, epic.labels)
    if label_score > 0:
        score += label_score * 0.3
        reasons.append(f"label overlap: {label_score:.2f}")

    # 3. Description + child issues keyword overlap (weight: 0.2)
    # Include child issue titles as part of the epic's "context" — this helps
    # when the epic itself has a vague title or empty description.
    issue_desc_tokens = _tokenize(issue.description[:500])
    epic_context_tokens = _tokenize(epic.description)
    for child_title in epic.child_issue_titles:
        epic_context_tokens |= _tokenize(child_title)
    desc_score = _keyword_overlap(
        issue_title_tokens | issue_desc_tokens,
        epic_title_tokens | epic_context_tokens,
    )
    if desc_score > 0:
        score += desc_score * 0.2
        reasons.append(f"context overlap: {desc_score:.2f}")

    # 4. Exact important word match bonus (weight: 0.1)
    # If a non-trivial word from the epic title or child issues appears in the issue title
    important_epic_words = {w for w in (epic_title_tokens | epic_context_tokens) if len(w) > 4}
    shared_important = important_epic_words & issue_title_tokens
    if shared_important:
        bonus = min(0.1, len(shared_important) * 0.03)
        score += bonus
        reasons.append(f"key words: {', '.join(sorted(shared_important))}")

    return score, reasons


def score_all_issues(
    issues: list[GitLabIssue],
    epics: list[GitLabEpic],
) -> tuple[list[EpicGroup], list[GitLabIssue]]:
    """Score all issues against all epics.

    Returns:
        - List of EpicGroups (epics with matched issues, sorted by match count desc)
        - List of orphan issues (no match above MEDIUM_CONFIDENCE)
    """
    epic_groups: dict[int, EpicGroup] = {}
    orphans: list[GitLabIssue] = []

    for issue in issues:
        best_score = 0.0
        best_epic: GitLabEpic | None = None
        best_reasons: list[str] = []

        for epic in epics:
            sc, reasons = _score_issue_epic(issue, epic)
            if sc > best_score:
                best_score = sc
                best_epic = epic
                best_reasons = reasons

        if best_epic and best_score >= MEDIUM_CONFIDENCE:
            confidence = "high" if best_score >= HIGH_CONFIDENCE else "medium"
            match = IssueMatch(
                issue=issue,
                score=best_score,
                confidence=confidence,
                reasons=best_reasons,
            )
            if best_epic.iid not in epic_groups:
                epic_groups[best_epic.iid] = EpicGroup(epic=best_epic)
            epic_groups[best_epic.iid].matches.append(match)
        else:
            orphans.append(issue)

    # Sort epic groups by number of matches (descending)
    sorted_groups = sorted(epic_groups.values(), key=lambda g: len(g.matches), reverse=True)
    return sorted_groups, orphans


# ---------------------------------------------------------------------------
# Clustering orphans by theme
# ---------------------------------------------------------------------------


def cluster_orphans(
    orphans: list[GitLabIssue], min_cluster_size: int = 2
) -> tuple[list[ThemeCluster], list[GitLabIssue]]:
    """Group orphan issues by shared keywords into thematic clusters.

    Returns:
        - List of ThemeClusters (groups of related issues)
        - List of isolated issues (not part of any cluster)
    """
    if not orphans:
        return [], []

    # Build token sets per issue
    vocab = _domain_vocab()
    issue_tokens: list[tuple[GitLabIssue, set[str]]] = []
    for issue in orphans:
        tokens = _tokenize(issue.title) | _tokenize(issue.description[:300])
        # Add domain labels as tokens
        for label in issue.labels:
            if label in vocab:
                tokens.add(label.lower())
        issue_tokens.append((issue, tokens))

    # Find shared keywords across issues (appearing in 2+ issues but not in all)
    word_to_issues: dict[str, list[int]] = defaultdict(list)
    for idx, (_, tokens) in enumerate(issue_tokens):
        for token in tokens:
            word_to_issues[token].append(idx)

    # Filter to keywords appearing in 2+ issues but fewer than 80% of all
    max_freq = max(2, int(len(orphans) * 0.8))
    shared_keywords = {
        w: idxs for w, idxs in word_to_issues.items() if min_cluster_size <= len(idxs) < max_freq and len(w) > 3
    }

    # Greedy clustering: pick the most connecting keyword, form a cluster, repeat
    clustered: set[int] = set()
    clusters: list[ThemeCluster] = []

    # Sort keywords by number of connected issues (descending)
    sorted_keywords = sorted(shared_keywords.items(), key=lambda x: len(x[1]), reverse=True)

    for keyword, issue_indices in sorted_keywords:
        # Only consider unclustered issues
        unclustered = [i for i in issue_indices if i not in clustered]
        if len(unclustered) < min_cluster_size:
            continue

        # Find all keywords shared by these unclustered issues
        cluster_issues = [issue_tokens[i][0] for i in unclustered]
        cluster_token_sets = [issue_tokens[i][1] for i in unclustered]

        # Common keywords across at least half the cluster
        common_tokens: list[str] = []
        for token in sorted(cluster_token_sets[0], key=lambda t: -len(t)):
            count = sum(1 for ts in cluster_token_sets if token in ts)
            if count >= len(unclustered) / 2 and token not in _STOP_WORDS and len(token) > 3:
                common_tokens.append(token)
            if len(common_tokens) >= 5:
                break

        # Build theme name from top keywords
        theme = " + ".join(common_tokens[:3]) if common_tokens else keyword

        clusters.append(ThemeCluster(theme=theme, keywords=common_tokens, issues=cluster_issues))
        clustered.update(unclustered)

    isolated = [issue_tokens[i][0] for i in range(len(orphans)) if i not in clustered]
    return clusters, isolated


# ---------------------------------------------------------------------------
# Claude scoring prompt generation
# ---------------------------------------------------------------------------


def build_claude_scoring_prompt(
    orphans: list[GitLabIssue],
    epics: list[GitLabEpic],
) -> str:
    """Build a structured prompt for Claude to score issue-epic matches.

    Returns a JSON-embeddable prompt string that the SKILL.md can feed to
    Claude for semantic analysis.  The expected response format is specified
    in the prompt itself.
    """
    lines: list[str] = []
    lines.append("Tu es un expert en gestion de projet. Analyse les tickets orphelins ci-dessous et")
    lines.append("attribue chacun à l'epic la plus pertinente, ou marque-le comme « aucune ».\n")

    lines.append("## Epics disponibles\n")
    for epic in epics:
        child_summary = ""
        if epic.child_issue_titles:
            child_summary = f" — tickets existants : {', '.join(epic.child_issue_titles[:10])}"
            if len(epic.child_issue_titles) > 10:
                child_summary += f" (+{len(epic.child_issue_titles) - 10} autres)"
        desc = f" — {epic.description[:200]}" if epic.description.strip() else ""
        lines.append(f"- **Epic #{epic.iid}** : {epic.title}{desc}{child_summary}")

    lines.append("\n## Tickets orphelins\n")
    for issue in orphans:
        labels_str = f" [{', '.join(issue.labels)}]" if issue.labels else ""
        lines.append(f"- **#{issue.iid}** (project {issue.project_id}) : {issue.title}{labels_str}")

    lines.append("\n## Format de réponse attendu\n")
    lines.append("Réponds en JSON uniquement, sans markdown autour :")
    lines.append("```")
    lines.append("[")
    lines.append('  {"issue_iid": 301, "issue_project_id": 123, "epic_iid": 42, "confidence": "high",')
    lines.append('   "reason": "Le ticket concerne les notifications, thème central de l\'epic"},')
    lines.append('  {"issue_iid": 78, "issue_project_id": 456, "epic_iid": null, "confidence": "none",')
    lines.append('   "reason": "Aucune epic ne correspond au thème splash screen"}')
    lines.append("]")
    lines.append("```")
    lines.append('Utilise "high", "medium", ou "none" pour la confiance.')

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Fetch epics
# ---------------------------------------------------------------------------


def fetch_open_epics(enrich_children: bool = True) -> list[GitLabEpic]:
    """Fetch all open epics from the Pysae group.

    When *enrich_children* is True (default), fetch the titles of issues
    already linked to each epic.  This dramatically improves matching for
    epics that have a vague title or empty description.
    """
    group_id = resolve_group_id()
    raw_epics = glab_api_paginated(f"groups/{group_id}/epics?state=opened")
    epics = [GitLabEpic.from_api(e) for e in raw_epics]

    if enrich_children:
        for epic in epics:
            child_issues = glab_api_paginated(f"groups/{group_id}/epics/{epic.iid}/issues?per_page=100")
            epic.child_issue_titles = [ci.get("title", "") for ci in child_issues if ci.get("title")]
            print(f"  epic #{epic.iid} : {len(epic.child_issue_titles)} tickets rattachés", file=sys.stderr)

    return epics


def _is_excluded(raw: dict[str, Any]) -> bool:
    """Return True if the issue should be excluded from epic matching."""
    if raw.get("epic_iid") or raw.get("epic"):
        return True
    labels = set(raw.get("labels", []))
    if labels & EXCLUDED_LABELS:
        return True
    # Exclude issues not in workflow (no board column label)
    if not labels & BOARD_LABELS:
        return True
    return False


def fetch_orphan_issues(
    project: str | None = None,
    assignee_username: str | None = None,
    search: list[str] | None = None,
) -> list[GitLabIssue]:
    """Fetch open issues with no parent epic, excluding bugs, support and cancelled."""
    base = (
        f"projects/{project.replace('/', '%2F')}/issues?state=opened"
        if project
        else f"groups/{resolve_group_id()}/issues?state=opened"
    )

    if assignee_username:
        base += f"&assignee_username={assignee_username}"

    if search:
        seen: set[tuple[int, int]] = set()
        issues: list[GitLabIssue] = []
        for term in search:
            for raw in glab_api_paginated(f"{base}&search={term}&in=title,description"):
                if _is_excluded(raw):
                    continue
                issue = GitLabIssue.from_api(raw)
                key = (issue.project_id, issue.iid)
                if key not in seen:
                    seen.add(key)
                    issues.append(issue)
        return issues

    all_raw = glab_api_paginated(base)
    return [GitLabIssue.from_api(raw) for raw in all_raw if not _is_excluded(raw)]


# ---------------------------------------------------------------------------
# Project name resolution
# ---------------------------------------------------------------------------

_project_cache: dict[int, str] = {}


def _resolve_project_name(project_id: int) -> str:
    """Resolve a project ID to a short name (e.g. 'api', 'op')."""
    if project_id in _project_cache:
        return _project_cache[project_id]
    raw = run_glab("api", f"projects/{project_id}", allow_fail=True)
    if raw:
        data = json.loads(raw)
        name: str = data.get("path", str(project_id))
        _project_cache[project_id] = name
        return name
    _project_cache[project_id] = str(project_id)
    return str(project_id)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

app = typer.Typer(help="Find orphan issues and match them to epics")


@app.command(name="scan")
def scan(
    project: CommonProject = None,
    all_projects: CommonAllProjects = False,
    me: CommonMe = False,
    user: CommonUser = None,
    search: CommonSearch = None,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Report only, do not output attach commands"),
    ] = False,
    phase: Annotated[
        int,
        typer.Option("--phase", help="Run only phase 1 (match) or 2 (cluster). Default: both (0)"),
    ] = 0,
    scoring_mode: Annotated[
        str,
        typer.Option(
            "--scoring-mode",
            help="Scoring strategy: 'claude' outputs a prompt for LLM analysis, 'script' uses keyword-based scoring",
        ),
    ] = "claude",
    epic_iid: Annotated[
        int | None,
        typer.Option("--epic", help="Score orphans against a single epic only (by IID)"),
    ] = None,
) -> None:
    """Analyse orphan issues and score them against open epics."""
    filters = CommonIssueFilters(
        project=project,
        all_projects=all_projects,
        me=me,
        user=user,
        search=search,
    )
    resolved_project, assignee = resolve_issue_filters(filters)

    # Fetch all epics (needed for accurate scoring even in single-epic mode)
    print("Récupération des epics ouvertes...", file=sys.stderr)
    epics = fetch_open_epics()
    print(f"  {len(epics)} epics trouvées", file=sys.stderr)

    # Validate --epic target if provided
    if epic_iid:
        target_epic = next((e for e in epics if e.iid == epic_iid), None)
        if not target_epic:
            print(f"Epic #{epic_iid} introuvable ou fermée", file=sys.stderr)
            raise typer.Exit(code=1)
        print(f"  Mode ciblé : epic #{epic_iid} — {target_epic.title}", file=sys.stderr)

    print("Récupération des tickets orphelins (sans epic)...", file=sys.stderr)
    orphans = fetch_orphan_issues(
        project=resolved_project,
        assignee_username=assignee,
        search=search,
    )
    print(f"  {len(orphans)} tickets orphelins trouvés", file=sys.stderr)

    if not orphans:
        output = {
            "phase1": {"epic_groups": [], "total_matched": 0},
            "phase2": {"clusters": [], "isolated": []},
            "total_orphans": 0,
        }
        print(json.dumps(output, indent=2))
        return

    # Claude scoring mode: output a prompt for LLM-based analysis
    if scoring_mode == "claude":
        prompt = build_claude_scoring_prompt(orphans, epics)
        output_data: dict[str, Any] = {
            "mode": "claude-scoring",
            "total_orphans": len(orphans),
            "total_epics": len(epics),
            "prompt": prompt,
        }
        if epic_iid:
            output_data["target_epic"] = epic_iid
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
        return

    # Resolve project names for display
    project_ids = {i.project_id for i in orphans}
    for pid in project_ids:
        _resolve_project_name(pid)

    result: dict[str, Any] = {"total_orphans": len(orphans)}

    # Phase 1: score against existing epics
    if phase in (0, 1):
        print("Phase 1 : scoring des tickets contre les epics existantes...", file=sys.stderr)
        epic_groups, remaining = score_all_issues(orphans, epics)

        # If targeting a single epic, keep only that group
        if epic_iid:
            epic_groups = [g for g in epic_groups if g.epic.iid == epic_iid]
            # All issues NOT matched to the target epic are "remaining" (but we don't cluster them)
            matched_issue_ids = {(m.issue.project_id, m.issue.iid) for g in epic_groups for m in g.matches}
            remaining = [i for i in orphans if (i.project_id, i.iid) not in matched_issue_ids]

        total_matched = sum(len(g.matches) for g in epic_groups)
        print(f"  {total_matched} tickets matchés à {len(epic_groups)} epics", file=sys.stderr)
        print(f"  {len(remaining)} tickets sans correspondance", file=sys.stderr)

        result["phase1"] = {
            "epic_groups": [g.to_dict() for g in epic_groups],
            "total_matched": total_matched,
        }
        if epic_iid:
            result["target_epic"] = epic_iid

        # Enrich with project short names
        for group_data in result["phase1"]["epic_groups"]:
            for issue_data in group_data["issues"]:
                issue_data["project_name"] = _resolve_project_name(issue_data["project_id"])
    else:
        remaining = orphans
        result["phase1"] = {"epic_groups": [], "total_matched": 0}

    # Phase 2: cluster remaining orphans (skip in single-epic mode)
    if phase in (0, 2) and not epic_iid:
        print("Phase 2 : regroupement thématique des tickets restants...", file=sys.stderr)
        clusters, isolated = cluster_orphans(remaining)
        print(f"  {len(clusters)} thèmes détectés, {len(isolated)} tickets isolés", file=sys.stderr)

        result["phase2"] = {
            "clusters": [c.to_dict() for c in clusters],
            "isolated": [
                {
                    "iid": i.iid,
                    "project_id": i.project_id,
                    "project_name": _resolve_project_name(i.project_id),
                    "title": i.title,
                    "web_url": i.web_url,
                    "labels": i.labels,
                }
                for i in isolated
            ],
        }

        # Enrich clusters with project names
        for cluster_data in result["phase2"]["clusters"]:
            for issue_data in cluster_data["issues"]:
                issue_data["project_name"] = _resolve_project_name(issue_data["project_id"])
    else:
        result["phase2"] = {"clusters": [], "isolated": []}

    print(json.dumps(result, indent=2, ensure_ascii=False))


@app.command(name="match-one")
def match_one(
    title: Annotated[str, typer.Option("--title", help="Issue title to match against epics")],
    labels: Annotated[
        list[str] | None,
        typer.Option("--label", help="Issue label (repeatable)"),
    ] = None,
    description: Annotated[
        str,
        typer.Option("--description", help="Issue description (first 500 chars used)"),
    ] = "",
    top: Annotated[
        int,
        typer.Option("--top", help="Number of top matches to return"),
    ] = 5,
) -> None:
    """Score a single issue against all open epics and return the best matches."""
    print("Récupération des epics ouvertes...", file=sys.stderr)
    epics = fetch_open_epics(enrich_children=True)
    print(f"  {len(epics)} epics trouvées", file=sys.stderr)

    issue = GitLabIssue(
        title=title,
        labels=labels or [],
        description=description[:500],
    )

    scored: list[dict[str, Any]] = []
    for epic in epics:
        sc, reasons = _score_issue_epic(issue, epic)
        if sc > 0:
            scored.append(
                {
                    "epic_iid": epic.iid,
                    "epic_title": epic.title,
                    "score": round(sc, 3),
                    "confidence": "high" if sc >= HIGH_CONFIDENCE else ("medium" if sc >= MEDIUM_CONFIDENCE else "low"),
                    "reasons": reasons,
                }
            )

    scored.sort(key=lambda x: -x["score"])
    result = {"matches": scored[:top], "total_epics": len(epics)}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
