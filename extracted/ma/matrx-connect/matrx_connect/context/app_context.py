from __future__ import annotations

import dataclasses
import re
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID, uuid4

from matrx_connect.context.tenant_provenance import (
    AuthorizedResourceAdmission,
    AuthorizedResourceTenantProvenance,
    DelegatedMemberTenantProvenance,
    ExplicitSystemTenantProvenance,
    MembershipTenantProvenance,
    TenantProvenance,
    _TenantContextSeal,
    _require_principal,
)

if TYPE_CHECKING:
    from matrx_connect.context.emitter_protocol import Emitter


_EXECUTION_KIND_RE = re.compile(r"^[a-z][a-z0-9_.:-]{0,63}$")


#: ``AppContext.metadata`` key a child-agent fork stamps with the root parent's origin class.
PARENT_ORIGIN_CLASS_KEY = "parent_origin_class"

#: Metadata keys that name what the CALLER run is. A child agent run owns its own
#: turn, so ``fork_for_child_agent`` never carries them onto the child (they would be
#: stamped on the child's own ``chat.user_request``: the parent's surface binding,
#: voice session, workflow node or mandate). ``parent_request_id`` is a column now,
#: never metadata.
PARENT_RUN_IDENTITY_KEYS = frozenset(
    {
        "launch_binding_id",
        "workflow_node_id",
        "voice_session_id",
        "voice_interaction_id",
        "voice_provider_call_id",
        "mandate_key",
        "mandate_attribution",
        "parent_request_id",
    }
)


def _root_fork_origin_class(parent: AppContext) -> str:
    # Lazy: provenance imports this module for its type checks.
    from matrx_connect.context.provenance import root_fork_origin_class

    return root_fork_origin_class(parent)


