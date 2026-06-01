import importlib
import inspect
import pkgutil

from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.examples.all_workflows_worker import (
    SKIP_FILES,
    discover_all_workflows,
    is_workflow_class,
)


def test_discover_all_workflows() -> None:
    workflows = discover_all_workflows()

    assert len(workflows) > 0, "Should discover at least one workflow"

    workflow_names = []
    for workflow_class in workflows:
        assert hasattr(workflow_class, "__workflows_workflow_def"), (
            f"{workflow_class.__name__} should have workflow definition"
        )

        workflow_def = get_workflow_definition(workflow_class)
        assert workflow_def.name, f"{workflow_class.__name__} should have a name"
        workflow_names.append(workflow_def.name)

    assert len(workflow_names) == len(set(workflow_names)), (
        f"Duplicate workflow names detected: {[name for name in workflow_names if workflow_names.count(name) > 1]}"
    )


def test_discover_specific_workflows() -> None:
    workflows = discover_all_workflows()
    workflow_names = {get_workflow_definition(wf).name for wf in workflows}

    assert "example-hello-world-workflow" in workflow_names


def test_all_example_files_are_discovered() -> None:
    discovered_workflows = discover_all_workflows(include_on_behalf_of=True)
    discovered_modules = {wf.__module__ for wf in discovered_workflows}

    import mistralai.workflows.examples as examples_package

    missing_workflows: list[str] = []

    for _, modname, ispkg in pkgutil.iter_modules(examples_package.__path__, prefix="mistralai.workflows.examples."):
        if ispkg:
            continue

        base_name = modname.split(".")[-1]
        if base_name in SKIP_FILES:
            continue

        module = importlib.import_module(modname)
        has_workflow = any(is_workflow_class(obj) for _, obj in inspect.getmembers(module, inspect.isclass))

        if has_workflow and modname not in discovered_modules:
            missing_workflows.append(modname)

    assert not missing_workflows, (
        f"Example files with workflows not discovered by all_workflows_worker:\n"
        f"{', '.join(missing_workflows)}\n"
        f"Check discover_workflows_in_module() in all_workflows_worker.py"
    )


def test_excludes_on_behalf_of_by_default() -> None:
    workflows = discover_all_workflows()
    for workflow_class in workflows:
        workflow_def = get_workflow_definition(workflow_class)
        assert not workflow_def.on_behalf_of, (
            f"Workflow {workflow_def.name} has on_behalf_of=True but should be excluded by default"
        )


def test_includes_on_behalf_of_when_requested() -> None:
    workflows_without = discover_all_workflows(include_on_behalf_of=False)
    workflows_with = discover_all_workflows(include_on_behalf_of=True)

    assert len(workflows_with) >= len(workflows_without), (
        "Including on_behalf_of workflows should return at least as many workflows"
    )
