import glob
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import click
import requests

from tinybird.prompts import claude_rules_prompt, create_prompt, readme_prompt, rules_prompt
from tinybird.tb.client import TinyB
from tinybird.tb.modules.cicd import init_cicd
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import _generate_datafile, generate_datafile
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import persist_fixture
from tinybird.tb.modules.exceptions import CLICreateException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.llm_utils import extract_xml, parse_xml
from tinybird.tb.modules.local_common import get_tinybird_local_client
from tinybird.tb.modules.mock_common import create_mock_data
from tinybird.tb.modules.project import Project


@cli.command()
@click.option(
    "--data",
    type=str,
    default=None,
    help="Initial data to be used to create the project. Tinybird Local and authentication are required.",
)
@click.option(
    "--prompt",
    type=str,
    default=None,
    help="Prompt to be used to create the project. Tinybird Local and authentication are required.",
)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.option("--folder", type=str, default=None, help="Folder to create the project in")
@click.option("--agent", type=str, default="cursor", help="Agent to use for rules")
@click.pass_context
def create(
    ctx: click.Context, data: Optional[str], prompt: Optional[str], rows: int, folder: Optional[str], agent: str
) -> None:
    """Initialize a new project."""
    project: Project = ctx.ensure_object(dict)["project"]
    config = CLIConfig.get_project_config()
    ctx_config = ctx.ensure_object(dict)["config"]

    # If folder is provided, rewrite the config and project folder
    if folder:
        config.set_cwd(folder)
        config.persist_to_file()
        project.folder = folder

    root_folder = os.getcwd()
    if config._path:
        root_folder = os.path.dirname(config._path)

    folder = project.folder
    folder_path = project.path

    if not folder_path.exists():
        folder_path.mkdir()

    try:
        tb_client = config.get_client(token=ctx_config.get("token"), host=ctx_config.get("host"))
        user_token: str = ""
        created_something = False
        if prompt:
            user_token = ctx_config.get("user_token")
            if not user_token:
                raise Exception("This action requires authentication. Run 'tb login' first.")

        if not validate_project_structure(project):
            click.echo(FeedbackManager.highlight(message="\n» Creating new project structure..."))
            click.echo(
                FeedbackManager.info(
                    message="Learn more about data files https://www.tinybird.co/docs/forward/datafiles"
                )
            )
            create_project_structure(folder)
            click.echo(FeedbackManager.success(message="✓ Scaffolding completed!\n"))
            created_something = True
        result: List[Path] = []
        if data or prompt:
            click.echo(FeedbackManager.highlight(message="\n» Creating resources..."))

        data_result: List[Path] = []
        if data:
            if urlparse(data).scheme in ("http", "https"):
                data_result = create_resources_from_url(data, project, ctx_config)
            else:
                data_result = create_resources_from_data(data, project, ctx_config)
            result.extend(data_result)

        prompt_result: List[Path] = []
        if prompt:
            prompt_result = create_resources_from_prompt(tb_client, user_token, prompt, project)
            result.extend(prompt_result)
            readme_path = folder_path / "README.md"
            if readme_path.exists():
                click.echo(FeedbackManager.highlight(message="\n» Updating project description..."))
            else:
                click.echo(FeedbackManager.highlight(message="\n» Creating project description..."))
                readme_path.touch()
            llm = LLM(user_token=str(user_token), host=tb_client.host)
            readme_user_prompt = prompt or ""
            all_resources_xml = get_resources_xml(project)
            readme_response = llm.ask(
                system_prompt=readme_prompt(
                    readme_path.read_text(), tb_client.host, "$TB_ADMIN_TOKEN", all_resources_xml
                ),
                prompt=readme_user_prompt,
                feature="tb_create_readme",
            )
            readme_result = extract_xml(readme_response, "readme")
            readme_path.write_text(readme_result)
            click.echo(FeedbackManager.info_file_created(file="README.md"))
            created_something = True

        if data or prompt:
            click.echo(FeedbackManager.success(message="✓ Resources created!\n"))

        if not already_has_env_file(root_folder):
            click.echo(FeedbackManager.highlight(message="\n» Creating .env.local file..."))
            create_env_file(root_folder)
            click.echo(FeedbackManager.success(message="✓ Done!\n"))
            created_something = True

        if not already_has_cicd(root_folder):
            click.echo(FeedbackManager.highlight(message="\n» Creating CI/CD files for GitHub and GitLab..."))
            init_git(root_folder)
            init_cicd(root_folder, data_project_dir=os.path.relpath(folder))
            click.echo(FeedbackManager.success(message="✓ Done!\n"))
            created_something = True

        if not already_has_cursor_rules(root_folder):
            click.echo(FeedbackManager.highlight(message="\n» Creating rules..."))
            create_rules(root_folder, "tb", agent)
            click.echo(FeedbackManager.info_file_created(file=".cursorrules"))
            click.echo(FeedbackManager.success(message="✓ Done!\n"))
            created_something = True

        if not already_has_claude_rules(root_folder):
            click.echo(FeedbackManager.highlight(message="\n» Creating Claude Code rules..."))
            create_claude_rules(root_folder, "tb")
            click.echo(FeedbackManager.info_file_created(file="CLAUDE.md"))
            click.echo(FeedbackManager.success(message="✓ Done!\n"))
            created_something = True

        if should_generate_fixtures(result):
            click.echo(FeedbackManager.highlight(message="\n» Generating fixtures..."))

            if data:
                for ds_path in [ds for ds in data_result if ds.suffix == ".datasource"]:
                    parsed_url = urlparse(data)
                    if parsed_url.scheme in ("http", "https"):
                        response = requests.get(data)
                        data_content = response.text
                        data_format = parsed_url.path.split(".")[-1]
                    else:
                        data_path = Path(data)
                        data_content = data_path.read_text()
                        data_format = data_path.suffix.lstrip(".")

                    ds_name = ds_path.stem
                    datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
                    click.echo(FeedbackManager.info_file_created(file=f"fixtures/{ds_name}.{data_format}"))
                    persist_fixture(ds_name, data_content, folder, format=data_format)
                    click.echo(FeedbackManager.success(message="✓ Done!"))
                    created_something = True

            elif prompt and prompt_result:
                ds_results = [path for path in prompt_result if path.suffix == ".datasource"]
                for datasource_path in ds_results:
                    datasource_name = datasource_path.stem
                    datasource_content = datasource_path.read_text()
                    has_json_path = "`json:" in datasource_content
                    if has_json_path:
                        mock_data = create_mock_data(
                            datasource_name,
                            datasource_content,
                            rows,
                            prompt,
                            config,
                            ctx_config,
                            user_token,
                            tb_client,
                            format_="ndjson",
                            folder=project.folder,
                        )
                        if mock_data:
                            persist_fixture(datasource_name, mock_data, folder, format="ndjson")
                            click.echo(FeedbackManager.info_file_created(file=f"fixtures/{datasource_name}.ndjson"))
                            click.echo(FeedbackManager.success(message="✓ Done!"))
                            created_something = True

        if not created_something and not len(result) > 0:
            click.echo(FeedbackManager.warning(message="△ No resources created\n"))
    except Exception as e:
        raise CLICreateException(FeedbackManager.error(message=str(e)))


