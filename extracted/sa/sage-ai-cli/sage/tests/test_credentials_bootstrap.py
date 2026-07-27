"""Tests for secure credential bootstrap helpers."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace


def test_parse_env_file_handles_export_and_quotes(tmp_path: Path):
    from sage.core.credentials import parse_env_file

    env_file = tmp_path / ".env"
    env_file.write_text(
        "export SIMPLE=value\n"
        'QUOTED="hello world"\n'
        "SINGLE='quoted'\n"
        "# comment\n",
        encoding="utf-8",
    )

    values = parse_env_file(env_file)

    assert values == {
        "SIMPLE": "value",
        "QUOTED": "hello world",
        "SINGLE": "quoted",
    }


def test_load_project_env_files_prefers_project_over_home_but_not_real_env(
    tmp_path: Path,
    monkeypatch,
):
    import sage.core.credentials as credentials

    home_env = tmp_path / "home.env"
    home_env.write_text("API_KEY=home\nSHARED=home\nHOME_ONLY=1\n", encoding="utf-8")
    project_env = tmp_path / ".env"
    project_env.write_text("SHARED=project\nPROJECT_ONLY=1\n", encoding="utf-8")

    monkeypatch.setattr(credentials, "HOME_ENV_PATH", home_env)
    monkeypatch.setenv("API_KEY", "real-shell")
    monkeypatch.delenv("SHARED", raising=False)
    monkeypatch.delenv("HOME_ONLY", raising=False)
    monkeypatch.delenv("PROJECT_ONLY", raising=False)

    loaded = credentials.load_project_env_files(tmp_path)

    assert str(home_env) in loaded
    assert str(project_env) in loaded
    assert credentials.os.environ["API_KEY"] == "real-shell"
    assert credentials.os.environ["SHARED"] == "project"
    assert credentials.os.environ["HOME_ONLY"] == "1"
    assert credentials.os.environ["PROJECT_ONLY"] == "1"


def test_bootstrap_project_credentials_generates_secret_and_sqlite_env(tmp_path: Path):
    from sage.core.credentials import bootstrap_project_credentials, parse_env_file

    app_py = tmp_path / "app.py"
    app_py.write_text(
        'import os\n'
        'DATABASE_URL = os.environ.get("DATABASE_URL")\n'
        'APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")\n',
        encoding="utf-8",
    )
    (tmp_path / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")

    result = bootstrap_project_credentials(tmp_path, "Set up secrets and database url")

    values = parse_env_file(tmp_path / ".env")
    example = parse_env_file(tmp_path / ".env.example")
    gitignore = (tmp_path / ".gitignore").read_text("utf-8")

    assert "DATABASE_URL" in values
    assert "APP_SECRET_KEY" in values
    assert values["DATABASE_URL"].startswith("sqlite:///")
    assert result.sqlite_database_path is not None
    assert result.sqlite_database_path.exists()
    assert example["DATABASE_URL"] == ""
    assert example["APP_SECRET_KEY"] == ""
    assert ".env" in gitignore
    assert ".env.local" in gitignore
    assert "!.env.example" in gitignore
    assert "DATABASE_URL" in result.prompt_summary()
    assert values["APP_SECRET_KEY"] not in result.prompt_summary()


def test_bootstrap_imports_config_api_keys_but_does_not_fabricate_missing_external(
    tmp_path: Path,
):
    from sage.core.credentials import bootstrap_project_credentials, parse_env_file

    (tmp_path / "service.py").write_text(
        'import os\n'
        'GROQ_API_KEY = os.environ.get("GROQ_API_KEY")\n'
        'OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")\n',
        encoding="utf-8",
    )

    result = bootstrap_project_credentials(
        tmp_path,
        "Wire the API keys into a .env file",
        config_api_keys={"groq": "gr_live_123"},
    )

    values = parse_env_file(tmp_path / ".env")
    summary = result.prompt_summary()

    assert values["GROQ_API_KEY"] == "gr_live_123"
    assert "OPENAI_API_KEY" not in values
    assert "OPENAI_API_KEY" in result.missing_external
    assert "gr_live_123" not in summary
    assert "OPENAI_API_KEY" in summary


def test_detect_target_cloud_provider_understands_gcp_and_aws_aliases():
    from sage.core.credentials import detect_target_cloud_provider

    assert detect_target_cloud_provider("Deploy this service to gcloud") == "gcp"
    assert detect_target_cloud_provider("Ship this on AWS ECS") == "aws"


def test_bootstrap_imports_gcp_cli_context_into_env(tmp_path: Path, monkeypatch):
    import sage.core.credentials as credentials

    # Clear inherited GCP env vars so the bootstrap path actually reaches
    # the mocked `gcloud config get-value ...` calls instead of pulling
    # the user's real GOOGLE_CLOUD_PROJECT (e.g. when running locally
    # with a personal .env loaded). Without this, the test reads the
    # developer's real project ID and asserts "demo-project" wrongly.
    for k in (
        "GOOGLE_CLOUD_PROJECT", "CLOUDSDK_CORE_PROJECT",
        "GOOGLE_CLOUD_REGION", "CLOUDSDK_COMPUTE_REGION",
        "GOOGLE_CLOUD_ACCOUNT", "GCP_PROJECT_ID", "GCP_REGION",
    ):
        monkeypatch.delenv(k, raising=False)

    adc_path = tmp_path / "adc.json"
    adc_path.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", str(adc_path))

    def fake_run(command, capture_output, text, timeout, check):
        outputs = {
            ("gcloud", "config", "get-value", "project"): ("demo-project\n", 0),
            ("gcloud", "config", "get-value", "run/region"): ("us-central1\n", 0),
            ("gcloud", "config", "get-value", "account"): ("sage@example.com\n", 0),
        }
        stdout, returncode = outputs.get(tuple(command), ("", 1))
        return SimpleNamespace(returncode=returncode, stdout=stdout)

    monkeypatch.setattr(credentials.subprocess, "run", fake_run)

    result = credentials.bootstrap_project_credentials(
        tmp_path,
        "Deploy this app to gcloud",
        preferred_cloud="gcp",
    )

    values = credentials.parse_env_file(tmp_path / ".env")
    summary = result.prompt_summary()

    assert values["CLOUD_PROVIDER"] == "gcp"
    assert values["GOOGLE_CLOUD_PROJECT"] == "demo-project"
    assert values["GOOGLE_CLOUD_REGION"] == "us-central1"
    assert values["GOOGLE_CLOUD_ACCOUNT"] == "sage@example.com"
    assert values["GOOGLE_APPLICATION_CREDENTIALS"] == str(adc_path)
    assert "Google Cloud" in summary
    assert str(adc_path) not in summary


def test_load_config_reads_project_env_file(tmp_path: Path, monkeypatch):
    from sage.config import load_config

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SAGE_GROQ_API_KEY", raising=False)
    (tmp_path / ".env").write_text("SAGE_GROQ_API_KEY=from_project_env\n", encoding="utf-8")

    cfg = load_config(path=tmp_path / "missing-config.json")

    assert cfg.api_keys["groq"] == "from_project_env"
