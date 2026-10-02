"""This machine's stable identity: persistence, isolation, and refusal to merge.

The whole feature turns on one property -- the id survives everything a
credential does not -- and on one refusal: it must never be shared between two
machines. A duplicate row is annoying; a merged row silently attributes one
person's laptop to another's, and there is no evidence left to separate them.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from probe.client_headers import DEVICE_HEADER, device_headers
from probe.sdk import device_identity

#: Captured before the autouse fixture pins it, so the few tests that exercise
#: the real lookup can still reach it.
_REAL_MACHINE_ID = device_identity._machine_id


@pytest.fixture(autouse=True)
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    target = tmp_path / "state" / "device.json"
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(target))
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    # PIN THE MACHINE WITNESS. Without this the suite asserts against whatever
    # stable id the HOST happens to expose, so the witness tests below prove the
    # fix on a developer laptop and quietly prove nothing in a container with no
    # `/etc/machine-id` -- they would fail there, on code that is fine. The
    # module-level cache is cleared with it, or one test's real lookup leaks
    # into the next.
    monkeypatch.setattr(device_identity, "_MACHINE_ID_CACHE", "")
    monkeypatch.setattr(device_identity, "_machine_id", lambda: "test-machine-id")
    return target


def test_the_identity_is_minted_once_and_reused(isolated: Path) -> None:
    first = device_identity.device_instance_id()
    second = device_identity.device_instance_id()
    assert first is not None
    assert first == second
    assert json.loads(isolated.read_text())["device_instance_id"] == first


def test_the_identity_satisfies_the_shape_every_layer_validates() -> None:
    """Four layers check this: the SDK, the API schema, and both databases.

    A value one accepts and another rejects would fail at the far end of a
    browser approval the user has already completed.
    """
    value = device_identity.device_instance_id()
    assert device_headers(value) == {DEVICE_HEADER: value}


def test_the_identity_survives_a_rewritten_credential_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """It is not a credential, so logging out must not take it away.

    `config.clear_context` wipes a context wholesale on logout -- deliberately,
    because subtracting known keys would leave a newer client's credential
    behind. An identity stored in there would go with it, and the machine would
    come back as a brand new device after every sign-out.
    """
    from probe.sdk import config

    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(tmp_path / "device.json"))
    config.save_context({"base_url": "https://example.test", "token": "probe_pat_x"})
    minted = device_identity.device_instance_id()

    config.clear_context()

    assert config.load_context().get("token") is None
    assert device_identity.device_instance_id() == minted


def test_an_isolated_config_gets_an_isolated_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """PROBE_CONFIG_PATH pulls the device file with it.

    `sdk/config.py::config_path` documents the failure this prevents: the
    override was honoured by four readers and not the writer, so the setting
    "worked in the field and silently vanished under any test or dev
    environment". A test harness that isolates its config but shares the real
    machine's identity would register the developer's laptop from CI.
    """
    monkeypatch.delenv("PROBE_DEVICE_ID_PATH", raising=False)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "nested" / "config.json"))
    assert device_identity.device_file() == tmp_path / "nested" / "device.json"


def test_a_file_minted_on_another_machine_is_never_adopted(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A shared or NFS $HOME must not hand every node the same identity.

    The witness is a TRIPWIRE: it can say "this file was written somewhere
    else", which is safe. It is never used to decide that two machines are the
    same, which is not.
    """
    minted = device_identity.device_instance_id()
    payload = json.loads(isolated.read_text())
    payload["machine"] = "m1:" + "f" * 32
    payload["home"] = "some-other-box:/home/someone-else"
    isolated.write_text(json.dumps(payload))

    replacement = device_identity.device_instance_id()

    assert replacement is not None
    assert replacement != minted


def test_a_legacy_file_from_another_home_is_still_never_adopted(
    isolated: Path,
) -> None:
    """The pre-witness comparison keeps its full strictness.

    A file with no `machine` predates the stable witness, so the only evidence
    it carries is the hostname it was written under. A hostname-only difference
    is NOT read as a rename here: from disk it is indistinguishable from a
    second node on a shared $HOME, and merging two machines is the failure this
    module treats as strictly worse than splitting one.
    """
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(
        json.dumps({"device_instance_id": "b" * 32, "home": "some-other-box:/home/someone-else"})
    )

    assert device_identity.device_instance_id() != "b" * 32