@dataclass(frozen=True)
class AppContext:
    """Request-scoped context carried through the entire call stack via ContextVar.

    Set by middleware on every inbound request. Readable anywhere via
    ``get_app_context()``.

    **AppContext is FROZEN.** Direct field assignment raises
    ``FrozenInstanceError``. Use::

        ctx = ctx.with_overrides(field=value)
        set_app_context(ctx)

    Note that the ``metadata`` and ``api_keys`` dicts are still themselves
    mutable. ``with_overrides(metadata={**ctx.metadata, k: v})`` is the
    correct pattern for adding metadata. Phase 2 will replace these with
    truly-immutable mapping types.

    Auth fields
    -----------
    auth_type       : "token" (JWT) | "api_key" | "fingerprint" | "cookie" (browser file-session cookie, GET byte routes only) | "anonymous"
    is_authenticated: True for admitted JWT, API-key or file-cookie authority; fingerprint guests carry a resolved identity separately.
    is_anonymous    : True for a verified JWT whose ``is_anonymous`` claim is true (a guest token). ``has_account`` = is_authenticated and not is_anonymous.
    is_admin        : True when user_id has a row in admin.admins (resolved on every JWT auth). Exactly equivalent to ``admin_level is not None`` — a convenience boolean, never a substitute for the tier.
    admin_level     : The caller's admin tier from admin.admins.level — "super_admin" | "senior_admin" | "developer" — or None for a non-admin. Only "super_admin" carries unrestricted authority (e.g. the raw ``sql`` tool executes on the privileged pool). senior_admin/developer are recognized and logged but, until per-tier rule-sets exist, fall back to the caller's own RLS permissions. NEVER gate solely on is_admin where the tiers must differ — read admin_level.

    Identity fields
    ---------------
    All services share the same identity model so service-to-service calls
    propagate a consistent context regardless of which service originates the
    request.
    """

    emitter: Emitter

    # --- Auth ---
    user_id: str = ""
    email: str | None = None
    auth_type: Literal["token", "api_key", "fingerprint", "cookie", "anonymous"] = "anonymous"
    is_authenticated: bool = False
    # GUEST TOKEN (guests-use-everything D1, 2026-10-11). True when the verified
    # JWT carries ``is_anonymous: true`` — a Supabase anonymous user minted by
    # ``POST /auth/guest/session``. Such a token stays ``auth_type="token"`` and
    # ``is_authenticated=True`` (every inline ``is_authenticated`` read keeps
    # admitting it); only account-only work reads ``has_account`` and refuses.
    # False for every other lane (fingerprint, cookie, API key, anonymous).
    is_anonymous: bool = False
    is_admin: bool = False
    # Admin tier — see the class docstring. None for a non-admin; is_admin is
    # True iff this is non-None. Carried through with_overrides / fork_* via
    # dataclasses.replace (default field, no explicit copy needed).
    admin_level: str | None = None
    # THE ADMIN SURFACE (Arman, 2026-09-25: "Admin privileges cannot ever extend
    # beyond the admin sections of the system."). The ONE run-level flag: True only
    # when this request/run was started from an admin surface — an admin-mounted
    # router (the host marks it) or the admin-scoped MCP. Admin powers in agent
    # tools and admin reach in services require it; a normal chat never carries it,
    # so an admin there is an ordinary person. Meaningless without an admin
    # identity — read it through ``admin_surface_active()``, never alone. Carried
    # through with_overrides / fork_* via dataclasses.replace like admin_level.
    admin_surface: bool = False
    # Child content-safety flag (WP13). True iff the signed-in user's declared
    # age band is under 18 (`under_13` or `13_17`). Resolved ONCE per request at
    # the AI funnel (`_run_ai_task_body` → education_compliance.stamp_minor_status)
    # and read by every downstream content-safety lever — safe model tier, the
    # NSFW image filter, output moderation, and the minor-reminder context note.
    # "One flag, many changes" (Arman, 2026-08-17). Default False = adult/undeclared
    # /guest/unresolved (content-safety degrades OPEN, never blocking all AI). It
    # propagates to child-agent and workflow-step forks via dataclasses.replace,
    # which is correct: a child serving a minor's request stays minor-safe.
    is_minor: bool = False

    # --- Request metadata ---
    fingerprint_id: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    token: str | None = None

    request_id: str = ""
    operation_id: str = ""

    # --- Usage-gate admission (USAGE-GATE.md rule 5) ---
    # True when this context CONTINUES a user operation whose usage admission
    # was already decided: a resume of an existing request after a pause for
    # input / client tool results (possibly on another server process or after
    # a restart), or a request id minted internally for a step of the same user
    # action. The usage gate (matrx_ai.providers.usage_gate) never refuses such
    # a context — "a running request is never stopped" must hold across
    # processes, and the gate's in-process memo cannot see other processes.
    # Set ONLY by server code that has itself established the continuation
    # (never from a client header). Propagates through with_overrides / fork_*
    # via dataclasses.replace.
    usage_admitted: bool = False

    # --- Durable execution attribution ---
    # Generic, immutable pointer stamped onto every paid request. Consumers
    # choose the vocabulary (for example ``workflow_run``); persistence never
    # scrapes mutable metadata or infers ownership from a conversation id.
    execution_kind: str | None = None
    execution_id: str | None = None

    # The API route this request hit (request.url.path), stamped once at
    # context construction in AuthMiddleware. Used by observability (app_log
    # route tagging) and any code that wants to attribute work to a route.
    # None for non-HTTP contexts (workers, scheduled runs). Propagates through
    # with_overrides + fork_* via dataclasses.replace.
    route: str | None = None

    # --- Organizational scope ---
    organization_id: str | None = None
    project_id: str | None = None
    task_id: str | None = None

    # 🚨 WHY organization_id IS NULL — the answer, not the silence.
    #
    #   "none"         this request named no organization (a background job, a
    #                  worker, a signed-in user who has selected nothing). The
    #                  system rung is the honest answer.
    #   "verified"     an organization was named AND membership was proved.
    #                  organization_id is set.
    #   "denied"       an organization was named and the caller is provably NOT
    #                  a member. organization_id is None ON PURPOSE.
    #   "unknown"      an organization was named, it is well-formed, and NO SUCH
    #                  ORGANIZATION EXISTS. Permanent, like "denied", but a
    #                  different repair: "denied" means ask to be added, "unknown"
    #                  means the id is wrong or the organization is gone.
    #   "malformed"    an organization was named and it is not an organization id
    #                  at all. Never worth a membership lookup, and never worth
    #                  telling the caller to "try again".
    #   "unverifiable" an organization was named and the platform COULD NOT TELL
    #                  (an ORM/database failure inside the resolver). This is the
    #                  one nobody could see before 2026-09-07: it looked exactly
    #                  like "none", so a transient DB blip silently demoted a
    #                  signed-in user to no-org — and under the mandate ladder
    #                  (user -> ACTIVE org -> system) that means A DIFFERENT
    #                  AGENT RAN, with nothing on the screen and nothing in the
    #                  run record. Consumers that resolve BY organization must
    #                  refuse on this value, never resolve one rung lower.
    #
    # Set only by the auth middleware's organization admission
    # (matrx_connect.middleware.auth._resolve_organization). Propagates through
    # with_overrides / fork_* via dataclasses.replace.
    # 🚨 THE MARKER IS ONLY WORTH SETTING IF SOMETHING READS IT. Until
    # 2026-09-08 nothing did: the admission refusal answered all of these with
    # ONE sentence — "This request carried an identity but no organization" —
    # which is a lie in every case except "none", and told a permanent
    # non-member and a transient outage the same "try again"
    # (V-CORRECTNESS F1). `AuthMiddleware._organization_admission_words` reads
    # it now; a new value here MUST get a sentence there.
    organization_admission: Literal[
        "none", "verified", "denied", "unknown", "malformed", "unverifiable"
    ] = "none"
    #: The organization id that was CLAIMED, kept when admission is not
    #: "verified" so a refusal can name it instead of saying "some org".
    claimed_organization_id: str | None = None

    # The value installed by a tenant admission boundary.  It is deliberately
    # private implementation state rather than an authorization claim or wire
    # contract: a frozen TenantAppContext may be copied for ordinary execution
    # work, but it may never be repointed at another organization.
    _organization_admission_binding: str | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )
    _organization_admission_provenance_binding: Literal["none", "verified"] | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )
    _tenant_provenance: TenantProvenance | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )
    _tenant_context_seal: _TenantContextSeal | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )

    # --- Source tracking ---
    source_app: str = ""
    source_feature: str = ""

    # The TRUST axis of attribution — what KIND of thing initiated this work,
    # derived from platform-witnessed facts, never from caller declarations.
    # Vocabulary + derivation live in matrx_connect.context.provenance:
    # human | client_auto | api (attested — only the provenance module may
    # produce these) and child_agent | workflow | scheduled | system (machine
    # classes, set by the fork/system mint points below). "" = not yet derived;
    # the persistence gate reconciles it against the witness before any write,
    # so a value unsupported by the observed facts NEVER lands in the DB.
    # Guard: scripts/check_origin_provenance.py (build-failing).
    origin_class: str = ""

    # --- Persistence control ---
    store: bool = True

    # System-run mode: this context drives an INTERNAL machine call (fan-out
    # derivations, pipelines, probes, replays). It keeps its FULL history
    # exactly like a chat — conversation, cx_message rows, per-iteration
    # cx_request cost rows and the request snapshot (owner ruling 2026-10-05:
    # every AI call keeps its history one way). It differs from a person's run
    # only in its flags and ceremony: it is listed in no chat list by default (the
    # owning person can still open it, linked to the conversation it ran in), and
    # it skips the title LLM call, cache-state refresh and the context-state event.
    # store=False ("write NOTHING") is reserved for a PERSON's explicit unsaved
    # chat and the conversation labeler — never any other internal call (owner
    # ruling 2026-10-23; matrx_ai/orchestrator/unsaved_runs.py). Set via run_agent(system_run=True);
    # consumers read it with getattr(ctx, "system_run", False).
    system_run: bool = False

    # Confidential ("sealed") run: the person's content stays on their devices.
    # ``sealed_conversation_id`` is set ONLY by a chat door after the
    # conversation gate created/verified that sealed conversation row. ``store``
    # stays False on a sealed run, so every derived-content job keyed on
    # ``store`` (memory, titles, snapshots, KG, hindsight) skips exactly as an
    # ephemeral run does. Structure writers (conversation, message, request,
    # tool_call rows) opt in only for THAT conversation, and the one write
    # funnel (matrx_ai.persistence.queue_helpers._queue_or_drop) empties every
    # content column of every row written under a sealed context — forks
    # inherit the field, so a sub-agent of a sealed run is sealed too.
    # ``sealed_keeps_content`` is the organization knob
    # chat.confidential.keep_content_on_server: rows keep their content, the
    # conversation is still marked confidential.
    sealed_conversation_id: str | None = None
    sealed_keeps_content: bool = False

    # --- Extensible metadata ---
    api_keys: dict[str, str] = field(default_factory=dict, repr=False)
    # WHOSE KEY: sha256 fingerprints of the ``api_keys`` values that came from the
    # person's (or their organization's) own vault. Only these zero-rate a model
    # call; a platform key a code path copies into ``api_keys`` stays ours and
    # charges (owner ruling 2026-10-15 #6). Values are never stored here.
    own_api_key_fingerprints: frozenset[str] = field(default_factory=frozenset, repr=False)
    metadata: dict[str, Any] = field(default_factory=dict)
    debug: bool = False

    # --- Conversation / AI context ---
    # None == "no conversation supplied" (the caller wants one assigned, or an
    # ephemeral run). It is NEVER the empty string: a falsy-but-non-null sentinel
    # used to ride into cx_* UUID FK columns as "" and 22P02 at flush time, hours
    # after the request detached. The orchestrator (execute_ai_request) resolves
    # this to a real UUID before any persistence — identical to the API's
    # resolve_conversation contract.
    conversation_id: str | None = None
    parent_conversation_id: str | None = None
    # The turn this run's turn ran under (a child agent run's caller turn), or None
    # for a top-level turn. Every child agent run owns its OWN turn (its own
    # ``request_id`` → its own ``chat.user_request`` row); this names the caller's.
    parent_request_id: str | None = None
    # The top of this run's request tree, frozen at the first fork (None for a
    # top-level run: its root is itself). Read it through ``tree_request_id`` —
    # the one key the tree-wide cost cap, the usage / run-approval admission
    # memos and stop / retry-now controls use, so a child that owns its own turn
    # still spends, is admitted and is stopped as part of the tree it ran in.
    root_request_id: str | None = None
    is_internal_agent: bool = False

    # How the conversation this context drives was initiated — persisted to
    # cx_conversation.conversation_type and the UI's source of truth for routing
    # conversations by origin (standard / subagent / scheduled / workflow /
    # research / podcast / auto / system). The vocabulary + validation gate live
    # in matrx_ai.agents.conversation_type (matrx-connect can't import matrx-ai,
    # so the default is the literal "standard"). Set explicitly at every
    # context-construction site; the conversation gate re-derives from
    # is_internal_agent / source_feature as a safety net so an internal run is
    # never silently labeled "standard".
    conversation_type: str = "standard"

    # --- Per-request AI overrides ---
    initial_variables: dict[str, Any] = field(default_factory=dict)
    initial_overrides: dict[str, Any] = field(default_factory=dict)

    # --- Agent tracking (written to cx_conversation / cx_user_request) ---
    agent_id: str | None = None
    agent_version_id: str | None = None

    # --- Unit-version pinning for replay (chat.request_snapshot) ---
    # The workflow definition VERSION this call is being made inside, when the
    # run pinned one. `agent_version_id` above is the agent half and already
    # travels on every agent run; this is the workflow half, and there was no
    # carrier for it — a snapshot could not say which workflow version produced
    # the call, so a replay could not tell a candidate change apart from an edit
    # made to the workflow since.
    #
    # Set ONCE per run (the scheduler stamps it onto the run's context) and
    # inherited by every fork, so a nested agent call inside a workflow step
    # still records the run's pin.
    #
    # NULL is HONEST: a run started from a FLOATING definition genuinely has no
    # pinned version (workflow.run.definition_version_id is null there too), and
    # a call made outside any workflow has none either.
    workflow_definition_version_id: str | None = None

    # --- Client-delegated tools ---
    client_tools: list[str] = field(default_factory=list)

    # --- Block streaming ---
    block_mode: bool = False

    # --- Debug / replay ---
    # Per-request OVERRIDE of request-snapshot capture. Tri-state:
    #   None  → the platform default (matrx-ai's
    #           REQUEST_SNAPSHOT_CAPTURE_DEFAULT, which is ON — every
    #           persisted AI iteration's provider request/response is written
    #           to chat.request_snapshot, the input half of replay)
    #   True  → force capture ON, and additionally arm the wire-level
    #           outbound capture with the FULL body (the default None also
    #           streams the wire request — AI Watch, 2026-10-11 — but caps
    #           a large body to a preview; matrx_ai/providers/outbound_capture.py).
    #   False → explicit opt-out; this request writes no snapshot.
    # Ephemeral runs (store=False) never write one regardless.
    snapshot: bool | None = None

    # --- AI Watch (provision leak fix, 2026-10-19) ---
    # True only when the caller is PERMITTED to watch this run (aidream
    # ``ai_watch_permitted``: an admin today, a per-person permission later) AND
    # asked to (``?debug_view=1`` on the door). Set ONCE, at the request boundary
    # (aidream ``open_ai_watch``), never from a request body. Read by everything
    # that would put a run's VALUES on the wire to the browser — the exact
    # provider request (``context_analysis``, matrx_ai.providers.outbound_capture)
    # streams only when this is True; ``snapshot=True`` no longer arms the wire
    # capture without it.
    ai_watch: bool = False

    # --- Observational memory ---
    # When True, the observational memory system (Observer + Reflector) runs
    # around each LLM turn — injects prior observations as a system message
    # pre-call, extracts new observations post-call. Admin-gated; persists on
    # cx_conversation.metadata.observational_memory once enabled. See
    # packages/matrx-ai/matrx_ai/memory/ and the OM integration guide.
    memory_enabled: bool = False
    memory_model: str | None = None
    #: The chosen CLASS of ``memory_model`` (an ai.offering id) — rides only with it.
    memory_offering_id: str | None = None
    memory_scope: str = "thread"

    def __post_init__(self) -> None:
        if (self.execution_kind is None) != (self.execution_id is None):
            raise ValueError("execution_kind and execution_id must be set together")
        if self.execution_kind is None:
            return
        if not _EXECUTION_KIND_RE.fullmatch(self.execution_kind):
            raise ValueError(
                "execution_kind must be a lowercase namespaced identifier "
                "(letters, digits, '.', ':', '_', '-')"
            )
        try:
            canonical_id = str(UUID(str(self.execution_id)))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError("execution_id must be a valid UUID") from exc
        object.__setattr__(self, "execution_id", canonical_id)

    def with_overrides(self, **kwargs: Any) -> AppContext:
        """Return a new AppContext with the given fields overridden.

        This is the Phase 1+ replacement for ``extend()``.  Callers that
        previously did ``ctx.extend(foo=bar)`` should now do::

            ctx = ctx.with_overrides(foo=bar)
            set_app_context(ctx)

        The explicit ``set_app_context`` is required because ``with_overrides``
        does not touch the ContextVar — it produces a new value, the caller
        chooses whether to install it.  This makes context updates auditable:
        if you do not call ``set_app_context``, no downstream code will ever
        see the override, which is the desired behavior for "compute a
        derived ctx for one local call".

        Raises ``AttributeError`` for unknown field names so typos surface
        immediately instead of silently no-oping.
        """
        valid = {f.name for f in dataclasses.fields(self)}
        for key in kwargs:
            if key in {
                "_organization_admission_binding",
                "_organization_admission_provenance_binding",
                "_tenant_provenance",
                "_tenant_context_seal",
            }:
                raise AttributeError("organization admission bindings are not overrideable")
            if key not in valid:
                raise AttributeError(
                    f"AppContext has no field '{key}'. "
                    f"Add it to the dataclass before using with_overrides()."
                )
        if kwargs.get("system_run") is True and not self.system_run:
            kwargs = _own_conversation_for_system_run(self, kwargs)
        return dataclasses.replace(self, **kwargs)

    def with_execution_attribution(self, kind: str, execution_id: str) -> AppContext:
        """Return a context that attributes durable work to one execution."""
        return dataclasses.replace(
            self,
            execution_kind=kind,
            execution_id=execution_id,
        )

    def extend(self, **kwargs: Any) -> AppContext:
        """REMOVED — AppContext is frozen as of Phase 1.

        Use ``with_overrides`` + ``set_app_context``::

            ctx = ctx.with_overrides(field=value)
            set_app_context(ctx)

        This shim remains only to convert any latent call sites into a
        loud, traceable error rather than a silent ``FrozenInstanceError``
        deep in ``setattr``.
        """
        raise RuntimeError(
            "AppContext.extend() has been removed. AppContext is now immutable. "
            "Replace `ctx.extend(**fields)` with "
            "`ctx = ctx.with_overrides(**fields); set_app_context(ctx)`. "
            f"Caller attempted to set fields: {list(kwargs.keys())}"
        )

    @property
    def has_account(self) -> bool:
        """A signed-in person with a real account — never a guest token.

        Derived, never stored: ``is_authenticated and not is_anonymous``. The
        one question account-only work (credential vault, billing, org
        membership, HR, sending identities) asks; everything else admits guests.
        """
        return bool(self.is_authenticated and not self.is_anonymous)

    @property
    def tree_request_id(self) -> str:
        """The request id the whole tree keys on: ``root_request_id or request_id``.

        A top-level run is its own root; a child agent run (which owns its own turn)
        names the root it was forked under. Cost cap, admission memos and stop
        controls read THIS, never ``request_id``, so a child's own turn never
        escapes the tree it ran in.
        """
        return self.root_request_id or self.request_id

    @property
    def conversation_id_for_lineage(self) -> str | None:
        """Return conversation provenance without promoting a workflow id.

        A workflow is correlated by its execution tree and ``parent_request_id``,
        never by a conversation parent. Two workflow ids look like conversations
        but are not rows a child can link to: the run UUID itself, and the
        per-invocation id ``fork_for_workflow_step`` mints for every node — a
        graph-action node never writes that row, so a mandate or child it ran
        that named it hit the gate's parent_missing path every time (334
        ``conversation_parent_lineage_unavailable`` rows on 2026-10-05).
        """
        if self.execution_kind == "workflow_run" and self.conversation_id == self.execution_id:
            return None
        if self.conversation_type == "workflow" and self.origin_class == "workflow":
            return None
        return self.conversation_id or None

    def fork_for_child_agent(
        self,
        new_conversation_id: str,
        operation_id: str | None = None,
    ) -> AppContext:
        """Create a derived context for a child agent call.

        ``dataclasses.replace()`` produces a shallow copy, so all dict/list
        fields would still alias the parent without explicit copies.  We
        therefore deep-copy every mutable collection so executor-side
        mutations on the child never propagate back to the parent.

        EVERY CHILD OWNS ITS OWN TURN (owner ruling 2026-10-23: a child run is
        recorded exactly like a normal chat). The fork mints a fresh
        ``request_id`` — the child's own ``chat.user_request`` row — keeps the
        caller's id as ``parent_request_id`` and freezes the tree's root as
        ``root_request_id`` (``tree_request_id`` reads it). The cost cap, the
        usage / run-approval admission memos and stop controls key on the root,
        so the tree is still capped, admitted once and stopped together.

        A ROOT fork (no caller conversation — a mandate / job / pipeline run
        under a route boundary) also gets its own id; the boundary id is its
        root, so a stop on the boundary id still stops it.

        The caller run's IDENTITY keys (launch binding, voice session, workflow
        node, mandate) are scrubbed from the child's metadata: they name what the
        PARENT run is and would be stamped on the child's own turn. A child that
        IS a mandate run re-stamps its own key (``run_agent``).
        """
        parent_lineage = self.conversation_id_for_lineage
        return dataclasses.replace(
            self,
            conversation_id=new_conversation_id,
            parent_conversation_id=parent_lineage,
            parent_request_id=self.request_id or None,
            is_internal_agent=True,
            # "subagent" means "has a parent conversation" (matches
            # ConversationType.SUBAGENT in matrx-ai). A fork with no caller
            # conversation is the ROOT run of a mandate / pipeline / job: ``auto``.
            conversation_type="subagent" if parent_lineage else "auto",
            # A fork with a parent conversation is a true sub-agent; a fork with
            # none is the ROOT run of its caller and carries the caller's class
            # (an MCP agent_run is ``api``, never ``child_agent``).
            origin_class=_root_fork_origin_class(self),
            request_id=str(uuid4()),
            root_request_id=self.tree_request_id or None,
            # Pass operation_id to the fork so child_agent_context doesn't
            # need to mutate the result post-fork (which is illegal once
            # AppContext is frozen).
            operation_id=operation_id if operation_id is not None else self.operation_id,
            # Child agents should NOT inherit the parent conversation's
            # memory — their internal reasoning shouldn't contribute to
            # parent observations, and they're on a different conversation
            # anyway.
            memory_enabled=False,
            memory_model=None,
            memory_offering_id=None,
            memory_scope="thread",
            metadata=self._child_agent_metadata(),
            api_keys=dict(self.api_keys),
            initial_variables=dict(self.initial_variables),
            initial_overrides=dict(self.initial_overrides),
            client_tools=list(self.client_tools),
        )

    def _child_agent_metadata(self) -> dict[str, Any]:
        """The child's metadata: the parent's, plus the ROOT parent's origin under
        ``PARENT_ORIGIN_CLASS_KEY``.

        A sub-agent's own origin is ``child_agent``, which says nothing about WHO started the
        tree. A spend gate that must refuse a sub-agent of an automated parent (scheduled /
        workflow / system) on a protected account, yet keep a person's own sub-agent, needs the
        parent's class. A chain keeps the first (root) parent's class, never ``child_agent``.
        """
        metadata = {k: v for k, v in self.metadata.items() if k not in PARENT_RUN_IDENTITY_KEYS}
        if metadata.get(PARENT_ORIGIN_CLASS_KEY):
            return metadata
        # The parent's DECLARED class, never reconcile_origin(): a person's run rebuilt by a
        # worker has no route, and reconcile would downgrade it to 'system' and get its
        # sub-agents refused. Only a genuinely automated parent is recorded.
        declared = str(self.origin_class or "")
        # A worker re-running a person's request (crash recovery) declares 'system' but is
        # still that request: its sub-agents record the request's ORIGINAL class.
        from matrx_connect.context.provenance import resumed_origin_class

        declared = resumed_origin_class(self) or declared
        if declared in ("scheduled", "workflow", "system"):
            metadata[PARENT_ORIGIN_CLASS_KEY] = declared
        return metadata

    def fork_for_workflow_step(self, new_conversation_id: str) -> AppContext:
        """Create an independent context for a single workflow invocation.

        The scheduler calls this once per parallel invocation in a super-
        step (NOT once per step) so concurrent agents never share a mutable
        AppContext.  Mutable collections are copied for the same reason
        described on ``fork_for_child_agent``.
        """
        return dataclasses.replace(
            self,
            conversation_id=new_conversation_id,
            parent_conversation_id=None,
            parent_request_id=None,
            is_internal_agent=True,
            # A workflow-step invocation is a workflow conversation
            # (matches ConversationType.WORKFLOW in matrx-ai).
            conversation_type="workflow",
            origin_class="workflow",
            request_id=self.request_id,
            metadata=dict(self.metadata),
            api_keys=dict(self.api_keys),
            initial_variables=dict(self.initial_variables),
            initial_overrides=dict(self.initial_overrides),
            client_tools=list(self.client_tools),
        )


