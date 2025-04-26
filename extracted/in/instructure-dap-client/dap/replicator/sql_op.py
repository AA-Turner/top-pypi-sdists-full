import abc
import dataclasses
import datetime
import types
import typing
from typing import Dict, Optional

from pysqlsync.base import BaseContext, Explorer
from pysqlsync.model.entity_types import make_entity
from pysqlsync.model.properties import get_field_properties
from strong_typing.classdef import (
    SchemaFlatteningOptions,
    flatten_schema,
    schema_to_type,
)
from strong_typing.core import JsonType, Schema
from strong_typing.inspection import DataclassInstance, dataclass_fields

from dap.api import DAPSession, logger
from dap.dap_types import VersionedSchema
from dap.replicator import canvas, canvas_logs, catalog, meta_schema

DEFAULT_DOWNLOAD_DIR: str = "instructure_dap_temp"
UTC_TIMEZONE = datetime.timezone.utc
RETRY: int = 3


@dataclasses.dataclass
class _TabularLabelMapping:
    labels_to_types: Dict[str, type]
    labels_to_fields: Dict[str, str]


str_to_namespace = {
    "canvas": canvas,
    "catalog": catalog,
    "canvas_logs": canvas_logs,
    "meta_schema": meta_schema,
}


def get_module_for_namespace(namespace: str) -> types.ModuleType:
    if namespace not in str_to_namespace:
        raise ValueError(f"namespace {namespace} not supported")
    return str_to_namespace[namespace]


class SqlOp(abc.ABC):
    conn: BaseContext
    namespace: str
    table_name: str
    explorer: Explorer
    session: Optional[DAPSession]
    namespace_module: types.ModuleType

    def __init__(
        self,
        conn: BaseContext,
        namespace: str,
        table_name: str,
        explorer: Explorer,
        session: Optional[DAPSession] = None,
    ) -> None:
        self.conn = conn
        self.namespace = namespace
        self.table_name = table_name
        self.explorer = explorer
        self.session = session
        self.namespace_module = get_module_for_namespace(namespace)

    @abc.abstractmethod
    async def run(self) -> None:
        ...

    @staticmethod
    def get_tabular_mapping(
        entity_type: type[DataclassInstance], mapping: _TabularLabelMapping
    ) -> _TabularLabelMapping:
        for field in dataclass_fields(entity_type):
            props = get_field_properties(field.type)
            if props.is_primary:
                qual_name = f"key.{field.name}"
            else:
                qual_name = f"value.{field.name}"
            mapping.labels_to_types[qual_name] = props.tsv_type
            mapping.labels_to_fields[qual_name] = field.name
        return mapping


async def fetch_schema_for_table(
    session: DAPSession, namespace: str, table_name: str
) -> tuple:
    """
    Fetches the schema for a table.
    :param session: The DAP session.
    :param namespace: The namespace.
    :param table_name: The table name.
    :return:
    """

    ns_module = get_module_for_namespace(namespace)

    logger.debug(f"fetching schema for table: {namespace}.{table_name}")
    versioned_schema: VersionedSchema = await session.get_table_schema(
        namespace, table_name
    )
    schema: Dict[str, JsonType] = versioned_schema.schema
    entity_type: typing.Type[DataclassInstance] = create_table_dataclass(
        table_name, ns_module, schema
    )
    return entity_type, schema, versioned_schema


def create_table_dataclass(
    table_name: str, module: types.ModuleType, schema: Schema
) -> typing.Type[DataclassInstance]:
    """
    Synthesizes a Python data-class representing a database table.

    :param table_name: The name of the table.
    :param module: The Python module in which to create the new type. Corresponds to a database schema.
    :param schema: The JSON schema to use as a source.
    """

    properties = typing.cast(Schema, schema["properties"])
    properties.pop("meta")

    key_object: Schema = typing.cast(Schema, properties["key"])
    key_properties = typing.cast(Schema, key_object["properties"])
    key_name = next(iter(key_properties.keys()))

    table_schema = flatten_schema(
        schema,
        options=SchemaFlatteningOptions(qualified_names=False, recursive=False),
    )

    entity_type = typing.cast(
        type[DataclassInstance],
        schema_to_type(table_schema, module=module, class_name=table_name),
    )
    return make_entity(entity_type, key_name)
