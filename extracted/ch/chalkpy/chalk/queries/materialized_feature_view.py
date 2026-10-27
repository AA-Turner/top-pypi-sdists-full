from __future__ import annotations

import ast
import dataclasses
import inspect
import warnings
from datetime import UTC, datetime, timezone
from typing import TYPE_CHECKING, Collection, LiteralString, Type, cast

from typing_extensions import deprecated

from chalk.queries.feature_subset import FeatureSubset
from chalk.utils.collections import FrozenOrderedSet
from chalk.utils.duration import CronTab, Duration

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference
    from chalk.features.feature_field import Feature
    from chalk.features.feature_set import Features

_PLANNABLE_REMOVAL_DATE = datetime(2026, 11, 30, tzinfo=UTC)
_PLANNABLE_REMOVAL_DATE_TEXT = _PLANNABLE_REMOVAL_DATE.strftime("%B %d, %Y")
_PLANNABLE_DEPRECATION_MESSAGE = (
    "MaterializedFeatureView.plannable is deprecated; use queryable instead. "
    f"Support for plannable will be removed after {_PLANNABLE_REMOVAL_DATE_TEXT}."
)
_PLANNABLE_LSP_MESSAGE = cast(LiteralString, _PLANNABLE_DEPRECATION_MESSAGE)


def _feature_reference_nodes(
    features_node: ast.expr | None,
    references: Collection["str | Feature"],
) -> dict["str | Feature", ast.expr]:
    """Map each feature reference to its expression in the call, so a diagnostic can underline it.

    Only a literal list or tuple, passed directly or to `FeatureSubset.include` / `exclude`, can be matched up;
    anything else returns `{}`, and diagnostics underline the whole `features=` argument instead.
    """
    if (
        isinstance(features_node, ast.Call)
        and isinstance(features_node.func, ast.Attribute)
        and features_node.func.attr in ("include", "exclude")
    ):
        features_node = (
            features_node.args[0]
            if features_node.args
            else next((keyword.value for keyword in features_node.keywords if keyword.arg == "features"), None)
        )
    if not isinstance(features_node, (ast.List, ast.Tuple)):
        return {}
    elements = features_node.elts
    if len(elements) != len(references) or any(isinstance(element, ast.Starred) for element in elements):
        return {}
    nodes: dict["str | Feature", ast.expr] = {}
    for reference, element in zip(references, elements):
        nodes.setdefault(reference, element)
    return nodes


