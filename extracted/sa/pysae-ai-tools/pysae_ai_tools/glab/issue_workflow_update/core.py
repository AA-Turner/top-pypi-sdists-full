"""Pure decision logic for ``glab issue-workflow-update`` (no I/O — unit-testable).

A ticket's board status is reconciled with its merge requests:

0. **Cancelled label** → a ticket carrying a cancelled label (e.g. ``ANNULE``)
   is *closed*, whatever its MRs say. Highest precedence.
1. **Open MR** → the ticket is bumped to at least ``workflow::In progress``
   (``Under review`` when that open MR is already approved).
2. **All merged, none open** → the work is done. If every merged MR is already
   **shipped to prod** (its merge commit is an ancestor of the prod branch) the
   ticket is *closed*; otherwise it is bumped to at least ``workflow::To deploy``.

"Shipped" is decided by commit ancestry, not by the changelog: the caller marks
each merged MR ``in_prod`` and this module only reads that flag.
"""

import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from ...common.references.gitlab_labels import BOARD_LABEL_ORDER, BoardLabel

TO_DEPLOY: str = str(BoardLabel.TO_DEPLOY)
UNDER_REVIEW: str = str(BoardLabel.UNDER_REVIEW)
IN_PROGRESS: str = str(BoardLabel.IN_PROGRESS)
_BOARD_LABELS: frozenset[str] = frozenset(str(b) for b in BoardLabel)
# Position of each board label in the workflow (least → most advanced). A
# ticket with no board label ranks below everything (-1).
_BOARD_RANK: dict[str, int] = {str(b): i for i, b in enumerate(BOARD_LABEL_ORDER)}

_SEMVER = re.compile(r"^v?\d+\.\d+\.\d+$")


class Action(StrEnum):
    CLOSE = "close"
    REOPEN = "reopen"
    SET_TO_DEPLOY = "set_to_deploy"
    SET_UNDER_REVIEW = "set_under_review"
    SET_IN_PROGRESS = "set_in_progress"
    NOOP = "noop"


@dataclass
class MrSummary:
    """Aggregate state of a ticket's related merge requests."""

    total: int = 0
    has_merged: bool = False
    has_open: bool = False
    has_open_approved: bool = False  # an open MR that has at least one approval
    has_merged_not_in_prod: bool = False  # a merged MR whose commit is not (yet) in prod

    @property
    def all_merged_in_prod(self) -> bool:
        """Every merged MR is shipped to prod (and there is at least one)."""
        return self.has_merged and not self.has_merged_not_in_prod

    @classmethod
    def from_states(cls, states: list[str]) -> Self:
        """Build from MR states only (no approval nor prod info — merged MRs count as not-in-prod)."""
        return cls.from_mrs([(s, False, False) for s in states])

    @classmethod
    def from_mrs(cls, mrs: list[tuple[str, bool, bool]]) -> Self:
        """Build from ``(state, approved, in_prod)`` triples."""
        return cls(
            total=len(mrs),
            has_merged=any(state == "merged" for state, _, _ in mrs),
            has_open=any(state == "opened" for state, _, _ in mrs),
            has_open_approved=any(state == "opened" and approved for state, approved, _ in mrs),
            has_merged_not_in_prod=any(state == "merged" and not in_prod for state, _, in_prod in mrs),
        )


@dataclass
class RelatedMR:
    """A merge request linked to an issue (subset of the GitLab payload)."""

    iid: int
    state: str
    source_branch: str
    project_id: str
    merge_commit: str = ""  # on-target commit (merge or squash), used for the prod-ancestry check
    target_branch: str = ""


def branch_targets_issue(source_branch: str, iid: int) -> bool:
    """Whether a branch name encodes the issue IID (``<type>/<iid>-…``, ``ai-<iid>``).

    The IID must appear as a whole segment bounded by ``/`` or ``-`` so ``2648``
    does not match ``26480``.
    """
    return re.search(rf"(?:^|[/-]){iid}(?:[/-]|$)", source_branch) is not None


def select_fixing_mrs(candidates: list[RelatedMR], iid: int) -> list[RelatedMR]:
    """Pick the MR(s) that address issue ``iid`` among candidate MRs.

    Candidates are GitLab's ``closed_by`` MRs in priority (the authoritative
    ``Closes #N`` link), falling back to the issue's related MRs only when
    ``closed_by`` is empty. With 0 or 1 candidate there is nothing to
    disambiguate. With several, the right one is the MR whose **branch** encodes
    the IID (``<type>/<iid>-…``); if none does, all candidates are kept. The MR
    description is never parsed.
    """
    if len(candidates) <= 1:
        return list(candidates)
    branch_matched = [m for m in candidates if branch_targets_issue(m.source_branch, iid)]
    return branch_matched or list(candidates)


@dataclass
class Decision:
    iid: int
    title: str
    current_board: str
    action: Action
    reason: str
    target: str = ""  # board column to set after a REOPEN


def apply_mine_by_default(*, anyone: bool, has_assignee: bool, has_author: bool) -> bool:
    """Whether the implicit "mine" filter applies.

    "Mine" is the default scope; it is dropped only when the user opts out with
    ``--anyone`` or narrows to a specific ``--assignee`` / ``--author`` (targeting
    someone explicitly is incompatible with an implicit "only me").
    """
    return not (anyone or has_assignee or has_author)


