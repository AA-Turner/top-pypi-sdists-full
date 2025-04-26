from __future__ import annotations

import copy
import dataclasses
import functools
import itertools
import re
from datetime import timedelta, datetime
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Final,
    Generic,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
)

import numpy as np
import pyarrow as pa

from chalk._lsp.error_builder import FeatureClassErrorBuilder
from chalk._validation.feature_validation import FeatureValidation
from chalk._validation.validation import Validation
from chalk.features._encoding.converter import FeatureConverter, JSONCodec, TDecoder, TEncoder
from chalk.features._encoding.primitive import TPrimitive
from chalk.features.feature_set import FeatureSetBase
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.filter import Filter, TimeDelta, ClauseJoinWithAndException
from chalk.features.tag import Tags
from chalk.features.underscore import Underscore
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.utils.collections import ensure_tuple, get_unique_item, OrderedSet
from chalk.utils.duration import CHALK_MAX_TIMEDELTA, Duration, parse_chalk_duration
from chalk.utils.json import JSON, pyarrow_json_type
from chalk.utils.log_with_context import get_logger
from chalk.utils.pydanticutil.pydantic_compat import is_pydantic_basemodel, is_pydantic_basemodel_instance
from chalk.utils.string import to_snake_case, oxford_comma_list

if TYPE_CHECKING:
    from google.protobuf.message import Message as ProtobufMessage

    from chalk.features.feature_set import Features
    from chalk.streams._windows import GroupByWindowed, MaterializationWindowConfig

_TRich = TypeVar("_TRich")
_TPrim = TypeVar("_TPrim", bound=TPrimitive)

_logger = get_logger(__name__)


@dataclasses.dataclass(frozen=True)
class HasOnePathObj:
    parent: Feature
    child: Feature
    parent_to_child_attribute_name: str


@dataclasses.dataclass
class VersionInfo:
    version: int
    maximum: int
    default: int
    reference: Dict[int, Feature]
    base_name: str = ""

    def name_for_version(self, version: int) -> str:
        return self.base_name if version == 1 else f"{self.base_name}@{version}"


class JoinCatalogue:
    def __init__(self):
        super().__init__()
        self.catalogue: Dict[Filter, str] = {}

    def add_join(self, new_filter: Filter, fqn: str):
        for f in self.catalogue.keys():
            if f.operation == new_filter.operation and {f.lhs, f.rhs} == {new_filter.lhs, new_filter.rhs}:
                return
        self.catalogue[new_filter] = fqn

    def num_joins(self) -> int:
        return len(self.catalogue)

    def invalid_join_string(self) -> str:
        return oxford_comma_list(self.catalogue.values(), quoted=True)

    def only_valid_join(self) -> Filter:
        return get_unique_item(self.catalogue)


class FeatureNotFoundException(ValueError):
    def __init__(self, fqn: str) -> None:
        super().__init__(
            f"Feature '{fqn}' was not found in the registry. Please ensure that '{fqn}' is defined on your @features class and imported into this file."
        )


def get_distance_feature_name(local_namespace: str, local_name: str, local_hm_name: str, op: str, foreign_name: str):
    """Get the name for a pseudofeature in the foreign namespace that represents the vector distance"""
    return f"__chalk__distance__{foreign_name}__{op}__{local_namespace}__{local_name}__{local_hm_name}__"


@dataclasses.dataclass(frozen=True)
class WindowConfigResolved:
    """The window config is entirely in terms of the child namespace.
    Many parent namespaces could map into the same WindowConfigParsed.

    User.transactions.group_by(_.mcc).agg(_.amount.sum())
      - namespace = "transactions"
      - group_by = (Transactions.user_id, Transaction.mcc,)
      - aggregate_on = Transaction.amount
      - aggregation = "sum"

    User.transactions[_.amount].sum()
      - namespace = "transactions"
      - group_by = (Transactions.user_id,)
      - aggregate_on = Transaction.amount
      - aggregation = "sum"

    User.transactions.count()
      - namespace = "transactions"
      - group_by = (Transactions.user_id,)
      - aggregate_on = None
      - aggregation = "count"
    """

    namespace: str

    group_by: list[Feature]
    """Will have at least one feature, the foreign side of the join key"""

    bucket_duration_seconds: int
    """The duration of the buckets for the purpose of aggregations.
    This is not the same as the window duration, which aggregates
    many buckets to compute the rolled-up value.
    """

    bucket_start: datetime
    """The lower bound of the first bucket. All future buckets are aligned to this."""

    aggregation: str
    """'sum', 'count', 'min', 'max', etc."""

    aggregate_on: Feature | None
    """If there was no provided child feature,
    as could be the case with count, we will
    pick the primary key"""

    pyarrow_dtype: pa.DataType

    filters: list[Filter]

    backfill_resolver: str | None
    backfill_schedule: str | None
    backfill_lookback_duration_seconds: int | None
    backfill_start_time: datetime | None
    continuous_resolver: str | None
    continuous_buffer_duration_seconds: int | None


class CacheStrategy(Enum):
    ALL = "all"
    NO_NULLS = "no_nulls"
    NO_DEFAULTS = "no_defaults"
    NO_NULLS_OR_DEFAULTS = "no_nulls_or_defaults"
    EVICT_NULLS = "evict_nulls"
    EVICT_DEFAULTS = "evict_defaults"
    EVICT_NULLS_AND_DEFAULTS = "evict_nulls_and_defaults"


