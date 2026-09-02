"""Schema validator for parsed Flowtask tasks.

Validates a :class:`ParsedTask` against the JSON Schemas shipped under
``flowtask/documentation/generated/components/``. Designed to be **pragmatic**,
not strict:

* Unknown component → ``error``.
* Missing required attribute → ``error``.
* Unexpected attribute (key not in schema ``properties``) → ``warning``
  (component classes frequently accept extra kwargs forwarded by the runtime).
* Type mismatches are NOT enforced. The current schema generator emits
  ``"type": "string"`` for many fields that actually accept dicts/lists, so
  strict type validation would drown the report in false positives. Once the
  generator emits faithful types this can be tightened.

The validator caches loaded schemas in memory and never mutates the on-disk
files.
"""
from __future__ import annotations

import logging
from importlib import resources
from pathlib import Path
from typing import Any, Literal, Optional

import orjson
from pydantic import BaseModel, Field

from .parser import ParsedStep, ParsedTask


class ValidationIssue(BaseModel):
    """Single validation finding."""

    step_index: int
    step_name: Optional[str] = Field(
        None, description="Reserved for explicit step names (not yet supported in YAML)."
    )
    component: Optional[str] = None
    attribute: Optional[str] = Field(
        None,
        description="Attribute path within the step's attrs block, e.g. 'credentials.username'.",
    )
    severity: Literal["error", "warning"]
    message: str


class ValidationReport(BaseModel):
    """Aggregate result of validating a parsed task."""

    ok: bool
    component_count: int
    issues: list[ValidationIssue] = Field(default_factory=list)


