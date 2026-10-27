"""Validation for [`MaterializedFeatureView`][chalk.MaterializedFeatureView].

Arguments are checked when the view is declared, and its features against the graph at export. Every problem is
raised through `add_diagnostic`, so it is an ordinary exception outside the LSP and an underlined diagnostic in it.
"""

from __future__ import annotations

import ast
import re
from datetime import timedelta
from typing import TYPE_CHECKING, Mapping, NoReturn

from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.features import Feature, FeatureNotFoundException
from chalk.queries.feature_subset import FeatureSubset
from chalk.utils.duration import CronTab, Duration, parse_chalk_duration

if TYPE_CHECKING:
    from chalk._lsp.error_builder import FunctionCallErrorBuilder
    from chalk.features.feature_set import Features, FeaturesProtocol
    from chalk.queries.materialized_feature_view import MaterializedFeatureView

_MIN_UPDATE_CADENCE = timedelta(minutes=10)
_CRON_FIELD_RE = re.compile(r"^[0-9*/,\-]+$")


def is_materializable(feature: "Feature") -> bool:
    """Whether a wide table can hold `feature`.

    Must match `is_offline_store_eligible` in `chalk_offline_store`, or reads get routed to wide columns the fill
    never created.
    """
    return (
        # Windowed features count as scalar, but have no observation table of their own.
        feature.is_scalar
        and not feature.is_windowed
        and feature.store_offline
        and not feature.is_distance_pseudofeature
        # Only the generated singleton id is synthesized. Not `is_singleton`, which is set on every feature of a
        # singleton class.
        and feature.name != "__chalk_singleton_id__"
    )


def resolve_feature_reference(
    reference: "str | Feature", features_registry: dict[str, type["FeaturesProtocol"]]
) -> Feature:
    """The feature in `features_registry` that an entry of a view's `features` refers to.

    A class attribute is looked up by name too: its namespace may have been declared again since the view was, and
    the view must be checked against the definition being exported. Raises `FeatureNotFoundException` when the
    registry has no feature by that name.
    """
    root_fqn = reference.root_fqn if isinstance(reference, Feature) else reference
    return Feature.from_root_fqn_in_registry(root_fqn, features_registry)


# --- arguments, checked when the view is declared ---


def namespace_of(namespace: "type[Features] | str", builder: "FunctionCallErrorBuilder", node: ast.AST | None) -> str:
    """The namespace a view's `namespace` argument names."""
    from chalk.features.feature_set import is_features_cls

    if is_features_cls(namespace):
        return namespace.__chalk_namespace__  # type: ignore[union-attr]
    if isinstance(namespace, str):
        return namespace
    builder.add_diagnostic(
        message=f"MaterializedFeatureView 'namespace' must be a @features class or a string, got {type(namespace).__name__!r}",
        label="invalid namespace",
        code="217",
        range=node,
        raise_error=TypeError,
    )


def check_update_cadence(
    update_cadence: "CronTab | Duration", builder: "FunctionCallErrorBuilder", node: ast.AST | None
) -> None:
    """Reject a cadence that is not a duration or cron, or that can fire more often than every 10 minutes."""
    if isinstance(update_cadence, timedelta):
        if update_cadence < _MIN_UPDATE_CADENCE:
            _reject_update_cadence(
                f"MaterializedFeatureView 'update_cadence' must be at least 10 minutes, but got {update_cadence!r}.",
                builder,
                node,
            )
    elif isinstance(update_cadence, str):  # pyright: ignore[reportUnnecessaryIsInstance]
        if update_cadence in ("infinity", "all"):
            return
        if _is_cron_expression(update_cadence):
            try:
                min_interval = _cron_min_interval_minutes(update_cadence)
            except ValueError:
                _reject_malformed_update_cadence(update_cadence, builder, node)
            if min_interval < 10:
                _reject_update_cadence(
                    f"MaterializedFeatureView 'update_cadence' cron '{update_cadence}' can fire as frequently as every {min_interval} minute(s); the minimum allowed interval is 10 minutes.",
                    builder,
                    node,
                )
            return
        try:
            duration = parse_chalk_duration(update_cadence)
        except ValueError:
            _reject_malformed_update_cadence(update_cadence, builder, node)
        if duration < _MIN_UPDATE_CADENCE:
            _reject_update_cadence(
                f"MaterializedFeatureView 'update_cadence' must be at least 10 minutes, but got {update_cadence!r}.",
                builder,
                node,
            )
    else:
        builder.add_diagnostic(
            message=f"MaterializedFeatureView 'update_cadence' must be a string (cron expression or duration) or a timedelta, got {type(update_cadence).__name__!r}.",
            label="invalid update cadence",
            code="219",
            range=node,
            raise_error=TypeError,
        )


