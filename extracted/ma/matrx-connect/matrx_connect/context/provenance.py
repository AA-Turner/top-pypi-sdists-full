"""Origin-class provenance — the WITNESSED half of request attribution.

``source_app`` / ``source_feature`` are DECLARED labels: useful for grouping,
worthless for trust — any caller can claim any label. ``origin_class`` is the
TRUST axis: it answers "what kind of thing initiated this work" from facts the
platform itself observed (the auth credential, the HTTP route, the process
role, the execution lineage), never from what the caller says about itself.

The vocabulary
--------------
Attested classes (derivation-only — no code outside this module may produce
them as literals; ``scripts/check_origin_provenance.py`` fails the build when
one is STAMPED elsewhere — passed to a context constructor/fork, a
source-context stamper, or a row-creation/enqueue call, or assigned bare. That
guard is deliberately narrow, not broad: reading the class back (query filters,
dashboards, evidence records, adversarial tests) is always legal, because a
missed stamp is still caught by ``reconcile_origin`` below and by the DB CHECK,
while one false positive blocks every release):

* ``human``       — a person initiated this through a UI. Requires ALL of:
                    a live HTTP request (``ctx.route`` set), a real credential
                    (token/fingerprint), and the client's explicit
                    ``initiation="user"`` attestation on the request body.
* ``client_auto`` — client-side code triggered this without a direct user
                    action (page load effects, timers, auto-refresh). Same
                    witness requirements, ``initiation="auto"``.
* ``api``         — an HTTP caller that did not attest interactivity: coding
                    agents, scripts, curl, integrations. The honest default
                    for any HTTP request.

Machine classes (self-declarable — machine code naming itself a machine class
is harmless; the guard only forbids claiming UP the trust ladder):

* ``child_agent`` — forked mid-run by another agent (``fork_for_child_agent``).
                    PERSISTED only with a parent conversation: a parentless fork
                    records its root's class (``root_run_origin_class``) — a
                    server-side mandate run is never "started by another agent".
* ``workflow``    — a workflow run/step (``fork_for_workflow_step`` or the
                    workflow worker/runner contexts).
* ``scheduled``   — the scheduler fired it.
* ``system``      — server background work: sweeps, listeners, pipelines,
                    retries (``system_app_context`` default).
* ``delegated_member``
                  — a system worker acting FOR a proved member on a channel
                    that verified who is speaking (SMS, voice). Minted only by
                    ``delegated_member_context``, whose ``MembershipProof`` is
                    the witness. It sits BELOW the attested classes on purpose:
                    nobody is at a keyboard, so it may never be mistaken for
                    ``human`` — and it is not ``system`` either, because a real,
                    named, live-verified member is on the other end of the
                    channel, which is exactly what ``system`` cannot say.

``unknown`` exists only as the DB backfill value for pre-provenance history;
live code never writes it.

The one enforcement seam
------------------------
``reconcile_origin(ctx)`` runs at the persistence gate. It rebuilds the class
from the witness facts, compares against what the context claims, and when the
claim is not supported by the witness it OVERWRITES the claim with the derived
truth, records the contradiction in the witness payload, and screams. A lie
can therefore not land in the database quietly; at worst it lands corrected,
loudly, with the original claim preserved as evidence.
"""

from __future__ import annotations

from collections.abc import Callable
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext

ORIGIN_CLASS_HUMAN: Final = "human"
ORIGIN_CLASS_CLIENT_AUTO: Final = "client_auto"
ORIGIN_CLASS_API: Final = "api"
ORIGIN_CLASS_CHILD_AGENT: Final = "child_agent"
ORIGIN_CLASS_WORKFLOW: Final = "workflow"
ORIGIN_CLASS_SCHEDULED: Final = "scheduled"
ORIGIN_CLASS_SYSTEM: Final = "system"
ORIGIN_CLASS_DELEGATED_MEMBER: Final = "delegated_member"
ORIGIN_CLASS_UNKNOWN: Final = "unknown"

# Only derivable here — asserting interactivity requires a witness.
ATTESTED_ORIGIN_CLASSES: Final[tuple[str, ...]] = (
    ORIGIN_CLASS_HUMAN,
    ORIGIN_CLASS_CLIENT_AUTO,
    ORIGIN_CLASS_API,
)

