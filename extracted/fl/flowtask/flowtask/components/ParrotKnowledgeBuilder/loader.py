"""ParrotKnowledgeBuilder — FlowComponent that builds GraphIndex/PageIndex structures."""
import asyncio
from collections.abc import Callable
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Optional

from ...exceptions import ComponentError, ConfigError, DataNotFound
from ...interfaces.flow import FlowComponent

# Reuse module-level helpers and private methods from ParrotLoader without
# modifying it.  In Python 3, accessing a method via the class returns the
# underlying function whose __globals__ still live in ParrotLoader's module, so
# every helper they depend on (_has_glob, pd, json, …) resolves correctly.
from ..ParrotLoader.loader import (
    ParrotLoader as _PL,
    _has_glob,
)
from .payload import KnowledgeArtifact as KnowledgeArtifact  # re-exported

_VALID_INDEX_TYPES = frozenset({"graphindex", "pageindex"})


class ParrotKnowledgeBuilder(FlowComponent):
    """Build a GraphIndex graph or PageIndex tree from documents; emit KnowledgeArtifact.

    Config keys (YAML):
        index_type:      graphindex | pageindex   (required)
        path:            single file/dir/glob pattern
        path_list:       inline list or path to .txt/.json/.csv file of sources
        path_column:     column name when upstream component provides a DataFrame
        loader:          ParrotLoader class name (graphindex only)
        tenant_id:       ArangoDB tenant identifier (graphindex; default "default")
        directory:       KB storage directory under the task storage. A relative
                         path (e.g. "mi_agente/kb") resolves to
                         programs/{program}/agents/{directory}; absolute is used
                         as-is; if omitted, defaults to programs/{program}/agents.
                         Each mode writes to its own leaf so they never intermix:
                         pageindex → {directory}/pages, graphindex → {directory}/graph.
                         (index JSON + per-node markdown; graphindex section nodes
                         get a content_ref pointing at it.)
        llm:             LLM provider name (e.g. "anthropic", "google", "groq").
                         Required by pageindex; OPTIONAL for graphindex (enables
                         hierarchical section extraction + disk persistence;
                         omit for flat, in-memory extraction).
        llm_model:       model id for the adapter. If omitted, the client's own
                         default model is used (NOT the adapter's Google default).
        llm_concurrency: max concurrent LLM calls (legacy; the PageIndexToolkit
                         manages its own concurrency).
        with_summaries:  generate section summaries via LLM (pageindex; default True)
        fail_on_empty:   raise DataNotFound when no nodes/tree extracted (default True)
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the component from YAML config kwargs.

        Args:
            loop: optional event loop (forwarded to super).
            job: upstream job/component (forwarded to super).
            stat: stats callback (forwarded to super).
            **kwargs: YAML config keys consumed here; remainder forwarded to FlowComponent.
        """
        # Source resolution (mirror ParrotLoader attribute layout so rebound
        # methods work without modification)
        self.path: Optional[str] = kwargs.pop("path", None)
        self._path_list: Optional[Any] = kwargs.pop("path_list", None)
        self._path_list_format: str = str(
            kwargs.pop("path_list_format", "auto") or "auto"
        ).lower()
        self._path_column: Optional[str] = kwargs.pop("path_column", None)
        self.encoding: str = kwargs.get("encoding", "utf-8")

        # Mode
        self._index_type: Optional[str] = kwargs.pop("index_type", None)

        # graphindex config
        self._loader_name: Optional[str] = kwargs.pop("loader", None)
        self._tenant_id: str = kwargs.pop("tenant_id", "default")

        # KB storage directory (both modes persist the PageIndex tree here)
        self._directory: Optional[str] = kwargs.pop("directory", None)

        # pageindex config
        self._llm: Optional[Any] = kwargs.pop("llm", None)
        self._llm_model: Optional[str] = kwargs.pop("llm_model", None)
        self._llm_concurrency: int = int(kwargs.pop("llm_concurrency", 8))
        self._with_summaries: bool = bool(kwargs.pop("with_summaries", True))

        # Behaviour
        self._fail_on_empty: bool = bool(kwargs.pop("fail_on_empty", True))

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    # ------------------------------------------------------------------
    # Reuse ParrotLoader source-resolution and LLM-building helpers.
    # These functions' __globals__ live in ParrotLoader's module, so their
    # module-level dependencies (_has_glob, pd, json, …) resolve correctly.
    # ------------------------------------------------------------------
    _build_llm_client = _PL._build_llm_client
    _resolve_loader_class = _PL._resolve_loader_class
    _resolve_sources = _PL._resolve_sources
    _read_path_list_file = _PL._read_path_list_file
    _extract_paths_from_dataframe = _PL._extract_paths_from_dataframe

    def _resolve_model(self, client: Any) -> Optional[str]:
        """Resolve the model name to hand to ``PageIndexLLMAdapter``.

        Precedence: explicit ``llm_model`` config → the client's configured
        ``model`` → the client's provider default (``_default_model``). This
        avoids ``PageIndexLLMAdapter``'s hardcoded Google default
        (``gemini-3.1-flash-lite-preview``) leaking onto a non-Google client
        (e.g. Groq), which causes a 404 model_not_found.

        Args:
            client: the built ``AbstractClient`` (e.g. GroqClient).

        Returns:
            A provider-appropriate model name, or ``None`` to defer to the
            adapter (only when nothing could be resolved).
        """
        return (
            self._llm_model
            or getattr(client, "model", None)
            or getattr(client, "_default_model", None)
        )

    def _resolve_kb_directory(self, subdir: str) -> Path:
        """Resolve the KB storage directory under the task storage.

        Layout (per Jesús Lara): ``<task-storage-root>/{program}/agents/{directory}``,
        with a per-mode ``subdir`` appended so the two builders never intermix in
        the same folder:

            programs/{program}/agents/{directory}/pages   (pageindex)
            programs/{program}/agents/{directory}/graph   (graphindex)

        - relative ``directory`` (e.g. "mi_agente/kb") → joined under
          ``programs/{program}/agents``;
        - absolute ``directory`` → used as-is;
        - omitted → defaults to ``programs/{program}/agents``.

        The PageIndex stores auto-create the directory (``mkdir parents=True``).

        Args:
            subdir: per-mode leaf folder ("pages" or "graph").

        Returns:
            Absolute :class:`~pathlib.Path` for the PageIndex ``storage_dir``.
        """
        base = Path(self._taskstore.get_path()).joinpath(self._program, "agents")
        if self._directory:
            directory = Path(self._directory)
            base = directory if directory.is_absolute() else base.joinpath(directory)
        return base.joinpath(subdir)

    # ------------------------------------------------------------------
    # FlowComponent lifecycle
    # ------------------------------------------------------------------

    async def start(self, **kwargs: Any) -> None:
        """Validate config and resolve document sources.

        Args:
            **kwargs: forwarded to FlowComponent.start().

        Raises:
            ConfigError: missing/invalid index_type or no source provided.
            ComponentError: resolved path does not exist.
        """
        await super().start(**kwargs)

        # Validate index_type
        if not self._index_type:
            raise ConfigError(
                "ParrotKnowledgeBuilder: 'index_type' is required. "
                f"Supported values: {sorted(_VALID_INDEX_TYPES)}."
            )
        if self._index_type == "ontology":
            raise ConfigError(
                "ParrotKnowledgeBuilder: 'index_type: ontology' is not supported here. "
                "Ontology is an ArangoDB persistence/schema layer — use the CopyToArango "
                "spec for persistence instead."
            )
        if self._index_type not in _VALID_INDEX_TYPES:
            raise ConfigError(
                f"ParrotKnowledgeBuilder: unsupported index_type '{self._index_type}'. "
                f"Supported values: {sorted(_VALID_INDEX_TYPES)}."
            )

        # Normalize path_list string through mask replacement
        if isinstance(self._path_list, str):
            self._path_list = self.mask_replacement_recursively(self._path_list)

        # Resolve and validate single path
        if self.path:
            if isinstance(self.path, str):
                self.path = self.mask_replacement_recursively(self.path)
                if not self.path.startswith(("http://", "https://", "ftp://")):
                    if _has_glob(self.path):
                        pass  # glob expansion deferred to run()
                    else:
                        self.path = Path(self.path).resolve()
                        if not self.path.exists():
                            raise ComponentError(
                                f"ParrotKnowledgeBuilder: {self.path} doesn't exist."
                            )
            elif isinstance(self.path, Path) and not self.path.exists():
                raise ComponentError(
                    f"ParrotKnowledgeBuilder: {self.path} doesn't exist."
                )
        elif self._path_list is None and not self._path_column:
            raise ConfigError(
                "ParrotKnowledgeBuilder: provide at least one of: 'path', "
                "'path_list', or 'path_column' (with an upstream DataFrame)."
            )

    async def run(self) -> bool:
        """Dispatch to the appropriate index-type branch and set self._result.

        Returns:
            True on success.
        """
        if self._index_type == "graphindex":
            await self._run_graphindex()
        else:
            await self._run_pageindex()
        return True

    async def _run_graphindex(self) -> None:
        """Build a merged tenant graph via LoaderExtractor + GraphAssembler.

        For each resolved source, runs LoaderExtractor.extract() to get
        (nodes, edges), feeds them into a single GraphAssembler, then emits one
        KnowledgeArtifact(kind="graph") with model_dump() dicts. When `llm` is
        set, a PageIndexToolkit(storage_dir) is supplied so section content is
        persisted to disk and nodes carry a content_ref; otherwise extraction is
        flat/in-memory. Embed and cross-domain resolve are intentionally skipped
        (no vectors in v1).

        Raises:
            ConfigError: loader name not provided or loader class not found.
            DataNotFound: extraction produced no nodes and fail_on_empty is True.
        """
        # defer heavy import so graphindex extra is only required at runtime
        from parrot.knowledge.graphindex.assemble import GraphAssembler
        from parrot.knowledge.graphindex.extractors.loader import LoaderExtractor

        if not self._loader_name:
            raise ConfigError(
                "ParrotKnowledgeBuilder: 'loader' is required for graphindex mode."
            )
        loader_cls = self._resolve_loader_class(self._loader_name)
        if loader_cls is None:
            raise ConfigError(
                f"ParrotKnowledgeBuilder: loader '{self._loader_name}' not found "
                "in LOADER_REGISTRY, parrot_loaders, or parrot.loaders."
            )

        sources = self._resolve_sources()
        if sources is None:
            sources = [self.path]

        # Deduplicate the payload to mirror the assembler's merged view: a
        # node_id seen across multiple sources collapses to one entry (last
        # wins, as GraphAssembler.add_node does), and parallel edges collapse
        # on (source_id, target_id, kind). This keeps artifact.nodes/edges
        # consistent with the node_count/edge_count metadata and avoids pushing
        # duplicate upserts to a downstream CopyToArango.
        assembler = GraphAssembler(self._tenant_id)
        nodes_by_id: dict[str, Any] = {}
        edges_by_key: dict[tuple, Any] = {}

        # Optional LLM adapter + PageIndexToolkit: when `llm` is configured,
        # LoaderExtractor routes hierarchical content through the toolkit, which
        # persists each document's sections to disk (index JSON + per-node
        # markdown under storage_dir) and gives every SECTION node a
        # content_ref = "pageindex://<tree>/<node>". Without `llm` it degrades to
        # flat, in-memory extraction (one DOCUMENT node, no content_ref).
        # The AbstractClient MUST be entered as an async context manager
        # (__aenter__ initializes the per-loop SDK client).
        storage_dir = self._resolve_kb_directory("graph")
        persisted = self._llm is not None
        async with AsyncExitStack() as stack:
            extractor_kwargs: dict = {"toolkit": None}
            if persisted:
                from parrot.knowledge.pageindex.llm_adapter import PageIndexLLMAdapter
                from parrot.knowledge.pageindex.toolkit import PageIndexToolkit
                client = await stack.enter_async_context(self._build_llm_client())
                adapter = PageIndexLLMAdapter(
                    client=client, model=self._resolve_model(client)
                )
                extractor_kwargs["llm_adapter"] = adapter
                extractor_kwargs["toolkit"] = PageIndexToolkit(
                    adapter=adapter, storage_dir=str(storage_dir)
                )

            extractor = LoaderExtractor(**extractor_kwargs)

            for source in sources:
                source_str = str(source)
                try:
                    loader = loader_cls(source=source_str)
                    nodes, edges = await extractor.extract(loader, source_str)
                except Exception as exc:  # noqa: BLE001
                    self._logger.warning(
                        "ParrotKnowledgeBuilder: source %s failed, skipping: %s",
                        source_str, exc,
                    )
                    continue
                assembler.add_nodes(nodes)
                assembler.add_edges(edges)
                for node in nodes:
                    nodes_by_id[node.node_id] = node
                for edge in edges:
                    edges_by_key[(edge.source_id, edge.target_id, edge.kind)] = edge

        if self._fail_on_empty and not nodes_by_id:
            raise DataNotFound(
                "ParrotKnowledgeBuilder: graphindex extraction produced no nodes "
                f"across {len(sources)} source(s)."
            )

        self._result = KnowledgeArtifact(
            kind="graph",
            index_type="graphindex",
            source="<merged>",
            tenant_id=self._tenant_id,
            nodes=[n.model_dump() for n in nodes_by_id.values()],
            edges=[e.model_dump() for e in edges_by_key.values()],
            metadata={
                "source_count": len(sources),
                "node_count": assembler.node_count,
                "edge_count": assembler.edge_count,
                # Where section markdown/index were persisted (content_ref base);
                # None when running flat/in-memory (no `llm`).
                "storage_dir": str(storage_dir) if persisted else None,
            },
        )
        self.add_metric("NUM_NODES", assembler.node_count)
        self.add_metric("NUM_EDGES", assembler.edge_count)

    async def _run_pageindex(self) -> None:
        """Build + persist one PageIndex tree per PDF via PageIndexToolkit.

        For each PDF, ``toolkit.import_pdf`` builds the tree AND writes it to
        disk under the resolved storage_dir:
        ``<storage_dir>/<tree_name>.json`` (index) + ``<storage_dir>/<tree_name>/
        <node_id>.md`` (per-node markdown). The emitted KnowledgeArtifact keeps
        the lean tree/index in ``tree`` and points at the on-disk content via
        ``metadata`` (storage_dir / tree_name / index_file / content_dir);
        ``node_markdown`` stays empty since the bodies live on disk. A downstream
        CopyTo* persister reads from those paths.

        Raises:
            ConfigError: source is not a PDF file.
            DataNotFound: no trees produced and fail_on_empty is True.
        """
        # defer heavy import; requires dev parrot 0.25.7 + editable-source toggle
        from parrot.knowledge.pageindex.llm_adapter import PageIndexLLMAdapter
        from parrot.knowledge.pageindex.toolkit import PageIndexToolkit

        sources = self._resolve_sources()
        if sources is None:
            sources = [self.path]

        storage_dir = self._resolve_kb_directory("pages")
        artifacts: list[KnowledgeArtifact] = []

        # The AbstractClient MUST be entered as an async context manager so its
        # per-loop SDK client is initialized; a bare instance leaves the SDK as
        # None and the toolkit's LLM calls fail with 'NoneType .. chat'.
        async with self._build_llm_client() as client:
            adapter = PageIndexLLMAdapter(
                client=client, model=self._resolve_model(client)
            )
            toolkit = PageIndexToolkit(adapter=adapter, storage_dir=str(storage_dir))

            for source in sources:
                source_str = str(source)
                if not source_str.lower().endswith(".pdf"):
                    raise ConfigError(
                        f"ParrotKnowledgeBuilder: pageindex requires PDF sources, "
                        f"got: {source_str!r}. Non-PDF formats are not supported by build_page_index."
                    )
                tree_name = Path(source_str).stem
                try:
                    # Idempotent: replace any prior tree for this document.
                    if tree_name in await toolkit.list_trees():
                        await toolkit.delete_tree(tree_name)
                    await toolkit.create_tree(tree_name, doc_name=Path(source_str).name)
                    await toolkit.import_pdf(
                        tree_name=tree_name,
                        pdf_path=source_str,
                        with_summaries=self._with_summaries,
                    )
                    tree = await toolkit.get_tree(tree_name)
                except Exception as exc:  # noqa: BLE001
                    self._logger.warning(
                        "ParrotKnowledgeBuilder: pageindex failed for %s, skipping: %s",
                        source_str, exc,
                    )
                    continue

                artifacts.append(
                    KnowledgeArtifact(
                        kind="tree",
                        index_type="pageindex",
                        source=source_str,
                        tree=tree,            # lean index kept in the payload too
                        node_markdown={},     # bodies live on disk, not embedded
                        metadata={
                            "storage_dir": str(storage_dir),
                            "tree_name": tree_name,
                            "index_file": str(storage_dir / f"{tree_name}.json"),
                            "content_dir": str(storage_dir / tree_name),
                        },
                    )
                )

        if self._fail_on_empty and not artifacts:
            raise DataNotFound(
                "ParrotKnowledgeBuilder: pageindex extraction produced no trees "
                f"across {len(sources)} source(s)."
            )

        self._result = artifacts
        self.add_metric("NUM_TREES", len(artifacts))
        self.add_metric("STORAGE_DIR", str(storage_dir))

    async def close(self) -> None:
        """Release resources (LLM client, etc.)."""
