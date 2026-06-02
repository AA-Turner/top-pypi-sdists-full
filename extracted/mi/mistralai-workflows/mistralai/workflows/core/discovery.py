import importlib
import inspect
import pkgutil
from typing import Type

import structlog

from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

logger = structlog.get_logger(__name__)


def is_workflow_class(obj: object) -> bool:
    return hasattr(obj, "__workflows_workflow_def")


def discover_workflows_in_module(module_name: str) -> list[Type]:
    workflow_classes: list[Type] = []

    try:
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if is_workflow_class(obj):
                try:
                    workflow_def = get_workflow_definition(obj)
                    logger.info(
                        "Discovered workflow",
                        workflow_class=name,
                        workflow_name=workflow_def.name,
                        module=module_name,
                    )
                    workflow_classes.append(obj)
                except Exception as e:
                    logger.warning(
                        "Failed to get workflow definition",
                        workflow_class=name,
                        module=module_name,
                        error=str(e),
                    )
    except Exception as e:
        logger.warning("Failed to import module", module=module_name, error=str(e))

    return workflow_classes


def discover_all_workflows_in_package(
    package_name: str,
    skip_modules: set[str] | None = None,
) -> list[Type]:
    all_workflows: list[Type] = []
    seen_workflow_names: set[str] = set()
    _skip = skip_modules or set()

    def scan_package(pkg_name: str) -> None:
        try:
            pkg = importlib.import_module(pkg_name)
        except ImportError as e:
            logger.error("Failed to import package", package=pkg_name, error=str(e))
            return

        if not hasattr(pkg, "__path__"):
            logger.error("Package has no __path__ attribute", package=pkg_name)
            return

        for _, modname, ispkg in pkgutil.iter_modules(pkg.__path__, prefix=f"{pkg_name}."):
            base_name = modname.split(".")[-1]
            if base_name in _skip:
                continue

            if ispkg:
                scan_package(modname)
                continue

            logger.debug("Scanning module for workflows", module=modname)
            for workflow_class in discover_workflows_in_module(modname):
                workflow_def = get_workflow_definition(workflow_class)
                if workflow_def.name in seen_workflow_names:
                    logger.warning(
                        "Skipping duplicate workflow",
                        workflow_name=workflow_def.name,
                        workflow_class=workflow_class.__name__,
                        module=modname,
                    )
                    continue
                seen_workflow_names.add(workflow_def.name)
                all_workflows.append(workflow_class)

    logger.info("Scanning package for workflows", package=package_name)
    scan_package(package_name)
    return all_workflows
