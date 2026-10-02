from enum import Enum
from importlib.metadata import version
import logging
import os
import shutil
from subprocess import Popen
import sys
import tempfile


logger = logging.getLogger(__name__)


class CloudEnvironment(Enum):
    AZURE_FUNCTION = "Azure Function"
    GOOGLE_CLOUD_RUN_FUNCTION_1ST_GEN = "Google Cloud Run Function 1st gen"
    GOOGLE_CLOUD_RUN_FUNCTION_2ND_GEN = "Google Cloud Run Function 2nd gen"
    UNKNOWN = "Unknown"


def get_environment():
    if (
        os.environ.get("FUNCTIONS_EXTENSION_VERSION") is not None
        and os.environ.get("FUNCTIONS_WORKER_RUNTIME") is not None
    ):
        return CloudEnvironment.AZURE_FUNCTION

    if os.environ.get("FUNCTION_NAME") is not None and os.environ.get("GCP_PROJECT") is not None:
        return CloudEnvironment.GOOGLE_CLOUD_RUN_FUNCTION_1ST_GEN

    if os.environ.get("K_SERVICE") is not None and os.environ.get("FUNCTION_TARGET") is not None:
        return CloudEnvironment.GOOGLE_CLOUD_RUN_FUNCTION_2ND_GEN

    return CloudEnvironment.UNKNOWN


def get_binary_path():
    # Use user defined path if provided
    binary_path = os.getenv("DD_SERVERLESS_COMPAT_PATH")

    if binary_path is not None:
        return binary_path

    binary_path_os_folder = os.path.join(
        os.path.dirname(__file__),
        "bin/windows-amd64" if sys.platform == "win32" else "bin/linux-amd64",
    )
    binary_extension = ".exe" if sys.platform == "win32" else ""
    binary_path = os.path.join(binary_path_os_folder, f"datadog-serverless-compat{binary_extension}")

    return binary_path


def get_package_version():
    try:
        package_version = version("datadog-serverless-compat")
    except Exception as e:
        logger.error(f"Unable to identify package version: {e}")
        package_version = "unknown"

    return package_version


def is_azure_flex_without_dd_azure_rg_env_var():
    return os.environ.get("WEBSITE_SKU") == "FlexConsumption" and os.environ.get("DD_AZURE_RESOURCE_GROUP") is None


def start():
    environment = get_environment()
    logger.debug(f"Environment detected: {environment.value}")

    if environment == CloudEnvironment.UNKNOWN:
        logger.error(
            f"{environment.value} environment detected, will not start the Datadog Serverless Compatibility Layer"
        )
        return

    logger.debug(f"Platform detected: {sys.platform}")

    if sys.platform not in {"win32", "linux"}:
        logger.error(
            f"Platform {sys.platform} detected, the Datadog Serverless Compatibility Layer is only supported"
            " on Windows and Linux"
        )
        return

    if environment == CloudEnvironment.AZURE_FUNCTION and is_azure_flex_without_dd_azure_rg_env_var():
        logger.error(
            "Azure function detected on flex consumption plan without DD_AZURE_RESOURCE_GROUP set."
            " Please set the DD_AZURE_RESOURCE_GROUP environment variable to your resource group name"
            " in Azure app settings. Shutting down Datadog Serverless Compatibility Layer."
        )
        return

    binary_path = get_binary_path()

    if not os.path.exists(binary_path):
        logger.error(f"Serverless Compatibility Layer did not start, could not find binary at path {binary_path}")
        return

    package_version = get_package_version()
    logger.debug(f"Found package version {package_version}")

    try:
        temp_dir = os.path.join(tempfile.gettempdir(), "datadog")
        os.makedirs(temp_dir, exist_ok=True)
        executable_file_path = os.path.join(temp_dir, os.path.basename(binary_path))
        shutil.copy2(binary_path, executable_file_path)
        os.chmod(executable_file_path, 0o744)
        logger.debug(f"Spawning process from binary at path {executable_file_path}")

        env = os.environ.copy()
        env["DD_SERVERLESS_COMPAT_VERSION"] = package_version
        Popen(executable_file_path, env=env)
    except Exception:
        logger.exception("An unexpected error occurred while spawning Serverless Compatibility Layer process")
