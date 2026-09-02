"""
Matrx AI — Unified multi-provider AI client, orchestration, and tool system.

Core Components:
- UnifiedConfig: Configuration dataclass for AI requests
- UnifiedMessage: Message representation across providers
- MessageList: Container for conversation messages
- UnifiedResponse: Standardized response from AI providers

Client & Orchestration:
- UnifiedAIClient: Main client for executing AI requests
- AIMatrixRequest, CompletedRequest: Request/response containers (from matrx_ai.orchestrator)
- execute_until_complete: Autonomous execution entry point

Usage:
    from matrx_ai import UnifiedConfig, UnifiedMessage, UnifiedAIClient
    from matrx_ai import AIMatrixRequest, CompletedRequest, execute_until_complete

Submodules:
- matrx_ai.agents: Agent system for template-based AI interactions
- matrx_ai.config: Configuration types (UnifiedConfig, TokenUsage, etc.)
- matrx_ai.context: Shared context interfaces (AppContext, Emitter, events)
- matrx_ai.orchestrator: Execution, requests, resolvers
- matrx_ai.providers: Provider-specific API implementations
- matrx_ai.processing: Audio preprocessing, transcription
- matrx_ai.tools: Tool execution and registry
"""

__all__ = [
    "AIMatrixRequest",
    "Capability",
    "ClientContext",
    "CompletedRequest",
    "ContentType",
    "ExtractedSpan",
    "FinishReason",
    "MessageList",
    "Provider",
    "Role",
    "SpanExtractionResult",
    "TimingUsage",
    "TokenUsage",
    "ToolCallUsage",
    "UnifiedAIClient",
    "UnifiedConfig",
    "UnifiedMessage",
    "UnifiedResponse",
    "configure",
    "execute_until_complete",
    "extract_spans",
]


