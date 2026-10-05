"""The harness registry (probe.harness): its rules, and that every consumer's
copy is the same file and loads on its own.

The hooks, the tap and the server cannot import `probe`, so `make
sync-harnesses` copies the stdlib loader and the JSON next to each of them.
These tests are what make "one list" true rather than aspirational.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from probe.harness import registry as registry_mod

AGENT = Path(__file__).resolve().parents[1]
REPO = AGENT.parent
SOURCE_DIR = AGENT / "src" / "probe" / "harness"
SOURCE_JSON = SOURCE_DIR / "harnesses.json"
SOURCE_LOADER = SOURCE_DIR / "registry.py"

#: Every copy of the JSON, by the consumer that reads it.
JSON_COPIES = {
    "plugin hooks": AGENT / "plugins/probe-research/hooks/harnesses.json",
    "daemon plugin hooks": AGENT / "plugins/probe-research-daemon/hooks/harnesses.json",
    "tap": AGENT / "plugins/probe-research-tap/tap/harnesses.json",
    "tap_core": AGENT / "src/probe/tap_core/harnesses.json",
    "server": REPO / "app/ingestion/harnesses.json",
    "dashboard": REPO / "dashboard/src/lib/harnesses.json",
    "pi extension": AGENT / "plugins/probe-research-pi/src/harnesses.json",
}
#: Every copy of the loader (consumers that run Python but cannot import probe).
LOADER_COPIES = {
    "plugin hooks": AGENT / "plugins/probe-research/hooks/_harness_registry.py",
    "daemon plugin hooks": AGENT / "plugins/probe-research-daemon/hooks/_harness_registry.py",
    "tap": AGENT / "plugins/probe-research-tap/tap/harness_registry.py",
    "tap_core": AGENT / "src/probe/tap_core/harness_registry.py",
    "server": REPO / "app/ingestion/harness_registry.py",
}


def _row(**overrides) -> dict:
    row = json.loads(SOURCE_JSON.read_text())["harnesses"][0]
    fake = {
        **row,
        "id": "fake_harness",
        "label": "Fake",
        "display": "Fake session",
        "aliases": ["fake"],
        "route": "fake",
        "detect_env": ["FAKE_HARNESS"],
        "session_env": "FAKE_HARNESS_SESSION",
        "icon": "/icons/fake.svg",
    }
    return {**fake, **overrides}


def test_the_registry_loads_and_names_its_default():
    reg = registry_mod.load()
    # Detection order: the first row whose marker is set wins (same as the SDK's AGENTS).
    assert reg.ids() == ("claude_code", "cursor", "codex", "pi", "kimi_code")
    assert reg.default == "claude_code"
    assert reg.get(reg.default).captured


def test_find_takes_ids_and_aliases_and_nothing_else():
    reg = registry_mod.load()
    assert reg.find("Claude").id == "claude_code"
    assert reg.find(" CLAUDE ").id == "claude_code"
    assert reg.find("claude-code") is None  # that is its ingest route, not a name
    assert reg.find("codex").id == "codex"
    assert reg.find("kimi").id == "kimi_code"
    assert reg.find("kimi-code") is None  # its ingest route, not a name
    assert reg.find("gemini") is None
    assert reg.find("") is None
    with pytest.raises(KeyError):
        reg.get("claude")  # get() takes exact ids only, never an alias or a default


def test_detect_reads_each_harness_marker_and_nothing_means_none():
    reg = registry_mod.load()
    assert reg.detect({"CLAUDECODE": "1"}).id == "claude_code"
    assert reg.detect({"CODEX_THREAD_ID": "t"}).id == "codex"
    assert reg.detect({"PI_CODING_AGENT": "true"}).id == "pi"
    assert reg.detect({}) is None


def test_home_dir_honours_the_override_variable(tmp_path):
    pi = registry_mod.load().get("pi")
    assert pi.home_dir({"PI_CODING_AGENT_DIR": str(tmp_path)}) == tmp_path
    assert pi.home_dir({}) == Path.home() / ".pi" / "agent"


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda d: d["harnesses"].append(_row(id="codex")), "names both"),
        (lambda d: d["harnesses"].append(_row(aliases=["claude"])), "names both"),
        (lambda d: d["harnesses"].append(_row(route="pi")), "share an ingest route"),
        (lambda d: d["harnesses"].append(_row(family="plugin")), "family must be one of"),
        (lambda d: d["harnesses"].append(_row(route=None)), "needs route"),
        (lambda d: d["harnesses"].append(_row(plugin=None)), "needs plugin"),
        (
            lambda d: d["harnesses"].append(
                _row(plugin={"root_env": "FAKE_ROOT", "manifest_dir": ".fake-plugin"})
            ),
            "plugin.marketplace",
        ),
        (
            lambda d: d["harnesses"].append(
                _row(plugin={**d["harnesses"][0]["plugin"], "marketplace_source": "url"})
            ),
            "marketplace_source must be one of",
        ),
        (
            lambda d: d["harnesses"].append(_row(family="extension", plugin=None, package_dir=None)),
            "needs package_dir",
        ),
        (lambda d: d["harnesses"].append(_row(detect_env=[])), "detect_env"),
        (lambda d: d["harnesses"].append(_row(captured="false")), "captured must be true or false"),
        (
            lambda d: d["harnesses"].append(
                _row(capture={**d["harnesses"][0]["capture"], "cli_token_fallback": "false"})
            ),
            "cli_token_fallback must be true or false",
        ),
        (lambda d: d["harnesses"].append(_row(transcripts="projects")), "transcripts must be an object"),
        (lambda d: d["harnesses"].append(_row(home={"path": ".fake"})), "home.env must be"),
        (lambda d: d.update(default="gemini"), "is not a harness id"),
        (lambda d: d.update(version=2), "unsupported registry version"),
    ],
)
def test_the_registry_refuses_a_broken_document(change, message):
    data = json.loads(SOURCE_JSON.read_text())
    change(data)
    with pytest.raises(registry_mod.RegistryError, match=message):
        registry_mod.parse(data)


def test_a_new_harness_needs_only_a_row():
    """The acceptance test of the whole registry: a row the code has never
    heard of is found, detected and listed with no code change."""
    reg = registry_mod.load(extra=[_row()])
    fake = reg.find("fake")
    assert fake is not None and fake.id == "fake_harness"
    assert reg.detect({"FAKE_HARNESS": "1"}).id == "fake_harness"
    assert "fake_harness" in [h.id for h in reg.captured()]


@pytest.mark.parametrize("consumer", sorted(JSON_COPIES))
def test_every_json_copy_is_the_source_byte_for_byte(consumer):
    copy = JSON_COPIES[consumer]
    assert copy.read_bytes() == SOURCE_JSON.read_bytes(), (
        f"{copy} drifted from {SOURCE_JSON}: run `make -C agent sync-harnesses`"
    )


@pytest.mark.parametrize("consumer", sorted(LOADER_COPIES))
def test_every_loader_copy_is_the_source_byte_for_byte(consumer):
    copy = LOADER_COPIES[consumer]
    assert copy.read_bytes() == SOURCE_LOADER.read_bytes(), (
        f"{copy} drifted from {SOURCE_LOADER}: run `make -C agent sync-harnesses`"
    )


@pytest.mark.parametrize("consumer", sorted(LOADER_COPIES))
def test_every_loader_copy_reads_the_json_beside_it_without_probe(consumer, tmp_path):
    """Copy the loader and its JSON into an empty folder and load it from a
    fresh interpreter with nothing on sys.path but that folder: what a hook,
    the tap or the server sees. If the loader ever imports `probe`, this fails."""
    import subprocess

    loader = LOADER_COPIES[consumer]
    (tmp_path / loader.name).write_bytes(loader.read_bytes())
    (tmp_path / "harnesses.json").write_bytes(loader.with_name("harnesses.json").read_bytes())
    module = loader.stem
    result = subprocess.run(
        # -I -S: no site-packages, so `probe` is not importable -- only the
        # standard library and this folder, exactly what a hook or the tap has.
        [
            sys.executable,
            "-I",
            "-S",
            "-c",
            f"import sys; sys.path.insert(0, '.'); import {module} as r; print(','.join(r.load().ids()))",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ",".join(registry_mod.load().ids())


def test_the_wheel_ships_the_json():
    """The CLI reads the JSON from its installed package; hatch must not drop it.

    The wheel target packages `src/probe` whole; a later `exclude` that matched
    `*.json` would break every installed CLI at import of probe.harness.
    """
    pyproject = (AGENT / "pyproject.toml").read_text()
    wheel = pyproject.split("[tool.hatch.build.targets.wheel]", 1)[1].split("\n[", 1)[0]
    assert "src/probe" in wheel
    assert "json" not in wheel.lower(), (
        "the wheel config names json: check it still ships harnesses.json"
    )


def test_the_mirror_render_carries_the_hooks_and_tap_copies(tmp_path):
    """The public mirror is how the Claude Code / Codex plugins and the pi
    package reach users: their copies must survive the render."""
    spec = importlib.util.spec_from_file_location(
        "mirror_render", AGENT / "tools" / "mirror_render.py"
    )
    mirror_render = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror_render)
    mirror = tmp_path / "mirror"
    mirror.mkdir()
    mirror_render.render(AGENT, mirror)
    for rel in (
        "plugins/probe-research/hooks/harnesses.json",
        "plugins/probe-research/hooks/_harness_registry.py",
        "plugins/probe-research-daemon/hooks/harnesses.json",
        "plugins/probe-research-tap/tap/harnesses.json",
        "plugins/probe-research-tap/tap/harness_registry.py",
        "plugins/probe-research-pi/src/harnesses.json",
    ):
        assert (mirror / rel).read_bytes() == SOURCE_JSON.read_bytes() or rel.endswith(".py"), rel


def test_the_server_image_carries_its_copy():
    """The API image copies `app/` (Dockerfile), not `agent/`: the server's
    copy must live under app/ and nothing may exclude it."""
    dockerfile = (REPO / "Dockerfile").read_text()
    assert "COPY app/ ./app/" in dockerfile
    ignore = REPO / ".dockerignore"
    if ignore.exists():
        assert "harnesses.json" not in ignore.read_text()
        assert "*.json" not in ignore.read_text().split()
