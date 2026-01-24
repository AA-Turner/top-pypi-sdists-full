from typing import Any, Dict, List, Optional

from tinybird.datafile.common import Datafile
from tinybird.sql_template_fmt import format_sql_template
from tinybird.tb.client import TinyB

DATAFILE_NEW_LINE = "\n"
DATAFILE_INDENT = " " * 4


def format_description(file_parts: List[str], doc: Any) -> List[str]:
    description = doc.description if doc.description is not None else ""
    if description:
        file_parts.append("DESCRIPTION >")
        file_parts.append(DATAFILE_NEW_LINE)
        [
            file_parts.append(f"{DATAFILE_INDENT}{d.strip()}\n")  # type: ignore
            for d in description.split(DATAFILE_NEW_LINE)
            if d.strip()
        ]
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_maintainer(file_parts: List[str], doc: Datafile) -> List[str]:
    maintainer = doc.maintainer if doc.maintainer is not None else ""
    if maintainer:
        file_parts.append(f"MAINTAINER {maintainer}")
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tokens(file_parts: List[str], doc: Datafile) -> List[str]:
    for token in doc.tokens:
        file_parts.append(f'TOKEN "{token["token_name"]}" {token["permission"]}')
        file_parts.append(DATAFILE_NEW_LINE)
    if len(doc.tokens):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tags(file_parts: List[str], doc: Datafile) -> List[str]:
    if doc.filtering_tags:
        file_parts.append(f'TAGS "{", ".join(doc.filtering_tags)}"')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_include(file_parts: List[str], doc: Datafile, unroll_includes: bool = False) -> List[str]:
    if unroll_includes:
        return file_parts

    assert doc.raw is not None

    include = [line for line in doc.raw if "INCLUDE" in line and ".incl" in line]
    if include:
        file_parts.append(include[0])
        file_parts.append(DATAFILE_NEW_LINE)
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


def format_sql(
    sql: str,
    DATAFILE_INDENT: str,
    line_length: Optional[int] = None,
    lower_keywords: bool = False,
    resource_name: Optional[str] = None,
    resource_source: Optional[str] = None,
) -> str:
    sql = format_sql_template(
        sql.strip(),
        line_length=line_length,
        lower_keywords=lower_keywords,
        resource_name=resource_name,
        resource_source=resource_source,
    )
    return "\n".join([f"{DATAFILE_INDENT}{part}" for part in sql.split("\n") if len(part.strip())])
