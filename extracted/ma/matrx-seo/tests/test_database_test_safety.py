"""Guard against ordinary SEO checks connecting with inherited production credentials."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from psycopg.conninfo import conninfo_to_dict
from seo_contract_database import UnsafeContractDatabase, contract_database_dsn

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOCAL = "host=127.0.0.1 port=55441 dbname=matrx_seo_contract_guard user=guard password=local-only"


@pytest.mark.parametrize(
    "raw",
    [
        "",
        "host=db.matrxserver.com port=5432 dbname=postgres user=guard password=local-only",
        LOCAL.replace("127.0.0.1", "localhost"),
        LOCAL.replace("127.0.0.1", "127.0.0.1,db.matrxserver.com"),
        LOCAL.replace("matrx_seo_contract_guard", "postgres"),
        LOCAL.replace("55441", "543"),
        LOCAL.replace("55441", "65536"),
        LOCAL.replace("55441", "invalid"),
        LOCAL.replace(" password=local-only", ""),
        LOCAL + " hostaddr=203.0.113.2",
        LOCAL + " service=production",
        LOCAL + " options='-c search_path=public'",
        "malformed connection",
    ],
)
def test_unsafe_target_is_refused_without_platform_fallback(monkeypatch, raw):
    monkeypatch.setenv("SUPABASE_MATRIX_HOST", "db.matrxserver.com")
    monkeypatch.setenv("MATRX_SEO_CONTRACT_TEST_DSN", raw)
    with pytest.raises(UnsafeContractDatabase):
        contract_database_dsn()


@pytest.mark.parametrize("host", ["127.0.0.1", "::1"])
def test_loopback_target_overrides_libpq_routing_defaults(monkeypatch, host):
    monkeypatch.setenv("MATRX_SEO_CONTRACT_TEST_DSN", LOCAL.replace("127.0.0.1", host))
    monkeypatch.setenv("PGHOSTADDR", "203.0.113.2")
    monkeypatch.delenv("PGSERVICE", raising=False)
    params = conninfo_to_dict(contract_database_dsn())
    assert params["host"] == host
    assert params["hostaddr"] == host
    assert "service" not in params
    assert params["port"] == "55441"
    assert params["dbname"] == "matrx_seo_contract_guard"
    assert params["connect_timeout"] == "5"
    assert params["sslmode"] == "disable"


def _pytest(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.pop("MATRX_SEO_CONTRACT_TEST_DSN", None)
    return subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=90,
    )


def test_non_live_selection_deselects_all_four_contract_suites():
    paths = [
        str(HERE / name)
        for name in (
            "test_topical_map_door_contract.py",
            "test_site_door_access_before_existence.py",
            "test_seo_map_door_rules_generated.py",
            "test_seo_access_door_rules_generated.py",
        )
    ]
    result = _pytest(*paths, "-m", "not live", "--collect-only", "-q")
    assert result.returncode == 0, result.stdout + result.stderr
    nodes = [line for line in result.stdout.splitlines() if "::test_" in line]
    assert len(nodes) == 2
    assert all(line.endswith("::test_every_declared_entity_argument_is_covered") for line in nodes)
    assert "deselected" in result.stdout


def test_selected_contract_requires_authorization_before_database_fixture():
    result = _pytest(
        str(HERE / "test_topical_map_door_contract.py"),
        "-k",
        "door_rows_declare",
        "-q",
    )
    assert result.returncode == 4, result.stdout + result.stderr
    assert "without --run-seo-database-tests" in result.stderr
    assert "UnsafeContractDatabase" not in result.stdout  # no fixture ran


def test_mixed_budget_selection_keeps_offline_checks_and_excludes_database_tests():
    result = _pytest(str(HERE / "test_budget.py"), "-m", "not live", "--collect-only", "-q")
    assert result.returncode == 0, result.stdout + result.stderr
    nodes = [line for line in result.stdout.splitlines() if "::test_" in line]
    assert nodes
    assert not any("live" in line for line in nodes)
    assert "deselected" in result.stdout


def test_inherited_libpq_service_is_refused_before_connect(monkeypatch):
    monkeypatch.setenv("MATRX_SEO_CONTRACT_TEST_DSN", LOCAL)
    monkeypatch.setenv("PGSERVICE", "production")
    with pytest.raises(UnsafeContractDatabase, match="Clear inherited PGSERVICE"):
        contract_database_dsn()


def test_nightly_caller_routes_seo_offline_and_preserves_other_scopes(tmp_path):
    # Execute the actual workflow shell; substitute only its external test runner.
    import json

    import yaml

    workflow = yaml.safe_load((ROOT / ".github/workflows/test.yml").read_text())
    steps = [step for job in workflow["jobs"].values() for step in job.get("steps", [])]
    script = next(
        step["run"]
        for step in steps
        if step.get("name") == "Run the previously-uncovered suite inventory"
    )
    calls = tmp_path / "calls.jsonl"
    runner = tmp_path / "uv"
    runner.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "with open(os.environ['SEO_TEST_CALL_LOG'], 'a') as stream:\n"
        "    stream.write(json.dumps(sys.argv[1:]) + '\\n')\n"
    )
    runner.chmod(0o700)
    env = {
        **os.environ,
        "PATH": str(tmp_path) + os.pathsep + os.environ["PATH"],
        "SEO_TEST_CALL_LOG": str(calls),
    }
    result = subprocess.run(
        ["bash", "-c", script], env=env, capture_output=True, text=True, timeout=15
    )
    assert result.returncode == 0, result.stdout + result.stderr
    observed = [json.loads(line) for line in calls.read_text().splitlines()]
    seo = [args for args in observed if "packages/matrx-seo" in args]
    assert len(seo) == 1
    assert "not live" in seo[0]
    assert "--run-seo-database-tests" not in seo[0]
    others = [args for args in observed if "packages/matrx-seo" not in args]
    assert len(others) == 12
    assert all("not live" not in args for args in others)