def issue_passes_filter(
    author: str,
    assignees: list[str],
    *,
    mine_user: str | None = None,
    assignee_user: str | None = None,
    author_user: str | None = None,
) -> bool:
    """Whether an issue survives the assignment filters (all applied as AND).

    ``mine_user`` matches the compound rule "mine": the ticket is assigned to me,
    **or** I authored it and nobody else is assigned. ``assignee_user`` keeps
    tickets that user is assigned to; ``author_user`` keeps tickets that user
    authored. A ``None`` filter is not applied; all-``None`` passes everything.
    """
    if mine_user is not None:
        is_assigned = mine_user in assignees
        owned_solo = author == mine_user and not [a for a in assignees if a != mine_user]
        if not (is_assigned or owned_solo):
            return False
    if assignee_user is not None and assignee_user not in assignees:
        return False
    if author_user is not None and author != author_user:
        return False
    return True


def is_semver_tag(tag: str) -> bool:
    return bool(_SEMVER.match(tag.strip()))


def current_board_label(labels: list[str]) -> str:
    """Return the issue's board column label, or '' if it has none."""
    return next((lbl for lbl in labels if lbl in _BOARD_LABELS), "")


def board_rank(label: str) -> int:
    """Position of a board label in the workflow; '' (no column) ranks -1."""
    return _BOARD_RANK.get(label, -1)


def issue_in_board_columns(labels: list[str], columns: frozenset[str]) -> bool:
    """Whether the issue sits in one of ``columns``. Empty ``columns`` = no restriction."""
    return not columns or bool(set(labels) & columns)


def latest_semver(tags: list[str]) -> str | None:
    """Return the highest semver tag from ``tags`` (already filtered or not).

    ``tags`` is expected pre-sorted descending by the caller (git
    ``--sort=-version:refname``); this just picks the first semver-shaped one.
    """
    for tag in tags:
        if is_semver_tag(tag):
            return tag.strip()
    return None


def decide(
    iid: int,
    title: str,
    labels: list[str],
    mr: MrSummary,
    cancelled_labels: frozenset[str] = frozenset(),
    has_deploy: bool = True,
) -> Decision:
    """Compute the action for one issue.

    Rule precedence: cancelled label (close) → open MR (at least In progress /
    Under review) → all merged, then depending on the project's deployment:

    - ``has_deploy`` is ``False`` (no ``deploy/prod`` branch → no deployment step,
      so ``To deploy`` is meaningless): all merged, none open → **close**.
    - ``has_deploy`` is ``True``: shipped to prod → close; not yet in prod → To deploy.
    """
    board = current_board_label(labels)
    if cancelled_labels and cancelled_labels.intersection(labels):
        return Decision(iid, title, board, Action.CLOSE, "ticket annulé (label) → fermeture")
    if mr.total and mr.has_merged and not mr.has_open:
        if not has_deploy:
            return Decision(iid, title, board, Action.CLOSE, "MR mergée, projet sans étape « To deploy » → fermeture")
        if mr.all_merged_in_prod:
            return Decision(iid, title, board, Action.CLOSE, "merge commit déployé en prod")
        if board == TO_DEPLOY:
            return Decision(iid, title, board, Action.NOOP, "déjà en « To deploy »")
        return Decision(iid, title, board, Action.SET_TO_DEPLOY, "MR mergée, pas encore en prod")
    if mr.has_open:
        if mr.has_open_approved:
            target, action = UNDER_REVIEW, Action.SET_UNDER_REVIEW
        else:
            target, action = IN_PROGRESS, Action.SET_IN_PROGRESS
        if board == target:
            return Decision(iid, title, board, Action.NOOP, f"MR ouverte, déjà « {target} »")
        # An open MR means the work is not done: a ticket parked in To deploy (or
        # beyond « Under review ») must be pulled back to its work column.
        if board_rank(board) > board_rank(UNDER_REVIEW):
            return Decision(iid, title, board, action, f"MR ouverte alors qu'en « {board} » → retour « {target} »")
        if board_rank(board) < board_rank(target):
            reason = f"MR {'approuvée ' if action == Action.SET_UNDER_REVIEW else ''}ouverte → « {target} »"
            return Decision(iid, title, board, action, reason)
        return Decision(iid, title, board, Action.NOOP, f"MR ouverte, déjà au moins « {target} »")
    return Decision(iid, title, board, Action.NOOP, "aucune condition remplie")


def should_reopen(mr: MrSummary, has_deploy: bool = True) -> bool:
    """Whether a *closed* ticket looks closed by mistake.

    It does when work is clearly not finished: an MR is still open, or — on a
    project that deploys — a merged MR has not reached prod. On a project with no
    ``deploy/prod`` branch, a merged MR *is* the finished state, so only a still
    open MR warrants reopening. A ticket with no MR, or only abandoned MRs, is
    left closed.
    """
    if mr.has_open:
        return True
    if not has_deploy:
        return False
    return mr.has_merged_not_in_prod


def reopen_target(mr: MrSummary, has_deploy: bool = True) -> str:
    """Board column a reopened ticket should land in, from its MR state."""
    if mr.has_open:
        return UNDER_REVIEW if mr.has_open_approved else IN_PROGRESS
    return TO_DEPLOY


def decide_closed(iid: int, title: str, labels: list[str], mr: MrSummary, has_deploy: bool = True) -> Decision:
    """Compute the action for a *closed* issue: REOPEN it, or leave it (NOOP)."""
    board = current_board_label(labels)
    if not should_reopen(mr, has_deploy):
        return Decision(iid, title, board, Action.NOOP, "fermeture correcte")
    target = reopen_target(mr)
    why = "MR ouverte" if mr.has_open else "MR mergée pas encore en prod"
    return Decision(
        iid, title, board, Action.REOPEN, f"fermé à tort ({why}) → réouverture en « {target} »", target=target
    )