@dataclass(frozen=True)
class TenantAppContext(AppContext):
    """An AppContext with immutable organization and admission provenance."""

    organization_id: str = field(kw_only=True)

    def __post_init__(self) -> None:
        super().__post_init__()
        try:
            organization_id = str(UUID(str(self.organization_id).strip()))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError("organization_id must be a valid UUID") from exc
        organization_binding = self._organization_admission_binding
        if organization_binding is None:
            raise ValueError("tenant organization admission binding is required")
        try:
            organization_binding = str(UUID(str(organization_binding).strip()))
        except (ValueError, TypeError, AttributeError) as exc:
            raise ValueError("organization admission binding must be a valid UUID") from exc
        if organization_binding != organization_id:
            raise ValueError("tenant organization cannot be replaced after admission")
        admission = self.organization_admission
        if admission not in {"none", "verified"}:
            raise ValueError("tenant admission must be none or verified")
        provenance_binding = self._organization_admission_provenance_binding
        if provenance_binding is None:
            raise ValueError("tenant admission provenance binding is required")
        if provenance_binding not in {"none", "verified"}:
            raise ValueError("tenant admission provenance binding is invalid")
        if provenance_binding != admission:
            raise ValueError("tenant admission provenance cannot be replaced")
        _require_principal(self.user_id, "tenant principal")
        provenance = self._tenant_provenance
        if type(provenance) not in {
            MembershipTenantProvenance,
            ExplicitSystemTenantProvenance,
            AuthorizedResourceTenantProvenance,
            DelegatedMemberTenantProvenance,
        }:
            raise ValueError("tenant provenance must be a typed admitted provenance")
        if provenance.organization_id != organization_id or provenance.principal != self.user_id:
            raise ValueError("tenant provenance does not match tenant identity")
        if type(provenance) in _VERIFIED_TENANT_PROVENANCES:
            if admission != "verified":
                raise ValueError("membership tenant provenance requires verified admission")
        elif admission != "none":
            raise ValueError("system and resource tenant provenance require admission none")
        if isinstance(self, DelegatedMemberAppContext) != isinstance(
            provenance, DelegatedMemberTenantProvenance
        ):
            raise ValueError(
                "a delegated member context and delegated member provenance are one "
                "thing: neither may be worn without the other"
            )
        seal = self._tenant_context_seal
        if type(seal) is not _TenantContextSeal:
            raise ValueError("tenant context requires a typed private binding")
        if (
            seal.organization_id != organization_id
            or seal.principal != self.user_id
            or seal.provenance != provenance
        ):
            raise ValueError("tenant private binding cannot be replaced")
        object.__setattr__(self, "organization_id", organization_id)
        object.__setattr__(self, "organization_admission", admission)
        object.__setattr__(
            self, "_organization_admission_binding", organization_binding or organization_id
        )
        object.__setattr__(
            self,
            "_organization_admission_provenance_binding",
            provenance_binding or admission,
        )


