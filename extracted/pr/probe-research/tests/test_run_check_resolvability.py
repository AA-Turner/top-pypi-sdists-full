"""`run check` must not say "complete" on the strength of a row existing.

Seventeen bird-sql-sft runs read as captured for a week because the check counted
artifacts instead of proving retrieval. Their code_snapshot rows were all present
and all pointed at commits that lived nowhere.

Proving retrieval was the first fix. Not needing to is the second: since git
referencing was retired a run's code lives in R2, so `n_git_referenced == 0`
earns `complete` outright and the network probe is left for the runs captured
while the old classifier was live.
"""

from __future__ import annotations

import subprocess


from probe.sdk.snapshot import commit_on_remote


class _Client:
    """Just enough of Client to exercise check_run against a canned bundle."""

    def __init__(self, bundle):
        self._bundle = bundle

    def run_bundle(self, run_id):
        return self._bundle


def _check(bundle, **kw):
    from probe.sdk.client import Client

    c = _Client(bundle)
    return Client.check_run(c, "run-1", **kw)


def _bundle(*, env_ref="e" * 64, snapshot_meta=None, artifacts=None):
    arts = (
        artifacts
        if artifacts is not None
        else [
            {
                "kind": "code_snapshot",
                "is_reference": True,
                "meta": snapshot_meta
                if snapshot_meta is not None
                else {
                    "base_commit": "d" * 40,
                    "remote": "https://github.com/acme/repo.git",
                    "n_git_referenced": 10,
                    "n_pending_upload": 0,
                },
            },
        ]
    )
    return {"run": {"env_ref": env_ref, "metadata": {}}, "artifacts": arts}


# --- the verdict vocabulary ------------------------------------------------


def test_default_is_unverified_not_complete():
    """The word that caused this. Nothing absent is not the same as rebuildable."""
    assert _check(_bundle())["state"] == "unverified"


def test_complete_is_only_earned_by_verifying(monkeypatch):
    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", lambda *a, **k: True)
    assert _check(_bundle(), verify=True)["state"] == "complete"


def test_unresolvable_reference_is_incomplete(monkeypatch):
    """The 17-run case: the row is there, the commit is not."""
    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", lambda *a, **k: False)
    out = _check(_bundle(), verify=True)
    assert out["state"] == "incomplete"
    assert "unresolvable_code_reference" in out["missing"]


# --- the runs that need no probe at all ------------------------------------


def _self_contained(**over):
    meta = {
        "base_commit": "d" * 40,
        "remote": "https://github.com/acme/repo.git",
        "n_git_referenced": 0,
        "n_pending_upload": 0,
    }
    meta.update(over)
    return _bundle(snapshot_meta=meta)


def test_a_self_contained_capture_verifies_without_touching_the_network(monkeypatch):
    """Every byte is on Probe, so there is nothing for a fetch to prove."""

    def _never(*a, **k):
        raise AssertionError("check_run must not probe a remote it does not need")

    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", _never)
    out = _check(_self_contained(), verify=True)
    assert out["state"] == "complete"
    assert out["verified_code_reference"] is True
    assert out["missing"] == []


def test_a_stale_commit_no_longer_fails_a_run_whose_bytes_are_stored(monkeypatch):
    """base_commit is provenance now. A force-push or a deleted fork makes it
    unresolvable and changes nothing about whether the code can be rebuilt --
    reporting `incomplete` there would be the 17-run mistake inverted, calling a
    captured run lost."""
    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", lambda *a, **k: False)
    out = _check(_self_contained(), verify=True)
    assert out["state"] == "complete"
    assert "unresolvable_code_reference" not in out["missing"]


def test_an_offsite_reference_does_not_disqualify_the_capture(monkeypatch):
    """A deliberate size reference is part of a complete capture, not a gap.

    Maintainer decision 2026-08-21. A file over the threshold has its bytes
    off-platform, so `complete` here is NOT a claim that the run rebuilds from
    Probe alone -- it is the same judgment `capture-run-inputs` already states
    to agents ("they are not failures"). The alternative, downgrading every run
    that references a big checkpoint, calls a correctly-captured run unproven.
    """

    def _never(*a, **k):
        raise AssertionError("an offsite reference is not a reason to probe git")

    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", _never)
    out = _check(_self_contained(n_referenced_offsite=2), verify=True)
    assert out["state"] == "complete"
    assert out["missing"] == [], "a deliberate reference is not a capture GAP"


