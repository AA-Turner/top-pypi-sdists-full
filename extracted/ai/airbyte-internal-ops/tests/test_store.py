# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the registry store abstraction."""

from __future__ import annotations

from pathlib import Path

import pytest

from airbyte_ops_mcp.registry._constants import (
    DEV_METADATA_SERVICE_BUCKET_NAME,
    PROD_METADATA_SERVICE_BUCKET_NAME,
    SONAR_DEV_BUCKET_NAME,
    SONAR_PROD_BUCKET_NAME,
)
from airbyte_ops_mcp.registry.store import (
    REGISTRY_STORE_ENV_VAR,
    RegistryStore,
    StoreType,
    resolve_registry_store,
)

# ---------------------------------------------------------------------------
# StoreType enum
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param("sonar", StoreType.SONAR, id="sonar"),
        pytest.param("coral", StoreType.CORAL, id="coral"),
    ],
)
def test_store_type_from_value(value: str, expected: StoreType) -> None:
    """StoreType can be constructed from its string value."""
    assert StoreType(value) is expected


# ---------------------------------------------------------------------------
# RegistryStore.parse
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "target,expected_type,expected_env,expected_prefix,expected_bucket",
    [
        pytest.param(
            "coral:dev",
            StoreType.CORAL,
            "dev",
            "",
            DEV_METADATA_SERVICE_BUCKET_NAME,
            id="coral_dev",
        ),
        pytest.param(
            "coral:prod",
            StoreType.CORAL,
            "prod",
            "",
            PROD_METADATA_SERVICE_BUCKET_NAME,
            id="coral_prod",
        ),
        pytest.param(
            "coral:dev/aj-test100",
            StoreType.CORAL,
            "dev",
            "aj-test100",
            DEV_METADATA_SERVICE_BUCKET_NAME,
            id="coral_dev_prefix",
        ),
        pytest.param(
            "coral:dev/a/b/c",
            StoreType.CORAL,
            "dev",
            "a/b/c",
            DEV_METADATA_SERVICE_BUCKET_NAME,
            id="coral_dev_nested_prefix",
        ),
        pytest.param(
            "sonar:prod",
            StoreType.SONAR,
            "prod",
            "",
            SONAR_PROD_BUCKET_NAME,
            id="sonar_prod",
        ),
        pytest.param(
            "sonar:dev",
            StoreType.SONAR,
            "dev",
            "",
            SONAR_DEV_BUCKET_NAME,
            id="sonar_dev",
        ),
        pytest.param(
            "CORAL:dev",
            StoreType.CORAL,
            "dev",
            "",
            DEV_METADATA_SERVICE_BUCKET_NAME,
            id="case_insensitive_store_type",
        ),
    ],
)
def test_store_target_parse(
    target: str,
    expected_type: StoreType,
    expected_env: str,
    expected_prefix: str,
    expected_bucket: str,
) -> None:
    """RegistryStore.parse produces the expected fields and bucket resolution."""
    result = RegistryStore.parse(target)
    assert result.store_type is expected_type
    assert result.env == expected_env
    assert result.prefix == expected_prefix
    assert result.bucket == expected_bucket


@pytest.mark.unit
@pytest.mark.parametrize(
    "target,error_fragment",
    [
        pytest.param("dev", "Expected format", id="missing_colon"),
        pytest.param("unknown:dev", "Unknown store type", id="bad_store_type"),
        pytest.param("coral:staging", "Unknown environment", id="bad_env"),
        pytest.param("sonar:staging", "Unknown environment", id="bad_env_sonar"),
        pytest.param("file:/tmp/output", "Unknown store type", id="file_target"),
    ],
)
def test_store_target_parse_errors(target: str, error_fragment: str) -> None:
    """RegistryStore.parse raises ValueError for invalid inputs."""
    with pytest.raises(ValueError, match=error_fragment):
        RegistryStore.parse(target)


