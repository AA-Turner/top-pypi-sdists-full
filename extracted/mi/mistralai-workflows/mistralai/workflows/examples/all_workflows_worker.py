import argparse
import asyncio
import importlib
import inspect
import pkgutil
import sys
from typing import Type

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)

SKIP_FILES = {
    "__init__",
    "worker_example",
    "all_workflows_worker",
    "old_workflow_insurance_claims",
    "old_workflow_multi_turn_chat",
}


def is_workflow_class(obj: object) -> bool:
    return hasattr(obj, "__workflows_workflow_def")


def discover_workflows_in_module(module_name: str) -> list[Type]:
    workflow_classes = []

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
    include_on_behalf_of: bool = False,
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
                if not include_on_behalf_of and workflow_def.on_behalf_of:
                    continue
                seen_workflow_names.add(workflow_def.name)
                all_workflows.append(workflow_class)

    logger.info("Scanning package for workflows", package=package_name)
    scan_package(package_name)
    return all_workflows


def discover_all_workflows(include_on_behalf_of: bool = False) -> list[Type]:
    packages_to_scan = [
        "mistralai.workflows.examples",
        "mistralai.workflows.plugins.webhook.examples",
        "mistralai.workflows.plugins.mistralai.connectors.examples",
    ]
    all_workflows: list[Type] = []
    seen_names: set[str] = set()

    for package in packages_to_scan:
        for workflow_class in discover_all_workflows_in_package(
            package, skip_modules=SKIP_FILES, include_on_behalf_of=include_on_behalf_of
        ):
            workflow_def = get_workflow_definition(workflow_class)
            if workflow_def.name in seen_names:
                logger.warning(
                    "Skipping duplicate workflow across packages",
                    workflow_name=workflow_def.name,
                    workflow_class=workflow_class.__name__,
                    package=package,
                )
                continue
            seen_names.add(workflow_def.name)
            all_workflows.append(workflow_class)

    return all_workflows


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run all example workflows worker")
    parser.add_argument(
        "--include-on-behalf-of",
        action="store_true",
        help="Include workflows with on_behalf_of=True (excluded by default)",
    )
    args = parser.parse_args()

    logger.info("Starting workflow discovery...")

    discovered_workflows = discover_all_workflows(include_on_behalf_of=args.include_on_behalf_of)

    if not discovered_workflows:
        logger.error("No workflows discovered")
        sys.exit(1)

    logger.info(
        "Workflow discovery complete",
        total_workflows=len(discovered_workflows),
        workflows=[get_workflow_definition(wf).name for wf in discovered_workflows],
    )

    logger.info("Starting worker...")
    await workflows.run_worker(discovered_workflows)


if __name__ == "__main__":
    asyncio.run(main())
