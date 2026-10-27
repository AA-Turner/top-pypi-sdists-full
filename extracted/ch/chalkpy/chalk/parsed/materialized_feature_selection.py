"""Resolves the features an MFV will materialize from the `features=...` parameter
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from chalk.features import Feature
from chalk.parsed.validate_materialized_feature_views import is_materializable, resolve_feature_reference
from chalk.queries.feature_subset import FeatureSubset
from chalk.utils.collections import FrozenOrderedSet

if TYPE_CHECKING:
    from chalk.features.feature_set import FeaturesProtocol
    from chalk.queries.materialized_feature_view import MaterializedFeatureView


def _feature_names_for(feature: "Feature", *, all_versions: bool) -> "FrozenOrderedSet[str]":
    """The fqns a reference to `feature` covers: its own, or with `all_versions` every version's.

    Expanded versions a wide table can't hold are dropped, since the caller never named them. A
    version named directly is kept, so the validator can reject it.
    """
    if not all_versions or feature.version is None:
        return FrozenOrderedSet([feature.root_fqn])
    return FrozenOrderedSet(
        versioned.root_fqn
        for versioned in feature.version.reference.values()
        if isinstance(versioned, Feature) and is_materializable(versioned)
    )


def materialized_feature_names(
    view: "MaterializedFeatureView",
    features_registry: dict[str, type["FeaturesProtocol"]],
) -> "FrozenOrderedSet[str]":
    """Root fqns of the features `view` materializes, with an exclusion resolved to its complement.

    `view` must have passed validation; an unresolvable reference raises. Empty means "everything",
    as in the proto. An exclusion is never empty, since it always keeps the primary key.
    """
    subset = view.features
    if subset is None:
        return FrozenOrderedSet()

    referenced = FrozenOrderedSet(
        name
        for reference in subset.features
        for name in _feature_names_for(
            resolve_feature_reference(reference, features_registry), all_versions=subset.all_versions
        )
    )
    if subset.mode is FeatureSubset.INCLUDE:
        return referenced

    features_cls = features_registry[view.namespace]
    eligible = FrozenOrderedSet(feature.root_fqn for feature in features_cls.features if is_materializable(feature))
    # Retain primary key in exclusion mode: it is the wide row's key.
    return eligible - (referenced - primary_key_names(features_cls))


def primary_key_names(features_cls: type["FeaturesProtocol"]) -> "FrozenOrderedSet[str]":
    return FrozenOrderedSet(feature.root_fqn for feature in features_cls.features if feature.primary)