PROJECT_PATHS = (
    "datasources",
    "endpoints",
    "materializations",
    "copies",
    "sinks",
    "pipes",
    "fixtures",
    "tests",
    "connections",
)


def validate_project_structure(project: Project) -> bool:
    some_folder_created = any((Path(project.folder) / path).exists() for path in PROJECT_PATHS)
    if some_folder_created:
        return True

    datasources = project.get_datasource_files()
    pipes = project.get_pipe_files()

    return len(datasources) > 0 or len(pipes) > 0


def should_generate_fixtures(result: List[Path]) -> List[Path]:
    if not result:
        return []
    return [
        path
        for path in result
        if path.suffix == ".datasource"
        # we only want to generate fixtures for MergeTree or Null engines
        and (
            re.search(r'ENGINE\s+(?:"MergeTree"|MergeTree|"Null"|Null)', path.read_text())
            or not re.search(r"ENGINE\s+", path.read_text())
        )
    ]


def already_has_cicd(folder: str) -> bool:
    ci_cd_paths = (".gitlab", ".github")
    return any((Path(folder) / path).exists() for path in ci_cd_paths)


def already_has_cursor_rules(folder: str) -> bool:
    cursor_rules_paths = (".cursorrules", ".windsurfrules")
    return any((Path(folder) / path).exists() for path in cursor_rules_paths)


