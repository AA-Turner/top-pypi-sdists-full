from __future__ import annotations

import abc
import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Iterable, Mapping, Sequence

if TYPE_CHECKING:
    from chalk.queries.scheduled_query import ScheduledQuery

# Schema the checked table is registered under, so a check reads `FROM dqm.input`.
DQM_SCHEMA = "dqm"

# Environment variable the engine reads specs from when it cannot import this source.
CHECK_SPECS_ENV_VAR = "CHALK_DQM_CHECK_SPECS"

# Column-name suffixes that make an output column a result.
CHECK_SUFFIXES = ("_check", "_metric", "_distribution")

# Default predicate for a bad-rows check: every row the source returns is a bad one. A
# predicate matching everything is what "the finding *is* the query" means, so it is the
# default rather than a separate mode.
ALL_ROWS = "TRUE"

# Alias the compiled SQL gives an expression, so the threshold can reference it once
# instead of repeating (and recomputing) the expression for every comparison.
_VALUE_ALIAS = "dqm_value"

_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


class DataQualityStage(str, Enum):
    INPUT = "input"
    """The query's input -- its spine, however it was produced. Checked before anything
    shards on it, so a failure stops the query before a single shard is planned."""

    OUTPUT = "output"
    """The query's computed output, checked before it is written to the online/offline
    stores."""

    @property
    def table(self) -> str:
        """The table name a check at this stage selects from, e.g. `dqm.input`."""
        return f"{DQM_SCHEMA}.{self.value}"

    @property
    def other(self) -> "DataQualityStage":
        return DataQualityStage.OUTPUT if self is DataQualityStage.INPUT else DataQualityStage.INPUT


class DataQualityCheckKind(str, Enum):
    SQL = "sql"
    BOOL = "bool"
    BAD_ROWS = "bad_rows"
    METRIC = "metric"
    DISTRIBUTION = "distribution"


class DataQualityCheckError(ValueError):
    """A check could not be compiled into runnable SQL."""


@dataclass(frozen=True)
class CompiledCheck:
    name: str
    sql: str
    terminate_on_failure: bool
    kind: DataQualityCheckKind
    stage: DataQualityStage
    description: str | None = None
    source_sql: str | None = None
    preview_sql: str | None = None

    def to_assertion(self) -> dict[str, Any]:
        """This check as one entry in a spec's `assertions` list.

        `name` / `sql` / `terminate_on_failure` are the engine's `DqmAssertion` fields; the
        rest are extra keys, which its parser ignores. That asymmetry is deliberate -- it
        means a chalkpy that knows about a new kind still produces specs an older engine
        runs correctly, just without the extra reporting.
        """
        assertion: dict[str, Any] = {
            "name": self.name,
            "sql": self.sql,
            "terminate_on_failure": self.terminate_on_failure,
            "kind": self.kind.value,
        }
        for key, value in (
            ("description", self.description),
            ("source_sql", self.source_sql),
            ("preview_sql", self.preview_sql),
        ):
            if value is not None:
                assertion[key] = value
        return assertion


