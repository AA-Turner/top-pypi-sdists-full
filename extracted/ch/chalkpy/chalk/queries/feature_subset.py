"""How a [`MaterializedFeatureView`][chalk.MaterializedFeatureView] names the features it materializes."""

from __future__ import annotations

import dataclasses
import enum
from typing import TYPE_CHECKING, ClassVar, Collection, Sequence

if TYPE_CHECKING:
    from chalk.client.models import FeatureReference


class _FeatureSubsetMode(enum.Enum):
    """Whether a [`FeatureSubset`][chalk.FeatureSubset] names what to materialize, or what to skip."""

    INCLUDE = "include"
    EXCLUDE = "exclude"


@dataclasses.dataclass(frozen=True)
class FeatureSubset:
    """Which features of a namespace a [`MaterializedFeatureView`][chalk.MaterializedFeatureView]
    materializes: the ones listed, or all but the ones listed.

    Pass one to ``features=``; a plain list is shorthand for
    [`FeatureSubset.include`][chalk.FeatureSubset.include]. Prefer ``exclude`` to drop a few columns:
    features added to the namespace later are then materialized without editing the view.

    Examples
    --------
    >>> from chalk import FeatureSubset, MaterializedFeatureView
    >>> MaterializedFeatureView(
    ...     User,
    ...     time_resolution="1h",
    ...     update_cadence="1d",
    ...     features=FeatureSubset.exclude([User.raw_payload]),
    ... )
    """

    features: Collection["FeatureReference"]
    """The features to include or exclude, depending on ``mode``."""

    mode: _FeatureSubsetMode
    """Whether ``features`` is what to materialize, or what to leave out."""

    all_versions: bool = False
    """Whether a reference covers every version of its feature, rather than only the version it
    resolves to (the ``default_version``, for a bare reference). This applies to an explicit
    version too: ``f @ 2`` covers every version of ``f``.
    """

    INCLUDE: ClassVar[_FeatureSubsetMode] = _FeatureSubsetMode.INCLUDE
    EXCLUDE: ClassVar[_FeatureSubsetMode] = _FeatureSubsetMode.EXCLUDE

    def __post_init__(self) -> None:
        # Only types are checked here. A name may refer to a feature defined later, so it is resolved
        # at export.
        from chalk.features.feature_field import Feature
        from chalk.features.feature_wrapper import FeatureWrapper

        if isinstance(self.features, (str, bytes)) or not isinstance(
            self.features, Collection  # pyright: ignore[reportUnnecessaryIsInstance]
        ):
            raise TypeError(
                f"FeatureSubset 'features' must be a list of features, got {type(self.features).__name__!r}"
            )
        for feature in self.features:
            if not isinstance(feature, (str, Feature, FeatureWrapper)):
                raise TypeError(
                    f"FeatureSubset 'features' must contain features or fully-qualified feature names, "
                    + f"got {feature!r} of type {type(feature).__name__!r}"
                )

    @classmethod
    def include(
        cls,
        features: "Sequence[FeatureReference]",
        *,
        all_versions: bool = False,
    ) -> "FeatureSubset":
        """Materialize exactly these features. Equivalent to passing the list on its own.

        Parameters
        ----------
        features
            The scalar features to materialize.
        all_versions
            Whether a reference to a feature implicitly should apply to all of its versions, rather
            than only the single version it resolves to.
        """
        return cls(features=features, mode=_FeatureSubsetMode.INCLUDE, all_versions=all_versions)

    @classmethod
    def exclude(
        cls,
        features: "Sequence[FeatureReference]",
        *,
        all_versions: bool = False,
    ) -> "FeatureSubset":
        """Materialize every eligible feature in the namespace except these.

        Resolved at each ``chalk apply``, so features added later are materialized without editing
        the view.

        Parameters
        ----------
        features
            The scalar features to leave out of the wide table. They stay queryable, served from
            the observation tables.
        all_versions
            Whether a reference to a feature implicitly should apply to all of its versions, rather
            than only the single version it resolves to.
        """
        return cls(features=features, mode=_FeatureSubsetMode.EXCLUDE, all_versions=all_versions)
