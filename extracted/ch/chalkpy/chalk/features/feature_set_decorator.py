# pyright: reportPrivateUsage = false

from __future__ import annotations

import builtins
import collections
import copy
import inspect
import re
import sys
import types
import typing
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import pyarrow as pa

from chalk._lsp.error_builder import FeatureClassErrorBuilder, LSPErrorBuilder
from chalk.utils import HAS_PEP_649
from chalk.features import is_features_cls
from chalk.features._class_property import classproperty, classproperty_support
from chalk.features._encoding.pyarrow import pyarrow_to_primitive
from chalk.features.dataframe._impl import DataFrameMeta
from chalk.features.feature_field import Feature, VersionInfo
from chalk.features.feature_set import Features, CURRENT_FEATURE_REGISTRY
from chalk.features.feature_time import feature_time
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.namespace_context import build_namespaced_name
from chalk.features.tag import Tags
from chalk.features.underscore import Underscore
from chalk.parsed.ast_context import get_project_ast_context
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.streams import Windowed
from chalk.streams._windows import GroupByWindowed, get_name_with_duration
from chalk.utils import notebook
from chalk.utils.collections import FrozenOrderedSet, ensure_tuple
from chalk.utils.duration import Duration, parse_chalk_duration, parse_chalk_duration_s
from chalk.utils.metaprogramming import MISSING, set_new_attribute
from chalk.utils.string import to_snake_case
from chalk.stores.online_store_config import OnlineStoreConfig

from chalk.features.feature_cache_strategy import (
    CacheStrategy,
    CacheNullsType,
    CacheDefaultsType,
    get_cache_settings_from_strategy,
    get_cache_strategy_from_cache_settings,
)

if TYPE_CHECKING:
    from chalk_rs import FeatureClassAST, FeatureFieldAST

T = TypeVar("T")

GENERATED_OBSERVED_AT_NAME = "__chalk_observed_at__"

__all__ = ["features", "add_features"]

def _get_class_definition_location(class_ast: FeatureClassAST | None) -> tuple[int, int, int, int] | None:
    return None if class_ast is None else class_ast.class_definition_location


def _resolve_part_of_namespace(part_of: str) -> str:
    """Map a `part_of=` string (class name or namespace) to a target namespace."""
    return build_namespaced_name(name=to_snake_case(part_of))


def _resolve_class_source_info(
    c: Type[Any], namespace: str
) -> tuple[str | None, str | None, "FeatureClassAST | None", FeatureClassErrorBuilder]:
    """Look up source filename, source text, AST, and an error builder for a class."""
    try:
        class_file_path = Path(inspect.getfile(c)).resolve()
    except (OSError, TypeError):
        class_file_path = None
    ast_index = get_project_ast_context()
    feature_class_ast = None
    if class_file_path is not None:
        feature_class_ast = ast_index.feature_class_ast_in_file(str(class_file_path), c.__name__)
    if feature_class_ast is None:
        feature_class_ast = ast_index.feature_class_ast(c.__module__, c.__name__)
    class_source = None if feature_class_ast is None else feature_class_ast.source
    class_filename = str(class_file_path) if class_file_path is not None else None
    error_builder = FeatureClassErrorBuilder(
        uri=class_filename or "__main__",
        namespace=namespace,
        range_node=feature_class_ast,
    )
    return class_filename, class_source, feature_class_ast, error_builder


class _AuxiliaryFieldOrigin:
    """Per-field provenance for fields contributed by an auxiliary class."""

    __slots__ = (
        "aux_class",
        "namespace",
        "filename",
        "source",
        "feature_class_ast",
        "error_builder",
        "comment_metadata",
    )

    def __init__(
        self,
        aux_class: Type[Any],
        namespace: str,
        filename: str | None,
        source: str | None,
        feature_class_ast: "FeatureClassAST | None",
        error_builder: FeatureClassErrorBuilder,
        comment_metadata: Mapping[str, FeatureFieldAST],
    ):
        super().__init__()
        self.aux_class = aux_class
        self.namespace = namespace
        self.filename = filename
        self.source = source
        self.feature_class_ast = feature_class_ast
        self.error_builder = error_builder
        self.comment_metadata = comment_metadata


class _PendingAuxiliary:
    """A `@features(part_of=...)` class or `add_features(...)` call whose target
    feature class has not been decorated yet."""

    __slots__ = ("cls", "part_of", "via", "filename", "lineno")

    def __init__(
        self,
        cls: Type[Any],
        part_of: str,
        via: str,
        filename: str | None,
        lineno: int | None,
    ):
        super().__init__()
        self.cls = cls
        self.part_of = part_of
        self.via = via
        self.filename = filename
        self.lineno = lineno

    def declared_at(self) -> str | None:
        if self.filename is None:
            return None
        if self.lineno is None:
            return self.filename
        return f"{self.filename}:{self.lineno}"


def _register_auxiliary_class(
    c: Type[T],
    *,
    part_of: str,
    via: str = "part_of",
    filename: str | None = None,
    lineno: int | None = None,
) -> Type[T]:
    """Fold an auxiliary class into its target feature class.

    Auxiliary classes declared with `@features(part_of=...)` (or built by
    `add_features(...)`) aren't themselves feature classes — their annotations
    and class-attribute defaults get folded into the target class. If the
    target is already registered, the fields are merged into it immediately;
    otherwise the auxiliary is stashed and merged when the target class is
    decorated.
    """
    target_namespace = _resolve_part_of_namespace(part_of)
    registry = CURRENT_FEATURE_REGISTRY.get()
    existing = registry.get_feature_sets().get(target_namespace)
    if existing is not None:
        _extend_existing_feature_class(target=existing, aux=c, via=via)
        return c
    if filename is None:
        try:
            filename = str(Path(inspect.getfile(c)).resolve())
        except (OSError, TypeError):
            filename = None
    _PENDING_AUXILIARY_CLASSES.setdefault(target_namespace, []).append(
        _PendingAuxiliary(cls=c, part_of=part_of, via=via, filename=filename, lineno=lineno)
    )
    return c


def _clear_cached_classproperty(cls: Type[Any], name: str) -> None:
    """Drop the memoized value of a `classproperty(..., cached=True)`.

    `classproperty_support` installs cached classproperties on the metaclass as
    `property(functools.partial(_cached_getter, getter=..., cache=[...]))`; the
    one-element `cache` list is the memo, so clearing it forces a recompute on
    next access."""
    for klass in inspect.getmro(type(cls)):
        prop = klass.__dict__.get(name)
        fget = getattr(prop, "fget", None)
        cache = getattr(fget, "keywords", {}).get("cache")
        if cache is not None:
            cache.clear()
            return


def _extend_existing_feature_class(*, target: Type[Any], aux: Type[Any], via: str) -> None:
    """Merge the fields of auxiliary class `aux` into the already-processed
    feature class `target`.

    Unlike the pending path (auxiliary declared before its target), the target
    here has already gone through `_process_class`, so we can't re-run the class
    pipeline. Instead each auxiliary field is processed individually with
    `_get_field` — the same routine `_process_class` uses — and appended to the
    target's feature list, after which the memoized `features`/`__chalk_primary__`
    classproperties are invalidated so they recompute with the new fields.
    """
    namespace = target.__chalk_namespace__
    aux_namespace = build_namespaced_name(name=to_snake_case(aux.__name__))
    aux_filename, aux_source, aux_class_ast, aux_error_builder = _resolve_class_source_info(aux, aux_namespace)
    aux_annotations = aux.__annotations__ if HAS_PEP_649 else aux.__dict__.get("__annotations__", {})
    comment_metadata: Mapping[str, FeatureFieldAST] = aux_class_ast.fields if aux_class_ast is not None else {}
    origin = _AuxiliaryFieldOrigin(
        aux_class=aux,
        namespace=aux_namespace,
        filename=aux_filename,
        source=aux_source,
        feature_class_ast=aux_class_ast,
        error_builder=aux_error_builder,
        comment_metadata=comment_metadata,
    )

    new_features: List[Tuple[str, Any, Feature]] = []
    new_aliases: Dict[str, str] = {}
    new_additional_inits: List[str] = []
    for attr_name, annotation in aux_annotations.items():
        existing_attr = inspect.getattr_static(target, attr_name, None)
        if attr_name in target.__annotations__ or isinstance(existing_attr, FeatureWrapper):
            aux_error_builder.add_diagnostic(
                message=(
                    f"'{via}' for feature class '{namespace}' redefines feature '{attr_name}', which is"
                    f" already present on '{namespace}'."
                ),
                code="162",
                label="duplicate feature",
                range=aux_error_builder.property_range(attr_name),
                raise_error=ValueError,
            )
            continue
        default = aux.__dict__.get(attr_name, MISSING)
        if isinstance(default, GroupByWindowed):
            aux_error_builder.add_diagnostic(
                message=(
                    f"Feature '{namespace}.{attr_name}' uses group_by_windowed() and cannot be added to"
                    f" '{namespace}' after the feature class is defined. Declare it in the class body of"
                    f" '{namespace}', or declare this '{via}' extension before the target class is defined."
                ),
                code="163",
                label="group-by windowed feature in late extension",
                range=aux_error_builder.property_range(attr_name),
                raise_error=TypeError,
            )
            continue
        if isinstance(annotation, str) and "Windowed" in annotation:
            try:
                annotation = parse_quoted_window_feature(annotation, aux.__module__)
            except Exception as e:
                aux_error_builder.add_diagnostic(
                    message=(
                        f"Quoted Windowed feature type annotation '{annotation}' for '{namespace}.{attr_name}'"
                        f" could not be parsed: {e}."
                    ),
                    label="invalid Windowed annotation",
                    range=aux_error_builder.property_range(attr_name),
                    raise_error=TypeError,
                    code="17",
                )
                continue
        if isinstance(annotation, Windowed) or isinstance(default, Windowed):
            if not isinstance(default, Windowed):
                aux_error_builder.add_diagnostic(
                    message=(
                        f"Windowed feature '{namespace}.{attr_name}' is missing windows. "
                        f"To create a windowed feature, use "
                        f"'{attr_name}: Windowed[...] = windowed(\"10m\", ...)'"
                    ),
                    label="missing windowed(...) call",
                    range=aux_error_builder.property_range(attr_name),
                    raise_error=TypeError,
                    code="17",
                )
                continue
            _extend_windowed_field(
                target=target,
                aux=aux,
                attr_name=attr_name,
                annotation=annotation,
                wind=default,
                aux_error_builder=aux_error_builder,
                comment_metadata=comment_metadata,
                new_features=new_features,
                new_aliases=new_aliases,
                new_additional_inits=new_additional_inits,
            )
            continue

        f = _get_field(
            cls=aux,
            error_builder=aux_error_builder,
            annotation_name=attr_name,
            comment_metadata=comment_metadata,
            class_owner=target.__chalk_owner__,
            class_tags=tuple(target.__chalk_tags__),
            class_etl_offline_to_online=target.__chalk_etl_offline_to_online__,
            class_max_staleness=target.__chalk_max_staleness__,
            namespace=namespace,
            is_singleton=target.__chalk_is_singleton__,
            class_cache_strategy=target.__chalk_cache_strategy__,
        )
        if f.version is not None:
            aux_error_builder.add_diagnostic(
                message=(
                    f"Versioned feature '{namespace}.{attr_name}' cannot be added to '{namespace}' after the"
                    f" feature class is defined. Declare it in the class body of '{namespace}', or declare"
                    f" this '{via}' extension before the target class is defined."
                ),
                code="163",
                label="versioned feature in late extension",
                range=aux_error_builder.property_range(attr_name),
                raise_error=TypeError,
            )
            continue
        if f._primary is True or f._is_feature_time is True:
            kind = "primary key" if f._primary else "feature time"
            aux_error_builder.add_diagnostic(
                message=(
                    f"Feature '{namespace}.{attr_name}' is marked as the {kind} of '{namespace}', but"
                    f" '{namespace}' is already defined. The {kind} must be declared in the class body of"
                    f" '{namespace}'."
                ),
                code="163",
                label=f"{kind} in late extension",
                range=aux_error_builder.property_range(attr_name),
                raise_error=ValueError,
            )
            continue
        new_features.append((attr_name, annotation, f))

    for attr_name, annotation, f in new_features:
        f.features_cls = cast(Type[Features], target)
        f.auxiliary_namespace = origin.namespace
        f.auxiliary_filename = origin.filename
        f.auxiliary_source = origin.source
        f.auxiliary_feature_class_ast = origin.feature_class_ast
        f.auxiliary_error_builder = origin.error_builder
        target.__annotations__[attr_name] = annotation
        target.__chalk_features_raw__.append(f)
        wrapper = FeatureWrapper(f)
        type.__setattr__(target, attr_name, wrapper)
        # Mirror the wrapper onto the auxiliary class so attribute access on it
        # resolves to the same feature as on the target.
        setattr(aux, attr_name, wrapper)

    if new_aliases or new_additional_inits:
        # Windowed fields introduce friendly aliases (`clicks_10m` for the
        # bucket pseudofeature). The alias maps are baked into the closures of
        # __init__ and __setattr__, so extend the stored maps and regenerate
        # both methods.
        alias_from_to = inspect.getattr_static(target, "__chalk_alias_from_to__", None)
        additional_inits = inspect.getattr_static(target, "__chalk_additional_inits__", None)
        if alias_from_to is None:
            alias_from_to = {}
            type.__setattr__(target, "__chalk_alias_from_to__", alias_from_to)
        if additional_inits is None:
            additional_inits = []
            type.__setattr__(target, "__chalk_additional_inits__", additional_inits)
        alias_from_to.update(new_aliases)
        additional_inits.extend(new_additional_inits)
        type.__setattr__(
            target,
            "__setattr__",
            _setattr_fn(
                bidirectional_alias={**{v: k for k, v in alias_from_to.items()}, **alias_from_to},
            ),
        )
        type.__setattr__(
            target,
            "__init__",
            _init_fn(
                additional_inits=FrozenOrderedSet(additional_inits),
                alias_from_to=alias_from_to,
            ),
        )

    # `features` and `__chalk_primary__` memoize over `__chalk_features_raw__`;
    # recompute them so the merged fields are visible. The feature-time caches
    # are left alone: late extensions cannot contribute a feature time (rejected
    # above), so the resolved ts feature cannot change.
    _clear_cached_classproperty(target, "features")
    _clear_cached_classproperty(target, "__chalk_primary__")
    Feature._from_root_fqn.cache_clear()


