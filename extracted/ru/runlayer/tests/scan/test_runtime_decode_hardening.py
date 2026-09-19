"""Runtime-output decoders survive deeply nested JSON (ISS-01).

Container labels, WSL ``docker ps`` rows, Warp's SQLite cells and the on-disk
scan caches are all attacker-writable. Each decoder here used to catch only
``ValueError``; a nested-array payload raised ``RecursionError`` out of the
phase instead.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.scan import scan_state, warp_sqlite, wsl_exec
from runlayer_cli.scan.artifact_cache import ArtifactCache
from runlayer_cli.scan.containers import inspect_parse, k3s_cli
from runlayer_cli.scan.processes.enumerate import parse_windows_cim
from tests.hostile_inputs import DEEP_NESTING


def test_docker_ps_row_is_marked_malformed_not_raised():
    text = '{"ID": "good"}\n' + DEEP_NESTING + "\n"
    parsed = inspect_parse._parse_docker_ps_inventory(text)
    assert parsed["container_ids"] == ["good"]
    assert parsed["malformed"] is True


def test_docker_engine_inventory_treats_deep_nesting_as_no_rows():
    parsed = inspect_parse._parse_docker_engine_inventory(DEEP_NESTING)
    assert parsed["container_ids"] == []


def test_image_digest_and_config_parsers_return_empty():
    assert inspect_parse.parse_image_digests(DEEP_NESTING) == {}
    assert inspect_parse.parse_image_config_metadata(DEEP_NESTING) == {}
    assert inspect_parse.parse_docker_image_ls(DEEP_NESTING) is None
    assert inspect_parse.parse_docker_engine_images(DEEP_NESTING) is None


def test_crictl_parsers_return_empty():
    assert k3s_cli._parse_crictl_ps_inventory(DEEP_NESTING)["container_ids"] == []
    assert k3s_cli._parse_crictl_image_digest(DEEP_NESTING) is None


def test_wsl_container_rows_mark_malformed_and_keep_siblings():
    text = '{"ID": "good"}\n' + DEEP_NESTING + "\n"
    containers, complete = wsl_exec._parse_container_rows(
        text, runtime="docker", distro="Ubuntu"
    )
    assert [container.container_id for container in containers] == ["good"]
    assert complete is False


def test_windows_cim_deep_nesting_yields_no_candidates():
    assert parse_windows_cim(DEEP_NESTING) == []


def test_warp_cell_deep_nesting_decodes_to_none():
    assert warp_sqlite._decode_cell(DEEP_NESTING) is None


def test_scan_state_file_deep_nesting_is_empty_state(tmp_path: Path):
    state_path = tmp_path / "scan_state.json"
    state_path.write_text(DEEP_NESTING)
    assert scan_state._load_state(state_path) == {}


def test_artifact_cache_deep_nesting_is_integrity_miss(tmp_path: Path):
    cache_path = tmp_path / "artifact_cache.json"
    cache_path.write_text(DEEP_NESTING)
    cache = ArtifactCache("https://example.test", "key", cache_path=cache_path)
    assert cache._load_entries() == {}