@pytest.mark.unit
def test_local_store_target_is_local_only(tmp_path: Path) -> None:
    """A local target resolves to a local root and never exposes a bucket."""
    target = RegistryStore.parse(f"coral:local:{tmp_path}")
    assert target.env == "local"
    assert target.local_path == tmp_path
    assert target.read_only is False
    assert target.bucket_root == str(tmp_path)
    with pytest.raises(ValueError, match="do not have a bucket"):
        _ = target.bucket


@pytest.mark.unit
def test_local_store_without_path_allocates_temp_dir() -> None:
    """A local target without a path allocates a temporary directory."""
    target = RegistryStore.parse("coral:local:")
    assert target.local_path is not None
    assert target.local_path.is_dir()


@pytest.mark.unit
def test_local_path_invariant() -> None:
    """Only local targets may carry a local path."""
    with pytest.raises(ValueError, match="Only local"):
        RegistryStore(
            store_type=StoreType.CORAL,
            env="prod",
            local_path=Path("/tmp/output"),
        )


# ---------------------------------------------------------------------------
# RegistryStore properties
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "prefix,expected_root",
    [
        pytest.param("", DEV_METADATA_SERVICE_BUCKET_NAME, id="no_prefix"),
        pytest.param(
            "my-test",
            f"{DEV_METADATA_SERVICE_BUCKET_NAME}/my-test",
            id="with_prefix",
        ),
    ],
)
def test_store_target_bucket_root(prefix: str, expected_root: str) -> None:
    """bucket_root reflects prefix when present."""
    t = RegistryStore(store_type=StoreType.CORAL, env="dev", prefix=prefix)
    assert t.bucket_root == expected_root


# ---------------------------------------------------------------------------
# StoreType.get_from_connector_name
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "name,expected",
    [
        pytest.param("source-github", StoreType.CORAL, id="source_prefix"),
        pytest.param("destination-bigquery", StoreType.CORAL, id="destination_prefix"),
        pytest.param("source-faker", StoreType.CORAL, id="source_faker"),
        pytest.param("stripe", StoreType.SONAR, id="bare_name"),
        pytest.param("github", StoreType.SONAR, id="bare_github"),
        pytest.param("salesforce", StoreType.SONAR, id="bare_salesforce"),
    ],
)
def test_store_type_get_from_connector_name(name: str, expected: StoreType) -> None:
    """StoreType.get_from_connector_name auto-detects by name prefix."""
    assert StoreType.get_from_connector_name(name) is expected


# ---------------------------------------------------------------------------
# StoreType.detect_from_repo_dir
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "subdirs,expected",
    [
        pytest.param(
            ["integrations", "connector-sdk"],
            StoreType.SONAR,
            id="sonar_markers",
        ),
        pytest.param(
            ["airbyte-integrations/connectors"],
            StoreType.CORAL,
            id="coral_markers",
        ),
        pytest.param([], None, id="unknown"),
    ],
)
def test_store_type_detect_from_repo_dir(
    tmp_path: Path,
    subdirs: list[str],
    expected: StoreType | None,
) -> None:
    """detect_from_repo_dir infers store type from directory markers."""
    for d in subdirs:
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    assert StoreType.detect_from_repo_dir(tmp_path) is expected


# ---------------------------------------------------------------------------
# resolve_registry_store
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "kwargs,expected_type,expected_env",
    [
        pytest.param(
            {"store": "sonar:prod", "connector_name": "stripe"},
            StoreType.SONAR,
            "prod",
            id="explicit_and_connector_agree",
        ),
        pytest.param(
            {"store": "sonar:prod", "connector_name": "source-faker"},
            StoreType.SONAR,
            "prod",
            id="explicit_overrides_conflicting_connector",
        ),
        pytest.param(
            {"connector_name": "source-faker"},
            StoreType.CORAL,
            "dev",
            id="coral_from_connector_name",
        ),
        pytest.param(
            {"connector_name": "stripe"},
            StoreType.SONAR,
            "dev",
            id="sonar_from_connector_name",
        ),
        pytest.param(
            {"connector_name": "stripe", "default_env": "prod"},
            StoreType.SONAR,
            "prod",
            id="custom_default_env",
        ),
    ],
)
def test_resolve_registry_store(
    kwargs: dict[str, str],
    expected_type: StoreType,
    expected_env: str,
) -> None:
    """resolve_registry_store resolves from explicit store or connector name."""
    result = resolve_registry_store(**kwargs)
    assert result.store_type is expected_type
    assert result.env == expected_env


