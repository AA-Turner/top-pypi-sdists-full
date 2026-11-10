"""`python -m probe.integrations.verl.launch [--] [python3] -m verl.trainer.main_ppo <overrides...>` (also
`verl.experimental.fully_async_policy.fully_async_main`, `verl.experimental.one_step_off_policy.main_ppo`, or a
script): run a verl job with Probe. Every verl entry point hands its composed config to `run_ppo`
(`trainer/main_ppo.py:35`), which calls `ray.init` with verl's runtime env. The launcher wraps `run_ppo` in this
driver: it opens the run (reopened with a rewind on a resume), puts the setup hook and `PROBE_*` in the Ray job
config that `ray.init` merges, runs verl, then closes the run behind the producers' close barrier, or at once on a
SIGTERM. Why: DESIGN.md."""

from __future__ import annotations

import contextlib
import functools
import importlib
import os
import runpy
import signal
import sys
import threading
from collections.abc import Callable, Iterator
from typing import Any

from probe.foundation.safe_warn import safe_warn as _diagnostics

from .. import _rl_owner
from .runs import (
    PROBE_BACKEND,
    add_to_job_config,
    build_runtime_env,
    get_resume_folder,
    get_external_id,
    get_names,
    get_rewind_step,
    get_run_config,
    get_run_name,
    make_backends,
    read_resume_step,
)

#: Where `run_ppo` lives; the fully async and one-step-off mains import it from here at call time.
RUN_PPO_MODULE = "verl.trainer.main_ppo"
#: The owner writes its terminal manifest as this producer, never standing in for `verl`'s lease.
OWNER_PRODUCER = "driver"
USAGE = ("usage: python -m probe.integrations.verl.launch [--] [python3] (-m <verl entry module> | <script.py>) "
         "[hydra overrides...]")
_PYTHON_NAMES = ("python", "python3")


