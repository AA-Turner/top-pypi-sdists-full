import glob
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import click

from tinybird.tb.modules.cicd import check_cicd_exists, init_cicd
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLICreateException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.login_common import login
from tinybird.tb.modules.project import Project

DEFAULT_FOLDER = "tinybird"
DEFAULT_SDK = "cli"
DEFAULT_MODE = "branch"
DEFAULT_CICD = "skip"
SDK_CHOICES = ("typescript", "python", "cli")
MODE_CHOICES = ("branch", "local", "manual")
CICD_CHOICES = ("github", "gitlab", "skip")
SKILLS_INSTALL_REGISTRY = "tinybirdco/tinybird-agent-skills"
SKILLS_INSTALL_BASE_ARGS = [
    "skills",
    "add",
    SKILLS_INSTALL_REGISTRY,
]
GLOBAL_AGENT_SKILL = "tinybird"
PROJECT_TYPE_AGENT_SKILLS = {
    "cli": "tinybird-cli-guidelines",
    "python": "tinybird-python-sdk-guidelines",
    "typescript": "tinybird-typescript-sdk-guidelines",
}
SKILLS_INSTALL_TIMEOUT_SECONDS = 120


@cli.command(name="init")
@click.option(
    "--type",
    "project_type",
    type=click.Choice(SDK_CHOICES, case_sensitive=False),
    default=None,
    help="Project type: typescript, python, or cli.",
)
@click.option(
    "--dev-mode",
    type=click.Choice(MODE_CHOICES, case_sensitive=False),
    default=None,
    help="Development mode: branch, local, or manual.",
)
@click.option("--folder", type=str, default=None, help=f"Project folder. Default: {DEFAULT_FOLDER}")
@click.option(
    "--cicd",
    "cicd_provider",
    type=click.Choice(CICD_CHOICES, case_sensitive=False),
    default=None,
    help="Generate CI/CD templates for github, gitlab, or skip.",
)
@click.option(
    "--skip-login",
    default=False,
    is_flag=True,
    help="Authenticate after init.",
)
@click.pass_context
def init(
    ctx: click.Context,
    project_type: Optional[str],
    dev_mode: Optional[str],
    folder: Optional[str],
    cicd_provider: Optional[str],
    skip_login: bool,
) -> None:
    """Initialize a new project."""
    project: Project = ctx.ensure_object(dict)["project"]
    config = CLIConfig.get_project_config()

    root_folder = os.getcwd()
    if config._path:
        root_folder = os.path.dirname(config._path)

    selected_sdk = _prompt_sdk(project_type)
    selected_mode = _prompt_mode(dev_mode)
    selected_folder = _prompt_folder(folder)
    selected_cicd = _prompt_cicd_provider(cicd_provider)

    folder_path = _resolve_folder_path(root_folder, selected_folder)
    project.folder = str(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)

    try:
        config_status = "unchanged"
        project_structure_status = "unchanged"
        env_status = "already exists"
        cicd_status = "skipped"

        config_changed, config_created = persist_tinybird_config(
            root_folder,
            project_type=selected_sdk,
            dev_mode=selected_mode,
            folder=selected_folder,
        )
        if config_changed:
            config_file_action = "Created" if config_created else "Updated"
            config_status = config_file_action.lower()

        if selected_sdk == "cli" and not validate_project_structure(project):
            project_structure_status = "created"
            click.echo(FeedbackManager.highlight(message="\n» Creating new project structure..."))
            click.echo(
                FeedbackManager.info(
                    message="Learn more about data files https://www.tinybird.co/docs/forward/datafiles"
                )
            )
            create_project_structure(str(folder_path))
            click.echo(FeedbackManager.success(message="✓ Scaffolding completed!\n"))
        elif selected_sdk == "cli":
            project_structure_status = "already exists"

        if not already_has_env_file(root_folder):
            env_status = "created"
            click.echo(FeedbackManager.highlight(message="\n» Creating .env.local file..."))
            create_env_file(root_folder)
            click.echo(FeedbackManager.success(message="✓ Done!\n"))

        if selected_cicd != "skip":
            if check_cicd_exists(root_folder, provider=selected_cicd):
                cicd_status = f"{selected_cicd} already exists"
                click.echo(
                    FeedbackManager.warning(
                        message=f"△ {selected_cicd} CI/CD templates already exist. Skipping generation.\n"
                    )
                )
            else:
                cicd_status = f"{selected_cicd} generated"
                click.echo(FeedbackManager.highlight(message=f"\n» Creating CI/CD files for {selected_cicd}..."))
                init_git(root_folder)
                init_cicd(
                    root_folder,
                    data_project_dir=os.path.relpath(folder_path, root_folder),
                    provider=selected_cicd,
                )
                click.echo(FeedbackManager.success(message="✓ Done!\n"))
        else:
            cicd_status = "skipped"

        if _resolve_install_skills_choice():
            click.echo(FeedbackManager.highlight(message="\n» Installing Tinybird agent skills..."))
            install_agent_skills(selected_sdk)

        _show_init_summary(
            selected_sdk=selected_sdk,
            selected_mode=selected_mode,
            selected_folder=selected_folder,
            config_status=config_status,
            project_structure_status=project_structure_status,
            env_status=env_status,
            cicd_status=cicd_status,
        )

        login_choice = _resolve_login_choice(skip_login)
        if login_choice:
            click.echo(FeedbackManager.highlight(message="\n» Starting login..."))
            login(host=None, interactive=True, method="browser")
            click.echo(FeedbackManager.success(message="✓ Done!\n"))

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
# Learn more at https://www.tinybird.co/docs/forward/get-data-in/connectors/s3#s3-connection-settings
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


