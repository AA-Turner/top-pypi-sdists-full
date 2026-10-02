"""Probe and W&B side by side in one script (W&B offline: no account).

What it simulates: a team mid-migration that runs both SDKs in the same
training script -- both init, both log the same metrics, both finish -- and
the ways such a script ends: normally, ``sys.exit(2)``, an uncaught
exception, and Ctrl-C (SIGINT to the whole process group, as a terminal
sends it). Both SDKs install exit hooks (``sys.excepthook``, atexit; W&B
also a service process), so each ending is run in BOTH import/init orders.
Plus ``wandb.init(sync_tensorboard=True)`` with a torch SummaryWriter.

Real: wandb (offline mode, its wandb-core service), torch's SummaryWriter,
the released Probe SDK, real child processes and real signals. Simulated:
the Probe server (the fake, unless PROBE_BASE_URL is set); W&B's server is
not involved (offline), and its record is read back from the run's own
transaction log (``wb_read.py``).
"""

from __future__ import annotations

import glob
import os
import signal
import time
from pathlib import Path

import pytest

from tests.environments import envchild, envkit

pytestmark = envkit.requires_env

TIMEOUT = 240
ORDERS = ["probe-first", "wandb-first"]
#: end -> (exit code, Probe status, W&B exit record)
ENDS = {
    "ok": (0, "completed", 0),
    "exit2": (2, "failed", 2),
    "raise": (1, "failed", 1),
    # Ctrl-C: the process dies BY SIGINT (130 in a shell); Probe reads it
    # `canceled`. W&B's exit record for a KeyboardInterrupt is 255.
    "sigint": (-signal.SIGINT, "canceled", 255),
}


def _sigint_when_ready(proc, out_path: Path) -> None:
    deadline = time.monotonic() + 150
    while time.monotonic() < deadline and proc.poll() is None:
        if "READY" in out_path.read_text(errors="replace"):
            os.killpg(proc.pid, signal.SIGINT)
            return
        time.sleep(0.2)


def _wandb_record(dirs, res) -> dict:
    run_dir = os.path.dirname(res["wandb_dir"].rstrip("/"))
    if not glob.glob(os.path.join(run_dir, "run-*.wandb")):
        (run_dir,) = glob.glob(os.path.join(str(dirs.work), "wandb", "offline-run-*"))
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("wandb_side_by_side", "wb_read.py"), run_dir],
        env=envkit.child_env_offline(dirs),
        cwd=dirs.work,
        timeout=60,
    )
    assert child.returncode == 0, child.tail()
    return child.result("wbread")


def _run(target, dirs, order: str, end: str, *extra: str) -> tuple[envkit.Child, dict]:
    envkit.requirement("wandb")
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("wandb_side_by_side", "wb_job.py"), order, end, *extra],
        env=envkit.child_env(target, dirs),
        cwd=dirs.work,
        timeout=TIMEOUT,
        on_start=_sigint_when_ready if end == "sigint" else None,
    )
    assert not child.timed_out, f"hung: {child.tail()}"
    return child, child.result("wb")


@pytest.mark.parametrize("end", list(ENDS))
@pytest.mark.parametrize("order", ORDERS)
def test_both_sdks_in_one_script(target, dirs, started, order, end):
    want_rc, want_status, want_wandb_exit = ENDS[end]
    child, res = _run(target, dirs, order, end)
    reader = target.reader()
    run_id = res["run_id"]
    status = envkit.wait_status(reader, run_id)
    wb = _wandb_record(dirs, res)
    history = [r for r in wb["history"] if "train" in r or "train/loss" in r]
    summary = (
        f"[{order}/{end}] rc={child.returncode} probe={status} "
        f"wandb_exit={wb['exit_codes']} wandb_rows={len(history)} hooks={res['hooks']} "
        f"{child.elapsed:.1f}s"
    )
    print(summary)

    # Probe: every point, the right verdict, the lease released with it.
    missing, wrong, _ = envkit.reconcile(reader, run_id, envchild.expected(range(12)))
    assert not missing and not wrong, (summary, missing[:4], wrong[:4])
    assert status == want_status, summary
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    assert leases == [("owner", None, True, want_status)], (summary, leases)
    # W&B: its 12 rows, its own exit record.
    assert len(history) == 12, summary
    assert wb["exit_codes"] == [want_wandb_exit], summary
    # The process: the exit code the script's own ending means.
    assert child.returncode == want_rc, f"{summary}\n{child.tail()}"
    if end == "ok":
        names = set(res["artifacts"])
        arts = envkit.wait_artifacts(reader, run_id, names)
        assert names <= set(arts), (names, sorted(arts))
    assert "Traceback" not in child.stderr or end == "raise" or end == "sigint", child.tail()
    assert envkit.leaked_files([run_id], started) == []


@pytest.mark.parametrize("order", ORDERS)
def test_sync_tensorboard_beside_probe(target, dirs, order):
    envkit.requirement("torch.utils.tensorboard")
    child, res = _run(target, dirs, order, "ok", "--tb")
    assert child.returncode == 0, child.tail()
    reader = target.reader()
    run_id = res["run_id"]
    assert envkit.wait_status(reader, run_id) == "completed"
    missing, wrong, got = envkit.reconcile(reader, run_id, envchild.expected(range(12)))
    assert not missing and not wrong, (missing[:4], wrong[:4])
    # Probe does not read TensorBoard: no tb/* series appears on the Probe run.
    assert not [k for k in got if k[1].startswith("tb/")], sorted(got)[:5]
    wb = _wandb_record(dirs, res)
    tb_rows = [r for r in wb["history"] if "tb/loss" in r or "loss" in r and "global_step" in r]
    print(f"[{order}/tb] wandb rows {len(wb['history'])} (tb rows {len(tb_rows)}), exit {wb['exit_codes']}")
    assert wb["exit_codes"] == [0]
    assert tb_rows, f"wandb synced no TensorBoard scalar: {wb['history'][:3]}"
