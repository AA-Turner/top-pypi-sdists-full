import pytest
from pytest_mock import MockerFixture
from typing import Iterator

from dlt.common.configuration.specs.pluggable_run_context import RunContextBase

from dlthub.project.config.config import Project
from dlthub.project.exceptions import ProjectRunContextNotAvailable
from dlthub.project.project_context import ProjectRunContext

from dlt_plus_tests.utils import get_test_run_context


@pytest.fixture(autouse=True)
def auto_test_access_profile(
    dpt_project_context: ProjectRunContext, mocker: MockerFixture
) -> Iterator[None]:
    """Adds tests- to access profile returned by dlt package access_profile()"""
    mod_ = dpt_project_context.module
    if hasattr(mod_, "access_profile"):
        # mock so the real returned profile name has "tests-" string prefixed to it
        original_access_profile = mod_.access_profile
        mocker.patch.object(
            mod_,
            "access_profile",
            side_effect=lambda *args, **kwargs: "tests-" + original_access_profile(*args, **kwargs),
        )
    yield


@pytest.fixture
def dpt_project_context(dpt_run_context: RunContextBase) -> ProjectRunContext:
    ctx = get_test_run_context()
    if not isinstance(ctx, ProjectRunContext):
        raise ProjectRunContextNotAvailable(ctx.run_dir)
    # TODO: remove
    assert ctx.profile == "tests"
    return ctx


@pytest.fixture
def dpt_project_config(dpt_project_context: ProjectRunContext) -> Project:
    return dpt_project_context.project