@pytest.mark.unit
def test_resolve_registry_store_from_directory(tmp_path: Path) -> None:
    """Working-directory auto-detection as last fallback."""
    (tmp_path / "integrations").mkdir()
    (tmp_path / "connector-sdk").mkdir()
    result = resolve_registry_store(cwd=tmp_path)
    assert result.store_type is StoreType.SONAR
    assert result.env == "dev"


@pytest.mark.unit
def test_resolve_registry_store_from_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    """AIRBYTE_REGISTRY_STORE env var is used when set."""
    monkeypatch.setenv(REGISTRY_STORE_ENV_VAR, "coral:prod")
    result = resolve_registry_store()
    assert result.store_type is StoreType.CORAL
    assert result.env == "prod"


@pytest.mark.unit
def test_resolve_registry_store_explicit_overrides_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """--store takes priority over AIRBYTE_REGISTRY_STORE env var."""
    monkeypatch.setenv(REGISTRY_STORE_ENV_VAR, "sonar:dev")
    result = resolve_registry_store(store="coral:prod")
    assert result.store_type is StoreType.CORAL
    assert result.env == "prod"


@pytest.mark.unit
def test_resolve_registry_store_explicit_ignores_invalid_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """--store succeeds even when env var contains an invalid value."""
    monkeypatch.setenv(REGISTRY_STORE_ENV_VAR, "garbage")
    result = resolve_registry_store(store="coral:dev")
    assert result.store_type is StoreType.CORAL
    assert result.env == "dev"


@pytest.mark.unit
def test_resolve_registry_store_env_var_overrides_auto(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Env var takes priority over auto-detected sources."""
    monkeypatch.setenv(REGISTRY_STORE_ENV_VAR, "coral:prod")
    # sonar directory markers present but env var wins
    (tmp_path / "integrations").mkdir()
    (tmp_path / "connector-sdk").mkdir()
    result = resolve_registry_store(connector_name="stripe", cwd=tmp_path)
    assert result.store_type is StoreType.CORAL
    assert result.env == "prod"


@pytest.mark.unit
def test_resolve_registry_store_conflict_raises(
    tmp_path: Path,
) -> None:
    """Conflicting detections raise ValueError."""
    # sonar directory markers + coral connector name -> conflict
    (tmp_path / "integrations").mkdir()
    (tmp_path / "connector-sdk").mkdir()
    with pytest.raises(ValueError, match="Conflicting store types"):
        resolve_registry_store(connector_name="source-faker", cwd=tmp_path)


@pytest.mark.unit
def test_resolve_registry_store_agreement_succeeds(
    tmp_path: Path,
) -> None:
    """Multiple detections that agree resolve successfully."""
    # sonar directory markers + sonar connector name -> no conflict
    (tmp_path / "integrations").mkdir()
    (tmp_path / "connector-sdk").mkdir()
    result = resolve_registry_store(connector_name="stripe", cwd=tmp_path)
    assert result.store_type is StoreType.SONAR
    assert result.env == "dev"


@pytest.mark.unit
def test_resolve_registry_store_raises_when_unresolvable(tmp_path: Path) -> None:
    """ValueError when nothing can be resolved."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    with pytest.raises(ValueError, match="Cannot determine registry store"):
        resolve_registry_store(cwd=empty_dir)