def _extend_windowed_field(
    *,
    target: Type[Any],
    aux: Type[Any],
    attr_name: str,
    annotation: Any,
    wind: Windowed,
    aux_error_builder: FeatureClassErrorBuilder,
    comment_metadata: Mapping[str, FeatureFieldAST],
    new_features: List[Tuple[str, Any, Feature]],
    new_aliases: Dict[str, str],
    new_additional_inits: List[str],
) -> None:
    """Merge one windowed field into an already-processed feature class.

    Mirrors the non-versioned windowed handling of `_process_class`: validates
    the buckets, registers one pseudofeature per bucket directly on the target,
    and hands the root feature back through `new_features` so the caller's
    commit loop wires it up like any other merged field. Bucket aliases are
    accumulated in `new_aliases`/`new_additional_inits` for __init__/__setattr__
    regeneration.
    """
    namespace = target.__chalk_namespace__
    if isinstance(annotation, Windowed) and annotation is not wind:
        if wind._kind is None and annotation._kind is not None:
            wind.kind = annotation.kind
        elif wind._kind is not None and annotation._kind is not None and wind._kind is not annotation._kind:
            aux_error_builder.add_diagnostic(
                message=(
                    f"Windowed feature '{namespace}.{attr_name}' specifies conflicting types: "
                    f"'Windowed[{getattr(annotation.kind, '__name__', None) or str(annotation.kind)}]' in the annotation and "
                    f"'typ={getattr(wind._kind, '__name__', None) or str(wind._kind)}' in the windowed() call."
                ),
                label="conflicting windowed types",
                code="17",
                range=aux_error_builder.property_range(attr_name),
                raise_error=TypeError,
            )
            return
    if wind._kind is None:
        aux_error_builder.add_diagnostic(
            message=(
                f"Windowed feature '{namespace}.{attr_name}' has no type. Annotate it with"
                f" 'Windowed[...]' or specify 'windowed(..., typ=...)'."
            ),
            label="missing windowed type",
            range=aux_error_builder.property_range(attr_name),
            raise_error=TypeError,
            code="17",
        )
        return
    if wind._name is None:
        wind._name = attr_name
    if wind._version is not None:
        aux_error_builder.add_diagnostic(
            message=(
                f"Versioned windowed feature '{namespace}.{attr_name}' cannot be added to '{namespace}'"
                f" after the feature class is defined. Declare it in the class body of '{namespace}', or"
                f" declare the extension before the target class is defined."
            ),
            code="163",
            label="versioned feature in late extension",
            range=aux_error_builder.property_range(attr_name),
            raise_error=TypeError,
        )
        return
    if isinstance(annotation, Windowed):
        annotation._buckets = wind._buckets

    valid_bucket_seconds = _validate_windowed(
        wind=wind,
        namespace=namespace,
        name=attr_name,
        annotation_kind_name=getattr(wind.kind, "__name__", None) or str(wind.kind),
        error_builder=aux_error_builder,
    )

    # Mirror _process_class: keep only parseable buckets and remember the
    # original bucket strings for friendly alias generation.
    seconds_to_bucket_str: Dict[int, str] = {}
    valid_buckets: List[str] = []
    for b in wind._buckets:
        try:
            s = parse_chalk_duration_s(b)
            valid_buckets.append(b)
            if s not in seconds_to_bucket_str:
                seconds_to_bucket_str[s] = b
        except ValueError:
            pass
    wind._buckets = valid_buckets

    for bucket_seconds in sorted(valid_bucket_seconds):
        try:
            feat = wind._to_feature(bucket=bucket_seconds)
        except ValueError as e:
            aux_error_builder.add_diagnostic(
                message=f"Invalid window found for feature '{namespace}.{attr_name}'. {e.args[0]}",
                label="invalid duration",
                range=aux_error_builder.property_value_range(attr_name) or aux_error_builder.property_range(attr_name),
                code="18",
            )
            continue
        feat.namespace = namespace
        if not feat.is_typ_set():
            feat.typ = ParsedAnnotation(underlying=wind.kind)
        feat.features_cls = cast(Type[Features], target)
        feat.attribute_name = feat.name
        feat.unversioned_attribute_name = feat.name
        feat.is_singleton = target.__chalk_is_singleton__
        _process_field(
            f=feat,
            comment_metadata=comment_metadata,
            class_owner=target.__chalk_owner__,
            class_tags=tuple(target.__chalk_tags__),
            class_etl_offline_to_online=target.__chalk_etl_offline_to_online__,
            class_max_staleness=target.__chalk_max_staleness__,
            class_cache_strategy=target.__chalk_cache_strategy__,
            error_builder=aux_error_builder,
        )
        if feat.window_materialization is not None:
            target.__chalk_materialized_windows__.append(feat)
        elif feat.underscore_expression is not None:
            target.__chalk_expression_windows__.append(feat)
        # Bucket pseudofeatures are committed directly: they are not part of the
        # auxiliary class's annotations, so they get no provenance tagging and no
        # mirror onto the auxiliary class — matching the pending-merge path.
        target.__annotations__[feat.name] = wind.kind
        target.__chalk_features_raw__.append(feat)
        type.__setattr__(target, feat.name, FeatureWrapper(feat))

        bucket_str = seconds_to_bucket_str.get(bucket_seconds)
        if bucket_str is not None:
            alias = f"{attr_name}_{bucket_str}"
            new_additional_inits.append(alias)
            new_aliases[get_name_with_duration(name_or_fqn=attr_name, duration=bucket_seconds)] = alias

    # The root feature flows through the same `_get_field` routine the class
    # pipeline uses (its Windowed branch builds the root with window_durations
    # spanning every bucket); the caller's commit loop wires it to the target.
    root = _get_field(
        cls=aux,
        error_builder=aux_error_builder,
        annotation_name=attr_name,
        comment_metadata=comment_metadata,
        class_owner=target.__chalk_owner__,
        class_tags=tuple(target.__chalk_tags__),
        class_etl_offline_to_online=target.__chalk_etl_offline_to_online__,
        class_max_staleness=target.__chalk_max_staleness__,
        namespace=namespace,
        is_singleton=target.__chalk_is_singleton__,
        class_cache_strategy=target.__chalk_cache_strategy__,
    )
    new_features.append((attr_name, annotation, root))


def _merge_auxiliary_classes_into(
    *, target: Type[Any], auxiliaries: List[Type[Any]]
) -> Dict[str, _AuxiliaryFieldOrigin]:
    """Copy annotations and class attributes from each auxiliary into target.

    Returns a mapping `attr_name -> _AuxiliaryFieldOrigin` for every field
    contributed by an auxiliary, so the caller can tag the resulting Feature
    objects with provenance for LSP diagnostics.

    This runs before `_process_class` so the target's normal pipeline picks up
    the merged annotations as if they had been declared inline.
    """
    if HAS_PEP_649:
        # Triggers __annotate__ and caches the result back into target.__dict__.
        target_annotations = target.__annotations__
    else:
        target_annotations = target.__dict__.get("__annotations__")
        if target_annotations is None:
            target_annotations = {}
            target.__annotations__ = target_annotations

    origins: Dict[str, _AuxiliaryFieldOrigin] = {}
    for aux in auxiliaries:
        aux_namespace = build_namespaced_name(name=to_snake_case(aux.__name__))
        aux_filename, aux_source, aux_class_ast, aux_error_builder = _resolve_class_source_info(
            aux, aux_namespace
        )
        aux_annotations = aux.__annotations__ if HAS_PEP_649 else aux.__dict__.get("__annotations__", {})
        aux_comment_metadata: Mapping[str, FeatureFieldAST] = {}
        if aux_class_ast is not None:
            aux_comment_metadata = _expand_windowed_comment_metadata(aux_class_ast.fields, aux_annotations)
        origin = _AuxiliaryFieldOrigin(
            aux_class=aux,
            namespace=aux_namespace,
            filename=aux_filename,
            source=aux_source,
            feature_class_ast=aux_class_ast,
            error_builder=aux_error_builder,
            comment_metadata=aux_comment_metadata,
        )
        for attr_name, annotation in aux_annotations.items():
            if attr_name in target_annotations:
                raise ValueError(
                    f"Auxiliary class '{aux.__name__}' redefines feature '{attr_name}'"
                    + f" already present on target '{target.__name__}'."
                )
            target_annotations[attr_name] = annotation
            if attr_name in aux.__dict__:
                setattr(target, attr_name, aux.__dict__[attr_name])
            origins[attr_name] = origin
    return origins


def _apply_auxiliary_origins(
    *, target: Type[Any], origins: Dict[str, _AuxiliaryFieldOrigin]
) -> None:
    """Tag each merged Feature with auxiliary provenance and mirror the
    target's FeatureWrapper onto the auxiliary class so attribute access on
    the auxiliary returns the same FeatureWrapper as the target."""
    for f in target.__chalk_features_raw__:
        attr_name = f.attribute_name
        if attr_name is None:
            continue
        origin = origins.get(attr_name)
        if origin is None:
            origin = origins.get(f.unversioned_attribute_name) if f.unversioned_attribute_name else None
        if origin is None:
            continue
        f.auxiliary_namespace = origin.namespace
        f.auxiliary_filename = origin.filename
        f.auxiliary_source = origin.source
        f.auxiliary_feature_class_ast = origin.feature_class_ast
        f.auxiliary_error_builder = origin.error_builder

    seen_aux_classes: set[int] = set()
    for attr_name, origin in origins.items():
        if id(origin.aux_class) in seen_aux_classes:
            wrapper = getattr(target, attr_name, None)
            if wrapper is not None:
                setattr(origin.aux_class, attr_name, wrapper)
            continue
        seen_aux_classes.add(id(origin.aux_class))
        # For each unique auxiliary class, mirror every wrapper for *its* fields.
        aux_fields = (
            origin.aux_class.__annotations__
            if HAS_PEP_649
            else origin.aux_class.__dict__.get("__annotations__", {})
        )
        for aux_attr in aux_fields:
            wrapper = getattr(target, aux_attr, None)
            if wrapper is not None:
                setattr(origin.aux_class, aux_attr, wrapper)


# Auxiliary feature classes (declared with `@features(part_of="User")` or built by
# `add_features(...)`) defined before their target gets stashed here, keyed by the
# target's namespace, and merged when the target class is decorated. Entries still
# here at export time reference a feature class that was never defined; see
# `validate_no_unmerged_auxiliary_classes`.
_PENDING_AUXILIARY_CLASSES: Dict[str, List[_PendingAuxiliary]] = {}