class Feature(Generic[_TPrim, _TRich]):
    window_materialization: MaterializationWindowConfig | Literal[True] | None

    @property
    def lsp_error_builder(self) -> FeatureClassErrorBuilder:
        assert self.features_cls is not None
        return self.features_cls.__chalk_error_builder__

    __slots__ = (
        "_all_validations",
        "_converter",
        "_converter_entered",
        "_decoder",
        "_default",
        "_encoder",
        "_fqn",
        "_hash",
        "_is_feature_time",
        "_is_has_many_subfeature",
        "_join",
        "_join_type",
        "_path",
        "_primary",
        "_primary_feature",
        "_pyarrow_dtype",
        "_raw_max_staleness",
        "_root_fqn",
        "_root_namespace",
        "_typ",
        "_validations",
        "attribute_name",
        "cache_strategy",
        "description",
        "etl_offline_to_online",
        "features_cls",
        "group_by_windowed",
        "hook",
        "is_autogenerated",
        "is_deprecated",
        "is_distance_pseudofeature",
        "is_pseudofeature",
        "is_singleton",
        "last",
        "last_for",
        "max_staleness",
        "name",
        "namespace",
        "no_display",
        "offline_ttl",
        "owner",
        "raw_etl_offline_to_online",
        "store_online",
        "store_offline",
        "tags",
        "underlying",
        "underscore_expression",
        "version",
        "window_duration",
        "window_durations",
        "window_materialization",
        "window_materialization_parsed",
    )

    def __init__(
        self,
        name: str | None = None,
        attribute_name: str | None = None,
        namespace: str | None = None,
        features_cls: Type[Features] | None = None,
        typ: ParsedAnnotation | Type[_TRich] | None = None,
        version: int | None = None,
        default_version: int = 1,
        description: str | None = None,
        owner: str | None = None,
        tags: list[str] | None = None,
        primary: bool | None = None,
        default: _TRich | ellipsis = ...,
        underscore_expression: Underscore | None = None,
        max_staleness: Duration | None | ellipsis = ...,
        cache_strategy: CacheStrategy = CacheStrategy.ALL,
        etl_offline_to_online: bool | None = None,
        encoder: TEncoder[_TPrim, _TRich] | None = None,
        decoder: TDecoder[_TPrim, _TRich] | None = None,
        pyarrow_dtype: pa.DataType | None = None,
        join: Callable[[], Filter] | Filter | None = None,
        is_feature_time: bool | None = None,
        is_autogenerated: bool = False,
        validations: FeatureValidation | None = None,
        all_validations: list[FeatureValidation] | None = None,
        # Window durations should be set on the Windowed() parent feature,
        # and contain all the durations of the child features
        window_durations: Sequence[int] = (),
        # Windowed duration should be set on the underlying pseudofeature that represents a particular windowed bucket
        window_duration: int | None = None,
        no_display: bool = False,
        offline_ttl: Duration | None | ellipsis = ...,
        last_for: Feature | None = None,
        hook: Callable[[type[Features]], None] | None = None,
        is_distance_pseudofeature: bool = False,
        is_pseudofeature: bool = False,
        window_materialization: "MaterializationWindowConfig | Literal[True] | None" = None,
        group_by_windowed: GroupByWindowed | None = None,
        is_deprecated: bool = False,
        join_type: Literal["has_one", "has_many"] | None = None,
        store_online: bool = True,
        store_offline: bool = True,
        # only used for type validation on chalk apply. see `.typ`, '.join`, etc. for the actual join info
    ):
        super().__init__()
        self.is_deprecated = is_deprecated
        self.is_pseudofeature = is_pseudofeature
        self.is_singleton = False
        self.group_by_windowed = group_by_windowed
        self.last = None
        self.last_for = last_for
        self._typ = typ if typ is None or isinstance(typ, ParsedAnnotation) else ParsedAnnotation(underlying=typ)
        self._converter = None
        self.features_cls = features_cls
        if name is None:
            name = attribute_name
        if name is not None:
            self.name = name
        # the attribute name for the feature in the @features class (in case if the name is specified differently)
        if attribute_name is not None:
            self.attribute_name = attribute_name
        if namespace is not None:
            self.namespace = namespace
        self._path: tuple[HasOnePathObj, ...] = ()
        self._is_has_many_subfeature: bool | None = None
        self.window_materialization: MaterializationWindowConfig | Literal[True] | None = window_materialization
        self.window_materialization_parsed: WindowConfigResolved | None = None
        self._converter_entered = 0

        # if primary is True and version is not None:
        #     self.lsp_error_builder.add_diagnostic(
        #         label="versioned feature",
        #         code="44",
        #         range=self.lsp_error_builder.property_value_kwarg_range(attribute_name or name, kwarg="version")
        #         or self.lsp_error_builder.property_value_range(attribute_name or name)
        #         or self.lsp_error_builder.annotation_range(attribute_name or name)
        #         or self.lsp_error_builder.property_range(attribute_name or name),
        #         message=(
        #             "A versioned feature cannot also be marked as a primary feature. You provided "
        #             f"primary={primary}, version={str(version)}. Please remove version={str(version)} "
        #             "from the `features` declaration."
        #         ),
        #         raise_error=ValueError,
        #     )

        self.version: Optional[VersionInfo] = (
            VersionInfo(
                version=default_version,
                maximum=version,
                default=default_version,
                reference={},
            )
            if version is not None
            else None
        )

        self.description = description
        self.owner = owner
        # The encoder, decoder, pyarrow dtype, and default are marked as final,
        # as they are forwarded to the FeatureConverter, which is constructed
        # on first use to get around forward references.
        self._encoder: Final = encoder
        self._decoder: Final = decoder
        self._pyarrow_dtype: Final = pyarrow_dtype
        self._default: Final = default
        self.tags = tags
        self._primary = primary
        self._primary_feature: Optional[Feature] = None
        self.underscore_expression: Underscore | None = underscore_expression
        self.is_distance_pseudofeature = is_distance_pseudofeature

        self._raw_max_staleness = max_staleness
        if last_for is not None:
            max_staleness = CHALK_MAX_TIMEDELTA
        elif max_staleness is None:
            max_staleness = timedelta(0)
        elif isinstance(max_staleness, str):
            max_staleness = parse_chalk_duration(max_staleness)
        if max_staleness is not ...:
            self.max_staleness = max_staleness

        if offline_ttl is None:
            offline_ttl = timedelta(0)
        elif offline_ttl is ...:
            # Should we allow the offline_ttl to be set via the class decorator?
            offline_ttl = CHALK_MAX_TIMEDELTA
        elif isinstance(offline_ttl, str):
            offline_ttl = parse_chalk_duration(offline_ttl)
        self.offline_ttl = offline_ttl

        self.cache_strategy = cache_strategy

        if etl_offline_to_online is not None:
            self.etl_offline_to_online = etl_offline_to_online
        self.raw_etl_offline_to_online = etl_offline_to_online
        self._is_feature_time = is_feature_time
        self.is_autogenerated = is_autogenerated
        self.no_display = no_display
        self._join = join
        self._validations = validations
        self._all_validations = all_validations or []
        if self._validations is not None:
            self._all_validations.append(self._validations)
        self.window_durations = window_durations
        self.window_duration = window_duration
        if last_for is not None:
            assert last_for.features_cls is not None
            for f in last_for.features_cls.features:
                if f.name == last_for.name:
                    f.last = last_for
                    break
        self.hook = hook
        self.underlying: Feature | None = None
        self._root_fqn: str | None = None
        self._root_namespace: str | None = None
        self._fqn: str | None = None
        self._hash: int | None = None
        self._join_type: Literal["has_one", "has_many"] | None = join_type
        self.store_online = store_online
        self.store_offline = store_offline

    @property
    def all_validations(self):
        return self._all_validations

    @property
    def raw_max_staleness(self):
        return self._raw_max_staleness

    @property
    def default(self):
        return self._default

    @property
    def fqn(self):
        if self._fqn is None:
            self._fqn = f"{self.namespace}.{self.name}"
        return self._fqn

    def __str__(self):
        return self.root_fqn

    @property
    def typ(self) -> ParsedAnnotation:
        if self._typ is None:
            raise RuntimeError("Feature.typ has not yet been set")
        return self._typ

    @typ.setter
    def typ(self, typ: ParsedAnnotation):
        self._typ = typ

    def is_typ_set(self):
        return self._typ is not None

    @property
    def primary(self) -> bool:
        if self._primary is not None:
            return self._primary
        if self.underlying is None:
            return (
                self.features_cls is not None
                and self.features_cls.__chalk_primary__ is not None
                and self.features_cls.__chalk_primary__.name == self.name
            ) or self.typ.is_primary()
        else:
            return self.underlying.primary

    @property
    def is_feature_time(self) -> bool:
        if self._is_feature_time is not None:
            return self._is_feature_time

        if self.underlying is None:
            return (
                self.features_cls is not None
                and self.features_cls.__chalk_ts__ is not None
                and self.features_cls.__chalk_ts__.name == self.name
            ) or self.typ.is_feature_time()
        else:
            return self.underlying.is_feature_time

    @property
    def converter(self) -> FeatureConverter:
        from chalk.features import DataFrame, Vector

        self._converter_entered += 1

        if self.underlying is not None:
            return self.underlying.converter
        if self._converter is not None:
            return self._converter

        encoder: TEncoder[_TPrim, _TRich] | None = self._encoder
        decoder: TDecoder[_TPrim, _TRich] | None = self._decoder
        pyarrow_dtype = self._pyarrow_dtype
        rich_type = self.typ.parsed_annotation

        if rich_type is JSON:  # pyright: ignore[reportUnnecessaryComparison]
            pyarrow_dtype = pyarrow_json_type()
            encoder = cast(TEncoder[_TPrim, _TRich], JSONCodec.encode)
            decoder = cast(TDecoder[_TPrim, _TRich], JSONCodec.decode)

        document_typ = self.typ.as_document()
        if document_typ is not None:
            if encoder is None:

                def document_encoder(x: _TRich):
                    if is_pydantic_basemodel_instance(x):
                        return x.json()
                    raise TypeError("Document classes must be Pydantic models")

                encoder = cast(TEncoder[_TPrim, _TRich], document_encoder)

            if decoder is None:

                def document_decoder(x: str):
                    assert document_typ is not None
                    if is_pydantic_basemodel(document_typ):
                        return document_typ.parse_raw(x)
                    raise TypeError("Document classes must be Pydantic models")

                decoder = cast(TDecoder[_TPrim, _TRich], document_decoder)

            if pyarrow_dtype is None:
                pyarrow_dtype = pa.large_utf8()

        proto_typ = self.typ.as_proto()
        if proto_typ is not None:
            if encoder is None:

                def proto_encoder(x: ProtobufMessage):
                    return x.SerializeToString()

                encoder = cast(TEncoder[_TPrim, _TRich], proto_encoder)

            if decoder is None:

                def proto_decoder(x: bytes):
                    message = proto_typ()
                    message.ParseFromString(x)
                    return message

                decoder = cast(TDecoder[_TPrim, _TRich], proto_decoder)

            if pyarrow_dtype is None:
                pyarrow_dtype = pa.large_binary()

        dataframe_typ = self.typ.as_dataframe()
        if dataframe_typ is not None:
            # the has_many signature doesn't have fields for the encoder/decoder/pyarrow_dtype, so these fields should always be null
            assert decoder is None
            assert encoder is None
            assert pyarrow_dtype is None

            column_features: Dict[str, Feature] = {col.root_fqn: col for col in dataframe_typ.columns}

            def frame_encoder(x: DataFrame) -> List[Dict[str, Any]]:
                # DataFrame --> List[Dict[root_fqn, value]]
                # Storing these in column-major order (Dict[fqn -> List[value]]) might be better but
                # Right now it lines up w/ how resolvers expect DF[has-many's] to show up, i.e. a list of structs
                # (Primarily so that resolvers that receive a DataFrame w/ a has-many can inspect length easily)
                if len(x) == 0:
                    return []
                result: List[Dict[str, Any]] = []
                for row in x.to_features():
                    row_dict: Dict[str, Any] = {}
                    for fqn, value in row.items():
                        converted_value = column_features[fqn].converter.from_rich_to_primitive(value)
                        row_dict[fqn] = converted_value
                    result.append(row_dict)
                return result

            encoder = cast(TEncoder[_TPrim, _TRich], frame_encoder)

            def frame_decoder(x: List[Dict[str, Any]]):
                # List[Dict[root_fqn, value]] --> DataFrame

                # Special case for empty dataframe, need to specify the columns manually
                # since there are no elements to infer them from
                if len(x) == 0:
                    return DataFrame({k: [] for k in column_features.keys()})

                results: List[Features] = []
                for row in x:
                    rich_features = {}
                    for fqn, value in row.items():
                        if fqn not in column_features:
                            continue
                        # Strip namespace from FQN before passing in to rich type constructor
                        rich_features[fqn.split(".")[-1]] = column_features[fqn].converter.from_primitive_to_rich(value)
                    assert dataframe_typ is not None
                    assert dataframe_typ.references_feature_set is not None
                    results.append(dataframe_typ.references_feature_set(**rich_features))
                return DataFrame(results)

            decoder = cast(TDecoder[_TPrim, _TRich], frame_decoder)

        feature_set_typ = self.typ.as_features_cls()
        if feature_set_typ is not None:
            # Don't explicitly get field.converter here to avoid infinite recursion
            # the has_one signature doesn't have fields for the encoder/decoder/pyarrow_dtype, so these fields should always be null
            assert decoder is None
            assert encoder is None
            assert pyarrow_dtype is None

            field_features: Dict[str, Feature] = {field.root_fqn: field for field in feature_set_typ.features}

            def feature_class_encoder(rich: Features) -> Dict[str, Any]:
                # @features class -> Dict[root_fqn, primitive_value]
                encoded_fields = {}
                for fqn, rich_value in rich.items():
                    encoded_fields[fqn] = field_features[fqn].converter.from_rich_to_primitive(rich_value)
                return encoded_fields

            encoder = cast(TEncoder[_TPrim, _TRich], feature_class_encoder)

            def feature_class_decoder(x: Dict[str, Any]) -> Features:
                # Dict[root_fqn, primitive_value] -> @features class
                decoded_fields = {}
                for root_fqn, primitive_value in x.items():
                    field_name = root_fqn.split(".")[-1]
                    rich_value = field_features[root_fqn].converter.from_primitive_to_rich(primitive_value)
                    decoded_fields[field_name] = rich_value
                return feature_set_typ(**decoded_fields)

            decoder = cast(TDecoder[_TPrim, _TRich], feature_class_decoder)

        vector_typ = self.typ.as_vector()
        if vector_typ is not None:
            if decoder is not None:
                raise ValueError(
                    (
                        "When using a Vector type, the decoder cannot be manually specified. Please remove the "
                        f"`feature(decoder=...)` argument from the feature definition for feature '{self.root_fqn}'."
                    )
                )

            def vector_decoder(primitive: Vector | List[float]) -> Vector:
                if isinstance(primitive, Vector):
                    return primitive
                data = np.array(primitive, dtype=np.dtype(vector_typ.precision.replace("fp", "float")))
                return Vector(data)

            decoder = cast(TDecoder[_TPrim, _TRich], vector_decoder)
            if encoder is not None:
                raise ValueError(
                    (
                        "When using a Vector type, the encoder cannot be manually specified. Please remove the "
                        f"`feature(encoder=...)` argument from the feature definition for feature '{self.root_fqn}'"
                    )
                )

            def vector_encoder(rich: Vector) -> List[float]:
                return [float(x) for x in rich.to_pylist()]

            encoder = cast(TEncoder[_TPrim, _TRich], vector_encoder)
            if pyarrow_dtype is None:
                try:
                    pyarrow_dtype = vector_typ.dtype
                except AttributeError:
                    # The dtype property will not be set if someone does x: Vector without specifying the type in the generics
                    raise ValueError(
                        (
                            f"The vector annotation for feature '{self.root_fqn}' is missing the number of dimensions. "
                            f"Please update the annotation from `{self.attribute_name}: Vector` to "
                            f"`{self.attribute_name}: Vector[N]`, where N is the number of dimensions."
                        )
                    ) from None

            if not pa.types.is_fixed_size_list(pyarrow_dtype):
                raise TypeError(
                    f"Vector types must be serialized as a PyArrow FixedSizeList. Feature '{self.root_fqn}' is of type {pyarrow_dtype}."
                )
            assert isinstance(pyarrow_dtype, pa.FixedSizeListType)
            value_type = pyarrow_dtype.value_type
            if value_type not in (pa.float16(), pa.float32(), pa.float64()):
                raise TypeError(
                    f"Vector types must be PyArrow FixedSizeLists of float16, float32, or float64 values. Feature '{self.root_fqn}' is of type {pyarrow_dtype}."
                )

        feature_typ = self.typ.as_feature()
        if feature_typ is not None:
            if self._converter_entered > 1:
                raise TypeError(
                    (
                        f"Feature annotation cycle detected: feature '{self.fqn}' is annotated with "
                        f"type '{feature_typ.fqn}', but '{feature_typ.fqn}'s type cannot be resolved because of the presence of a cycle. "
                        f"Please make sure that feature types that are annotated with other features are not defined circularly."
                    )
                )

            rich_type = feature_typ.converter.rich_type
            encoder = cast(TEncoder[_TPrim, _TRich], feature_typ.converter.encoder)
            decoder = cast(TDecoder[_TPrim, _TRich], feature_typ.converter.decoder)
            pyarrow_dtype = feature_typ.converter.pyarrow_dtype

        self._converter = FeatureConverter(
            name=self.fqn,
            rich_type=rich_type,
            is_nullable=self.typ.is_nullable,
            rich_default=self._default,
            pyarrow_dtype=pyarrow_dtype,
            encoder=encoder,
            decoder=decoder,
        )
        return self._converter

    def is_name_set(self):
        return hasattr(self, "name")

    @classmethod
    @functools.lru_cache(None)
    def from_root_fqn(cls, root_fqn: str) -> Feature:
        """Convert a Root FQN into a feature.

        Parameters
        ----------
        root_fqn
            The root fqn of the feature

        Returns
        -------
        Feature
            The feature for that root_fqn.
        """
        from chalk.features.feature_set import FeatureSetBase
        from chalk.features.pseudofeatures import FQN_OR_NAME_TO_PSEUDOFEATURE

        if root_fqn in FQN_OR_NAME_TO_PSEUDOFEATURE:
            return FQN_OR_NAME_TO_PSEUDOFEATURE[root_fqn]

        split_fqn = root_fqn.split(".")
        root_ns = split_fqn[0]
        root_ns_snake_case = to_snake_case(root_ns)
        root_ns = root_ns_snake_case
        split_fqn = split_fqn[1:]
        if root_ns not in FeatureSetBase.registry:
            raise FeatureNotFoundException(root_fqn)
        features_cls = FeatureSetBase.registry[root_ns]

        # FQNs are by name, so must look up the feature in features_cls.features instead of using getattr
        feat: Optional[Feature] = None

        while len(split_fqn) > 0:
            feature_name = split_fqn[0]
            split_fqn = split_fqn[1:]

            found_feature = False

            for x in features_cls.features:
                assert isinstance(x, Feature)
                if x.name == feature_name or feature_name.lower() in {x.name, *x.window_alias_name}:
                    assert x.attribute_name is not None
                    found_feature = True
                    feat = x if feat is None else feat.copy_with_path(x)
                    if len(split_fqn) > 0:
                        # Going to recurse, so validate that the feature is something that we can recurse on.
                        if not x.is_has_one and not x.is_has_many:
                            raise FeatureNotFoundException(root_fqn)
                        assert x.joined_class is not None
                        features_cls = x.joined_class
                    break
            if not found_feature:
                raise FeatureNotFoundException(root_fqn)
        if feat is None:
            raise FeatureNotFoundException(root_fqn)

        return feat

    @property
    def root_namespace(self):
        if self._root_namespace is None:
            self.path = self._path
        assert self._root_namespace is not None
        return self._root_namespace

    @property
    def root_fqn(self):
        if self._root_fqn is None:
            self.path = self._path
        assert self._root_fqn is not None
        return self._root_fqn

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: tuple[HasOnePathObj, ...]):
        self._path = path
        if len(path) > 0:
            assert path[0].parent.namespace is not None, "parent namespace is None"
            self._root_namespace = path[0].parent.namespace
            self._root_fqn = ".".join(
                itertools.chain(
                    (self._root_namespace,),
                    (x.parent.name for x in self.path),
                    (self.name,),
                )
            )
        else:
            self._root_namespace = self.namespace
            self._root_fqn = f"{self.namespace}.{self.name}"
        self._hash = hash(self.root_fqn)
        self._is_has_many_subfeature = any(p.parent.is_has_many for p in self.path)

    def __hash__(self) -> int:
        if self._hash is None:
            self.path = self._path
        assert self._hash is not None
        return self._hash

    def __eq__(self, other: object) -> bool:
        if self.is_has_many:
            # For equality checks on a has-many, we would also need to compare the columns and types
            # For now, ignoring.

            if not isinstance(other, Feature):
                return NotImplemented

            if other.root_fqn != self.root_fqn:
                return False

            if not other.is_has_many:
                return False

            is_equal = other.typ == self.typ
            return is_equal
        if isinstance(other, Feature):
            other = other.root_fqn
        if isinstance(other, str):
            return self.root_fqn == other
        return NotImplemented

    def __repr__(self):
        return f"Feature(fqn={self.root_fqn}, typ={self.typ})"

    @property
    def is_has_one(self) -> bool:
        # A feature is a has-one relationship if the type is
        # another singleton features cls and there is a join condition
        # Need to short-circuit if it is a dataframe, as DataFrames
        # might not have an underlying
        if self.underlying is None:
            return self.typ.as_features_cls() is not None
        else:
            return self.underlying.is_has_one

    @property
    def is_proto(self):
        if self.underlying is None:
            return self.typ.as_proto() is not None
        else:
            return self.underlying.is_proto

    @property
    def is_has_many(self):
        if self.underlying is None:
            return self.typ.as_dataframe() is not None
        else:
            return self.underlying.is_has_many

    @property
    def is_has_many_subfeature(self) -> bool:
        if self._is_has_many_subfeature is None:
            self.path = self._path
        assert self._is_has_many_subfeature is not None
        return self._is_has_many_subfeature

    @property
    def is_scalar(self):
        return not self.is_has_many and not self.is_has_one and not self.is_feature_time

    @property
    def is_windowed(self):
        """Whether the feature is a "fake" feature that has underlying windowed pseudofeatures.
        This feature fqn is not associated with any data in the online or offline stores, because
        it represents multiple windowed features."""
        return self.is_scalar and len(self.window_durations) > 0

    @property
    def is_windowed_pseudofeature(self):
        """Whether the feature is an underlying windowed pseudofeature,
        representing a particular windowed bucket. This feature is like
        any other scalar feature, and has data associated in the offline
        and online stores."""
        return self.window_duration is not None

    @property
    def window_stem(self) -> str:
        if not self.is_windowed_pseudofeature:
            return self.name
        return self.name[: -len(f"__{self.window_duration}__")]

    @property
    def window_alias_name(self) -> frozenset[str]:
        """Forgive us our trespasses, as we forgive those who trespass against us."""
        if not self.is_windowed_pseudofeature:
            return frozenset()

        suffix_len = len(f"__{self.window_duration}__")
        window_alias_formats = ["{stem}_{timerep}", "{stem}__{timerep}__"]  # w_1d_1h_1m_1s  # w__1d_1h_1m_1s__
        bucketed_time_groups = []

        stem = self.name[:-suffix_len]
        b = self.window_duration
        assert b is not None
        days = b // 86400
        days_as_seconds = days * 86400
        hours = (b - days_as_seconds) // 3600
        hours_as_seconds = hours * 3600
        minutes = (b - days_as_seconds - hours_as_seconds) // 60
        minutes_as_seconds = minutes * 60
        seconds = b - days_as_seconds - hours_as_seconds - minutes_as_seconds

        if (b % 3600) == 0:  # if the window is expressible in hours
            window_as_hours = b // 3600
            bucketed_time_groups.append(f"{window_as_hours}h")

        bucketed_time_groups.append(
            "".join(
                [
                    f"{count}{unit}"
                    for count, unit in (
                        (days, "d"),
                        (hours, "h"),
                        (minutes, "m"),
                        (seconds, "s"),
                    )
                    if count > 0
                ]
            )
        )

        return frozenset(
            {
                form.format(stem=stem, timerep=bucketed_time)
                for form in window_alias_formats
                for bucketed_time in bucketed_time_groups
            }
        )

    @property
    def window_buckets(self) -> Optional[Set[int]]:
        if self.is_windowed:
            return set(self.window_durations)
        return None

    @property
    def has_resolved_join(self) -> bool:
        return self._join is not None

    @property
    def _is_scalar(self) -> bool:
        return not len(self.path) > 0

    @property
    def join(self) -> Optional[Filter]:
        # Need to manually check the pseudofeatures because they
        # do not have a features class
        if self.underlying is not None:
            return self.underlying.join
        if self.is_pseudofeature:
            return None

        if self._join is not None:
            # Join was explicitly specified
            if not callable(self._join):
                return self._join
            self._join = self._validate_join()
            return self._join

        # The join was NOT specified on this feature.
        # It's possible it was specified with a type that points to another feature class.
        foreign_features_cls = self.typ.as_features_cls()
        if foreign_features_cls is None:
            dataframe_cls = self.typ.as_dataframe()
            if dataframe_cls is not None:
                foreign_features_cls = dataframe_cls.references_feature_set
        if foreign_features_cls is None:
            # Not a has-one or a has-many
            return None
        # Attempt to extract the join condition from the foreign feature
        assert self.features_cls is not None
        joins = JoinCatalogue()

        # Iterate through foreign feature class and find the join pointing to our feature.
        for f in foreign_features_cls.features:
            sub_features_cls = f.typ.as_features_cls()
            if sub_features_cls is None:
                sub_df_cls = f.typ.as_dataframe()
                if sub_df_cls is not None:
                    sub_features_cls = sub_df_cls.references_feature_set
            if sub_features_cls is not None and sub_features_cls is self.features_cls and f.has_resolved_join:
                # If there is another has-one on this features set that we already figured out, then use the same join key
                assert f.join is not None
                assert f.name is not None
                join = f.join() if callable(f.join) else f.join
                if join.operation == "==":
                    # If the join is a nearest neighbor, then implied reverse lookups do not apply
                    joins.add_join(join, f.fqn)

            # Supports direct has-ones/has-manys, where the type is the foreign feature to join with
            sub_feature = f.typ.as_feature()
            if sub_feature is not None and sub_feature.namespace == self.namespace:
                match = False
                assert sub_feature.features_cls is not None
                for feat in sub_feature.features_cls.features:
                    if feat.typ.as_features_cls() == f.features_cls:
                        match = True
                        break
                    feat_df = feat.typ.as_dataframe()
                    if feat_df is not None:
                        if feat_df.references_feature_set == f.features_cls:
                            match = True
                            break
                if match:
                    joins.add_join(Filter(lhs=f, operation="==", rhs=sub_feature), f.fqn)
        # The direct has-one/has-many join can also be found in the current namespace
        for f in self.features_cls.features:
            sub_feature = f.typ.as_feature()
            if sub_feature is not None and sub_feature.namespace == foreign_features_cls.namespace:
                joins.add_join(Filter(lhs=f, operation="==", rhs=sub_feature), f.fqn)

        num_joins = joins.num_joins()
        if num_joins == 0:
            # It's a nested feature, or no join is defined
            return None
        if num_joins > 1:
            self.lsp_error_builder.add_diagnostic(
                message=(
                    f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                    f"has an incorrectly-configured join function. "
                    f"There are multiple joins to '{foreign_features_cls.__name__}' on features "
                    f"{joins.invalid_join_string()}. "
                    f"Chalk is unable to determine which join function to use."
                ),
                label="invalid join",
                range=self.lsp_error_builder.property_value_range(self.attribute_name)
                or self.lsp_error_builder.property_range(self.attribute_name),
                code="38",
                raise_error=ValueError,
            )
        join = joins.only_valid_join()
        if callable(join):
            join = join()

        join = self._validate_filter(filter=join)
        self._join = join
        return join

    @property
    def foreign_join_key(self) -> Optional[Feature]:
        j = self.join
        if j is None:
            return None

        if j.lhs is not None and j.rhs is not None and isinstance(j.lhs, Feature) and isinstance(j.rhs, Feature):
            if j.lhs.namespace != self.namespace:
                return j.lhs
            return j.rhs
        return None

    @property
    def joined_class(self) -> Optional[Type[Features]]:
        joined_classes: OrderedSet[Optional[Type[Features]]] = OrderedSet()

        def _joined_class(join: Filter):
            if join.lhs is None or join.rhs is None:
                joined_classes.add(None)
            elif isinstance(join.lhs, Feature) and isinstance(join.rhs, Feature):
                if join.lhs.namespace != self.namespace:
                    joined_classes.add(join.lhs.features_cls)
                else:
                    joined_classes.add(join.rhs.features_cls)
            elif isinstance(join.lhs, Filter) and isinstance(join.rhs, Filter):
                _joined_class(join.lhs)
                _joined_class(join.rhs)
            return OrderedSet([None])

        j = self.join
        if j is None:
            return None
        _joined_class(j)
        if None in joined_classes:
            return None
        return get_unique_item(joined_classes)

    def as_last(self) -> Feature:
        last_name = f"__chalklast__{self.name}"
        last_feature = None
        assert self.features_cls is not None
        for f in self.features_cls.features:
            if f.name == last_name:
                last_feature = f
                break

        if not self.is_scalar:
            raise TypeError(
                f"Last[...] can only be used with scalar features, and '{self.root_fqn}' is not a scalar feature."
            )

        if last_feature is None:
            last_feature = Feature(
                name=last_name,
                attribute_name=last_name,
                namespace=self.namespace,
                features_cls=self.features_cls,
                typ=self.typ,
                version=self.version and self.version.maximum,
                default_version=(self.version and self.version.default) or 1,
                primary=False,
                etl_offline_to_online=False,
                default=None,
                max_staleness=CHALK_MAX_TIMEDELTA,
                encoder=self._encoder,  # pyright: ignore[reportArgumentType]
                decoder=self._decoder,
                pyarrow_dtype=self._pyarrow_dtype,
                tags=self.tags,
                join=None,
                is_feature_time=False,
                is_autogenerated=True,
                no_display=True,
                offline_ttl=self.offline_ttl,
                last_for=self,
            )
            self.features_cls.features.append(last_feature)
            setattr(self.features_cls, last_name, FeatureWrapper(last_feature))

        if len(self.path) == 0:
            return last_feature

        last_copy = copy.copy(last_feature)
        last_copy.path = (
            *self.path[:-1],
            HasOnePathObj(
                parent=self.path[-1].parent,
                child=last_feature,
                parent_to_child_attribute_name=last_copy.name,
            ),
        )
        return last_copy

    def copy_with_path(self, child: Feature) -> Feature:
        child_copy = copy.copy(child)
        assert child.attribute_name is not None
        child_copy.path = tuple(
            (
                *self.path,
                HasOnePathObj(
                    parent=self,
                    child=child,
                    parent_to_child_attribute_name=child.attribute_name,
                ),
            )
        )
        child_copy.underlying = child if child.underlying is None else child.underlying
        return child_copy

    @property
    def primary_feature(self) -> Optional[Feature]:
        if self._primary_feature is not None:
            return self._primary_feature
        if self.features_cls is None:
            return None
        self._primary_feature = self.features_cls.__chalk_primary__
        return self._primary_feature

    def for_version(self, version: int) -> Feature:
        if self.version is None:
            assert self.features_cls is not None
            raise ValueError(
                (
                    f"Cannot request version {version} of feature '{self.root_fqn}', because this feature "
                    "doesn't have a version set at definition. To set a version, write \n"
                    f"""    @features
    class {self.features_cls.__name__}:
        {self.attribute_name}: ... = feature(version={version})
        ...
"""
                )
            )

        if version not in self.version.reference:
            assert self.features_cls is not None
            raise ValueError(
                (
                    f"Cannot request version {version} of feature '{re.sub('@.*', '', self.root_fqn)}', because this feature "
                    f"has a maximum version of {self.version.maximum} < {version}. "
                    f"To add versions, write \n"
                    f"""    @features
    class {self.features_cls.__name__}:
   -    {self.attribute_name}: ... = feature(version={self.version.maximum})
   +    {self.attribute_name}: ... = feature(version={version})
        ...
"""
                )
            )

        versioned_feature = self.version.reference[version]
        if len(self.path) == 0:
            return versioned_feature

        # We have a path
        copied_versioned_feature = copy.copy(versioned_feature)
        assert versioned_feature.version is not None
        copied_versioned_feature.version = VersionInfo(
            maximum=versioned_feature.version.maximum,
            default=versioned_feature.version.default,
            reference=versioned_feature.version.reference,
            version=version,
        )
        copied_versioned_feature.path = tuple(
            (
                *self.path[:-1],
                HasOnePathObj(
                    parent=self.path[-1].parent,
                    child=copied_versioned_feature,
                    parent_to_child_attribute_name=copied_versioned_feature.attribute_name,
                ),
            )
        )
        return copied_versioned_feature

    def _validate_join(self) -> Filter:
        assert callable(self._join)
        try:
            join = self._join()
        except ClauseJoinWithAndException:
            assert self.features_cls is not None
            self.lsp_error_builder.add_diagnostic(
                message=(
                    f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                    f"has a join function that is incorrectly configured. "
                    f"Joins with multiple clauses must use '&' instead of 'and', e.g. `(a.id1 == b.id1) & (a.id2 == b.id2)`. "
                    f" (Note that you must surround your clauses with parenthesis due to operator precedence rules.) "
                    f"Joins with multiple clauses are only supported on has-one features."
                ),
                label="invalid join",
                range=self.lsp_error_builder.property_value_range(self.attribute_name)
                or self.lsp_error_builder.property_range(self.attribute_name),
                code="32",
                raise_error=TypeError,
            )
        except Exception:
            assert self.features_cls is not None
            self.lsp_error_builder.add_diagnostic(
                message=(
                    f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                    f"has a join function that is incorrectly configured. "
                    f"Ensure that the join is a lambda function that sets features from two feature classes as "
                    f"equal. For example, ' = has_one(lambda: "
                    f"{self.features_cls.__name__}.id == "
                    f"OtherClass.{to_snake_case(self.features_cls.__name__)}_id"
                    f")'"
                ),
                label="invalid join",
                range=self.lsp_error_builder.property_value_range(self.attribute_name)
                or self.lsp_error_builder.property_range(self.attribute_name),
                code="32",
                raise_error=TypeError,
            )

        if not self.is_has_many and not self.is_has_one:
            assert self.features_cls is not None
            self.lsp_error_builder.add_diagnostic(
                message=(
                    f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                    f"has a join filter ({join}) but its type annotation '{self.typ}' is not a feature class or DataFrame."
                ),
                label="invalid join",
                range=self.lsp_error_builder.property_value_range(self.attribute_name)
                or self.lsp_error_builder.property_range(self.attribute_name),
                code="37",
                raise_error=TypeError,
            )
        if self._join_type == "has_one":
            if self.is_has_many:
                assert self.features_cls is not None
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                        "is specified as 'has_one' but its type annotation is a 'DataFrame'. "
                        "Please remove the 'DataFrame' type if you'd like to define a 'has_one' relationship."
                    ),
                    label="invalid 'has_one' type",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="36",
                    raise_error=TypeError,
                )
        if self._join_type == "has_many":
            if self.is_has_one:
                assert self.features_cls is not None
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                        "is specified as 'has_many' but its type annotation is a feature class. "
                        "Please use the 'DataFrame' type around the feature class if you'd like to define a 'has_many' relationship."
                    ),
                    label="invalid 'has_many' type",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="36",
                    raise_error=TypeError,
                )

        join = self._validate_filter(filter=join)

        return join

    def _validate_filter(self, filter: Filter) -> Filter:
        seen_namespaces: OrderedSet[str] = OrderedSet()

        def _validate_filter_internal(filter: Filter) -> Filter:
            if not isinstance(
                filter, Filter
            ) or filter.operation not in (  # pyright: ignore[reportUnnecessaryIsInstance]
                "==",
                "and",
                "is_near_ip",
                "is_near_l2",
                "is_near_cos",
            ):
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"Join function for '{self.root_fqn}' is incorrectly configured. "
                        f"Ensure that the join is a lambda function that sets features from two feature classes as equal."
                    ),
                    label="invalid join",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="40",
                    raise_error=TypeError,
                )
            if isinstance(filter.lhs, Filter) and isinstance(filter.lhs, Filter) and filter.operation == "and":  # pyright: ignore[reportUnnecessaryIsInstance]
                if not self.is_has_one and not self.is_has_many:
                    assert self.features_cls is not None
                    my_primary_name = (
                        self.features_cls.__chalk_primary__.name
                        if self.features_cls.__chalk_primary__ is not None
                        else "id"
                    )
                    self.lsp_error_builder.add_diagnostic(
                        message=(
                            f"The attribute '{self.features_cls.__name__}.{self.attribute_name}' "
                            f"has a join function that is incorrectly configured. "
                            f"Ensure that the join is a lambda function that sets features from two feature classes as "
                            f"equal. For example, ' = has_one(lambda: "
                            f"{self.features_cls.__name__}.{my_primary_name} == "
                            f"OtherClass.{to_snake_case(self.features_cls.__name__)}_{my_primary_name}"
                            f")'"
                        ),
                        label="invalid join",
                        range=self.lsp_error_builder.property_value_range(self.attribute_name)
                        or self.lsp_error_builder.property_range(self.attribute_name),
                        code="32",
                        raise_error=TypeError,
                    )
                return Filter(_validate_filter_internal(filter.lhs), "and", _validate_filter_internal(filter.rhs))
            if not isinstance(filter.lhs, Feature):
                if isinstance(filter.lhs, str):
                    try:
                        filter.lhs = Feature.from_root_fqn(filter.lhs)
                    except FeatureNotFoundException:
                        self.lsp_error_builder.add_diagnostic(
                            message=(
                                f"Join function for '{self.root_fqn}' is incorrectly configured. Left hand side {filter.lhs} does not refer to a feature. "
                                f"Ensure that the join is a lambda function that sets features from two feature classes as equal."
                            ),
                            label="invalid join",
                            range=self.lsp_error_builder.property_value_range(self.attribute_name)
                            or self.lsp_error_builder.property_range(self.attribute_name),
                            code="40",
                            raise_error=TypeError,
                        )
                else:
                    self.lsp_error_builder.add_diagnostic(
                        message=(
                            f"Join function for '{self.root_fqn}' is incorrectly configured. Left hand side {filter.lhs} is not a feature. "
                            f"Ensure that the join is a lambda function that sets features from two feature classes as equal."
                        ),
                        label="invalid join",
                        range=self.lsp_error_builder.property_value_range(self.attribute_name)
                        or self.lsp_error_builder.property_range(self.attribute_name),
                        code="40",
                        raise_error=TypeError,
                    )

            if not isinstance(filter.rhs, Feature):
                if isinstance(filter.rhs, str):
                    try:
                        filter.rhs = Feature.from_root_fqn(filter.rhs)
                    except FeatureNotFoundException:
                        self.lsp_error_builder.add_diagnostic(
                            message=(
                                f"Join function for '{self.root_fqn}' is incorrectly configured. Left hand side {filter.rhs} does not refer to a feature. "
                                f"Ensure that the join is a lambda function that sets features from two feature classes as equal."
                            ),
                            label="invalid join",
                            range=self.lsp_error_builder.property_value_range(self.attribute_name)
                            or self.lsp_error_builder.property_range(self.attribute_name),
                            code="40",
                            raise_error=TypeError,
                        )
                else:
                    self.lsp_error_builder.add_diagnostic(
                        message=(
                            f"Join function for '{self.root_fqn}' is incorrectly configured. Left hand side {filter.rhs} is not a feature. "
                            f"Ensure that the join is a lambda function that sets features from two feature classes as equal."
                        ),
                        label="invalid join",
                        range=self.lsp_error_builder.property_value_range(self.attribute_name)
                        or self.lsp_error_builder.property_range(self.attribute_name),
                        code="40",
                        raise_error=TypeError,
                    )

            if filter.lhs.converter.pyarrow_dtype != filter.rhs.converter.pyarrow_dtype:
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"Join function for '{self.root_fqn}' is incorrectly configured. "
                        f"Ensure that both sides of the join are the same type. "
                        f"'{filter.lhs.root_fqn}' is of type {filter.lhs.typ}, and "
                        f"'{filter.rhs.root_fqn}' is of type {filter.rhs.typ}. "
                    ),
                    label="invalid join",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="42",
                    raise_error=TypeError,
                )
            seen_namespaces.update((filter.lhs.root_namespace, filter.rhs.root_namespace))
            if len(seen_namespaces) > 2:
                seen_namespaces.remove(self.namespace)
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"Join function for '{self.root_fqn}' is incorrectly configured. "
                        f"The feature '{self.fqn}' joins multiple foreign namespaces {tuple(seen_namespaces)}. "
                        "A multi-item join can only reference one foreign namespace. "
                        "Ensure that the join is a lambda function that sets features from two feature classes as equal."
                    ),
                    label="invalid join",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="43",
                    raise_error=TypeError,
                )
            namespace_conditions = (
                filter.lhs.root_namespace == self.namespace,
                filter.rhs.root_namespace == self.namespace,
            )
            features_are_simple = filter.lhs.is_scalar and filter.rhs.is_scalar
            if sum(namespace_conditions) != 1 or not features_are_simple:
                self.lsp_error_builder.add_diagnostic(
                    message=(
                        f"Join function for '{self.root_fqn}' is incorrectly configured. "
                        f"The feature '{self.fqn}' joins '{filter.lhs.root_fqn}' and '{filter.rhs.root_fqn}'. "
                        "Exactly one of the features in the join must be of the same root namespace as the has-one feature. "
                        "Ensure that the join is a lambda function that sets features from two feature classes as equal."
                    ),
                    label="invalid join",
                    range=self.lsp_error_builder.property_value_range(self.attribute_name)
                    or self.lsp_error_builder.property_range(self.attribute_name),
                    code="43",
                    raise_error=TypeError,
                )

            if filter.operation in ("is_near_ip", "is_near_l2", "is_near_cos"):
                # Synthesize a distance pseudo-feature on the foreign feature set
                assert isinstance(filter.lhs, Feature)
                assert isinstance(filter.rhs, Feature)
                local_feature = filter.lhs if filter.lhs.namespace == self.namespace else filter.rhs
                foreign_feature = filter.lhs if filter.lhs.namespace != self.namespace else filter.rhs
                if local_feature == foreign_feature:
                    self.lsp_error_builder.add_diagnostic(
                        message=(
                            f"Join function for '{self.root_fqn}' is incorrectly configured. "
                            f"The join condition must join two distinct feature classes, but this join "
                            f"references only {local_feature}."
                        ),
                        label="invalid join",
                        range=self.lsp_error_builder.property_value_range(self.attribute_name)
                        or self.lsp_error_builder.property_range(self.attribute_name),
                        code="44",
                        raise_error=TypeError,
                    )

                key = get_distance_feature_name(
                    local_namespace=self.namespace,
                    local_name=local_feature.name,
                    local_hm_name=self.name,
                    op=filter.operation,
                    foreign_name=foreign_feature.name,
                )
                foreign_ns = filter.lhs.namespace if filter.lhs.namespace != self.namespace else filter.rhs.namespace
                foreign_feature_set = FeatureSetBase.registry[foreign_ns]
                f = Feature(
                    namespace=foreign_ns,
                    name=key,
                    attribute_name=key,
                    features_cls=foreign_feature_set,
                    typ=ParsedAnnotation(underlying=float),
                    no_display=True,
                    is_autogenerated=True,
                    max_staleness=None,
                    version=self.version and self.version.maximum,
                    default_version=(self.version and self.version.default) or 1,
                    primary=False,
                    etl_offline_to_online=False,
                    join=None,
                    is_feature_time=False,
                    offline_ttl=timedelta(0),
                    is_distance_pseudofeature=True,
                )
                foreign_feature_set.features.append(f)
                wrapped_feature = FeatureWrapper(f)
                setattr(foreign_feature_set, f.attribute_name, wrapped_feature)
            return filter

        return _validate_filter_internal(filter)

    def __getstate__(self):
        """
        FeatureConverter is sometimes not serializable, so don't include it when (un)pickling
        """
        return {
            slot: None if slot == "_converter" else getattr(self, slot)
            for slot in self.__slots__
            if hasattr(self, slot)
        }

    def __setstate__(self, state: Dict[str, Any]):
        for k, v in state.items():
            setattr(self, k, v)

    def __sub__(self, other: Any):
        from chalk.features.pseudofeatures import Now

        if self.namespace != Now.namespace or self.name != Now.name:
            raise TypeError(f"Cannot subtract {other} from {self}")

        if isinstance(other, timedelta):
            return TimeDelta(
                days_ago=other.days,
                seconds_ago=other.seconds,
                microseconds_ago=other.microseconds,
            )

        raise TypeError(f"Cannot subtract {other} from {self}")