@dataclass(frozen=True, kw_only=True)
class DataQualityCheck(abc.ABC):
    """A data quality check. Build one with a `sql_*` constructor rather than directly.

    Parameters
    ----------
    name
        Identifies the check in logs, metrics and failure summaries, and names the columns
        the compiled SQL selects. Required for every kind but `sql_raw`, which takes its
        name from the first result column the query selects.
    terminate_on_failure
        When `True` (the default) a failing check fails the run and cancels the downstream
        work. When `False` the check is advisory: failures are still logged and reported,
        but the run proceeds. Gating is per check, so one advisory check does not make its
        neighbors advisory.
    description
        Free text shown alongside a failure, for saying what the check is protecting and
        what to do when it trips.

    Examples
    --------
    >>> from chalk.queries import Check
    >>> Check.sql_metric('count("user.email") * 1.0 / count(*)', min=0.9, name="email_coverage")
    """

    name: str | None = None
    terminate_on_failure: bool = True
    description: str | None = None
    kind: ClassVar[DataQualityCheckKind]

    @staticmethod
    def sql_bool(
        expression: str,
        *,
        name: str,
        from_sql: str | None = None,
        terminate_on_failure: bool = True,
        description: str | None = None,
    ) -> "SqlBoolCheck":
        """Assert that a boolean SQL expression over the checked table holds.

        Takes the expression rather than a whole `SELECT` so the checked table is inferred.
        Pass `from_sql` to check over a derived table instead.

        Parameters
        ----------
        expression
            A boolean aggregate over the checked table, e.g. `count(*) > 0`. Feature columns
            are dotted, so they must be quoted: `"user.id"`, not `user.id`. An expression
            that evaluates to null counts as a failure.
        from_sql
            A query to check over instead of the stage's table, e.g. a group-by whose groups
            are the thing being asserted on.

        Examples
        --------
        >>> from chalk.queries import Check
        >>> Check.sql_bool('count(DISTINCT "txn.mcc") >= 10', name="enough_mccs")
        """
        return SqlBoolCheck(
            expression,
            from_sql=from_sql,
            name=name,
            terminate_on_failure=terminate_on_failure,
            description=description,
        )

    @staticmethod
    def sql_bad_rows(
        where: str = ALL_ROWS,
        *,
        name: str,
        from_sql: str | None = None,
        max_bad_rows: int = 0,
        preview_rows: int = 10,
        terminate_on_failure: bool = True,
        description: str | None = None,
    ) -> "SqlBadRowsCheck":
        """Assert that no row matches a predicate -- the rows themselves are the failure.

        The check passes when no more than `max_bad_rows` rows match, and reports the count
        either way, so a rule that is being tightened can be watched before it is enforced.
        Stating the failure as rows rather than as a boolean is what makes it diagnosable:
        the query that found them is the query you re-run to look at them.

        Parameters
        ----------
        where
            A predicate selecting the rows that should not exist. Omit it to treat every row
            `from_sql` returns as bad, which is the shape to use when the finding is the
            query rather than a filter over it.
        from_sql
            A query to look for bad rows in, instead of the stage's table.
        max_bad_rows
            How many offending rows to tolerate. Defaults to 0.
        preview_rows
            How many offending rows to keep for the failure record.

        Examples
        --------
        >>> from chalk.queries import Check
        >>> Check.sql_bad_rows('"user.email" IS NULL', name="missing_email")

        A finder query, where every row it returns is a bad one:

        >>> Check.sql_bad_rows(
        ...     from_sql='SELECT "user.id" FROM dqm.output GROUP BY "user.id" HAVING count(*) > 1',
        ...     name="duplicate_users",
        ... )
        """
        return SqlBadRowsCheck(
            where,
            from_sql=from_sql,
            max_bad_rows=max_bad_rows,
            preview_rows=preview_rows,
            name=name,
            terminate_on_failure=terminate_on_failure,
            description=description,
        )

    @staticmethod
    def sql_metric(
        expression: str,
        *,
        name: str,
        min: float | None = None,  # noqa: A002 - reads as a bound, which is the point
        max: float | None = None,  # noqa: A002
        equals: float | None = None,
        from_sql: str | None = None,
        terminate_on_failure: bool = True,
        description: str | None = None,
    ) -> "SqlMetricCheck":
        """Report a number, and optionally assert that it is within bounds.

        The number is always reported as a gauge, whether or not it is thresholded, so the
        thing being asserted on is plottable and a threshold can be chosen from the history
        rather than guessed. With no bound at all this is pure observability.

        Parameters
        ----------
        expression
            A numeric aggregate over the checked table, e.g. `count(*)`.
        min, max
            Inclusive bounds. Give either, both, or neither.
        equals
            An exact value the metric must equal. Mutually exclusive with `min` / `max`.
        from_sql
            A query to measure over instead of the stage's table.

        Examples
        --------
        >>> from chalk.queries import Check
        >>> Check.sql_metric("count(*)", min=1000, name="spine_rows")
        """
        return SqlMetricCheck(
            expression,
            min=min,
            max=max,
            equals=equals,
            from_sql=from_sql,
            name=name,
            terminate_on_failure=terminate_on_failure,
            description=description,
        )

    @staticmethod
    def sql_distribution(
        expression: str,
        *,
        name: str,
        from_sql: str | None = None,
        description: str | None = None,
    ) -> "SqlDistributionCheck":
        """Report an array of numbers as histogram bucket counts.

        A distribution is a group-then-collect, so `from_sql` is usually where the work is.
        Distributions only report; there is nothing here that can fail a run.

        Examples
        --------
        >>> from chalk.queries import Check
        >>> Check.sql_distribution(
        ...     "array_agg(n)",
        ...     from_sql='SELECT count(*) AS n FROM dqm.output GROUP BY "txn.mcc"',
        ...     name="mcc_frequencies",
        ... )
        """
        return SqlDistributionCheck(
            expression,
            from_sql=from_sql,
            name=name,
            description=description,
        )

    @staticmethod
    def sql_raw(
        sql: str,
        *,
        name: str | None = None,
        terminate_on_failure: bool = True,
        description: str | None = None,
    ) -> "SqlRawCheck":
        """Run a query exactly as written, naming its own result columns.

        The query must select `_check` / `_metric` / `_distribution` columns itself,
        from `dqm.input` or `dqm.output`, and must aggregate the whole table down to
        exactly one row.

        Examples
        --------
        >>> from chalk.queries import Check
        >>> Check.sql_raw(
        ...     '''SELECT count("user.email") * 1.0 / count(*)        AS email_coverage_metric,
        ...               count("user.email") * 1.0 / count(*) >= 0.9 AS email_coverage_check
        ...        FROM dqm.output'''
        ... )
        """
        return SqlRawCheck(sql, name=name, terminate_on_failure=terminate_on_failure, description=description)

    def compile(self, stage: DataQualityStage) -> CompiledCheck:
        """Lower this check to the SQL that will run at `stage`.

        Raises `DataQualityCheckError` when the check cannot produce runnable SQL; callers
        turn that into a declaration error rather than letting it fail at run time.
        """
        return self._compile_as(self._resolve_name(), stage)

    def _compile_as(self, name: str, stage: DataQualityStage) -> CompiledCheck:
        """Compile under an already-resolved name.

        Resolving is not idempotent -- it strips one result suffix, so running it twice over
        `foo_check_check` would yield `foo` and quietly drop a suffix the author wrote. The
        batch path resolves and dedupes names up front, then compiles through here, so a
        name is resolved exactly once.
        """
        self._check_tables(stage)
        return CompiledCheck(
            name=name,
            sql=self._compile_sql(name=name, stage=stage),
            terminate_on_failure=self.terminate_on_failure,
            kind=self.kind,
            stage=stage,
            description=self.description,
            source_sql=self._source_sql(),
            preview_sql=self._preview_sql(stage),
        )

    @abc.abstractmethod
    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str: ...

    def _resolve_name(self) -> str:
        """The name this check reports under, which is also the stem of its columns."""
        if self.name is None:
            raise DataQualityCheckError(
                f"A `{self.kind.value}` check needs a `name=`: it names the columns the generated SQL "
                + "selects, and identifies the check in metrics and failure summaries."
            )
        name = _strip_suffix(_require_str_name(self.name))
        if not _IDENTIFIER.match(name):
            raise DataQualityCheckError(
                f"Check name '{self.name}' is not a SQL identifier. It becomes a column name in the "
                + "generated query, so it must start with a letter or underscore and contain only "
                + "letters, digits and underscores."
            )
        return name

    def _sql_fragments(self) -> Iterable[str]:
        """Every piece of author-written SQL, for the wrong-table check below."""
        return ()

    def _check_tables(self, stage: DataQualityStage) -> None:
        """Reject a check that can only read the *other* stage's table.

        Only one of `dqm.input` / `dqm.output` is registered when a check runs, so this
        would fail at run time with nothing to say about why.
        """
        for fragment in self._sql_fragments():
            lowered = fragment.lower()
            if stage.other.table in lowered and stage.table not in lowered:
                raise DataQualityCheckError(
                    f"This check was attached to the `{stage.value}` stage but selects from "
                    + f"`{stage.other.table}`. Checks at the `{stage.value}` stage read `{stage.table}`; "
                    + "only that table is registered when they run."
                )

    def _source_sql(self) -> str | None:
        return None

    def _preview_sql(self, stage: DataQualityStage) -> str | None:
        return None