def validate_no_unmerged_auxiliary_classes(features_registry: Optional[Mapping[str, Any]] = None) -> None:
    """Report `@features(part_of=...)` classes and `add_features(...)` calls whose
    target feature class was never defined.

    Without this check the auxiliary fields would silently vanish from the graph:
    they are only merged when the target class is decorated, which never happens
    for a mistyped or missing target.
    """
    import difflib

    if not _PENDING_AUXILIARY_CLASSES:
        return
    if features_registry is None:
        features_registry = CURRENT_FEATURE_REGISTRY.get().get_feature_sets()
    known_namespaces = sorted(features_registry.keys())
    for target_namespace in sorted(_PENDING_AUXILIARY_CLASSES):
        for pending in _PENDING_AUXILIARY_CLASSES[target_namespace]:
            close = difflib.get_close_matches(target_namespace, known_namespaces, n=1)
            hint = f" Did you mean '{close[0]}'?" if close else ""
            declared_at = pending.declared_at()
            where = f" (defined at {declared_at})" if declared_at is not None else ""
            if pending.via == "add_features":
                message = (
                    f"add_features('{pending.part_of}', ...){where} expects a feature class with"
                    f" namespace '{target_namespace}', but no @features class with that namespace"
                    f" was ever defined.{hint}"
                )
            else:
                message = (
                    f"Feature class '{pending.cls.__name__}'{where} was declared with"
                    f" @features(part_of='{pending.part_of}'), but no @features class with namespace"
                    f" '{target_namespace}' was ever defined.{hint}"
                )
            _, _, _, error_builder = _resolve_class_source_info(pending.cls, target_namespace)
            error_builder.add_diagnostic(
                message=message,
                code="164",
                label="unknown feature class",
                range=error_builder.decorator_kwarg_value_range(kwarg="part_of")
                or error_builder.class_definition_range(),
                raise_error=ValueError,
            )


@overload
def features(
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: bool = False,
    max_staleness: Optional[Duration] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    singleton: bool = False,
    online_store_config: Optional[OnlineStoreConfig] = None,
    cache_nulls: CacheNullsType = True,
    cache_defaults: CacheDefaultsType = True,
    part_of: Optional[str] = None,
) -> Callable[[Type[T]], Type[T]]: ...


@overload
def features(cls: Type[T]) -> Type[T]: ...


def features(
    cls: Optional[Type[T]] = None,
    *,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: bool = False,
    max_staleness: Optional[Duration] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    singleton: bool = False,
    online_store_config: Optional[OnlineStoreConfig] = None,
    cache_nulls: CacheNullsType = True,
    cache_defaults: CacheDefaultsType = True,
    part_of: Optional[str] = None,
) -> Union[Callable[[Type[T]], Type[T]], Type[T]]:
    """Chalk lets you spell out your features directly in Python.

    Features are namespaced to a `FeatureSet`.
    To create a new `FeatureSet`, apply the `@features`
    decorator to a Python class with typed attributes.
    A `FeatureSet` is constructed and functions much like
    Python's own `dataclass`.

    Parameters
    ----------
    owner
        The individual or team responsible for these features.
        The Chalk Dashboard will display this field, and alerts
        can be routed to owners.
    tags
        Added metadata for features for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.
        Setting `etl_offline_to_online` on a feature class assigns it to all features on the
        class which do not explicitly specify `etl_offline_to_online`.
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.
        Assigning a `max_staleness` to the feature class assigns it to all features on the
        class which do not explicitly specify a `max_staleness` value of their own.
    cache_nulls
        When `True` (default), Chalk will cache all values, including nulls.
        When `False`, Chalk will not update the null entry in the cache.
        When `"evict_nulls"`, Chalk will evict the entry that would have been
        null from the cache, if it exists.

        Concretely, suppose the current state of a database is `{a: 1, b: 2}`,
        and you write a row `{a: 2, b: None}`. Here is the expected result in the db:
            - `{a: 2, b: None}` when `cache_nulls=True` (default)
            - `{a: 2, b: 2}` when `cache_nulls=False`
            - `{a: 2}` when `cache_nulls="evict_nulls"`
    cache_defaults
        When `True` (default), Chalk will cache all values, including default values.
        When `False`, Chalk will not update the default entry in the cache.
        When `"evict_defaults"`, Chalk will evict the entry that would have been
        a default value from the cache, if it exists.

        Concretely, suppose the current state of a database is `{a: 1, b: 2}`,
        and you write a row `{a: 2, b: "default"}`, and the default value for feature b is `"default"`.
        Here is the expected result in the db:
            - `{a: 2, b: "default"}` when `cache_defaults=True`
            - `{a: 2, b: 2}` when `cache_defaults=False`
            - `{a: 2}` when `cache_defaults="evict_defaults"`

        The `cache_nulls` and `cache_defaults` options can be used together on the same feature with the
        following exceptions: if `cache_nulls=False`, then `cache_defaults` cannot be `"evict_defaults"`, and if
        `cache_nulls="evict_defaults"`, then `cache_defaults` cannot be `False`.

    Other Parameters
    ----------------
    cls
        The decorated class. You shouldn't need to pass this argument.
    name
        The name for the feature set. By default, the name of a feature is
        taken from the name of the attribute on the class, prefixed with
        the camel-cased name of the class.
    description
        The description of the entire feature set. This will be displayed in the 
        Chalk Dashboard and can be helpful for documentation purposes. Takes precedence 
        over the description in the class docstring if both are provided.
    singleton
        If `True`, the feature set is a singleton, and there will be only
        one instance of the class. Because there is only one instance, a
        singleton feature class does not have a primary key. Features
        defined on a singleton feature class are available in all resolvers,
        regardless of whatever other features are used as inputs to the resolver.

    Examples
    --------
    >>> from chalk.features import features
    >>> @features(
    ...     owner="andy@chalk.ai",
    ...     max_staleness="30m",
    ...     etl_offline_to_online=True,
    ...     tags="user-group",
    ... )
    ... class User:
    ...     id: str
    ...     # Comments here appear in the web!
    ...     # :tags: pii
    ...     name: str | None
    ...     # :owner: userteam@mycompany.com
    ...     location: LatLng
    """

    def wrap(c: Type[T]) -> Type[T]:
        if part_of is not None:
            return _register_auxiliary_class(c, part_of=part_of)

        namespace = name if name is not None else to_snake_case(c.__name__)
        namespace = build_namespaced_name(name=namespace)

        pending = _PENDING_AUXILIARY_CLASSES.pop(namespace, None)
        aux_origins: Dict[str, _AuxiliaryFieldOrigin] = {}
        if pending:
            aux_origins = _merge_auxiliary_classes_into(target=c, auxiliaries=[p.cls for p in pending])

        class_filename, class_source, feature_class_ast, error_builder = _resolve_class_source_info(c, namespace)
        nonlocal max_staleness
        if name is not None and re.sub(r"[^a-z_0-9]", "", namespace) != namespace:
            error_builder.add_diagnostic(
                message=(
                    f"Namespace must be composed of lower-case alpha-numeric characters and '_'. Provided namespace "
                    f"'{namespace}' for class '{c.__name__}' contains invalid characters."
                ),
                code="11",
                label="invalid namespace",
                range=error_builder.decorator_kwarg_value_range(kwarg="name") or error_builder.class_definition_range(),
                raise_error=ValueError,
            )

        if name is not None and len(namespace) == 0:
            error_builder.add_diagnostic(
                message=f"Namespace cannot be an empty string, but is for the class '{c.__name__}'.",
                label="empty name",
                code="12",
                range=error_builder.decorator_kwarg_value_range(kwarg="name") or error_builder.class_definition_range(),
                raise_error=ValueError,
            )

        if max_staleness is None:
            max_staleness = timedelta(0)
        else:
            try:
                max_staleness = parse_chalk_duration(max_staleness)
            except ValueError as e:
                error_builder.add_diagnostic(
                    message=f"Invalid 'max_staleness'. {e.args[0]}",
                    label=f"invalid duration {max_staleness}",
                    range=error_builder.decorator_kwarg_value_range(kwarg="max_staleness"),
                    raise_error=ValueError,
                    code="13",
                )

        cache_strategy = get_cache_strategy_from_cache_settings(cache_nulls=cache_nulls, cache_defaults=cache_defaults)

        registry = CURRENT_FEATURE_REGISTRY.get()
        registry_features = registry.get_feature_sets()
        previous_features_class = registry_features.get(namespace, None)
        previous_feature_class_ast = (
            None if previous_features_class is None else previous_features_class.__chalk_feature_class_ast__
        )
        class_definition_location = _get_class_definition_location(feature_class_ast)
        previous_class_definition_location = _get_class_definition_location(previous_feature_class_ast)

        if (
            previous_features_class is not None
            and not notebook.is_notebook()
            and (
                class_filename != previous_features_class.__chalk_filename__
                or class_source != previous_features_class.__chalk_source__
                or (
                    class_definition_location is not None
                    and previous_class_definition_location is not None
                    and class_definition_location != previous_class_definition_location
                )
            )
        ):
            error_builder.add_diagnostic(
                message=(
                    f"Feature class '{previous_features_class.__name__}' is defined twice: "
                    f"once in '{c.__module__}' and once in '{previous_features_class.__module__}'."
                ),
                code="14",
                label="duplicate class",
                range=error_builder.decorator_kwarg_value_range("name") or error_builder.class_definition_range(),
                raise_error=ValueError,
            )

        if (
            notebook.is_notebook()
            and previous_features_class is not None
            and notebook.is_defined_in_module(previous_features_class)
        ):
            # Not generating an LSP here because we're in a notebook anyway
            # TODO: See if we can pretty-print lsp errors in notebooks, at which point we can generate one that points to the old feature class
            raise ValueError(
                f"Cannot re-define feature class '{previous_features_class.__name__}' in a notebook: it was previously defined in '{previous_features_class.__module__}'."
            )

        updated_class = _process_class(
            cls=c,
            class_filename=class_filename,
            class_source=class_source,
            feature_class_ast=feature_class_ast,
            error_builder=error_builder,
            owner=owner,
            tags=ensure_tuple(tags),
            etl_offline_to_online=etl_offline_to_online,
            max_staleness=max_staleness,
            cache_strategy=cache_strategy,
            namespace=namespace,
            singleton=singleton,
            description=description,
            online_store_config=online_store_config,
            aux_origins=aux_origins,
        )
        assert is_features_cls(updated_class)

        if aux_origins:
            _apply_auxiliary_origins(target=updated_class, origins=aux_origins)

        registry.add_feature_set(updated_class)
        return cast(Type[T], updated_class)

    # See if we're being called as @features or @features().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @features without parens.
    return wrap(cls)


