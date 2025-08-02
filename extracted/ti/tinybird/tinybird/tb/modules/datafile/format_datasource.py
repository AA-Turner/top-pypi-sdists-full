from typing import Any, Dict, List, Optional

from tinybird.datafile.common import Datafile
from tinybird.datafile.parse_datasource import parse_datasource
from tinybird.sql import schema_to_sql_columns
from tinybird.tb.client import TinyB
from tinybird.tb.modules.datafile.format_common import (
    DATAFILE_INDENT,
    DATAFILE_NEW_LINE,
    format_description,
    format_include,
    format_maintainer,
    format_tags,
    format_tokens,
)


def format_datasource(
    filename: str,
    unroll_includes: bool = False,
    for_diff: bool = False,
    client: Optional[TinyB] = None,
    replace_includes: bool = False,
    datafile: Optional[Datafile] = None,
    for_deploy_diff: bool = False,
    skip_eval: bool = False,
    content: Optional[str] = None,
) -> str:
    if datafile:
        doc = datafile
    else:
        doc = parse_datasource(
            filename, replace_includes=replace_includes, skip_eval=skip_eval, content=content
        ).datafile

    file_parts: List[str] = []
    if for_diff:
        is_kafka = "kafka_connection_name" in doc.nodes[0]
        if is_kafka:
            kafka_metadata_columns = [
                "__value",
                "__headers",
                "__topic",
                "__partition",
                "__offset",
                "__timestamp",
                "__key",
            ]
            columns = [c for c in doc.nodes[0]["columns"] if c["name"] not in kafka_metadata_columns]
            doc.nodes[0].update(
                {
                    "columns": columns,
                }
            )
        if for_deploy_diff:
            format_description(file_parts, doc)
        format_tags(file_parts, doc)
        format_schema(file_parts, doc.nodes[0])
        format_indices(file_parts, doc.nodes[0])
        format_engine(file_parts, doc.nodes[0], only_ttl=bool(not for_deploy_diff), client=client)
        if for_deploy_diff:
            format_import_settings(file_parts, doc.nodes[0])
        format_shared_with(file_parts, doc)
    else:
        format_maintainer(file_parts, doc)
        format_description(file_parts, doc)
        format_tokens(file_parts, doc)
        format_tags(file_parts, doc)
        format_schema(file_parts, doc.nodes[0])
        format_indices(file_parts, doc.nodes[0])
        format_engine(file_parts, doc.nodes[0])
        format_include(file_parts, doc, unroll_includes=unroll_includes)
        format_data_connector(file_parts, doc.nodes[0])
        format_import_settings(file_parts, doc.nodes[0])
        format_shared_with(file_parts, doc)
    result = "".join(file_parts)
    result = result.rstrip("\n") + "\n"
    return result


def format_schema(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    if node.get("schema"):
        file_parts.append("SCHEMA >")
        file_parts.append(DATAFILE_NEW_LINE)
        columns = schema_to_sql_columns(node["columns"])
        file_parts.append(f",{DATAFILE_NEW_LINE}".join(map(lambda x: f"    {x}", columns)))
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)

    return file_parts


def format_indices(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    if node.get("indexes"):
        indexes = node["indexes"]
        file_parts.append("INDEXES >")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(f"{DATAFILE_NEW_LINE}".join(map(lambda index: f"    {index.to_datafile()}", indexes)))
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)

    return file_parts


def format_data_connector(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    ll = len(file_parts)
    quotes = "''"
    [file_parts.append(f"{k.upper()} {v or quotes}{DATAFILE_NEW_LINE}") for k, v in node.items() if "kafka" in k]  # type: ignore
    if ll < len(file_parts):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_import_settings(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    ll = len(file_parts)
    [file_parts.append(f"{k.upper()} {v}{DATAFILE_NEW_LINE}") for k, v in node.items() if "import_" in k]  # type: ignore
    if ll < len(file_parts):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_shared_with(file_parts: List[str], doc: Datafile) -> List[str]:
    if doc.shared_with:
        file_parts.append("SHARED_WITH >")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append("\n".join([f"{DATAFILE_INDENT}{workspace_name}" for workspace_name in doc.shared_with]))
    return file_parts


def format_engine(
    file_parts: List[str], node: Dict[str, Any], only_ttl: bool = False, client: Optional[TinyB] = None
) -> List[str]:
    if only_ttl:
        if node.get("engine", None):
            for arg in sorted(node["engine"].get("args", [])):
                if arg[0].upper() == "TTL":
                    elem = ", ".join([x.strip() for x in arg[1].split(",")])
                    try:
                        if client:
                            ttl_sql = client.sql_get_format(f"select {elem}", with_clickhouse_format=True)
                            formatted_ttl = ttl_sql[7:]
                        else:
                            formatted_ttl = elem
                    except Exception:
                        formatted_ttl = elem
                    file_parts.append(f"ENGINE_{arg[0].upper()} {formatted_ttl}")
                    file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)
        return file_parts
    else:
        if node.get("engine", None):
            empty = '""'
            file_parts.append(f"ENGINE {node['engine']['type']}" if node.get("engine", {}).get("type") else empty)
            file_parts.append(DATAFILE_NEW_LINE)
            for arg in sorted(node["engine"].get("args", [])):
                elem = ", ".join([x.strip() for x in arg[1].split(",")])
                file_parts.append(f"ENGINE_{arg[0].upper()} {elem if elem else empty}")
                file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)
        return file_parts