# Self-declarable by machine code (claiming DOWN the trust ladder is honest).
MACHINE_ORIGIN_CLASSES: Final[tuple[str, ...]] = (
    ORIGIN_CLASS_CHILD_AGENT,
    ORIGIN_CLASS_WORKFLOW,
    ORIGIN_CLASS_SCHEDULED,
    ORIGIN_CLASS_SYSTEM,
    ORIGIN_CLASS_DELEGATED_MEMBER,
)

ORIGIN_CLASSES: Final[tuple[str, ...]] = ATTESTED_ORIGIN_CLASSES + MACHINE_ORIGIN_CLASSES

#: ``AppContext.metadata`` key a worker sets when it RE-RUNS a request it did not receive
#: (crash recovery after a deploy or a dead server). The value is the ORIGINAL request's
#: persisted witness, built by ``resumed_run_witness``: the run is still that request, so it
#: keeps the class its HTTP boundary witnessed instead of reading as background ``system`` work.
RESUMED_RUN_WITNESS_KEY: Final = "resumed_run_witness"

#: ``AppContext.metadata`` key a worker sets when it runs a NEW turn that CONTINUES a person's own
#: request — the answer a helper they started handed back, a wake-up they asked for. The value is
#: the ORIGINATING request's persisted witness, built by ``continued_run_witness`` from that
#: request's own row (never typed by the caller). The turn is the person's own work, so it keeps
#: the person class the original request's HTTP boundary witnessed; read as ``system`` it was
#: refused on a protected account and counted as system spend (live 2026-10-18).
CONTINUED_RUN_WITNESS_KEY: Final = "continued_run_witness"

#: ``AppContext.metadata`` key a worker sets when it runs a turn on a person's OWN TEXT that the host
#: proved is theirs: the inbound message was claimed by the door that answers it AND its sender is the
#: verified number of the person the turn runs as (the spend desk: Arman's reply to the morning spend
#: text, 2026-10-19 K4). Built by ``own_text_witness`` after both checks — never typed by a caller. The
#: turn is the person's own start, so it records ``human`` with the mark, never background ``system``.
OWN_TEXT_WITNESS_KEY: Final = "own_text_witness"

#: The classes a continuation may keep: a person at the keyboard or on a verified channel.
_PERSON_CLASSES: Final[tuple[str, ...]] = (ORIGIN_CLASS_HUMAN, ORIGIN_CLASS_DELEGATED_MEMBER)


def _process_role() -> str:
    try:
        from matrx_utils import get_runtime_env

        return str(get_runtime_env().role)
    except Exception:  # noqa: BLE001 — witness capture must never kill a request
        return ""


def derive_http_origin_class(
    *,
    route: str | None,
    auth_type: str,
    initiation: str | None,
) -> str:
    """Derive the origin class for an HTTP request at the scope funnel.

    Returns "" when there is no HTTP witness (route unset) — the persistence
    gate then derives a machine class from the remaining facts instead of this
    function guessing.
    """
    if not route:
        return ""
    if auth_type not in ("token", "fingerprint"):
        return ORIGIN_CLASS_API
    if initiation == "user":
        return ORIGIN_CLASS_HUMAN
    if initiation == "auto":
        return ORIGIN_CLASS_CLIENT_AUTO
    return ORIGIN_CLASS_API


def _derive_machine_class(ctx: AppContext) -> str:
    # A delegated member turn is a TYPE, not a label: even if its class were
    # dropped somewhere downstream, the witness still knows what this is and
    # must never quietly call it plain 'system' (which is what made the staff
    # turn refuse to text the person in the first place).
    from matrx_connect.context.app_context import DelegatedMemberAppContext

    if isinstance(ctx, DelegatedMemberAppContext):
        return ORIGIN_CLASS_DELEGATED_MEMBER
    if ctx.execution_kind == "workflow_run" or ctx.conversation_type == "workflow":
        return ORIGIN_CLASS_WORKFLOW
    if ctx.conversation_type == "scheduled":
        return ORIGIN_CLASS_SCHEDULED
    if ctx.is_internal_agent and ctx.parent_conversation_id:
        return ORIGIN_CLASS_CHILD_AGENT
    return ORIGIN_CLASS_SYSTEM