def add_features(
    namespace: str,
    *fields: Union[Feature, Windowed],
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    etl_offline_to_online: Optional[bool] = None,
    max_staleness: Optional[Duration] = None,
    class_name: Optional[str] = None,
) -> Type[Any]:
    """Programmatically add features to an existing `@features` class.

    `namespace` references the target feature class, either by class name
    (`"User"`) or by namespace (`"user"`). The target may be defined in any
    file of the project, before or after this call; if it is never defined,
    the deployment fails with an error pointing at this call.

    Each `feature(...)` or `windowed(...)` passed in must specify both
    `name=` (the attribute name on the target class) and `typ=` (the Python
    type), since there is no class body to derive these from.

    Returns a handle class whose attributes resolve to the same features as
    the target class once the target is defined.

    Parameters
    ----------
    namespace
        The class name or namespace of the `@features` class to extend.
    fields
        The `feature(...)` or `windowed(...)` definitions to add to the
        target class.
    owner
        Default owner for the added features; features that set their own
        `owner=` keep it.
    tags
        Tags appended to every added feature.
    etl_offline_to_online
        Default `etl_offline_to_online` for the added features.
    max_staleness
        Default `max_staleness` for the added features.
    class_name
        Name of the returned handle class, for repr/debugging purposes.

    Examples
    --------
    >>> from chalk.features import add_features, feature, features
    >>> from chalk.streams import windowed
    >>> @features
    ... class User:
    ...     id: int
    >>> UserRiskFeatures = add_features(
    ...     "user",
    ...     feature(name="age", typ=int),
    ...     feature(name="risk_score", typ=float),
    ...     windowed("10m", "1h", name="login_count", typ=int),
    ... )
    """
    annotations: Dict[str, Any] = {}
    attrs: Dict[str, Any] = {}
    for f in fields:
        if isinstance(f, Windowed):
            # The Windowed object serves as both the annotation and the
            # class-attribute value; the class pipeline (and the late-extension
            # path) read the kind from the annotation, here supplied via typ=.
            attr_name = f._name
            if not attr_name:
                raise ValueError("Each windowed() passed to add_features() must specify name=.")
            if f._kind is None:
                raise ValueError(
                    f"Windowed feature with name={attr_name!r} must specify typ= when used with"
                    + " add_features(), like windowed('10m', name='login_count', typ=int)."
                )
            if owner is not None and f._owner is None:
                f._owner = owner
            if tags is not None:
                f._tags = (
                    list(ensure_tuple(tags)) if f._tags is None else [*ensure_tuple(f._tags), *ensure_tuple(tags)]
                )
            if max_staleness is not None and f._max_staleness is ...:
                f._max_staleness = max_staleness
            if etl_offline_to_online is not None and f._etl_offline_to_online is None:
                f._etl_offline_to_online = etl_offline_to_online
            annotations[attr_name] = f
            attrs[attr_name] = f
            continue
        if not isinstance(f, Feature):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"add_features() arguments must be feature() or windowed() definitions; got {f!r}. "
                + "For example: add_features('user', feature(name='age', typ=int))."
            )
        attr_name = getattr(f, "name", None)
        if not attr_name:
            raise ValueError("Each feature() passed to add_features() must specify name=.")
        if not f.is_typ_set():
            raise ValueError(
                f"Feature with name={attr_name!r} must specify typ= when used with add_features()."
            )
        if owner is not None and f.owner is None:
            f.owner = owner
        if tags is not None:
            f.tags = list(ensure_tuple(tags)) if f.tags is None else [*f.tags, *ensure_tuple(tags)]
        if max_staleness is not None and not hasattr(f, "max_staleness"):
            f.max_staleness = parse_chalk_duration(max_staleness)
        if etl_offline_to_online is not None and not hasattr(f, "etl_offline_to_online"):
            f.etl_offline_to_online = etl_offline_to_online
        annotations[attr_name] = f.typ.parsed_annotation
        attrs[attr_name] = f

    if class_name is None:
        # Suffix the derived name so the handle class is distinguishable from the
        # target class (`User` vs `UserAddedFeatures`) in reprs and tracebacks.
        camel = "".join(part.capitalize() for part in namespace.split("_"))
        class_name = f"{camel}AddedFeatures" if camel else "_AddFeatures"

    # Capture the caller's module and call site: the module so string annotations
    # resolve in the caller's namespace, the file:line for the never-defined-target
    # diagnostic at export time.
    caller_module = "chalk.features._add_features"
    caller_filename: str | None = None
    caller_lineno: int | None = None
    caller_frame = sys._getframe().f_back
    if caller_frame is not None:
        caller_module = caller_frame.f_globals.get("__name__", caller_module)
        caller_filename = caller_frame.f_code.co_filename
        caller_lineno = caller_frame.f_lineno

    cls = type(
        class_name,
        (object,),
        {
            "__annotations__": annotations,
            "__module__": caller_module,
            **attrs,
        },
    )
    return _register_auxiliary_class(
        cls,
        part_of=namespace,
        via="add_features",
        filename=caller_filename,
        lineno=caller_lineno,
    )


def _discover_feature(
    fs: Sequence[Feature],
    name: str,
    *conditions: Callable[[Feature], bool],
) -> Optional[Feature]:
    """
    Parameters
    ----------
    fs
        The features to search
    name
        Used for error messages
    conditions
        Tested in order. The first feature that matches _any_ condition is returned.
    """
    for cond in conditions:
        filtered_features = [c for c in fs if cond(c)]

        if len(filtered_features) == 1:
            return filtered_features[0]

        if len(filtered_features) > 1:
            assert filtered_features[0].features_cls is not None
            representative = filtered_features[0]
            assert representative.features_cls is not None
            b = representative.lsp_error_builder.add_diagnostic(
                message=(
                    f"Multiple {name} features are not supported in {representative.features_cls.__name__}: "
                    + ", ".join(f"{representative.features_cls.__name__}.{x.name}" for x in filtered_features)
                ),
                code="51",
                label=f"duplicate {name} feature",
                range=representative.lsp_error_builder.property_range(representative.attribute_name),
                raise_error=ValueError,
            )

            for ff in filtered_features[1:]:
                b.with_range(
                    range=ff.lsp_error_builder.property_range(ff.attribute_name),
                    label=f"duplicate {name} feature",
                )

    return None


def _setattr_fn(bidirectional_alias: Mapping[str, str]):
    def setattr(self: object, key: str, value: object):
        if key in bidirectional_alias:
            super(self.__class__, self).__setattr__(bidirectional_alias[key], value)
        return super(self.__class__, self).__setattr__(key, value)

    setattr.__name__ = "__setattr__"
    return setattr


def _getattribute_fn(self: object, attribute_name: str):
    # If calling getattr() on an instance for a feature name,
    # do NOT return a class-level FeatureWrapper.
    # Instead, raise an attribute error
    o = object.__getattribute__(self, attribute_name)
    if isinstance(o, FeatureWrapper):
        raise AttributeError(
            f"Feature '{attribute_name}' is not defined on this instance of class'{type(self).__name__}'"
        )
    return o


_getattribute_fn.__name__ = "__getattribute__"


def _init_fn(
    additional_inits: FrozenOrderedSet[str],
    alias_from_to: Mapping[str, str],
):
    def _init(self: Features, /, *args: object, **kwargs: object):
        for feat, val in zip(self.features, args):
            if feat.attribute_name in kwargs:
                raise ValueError(
                    f"Argument '{feat.attribute_name}' cannot be specified as both a positional and keyword argument"
                )
            kwargs[feat.attribute_name] = val

        for from_, to in alias_from_to.items():
            if from_ in kwargs and to in kwargs:
                raise ValueError(
                    f"The features '{from_}' and '{to}' are aliases of each other. Only one can be specified, but both were given."
                )
            if to in kwargs:
                kwargs[from_] = kwargs[to]
        assert self.__chalk_ts__ is not None
        ts_feature_name = self.__chalk_ts__.attribute_name

        for k, v in kwargs.items():
            actual_key = k
            if "@" in k:
                base_name, version_str = k.rsplit("@", 1)
                try:
                    version = int(version_str)
                    actual_key = f"{base_name}_v{version}"
                    if not hasattr(self.__class__, actual_key):
                        actual_key = base_name
                except ValueError:
                    pass

            cls_field = getattr(self.__class__, actual_key, None)
            if (
                type(cls_field) is not FeatureWrapper
                and actual_key not in additional_inits
                and actual_key != ts_feature_name
            ):
                raise TypeError(f"{self.__class__.__name__}.__init__() got an unexpected keyword argument '{k}'")

            setattr(self, actual_key, v)

    _init.__name__ = "__init__"
    return _init


def _get_field(
    cls: Type,
    error_builder: FeatureClassErrorBuilder,
    annotation_name: str,
    comment_metadata: Mapping[str, FeatureFieldAST],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: bool,
    class_max_staleness: timedelta,
    namespace: str,
    is_singleton: bool,
    class_cache_strategy: CacheStrategy = CacheStrategy.ALL,
) -> Feature:
    # Return a Field object for this field name and type.  ClassVars and
    # InitVars are also returned, but marked as such (see f._field_type).
    # default_kw_only is the value of kw_only to use if there isn't a field()
    # that defines it.

    # If the default value isn't derived from Field, then it's only a
    # normal default value.  Convert it to a Field().
    last_value = LSPErrorBuilder.lsp
    LSPErrorBuilder.lsp = False
    default = getattr(cls, annotation_name, ...)
    LSPErrorBuilder.lsp = last_value

    if isinstance(default, Feature):
        # The feature was set like x: int = feature(...)
        f = default
        if f.unversioned_attribute_name is None and not f.is_autogenerated:
            f.unversioned_attribute_name = annotation_name
        if f.version is not None:
            f.version.base_name = f.name if f.is_name_set() else annotation_name
            f.name = f.version.name_for_version(f.version.default)
        if f.is_name_set():
            if "." in f.name:
                error_builder.add_diagnostic(
                    message=(
                        f"Custom feature names cannot contain a dot, but the feature '{f.name}' on the class '{cls.__name__}' includes a dot. You might consider using a has-one feature instead."
                    ),
                    code="75",
                    label="dotted name",
                    range=error_builder.property_value_kwarg_range(annotation_name, kwarg="name")
                    or error_builder.property_range(annotation_name),
                    raise_error=ValueError,
                )
            elif " " in f.name:
                error_builder.add_diagnostic(
                    message=(
                        f"Custom feature names cannot contain spaces, but the feature '{f.name}' on the class '{cls.__name__}' includes a space."
                    ),
                    code="75",
                    label="name with space",
                    range=error_builder.property_value_kwarg_range(annotation_name, kwarg="name")
                    or error_builder.property_range(annotation_name),
                    raise_error=ValueError,
                )

    elif isinstance(default, Windowed):
        # The feature was set like x: Windowed[int] = windowed()
        # Convert it to a Feature. Invalid buckets are caught by _validate_windowed later.
        try:
            f = default._to_feature(bucket=None)
        except Exception:
            # Invalid windowed definition; _validate_windowed will emit the diagnostic later.
            # Create a placeholder Feature so downstream attribute access doesn't crash.
            f = Feature(name=annotation_name, namespace=namespace)
        if f.version is not None:
            f.version.base_name = f.name if f.is_name_set() else annotation_name
            f.name = f.version.name_for_version(f.version.default)

    else:
        underscore_expression = None
        # The feature was not set explicitly
        if isinstance(default, types.MemberDescriptorType):
            # This is a field in __slots__, so it has no default value.
            default = ...
        if isinstance(default, Underscore):
            underscore_expression = default
            default = ...

        f = Feature(
            name=annotation_name,
            namespace=namespace,
            default=default,
            underscore_expression=underscore_expression,
        )

    # Only at this point do we know the name and the type.  Set them.
    f.namespace = namespace

    if not f.is_typ_set():
        f.typ = ParsedAnnotation(cls, annotation_name)

    f.features_cls = cls
    f.attribute_name = annotation_name
    f.unversioned_attribute_name = annotation_name
    if not hasattr(f, "name"):
        f.name = annotation_name
    f.is_singleton = is_singleton

    _process_field(
        f=f,
        comment_metadata=comment_metadata,
        class_owner=class_owner,
        class_tags=class_tags,
        class_etl_offline_to_online=class_etl_offline_to_online,
        class_max_staleness=class_max_staleness,
        class_cache_strategy=class_cache_strategy,
        error_builder=error_builder,
    )
    return f


