# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import difflib
import glob
import urllib.parse
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click
import yaml
from requests import Response

from tinybird.prompts import test_create_prompt
from tinybird.tb.client import TinyB
from tinybird.tb.modules.build_common import process as build_project
from tinybird.tb.modules.common import sys_exit
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLITestException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.llm_utils import extract_xml, parse_xml
from tinybird.tb.modules.local_common import get_local_tokens, get_test_workspace_name
from tinybird.tb.modules.project import Project

yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str  # type: ignore[attr-defined]


def repr_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.org_represent_str(data)


yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)


def generate_test_file(pipe_name: str, tests: List[Dict[str, Any]], folder: Optional[str], mode: str = "w") -> Path:
    base = Path("tests")
    if folder:
        base = Path(folder) / base

    base.mkdir(parents=True, exist_ok=True)

    yaml_str = yaml.safe_dump(tests, sort_keys=False)
    formatted_yaml = yaml_str.replace("- name:", "\n- name:")

    path = base / f"{pipe_name}.yaml"
    with open(path, mode) as f:
        f.write(formatted_yaml)
    return path


def create_test(
    name_or_filename: str, prompt: str, project: Project, client: TinyB, preview: bool = False
) -> list[dict[str, Any]]:
    """
    Create a test for an existing pipe
    """
    tests: List[Dict[str, Any]] = []

    try:
        click.echo(FeedbackManager.highlight(message="\n» Building test environment"))
        build_error = build_project(project=project, tb_client=client, watch=False, silent=True, exit_on_error=False)
        if build_error:
            raise Exception(build_error)
        click.echo(FeedbackManager.info(message="✓ Done!\n"))
        config = CLIConfig.get_project_config()
        folder = project.folder
        pipe_path = get_pipe_path(name_or_filename, folder)
        pipe_name = pipe_path.stem
        click.echo(FeedbackManager.highlight(message=f"» Creating tests for {pipe_name} endpoint..."))
        pipe_content = pipe_path.read_text()
        pipe = client._req(f"/v0/pipes/{pipe_name}")
        parameters = set([param["name"] for node in pipe["nodes"] for param in node["params"]])

        system_prompt = test_create_prompt.format(
            name=pipe_name,
            content=pipe_content,
            parameters=parameters or "No parameters",
        )
        user_token = config.get_user_token()
        if not user_token:
            raise Exception("No user token found")

        llm = LLM(user_token=user_token, host=config.get_client().host)
        response_llm = llm.ask(system_prompt=system_prompt, prompt=prompt, feature="tb_test_create")
        response_xml = extract_xml(response_llm, "response")
        tests_content = parse_xml(response_xml, "test")

        for test_content in tests_content:
            test: Dict[str, Any] = {}
            test["name"] = extract_xml(test_content, "name")
            test["description"] = extract_xml(test_content, "description")
            parameters_api = extract_xml(test_content, "parameters")
            test["parameters"] = parameters_api.split("?")[1] if "?" in parameters_api else parameters_api
            test["expected_result"] = ""

            response = None
            try:
                response = get_pipe_data(client, pipe_name=pipe_name, test_params=test["parameters"])
            except Exception:
                pass

            if response:
                if response.status_code >= 400:
                    test["expected_http_status"] = response.status_code
                    test["expected_result"] = response.json()["error"]
                else:
                    test.pop("expected_http_status", None)
                    test["expected_result"] = response.text or ""

            tests.append(test)

        if not preview:
            if len(tests) > 0:
                generate_test_file(pipe_name, tests, folder, mode="a")
                for test in tests:
                    test_name = test["name"]
                    click.echo(FeedbackManager.info(message=f"✓ {test_name} created"))
            else:
                click.echo(FeedbackManager.info(message="* No tests created"))

            click.echo(FeedbackManager.success(message="✓ Done!\n"))
    except Exception as e:
        raise CLITestException(FeedbackManager.error(message=str(e)))
    finally:
        cleanup_test_workspace(client, project.folder)

    return tests


def parse_tests(tests_content: str) -> List[Dict[str, Any]]:
    return yaml.safe_load(tests_content)