@dataclass(frozen=True)
class SqlRawCheck(DataQualityCheck):
    """A query run exactly as written. See `DataQualityCheck.sql_raw`."""

    sql: str

    kind: ClassVar[DataQualityCheckKind] = DataQualityCheckKind.SQL

    def _resolve_name(self) -> str:
        if self.name is None:
            return default_check_name(self.sql)
        name = _require_str_name(self.name)
        if not name:
            raise DataQualityCheckError("A check's `name=` must not be empty.")
        return name

    def _sql_fragments(self) -> Iterable[str]:
        return (self.sql,)

    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str:
        if not any(suffix in self.sql.lower() for suffix in CHECK_SUFFIXES):
            raise DataQualityCheckError(
                "This check selects no result columns. A raw check reports through its output column "
                + "names: suffix a column with `_check` to assert on it, or `_metric` / `_distribution` "
                + "to report it."
            )
        return self.sql


@dataclass(frozen=True)
class SqlBoolCheck(DataQualityCheck):
    """A boolean expression over the checked table. See `DataQualityCheck.sql_bool`."""

    expression: str
    from_sql: str | None = None

    kind: ClassVar[DataQualityCheckKind] = DataQualityCheckKind.BOOL

    def _sql_fragments(self) -> Iterable[str]:
        return (self.from_sql,) if self.from_sql is not None else ()

    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str:
        return f"SELECT ({self.expression}) AS {name}_check FROM {_source(self.from_sql, stage)}"

    def _source_sql(self) -> str | None:
        return self.expression


