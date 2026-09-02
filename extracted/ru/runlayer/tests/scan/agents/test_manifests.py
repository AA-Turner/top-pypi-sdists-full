"""Manifest-parser unit tests, one ecosystem at a time, over tmp fixtures."""

from __future__ import annotations

import textwrap
from pathlib import Path

from runlayer_cli.scan.agents.manifests import (
    manifest_ecosystem,
    manifest_kind,
    normalize_dep,
    parse_manifest,
)


def _deps(tmp_path: Path, name: str, content: str) -> list[str]:
    # dedent so indented heredoc fixtures parse (ast/yarn need column-0 starts).
    path = tmp_path / name
    path.write_text(textwrap.dedent(content), encoding="utf-8")
    info = parse_manifest(path)
    assert info is not None
    return info.deps


# --------------------------------------------------------------------------- #
# manifest_kind / ecosystem / normalize_dep
# --------------------------------------------------------------------------- #


def test_manifest_kind_recognizes_core_and_breadth():
    assert manifest_kind("pyproject.toml") == "pyproject.toml"
    assert manifest_kind("package.json") == "package.json"
    assert manifest_kind("Cargo.toml") == "Cargo.toml"
    assert manifest_kind("go.mod") == "go.mod"
    assert manifest_kind("pom.xml") == "pom.xml"
    assert manifest_kind("Foo.csproj") == ".csproj"
    assert manifest_kind("build.gradle.kts") == "build.gradle.kts"
    # requirements*.txt variants collapse to one kind.
    assert manifest_kind("requirements.txt") == "requirements.txt"
    assert manifest_kind("requirements-dev.txt") == "requirements.txt"


def test_manifest_kind_rejects_non_manifests():
    assert manifest_kind("agent.py") is None
    assert manifest_kind("README.md") is None
    assert manifest_kind("notes.txt") is None


def test_manifest_ecosystem_mapping():
    assert manifest_ecosystem("pyproject.toml") == "python"
    assert manifest_ecosystem("package.json") == "npm"
    assert manifest_ecosystem("Cargo.toml") == "cargo"
    assert manifest_ecosystem("go.mod") == "go"
    assert manifest_ecosystem("build.gradle") == "maven"
    assert manifest_ecosystem(".csproj") == "nuget"


def test_normalize_dep_semantics():
    # PEP 503 for Python: case-insensitive, runs of -_. collapse to -.
    assert normalize_dep("Llama_Index.Core", "python") == "llama-index-core"
    # npm / cargo / maven / nuget: case-fold.
    assert normalize_dep("@LangChain/Core", "npm") == "@langchain/core"
    assert (
        normalize_dep("Microsoft.SemanticKernel", "nuget") == "microsoft.semantickernel"
    )
    # Go module paths are case-sensitive: preserved verbatim.
    assert (
        normalize_dep("github.com/tmc/LangChainGo", "go")
        == "github.com/tmc/LangChainGo"
    )


# --------------------------------------------------------------------------- #
# Python ecosystem
# --------------------------------------------------------------------------- #


def test_parse_pyproject(tmp_path):
    deps = _deps(
        tmp_path,
        "pyproject.toml",
        """
        [project]
        name = "x"
        dependencies = ["langchain>=0.3", "langchain-openai>=0.2"]
        [project.optional-dependencies]
        dev = ["pytest"]
        """,
    )
    assert "langchain" in deps
    assert "langchain-openai" in deps
    assert "pytest" in deps


def test_parse_pyproject_poetry_table(tmp_path):
    deps = _deps(
        tmp_path,
        "pyproject.toml",
        """
        [tool.poetry.dependencies]
        python = "^3.11"
        crewai = "^0.40"
        """,
    )
    assert "crewai" in deps
    assert "python" not in deps  # the interpreter pin is not a dependency


def test_parse_requirements_txt_skips_flags_and_comments(tmp_path):
    deps = _deps(
        tmp_path,
        "requirements.txt",
        """
        # a comment
        langchain==0.3.1
        requests>=2.31  # inline comment
        -r other.txt
        -e .
        --hash=sha256:abc
        """,
    )
    assert deps == sorted({"langchain", "requests"})


def test_parse_setup_py_install_requires_and_extras(tmp_path):
    deps = _deps(
        tmp_path,
        "setup.py",
        """
        from setuptools import setup
        setup(
            name="x",
            install_requires=["pydantic-ai", "httpx>=0.27"],
            extras_require={"dev": ["pytest", "ruff"]},
        )
        """,
    )
    assert {"pydantic-ai", "httpx", "pytest", "ruff"}.issubset(set(deps))


def test_parse_setup_cfg(tmp_path):
    deps = _deps(
        tmp_path,
        "setup.cfg",
        """
        [options]
        install_requires =
            smolagents
            rich>=13
        """,
    )
    assert "smolagents" in deps
    assert "rich" in deps


def test_parse_uv_lock(tmp_path):
    deps = _deps(
        tmp_path,
        "uv.lock",
        """
        version = 1
        [[package]]
        name = "langgraph"
        version = "0.2.0"
        [[package]]
        name = "langchain-openai"
        version = "0.2.0"
        """,
    )
    assert "langgraph" in deps
    assert "langchain-openai" in deps


