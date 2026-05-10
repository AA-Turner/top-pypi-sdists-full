"""Live RAG re-indexing on file changes.

Keeps the RAG index in sync with the project as the user edits. Two paths:

  - **Polling fallback** (always available): periodically scans for files
    whose mtime is newer than the last indexed timestamp.
  - **watchdog backend** (preferred when installed): event-driven,
    near-zero latency, uses native fsevents/inotify.

Run:
    python -m sage.core.rag_watcher              # blocking, polls every 5s
    python -m sage.core.rag_watcher --interval 1 # watchdog or 1s poll
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from pathlib import Path

__all__ = ["watch_and_reindex", "main"]


def _have_watchdog() -> bool:
    return importlib.util.find_spec("watchdog") is not None


def _watch_with_watchdog(cwd: Path, *, on_change) -> None:
    """Block; call on_change when any indexable file changes."""
    from watchdog.events import FileSystemEventHandler  # type: ignore
    from watchdog.observers import Observer            # type: ignore

    class Handler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            on_change(event.src_path)

    observer = Observer()
    observer.schedule(Handler(), str(cwd), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()


def _watch_with_polling(cwd: Path, *, interval: float, on_change) -> None:
    """Polling fallback. Tracks max(mtime) per scan."""
    from sage.core.rag import _walk_indexable
    last_max = 0.0
    try:
        while True:
            cur_max = last_max
            changed: list[str] = []
            for path in _walk_indexable(cwd):
                try:
                    m = path.stat().st_mtime
                except OSError:
                    continue
                if m > last_max:
                    changed.append(str(path))
                    if m > cur_max:
                        cur_max = m
            if changed:
                on_change(changed[0] if len(changed) == 1 else f"{len(changed)} files")
                last_max = cur_max
            else:
                last_max = max(last_max, cur_max)
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


def watch_and_reindex(cwd: Path, *, interval: float = 5.0, force_polling: bool = False,
                      reindex_fn=None) -> None:
    """Watch cwd; re-index on change.

    Args:
        cwd: directory to watch
        interval: polling interval (seconds) when watchdog isn't available
        force_polling: skip watchdog even if installed (useful in tests/docker)
        reindex_fn: callable invoked with (changed_path: str) on each event;
                    defaults to RAGIndex.reindex(cwd)
    """
    if reindex_fn is None:
        from sage.core.rag import RAGIndex
        index = RAGIndex(cwd)
        last_run = [0.0]

        def _default(_path):
            # Debounce — at most one reindex per interval
            now = time.time()
            if now - last_run[0] < interval:
                return
            last_run[0] = now
            stats = index.reindex()
            print(f"[rag-watcher] reindex: chunks_added={stats['chunks_added']}")
        reindex_fn = _default

    if not force_polling and _have_watchdog():
        print(f"[rag-watcher] watchdog active; watching {cwd}")
        _watch_with_watchdog(cwd, on_change=reindex_fn)
    else:
        print(f"[rag-watcher] polling every {interval}s; watching {cwd}")
        _watch_with_polling(cwd, interval=interval, on_change=reindex_fn)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cwd", type=Path, default=Path.cwd())
    p.add_argument("--interval", type=float, default=5.0)
    p.add_argument("--force-polling", action="store_true")
    args = p.parse_args(argv)
    watch_and_reindex(args.cwd, interval=args.interval, force_polling=args.force_polling)
    return 0


if __name__ == "__main__":
    sys.exit(main())