def test_a_non_integer_count_does_not_earn_the_short_circuit(monkeypatch):
    """`false` is not zero. Python says otherwise (False == 0), and this value
    arrives as server JSON, so the guard is typed rather than truthy -- a
    malformed meta must fall through to the probe, not collect `complete`."""
    monkeypatch.setattr("probe.sdk.snapshot.commit_on_remote", lambda *a, **k: False)
    out = _check(_self_contained(n_git_referenced=False), verify=True)
    assert out["state"] == "incomplete"
    assert "unresolvable_code_reference" in out["missing"]


def test_pending_bytes_still_beat_the_short_circuit():
    """`n_git_referenced == 0` says nothing was excused from upload -- not that
    the upload happened. The pending count is still the gate."""
    out = _check(_self_contained(n_pending_upload=2), verify=True)
    assert out["state"] == "incomplete"
    assert "pending_code_bytes" in out["missing"]


# --- the free check --------------------------------------------------------


def test_pending_bytes_are_incomplete_without_any_network():
    """Costs a dict lookup: the summary already rode in on the artifact meta."""
    out = _check(
        _bundle(
            snapshot_meta={
                "base_commit": "d" * 40,
                "remote": "r",
                "n_git_referenced": 9,
                "n_pending_upload": 1,
            }
        )
    )
    assert out["state"] == "incomplete"
    assert "pending_code_bytes" in out["missing"]


def test_zero_pending_does_not_flag():
    assert "pending_code_bytes" not in _check(_bundle())["missing"]


# --- pre-existing checks still hold ---------------------------------------


def test_missing_env_ref_still_incomplete():
    out = _check(_bundle(env_ref=None))
    assert out["state"] == "incomplete" and "execution_record" in out["missing"]


def test_missing_code_snapshot_still_incomplete():
    out = _check(_bundle(artifacts=[]))
    assert "code_snapshot_artifact" in out["missing"]


def test_old_run_without_a_manifest_cannot_be_verified(monkeypatch):
    """Pre-0.26.3 captures recorded no base_commit; refuse to guess either way."""
    out = _check(_bundle(snapshot_meta={"dirty": False}), verify=True)
    assert out["verified_code_reference"] is False
    assert out["state"] == "unverified"


# --- the network probe -----------------------------------------------------


def test_commit_on_remote_is_false_for_an_unreachable_host():
    # 10.255.255.1 blackholes the SYN, so this test costs exactly `timeout`
    # seconds of waiting -- it is bounded by the knob, not by the network. The
    # guarantee under test is "an unreachable host answers False instead of
    # hanging", which one second proves as well as five, so CI does not pay
    # four extra seconds to re-prove it.
    commit_on_remote.cache_clear()
    assert commit_on_remote("https://10.255.255.1/nope.git", "a" * 40, timeout=1.0) is False


def test_commit_on_remote_rejects_empty_inputs():
    assert commit_on_remote("", "a" * 40) is False
    assert commit_on_remote("https://example.com/r.git", "") is False


def test_commit_on_remote_is_memoized_so_audits_do_not_scale_with_runs(tmp_path):
    """Runs from one machine share a base commit; 200 runs must not be 200 fetches."""
    remote = tmp_path / "r.git"
    subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
    work = tmp_path / "w"
    work.mkdir()
    for args in (
        ["init", "-q"],
        ["config", "user.email", "t@t"],
        ["config", "user.name", "t"],
        ["remote", "add", "origin", str(remote)],
    ):
        subprocess.run(["git", *args], cwd=work, check=True)
    (work / "a.py").write_text("a = 1\n")
    subprocess.run(["git", "add", "-A"], cwd=work, check=True)
    subprocess.run(["git", "commit", "-qm", "i"], cwd=work, check=True)
    subprocess.run(["git", "push", "-q", "origin", "HEAD:refs/heads/main"], cwd=work, check=True)
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=work, capture_output=True, text=True
    ).stdout.strip()

    commit_on_remote.cache_clear()
    assert commit_on_remote(str(remote), sha) is True
    before = commit_on_remote.cache_info()
    for _ in range(50):
        commit_on_remote(str(remote), sha)
    after = commit_on_remote.cache_info()
    assert after.misses == before.misses, "repeat audits must be served from cache"
    assert after.hits >= 50