def configure(
    *,
    db_models: dict | None = None,
    db_bases: dict | None = None,
    db_instances: dict | None = None,
    db_extras: dict | None = None,
    capabilities: list | None = None,
    api_key_resolver=None,
    conversation_store=None,
    model_catalog=None,
    tool_source=None,
    execution_agent_source=None,
    get_jwt=None,
    server_url=None,
    source_app=None,
    persistence_policy_registrar=None,
    handoff_ledger=None,
    **ext_kwargs,
) -> None:
    """Configure matrx-ai with external dependencies from the host application.

    Must be called before accessing any DB-dependent functionality.

    CLIENT HOST (desktop — no Postgres, no server API keys)
    -------------------------------------------------------
    A client host like matrx-local configures ONLY the client seams — no
    db_models / db_bases / db_instances wiring at all::

        matrx_ai.configure(
            settings=app_settings,
            api_key_resolver=secret_store.get,          # provider keys
            conversation_store=SqliteConversationStore(),  # persistence
            model_catalog=ServerModelCatalog(),         # model lookup+routing
            get_jwt=lambda: auth.current_token,         # user identity
            server_url=os.environ["AIDREAM_SERVER_URL_LIVE"],
            source_app="matrx_local",
        )

    After this call, the classic execution path (execute_until_complete via
    UnifiedAIClient) runs with ZERO database access: any DBNotConfiguredError
    raised after a configure() like the above is a matrx-ai packaging bug —
    report it, don't work around it. The seam combination is validated
    all-errors-at-once (ClientHostConfigError) so startup wiring is fixed in
    one pass.

    Args:
        db_models: Map of model name -> model class (e.g., {"AiModel": AiModel}).
            The AI catalog (``matrx_ai.catalog``) consumes "AiModel" (the host's
            ai.model_definition class) plus "AiEndpoint" / "AiApi" /
            "AiOffering" / "AiSetting" / "AiProvider" / "AiModelAlias"
            (ai.endpoint / ai.api / ai.offering / ai.setting / ai.provider /
            ai.model_alias).
        db_bases: Map of base name -> base class (e.g., {"TasksBase": TasksBase}).
        db_instances: Map of instance name -> instance (e.g., {"guest_executions_manager": gm}).
        db_extras: Map of extra name -> object (e.g., {"RenderDefinitionDTO": dto_cls}).
        capabilities: List of ``Capability`` objects the host wants registered
            in addition to matrx-ai's built-in bundles. The host owns
            product-specific capabilities (editor-state, aidream-app, etc.);
            matrx-ai owns platform-level ones (sandbox-fs, …). Re-registering
            the same name raises unless the Capability has ``replace=True``
            semantics — pass via ``register_capability`` directly for that.
        api_key_resolver: Optional ``Callable[[str], str | None]``. When set,
            every provider API key resolves through it FIRST (per env-style
            name, e.g. ``"OPENAI_API_KEY"``), falling back to ``os.environ``.
            Desktop hosts inject one so provider keys never live in the
            process environment; server hosts omit it and keep the env path.
            Provider clients re-key on the resolved value, so a rotation takes
            effect on the next request without a restart.
        conversation_store: Optional ``matrx_ai.client_host.ConversationStore``
            implementation. When set (client hosts — no Postgres), ALL
            conversation persistence (gate, persist_completed_request, tool
            logging) and the history read delegate to the store instead of the
            cx_ ORM tables. Validated structurally at configure() time.
        model_catalog: Optional ``matrx_ai.catalog.ModelCatalog`` implementation
            (``async list_models() -> list[dict]``, ``async get_model(id_or_name)
            -> dict | None`` — ai.model_definition ``to_dict()`` shape). When
            set, model lookup + call routing resolve from the catalog and the
            ORM model manager is never constructed. Pair with
            ``matrx_ai.catalog.register_runtime_model`` for synthetic local-LLM
            entries. ``matrx_ai/local_data/models_data.py`` is the packaged
            offline baseline a host can build its catalog from.
        tool_source: Optional ``matrx_ai.tools.tool_source.ToolSource``
            implementation (``async list_tools() -> list[dict]`` — rows in
            the ``tool.definition`` ``to_dict()`` shape). When set, the tool
            registry loads from it INSTEAD of the ORM base. When unset but
            BOTH ``server_url`` and ``source_app`` are configured, a
            server-backed source is derived automatically (GET
            ``{server_url}/ai-tools/app/{source_app}/all`` with the current
            JWT) — see ``matrx_ai.tools.tool_source.ServerToolSource``.
        execution_agent_source: Optional
            ``matrx_ai.client_host.agent_source.ExecutionAgentSource``. ORM-less
            hosts inject this to make ``agx.load_for_execution`` and
            ``Agent.from_agent`` consume complete canonical definitions rather
            than reconstructing agents from listing metadata.
        get_jwt: Optional zero-argument callable returning the current user's
            JWT (str | None). Called at request time, never cached — token
            refreshes are picked up automatically. Requires ``server_url``.
            Used by the derived server-backed tool source (above) and any
            future authenticated server reads.
        server_url: Optional AIDream server base URL for server-backed
            features — e.g. the value of ``AIDREAM_SERVER_URL_LIVE``. With
            ``source_app`` set, enables the derived server-backed tool
            registry fetch.
        source_app: Optional app identity stamp (e.g. ``"matrx_local"``) —
            selects which app's tools the server-backed tool fetch returns
            and stamps persisted rows.
        **ext_kwargs: External deps (settings, get_async_supabase_client, etc.).
    """
    # A normal import — NOT a file-path load. matrx_ai/db/__init__.py resolves
    # its names lazily (PEP 562 __getattr__), so importing _registry through the
    # package is already cheap and cycle-free; a spec_from_file_location() load
    # would additionally break every frozen host (PyInstaller ships modules in a
    # PYZ archive with no .py on disk → FileNotFoundError at configure()).
    from matrx_ai._ext import configure_ext
    from matrx_ai.db._registry import configure_db

    configure_db(
        models=db_models,
        bases=db_bases,
        instances=db_instances,
        extras=db_extras,
    )
    if persistence_policy_registrar is not None:
        from matrx_ai.persistence.registry import configure_policy_registrar

        configure_policy_registrar(persistence_policy_registrar)
    # Client-host seams: validate the COMBINATION all-errors-at-once
    # (ClientHostConfigError — the 0.1.26 ClientModeConfigError UX), then
    # register each provided seam in the _ext registry.
    _client_seams = {
        "conversation_store": conversation_store,
        "model_catalog": model_catalog,
        "tool_source": tool_source,
        "execution_agent_source": execution_agent_source,
        "api_key_resolver": api_key_resolver,
        "get_jwt": get_jwt,
        "server_url": server_url,
        "source_app": source_app,
    }
    if any(value is not None for value in _client_seams.values()):
        from matrx_ai.client_host.validate import validate_client_host_config

        validate_client_host_config(**_client_seams)
        for key, value in _client_seams.items():
            if value is not None:
                ext_kwargs[key] = value
    if ext_kwargs:
        configure_ext(**ext_kwargs)

    # A CLIENT host resolves Mandates over the API — the same question the
    # server answers from `agent.mandate`, asked the only way a client
    # can ask it. Installed automatically so a client never silently lacks slot
    # resolution: without it, every mandated agent refuses (there is no seed
    # fallback), which is correct but useless. A host that installed its own
    # resolver wins — this never overwrites one.
    if server_url is not None and get_jwt is not None:
        from matrx_ai.mandates import get_mandate_resolver, set_mandate_resolver

        if get_mandate_resolver() is None:
            from matrx_ai.client_host.mandate_source import ServerMandateSource

            set_mandate_resolver(ServerMandateSource(server_url, get_jwt))

    # Wire a host-injected durable VFS backend (e.g. aidream's code_files-backed
    # store) into the self-contained ``vfs`` package. That package imports
    # nothing from ``matrx_ai`` and exposes only a plain ``set_backend`` setter,
    # so this — reading the injected backend and installing it — is the correct
    # place for the wiring. Unconfigured ⇒ the VFS keeps its in-memory default,
    # so standalone matrx-ai is unchanged.
    # Cloud Browser human-handoff pending-call ledger (S5 §5.6). The host wires
    # the durable delegate + exactly-once resolve (aidream's log_delegated /
    # finalize / resolve_client_tool_results). Unwired ⇒ a browser park raises
    # loudly at the boundary; there is NO fallback by design.
    if handoff_ledger is not None:
        from matrx_ai.browser_handoff import set_handoff_ledger

        set_handoff_ledger(handoff_ledger)

    from matrx_ai._ext import get_ext, has_ext

    if has_ext("vfs_backend"):
        from matrx_ai.tools.vfs.workspace import set_backend as _set_vfs_backend

        _set_vfs_backend(get_ext("vfs_backend"))

    # Static-input admission: every node type that runs an authored agent builds
    # the host's AgentStartRequest at RUN time, so values its field validators
    # reject (an unregistered source_feature, a malformed ToolSpec) used to pass
    # /workflows/validate and only explode after a paid run started. Registering
    # the model lets matrx-graph's validate_definition exercise those validators
    # over the node's authored static inputs — validators only, no execution.
    # Both agent node types share ONE builder, so both get the same admission.
    if has_ext("AgentStartRequest"):
        from matrx_graph.validation import register_admission_request_model

        for _agent_node_type in ("ai.agent.start", "ai.agent.produce"):
            register_admission_request_model(_agent_node_type, get_ext("AgentStartRequest"))

    if capabilities:
        from matrx_ai.capabilities import register_capability

        for cap in capabilities:
            register_capability(cap)

    # Register the vision-class encoder with matrx-utils so MediaRefs that
    # carry ``vision_class`` resolve to a variant ``cld_files`` row at the
    # boundary normaliser. matrx-utils never imports matrx-ai at module
    # top-level — this is the wiring point.
    _register_vision_encoder()