def _prompt_sdk(sdk: Optional[str]) -> str:
    if sdk:
        return sdk.lower()

    return DEFAULT_SDK


def _prompt_mode(mode: Optional[str]) -> str:
    if mode:
        return mode.lower()

    click.echo(FeedbackManager.highlight(message="\n? Select development mode:"))
    click.echo("  [1] branch - Cloud branches mapped to your git feature branch")
    click.echo("  [2] local - Run build/test against Tinybird Local")
    click.echo("  [3] manual - Choose environment manually with flags")
    choice = click.prompt("\nSelect option", default=1, type=int)
    if choice == 1:
        return "branch"
    if choice == 2:
        return "local"
    if choice == 3:
        return "manual"
    click.echo(FeedbackManager.warning(message=f"Invalid option '{choice}'. Defaulting to {DEFAULT_MODE}."))
    return DEFAULT_MODE


def _prompt_folder(folder: Optional[str]) -> str:
    if folder and folder.strip():
        return folder.strip()

    selected = click.prompt(
        FeedbackManager.highlight(message=f"\n? Project folder [{DEFAULT_FOLDER}]"),
        type=str,
        default=DEFAULT_FOLDER,
        show_default=False,
    ).strip()
    return selected or DEFAULT_FOLDER


def _prompt_cicd_provider(cicd_provider: Optional[str]) -> str:
    if cicd_provider:
        return cicd_provider.lower()

    click.echo(FeedbackManager.highlight(message="\n? Select CI/CD templates:"))
    click.echo("  [1] github - Generate GitHub Actions workflows")
    click.echo("  [2] gitlab - Generate GitLab CI templates")
    click.echo("  [3] skip - Do not generate CI/CD templates")
    choice = click.prompt("\nSelect option", default=3, type=int)
    if choice == 1:
        return "github"
    if choice == 2:
        return "gitlab"
    if choice == 3:
        return "skip"
    click.echo(FeedbackManager.warning(message=f"Invalid option '{choice}'. Defaulting to {DEFAULT_CICD}."))
    return DEFAULT_CICD


def _prompt_login(should_login: Optional[bool]) -> bool:
    if should_login is not None:
        return should_login

    return click.confirm(
        FeedbackManager.highlight(message="\n? Do you want to login now? [Y/n]"),
        default=True,
        show_default=False,
    )


