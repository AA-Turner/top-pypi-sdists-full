from subprocess import PIPE, Popen
from unittest.mock import patch

import pytest
from CTADIRAC.Core.Utilities.typer_callbacks import PRODUCTION_FIELDS
from CTADIRAC.ProductionSystem.scripts.cta_prod_get_all import (
    app,
    extract_user_name_from_dn,
    fill_columns,
)
from tests.unit.production import PRODUCTION_RESULTS
from typer.testing import CliRunner

runner = CliRunner()


def test_extract_user_name_from_dn():
    name = "Surname Lastname"
    dn = f"/O=GRID-FR/C=FR/O=CNRS/OU=LUPM/CN={name}"
    result = extract_user_name_from_dn(dn)
    assert result == name


def test_fill_columns():
    result = fill_columns(PRODUCTION_RESULTS[0], PRODUCTION_FIELDS, True)
    assert isinstance(result, list)


@pytest.fixture
def mock_production_client():
    with patch(
        "DIRAC.ProductionSystem.Client.ProductionClient.ProductionClient"
    ) as mock_client:
        yield mock_client


def test_main(mock_production_client):
    mock_client_instance = mock_production_client.return_value
    mock_client_instance.getProductions.return_value = {
        "OK": True,
        "Value": PRODUCTION_RESULTS,
    }

    result = runner.invoke(app, ["--long", "--cond", '{"Status": "Active"}'])
    assert result.exit_code == 0
    mock_client_instance.getProductions.assert_called_once_with(
        condDict={"Status": "Active"}
    )
    assert PRODUCTION_RESULTS[0]["AuthorGroup"] in result.stdout


PRODUCTION_CONFIG = """ProdSteps:
  - ID: 1
    input_meta_query:
      parentID:
      dataset:
    job_config:
      type: MCSimulation
      version: 2020-06-29b
      array_layout: Advanced-Baseline
      site: LaPalma
      particle: electron
      pointing_dir: North
      zenith_angle: 20
      n_shower: 100
      magic:
      sct:
      moon: dark
      start_run_number: 0

Common:
  MCCampaign: Prod5bTest
  configuration_id: 15
  base_path: /ctao/tests/prodsys/MC"""


def run_cli(cmd):
    """Run cli command"""
    cli = Popen([cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    cli.wait()
    return cli.communicate()


@pytest.mark.xfail(reason="Needs to be fixed.")
def test_cta_prod_submit(tmp_path):
    production_config = tmp_path / "production_config.yml"
    with open(production_config, "w") as f:
        f.write(PRODUCTION_CONFIG)
    script_name = "cta-prod-submit"
    prod_name = "cta_prod_submit_test"
    mode = "dry-run"

    cmd = f"{script_name} {prod_name} {production_config} {mode}"
    result = run_cli(cmd)
    output, err = result
    assert err.decode("utf-8") == ""


WORKFLOW_CONFIG = """MCCampaign: PROD6
site: LaPalma
input_array_layout: Prod6-Hyperarray
processing_array_layout: Alpha
zenith: 60.0
analysis_prog_version: v0.23.0
analysis_config_version: v1
configuration_id: 16
moon: dark
pointing: North"""


def test_cta_prod_create_workflow_config(tmp_path):
    workflow_config = tmp_path / "workflow_config.yml"
    with open(workflow_config, "w") as f:
        f.write(WORKFLOW_CONFIG)

    script_name = "cta-prod-create-workflow-config"

    cmd = f"{script_name} {workflow_config}"
    result = run_cli(cmd)
    output, err = result
    assert err.decode("utf-8") == ""