def _process_field(
    f: Feature,
    comment_metadata: Mapping[str, FeatureFieldAST],
    class_owner: Optional[str],
    class_tags: Optional[Tuple[str, ...]],
    class_etl_offline_to_online: bool,
    class_max_staleness: timedelta,
    error_builder: FeatureClassErrorBuilder,
    class_cache_strategy: CacheStrategy = CacheStrategy.ALL,
) -> Feature:
    field_comment_metadata = comment_metadata.get(f.attribute_name)
    if (
        field_comment_metadata is None
        and f.unversioned_attribute_name is not None
        and f.unversioned_attribute_name != f.attribute_name
    ):
        # Versioned-feature children have an attribute_name like `x_v1`, but the
        # comment is keyed on the alias's annotation name (`x`). Fall back so
        # per-version children inherit the same comment-derived description/owner/
        # tags as the alias. Without this, the alias and its default-version child
        # desync — visible as a proto roundtrip failure on the FQN.
        field_comment_metadata = comment_metadata.get(f.unversioned_attribute_name)
    comment_based_description = field_comment_metadata and field_comment_metadata.description
    comment_based_owner = field_comment_metadata and field_comment_metadata.owner
    comment_based_tags = (
        tuple(field_comment_metadata.tags) if field_comment_metadata and field_comment_metadata.tags else None
    )

    if f.description is None and comment_based_description:
        f.description = comment_based_description

    if comment_based_tags is not None:
        if f.tags is None:
            f.tags = list(comment_based_tags)
        else:
            f.tags.extend(comment_based_tags)

    if class_tags is not None:
        if f.tags is None:
            f.tags = list(class_tags)
        else:
            f.tags.extend(class_tags)

    if f.owner is not None and comment_based_owner is not None:
        assert f.features_cls is not None
        error_builder.add_diagnostic(
            message=(
                f"Owner for feature '{f.name}' on class '{f.features_cls.__name__}' "
                f"specified both on the feature and in the comment. Please use only one of these two."
            ),
            code="15",
            label="second declaration",
            range=error_builder.property_value_kwarg_range(f.attribute_name, kwarg="owner")
            or error_builder.property_range(f.attribute_name),
            raise_error=ValueError,
        )

    elif f.owner is None:
        f.owner = comment_based_owner or class_owner

    # The attribute is not defined if the feature intends to use the class default
    if not hasattr(f, "max_staleness"):
        f.max_staleness = class_max_staleness

    f_cache_nulls, f_cache_defaults = get_cache_settings_from_strategy(f.cache_strategy)
    class_cache_nulls, class_cache_defaults = get_cache_settings_from_strategy(class_cache_strategy)

    f.cache_strategy = get_cache_strategy_from_cache_settings(
        cache_nulls=f_cache_nulls if f_cache_nulls is not None else class_cache_nulls,
        cache_defaults=f_cache_defaults if f_cache_defaults is not None else class_cache_defaults,
    )

    # Using the private variable because the etl_offline_to_online is a read-only property
    if not hasattr(f, "etl_offline_to_online"):
        f.etl_offline_to_online = class_etl_offline_to_online
    return f


def _repr_fn(self: Features):
    parts: list[str] = []
    for f in self.features:
        val = getattr(self, f.attribute_name, MISSING)
        if val is not MISSING:
            parts.append(f"{f.attribute_name}={val!r}")
    return f"{self.__class__.__name__}(" + ", ".join(parts) + ")"


_repr_fn.__name__ = "__repr__"


def _eq_fn(self: Features, other: object):
    if not isinstance(other, type(self)):
        return NotImplemented
    return all(
        getattr(self, f.attribute_name, MISSING) == getattr(other, f.attribute_name, MISSING) for f in self.features
    )


_eq_fn.__name__ = "__eq__"


def _len_fn(self: Features):
    count = 0
    for f in self.features:
        if not f.no_display and hasattr(self, f.attribute_name):
            count += 1
    return count


_len_fn.__name__ = "__len__"


def _items_fn(self: Features):
    for f in self.features:
        if not f.no_display and hasattr(self, f.attribute_name):
            yield f.fqn, getattr(self, f.attribute_name)


_items_fn.__name__ = "__items__"


def _iter_fn(self: Features):
    for f in self.features:
        if (
            hasattr(self, f.attribute_name)
            and type(f).__name__ == "Feature"
            and not f.is_has_one
            and not f.is_has_many
            and not f.no_display
        ):
            yield f.fqn, getattr(self, f.attribute_name)


_iter_fn.__name__ = "__iter__"


def _expand_windowed_comment_metadata(
    metadata_by_field: Mapping[str, FeatureFieldAST],
    cls_annotations: Dict[str, Any],
) -> Dict[str, FeatureFieldAST]:
    expanded_metadata = dict(metadata_by_field)

    for annotation, feature_type in cls_annotations.items():
        if annotation in metadata_by_field and isinstance(feature_type, Windowed):
            for bucket_size in feature_type.buckets_seconds:
                pseudofeature_name = get_name_with_duration(annotation, bucket_size)
                expanded_metadata[pseudofeature_name] = metadata_by_field[annotation]

    return expanded_metadata


CHALK_SINGLETON_VALUE = 111


def _process_group_by_windowed(
    cls: Type,
    namespace: str,
    attribute_name: str,
    gbw: GroupByWindowed,
    cls_annotations: Dict[str, Any],
    error_builder: FeatureClassErrorBuilder,
) -> Feature:
    if gbw._name is None:
        gbw._name = gbw._name if gbw._name is not None else attribute_name

    gbw._namespace = namespace

    if gbw._dtype is not None:
        gbw._kind = pyarrow_to_primitive(gbw._dtype, name=attribute_name)
        if gbw._kind not in (int, float):
            error_builder.add_diagnostic(
                message=(
                    f"group_by_window feature '{namespace}.{attribute_name}' has an invalid dtype '{gbw._dtype}'. "
                    "Please use a numeric integer or float dtype, like 'int64' or 'float64'."
                ),
                label="invalid dtype",
                range=error_builder.property_value_kwarg_range(attribute_name, kwarg="dtype")
                or error_builder.property_value_range(attribute_name)
                or error_builder.property_range(attribute_name),
                code="16",
            )
    else:
        gbw._dtype = pa.float32()
        gbw._kind = float

    return Feature(
        name=gbw._name,
        attribute_name=attribute_name,
        namespace=namespace,
        features_cls=cls,
        typ=gbw._kind,
        version=None,
        default_version=1,
        description=gbw._description,
        owner=gbw._owner,
        tags=gbw._tags,
        primary=False,
        default=gbw._default,
        underscore_expression=gbw._expression,
        max_staleness=None,
        cache_strategy=CacheStrategy.ALL,
        etl_offline_to_online=None,
        encoder=None,
        decoder=None,
        pyarrow_dtype=gbw._dtype,
        join=None,
        is_feature_time=False,
        is_autogenerated=False,
        validations=None,
        all_validations=None,
        window_durations=tuple(),  # Not here, but on group by windowed
        window_duration=None,
        no_display=False,
        offline_ttl=None,
        last_for=None,
        hook=None,
        is_distance_pseudofeature=False,
        is_pseudofeature=False,
        window_materialization=gbw._materialization,
        group_by_windowed=gbw,
    )


_skip_attrs = {
    "__dict__",
    "__class__",
    "__annotations__",
    "__delattr__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__gt__",
    "__hash__",
    "__init__",
}


def _validate_windowed(
    wind: "Windowed",
    namespace: str,
    name: str,
    annotation_kind_name: str,
    error_builder: "FeatureClassErrorBuilder",
    label_prefix: str = "",
) -> set[int]:
    """Validate a Windowed instance: bucket durations + materialization config.

    Returns the set of valid bucket seconds. Shared between versioned and non-versioned paths.
    label_prefix is e.g. "version 2 " for per-version errors.
    """

    def get_mat_range():
        return (
            error_builder.property_value_kwarg_range(name, kwarg="materialization")
            or error_builder.property_value_range(name)
            or error_builder.property_range(name)
        )

    # Validate bucket durations
    valid_bucket_seconds: set[int] = set()
    if len(wind._buckets) == 0:
        error_builder.add_diagnostic(
            message=(
                f"Windowed feature '{namespace}.{name}' {label_prefix}does not have any window durations. "
                f"To create a windowed feature, use "
                f'\'{name}: Windowed[{annotation_kind_name}] = windowed("1h", "1d"))\''
            ),
            label="missing window durations",
            range=error_builder.property_value_range(name) or error_builder.property_range(name),
            code="777",
        )
    for bucket in wind._buckets:
        try:
            valid_bucket_seconds.add(parse_chalk_duration_s(bucket))
        except ValueError as e:
            error_builder.add_diagnostic(
                message=f"Windowed feature '{namespace}.{name}' {label_prefix}has an invalid duration '{bucket}'. {e.args[0]}",
                label="invalid duration",
                range=error_builder.property_value_range(name) or error_builder.property_range(name),
                code="18",
            )

    # Validate materialization config (dict form only; True is handled by _to_feature)
    if isinstance(wind._materialization, dict):
        if wind._expression is None:
            error_builder.add_diagnostic(
                message=(
                    f"Windowed feature '{namespace}.{name}' {label_prefix}has a materialization, but no expression. "
                    f"To create a materialized windowed feature, use "
                    f"'{name}: Windowed[{annotation_kind_name}] = windowed(\"10m\", materialization={wind._materialization}, expression=_.your_dataframe_feature[_.field_to_agg].sum())'"
                ),
                label="materialization config",
                range=get_mat_range(),
                code="177",
            )

        bucket_duration_raw = wind._materialization.get("bucket_duration", None)
        if bucket_duration_raw is not None:
            try:
                wind._materialization["bucket_duration"] = parse_chalk_duration(bucket_duration_raw)
            except ValueError as e:
                error_builder.add_diagnostic(
                    message=f"Windowed feature '{namespace}.{name}' {label_prefix}has an invalid `bucket_duration`. {e.args[0]}",
                    label="invalid duration",
                    range=get_mat_range(),
                    code="18",
                )

        validated_bucket_durations: dict[Duration, list[Duration]] = collections.defaultdict(list)
        for d, windows_or_window in wind._materialization.get("bucket_durations", {}).items():
            try:
                d = parse_chalk_duration(d)
            except ValueError as e:
                error_builder.add_diagnostic(
                    message=f"Windowed feature '{namespace}.{name}' {label_prefix}has an invalid key in `bucket_durations`. {e.args[0]}",
                    label="invalid duration",
                    range=get_mat_range(),
                    code="18",
                    raise_error=ValueError,
                )
            for w in ensure_tuple(windows_or_window):
                try:
                    w = parse_chalk_duration(w)
                except ValueError as e:
                    error_builder.add_diagnostic(
                        message=f"Windowed feature '{namespace}.{name}' {label_prefix}has an invalid key in `bucket_durations`. {e.args[0]}",
                        label="invalid duration",
                        range=get_mat_range(),
                        code="18",
                        raise_error=ValueError,
                    )
                validated_bucket_durations[d].append(w)

        wind._materialization["bucket_durations"] = validated_bucket_durations
        if bucket_duration_raw is None and not validated_bucket_durations:
            error_builder.add_diagnostic(
                message=(
                    f"Windowed feature '{namespace}.{name}' {label_prefix}has a materialization, but no 'bucket_duration'. "
                    "Please provide a 'bucket_duration', like '1h', in the dictionary under the keyword "
                    "argument 'materialization'."
                ),
                label="missing 'bucket_duration' key",
                range=get_mat_range(),
                code="188",
            )

    return valid_bucket_seconds


