"""Registry-load tests: schema validation + the data-only extensibility guarantee."""

from __future__ import annotations

import json

import pytest

from runlayer_cli.scan.agents.registry import (
    DEFAULT_WEIGHTS,
    RegistryError,
    load_registry,
    signatures_path,
)

# Frameworks that must be present in the shipped signatures.json.
_PROTOTYPE_VALIDATED = {
    "langchain",
    "langgraph",
    "llamaindex",
    "crewai",
    "autogen-agentchat",
    "pydantic-ai",
    "openai-agents",
    "google-adk",
    "langchain-js",
    "mastra",
    "vercel-ai-sdk",
    "openai-agents-js",
    "rig",
    "langchaingo",
    "langchain4j",
    "spring-ai",
    "semantic-kernel",
}
_BREADTH = {
    "anthropic-claude-agent-sdk",
    "haystack",
    "smolagents",
    "llamaindex-ts",
    "openai-node",
    "anthropic-node",
    "voltagent",
    "semantic-kernel-java",
    "mcp-server-typescript",
    "mcp-server-python",
}


def test_signatures_path_exists():
    assert signatures_path().is_file()


def test_default_registry_loads():
    reg = load_registry()
    assert reg.frameworks
    assert reg.weights == DEFAULT_WEIGHTS


def test_all_expected_frameworks_present():
    ids = set(load_registry().framework_ids)
    missing = (_PROTOTYPE_VALIDATED | _BREADTH) - ids
    assert not missing, f"missing frameworks in signatures.json: {sorted(missing)}"


def test_framework_ids_are_unique():
    ids = load_registry().framework_ids
    assert len(ids) == len(set(ids))


def test_every_framework_has_required_fields():
    for fw in load_registry().frameworks:
        assert fw.framework_id
        assert fw.display_name
        assert fw.language
        assert fw.manifest_files  # non-empty tuple


def test_adding_a_framework_is_data_only(tmp_path):
    """A brand-new framework appears just by editing the data file -- no code."""
    data = {
        "frameworks": [
            {
                "framework_id": "totally-new-framework",
                "display_name": "Totally New Framework",
                "language": "Python",
                "manifest_files": ["pyproject.toml"],
                "package_deps": ["totally-new"],
                "imports": ["from totally_new import"],
                "symbols": ["NewAgent("],
            }
        ]
    }
    path = tmp_path / "signatures.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    reg = load_registry(path)
    assert reg.framework_ids == ("totally-new-framework",)
    fw = reg.frameworks[0]
    assert fw.package_deps == ("totally-new",)
    # Unspecified signature lists default to empty tuples.
    assert fw.shared_deps == ()


def test_weights_override_from_data(tmp_path):
    data = {
        "weights": {"package_dep": 5, "unknown_key": 99},
        "frameworks": [
            {
                "framework_id": "x",
                "display_name": "X",
                "language": "Python",
                "manifest_files": ["pyproject.toml"],
            }
        ],
    }
    path = tmp_path / "signatures.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    reg = load_registry(path)
    assert reg.weights["package_dep"] == 5  # overridden
    assert reg.weights["import"] == DEFAULT_WEIGHTS["import"]  # untouched
    assert "unknown_key" not in reg.weights  # unknown keys ignored


@pytest.mark.parametrize(
    "payload",
    [
        "{ not json",
        json.dumps({}),  # no frameworks key
        json.dumps({"frameworks": []}),  # empty
        json.dumps({"frameworks": [{"display_name": "x", "language": "Python"}]}),
        json.dumps(
            {
                "frameworks": [
                    {
                        "framework_id": "x",
                        "display_name": "X",
                        "language": "Python",
                        # missing manifest_files
                    }
                ]
            }
        ),
        json.dumps(
            {
                "frameworks": [
                    {
                        "framework_id": "x",
                        "display_name": "X",
                        "language": "Python",
                        "manifest_files": ["pyproject.toml"],
                        "imports": "not-a-list",
                    }
                ]
            }
        ),
        json.dumps(
            {
                "frameworks": [
                    {
                        "framework_id": "dup",
                        "display_name": "A",
                        "language": "Python",
                        "manifest_files": ["pyproject.toml"],
                    },
                    {
                        "framework_id": "dup",
                        "display_name": "B",
                        "language": "Python",
                        "manifest_files": ["pyproject.toml"],
                    },
                ]
            }
        ),
    ],
)
def test_malformed_registry_raises(tmp_path, payload):
    path = tmp_path / "signatures.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(RegistryError):
        load_registry(path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(RegistryError):
        load_registry(tmp_path / "does-not-exist.json")
