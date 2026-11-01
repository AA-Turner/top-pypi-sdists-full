"""The knowledge graph research-os and the engine both write: node labels, edge types, agent-session node ids.

Lifted from the engine (engine/shared/vocab, engine:3); the engine imports this package.
"""

from __future__ import annotations

from ..compat import StrEnum


class NodeLabel(StrEnum):
    """Graph node labels — four canonical kinds post-migration 0091.

    Sub-type discrimination (Module vs Function for code; PR vs Issue for
    documents) lives in ``properties['kind']`` using the typed enums below
    (CodeSymbolKind, DocumentKind). Emit via the factories in shared.models
    (`make_code_symbol`, `make_document`, `make_person`, `make_feature`)
    rather than constructing GraphNodeSpec directly — the factories enforce
    the label-to-kind relationship.

    Other domain labels (SERVICE, SERVICE_CARD, DECISION, RUNBOOK,
    ERROR_GROUP, AGENT, WORKFLOW, FIX_ARTIFACT, VERIFICATION_RESULT) are
    out of scope for the collapse — they're either unused for acme
    today or carry distinct semantics worth preserving.
    """

    # ---- Canonical labels ----
    PERSON = "Person"
    DOCUMENT = "Document"
    FEATURE = "Feature"
    CODE_SYMBOL = "CodeSymbol"

    # ---- Domain labels (untouched by 0091) ----
    SERVICE = "Service"
    ERROR_GROUP = "ErrorGroup"
    SERVICE_CARD = "ServiceCard"
    DECISION = "Decision"
    RUNBOOK = "Runbook"
    AGENT = "Agent"
    WORKFLOW = "Workflow"
    FIX_ARTIFACT = "FixArtifact"
    VERIFICATION_RESULT = "VerificationResult"

    # ---- Research domain ---- generic experiment-tracking vocabulary (a Project nests Projects and has
    # Runs, a Run produces Artifacts, an Asset is a reusable input/output pinned across runs). No Experiment
    # label any more: research-os made an experiment a Project of kind 'experiment'; a client still
    # SENDING the old label is mapped, not refused (RETIRED_NODE_LABELS). Deliberately NOT collapsed into
    # DOCUMENT (as 0091 did for PR/Issue/Ticket/Channel/Repo): a Run is a domain object, not a document
    # about one. Each is paired with its own Document node at ingest and reached through it (the graph
    # retriever's neighbour join is `AND n.label = 'Document'`), so an entity node is an ANCHOR, never a
    # returned hit.
    PROJECT = "Project"
    RUN = "Run"
    ARTIFACT = "Artifact"
    ASSET = "Asset"

    # ---- Coding-agent sessions ----
    # A coding-agent conversation (Claude Code today; Codex has a handler but
    # no capture plugin yet). It is the JOIN between two independent ingest
    # pipelines: the transcript connector emits it beside the session
    # document, and research-os emits it beside the run document, so a session
    # and the runs it produced become one-hop neighbours through it.
    #
    # It has to be an entity rather than a reference to the session Document:
    # custom-ingest rewrites EVERY Document-labelled edge endpoint through
    # custom_ingest_doc_id() (see engine/ingest/handlers/custom_ingest.py),
    # which is the namespace-confinement control that stops one system
    # attaching edges to another tenant's or another connector's documents.
    # That rewrite is unconditional, so a same-tenant cross-connector
    # reference is mangled just like a hostile one, accepted with a 200, and
    # parked in pending_edges until the reaper drops it. Non-Document labels
    # pass through untouched.
    AGENT_SESSION = "AgentSession"


class EdgeType(StrEnum):
    OWNS = "OWNS"
    MENTIONS = "MENTIONS"
    AUTHORED = "AUTHORED"
    BLOCKS = "BLOCKS"
    SUPERSEDES = "SUPERSEDES"
    DUPLICATES = "DUPLICATES"
    TOUCHES = "TOUCHES"
    FIRES_IN = "FIRES_IN"
    MEMBER_OF = "MEMBER_OF"
    LINKED_FROM = "LINKED_FROM"

    CONFLICTS_WITH = "CONFLICTS_WITH"
    VERIFIED_BY = "VERIFIED_BY"
    DERIVED_FROM = "DERIVED_FROM"
    FIXES = "FIXES"
    REGRESSES = "REGRESSES"
    ASSIGNED_TO = "ASSIGNED_TO"
    COMPILED_FROM = "COMPILED_FROM"
    DESCRIBES = "DESCRIBES"

    CALLS = "CALLS"
    IMPORTS = "IMPORTS"
    INHERITS = "INHERITS"
    IMPLEMENTS = "IMPLEMENTS"
    REFERENCES = "REFERENCES"
    DEFINED_IN = "DEFINED_IN"

    # LLM-inferred edge types (Lane B). These are emitted only by the
    # inferred_edges extractor and carry INFERRED or AMBIGUOUS confidence.
    DISCUSSES = "DISCUSSES"
    DOCUMENTS = "DOCUMENTS"
    RESOLVES = "RESOLVES"
    MENTIONS_ENTITY = "MENTIONS_ENTITY"
    RELATES_TO = "RELATES_TO"


def agent_session_canonical_id(agent: str, session_id: str) -> str:
    """canonical_id for an AGENT_SESSION node.

    More: DESIGN.md.
    """
    return f"agent_session:{agent}:{session_id}"


def agent_session_display_name(
    agent: str, session_id: str, person: str | None = None
) -> str:
    """properties['name'] for an AGENT_SESSION node.
    The ENGINE owns this name. research-os asserts only the edge, so there is
    exactly one writer and the node's name cannot flip-flop between two sides
    that know different things about the session.

    More: DESIGN.md.
    """
    spaced = agent.replace("_", " ")
    if person:
        return f"{person} {spaced} session {session_id}"
    return f"{spaced} session {session_id}"
