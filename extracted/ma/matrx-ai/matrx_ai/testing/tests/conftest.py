"""Conftest for record/replay tests.

Stubs matrx-ai's DB registry with no-op classes so that importing
``matrx_ai.orchestrator.executor`` doesn't fail with DBNotConfiguredError.

The stubs are never *called* by the tests — RecordReplayExecutor intercepts
before any real DB access happens. They exist only to satisfy the
module-level ``get_model()`` / ``get_base()`` / ``get_instance()`` calls that
run at import time in matrx-ai.
"""

from __future__ import annotations


def pytest_configure(config):  # noqa: ARG001
    """Configure matrx-ai with stubs once per test session, before collection."""
    _configure_stubs()


class _StubMeta(type):
    """Answer attribute access on the *class* object itself.

    matrx-orm Model APIs are classmethods (``AiModel.filter(...)``,
    ``Model.load_by_id(...)``), so the stub must resolve attributes at the
    class level too — instance ``__getattr__`` alone leaves
    ``type object '_Stub' has no attribute 'filter'`` errors behind.
    """

    def __getattr__(cls, _name):
        return _Stub()


class _Stub(metaclass=_StubMeta):
    """Attribute-accepting placeholder that pretends to be any DB model/base.

    Any chained call is also *awaitable* and resolves to an empty list —
    i.e. the stub behaves like an empty database (``await
    Model.filter().limit(n).all()`` → ``[]``) instead of raising mid-chain.
    """

    # A stub has NO Model metadata, and it must SAY so. Answering these with
    # another _Stub made callers treat the stub as a fully-described model and
    # blow up far away:
    #   * register_table compared its key against
    #     "<_Stub object>.<_Stub object>" and raised (table_name / db_schema);
    #   * matrx_orm.session.op._resolve_pk did ``len(meta.primary_keys)`` on a
    #     _Stub → TypeError → the tool_trace insert was DROPPED → the whole
    #     request died on PersistenceBarrierError 'dropped_ops:1'.
    # ``None`` is the honest answer and every one of those call sites already
    # has a correct "no metadata" branch.
    _NO_METADATA_ATTRS = frozenset({"table_name", "db_schema", "primary_keys"})

    def __getattr__(self, _name):
        if _name in _Stub._NO_METADATA_ATTRS:
            return None
        return _Stub()

    def __call__(self, *args, **kwargs):
        return _Stub()

    def __await__(self):
        async def _empty_db() -> list:
            return []

        return _empty_db().__await__()


def _configure_stubs() -> None:
    import matrx_ai

    # Every model name that matrx-ai touches at import time (found by reading
    # the error trace from a bare import). Add to this list if future imports
    # break — each entry just needs a stand-in, not a real class.
    # Prefix-free names (post schema-aware-registry reorg). This is the SAME
    # curated set the pre-reorg conftest stubbed, with the Cx*/Agx*/Ctx*/Ws*
    # prefixes stripped to match the new generated class names. Stub ONLY the
    # names matrx-ai resolves at import time AND that have no real try/except
    # fallback class — bases like AiModelBase / AgentRunBase intentionally stay
    # OUT so their ``except DBNotConfiguredError`` real-class branch is used
    # (a stub would shadow a base whose super().__init__ takes kwargs).
    model_names = [
        "AiModel",
        # AI-catalog models (matrx_ai.catalog) — resolved lazily at load time,
        # stubbed here so any future import-time resolution keeps working.
        "AiProvider",
        "AiEndpoint",
        "AiApi",
        "AiModelAlias",
        "AiOffering",
        "AiSetting",
        "RenderDefinition",
        "AgentMemory",
        "Conversation",
        "Media",
        "Message",
        "ObservationalMemory",
        "ObservationalMemoryEvent",
        "PendingInjection",
        "Request",
        "RequestSnapshot",
        "ToolCall",
        "ToolTrace",
        "UserRequest",
        "Notes",
        "OpsIssueClass",
        "OpsIssueEvent",
        # User-defined data type (UDT) models — backed by udt_* tables.
        "UdtDatasets",
        "UdtDatasetFields",
        "UdtDatasetRows",
        "UdtStructuredLists",
        "UdtStructuredListItems",
        "Tasks",
        "Projects",
        "Definition",
        "DefinitionVersion",
        "Shortcut",
    ]
    base_names = [
        "AgentMemoryBase",
        "ConversationBase",
        "MediaBase",
        "MessageBase",
        "ObservationalMemoryBase",
        "ObservationalMemoryEventBase",
        "PendingInjectionBase",
        "RequestBase",
        "RequestSnapshotBase",
        "ToolCallBase",
        "ToolTraceBase",
        "UserRequestBase",
        "TasksBase",
        "ProjectsBase",
        "NotesBase",
        "ToolDefBase",
        "ToolBindingBase",
        "ToolExecutorBase",
        "DefinitionBase",
        "DefinitionVersionBase",
        "ShortcutBase",
    ]
    instance_names = [
        "guest_executions_manager",
        "guest_execution_log_manager",
    ]
    extra_names = ["RenderDefinitionDTO"]

    # External utilities used at module-import time in matrx_ai submodules.
    ext_stubs: dict[str, object] = {
        "update_data_in_code": lambda *a, **kw: None,
        "dataset_reference_fetch": {},
        "picklist_reference_fetch": {},
        "settings": _Stub(),
        "TEMP_DIR": "/tmp",
        "get_async_supabase_client": lambda *a, **kw: None,
        "DatasetCreator": _Stub,
        "PicklistCreator": _Stub,
        "brave_search": {},
        "get_top_headlines": lambda *a, **kw: None,
        "keyword_research": lambda *a, **kw: None,
        "load_manifest_from_ctx": lambda *a, **kw: None,
        "IdeState": _Stub,
        "initialize": lambda *a, **kw: None,
        "create_test_app_context": lambda *a, **kw: None,
        "create_test_execution_context": lambda *a, **kw: None,
        "create_test_tool_context": lambda *a, **kw: None,
    }

    # NEVER clobber a REAL registration. ``matrx_ai.configure`` ``update``s the
    # global registries, and this function runs from ``pytest_configure`` in
    # several directory conftests — i.e. repeatedly, across a whole session, at
    # collection time. A host that already wired the real models (aidream's
    # ``configure_packages()``, imported by a test module collected earlier)
    # would silently get its ``ToolDefBase`` replaced by ``_Stub``, and every
    # later DB read returned "0 rows" with no error — that is exactly how
    # services/agent_data/tests/test_tool_gating.py ended up asserting against
    # an EMPTY tool registry. Fill gaps only.
    from matrx_ai._ext import has_ext
    from matrx_ai.db import _registry as _db_registry

    matrx_ai.configure(
        db_models={n: _Stub for n in model_names if n not in _db_registry._models},
        db_bases={n: _Stub for n in base_names if n not in _db_registry._bases},
        db_instances={
            n: _Stub() for n in instance_names if n not in _db_registry._instances
        },
        db_extras={n: _Stub for n in extra_names if n not in _db_registry._extras},
        **{n: v for n, v in ext_stubs.items() if not has_ext(n)},
    )