def root_fork_origin_class(parent: AppContext) -> str:
    """The origin class for an agent run forked from ``parent``.

    A run forked from a context that is itself running a conversation is a true
    sub-agent: ``child_agent``. A run forked from an HTTP request that runs NO
    conversation is not anyone's child — it is the root run of the caller (a
    person's coding agent through the MCP ``agent_run`` tool, a script, an
    integration). Calling that ``child_agent`` made a person's deliberate run
    read as automated sub-agent traffic in every usage report (2026-10-08:
    1,000+ ``mcp:*`` turns). Such a root run carries the caller's witnessed
    class instead (``api`` for an unattested token caller).

    Machine parents (system / scheduled / workflow / delegated member) keep
    ``child_agent`` deliberately: the usage gate and the tree budgets key off
    those classes, so re-classing machine forks would change who is gated.
    """
    if parent.conversation_id_for_lineage:
        return ORIGIN_CLASS_CHILD_AGENT
    derived = derive_http_origin_class(
        route=parent.route, auth_type=parent.auth_type, initiation=None
    )
    if not derived or parent.origin_class in MACHINE_ORIGIN_CLASSES:
        return ORIGIN_CLASS_CHILD_AGENT
    if parent.origin_class in ATTESTED_ORIGIN_CLASSES:
        # The same HTTP witness exists, so the caller's attested claim carries.
        return parent.origin_class
    return derived


def root_run_origin_class(ctx: AppContext) -> str:
    """The TRUE starter of a parentless agent run forked from machine work.

    The fork records the root parent's declared machine class under ``parent_origin_class``
    (``workflow`` / ``scheduled`` / ``system``); a fork that carried none is read from the
    remaining witness (a workflow run's execution, a scheduler conversation) and is otherwise
    background work: ``system``.
    """
    # A fork keeps its parent's context TYPE (``dataclasses.replace``): a fork under a staff turn
    # for a verified member (SMS / voice) was started on that member's word, not by the platform.
    from matrx_connect.context.app_context import DelegatedMemberAppContext

    if isinstance(ctx, DelegatedMemberAppContext):
        return ORIGIN_CLASS_DELEGATED_MEMBER
    metadata = ctx.metadata if isinstance(ctx.metadata, dict) else {}
    parent = str(metadata.get("parent_origin_class") or "")
    if parent in (ORIGIN_CLASS_WORKFLOW, ORIGIN_CLASS_SCHEDULED, ORIGIN_CLASS_SYSTEM):
        return parent
    if ctx.execution_kind == "workflow_run":
        return ORIGIN_CLASS_WORKFLOW
    if ctx.conversation_type == "scheduled" or ctx.execution_kind == "sch_run":
        return ORIGIN_CLASS_SCHEDULED
    return ORIGIN_CLASS_SYSTEM


def gate_origin_class(ctx: AppContext | None) -> str:
    """The origin class every GATE and DRIVER reads: ``reconcile_origin`` WITHOUT the root-run
    relabel. The relabel makes the RECORD honest (a parentless fork is not "started by another
    agent"); it must never move who is gated — the usage gate leaves ``system`` / ``scheduled``
    ungated, and ``platform.run_driver`` reads ``child_agent`` as ``sub_agent``. Persistence of a
    conversation / user request label reads ``reconcile_origin``; anything that DECIDES (a usage
    or approval gate, a driver, an execution row a driver reads, an SMS dispatcher context) reads
    this.
    """
    final, witness = reconcile_origin(ctx)
    relabel = witness.get("root_run_class") if isinstance(witness, dict) else None
    if isinstance(relabel, dict) and relabel.get("from"):
        return str(relabel["from"])
    return final


def build_origin_witness(ctx: AppContext) -> dict[str, Any]:
    """Snapshot the platform-observed facts this class derivation rests on."""
    return {
        "auth_type": ctx.auth_type,
        "route": ctx.route,
        "process_role": _process_role(),
        "execution_kind": ctx.execution_kind,
        "execution_id": ctx.execution_id,
        "is_internal_agent": ctx.is_internal_agent,
        "parent_conversation_id": ctx.parent_conversation_id,
        "conversation_type": ctx.conversation_type,
        "declared_class": ctx.origin_class or None,
        "declared_app": ctx.source_app or None,
        "declared_feature": ctx.source_feature or None,
        # The delegated-turn audit record (reason, channel, membership proof id),
        # so a row written inside a staff turn says on its face WHY a worker was
        # allowed to act as this member and which verification event admitted it.
        "delegated_member_admission": (ctx.metadata or {}).get("delegated_member_admission")
        if isinstance(ctx.metadata, dict)
        else None,
        # The run-as audit record: when a host runs a caller's work as ANOTHER account (the
        # AI Dream MCP runs a super admin's coding-agent AI work as the designated test
        # account), who really asked and why, so the request row stays honest about it.
        "run_as_admission": (ctx.metadata or {}).get("run_as_admission")
        if isinstance(ctx.metadata, dict)
        else None,
    }