def check_features_argument(
    features: FeatureSubset | None, builder: "FunctionCallErrorBuilder", node: ast.AST | None
) -> None:
    """Reject an empty `features`, whether it lists features to include or to exclude."""
    if features is None or len(features.features) > 0:
        return
    builder.add_diagnostic(
        message=(
            "MaterializedFeatureView 'features' excludes nothing, which materializes every "
            + "eligible feature in the namespace. Omit the argument to say that directly."
            if features.mode is FeatureSubset.EXCLUDE
            else "MaterializedFeatureView 'features' is empty, which would materialize nothing. "
            + "Omit the argument to materialize every eligible feature in the namespace."
        ),
        label="empty features",
        code="220",
        range=node,
        raise_error=ValueError,
    )


def check_namespace_is_unique(
    namespace: str,
    registry: Mapping[str, "MaterializedFeatureView"],
    builder: "FunctionCallErrorBuilder",
    node: ast.AST | None,
) -> None:
    """Reject a second view of a namespace that already has one."""
    if namespace not in registry:
        return
    builder.add_diagnostic(
        message=f"A MaterializedFeatureView for namespace '{namespace}' already exists. Only one is allowed per namespace.",
        label="duplicate materialized feature view",
        code="221",
        range=node,
        raise_error=ValueError,
    )


def _reject_update_cadence(message: str, builder: "FunctionCallErrorBuilder", node: ast.AST | None) -> NoReturn:
    builder.add_diagnostic(
        message=message,
        label="update cadence too frequent",
        code="218",
        range=node,
        raise_error=ValueError,
    )


def _reject_malformed_update_cadence(
    update_cadence: str, builder: "FunctionCallErrorBuilder", node: ast.AST | None
) -> NoReturn:
    builder.add_diagnostic(
        message=f"MaterializedFeatureView 'update_cadence' {update_cadence!r} is neither a duration, like '1h' or '1d', nor a cron expression.",
        label="invalid update cadence",
        code="219",
        range=node,
        raise_error=ValueError,
    )


def _is_cron_expression(s: str) -> bool:
    parts = s.split()
    return len(parts) == 5 and all(_CRON_FIELD_RE.match(p) for p in parts)


def _cron_min_interval_minutes(cron_expr: str) -> int:
    """Returns the minimum possible interval in minutes between firings of a cron expression."""
    minute_field = cron_expr.split()[0]
    values: set[int] = set()
    for part in minute_field.split(","):
        if part == "*":
            return 1
        if "/" in part:
            base, step_str = part.split("/", 1)
            step = int(step_str)
            if base == "*":
                start, end = 0, 59
            elif "-" in base:
                start, end = map(int, base.split("-", 1))
            else:
                start, end = int(base), 59
            values.update(range(start, end + 1, step))
        elif "-" in part:
            start, end = map(int, part.split("-", 1))
            values.update(range(start, end + 1))
        else:
            values.add(int(part))

    if len(values) <= 1:
        return 60
    sorted_vals = sorted(values)
    min_gap = min(b - a for a, b in zip(sorted_vals, sorted_vals[1:]))
    wrap_gap = sorted_vals[0] + 60 - sorted_vals[-1]
    return min(min_gap, wrap_gap)


# --- features, checked against the built graph at export ---


class _InvalidView(ValueError):
    """Raised by the export-time checks, so validation doesn't catch unrelated `ValueError`s."""


