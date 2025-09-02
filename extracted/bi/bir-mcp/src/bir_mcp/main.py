import enum
import functools
import inspect
import warnings
from typing import Annotated

import fastmcp
import typer

import bir_mcp.atlassian
import bir_mcp.charts
import bir_mcp.git_lab
import bir_mcp.grafana
import bir_mcp.sql
from bir_mcp.config import SystemManagedConfig


class McpCategory(enum.StrEnum):
    gitlab = enum.auto()
    grafana = enum.auto()
    jira = enum.auto()
    local = enum.auto()


def build_mcp_server(
    enable_local_tools: Annotated[
        bool,
        typer.Option(
            help=inspect.cleandoc(
                """
                Whether to include local tools, such as those that interact with local
                file system and perform local Git actions.
                """
            ),
        ),
    ] = False,
    include_non_readonly_tools: Annotated[
        bool,
        typer.Option(
            help=inspect.cleandoc(
                """
                Whether to include tools with ability to write and create new resources,
                for example new Jira issues, GitLab branches or commits.
                """
            ),
        ),
    ] = False,
    include_destructive_tools: Annotated[
        bool,
        typer.Option(
            help=inspect.cleandoc(
                """
                Whether to include tools with ability to delete or overwrite resources,
                such as GitLab file updates.
                """
            ),
        ),
    ] = False,
    consul_host: Annotated[
        str | None,
        typer.Option(
            help=inspect.cleandoc(
                """
                The host of the Consul key-value store to load the system managed configuration from,
                with the SQL connections and default system connection credentials.
                Any parameters explicity provided to this function will override the ones
                loaded from Consul.
                """
            ),
        ),
    ] = None,
    consul_key: Annotated[
        str | None,
        typer.Option(help="The key name of the Consul key-value store."),
    ] = None,
    consul_token: Annotated[
        str | None,
        typer.Option(help="The token to use for authentication with Consul."),
    ] = None,
    gitlab_private_token: Annotated[
        str | None,
        typer.Option(
            help=inspect.cleandoc(
                """
                The GitLab token to use for authentication with GitLab. To enable writing tools,
                the token should have write API permissions.
                """
            ),
        ),
    ] = None,
    grafana_username: str | None = None,
    grafana_password: str | None = None,
    grafana_token: Annotated[
        str | None,
        typer.Option(
            help=inspect.cleandoc(
                """
                The Grafana API token to use for authentication with Grafana.
                If provided, this will be used instead of username/password authentication.
                """
            ),
        ),
    ] = None,
    jira_token: str | None = None,
    gitlab_url: str = "https://gitlab.kapitalbank.az",
    grafana_url: str = "https://yuno.kapitalbank.az",
    jira_url: str = "https://jira-support.kapitalbank.az",
    timezone: Annotated[
        str,
        typer.Option(
            help=inspect.cleandoc(
                """
                The timezone to use for datetime formatting in the output of tools.
                """
            ),
        ),
    ] = "Asia/Baku",
    tools_max_output_length: Annotated[
        int | None,
        typer.Option(
            help=inspect.cleandoc(
                """
                The maximum output string length for tools, with longer strings being truncated.
                Especially useful for AI clients with smaller context windows and those that
                cannot automatically trim or summarize chat history, for example Claude Desktop.
                """
            )
        ),
    ] = None,
    verify_ssl: Annotated[bool, typer.Option(help="Whether to verify SSL certificates.")] = True,
    ca_file: Annotated[
        str | None,
        typer.Option(help="Path to a local certificate authority file to verify SSL certificates."),
    ] = None,
    prompts_to_tools: Annotated[
        bool,
        typer.Option(
            help=inspect.cleandoc(
                """
                Whether to convert prompts to tools. Not all MCP clients support prompts (for example
                Windsurf at the time of writing), but all of them support tools.
                """
            )
        ),
    ] = False,
) -> fastmcp.FastMCP:
    ssl_verify = ca_file or verify_ssl  # Workaround because typer doesn't support union types.
    if consul_host and consul_key:
        config = SystemManagedConfig.from_consul(
            consul_host=consul_host,
            consul_token=consul_token,
            consul_key=consul_key,
        )
    else:
        config = SystemManagedConfig()

    config_overrides = dict(
        gitlab_private_token=gitlab_private_token,
        grafana_token=grafana_token,
        grafana_username=grafana_username,
        grafana_password=grafana_password,
        jira_token=jira_token,
        gitlab_url=gitlab_url,
        grafana_url=grafana_url,
        jira_url=jira_url,
    )
    config_overrides = {k: v for k, v in config_overrides.items() if v}
    config = config.model_copy(update=config_overrides)

    server = fastmcp.FastMCP(
        name="Bir MCP server",
        instructions=inspect.cleandoc("""
            MCP server for BirBank.
        """),
    )
    for sub_mcp in generate_mcps(
        config=config,
        timezone=timezone,
        enable_local_tools=enable_local_tools,
        ssl_verify=ssl_verify,
    ):
        subserver = sub_mcp.get_mcp_server(
            include_non_readonly_tools=include_non_readonly_tools,
            include_destructive_tools=include_destructive_tools,
            max_output_length=tools_max_output_length,
            prompts_to_tools=prompts_to_tools,
        )
        server.mount(subserver, prefix=sub_mcp.get_tag())

    return server


def generate_mcps(
    config: SystemManagedConfig,
    timezone: str,
    enable_local_tools: bool,
    ssl_verify: bool | str,
):
    common_params = dict(timezone=timezone)
    if enable_local_tools:
        from bir_mcp.local.filesystem import Filesystem
        from bir_mcp.local.git_local import Git

        for local_mcp in [
            Git(**common_params),
            Filesystem(**common_params),
        ]:
            yield local_mcp

    for sql_context in config.sql_contexts:
        yield bir_mcp.sql.SQL(sql_context=sql_context, **common_params)

    yield bir_mcp.charts.Charts(
        engines={name: conn.get_engine() for name, conn in config.sql_connections.items()},
        **common_params,
    )

    common_params["ssl_verify"] = ssl_verify
    if config.gitlab_private_token:
        yield bir_mcp.git_lab.GitLab(
            url=config.gitlab_url, private_token=config.gitlab_private_token, **common_params
        )
    else:
        warnings.warn(
            "Since GitLab private token is not provided, the GitLab tools will not be available."
        )

    if grafana_token_or_auth := config.get_grafana_token_or_auth():
        yield bir_mcp.grafana.Grafana(
            url=config.grafana_url,
            token_or_auth=grafana_token_or_auth,
            **common_params,
        )
    else:
        warnings.warn(
            "Since Grafana token or username/password are not provided, the Grafana tools will not be available."
        )

    if config.jira_token:
        yield bir_mcp.atlassian.Jira(token=config.jira_token, **common_params)
    else:
        warnings.warn("Since Jira token is not provided, the Jira tools will not be available.")

    if config.confluence_token:
        yield bir_mcp.atlassian.Confluence(token=config.confluence_token, **common_params)
    else:
        warnings.warn(
            "Since Confluence token is not provided, the Confluence tools will not be available."
        )

    if config.sonarqube_token:
        yield bir_mcp.git_lab.SonarQube(token=config.sonarqube_token, **common_params)
    else:
        warnings.warn(
            "Since SonarQube token is not provided, the SonarQube tools will not be available."
        )


@functools.wraps(build_mcp_server)
def build_and_run(*args, **kwargs):
    server = build_mcp_server(*args, **kwargs)
    server.run()


def main():
    typer.run(build_and_run)


if __name__ == "__main__":
    main()
