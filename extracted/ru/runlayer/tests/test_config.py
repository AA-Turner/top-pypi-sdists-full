"""Tests for configuration loading and updating functions."""

import tempfile
from pathlib import Path
import pytest
import yaml

from runlayer_cli.deploy.config import load_config, load_config_raw, update_config_id


def test_load_config_success():
    """Test loading a valid YAML config file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_data = {
            "name": "test-service",
            "runtime": "docker",
            "build": {"dockerfile": "Dockerfile", "context": "."},
        }
        yaml.dump(config_data, f)
        config_path = f.name

    try:
        result = load_config(config_path)
        assert result["name"] == "test-service"
        assert result["runtime"] == "docker"
        assert "build" in result
    finally:
        Path(config_path).unlink()


def test_load_config_file_not_found():
    """Test that missing config file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError) as exc_info:
        load_config("nonexistent.yaml")
    assert "not found" in str(exc_info.value).lower()


def test_load_config_empty_file():
    """Test that empty YAML file raises ValueError."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_path = f.name

    try:
        with pytest.raises(ValueError) as exc_info:
            load_config(config_path)
        assert "empty" in str(exc_info.value).lower()
    finally:
        Path(config_path).unlink()


def test_load_config_invalid_yaml():
    """Test that invalid YAML syntax raises ValueError."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("invalid: yaml: content: [")
        config_path = f.name

    try:
        with pytest.raises(ValueError) as exc_info:
            load_config(config_path)
        assert (
            "yaml" in str(exc_info.value).lower()
            or "syntax" in str(exc_info.value).lower()
        )
    finally:
        Path(config_path).unlink()


def test_load_config_raw():
    """Test loading raw YAML content as string."""
    yaml_content = "name: test-service\nruntime: docker\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        config_path = f.name

    try:
        result = load_config_raw(config_path)
        assert isinstance(result, str)
        assert "name: test-service" in result
        assert "runtime: docker" in result
    finally:
        Path(config_path).unlink()


def test_update_config_id_existing():
    """Test updating existing ID field in config."""
    config_content = """# Deployment config
name: test-service
id: old-id-123
runtime: docker
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(config_content)
        config_path = f.name

    try:
        update_config_id(config_path, "new-id-456")
        updated_content = Path(config_path).read_text()
        assert "id: new-id-456" in updated_content
        assert "old-id-123" not in updated_content
    finally:
        Path(config_path).unlink()


def test_update_config_id_new():
    """Test adding ID field to config without one."""
    config_content = """# Deployment config
name: test-service
runtime: docker
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(config_content)
        config_path = f.name

    try:
        update_config_id(config_path, "new-id-789")
        updated_content = Path(config_path).read_text()
        assert "id: new-id-789" in updated_content
        assert "name: test-service" in updated_content
    finally:
        Path(config_path).unlink()
