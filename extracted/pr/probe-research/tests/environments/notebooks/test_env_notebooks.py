"""Notebooks: a real ipykernel, driven by nbclient the way JupyterLab drives it.

The kernel is the RELEASED SDK's interpreter (a kernelspec pointing at
``PROBE_ENV_PYTHON``, which run.sh gives ``ipykernel``), started with a
customer's environment, and cells execute one by one over the Jupyter
protocol. A restart is ``KernelManager.restart_kernel`` and the end of a
notebook is nbclient's graceful shutdown (``shutdown_request``, then a kill
after jupyter_client's default 5 s) -- the same calls JupyterLab's "Restart"
and "Shut Down Kernel" make.

Colab and Kaggle are SIMULATED by their tell-tale environment variables only:
no ``google.colab`` module, no /content or /kaggle mounts, no container, no
Google Drive. The SDK keys its "disposable machine" verdict on those variables
(``COLAB_RELEASE_TAG``) and on container marker files (/.dockerenv, which real
Kaggle has and this simulation does not), so the test pins the verdict the SDK
reaches here and says why it would differ on the real service.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from tests.environments import envlib
from tests.environments.envlib import record

pytestmark = [envlib.requires_env]

if envlib.ENABLED:
    # An opt-in run that silently skipped would read as a pass: fail instead.
    import nbclient
    import nbformat  # noqa: F401 -- the notebook object model nbclient runs
else:
    nbformat = pytest.importorskip("nbformat")
    nbclient = pytest.importorskip("nbclient")

KERNEL = "probe-env-released"
TERMINAL = {"completed", "failed", "crashed", "canceled"}


def _kernelspec(root: Path, sdk_py: str) -> Path:
    spec = root / "jupyter" / "kernels" / KERNEL
    spec.mkdir(parents=True, exist_ok=True)
    (spec / "kernel.json").write_text(
        json.dumps(
            {
                "argv": [sdk_py, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                "display_name": "probe released SDK",
                "language": "python",
            }
        )
    )
    return root / "jupyter"


def _prelude(name: str, *, external_id: str | None = None) -> str:
    ext = f", external_id={external_id!r}" if external_id else ""
    return (
        "import os, sys, json\n"
        f"sys.path.insert(0, {str(envlib.HERE)!r})\n"
        "from customer_loop import row, CONFIG, _where_the_outbox_is\n"
        "import probe\n"
        f"run = probe.init(project=os.environ['PROBE_ENV_PROJECT'], name={name!r}{ext})\n"
        "print('PROBE-ENV ' + json.dumps({'event': 'run', 'id': run.id, 'outbox': _where_the_outbox_is()}))\n"
    )


def _log_cell(first: int, last: int) -> str:
    return f"for s in range({first}, {last + 1}):\n    probe.log(row(s), step=s)\n"


class Notebook:
    """Cells executed one at a time on one kernel, with restarts on request."""

    def __init__(self, sdk_py: str, env: dict[str, str], cwd: Path, root: Path, monkeypatch):
        from nbformat.v4 import new_notebook

        monkeypatch.setenv("JUPYTER_PATH", str(_kernelspec(root, sdk_py)))
        monkeypatch.setenv("JUPYTER_RUNTIME_DIR", str(root / "jupyter-runtime"))
        self.nb = new_notebook()
        self.client = nbclient.NotebookClient(
            self.nb,
            kernel_name=KERNEL,
            timeout=300,
            allow_errors=True,
            resources={"metadata": {"path": str(cwd)}},
        )
        self.env = env
        self.outputs: list[str] = []
        self.errors: list[str] = []

    def __enter__(self):
        self._cm = self.client.setup_kernel(env=self.env)
        self._cm.__enter__()
        return self

    def __exit__(self, *exc):
        # nbclient's own cleanup: a graceful shutdown, as when a notebook ends.
        return self._cm.__exit__(*exc)

    def run(self, source: str) -> None:
        from nbformat.v4 import new_code_cell

        cell = new_code_cell(source)
        self.nb.cells.append(cell)
        self.client.execute_cell(cell, len(self.nb.cells) - 1)
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                self.outputs.append(out.get("text", ""))
            elif out.get("output_type") == "error":
                self.errors.append(f"{out.get('ename')}: {out.get('evalue')}")

    def restart(self, *, now: bool) -> None:
        from jupyter_core.utils import run_sync

        run_sync(self.client.km.restart_kernel)(now=now)
        run_sync(self.client.kc.wait_for_ready)(timeout=120)

    def events(self) -> envlib.LoopEvents:
        return envlib.LoopEvents.parse("".join(self.outputs))


def _open(be, sdk_py, tmp_path, monkeypatch, **extra):
    env = envlib.child_env(be, tmp_path, **extra)
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    return Notebook(sdk_py, env, work, tmp_path, monkeypatch)


def _common(be, run_id: str, steps, *, want_status: set[str], config: bool = False) -> dict:
    rec = be.wait_points(run_id, envlib.expected_points(steps), timeout=60)
    status = be.wait_status(run_id, TERMINAL, timeout=60)
    run = be.run(run_id)
    return {
        "rec": rec,
        "status": status,
        "status_ok": status in want_status,
        "config": (run.get("config") or {}).get("model") == envlib.CONFIG["model"] if config else None,
    }


def test_env_notebook_run_opened_in_one_cell_logged_across_cells(be, sdk_py, sdk_version, tmp_path, monkeypatch):
    started = time.time()
    with _open(be, sdk_py, tmp_path, monkeypatch) as nb:
        nb.run(_prelude("nb-across-cells"))
        nb.run(_log_cell(0, 9))
        nb.run(_log_cell(10, 19))
        nb.run("probe.update_config(CONFIG)")
        nb.run(
            "open('small.txt', 'w').write('notebook artifact\\n')\n"
            "probe.log_artifact('small.txt', path='small.txt')"
        )
        nb.run("probe.finish()")
    run_id = nb.events().run_id
    got = _common(be, run_id, range(0, 20), want_status={"completed"}, config=True)
    arts = {a.get("name"): a.get("status") for a in be.artifacts(run_id)}
    home = envlib.real_home_writes(started, [run_id, str(tmp_path)])
    record(
        "notebook/across-cells",
        sdk=sdk_version,
        points=got["rec"].summary(),
        status=got["status"],
        config=got["config"],
        small_artifact=arts.get("small.txt"),
        cell_errors=nb.errors,
        real_home_writes=home,
    )
    assert nb.errors == []
    assert got["rec"].ok and got["status"] == "completed" and got["config"]
    assert arts.get("small.txt") == "complete"
    assert home == []


_KILLED_KERNEL_LEFT_RUNNING = (
    "finding (reported by lane E3): a kernel that is killed (forced restart, OOM) leaves its "
    "run `running` until the 15-min reaper -- under ipykernel the SDK starts no output helper, "
    "so nothing reports the writer gone (plan 2.2 covers scripts only)"
)


@pytest.mark.parametrize(
    "now",
    [False, pytest.param(True, marks=pytest.mark.xfail(strict=True, reason=_KILLED_KERNEL_LEFT_RUNNING))],
    ids=["restart", "restart-forced"],
)
def test_env_notebook_kernel_restart_mid_run(be, sdk_py, sdk_version, tmp_path, monkeypatch, now):
    """Run 1 logs steps 0..9, the kernel restarts ("Restart" = graceful; the
    forced one is what Jupyter does to a kernel that does not answer), and
    the notebook is re-run from the top: run 2 logs 10..19 and finishes.

    Pass = run 1 keeps every point it logged and ENDS (not left `running`
    for the reaper) within 60 s; run 2 is complete."""
    with _open(be, sdk_py, tmp_path, monkeypatch) as nb:
        nb.run(_prelude("nb-restart-1"))
        nb.run(_log_cell(0, 9))
        nb.restart(now=now)
        nb.run(_prelude("nb-restart-2"))
        nb.run(_log_cell(10, 19))
        nb.run("probe.finish()")
    ids = [e["id"] for e in nb.events().events if e.get("event") == "run"]
    assert len(ids) == 2, nb.outputs
    first = _common(be, ids[0], range(0, 10), want_status={"completed", "canceled", "failed", "crashed"})
    second = _common(be, ids[1], range(10, 20), want_status={"completed"})
    record(
        f"notebook/kernel-restart[{'forced' if now else 'graceful'}]",
        sdk=sdk_version,
        run_1_points=first["rec"].summary(),
        run_1_status=first["status"],
        run_2_points=second["rec"].summary(),
        run_2_status=second["status"],
        cell_errors=nb.errors,
    )
    assert nb.errors == []
    assert second["rec"].ok and second["status"] == "completed"
    assert first["rec"].ok, f"run 1 lost points in the restart: {first['rec'].summary()}"
    assert first["status_ok"], f"run 1 left {first['status']!r} after the kernel restart"


def test_env_notebook_exception_in_a_cell_keeps_the_run(be, sdk_py, sdk_version, tmp_path, monkeypatch):
    """IPython shows a cell's traceback and the kernel carries on: the run
    must too -- not closed `failed` by an excepthook, still taking logs."""
    with _open(be, sdk_py, tmp_path, monkeypatch) as nb:
        nb.run(_prelude("nb-exception"))
        nb.run(_log_cell(0, 9))
        nb.run("raise ValueError('bad batch')")
        nb.run(_log_cell(10, 19))
        nb.run("probe.finish()")
    run_id = nb.events().run_id
    got = _common(be, run_id, range(0, 20), want_status={"completed"})
    record(
        "notebook/cell-exception",
        sdk=sdk_version,
        points=got["rec"].summary(),
        status=got["status"],
        cell_errors=nb.errors,
    )
    assert nb.errors == ["ValueError: bad batch"]
    assert got["rec"].ok, got["rec"].summary()
    assert got["status"] == "completed"


def test_env_notebook_finish_never_called_then_kernel_shuts_down(be, sdk_py, sdk_version, tmp_path, monkeypatch):
    """The common notebook ending: nobody calls finish(); the notebook is
    closed and its kernel shut down. Pass = every point and the config land
    and the run ends `completed` (its atexit close), not `running`."""
    with _open(be, sdk_py, tmp_path, monkeypatch) as nb:
        nb.run(_prelude("nb-no-finish"))
        nb.run(_log_cell(0, 19))
        nb.run("probe.update_config(CONFIG)")
    run_id = nb.events().run_id
    got = _common(be, run_id, range(0, 20), want_status={"completed"}, config=True)
    record(
        "notebook/no-finish-shutdown",
        sdk=sdk_version,
        points=got["rec"].summary(),
        status=got["status"],
        config=got["config"],
        cell_errors=nb.errors,
    )
    assert got["rec"].ok, got["rec"].summary()
    assert got["config"]
    assert got["status"] == "completed"


_HOSTED = {
    # Colab's own variables (a Colab VM exports these to every kernel).
    "colab": {
        "COLAB_RELEASE_TAG": "release-colab_20260920-060000_RC00",
        "COLAB_BACKEND_VERSION": "next",
        "COLAB_GPU": "",
    },
    # Kaggle's kernel variables.
    "kaggle": {
        "KAGGLE_KERNEL_RUN_TYPE": "Interactive",
        "KAGGLE_URL_BASE": "https://www.kaggle.com",
        "KAGGLE_DOCKER_IMAGE": "gcr.io/kaggle-images/python",
    },
}
#: The SDK's verdict on its queue's disk in each simulation, and why.
_VERDICT = {
    # COLAB_RELEASE_TAG is one of the SDK's disposable-machine markers.
    "colab": False,
    # No Kaggle variable is a marker; real Kaggle is still judged disposable,
    # through /.dockerenv, which this host-side simulation cannot have.
    "kaggle": True,
}


@pytest.mark.parametrize("hosted", sorted(_HOSTED))
def test_env_notebook_hosted_colab_kaggle_simulated(be, sdk_py, sdk_version, tmp_path, monkeypatch, hosted):
    """The across-cells loop with a 65 MiB artifact, under Colab's or
    Kaggle's tell-tale variables. On a machine the SDK judges disposable the
    big upload is sent before the close returns, never left to a background
    worker that dies with the VM."""
    with _open(be, sdk_py, tmp_path, monkeypatch, **_HOSTED[hosted]) as nb:
        nb.run(_prelude(f"nb-{hosted}"))
        nb.run(_log_cell(0, 19))
        nb.run("probe.update_config(CONFIG)")
        nb.run(
            "import os\n"
            "with open('big.bin', 'wb') as fh:\n"
            "    fh.write(os.urandom(16))  # unique per run: one active upload per hash\n"
            "    fh.truncate(65 * 1024 * 1024 + 7)\n"
            "probe.log_artifact('big.bin', path='big.bin')"
        )
        nb.run("probe.finish()")
    event = nb.events().first("run") or {}
    run_id = event.get("id")
    outbox = event.get("outbox") or {}
    # Read at once: on a disposable machine the close itself must have sent it.
    big_at_close = {a.get("name"): a.get("status") for a in be.artifacts(run_id)}.get("big.bin")
    got = _common(be, run_id, range(0, 20), want_status={"completed"}, config=True)
    record(
        f"notebook/hosted[{hosted}]",
        sdk=sdk_version,
        outbox_verdict={k: outbox.get(k) for k in ("durable", "reason")},
        points=got["rec"].summary(),
        status=got["status"],
        config=got["config"],
        big_artifact_when_close_returned=big_at_close,
        cell_errors=nb.errors,
    )
    assert nb.errors == []
    assert got["rec"].ok and got["status"] == "completed" and got["config"]
    assert outbox.get("durable") is _VERDICT[hosted], outbox
    if _VERDICT[hosted] is False:
        assert big_at_close == "complete", big_at_close
