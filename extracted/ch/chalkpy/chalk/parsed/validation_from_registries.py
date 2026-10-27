"""
Unified validation layer that operates directly on registries.

This module provides validation that works for BOTH GQL and Proto conversion paths.
It triggers lazy validations by accessing properties on registry objects and performs
explicit validation checks.

This ensures validation parity between:
- GQL path: get_registered_types() → validate_graph()
- Proto path: ToProtoConverter.convert_graph()

By calling validate_all_from_registries() before conversion in both paths, we ensure
developers cannot add validation to one path and forget the other.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.features import Feature, FeatureNotFoundException
from chalk.parsed.ast_context import get_project_ast_context

if TYPE_CHECKING:
    from chalk.features.feature_set import Features, FeaturesProtocol
    from chalk.features.resolver import ResolverRegistry
    from chalk.queries.scheduled_aggregate_backfill import ScheduledAggregateBackfill
    from chalk_rs import AstProjectIndex


def validate_all_from_registries(
    features_registry: dict[str, type["Features"]],
    resolver_registry: "ResolverRegistry",
) -> None:
    """
    Trigger all validations by accessing properties on registry objects.
    This can be run multiple times and not show duplicates.

    This function should be called by BOTH GQL and Proto conversion paths BEFORE
    they perform their conversions. It validates by triggering lazy validations:

    - Error[24]: Feature names with protected prefixes
    - Error[25]: Namespace names with protected prefixes
    - Error[28]: Feature re-definition
    - Error[32]: Invalid join syntax (composite joins must use & not and)
    - Error[35]: Missing has-one join definition
    - Error[37]: Join filter with incorrect type annotation
    - Error[40]: Invalid join lambda
    - Error[42]: Bad foreign key types (type mismatch)
    - Error[43]: Multi-namespace joins
    - Error[51]: Multiple primary features (versioned primary keys)
    - Error[135]: Unrecognized feature reference

    Parameters
    ----------
    features_registry : dict[str, type[Features]]
        The feature registry to validate (FeatureSetBase.registry).
    resolver_registry : ResolverRegistry
        The resolver registry to validate (RESOLVER_REGISTRY).

    Returns
    -------
    None
        Validation errors are accumulated in LSPErrorBuilder and raised as exceptions.
    """

    # ========================================================================
    # FEATURE VALIDATION
    # ========================================================================

    # --------------------------------------------------------------------
    # Error[164]: part_of / add_features against a never-defined feature class
    # --------------------------------------------------------------------
    # Auxiliary classes are merged into their target when the target class is
    # decorated; an entry still pending here means the target namespace was
    # never defined and the auxiliary's fields silently never made it into the
    # graph. Report it before the rest of validation: it is the root cause of
    # any downstream "unknown feature" errors.
    from chalk.features.feature_set_decorator import validate_no_unmerged_auxiliary_classes

    try:
        validate_no_unmerged_auxiliary_classes(features_registry)
    except Exception as e:
        if not LSPErrorBuilder.promote_exception(e):
            raise

    ast_index = get_project_ast_context()

    for _, features_cls in features_registry.items():
        # --------------------------------------------------------------------
        # Error[51]: Multiple primary features (versioned primary keys)
        # --------------------------------------------------------------------
        # Accessing __chalk_primary__ triggers _discover_feature() which
        # validates that there's only one primary key. Versioned features
        # create multiple primary keys (e.g., id, id@2, id@3, id@4) which
        # triggers Error[51].
        try:
            _ = features_cls.__chalk_primary__
        except Exception as e:
            # LSPErrorBuilder.promote_exception() re-raises LSP errors
            if not LSPErrorBuilder.promote_exception(e):
                # If it's not an LSP error, something else went wrong
                raise

        feature_definition_counts = _get_feature_definition_counts(
            features_cls=features_cls,
            ast_index=ast_index,
        )

        # --------------------------------------------------------------------
        # Iterate through all features in this feature set
        # --------------------------------------------------------------------
        for feature in features_cls.features:
            feature_name = feature.attribute_name or feature.name

            if feature_definition_counts[feature_name] >= 2:
                # This feature has been defined multiple times.
                feature.lsp_error_builder.add_diagnostic(
                    message=f"Feature '{feature_name}' has been defined multiple times on the feature class '{features_cls.__name__}'. This feature definition is overwritten by a later definition.",
                    range=feature.lsp_error_builder.property_range(feature_name),
                    label="redefined feature",
                    code="28",
                )

            # Skip autogenerated and no-display features (same as user_types_to_json.py:138)
            # This prevents validating internal features like __chalk_* that are allowed
            # to have protected names
            if feature.is_autogenerated or feature.no_display:
                continue

            # ----------------------------------------------------------------
            # Error[32,35,37,40,42,43]: Join validation
            # ----------------------------------------------------------------
            # Accessing the .join property triggers:
            # - _validate_join() in feature_field.py (Error[32,37])
            # - _validate_filter() in feature_field.py (Error[40,42,43])
            #
            # During GQL conversion, convert_type_to_gql() also checks:
            # - Error[35]: if t.is_has_one and t.join is None
            try:
                _ = feature.join
            except Exception as e:
                if not LSPErrorBuilder.promote_exception(e):
                    raise

            # ----------------------------------------------------------------
            # Error[24,25]: Feature and namespace name validation
            # ----------------------------------------------------------------
            try:
                _validate_feature_names_from_registry(feature)
            except Exception as e:
                if not LSPErrorBuilder.promote_exception(e):
                    raise

    # ========================================================================
    # RESOLVER VALIDATION
    # ========================================================================

    for resolver in resolver_registry.get_all_resolvers():
        # --------------------------------------------------------------------
        # Error[135]: Unrecognized feature reference
        # --------------------------------------------------------------------
        # Accessing resolver.inputs triggers _do_parse() which validates
        # that all input features are recognized and exist in the registry.
        try:
            _ = resolver.inputs
        except Exception as e:
            if not LSPErrorBuilder.promote_exception(e):
                raise

        try:
            _ = resolver.default_args
        except Exception as e:
            if not LSPErrorBuilder.promote_exception(e):
                raise


def _get_feature_definition_counts(
    features_cls: type["Features"],
    ast_index: "AstProjectIndex | None",
) -> Counter[str]:
    filename = features_cls.__chalk_filename__
    if ast_index is None or filename is None:
        return Counter()

    feature_class_ast = ast_index.feature_class_ast_in_file(
        str(Path(filename).resolve()),
        features_cls.__name__,
    )

    if feature_class_ast is None:
        return Counter()

    return Counter(field.field_name for field in feature_class_ast.annotations)


def _validate_feature_names_from_registry(feature: "Feature") -> None:
    """
    Validate that feature names and namespace names don't use protected prefixes.

    This performs the same validation as _validate_feature_names() in
    _graph_validation.py, but operates on Feature objects from the registry
    rather than UpsertFeatureGQL objects.

    Parameters
    ----------
    feature : Feature
        The feature to validate from FeatureSetBase.registry

    Raises
    ------
    Exception
        If feature or namespace name starts with '_chalk' or '__'
    """
    # Error[24]: Feature names cannot begin with '_chalk' or '__'
    if feature.name.startswith("__") or feature.name.startswith("_chalk"):
        feature.lsp_error_builder.add_diagnostic(
            message="Feature names cannot begin with '_chalk' or '__'.",
            range=feature.lsp_error_builder.property_range(feature.attribute_name or feature.name),
            label="protected name",
            code="24",
        )

    # Error[25]: Namespace names cannot begin with '_chalk' or '__'
    if feature.namespace.startswith("__") or feature.namespace.startswith("_chalk"):
        feature.lsp_error_builder.add_diagnostic(
            message="Feature classes cannot have names that begin with '_chalk' or '__'.",
            label="protected namespace",
            range=feature.lsp_error_builder.decorator_kwarg_value_range("name")
            or feature.lsp_error_builder.class_definition_range(),
            code="25",
        )


def validate_scheduled_agg_backfill_from_registries(
    backfill: "ScheduledAggregateBackfill",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> list[str]:
    """
    Returns explicit validation failures on a scheduled aggregate backfill.
    """
    errors: list[str] = []
    for fqn in backfill.features:
        try:
            feature = Feature.from_root_fqn_in_registry(fqn, features_registry)
        except FeatureNotFoundException:
            errors.append(
                f"ScheduledAggregateBackfill '{backfill.name}' references feature '{fqn}' which does not exist."
            )
            continue

        if not feature.is_windowed and not feature.is_windowed_pseudofeature:
            errors.append(
                f"ScheduledAggregateBackfill '{backfill.name}' references feature '{fqn}' which is not a windowed aggregation."
            )
            continue

        # Windowed features sometimes have materialization config on the underlying windowed pseudofeatures instead (materialization=True)
        # If there is no top level materialization config, then we need to check the underlying pseudofeatures before failing validation.
        features_to_check = [feature]
        if feature.is_windowed and not feature.window_materialization:
            from chalk.streams._windows import get_name_with_duration

            features_to_check = [
                Feature.from_root_fqn_in_registry(
                    get_name_with_duration(feature.root_fqn, duration),
                    features_registry,
                )
                for duration in feature.window_durations
            ]
        feature_missing_materialization = not any(c.window_materialization is not None for c in features_to_check)
        if not features_to_check or feature_missing_materialization:
            errors.append(
                f"ScheduledAggregateBackfill '{backfill.name}' references feature '{fqn}' which does not have a valid window materialization config."
            )
            continue
        feature_has_backfill_schedule = any(
            isinstance(c.window_materialization, dict) and c.window_materialization.get("backfill_schedule") is not None
            for c in features_to_check
        )
        if feature_has_backfill_schedule:
            errors.append(
                f"ScheduledAggregateBackfill '{backfill.name}' includes feature '{fqn}' which already has an inline backfill_schedule. Remove the backfill_schedule from the feature's materialization config or remove the feature from the ScheduledAggregateBackfill."
            )
            continue
    return errors