#: Provenances that ARE an admitted membership. Two kinds of evidence answer
#: "this principal is a member of this organization, proved live": a verified
#: HTTP admission, and a delegated member turn's ``MembershipProof``. Both mint
#: ``organization_admission="verified"``; everything else mints "none".
_VERIFIED_TENANT_PROVENANCES = {MembershipTenantProvenance, DelegatedMemberTenantProvenance}

#: The origin classes that say a PERSON initiated the work through a UI. A
#: delegated member context may never wear one: there is no interactive human
#: inside it, and anything gating on "a person is here right now" must refuse.
_ATTESTED_ORIGIN_CLASSES = frozenset({"human", "client_auto", "api"})


@dataclass(frozen=True)
class DelegatedMemberAppContext(TenantAppContext):
    """A system worker acting FOR a proved member on a verified channel.

    THE PROBLEM IT CLOSES. The Chief of Staff answers a text. The SMS worker ran
    that turn under ``system_app_context``, which mints
    ``organization_admission="none"`` — so every tenant-gated tool on the staff
    belt refused: the assistant could not text the person back, could not notify
    them, could not drive their browser. The person's identity HAD been proved
    (the carrier verified the number), but there was no boundary that could say
    so, because the only "verified" admission in the platform came from a live
    HTTP request.

    WHAT IT IS, AND IS NOT. It is admitted as a MEMBER — ``organization_admission
    == "verified"`` — because a membership was proved LIVE for this turn against
    ``iam.memberships``, not inferred, not remembered, not claimed. It is NOT a
    signed-in session: it carries no token and no JWT claims, never an admin
    tier, and its ``origin_class`` is ``delegated_member``, which is the word
    every downstream reader sees. Anything that requires an interactive human
    (recent-auth on a reveal, a consent click, a credential fill) must refuse
    here, and the absence of a token makes recent-auth fail closed by
    construction rather than by anyone remembering to check.

    It cannot be built. ``delegated_member_context`` is the only door; the
    provenance it needs cannot exist without a ``MembershipProof``, and a
    ``MembershipProof`` cannot exist without the boundary's private mint token.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.organization_admission != "verified":
            raise ValueError("a delegated member context is a verified membership admission")
        if not self.is_authenticated:
            raise ValueError("a delegated member context acts for an identified member")
        if self.origin_class in _ATTESTED_ORIGIN_CLASSES:
            raise ValueError(
                f"a delegated member context may not claim origin_class "
                f"{self.origin_class!r}: no interactive human is inside it"
            )
        if self.token is not None:
            raise ValueError(
                "a delegated member context carries no session token — it is not a "
                "signed-in session, and a token here would make recent-auth gates "
                "pass for a turn with nobody at the keyboard"
            )
        if isinstance(self.metadata, dict) and self.metadata.get("jwt_claims") is not None:
            raise ValueError(
                "a delegated member context carries no JWT claims — recent-auth and "
                "every other session-freshness gate must fail closed here"
            )
        if self.is_admin or self.admin_level is not None:
            raise ValueError(
                "a delegated member context never carries an admin tier: delegation "
                "conveys the member's own reach, never more"
            )
        if self.system_run:
            raise ValueError(
                "system_run marks unattended machine work kept out of people's chat "
                "lists; a delegated turn is a real member's conversation"
            )


@dataclass(frozen=True)
class OrganizationFreeAppContext(AppContext):
    """An explicitly organization-free HTTP operation; it cannot enter tenant sinks."""

    organization_id: None = field(default=None, init=False)
    organization_admission: Literal["none"] = field(default="none", init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        object.__setattr__(self, "organization_id", None)
        object.__setattr__(self, "organization_admission", "none")
        object.__setattr__(self, "claimed_organization_id", None)
        object.__setattr__(self, "_organization_admission_binding", None)
        object.__setattr__(self, "_organization_admission_provenance_binding", None)
        object.__setattr__(self, "_tenant_provenance", None)
        object.__setattr__(self, "_tenant_context_seal", None)


def _own_conversation_for_system_run(ctx: AppContext, kwargs: dict[str, Any]) -> dict[str, Any]:
    """A context that BECOMES a system run gets its own conversation and request.

    Every stored run writes its full history (messages + conversation config).
    A machine call made inside a person's turn (the title labeler, a held code
    call, a RAG judge) that kept the person's ``conversation_id`` would write
    its prompt, its answer and its config INTO that person's chat. So the
    transition into a system run mints a fresh conversation linked to the one it
    ran inside (``parent_conversation_id``) and a fresh request id, unless the
    caller names them explicitly.
    """
    if "conversation_id" in kwargs or not ctx.conversation_id:
        return kwargs
    owned = dict(kwargs)
    owned["conversation_id"] = str(uuid4())
    owned.setdefault("parent_conversation_id", ctx.conversation_id_for_lineage)
    if "request_id" not in owned:
        owned["request_id"] = str(uuid4())
        owned.setdefault("parent_request_id", ctx.request_id or None)
        # Its own turn, the TREE's cap / admission / stop (``tree_request_id``).
        owned.setdefault("root_request_id", ctx.tree_request_id or None)
    return owned


def _context_init_fields(ctx: AppContext, **overrides: Any) -> dict[str, Any]:
    """Copy constructor fields without manufacturing a general wire format."""
    fields = {item.name: getattr(ctx, item.name) for item in dataclasses.fields(ctx) if item.init}
    fields.update(overrides)
    return fields


def _mint_tenant_context(
    fields: dict[str, Any],
    provenance: TenantProvenance,
) -> TenantAppContext:
    """Mint a sealed tenant value at a named package admission boundary."""
    if type(provenance) not in {
        MembershipTenantProvenance,
        ExplicitSystemTenantProvenance,
        AuthorizedResourceTenantProvenance,
        DelegatedMemberTenantProvenance,
    }:
        raise ValueError("tenant provenance must be typed")
    fields["organization_id"] = provenance.organization_id
    fields["user_id"] = provenance.principal
    admission: Literal["none", "verified"] = (
        "verified" if type(provenance) in _VERIFIED_TENANT_PROVENANCES else "none"
    )
    fields["organization_admission"] = admission
    fields["_organization_admission_binding"] = provenance.organization_id
    fields["_organization_admission_provenance_binding"] = admission
    fields["_tenant_provenance"] = provenance
    fields["_tenant_context_seal"] = _TenantContextSeal(
        organization_id=provenance.organization_id,
        principal=provenance.principal,
        provenance=provenance,
    )
    if isinstance(provenance, DelegatedMemberTenantProvenance):
        return DelegatedMemberAppContext(**fields)
    return TenantAppContext(**fields)


def require_tenant_context(ctx: AppContext) -> TenantAppContext:
    """Promote only an already verified HTTP admission into a tenant context."""
    if isinstance(ctx, TenantAppContext):
        return ctx
    if isinstance(ctx, OrganizationFreeAppContext):
        raise ValueError("organization-free contexts cannot be promoted to tenant contexts")
    if ctx.organization_admission != "verified" or not ctx.organization_id:
        raise ValueError("verified organization admission is required")
    provenance = MembershipTenantProvenance(ctx.organization_id, ctx.user_id)
    return _mint_tenant_context(_context_init_fields(ctx), provenance)


def organization_free_context(ctx: AppContext) -> OrganizationFreeAppContext:
    """Clear tenancy while retaining the incoming claim only for diagnostics."""
    if isinstance(ctx, OrganizationFreeAppContext):
        return ctx
    metadata = dict(ctx.metadata)
    metadata["organization_free_diagnostic"] = {
        "claimed_organization_id": ctx.claimed_organization_id or ctx.organization_id,
        "organization_admission": ctx.organization_admission,
    }
    fields = _context_init_fields(
        ctx,
        metadata=metadata,
        claimed_organization_id=None,
        _organization_admission_binding=None,
        _organization_admission_provenance_binding=None,
        _tenant_provenance=None,
        _tenant_context_seal=None,
    )
    fields.pop("organization_id", None)
    fields.pop("organization_admission", None)
    return OrganizationFreeAppContext(**fields)


def _canonical_claimed_organization(value: object, field_name: str) -> str:
    try:
        return str(UUID(str(value).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError(f"{field_name} must be a valid UUID") from exc


def tenant_resource_context(
    ctx: AppContext,
    admission: AuthorizedResourceAdmission,
    *,
    organization_id: str | None = None,
) -> TenantAppContext:
    """Return a new sealed tenant operation for an already-authorized resource."""
    if type(admission) is not AuthorizedResourceAdmission:
        raise ValueError("admission must be typed authorized resource evidence")
    if isinstance(ctx, OrganizationFreeAppContext):
        raise ValueError("organization-free contexts cannot bootstrap resource tenancy")
    if isinstance(ctx, TenantAppContext):
        raise ValueError("admitted tenant contexts cannot be retargeted to a resource")
    if not ctx.is_authenticated:
        raise ValueError("authenticated base context is required")
    if ctx.organization_admission == "malformed":
        raise ValueError("malformed organization admission cannot bootstrap resource tenancy")
    _require_principal(ctx.user_id, "authenticated principal")
    if ctx.user_id != admission.principal:
        raise ValueError("authenticated principal does not match resource admission")
    expected_organization_id = admission.organization_id
    claims: tuple[tuple[str, object | None], ...] = (
        ("organization_id", ctx.organization_id),
        ("claimed_organization_id", ctx.claimed_organization_id),
        ("explicit organization_id", organization_id),
    )
    for field_name, claim in claims:
        if claim is not None and _canonical_claimed_organization(claim, field_name) != expected_organization_id:
            raise ValueError(f"{field_name} does not match resource admission organization")
    provenance = AuthorizedResourceTenantProvenance(admission)
    metadata = dict(ctx.metadata)
    metadata["resource_tenant_diagnostic_prior_admission"] = ctx.organization_admission
    fields = _context_init_fields(
        ctx,
        organization_admission="none",
        claimed_organization_id=None,
        request_id=ctx.request_id,
        operation_id=str(uuid4()),
        metadata=metadata,
        api_keys=dict(ctx.api_keys),
        initial_variables=dict(ctx.initial_variables),
        initial_overrides=dict(ctx.initial_overrides),
        client_tools=list(ctx.client_tools),
    )
    return _mint_tenant_context(fields, provenance)


def _resource_operation_base(parent_context: AppContext) -> AppContext:
    """Copy only request identity safe for a separately authorized resource operation."""
    if isinstance(parent_context, OrganizationFreeAppContext):
        raise ValueError("organization-free contexts cannot bootstrap resource operations")
    if type(parent_context) not in {AppContext, TenantAppContext}:
        raise ValueError("parent_context must be an authenticated base or sealed tenant context")
    if not parent_context.is_authenticated:
        raise ValueError("authenticated parent context is required")
    if parent_context.organization_admission == "malformed":
        raise ValueError("malformed organization admission cannot bootstrap resource operations")
    _require_principal(parent_context.user_id, "authenticated principal")

    # This intentionally names every carrier that crosses the boundary.  Do
    # not replace it with ``_context_init_fields``: tenant, execution, AI, and
    # provider state belong to the parent operation, never the newly admitted
    # resource operation.
    parent_operation_id = parent_context.operation_id
    return AppContext(
        emitter=parent_context.emitter,
        user_id=parent_context.user_id,
        email=parent_context.email,
        auth_type=parent_context.auth_type,
        is_authenticated=True,
        is_anonymous=parent_context.is_anonymous,
        is_admin=parent_context.is_admin,
        admin_level=parent_context.admin_level,
        admin_surface=parent_context.admin_surface,
        is_minor=parent_context.is_minor,
        fingerprint_id=parent_context.fingerprint_id,
        ip_address=parent_context.ip_address,
        user_agent=parent_context.user_agent,
        token=parent_context.token,
        request_id=parent_context.request_id,
        usage_admitted=parent_context.usage_admitted,
        operation_id=str(uuid4()),
        route=parent_context.route,
        source_app=parent_context.source_app,
        source_feature=parent_context.source_feature,
        metadata={"resource_operation_parent_operation_id": parent_operation_id},
    )


def _guest_resource_operation_base(parent_context: AppContext) -> AppContext:
    """Copy a middleware-admitted fingerprint guest for one resource operation.

    This is deliberately separate from :func:`_resource_operation_base`: a
    fingerprint is not a JWT and must never become generally authenticated just
    because it may read one host-authorized resource.
    """
    if isinstance(parent_context, OrganizationFreeAppContext):
        raise ValueError("organization-free contexts cannot bootstrap guest resource operations")
    if type(parent_context) is not AppContext:
        raise ValueError("parent_context must be a fingerprint guest base context")
    if parent_context.auth_type != "fingerprint" or parent_context.is_authenticated:
        raise ValueError("fingerprint guest parent context is required")
    if parent_context.organization_admission != "none":
        raise ValueError("fingerprint guest must not carry an organization admission")
    _require_principal(parent_context.user_id, "fingerprint guest principal")

    parent_operation_id = parent_context.operation_id
    return AppContext(
        emitter=parent_context.emitter,
        user_id=parent_context.user_id,
        email=parent_context.email,
        auth_type="fingerprint",
        is_authenticated=False,
        fingerprint_id=parent_context.fingerprint_id,
        ip_address=parent_context.ip_address,
        user_agent=parent_context.user_agent,
        request_id=parent_context.request_id,
        usage_admitted=parent_context.usage_admitted,
        operation_id=str(uuid4()),
        route=parent_context.route,
        source_app=parent_context.source_app,
        source_feature=parent_context.source_feature,
        metadata={"resource_operation_parent_operation_id": parent_operation_id},
    )


def tenant_guest_resource_context(
    ctx: AppContext,
    admission: AuthorizedResourceAdmission,
) -> TenantAppContext:
    """Seal one host-authorized resource operation for a fingerprint guest.

    The resource organization comes solely from typed host evidence made after
    the host's actual ownership/ACL check. This factory performs no I/O and is
    not a replacement for that check.
    """
    if type(admission) is not AuthorizedResourceAdmission:
        raise ValueError("admission must be typed authorized resource evidence")
    base = _guest_resource_operation_base(ctx)
    if base.user_id != admission.principal:
        raise ValueError("fingerprint guest principal does not match resource admission")
    return _mint_tenant_context(
        _context_init_fields(base), AuthorizedResourceTenantProvenance(admission)
    )


@asynccontextmanager
async def authorized_resource_operation(
    parent_context: AppContext,
    admission: AuthorizedResourceAdmission,
    *,
    expected_organization_id: str | None = None,
) -> AsyncGenerator[TenantAppContext]:
    """Install one freshly sealed operation for host-authorized resource work.

    ``expected_organization_id`` belongs to the new resource operation.  It is
    deliberately not compared to a sealed parent's tenant because a caller may
    be authorized to act on a resource owned by another organization.
    """
    if type(admission) is not AuthorizedResourceAdmission:
        raise ValueError("admission must be typed authorized resource evidence")
    base = _resource_operation_base(parent_context)
    if base.user_id != admission.principal:
        raise ValueError("authenticated principal does not match resource admission")
    if expected_organization_id is not None:
        if (
            _canonical_claimed_organization(expected_organization_id, "expected_organization_id")
            != admission.organization_id
        ):
            raise ValueError("expected_organization_id does not match resource admission organization")

    # The existing factory remains the sole sealing authority.  The private,
    # organization-free base prevents a sealed parent from retargeting it.
    resource_context = tenant_resource_context(base, admission)
    resource_context.metadata.clear()
    resource_context.metadata["resource_operation_parent_operation_id"] = parent_context.operation_id
    token = set_app_context(resource_context)
    try:
        yield resource_context
    finally:
        clear_app_context(token)


@asynccontextmanager
async def authorized_guest_resource_operation(
    parent_context: AppContext,
    admission: AuthorizedResourceAdmission,
) -> AsyncGenerator[TenantAppContext]:
    """Install one sealed host-authorized resource operation for a guest."""
    resource_context = tenant_guest_resource_context(parent_context, admission)
    token = set_app_context(resource_context)
    try:
        yield resource_context
    finally:
        clear_app_context(token)


# ── THE BACKGROUND DOOR'S APP ────────────────────────────────────────────────
# Work minted outside a request still belongs to an APP. `source_app` defaulted
# to the empty string, so every background door that named only its feature
# produced conversations, requests and usage rows with a BLANK app —
# unfilterable, uncostable, and dropped into the person-facing 'matrx' lane by
# chat.conversation_lane, where they show up in someone's chat sidebar as if
# they had started them. The host injects its own server name once at startup;
# the default is the platform server this package ships for.
#
# The DERIVED branches (a system block opened inside a live request) are
# deliberately untouched: there `source_app or ambient.source_app` already
# carries the real request's app, and that must keep winning.
_DEFAULT_SYSTEM_SOURCE_APP = "aidream"


def configure_default_system_source_app(source_app: str) -> None:
    """Host injection: the ``source_app`` a freshly minted system context carries."""
    global _DEFAULT_SYSTEM_SOURCE_APP
    value = str(source_app or "").strip()
    if not value:
        raise ValueError(
            "configure_default_system_source_app requires a non-empty source_app; "
            "the empty string is the defect this exists to close."
        )
    _DEFAULT_SYSTEM_SOURCE_APP = value


#: Host injection: called with every feature a system context MINTS. It ANNOUNCES an
#: unregistered one (log + error capture) and never blocks — validation offers, never
#: blocks. Default: no check (a bare package has no feature registry).
_FEATURE_MINT_CHECK: Callable[[str], Awaitable[None]] | None = None


def configure_feature_mint_check(check: Callable[[str], Awaitable[None]] | None) -> None:
    """Host injection: the check every ``system_app_context`` feature passes through."""
    global _FEATURE_MINT_CHECK
    _FEATURE_MINT_CHECK = check


async def _announce_minted_features(*features: Any) -> None:
    """Run the host's mint check on each feature; a failing check never stops the work."""
    check = _FEATURE_MINT_CHECK
    if check is None:
        return
    for feature in features:
        if not isinstance(feature, str) or not feature.strip():
            continue
        try:
            await check(feature.strip())
        except Exception as exc:  # noqa: BLE001 — an announcement must never block the work
            from matrx_utils import vcprint

            vcprint(
                f"[system_app_context] feature mint check failed for {feature!r}: "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )


