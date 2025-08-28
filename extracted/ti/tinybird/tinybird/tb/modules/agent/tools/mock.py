import click
from pydantic_ai import RunContext

from tinybird.tb.modules.agent.utils import (
    AgentRunCancelled,
    TinybirdAgentContext,
    create_terminal_box,
    show_confirmation,
    show_input,
)
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_pretty_table, format_data_to_ndjson
from tinybird.tb.modules.datafile.fixture import persist_fixture
from tinybird.tb.modules.feedback_manager import FeedbackManager


def generate_mock_fixture(
    ctx: RunContext[TinybirdAgentContext], datasource_name: str, sql: str, data_format: str, rows: int, task: str
) -> str:
    """Given a datasource name and a sql query to execute, generate a fixture file with mock data and append it to the datasource.

    Args:
        datasource_name (str): Name of the datasource to create mock data for. Required.
        sql (str): SQL query to execute to generate the mock data. Required.
        data_format (str): Format of the mock data to create. Options: ndjson, csv. Required.
        rows (int): Number of rows to create. If not provided, the default is 10. Required.
        task (str): Extra details about how to generate the mock data (nested json if any, sample row to help with the generation, etc). You can use this to fix issues with the mock data generation. Required.

    Returns:
        str: Message indicating the success or failure of the mock data generation
    """
    try:
        ctx.deps.thinking_animation.stop()

        click.echo(FeedbackManager.highlight(message=f"» Generating mock data for datasource '{datasource_name}'..."))
        try:
            sql_format = "JSON" if data_format == "ndjson" else "CSV"
            sql = f"SELECT * FROM ({sql}) LIMIT {rows} FORMAT {sql_format}"
            result = ctx.deps.execute_query_local(query=sql)
        except Exception as e:
            click.echo(
                FeedbackManager.error(message="✗ Failed to generate a valid SQL query for generating mock data.\n{e}")
            )
            ctx.deps.thinking_animation.start()
            return f"Failed to generate a valid sql for generating mock data for datasource '{datasource_name}'. SQL: {sql}\nError: {e}"

        preview_content = ""
        if sql_format == "JSON":
            data = result.get("data", [])[:rows]
            preview_content = str(format_data_to_ndjson(data[:10]))

            if len(data) != rows:
                raise Exception(
                    f"Failed to generate a valid sql for generating mock data for datasource '{datasource_name}'. Rows generated: {len(data)} != {rows}. SQL: {sql}\nError: {result}"
                )

            error_response = result.get("error", None)
            if error_response:
                raise Exception(
                    f"Failed to generate a valid sql for generating mock data for datasource '{datasource_name}'. SQL: {sql}\nError: {error_response}"
                )

        else:
            data = result
            preview_content = str(data[:1000])

        if isinstance(data, dict):
            data = data.get("data", [])[:rows]
            preview_content = str(format_data_to_ndjson(data[:10]))

        content = create_terminal_box(preview_content, title=f"fixtures/{datasource_name}.{data_format}")
        click.echo(content)
        click.echo("Showing a preview of the file.\n")
        active_plan = ctx.deps.get_plan() is not None
        confirmation = show_confirmation(
            title=f"Create fixture file for datasource '{datasource_name}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )

        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"User did not confirm mock data for datasource '{datasource_name}' in Tinybird Local and gave the following feedback: {feedback}"

        fixture_path = persist_fixture(datasource_name, data, ctx.deps.folder, format=data_format)
        fixture_path_name = f"fixtures/{fixture_path.name}"
        click.echo(FeedbackManager.success(message=f"✓ {fixture_path_name} created"))
        confirmation = show_confirmation(
            title=f"Append {fixture_path_name} to datasource '{datasource_name}'?",
            skip_confirmation=ctx.deps.dangerously_skip_permissions or active_plan,
        )
        if confirmation == "review":
            feedback = show_input(ctx.deps.workspace_name)
            ctx.deps.thinking_animation.start()
            return f"Mock data was generated in {fixture_path_name} but user did not confirm appending {fixture_path_name} to datasource '{datasource_name}' in Tinybird Local and gave the following feedback: {feedback}"

        ctx.deps.append_data_local(datasource_name=datasource_name, path=str(fixture_path))
        click.echo(FeedbackManager.success(message=f"✓ Data appended to datasource '{datasource_name}'"))
        ctx.deps.thinking_animation.start()
        return f"Mock data generated in {fixture_path_name} and appended to datasource '{datasource_name}' in Tinybird Local"
    except AgentRunCancelled as e:
        raise e
    except Exception as e:
        ctx.deps.thinking_animation.stop()
        error_message = str(e)
        click.echo(FeedbackManager.error(message=error_message))
        try:
            if "in quarantine" in error_message:
                click.echo(
                    FeedbackManager.highlight(message=f"» Looking for errors in {datasource_name}_quarantine...")
                )
                query = f"select * from {datasource_name}_quarantine order by insertion_date desc limit 5 FORMAT JSON"
                quarantine_result = ctx.deps.execute_query_local(query=query)
                quarantine_data = quarantine_result["data"] or []
                quarantine_meta = quarantine_result["meta"] or []
                column_names = [c["name"] for c in quarantine_meta]
                echo_safe_humanfriendly_tables_format_pretty_table(
                    data=[d.values() for d in quarantine_data], column_names=column_names
                )
                click.echo(
                    FeedbackManager.info(
                        message=f"These are the first 5 rows of the quarantine table for datasource '{datasource_name}':"
                    )
                )
                error_message = (
                    error_message
                    + f"\nThese are the first 5 rows of the quarantine table for datasource '{datasource_name}':\n{quarantine_data}. Use again `mock` tool but add this issue to the context."
                )

        except Exception as quarantine_error:
            error_message = error_message + f"\nError accessing to {datasource_name}_quarantine: {quarantine_error}"

        if "must be created first with 'mode=create'" in error_message:
            error_message = error_message + "\nBuild the project again."

        ctx.deps.thinking_animation.start()
        return f"Error generating mock data for datasource '{datasource_name}' in Tinybird Local: {error_message}"
