import importlib.resources
from pathlib import Path

# datahub-executor bakes (and compose hot-mounts) GMS configuration YAMLs here,
# next to ingestion-pipeline-config.yaml. Prefer this path so image/package
# symlinks into metadata-service/ need not resolve inside the container.
EXECUTOR_CONFIG_DIR = Path("/etc/datahub-executor")

PERIODIC_ANALYTICS_PACKAGE = "acryl_datahub_cloud.periodic_analytics"
REGISTRIES_PACKAGE_DIR = "registries"


def read_config_yaml(name: str) -> str:
    mounted = EXECUTOR_CONFIG_DIR / name
    if mounted.is_file():
        return mounted.read_text()
    package = (
        importlib.resources.files(PERIODIC_ANALYTICS_PACKAGE) / REGISTRIES_PACKAGE_DIR
    )
    return (package / name).read_text()
