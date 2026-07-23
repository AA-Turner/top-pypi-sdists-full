import os
from typing import Dict, List, Optional

import click

from tinybird.datafile.common import (
    DatafileKind,
    DatafileSyntaxError,
    ParseResult,
    format_filename,
    parse,
)
from tinybird.datafile.exceptions import IncludeFileNotFoundException, ParseException
from tinybird.sql_template import (
    get_template_and_variables,
    render_sql_template,
    validate_template_parameter_names,
)
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tornado_template import UnClosedIfError


def parse_pipe(
    filename: str,
    replace_includes: bool = True,
    content: Optional[str] = None,
    skip_eval: bool = False,
    hide_folders: bool = False,
    add_context_to_datafile_syntax_errors: bool = True,
    secrets: Optional[Dict[str, str]] = None,
    ignore_secrets: bool = False,
) -> ParseResult:
    basepath = ""
    if not content:
        with open(filename) as file:
            s = file.read()
        basepath = os.path.dirname(filename)
    else:
        s = content

    filename = format_filename(filename, hide_folders)
    try:
        sql = ""
        try:
            doc, warnings = parse(
                s, basepath=basepath, replace_includes=replace_includes, skip_eval=skip_eval, kind=DatafileKind.pipe
            )
            doc.validate()
        except DatafileSyntaxError as e:
            try:
                if add_context_to_datafile_syntax_errors:
                    e.get_context_from_file_contents(s)
            finally:
                raise e
        for node in doc.nodes:
            if "type" in node:
                node["type"] = node["type"].lower()
            sql = node.get("sql", "")
            source_sql = sql.strip()
            if not source_sql:
                raise click.ClickException(
                    FeedbackManager.error_parsing_node(node=node["name"], pipe=filename, error="Empty query")
                )
            if source_sql.startswith("%"):
                secrets_list: Optional[List[str]] = None
                if secrets:
                    secrets_list = list(secrets.keys())
                # Reject parameters declared without a usable name (e.g. a numeric
                # literal cast like `{{Float32(1682892000.0)}}`) before rendering.
                validate_template_parameter_names(sql[1:], node_id=node["name"])
                # Setting test_mode=True to ignore errors on required parameters and
                # secrets_in_test_mode=False to raise errors on missing secrets
                sql, _, variable_warnings = render_sql_template(
                    source_sql[1:],
                    name=node["name"],
                    secrets=secrets_list,
                    test_mode=True,
                    secrets_in_test_mode=ignore_secrets,
                )
                doc.warnings = variable_warnings
                if not sql.strip():
                    raise click.ClickException(
                        FeedbackManager.error_parsing_node(
                            node=node["name"],
                            pipe=filename,
                            error="Template renders to an empty query without parameters",
                        )
                    )
            else:
                sql = source_sql
            # it'll fail with a ModuleNotFoundError when the toolset is not available but it returns the parsed doc
            from tinybird.sql_toolset import format_sql as toolset_format_sql

            toolset_format_sql(sql)
    # TODO(eclbg): all these exceptions that trigger a ClickException shouldn't be here, as this code will only run in
    # the server soon
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno=e.lineno, error=f"{str(e)} + SQL(parse exception): {sql}"
            )
        )
    except ValueError as e:
        source_sql = node.get("sql", "")
        source_sql_stripped = source_sql.strip()
        t, template_variables, _ = get_template_and_variables(source_sql, name=node["name"])

        if not source_sql_stripped.startswith("%") and len(template_variables) > 0:
            raise click.ClickException(FeedbackManager.error_template_start(filename=filename))
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno="", error=f"{str(e)} + SQL(value error): {source_sql}"
            )
        )
    except UnClosedIfError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_node_with_unclosed_if(node=e.node, pipe=filename, lineno=e.lineno, sql=e.sql)
        )
    except IncludeFileNotFoundException as e:
        raise click.ClickException(FeedbackManager.error_not_found_include(filename=e, lineno=e.lineno))
    except ModuleNotFoundError:
        pass
    return ParseResult(datafile=doc, warnings=warnings)