@asynccontextmanager
async def tenant_system_context(
    feature: str,
    *,
    user_id: str,
    organization_id: str,
    # None = "the caller named no app"; the body resolves it to the host's
    # server (_DEFAULT_SYSTEM_SOURCE_APP). The empty string is never a value.
    source_app: str | None = None,
    label: str | None = None,
    **overrides: Any,
) -> AsyncGenerator[TenantAppContext]:
    """Establish or reuse an explicitly owned non-HTTP tenant context."""
    try:
        canonical_organization_id = str(UUID(str(organization_id).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError("organization_id must be a valid UUID") from exc

    _require_principal(user_id, "user_id")
    if overrides.get("organization_admission", "none") != "none":
        raise ValueError("tenant system contexts cannot claim verified HTTP admission")
    for private_field in (
        "_organization_admission_binding",
        "_organization_admission_provenance_binding",
        "_tenant_provenance",
        "_tenant_context_seal",
    ):
        if private_field in overrides:
            raise ValueError(f"{private_field} is not overrideable")
    for identity_field in ("user_id", "organization_id", "is_authenticated", "auth_type"):
        if identity_field in overrides:
            raise ValueError(f"{identity_field} is not overrideable")
    overrides.pop("organization_admission", None)
    overrides.pop("claimed_organization_id", None)

    existing = try_get_app_context()
    if existing is not None:
        tenant = require_tenant_context(existing)
        if tenant.organization_id != canonical_organization_id:
            raise ValueError("tenant system context organization does not match ambient context")
        if tenant.user_id != user_id:
            raise ValueError("tenant system context principal does not match ambient context")
        if tenant is existing:
            yield tenant
            return
        token = set_app_context(tenant)
        try:
            yield tenant
        finally:
            clear_app_context(token)
        return

    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    overrides.setdefault("origin_class", "system")
    fields: dict[str, Any] = {
        "emitter": ConsoleEmitter(label or feature, accumulate=False),
        "user_id": user_id,
        "auth_type": "token",
        "is_authenticated": True,
        "organization_id": canonical_organization_id,
        "organization_admission": "none",
        "claimed_organization_id": None,
        "request_id": str(uuid4()),
        "operation_id": str(uuid4()),
        "is_internal_agent": True,
        "store": True,
        # NEVER MINT AN UNATTRIBUTED CONTEXT — see _DEFAULT_SYSTEM_SOURCE_APP.
        "source_app": source_app or _DEFAULT_SYSTEM_SOURCE_APP,
        "source_feature": feature,
    }
    fields.update(overrides)
    ctx = _mint_tenant_context(
        fields,
        ExplicitSystemTenantProvenance(canonical_organization_id, user_id, feature),
    )
    token = set_app_context(ctx)
    try:
        yield ctx
    finally:
        clear_app_context(token)


# ---------------------------------------------------------------------------
# ContextVar storage — one slot per async task / request
# ---------------------------------------------------------------------------

_app_context: ContextVar[AppContext | None] = ContextVar("app_context", default=None)

# 🚨 THE REQUEST CONTEXT IS CARRIED ACROSS EVERY HOP. ``matrx_utils.detached_task``
# spawns fire-and-forget work in a FRESH contextvars Context so a child never
# inherits the parent's open transaction connection — and until 2026-09-17 that
# also dropped this variable, so ~110 call sites re-minted an AppContext by hand
# (or forgot, and died with "No AppContext is set", or minted one without the
# organization and landed work in the wrong tenant). Registering the carrier
# here means the identity crosses the hop unchanged while the transaction state
# still does not. Nothing is manufactured: an unset context stays unset.
#
# The registry first shipped in matrx-utils 2.0.47 (this package's floor). The
# import is guarded so a stale matrx-utils degrades to the pre-2.0.47 behavior
# — detached tasks start without the context, exactly as before — and says so
# once, loudly, instead of failing to import; the sibling-floor guard keeps our
# own deployment from ever running that combination.


def _register_detached_context_carrier() -> None:
    try:
        from matrx_utils.utils.detached_task import register_detached_context_carrier
    except ImportError:
        import logging

        logging.getLogger("matrx_connect.context").warning(
            "the installed matrx-utils does not export register_detached_context_carrier: "
            "detached tasks will NOT inherit the ambient AppContext. Upgrade matrx-utils to "
            ">= 2.0.47 (the floor this package declares)."
        )
        return
    register_detached_context_carrier(_app_context)


_register_detached_context_carrier()


def set_app_context(ctx: AppContext) -> Token:
    return _app_context.set(ctx)


def get_app_context() -> AppContext:
    ctx = _app_context.get(None)
    if ctx is None:
        raise RuntimeError(
            "No AppContext is set. Ensure AuthMiddleware is registered and running "
            "before this code path."
        )
    return ctx


def tree_request_id_of(ctx: Any) -> str:
    """``ctx.tree_request_id`` for any context-shaped value (a test stub included):
    ``root_request_id or request_id``, ``""`` for None."""
    if ctx is None:
        return ""
    return str(getattr(ctx, "root_request_id", None) or getattr(ctx, "request_id", "") or "")


def try_get_app_context() -> AppContext | None:
    return _app_context.get(None)


def admin_surface_active(ctx: AppContext | None = None) -> bool:
    """True only for an ADMIN acting from an ADMIN SURFACE (THE ADMIN LANE, 2026-09-25).

    ``ctx`` defaults to the ambient context; no context reads as False (fail closed).
    This is the one question an admin-only tool or an admin-reach branch asks — never
    ``ctx.is_admin`` alone, which is merely who the person is, not where they are.
    """
    ctx = ctx if ctx is not None else _app_context.get(None)
    return bool(
        ctx is not None
        and getattr(ctx, "is_admin", False)
        and getattr(ctx, "admin_surface", False)
    )


def admin_lane_active(ctx: AppContext | None = None, *, user_id: str | None = None) -> bool:
    """True only for a verified ADMIN acting from the ADMIN SYSTEM — the ONE admin-reach question.

    Arman's rule (2026-09-25/26, restated 2026-10-08): platform admins keep FULL access inside
    the admin system and only there; on a user page an admin is an ordinary person. An
    admin-reach door asks this AFTER its access kernel refused, so an ordinary person — and an
    admin on a user page — is never affected. Two lawful ways in, both verified upstream:

    * the HEADER LANE — the auth boundary admitted this request's organization through the
      admin lane (``metadata["organization_admitted_by"] == "admin_lane"``, set only by
      ``AuthMiddleware`` after the host re-verified the caller in its admin registry for the
      platform tenant, on a request carrying ``x-matrx-admin-lane: 1``, and audited it);
    * the ADMIN SURFACE — the request/run was started from an admin-mounted route
      (``admin_surface_active``).

    ``user_id``, when given, must be THIS context's actor (another actor reads False). No
    context, a non-admin, or neither lane reads False (fail closed).
    """
    ctx = ctx if ctx is not None else _app_context.get(None)
    if ctx is None or not getattr(ctx, "is_admin", False):
        return False
    if user_id is not None and str(getattr(ctx, "user_id", "") or "") != str(user_id):
        return False
    if getattr(ctx, "admin_surface", False):
        return True
    metadata = getattr(ctx, "metadata", None)
    metadata = metadata if isinstance(metadata, dict) else {}
    return metadata.get("organization_admitted_by") == "admin_lane"


def admin_tool_authorized(ctx: AppContext | None = None) -> bool:
    """True for an ADMIN running an admin-only TOOL — from ANY surface (Arman, 2026-10-07).

    An admin tool (the ``sql`` tool, the errors tool, admin browser tools) is a capability
    an admin deliberately put on their own agent, so it works wherever that agent runs,
    a normal chat included. The admin lane (``admin_surface_active``) governs AMBIENT reach —
    what a normal page shows an admin — and never refuses a tool the admin chose. A
    non-admin is always refused; no context reads as False (fail closed).
    """
    ctx = ctx if ctx is not None else _app_context.get(None)
    return bool(ctx is not None and getattr(ctx, "is_admin", False))


def admin_tool_level(ctx: AppContext | None = None) -> str | None:
    """The admin tier an admin-only tool runs under (see ``admin_tool_authorized``)."""
    ctx = ctx if ctx is not None else _app_context.get(None)
    if not admin_tool_authorized(ctx):
        return None
    return getattr(ctx, "admin_level", None)


def clear_app_context(token: Token) -> None:
    _app_context.reset(token)


def _identity_matches(ctx: AppContext, user_id: str, organization_id: str) -> bool:
    """Same actor, same organization — the ambient context IS the requested one."""
    ambient_org = str(ctx.organization_id or "").strip().lower()
    return str(ctx.user_id or "") == str(user_id or "") and ambient_org == organization_id.lower()


def _key_fingerprint(value: object) -> str:
    """sha256 of a key value — how ``own_api_key_fingerprints`` names a key without holding it."""
    import hashlib

    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


_SYSTEM_CONTEXT_PRIVATE_FIELDS = (
    "_organization_admission_binding",
    "_organization_admission_provenance_binding",
    "_tenant_provenance",
    "_tenant_context_seal",
)


def _derive_system_identity(
    ambient: AppContext,
    *,
    feature: str,
    user_id: str,
    organization_id: str,
    source_app: str | None,
    overrides: dict[str, Any],
) -> AppContext:
    """An ambient context re-pointed at the identity a system caller named.

    The request carriers survive (emitter, request_id, route, api keys,
    metadata, client tools) so streaming and attribution keep working; the
    IDENTITY is replaced, never merged. A different actor never inherits the
    ambient actor's admin tier, token or email — that would be a privilege
    leak dressed as convenience.
    """
    fields = _context_init_fields(ambient)
    for private_field in _SYSTEM_CONTEXT_PRIVATE_FIELDS:
        fields[private_field] = None
    same_actor = str(ambient.user_id or "") == str(user_id or "")
    fields.update(
        {
            "user_id": user_id,
            "organization_id": organization_id,
            "organization_admission": "none",
            "claimed_organization_id": None,
            "auth_type": "token",
            "is_authenticated": True,
            "is_admin": ambient.is_admin if same_actor else False,
            "admin_level": ambient.admin_level if same_actor else None,
            "ai_watch": ambient.ai_watch if same_actor else False,
            "admin_surface": ambient.admin_surface if same_actor else False,
            "email": ambient.email if same_actor else None,
            "token": ambient.token if same_actor else None,
            "operation_id": str(uuid4()),
            "is_internal_agent": True,
            "store": True,
            "source_app": source_app or ambient.source_app,
            "source_feature": feature,
            "origin_class": "system",
            "metadata": dict(ambient.metadata),
            # A system run spends OUR keys and charges: the person's own vault keys
            # never fund it (owner ruling 2026-10-15 #6), whoever it acts for.
            "api_keys": {
                name: value
                for name, value in ambient.api_keys.items()
                if _key_fingerprint(value) not in ambient.own_api_key_fingerprints
            },
            "own_api_key_fingerprints": frozenset(),
            "initial_variables": dict(ambient.initial_variables),
            "initial_overrides": dict(ambient.initial_overrides),
            "client_tools": list(ambient.client_tools),
        }
    )
    fields.update(overrides)
    return AppContext(**fields)


#: Features whose dropped same-identity overrides were already announced (once per process).
_DROPPED_OVERRIDES_ANNOUNCED: set[str] = set()


def _announce_dropped_overrides(feature: str, overrides: dict[str, Any]) -> None:
    """Say, once per feature, which overrides the same-identity no-op did not apply. The live
    request keeps its own context by design; a caller that needs its overrides beside it passes
    ``isolated=True`` (a parked turn's continuation lost its channel metadata and narrowed
    authority here, silently, until 2026-10-24)."""
    if feature in _DROPPED_OVERRIDES_ANNOUNCED:
        return
    _DROPPED_OVERRIDES_ANNOUNCED.add(feature)
    import logging

    logging.getLogger(__name__).warning(
        "[system_app_context] %s: the ambient context is already this actor and organization, so "
        "it is used as is and these overrides were NOT applied: %s. Pass isolated=True to run "
        "beside the live request with them.",
        feature,
        sorted(overrides),
    )


@asynccontextmanager
async def system_app_context(
    feature: str,
    *,
    user_id: str,
    organization_id: str,
    # None = "the caller named no app"; the body resolves it to the host's
    # server (_DEFAULT_SYSTEM_SOURCE_APP). The empty string is never a value.
    source_app: str | None = None,
    label: str | None = None,
    isolated: bool = False,
    **overrides: Any,
) -> AsyncGenerator[AppContext]:
    """Guarantee an ambient AppContext for work running OUTSIDE a request.

    Background work — a ``detached_task`` spawned with no ambient context, a
    queue worker, a NOTIFY listener, a scheduled run — starts with an EMPTY
    contextvars Context. Anything it calls that reaches for
    ``get_app_context()`` (every agent run does) dies with "No AppContext is
    set. Ensure AuthMiddleware is registered and running…" — a message that
    blames middleware for a request that never existed.

    This is the sanctioned re-entry point, and it has ONE rule: **the identity
    comes from the durable record the work belongs to, never from a default.**

    * ``organization_id`` is REQUIRED and must be an organization id. The
      record being processed (a run, a job, an enrollment, a claim) carries the
      organization it belongs to; pass that. Platform-owned automation with no
      customer record passes the platform organization *explicitly*. There is
      no ``None`` — an organization-less system context is how work silently
      landed in a personal or system tenant, or crashed hours later on a
      NOT NULL column, from 2026-06 to 2026-09-17.
    * ``user_id`` is the actor the record names (its owner / creator), or the
      empty string for genuinely actor-less platform work.

    **Ambient rule.** When a context is already ambient:

    * same actor + same organization → it is yielded untouched (idempotent, so
      an entry point with both an HTTP caller and a background caller stays
      safe; keyword overrides are NOT applied to a context this call did not
      mint);
    * a DIFFERENT actor or organization → a derived context carrying the
      requested identity is installed for the block and restored on exit. The
      request carriers (emitter, request id, api keys, metadata) survive so
      streaming and attribution keep working. Until 2026-09-17 this case
      silently yielded the ambient context and DROPPED the identity the caller
      named — hindsight replays ran as the wrong user, sweeps ran in whichever
      organization the triggering person happened to have selected.

    **Isolation.** ``isolated=True`` turns the same-identity no-op OFF: a
    derived context is minted through the same path, installed for the block
    and restored on exit even when the ambient context already IS this actor in
    this organization. It is for an in-process side computation running BESIDE
    a live request for the same person — an auto-ingest NER pass fired from a
    save hook, a derivation fanned out from a chat turn. Such work must never
    write into the request's stream: the ambient context carries the person's
    live emitter, conversation id and persistence intent, so yielding it would
    stream the side computation's events onto their screen and file its
    transcript in their conversation. Pass the side computation's own carriers
    as keyword overrides — ``emitter=`` (a fresh emitter replaces the ambient
    one), ``conversation_id=``, ``store=``, ``system_run=`` — and everything
    not overridden still comes from the ambient context (request_id, api_keys,
    metadata), so the work stays attributable to the request that caused it.
    The refusals are unchanged: ``isolated=True`` never permits an identity or
    private-binding override the primitive already refuses.

    The minted context PERSISTS by default (``store=True`` — every AI run keeps its
    history, owner ruling 2026-10-05; ``store=False`` is only a PERSON's own
    ephemeral choice, never an internal one) and
    marked ``is_internal_agent`` — it is a machine call, not a user turn. Pass
    any AppContext field as a keyword to override (``system_run=True`` for machine work —
    full history, kept out of people's chat lists; ``conversation_type=...``).

    Install it at the FUNNEL every background dispatcher passes through, not at
    each agent call site — one guard covers every stage downstream.
    """
    try:
        canonical_organization_id = str(UUID(str(organization_id).strip()))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError(
            f"system_app_context({feature!r}): organization_id is required and must be "
            f"an organization id, got {organization_id!r}. Pass the organization the "
            "record being processed belongs to (its organization_id column); platform-"
            "owned automation passes the platform organization explicitly. A system "
            "context never runs without one."
        ) from exc
    for private_field in _SYSTEM_CONTEXT_PRIVATE_FIELDS:
        if private_field in overrides:
            raise ValueError(f"{private_field} is not overrideable")
    for identity_field in ("user_id", "organization_id"):
        if identity_field in overrides:
            raise ValueError(f"{identity_field} is a named argument, not an override")

    # The stamp this context will carry is checked against the host's registry HERE,
    # where it is minted — an unregistered one is announced (never refused), so a new
    # harness cannot silently mint a stamp its own conversations cannot continue under.
    await _announce_minted_features(feature, overrides.get("source_feature"))

    existing = try_get_app_context()
    if existing is not None:
        same_identity = _identity_matches(existing, user_id, canonical_organization_id)
        if same_identity and not isolated:
            if overrides:
                _announce_dropped_overrides(feature, overrides)
            yield existing
            return
        derived = _derive_system_identity(
            existing,
            feature=feature,
            user_id=user_id,
            organization_id=canonical_organization_id,
            source_app=source_app,
            overrides=overrides,
        )
        from matrx_utils import vcprint

        if same_identity:
            vcprint(
                f"[system_app_context] {feature}: isolated=True — minting a separate "
                f"context beside the ambient one for user={user_id or '-'} "
                f"org={canonical_organization_id}, so this side computation never "
                "emits, persists or borrows the live request's stream.",
                color="cyan",
                log_level="INFO",
            )
        else:
            vcprint(
                f"[system_app_context] {feature}: ambient context is "
                f"user={existing.user_id or '-'} org={existing.organization_id or '-'}; "
                f"installing the requested identity user={user_id or '-'} "
                f"org={canonical_organization_id} for this block (request carriers kept).",
                color="cyan",
                log_level="INFO",
            )
        token = set_app_context(derived)
        try:
            yield derived
        finally:
            clear_app_context(token)
        return

    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    # Background work is class "system" unless the caller names another MACHINE
    # class (the scheduler passes origin_class="scheduled"). Attested classes
    # (human/client_auto/api) cannot be minted here — reconcile_origin at the
    # persistence gate overrules them, since a system context has no HTTP witness.
    overrides.setdefault("origin_class", "system")

    # DEFAULTS overridable by kwargs — the docstring promises `store=True` /
    # `auth_type=...` etc. work as overrides, so no default may be a literal
    # kwarg beside **overrides (that made `store=True` a TypeError, found
    # 2026-08-17 while probing the snapshot-capture defect).
    fields: dict[str, Any] = {
        "emitter": ConsoleEmitter(label or feature, accumulate=False),
        "user_id": user_id,
        "auth_type": "token",
        "is_authenticated": True,
        "organization_id": canonical_organization_id,
        "request_id": str(uuid4()),
        "operation_id": str(uuid4()),
        "is_internal_agent": True,
        "store": True,
        # NEVER MINT AN UNATTRIBUTED CONTEXT — see _DEFAULT_SYSTEM_SOURCE_APP.
        "source_app": source_app or _DEFAULT_SYSTEM_SOURCE_APP,
        "source_feature": feature,
    }
    fields.update(overrides)
    ctx = AppContext(**fields)
    token = set_app_context(ctx)
    try:
        yield ctx
    finally:
        try:
            clear_app_context(token)
        except Exception:  # noqa: BLE001 — teardown must never mask the body's error
            pass


@asynccontextmanager
async def child_agent_context(
    label: str, *, emit_lifecycle: bool = True, conversation_id: str | None = None
) -> AsyncGenerator[AppContext]:
    """Fork AppContext for a child agent and emit init/completion lifecycle events.

    ``emit_lifecycle=False`` (an invisible handoff): the sub_agent INIT and the
    SUCCESS completion are suppressed so the child reads as one seamless stream —
    but the FAILED completion is ALWAYS emitted (the client's only rewind signal
    to truncate a partially-streamed child answer).

    ``conversation_id``: run the child inside this EXISTING conversation instead
    of a freshly minted uuid (fork-mode collaboration). It must be set HERE, not
    overridden after entry — the sub_agent INIT event and every child-fork hook
    read the forked context's conversation_id, so a later override would
    announce a phantom conversation to the FE. The caller owns the access check.

    Handles the full sub-agent lifecycle in one place:
    - Forks the current AppContext with a new conversation_id and operation_id
    - Sets the forked context as the active context for the duration of the block
    - Gives the child its own isolated ReservationTracker so its reserved rows
      never bleed into the parent's fail_all_pending() sweep
    - Invokes every registered child-fork hook (see ``register_child_fork_hook``),
      giving downstream packages a way to fork their own scoped state (e.g.
      a write coordinator / Session) without matrx-connect needing to know
      about them.
    - Emits a ``sub_agent`` init event (with parent_operation_id) before yielding
    - Emits a ``sub_agent`` completion event (success or failed) on exit
    - Restores the parent context and tracker when done

    Usage::

        async with child_agent_context("my_label") as child_ctx:
            agent = await Agent.from_prompt(prompt_id)
            result = await agent.execute()

    The emitter used for events is always the *parent* emitter, since child agents
    share the same stream as the parent request.
    """
    from contextlib import AsyncExitStack

    from matrx_connect.context.operations import CompletionPayload, InitPayload
    from matrx_connect.reservations import ReservationTracker, _reservation_tracker

    parent_ctx = get_app_context()
    parent_operation_id = parent_ctx.operation_id or None
    sub_agent_operation_id = str(uuid4())

    child_ctx = parent_ctx.fork_for_child_agent(
        conversation_id or str(uuid4()),
        operation_id=sub_agent_operation_id,
    )
    # The child owns its own turn id; a stop / retry-now on any id of the tree
    # reaches it (the registry resolves a linked id to its root).
    from matrx_connect.request_controls import register_request_tree

    register_request_tree(child_ctx)
    token = set_app_context(child_ctx)

    # Give the child its own tracker so its reservations never bleed into the
    # parent's _records list. Without this, fail_all_pending() on the parent
    # would emit spurious "failed" events for child-owned rows.
    child_tracker_token = _reservation_tracker.set(ReservationTracker())

    emitter = parent_ctx.emitter
    # Outer try/finally guarantees context + tracker teardown even when
    # send_init itself raises (Bug 10-A fix).
    try:
        # Stamp the child's conversation_id onto the INIT so the FE can label
        # and deep-link the sub-agent's conversation the moment it starts (the
        # child streams on the SAME wire as the parent — without this the FE has
        # no handle to attribute or navigate to the child). Additive: metadata is
        # an open dict; existing consumers ignore the new key. agent_id is NOT
        # known here (run_agent stamps it via overrides after this fork) — the FE
        # reads it from the child cx_conversation row via this conversation_id.
        if emit_lifecycle:
            await emitter.send_init(
                InitPayload(
                    operation="sub_agent",
                    operation_id=sub_agent_operation_id,
                    parent_operation_id=parent_operation_id,
                    metadata={
                        "label": label,
                        "conversation_id": child_ctx.conversation_id or None,
                    },
                )
            )
        # Run registered child-fork hooks. Each hook is an async context
        # manager that runs INSIDE the child's AppContext (so it can read
        # child_ctx.* via get_app_context()) and is torn down BEFORE the
        # child context is restored. This is how matrx-ai's WriteCoordinator
        # forks a child scope so sub-agent writes don't pile into the
        # parent's queue.
        async with AsyncExitStack() as fork_stack:
            for hook in list(_child_fork_hooks):
                try:
                    await fork_stack.enter_async_context(hook(label, child_ctx))
                except Exception as hook_exc:
                    # A hook raising during enter is a programmer bug in the
                    # downstream package. Log and continue without that hook
                    # rather than killing the whole sub-agent run.
                    from matrx_utils import vcprint

                    vcprint(
                        f"[child_agent_context] fork hook raised on enter: "
                        f"{type(hook_exc).__name__}: {hook_exc} — continuing without it",
                        color="red",
                    )
                    from matrx_connect.streaming.error_capture import capture_error

                    await capture_error(
                        hook_exc,
                        kind="child_context_hook_failed",
                        request_id=child_ctx.request_id,
                        user_id=child_ctx.user_id,
                        conversation_id=child_ctx.conversation_id,
                        route="child_agent_context/fork_hook",
                        error_type=type(hook_exc).__name__,
                        payload={"label": label},
                    )
            try:
                yield child_ctx
            except Exception as agent_exc:
                # Agent body raised — notify the client, but swallow any secondary
                # error so we never mask the original agent exception (Bug 10-C fix).
                try:
                    await emitter.send_completion(
                        CompletionPayload(
                            operation="sub_agent",
                            operation_id=sub_agent_operation_id,
                            status="failed",
                            result={"label": label, "error": str(agent_exc)},
                        )
                    )
                except Exception:
                    pass
                raise
            else:
                # Agent body succeeded — send success.  Exceptions here propagate
                # normally without triggering a false "failed" event (Bug 10-B fix).
                # A contained loop failure does not raise, so the child execution
                # funnel marks it explicitly. Its FAILED completion is never
                # suppressed: invisible handoffs need it to rewind partial text.
                active_ctx = try_get_app_context()
                contained_error = (
                    active_ctx.metadata.get(_CHILD_AGENT_FAILURE_METADATA_KEY)
                    if active_ctx is not None and isinstance(active_ctx.metadata, dict)
                    else None
                )
                if contained_error:
                    await emitter.send_completion(
                        CompletionPayload(
                            operation="sub_agent",
                            operation_id=sub_agent_operation_id,
                            status="failed",
                            result={"label": label, "error": str(contained_error)},
                        )
                    )
                elif emit_lifecycle:
                    await emitter.send_completion(
                        CompletionPayload(
                            operation="sub_agent",
                            operation_id=sub_agent_operation_id,
                            status="success",
                            result={"label": label},
                        )
                    )
        # fork_stack exits here: hooks' __aexit__ run in reverse registration
        # order, BEFORE the child AppContext is torn down below. This is
        # the spot where the WriteCoordinator fork hook flushes the child's
        # queue.
    finally:
        _reservation_tracker.reset(child_tracker_token)
        clear_app_context(token)


_CHILD_AGENT_FAILURE_METADATA_KEY = "_matrx_child_agent_failure"


def mark_child_agent_failed(error: str) -> None:
    """Mark a contained child failure so its lifecycle exits as failed."""
    ctx = get_app_context()
    set_app_context(
        ctx.with_overrides(
            metadata={
                **ctx.metadata,
                _CHILD_AGENT_FAILURE_METADATA_KEY: error or "child agent did not complete",
            }
        )
    )


# ---------------------------------------------------------------------------
# Child-fork hook registry — downstream packages register hooks here.
# ---------------------------------------------------------------------------
#
# A child-fork hook is an async-context-manager factory:
#
#   async def my_hook(label: str, child_ctx: AppContext) -> AsyncContextManager:
#       async with something_new() as scope:
#           yield scope
#
# Hooks are called inside child_agent_context AFTER the child AppContext is
# set on the ContextVar and BEFORE control yields to user code. They are
# torn down (in reverse registration order) AFTER user code completes and
# BEFORE the child AppContext is restored. This is the right window for
# any per-sub-agent scoped state — e.g. matrx-ai registers a hook that
# opens a fresh WriteCoordinator so child writes flush on sub-agent exit
# rather than piling into the parent's queue.
#
# Registration is idempotent on identity (re-registering the same callable
# is a no-op). The list is process-global, set once at host configure()
# time.

_child_fork_hooks: list = []


def register_child_fork_hook(hook) -> None:
    """Register a callback fired on every child_agent_context entry.

    ``hook`` MUST be an async-context-manager factory: a callable that
    takes ``(label: str, child_ctx: AppContext)`` and returns an async
    context manager. Its ``__aenter__`` runs inside the child scope; its
    ``__aexit__`` runs before the child scope is torn down.

    Idempotent on identity — registering the same callable twice is a no-op.
    """
    if hook not in _child_fork_hooks:
        _child_fork_hooks.append(hook)


def unregister_child_fork_hook(hook) -> bool:
    """Remove a previously-registered hook. Returns True if removed."""
    try:
        _child_fork_hooks.remove(hook)
        return True
    except ValueError:
        return False
