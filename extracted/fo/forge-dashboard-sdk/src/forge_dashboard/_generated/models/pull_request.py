from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.ci_status import CIStatus
from ..models.forge import Forge
from ..models.merge_status import MergeStatus
from ..models.pull_request_kind import PullRequestKind
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.allowed_action import AllowedAction
  from ..models.auto_merge_status import AutoMergeStatus
  from ..models.auto_update import AutoUpdate
  from ..models.bot_request import BotRequest
  from ..models.check_counts import CheckCounts
  from ..models.closing_issue import ClosingIssue
  from ..models.label import Label
  from ..models.mentioned_issue import MentionedIssue
  from ..models.pull_request_status import PullRequestStatus
  from ..models.queued_action import QueuedAction
  from ..models.review_state import ReviewState
  from ..models.stack_position import StackPosition
  from ..models.stack_ref import StackRef
  from ..models.update_request import UpdateRequest





T = TypeVar("T", bound="PullRequest")



@_attrs_define
class PullRequest:
    """ 
        Attributes:
            forge (Forge):
            repo (str): Owner-qualified repository name.
            number (int):
            title (str):
            url (str): The real pull request URL on its own forge.
            author (str):
            author_avatar_url (str): The forge's own avatar URL for the author, passed through unchanged and never proxied.
                Empty when the forge supplies none, such as a deleted account.
            author_url (str): The author's profile page on the forge, built by the server from the forge's own web address,
                so a client needs no rule per forge. A GitHub bot links to its app page. Empty when there is nothing to link to,
                such as a deleted account.
            draft (bool):
            labels (list[Label]):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            ci (CIStatus): The combined result across every check reported against the pull
                request's head commit. "none" means neither forge reported any
                check at all, not that one failed.

                This is the server's answer, and the server's rules read it: what a
                pull request may do, auto-merge, the quick filters, the navigation
                counts and the CI poll. The page draws it for a row it has no job
                facts for. For a row it has them for (the rows in view on the live
                stream), the page folds the jobs itself, so the pill it draws can
                differ from this field until the next refresh. A run that was only
                cancelled reads as cancelled in that fold; GitHub's rollup says
                `failure` and Forgejo's says `none` or `success` here.
            checks (CheckCounts): How many checks are in each state, so a client can say how far a
                pipeline is without opening it. It is on every pull request and on
                every default branch, for a passed, a failed and a running pipeline
                alike. The server tallies them from what it already reads to work out
                the overall state, so they cost no request. Always present, all zero
                when there are no checks.

                `waiting` is a check that has not started: queued, or pending where the
                forge doesn't tell queued from running. A failed pipeline can still have
                checks running or waiting, and says so. A pull request's counts agree
                with its `ci`: one whose `ci` is `pending` has `failed` at 0, and one
                whose `ci` is `success` has nothing running, waiting or failed. Two
                kinds of run are therefore in none of the four, as long as something
                else explains the state. A run held for approval: on a pull request
                `awaitingWorkflowApproval` says that. A cancelled run: a push or a
                concurrency group superseded it, and the overall state does not read it
                as a failure while others still run. When cancelled runs (and, on a
                branch, held ones) are the only reason a pipeline reads as failed, they
                count as `failed` (a held run first, where both are there), so a failed
                pipeline always has a failed count on GitHub. A branch whose status is
                `cancelled` has `failed` at 0. A timed-out or stale check counts as `failed`, a skipped,
                neutral or bare completed one as `passed`, on Forgejo too.

                `skipped` is a newer field and says how many of the `passed` checks
                were skipped. It never exceeds `passed`: it is inside `passed`, not
                beside it, so `passed` still counts every check that needs nothing more
                and the four states still add up to the checks the pipeline lists, bar
                the blocked jobs of a failed Forgejo run described below. The
                server always sends it, which is why it is required; a client that may
                talk to an older server may read a missing one as zero. A neutral or bare
                completed check is passed without being skipped. A client that draws the
                two side by side must subtract `skipped` from `passed` for the passed figure, or a skipped check is
                counted twice, and a pipeline where every passed check was skipped can
                read as skipped.

                On GitHub the counts come from the same rollup as the overall state,
                for a pull request and a branch alike; on Forgejo a pull request counts
                the statuses of the combined commit status, which only say pending, and
                takes the running ones out of the pending count by reading the jobs of
                the commit's runs that are still going. When a run has failed, a
                pending status of a job in a run that has failed is no wait: its
                needs failed, so Forgejo leaves it blocked and nothing will start it,
                and it is in none of the four. A default branch holds to the same: it
                counts the jobs of the workflow runs of the newest commit that has one,
                where a running job is `running`, a queued one `waiting`, and a blocked
                one `waiting` unless its run has failed, when it is in none of the four. A run
                whose jobs can't be read counts as one check by its own status. Forgejo
                answers one page of those statuses, and when its total says there are
                more than the page holds a pull request's counts are all zero rather
                than an undercount. When GitHub's rollup of a pull request is of an
                earlier commit than the head (a push still being processed), the counts
                are zero too. GitHub's unauthenticated fallback has no such counts, so
                there they are all zero.
            merge_status (MergeStatus): A pull request's mergeable/blocked state, as coarse as every forge
                this service talks to can agree on. "blocked" covers anything
                stopping a merge that isn't confirmed to be a real conflict —
                including Forgejo's own mergeable flag reporting false, since its
                server computes that asynchronously and can report it stale.
                "unstable" is GitHub's UNSTABLE: the pull request can be merged, but
                a check that branch protection doesn't require is failing or still
                running. Merge stays available.
                "unknown" covers both a forge that hasn't determined this yet and
                this service being unable to determine it.
            behind (bool): Whether this pull request's base branch has moved since its
                merge-base was computed. Deliberately its own field rather
                than a mergeStatus value: on Forgejo a pull request can be
                both mergeable and behind at once (its mergeable flag doesn't
                get recomputed just because the base moved), so folding this
                into mergeStatus would force picking one and losing the
                other.
            head_sha (str): The commit the pull request's head branch points at. A bot's
                rebase moves it, which shows the bot acted even when the pull
                request is still reported behind, or wasn't behind to begin
                with. Empty when the forge didn't say. Always present.
            kind (PullRequestKind): What sort of pull request this is, decided by the server so no
                client keeps its own copy of the rule. `release`: release-please's,
                by its `autorelease:` label (a person opens these, so the label is
                the main signal, and it wins over any bot author), or, when the
                label is missing because release-please failed before applying it,
                by its head branch: `release-please--branches--<base branch>`
                (with `--components--<name>` after it for a repo that releases
                several components) in the same repository and aimed at that base
                branch. A fork's pull request is never a release. `dependency`:
                opened by Dependabot or Renovate, in either spelling of the login
                (the bare slug GraphQL gives, or REST's `[bot]` form), on either
                forge. `regular`: everything else. Always present.
            base_branch (str): The branch the pull request targets. Empty when the forge didn't
                say.
            head_branch (str): The branch the pull request comes from. Empty when the forge
                didn't say.
            cross_repository (bool): True when the head branch lives in another repository (a fork).
                A fork pull request is never part of a stack.
            stack (None | StackPosition): Where this pull request sits in a stack of pull requests, or
                null when it is in none. A stack is worked out on the server:
                pull request B is stacked on A when B's base branch is A's head
                branch, in the same repository on the same forge, and neither is
                a fork. A branch with several open pull requests takes the one
                with the lowest number as parent, and a loop of branches is
                treated as no stack. The snapshot holds open pull requests
                only, so a base branch that no open pull request owns (a parent
                that already merged and was not retargeted) is not flagged.
            stacked_on (None | StackRef): The open pull request this one is stacked on, or null when its
                base is not another open pull request's head.
            stack_children (list[int]): The numbers of the open pull requests stacked directly on this
                one. Always a list, empty when none.
            requested_reviewer_logins (list[str]): The logins of the users asked to review this pull request, on
                both forges. A team request has no login and is left out.
                Always present, and empty when nobody was asked. Costs no
                extra request: GitHub returns it with the reviewRequests count
                already queried, Forgejo with the pull request itself.
            awaiting_workflow_approval (bool): True when GitHub is holding a workflow run on the head commit
                until someone approves it: its rollup counts a check run
                as ACTION_REQUIRED. Those runs also keep `ci` at failure when
                nothing else is running, so a client reads this to say "waiting
                for approval" rather than "check failed". It can be true while
                `ci` is pending (other runs are going) or failing for another
                reason too. Always present; false on Forgejo, which has no
                such state.
            review_comments (int): How many review comments the pull request has, the ones on a
                line of code. Ordinary conversation comments are counted apart,
                in `conversationComments`. Always present, and 0 when
                there are none or the forge can't say (a Forgejo draft or failed
                reviews call, GitHub's unauthenticated fallback). On GitHub it is read from
                the review threads in the pull request query, first 30 threads; on Forgejo it is the sum
                of each review's comment count, from the reviews call that already
                feeds `review`, so a draft (which makes no such call) reports 0.
            conversation_comments (int): How many ordinary comments the pull request's conversation has,
                apart from `reviewComments`. A review's own body is not a comment.
                Always present, and 0 when there are none. On GitHub it comes from
                the pull request query, on Forgejo from the pull request itself, so
                neither costs a request.
            closes_issues (list[ClosingIssue]): The issues the pull request will close when it merges. Always
                present, and empty when there are none. On GitHub it is the
                forge's own list of closing references, read in the pull request
                query; GitHub's unauthenticated fallback (no token) has no such
                field, so it lists none. Forgejo has none either, so the server
                reads the closing keywords (close, closes, closed, fix, fixes,
                fixed, resolve, resolves, resolved) in the description the way
                Forgejo does: a keyword, an optional colon, one space, then `#NUMBER`
                or `owner/repo#NUMBER`, and each keyword covers the one reference
                right after it. Code, HTML comments and a number that runs into
                letters count for nothing. The `owner/repo#NUMBER` form follows
                Forgejo's source and has not been tried on a live instance. Only a
                pull request aimed at its repo's default branch closes anything,
                so one aimed elsewhere always lists none.
            mentions_issues (list[MentionedIssue]): The issues and pull requests the title or description mentions
                without closing them, in order of first appearance and without
                repeats, at most 20. Always present, and empty when there are none.
                A mention is what GitHub and Forgejo both link: `#NUMBER`,
                `owner/repo#NUMBER`, or the address of an issue or pull request
                page on the forge, and on GitHub also `GH-NUMBER`. It has to stand
                alone: `abc#1`, `&#1` and `#1abc` are not mentions, while emphasis
                and table markup around it (`**#1**`, `_#1_`, `|#1|`) is fine. Code,
                HTML comments and the text of a link, Markdown or HTML anchor,
                count for nothing, and a link counts only by its target, when that
                is a page on the forge. Only the first 64 KiB of the description is
                read, cut at a space (a Unicode space too; with none, at the last
                comma or semicolon outside brackets; an anchor still open within 1 KiB of the cut
                loses the text after its tag), and the first 100 references in it. A reference
                in a quotation still counts, and the pull request's own number
                does not. What the pull request actually
                closes is left out, even when the text also mentions it, and the
                cap applies after that. Which references close depends on the
                branch the pull request aims at, so a closing keyword on a pull
                request that does not target the default branch is a mention. Only
                the description closes, so a keyword in the title is a mention.
                Comments, reviews and commit messages are not read. The server
                reads the text on both forges, with or without a GitHub token, so a
                client needs no rule of its own.
            unresolved_threads (int | None): How many review threads are still open, or null when the forge
                can't say. GitHub reports it from its review threads, except in the
                unauthenticated fallback, which has none. Forgejo reports no
                resolved state on a review without a call per review, so it is null
                there and a client shows the comment count without an open state.
            review_requested_from_me (bool): True when this open, non-draft pull request asks the signed-in
                user to review it, matched without regard to case against the
                username saved in Settings for its forge. False when no
                username is saved for that forge. Always present.
            empty (bool): Whether merging this pull request would produce an empty
                commit — its content already landed on the base branch some
                other way. False whenever this service can't tell (the
                unauthenticated GitHub REST fallback, or a Forgejo instance
                old enough not to report additions/deletions/changed_files on
                its list endpoint), never a false positive: a pull request
                this never confirms empty just renders as it always has.
            allowed_actions (list[AllowedAction]): The actions this pull request offers, worked out on the server
                from its own fields, so a client needs no copy of the rules. An
                action that doesn't apply (Update branch on a pull request that
                isn't behind, a Dependabot command on a Renovate pull request)
                is absent, not listed as blocked. Always present; `close` is
                always in it. Live state is the client's: a rate-limited or
                unreachable forge, a missing token and an action already in
                flight can still stop an offered action.
            status (None | PullRequestStatus): The one reason this pull request is waiting on something or can't
                be merged, for a fixed place on its row: a check still
                running, a conflict, a draft, a parent it is stacked on, or, for
                an empty pull request, that there is nothing to merge. `code`,
                `message` and `next` are the same as on `allowedActions[].blocked`,
                and for a pull request that waiting or fixing can unlock they
                repeat Merge's blocked reason. An empty pull request offers no
                `merge` (only `close`), so this is where its reason lives. Null
                when nothing holds the pull request back. Always present.
            ready_to_merge (bool): True when the pull request is mergeable, its CI is green and it
                isn't a draft: what the Ready quick filter lists. Always
                present. A pull request with no checks isn't ready.
            failing_ci (bool): True when CI is failing and not only because a workflow run is
                held for approval: what the Failing CI quick filter lists, and
                what the menu pill's Failed number counts. Always present.
            needs_review (bool): True when a review is outstanding: the forge requires one, or a
                reviewer was asked and hasn't answered, and the pull request
                isn't a draft. Unreviewed with nobody asked, approved, changes
                requested and an unknown review state are all false. Always
                present.
            auto_update (AutoUpdate): Whether the dashboard brings this pull request's branch up to date by
                itself: the pull request's own choice when it has one
                (`POST /api/v1/pull-requests/auto-update`), else its repo's
                auto-update setting. Always present.
            bot_request (BotRequest | None | Unset): A Dependabot or Renovate rebase asked for through this app and not
                settled yet, or null. The server keeps it, so a reload during the
                wait still shows it, and moves it along on every snapshot that
                came from a fetch started after the request. Held in memory per
                account: a server restart forgets it.
            update_request (None | Unset | UpdateRequest): An Update branch the forge accepted and that no snapshot has
                shown
                landing yet, or null. The server keeps it, so a reload during the
                wait still shows it. It is dropped once a snapshot from a fetch
                started after the request shows the pull request no longer
                behind, or when the pull request is gone. Held in memory per
                account: a server restart forgets it.
            queued (None | QueuedAction | Unset): A safe action this user queued on this pull request that is still
                waiting for its forge's rate limit to reset, or null. The row can
                say "Update branch queued for 14:32" from `runAt` and offer
                Cancel with `id`. A final outcome is not here: it is in the
                dashboard's `queuedActions`.
            auto_merge_enabled (bool | Unset): Whether auto-merge is currently scheduled on this pull request.
                On Forgejo it is true when the signed-in user armed it in this
                app, which holds the intent itself, or when a merge is scheduled
                on Forgejo (read from the issue timeline's `pull_scheduled_merge`
                and `pull_cancel_scheduled_merge` events, for open non-draft pull
                requests, a bounded number per refresh). It is false once the
                timeline shows no schedule. Omitted when it hasn't been read yet
                or the read failed, since this service then doesn't know.
            auto_merge_held_by (str | Unset): Who holds the auto-merge, so a client can word it right. Present
                only when `autoMergeEnabled` is true. `dashboard` means this app
                holds a stored intent and performs the merge itself (Forgejo).
                `forge` means the merge is scheduled on the forge: Forgejo's own
                scheduled merge, or GitHub's auto-merge. When both exist on
                Forgejo it is `dashboard`, since this app's loop merges and
                Cancel clears both. Omitted means unknown: a client must not
                guess it from other fields, and should treat a value it doesn't
                know like an omitted one.
            auto_merge_allowed (bool | Unset): Whether GitHub will accept an "Enable auto-merge" request for
                this pull request from the signed-in viewer, read from the
                GraphQL `PullRequest.viewerCanEnableAutoMerge` field. GitHub
                decides this per viewer and per pull request: auto-merge needs
                something on the base branch to wait for (required checks or
                reviews from a branch protection rule or ruleset), so a stacked
                pull request on an unprotected base reports false even when the
                repository allows auto-merge. Omitted when unknown (the
                unauthenticated REST fallback, and Forgejo), never false in
                that case, so clients keep today's behaviour.
            review (ReviewState | Unset): Where a pull request stands on code review. The whole object is
                omitted when the owning forge couldn't report it (a Forgejo
                reviews call that failed, a draft Forgejo pull request this
                service doesn't spend a call on), so a missing "review" means
                "unknown" and never "nobody reviewed it."

                GitHub: read from fields on the existing GraphQL query
                (reviewDecision, reviewRequests, latestReviews), so it adds no
                per-pull-request requests. Forgejo: requestedReviewers comes free
                on the pull request list, but approvals and the decision need one
                reviews call per open, non-draft pull request, cached until that
                pull request's updatedAt changes.
            auto_merge (AutoMergeStatus | Unset): Where an armed pull request stands, so the row can say why
                auto-merge is waiting or stopped in words and not by colour. Present
                while auto-merge is armed on it: on Forgejo the signed-in user's
                intent held by this app, on GitHub the forge's own auto-merge.
                Also present for ten minutes after this app cancelled an armed
                auto-merge because the pull request went empty (its branch landed on
                the base some other way): `stopped`, code `already_up_to_date` and the
                message "Auto-merge was cancelled: there is nothing left to merge."
                Auto-merge is off by then, so this is the only place the reason lives.
            hidden (bool | Unset): True on a pull request the user hid. Only present when the request
                set `includeHidden=true`: without it a hidden pull request isn't
                in the list at all.
            hidden_until (datetime.datetime | Unset): When a hide for a number of days ends. Absent for a pull request
                hidden until it is restored, and for one that isn't hidden.
     """

    forge: Forge
    repo: str
    number: int
    title: str
    url: str
    author: str
    author_avatar_url: str
    author_url: str
    draft: bool
    labels: list[Label]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    ci: CIStatus
    checks: CheckCounts
    merge_status: MergeStatus
    behind: bool
    head_sha: str
    kind: PullRequestKind
    base_branch: str
    head_branch: str
    cross_repository: bool
    stack: None | StackPosition
    stacked_on: None | StackRef
    stack_children: list[int]
    requested_reviewer_logins: list[str]
    awaiting_workflow_approval: bool
    review_comments: int
    conversation_comments: int
    closes_issues: list[ClosingIssue]
    mentions_issues: list[MentionedIssue]
    unresolved_threads: int | None
    review_requested_from_me: bool
    empty: bool
    allowed_actions: list[AllowedAction]
    status: None | PullRequestStatus
    ready_to_merge: bool
    failing_ci: bool
    needs_review: bool
    auto_update: AutoUpdate
    bot_request: BotRequest | None | Unset = UNSET
    update_request: None | Unset | UpdateRequest = UNSET
    queued: None | QueuedAction | Unset = UNSET
    auto_merge_enabled: bool | Unset = UNSET
    auto_merge_held_by: str | Unset = UNSET
    auto_merge_allowed: bool | Unset = UNSET
    review: ReviewState | Unset = UNSET
    auto_merge: AutoMergeStatus | Unset = UNSET
    hidden: bool | Unset = UNSET
    hidden_until: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.allowed_action import AllowedAction # noqa: PLC0415
        from ..models.auto_merge_status import AutoMergeStatus # noqa: PLC0415
        from ..models.auto_update import AutoUpdate # noqa: PLC0415
        from ..models.bot_request import BotRequest # noqa: PLC0415
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        from ..models.closing_issue import ClosingIssue # noqa: PLC0415
        from ..models.label import Label # noqa: PLC0415
        from ..models.mentioned_issue import MentionedIssue # noqa: PLC0415
        from ..models.pull_request_status import PullRequestStatus # noqa: PLC0415
        from ..models.queued_action import QueuedAction # noqa: PLC0415
        from ..models.review_state import ReviewState # noqa: PLC0415
        from ..models.stack_position import StackPosition # noqa: PLC0415
        from ..models.stack_ref import StackRef # noqa: PLC0415
        from ..models.update_request import UpdateRequest # noqa: PLC0415
        forge = self.forge.value

        repo = self.repo

        number = self.number

        title = self.title

        url = self.url

        author = self.author

        author_avatar_url = self.author_avatar_url

        author_url = self.author_url

        draft = self.draft

        labels = []
        for labels_item_data in self.labels:
            labels_item = labels_item_data.to_dict()
            labels.append(labels_item)



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        ci = self.ci.value

        checks = self.checks.to_dict()

        merge_status = self.merge_status.value

        behind = self.behind

        head_sha = self.head_sha

        kind = self.kind.value

        base_branch = self.base_branch

        head_branch = self.head_branch

        cross_repository = self.cross_repository

        stack: dict[str, Any] | None
        if isinstance(self.stack, StackPosition):
            stack = self.stack.to_dict()
        else:
            stack = self.stack

        stacked_on: dict[str, Any] | None
        if isinstance(self.stacked_on, StackRef):
            stacked_on = self.stacked_on.to_dict()
        else:
            stacked_on = self.stacked_on

        stack_children = self.stack_children



        requested_reviewer_logins = self.requested_reviewer_logins



        awaiting_workflow_approval = self.awaiting_workflow_approval

        review_comments = self.review_comments

        conversation_comments = self.conversation_comments

        closes_issues = []
        for closes_issues_item_data in self.closes_issues:
            closes_issues_item = closes_issues_item_data.to_dict()
            closes_issues.append(closes_issues_item)



        mentions_issues = []
        for mentions_issues_item_data in self.mentions_issues:
            mentions_issues_item = mentions_issues_item_data.to_dict()
            mentions_issues.append(mentions_issues_item)



        unresolved_threads: int | None
        unresolved_threads = self.unresolved_threads

        review_requested_from_me = self.review_requested_from_me

        empty = self.empty

        allowed_actions = []
        for allowed_actions_item_data in self.allowed_actions:
            allowed_actions_item = allowed_actions_item_data.to_dict()
            allowed_actions.append(allowed_actions_item)



        status: dict[str, Any] | None
        if isinstance(self.status, PullRequestStatus):
            status = self.status.to_dict()
        else:
            status = self.status

        ready_to_merge = self.ready_to_merge

        failing_ci = self.failing_ci

        needs_review = self.needs_review

        auto_update = self.auto_update.to_dict()

        bot_request: dict[str, Any] | None | Unset
        if isinstance(self.bot_request, Unset):
            bot_request = UNSET
        elif isinstance(self.bot_request, BotRequest):
            bot_request = self.bot_request.to_dict()
        else:
            bot_request = self.bot_request

        update_request: dict[str, Any] | None | Unset
        if isinstance(self.update_request, Unset):
            update_request = UNSET
        elif isinstance(self.update_request, UpdateRequest):
            update_request = self.update_request.to_dict()
        else:
            update_request = self.update_request

        queued: dict[str, Any] | None | Unset
        if isinstance(self.queued, Unset):
            queued = UNSET
        elif isinstance(self.queued, QueuedAction):
            queued = self.queued.to_dict()
        else:
            queued = self.queued

        auto_merge_enabled = self.auto_merge_enabled

        auto_merge_held_by = self.auto_merge_held_by

        auto_merge_allowed = self.auto_merge_allowed

        review: dict[str, Any] | Unset = UNSET
        if not isinstance(self.review, Unset):
            review = self.review.to_dict()

        auto_merge: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_merge, Unset):
            auto_merge = self.auto_merge.to_dict()

        hidden = self.hidden

        hidden_until: str | Unset = UNSET
        if not isinstance(self.hidden_until, Unset):
            hidden_until = self.hidden_until.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "repo": repo,
            "number": number,
            "title": title,
            "url": url,
            "author": author,
            "authorAvatarUrl": author_avatar_url,
            "authorUrl": author_url,
            "draft": draft,
            "labels": labels,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "ci": ci,
            "checks": checks,
            "mergeStatus": merge_status,
            "behind": behind,
            "headSha": head_sha,
            "kind": kind,
            "baseBranch": base_branch,
            "headBranch": head_branch,
            "crossRepository": cross_repository,
            "stack": stack,
            "stackedOn": stacked_on,
            "stackChildren": stack_children,
            "requestedReviewerLogins": requested_reviewer_logins,
            "awaitingWorkflowApproval": awaiting_workflow_approval,
            "reviewComments": review_comments,
            "conversationComments": conversation_comments,
            "closesIssues": closes_issues,
            "mentionsIssues": mentions_issues,
            "unresolvedThreads": unresolved_threads,
            "reviewRequestedFromMe": review_requested_from_me,
            "empty": empty,
            "allowedActions": allowed_actions,
            "status": status,
            "readyToMerge": ready_to_merge,
            "failingCi": failing_ci,
            "needsReview": needs_review,
            "autoUpdate": auto_update,
        })
        if bot_request is not UNSET:
            field_dict["botRequest"] = bot_request
        if update_request is not UNSET:
            field_dict["updateRequest"] = update_request
        if queued is not UNSET:
            field_dict["queued"] = queued
        if auto_merge_enabled is not UNSET:
            field_dict["autoMergeEnabled"] = auto_merge_enabled
        if auto_merge_held_by is not UNSET:
            field_dict["autoMergeHeldBy"] = auto_merge_held_by
        if auto_merge_allowed is not UNSET:
            field_dict["autoMergeAllowed"] = auto_merge_allowed
        if review is not UNSET:
            field_dict["review"] = review
        if auto_merge is not UNSET:
            field_dict["autoMerge"] = auto_merge
        if hidden is not UNSET:
            field_dict["hidden"] = hidden
        if hidden_until is not UNSET:
            field_dict["hiddenUntil"] = hidden_until

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.allowed_action import AllowedAction # noqa: PLC0415
        from ..models.auto_merge_status import AutoMergeStatus # noqa: PLC0415
        from ..models.auto_update import AutoUpdate # noqa: PLC0415
        from ..models.bot_request import BotRequest # noqa: PLC0415
        from ..models.check_counts import CheckCounts # noqa: PLC0415
        from ..models.closing_issue import ClosingIssue # noqa: PLC0415
        from ..models.label import Label # noqa: PLC0415
        from ..models.mentioned_issue import MentionedIssue # noqa: PLC0415
        from ..models.pull_request_status import PullRequestStatus # noqa: PLC0415
        from ..models.queued_action import QueuedAction # noqa: PLC0415
        from ..models.review_state import ReviewState # noqa: PLC0415
        from ..models.stack_position import StackPosition # noqa: PLC0415
        from ..models.stack_ref import StackRef # noqa: PLC0415
        from ..models.update_request import UpdateRequest # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        repo = d.pop("repo")

        number = d.pop("number")

        title = d.pop("title")

        url = d.pop("url")

        author = d.pop("author")

        author_avatar_url = d.pop("authorAvatarUrl")

        author_url = d.pop("authorUrl")

        draft = d.pop("draft")

        labels = []
        _labels = d.pop("labels")
        for labels_item_data in (_labels):
            labels_item = Label.from_dict(labels_item_data)



            labels.append(labels_item)


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        ci = CIStatus(d.pop("ci"))




        checks = CheckCounts.from_dict(d.pop("checks"))




        merge_status = MergeStatus(d.pop("mergeStatus"))




        behind = d.pop("behind")

        head_sha = d.pop("headSha")

        kind = PullRequestKind(d.pop("kind"))




        base_branch = d.pop("baseBranch")

        head_branch = d.pop("headBranch")

        cross_repository = d.pop("crossRepository")

        def _parse_stack(data: object) -> None | StackPosition:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                stack_type_1 = StackPosition.from_dict(data)



                return stack_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StackPosition, data)

        stack = _parse_stack(d.pop("stack"))


        def _parse_stacked_on(data: object) -> None | StackRef:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                stacked_on_type_1 = StackRef.from_dict(data)



                return stacked_on_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StackRef, data)

        stacked_on = _parse_stacked_on(d.pop("stackedOn"))


        stack_children = cast(list[int], d.pop("stackChildren"))


        requested_reviewer_logins = cast(list[str], d.pop("requestedReviewerLogins"))


        awaiting_workflow_approval = d.pop("awaitingWorkflowApproval")

        review_comments = d.pop("reviewComments")

        conversation_comments = d.pop("conversationComments")

        closes_issues = []
        _closes_issues = d.pop("closesIssues")
        for closes_issues_item_data in (_closes_issues):
            closes_issues_item = ClosingIssue.from_dict(closes_issues_item_data)



            closes_issues.append(closes_issues_item)


        mentions_issues = []
        _mentions_issues = d.pop("mentionsIssues")
        for mentions_issues_item_data in (_mentions_issues):
            mentions_issues_item = MentionedIssue.from_dict(mentions_issues_item_data)



            mentions_issues.append(mentions_issues_item)


        def _parse_unresolved_threads(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        unresolved_threads = _parse_unresolved_threads(d.pop("unresolvedThreads"))


        review_requested_from_me = d.pop("reviewRequestedFromMe")

        empty = d.pop("empty")

        allowed_actions = []
        _allowed_actions = d.pop("allowedActions")
        for allowed_actions_item_data in (_allowed_actions):
            allowed_actions_item = AllowedAction.from_dict(allowed_actions_item_data)



            allowed_actions.append(allowed_actions_item)


        def _parse_status(data: object) -> None | PullRequestStatus:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                status_type_1 = PullRequestStatus.from_dict(data)



                return status_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PullRequestStatus, data)

        status = _parse_status(d.pop("status"))


        ready_to_merge = d.pop("readyToMerge")

        failing_ci = d.pop("failingCi")

        needs_review = d.pop("needsReview")

        auto_update = AutoUpdate.from_dict(d.pop("autoUpdate"))




        def _parse_bot_request(data: object) -> BotRequest | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                bot_request_type_1 = BotRequest.from_dict(data)



                return bot_request_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(BotRequest | None | Unset, data)

        bot_request = _parse_bot_request(d.pop("botRequest", UNSET))


        def _parse_update_request(data: object) -> None | Unset | UpdateRequest:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                update_request_type_1 = UpdateRequest.from_dict(data)



                return update_request_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UpdateRequest, data)

        update_request = _parse_update_request(d.pop("updateRequest", UNSET))


        def _parse_queued(data: object) -> None | QueuedAction | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                queued_type_1 = QueuedAction.from_dict(data)



                return queued_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | QueuedAction | Unset, data)

        queued = _parse_queued(d.pop("queued", UNSET))


        auto_merge_enabled = d.pop("autoMergeEnabled", UNSET)

        auto_merge_held_by = d.pop("autoMergeHeldBy", UNSET)

        auto_merge_allowed = d.pop("autoMergeAllowed", UNSET)

        _review = d.pop("review", UNSET)
        review: ReviewState | Unset
        if isinstance(_review,  Unset):
            review = UNSET
        else:
            review = ReviewState.from_dict(_review)




        _auto_merge = d.pop("autoMerge", UNSET)
        auto_merge: AutoMergeStatus | Unset
        if isinstance(_auto_merge,  Unset):
            auto_merge = UNSET
        else:
            auto_merge = AutoMergeStatus.from_dict(_auto_merge)




        hidden = d.pop("hidden", UNSET)

        _hidden_until = d.pop("hiddenUntil", UNSET)
        hidden_until: datetime.datetime | Unset
        if isinstance(_hidden_until,  Unset):
            hidden_until = UNSET
        else:
            hidden_until = datetime.datetime.fromisoformat(_hidden_until)




        pull_request = cls(
            forge=forge,
            repo=repo,
            number=number,
            title=title,
            url=url,
            author=author,
            author_avatar_url=author_avatar_url,
            author_url=author_url,
            draft=draft,
            labels=labels,
            created_at=created_at,
            updated_at=updated_at,
            ci=ci,
            checks=checks,
            merge_status=merge_status,
            behind=behind,
            head_sha=head_sha,
            kind=kind,
            base_branch=base_branch,
            head_branch=head_branch,
            cross_repository=cross_repository,
            stack=stack,
            stacked_on=stacked_on,
            stack_children=stack_children,
            requested_reviewer_logins=requested_reviewer_logins,
            awaiting_workflow_approval=awaiting_workflow_approval,
            review_comments=review_comments,
            conversation_comments=conversation_comments,
            closes_issues=closes_issues,
            mentions_issues=mentions_issues,
            unresolved_threads=unresolved_threads,
            review_requested_from_me=review_requested_from_me,
            empty=empty,
            allowed_actions=allowed_actions,
            status=status,
            ready_to_merge=ready_to_merge,
            failing_ci=failing_ci,
            needs_review=needs_review,
            auto_update=auto_update,
            bot_request=bot_request,
            update_request=update_request,
            queued=queued,
            auto_merge_enabled=auto_merge_enabled,
            auto_merge_held_by=auto_merge_held_by,
            auto_merge_allowed=auto_merge_allowed,
            review=review,
            auto_merge=auto_merge,
            hidden=hidden,
            hidden_until=hidden_until,
        )


        pull_request.additional_properties = d
        return pull_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