def _process_class(
    cls: Type[T],
    class_filename: str | None,
    class_source: str | None,
    feature_class_ast: FeatureClassAST | None,
    error_builder: FeatureClassErrorBuilder,
    owner: Optional[str],
    tags: Tuple[str, ...],
    etl_offline_to_online: bool,
    max_staleness: timedelta,
    namespace: str,
    singleton: bool,
    online_store_config: Optional[OnlineStoreConfig],
    description: Optional[str],
    cache_strategy: CacheStrategy = CacheStrategy.ALL,
    aux_origins: Mapping[str, _AuxiliaryFieldOrigin] | None = None,
) -> Type[T]:
    if HAS_PEP_649:
        raw_cls_annotations = cls.__annotations__
    else:
        raw_cls_annotations = cls.__dict__.get("__annotations__", {})

    alias_from_to: Dict[str, str] = {}
    additional_inits: list[str] = []

    materialized_windows: list[Feature] = []
    group_by_materialized_windows: list[Feature] = []
    expression_windows: List[Feature] = []
    cls_annotations: Dict[str, Any] = {}

    if online_store_config is not None:
        online_store_config.feature_set_namespaces.add(namespace)

    for name, annotation in raw_cls_annotations.items():
        if name in ("features", "namespace", "items", "is_near"):
            error_builder.add_diagnostic(
                message=f"Feature '{name}' on class '{cls.__name__}' uses a reserved name.",
                label=f"reserved name '{name}'",
                range=error_builder.property_range(name),
                raise_error=TypeError,
                code="16",
            )

        if isinstance(annotation, Windowed) or (isinstance(annotation, str) and "Windowed" in annotation):
            # NOTE: For Windowed resolvers, both the Annotation and the value are instances of
            # Windowed, unlike normal features whose annotation is the underlying type, and the
            # value is an instance of FeatureWrapper. So both `annotation` and `wind` should be
            # instances of Windowed.
            #
            # In the future, we should use a subclass of Windowed, rather than an instance, for
            # the type annotation, similar to what we do for Features.
            if isinstance(annotation, str) and "Windowed" in annotation:
                try:
                    annotation = parse_quoted_window_feature(annotation, cls.__module__)
                except Exception as e:
                    error_builder.add_diagnostic(
                        message=(
                            f"Quoted Windowed feature type annotation '{annotation}' for '{namespace}.{name}' could not be parsed: {e}."
                            f"To create a windowed feature with quotes for typing, use "
                            f'\'{name}: "Windowed[int]" = windowed("10m", ...)\''
                        ),
                        label="missing windowed(...) call",
                        range=error_builder.property_range(name),
                        raise_error=TypeError,
                        code="17",
                    )
            assert isinstance(annotation, Windowed), f"failed to parse annotation {annotation} as Windowed"

            wind = getattr(cls, name, None)

            # Check for versioned windowed: feature(versions={1: windowed(...), 2: windowed(...)})
            _is_versioned_windowed = (
                isinstance(wind, Feature)
                and wind.version is not None
                and wind.version.explicitly_enumerated
                and any(isinstance(v, Windowed) for v in wind.version.reference.values())
            )
            if _is_versioned_windowed:
                assert isinstance(wind, Feature) and wind.version is not None
                windowed_versions: dict[int, Windowed] = {
                    k: v for k, v in wind.version.reference.items() if isinstance(v, Windowed)
                }

                # All versions must be windowed — mixing windowed() and feature() is not allowed
                non_windowed_versions = {k: v for k, v in wind.version.reference.items() if not isinstance(v, Windowed)}
                if non_windowed_versions:
                    bad_keys = ", ".join(str(k) for k in sorted(non_windowed_versions.keys()))
                    error_builder.add_diagnostic(
                        message=(
                            f"Windowed feature '{namespace}.{name}' has a mix of windowed() and feature() in its versions dict. "
                            f"Version(s) {bad_keys} use feature() instead of windowed(). "
                            f"All versions must use windowed() when the annotation is Windowed."
                        ),
                        label="mixed windowed/feature versions",
                        range=error_builder.property_value_range(name) or error_builder.property_range(name),
                        code="39",
                    )
                    cls_annotations[name] = annotation.kind
                    continue

                default_ver = wind.version.default
                default_wind = windowed_versions[default_ver]
                max_ver = wind.version.maximum

                # Set kind and _name on all version Windowed instances. The kind
                # setter forbids assigning twice, so skip instances that already
                # carry a kind from `windowed(typ=...)`.
                for v_wind in windowed_versions.values():
                    if v_wind._kind is None:
                        v_wind.kind = annotation.kind
                    if v_wind._name is None:
                        v_wind._name = name

                # Validate and collect bucket seconds across all versions
                all_bucket_seconds: set[int] = set()
                seconds_to_bucket_str: dict[int, str] = {}
                for ver, v_wind in windowed_versions.items():
                    ver_buckets = _validate_windowed(
                        wind=v_wind,
                        namespace=namespace,
                        name=name,
                        annotation_kind_name=getattr(annotation.kind, "__name__", None) or str(annotation.kind),
                        error_builder=error_builder,
                        label_prefix=f"version {ver} ",
                    )
                    all_bucket_seconds.update(ver_buckets)
                    for b in v_wind._buckets:
                        try:
                            s = parse_chalk_duration_s(b)
                            if s not in seconds_to_bucket_str:
                                seconds_to_bucket_str[s] = b
                        except ValueError:
                            pass
                annotation._buckets = default_wind._buckets

                # Create pseudo-features for each bucket across all versions
                for bucket_s in sorted(all_bucket_seconds):
                    versions_with_bucket = {
                        ver: w for ver, w in windowed_versions.items() if bucket_s in w.buckets_seconds
                    }
                    default_has_bucket = default_ver in versions_with_bucket
                    source_ver = default_ver if default_has_bucket else min(versions_with_bucket.keys())
                    source_wind = versions_with_bucket[source_ver]

                    # Create the base pseudo-feature from the source version
                    try:
                        base_feat = source_wind._to_feature(bucket=bucket_s)
                    except ValueError as e:
                        error_builder.add_diagnostic(
                            message=f"Invalid window found for feature '{namespace}.{name}'. {e.args[0]}",
                            label="invalid duration",
                            range=error_builder.property_value_range(name),
                            code="18",
                        )
                        continue

                    # Build version reference with Feature instances for each version that has this bucket.
                    # Delete `name` so that version expansion assigns it via name_for_version,
                    # which adds the @N suffix for non-v1 versions.
                    version_reference: dict[int, Feature | Windowed] = {}
                    for ver, v_wind in versions_with_bucket.items():
                        try:
                            ver_feat = v_wind._to_feature(bucket=bucket_s)
                        except ValueError:
                            continue
                        if hasattr(ver_feat, "name"):
                            del ver_feat.name
                        version_reference[ver] = ver_feat

                    base_feat.version = VersionInfo(
                        version=source_ver,
                        maximum=max_ver,
                        default=default_ver if default_has_bucket else source_ver,
                        reference=version_reference,
                        explicitly_enumerated=True,
                        base_name=base_feat.name,
                    )

                    if base_feat.window_materialization is not None:
                        materialized_windows.append(base_feat)
                    elif base_feat.underscore_expression is not None:
                        expression_windows.append(base_feat)

                    cls_annotations[base_feat.name] = annotation.kind
                    setattr(cls, base_feat.name, base_feat)

                    bucket_str = seconds_to_bucket_str.get(bucket_s)
                    if bucket_str is not None:
                        alias = f"{name}_{bucket_str}"
                        additional_inits.append(alias)
                        alias_from_to[get_name_with_duration(name_or_fqn=name, duration=bucket_s)] = alias

                # Build a per-version root_feat for every enumerated version, mirroring
                # the per-bucket version_reference construction above. Without this, the
                # version-expansion pass below (~line 1505) only sees `reference={}` on
                # the root and never emits a `name@N` stem feature for non-default
                # versions. That breaks `chalk aggregate backfill --feature foo@2`,
                # which walks `mat_agg_service.get_window_materializations_for_feature_names`
                # → stem fqn → `windowed_pseudo_features` iteration; the per-bucket
                # pseudofeatures are emitted per-version (above), but with no stem they're
                # unreachable through the standard backfill lookup path.
                root_version_reference: dict[int, Feature | Windowed] = {}
                for ver, v_wind in windowed_versions.items():
                    ver_root = v_wind._to_feature(bucket=None)
                    ver_root.window_durations = tuple(sorted(v_wind.buckets_seconds))
                    # Match the per-bucket pattern: clear `name` so version expansion
                    # below assigns it via name_for_version (`base_name` for v1,
                    # `base_name@N` for non-default versions). _to_feature always
                    # sets name, so no guard needed.
                    del ver_root.name
                    root_version_reference[ver] = ver_root

                # Set up the root feature with window_durations across all buckets.
                root_feat = default_wind._to_feature(bucket=None)
                root_feat.window_durations = tuple(sorted(all_bucket_seconds))
                root_feat.version = VersionInfo(
                    version=default_ver,
                    maximum=max_ver,
                    default=default_ver,
                    reference=root_version_reference,
                    explicitly_enumerated=True,
                    base_name=name,
                )
                f = root_feat
                cls_annotations[name] = annotation
                # Skip the normal windowed processing below
                setattr(cls, name, f)
                continue

            elif wind is None or not isinstance(wind, Windowed):
                assert annotation._kind is not None
                error_builder.add_diagnostic(
                    message=(
                        f"Windowed feature '{namespace}.{name}' is missing windows. "
                        f"To create a windowed feature, use "
                        f"'{name}: Windowed[{getattr(annotation.kind, '__name__', None) or str(annotation.kind)}] = windowed(\"10m\", ...)' "
                        f"or '{name}: Windowed[{getattr(annotation.kind, '__name__', None) or str(annotation.kind)}] = feature(versions={{1: windowed(\"10m\", ...), ...}})'"
                    ),
                    label="missing windowed(...) call",
                    range=error_builder.property_range(name),
                    raise_error=TypeError,
                    code="17",
                )

            # `wind._kind` is already set when the windowed() call specified `typ=`
            # (and when the annotation and the value are the same object, as with
            # add_features); the kind setter forbids assigning twice.
            if wind._kind is None:
                wind.kind = annotation.kind
            elif annotation._kind is not None and wind._kind is not annotation._kind:
                error_builder.add_diagnostic(
                    message=(
                        f"Windowed feature '{namespace}.{name}' specifies conflicting types: "
                        f"'Windowed[{getattr(annotation.kind, '__name__', None) or str(annotation.kind)}]' in the annotation and "
                        f"'typ={getattr(wind._kind, '__name__', None) or str(wind._kind)}' in the windowed() call."
                    ),
                    label="conflicting windowed types",
                    range=error_builder.property_range(name),
                    raise_error=TypeError,
                    code="17",
                )
            if wind._name is None:
                wind._name = name
            annotation._buckets = wind._buckets

            valid_bucket_seconds = _validate_windowed(
                wind=wind,
                namespace=namespace,
                name=name,
                annotation_kind_name=getattr(annotation.kind, "__name__", None) or str(annotation.kind),
                error_builder=error_builder,
            )

            # Build reverse mapping: seconds → original bucket string for alias generation,
            # and filter wind._buckets to only valid ones so _to_feature doesn't choke
            # on invalid durations when accessing self.buckets_seconds internally.
            seconds_to_bucket_str: dict[int, str] = {}
            valid_buckets: list[str] = []
            for b in wind._buckets:
                try:
                    s = parse_chalk_duration_s(b)
                    valid_buckets.append(b)
                    if s not in seconds_to_bucket_str:
                        seconds_to_bucket_str[s] = b
                except ValueError:
                    pass
            wind._buckets = valid_buckets

            for bucket_seconds in sorted(valid_bucket_seconds):
                # Make pseudo-features for each valid bucket of the window
                try:
                    feat = wind._to_feature(bucket=bucket_seconds)
                except ValueError as e:
                    error_builder.add_diagnostic(
                        message=f"Invalid window found for feature '{namespace}.{name}'. {e.args[0]}",
                        label="invalid duration",
                        range=error_builder.property_value_range(name),
                        code="18",
                    )
                    continue

                if feat.window_materialization is not None:
                    materialized_windows.append(feat)
                elif feat.underscore_expression is not None:
                    expression_windows.append(feat)

                # For the pseudo-features, which track an individual bucket,
                # the correct annotation is the underlying annotation, not
                # Windowed[underlying], since it's only one value
                cls_annotations[feat.name] = wind.kind
                setattr(cls, feat.name, feat)
                bucket_str = seconds_to_bucket_str.get(bucket_seconds)
                if bucket_str is not None:
                    alias = f"{name}_{bucket_str}"
                    additional_inits.append(alias)
                    alias_from_to[
                        get_name_with_duration(
                            name_or_fqn=name,
                            duration=bucket_seconds,
                        )
                    ] = alias

        windowed_group_by = getattr(cls, name, None)
        if isinstance(annotation, DataFrameMeta) and isinstance(windowed_group_by, GroupByWindowed):
            feat = _process_group_by_windowed(
                cls=cls,
                namespace=namespace,
                attribute_name=name,
                gbw=windowed_group_by,
                cls_annotations=cls_annotations,
                error_builder=error_builder,
            )
            group_by_materialized_windows.append(feat)
            setattr(cls, name, feat)
            kind = windowed_group_by._kind
            cls_annotations[name] = kind
        else:
            cls_annotations[name] = annotation

    _globals = sys.modules[cls.__module__].__dict__ if cls.__module__ in sys.modules else {}

    for name, member in inspect.getmembers(cls):
        if name in _skip_attrs:
            continue
        if name not in cls_annotations and isinstance(member, Windowed):
            error_builder.add_diagnostic(
                range=error_builder.property_range(name),
                message=f"Windowed feature '{namespace}.{name}' is missing an annotation, like 'Windowed[str]'",
                label="missing annotation",
                raise_error=TypeError,
                code="20",
            )

        # Feature times that weren't annotated.
        if name not in cls_annotations and isinstance(member, Feature):
            # All feature types need annotations, except for datetimes, which we can automatically infer
            if member._is_feature_time:
                # We must read the private variable to avoid parsing the annotation,
                # which might contain forward references that are not yet loaded
                cls_annotations[name] = datetime
            else:
                error_builder.add_diagnostic(
                    code="18",
                    range=error_builder.property_range(name),
                    message=f"Feature '{namespace}.{name}' is missing an annotation. Please add one, like '{name}: str = ...'",
                    label="missing annotation",
                    raise_error=TypeError,
                )
        if name not in cls_annotations and isinstance(member, str) and not name.startswith("__"):
            error_builder.add_diagnostic(
                code="18",
                range=error_builder.property_range(name),
                message=(
                    f"Feature '{namespace}.{name}' is missing an annotation. Did you use an equals sign instead of a colon? "
                    f"If so, please change your feature definition to '{name}: {member}'"
                ),
                label="missing annotation",
                raise_error=TypeError,
            )

        if name not in cls_annotations and isinstance(member, Underscore):
            error_builder.add_diagnostic(
                code="18",
                range=error_builder.property_range(name),
                message=f"Underscore feature '{namespace}.{name}' is missing an annotation. Please add one, like '{name}: int = ...'",
                label="missing annotation",
                raise_error=TypeError,
            )

        # catch malformed features like num_transactions: int = windowed("2h") with no Windowed type
        if isinstance(member, Windowed) and not isinstance(cls_annotations.get(name), Windowed):
            error_builder.add_diagnostic(
                message=(
                    f"Feature '{namespace}.{name}' is marked as 'windowed()', "
                    f"but also needs to be marked as a Windowed type. "
                    f"Please add one, like '{name}: Windowed[int] = ...'"
                ),
                range=error_builder.annotation_range(name) or error_builder.property_range(name),
                label="missing Windowed[...]",
                raise_error=TypeError,
                code="19",
            )

    cls.__annotations__ = cls_annotations
    del cls_annotations  # unused; set cls.__annotations__ directly

    set_new_attribute(cls=cls, name="__chalk_is_singleton__", value=singleton)
    set_new_attribute(
        cls=cls, name="__chalk_online_store_config__", value=(online_store_config and online_store_config.id)
    )
    set_new_attribute(cls=cls, name="__chalk_error_builder__", value=error_builder)
    set_new_attribute(cls=cls, name="__chalk_filename__", value=class_filename)
    set_new_attribute(cls=cls, name="__chalk_source__", value=class_source)
    set_new_attribute(cls=cls, name="__chalk_feature_class_ast__", value=feature_class_ast)
    set_new_attribute(cls=cls, name="__chalk_materialized_windows__", value=materialized_windows)
    set_new_attribute(cls=cls, name="__chalk_group_by_materialized_windows__", value=group_by_materialized_windows)
    set_new_attribute(cls=cls, name="__chalk_expression_windows__", value=expression_windows)

    cls_fields: List[Feature] = []

    if singleton:
        if online_store_config is not None:
            error_builder.add_diagnostic(
                message="Singleton feature sets cannot be stored in an online store.",
                label="invalid online store",
                range=error_builder.decorator_kwarg_value_range("online_store_config"),
                raise_error=ValueError,
                code="74",
            )
        f = Feature(
            primary=True,
            attribute_name="__chalk_singleton_id__",
            name="__chalk_singleton_id__",
            default=CHALK_SINGLETON_VALUE,
            namespace=namespace,
            typ=int,
            pyarrow_dtype=pa.uint8(),
            max_staleness=None,
            cache_strategy=CacheStrategy.ALL,
            etl_offline_to_online=False,
            is_autogenerated=True,
            no_display=True,
        )
        f.is_singleton = True
        set_new_attribute(cls=cls, name="__chalk_singleton_id__", value=f)
        cls.__annotations__[f.attribute_name] = int

    def __chalk_primary__(_: Type[Features]):
        return _discover_feature(
            cls_fields,
            "primary",
            lambda q: q._primary is True,
            lambda q: q.typ.is_primary(),
            lambda q: (
                q.name == "id" and not q.has_resolved_join and not q._is_feature_time and not q.typ.is_feature_time()
            ),
        )

    set_new_attribute(cls, "__chalk_primary__", value=classproperty(__chalk_primary__, cached=True))

    def __chalk_ts__(cl: Type[Features]) -> Feature:
        # Not using `f.is_feature_time` as that would create an infinite recursion, since
        # `.is_feature_time` accesses `__chalk_ts__`
        ts_feature: Optional[Feature] = _discover_feature(
            cls_fields,
            "feature time",
            lambda q: q._is_feature_time is True,
            lambda q: q.typ.is_feature_time(),
            lambda q: q.name == "ts" and not q.has_resolved_join and not q._primary and not q.typ.is_primary(),
        )
        if ts_feature is None:
            return unwrap_feature(getattr(cl, GENERATED_OBSERVED_AT_NAME))
        return ts_feature

    set_new_attribute(
        cls=cls,
        name="__chalk_ts__",
        value=classproperty(__chalk_ts__, cached=True),
    )

    def __chalk_observed_at__(cls: Type[Features]) -> FeatureWrapper:
        ts_feature: Optional[Feature] = _discover_feature(
            cls_fields,
            "feature time",
            # Not using `f.is_feature_time` as that would create an infinite recursion, since
            # `.is_feature_time` accesses `__chalk_ts__` which can access this function
            lambda f: f._is_feature_time is True,
            lambda f: f.typ.is_feature_time(),
            lambda f: f.name == "ts" and not f.has_resolved_join and not f._primary and not f.typ.is_primary(),
        )
        if ts_feature is not None:
            if ts_feature.attribute_name != GENERATED_OBSERVED_AT_NAME:
                error_builder.add_diagnostic(
                    message=f"Object {cls.__name__} has no attribute '{GENERATED_OBSERVED_AT_NAME}",
                    label="missing attribute",
                    range=error_builder.property_range(ts_feature.attribute_name),
                    raise_error=AttributeError,
                    code="26",
                )

        # If the timestamp feature is still none, then synthesize one on first use
        ts_feature = feature_time()
        assert ts_feature is not None
        ts_feature.name = GENERATED_OBSERVED_AT_NAME
        ts_feature.attribute_name = GENERATED_OBSERVED_AT_NAME
        ts_feature.unversioned_attribute_name = None
        ts_feature.namespace = cls.__chalk_namespace__
        ts_feature.features_cls = cls
        ts_feature.is_autogenerated = True
        cls.__annotations__[GENERATED_OBSERVED_AT_NAME] = datetime

        _process_field(
            f=ts_feature,
            error_builder=error_builder,
            comment_metadata={},
            class_owner=cls.__chalk_owner__,
            class_tags=tuple(cls.__chalk_tags__),
            class_etl_offline_to_online=cls.__chalk_etl_offline_to_online__,
            class_max_staleness=cls.__chalk_max_staleness__,
            class_cache_strategy=cls.__chalk_cache_strategy__,
        )

        return FeatureWrapper(ts_feature)

    set_new_attribute(
        cls=cls,
        name=GENERATED_OBSERVED_AT_NAME,
        value=classproperty(__chalk_observed_at__, cached=True, bind_to_instances=False),
    )

    def __features__(cl: Type[Features]) -> List[Feature]:
        fs = list(cls_fields)
        if cl.__chalk_ts__ not in fs:
            assert cl.__chalk_ts__ is not None
            fs.append(cl.__chalk_ts__)
        return fs

    set_new_attribute(cls=cls, name="features", value=classproperty(__features__, cached=True))
    set_new_attribute(cls=cls, name="__str__", value=classmethod(lambda _: namespace))
    set_new_attribute(cls=cls, name="__chalk_features_raw__", value=cls_fields)
    set_new_attribute(cls=cls, name="__chalk_is_loaded_from_notebook__", value=False)
    set_new_attribute(cls=cls, name="__chalk_notebook_feature_expressions__", value=dict())
    set_new_attribute(cls=cls, name="__repr__", value=_repr_fn)
    set_new_attribute(cls=cls, name="__eq__", value=_eq_fn)
    set_new_attribute(cls=cls, name="__hash__", value=None)
    set_new_attribute(cls=cls, name="__iter__", value=_iter_fn)
    set_new_attribute(cls=cls, name="__chalk_description__", value=description)
    set_new_attribute(cls=cls, name="items", value=_items_fn)
    set_new_attribute(cls=cls, name="namespace", value=namespace)
    set_new_attribute(cls=cls, name="__chalk_namespace__", value=namespace)
    set_new_attribute(cls=cls, name="__chalk_owner__", value=owner)
    set_new_attribute(cls=cls, name="__chalk_tags__", value=list(tags))
    set_new_attribute(cls=cls, name="__chalk_max_staleness__", value=max_staleness)
    set_new_attribute(cls=cls, name="__chalk_cache_strategy__", value=cache_strategy)
    set_new_attribute(cls=cls, name="__is_features__", value=True)
    set_new_attribute(cls=cls, name="__len__", value=_len_fn)
    set_new_attribute(cls=cls, name="__getattribute__", value=_getattribute_fn)
    set_new_attribute(cls=cls, name="__setattr__", value=classmethod(_class_setattr))
    set_new_attribute(
        cls=cls,
        name="__chalk_etl_offline_to_online__",
        value=etl_offline_to_online,
    )

    comment_metadata: Mapping[str, FeatureFieldAST] = {}
    if feature_class_ast is not None:
        comment_metadata = _expand_windowed_comment_metadata(feature_class_ast.fields, cls.__annotations__)
    aux_origins = aux_origins or {}
    if aux_origins:
        comment_metadata = dict(comment_metadata)
        for attr_name, origin in aux_origins.items():
            aux_field_comment_metadata = origin.comment_metadata.get(attr_name)
            if aux_field_comment_metadata is not None:
                comment_metadata[attr_name] = aux_field_comment_metadata

    # Moving this line lower causes all kinds of problems.
    cls = classproperty_support(cls)

    # Parse the fields after we have the correct `cls` set
    cls_fields.extend(
        _get_field(
            cls=cls,
            error_builder=error_builder,
            annotation_name=name,
            comment_metadata=comment_metadata,
            class_owner=owner,
            class_tags=tags,
            class_etl_offline_to_online=etl_offline_to_online,
            class_max_staleness=max_staleness,
            class_cache_strategy=cache_strategy,
            namespace=namespace,
            is_singleton=singleton,
        )
        for name in cls.__annotations__
    )
    for f in tuple(cls_fields):
        if singleton and f.primary and f.name != "__chalk_singleton_id__":
            error_builder.add_diagnostic(
                message=(
                    f"The singleton feature class '{namespace}' includes a feature '{f.name}' that is primary. "
                    f"Please remove the feature '{f.fqn}' "
                    f"or remove the singleton keyword argument to the feature class '{namespace}'."
                ),
                range=error_builder.property_range(f.attribute_name),
                label="primary feature",
                raise_error=ValueError,
                code="27",
            )

        if f.version is None:
            continue

        alias_from_to[f.attribute_name] = f"{f.attribute_name}_v{f.version.default}"

        if f.version.explicitly_enumerated:
            # Check for windowed values that weren't handled in the windowed annotation path
            # (e.g. annotation is int but versions contain windowed() — wrong annotation type)
            has_windowed_ref = any(isinstance(v, Windowed) for v in f.version.reference.values())
            if has_windowed_ref:
                # Only emit this error if the annotation isn't Windowed — if it is Windowed,
                # the Windowed annotation block already handled this (possibly with a different error)
                orig_annotation = raw_cls_annotations.get(f.attribute_name)
                is_windowed_annotation = isinstance(orig_annotation, Windowed) or (
                    isinstance(orig_annotation, str) and "Windowed" in orig_annotation
                )
                if not is_windowed_annotation:
                    error_builder.add_diagnostic(
                        message=(
                            f"Feature '{namespace}.{f.attribute_name}' uses windowed() in its versions dict, "
                            f"but the type annotation is not Windowed. "
                            f"Use 'Windowed[<type>]' as the annotation, e.g. "
                            f"'{f.attribute_name}: Windowed[float] = feature(versions={{...}})'"
                        ),
                        label="windowed versions need Windowed annotation",
                        range=error_builder.property_range(f.attribute_name),
                        code="19",
                    )
                continue

            for i, mapped_feature in f.version.reference.items():
                if not isinstance(mapped_feature, Feature):
                    continue
                f_i = copy.copy(mapped_feature)
                f_i.namespace = namespace

                f_i.version = VersionInfo(
                    version=i,
                    maximum=f.version.maximum,
                    default=f.version.default,
                    reference=f.version.reference,
                    base_name=getattr(f_i, "name", None) or f.version.base_name,
                    explicitly_enumerated=False,
                )
                cls_cast = cast(Type, cls)
                if not f_i.is_typ_set():
                    f_i.typ = ParsedAnnotation(cls_cast, f.attribute_name)

                f_i.features_cls = cls_cast
                f_i.attribute_name = f"{f.attribute_name}_v{i}"
                if not hasattr(f_i, "name"):
                    f_i.name = f_i.version.name_for_version(i)
                f_i.unversioned_attribute_name = f.attribute_name
                f_i.is_singleton = f.is_singleton
                _process_field(
                    f=f_i,
                    comment_metadata=comment_metadata,
                    class_owner=owner,
                    class_tags=tags,
                    class_etl_offline_to_online=etl_offline_to_online,
                    class_max_staleness=max_staleness,
                    class_cache_strategy=cache_strategy,
                    error_builder=error_builder,
                )

                # copy over expressions and metadata for default version
                if i == f.version.default:
                    if f.underscore_expression is None and f_i.underscore_expression is not None:
                        f.underscore_expression = f_i.underscore_expression
                    if f.offline_underscore_expression is None and f_i.offline_underscore_expression is not None:
                        f.offline_underscore_expression = f_i.offline_underscore_expression
                    # Copy description from the explicitly defined default version,
                    # or fall back the other direction so the alias's comment-derived
                    # description reaches the default-version child. Without this
                    # fallback, the unversioned alias and its v1 child desync, and a
                    # proto roundtrip on the FQN returns a feature with description=None.
                    if f.description is None and f_i.description is not None:
                        f.description = f_i.description
                    elif f_i.description is None and f.description is not None:
                        f_i.description = f.description
                    # Propagate per-version properties from the default version to the
                    # unversioned-access alias. Without this, `A.x` returns a Feature that
                    # only carries class-level settings, ignoring anything set per-version.
                    f.max_staleness = f_i.max_staleness
                    f._raw_max_staleness = f_i._raw_max_staleness
                    f.etl_offline_to_online = f_i.etl_offline_to_online
                    f.raw_etl_offline_to_online = f_i.raw_etl_offline_to_online
                    f.offline_ttl = f_i.offline_ttl
                    f.cache_strategy = f_i.cache_strategy
                    f.owner = f_i.owner
                    f.tags = f_i.tags
                    # `_default`, `_typ`, `_converter`, `_encoder`, `_decoder`,
                    # `_pyarrow_dtype` are typed Final at runtime (feature_field.py:390-393);
                    # bypass the typing restriction since we legitimately need to re-target
                    # the alias's type/converter to the default version's (e.g. versioned
                    # dtype like uint32 on v1 vs int32 on v2).
                    object.__setattr__(f, "_default", f_i._default)
                    object.__setattr__(f, "_typ", f_i._typ)
                    object.__setattr__(f, "_converter", f_i._converter)
                    object.__setattr__(f, "_encoder", f_i._encoder)
                    object.__setattr__(f, "_decoder", f_i._decoder)
                    object.__setattr__(f, "_pyarrow_dtype", f_i._pyarrow_dtype)
                    f.is_deprecated = f_i.is_deprecated
                    f.store_online = f_i.store_online
                    f.store_offline = f_i.store_offline

                f.version.reference[i] = f_i
                # The default feature already exists.
                f_i.no_display = i == f.version.default
                cls_fields.append(f_i)
                # Ensure version-expanded windowed features get processed by the importer
                # for materialization parsing (otherwise only the base/default gets parsed).
                if f_i.window_materialization is not None and i != f.version.default:
                    materialized_windows.append(f_i)
            continue

        for i in range(1, f.version.maximum + 1):
            f_i = copy.copy(f)
            f_i.name = f.version.name_for_version(i)
            f_i.unversioned_attribute_name = f.attribute_name
            f_i.attribute_name = f"{f.attribute_name}_v{i}"
            f_i.version = VersionInfo(
                version=i,
                maximum=f.version.maximum,
                default=f.version.default,
                reference=f.version.reference,
                base_name=f.version.base_name,
                explicitly_enumerated=False,
            )
            f.version.reference[i] = f_i
            cls_fields.append(f_i)

            # The default feature already exists.
            f_i.no_display = i == f.version.default

            if f_i.attribute_name in cls.__annotations__:
                assert f_i.features_cls is not None
                error_builder.add_diagnostic(
                    message=(
                        f"The class '{f_i.features_cls.__name__}' "
                        f"has an existing annotation '{f_i.attribute_name}' "
                        "that collides with a versioned feature. Please remove the existing "
                        "annotation, or lower the version."
                    ),
                    range=error_builder.property_range(f_i.attribute_name),
                    label="invalid name",
                    raise_error=ValueError,
                    code="21",
                )
            cls.__annotations__[f_i.attribute_name] = cls.__annotations__[f.attribute_name]

    set_new_attribute(
        cls=cls,
        name="__setattr__",
        value=_setattr_fn(
            bidirectional_alias={**{v: k for k, v in alias_from_to.items()}, **alias_from_to},
        ),
    )

    set_new_attribute(
        cls=cls,
        name="__init__",
        value=_init_fn(
            additional_inits=FrozenOrderedSet(additional_inits),
            alias_from_to=alias_from_to,
        ),
    )

    # Stored so late extensions (add_features / part_of after the class is
    # defined) can add windowed alias entries and regenerate __init__ and
    # __setattr__, whose alias maps are otherwise frozen in their closures.
    set_new_attribute(cls=cls, name="__chalk_alias_from_to__", value=alias_from_to)
    set_new_attribute(cls=cls, name="__chalk_additional_inits__", value=additional_inits)

    for f in cls_fields:
        assert f.attribute_name is not None
        f.features_cls = cast(Type[Features], cls)
        # Wrap all class features with FeatureWrapper
        setattr(cls, f.attribute_name, FeatureWrapper(f))

        if f.hook:
            f.hook(cast(Type[Features], cls))

    set_new_attribute(cls=cls, name="__chalk_feature_set__", value=True)
    return cls


