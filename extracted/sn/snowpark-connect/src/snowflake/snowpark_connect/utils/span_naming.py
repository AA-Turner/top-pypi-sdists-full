#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Derive a low-cardinality telemetry span name from a Spark Connect request.

Spark Connect multiplexes every DataFrame action over a handful of gRPC methods
(``ExecutePlan``, ``AnalyzePlan``, ``Config``), so naming a span after the gRPC
method says nothing about what the user actually ran. Instead we name the span
after the *terminal* operation the user invoked, recovered from the request
proto: the plan verb (the active ``oneof`` field) refined by the inner
``oneof`` / enum fields the wire already carries.

Two properties matter:

* **Low cardinality.** The name is always drawn from a fixed, closed set of
  verbs so spans aggregate cleanly. High-cardinality details (the call-site file
  and line) are attached as span *attributes*, never folded into the name.
* **Best effort.** When the proto cannot disambiguate a call -- e.g. ``collect``,
  ``toPandas`` and ``toLocalIterator`` are byte-identical on the wire -- the name
  degrades gracefully: refined name -> raw plan verb -> gRPC method name.

Translation table (request shape -> span name). ``(*)`` marks the
materializer-canonicalization rule explained below the table.

    ExecutePlan, plan.root =
        filter / project / sort / range / to_df / deduplicate / join / read ...   collect (*)
        aggregate                                                                 aggregate
        limit                                                                     limit
        tail                                                                      tail
        show_string                                                              show
        html_string                                                              replHtml
        stat_approx_quantile                                                     approxQuantile
        stat_corr / stat_cov                                                     corr / cov
        catalog(<op>)                                                            <op>  (listTables, getTable, ...)
        extension(aggregate)                                                     aggregate
        extension(lateral_join / rdd_map / ...)                                  collect (*)

    ExecutePlan, plan.command =
        write_operation     -> save_type=path                                    save
                            -> save_type=table, save_method=SAVE_AS_TABLE        saveAsTable
                            -> save_type=table, save_method=INSERT_INTO          insertInto
        write_operation_v2  -> mode=CREATE / REPLACE / CREATE_OR_REPLACE /       create / replace / createOrReplace /
                                    APPEND / OVERWRITE / OVERWRITE_PARTITIONS     append / overwrite / overwritePartitions
        create_dataframe_view -> is_global, replace                              createTempView / createOrReplaceTempView /
                                                                                 createGlobalTempView / createOrReplaceGlobalTempView
        sql_command                                                              sql
        register_function                                                        registerFunction
        register_table_function                                                  registerTableFunction
        write_stream_operation_start                                             start
        streaming_query_command(<inner>)                                         <inner>  (stop, processAllAvailable, ...)
        streaming_query_manager_command(<inner>)                                 <inner>  (awaitAnyTermination, ...)

    AnalyzePlan, analyze =
        schema / explain / persist / unpersist ...                               <verb verbatim>
        tree_string                                                              printSchema
        spark_version                                                            version
        is_local / is_streaming / input_files                                    isLocal / isStreaming / inputFiles
        same_semantics / semantic_hash / get_storage_level                       sameSemantics / semanticHash / storageLevel

