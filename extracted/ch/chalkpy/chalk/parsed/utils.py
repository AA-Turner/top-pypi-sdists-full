from __future__ import annotations

from typing import Sequence

from chalk.features import Feature


def validate_namespaced_features(features: Sequence[str] | None):
    if features is None:
        return None

    unique_namespace = set()
    for string_feature in features:
        Feature.from_root_fqn(string_feature)
        unique_namespace.add(string_feature.split(".", maxsplit=1)[0])
    if len(unique_namespace) > 1:
        raise ValueError(f"Output features of named query must belong to the same namespace, but got: '{features}'.")
    return features