DUMMY_FEATURE = Feature(
    name="__undefined__",
    namespace="__chalk__",
    typ=str,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)


def feature(
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Tags] = None,
    name: Optional[str] = None,
    version: Optional[int] = None,
    default_version: int = 1,
    primary: Optional[bool] = None,
    max_staleness: Optional[Union[ellipsis, Duration]] = ...,
    cache_nulls: Union[bool, Literal["evict_nulls"]] = True,
    cache_defaults: Union[bool, Literal["evict_defaults"]] = True,
    etl_offline_to_online: Optional[bool] = None,
    encoder: Optional[TEncoder[_TPrim, _TRich]] = None,
    decoder: Optional[TDecoder[_TPrim, _TRich]] = None,
    min: Optional[_TRich] = None,
    max: Optional[_TRich] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    strict: bool = False,
    validations: Optional[List[Validation]] = None,
    dtype: Optional[pa.DataType] = None,
    default: Union[_TRich, ellipsis] = ...,
    underscore: Optional[Underscore] = None,  # Deprecated. Prefer `expression`.
    expression: Optional[Underscore] = None,
    offline_ttl: Optional[Union[ellipsis, Duration]] = ...,
    deprecated: bool = False,
    store_online: bool = True,
    store_offline: bool = True,
) -> _TRich:
    """Add metadata and configuration to a feature.

    Parameters
    ----------
    owner
        You may also specify which person or group is responsible for a feature.
        The owner tag will be available in Chalk's web portal.
        Alerts that do not otherwise have an owner will be assigned
        to the owner of the monitored feature.
        Read more at https://docs.chalk.ai/docs/feature-discovery#owner

        >>> from chalk.features import features, feature
        >>> from datetime import date
        >>> @features
        ... class User:
        ...     id: str
        ...     # :owner: user-team@company.com
        ...     name: str
        ...     dob: date = feature(owner="user-team@company.com")
    tags
        Add metadata to a feature for use in filtering, aggregations,
        and visualizations. For example, you can use tags to assign
        features to a team and find all features for a given team.
        Read more at https://docs.chalk.ai/docs/feature-discovery#tags

        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     # :tags: pii
        ...     name: str
        ...     dob: date = feature(tags=["pii"])
    default
        The default value of the feature if it otherwise can't be computed.
        If you don't need to specify other metadata, you can also assign a default
        in the same way you would assign a default to a `dataclass`:

        >>> from chalk.features import features
        >>> @features
        ... class User:
        ...     num_purchases: int = 0
    expression
        An underscore expression for defining the feature. Typically,
        this value is assigned directly to the feature without needing
        to use the `feature(...)` function. However, if you want to define
        other properties, like a `default` or `max_staleness`, you'll
        want to use the `expression` keyword argument.
        >>> from chalk.features import features
        >>> from chalk import _
        >>> @features
        ... class Receipt:
        ...     subtotal: int
        ...     tax: int = 0  # Default value, without other metadata
        ...     total: int = feature(expression=_.subtotal + _.tax, default=0)

        See more at https://docs.chalk.ai/docs/expression
    dtype
        The backing `pyarrow.DataType` for the feature. This parameter can
        be used to control the storage format of data. For example, if you
        have a lot of data that could be represented as smaller data types,
        you can use this parameter to save space.

        >>> import pyarrow as pa
        >>> @features
        ... class WatchEvent:
        ...     id: str
        ...     duration_hours: float = feature(dtype=pa.float8())
    max_staleness
        When a feature is expensive or slow to compute, you may wish to cache its value.
        Chalk uses the terminology "maximum staleness" to describe how recently a feature
        value needs to have been computed to be returned without re-running a resolver.
        Read more at https://docs.chalk.ai/docs/feature-caching
    etl_offline_to_online
        When `True`, Chalk copies this feature into the online environment
        when it is computed in offline resolvers.
        Read more at https://docs.chalk.ai/docs/reverse-etl
    version
        The maximum version for a feature. Versioned features can be
        referred to with the `@` operator:

        >>> @features
        ... class User:
        ...     id: str
        ...     score: int = feature(version=2)
        >>> str(User.score @ 2)
        "user.score@2"

        See more at https://docs.chalk.ai/docs/feature-versions
    default_version
        The default version for a feature. When you reference a
        versioned feature without the `@` operator, you reference
        the `default_version`. Set to `1` by default.

        >>> @features
        ... class User:
        ...     id: str
        ...     score: int = feature(version=2, default_version=2)
        >>> str(User.score)
        "user.score"

        See more at https://docs.chalk.ai/docs/feature-versions#default-versions
    min
        If specified, when this feature is computed, Chalk will check that `x >= min`.
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     fico_score: int = feature(min=300, max=850)
    max
        If specified, when this feature is computed, Chalk will check that `x <= max`.
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     fico_score: int = feature(min=300, max=850)
    min_length
        If specified, when this feature is computed, Chalk will check that `len(x) >= min_length`.
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     name: str = feature(min_length=1)
    max_length
        If specified, when this feature is computed, Chalk will check that `len(x) <= max_length`.
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     name: str = feature(min_length=1000)
    strict
        If `True`, if this feature does not meet the validation criteria, Chalk will not persist
        the feature value and will treat it as failed.
    validations
        A list of validations to apply to this feature. Generally, `max`, `min`, `max_length`,
        and `min_length` are more convenient, but the parameter `strict` applies to all
        of those parameters. Use this parameter if you want to mix strict and non-strict validations.
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
    store_online
        By default `True`. Setting to `False` will prevent this feature from being written to the online store.
    store_offline
        By default `True`. Setting to `False` will prevent this feature from being written to the offline store.
    deprecated
        If `True`, this feature is considered deprecated, which impacts the dashboard, alerts,
        and warnings.
        >>> from chalk.features import features, feature
        >>> @features
        ... class User:
        ...     id: str
        ...     name: str = feature(deprecated=True)

    Other Parameters
    ----------------
    name
        The name for the feature. By default, the name of a feature is
        the name of the attribute on the class, prefixed with
        the camel-cased name of the class. Note that if you provide an
        explicit name, the namespace, determined by the feature class,
        will still be prepended. See `features` for more details.
    primary
        If `True`, this feature is considered a primary key for the
        feature class. Note that a feature class cannot have more than
        one primary key.

        Typically, you will not need to use this parameter. Features named
        `id` are declared primary keys by default.

        If you have primary key feature with a name other than `id`, you can
        use this parameter, or the class `Primary` to indicate the primary key.
        For example:

        >>> @features
        ... class User:
        ...     uid: Primary[int]

        >>> @features
        ... class User:
        ...     uid: int = feature(primary=True)
    description
        Descriptions are typically provided as comments preceding
        the feature definition. For example, you can document a
        `fraud_score` feature with information about the values
        as follows:

        >>> @features
        ... class User:
        ...     # 0 to 100 score indicating an identity match.
        ...     fraud_score: float

        You can also specify the description directly with this parameter.
        Read more at https://docs.chalk.ai/docs/feature-discovery#description
    offline_ttl
        Sets a maximum age for values eligible to be retrieved from the offline store,
        defined in relation to the query's current point-in-time.
    encoder
    decoder

    Returns
    -------
    _TRich
        The type of the input feature, given by `_TRich`.

    Examples
    --------
    >>> from chalk.features import Primary, features, feature
    >>> @features
    ... class User:
    ...     uid: Primary[int]
    ...     # Uses a default value of 0 when one cannot be computed.
    ...     num_purchases: int = 0
    ...     # Description of the name feature.
    ...     # :owner: fraud@company.com
    ...     # :tags: fraud, credit
    ...     name: str = feature(
    ...         max_staleness="10m",
    ...         etl_offline_to_online=True
    ...     )
    ...     score: int = feature(
    ...         version=2, default_version=2
    ...     )
    """
    if cache_nulls == "evict_nulls":
        if cache_defaults == "evict_defaults":
            cache_strategy = CacheStrategy.EVICT_NULLS_AND_DEFAULTS
        elif cache_defaults == False:
            raise ValueError(
                'Cannot evict nulls and not cache defaults. Did you mean to set `cache_nulls=False` or `cache_defaults="evict_defaults"`?'
            )
        elif cache_defaults == True:
            cache_strategy = CacheStrategy.EVICT_NULLS
        else:
            raise ValueError(
                f'Expected value of cache_defaults to be True, False, or "evict_defaults". Received {cache_defaults}'
            )
    elif cache_nulls is False:
        if cache_defaults == "evict_defaults":
            raise ValueError(
                'Cannot evict defaults and not cache nulls. Did you mean to set `cache_defaults=False` or `cache_nulls="evict_nulls"`?'
            )
        elif cache_defaults == False:
            cache_strategy = CacheStrategy.NO_NULLS_OR_DEFAULTS
        elif cache_defaults == True:
            cache_strategy = CacheStrategy.NO_NULLS
        else:
            raise ValueError(
                f'Expected value of cache_defaults to be True, False, or "evict_defaults". Received {cache_defaults}'
            )
    elif cache_nulls is True:
        if cache_defaults == "evict_defaults":
            cache_strategy = CacheStrategy.EVICT_DEFAULTS
        elif cache_defaults == False:
            cache_strategy = CacheStrategy.NO_DEFAULTS
        elif cache_defaults == True:
            cache_strategy = CacheStrategy.ALL
        else:
            raise ValueError(
                f'Expected value of cache_defaults to be True, False, or "evict_defaults". Received {cache_defaults}'
            )
    else:
        raise ValueError(f'Expected value of cache_nulls to be True, False, or "evict_nulls". Received {cache_nulls}')

    return cast(
        _TRich,
        Feature(
            name=name,
            version=version,
            default_version=default_version,
            owner=owner,
            tags=None if tags is None else list(ensure_tuple(tags)),
            description=description,
            primary=primary,
            max_staleness=max_staleness,
            cache_strategy=cache_strategy,
            etl_offline_to_online=etl_offline_to_online,
            encoder=encoder,
            decoder=decoder,
            pyarrow_dtype=dtype,
            validations=(
                FeatureValidation(
                    min=min,
                    max=max,
                    min_length=min_length,
                    max_length=max_length,
                    contains=None,
                    strict=strict,
                )
                if (min is not None or max is not None or min_length is not None or max_length is not None)
                else None
            ),
            all_validations=(
                None
                if validations is None
                else [
                    FeatureValidation(
                        min=v.min,
                        max=v.max,
                        min_length=v.min_length,
                        max_length=v.max_length,
                        contains=None,
                        strict=v.strict,
                    )
                    for v in validations
                ]
            ),
            default=default,
            underscore_expression=expression if expression is not None else underscore,
            offline_ttl=offline_ttl,
            is_deprecated=deprecated,
            store_online=store_online,
            store_offline=store_offline,
        ),
    )