``(*)`` A relation that is not tied to a *specific* action only reaches the wire
as an ExecutePlan root because a result materializer (``collect`` / ``toPandas``
/ ``toLocalIterator``) ran on top of a transform chain. Those byte-identical
materializers, and every plain transform under them, canonicalize to ``collect``
-- which is what the Spark UI labels the resulting job. Relations a specific
action injects (``limit`` from ``take``/``head``, ``show_string`` from ``show``,
``aggregate`` from ``count``/``agg``, ...) keep their own name instead.
"""

import os

import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.commands_pb2 as commands_proto

# rel_type verbs that map to a nicer bare API name.
_REL_TYPE_RENAMES = {
    "show_string": "show",
    "html_string": "replHtml",
    "approx_quantile": "approxQuantile",
}

# Root relations injected by a *specific* terminal action, which therefore keep
# their own name. Every other relation can only appear as an ExecutePlan root
# because a plain result materializer ran on top of a transform chain, so those
# canonicalize to ``collect`` (see ``_root_relation_span_name``).
_DISTINCTIVE_ROOT_RELS = frozenset(
    {
        "show_string",
        "html_string",
        "limit",
        "tail",
        "aggregate",
        "approx_quantile",
        "corr",
        "cov",
    }
)

# command_type verbs that map to a nicer bare API name (the ones not refined by
# an inner field in ``_command_terminal_name``).
_COMMAND_TYPE_RENAMES = {
    "sql_command": "sql",
    "register_function": "registerFunction",
    "register_table_function": "registerTableFunction",
    "write_stream_operation_start": "start",
}

# analyze verbs that map to a nicer bare API name.
_ANALYZE_RENAMES = {
    "tree_string": "printSchema",
    "get_storage_level": "storageLevel",
    "same_semantics": "sameSemantics",
    "semantic_hash": "semanticHash",
    "input_files": "inputFiles",
    "is_local": "isLocal",
    "is_streaming": "isStreaming",
    "spark_version": "version",
}

# df.write.saveAsTable(...) / df.write.insertInto(...) ride the same
# write_operation command and are told apart only by this enum.
_TABLE_SAVE_METHOD_NAMES = {
    commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_SAVE_AS_TABLE: "saveAsTable",
    commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_INSERT_INTO: "insertInto",
}

# DataFrameWriterV2 actions all ride write_operation_v2 and differ only by mode.
_WRITE_V2_MODE_NAMES = {
    commands_proto.WriteOperationV2.Mode.MODE_CREATE: "create",
    commands_proto.WriteOperationV2.Mode.MODE_REPLACE: "replace",
    commands_proto.WriteOperationV2.Mode.MODE_CREATE_OR_REPLACE: "createOrReplace",
    commands_proto.WriteOperationV2.Mode.MODE_APPEND: "append",
    commands_proto.WriteOperationV2.Mode.MODE_OVERWRITE: "overwrite",
    commands_proto.WriteOperationV2.Mode.MODE_OVERWRITE_PARTITIONS: "overwritePartitions",
}


def _camel(name: str) -> str:
    """snake_case -> camelCase (``list_tables`` -> ``listTables``)."""
    head, *tail = name.split("_")
    return head + "".join(part[:1].upper() + part[1:] for part in tail)


def _operation_span_suffix(request) -> str | None:
    """Raw plan verb from the request's operation ``oneof`` (the fallback name)."""
    try:
        if isinstance(request, proto_base.ExecutePlanRequest):
            op = request.plan.WhichOneof("op_type")
            if op == "root":
                return request.plan.root.WhichOneof("rel_type")
            if op == "command":
                return request.plan.command.WhichOneof("command_type")
        elif isinstance(request, proto_base.AnalyzePlanRequest):
            return request.WhichOneof("analyze")
        elif isinstance(request, proto_base.ConfigRequest):
            return request.operation.WhichOneof("op_type")
    except Exception:
        return None
    return None


def _command_terminal_name(command, verb) -> str | None:
    """Refine an ExecutePlan command verb into the bare terminal API name.

    Returns ``None`` when the discriminating inner field is unset, so the caller
    falls back to the raw plan verb.
    """
    if verb == "write_operation":
        write = command.write_operation
        save_type = write.WhichOneof("save_type")
        if save_type == "path":
            return "save"
        if save_type == "table":
            return _TABLE_SAVE_METHOD_NAMES.get(write.table.save_method, "save")
        return None
    if verb == "write_operation_v2":
        return _WRITE_V2_MODE_NAMES.get(command.write_operation_v2.mode)
    if verb == "create_dataframe_view":
        view = command.create_dataframe_view
        if view.is_global:
            return (
                "createOrReplaceGlobalTempView"
                if view.replace
                else "createGlobalTempView"
            )
        return "createOrReplaceTempView" if view.replace else "createTempView"
    if verb == "streaming_query_command":
        inner = command.streaming_query_command.WhichOneof("command")
        return _camel(inner) if inner else None
    if verb == "streaming_query_manager_command":
        inner = command.streaming_query_manager_command.WhichOneof("command")
        return _camel(inner) if inner else None
    return _COMMAND_TYPE_RENAMES.get(verb, verb)