@dataclass(frozen=True)
class SqlBadRowsCheck(DataQualityCheck):
    """A query selecting rows that should not exist. See `DataQualityCheck.sql_bad_rows`."""

    where: str = ALL_ROWS
    from_sql: str | None = None
    max_bad_rows: int = 0
    preview_rows: int = 10

    kind: ClassVar[DataQualityCheckKind] = DataQualityCheckKind.BAD_ROWS

    # The stage is only known at compile time, so the row-selecting query is built twice:
    # once to count for the verdict, once to preview. Both go through `_rows_from` so they
    # cannot drift -- a preview showing different rows than the ones that failed the check
    # would be worse than no preview.
    def _rows_from(self, stage: DataQualityStage) -> str:
        source = _source(self.from_sql, stage)
        if self.where.strip().upper() == ALL_ROWS:
            return source
        return f"{source} WHERE ({self.where})"

    def _sql_fragments(self) -> Iterable[str]:
        return (self.from_sql, self.where) if self.from_sql is not None else (self.where,)

    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str:
        if _looks_like_a_query(self.where):
            raise DataQualityCheckError(
                "`where=` takes a predicate over the checked table, not a whole query -- Chalk "
                + "writes the SELECT. Pass a query as `from_sql=` instead, and every row it "
                + "returns is treated as a bad one."
            )
        if self.max_bad_rows < 0:
            raise DataQualityCheckError(f"`max_bad_rows` must be at least 0; got {self.max_bad_rows}.")
        if self.preview_rows < 0:
            raise DataQualityCheckError(f"`preview_rows` must be at least 0; got {self.preview_rows}.")
        return (
            f"SELECT count(*) AS {name}_bad_rows_metric, "
            + f"count(*) <= {self.max_bad_rows} AS {name}_check "
            + f"FROM {self._rows_from(stage)}"
        )

    def _source_sql(self) -> str | None:
        return self.where

    def _preview_sql(self, stage: DataQualityStage) -> str | None:
        if self.preview_rows == 0:
            return None
        return f"SELECT * FROM {self._rows_from(stage)} LIMIT {self.preview_rows}"


