import importlib
import json
import os
import re
import sys
import time
from typing import List, Optional

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent"))
import coverage
from agent.agent_config import AgentConfig
from agent.footprints import FootprintModel
from agent.logging import debug, error, info, warn

PYTHON_FILES_REG = r".*\.pyw?$"
cov = coverage.Coverage(data_file="/tmp/.coverage", config_file=False)
sys.path.append(os.getcwd())


def lambda_handler(event, context):
    debug("Debug mode is on")
    # Get the original handler function from the environment variable
    orig_lambda_handler = os.environ.get("ORIG_NAME", "")
    debug(f"Original handler to run is: {orig_lambda_handler}")
    parts = orig_lambda_handler.replace("/", ".").split(".")
    if len(parts) < 2:
        error(f"Invalid handler format: {orig_lambda_handler}")
        raise ValueError("Invalid handler format")

    # The module path is everything except the last part
    module_path = ".".join(parts[:-1])
    # The function name is the last part
    function_name = parts[-1]

    try:
        # First, try to import as is (handles 'api.app.lambda_handler' case)
        debug(f"Attempting to import module of original handler: {module_path}")
        orig_module = importlib.import_module(module_path)
    except ImportError as e:
        error(
            f"Failed to import original lambda handler module{module_path}. Error: {e}. Trying alternative import method..."
        )
        # If that fails, try treating it as a file path (handles 'api/app.lambda_handler' case)
        try:
            sys.path.append(os.path.dirname(module_path.replace(".", "/")))
            orig_module = importlib.import_module(os.path.basename(module_path))
        except ImportError as e2:
            error(
                f"Second alternative failed to import {module_path}. Error: {e2}. check the handler path and make sure it is correct."
            )
            raise

    debug(f"Successfully imported module: {orig_module}")

    try:
        # Get the handler function
        orig_function = getattr(orig_module, function_name)
    except AttributeError as e:
        error(
            f"Failed to get function {function_name} from module {module_path}. Error: {e}"
        )
        raise
    agent_config = None
    build_digest: dict[str, dict[int, str]] = {}
    proxy_url = os.environ.get("SL_PROXY", "")
    token = os.environ.get("SL_TOKEN", "")
    try:
        config_data = config_loader()
        token = config_data.get("token", token)
        agent_config = AgentConfig(config_data)
        agent_config.validate()
        build_digest = load_build_digest_from_json(config_data)
        info("Sealights lambda wrapper handler loaded successfully")
    except Exception as e:
        error(
            f"Failed to to load Sealights configuration: {e}, Sealights coverage will be disabled, but the original lambda function will still run"
        )
        return run_original_lambda_handler(orig_function, event, context)

    enable_reporting = to_report(agent_config, proxy_url, token)
    if not enable_reporting:
        info("Sealights execution is not opened, skipping Sealights Coverage")
        return run_original_lambda_handler(orig_function, event, context)

    debug("Starting Sealights Coverage")

    try:
        cov.start()
        start_time = int(time.time())
        lambda_response = orig_function(event, context)
    finally:
        debug("Stopping Sealights Coverage")
        cov.stop()
        end_time = int(time.time())

    info("Getting Sealights Footprints")
    try:
        coverage_data = cov.get_data()
    except Exception as e:
        error(f"Failed to get coverage data: {e}")
        return lambda_response
    footprints = get_footprints_from_coverage(coverage_data, build_digest)
    footprints_length = len(footprints)
    if footprints_length == 0:
        warn("No footprints found, skipping Sealights Footprints report")
        return lambda_response
    else:
        info(f"Found {footprints_length} footprints")
    debug("Creating Sealights Footprint Model")
    try:
        fm = FootprintModel(
            agent_config=agent_config,
            methods=footprints,
            start_time=start_time,
            end_time=end_time,
        )
    except Exception as e:
        error(f"Failed to create Sealights Footprint Model: {e}")
        return lambda_response
    info("Posting Sealights Footprints started")
    try:
        fm.send_collector(agent_config, proxy_url, token)
    except Exception as e:
        error(f"Failed to post Sealights Footprints to collector: {e}")
        return lambda_response
    info("Posting Sealights Footprints completed")
    try:
        cov.erase()
    except Exception as e:
        error(f"Failed to erase coverage data: {e}")
    info("Finished Sealights lambda wrapper handler")
    return lambda_response