def test_a_file_from_before_the_home_witness_is_kept(isolated: Path) -> None:
    """An id written by an earlier client has no `home` and is still ours.

    Treating a missing witness as a mismatch would re-mint on upgrade and split
    every existing machine in two -- the bug, reintroduced by the guard against
    it.
    """
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(json.dumps({"device_instance_id": "a" * 32}))
    assert device_identity.device_instance_id() == "a" * 32


def test_a_corrupt_file_is_replaced_rather_than_fatal(isolated: Path) -> None:
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text("{ not json")
    value = device_identity.device_instance_id()
    assert value is not None
    assert device_headers(value)


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_an_unwritable_home_reports_no_identity_rather_than_an_unstable_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Better to look like an older client than to mint a new id per command.

    An identity that cannot be persisted would differ on every invocation, so
    every command would register another device -- the original bug, amplified
    from once-per-setup to once-per-command.
    """
    blocked = tmp_path / "blocked"
    blocked.mkdir()
    blocked.chmod(0o500)
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(blocked / "sub" / "device.json"))
    try:
        assert device_identity.device_instance_id() is None
    finally:
        blocked.chmod(0o700)


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission bits; Windows uses ACLs")
def test_the_file_is_not_world_readable(isolated: Path) -> None:
    """Not a secret, but it identifies a machine; keep it user-only like config."""
    device_identity.device_instance_id()
    assert isolated.stat().st_mode & 0o077 == 0


def test_a_concurrent_first_run_mints_exactly_one_identity(isolated: Path) -> None:
    """Two processes racing the first mint must not create two devices.

    `sdk/config.py::_config_lock` exists because "two `probe` processes can both
    read the file, each add their own context, and the second write silently
    drops the first -- reachable from ordinary use (a CI matrix, two worktree
    sessions)". A first-run mint has the identical shape, and its cost is a
    permanent duplicate row rather than a lost context.
    """
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: device_identity.device_instance_id(), range(8)))

    minted = {value for value in results if value is not None}
    assert minted, "every racer failed to mint"
    assert len(minted) == 1, f"the race produced {len(minted)} identities: {minted}"
    assert json.loads(isolated.read_text())["device_instance_id"] in minted


def test_a_file_this_machine_just_wrote_is_never_treated_as_a_rival(
    isolated: Path,
) -> None:
    """The shared-$HOME guard must not fire on our OWN file.

    Caught by CI on 3.11 after the guard was added: the first read is a
    snapshot, so in a race a second process finds the file the FIRST one wrote
    on this same machine, decides it belongs to a rival, and forks itself onto a
    namespaced path. Two ids for one laptop -- the exact failure the mint lock
    exists to prevent, reintroduced just above it. Existence is not the test;
    a DIFFERENT recorded home is.
    """
    minted = device_identity.device_instance_id()
    assert device_identity.device_instance_id() == minted
    # No namespaced sibling was created beside it.
    siblings = list(isolated.parent.glob(f"{isolated.stem}-*{isolated.suffix}"))
    assert siblings == [], f"forked onto {siblings} for its own file"


def test_the_lock_file_does_not_survive_a_mint(isolated: Path) -> None:
    """A stale lock must not make every later invocation fall back to None."""
    device_identity.device_instance_id()
    assert not isolated.with_suffix(".lock").exists()


@pytest.mark.parametrize(
    "value",
    ["", "short", "!" * 32, "x" * 200, None, 12345],
)
def test_a_malformed_identity_sends_no_header(value: object) -> None:
    """Drop, never 4xx. A bad header must not break a valid credential."""
    assert device_headers(value) == {}


def test_the_env_override_wins_over_the_config_derivation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    explicit = tmp_path / "explicit.json"
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(explicit))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "other" / "config.json"))
    assert device_identity.device_file() == explicit


def test_the_default_location_is_state_not_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """config.json is symlinked into dotfiles repos; state is not.

    An identity inside a dotfiles-managed config would be checked out on every
    machine that repo touches, merging them all into one device -- the one
    failure this design says must never happen.
    """
    monkeypatch.delenv("PROBE_DEVICE_ID_PATH", raising=False)
    monkeypatch.delenv("PROBE_CONFIG_PATH", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    resolved = device_identity.device_file()
    assert resolved == tmp_path / "state" / "probe" / "device.json"
    assert "config" not in str(resolved)


def test_the_transport_sends_the_machine_on_cli_and_sdk_but_never_mcp() -> None:
    """The MCP lane must not report a device, and the reason is structural.

    `_client_for_token` is shared by the local stdio server and the HOSTED one,
    which memoizes one transport per token while serving many people through it.
    A device identity fixed there would report our pod as every caller's machine
    -- the same bug `client_headers_scope` was introduced to prevent for
    versions.
    """
    from probe.sdk.surface import Surface
    from probe.sdk.transport import _device_headers_for

    assert _device_headers_for(Surface.CLI.value)
    assert _device_headers_for(Surface.SDK.value)
    assert _device_headers_for(Surface.MCP.value) == {}


def test_identity_failures_never_reach_the_caller(monkeypatch: pytest.MonkeyPatch) -> None:
    """A broken identity file must not fail a research write."""
    from probe.sdk.surface import Surface
    from probe.sdk.transport import _device_headers_for

    def boom() -> str:
        raise RuntimeError("disk on fire")

    monkeypatch.setattr(device_identity, "device_instance_id", boom)
    assert _device_headers_for(Surface.CLI.value) == {}


# ---------------------------------------------------------------------------
# The witness must not move with the network.
#
# Every test below is a regression on one production incident: a MacBook joined
# a captive campus WiFi, `socket.gethostname()` started returning
# `visitor-10-59-125-182`, the laptop stopped recognising its own device file,
# and it minted a second identity and a second Settings row.
# ---------------------------------------------------------------------------


def _rename_host(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    """What a DHCP lease does to `socket.gethostname()`, and nothing else."""
    monkeypatch.setattr(device_identity.socket, "gethostname", lambda: name)


def test_a_renamed_host_keeps_its_identity(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """THE BUG. Joining a network is not becoming a different computer."""
    _rename_host(monkeypatch, "my-laptop")
    minted = device_identity.device_instance_id()

    _rename_host(monkeypatch, "visitor-10-59-125-182")
    after = device_identity.device_instance_id()

    assert after == minted
    # And it did not quietly settle onto a namespaced file instead.
    assert list(isolated.parent.glob("device-*.json")) == []


def test_a_renamed_host_keeps_its_identity_across_many_networks(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A laptop is carried between networks, not just to one of them.

    Asserting a single rename would pass on an implementation that merely
    re-mints deterministically per host, which is the bug wearing a hat.
    """
    _rename_host(monkeypatch, "my-laptop")
    minted = device_identity.device_instance_id()

    for name in ("visitor-10-59-125-182", "guest-192-168-0-9", "my-laptop", "eduroam-42"):
        _rename_host(monkeypatch, name)
        assert device_identity.device_instance_id() == minted

    assert list(isolated.parent.glob("device-*.json")) == []


