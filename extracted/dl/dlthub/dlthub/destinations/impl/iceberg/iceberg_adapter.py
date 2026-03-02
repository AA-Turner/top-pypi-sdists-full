from dataclasses import dataclass
from typing import Any, List, Dict, Union, Sequence, Optional, Callable
from pyiceberg.transforms import (
    Transform,
    IdentityTransform,
    YearTransform,
    MonthTransform,
    DayTransform,
    HourTransform,
    BucketTransform,
    TruncateTransform,
    S,
)
from pyiceberg.partitioning import PartitionSpec as IcebergPartitionSpec, PartitionField
from pyiceberg.schema import Schema as IcebergSchema
from pyiceberg.io.pyarrow import pyarrow_to_schema
from pyiceberg.table.name_mapping import NameMapping, MappedField

from dlt.common.libs.pyarrow import pyarrow as pa
from dlt.destinations.utils import get_resource_for_adapter
from dlt.extract import DltResource

PARTITION_HINT = "x-iceberg-partition"

_TRANSFORM_LOOKUP: Dict[str, Callable[[Optional[int]], Transform[S, Any]]] = {
    "identity": lambda _: IdentityTransform(),
    "year": lambda _: YearTransform(),
    "month": lambda _: MonthTransform(),
    "day": lambda _: DayTransform(),
    "hour": lambda _: HourTransform(),
    "bucket": lambda n: BucketTransform(n),
    "truncate": lambda w: TruncateTransform(w),
}


@dataclass(frozen=True)
class PartitionSpec:
    source_column: str
    transform: str = "identity"
    param_value: Optional[int] = None
    partition_field: Optional[str] = None

    def get_transform(self) -> Transform[S, Any]:
        """Get the PyIceberg Transform object for this partition.

        Returns:
            A PyIceberg Transform object

        Raises:
            ValueError: If the transform is not recognized
        """
        try:
            factory = _TRANSFORM_LOOKUP[self.transform]
        except KeyError as exc:
            raise ValueError(f"Unknown partition transformation type: {self.transform}") from exc
        return factory(self.param_value)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "transform": self.transform,
            "source_column": self.source_column,
        }
        if self.partition_field:
            d["partition_field"] = self.partition_field
        if self.param_value is not None:
            d["param_value"] = self.param_value
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PartitionSpec":
        return cls(
            source_column=d["source_column"],
            transform=d["transform"],
            param_value=d.get("param_value"),
            partition_field=d.get("partition_field"),
        )


class iceberg_partition:
    """Helper class with factory methods for creating partition specs."""

    @staticmethod
    def identity(column_name: str) -> PartitionSpec:
        return PartitionSpec(column_name, "identity")

    @staticmethod
    def year(column_name: str, partition_field_name: Optional[str] = None) -> PartitionSpec:
        return PartitionSpec(column_name, "year", partition_field=partition_field_name)

    @staticmethod
    def month(column_name: str, partition_field_name: Optional[str] = None) -> PartitionSpec:
        return PartitionSpec(column_name, "month", partition_field=partition_field_name)

    @staticmethod
    def day(column_name: str, partition_field_name: Optional[str] = None) -> PartitionSpec:
        return PartitionSpec(column_name, "day", partition_field=partition_field_name)

    @staticmethod
    def hour(column_name: str, partition_field_name: Optional[str] = None) -> PartitionSpec:
        return PartitionSpec(column_name, "hour", partition_field=partition_field_name)

    @staticmethod
    def bucket(
        num_buckets: int, column_name: str, partition_field_name: Optional[str] = None
    ) -> PartitionSpec:
        return PartitionSpec(
            source_column=column_name,
            transform="bucket",
            param_value=num_buckets,
            partition_field=partition_field_name,
        )

    @staticmethod
    def truncate(
        width: int, column_name: str, partition_field_name: Optional[str] = None
    ) -> PartitionSpec:
        return PartitionSpec(
            source_column=column_name,
            transform="truncate",
            param_value=width,
            partition_field=partition_field_name,
        )


