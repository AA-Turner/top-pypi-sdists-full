import importlib
import os
import shutil
import sys
from pathlib import Path
from typing import cast
from unittest import mock

import pytest
import requests
from dagster import AssetsDefinition, materialize
from dagster._core.test_utils import environ
from dagster_cloud_cli.core.artifacts import (
    download_deployment_artifact,
    download_organization_artifact,
    upload_deployment_artifact,
    upload_organization_artifact,
)
from dagster_cloud_cli.entrypoint import app
from dagster_dbt import DbtCliResource, DbtProject
from dagster_dbt.cli.app import app as dagster_dbt_app
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture
def ci_env(agent_token):
    with environ(
        {
            "DAGSTER_CLOUD_ORGANIZATION": "acme",
            "DAGSTER_CLOUD_DEPLOYMENT": "prod",
            "DAGSTER_CLOUD_API_TOKEN": agent_token,
        }
    ):
        yield


@pytest.fixture
def mocked_dagit(dagit_test_client):
    with mock.patch(
        "dagster_cloud_cli.core.artifacts._dagster_cloud_http_client",
        return_value=dagit_test_client,
    ):
        yield


@pytest.fixture
def dbt_project_dir(tmp_path: Path) -> Path:
    dbt_project_dir = tmp_path.joinpath("test_jaffle_shop")
    shutil.copytree(src=Path(__file__).joinpath("..", "dbt_project").resolve(), dst=dbt_project_dir)

    return dbt_project_dir


def test_org_scoped(mocked_dagit, ci_env, tmp_path: Path):
    content = "yikes"
    origin_file = tmp_path.joinpath("origin.txt")
    origin_file.write_text(content)

    key = "o-artifact"

    upload_organization_artifact(key=key, path=origin_file)

    copy_path = tmp_path.joinpath("copy.txt")

    download_organization_artifact(key=key, path=copy_path)

    assert copy_path.read_text() == content
    with pytest.raises(requests.exceptions.HTTPError, match="404"):
        download_deployment_artifact(key=key, path=copy_path)


def test_deploy_scoped(mocked_dagit, ci_env, tmp_path: Path):
    content = "yikes"
    origin_file = tmp_path.joinpath("origin.txt")
    origin_file.write_text(content)

    key = "d-artifact"

    upload_deployment_artifact(key=key, path=origin_file)

    copy_path = tmp_path.joinpath("copy.txt")

    download_deployment_artifact(key=key, path=copy_path)

    assert copy_path.read_text() == content

    with pytest.raises(requests.exceptions.HTTPError, match="404"):
        download_organization_artifact(key=key, path=copy_path)


def test_missing_file(ci_env, tmp_path: Path):
    origin_file = tmp_path.joinpath("missing.txt")
    with pytest.raises(FileNotFoundError):
        upload_organization_artifact(key="the-artifact", path=origin_file)


def test_org_mismatch(mocked_dagit, tmp_path: Path, agent_token):
    with environ(
        {
            "DAGSTER_CLOUD_ORGANIZATION": "hooli",
            "DAGSTER_CLOUD_API_TOKEN": agent_token,  # acme token
        }
    ):
        content = "yikes"
        origin_file = tmp_path.joinpath("origin.txt")
        origin_file.write_text(content)

        key = "o-artifact"
        with pytest.raises(Exception, match="401"):
            upload_organization_artifact(key=key, path=origin_file)


def test_manage_state(
    monkeypatch: pytest.MonkeyPatch,
    mocked_dagit,
    agent_token: str,
    dbt_project_dir: Path,
    tmp_path: Path,
) -> None:
    project_name = "jaffle_dagster"
    dagster_project_dir = dbt_project_dir.joinpath(project_name)
    dbt_project_file_path = dagster_project_dir.joinpath(project_name, "project.py")

    monkeypatch.chdir(dbt_project_dir)
    sys.path.append(os.fspath(dbt_project_dir))

    monkeypatch.setenv("DAGSTER_CLOUD_ORGANIZATION", "acme")
    monkeypatch.setenv("DAGSTER_CLOUD_API_TOKEN", agent_token)

    # Scaffold the project
    result = runner.invoke(
        dagster_dbt_app,
        [
            "project",
            "scaffold",
            "--project-name",
            project_name,
            "--dbt-project-dir",
            os.fspath(dbt_project_dir),
            "--use-experimental-dbt-state",
        ],
    )
    assert result.exit_code == 0

    # Build the manifest
    result = runner.invoke(
        dagster_dbt_app,
        ["project", "prepare-and-package", "--file", os.fspath(dbt_project_file_path)],
    )

    assert result.exit_code == 0, result.output

    dagster_cloud_state_dir = tmp_path.joinpath("build")
    dagster_cloud_state_dir.mkdir()

    # prod ci run
    monkeypatch.setenv("DAGSTER_CLOUD_DEPLOYMENT", "prod")

    result = runner.invoke(
        app,
        [
            "ci",
            "init",
            "--statedir",
            os.fspath(dagster_cloud_state_dir),
            "--project-dir",
            os.fspath(dbt_project_dir),
        ],
    )
    assert result.exit_code == 0, result.output

    result = runner.invoke(
        app,
        [
            "ci",
            "dagster-dbt",
            "project",
            "manage-state",
            "--file",
            os.fspath(dbt_project_file_path),
            "--statedir",
            os.fspath(dagster_cloud_state_dir),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Upload complete" in result.output

    scaffold_defs_module = importlib.import_module(f"{project_name}.{project_name}.definitions")
    my_dbt_assets: AssetsDefinition = getattr(scaffold_defs_module, "jaffle_shop_dbt_assets")
    project = cast("DbtProject", getattr(scaffold_defs_module, "jaffle_shop_project"))
    dbt = DbtCliResource(project_dir=project)

    assert dbt.state_path

    # prod full materialization
    result = materialize([my_dbt_assets], resources={"dbt": dbt})
    assert result.success

    # branch ci run
    monkeypatch.setenv("DAGSTER_CLOUD_DEPLOYMENT", "staging")
    monkeypatch.setenv("DAGSTER_DBT_JAFFLE_SCHEMA", "staging")

    # Running in staging should fail because the state directory is empty, so there is no --defer.
    result = materialize(
        [my_dbt_assets], selection="orders", resources={"dbt": dbt}, raise_on_error=False
    )
    assert not result.success

    with mock.patch(
        "dagster_cloud_cli.commands.ci.create_or_update_deployment_from_context",
        return_value="branch-dep-name",
    ):
        result = runner.invoke(
            app,
            [
                "ci",
                "init",
                "--statedir",
                os.fspath(dagster_cloud_state_dir),
                "--project-dir",
                os.fspath(dbt_project_dir),
            ],
        )
        assert result.exit_code == 0, result.output

        result = runner.invoke(
            app,
            [
                "ci",
                "dagster-dbt",
                "project",
                "manage-state",
                "--file",
                os.fspath(dbt_project_file_path),
                "--statedir",
                os.fspath(dagster_cloud_state_dir),
            ],
        )
        assert result.exit_code == 0, result.output
        assert "Download complete" in result.output

    # Once the state directory is populated, the subselected asset can be produced.
    result = materialize([my_dbt_assets], selection="orders", resources={"dbt": dbt})
    assert result.success
