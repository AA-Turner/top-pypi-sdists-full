import os
import pathlib
import re
import sys

from connector.oai.capability import StandardCapabilityName
from connector.oai.integration import Integration


def gather_cases(
    integration: Integration,
    capabilities_to_test: list[str] | None = None,
    tests_dir_path: pathlib.Path | None = None,
) -> list[str]:
    """
    Gather test cases for the given integration. Tries to discover test cases based on location of integration instance.
    Goes through all test files and checks if they are named within convention: test_{capability_name}_cases.py.
    Validates if all capabilities have corresponding test cases, if not, adds a coverage check.
    """
    if tests_dir_path is None:
        if not isinstance(integration.app_id, str):
            raise ValueError(
                "Integration app_id must be a string, please check your test_all_cases.py and consider using static paths in args to gather_cases."
            )

        module_path: str | None = None
        try:
            module = sys.modules[integration.app_id]
            if module and hasattr(module, "__file__"):
                module_path = module.__file__
        except Exception:
            """
            In case of no module access, try to get the folder of the caller via inspect
            This is used for example when you want to detach a single module and run
            it in a Docker container, without any of the other modules or actual module access.
            """
            import inspect

            caller_frame = inspect.currentframe()
            if caller_frame and caller_frame.f_back:
                caller_path = inspect.getfile(caller_frame.f_back)
                caller_folder = pathlib.Path(caller_path).resolve()
                if caller_folder:
                    module_path = str(caller_folder)

        if module_path:
            integration_path = pathlib.Path(module_path).parent.parent
            tests_dir_path = integration_path / "tests"
        else:
            raise ValueError(
                f"Could not find module path for {integration.app_id}, please check your test_all_cases.py and consider using static paths in args to gather_cases."
            )

    if capabilities_to_test is None:
        capabilities_to_test = [value for value in integration.capabilities.keys()]

    files = []
    for capability in capabilities_to_test:
        pattern = rf"test_(?:.+_)*?{capability}(?:_.+)*_cases.py"
        compiled = re.compile(pattern)
        matching_files = [
            file for file in tests_dir_path.rglob("*.py") if compiled.fullmatch(file.name)
        ]

        for file_path in matching_files:
            relative_path = file_path.relative_to(tests_dir_path)
            module_path = str(relative_path.with_suffix("")).replace(os.sep, ".")
            files.append(f"tests.{module_path}")

    has_full_coverage, missing_capabilities = calculate_coverage(integration, files)
    if not has_full_coverage:
        import connector.tests.coverage_check as coverage_check

        coverage_check.missing_capabilities = missing_capabilities
        coverage_check.integration_name = integration.app_id
        files.append("connector.tests.coverage_check")

    return files


def calculate_coverage(integration: Integration, cases: list[str]) -> tuple[bool, set[str]]:
    """
    Checks if all registered capabilities have corresponding test case files.
    Ignores system wide capabilities that have their own module and tests.
    """
    ignored_capabilities = [
        StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK,
        StandardCapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST,
        StandardCapabilityName.REFRESH_ACCESS_TOKEN,
        StandardCapabilityName.GET_AUTHORIZATION_URL,
        StandardCapabilityName.APP_INFO,
    ]
    capabilities_to_test = [
        value
        for value in integration.capabilities.keys()
        if value not in ignored_capabilities and value in [c.value for c in StandardCapabilityName]
    ]
    existing_capabilities = set(
        capability
        for file in cases
        for capability in capabilities_to_test
        if re.search(f"test_(?:.+_)*?{capability}(?:_.+)*_cases", file) is not None
    )
    required_capabilities = set(capability for capability in capabilities_to_test)
    missing_capabilities = required_capabilities - existing_capabilities

    coverage = len(existing_capabilities) / len(required_capabilities)
    return coverage >= 1, missing_capabilities