@dataclass(frozen=True)
class SqlMetricCheck(DataQualityCheck):
    """A number, optionally thresholded. See `DataQualityCheck.sql_metric`."""

    expression: str
    min: float | None = None  # noqa: A003 - mirrors the constructor keyword
    max: float | None = None  # noqa: A003
    equals: float | None = None
    from_sql: str | None = None

    kind: ClassVar[DataQualityCheckKind] = DataQualityCheckKind.METRIC

    def _sql_fragments(self) -> Iterable[str]:
        return (self.from_sql,) if self.from_sql is not None else ()

    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str:
        conditions = self._conditions()
        projections = [f"{_VALUE_ALIAS} AS {name}_metric"]
        if conditions:
            projections.append(f"{' AND '.join(conditions)} AS {name}_check")
        # The expression is aliased once in a subquery so each bound references it by name:
        # inlining it would recompute the aggregate for the metric and for every comparison.
        return (
            f"SELECT {', '.join(projections)} "
            + f"FROM (SELECT ({self.expression}) AS {_VALUE_ALIAS} FROM {_source(self.from_sql, stage)})"
        )

    def _conditions(self) -> list[str]:
        if self.equals is not None and (self.min is not None or self.max is not None):
            raise DataQualityCheckError("Pass `equals=` or `min=` / `max=`, not both.")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise DataQualityCheckError(f"`min={self.min}` is greater than `max={self.max}`, so nothing can pass.")
        conditions: list[str] = []
        if self.equals is not None:
            conditions.append(f"{_VALUE_ALIAS} = {_render_number('equals', self.equals)}")
        if self.min is not None:
            conditions.append(f"{_VALUE_ALIAS} >= {_render_number('min', self.min)}")
        if self.max is not None:
            conditions.append(f"{_VALUE_ALIAS} <= {_render_number('max', self.max)}")
        return conditions

    def _source_sql(self) -> str | None:
        return self.expression


@dataclass(frozen=True)
class SqlDistributionCheck(DataQualityCheck):
    """An array read as bucket counts. See `DataQualityCheck.sql_distribution`."""

    expression: str
    from_sql: str | None = None

    kind: ClassVar[DataQualityCheckKind] = DataQualityCheckKind.DISTRIBUTION

    def _sql_fragments(self) -> Iterable[str]:
        return (self.from_sql,) if self.from_sql is not None else ()

    def _compile_sql(self, *, name: str, stage: DataQualityStage) -> str:
        return f"SELECT ({self.expression}) AS {name}_distribution FROM {_source(self.from_sql, stage)}"

    def _source_sql(self) -> str | None:
        return self.expression


Check = DataQualityCheck
"""Short alias, so a declaration reads `Check.sql_bool(...)`."""


def _source(from_sql: str | None, stage: DataQualityStage) -> str:
    """Where a compiled check selects from: the stage's table, or the author's subquery."""
    return stage.table if from_sql is None else f"({from_sql})"


def _looks_like_a_query(fragment: str) -> bool:
    """Whether a fragment is a whole SELECT rather than the expression that was asked for.

    Attempting to fail fast when incorrect.
    """
    return fragment.strip().upper().startswith(("SELECT ", "WITH "))


def _require_str_name(value: object) -> str:
    """Guard a declared name against a type checker's blind spot."""
    if not isinstance(value, str):
        raise DataQualityCheckError(f"A check's `name=` must be a string; got {type(value).__name__}.")
    return value