def _is_worker_context(ctx: AppContext) -> bool:
    """True for a context a worker runs on: it DECLARES background ``system``, or declares nothing
    and has no live HTTP witness. A worker started from inside a live request
    (``system_app_context`` deriving from the ambient one) keeps that request's ``route`` as a
    carrier, but the route is the DOOR's witness, never the re-run request's: read as "a live
    request is its own witness", a person's own parked turn resumed from the action-request page
    lost its witness and was refused on a protected account (live 2026-10-24). A live request
    that declares nothing (``""`` with a route) is still its own witness."""
    declared = str(ctx.origin_class or "")
    if declared == ORIGIN_CLASS_SYSTEM:
        return True
    return declared == "" and not ctx.route


def resumed_run_witness(
    *,
    request_id: str,
    user_id: str,
    origin_class: str | None,
    origin_witness: dict[str, Any] | None,
) -> dict[str, Any]:
    """The record a worker carries (under ``RESUMED_RUN_WITNESS_KEY``) when it re-runs
    ``request_id``: that request's persisted class, its person, and the route + credential that
    witnessed it. Read back off the request's own row — never typed by the caller."""
    original = origin_witness if isinstance(origin_witness, dict) else {}
    return {
        "request_id": str(request_id),
        "user_id": str(user_id or ""),
        "origin_class": str(origin_class or ""),
        "route": original.get("route"),
        "auth_type": original.get("auth_type"),
    }


def _resumed_record(
    ctx: AppContext, contradictions: list[str]
) -> tuple[str, dict[str, Any]] | None:
    """The class a re-run request keeps from its ORIGINAL witness, with its record, or None.

    Applies only to the worker's own re-run (``_is_worker_context``: a declared ``system`` context,
    or one with no live HTTP witness — a live request is always its own witness), a context that
    declares nothing more specific than background ``system`` (a
    fork declaring ``child_agent`` / ``workflow`` keeps the request id and the metadata but is
    read from its own facts), and exactly the request the record names. A record that cannot
    support its class is a contradiction, never trusted.
    """
    if not _is_worker_context(ctx):
        return None
    metadata = ctx.metadata if isinstance(ctx.metadata, dict) else {}
    record = metadata.get(RESUMED_RUN_WITNESS_KEY)
    if not isinstance(record, dict):
        return None
    if not ctx.request_id or str(record.get("request_id") or "") != str(ctx.request_id):
        return None
    # The SAME person, as the continued reader requires. A record that names nobody (built before
    # the record carried ``user_id``) is refused, never assumed: refusing cannot widen trust.
    if not ctx.user_id or str(record.get("user_id") or "") != str(ctx.user_id):
        contradictions.append(
            "resumed run names a different person than the run, or none — not trusted"
        )
        return None
    recorded = str(record.get("origin_class") or "")
    if recorded not in ORIGIN_CLASSES:
        contradictions.append(f"resumed run recorded an unregistered origin_class {recorded!r}")
        return None
    if recorded in ATTESTED_ORIGIN_CLASSES and not record.get("route"):
        contradictions.append(
            f"resumed run recorded {recorded!r} with no original route — not trusted"
        )
        return None
    if recorded == ORIGIN_CLASS_HUMAN and record.get("auth_type") not in ("token", "fingerprint"):
        contradictions.append(
            f"resumed run recorded 'human' with auth_type={record.get('auth_type')!r} — not trusted"
        )
        return None
    return recorded, record


def continued_run_witness(
    *,
    request_id: str,
    user_id: str,
    origin_class: str | None,
    origin_witness: dict[str, Any] | None,
) -> dict[str, Any]:
    """The record a worker carries (under ``CONTINUED_RUN_WITNESS_KEY``) when a new turn continues
    ``request_id`` — that request's persisted class, its person, and the route + credential that
    witnessed it. Read back off the request's own row — never typed by the caller."""
    original = origin_witness if isinstance(origin_witness, dict) else {}
    return {
        "request_id": str(request_id),
        "user_id": str(user_id or ""),
        "origin_class": str(origin_class or ""),
        "route": original.get("route"),
        "auth_type": original.get("auth_type"),
    }