def _root_relation_span_name(verb: str | None) -> str:
    """Name a root relation.

    Relations injected by a specific action keep their own name; any other root
    relation only reaches the wire because a plain result materializer ran on top
    of it, so it canonicalizes to ``collect`` (mirrors the Spark UI).
    """
    if verb in _DISTINCTIVE_ROOT_RELS:
        return _REL_TYPE_RENAMES.get(verb, verb)
    return "collect"


def _extension_op(root) -> str | None:
    """Inner op of a Snowflake relation extension (``Extension.WhichOneof("op")``)."""
    try:
        import snowflake.snowpark_connect.proto.snowflake_relation_ext_pb2 as snowflake_proto

        extension = snowflake_proto.Extension()
        root.extension.Unpack(extension)
        return extension.WhichOneof("op")
    except Exception:
        return None


def terminal_operation_name(request) -> str | None:
    """Bare terminal operation name for the request.

    Returns ``None`` when the operation cannot be refined to a distinct name, so
    the caller falls back to the raw plan verb.
    """
    try:
        verb = _operation_span_suffix(request)
        if not verb:
            return None

        if isinstance(request, proto_base.ExecutePlanRequest):
            op = request.plan.WhichOneof("op_type")
            if op == "root":
                root = request.plan.root
                if verb == "catalog":
                    cat = root.catalog.WhichOneof("cat_type")
                    return _camel(cat) if cat else verb
                if verb == "extension":
                    # Snowflake relation extensions wrap their own op; treat that
                    # inner op like a normal rel_type so an enhanced aggregate
                    # (PIVOT/GROUPING SETS/HAVING) is named `aggregate`, matching
                    # the standard aggregate relation, while transform-like
                    # extensions (lateral_join, rdd_map, ...) become `collect`.
                    return _root_relation_span_name(_extension_op(root))
                return _root_relation_span_name(verb)
            if op == "command":
                return _command_terminal_name(request.plan.command, verb)

        if isinstance(request, proto_base.AnalyzePlanRequest):
            return _ANALYZE_RENAMES.get(verb, verb)

        return verb
    except Exception:
        return None


def span_name(method_name, request) -> str:
    """Span name: terminal op -> raw plan verb -> gRPC method name."""
    return (
        terminal_operation_name(request)
        or _operation_span_suffix(request)
        or method_name
    )


def call_site_attributes(client_stack) -> dict:
    """Map the innermost user frame to ``code.*`` span attributes."""
    if not client_stack:
        return {}
    frame = client_stack[0]
    attrs: dict = {}
    if frame.get("line_number") is not None:
        try:
            attrs["code.lineno"] = int(frame["line_number"])
        except (TypeError, ValueError):
            pass
    if frame.get("file_name"):
        # The client ships an absolute path; keep only the file name.
        attrs["code.filepath"] = os.path.basename(frame["file_name"])
    return attrs


def add_call_site_attributes(span, client_stack) -> None:
    """Attach ``code.filepath`` / ``code.lineno`` to a span."""
    if span is None or not span.is_recording():
        return
    for key, value in call_site_attributes(client_stack).items():
        span.set_attribute(key, value)


def add_terminal_op_attribute(span, request) -> None:
    """Attach the raw plan verb as ``code.terminal_op`` for drill-down."""
    if span is None or not span.is_recording():
        return
    verb = _operation_span_suffix(request)
    if verb:
        span.set_attribute("code.terminal_op", verb)