def test_a_legacy_file_is_adopted_and_stamped(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Upgrading must not split a machine, and must immunise it going forward."""
    _rename_host(monkeypatch, "my-laptop")
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(
        json.dumps({"device_instance_id": "c" * 32, "home": "my-laptop:" + str(Path.home())})
    )

    assert device_identity.device_instance_id() == "c" * 32

    stamped = json.loads(isolated.read_text())
    assert stamped["machine"] == device_identity._machine_witness()

    # The stamp is the point: the next rename is now a non-event.
    _rename_host(monkeypatch, "visitor-10-59-125-182")
    assert device_identity.device_instance_id() == "c" * 32



def test_without_a_stable_machine_id_the_old_behaviour_is_unchanged(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A platform offering no machine id is exactly as well off as before.

    It still splits on rename -- there is nothing left to recognise itself by --
    but it must not do anything WORSE, and must never write a `machine` it
    cannot honour.
    """
    monkeypatch.setattr(device_identity, "_machine_id", lambda: "")
    _rename_host(monkeypatch, "my-laptop")
    minted = device_identity.device_instance_id()
    assert "machine" not in json.loads(isolated.read_text())

    _rename_host(monkeypatch, "visitor-10-59-125-182")
    assert device_identity.device_instance_id() != minted


def test_two_machines_sharing_a_home_still_get_their_own_identities(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The guarantee the witness exists for, restated against the new witness."""
    monkeypatch.setattr(device_identity, "_machine_id", lambda: "machine-a")
    first = device_identity.device_instance_id()

    monkeypatch.setattr(device_identity, "_machine_id", lambda: "machine-b")
    second = device_identity.device_instance_id()

    assert first is not None
    assert second is not None
    assert first != second

    # ...and each settles back on its own file rather than fighting over one.
    monkeypatch.setattr(device_identity, "_machine_id", lambda: "machine-a")
    assert device_identity.device_instance_id() == first


def test_the_witness_does_not_record_the_raw_hardware_id(isolated: Path) -> None:
    """A hardware UUID is a durable cross-application fingerprint.

    It answers "same machine?" just as well hashed, and this file is readable by
    anything that can read $HOME.
    """
    device_identity.device_instance_id()
    written = isolated.read_text()
    machine = device_identity._machine_id()
    if machine:
        assert machine not in written


def test_the_migration_is_order_independent_when_it_starts_at_home(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The mirror of the forked-machine test: upgrade on the HOME network first.

    Which of a machine's two historical ids survives depends on where it happened
    to be standing when it first ran this code. Both are genuinely this machine,
    so either is defensible -- but the outcome must be STABLE once chosen, and
    only one of the two orders was pinned before.
    """
    home = str(Path.home())
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(json.dumps({"device_instance_id": "d" * 32, "home": "my-laptop:" + home}))
    forked_name = "visitor-10-59-125-182"
    fork = device_identity._namespaced(isolated, f"{forked_name}:{home}")
    fork.write_text(
        json.dumps({"device_instance_id": "e" * 32, "home": f"{forked_name}:{home}"})
    )

    _rename_host(monkeypatch, "my-laptop")
    assert device_identity.device_instance_id() == "d" * 32

    _rename_host(monkeypatch, forked_name)
    assert device_identity.device_instance_id() == "d" * 32


def test_a_failed_stamp_still_returns_the_adopted_identity(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Stamping is best effort; adoption is not."""
    _rename_host(monkeypatch, "my-laptop")
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(
        json.dumps({"device_instance_id": "f" * 32, "home": "my-laptop:" + str(Path.home())})
    )

    def _boom(*_args, **_kwargs):
        raise OSError("read-only home")

    monkeypatch.setattr(device_identity, "_write", _boom)
    assert device_identity.device_instance_id() == "f" * 32


def test_an_unusable_id_in_the_file_is_never_adopted(isolated: Path) -> None:
    """A malformed id must not reach the wire.

    `device_headers` drops one silently, but `device_authorize` sends the same
    value in a request BODY where nothing filters it, so a hand-edited file
    would turn into a 4xx on LOGIN rather than a missing telemetry header.
    """
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(json.dumps({"device_instance_id": "short", "home": None}))

    value = device_identity.device_instance_id()

    assert value != "short"
    assert value is not None
    assert device_headers(value) == {DEVICE_HEADER: value}


def test_a_device_file_that_is_not_a_regular_file_is_ignored(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A symlink is not a device file, however it is named.

    Following one lets a peer on a shared `$HOME` point this machine's identity
    at content they control -- or at `/dev/zero`, which reads until the process
    dies.
    """
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.parent.joinpath("elsewhere.json").write_text(
        json.dumps({"device_instance_id": "8" * 32, "machine": device_identity._machine_witness()})
    )
    isolated.symlink_to(isolated.parent / "elsewhere.json")
    _rename_host(monkeypatch, "my-laptop")

    assert device_identity._read(isolated) == {}
    assert device_identity.device_instance_id() != "8" * 32


def test_a_second_machine_never_adopts_a_hostname_keyed_fork(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """THE MERGE THIS MODULE EXISTS TO PREVENT, in its subtlest shape.

    DHCP names are derived from an IP, so two machines on one captive network
    are handed the SAME transient hostname. Machine A forks under it before the
    witness existed; machine B, sharing the `$HOME`, then sees a file whose only
    evidence is that name. Adopting it would hand B the id of A -- and stamping
    it would make the theft permanent, because the file is thereafter judged on
    B's witness alone and A can never reclaim it.
    """
    home = str(Path.home())
    shared_name = "visitor-10-59-125-182"
    _rename_host(monkeypatch, shared_name)

    # Machine A's pre-witness fork, keyed on the hostname the two machines share.
    fork = device_identity._namespaced(isolated, f"{shared_name}:{home}")
    fork.parent.mkdir(parents=True, exist_ok=True)
    fork.write_text(
        json.dumps({"device_instance_id": "a" * 32, "home": f"{shared_name}:{home}"})
    )
    # ...and a canonical file belonging to some third machine, so resolution
    # reaches the namespaced branch at all.
    isolated.write_text(
        json.dumps({"device_instance_id": "c" * 32, "machine": "m1:" + "f" * 32})
    )

    monkeypatch.setattr(device_identity, "_machine_id", lambda: "b" * 32)
    mine = device_identity.device_instance_id()

    assert mine is not None
    assert mine != "a" * 32, "machine B adopted machine A's identity"
    assert json.loads(fork.read_text())["device_instance_id"] == "a" * 32
    assert "machine" not in json.loads(fork.read_text()), "A's file was stamped by B"


def test_this_machine_finds_its_own_namespaced_file_from_any_network(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A shared `$HOME` machine never owns the canonical file, so it must resolve
    its own namespaced one directly -- on every network, without a scan."""
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(
        json.dumps({"device_instance_id": "c" * 32, "machine": "m1:" + "f" * 32})
    )
    _rename_host(monkeypatch, "my-laptop")
    mine = device_identity.device_instance_id()

    for name in ("visitor-10-59-125-182", "guest-192-168-0-9", "my-laptop"):
        _rename_host(monkeypatch, name)
        assert device_identity.device_instance_id() == mine


@pytest.mark.skipif(not hasattr(os, "mkfifo"), reason="no FIFOs on Windows")
def test_a_canonical_file_that_blocks_on_open_cannot_hang_the_cli(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A shared `$HOME` is writable by a peer, and `open()` on a FIFO with no
    writer never returns -- on the startup path, before anything is printed."""
    isolated.parent.mkdir(parents=True, exist_ok=True)
    os.mkfifo(isolated)
    _rename_host(monkeypatch, "my-laptop")

    assert device_identity._read(isolated) == {}


def test_an_oversized_file_is_not_read_into_memory(isolated: Path) -> None:
    """`$HOME` is writable by a peer; the read is bounded, not trusting."""
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(" " * (device_identity._MAX_DEVICE_FILE_BYTES + 1024) + "{}")
    assert device_identity._read(isolated) == {}


@pytest.mark.parametrize("value", ["uninitialized", "0" * 32, "", "NOT-HEX", "abc"])
def test_a_machine_id_that_identifies_a_CLASS_of_machines_is_refused(value: str) -> None:
    """systemd writes `uninitialized` during first boot and factory reset, and
    some VMs return an all-zero hardware UUID. Both are stable and IDENTICAL
    across every host in that state: a fleet-wide merge dressed as a witness."""
    assert not device_identity._usable_machine_id(value)


def test_a_real_machine_id_is_accepted_and_cached_only_when_usable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Caching a miss would pin a long-lived process to the hostname fallback."""
    monkeypatch.setattr(device_identity, "_MACHINE_ID_CACHE", "")
    calls: list[int] = []

    def _flaky() -> str:
        calls.append(1)
        return "uninitialized" if len(calls) == 1 else "9931886db6634709a34c980c5c988982"

    monkeypatch.setattr(device_identity, "_darwin_host_uuid", _flaky)
    monkeypatch.setattr(device_identity.sys, "platform", "darwin")
    monkeypatch.setattr(
        device_identity.Path, "read_text", lambda *_a, **_k: (_ for _ in ()).throw(OSError())
    )

    assert _REAL_MACHINE_ID() == ""
    assert _REAL_MACHINE_ID() == "9931886db6634709a34c980c5c988982"
    assert _REAL_MACHINE_ID() == "9931886db6634709a34c980c5c988982"
    assert len(calls) == 2, "a usable id must be cached, an unusable one retried"


def test_the_macos_uuid_lookup_is_bounded_and_fails_soft(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`gethostuuid(2)` reads a zero wait as "block forever"; a stall must not
    hang every CLI invocation before it has printed anything."""
    import ctypes

    seen: dict[str, object] = {}

    class _FakeLibc:
        def __init__(self) -> None:
            self.gethostuuid = self

        argtypes: object = None
        restype: object = None

        def __call__(self, buf, wait):
            seen["tv_sec"] = wait._obj.tv_sec
            return -1

    monkeypatch.setattr(ctypes, "CDLL", lambda _name: _FakeLibc())

    assert device_identity._darwin_host_uuid() == ""
    assert seen["tv_sec"] == device_identity._UUID_WAIT_SECONDS
    assert seen["tv_sec"] > 0

def test_a_machine_that_already_forked_settles_on_ONE_id_going_forward(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The state a laptop bitten by this bug is actually in, today.

    Two legacy files, both genuinely this machine's: the original under its real
    name, and the fork minted while the network was renaming it. Reclaiming the
    fork is NOT safe -- a DHCP name is shared between machines, so a file keyed
    on one is not proof of ownership (see
    `test_a_second_machine_never_adopts_a_hostname_keyed_fork`). What this
    machine must do instead is stop accumulating: pick one id and keep it on
    every network, leaving the stale row to be retired by hand.
    """
    home = str(Path.home())
    isolated.parent.mkdir(parents=True, exist_ok=True)
    isolated.write_text(json.dumps({"device_instance_id": "d" * 32, "home": "my-laptop:" + home}))
    forked_name = "visitor-10-59-125-182"
    fork = device_identity._namespaced(isolated, f"{forked_name}:{home}")
    fork.write_text(json.dumps({"device_instance_id": "e" * 32, "home": f"{forked_name}:{home}"}))

    _rename_host(monkeypatch, forked_name)
    settled = device_identity.device_instance_id()
    assert settled is not None

    # Whatever it settled on, it is now the answer everywhere -- which is the
    # whole point. No third id, and no alternation.
    for name in ("my-laptop", forked_name, "guest-192-168-0-9", "my-laptop"):
        _rename_host(monkeypatch, name)
        assert device_identity.device_instance_id() == settled

def test_replicas_of_one_image_do_not_merge_into_one_machine(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`/etc/machine-id` names an IMAGE, not a machine.

    Three replicas of one image sharing one `$HOME` volume all read the same
    file, so trusting it would hand them a single identity -- the merge this
    module ranks below any split. Inside a container the witness is withheld and
    the per-container hostname governs, which is correct there.
    """
    monkeypatch.setattr(device_identity, "_MACHINE_ID_CACHE", "")
    monkeypatch.setattr(device_identity, "_in_container", lambda: True)
    monkeypatch.setattr(
        device_identity.Path, "read_text", lambda *_a, **_k: "9931886db6634709a34c980c5c988982"
    )
    monkeypatch.setattr(device_identity.sys, "platform", "linux")
    assert _REAL_MACHINE_ID() == "", "a container's baked machine-id was trusted"

    # Undo the fixture's pin: resolution must see what the REAL lookup returned.
    monkeypatch.setattr(device_identity, "_machine_id", _REAL_MACHINE_ID)
    seen = set()
    for replica in ("replica-a", "replica-b", "replica-c"):
        _rename_host(monkeypatch, replica)
        seen.add(device_identity.device_instance_id())
    assert len(seen) == 3, f"replicas merged into {len(seen)} identity/identities"


def test_a_bare_metal_host_still_gets_the_stable_witness(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The container carve-out must not cost an ordinary Linux box the fix."""
    monkeypatch.setattr(device_identity, "_MACHINE_ID_CACHE", "")
    monkeypatch.setattr(device_identity, "_in_container", lambda: False)
    monkeypatch.setattr(
        device_identity.Path, "read_text", lambda *_a, **_k: "9931886db6634709a34c980c5c988982\n"
    )
    assert _REAL_MACHINE_ID() == "9931886db6634709a34c980c5c988982"


@pytest.mark.parametrize(
    ("dockerenv", "cgroup", "expected"),
    [
        (True, "", True),
        (False, "0::/kubepods/besteffort/pod123/abc", True),
        (False, "12:devices:/docker/abcdef", True),
        (False, "0::/system.slice/ssh.service", False),
        (False, None, False),
    ],
)
def test_container_detection_reads_only_signals_a_runtime_creates(
    dockerenv: bool, cgroup: str | None, expected: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A false positive costs a host the fix, so the signals stay narrow."""
    monkeypatch.setattr(device_identity.Path, "exists", lambda _self: dockerenv)

    def _read(_self, **_kwargs):
        if cgroup is None:
            raise OSError("no /proc on this platform")
        return cgroup

    monkeypatch.setattr(device_identity.Path, "read_text", _read)
    assert device_identity._in_container() is expected
