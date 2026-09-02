"""Resolve a board's assignee to an InnoDay user.

**Every match is scoped to one organization.** ``resolve`` takes the
``organization_id`` of the board being synced and will only ever answer with a
user holding an *active* ``OrganizationMembership`` in it. Without that scope
the email path matched ``users.email`` across the entire platform: a board in
org A whose assignee email belongs to someone who exists only in org B would
write that stranger's user id into org A's ``ticket.assigned_to``. The email is
globally unique, so it identified the right *human* — but being the right human
somewhere else on the platform is not authorisation to appear in this org's
tickets. Org is the tenancy boundary (see CLAUDE.md, "Architecture"), and a
resolver that crosses it is a tenancy leak whichever column it matched on.

The resolution order is deliberately short and has no tail:

1. **Email**, case-insensitively against ``users.email`` *or*
   ``users.jira_email`` — only when the board actually supplied one. Jira often
   withholds it (Atlassian privacy settings) and Trello never exposes member
   email at all.
2. **Handle**, exactly, against a registered ``user_identity`` row for that
   platform — a row scoped to this project first, then a global
   (``project_id IS NULL``) one. Both name the same person; the project row
   exists because one client's board may call them something else.
3. **For GitHub only**, ``users.github_username``, case-insensitively.
4. **Nothing.** Return ``None``.

**Why the explicit row is consulted before the column, and not the other way
round.** ``users.github_username`` is written automatically — the profile page
and the Team page's commit-handle control both set it, and it is the column an
account connection populates without anybody deciding anything about
attribution. A ``user_identity`` row is only ever created by somebody saying
"this handle is that person". Reading the column first let an automatic value
shadow a deliberate one: a project-scoped override, made precisely because the
generic answer was wrong, stopped answering the moment anyone's login happened
to match. A manual override that a background write can silently defeat is not
an override.

**The membership requirement applies to both paths, including a global handle
row.** A ``project_id IS NULL`` row is cross-*project* by design — one person,
several boards — but that is not the same as cross-*organization*, and nothing
about writing the row establishes that its owner belongs to whichever org later
syncs a board using that handle. A global row is in fact the easier way in: one
row, claimed once, and it answers for every org on the platform. Applying the
same check to both keeps one rule ("a match is a member of this org") rather
than two, and leaves the global row doing exactly the job it was added for.

There is no fuzzy display-name matching and there must never be one. Two people
called "Alex" on a client's board is normal; guessing between them silently
reassigns someone's work. An unmatched assignee is the expected outcome for most
boards, not an error — `Ticket.assignee` still records exactly what the board
said, so no information is lost by declining to guess. A non-member is simply
one more kind of non-match: ``None``, no partial credit, nothing logged as
resolved.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import func, or_
from sqlmodel import Session, select

from src.adapters.board_assignee import BoardAssignee
from src.domain.organization import OrganizationMembership
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity

logger = logging.getLogger(__name__)


class HandleAlreadyClaimedError(Exception):
    """A handle is already linked to a different user.

    Catchable on purpose: the caller renders "That handle is already linked to
    another user" rather than a 500.
    """

    def __init__(
        self,
        platform: IdentityPlatform,
        handle: str,
        claimed_by_user_id: str,
    ) -> None:
        self.platform = platform
        self.handle = handle
        self.claimed_by_user_id = claimed_by_user_id
        super().__init__(
            f"{platform.value} handle {handle!r} is already linked to another user"
        )


@dataclass(frozen=True)
class IdentityMatch:
    """A resolved user, and how we got there.

    **Kept deliberately, despite no production caller reading the last two
    fields.** They are the resolver's provenance: `project_scoped` is the only
    observable that tells a project override apart from the global fallback,
    and both answers name the same user, so without it the precedence rule --
    the whole reason `project_id` is nullable -- is unobservable and untestable.
    `tests/test_user_identity_mapping.py` asserts on both.

    `src/routers/webui/data.py` reconstructs the equivalent of `match_source`
    by hand today; pointing it at this field is a worthwhile follow-up and a
    change to a live page, so it is not being done as part of a fix pass.
    """

    user: User
    match_source: MatchSource
    project_scoped: bool = False


class IdentityResolutionService:
    """Board assignee → InnoDay user, and the claim rules behind it."""

    @staticmethod
    def active_member(
        session: Session, *, user_id: str, organization_id: str
    ) -> Optional[User]:
        """The user, but only if they are an active member of that org.

        `is_active` is checked, not just the row's existence: a deactivated
        membership is how someone is taken off an org without deleting the
        history, and reassigning tickets to them would undo that silently.

        **Part of this class's supported surface, not a private helper.** It was
        `_active_member` while `resolve` was its only caller; the identities
        routes then reached across the module boundary into the underscore,
        which is a signal that the check belongs to callers as much as to the
        resolver. It does: "would resolution accept this person here?" is the
        same question a mapping route has to answer before it writes a row that
        could never fire. The name now says so, so the answer keeps coming from
        one place rather than being re-derived per caller.
        """
        return session.exec(
            select(User)
            .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
            .where(
                User.id == user_id,
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active.is_(True),
            )
        ).first()

    @staticmethod
    def resolve(
        session: Session,
        *,
        organization_id: str,
        project_id: Optional[str],
        platform: IdentityPlatform,
        assignee: BoardAssignee,
    ) -> Optional[IdentityMatch]:
        """Resolve `assignee` to a member of `organization_id`, or None.

        Never guesses, and never answers with a user who is not an active
        member of that organization — see the module docstring.
        """
        if assignee is None or assignee.is_empty():
            return None

        # 1. Email, case-insensitive. Only when the board gave us one.
        #    `jira_email` counts too: it exists precisely because the Atlassian
        #    address routinely differs from the InnoDay login email, which is
        #    the main case this path has to cover on Jira.
        #
        #    Membership is a JOIN rather than a check on the result, so a
        #    non-member cannot shadow a member: `users.email` is unique but
        #    `jira_email` is not, and filtering after a `.first()` would let an
        #    outsider's row win the ordering and turn a real match into None.
        email = (assignee.email or "").strip()
        if email:
            user = session.exec(
                select(User)
                .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
                .where(
                    OrganizationMembership.organization_id == organization_id,
                    OrganizationMembership.is_active.is_(True),
                    or_(
                        func.lower(User.email) == email.lower(),
                        func.lower(User.jira_email) == email.lower(),
                    ),
                )
            ).first()
            if user:
                return IdentityMatch(user=user, match_source=MatchSource.EMAIL)

        handle = (assignee.display_name or "").strip()

        # 2. A registered handle for this platform: project override, then global.
        if handle:
            # Ordered so the winner is never arbitrary. The constraints make a
            # tie unlikely -- one row per scope, one global owner per handle --
            # but rows predating those constraints can still exist, and an
            # unordered SELECT would hand the choice to whatever Postgres
            # happened to return first.
            rows = session.exec(
                select(UserIdentity)
                .where(
                    UserIdentity.platform == platform,
                    UserIdentity.handle == handle,
                )
                .order_by(UserIdentity.created_at.asc(), UserIdentity.id.asc())
            ).all()
            overrides = (
                [r for r in rows if r.project_id == project_id]
                if project_id is not None
                else []
            )
            globals_ = [r for r in rows if r.project_id is None]
            for row, scoped in [(r, True) for r in overrides] + [
                (r, False) for r in globals_
            ]:
                # Same membership rule as the email path, global rows included.
                user = IdentityResolutionService.active_member(
                    session,
                    user_id=row.user_id,
                    organization_id=organization_id,
                )
                if user:
                    return IdentityMatch(
                        user=user,
                        match_source=MatchSource.HANDLE,
                        project_scoped=scoped,
                    )

        # 3. For GitHub, `users.github_username` -- the column the profile page and
        #    the Team page's commit-handle mapping both write.
        #
        #    **This is the fix for a control that looked like it worked.** Mapping
        #    a commit handle set that column and nothing else, while resolution
        #    read only `user_identity` -- so the Team page stopped listing the
        #    handle as unmapped (its own list matches `github_username`) and every
        #    summary that followed still showed the author as unmapped. The mapping
        #    appeared to take and changed nothing that mattered. One column read by
        #    both is the honest fix; writing two rows on every mapping would leave
        #    two sources to keep in step.
        #
        #    **Last, not first** -- see the module docstring. The column is written
        #    automatically; a `user_identity` row is written by a person. An
        #    automatic value must not shadow a deliberate one.
        #
        #    Same active-membership JOIN as the email path, and for a sharper
        #    reason: `github_username` carries no uniqueness constraint at all, so
        #    filtering after a `.first()` would let a non-member shadow a member.
        if handle and platform == IdentityPlatform.GITHUB:
            user = session.exec(
                select(User)
                .join(OrganizationMembership, OrganizationMembership.user_id == User.id)
                .where(
                    OrganizationMembership.organization_id == organization_id,
                    OrganizationMembership.is_active.is_(True),
                    func.lower(User.github_username) == handle.lower(),
                )
            ).first()
            if user:
                # `GITHUB_USERNAME`, not `HANDLE`. Both name the same human and
                # only the label tells them apart, which is exactly why they
                # must not share one: since the explicit row was made to beat
                # this column, "the override fired" and "the override did not
                # exist" were the same telemetry value. See `MatchSource`.
                return IdentityMatch(
                    user=user, match_source=MatchSource.GITHUB_USERNAME
                )

        # 4. Unmatched. That is a valid answer.
        return None

    @staticmethod
    def find_conflicting_claim(
        session: Session,
        *,
        user_id: str,
        platform: IdentityPlatform,
        handle: str,
        organization_id: str,
        project_id: Optional[str] = None,
    ) -> Optional[UserIdentity]:
        """The row, if any, that links this handle to a *different* user here.

        "A handle already matched cannot be paired with another person" is the
        rule, and it holds across every project -- letting two users hold one
        handle in different projects would make the global fallback ambiguous.
        But it is an **intra-organisation** rule, and it used to be enforced
        platform-wide.

        That had two cross-tenant effects, both reproduced before this changed.
        One org claiming a common display name permanently blocked every other
        org's member from the same string on a board they share nothing with --
        so the first tenant to type `admin` or a common personal name squatted
        it for the platform. And the refusal was readable: "already linked to
        another user" answered "does anybody, anywhere, hold this handle?" for
        any authenticated caller, about tenants they cannot otherwise see.

        Scoping to the claiming organisation keeps the rule where it means
        something. Membership is what scopes it -- the *other* user's active
        membership, not the row's project -- because a global row (`project_id
        IS NULL`) has no project to scope by and is precisely the row that would
        otherwise reach across.

        `project_id` adds the one case membership cannot cover: a row already
        sitting in the exact scope being claimed. `UNIQUE(project_id, platform,
        handle)` means the database can only hold one, so whoever holds it is a
        conflict whatever their membership says -- a user who has since left the
        org still occupies the slot. Without this the caller was handed *their*
        row back as though the claim had succeeded. It reveals nothing across
        tenants: the scope being asked about is the caller's own project.
        """
        by_membership = session.exec(
            select(UserIdentity)
            .join(
                OrganizationMembership,
                OrganizationMembership.user_id == UserIdentity.user_id,
            )
            .where(
                UserIdentity.platform == platform,
                UserIdentity.handle == handle,
                UserIdentity.user_id != user_id,
                OrganizationMembership.organization_id == organization_id,
                OrganizationMembership.is_active.is_(True),
            )
        ).all()
        if by_membership:
            return by_membership[0]

        occupant = session.exec(
            select(UserIdentity).where(
                UserIdentity.platform == platform,
                UserIdentity.handle == handle,
                UserIdentity.user_id != user_id,
                (
                    UserIdentity.project_id.is_(None)
                    if project_id is None
                    else UserIdentity.project_id == project_id
                ),
            )
        ).first()
        return occupant

    @staticmethod
    def claim_identity(
        session: Session,
        *,
        user_id: str,
        platform: IdentityPlatform,
        handle: str,
        organization_id: str,
        project_id: Optional[str] = None,
        board_user_id: Optional[str] = None,
        match_source: MatchSource = MatchSource.MANUAL,
    ) -> UserIdentity:
        """Register `handle` for `user_id`, or raise if someone else holds it.

        Idempotent for the same (project, platform, handle, user): the existing
        row is returned, with `board_user_id` filled in if it was missing. The
        same user holding the same handle in several projects is allowed — that
        is one person on two boards, not a conflict.

        `organization_id` is required rather than defaulted: it scopes the
        conflict check (see `find_conflicting_claim`), and a default would make
        the safe behaviour the one you have to remember to ask for.

        Raises:
            HandleAlreadyClaimedError: a different user in this organisation
                already holds it.
        """
        handle = handle.strip()
        if not handle:
            raise ValueError("handle must not be empty")

        conflict = IdentityResolutionService.find_conflicting_claim(
            session,
            user_id=user_id,
            platform=platform,
            handle=handle,
            organization_id=organization_id,
            project_id=project_id,
        )
        if conflict is not None:
            raise HandleAlreadyClaimedError(platform, handle, conflict.user_id)

        # `user_id` in the lookup, not just the scope: the conflict check above
        # has already refused every row belonging to somebody else, so this can
        # only match the caller's own -- but stating it means a future change to
        # that check cannot turn "idempotent" into "returns another user's row".
        existing = session.exec(
            select(UserIdentity).where(
                UserIdentity.user_id == user_id,
                UserIdentity.platform == platform,
                UserIdentity.handle == handle,
                UserIdentity.project_id == project_id,
            )
        ).first()
        if existing is not None:
            if board_user_id and existing.board_user_id != board_user_id:
                existing.board_user_id = board_user_id
                existing.touch()
                session.add(existing)
                session.flush()
            return existing

        identity = UserIdentity(
            user_id=user_id,
            project_id=project_id,
            platform=platform,
            handle=handle,
            board_user_id=board_user_id,
            match_source=match_source,
        )
        session.add(identity)
        session.flush()
        return identity
