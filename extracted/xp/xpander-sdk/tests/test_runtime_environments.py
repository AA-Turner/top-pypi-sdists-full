"""Runtime environment models + the inheritance resolver (mirror of the mono dev_utils suite)."""
import pytest

from xpander_sdk.models.configuration import Configuration
from xpander_sdk.models.runtime_environments import (
    ResolvedRuntimeEnvironment,
    RuntimeConfigFile,
    RuntimeEnvironment,
    RuntimeEnvironmentCycleError,
    RuntimePackages,
    RuntimeScript,
    _package_identity,
    resolve_runtime_environment,
)
from xpander_sdk.modules.agents.sub_modules.agent import Agent, AgentGraph
from tests.helpers.factories import make_agent


def _env(env_id, parent=None, **kw):
    return RuntimeEnvironment(id=env_id, organization_id="org", name=env_id, parent_environment_id=parent, **kw)


def test_single_env_resolves_to_its_own_spec():
    env = _env("a", packages=RuntimePackages(pip=["httpx==0.27"], brew=["kubectl"]),
               setup_scripts=[RuntimeScript(name="s", body="echo hi")])
    r = resolve_runtime_environment("a", {"a": env})
    assert r.packages.pip == ["httpx==0.27"] and r.packages.brew == ["kubectl"]
    assert [s.name for s in r.setup_scripts] == ["s"]
    assert r.chain == ["a"] and r.hash


def test_child_extends_base_packages_scripts_ordered_base_then_child():
    base = _env("base", packages=RuntimePackages(brew=["kubectl", "awscli"]),
                setup_scripts=[RuntimeScript(name="base", body="b")])
    child = _env("web", parent="base", packages=RuntimePackages(pnpm=["vite"]),
                 setup_scripts=[RuntimeScript(name="web", body="w")])
    r = resolve_runtime_environment("web", {"base": base, "web": child})
    assert r.chain == ["base", "web"]
    assert r.packages.brew == ["kubectl", "awscli"] and r.packages.pnpm == ["vite"]
    assert [s.name for s in r.setup_scripts] == ["base", "web"]


def test_child_overrides_parent_package_version_keeping_order():
    base = _env("base", packages=RuntimePackages(pip=["httpx==0.27", "ruff"]))
    child = _env("c", parent="base", packages=RuntimePackages(pip=["httpx==0.28"]))
    r = resolve_runtime_environment("c", {"base": base, "c": child})
    assert r.packages.pip == ["httpx==0.28", "ruff"]


def test_config_merges_by_path_child_wins_sorted():
    base = _env("base", config=[RuntimeConfigFile(path="b", contents="1"), RuntimeConfigFile(path="a", contents="1")])
    child = _env("c", parent="base", config=[RuntimeConfigFile(path="a", contents="2")])
    r = resolve_runtime_environment("c", {"base": base, "c": child})
    assert [(c.path, c.contents) for c in r.config] == [("a", "2"), ("b", "1")]


def test_hash_is_stable_and_content_sensitive():
    e1 = _env("a", packages=RuntimePackages(brew=["kubectl"]))
    e2 = _env("a", packages=RuntimePackages(brew=["kubectl"]))
    e3 = _env("a", packages=RuntimePackages(brew=["kubectl", "jq"]))
    assert resolve_runtime_environment("a", {"a": e1}).hash == resolve_runtime_environment("a", {"a": e2}).hash
    assert resolve_runtime_environment("a", {"a": e1}).hash != resolve_runtime_environment("a", {"a": e3}).hash


def test_cycle_raises():
    a = _env("a", parent="b")
    b = _env("b", parent="a")
    with pytest.raises(RuntimeEnvironmentCycleError):
        resolve_runtime_environment("a", {"a": a, "b": b})


def test_missing_parent_ends_the_walk_as_a_root():
    child = _env("c", parent="ghost", packages=RuntimePackages(brew=["node"]))
    r = resolve_runtime_environment("c", {"c": child})  # 'ghost' absent
    assert r.chain == ["c"] and r.packages.brew == ["node"]


def test_missing_leaf_returns_none_not_an_empty_env():
    assert resolve_runtime_environment("ghost", {}) is None
    assert resolve_runtime_environment("ghost", {"other": _env("other")}) is None


@pytest.mark.parametrize("bad", ["/etc/passwd", "~/x", "../escape", "a/../../b", "a\\b", "a\x00b", ""])
def test_config_path_rejects_escapes(bad):
    with pytest.raises(ValueError):
        RuntimeConfigFile(path=bad, contents="x")


@pytest.mark.parametrize("manager,spec,name", [
    ("pip", "httpx==0.27", "httpx"),
    ("pip", "ruff>=0.1,<0.2", "ruff"),
    ("brew", "node@22", "node"),
    ("npm", "typescript@5.4", "typescript"),
    ("npm", "@scope/pkg@1.2.3", "@scope/pkg"),
    ("pnpm", "vite", "vite"),
])
def test_package_identity(manager, spec, name):
    assert _package_identity(manager, spec) == name


def test_resolved_model_shape():
    r = resolve_runtime_environment("a", {"a": _env("a", packages=RuntimePackages(brew=["kubectl"]))})
    assert isinstance(r, ResolvedRuntimeEnvironment)
    assert set(r.model_dump().keys()) >= {"environment_id", "chain", "packages", "setup_scripts", "config", "hash"}


def _agent(**over):
    data = make_agent(**over)
    return Agent.model_validate({**data, "graph": AgentGraph([]), "tools": None, "configuration": Configuration()})


def test_agent_carries_runtime_environment_id_through_dumps():
    agent = _agent(id="ag1", name="A", organization_id="org", runtime_environment_id="env-1")
    assert agent.runtime_environment_id == "env-1"
    dump = agent.model_dump(include={"runtime_environment_id", "runtime_environment"})
    assert dump.get("runtime_environment_id") == "env-1"


def test_agent_runtime_environment_id_defaults_none():
    agent = _agent(id="ag2", name="B", organization_id="org")
    assert "runtime_environment_id" in Agent.model_fields and "runtime_environment" in Agent.model_fields
    assert agent.runtime_environment_id is None
    assert agent.runtime_environment is None