def already_has_claude_rules(folder: str) -> bool:
    claude_rules_path = "CLAUDE.md"
    return (Path(folder) / claude_rules_path).exists()


def already_has_env_file(folder: str) -> bool:
    env_file_pattern = ".env.*"
    return any((Path(folder) / path).exists() for path in glob.glob(env_file_pattern))


def create_project_structure(folder: str):
    folder_path = Path(folder)
    PROJECT_PATHS_DESCRIPTIONS = {
        "datasources       →": "Where your data lives. Define the schema and settings for your tables.",
        "endpoints         →": "Expose real-time HTTP APIs of your transformed data.",
        "materializations  →": "Stream continuous updates of the result of a pipe into a new data source.",
        "copies            →": "Capture the result of a pipe at a moment in time and write it into a target data source.",
        "sinks             →": "Export your data to external systems on a scheduled or on-demand basis.",
        "pipes             →": "Transform your data and reuse the logic in endpoints, materializations and copies.",
        "fixtures          →": "Files with sample data for your project.",
        "tests             →": "Test your pipe files with data validation tests.",
        "connections       →": "Connect to and ingest data from popular sources: Kafka, S3 or GCS.",
    }

    for x in PROJECT_PATHS_DESCRIPTIONS.keys():
        try:
            path = x.split("→")[0].strip()
            f = folder_path / path
            f.mkdir()
            click.echo(
                FeedbackManager.info(message=f"./{x} ") + FeedbackManager.gray(message=PROJECT_PATHS_DESCRIPTIONS[x])
            )
        except FileExistsError:
            pass


def create_resources_from_prompt(
    tb_client: TinyB,
    user_token: str,
    prompt: str,
    project: Project,
    feature: str = "tb_create_resources",
) -> List[Path]:
    result: List[Path] = []
    datasource_paths = [Path(ds_file) for ds_file in project.get_datasource_files()]
    pipes_paths = [Path(pipe_file) for pipe_file in project.get_pipe_files()]
    connections_paths = [Path(conn_file) for conn_file in project.get_connection_files()]
    resources_xml = "\n".join(
        [
            f"<resource><type>{resource_type}</type><name>{resource_name}</name><content>{resource_content}</content></resource>"
            for resource_type, resource_name, resource_content in [
                ("datasource", ds.stem, ds.read_text()) for ds in datasource_paths
            ]
            + [
                (
                    "pipe",
                    pipe.stem,
                    pipe.read_text(),
                )
                for pipe in pipes_paths
            ]
            + [
                (
                    "connection",
                    conn.stem,
                    conn.read_text(),
                )
                for conn in connections_paths
            ]
        ]
    )
    llm = LLM(user_token=user_token, host=tb_client.host)
    prompt_result = llm.ask(system_prompt=create_prompt(resources_xml), prompt=prompt, feature=feature)
    prompt_result = extract_xml(prompt_result, "response")
    resources = parse_xml(prompt_result, "resource")
    datasources = []
    pipes = []
    connections = []
    for resource_xml in resources:
        resource_type = extract_xml(resource_xml, "type")
        name = extract_xml(resource_xml, "name")
        content = extract_xml(resource_xml, "content")
        resource = {
            "name": name,
            "content": content,
        }
        if resource_type.lower() == "datasource":
            datasources.append(resource)
        elif resource_type.lower() == "pipe":
            pipes.append(resource)
        elif resource_type.lower() == "connection":
            connections.append(resource)

    for ds in datasources:
        content = ds["content"].replace("```", "")
        filename = f"{ds['name']}.datasource"
        ds_file = generate_datafile(
            content,
            filename=filename,
            data=None,
            _format="ndjson",
            force=True,
            folder=project.folder,
        )
        result.append(ds_file)
    for pipe in pipes:
        content = pipe["content"].replace("```", "")
        pipe_file = generate_pipe_file(pipe["name"], content, project.folder)
        result.append(pipe_file)

    for conn in connections:
        content = conn["content"].replace("```", "")
        filename = f"{conn['name']}.connection"
        conn_file = generate_connection_file(conn["name"], content, project.folder)
        result.append(conn_file)

    return result