class MaterializedFeatureView:
    """Declares materialization scheduling and time-resolution config for one feature namespace.

    Args:
        namespace: The feature class (decorated with ``@features``) or its namespace string.
        time_resolution: Bucket duration for time-series materialization, e.g. ``"1s"``.
        update_cadence: How often to refresh materialized data, as a cron expression or
            duration. Any finite cadence must be at least 10 minutes; more frequent
            updates are not supported. Set ``update_cadence="infinity"`` to disable
            automatic view refreshes.
        lower_bound: Fixed, inclusive lower bound on the feature times of observations
            included in the materialized feature view. Observations with earlier feature
            times continue to be retained in the observation tables, but are not copied
            to the view. Queries using wide table acceleration are therefore not aware
            of these observations. Defaults to ``None``, which applies no fixed lower
            bound.
        lookback_retention_period: Moving retention window on the feature times of
            observations included in the materialized feature view, measured back from
            the current execution time. Observations outside this window are deleted
            from the view. As with observations earlier than ``lower_bound``, they
            continue to be retained in the observation tables, but queries using wide
            table acceleration are not aware of them. When both retention parameters
            are set, the later lower bound applies. Defaults to ``None``, which applies
            no moving retention window, and therefore retains data indefinitely.
        queryable: Whether the planner includes this MaterializedFeatureView (MFV) as a candidate during planning
            for any query. Defaults to ``True``. ``False`` excludes it from reads and
            serves queries from observation tables while the MFV continues to be refreshed.
            ``True`` makes it eligible in the planner for reads. Note that the query must also support wide-table
            acceleration. I.e.m setting the per-query
            ``planner_options={"offline_store_wide_read": False}`` does exclude all MFVs from the planner regardless
            of a per-MFV `queryable` setting.
        plannable: Deprecated alias for ``queryable``. Use ``queryable`` instead.
            Emits ``FutureWarning``. Support will be removed after November 30, 2026 (UTC).
            Supplying both arguments raises ``ValueError``.
        background_compaction: Whether to include this view in automatic background
            compaction. Compaction combines multiple rows into a summary row when
            possible, making the table smaller and reads cheaper. Defaults to ``True``.
            Another option is manual compaction, which can be triggered via the UI.
        features: Which scalar features to materialize. Defaults to ``None``, which materializes
            every offline-store-eligible feature in the namespace. Pass a list to materialize exactly
            those features, or ``FeatureSubset.exclude([...])`` to materialize everything except them,
            which also picks up features added to the namespace later. The primary key is always
            materialized; see [`FeatureSubset`][chalk.FeatureSubset] for how versions are matched.

            Naming a subset reduces the cost of the fill and of background compaction,
            which would otherwise process every column. Excluded features remain fully
            queryable: they are served from the observation tables, which return the same
            values without wide table acceleration.
        resource_group: The resource group used to run fill & maintence jobs for this materialized feature view.
            If not specified, uses the 'default' resource group.

    Examples:
        Materialize only the features a model reads. The rest stay queryable from the observation
        tables, and cost nothing to fill or compact:

        >>> from chalk.features import features
        >>> from chalk.queries.materialized_feature_view import MaterializedFeatureView
        >>> @features
        ... class User:
        ...     id: int
        ...     credit_score: int
        ...     account_age_days: int
        ...     email: str
        >>> _ = MaterializedFeatureView(
        ...     User,
        ...     time_resolution="1h",
        ...     update_cadence="1d",
        ...     features=[User.credit_score, User.account_age_days],
        ... )

        Materialize everything except a few expensive columns. Features added to ``Account`` later
        are materialized without editing the view, and ``raw_payload`` stays queryable from the
        observation tables:

        >>> from chalk import FeatureSubset
        >>> @features
        ... class Account:
        ...     id: int
        ...     balance: float
        ...     open_date_days: int
        ...     raw_payload: str
        >>> _ = MaterializedFeatureView(
        ...     Account,
        ...     time_resolution="1h",
        ...     update_cadence="1d",
        ...     features=FeatureSubset.exclude([Account.raw_payload]),
        ... )

        A bare reference names only a feature's default version, so without ``all_versions=True``
        this would still materialize ``score@2``:

        >>> from chalk.features import feature
        >>> @features
        ... class Transaction:
        ...     id: int
        ...     amount: float
        ...     score: float = feature(version=2)
        >>> _ = MaterializedFeatureView(
        ...     Transaction,
        ...     time_resolution="1h",
        ...     update_cadence="1d",
        ...     features=FeatureSubset.exclude([Transaction.score], all_versions=True),
        ... )

        Create and fill an MFV without having live queries use it:

        ```python
        MaterializedFeatureView(
            User,
            time_resolution="1s",
            update_cadence="1h",
            queryable=False,
        )
        ```

        To cut over a live production system:

        1. Enable wide-table acceleration and check query correctness in staging
           with MFVs enabled.
        2. Deploy the MFV in production with ``queryable=False`` using ``chalk apply`` and observe the initial fill/reresh happen.
        3. Wait for the initial fill to complete.
        4. When critical offline queries are not in flight, change the declaration
           to ``queryable=True`` and redeploy via ``chalk apply`. Once the deploy succeeded, the planner will now automatically switch to MFVs whenever they're available for queries.

        To disable scheduled writes while keeping the filled MFV eligible for reads,
        use this declaration instead:

        ```python
        MaterializedFeatureView(
            User,
            time_resolution="1s",
            update_cadence="infinity",
            queryable=True,
        )
        ```

        Set both ``queryable=False`` and ``update_cadence="infinity"`` to exclude
        the MFV from normal query reads and disable scheduled writes. These settings
        do not cancel an already-running query or fill. The UI also provides options
        to manually trigger fills.
    """

    def __init__(
        self,
        namespace: "Type[Features] | str",
        *,
        time_resolution: Duration,
        update_cadence: "CronTab | Duration",
        lower_bound: datetime | None = None,
        lookback_retention_period: Duration | None = None,
        background_compaction: bool = True,
        queryable: bool | None = None,
        features: "Collection[FeatureReference] | FeatureSubset | None" = None,
        plannable: bool | None = None,
        resource_group: str | None = None,
    ):
        super().__init__()

        # TODO CHA-11885: Remove this code and plannable after 1st December, 2026.
        # Remove the `plannable` parameter, this block, `surface_plannable_deprecation`, the `plannable`
        # property, and the `_PLANNABLE_*` constants. Change the
        # signature to `queryable: bool = True` and assign `self.queryable = queryable` directly.
        if plannable is not None:
            if queryable is not None:
                raise ValueError("Specify only 'queryable'; 'plannable' is a deprecated alias.")
            self.surface_plannable_deprecation(from_constructor=True)
            queryable = plannable
        # The desired default is `True` (CHA-11885 makes the signature `queryable: bool = True`). `None`
        # in the signature lets an explicit `plannable=` be detected as supplied.
        if queryable is None:
            queryable = True

        from chalk._lsp.error_builder import FunctionCallErrorBuilder, get_function_caller_info
        from chalk.features.feature_wrapper import unwrap_feature
        from chalk.parsed.validate_materialized_feature_views import (
            check_features_argument,
            check_namespace_is_unique,
            check_update_cadence,
            namespace_of,
        )

        # Locates this call in the source, so diagnostics can underline its arguments.
        self.lsp_error_builder = FunctionCallErrorBuilder(get_function_caller_info(frame_offset=1))

        namespace_str = namespace_of(namespace, self.lsp_error_builder, self.argument_node("namespace"))

        if lower_bound is not None and lower_bound.tzinfo is not None:
            lower_bound = lower_bound.astimezone(tz=timezone.utc)

        check_update_cadence(update_cadence, self.lsp_error_builder, self.argument_node("update_cadence"))
        # A plain collection is shorthand for an inclusion.
        subset = (
            features
            if features is None or isinstance(features, FeatureSubset)
            else FeatureSubset.include(list(features))
        )
        check_features_argument(subset, self.lsp_error_builder, self.argument_node("features"))
        # Unwrap class attributes to features. Strings are kept and resolved at export, since they may name
        # features defined later.
        references: list[str | Feature] = (
            []
            if subset is None
            else [
                reference if isinstance(reference, str) else unwrap_feature(reference) for reference in subset.features
            ]
        )
        # Must run before `self.features` dedups the references, or they won't line up with the source.
        self._feature_reference_nodes = _feature_reference_nodes(
            self.lsp_error_builder.function_arg_node("features", None), references
        )

        from chalk.utils.object_inspect import get_source_object_starting

        source_line_start: int | None = None
        source_line_end: int | None = None
        source_code: str | None = None
        frame = inspect.currentframe()
        assert frame is not None, "Failed to get current frame"
        caller_frame = frame.f_back
        assert caller_frame is not None, "Failed to get caller frame"
        caller_filename = caller_frame.f_code.co_filename
        try:
            source_code, source_line_start, source_line_end = get_source_object_starting(caller_frame)
        except Exception:
            source_line_start = caller_frame.f_lineno
        del frame

        self.namespace = namespace_str
        self.time_resolution = time_resolution
        self.update_cadence = update_cadence
        self.lower_bound = lower_bound
        self.lookback_retention_period = lookback_retention_period
        self.background_compaction = background_compaction
        self.queryable = queryable
        # `None` means every eligible feature, which the proto spells differently from an explicit selection.
        self.features = None if subset is None else dataclasses.replace(subset, features=FrozenOrderedSet(references))
        self.resource_group: str | None = resource_group
        self.filename = caller_filename
        self.source_line_start = source_line_start
        self.source_line_end = source_line_end
        self.code = source_code

        check_namespace_is_unique(
            namespace_str, MATERIALIZED_FEATURE_VIEW_REGISTRY, self.lsp_error_builder, self.argument_node("namespace")
        )
        MATERIALIZED_FEATURE_VIEW_REGISTRY[namespace_str] = self

    @staticmethod
    def surface_plannable_deprecation(*, from_constructor: bool = False) -> None:
        if from_constructor:
            # Surfaced by `chalk apply` / `chalk lint` at the `plannable=` argument: a warning until one day
            # after the removal date, then an error.
            from chalk._lsp.error_builder import FunctionCallErrorBuilder, LSPErrorBuilder, get_function_caller_info
            from chalk.parsed.duplicate_input_gql import DiagnosticSeverityGQL

            if LSPErrorBuilder.lsp:
                error_builder = FunctionCallErrorBuilder(get_function_caller_info(frame_offset=2))
                plannable_range = error_builder.function_arg_range_by_name("plannable")
                if plannable_range is not None:
                    error_builder.add_diagnostic(
                        message=_PLANNABLE_DEPRECATION_MESSAGE,
                        label="deprecated plannable",
                        code="217",
                        range=plannable_range,
                        severity=DiagnosticSeverityGQL.Warning,
                    )
        warnings.warn(_PLANNABLE_DEPRECATION_MESSAGE, FutureWarning, stacklevel=3)

    @property
    @deprecated(_PLANNABLE_LSP_MESSAGE, category=None)
    def plannable(self) -> bool:
        self.surface_plannable_deprecation()
        return self.queryable

    @plannable.setter
    @deprecated(_PLANNABLE_LSP_MESSAGE, category=None)
    def plannable(self, value: bool) -> None:
        self.surface_plannable_deprecation()
        self.queryable = value

    def argument_node(self, name: str) -> ast.AST | None:
        """The node for argument `name` in this view's call, or the whole call if it isn't passed.

        `None` if the call site couldn't be parsed, e.g. in a REPL or under `exec`.
        """
        # `namespace` is the only argument that can be passed positionally.
        position = 0 if name == "namespace" else None
        return self.lsp_error_builder.function_arg_node(name, position) or self.lsp_error_builder.caller_info.node

    def feature_reference_node(self, reference: "str | Feature") -> ast.AST | None:
        """The node for one entry of `features`, or the whole argument if entries can't be matched up."""
        return self._feature_reference_nodes.get(reference) or self.argument_node("features")

    def __repr__(self) -> str:
        return (
            f"MaterializedFeatureView("
            f"namespace={self.namespace!r}, "
            f"time_resolution={self.time_resolution!r}, "
            f"update_cadence={self.update_cadence!r}, "
            f"background_compaction={self.background_compaction!r}, "
            f"queryable={self.queryable!r}, "
            f"features={self.features!r}"
            f")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MaterializedFeatureView):
            return NotImplemented
        return (
            self.namespace == other.namespace
            and self.time_resolution == other.time_resolution
            and self.update_cadence == other.update_cadence
            and self.lower_bound == other.lower_bound
            and self.lookback_retention_period == other.lookback_retention_period
            and self.background_compaction == other.background_compaction
            and self.queryable == other.queryable
            and self.features == other.features
        )


MATERIALIZED_FEATURE_VIEW_REGISTRY: dict[str, MaterializedFeatureView] = {}


__all__ = (
    "MATERIALIZED_FEATURE_VIEW_REGISTRY",
    "MaterializedFeatureView",
)