def _prompt_install_skills(should_install: Optional[bool]) -> bool:
    if should_install is not None:
        return should_install

    return click.confirm(
        FeedbackManager.highlight(message="\n? Do you want to install Tinybird agent skills? [Y/n]"),
        default=True,
        show_default=False,
    )


def _build_agent_skills_install_command(project_type: str) -> list[str]:
    # Pass --yes to npx itself to avoid waiting on package-install confirmation.
    command = ["npx", "--yes", *SKILLS_INSTALL_BASE_ARGS]
    command.extend(["--skill", GLOBAL_AGENT_SKILL])
    project_type_skill = PROJECT_TYPE_AGENT_SKILLS.get(project_type)
    if project_type_skill:
        command.extend(["--skill", project_type_skill])
    command.append("--yes")
    return command


def _manual_agent_skills_install_command(project_type: str) -> str:
    command = _build_agent_skills_install_command(project_type)
    command = [part for part in command if part != "--yes"]
    return " ".join(command)


def install_agent_skills(project_type: str) -> bool:
    command = _build_agent_skills_install_command(project_type)
    manual_command = _manual_agent_skills_install_command(project_type)

    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=SKILLS_INSTALL_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        click.echo(
            FeedbackManager.warning(
                message=(
                    "△ Could not install Tinybird agent skills automatically because `npx` is not available. "
                    f"Run manually: {manual_command}"
                )
            )
        )
        return False
    except subprocess.TimeoutExpired:
        click.echo(
            FeedbackManager.warning(
                message=(
                    f"△ Timed out while installing Tinybird agent skills automatically. Run manually: {manual_command}"
                )
            )
        )
        return False
    except Exception as exc:
        click.echo(
            FeedbackManager.warning(
                message=(
                    f"△ Failed to install Tinybird agent skills automatically: {exc}. Run manually: {manual_command}"
                )
            )
        )
        return False

    if result.returncode != 0:
        click.echo(
            FeedbackManager.warning(
                message=(f"△ Failed to install Tinybird agent skills automatically. Run manually: {manual_command}")
            )
        )
        return False

    click.echo(FeedbackManager.success(message="✓ Tinybird agent skills installed!\n"))
    return True


def _has_credentials() -> bool:
    # Intentionally read only `.tinyb` in the current working directory.
    # Do not traverse parent folders for init login detection.
    tinyb_path = Path(os.getcwd()) / ".tinyb"
    if tinyb_path.exists():
        try:
            raw = json.loads(tinyb_path.read_text())
            if isinstance(raw, dict) and (raw.get("token") or raw.get("user_token")):
                return True
        except Exception:
            pass

    return bool(os.environ.get("TB_TOKEN") or os.environ.get("TB_USER_TOKEN"))


def _resolve_login_choice(skip_login: bool) -> bool:
    if skip_login is True:
        return False

    if _has_credentials():
        return False

    return _prompt_login(None)


def _resolve_install_skills_choice() -> bool:
    if not sys.stdin.isatty():
        return False
    return _prompt_install_skills(None)


def _show_init_summary(
    selected_sdk: str,
    selected_mode: str,
    selected_folder: str,
    config_status: str,
    project_structure_status: str,
    env_status: str,
    cicd_status: str,
) -> None:
    click.echo(FeedbackManager.gray(message="\nProject type: ") + FeedbackManager.info(message=selected_sdk))
    click.echo(FeedbackManager.gray(message="Development mode: ") + FeedbackManager.info(message=selected_mode))
    click.echo(FeedbackManager.gray(message="Folder: ") + FeedbackManager.info(message=selected_folder))
    click.echo(FeedbackManager.gray(message="Config: ") + FeedbackManager.info(message=config_status))
    if selected_sdk == "cli":
        click.echo(
            FeedbackManager.gray(message="Project structure: ") + FeedbackManager.info(message=project_structure_status)
        )
    click.echo(FeedbackManager.gray(message=".env.local: ") + FeedbackManager.info(message=env_status))
    click.echo(FeedbackManager.gray(message="CI/CD: ") + FeedbackManager.info(message=cicd_status))
    click.echo(FeedbackManager.success(message="\n✓ Setup completed!"))