def _can_overwrite_feature(cls: Type[Features], key: str, existing_feature: Optional[Feature] = None) -> bool:
    """
    Note: Can't really distinguish between features declared like this in a notebook cell
    vs. features declared like this in code imported from a notebook cell (e.g. customer code)
    Gonna treat both the same since this code only runs in a notebook context
    (e.g. customers can't use this pattern as part of their deployment code)
    """
    from chalk.features.feature_set import FeatureSetBase

    if notebook.is_defined_in_module(cls) and key not in FeatureSetBase.__chalk_notebook_defined_feature_fields__.get(
        cls.namespace, set()
    ):
        if existing_feature is not None:
            return False

    return True


def _class_setattr(
    cls: Type[Features],
    key: str,
    value: Any,
):
    from chalk.features.feature_set import FeatureSetBase

    # Handle inline feature definitions in notebooks
    if (
        (key.startswith("__") and key.endswith("__"))
        or key == "features"
        or key == "namespace"
        or isinstance(value, FeatureWrapper)
    ):
        # If it's a dunder, then  set it directly
        # If it's the literal 'features' or 'namespace', then set it directly -- Chalk reserves these names
        # If it's already a FeatureWrapper, then assume it was already constructed correctly, so set it directly
        type.__setattr__(cls, key, value)
        return
    f = None
    existing_feature = None
    is_notebook_defined_feature = False
    if isinstance(value, Underscore):
        # Handle the case of `User.new_feat: typ = ....` in a notebook
        from chalk.df.ast_parser import parse_inline_setattr_annotation

        fqn = build_namespaced_name(name=f"{cls.namespace}.{key}")
        existing_feature = next((ff for ff in cls.features if ff.fqn == fqn), None)
        typ = parse_inline_setattr_annotation(key)
        is_notebook_defined_feature: bool = notebook.is_notebook()

        if is_notebook_defined_feature and not _can_overwrite_feature(cls, key, existing_feature):
            raise ValueError(
                f"Can't overwrite feature '{cls.namespace}.{key}' because it already exists in the deployment source."
            )

        if typ is None:
            if is_notebook_defined_feature or existing_feature is None:
                raise TypeError(
                    f"Please define a type annotation for feature '{fqn}', like so: User.new_feature: typ = _.a + _.b"
                )
            else:
                parsed_annotation = ParsedAnnotation(underlying=existing_feature.typ.parsed_annotation)
        else:
            parsed_annotation = ParsedAnnotation(underlying=typ)

        # Always create a new feature to avoid type initialization issues
        f = Feature(
            namespace=cls.namespace,
            name=key,
            attribute_name=key,
            features_cls=cls,
            typ=parsed_annotation,
            underscore_expression=value,
        )
    elif isinstance(value, Feature):
        # Handle the case of `User.new_feat = feature(....)` in a notebook
        f = value
        if notebook.is_notebook():
            is_notebook_defined_feature = True
            existing_feature = next((ff for ff in cls.features if ff.unversioned_attribute_name == key), None)
            if not _can_overwrite_feature(cls, key, existing_feature):
                raise ValueError(
                    f"Can't overwrite feature '{cls.namespace}.{key}' because it already exists in the deployment source."
                )
            if hasattr(f, "max_staleness") and f.max_staleness.total_seconds() > 0:
                raise ValueError(
                    "Cannot set `max_staleness` on a notebook defined feature: persistence is not supported for notebook defined features"
                )
            # Get the type annotation
            parsed_annotation: Optional[ParsedAnnotation] = None
            if existing_feature is not None:
                parsed_annotation = ParsedAnnotation(underlying=existing_feature.typ.parsed_annotation)
            if f._typ is not None and f.typ._unparsed_underlying is not None:
                # If the feature already has a type annotation, use that
                parsed_annotation = f.typ
            else:
                from chalk.df.ast_parser import parse_inline_setattr_annotation

                typ = parse_inline_setattr_annotation(key)
                if typ is not None:
                    parsed_annotation = ParsedAnnotation(underlying=typ)
            if parsed_annotation is None:
                raise TypeError(
                    f"Please define a type annotation for feature '{cls.namespace}.{key}', like so: User.new_feature=feature(typ=str)"
                )
            # Set some attributes that usually get set when the feature is created inside the class definition
            f.attribute_name = key
            f.unversioned_attribute_name = key
            if getattr(f, "name", None) is None:
                f.name = key
            f.namespace = cls.namespace
            f.typ = parsed_annotation
    else:
        # Passing a feature in directly is used internally, so not mentioning that in the error message
        raise TypeError(
            (
                f"In order to define feature '{cls.namespace}.{key}', "
                "please set it equal to an underscore expression. "
                f"For example, `{cls.__name__}.{key}: int = _.a + _.b`."
            )
        )

    # Clear the cache so that the new feature definition propagates
    Feature._from_root_fqn.cache_clear()

    # Process feature field
    f.features_cls = cls
    _process_field(
        f=f,
        error_builder=cls.__chalk_error_builder__,
        comment_metadata={},
        class_owner=cls.__chalk_owner__,
        class_tags=tuple(cls.__chalk_tags__),
        class_etl_offline_to_online=cls.__chalk_etl_offline_to_online__,
        class_max_staleness=cls.__chalk_max_staleness__,
        class_cache_strategy=cls.__chalk_cache_strategy__,
    )
    if existing_feature is not None:
        cls.features.remove(existing_feature)
    cls.features.append(f)
    wrapped_feature = FeatureWrapper(f)
    type.__setattr__(cls, key, wrapped_feature)
    if is_notebook_defined_feature:
        assert f.unversioned_attribute_name is not None  # for pyright
        FeatureSetBase.__chalk_notebook_defined_feature_fields__[cls.namespace].add(f.unversioned_attribute_name)


def parse_quoted_window_feature(annotation_str: str, module_str: str) -> Type[Windowed]:
    """
    Parses a string like "Windowed[int]", "Windowed[list[int]]", "Windowed[SomeStruct]",
    "Windowed[Optional[datetime]]", or "Windowed[dt.datetime | None]"
    and returns Windowed with the appropriate type.
    """
    match = re.fullmatch(r"Windowed\[(.+)\]", annotation_str)
    if not match:
        raise ValueError(f"Invalid type format: {annotation_str}")

    inner_type_str = match.group(1)

    module = sys.modules.get(module_str, None)
    module_globals = getattr(module, "__dict__", {})

    try:
        # Handle built-in types, typing constructs, and module-level names (including
        # dotted aliases like `dt.datetime` and union types like `dt.datetime | None`)
        inner_type = eval(inner_type_str, {"__builtins__": builtins, **typing.__dict__, **module_globals})
    except Exception:
        raise ValueError(f"Unknown type: {inner_type_str}")

    return Windowed[inner_type]