def _continued_record(
    ctx: AppContext, contradictions: list[str]
) -> tuple[str, dict[str, Any]] | None:
    """The person class a continuation keeps from its ORIGINATING request, with its record, or None.

    Applies only to a worker's turn (no live HTTP witness, declared nothing more specific than
    ``system``) for the SAME person the original request names, and only to a person class
    (``human`` / ``delegated_member``) or a person's own unattested request (``api`` on a non-MCP
    route with a person's credential) the original record can support. Anything else is read
    from its own facts; an unsupportable record is a contradiction, never trusted.
    """
    if not _is_worker_context(ctx):
        return None
    metadata = ctx.metadata if isinstance(ctx.metadata, dict) else {}
    record = metadata.get(CONTINUED_RUN_WITNESS_KEY)
    if not isinstance(record, dict) or not record.get("request_id"):
        return None
    if not ctx.user_id or str(record.get("user_id") or "") != str(ctx.user_id):
        contradictions.append("continued run names a different person than the run — not trusted")
        return None
    recorded = str(record.get("origin_class") or "")
    if recorded == ORIGIN_CLASS_API:
        # A person's own request their client did not attest (``initiation`` omitted: the research
        # Run, a Battle, a coding agent's HTTP turn): its continuation keeps THAT class with the
        # mark, never ``system`` (live 2026-10-19: 362 such wakes in 30 h recorded as system work).
        # It needs the person's own HTTP witness; an MCP route is a coding agent and stays as-is.
        route = str(record.get("route") or "")
        if not route or route.startswith("mcp:") or record.get("auth_type") not in ("token", "fingerprint"):
            return None
        return recorded, record
    if recorded not in _PERSON_CLASSES:
        return None  # a continuation of machine work stays machine work
    if recorded == ORIGIN_CLASS_HUMAN and (
        not record.get("route") or record.get("auth_type") not in ("token", "fingerprint")
    ):
        contradictions.append(
            f"continued run recorded 'human' with route={record.get('route')!r} "
            f"auth_type={record.get('auth_type')!r} — not trusted"
        )
        return None
    return recorded, record


def own_text_witness(
    *, inbound_message_id: str, user_id: str, channel: str, claim: str
) -> dict[str, Any]:
    """The record a worker carries (under ``OWN_TEXT_WITNESS_KEY``) for a turn on a person's own
    text: which inbound message, whose verified number sent it, on what channel, and which door
    claimed it. The host stamps it only AFTER the claim succeeded and the sender matched."""
    return {
        "inbound_message_id": str(inbound_message_id or ""),
        "user_id": str(user_id or ""),
        "channel": str(channel or ""),
        "claim": str(claim or ""),
    }


def _own_text_record(
    ctx: AppContext, contradictions: list[str]
) -> dict[str, Any] | None:
    """The own-text record a worker turn may honour, or None.

    Applies only to a worker's turn (``_is_worker_context``, the same test the resumed and continued
    readers use; or the parentless root fork of such a turn, which is the same run) — for the SAME
    person the record names, on a named inbound message. Anything else is read from its own facts.
    """
    declared = str(ctx.origin_class or "")
    # The parentless root fork of a worker turn is the same run; it never carries a live route.
    root_fork = declared == ORIGIN_CLASS_CHILD_AGENT and not ctx.parent_conversation_id and not ctx.route
    if not _is_worker_context(ctx) and not root_fork:
        return None
    metadata = ctx.metadata if isinstance(ctx.metadata, dict) else {}
    record = metadata.get(OWN_TEXT_WITNESS_KEY)
    if not isinstance(record, dict):
        return None
    if not record.get("inbound_message_id"):
        contradictions.append("own-text record names no inbound message — not trusted")
        return None
    if not ctx.user_id or str(record.get("user_id") or "") != str(ctx.user_id):
        contradictions.append("own-text record names a different person than the run — not trusted")
        return None
    return record