def _resolve_folder_path(root_folder: str, folder: str) -> Path:
    folder_path = Path(folder)
    if folder_path.is_absolute():
        return folder_path
    return Path(root_folder) / folder_path


def persist_tinybird_config(root_folder: str, project_type: str, dev_mode: str, folder: str) -> tuple[bool, bool]:
    config_path = Path(root_folder) / "tinybird.config.json"
    config_data: Dict[str, Any] = {}
    created = not config_path.exists()

    if config_path.exists():
        try:
            config_data = json.loads(config_path.read_text())
            if not isinstance(config_data, dict):
                raise ValueError("tinybird.config.json must contain a JSON object")
        except Exception as exc:
            raise CLICreateException(FeedbackManager.error(message=f"Invalid tinybird.config.json: {exc}"))

    if project_type == "typescript":
        updates = {
            "devMode": dev_mode,
            "folder": folder,
        }
        keys_to_remove = ("type", "projectType", "project_type", "dev_mode", "sdk", "include")
        preferred_order = ("devMode", "folder")
    else:
        updates = {
            "dev_mode": dev_mode,
            "folder": folder,
        }
        keys_to_remove = ("type", "projectType", "project_type", "devMode", "sdk", "include")
        preferred_order = ("dev_mode", "folder")

    changed = False
    for key in keys_to_remove:
        if key in config_data:
            del config_data[key]
            changed = True

    for key, value in updates.items():
        if config_data.get(key) != value:
            config_data[key] = value
            changed = True

    # Keep the main init keys at the top for readability/consistency.
    ordered_config: Dict[str, Any] = {}
    for key in preferred_order:
        if key in config_data:
            ordered_config[key] = config_data[key]
    for key, value in config_data.items():
        if key not in ordered_config:
            ordered_config[key] = value

    if list(ordered_config.keys()) != list(config_data.keys()):
        changed = True
    config_data = ordered_config

    if changed or created:
        config_path.write_text(json.dumps(config_data, indent=2) + "\n")
        return True, created

    return False, False


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
    ssl_ca_pem: Optional[str],
    tb_secret_ssl_ca_pem: Optional[str],
    schema_registry_url: Optional[str],
    folder: str,
) -> Path:
    kafka_bootstrap_servers = (
        inject_tb_secret(tb_secret_bootstrap_servers) if tb_secret_bootstrap_servers else bootstrap_servers
    )
    kafka_key = inject_tb_secret(tb_secret_key) if tb_secret_key else key
    kafka_secret = inject_tb_secret(tb_secret_secret) if tb_secret_secret else secret
    kafka_ssl_ca_pem = inject_tb_secret(tb_secret_ssl_ca_pem) if tb_secret_ssl_ca_pem else ssl_ca_pem
    content = f"""TYPE kafka
KAFKA_BOOTSTRAP_SERVERS {kafka_bootstrap_servers}
KAFKA_SECURITY_PROTOCOL {security_protocol or "SASL_SSL"}
KAFKA_SASL_MECHANISM {sasl_mechanism or "PLAIN"}
KAFKA_KEY {kafka_key}
KAFKA_SECRET {kafka_secret}
"""
    if schema_registry_url:
        content += f"""KAFKA_SCHEMA_REGISTRY_URL {schema_registry_url}\n"""
    if kafka_ssl_ca_pem:
        content += f"""KAFKA_SSL_CA_PEM >\n    {kafka_ssl_ca_pem}\n"""
    content += """# Learn more at https://www.tinybird.co/docs/forward/get-data-in/connectors/kafka#kafka-connection-settings
"""

    return generate_connection_file(name, content, folder, skip_feedback=True)


def inject_tb_secret(secret_name: str) -> str:
    return f"""{{{{ tb_secret("{secret_name}") }}}}"""