def dump_tests(tests: List[Dict[str, Any]]) -> str:
    yaml_str = yaml.safe_dump(tests, sort_keys=False)
    return yaml_str.replace("- name:", "\n- name:")


def update_test(pipe: str, project: Project, client: TinyB) -> None:
    try:
        folder = project.folder
        click.echo(FeedbackManager.highlight(message="\n» Building test environment"))
        build_error = build_project(project=project, tb_client=client, watch=False, silent=True, exit_on_error=False)
        if build_error:
            raise Exception(build_error)

        click.echo(FeedbackManager.info(message="✓ Done!"))
        pipe_tests_path = get_pipe_path(pipe, folder)
        pipe_name = pipe_tests_path.stem
        if pipe_tests_path.suffix == ".yaml":
            pipe_name = pipe_tests_path.stem
        else:
            pipe_tests_path = Path("tests", f"{pipe_name}.yaml")

        click.echo(FeedbackManager.highlight(message=f"\n» Updating tests expectations for {pipe_name} endpoint..."))
        pipe_tests_path = Path(project.folder) / pipe_tests_path
        pipe_tests_content = parse_tests(pipe_tests_path.read_text())
        for test in pipe_tests_content:
            test_params = test["parameters"].split("?")[1] if "?" in test["parameters"] else test["parameters"]
            response = None
            try:
                response = get_pipe_data(client, pipe_name=pipe_name, test_params=test_params)
            except Exception:
                continue

            if response.status_code >= 400:
                test["expected_http_status"] = response.status_code
                test["expected_result"] = response.json()["error"]
            else:
                if "expected_http_status" in test:
                    del test["expected_http_status"]

                test["expected_result"] = response.text or ""

        generate_test_file(pipe_name, pipe_tests_content, folder)
        for test in pipe_tests_content:
            test_name = test["name"]
            click.echo(FeedbackManager.info(message=f"✓ {test_name} updated"))

        click.echo(FeedbackManager.success(message="✓ Done!\n"))
    except Exception as e:
        raise CLITestException(FeedbackManager.error(message=str(e)))
    finally:
        cleanup_test_workspace(client, project.folder)