# ── THE HOST'S PERSON-REQUEST RESOLVER ───────────────────────────────────────
# Whether an unattested HTTP request (``api``) is a real person's own direct request needs the
# host's account lists (real people vs agent seats and bots), which this package cannot hold. The
# host injects its answer; with none configured an ``api`` request stays ``api``.
_person_request_resolver: Callable[[Any], bool] | None = None
_RESOLVING_PERSON_REQUEST: ContextVar[bool] = ContextVar("_resolving_person_request", default=False)


def set_person_request_resolver(resolver: Callable[[Any], bool] | None) -> None:
    """Install the host's "is this a real person's own direct request?" predicate (None clears it).

    When it answers yes for a request the witness reads as ``api`` (a person's client that did not
    attest ``initiation="user"``), the request is recorded ``human`` with
    ``witness["person_request"]`` — in ``chat.user_request``, the conversation and every reading
    that goes through ``reconcile_origin`` / ``gate_origin_class``.
    """
    global _person_request_resolver
    _person_request_resolver = resolver


def _is_person_request(ctx: AppContext) -> bool:
    resolver = _person_request_resolver
    # The host's predicate may itself read ``gate_origin_class`` (it must see ``api``): re-entry
    # answers no, so the inner reading is the plain witness.
    if resolver is None or _RESOLVING_PERSON_REQUEST.get():
        return False
    token = _RESOLVING_PERSON_REQUEST.set(True)
    try:
        return bool(resolver(ctx))
    except Exception:  # noqa: BLE001 — an unanswerable predicate leaves the honest default
        return False
    finally:
        _RESOLVING_PERSON_REQUEST.reset(token)


def resumed_origin_class(ctx: AppContext) -> str | None:
    """The original class of the request a worker is re-running in ``ctx``, or None — for a
    reader that records who started a tree (a sub-agent's parent class) before any write."""
    found = _resumed_record(ctx, [])
    return found[0] if found is not None else None


def true_starter_class(ctx: AppContext | None) -> str:
    """Who really started this run: ``reconcile_origin`` quietly (no contradiction banner).

    For a reader that asks "is anyone watching this step?" — it must see the starter the
    record shows (a mandate run forked from a workflow step is ``workflow``, not the fork's
    declared ``child_agent``). Gates keep reading ``gate_origin_class``.
    """
    return reconcile_origin(ctx, announce=False)[0]