class FlowtaskSchemaValidator:
    """Validate parsed Flowtask tasks against the generated component schemas.

    The validator can source schemas from one of two places, in order:

    1. A caller-supplied directory (``schemas_dir`` arg).
    2. The packaged ``flowtask.documentation.generated.components`` resource —
       this is what ships with the wheel and is the production default.
    """

    def __init__(self, schemas_dir: Optional[Path] = None) -> None:
        """Initialise the validator.

        Args:
            schemas_dir: Optional override pointing at a directory of
                ``<Component>.doc.json`` files (each carries the JSON Schema
                under its ``schema`` key). When ``None`` the validator reads
                from the installed package via :mod:`importlib.resources`.
        """
        self._schemas_dir = Path(schemas_dir) if schemas_dir is not None else None
        self._cache: dict[str, dict[str, Any]] = {}
        self._known_components: Optional[set[str]] = None
        # Cached {name: (consumes, produces)} populated lazily from the
        # schemas' ``x-flowtask-io`` extension. Used by the boundary check
        # and by the bridge lookup.
        self._io_cache: Optional[dict[str, tuple[str, str]]] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def validate(self, parsed: ParsedTask) -> ValidationReport:
        """Validate every step in a parsed task.

        Runs two passes:

        * **Per-step**: unknown component, missing required, extra attribute.
        * **Boundary**: between consecutive steps, the previous step's
          ``produces`` must match the next step's ``consumes``. ``any`` on
          either side disables the check (polymorphic components opt out).

        Args:
            parsed: Output of :class:`YamlTaskParser.parse`.

        Returns:
            ValidationReport with ``ok=True`` iff no ``error``-severity issues.
        """
        issues: list[ValidationIssue] = []
        for step in parsed.steps:
            issues.extend(self._validate_step(step))

        issues.extend(self._validate_boundaries(parsed.steps))

        ok = not any(i.severity == "error" for i in issues)
        return ValidationReport(
            ok=ok,
            component_count=len(parsed.steps),
            issues=issues,
        )

    def known_components(self) -> set[str]:
        """Return the set of component names the validator can resolve.

        Lazily populated on first call.
        """
        if self._known_components is None:
            self._known_components = self._discover_components()
        return self._known_components

    # ------------------------------------------------------------------
    # Step-level
    # ------------------------------------------------------------------

    def _validate_step(self, step: ParsedStep) -> list[ValidationIssue]:
        schema = self._load_schema(step.component)
        if schema is None:
            return [
                ValidationIssue(
                    step_index=step.step_index,
                    component=step.component,
                    severity="error",
                    message=f"Unknown component '{step.component}'.",
                )
            ]

        issues: list[ValidationIssue] = []
        properties: dict[str, Any] = schema.get("properties", {}) or {}
        required: list[str] = list(schema.get("required", []) or [])

        # Missing required.
        for key in required:
            if key not in step.attrs:
                issues.append(
                    ValidationIssue(
                        step_index=step.step_index,
                        component=step.component,
                        attribute=key,
                        severity="error",
                        message=f"Missing required attribute '{key}'.",
                    )
                )

        # Unexpected attributes — warning only.
        for key in step.attrs.keys():
            if key not in properties:
                issues.append(
                    ValidationIssue(
                        step_index=step.step_index,
                        component=step.component,
                        attribute=key,
                        severity="warning",
                        message=(
                            f"Attribute '{key}' is not declared in the schema for "
                            f"'{step.component}'. It may be a valid runtime kwarg, "
                            "but typo-check is recommended."
                        ),
                    )
                )

        return issues

    # ------------------------------------------------------------------
    # Boundary check
    # ------------------------------------------------------------------

    def _validate_boundaries(
        self, steps: list[ParsedStep]
    ) -> list[ValidationIssue]:
        """Detect incompatible dataflow boundaries between consecutive steps.

        Skips pairs where either side declares ``any`` — that's the escape
        hatch for polymorphic components. Unknown components are skipped
        too because they'll already have their own `error` issue from the
        per-step pass; piling on a boundary error would only confuse.
        """
        if len(steps) < 2:
            return []

        issues: list[ValidationIssue] = []
        for idx in range(len(steps) - 1):
            here = steps[idx]
            nxt = steps[idx + 1]

            here_io = self._component_io(here.component)
            next_io = self._component_io(nxt.component)
            if here_io is None or next_io is None:
                continue  # unknown component handled elsewhere

            produces = here_io[1]
            consumes = next_io[0]
            if produces == "any" or consumes == "any":
                continue
            if produces == consumes:
                continue

            bridges = self.find_bridges(produces, consumes)
            suggestion = (
                f" Bridge {produces} → {consumes} with one of: "
                f"{', '.join(bridges[:3])}."
                if bridges
                else f" No bridge component found in the corpus for {produces} → {consumes}."
            )
            issues.append(
                ValidationIssue(
                    step_index=idx + 1,
                    component=nxt.component,
                    severity="error",
                    message=(
                        f"Boundary mismatch: step #{idx} ({here.component}) "
                        f"produces '{produces}' but step #{idx + 1} "
                        f"({nxt.component}) consumes '{consumes}'.{suggestion}"
                    ),
                )
            )
        return issues

    def find_bridges(self, produces: str, consumes: str) -> list[str]:
        """Return component names that bridge a ``produces`` → ``consumes`` gap.

        A bridge ``B`` is any component where
        ``B.consumes == produces`` and ``B.produces == consumes``. Useful for
        the agent to call directly (via the toolkit) when the validator
        reports a mismatch.

        Args:
            produces: What the upstream step emits (e.g. ``"file"``).
            consumes: What the downstream step expects (e.g. ``"dataframe"``).

        Returns:
            Sorted list of candidate component names. Empty when no bridge
            exists in the corpus.
        """
        catalogue = self._all_io()
        return sorted(
            name
            for name, (c, p) in catalogue.items()
            if c == produces and p == consumes
        )

    def _component_io(self, name: str) -> Optional[tuple[str, str]]:
        """Return ``(consumes, produces)`` for a component, or None if unknown."""
        return self._all_io().get(name)

    def _all_io(self) -> dict[str, tuple[str, str]]:
        """Lazily load every component's dataflow contract."""
        if self._io_cache is not None:
            return self._io_cache
        cache: dict[str, tuple[str, str]] = {}
        for name in self.known_components():
            schema = self._load_schema(name)
            if not schema:
                continue
            io = schema.get("x-flowtask-io") or {}
            consumes = io.get("consumes", "any")
            produces = io.get("produces", "any")
            cache[name] = (consumes, produces)
        self._io_cache = cache
        return cache

    # ------------------------------------------------------------------
    # Schema I/O
    # ------------------------------------------------------------------

    def _load_schema(self, component: str) -> Optional[dict[str, Any]]:
        """Return the cached schema for a component, or ``None`` if unknown.

        Reads the merged ``<Component>.doc.json`` and extracts the JSON Schema
        from its ``schema`` key. The validator never needs the prose fields.
        """
        if component in self._cache:
            return self._cache[component]

        raw = self._read_doc_bytes(component)
        if raw is None:
            return None

        try:
            doc = orjson.loads(raw)
        except orjson.JSONDecodeError as exc:
            self.logger.warning("Malformed doc for %s: %s", component, exc)
            return None

        schema = doc.get("schema")
        if not isinstance(schema, dict):
            self.logger.warning(
                "Doc for %s has no embedded schema; treating as unknown.",
                component,
            )
            return None

        self._cache[component] = schema
        return schema

    def _read_doc_bytes(self, component: str) -> Optional[bytes]:
        filename = f"{component}.doc.json"

        if self._schemas_dir is not None:
            path = self._schemas_dir / filename
            if path.is_file():
                return path.read_bytes()
            return None

        try:
            # MultiplexedPath (namespace packages) only accepts a single arg
            # per joinpath() call — chain instead of passing multiple parts.
            res = (
                resources.files("flowtask.documentation.generated")
                .joinpath("components")
                .joinpath(filename)
            )
        except (ModuleNotFoundError, AttributeError):
            return None

        if not res.is_file():
            return None
        return res.read_bytes()

    def _discover_components(self) -> set[str]:
        if self._schemas_dir is not None:
            return {
                p.name.removesuffix(".doc.json")
                for p in self._schemas_dir.glob("*.doc.json")
            }
        try:
            components_dir = resources.files(
                "flowtask.documentation.generated"
            ).joinpath("components")
        except (ModuleNotFoundError, AttributeError):
            return set()
        return {
            entry.name.removesuffix(".doc.json")
            for entry in components_dir.iterdir()
            if entry.name.endswith(".doc.json")
        }