def run_tests(name: Tuple[str, ...], project: Project, client: TinyB) -> Optional[str]:
    full_error = ""
    try:
        click.echo(FeedbackManager.highlight(message="\n» Building test environment"))
        build_error = build_project(project=project, tb_client=client, watch=False, silent=True, exit_on_error=False)
        if build_error:
            raise Exception(build_error)
        click.echo(FeedbackManager.info(message="✓ Done!"))

        click.echo(FeedbackManager.highlight(message="\n» Running tests"))
        paths = [Path(n) for n in name]
        endpoints = [f"{project.path}/tests/{p.stem}.yaml" for p in paths]
        test_files: List[str] = (
            endpoints if len(endpoints) > 0 else glob.glob(f"{project.path}/tests/**/*.y*ml", recursive=True)
        )

        def run_test(test_file) -> Tuple[Optional[str], int, int, bool]:
            test_file_path = Path(test_file)
            test_file_content = parse_tests(test_file_path.read_text())
            total_tests = len(test_file_content)

            # Check if pipe exists before processing any tests
            try:
                client._req(f"/v0/pipes/{test_file_path.stem}")
                click.echo(FeedbackManager.info(message=f"* {test_file_path.stem}{test_file_path.suffix}"))
            except Exception:
                # Entire test file skipped because pipe doesn't exist
                click.echo(FeedbackManager.info(message=f"* {test_file_path.stem}{test_file_path.suffix}"))
                click.echo(
                    FeedbackManager.warning(message=f"✗ All tests skipped ({test_file_path.stem}.pipe not found)")
                )
                return None, total_tests, total_tests, True  # True indicates file was skipped

            test_file_errors = ""
            skipped_count = 0

            for test in test_file_content:
                try:
                    test_params = test["parameters"].split("?")[1] if "?" in test["parameters"] else test["parameters"]
                    response = get_pipe_data(client, pipe_name=test_file_path.stem, test_params=test_params)

                    expected_result = response.text
                    if response.status_code >= 400:
                        expected_result = response.json()["error"]
                        if "expected_http_status" not in test:
                            raise Exception("Expected to not fail but got an error")
                        if test["expected_http_status"] != response.status_code:
                            raise Exception(f"Expected {test['expected_http_status']} but got {response.status_code}")

                    if test["expected_result"] != expected_result:
                        diff = difflib.ndiff(
                            test["expected_result"].splitlines(keepends=True), expected_result.splitlines(keepends=True)
                        )
                        printable_diff = "".join(diff)
                        raise Exception(
                            f"\nExpected: \n{test['expected_result']}\nGot: \n{expected_result}\nDiff: \n{printable_diff}"
                        )
                    click.echo(FeedbackManager.info(message=f"✓ {test['name']} passed"))
                except Exception as e:
                    test_file_errors += f"✗ {test['name']} failed\n** Output and expected output are different: \n{e}"
                    click.echo(FeedbackManager.error(message=test_file_errors))
                    return test_file_errors, skipped_count, total_tests, False
            return None, skipped_count, total_tests, False  # False indicates file was not skipped

        failed_tests_count = 0
        skipped_files_count = 0
        total_tests_count = 0
        test_count = len(test_files)
        output = ""
        for test_file in test_files:
            run_test_error, skipped_count, individual_tests_count, file_skipped = run_test(test_file)
            total_tests_count += individual_tests_count

            if file_skipped:
                skipped_files_count += 1
            elif run_test_error:
                full_error += f"\n{run_test_error}"
                failed_tests_count += 1

        runnable_files_count = test_count - skipped_files_count
        passed_files_count = runnable_files_count - failed_tests_count

        if failed_tests_count:
            error = f"\n✗ {passed_files_count}/{runnable_files_count} passed"
            if skipped_files_count > 0:
                error += f" ({skipped_files_count} skipped)"
            output += f"{error}\n"
            click.echo(FeedbackManager.error(message=error))
            sys_exit("test_error", full_error)
        else:
            if runnable_files_count == 0:
                success_message = "\n✓ No tests to run"
            else:
                success_message = f"\n✓ {runnable_files_count}/{runnable_files_count} passed"
            if skipped_files_count > 0:
                success_message += f" ({skipped_files_count} skipped)"
            message_color = FeedbackManager.success if runnable_files_count > 0 else FeedbackManager.warning
            click.echo(message_color(message=success_message))
            output += f"{success_message}\n"
        return output
    except Exception as e:
        raise CLITestException(FeedbackManager.error(message=str(e)))
    finally:
        cleanup_test_workspace(client, project.folder)


def get_pipe_data(client: TinyB, pipe_name: str, test_params: str) -> Response:
    pipe = client._req(f"/v0/pipes/{pipe_name}")
    output_node = next(
        (node for node in pipe["nodes"] if node["node_type"] != "default" and node["node_type"] != "standard"),
        {"name": "not_found"},
    )
    if output_node["node_type"] == "endpoint":
        return client._req_raw(f"/v0/pipes/{pipe_name}.ndjson?{test_params}")

    params = {
        "q": output_node["sql"],
        "pipeline": pipe_name,
    }
    return client._req_raw(f"""/v0/sql?{urllib.parse.urlencode(params)}&{test_params}""")


def get_pipe_path(name_or_filename: str, folder: str) -> Path:
    pipe_path: Optional[Path] = None

    if ".pipe" in name_or_filename:
        pipe_path = Path(name_or_filename)
        if not pipe_path.exists():
            pipe_path = None
    else:
        pipes = glob.glob(f"{folder}/**/{name_or_filename}.pipe", recursive=True)
        pipe_path = next((Path(p) for p in pipes if Path(p).exists()), None)

    if not pipe_path:
        raise Exception(f"Pipe {name_or_filename} not found")

    return pipe_path


def cleanup_test_workspace(client: TinyB, path: str) -> None:
    user_client = deepcopy(client)
    tokens = get_local_tokens()
    try:
        user_token = tokens["user_token"]
        user_client.token = user_token
        user_client.delete_workspace(get_test_workspace_name(path), hard_delete_confirmation="yes", version="v1")
    except Exception:
        pass