def _register_vision_encoder() -> None:
    """Wire matrx-ai's vision re-encoder into matrx-utils' variant registry.

    Idempotent: re-registering the same family replaces the previous
    encoder, which is fine.
    """
    try:
        from matrx_files.cloud_sync.variants import register_variant_encoder
    except Exception:
        return

    from matrx_ai.processing.vision import (
        VISION_API_CLASSES,
        reencode_for_vision_class,
    )

    def _encoder(master_bytes: bytes, variant_key: str) -> tuple[bytes, str]:
        cls = VISION_API_CLASSES.get(variant_key)
        if cls is None:
            raise KeyError(
                f"unknown vision_class={variant_key!r}; "
                f"known classes: {sorted(VISION_API_CLASSES)}"
            )
        encoded = reencode_for_vision_class(master_bytes, cls)
        mime = "image/jpeg" if cls.format.upper() == "JPEG" else f"image/{cls.format.lower()}"
        return encoded, mime

    register_variant_encoder("vision", _encoder)


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name in (
        "UnifiedConfig",
        "UnifiedMessage",
        "MessageList",
        "UnifiedResponse",
        "Role",
        "ContentType",
        "Provider",
        "FinishReason",
    ):
        from matrx_ai import config

        return getattr(config, name)
    if name in ("AIMatrixRequest", "CompletedRequest"):
        from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

        return AIMatrixRequest if name == "AIMatrixRequest" else CompletedRequest
    if name == "UnifiedAIClient":
        from matrx_ai.providers import UnifiedAIClient

        return UnifiedAIClient
    if name == "execute_until_complete":
        from matrx_ai.orchestrator import execute_until_complete

        return execute_until_complete
    if name == "TokenUsage":
        from matrx_ai.config import TokenUsage

        return TokenUsage
    if name == "TimingUsage":
        from matrx_ai.orchestrator.tracking import TimingUsage

        return TimingUsage
    if name == "ToolCallUsage":
        from matrx_ai.orchestrator.tracking import ToolCallUsage

        return ToolCallUsage
    if name in ("Capability", "ClientContext"):
        from matrx_ai.capabilities import Capability, ClientContext

        return Capability if name == "Capability" else ClientContext
    if name == "extract_spans":
        from matrx_ai.extraction import extract_spans

        return extract_spans
    if name in ("SpanExtractionResult", "ExtractedSpan"):
        from matrx_ai.providers.fastino import ExtractedSpan, SpanExtractionResult

        return SpanExtractionResult if name == "SpanExtractionResult" else ExtractedSpan
    raise AttributeError(f"module 'matrx_ai' has no attribute '{name}'")