def run_original_lambda_handler(orig_function, event, context):
    debug("Original lambda function starting")
    try:
        lambda_response = orig_function(event, context)
    except Exception as e:
        error(
            f"Client's lambda function threw an unhandled exception: {e}, raising client's exception"
        )
        raise
    debug("Original lambda function returned")
    return lambda_response


def config_loader() -> dict:
    """
    This function is used to load the Sealights configuration from a JSON file.

    :return: The loaded configuration data as a dictionary.
    :rtype: dict
    """
    debug("Loading Sealights Configuration")
    file_name = "sl_lambda_config.json"

    def find_file(start_path):
        for root, dirs, files in os.walk(start_path):
            if file_name in files:
                return os.path.join(root, file_name)
        return None

    # First, try to find the file in the current directory
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)

    if not os.path.exists(file_path):
        # If not found in current directory, search recursively from the root
        root_dir = "/"
        file_path = find_file(root_dir)

    if file_path is None:
        raise FileNotFoundError(f"'{file_name}' not found in any directory")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"Failed to load config from {file_path}: {e}")

    return data


def get_top_relative_path(filepath):
    """
    Function to get the top relative path for a given file path.

    :param filepath: The path of the file for which the top relative path needs to be obtained.
    :return: The top relative path of the given file path.

    This function takes in a file path as input and returns the top relative path of the file with respect to the current working directory. It uses the os module to calculate the relative path and replaces any backslashes with forward slashes to ensure consistency in the path.
    """
    return os.path.relpath(filepath, os.getcwd()).replace("\\", "/")


def load_build_digest_from_json(data) -> dict[str, dict[int, str]]:
    """
    Load Build Digest from JSON

    :param data: The JSON data containing the build digest information.
    :return: A dictionary representing the build digest, with file paths as keys and a nested dictionary of line numbers and methods as values.

    This function takes in a dictionary of JSON data and retrieves the build digest from the "buildDigest" key. It then iterates through each file path and its corresponding methods, storing the line numbers and associated methods in a nested dictionary structure.

    If any errors occur during the process, a ValueError exception is raised with an appropriate error message.

    If no build digest is found in the JSON data, a ValueError is raised, suggesting to re-run the "sl-python configlambda" command to generate a new build digest.

    Example usage:
    ```
    data = {
        "buildDigest": {
            "file1.py": {
                "method1": [1, 2, 3],
                "method2": [4, 5]
            },
            "file2.py": {
                "method3": [10, 11],
                "method4": [12]
            }
        }
    }

    result = load_build_digest_from_json(data)
    print(result)
    # Output: {'file1.py': {1: 'method1', 2: 'method1', 3: 'method1', 4: 'method2', 5: 'method2'}, 'file2.py': {10: 'method3', 11: 'method3', 12: 'method4'}}
    ```
    """
    debug("Loading Sealights Build Digest")
    try:
        build_digest = data.get("buildDigest", {})
        file_lines_methods: dict[str, dict[int, str]] = {}
        for file_path, methods in build_digest.items():
            lines_methods: dict[int, str] = {}
            for method, lines in methods.items():
                debug(
                    f"File: {file_path} Method: {method} Line: {lines} to file {file_path}"
                )
                for line in lines:
                    lines_methods[line] = method
            file_lines_methods[file_path] = lines_methods
    except Exception as e:
        raise ValueError(f"Failed to load build digest from json: {e}")
    if not file_lines_methods:
        raise ValueError(
            "No build digest found in json, re-run sl-python configlambda command to generate a new build digest."
        )
    return file_lines_methods


