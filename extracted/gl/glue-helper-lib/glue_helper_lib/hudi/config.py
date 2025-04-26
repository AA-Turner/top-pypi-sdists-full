import enum
import typing
from dataclasses import dataclass


class TableType(enum.Enum):
    COPY_ON_WRITE = "COPY_ON_WRITE"
    MERGE_ON_READ = "MERGE_ON_READ"


def get_table_type_opt_key_value(table_type: TableType):
    if table_type == TableType.COPY_ON_WRITE:
        return "COW_TABLE_TYPE_OPT_VAL"
    elif table_type == TableType.MERGE_ON_READ:
        return "MOR_TABLE_TYPE_OPT_VAL"


class IndexType(enum.Enum):
    BLOOM = "BLOOM"
    SIMPLE = "SIMPLE"
    GLOBAL_BLOOM = "GLOBAL_BLOOM"
    GLOBAL_SIMPLE = "GLOBAL_SIMPLE"


class KeyGeneratorNotKnownException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(
            (
                "This combination of arguments have not been experimented to see "
                "which key generator should be used. Experiment and update the "
                "relevant tests if in dev and acc this new combination can be make "
                "to work experimentally"
            ),
            *args,
        )


class KeyGenerator(enum.Enum):
    """The keygenerator class has to be specified based on the
    configuration of a table.
    The weird thing is that there is a NonpartitionedKeyGenerator class for
    when you dont wanna partition your data. However, the SimpleKeyGenerator just works
    for non-partitioned data. When mutliple columns are specified for the record key,
    the ComplexKeyGenerator has to be used. But this one apparently cannot handle
    empty (None) partitions.
    https://hudi.apache.org/blog/2021/02/13/hudi-key-generators/

    """

    SIMPLE = "SimpleKeyGenerator"
    COMPLEX = "ComplexKeyGenerator"
    TIMESTAMP = "TimestampBasedKeyGenerator"
    NONPARTITIONED = "NonpartitionedKeyGenerator"
    CUSTOM = "CustomKeyGenerator"


def get_keygenerator_class(
    n_record_key_columns: int,
    partitioning: bool,
    partitioned_on_datetime: bool,
):
    if n_record_key_columns == 1 and not partitioned_on_datetime:
        return KeyGenerator.COMPLEX
    elif n_record_key_columns > 1 and not partitioned_on_datetime:
        return KeyGenerator.COMPLEX
    elif partitioning and partitioned_on_datetime:
        return KeyGenerator.CUSTOM
    else:
        raise KeyGeneratorNotKnownException(
            "number of record key columns:",
            n_record_key_columns,
            "partitioning:",
            partitioning,
            "partitioned on datetime:",
            partitioned_on_datetime,
        )


def get_keygenerator_class_name(key_generator: KeyGenerator):
    return f"org.apache.hudi.keygen.{key_generator.value}"


@dataclass
class DatetimePartitioning:
    input_date_format: str = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
    timezone: str = "UTC"
    output_date_format: str = "yyyyMMdd"


def get_additional_options_for_datetime_keygen(
    datetime_partitioning: typing.Optional[DatetimePartitioning],
):
    # https://hudi.apache.org/blog/2021/02/13/hudi-key-generators/#timestampbasedkeygenerator
    if datetime_partitioning:
        return {
            "hoodie.deltastreamer.keygen.timebased.timestamp.type": "DATE_STRING",
            "hoodie.deltastreamer.keygen.timebased.input.dateformat": datetime_partitioning.input_date_format,
            "hoodie.deltastreamer.keygen.timebased.input.dateformat.list.delimiter.regex": "",  # noqa: E501
            "hoodie.deltastreamer.keygen.timebased.input.timezone": "",
            "hoodie.deltastreamer.keygen.timebased.output.dateformat": datetime_partitioning.output_date_format,  # noqa: E501
            "hoodie.deltastreamer.keygen.timebased.timezone": datetime_partitioning.timezone,
        }
    else:
        return {}


def parse_record_key_columns(columns: typing.List[str]):
    if not columns:
        raise ValueError("No columns set for record key")
    return ",".join(columns)


def get_index_type_option(index_type: IndexType):
    return {"hoodie.index.type": index_type.value}


def get_partitioning_options(
    partition_key_column_name: typing.Union[None, str],
    partitioned_on_datetime: bool,
    key_generator_class: KeyGenerator,
):
    if key_generator_class == KeyGenerator.CUSTOM:
        # https://hudi.apache.org/docs/0.12.1/key_generation#customkeygenerator
        partition_key_type = (
            "TIMESTAMP" if partitioned_on_datetime else "SIMPLE"
        )
        partition_field_value = (
            f"{partition_key_column_name}:{partition_key_type}"
        )
    else:
        partition_field_value = (
            partition_key_column_name if partition_key_column_name else ""
        )
    return {
        "hoodie.datasource.write.partitionpath.field": partition_field_value,
        "hoodie.datasource.hive_sync.assume_date_partitioning": "false",
        "hoodie.datasource.write.hive_style_partitioning": "true",
    }


