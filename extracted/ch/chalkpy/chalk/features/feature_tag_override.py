from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Mapping, Sequence, Union

if TYPE_CHECKING:
    from chalk.features.feature_field import Feature
    from chalk.features.feature_set import Features
    from chalk.features.feature_wrapper import FeatureWrapper

FeatureReference = Union[str, "Feature", "FeatureWrapper"]


class FeatureTagOverrides:
    """Holds centrally-managed feature-tag overrides for one scope.

    Feature tags exist to apply feature permissions for access control. When an
    org opts into centrally-managed tags, the overrides recorded on this instance
    become the single source of truth for tags (see `override_feature_tags` for
    the full security rationale).

    State:
      - `_overrides is None` -> override mode OFF (the default): code-defined
        (inline / class / comment) tags are left untouched and serialized as
        written.
      - `_overrides` is a dict (possibly empty) -> override mode ON: at export
        time ALL code-defined feature tags are discarded and the ONLY tags that
        survive are the ones recorded here, keyed by root fqn.

    The process-wide instance `_feature_tag_overrides` backs the module-level
    `override_feature_tags` / `apply_feature_tag_overrides` API, but this class
    is intentionally instantiable so tests can exercise it on a throwaway instance
    without having to reset the shared one.
    """

    def __init__(self) -> None:
        super().__init__()
        self._overrides: Dict[str, List[str]] | None = None

    @property
    def is_active(self) -> bool:
        """Whether override mode is on (i.e. `override` has been called)."""
        return self._overrides is not None

    def reset(self) -> None:
        """Clear override state, returning to override mode OFF."""
        self._overrides = None

    def override(self, overrides: Mapping[FeatureReference, Sequence[str]]) -> None:
        """Record (and accumulate) the tag overrides. See `override_feature_tags`."""
        from chalk.features.feature_wrapper import ensure_feature

        if not isinstance(overrides, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"override_feature_tags expects a mapping of feature -> list[str], got '{type(overrides).__name__}'."
            )

        resolved: Dict[str, List[str]] = {}
        for ref, tag_list in overrides.items():
            feature = ensure_feature(ref)
            if isinstance(tag_list, str):
                raise TypeError(
                    f"Tags for '{feature.root_fqn}' must be a list of strings, not a bare string '{tag_list}'."
                )
            if not isinstance(tag_list, Sequence):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise TypeError(
                    f"Tags for '{feature.root_fqn}' must be a list of strings, got '{type(tag_list).__name__}'."
                )
            normalized: List[str] = []
            for tag in tag_list:
                if not isinstance(tag, str):  # pyright: ignore[reportUnnecessaryIsInstance]
                    raise TypeError(f"Tag for '{feature.root_fqn}' must be a string, got '{type(tag).__name__}'.")
                normalized.append(tag)
            resolved[feature.root_fqn] = normalized

        # Accumulate across calls. A repeated feature reference is *replaced* by
        # the most recent assignment (tags are not unioned), and the presence of
        # a (possibly empty) dict is what flips the scope into override mode.
        if self._overrides is None:
            self._overrides = {}
        self._overrides.update(resolved)

    def apply(self, features_registry: Mapping[str, "type[Features]"]) -> None:
        """Apply the recorded overrides across `features_registry`. See `apply_feature_tag_overrides`."""
        if self._overrides is None:
            return

        from chalk.features.feature_field import Feature

        for feature_cls in features_registry.values():
            # Class tags are flattened into each feature's `.tags` at decoration
            # time and feed the proto export; `__chalk_tags__` feeds the JSON/GQL
            # export. Clear both so no code-defined tag survives on any path.
            feature_cls.__chalk_tags__ = []
            for feature in feature_cls.features:
                feature.tags = []

        for root_fqn, tag_list in self._overrides.items():
            feature = Feature.from_root_fqn(root_fqn)
            feature.tags = list(tag_list)


# Process-wide instance backing the public API below. This is the single source
# of truth for centrally-managed tags in a deploy; nothing else should mutate it.
_feature_tag_overrides = FeatureTagOverrides()


def override_feature_tags(overrides: Mapping[FeatureReference, Sequence[str]]) -> None:
    """Centrally assign feature tags, overriding every code-defined tag.

    Feature tags exist to enforce access control via feature permissions.
    Calling this function switches the project into *override mode*: at deploy
    time every code-defined tag (inline ``feature(tags=...)``, class-level
    ``@features(tags=...)``, and ``# :tags:`` comment tags) is discarded, and the
    only tags that survive are the ones supplied here.

    The point of wiping every code-defined tag is that the audit surface for
    feature permissions collapses to wherever ``override_feature_tags`` is invoked: once
    this call is the *only* source of tags, that single (CODEOWNERS- or
    lint-guarded) location is the one place a reviewer must read to reason about
    access control. This is a security requirement, not a convenience — if inline
    tags coexisted with these central overrides, a developer could grant a sensitive
    feature an ``allow-downstream`` tag from any file and self-escalate access,
    bypassing that reviewed location.

    The override is applied at deploy time over the fully-populated feature
    registry, so it covers features defined in files imported *after* this call, i.e.
    import order *cannot* be used to smuggle a tag past the wipe.

    ``override_feature_tags`` may be called more than once (for example, split
    across sections of the same reviewed file). Calls accumulate into a single
    mapping; if the same feature is named in more than one call, the most recent
    call wins and *replaces* that feature's tags rather than unioning them.
    Replacing instead of merging is deliberate: each entry then states a
    feature's complete tag set on its own, so a reviewer never has to chase every
    call site to know what a feature ends up with. Calling with an empty mapping
    still enables override mode and so wipes every code-defined tag while granting
    none — a valid way to strip all tags from a project.

    Parameters
    ----------
    overrides
        A mapping from feature reference (``Transaction.amount_bucket``, a
        ``Feature``, or a root-fqn string like ``"transaction.amount_bucket"``)
        to the list of tags to assign to that feature. A feature absent from this
        mapping ends up with no tags.

    Examples
    --------
    >>> from chalk.features import override_feature_tags
    >>> override_feature_tags(
    ...     {
    ...         Transaction.raw_amount: ["access:pii"],
    ...         Transaction.amount_bucket: ["access:aggregation"],
    ...     }
    ... )
    """
    _feature_tag_overrides.override(overrides)


def is_feature_tag_override_active() -> bool:
    """Whether feature-tag override mode is on for this process.

    Returns ``True`` once `override_feature_tags` has been called (even with an
    empty mapping), and ``False`` otherwise. Useful as a deploy-time assertion to
    confirm that centrally-managed tags are in force before shipping a project.
    """
    return _feature_tag_overrides.is_active


def reset_feature_tag_overrides() -> None:
    """Clear the process-wide override state. Intended for tests."""
    _feature_tag_overrides.reset()


def apply_feature_tag_overrides(features_registry: Mapping[str, "type[Features]"]) -> None:
    """Apply the centrally-declared tag overrides across the whole registry.

    No-op unless `override_feature_tags` has been called. When active, this
    wipes every code-defined tag (both per-feature ``Feature.tags`` and the
    class-level ``__chalk_tags__`` that the JSON/GQL export path serializes
    separately) and then stamps on only the declared tags. Called from the
    export pipeline once the registry is fully populated, so it is the
    authoritative last word on feature tags regardless of import order.
    """
    _feature_tag_overrides.apply(features_registry)