def has_one(f: Callable[[], Any]) -> Any:
    """Specify a feature that represents a one-to-one relationship.

    This function allows you to explicitly specify a join condition between
    two `@features` classes. When there is only one way to join two classes,
    we recommend using the foreign-key definition instead of this `has_one`
    function. For example, if you have a `User` class and a `Card` class, and
    each user has one card, you can define the `Card` and `User` classes as
    follows:

    >>> @features
    ... class User
    ...     id: str
    >>> @features
    ... class Card
    ...     id: str
    ...     user_id: User.id
    ...     user: User

    However, if `User` has two cards (say, a primary and secondary),
    the foreign key syntax cannot be used to define the relationship,
    and you should use the `has_one` function.

    Read more at https://docs.chalk.ai/docs/has-one

    Parameters
    ----------
    f
        The join condition between `@feature` classes.
        This argument is callable to allow for forward
        references to members of this class and the joined
        class.

    Examples
    --------
    >>> from chalk.features import DataFrame, features
    >>> @features
    ... class Card
    ...     id: str
    ...     user_id: str
    ...     balance: float
    >>> @features
    ... class User
    ...     id: str
    ...     card: Card = has_one(
    ...         lambda: User.id == Card.user_id
    ...     )
    """
    return Feature(join=f, join_type="has_one")


def has_many(
    f: Callable[[], Any],
    max_staleness: Union[Duration, None, ellipsis] = ...,
) -> Any:
    """Specify a feature that represents a one-to-many relationship.

    Parameters
    ----------
    f
        The join condition between `@features` classes.
        This argument is callable to allow for forward
        references to members of this class and the joined
        class.
    max_staleness
        The maximum staleness of the joined feature. The items in the
        joined feature aggregate, storing the latest values of the joined
        feature for each primary key in the joined feature.

    Examples
    --------
    >>> from chalk.features import DataFrame, features
    >>> @features
    ... class Card
    ...     id: str
    ...     user_id: str
    ...     balance: float
    >>> @features
    ... class User
    ...     id: str
    ...     cards: DataFrame[Card] = has_many(
    ...         lambda: User.id == Card.user_id
    ...     )
    """
    return Feature(join=f, max_staleness=max_staleness, join_type="has_many")


__all__ = (
    "Feature",
    "feature",
    "has_one",
    "has_many",
    "CacheStrategy",
)