def get_footprints_from_coverage(
    coverage_data: coverage.CoverageData, build_digest: dict[str, dict[int, str]]
) -> dict[str, List[int]]:
    """
    Function Name: get_footprints_from_coverage

    Parameters:
    - coverage_data: An object of type coverage.CoverageData that contains coverage information for the measured files.
    - build_digest: A dictionary of type dict[str, dict[int, str]] that represents the build digest containing file information.

    Return:
    - A dictionary of type dict[str, List[int]] that contains the footprints of covered lines in the measured files.

    Description:
    This function takes the coverage data and build digest as input and returns a dictionary that maps unique identifiers (unique_id) to a list of covered line numbers. It iterates through the files in the coverage data and checks if the file is a Python file using a regular expression. It then retrieves the relative path of the file and looks for its corresponding digest in the build digest. If the digest is found, it retrieves the covered lines from the coverage data and maps them to the unique_id in the footprints dictionary. If a line is covered but not found in the build digest, a warning message is logged indicating that the line will not be reported. Finally, the function returns the footprints dictionary.

    Note:
    - This function requires the `coverage` module to be installed.
    - The `build_digest` parameter should be a dictionary where the keys are relative file paths and the values are dictionaries mapping line numbers to unique identifiers.
    - The function internally uses the following helper functions: `get_top_relative_path` to get the relative path of a file, `debug` to log debug messages, and `warn` to log warning messages.

    Example Usage:
    ```python
    import coverage

    # Create a CoverageData object
    coverage_data = coverage.CoverageData()

    # Load coverage data from file
    coverage_data.read_file("coverage_file.txt")

    # Create a build digest
    build_digest = {
        "path/to/file.py": {
            1: "unique_id_1",
            2: "unique_id_2",
            # ...
        },
        "path/to/another_file.py": {
            1: "unique_id_3",
            2: "unique_id_4",
            # ...
        },
        # ...
    }

    # Get footprints from coverage
    footprints = get_footprints_from_coverage(coverage_data, build_digest)

    # Print the footprints
    for unique_id, lines in footprints.items():
        print(f"Unique ID: {unique_id}, Covered Lines: {lines}")
    ```
    """
    footprints = {}
    for filename in coverage_data.measured_files():
        if not re.match(PYTHON_FILES_REG, os.path.split(filename)[1]):
            continue
        relative_path = get_top_relative_path(filename).replace("\\", "/")
        file_digest: dict[int, str] = build_digest.get(relative_path)
        if not file_digest:
            debug(f"File {relative_path} not found in build digest, skipping")
            continue
        covered_lines = coverage_data.lines(filename)
        for line in covered_lines:
            unique_id = file_digest.get(int(line))
            if unique_id:
                if unique_id not in footprints:
                    footprints[unique_id] = [line]
                else:
                    footprints[unique_id].append(line)
            else:
                warn(
                    f"Line {line} in file {relative_path} was covered but not found in build digest thus will not be reported, re-run sl-python configlambda command to generate a new build digest."
                )
    return footprints


def to_report(
    agent_config: AgentConfig, proxy: Optional[str] = None, token: Optional[str] = None
) -> bool:
    import requests

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{agent_config.collectorUrl}/api/v4/testExecution/{agent_config.labId}"
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        debug(f"Checking if execution is opened with url: {url}")
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code != 200:
            error(
                f"Failed to check execution status: {response.text}. not allowing to report"
            )
            return False
        data = response.json()
        execution = data.get("execution")
        if execution is None:
            debug("No execution found, not allowing to report")
            return False
        status = execution.get("status")
        debug(f"Execution status is: {status}")
        if status == "created":
            debug("Execution was created, allowing to report")
            return True
        debug("Execution is not created, not allowing to report")
        return False

    except Exception as e:
        error(f"Failed to check execution status: {e}. not allowing to report")
        return False
