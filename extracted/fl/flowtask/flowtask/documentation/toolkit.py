"""ComponentDocsToolkit — ai-parrot toolkit for Flowtask component discovery.

Reads the JSON schemas + docs shipped under
``flowtask/documentation/generated/`` and exposes them as ai-parrot tools so an
orchestrator agent can translate natural-language requests into Flowtask
YAML.

Stays deterministic on purpose:

* Discovery uses BM25 over name + category + description (rank_bm25). Embedding
  ranker is an opt-in upgrade for a future iteration.
* Retrieval is exact-match by component name and returns the schema verbatim
  — never embedded, never re-shaped.
* ``validate_flowtask_yaml`` is a thin wrapper over
  :mod:`flowtask.factory.parser` + :mod:`flowtask.factory.validator`.

Design choices:

* Public methods are async and have docstrings + type hints; ai-parrot's
  ``AbstractToolkit`` turns them into tools automatically. Internal helpers
  are listed in :attr:`exclude_tools`.
* All data is held in memory (~120 components × small JSON ≈ <2 MB).
* This module imports :mod:`parrot.tools.toolkit`. If ai-parrot is not
  installed, the import will fail loudly — that's intentional. Callers that
  only want the underlying data should use
  :class:`flowtask.documentation.generator.ComponentDocGenerator` or the
  factory parser/validator directly.
"""
from __future__ import annotations

import re
from importlib import resources
from typing import Any, Iterable, Literal, Optional

import orjson
from pydantic import BaseModel, Field
from rank_bm25 import BM25Okapi

from parrot.tools.toolkit import AbstractToolkit

from flowtask.factory.composer import (
    BoundNode,
    ComposedTask,
    DagComposer,
    DagNode,
    DagSketch,
)
from flowtask.factory.parser import ParserError, YamlTaskParser
from flowtask.factory.validator import (
    FlowtaskSchemaValidator,
    ValidationIssue,
    ValidationReport,
)


# ---------------------------------------------------------------------------
# Return models
# ---------------------------------------------------------------------------


class ComponentSummary(BaseModel):
    """Lightweight component record returned by list/search calls."""

    name: str = Field(..., description="Component class name.")
    category: str = Field(..., description="Curated category, e.g. 'Download'.")
    description: str = Field(..., description="One-line summary from the docstring.")
    score: Optional[float] = Field(
        None,
        description="BM25 score from the last search. Higher is better; omitted for non-search calls.",
    )


class CategoryInfo(BaseModel):
    """Category bucket with its components."""

    name: str
    count: int
    components: list[str]


class ComponentAttribute(BaseModel):
    """Single attribute definition for a component."""

    name: str
    required: bool
    description: str = ""
    default: Optional[str] = None


class ComponentDetail(BaseModel):
    """Full component documentation + JSON schema."""

    name: str
    category: str
    description: str
    version: Optional[str] = None
    attributes: list[ComponentAttribute]
    json_schema: dict = Field(..., description="JSON Schema for the component's attribute block.")
    examples: list[str] = Field(default_factory=list)


class ValidationFinding(ValidationIssue):
    """Alias of :class:`flowtask.factory.validator.ValidationIssue`.

    Kept as a public class so the toolkit's tool schema is self-contained
    and doesn't leak the internal factory model name.
    """


class ComponentNotFoundError(KeyError):
    """Raised when a tool is asked about a component that isn't documented."""


# ---------------------------------------------------------------------------
# Toolkit
# ---------------------------------------------------------------------------


_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def _attributes_from_schema(schema: dict[str, Any]) -> list["ComponentAttribute"]:
    """Reconstruct the per-attribute view from a JSON Schema dict.

    Used by :meth:`ComponentDocsToolkit.get_component` to populate the
    flat ``attributes`` list it has historically returned. Pulls names,
    descriptions, and defaults from ``properties`` and required-ness from
    the top-level ``required`` array.
    """
    properties: dict[str, Any] = schema.get("properties") or {}
    required: set[str] = set(schema.get("required") or [])
    attrs: list[ComponentAttribute] = []
    for name, prop in properties.items():
        if not isinstance(prop, dict):
            continue
        default = prop.get("default")
        attrs.append(
            ComponentAttribute(
                name=name,
                required=name in required,
                description=prop.get("description", "") or "",
                default=str(default) if default is not None else None,
            )
        )
    return attrs