def init_git(folder: str):
    try:
        path = Path(folder)
        gitignore_file = path / ".gitignore"

        if gitignore_file.exists():
            content = gitignore_file.read_text()
            if ".tinyb" not in content:
                gitignore_file.write_text(content + "\n.tinyb\n.terraform\n")
        else:
            gitignore_file.write_text(".tinyb\n.terraform\n")

        click.echo(FeedbackManager.info_file_created(file=".gitignore"))
    except Exception as e:
        raise Exception(f"Error initializing Git: {e}")


def generate_pipe_file(name: str, content: str, folder: str) -> Path:
    def is_copy(content: str) -> bool:
        return re.search(r"TYPE copy", content, re.IGNORECASE) is not None

    def is_materialization(content: str) -> bool:
        return re.search(r"TYPE materialized", content, re.IGNORECASE) is not None

    def is_sink(content: str) -> bool:
        return re.search(r"TYPE sink", content, re.IGNORECASE) is not None

    def is_endpoint(content: str) -> bool:
        return re.search(r"TYPE endpoint", content, re.IGNORECASE) is not None

    already_exists = glob.glob(f"{folder}/**/{name}.pipe")
    if already_exists:
        f = Path(already_exists[0])
    else:
        if is_copy(content):
            pathname = "copies"
        elif is_materialization(content):
            pathname = "materializations"
        elif is_sink(content):
            pathname = "sinks"
        elif is_endpoint(content):
            pathname = "endpoints"
        else:
            pathname = "pipes"

        base = Path(folder) / pathname
        if not base.exists():
            base.mkdir()
        f = base / (f"{name}.pipe")
    with open(f"{f}", "w") as file:
        file.write(content)
    click.echo(FeedbackManager.info_file_created(file=f.relative_to(folder)))
    return f.relative_to(folder)


def generate_connection_file(name: str, content: str, folder: str, skip_feedback: bool = False) -> Path:
    already_exists = glob.glob(f"{folder}/**/{name}.connection")
    if already_exists:
        f = Path(already_exists[0])
    else:
        base = Path(folder) / "connections"
        if not base.exists():
            base.mkdir()
        f = base / (f"{name}.connection")
    with open(f"{f}", "w") as file:
        file.write(content)
    if not skip_feedback:
        click.echo(FeedbackManager.info_file_created(file=f.relative_to(folder)))
    return f.relative_to(folder)


def generate_aws_iamrole_connection_file_with_secret(
    name: str, service: str, role_arn_secret_name: str, region: str, folder: str, with_default_secret: bool = False
) -> Path:
    if with_default_secret:
        default_secret = ', "arn:aws:iam::123456789012:role/my-role"'
    else:
        default_secret = ""
    content = f"""TYPE {service}
S3_ARN {{{{ tb_secret("{role_arn_secret_name}"{default_secret}) }}}}
S3_REGION {region}
"""
    file_path = generate_connection_file(name, content, folder, skip_feedback=True)
    return file_path


def generate_gcs_connection_file_with_secrets(name: str, service: str, svc_account_creds: str, folder: str) -> Path:
    content = f"""TYPE {service}
GCS_SERVICE_ACCOUNT_CREDENTIALS_JSON {{{{ tb_secret("{svc_account_creds}") }}}}
"""
    file_path = generate_connection_file(name, content, folder, skip_feedback=True)
    return file_path


def create_env_file(folder: str):
    env_file = Path(folder) / ".env.local"
    env_file.write_text("")


def create_rules(folder: str, source: str, agent: str):
    if agent == "cursor":
        extension = ".cursorrules"
    elif agent == "windsurf":
        extension = ".windsurfrules"
    else:
        extension = ".md"

    rules_file = Path(folder) / extension
    rules_content = rules_prompt(source)
    rules_file.write_text(rules_content)


def create_claude_rules(folder: str, source: str):
    try:
        is_claude_code_installed = shutil.which("claude") is not None
        if is_claude_code_installed:
            rules_content = claude_rules_prompt(source)
            claude_file = Path(folder) / "CLAUDE.md"
            claude_file.write_text(rules_content)
    except Exception:
        pass


