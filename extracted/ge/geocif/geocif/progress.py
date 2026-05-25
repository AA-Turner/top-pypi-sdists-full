"""Progress-bar helpers that stay readable under multiprocessing.

`pbar` is a drop-in for `tqdm.rich.tqdm` that turns into a no-op iterator
inside worker processes. The main process keeps its outer bar; workers
suppress their nested bars and emit single-line status lines instead.

Use `pbar(...)` where you'd write `tqdm(...)` inside worker-reachable
code. Keep raw `tqdm(...)` only at the parent-process orchestrator level
(geocif_runner.execute_models, indices_runner CID loop).
"""

import sys
import time

# TqdmExperimentalWarning is silenced once in geocif/__init__.py so the filter
# is active before any of the 17 submodules that import from tqdm.rich.

_IN_WORKER = False
_TOTAL = None


def set_worker_mode(enabled=True, total=None):
    """Mark the current process as a multiprocessing worker.

    Called once per worker via `mp.Pool(initializer=set_worker_mode,
    initargs=(True, len(inputs)))`. Module-level globals so `pbar` and
    `status` can read the flag without plumbing it through every call.
    """
    global _IN_WORKER, _TOTAL
    _IN_WORKER = bool(enabled)
    if total is not None:
        _TOTAL = int(total)


def in_worker():
    return _IN_WORKER


class _NoopBar:
    """Passthrough iterator that quacks like tqdm but renders nothing."""

    def __init__(self, iterable=None):
        self._iterable = iterable

    def __iter__(self):
        if self._iterable is None:
            return iter([])
        return iter(self._iterable)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def update(self, n=1):
        pass

    def set_description(self, *args, **kwargs):
        pass

    def set_description_str(self, *args, **kwargs):
        pass

    def set_postfix(self, *args, **kwargs):
        pass

    def set_postfix_str(self, *args, **kwargs):
        pass

    def refresh(self):
        pass

    def close(self):
        pass

    def reset(self, total=None):
        pass

    def write(self, msg, **kwargs):
        pwrite(msg)


def pbar(iterable=None, **kwargs):
    """`tqdm.rich.tqdm` wrapper that disables itself inside workers.

    tqdm.rich.tqdm.__init__ calls warn("rich is experimental/alpha",
    TqdmExperimentalWarning, stacklevel=2) on EVERY instantiation, not
    just at module import. The package-level filter in geocif/__init__.py
    catches first hit, but downstream libraries (pandas/scipy) often call
    warnings.simplefilter(...) which resets the filter table — after
    that, the warning starts firing again on every pbar() call. Wrap
    each instantiation in catch_warnings so the suppression survives
    regardless of what other libraries do to warnings.filters.
    """
    if _IN_WORKER:
        return _NoopBar(iterable)
    import warnings as _w
    from tqdm.rich import tqdm as rich_tqdm
    with _w.catch_warnings():
        try:
            from tqdm import TqdmExperimentalWarning as _TEW
            _w.simplefilter("ignore", _TEW)
        except ImportError:
            _w.simplefilter("ignore")
        return rich_tqdm(iterable, **kwargs)


def pwrite(msg):
    """Write a status line without tearing the active progress bar.

    Parent: uses `tqdm.write` so the live bar is cleared and redrawn.
    Worker: plain stderr write (no live bar in this process; the parent's
    bar will redraw on its next refresh).
    """
    if _IN_WORKER:
        print(msg, file=sys.stderr, flush=True)
        return
    try:
        from tqdm import tqdm as std_tqdm

        std_tqdm.write(msg, file=sys.stderr)
    except Exception:
        print(msg, file=sys.stderr, flush=True)


def _fmt_elapsed(seconds):
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def status(idx, msg, elapsed=None):
    """Emit `[i/total] msg` (and optional ` in M:SS`) as a single line."""
    n = _TOTAL if _TOTAL is not None else "?"
    line = f"[{idx + 1}/{n}] {msg}"
    if elapsed is not None:
        line += f" in {_fmt_elapsed(elapsed)}"
    pwrite(line)


class StatusTimer:
    """Context manager that emits start/done (or failed) status lines."""

    def __init__(self, idx, label):
        self.idx = idx
        self.label = label
        self.t0 = None

    def __enter__(self):
        self.t0 = time.time()
        status(self.idx, f"{self.label} start")
        return self

    def __exit__(self, exc_type, exc, tb):
        elapsed = time.time() - self.t0
        if exc_type is None:
            status(self.idx, f"{self.label} done", elapsed=elapsed)
        else:
            err = f"{exc_type.__name__}: {exc}"
            short = err if len(err) < 200 else err[:200] + "..."
            status(self.idx, f"{self.label} FAILED ({short})", elapsed=elapsed)
        return False