def test_parse_pipfile_lock(tmp_path):
    deps = _deps(
        tmp_path,
        "Pipfile.lock",
        '{"default": {"haystack-ai": {"version": "==2.0"}}, '
        '"develop": {"pytest": {"version": "*"}}}',
    )
    assert "haystack-ai" in deps
    assert "pytest" in deps


# --------------------------------------------------------------------------- #
# npm ecosystem
# --------------------------------------------------------------------------- #


def test_parse_package_json(tmp_path):
    deps = _deps(
        tmp_path,
        "package.json",
        '{"dependencies": {"@mastra/core": "^0.10", "zod": "^3"}, '
        '"devDependencies": {"typescript": "^5"}}',
    )
    assert "@mastra/core" in deps
    assert "zod" in deps
    assert "typescript" in deps


def test_parse_package_lock_json_v3(tmp_path):
    deps = _deps(
        tmp_path,
        "package-lock.json",
        '{"lockfileVersion": 3, "packages": {"": {"name": "x"}, '
        '"node_modules/ai": {"version": "5.0.0"}, '
        '"node_modules/@ai-sdk/openai": {"version": "2.0.0"}}}',
    )
    assert "ai" in deps
    assert "@ai-sdk/openai" in deps


def test_parse_package_lock_json_v1(tmp_path):
    v1_dir = tmp_path / "v1"
    v1_dir.mkdir()
    deps = _deps(
        v1_dir,
        "package-lock.json",
        '{"lockfileVersion": 1, "dependencies": {"express": {"version": "4"}}}',
    )
    assert "express" in deps


def test_parse_pnpm_lock_yaml(tmp_path):
    deps = _deps(
        tmp_path,
        "pnpm-lock.yaml",
        """
        lockfileVersion: '9.0'
        packages:
          '@voltagent/core@1.2.3':
            resolution: {integrity: sha512-aaa}
          zod@3.23.0:
            resolution: {integrity: sha512-bbb}
        """,
    )
    assert "@voltagent/core" in deps
    assert "zod" in deps


def test_parse_yarn_lock(tmp_path):
    deps = _deps(
        tmp_path,
        "yarn.lock",
        """
        # yarn lockfile v1
        "@openai/agents@^0.0.10":
          version "0.0.10"

        zod@^3.23.0:
          version "3.23.8"
        """,
    )
    assert "@openai/agents" in deps
    assert "zod" in deps


# --------------------------------------------------------------------------- #
# cargo / go / maven / gradle / nuget
# --------------------------------------------------------------------------- #


def test_parse_cargo(tmp_path):
    deps = _deps(
        tmp_path,
        "Cargo.toml",
        """
        [dependencies]
        rig-core = "0.6"
        tokio = { version = "1", features = ["full"] }
        """,
    )
    assert "rig-core" in deps
    assert "tokio" in deps


def test_parse_go_mod_single_and_block(tmp_path):
    deps = _deps(
        tmp_path,
        "go.mod",
        """
        module example.com/x
        go 1.22
        require github.com/tmc/langchaingo v0.1.13
        require (
            github.com/foo/bar v1.2.3
            github.com/baz/qux v0.0.1
        )
        """,
    )
    assert "github.com/tmc/langchaingo" in deps
    assert "github.com/foo/bar" in deps
    assert "github.com/baz/qux" in deps


def test_parse_pom_group_artifact(tmp_path):
    deps = _deps(
        tmp_path,
        "pom.xml",
        """<?xml version="1.0"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
          <dependencies>
            <dependency>
              <groupId>dev.langchain4j</groupId>
              <artifactId>langchain4j</artifactId>
              <version>1.1.0</version>
            </dependency>
          </dependencies>
        </project>
        """,
    )
    assert "dev.langchain4j:langchain4j" in deps


def test_parse_build_gradle_coords(tmp_path):
    deps = _deps(
        tmp_path,
        "build.gradle",
        """
        dependencies {
            implementation 'org.springframework.ai:spring-ai-openai:1.0.3'
            implementation("dev.langchain4j:langchain4j:1.1.0")
        }
        """,
    )
    assert "org.springframework.ai:spring-ai-openai" in deps
    assert "dev.langchain4j:langchain4j" in deps


def test_parse_csproj_package_reference(tmp_path):
    deps = _deps(
        tmp_path,
        "App.csproj",
        """<Project Sdk="Microsoft.NET.Sdk">
          <ItemGroup>
            <PackageReference Include="Microsoft.SemanticKernel" Version="1.77.0" />
          </ItemGroup>
        </Project>
        """,
    )
    assert "microsoft.semantickernel" in deps  # nuget case-folded


# --------------------------------------------------------------------------- #
# Robustness
# --------------------------------------------------------------------------- #


def test_parse_error_yields_empty_deps_not_crash(tmp_path):
    # Malformed TOML must not raise; the file is still a recognized manifest.
    path = tmp_path / "pyproject.toml"
    path.write_text("this is = = not valid toml [[[", encoding="utf-8")
    info = parse_manifest(path)
    assert info is not None
    assert info.kind == "pyproject.toml"
    assert info.ecosystem == "python"
    assert info.deps == []


def test_parse_manifest_returns_none_for_unrecognized(tmp_path):
    path = tmp_path / "agent.py"
    path.write_text("print('hi')", encoding="utf-8")
    assert parse_manifest(path) is None
