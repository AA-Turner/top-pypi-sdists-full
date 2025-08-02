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
from tinybird.sql_template import get_template_and_variables, render_sql_template, secret_template_key
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
            if sql.strip()[0] == "%":
                secrets_list: Optional[List[str]] = None
                if secrets:
                    secrets_list = [f"{secret_template_key(secret)}" for secret in secrets.keys()]
                # Setting test_mode=True to ignore errors on required parameters and
                # secrets_in_test_mode=False to raise errors on missing secrets
                sql, _, variable_warnings = render_sql_template(
                    sql[1:],
                    name=node["name"],
                    secrets=secrets_list,
                    test_mode=True,
                    secrets_in_test_mode=False,
                )
                doc.warnings = variable_warnings
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
        t, template_variables, _ = get_template_and_variables(sql, name=node["name"])

        if sql.strip()[0] != "%" and len(template_variables) > 0:
            raise click.ClickException(FeedbackManager.error_template_start(filename=filename))
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno="", error=f"{str(e)} + SQL(value error): {sql}"
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