def get_context_file() -> Path:
    context_file = Path(os.path.expanduser("~/.tb_create_context"))
    if not context_file.exists():
        context_file.touch()
    return context_file


def get_context() -> str:
    context_file = get_context_file()
    return context_file.read_text()


def save_context(prompt: str, feedback: str):
    context_file = get_context_file()
    context_file.write_text(f"- {prompt}\n{feedback}")


def get_resources_xml(project: Project) -> str:
    datasource_paths = [Path(f) for f in project.get_datasource_files()]
    pipes_paths = [Path(f) for f in project.get_pipe_files()]
    resources_xml = "\n".join(
        [
            f"<resource><type>{resource_type}</type><name>{resource_name}</name><content>{resource_content}</content></resource>"
            for resource_type, resource_name, resource_content in [
                ("datasource", ds.stem, ds.read_text()) for ds in datasource_paths
            ]
            + [
                (
                    "pipe",
                    pipe.stem,
                    pipe.read_text(),
                )
                for pipe in pipes_paths
            ]
        ]
    )
    return resources_xml


def create_resources_from_data(
    data: str,
    project: Project,
    config: Dict[str, Any],
    skip_pipes: bool = False,
) -> List[Path]:
    local_client = get_tinybird_local_client(config)
    folder_path = project.path
    path = folder_path / data
    if not path.exists():
        path = Path(data)
    result: List[Path] = []
    format = path.suffix.lstrip(".")
    ds_file = _generate_datafile(str(path), local_client, format=format, force=True, folder=project.folder)
    result.append(ds_file)
    name = ds_file.stem
    no_pipes = len(project.get_pipe_files()) == 0
    if not skip_pipes and no_pipes:
        pipe_file = generate_pipe_file(
            f"{name}_endpoint",
            f"""
NODE endpoint
SQL >
    SELECT * from {name}
TYPE ENDPOINT
            """,
            project.folder,
        )
        result.append(pipe_file)
    return result


def create_resources_from_url(
    url: str, project: Project, config: Dict[str, Any], skip_pipes: bool = False
) -> List[Path]:
    result: List[Path] = []
    local_client = get_tinybird_local_client(config)
    format = url.split(".")[-1]
    ds_file = _generate_datafile(url, local_client, format=format, force=True, folder=project.folder)
    result.append(ds_file)
    name = ds_file.stem
    no_pipes = len(project.get_pipe_files()) == 0
    if not skip_pipes and no_pipes:
        pipe_file = generate_pipe_file(
            f"{name}_endpoint",
            f"""
NODE endpoint
SQL >
    SELECT * from {name}
TYPE ENDPOINT
            """,
            project.folder,
        )
        result.append(pipe_file)
    return result


def generate_kafka_connection_with_secrets(
    name: str,
    bootstrap_servers: str,
    key: str,
    secret: str,
    tb_secret_bootstrap_servers: Optional[str],
    tb_secret_key: Optional[str],
    tb_secret_secret: Optional[str],
    security_protocol: str,
    sasl_mechanism: str,
    folder: str,
) -> Path:
    kafka_bootstrap_servers = (
        inject_tb_secret(tb_secret_bootstrap_servers) if tb_secret_bootstrap_servers else bootstrap_servers
    )
    kafka_key = inject_tb_secret(tb_secret_key) if tb_secret_key else key
    kafka_secret = inject_tb_secret(tb_secret_secret) if tb_secret_secret else secret
    content = f"""TYPE kafka
KAFKA_BOOTSTRAP_SERVERS {kafka_bootstrap_servers}
KAFKA_SECURITY_PROTOCOL {security_protocol or "SASL_SSL"}
KAFKA_SASL_MECHANISM {sasl_mechanism or "PLAIN"}
KAFKA_KEY {kafka_key}
KAFKA_SECRET {kafka_secret}
"""
    return generate_connection_file(name, content, folder, skip_feedback=True)


def inject_tb_secret(secret_name: str) -> str:
    return f"""{{{{ tb_secret("{secret_name}") }}}}"""