class VerlLauncher:
    """Wraps `run_ppo` for one launch: the run it opened and how verl ended."""

    def __init__(self, **init_kwargs: Any) -> None:
        self.guard = _rl_owner.HookGuard("verl")
        self.has_run = False
        #: What `probe.init` gets besides the run's identity (a client, a project); empty from the command line.
        self.init_kwargs = init_kwargs

    def wrap(self, run_ppo: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(run_ppo)
        def probe_run_ppo(config: Any, *args: Any, **kwargs: Any) -> Any:
            self.has_run = True
            opened = self.guard.call("the run", self.open_run, config)
            run, is_owner = opened if opened else (None, False)
            if run is None:
                # No run, no hook in the workers: a `probe` logger would fail verl's own backend check.
                self.guard.call("trainer.logger", set_backends, config, has_probe=False)
                return run_ppo(config, *args, **kwargs)
            stop = SigtermClose(lambda: self.guard.call("the run's end", self.close_run, run, "failed", is_owner,
                                                        is_stopping=True))
            status = "failed"
            try:
                with stop.watch_ray_init():
                    result = run_ppo(config, *args, **kwargs)
                status = "completed"
                return result
            finally:
                stop.close_once(lambda: self.guard.call("the run's end", self.close_run, run, status, is_owner))
                stop.uninstall()

        return probe_run_ppo

    def open_run(self, config: Any) -> tuple[Any, bool] | None:
        """Open (or reopen with `Rewind(step=k+1)`) the run, hand it to Ray's workers through the job config, and
        put `probe` in `trainer.logger`. None when Ray is already up: its workers would never get the hook."""
        if _is_ray_initialized():
            _diagnostics.warn("probe.integrations.verl.launch: Ray is already initialized, so its workers never get "
                              "Probe's setup hook; this job runs without Probe (start Ray from verl to record it).")
            return None
        resume = read_resume_step(config)
        _project, experiment = get_names(config)
        run, is_owner = _rl_owner.open_run(
            name=get_run_name(experiment) if experiment else None,
            external_id=get_external_id(config, self.init_kwargs.get("name")),
            rewind_step=get_rewind_step(resume) if resume > 0 else None,
            config=get_run_config(config), init_kwargs=self.init_kwargs,
            resume_from=get_resume_folder(config, resume), should_stamp_checkpoints=True,
        )
        try:
            add_to_job_config(os.environ, build_runtime_env(run, os.environ))
        except Exception:
            self.close_run(run, "failed", is_owner)  # the workers could not get it: verl runs without Probe
            raise
        self.guard.call("trainer.logger", set_backends, config, has_probe=True)
        return run, is_owner

    def close_run(self, run: Any, status: str, is_owner: bool, *, is_stopping: bool = False) -> None:
        """The terminal manifest (the `verl` producer wrote its last step), the barrier, the run's own status. On a
        SIGTERM (``is_stopping``) the workers are going down too: no wait for their last seals, and the run is
        finished here even when joined (the SDK's own close at exit runs after Ray's: too late), unless `probe exec`
        closes it from the exit code; delivery is bounded by `PROBE_SIGTERM_FLUSH_SECONDS`."""
        samples = run.samples.as_producer(OWNER_PRODUCER)
        if not is_stopping:
            _rl_owner.close_run(run, samples, final_step=None, should_finish=is_owner, status=status)
            return
        from probe.sdk.run.launch import preempt
        from probe.sdk.run.launch.execute import EXEC_FINALIZES_ENV

        is_closed_by_exec = os.environ.get(EXEC_FINALIZES_ENV, "").strip() == str(run.id)
        _rl_owner.close_run(run, samples, final_step=None, should_finish=is_owner or not is_closed_by_exec,
                            status=status, wait_seconds=0, flush_timeout=preempt.budget_seconds())


class SigtermClose:
    """Closes the run when a SIGTERM lands while verl runs. `ray.init` (inside `run_ppo`) replaces the handler
    `probe.init` put in with its own `sys.exit` (`ray/_private/worker.py` `init`), and the run's close on the way out
    did not happen in time (the GPU smoke's run stayed `running`). So ours goes in front of Ray's right after
    `ray.init`: it closes the run, then calls Ray's. It never swallows the signal. Why: DESIGN.md "SIGTERM"."""

    def __init__(self, close_on_signal: Callable[[], Any]) -> None:
        self._close_on_signal = close_on_signal
        self._previous: Any = None
        self._is_closing = False
        self._is_closed = False
        self._is_signal_pending = False

    @contextlib.contextmanager
    def watch_ray_init(self) -> Iterator[None]:
        """While verl runs, a `ray.init` puts ours in front of the SIGTERM handler it set."""
        ray = sys.modules.get("ray")
        init = getattr(ray, "init", None)
        if not callable(init):
            yield
            return

        @functools.wraps(init)
        def probe_ray_init(*args: Any, **kwargs: Any) -> Any:
            result = init(*args, **kwargs)
            self.install()
            return result

        ray.init = probe_ray_init
        try:
            yield
        finally:
            if ray.init is probe_ray_init:
                ray.init = init

    def install(self) -> None:
        """In front of the current SIGTERM handler when it is a Python one (main thread only; never with
        `PROBE_SIGTERM_FLUSH_SECONDS=0`, which turns the SDK's SIGTERM close off)."""
        from probe.sdk.run.launch import preempt

        if self._is_closed or threading.current_thread() is not threading.main_thread():
            return
        current = signal.getsignal(signal.SIGTERM)
        if callable(current) and current != self.handle_sigterm and preempt.budget_seconds() > 0:
            self._previous = current
            signal.signal(signal.SIGTERM, self.handle_sigterm)

    def uninstall(self) -> None:
        """SIGTERM back to the handler ours stood in front of; a SIGTERM that waited for the close goes to it now."""
        if threading.current_thread() is not threading.main_thread():
            return
        if signal.getsignal(signal.SIGTERM) == self.handle_sigterm:
            signal.signal(signal.SIGTERM, self._previous)
            if self._is_signal_pending:
                self._is_signal_pending = False
                signal.raise_signal(signal.SIGTERM)

    def handle_sigterm(self, signum: int, frame: Any) -> None:
        if self._is_closing:
            self._is_signal_pending = True  # the close under way finishes first; the signal goes on after it
            return
        try:
            self.close_once(self._close_on_signal)
        finally:
            self._is_signal_pending = False
            self._previous(signum, frame)

    def close_once(self, close: Callable[[], Any]) -> None:
        """Run ``close`` unless a close already ran (the SIGTERM's, or the normal one at the end)."""
        if self._is_closing or self._is_closed:
            return
        self._is_closing = True
        try:
            close()
        finally:
            self._is_closing, self._is_closed = False, True


def set_backends(config: Any, *, has_probe: bool) -> None:
    """`trainer.logger` gains `probe` and loses W&B (one warning) when the run is open; loses `probe` when it is
    not, so verl never asserts on a backend its workers were never taught."""
    trainer = config.trainer
    current = trainer.get("logger") if hasattr(trainer, "get") else getattr(trainer, "logger", None)
    names = [current] if isinstance(current, str) else [str(name) for name in (current or ())]
    backends = make_backends(names) if has_probe else [name for name in names if name != PROBE_BACKEND]
    if names == backends:
        return
    dropped = sorted(set(names) - set(backends))
    if dropped:
        _diagnostics.warn(f"probe.integrations.verl.launch: trainer.logger drops {', '.join(dropped)}"
                          f"{'; Probe records this run' if has_probe else ''} (logger is now {backends}).")
    trainer.logger = backends


def main(argv: list[str] | None = None, **init_kwargs: Any) -> None:
    kind, target, args = parse_target(list(sys.argv[1:] if argv is None else argv))
    launcher = VerlLauncher(**init_kwargs)
    try:
        from .tracking import add_probe_backend

        add_probe_backend()
        main_ppo = importlib.import_module(RUN_PPO_MODULE)
    except ImportError as exc:
        print(f"probe: verl is not importable here, so Probe is not wired in: {exc}", file=sys.stderr)
        main_ppo = None
    original = getattr(main_ppo, "run_ppo", None)
    if main_ppo is not None and callable(original):
        main_ppo.run_ppo = launcher.wrap(original)
    try:
        run_target(kind, target, args)
    finally:
        if main_ppo is not None and callable(original):
            main_ppo.run_ppo = original
    if main_ppo is not None and not launcher.has_run:
        _diagnostics.warn("probe.integrations.verl.launch: the job never called verl's run_ppo, so Probe opened no "
                          "run and recorded nothing.")


def parse_target(argv: list[str]) -> tuple[str, str, list[str]]:
    """(`module` | `script`, its name, its arguments); an optional `--` and `python3` before it are dropped."""
    if argv[:1] == ["--"]:
        argv = argv[1:]
    if argv and os.path.basename(argv[0]).split(".")[0] in _PYTHON_NAMES and not argv[0].endswith(".py"):
        argv = argv[1:]
    if not argv or argv[0] in ("-h", "--help") or (argv[0] == "-m" and len(argv) < 2):
        print(USAGE, file=sys.stderr)
        raise SystemExit(2)
    if argv[0] == "-m":
        return "module", argv[1], argv[2:]
    return "script", argv[0], argv[1:]


def run_target(kind: str, target: str, args: list[str]) -> None:
    """Run verl's entry as `python -m` / `python script.py` would. `verl.trainer.main_ppo` itself is imported and its
    `main()` called instead, so the `run_ppo` it calls is the wrapped one (run as `__main__` it would define its own;
    its hydra config is a package, so hydra finds it either way). The other mains import `run_ppo` from it at call
    time (`fully_async_main.py:224`, `one_step_off_policy/main_ppo.py:100`), and their configs are folders hydra
    finds only from a `__main__` file."""
    if kind == "module" and target == RUN_PPO_MODULE:
        module = importlib.import_module(target)
        sys.argv = [getattr(module, "__file__", None) or target, *args]
        module.main()
        return
    if kind == "module":
        sys.argv = [target, *args]
        runpy.run_module(target, run_name="__main__", alter_sys=True)
        return
    script = os.path.abspath(target)
    sys.argv = [script, *args]
    sys.path[0] = os.path.dirname(script)
    runpy.run_path(script, run_name="__main__")


def _is_ray_initialized() -> bool:
    ray = sys.modules.get("ray")
    try:
        return bool(ray is not None and ray.is_initialized())
    except Exception:  # noqa: BLE001 -- an odd Ray: assume not
        return False


if __name__ == "__main__":
    main()
