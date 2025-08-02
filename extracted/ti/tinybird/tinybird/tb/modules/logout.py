import click

from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.command(name="logout")
def logout() -> None:
    """
    Remove authentication from Tinybird.

    This command will remove the authentication credentials from the CLI configuration.
    """
    conf = CLIConfig.get_project_config()
    if workspace_name := conf.get("name", ""):
        click.echo(FeedbackManager.highlight(message=f"» Logging out from {workspace_name}..."))
    else:
        click.echo(FeedbackManager.highlight(message="» Logging out..."))
    conf.set_user_token("")
    conf.set_token("")
    conf.set_workspace_token(conf.get("id", ""), "")
    conf.set_token_for_host("", conf.get("host", ""))
    conf["tokens"] = {}
    conf["name"] = ""
    conf["id"] = ""
    conf["user_id"] = ""
    conf["user_email"] = ""
    conf.persist_to_file()
    click.echo(FeedbackManager.success(message="✓ Logged out!"))