def _render_number(keyword: str, value: object) -> str:
    """Render a bound as a SQL literal."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DataQualityCheckError(f"`{keyword}=` must be a number; got {type(value).__name__}.")
    return str(value) if isinstance(value, int) else repr(float(value))


def _strip_suffix(name: str) -> str:
    """Drop a result suffix an author included in the name.

    `name="non_empty_check"` is the natural thing to write, and appending our own suffix to
    it would report the check as `non_empty_check_check`.
    """
    for suffix in CHECK_SUFFIXES:
        if name.endswith(suffix) and len(name) > len(suffix):
            return name[: -len(suffix)]
    return name


def default_check_name(sql: str) -> str:
    """Name an unnamed raw check after the first result column it selects.

    A generated name shows up in logs, in metric tags and in the failure summary, so it is
    worth deriving something recognizable rather than an index. Mirrors the engine's own
    derivation so a check is called the same thing on both sides.
    """
    lowered = sql.lower().replace("\n", " ")
    for token in lowered.split():
        candidate = token.strip().strip(",").strip('"')
        if candidate.endswith(CHECK_SUFFIXES):
            return candidate
    return "check"


def _coerce(item: object, *, stage: DataQualityStage, index: int) -> DataQualityCheck:
    if isinstance(item, DataQualityCheck):
        return item
    if isinstance(item, str):
        # A bare string is the raw form: it is already a complete query naming its own
        # result columns, which is the only kind that needs nothing else to run.
        return SqlRawCheck(item)
    raise TypeError(
        f"Data quality check at position {index} of `{stage.value}=` must be a SQL string or a "
        + "check built with `Check.sql_bool(...)`, `Check.sql_bad_rows(...)` or another `Check.sql_*` "
        + f"constructor; got {type(item).__name__}."
    )


def compile_checks(
    items: Iterable[str | DataQualityCheck],
    *,
    stage: DataQualityStage,
    context: str,
) -> tuple[list[CompiledCheck], list[str]]:
    """Compile every check declared for one stage.

    Returns the checks that compiled and a message for each that did not, so a declaration
    with two mistakes in it reports both rather than one at a time. A check that failed to
    compile is left out: there is no SQL to run for it, and attaching a broken check would
    make a query that reports a failure it never actually evaluated.
    """
    checks = [_coerce(item, stage=stage, index=index) for index, item in enumerate(items)]
    errors: list[str] = []

    def _error(check: DataQualityCheck, index: int, e: DataQualityCheckError) -> None:
        errors.append(f"Data quality check '{check.name or f'at position {index}'}' on {context}: {e}")

    # Names are resolved before anything is compiled, because a name is baked into the
    # column names of the SQL we generate: deduping afterwards would mean rewriting a query
    # string, and a name that happens to appear elsewhere in the SQL would be rewritten too.
    seen: dict[str, int] = {}
    named: list[tuple[int, DataQualityCheck, str]] = []
    for index, check in enumerate(checks):
        try:
            name = check._resolve_name()  # pyright: ignore[reportPrivateUsage]
        except DataQualityCheckError as e:
            _error(check, index, e)
            continue
        count = seen.get(name, 0)
        seen[name] = count + 1
        # Two checks reporting under the same name would collide in the metric tag and the
        # failure summary, which would silently conflate them.
        named.append((index, check, name if count == 0 else f"{name}_{count + 1}"))

    compiled: list[CompiledCheck] = []
    for index, check, name in named:
        try:
            # `_compile_as`, not `compile`: the name is already resolved, and resolving it a
            # second time would strip a second suffix off it.
            compiled.append(check._compile_as(name, stage))  # pyright: ignore[reportPrivateUsage]
        except DataQualityCheckError as e:
            _error(check, index, e)
    return compiled, errors


def attach_checks(
    query: "ScheduledQuery",
    *,
    input: Iterable[str | DataQualityCheck] = (),  # noqa: A002 - the keyword names the stage
    output: Iterable[str | DataQualityCheck] = (),
) -> "ScheduledQuery":
    """Attach checks to `query` and return it, so the call wraps the declaration in place.

    Implements `ScheduledQuery.with_checks`; see there for the customer-facing docs.
    """
    for stage, items in ((DataQualityStage.INPUT, input), (DataQualityStage.OUTPUT, output)):
        compiled, errors = compile_checks(items, stage=stage, context=f"scheduled query '{query.name}'")
        query.errors.extend(errors)
        if not compiled:
            continue
        if query.checks_for_stage(stage):
            # Attaching twice would leave two sets of checks with the same names racing to
            # report under the same metric tags. One call per stage keeps the declaration
            # and what runs in agreement.
            query.errors.append(
                f"Scheduled query '{query.name}' already has `{stage.value}` data quality checks. "
                + f"Pass every {stage.value} check to a single `with_checks(...)` call."
            )
            continue
        if stage is DataQualityStage.INPUT:
            query.input_checks = tuple(compiled)
        else:
            query.output_checks = tuple(compiled)
        _register_with_engine(query_name=query.name, stage=stage, checks=compiled)
    return query


def _register_with_engine(*, query_name: str, stage: DataQualityStage, checks: Sequence[CompiledCheck]) -> None:
    """Mirror the checks into the engine's own registry, when there is one to mirror into.

    The engine reads its registry directly for deployments that import the customer's
    source, which is the only kind of process where `chalkengine` is importable at all --
    hence a guarded import rather than a dependency. Everywhere else (a local `chalk apply`,
    a unit test) this is a no-op and the checks travel through `dumps_check_specs`.
    """
    try:
        from chalkengine.dqm.authoring import DEFAULT_REGISTRY  # pyright: ignore[reportMissingImports]
        from chalkshared.rpc_models.dqm import DqmAssertion  # pyright: ignore[reportMissingImports]
    except ImportError:
        return

    assertions = [DqmAssertion(name=c.name, sql=c.sql, terminate_on_failure=c.terminate_on_failure) for c in checks]
    kwargs = {stage.value: assertions}
    DEFAULT_REGISTRY.with_checks(query_name, **kwargs)


def build_check_specs(
    *,
    query_name: str | None,
    input_checks: Sequence[CompiledCheck] = (),
    output_checks: Sequence[CompiledCheck] = (),
) -> list[dict[str, Any]]:
    """One spec per non-empty stage, in the shape the engine's `DqmCheckSpec` parses.

    `query_name=None` leaves the specs unscoped, which is what an ad-hoc offline query wants:
    it has no scheduled-query name to match on, and the specs reach it on its own job's
    environment rather than the deployment's, so there is nothing else they could apply to.
    """
    specs: list[dict[str, Any]] = []
    for stage, checks in ((DataQualityStage.INPUT, input_checks), (DataQualityStage.OUTPUT, output_checks)):
        if not checks:
            continue
        specs.append(
            {
                "name": f"{query_name}.{stage.value}" if query_name else stage.value,
                "stage": stage.value,
                "query_name": query_name,
                "assertions": [check.to_assertion() for check in checks],
            }
        )
    return specs


def check_specs(queries: Mapping[str, "ScheduledQuery"] | None = None) -> list[dict[str, Any]]:
    """The data quality specs declared across every scheduled query, as plain dicts.

    Defaults to every query declared in this process. One spec per query per stage, matching
    the shape the engine's `CHALK_DQM_CHECK_SPECS` expects.
    """
    if queries is None:
        from chalk.queries.scheduled_query import CRON_QUERY_REGISTRY

        queries = CRON_QUERY_REGISTRY

    specs: list[dict[str, Any]] = []
    for query in queries.values():
        specs.extend(
            build_check_specs(
                query_name=query.name,
                input_checks=query.input_checks,
                output_checks=query.output_checks,
            )
        )
    return specs


def dumps_check_specs(queries: Mapping[str, "ScheduledQuery"] | None = None) -> str:
    """Serialize declared checks into the JSON `CHALK_DQM_CHECK_SPECS` expects.

    The bridge for deployments whose engine never imports the customer's source: run this
    where the source *is* imported and set the result as the environment variable.

    Examples
    --------
    >>> from chalk.queries import dumps_check_specs
    >>> print(dumps_check_specs())  # doctest: +SKIP
    ["{\\"name\\": \\"ingest_users.input\\", ...}"]
    """
    return dumps_specs(check_specs(queries))


def dumps_specs(specs: Sequence[Mapping[str, Any]]) -> str:
    """Encode specs the way `CHALK_DQM_CHECK_SPECS` is read: a JSON array of JSON strings."""
    return json.dumps([json.dumps(spec) for spec in specs])


def check_env_overrides(
    *,
    input: Iterable[str | DataQualityCheck] = (),  # noqa: A002 - the keyword names the stage
    output: Iterable[str | DataQualityCheck] = (),
    query_name: str | None = None,
    context: str = "this offline query",
) -> dict[str, str]:
    """Compile checks into the environment an offline query's job should run with.

    A scheduled query's checks reach the engine because the deployment imported the source
    that declared them. An offline query has no such declaration -- it is a call, not a
    deployment -- so its checks travel on the job's own environment instead, which is the
    same surface an operator uses to configure checks for a deployment.

    Compilation problems raise here rather than being collected: a scheduled query reports
    them as `chalk apply` diagnostics, but there is no later point at which the caller of an
    offline query would see them.
    """
    compiled: dict[str, list[CompiledCheck]] = {}
    errors: list[str] = []
    for stage, items in ((DataQualityStage.INPUT, input), (DataQualityStage.OUTPUT, output)):
        stage_checks, stage_errors = compile_checks(items, stage=stage, context=context)
        compiled[stage.value] = stage_checks
        errors.extend(stage_errors)
    if errors:
        raise DataQualityCheckError("\n".join(errors))

    specs = build_check_specs(
        query_name=query_name,
        input_checks=compiled[DataQualityStage.INPUT.value],
        output_checks=compiled[DataQualityStage.OUTPUT.value],
    )
    return {CHECK_SPECS_ENV_VAR: dumps_specs(specs)} if specs else {}