MetaOptions = typing.TypedDict(
    "MetaOptions",
    {"className": str, "hoodie.datasource.write.keygenerator.class": str},
)

CatalogOptions = typing.TypedDict(
    "CatalogOptions",
    {
        "hoodie.table.name": str,
        "hoodie.datasource.hive_sync.table": str,
        "hoodie.datasource.hive_sync.database": str,
        "hoodie.datasource.hive_sync.enable": str,
        "hoodie.datasource.hive_sync.mode": str,
        "hoodie.datasource.hive_sync.use_jdbc": str,
        "hive_sync.support_timestamp": str,
        "path": str,
    },
)

UpsertOptions = typing.TypedDict(
    "UpsertOptions",
    {
        "hoodie.datasource.write.operation": str,
        "hoodie.datasource.write.table_type_opt_key": str,
        "hoodie.datasource.write.recordkey.field": str,
        "hoodie.datasource.write.precombine.field": str,
    },
)

hudi_option_keys = [
    # Meta
    "className",
    "hoodie.datasource.write.keygenerator.class",
    # cataloging
    "hoodie.table.name",
    "hoodie.datasource.hive_sync.table",
    "hoodie.datasource.hive_sync.database",
    "hoodie.datasource.hive_sync.enable",
    "hoodie.datasource.hive_sync.mode",
    "hoodie.datasource.hive_sync.use_jdbc",
    "hive_sync.support_timestamp",
    "path",
    # upsert
    "hoodie.datasource.write.operation",
    "hoodie.datasource.write.table_type_opt_key",
    "hoodie.datasource.write.recordkey.field",
    "hoodie.datasource.write.precombine.field",
    # partitioning
    "hoodie.datasource.write.partitionpath.field",
    "hoodie.datasource.hive_sync.assume_date_partitioning",
    "hoodie.datasource.write.hive_style_partitioning",
    # partitioning - timestamp
    "hoodie.deltastreamer.keygen.timebased.timestamp.type",
    "hoodie.deltastreamer.keygen.timebased.input.dateformat",
    "hoodie.deltastreamer.keygen.timebased.input.dateformat.list.delimiter.regex",  # noqa: E501
    "hoodie.deltastreamer.keygen.timebased.input.timezone",
    "hoodie.deltastreamer.keygen.timebased.output.dateformat",
    "hoodie.deltastreamer.keygen.timebased.timezone",
]

HudiOptionsDict = typing.TypedDict(
    "HudiOptions", {key: str for key in hudi_option_keys}  # type: ignore
)

fixed_hudi_options = {
    "className": "org.apache.hudi",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.hive_sync.enable": "true",
    "hoodie.datasource.hive_sync.use_jdbc": "false",
    "hoodie.datasource.hive_sync.mode": "hms",
    "hive_sync.support_timestamp": "true",
}


def get_hudi_options(
    database_name: str,
    table_name: str,
    table_type: TableType,
    datetime_partitioning: typing.Optional[DatetimePartitioning],
    index_type: IndexType,
    record_key_columns: typing.List[str],
    precombine_column_name: str,
    partition_key_column_name: typing.Optional[str],
    hudi_table_path: str,
):
    if not partition_key_column_name:
        partition_key_column_name = ""
    key_generator_class = get_keygenerator_class(
        len(record_key_columns),
        True if partition_key_column_name else False,
        True if datetime_partitioning else False,
    )
    options: typing.Dict[str, str] = {
        **fixed_hudi_options,
        "hoodie.table.name": table_name,
        "hoodie.datasource.write.table_type_opt_key": get_table_type_opt_key_value(
            table_type
        ),
        "hoodie.datasource.write.keygenerator.class": get_keygenerator_class_name(
            key_generator_class
        ),
        "hoodie.datasource.write.recordkey.field": parse_record_key_columns(
            record_key_columns
        ),
        "hoodie.datasource.write.precombine.field": precombine_column_name,
        "hoodie.datasource.hive_sync.enable": "true",
        "hoodie.datasource.hive_sync.database": database_name,
        "hoodie.datasource.hive_sync.table": table_name,
        "path": hudi_table_path,
        **get_index_type_option(index_type),
        **get_partitioning_options(
            partition_key_column_name,
            True if datetime_partitioning else False,
            key_generator_class,
        ),
        **get_additional_options_for_datetime_keygen(datetime_partitioning),
    }

    return options
