# mypy: disable-error-code="no-untyped-def"
import random
import string
from dataclasses import asdict

import pytest
from polars_cloud import ComputeContext, ComputeContextStatus, Workspace
from polars_cloud.polars_cloud import NotFoundError

from .conftest import ComputeContextSpecsInput  # noqa: TID252


@pytest.mark.parametrize(
    "specs_input",
    [
        pytest.param(
            ComputeContextSpecsInput(instance_type="t3.micro"),
            id="instance_type",
        ),
        pytest.param(
            ComputeContextSpecsInput(cpus=2, memory=2),
            id="specs",
        ),
    ],
)
def test_register_and_start(
    workspace: Workspace,
    specs_input: ComputeContextSpecsInput,
) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, **asdict(specs_input))
    ctx.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    ctx_from_name.start(wait=True)
    for key, _value in asdict(specs_input).items():
        assert getattr(ctx_from_name, key) == getattr(ctx, key)
    ctx_from_name.stop()


def test_register_upsert(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx2 = ComputeContext(workspace=workspace, instance_type="t3.small")
    ctx2.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    assert ctx_from_name.instance_type == "t3.small"


def test_register_and_unregister(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    ctx_from_name.unregister()

    with pytest.raises(NotFoundError):
        ctx_from_name = ComputeContext(workspace=workspace, name=name)


def test_get_and_stop(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    ctx_from_name = ComputeContext(workspace=workspace, name=name)
    ctx_from_name.start(wait=True)
    assert ctx_from_name.instance_type == "t3.micro"

    # Create a new context by name so it doesn't have a cached compute ID
    ctx_from_name2 = ComputeContext(workspace=workspace, name=name)
    assert ctx_from_name2.get_status() == ComputeContextStatus.IDLE
    ctx_from_name2.stop()


def test_get_status_manifest_new(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)

    assert ctx.get_status() == ComputeContextStatus.UNINITIALIZED


def test_get_status_manifest_inactive(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)
    ctx.start(wait=True)
    ctx.stop()

    assert ctx.get_status() == ComputeContextStatus.STOPPED


def test_stop_manifest_uninitialized(workspace: Workspace) -> None:
    name = "".join(random.choices(string.ascii_uppercase, k=7))
    ctx = ComputeContext(workspace=workspace, instance_type="t3.micro")
    ctx.register(name)
    with pytest.raises(RuntimeError, match="nothing to stop"):
        ctx.stop()
