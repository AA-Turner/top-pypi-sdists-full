"""Tests for boundary discovery — `efterlev boundary discover`.

Reconnaissance over Terraform: surface candidate in-boundary dependencies
(external providers, cross-account refs, remote state, SaaS endpoints, external
data sources). Deterministic, no LLM, no network, no writes.
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from efterlev.boundary_discovery import discover_boundary_signals
from efterlev.cli.main import app

runner = CliRunner()

_RICH_TF = """\
terraform {
  backend "s3" {
    bucket = "tfstate"
    key    = "prod/terraform.tfstate"
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "logging"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::222222222222:role/logging"
  }
}

provider "datadog" {
  api_key = "x"
}

data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "tfstate"
    key    = "network/terraform.tfstate"
  }
}

data "http" "ip" {
  url = "https://checkip.amazonaws.com"
}

resource "aws_iam_role" "app" {
  name               = "app"
  assume_role_policy = "{}"
  tags = {
    owner_arn = "arn:aws:iam::111111111111:role/admin"
    dd_site   = "datadoghq.com"
  }
}
"""

_CLEAN_TF = """\
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "my-self-contained-bucket"
}
"""


def _write(tmp_path: Path, body: str) -> Path:
    (tmp_path / "main.tf").write_text(body)
    return tmp_path


def test_discovers_each_signal_category(tmp_path: Path) -> None:
    signals = discover_boundary_signals(_write(tmp_path, _RICH_TF))
    cats = {s.category for s in signals}
    assert cats == {
        "external-provider",
        "cross-account",
        "remote-state",
        "saas-endpoint",
        "external-data",
    }
    titles = " | ".join(s.title for s in signals)
    assert "Datadog" in titles
    assert "distinct AWS account IDs" in titles  # 111… + 222…
    assert "Multi-account AWS provider" in titles  # alias + assume_role
    assert "Remote state backend (s3)" in titles
    assert "another Terraform stack's state" in titles  # terraform_remote_state
    assert "data.http.ip" in titles


def test_signals_carry_file_line_locations(tmp_path: Path) -> None:
    signals = discover_boundary_signals(_write(tmp_path, _RICH_TF))
    dd = next(s for s in signals if "Datadog (monitoring)" in s.title)
    assert dd.locations and all(loc.startswith("main.tf:") for loc in dd.locations)


def test_clean_workspace_has_no_signals(tmp_path: Path) -> None:
    assert discover_boundary_signals(_write(tmp_path, _CLEAN_TF)) == []


def test_single_account_is_not_flagged_cross_account(tmp_path: Path) -> None:
    body = (
        'resource "aws_iam_role" "a" {\n'
        '  name = "a"\n'
        '  tags = { arn = "arn:aws:iam::111111111111:role/x" }\n'
        "}\n"
    )
    signals = discover_boundary_signals(_write(tmp_path, body))
    assert not any(s.category == "cross-account" for s in signals)


def test_non_directory_returns_empty(tmp_path: Path) -> None:
    assert discover_boundary_signals(tmp_path / "nope") == []


def test_compact_backend_caught_but_attribute_not_false_positive(tmp_path: Path) -> None:
    # compact single-line terraform{} block should still flag the remote backend;
    # the `backend = "s3"` *attribute* inside a remote-state config must NOT.
    body = (
        'terraform { backend "s3" { bucket = "x" } }\n'
        'data "terraform_remote_state" "n" { backend = "s3" }\n'
    )
    signals = discover_boundary_signals(_write(tmp_path, body))
    backends = [s for s in signals if s.title.startswith("Remote state backend")]
    assert len(backends) == 1 and "(s3)" in backends[0].title


def test_cli_human_output(tmp_path: Path) -> None:
    _write(tmp_path, _RICH_TF)
    result = runner.invoke(app, ["boundary", "discover", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "Boundary reconnaissance" in result.output
    assert "Datadog" in result.output
    # the honesty posture must be present: reconnaissance, not a decision
    assert "candidates, not a boundary" in result.output
    assert "efterlev boundary set" in result.output


def test_cli_json_output(tmp_path: Path) -> None:
    _write(tmp_path, _RICH_TF)
    result = runner.invoke(app, ["boundary", "discover", "--target", str(tmp_path), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert isinstance(data, list) and data
    assert {"category", "title", "detail", "locations"} <= set(data[0])


def test_cli_clean_workspace_message(tmp_path: Path) -> None:
    _write(tmp_path, _CLEAN_TF)
    result = runner.invoke(app, ["boundary", "discover", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert "no external-dependency signals" in result.output
