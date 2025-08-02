import json
import typing as t

import click
from loguru import logger

from .sca_constants import SCA_ERROR_EXIT_CODE


class ScaException(click.ClickException):
    """Exception raised when an error occurs while running Gable SCA. Functions
    that run the SCA CLI can produce this exception when the SCA CLI fails, and
    optionally provide a markdown-formatted message that can be displayed as the
    PR comment."""

    def __init__(
        self,
        message: str,
        markdown: t.Optional[str] = None,
        exit_code: int = SCA_ERROR_EXIT_CODE,
    ):
        super().__init__(message)
        self.markdown = markdown
        # Override Click's default exit code with our custom one
        self.exit_code = exit_code


def create_pyspark_exception(e: Exception) -> t.Optional[ScaException]:
    """Try to parse the message from an exception raised by our PySpark runner,
    and create a ScaException with a markdown-formatted message that can be
    displayed as the PR comment. If the exception message cannot be parsed, return None.
    """
    markdown = "# PySpark Error\n"
    markdown_snippet_fmt_str = """
## {}

<pre><i>{}{}:{}</i>

{}</pre>
"""

    try:
        parsed_error_bodies: list[dict[str, str]] = json.loads(str(e))
        markdown_snippets = []
        for parsed_body in parsed_error_bodies:
            e_type = parsed_body.get("type")
            e_file = parsed_body.get("file")
            e_function = parsed_body.get("function")
            e_line = parsed_body.get("line")
            e_message = parsed_body.get("message")
            if e_type and e_file and e_line and e_message:
                function_str = f":{e_function}" if e_function else ""
                message_str = (
                    e_message.strip()
                    .strip("'\"")
                    .replace("\\n", "\n\t")
                    .replace("\\x1b[4m", "<i><b>")
                    .replace("\\x1b[0m", "</b></i>")
                )
                message_str = "\t" + message_str
                markdown_snippets.append(
                    markdown_snippet_fmt_str.format(
                        e_type, e_file, function_str, e_line, message_str
                    )
                )

        if markdown_snippets:
            for snippet in markdown_snippets:
                markdown += snippet
            return ScaException(str(e), markdown=markdown)
    except Exception as e:
        logger.opt(exception=True).debug("Failed to parse PySpark error message")
        logger.debug(e)
    return None
