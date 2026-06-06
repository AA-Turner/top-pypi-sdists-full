import os
import shutil
import subprocess
import sys

import requests as rq

from fivetran_connector_sdk.logger import Logging
from fivetran_connector_sdk.constants import EXAMPLES_GITHUB_REPO, GITHUB_BRANCH, \
    AGENT_PLUGINS, SUPPORTED_AGENT_DISPLAY_NAMES, TOOLS_GITHUB_REPO_URL, TEMPLATE_CONNECTOR_PATH, \
    CONNECTORS_GITHUB_REPO, CONNECTORS_TEMPLATE_PREFIX, ROOT_FILENAME
from fivetran_connector_sdk.helpers import print_library_log


def init(project_dir: str, template: str, non_interactive: bool):
    connector_path = os.path.join(project_dir, ROOT_FILENAME)
    if non_interactive:
        print_library_log("overriding existing files; --non-interactive is set")
        confirm = "y"
    else:
        if os.path.isfile(connector_path):
            print_library_log(
                f"{ROOT_FILENAME} already exists at {project_dir}",
                log_icon=Logging.LogIcon.STEP,
            )
            confirm = "n"
        else:
            confirm = input(f"create new connector project at {project_dir}? (Y/n): ").strip()
    try:
        if confirm.lower() == "n":
            print_library_log("skipping connector project creation", log_icon=Logging.LogIcon.STEP)
        else:
            setup_connector(project_dir, template, non_interactive)
            print_library_log("project initialized", log_icon=Logging.LogIcon.SUCCESS)
            print_library_log("Time to make a great connector; Happy coding")
        setup_ai_agent()
        sys.exit(0)
    except Exception as e:
        print_library_log(f"failed to initialize project error: {e}", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        sys.exit(1)


def setup_connector(project_dir: str, template: str, non_interactive: bool):
    os.makedirs(project_dir, exist_ok=True)
    download_git_directory(template, project_dir, non_interactive)
    print_library_log(f"new project created at: {project_dir}", log_icon=Logging.LogIcon.SUCCESS)


def detect_installed_agents() -> dict:
    return {
        key: config["display_name"]
        for key, config in AGENT_PLUGINS.items()
        if shutil.which(config["cli_command"]) is not None
    }


def install_agent_plugin(agent_key: str) -> bool:
    config = AGENT_PLUGINS[agent_key]
    print_library_log(f"installing {config['display_name']} plugin", log_icon=Logging.LogIcon.STEP)
    for cmd in config["install_commands"]:
        try:
            result = subprocess.run(cmd)
        except OSError as e:
            print_library_log(
                f"install command failed: {' '.join(cmd)}: {e}",
                level=Logging.Level.WARNING,
                log_icon=Logging.LogIcon.FAILURE,
            )
            print_library_log(
                f"install manually: {TOOLS_GITHUB_REPO_URL}",
                log_icon=Logging.LogIcon.STEP,
            )
            return False
        if result.returncode != 0:
            print_library_log(
                f"install command failed: {' '.join(cmd)}",
                level=Logging.Level.WARNING,
                log_icon=Logging.LogIcon.FAILURE,
            )
            print_library_log(
                f"install manually: {TOOLS_GITHUB_REPO_URL}",
                log_icon=Logging.LogIcon.STEP,
            )
            return False
    print_library_log(f"{config['display_name']} plugin installed", log_icon=Logging.LogIcon.SUCCESS)
    return True


def setup_ai_agent():
    installed = detect_installed_agents()

    if not installed:
        print_library_log(
            f"no supported coding agents detected ({SUPPORTED_AGENT_DISPLAY_NAMES}); skipping plugin setup",
            log_icon=Logging.LogIcon.STEP,
        )
        print_library_log(
            f"install manually: {TOOLS_GITHUB_REPO_URL}",
            log_icon=Logging.LogIcon.STEP,
        )
        return

    agent_list = list(installed.items())
    skip_num = len(agent_list) + 1
    menu = (
        "Installed coding agents detected. Which agent should we install the Fivetran plugin for?\n"
        + "\n".join(f"{i}. {name}" for i, (_, name) in enumerate(agent_list, 1))
        + f"\n{skip_num}. Skip — I'll install manually"
    )

    choice = input(f"{menu}\n\nPlease enter the number of your choice: ").strip()
    try:
        choice_num = int(choice)
        if not (1 <= choice_num <= skip_num):
            raise ValueError
    except ValueError:
        print_library_log("invalid choice; skipping agent setup", log_icon=Logging.LogIcon.FAILURE)
        return

    if choice_num == skip_num:
        print_library_log("skipping plugin setup", log_icon=Logging.LogIcon.STEP)
        print_library_log(f"install manually: {TOOLS_GITHUB_REPO_URL}", log_icon=Logging.LogIcon.STEP)
    else:
        agent_key = agent_list[choice_num - 1][0]
        if not install_agent_plugin(agent_key):
            print_library_log(
                "agent plugin setup failed; skipping plugin setup",
                level=Logging.Level.WARNING,
                log_icon=Logging.LogIcon.FAILURE,
            )


def validate_example_directory(files_to_download: list):
    connector_files = [
        f for f in files_to_download
        if f['local_path'].endswith("connector.py")
    ]

    if len(connector_files) != 1:
        print_library_log(
            "selected directory is not a valid example; missing connector.py",
            Logging.Level.SEVERE
        )
        raise ValueError("Invalid directory passed. Path did not resolve to a valid connector.")

def _resolve_repo_and_path(path_prefix: str) -> tuple:
    """Returns (repo, actual_path) based on template routing rules."""
    if path_prefix.startswith(CONNECTORS_TEMPLATE_PREFIX):
        return CONNECTORS_GITHUB_REPO, path_prefix[len(CONNECTORS_TEMPLATE_PREFIX):]
    if path_prefix.startswith("examples/"):
        return EXAMPLES_GITHUB_REPO, path_prefix
    return CONNECTORS_GITHUB_REPO, path_prefix


def download_git_directory(path_prefix: str, project_dir: str, non_interactive: bool):
    repo, actual_path = _resolve_repo_and_path(path_prefix)
    try:
        tree_url = f"https://api.github.com/repos/{repo}/git/trees/{GITHUB_BRANCH}?recursive=1"
        response = rq.get(tree_url, timeout=10)
        response.raise_for_status()

        tree_data = response.json()
        if 'tree' not in tree_data:
            print_library_log("failed to fetch repository from GitHub", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
            return

        files_to_download = []
        for item in tree_data['tree']:
            if item['type'] == 'blob' and item['path'].startswith(actual_path):
                relative_path = item['path'][len(actual_path):].lstrip('/')
                if path_prefix == TEMPLATE_CONNECTOR_PATH and "readme" in relative_path.lower():
                    continue
                files_to_download.append({
                    'github_path': item['path'],
                    'local_path': relative_path,
                    'size': item.get('size', 0)
                })

        if not files_to_download:
            print_library_log("no files to download", Logging.Level.WARNING)
            return

        validate_example_directory(files_to_download)

        print_library_log(f"downloading {len(files_to_download)} files from GitHub", log_icon=Logging.LogIcon.STEP)
        download_file_from_github(files_to_download, project_dir, non_interactive, repo)

    except Exception as e:
        print_library_log(f"failed to download files: {e}", Logging.Level.WARNING)
        print_library_log(f"files are available for manual download from: https://github.com/{repo}/tree/{GITHUB_BRANCH}/{actual_path}")


def download_file_from_github(files_to_download: list, project_dir: str, non_interactive: bool, repo: str = EXAMPLES_GITHUB_REPO):
    for file_info in files_to_download:
        # Construct raw download URL
        raw_url = f"https://raw.githubusercontent.com/{repo}/{GITHUB_BRANCH}/{file_info['github_path']}"

        # Create target path
        target_path = os.path.join(project_dir, file_info['local_path'])
        target_dir = os.path.dirname(target_path)

        # Create directory if needed
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        # Download file
        try:
            file_response = rq.get(raw_url, timeout=10)
            file_response.raise_for_status()

            if os.path.exists(target_path):
                if not non_interactive:
                    override_file = input(f"File {file_info['local_path']} already exists. Overwrite? (y/N): ")
                else:
                    override_file = "y"
                if override_file.lower() != "y":
                    print_library_log(f"skipped {file_info['local_path']}", level=Logging.Level.FINE, log_icon=Logging.LogIcon.SUCCESS)
                    continue

            with open(target_path, 'wb') as f:
                f.write(file_response.content)

            print_library_log(f"downloaded {file_info['local_path']}", level=Logging.Level.FINE, log_icon=Logging.LogIcon.SUCCESS)
        except Exception as e:
            print_library_log(f"failed to download {file_info['local_path']}: {e}", level=Logging.Level.WARNING, log_icon=Logging.LogIcon.FAILURE)