def iceberg_adapter(
    data: Any,
    partition: Union[str, PartitionSpec, Sequence[Union[str, PartitionSpec]]] = None,
) -> DltResource:
    """Prepares data or a DltResource for loading into Apache Iceberg table.

    Takes raw data or an existing DltResource and configures it for Iceberg,
    primarily by defining partitioning strategies via the DltResource\'s hints.

    Args:
        data: The data to be transformed. This can be raw data (e.g., list of dicts)
            or an instance of `DltResource`. If raw data is provided, it will be
            encapsulated into a `DltResource` instance.
        partition: Defines how the Iceberg table should be partitioned.
            Must be provided. It accepts:
            - A single column name (string): Defaults to an identity transform.
            - A `PartitionSpec` object: Allows for detailed partition configuration,
              including various transformation types (year, month, day, hour, bucket, truncate).
              Use the `iceberg_partition` helper class to create these specs.
            - A sequence of the above: To define multiple partition columns.

    Returns:
        A `DltResource` instance configured with Iceberg-specific partitioning hints,
        ready for loading.

    Raises:
        ValueError: If `partition` is not specified or if an invalid
            partition transform is requested within a `PartitionSpec`.

    Examples:
        >>> data = [{"id": 1, "event_time": "2023-03-15T10:00:00Z", "category": "A"}]
        >>> resource = iceberg_adapter(
        ...     data,
        ...     partition=[
        ...         "category",  # Identity partition on category
        ...         iceberg_partition.year("event_time"),
        ...     ]
        ... )
        >>> # The resource's hints now contain the Iceberg partition specs:
        >>> # resource.compute_table_schema().get('x-iceberg-partition')
        >>> # [
        >>> #     {'transform': 'identity', 'source_column': 'event_time'},
        >>> #     {'transform': 'year', 'source_column': 'event_time'},
        >>> # ]
        >>> #
        >>> # Using an existing DltResource
        >>> @dlt.resource
        ... def my_data():
        ...     yield [{"value": "abc"}]
        >>> iceberg_adapter(my_data, partition="value")
    """
    resource = get_resource_for_adapter(data)
    additional_table_hints: Dict[str, Any] = {}

    if partition:
        if isinstance(partition, (str, PartitionSpec)):
            partition = [partition]

        specs: List[PartitionSpec] = []
        for item in partition:
            if isinstance(item, PartitionSpec):
                specs.append(item)
            else:
                # Item is the column name, use identity transform
                specs.append(iceberg_partition.identity(item))

        additional_table_hints[PARTITION_HINT] = [spec.to_dict() for spec in specs]

    if additional_table_hints:
        resource.apply_hints(additional_table_hints=additional_table_hints)
    else:
        raise ValueError("A value for `partition` must be specified.")

    return resource


def _default_field_name(spec: PartitionSpec) -> str:
    """
    Replicate Iceberg's automatic partition-field naming by delegating to the private
    _PartitionNameGenerator. Falls back to the user-supplied `partition_field` if present.
    """
    from pyiceberg.partitioning import _PartitionNameGenerator

    _NAME_GEN = _PartitionNameGenerator()

    if spec.partition_field:  # user-supplied `partition_field`
        return spec.partition_field

    col = spec.source_column
    t = spec.transform

    if t == "bucket":
        # bucket/ truncate need the numeric parameter
        return _NAME_GEN.bucket(0, col, 0, spec.param_value)
    if t == "truncate":
        return _NAME_GEN.truncate(0, col, 0, spec.param_value)

    # identity, year, month, day, hour – all have the same signature
    method = getattr(_NAME_GEN, t)

    return method(0, col, 0)  # type: ignore[no-any-return]


def build_iceberg_partition_spec(
    arrow_schema: pa.Schema,
    helper_specs: Sequence[PartitionSpec],
) -> tuple[IcebergPartitionSpec, IcebergSchema]:
    """
    Turn our helper HintPartitionSpec list into a single pyiceberg PartitionSpec.
    Returns the spec and the IcebergSchema derived from the Arrow schema.
    """
    # convert Arrow -> Iceberg schema
    name_mapping = NameMapping([
        MappedField(field_id=i + 1, names=[name])  # type: ignore[call-arg]
        for i, name in enumerate(arrow_schema.names)
    ])
    iceberg_schema: IcebergSchema = pyarrow_to_schema(arrow_schema, name_mapping)

    # build PartitionField objects, one per helper spec
    fields: list[PartitionField] = []
    for spec in helper_specs:
        iceberg_field = iceberg_schema.find_field(spec.source_column)

        fields.append(
            PartitionField(
                field_id=iceberg_field.field_id,
                source_id=iceberg_field.field_id,
                transform=spec.get_transform(),
                name=_default_field_name(spec),
            )
        )

    # pack everything into a single PartitionSpec
    return IcebergPartitionSpec(*fields), iceberg_schema