def reconcile_origin(ctx: AppContext | None, *, announce: bool = True) -> tuple[str, dict[str, Any]]:
    """Resolve the final origin_class + witness payload for a persistence write.

    The witness always wins: a claimed attested class that the observed facts
    do not support is replaced with the derived truth, and the contradiction is
    recorded in ``witness["contradictions"]`` (and screamed to the console) —
    never silently accepted, never silently dropped.
    """
    if ctx is None:
        return ORIGIN_CLASS_SYSTEM, {
            "auth_type": None,
            "route": None,
            "process_role": _process_role(),
            "declared_class": None,
            "contradictions": ["no AppContext at persistence time"],
        }

    witness = build_origin_witness(ctx)
    contradictions: list[str] = []
    claimed = ctx.origin_class

    own_text = _own_text_record(ctx, contradictions)
    resumed = None if own_text is not None else _resumed_record(ctx, contradictions)
    continued = (
        None if own_text is not None or resumed is not None else _continued_record(ctx, contradictions)
    )
    if own_text is not None:
        # A turn on a person's own text, claimed by the door that answers it and sent from their
        # verified number, is that person's own start (2026-10-19 K4: the spend desk ran on
        # Arman's reply and recorded ``system``).
        final = ORIGIN_CLASS_HUMAN
        witness["own_text"] = {
            k: own_text.get(k) for k in ("inbound_message_id", "channel", "claim")
        }
    elif continued is not None:
        # A new turn continuing a person's own request (their helper's answer, their wake-up)
        # is their own work: it keeps the person class their request's boundary witnessed.
        final, record = continued
        witness["continued_from"] = {"request_id": str(record.get("request_id")), "origin_class": final}
        if record.get("route"):
            witness["route"] = record.get("route")
            witness["auth_type"] = record.get("auth_type")
    elif resumed is not None:
        # A worker re-running a request (crash recovery) is still that request: it keeps the
        # class its own HTTP boundary witnessed. Read as background ``system`` work, a
        # recovered person's turn was refused as an automated run on a protected account
        # (2026-10-16) and every other person's recovered turn escaped the usage gate.
        final, record = resumed
        witness["resumed_run"] = {"request_id": str(ctx.request_id), "origin_class": final}
        if record.get("route"):
            witness["route"] = record.get("route")
            witness["auth_type"] = record.get("auth_type")
    elif claimed in ATTESTED_ORIGIN_CLASSES:
        if not ctx.route:
            contradictions.append(
                f"claimed {claimed!r} with no HTTP witness (route is unset) — "
                "an interactive class cannot originate outside a request"
            )
            final = _derive_machine_class(ctx)
        elif claimed == ORIGIN_CLASS_HUMAN and ctx.auth_type not in ("token", "fingerprint"):
            contradictions.append(
                f"claimed 'human' with auth_type={ctx.auth_type!r} — "
                "a person always carries a credential"
            )
            final = ORIGIN_CLASS_API
        else:
            final = claimed
    elif claimed in MACHINE_ORIGIN_CLASSES:
        final = claimed
    elif not claimed:
        final = (
            derive_http_origin_class(
                route=ctx.route, auth_type=ctx.auth_type, initiation=None
            )
            or _derive_machine_class(ctx)
        )
    else:
        contradictions.append(f"unregistered origin_class {claimed!r}")
        final = _derive_machine_class(ctx)

    # A real person's own direct request their client did not attest (``api`` on our HTTP route:
    # the research Run, a Battle, an extension chat) is recorded as theirs: ``human`` with the mark.
    # The host decides who is a real person (``set_person_request_resolver``); MCP routes,
    # approved-server hops, ``initiation="auto"``, leases, triggers and agent seats stay as read.
    if (
        final == ORIGIN_CLASS_API
        and ctx.route
        and own_text is None
        and resumed is None
        and continued is None
        and _is_person_request(ctx)
    ):
        witness["person_request"] = {"from": ORIGIN_CLASS_API, "to": ORIGIN_CLASS_HUMAN}
        final = ORIGIN_CLASS_HUMAN

    # A conversation typed ``subagent`` WITH a parent is a helper the platform launched on the
    # person's behalf (the conversation labeler, a General Chat helper): it inherits the
    # request's HTTP witness (route + token -> 'human') but nobody started it. Its class is
    # ``child_agent``. Persistence only: gates read the DECLARED ``ctx.origin_class``.
    if (
        final in ATTESTED_ORIGIN_CLASSES
        and ctx.conversation_type == "subagent"
        and ctx.parent_conversation_id
    ):
        witness["lineage_class"] = {"from": final, "to": ORIGIN_CLASS_CHILD_AGENT}
        final = ORIGIN_CLASS_CHILD_AGENT

    # A ``child_agent`` with NO parent conversation was started by no agent: it is the ROOT run
    # of the machine work that forked it (``run_mandate`` from a workflow step, a service under
    # ``system_app_context``, the agent factory, a schedule). Recording it as "started by another
    # agent" mislabelled every server-side mandate run (2026-10-16). Persistence only, like the
    # rule above: gates keep reading the DECLARED ``ctx.origin_class`` (the usage gate leaves
    # system/scheduled ungated, so the fork's declared class must not move).
    if final == ORIGIN_CLASS_CHILD_AGENT and not ctx.parent_conversation_id:
        root = root_run_origin_class(ctx)
        witness["root_run_class"] = {"from": final, "to": root}
        final = root

    if contradictions:
        witness["contradictions"] = contradictions
    if contradictions and announce:
        try:
            from matrx_utils import vcprint

            vcprint(
                "\n"
                "================================================================\n"
                "🚨 ORIGIN PROVENANCE CONTRADICTION — claim overruled by witness\n"
                f"  claimed:  {claimed!r}\n"
                f"  recorded: {final!r}\n"
                f"  declared: app={ctx.source_app!r} feature={ctx.source_feature!r}\n"
                f"  witness:  route={ctx.route!r} auth={ctx.auth_type!r} "
                f"exec={ctx.execution_kind!r} internal={ctx.is_internal_agent}\n"
                f"  reasons:  {contradictions}\n"
                "  The derived truth was persisted; the claim is preserved in\n"
                "  origin_witness.declared_class as evidence. Fix the caller.\n"
                "================================================================",
                color="red",
            )
        except Exception:  # noqa: BLE001 — the write must land regardless
            pass

    return final, witness
