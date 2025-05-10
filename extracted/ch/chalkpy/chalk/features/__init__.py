from __future__ import annotations

from typing import Any, Optional, Sequence

from chalk.features._chalkop import Aggregation, op
from chalk.features._embedding.embedding import embed
from chalk.features._encoding.converter import FeatureConverter
from chalk.features._encoding.missing_value import MissingValueStrategy
from chalk.features._encoding.primitive import TPrimitive, TPrimitiveArrowScalar
from chalk.features._encoding.serialized_dtype import deserialize_dtype, serialize_dtype
from chalk.features._vector import Vector
from chalk.features.dataframe import DataFrame
from chalk.features.feature_field import CacheStrategy, Feature, FeatureNotFoundException, feature, has_many, has_one
from chalk.features.feature_set import Features, FeatureSetBase, is_features_cls
from chalk.features.feature_set_decorator import features
from chalk.features.feature_time import FeatureTime, feature_time, is_feature_time
from chalk.features.feature_wrapper import FeatureWrapper, ensure_feature, unwrap_feature
from chalk.features.filter import Filter, TimeDelta, after, before
from chalk.features.hooks import after_all, before_all
from chalk.features.primary import Primary, is_primary
from chalk.features.resolver import Cron, Resolver, ResolverProtocol, offline, online, sink
from chalk.features.tag import Environments, Tags
from chalk.features.underscore import Underscore, _, __, underscore
from chalk.queries.scheduled_query import ScheduledQuery  # import to maintain backwards compatibility
from chalk.utils import MachineType


def owner(f: Any) -> Optional[str]:
    """Get the owner for a feature, feature class, or resolver.

    Parameters
    ----------
    f
        A feature (`User.email`), feature class (`User`), or resolver (`get_user`)

    Returns
    -------
    str | None
        The owner for a feature or feature class, if it exists.
        Note that the owner of a feature could be inherited from the feature class.

    Examples
    --------
    >>> @features(owner="ship")
    ... class RocketShip:
    ...     id: int
    ...     software_version: str
    >>> owner(RocketShip.software_version)
    'ship'

    Raises
    ------
    TypeError
        If the supplied variable is not a feature, feature class, or resolver.
    """
    if is_features_cls(f):
        return f.__chalk_owner__
    if isinstance(f, (Feature, FeatureWrapper)):
        return unwrap_feature(f).owner
    if isinstance(f, Resolver):
        return f.owner
    raise TypeError(f"Could not determine the owner of {f} as it is neither a Feature, Feature Set, or Resolver")


def description(f: Any) -> Optional[str]:
    """Get the description of a feature, feature class, or resolver.
    Parameters
    ----------
    f
        A feature (`User.email`), feature class (`User`), or resolver (`get_user`)

    Returns
    -------
    str | None
        The description for a feature, feature class, or resolver, if it exists.

    Examples
    --------
    >>> @features
    ... class RocketShip:
    ...     # Comments above a feature become
    ...     # descriptions for the feature!
    ...     software_version: str
    >>> description(RocketShip.software_version)
    'Comments above a feature become descriptions for the feature!'

    Raises
    ------
    TypeError
        If the supplied variable is not a feature, feature class, or resolver.
    """
    if is_features_cls(f):
        return f.__doc__
    if isinstance(f, (Feature, FeatureWrapper)):
        return unwrap_feature(f).description
    if isinstance(f, Resolver):
        return f.__doc__
    raise TypeError(
        f"Could not determine the description of '{f}' as it is neither a Feature, Feature Set, or Resolver"
    )


def tags(f: Any) -> Optional[Sequence[str]]:
    """Get the tags for a feature, feature class, or resolver.

    Parameters
    ----------
    f
        A feature (`User.email`), feature class (`User`), or resolver (`get_user`)

    Returns
    -------
    list[str] | None
        The tags for a feature, feature class, or resolver, if it exists.
        Note that the tags of a feature could be inherited from the feature class.

    Examples
    --------
    Feature tags
    >>> @features(tags="group:risk")
    ... class User:
    ...     id: str
    ...     # :tags: pii
    ...     email: str
    >>> tags(User.id)
    ['group:risk']

    Feature class tags
    >>> tags(User)
    ['group:risk']

    Feature + feature class tags
    >>> tags(User.email)
    ['pii', 'group:risk']

    Raises
    ------
    TypeError
        If the supplied variable is not a feature, feature class, or resolver.
    """
    if is_features_cls(f):
        return f.__chalk_tags__
    if isinstance(f, (Feature, FeatureWrapper)):
        return unwrap_feature(f).tags
    if isinstance(f, Resolver):
        return f.tags
    raise TypeError(f"Could not determine the tags of '{f}' as it is neither a Feature, Feature Set, or Resolver")


def version(f: Any) -> int | None:
    """Get the version for a feature.

    Parameters
    ----------
    f
        A feature (`User.email`)

    Returns
    -------
    int | None
        The version for a feature, if it exists.

    Examples
    --------
    Feature version
    >>> @features
    ... class Animal:
    ... id: str
    ... sound: str = feature(version=2)
    >>> version(Animal.sound)
    2

    Raises
    ------
    TypeError
        If the supplied variable is not a feature.
    """
    if isinstance(f, (Feature, FeatureWrapper)):
        feature_version_info = unwrap_feature(f).version
        if feature_version_info:
            return feature_version_info.version
        return feature_version_info
    raise TypeError(f"Could not determine the version of '{f}' as it is not a Feature.")


__all__ = [
    "Aggregation",
    "CacheStrategy",
    "Cron",
    "DataFrame",
    "Environments",
    "Feature",
    "FeatureConverter",
    "FeatureNotFoundException",
    "FeatureSetBase",
    "FeatureTime",
    "FeatureWrapper",
    "Features",
    "Filter",
    "MachineType",
    "MissingValueStrategy",
    "Primary",
    "ResolverProtocol",
    "ScheduledQuery",
    "TPrimitive",
    "TPrimitiveArrowScalar",
    "Tags",
    "TimeDelta",
    "Underscore",
    "Vector",
    "after",
    "after_all",
    "before",
    "before_all",
    "description",
    "deserialize_dtype",
    "embed",
    "ensure_feature",
    "feature",
    "feature_time",
    "features",
    "has_many",
    "has_one",
    "is_feature_time",
    "is_features_cls",
    "is_primary",
    "offline",
    "online",
    "op",
    "owner",
    "serialize_dtype",
    "sink",
    "tags",
    "_",
    "__",
    "underscore",
    "unwrap_feature",
]