def validate_materialized_feature_view_from_registries(
    view: "MaterializedFeatureView",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> list[str]:
    """Every validation error in `view`'s features, each also reported as a diagnostic under the LSP."""
    try:
        _check_namespace_exists(view, features_registry)
    except _InvalidView as e:
        # Without the namespace, every feature check below would fail as well.
        return [_report(e)]

    subset = view.features
    if subset is None:
        return []

    errors: list[str] = []
    for reference in subset.features:
        try:
            _check_feature_reference(view, subset, reference, features_registry)
        except _InvalidView as e:
            errors.append(_report(e))

    # Only checked once every feature is valid; otherwise those errors already explain the problem.
    if not errors:
        try:
            _check_materializes_a_feature_column(view, features_registry)
        except _InvalidView as e:
            errors.append(_report(e))
    return errors


def _report(e: _InvalidView) -> str:
    # Publishes the diagnostic `add_diagnostic` saved on `e`, once even across repeated exports.
    LSPErrorBuilder.promote_exception(e)
    return str(e)


def _check_namespace_exists(
    view: "MaterializedFeatureView",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> None:
    if view.namespace in features_registry:
        return
    view.lsp_error_builder.add_diagnostic(
        message=f"MaterializedFeatureView references namespace '{view.namespace}' which does not exist in the feature registry.",
        label="unknown namespace",
        code="222",
        range=view.argument_node("namespace"),
        raise_error=_InvalidView,
    )


def _check_feature_reference(
    view: "MaterializedFeatureView",
    subset: FeatureSubset,
    reference: "str | Feature",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> None:
    """Raise if `reference`, one entry of `subset`, is invalid. Inclusions and exclusions follow the same rules."""
    named = "excludes feature" if subset.mode is FeatureSubset.EXCLUDE else "lists feature"
    node = view.feature_reference_node(reference)

    try:
        feature = resolve_feature_reference(reference, features_registry)
    except FeatureNotFoundException:
        view.lsp_error_builder.add_diagnostic(
            message=f"MaterializedFeatureView for namespace '{view.namespace}' {named} '{reference}' in 'features', "
            + "but that feature does not exist.",
            label="unknown feature",
            code="223",
            range=node,
            raise_error=_InvalidView,
        )

    prefix = (
        f"MaterializedFeatureView for namespace '{view.namespace}' {named} '{feature.root_fqn}' in 'features', but "
    )
    if feature.namespace != view.namespace:
        view.lsp_error_builder.add_diagnostic(
            message=prefix
            + f"that feature belongs to namespace '{feature.namespace}'. A "
            + "materialized feature view can only materialize features from its own namespace.",
            label="feature from another namespace",
            code="224",
            range=node,
            raise_error=_InvalidView,
        )

    _check_materializable(view, feature, prefix=prefix, node=node)


def _check_materializable(
    view: "MaterializedFeatureView", feature: Feature, *, prefix: str, node: ast.AST | None
) -> None:
    """Raise, with the reason, if a wide table can't hold `feature`.

    A condition added to `is_materializable` needs a branch here too, or it is reported as "synthesized".
    """
    if is_materializable(feature):
        return
    if not feature.is_scalar or feature.is_windowed:
        view.lsp_error_builder.add_diagnostic(
            message=prefix + "only scalar features can be materialized.",
            label="not a scalar feature",
            code="225",
            range=node,
            raise_error=_InvalidView,
        )
    if not feature.store_offline:
        # Otherwise reads would expect a wide column for it that the fill never creates.
        view.lsp_error_builder.add_diagnostic(
            message=prefix
            + "that feature sets 'store_offline=False' and so is never written "
            + "to the offline store. Remove it from 'features', or set 'store_offline=True'.",
            label="feature not stored offline",
            code="227",
            range=node,
            raise_error=_InvalidView,
        )
    view.lsp_error_builder.add_diagnostic(
        message=prefix + "that feature is synthesized by Chalk and is not stored offline.",
        label="synthesized feature",
        code="228",
        range=node,
        raise_error=_InvalidView,
    )


def _check_materializes_a_feature_column(
    view: "MaterializedFeatureView",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> None:
    """Reject a selection that leaves nothing but the primary key."""
    # Imported here because that module imports this one.
    from chalk.parsed.materialized_feature_selection import materialized_feature_names, primary_key_names

    features_cls = features_registry[view.namespace]
    if materialized_feature_names(view, features_registry) - primary_key_names(features_cls):
        return
    view.lsp_error_builder.add_diagnostic(
        message=f"MaterializedFeatureView for namespace '{view.namespace}' materializes only the "
        + "primary key, so its wide table would hold no feature values. Name at "
        + "least one other feature in 'features', or remove the view.",
        label="no feature columns",
        code="226",
        range=view.argument_node("features"),
        raise_error=_InvalidView,
    )