def _tokenize(text: str) -> list[str]:
    """Tokenise a string for BM25.

    Lower-cases and splits on non-alphanumeric/underscore boundaries. Splits
    CamelCase too so 'DownloadFromSharepoint' yields ['download', 'from',
    'sharepoint'] which dramatically helps recall on NL queries that use
    lowercase noun phrases.
    """
    tokens: list[str] = []
    for raw in _TOKEN_RE.findall(text):
        camel_split = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+", raw)
        if camel_split:
            tokens.extend(t.lower() for t in camel_split)
        else:
            tokens.append(raw.lower())
    return tokens


class ComponentDocsToolkit(AbstractToolkit):
    """Read-only knowledge base of Flowtask components.

    Use this toolkit to give an orchestrator agent the ability to discover,
    retrieve, and validate against the documented Flowtask components.
    """

    tool_prefix: str = "flowtask"

    exclude_tools: tuple[str, ...] = (
        "start",
        "stop",
        "cleanup",
    )

    def __init__(
        self,
        *,
        docs_package: str = "flowtask.documentation.generated",
        **kwargs: Any,
    ) -> None:
        """Initialise the toolkit.

        Args:
            docs_package: Importable package containing ``index.json`` and the
                ``components/`` subdirectory. Override only for tests.
            **kwargs: Forwarded to :class:`AbstractToolkit`.
        """
        super().__init__(**kwargs)
        self._docs_package = docs_package
        self._index: dict[str, Any] = {}
        # name -> merged doc.json (prose + embedded JSON Schema).
        self._components: dict[str, dict[str, Any]] = {}
        # name -> JSON Schema slice extracted from `_components[name]["schema"]`.
        self._schemas: dict[str, dict[str, Any]] = {}
        self._categories: dict[str, list[str]] = {}       # category -> [name]
        self._bm25: Optional[BM25Okapi] = None
        self._bm25_corpus: list[str] = []                 # parallel to _bm25_order
        self._bm25_order: list[str] = []                  # component names
        self._loaded = False
        self._parser = YamlTaskParser()
        self._validator: Optional[FlowtaskSchemaValidator] = None
        self._composer: Optional[DagComposer] = None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Load the index and component files into memory. Idempotent."""
        if self._loaded:
            return

        index_bytes = self._read_resource("index.json")
        self._index = orjson.loads(index_bytes)
        components_map: dict[str, dict[str, Any]] = self._index.get("components", {})

        # Load the merged doc for every component listed in the index. The
        # JSON Schema rides along under the doc's ``schema`` key.
        for name, entry in components_map.items():
            rel = entry.get("file")
            if not rel:
                self.logger.warning("Skipping %s: index entry has no 'file'.", name)
                continue
            try:
                doc_bytes = self._read_resource(rel)
            except FileNotFoundError:
                self.logger.warning("Skipping %s: doc file missing.", name)
                continue
            doc_data = orjson.loads(doc_bytes)
            schema = doc_data.get("schema")
            if not isinstance(schema, dict):
                self.logger.warning(
                    "Skipping %s: doc has no embedded schema.", name
                )
                continue
            self._components[name] = doc_data
            self._schemas[name] = schema
            self._categories.setdefault(entry.get("category", "Other"), []).append(name)

        for names in self._categories.values():
            names.sort()

        # BM25 index over name + category + description.
        self._bm25_order = sorted(self._components.keys())
        self._bm25_corpus = []
        for name in self._bm25_order:
            doc = self._components[name]
            blob = " ".join(
                [
                    name,
                    doc.get("category", ""),
                    doc.get("description", ""),
                ]
            )
            self._bm25_corpus.append(blob)
        if self._bm25_corpus:
            self._bm25 = BM25Okapi([_tokenize(b) for b in self._bm25_corpus])

        # Validator shares the same on-disk schemas via importlib.resources.
        self._validator = FlowtaskSchemaValidator()

        # Composer is wired against the same toolkit methods exposed below so
        # the agent only sees one cohesive tool surface.
        self._composer = DagComposer(
            search_fn=self.search_components,
            get_component_fn=self.get_component,
            validate_yaml_fn=self.validate_flowtask_yaml,
        )
        self._loaded = True

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    async def list_categories(self) -> list[CategoryInfo]:
        """List every category with its components and counts.

        Use this FIRST when the user describes a workflow shape
        ("download then load to Postgres") — it lets the agent narrow to the
        right buckets (e.g. ``Download`` + ``Outputs``) before naming specific
        components.
        """
        await self.start()
        return [
            CategoryInfo(name=cat, count=len(names), components=list(names))
            for cat, names in sorted(self._categories.items())
        ]

    async def search_components(
        self,
        query: str,
        category: Optional[str] = None,
        top_k: int = 8,
    ) -> list[ComponentSummary]:
        """Rank components against a natural-language query (BM25).

        Args:
            query: Free-form description, e.g. "download a file from sharepoint".
            category: Optional category filter — must match a name returned
                by :meth:`list_categories`. ``None`` searches the full corpus.
            top_k: Maximum number of results to return.

        Returns:
            Ranked list, highest score first. May be shorter than ``top_k`` if
            the corpus has fewer matches with non-zero score.
        """
        await self.start()
        if not query.strip() or self._bm25 is None:
            return []

        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(
            zip(self._bm25_order, scores),
            key=lambda pair: pair[1],
            reverse=True,
        )

        results: list[ComponentSummary] = []
        for name, score in ranked:
            if score <= 0:
                break
            doc = self._components[name]
            cat = doc.get("category", "Other")
            if category is not None and cat != category:
                continue
            results.append(
                ComponentSummary(
                    name=name,
                    category=cat,
                    description=doc.get("description", ""),
                    score=float(score),
                )
            )
            if len(results) >= top_k:
                break
        return results

    async def list_components_by_category(self, category: str) -> list[ComponentSummary]:
        """Return every component in a category, sorted alphabetically.

        Cheaper than :meth:`search_components` when the agent already knows
        the bucket and just wants to enumerate options to show the user.

        Args:
            category: Category name — must match :meth:`list_categories`.
        """
        await self.start()
        names = self._categories.get(category, [])
        return [
            ComponentSummary(
                name=name,
                category=category,
                description=self._components[name].get("description", ""),
                score=None,
            )
            for name in names
        ]

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    async def get_component(self, name: str) -> ComponentDetail:
        """Fetch the full doc + JSON schema + examples for one component.

        Use this once the agent has narrowed to a specific candidate so it can
        fill in attributes deterministically against the schema.

        Args:
            name: Exact component class name (case-sensitive).

        Raises:
            ComponentNotFoundError: If the component is not in the corpus.
        """
        await self.start()
        doc = self._components.get(name)
        schema = self._schemas.get(name)
        if doc is None or schema is None:
            raise ComponentNotFoundError(
                f"Component '{name}' is not documented. "
                f"Call search_components or list_categories first."
            )

        return ComponentDetail(
            name=doc["name"],
            category=doc.get("category", "Other"),
            description=doc.get("description", ""),
            version=doc.get("version"),
            attributes=_attributes_from_schema(schema),
            json_schema=schema,
            examples=list(doc.get("examples", [])),
        )

    async def get_component_schema(self, name: str) -> dict:
        """Return only the JSON Schema for a component.

        Use when composing or validating without needing the prose docs.

        Args:
            name: Exact component class name.

        Raises:
            ComponentNotFoundError: If the component is not documented.
        """
        await self.start()
        schema = self._schemas.get(name)
        if schema is None:
            raise ComponentNotFoundError(f"Component '{name}' is not documented.")
        return schema

    async def get_component_examples(self, name: str) -> list[str]:
        """Return only the example YAML snippets for a component.

        Args:
            name: Exact component class name.

        Raises:
            ComponentNotFoundError: If the component is not documented.
        """
        await self.start()
        doc = self._components.get(name)
        if doc is None:
            raise ComponentNotFoundError(f"Component '{name}' is not documented.")
        return list(doc.get("examples", []))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    async def validate_flowtask_yaml(self, yaml_text: str) -> ValidationReport:
        """Parse and validate a draft Flowtask YAML.

        Returns a structured report so the agent can patch errors and retry
        without consulting the user for mechanical fixes.

        Args:
            yaml_text: Full YAML text for the task.
        """
        await self.start()
        assert self._validator is not None  # set in start()

        try:
            parsed = self._parser.parse(yaml_text)
        except ParserError as exc:
            return ValidationReport(
                ok=False,
                component_count=0,
                issues=[
                    ValidationIssue(
                        step_index=-1,
                        severity="error",
                        message=str(exc),
                    )
                ],
            )

        return self._validator.validate(parsed)

    # ------------------------------------------------------------------
    # Dataflow bridges
    # ------------------------------------------------------------------

    async def suggest_bridge(
        self,
        produces: str,
        consumes: str,
    ) -> list[ComponentSummary]:
        """Suggest components that bridge a ``produces`` → ``consumes`` gap.

        Use when the validator reports a boundary mismatch (e.g. the step
        upstream produces ``file`` but the downstream step needs
        ``dataframe`` — call ``suggest_bridge("file", "dataframe")`` to find
        :class:`OpenWithPandas` and friends).

        Args:
            produces: IOType the upstream step emits ("file", "dataframe", ...).
            consumes: IOType the downstream step expects.

        Returns:
            ComponentSummary list sorted alphabetically by name. Empty when
            no bridge exists in the corpus.
        """
        await self.start()
        assert self._validator is not None
        names = self._validator.find_bridges(produces, consumes)
        return [
            ComponentSummary(
                name=name,
                category=self._components[name].get("category", "Other"),
                description=self._components[name].get("description", ""),
                score=None,
            )
            for name in names
            if name in self._components
        ]

    # ------------------------------------------------------------------
    # Composition (two-phase)
    # ------------------------------------------------------------------

    async def sketch_dag(
        self,
        nodes: list[dict],
        per_node_top_k: int = 5,
    ) -> DagSketch:
        """Rank candidate components for each abstract DAG node.

        Phase A of YAML composition. The agent provides abstract nodes — each
        with an ``id``, a ``kind`` (e.g. ``"download"``), optional ``hints``
        for refinement, and ``depends_on``. The toolkit ranks candidate
        components per node via :meth:`search_components` and validates the
        topology (no cycles, no dangling deps). NO YAML is rendered yet.

        Use the returned candidates to confirm the workflow shape with the
        user (or to let the agent self-pick) before calling
        :meth:`compose_flowtask_yaml`.

        Args:
            nodes: List of node specs. Each spec is a dict with keys ``id``,
                ``kind``, optional ``hints``, optional ``depends_on``.
            per_node_top_k: Maximum number of candidate components per node.
        """
        await self.start()
        assert self._composer is not None
        return await self._composer.sketch_dag(nodes, per_node_top_k=per_node_top_k)

    async def compose_flowtask_yaml(
        self,
        nodes: list[dict],
        task_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ComposedTask:
        """Render a Flowtask YAML from a bound DAG.

        Phase B of YAML composition. The agent provides one bound node per
        step — each with ``id``, ``component`` (the picked class name),
        ``attrs``, and ``depends_on``. The toolkit topologically sorts the
        DAG, renders the YAML, validates it, and surfaces any required
        attributes still unset as :attr:`ComposedTask.open_questions` for
        the human-in-the-loop turn.

        Args:
            nodes: List of bound node specs.
            task_name: Optional top-level ``name`` for the rendered YAML.
            description: Optional top-level ``description``.
        """
        await self.start()
        assert self._composer is not None
        return await self._composer.compose_flowtask_yaml(
            nodes,
            task_name=task_name,
            description=description,
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _read_resource(self, relpath: str) -> bytes:
        """Read a file from the docs package via importlib.resources.

        ``relpath`` is taken from the index (``components/Foo.doc.json``) or
        the literal ``"index.json"`` for the root index.
        """
        # MultiplexedPath only accepts one arg per joinpath() call.
        node = resources.files(self._docs_package)
        for part in _split_relpath(relpath):
            node = node.joinpath(part)
        if not node.is_file():
            raise FileNotFoundError(f"{self._docs_package}/{relpath}")
        return node.read_bytes()


def _split_relpath(relpath: str) -> Iterable[str]:
    """Split a forward-slash path while ignoring any leading slashes."""
    for part in relpath.split("/"):
        if part:
            yield part
