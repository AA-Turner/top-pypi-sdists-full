import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from tinybird.datafile.common import (
    ON_DEMAND,
    CopyParameters,
    Datafile,
    ExportReplacements,
    PipeNodeTypes,
    _unquote,
    eval_var,
)
from tinybird.datafile.parse_pipe import parse_pipe
from tinybird.sql_template_fmt import DEFAULT_FMT_LINE_LENGTH, format_sql_template
from tinybird.tb.modules.datafile.format_common import (
    DATAFILE_INDENT,
    DATAFILE_NEW_LINE,
    format_description,
    format_maintainer,
    format_tags,
    format_tokens,
)
from tinybird.tb.modules.datafile.format_datasource import format_engine


def format_node_sql(
    file_parts: List[str], node: Dict[str, Any], line_length: Optional[int] = None, lower_keywords: bool = False
) -> List[str]:
    file_parts.append("SQL >")
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(format_sql(node["sql"], DATAFILE_INDENT, line_length=line_length, lower_keywords=lower_keywords))
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_node_type(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    node_type = node.get("type", "").lower()
    node_type_upper = f"TYPE {node_type.upper()}"
    # Materialized pipe
    if node_type == PipeNodeTypes.MATERIALIZED:
        file_parts.append(node_type_upper)
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(f"DATASOURCE {node['datasource']}")
        file_parts.append(DATAFILE_NEW_LINE)
        format_engine(file_parts, node)

    # Copy pipe
    if node_type == PipeNodeTypes.COPY:
        file_parts.append(node_type_upper)
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(f"TARGET_DATASOURCE {node['target_datasource']}")
        if node.get("mode"):
            file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(f"COPY_MODE {node.get('mode')}")

        if node.get(CopyParameters.COPY_SCHEDULE):
            is_ondemand = node[CopyParameters.COPY_SCHEDULE].lower() == ON_DEMAND
            file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(
                f"{CopyParameters.COPY_SCHEDULE.upper()} {ON_DEMAND if is_ondemand else node[CopyParameters.COPY_SCHEDULE]}"
            )
        else:
            file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(f"{CopyParameters.COPY_SCHEDULE.upper()} {ON_DEMAND}")
        file_parts.append(DATAFILE_NEW_LINE)

    # Sink or Stream pipe
    if ExportReplacements.is_export_node(node):
        file_parts.append(node_type_upper)
        export_params = ExportReplacements.get_params_from_datafile(node)
        file_parts.append(DATAFILE_NEW_LINE)
        for param, value in export_params.items():
            if param == "schedule_cron" and not value:
                value = ON_DEMAND
            datafile_key = ExportReplacements.get_datafile_key(param, node)
            if datafile_key and value:
                file_parts.append(f"{datafile_key} {value}")
                file_parts.append(DATAFILE_NEW_LINE)

    return file_parts


def format_pipe_include(file_parts: List[str], node: Dict[str, Any], includes: Dict[str, Any]) -> List[str]:
    if includes:
        for k, v in includes.copy().items():
            if node["name"] in v:
                file_parts.append(f"INCLUDE {k}")
                file_parts.append(DATAFILE_NEW_LINE)
                file_parts.append(DATAFILE_NEW_LINE)
                del includes[k]
    return file_parts


def format_sql(sql: str, DATAFILE_INDENT: str, line_length: Optional[int] = None, lower_keywords: bool = False) -> str:
    sql = format_sql_template(sql.strip(), line_length=line_length, lower_keywords=lower_keywords)
    return "\n".join([f"{DATAFILE_INDENT}{part}" for part in sql.split("\n") if len(part.strip())])


def format_node(
    file_parts: List[str],
    node: Dict[str, Any],
    includes: Dict[str, Any],
    line_length: Optional[int] = None,
    unroll_includes: bool = False,
    lower_keywords: bool = False,
) -> None:
    if not unroll_includes:
        format_pipe_include(file_parts, node, includes)
    item = [k for k, _ in includes.items() if node["name"].strip() in k]
    if item and not unroll_includes:
        return

    file_parts.append(f"NODE {node['name'].strip()}")
    file_parts.append(DATAFILE_NEW_LINE)

    from collections import namedtuple

    Doc = namedtuple("Doc", ["description"])
    format_description(file_parts, Doc(node.get("description", "")))
    format_node_sql(file_parts, node, line_length=line_length, lower_keywords=lower_keywords)
    format_node_type(file_parts, node)


def format_pipe(
    filename: str,
    line_length: Optional[int] = DEFAULT_FMT_LINE_LENGTH,
    unroll_includes: bool = False,
    replace_includes: bool = False,
    datafile: Optional[Datafile] = None,
    for_deploy_diff: bool = False,
    skip_eval: bool = False,
    content: Optional[str] = None,
) -> str:
    if datafile:
        doc = datafile
    else:
        doc = parse_pipe(filename, replace_includes=replace_includes, skip_eval=skip_eval, content=content).datafile

    file_parts: List[str] = []
    format_maintainer(file_parts, doc)
    format_description(file_parts, doc)
    format_tokens(file_parts, doc)
    format_tags(file_parts, doc)
    if doc.includes and not unroll_includes:
        for k in doc.includes:
            # We filter only the include files as we currently have 2 items for each include
            # { 'include_file.incl': 'First node of the include" }
            # { 'first node of the pipe after the include': }
            if ".incl" not in k:
                continue

            # We get all the nodes inside the include and remove them from the unrolled pipe as we want things unrolled
            include_parameters = _unquote(k)

            # If they use an include with parameters like `INCLUDE "xxx.incl" "GROUP_COL=path" "MATERIALIZED_VIEW=speed_insights_path_daily_mv"``
            # We just want the file name to take nodes
            include_file = include_parameters.split('"')[0]
            include_file = (
                Path(os.path.dirname(filename)) / eval_var(include_file)
                if "." in include_file
                else eval_var(include_file)
            )
            included_pipe = parse_pipe(include_file, skip_eval=skip_eval).datafile
            pipe_nodes = doc.nodes.copy()
            for included_node in included_pipe.nodes.copy():
                unrolled_included_node = next(
                    (node for node in pipe_nodes if node["name"] == included_node["name"]), None
                )
                if unrolled_included_node:
                    doc.nodes.remove(unrolled_included_node)
    for node in doc.nodes:
        format_node(
            file_parts,
            node,
            doc.includes,
            line_length=line_length,
            unroll_includes=unroll_includes,
            lower_keywords=bool(for_deploy_diff),
        )

    if not unroll_includes:
        for k, _ in doc.includes.items():
            if ".incl" not in k:
                continue
            file_parts.append(f"INCLUDE {k}")
            file_parts.append(DATAFILE_NEW_LINE)
            file_parts.append(DATAFILE_NEW_LINE)

    result = "".join(file_parts)
    result = result.rstrip("\n") + "\n"
    return result
