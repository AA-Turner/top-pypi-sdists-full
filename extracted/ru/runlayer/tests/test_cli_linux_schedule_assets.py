"""Static contracts for the full CLI's Linux managed-skill scheduler."""

from __future__ import annotations

from pathlib import Path

import yaml

from runlayer_cli import regex_safe

_PACKAGING = Path(__file__).parent.parent / "packaging" / "linux"
_CRON = _PACKAGING / "cron.d-runlayer-cli"
_WRAPPER = _PACKAGING / "run-cli-schedule.sh"
_NFPM = _PACKAGING / "nfpm.yaml"

_CRON_DST = "/etc/cron.d/runlayer-cli"
_WRAPPER_DST = "/usr/lib/runlayer/run-cli-schedule.sh"


def _nfpm() -> dict:
    return yaml.safe_load(_NFPM.read_text())


def _nfpm_content_by_dst() -> dict[str, dict]:
    return {entry["dst"]: entry for entry in _nfpm()["contents"]}


def test_cron_destination_is_run_parts_safe_and_hourly() -> None:
    destination_name = _CRON.name.removeprefix("cron.d-")
    text = _CRON.read_text()

    assert destination_name == "runlayer-cli"
    assert regex_safe.fullmatch(r"[A-Za-z0-9_-]+", destination_name)
    assert "23 * * * * root /usr/lib/runlayer/run-cli-schedule.sh" in text
    assert "7 * * * *" not in text  # offset from AI Watch's hourly update


def test_cron_pins_shell_and_path() -> None:
    lines = _CRON.read_text().splitlines()

    assert any(line.startswith("SHELL=/bin/sh") for line in lines)
    assert any(line.startswith("PATH=") for line in lines)


def test_wrapper_gates_credentials_and_managed_host_before_fanout() -> None:
    text = _WRAPPER.read_text()
    source = '. "$CREDENTIALS_FILE"'
    fallback = "RUNLAYER_SKILL_SYNC_API_KEY=${RUNLAYER_API_KEY:-}"
    key_gate = '[ -z "$RUNLAYER_SKILL_SYNC_API_KEY" ]'
    host_gate = 'grep -Eq \'"Host"[[:space:]]*:[[:space:]]*"[^"]+"\''
    invocation = "/usr/bin/runlayer schedule"

    assert text.startswith("#!/bin/sh")
    assert "CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials" in text
    assert "CONFIG_FILE=/etc/runlayer/aiwatch/config.json" in text
    assert source in text
    assert fallback in text
    assert key_gate in text
    assert host_gate in text
    assert "export RUNLAYER_SKILL_SYNC_API_KEY" in text
    assert "export RUNLAYER_API_KEY" in text
    assert (
        text.find(source)
        < text.find(fallback)
        < text.find(key_gate)
        < text.find(host_gate)
        < text.find(invocation)
    )


def test_wrapper_uses_root_only_nonblocking_overlap_lock() -> None:
    text = _WRAPPER.read_text()

    assert "umask 077" in text
    assert "LOCK_DIR=/run/runlayer-cli" in text
    assert 'mkdir -p "$LOCK_DIR"' in text
    assert 'chmod 0700 "$LOCK_DIR"' in text
    assert 'exec 9>"$LOCK_DIR/schedule.lock"' in text
    assert 'chmod 0600 "$LOCK_DIR/schedule.lock"' in text
    assert "flock -n 9 || exit 0" in text
    assert text.find("flock -n") < text.find("CREDENTIALS_FILE=")


def test_wrapper_drops_privileges_for_each_real_login_user_home() -> None:
    """Write fan-out is gated to real login users (uid >= UID_MIN).

    Unlike the read-only scan wrapper, skill sync writes homes, so service
    accounts (daemon, games, ...) must never be handed to runuser — with a
    managed Username override they would all resolve to that identity and get
    skill trees written into homes like /usr/sbin.
    """
    text = _WRAPPER.read_text()
    uid_min_read = 'awk \'$1 == "UID_MIN"'
    uid_min_fallback = "uid_min=1000"
    uid_gate = '[ "$uid" -ge "$uid_min" ] || continue'

    assert "getent passwd" in text
    assert uid_min_read in text
    assert "/etc/login.defs" in text
    assert uid_min_fallback in text
    assert uid_gate in text
    assert '[ -d "$home" ] || continue' in text
    assert "readlink -f" in text
    assert "grep -Fxq" in text
    assert 'runuser -u "$user"' in text
    assert "timeout -k 30 600" in text
    assert 'env HOME="$home" USER="$user" LOGNAME="$user"' in text
    assert text.find(uid_gate) < text.find('runuser -u "$user"')
    # uid boundary, not shell allowlists: directory users can have odd shells.
    assert "nologin" not in text
    assert "/bin/false" not in text


def test_wrapper_isolates_failures_and_routes_output_to_syslog() -> None:
    text = _WRAPPER.read_text()

    assert "schedule_rc=$?" in text
    assert 'if [ "$schedule_rc" -ne 0 ]' in text
    assert "logger -t runlayer-cli" in text
    assert "rc=1" in text
    assert "exit $rc" in text


def test_nfpm_ships_plain_cron_and_executable_wrapper() -> None:
    contents = _nfpm_content_by_dst()
    wrapper = contents[_WRAPPER_DST]
    cron = contents[_CRON_DST]

    assert wrapper == {
        "src": "./packaging/linux/run-cli-schedule.sh",
        "dst": _WRAPPER_DST,
        "file_info": {"mode": 0o755, "owner": "root", "group": "root"},
    }
    assert cron == {
        "src": "./packaging/linux/cron.d-runlayer-cli",
        "dst": _CRON_DST,
        "file_info": {"mode": 0o644, "owner": "root", "group": "root"},
    }


def test_nfpm_requires_platform_cron_provider_without_owning_shared_config() -> None:
    data = _nfpm()
    destinations = _nfpm_content_by_dst()

    assert data["overrides"]["deb"]["depends"] == ["cron | cron-daemon | cronie"]
    assert data["overrides"]["rpm"]["depends"] == ["cronie"]
    assert "/etc/runlayer/aiwatch/config.json" not in destinations
    assert "/etc/runlayer/aiwatch/credentials" not in destinations
