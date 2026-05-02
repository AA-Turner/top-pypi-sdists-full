import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from threading import Event
from typing import List, Union

_RELOAD_SENTINEL = "/tmp/.cpsl_reload"
_POLL_INTERVAL = 0.5
_ARM_DELAY = 5.0


class ServeGateway:
    def __init__(self) -> None:
        self.process: Union[subprocess.Popen, None] = None
        self.exit_code: int = 0
        self.restart_event = Event()
        self.exit_event = Event()
        self._armed = Event()

        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, signum=None, frame=None) -> None:
        self.kill_subprocess()
        self.exit_event.set()
        self.restart_event.set()

    def kill_subprocess(self) -> None:
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                self.process.wait()
            except BaseException:
                pass

        self.process = None
        self.restart_event.set()

    def _sentinel_watcher(self) -> None:
        """Poll for the reload sentinel written by the gateway after a file sync."""
        self._armed.wait()

        # Clear any sentinels that arrived during the arm delay (initial sync).
        try:
            os.remove(_RELOAD_SENTINEL)
        except FileNotFoundError:
            pass

        while not self.exit_event.is_set():
            try:
                with open(_RELOAD_SENTINEL, "r") as f:
                    changed = f.read().strip()
                os.remove(_RELOAD_SENTINEL)
                if changed:
                    print(f"[cpsl.serve] synced {changed}, restarting", flush=True)
                self.restart_event.set()
            except FileNotFoundError:
                pass
            except Exception as exc:
                print(f"[cpsl.serve] sentinel watch error: {exc}", flush=True)
            time.sleep(_POLL_INTERVAL)

    def run(self, *, command: List[str]) -> None:
        watcher = threading.Thread(target=self._sentinel_watcher, daemon=True)
        watcher.start()

        first = True
        while not self.exit_event.is_set():
            if self.process:
                self.kill_subprocess()

            self.process = subprocess.Popen(
                command,
                preexec_fn=os.setsid,
                env=os.environ.copy(),
                stdout=sys.stdout,
                stderr=sys.stdout,
            )

            if first:
                threading.Timer(_ARM_DELAY, self._armed.set).start()
                first = False

            self.restart_event.clear()
            self.restart_event.wait()


if __name__ == "__main__":
    if len(sys.argv) != 2 or ":" not in sys.argv[1]:
        print("Usage: python -m cpsl.serve <module>:<Class>", file=sys.stderr)
        sys.exit(1)

    entry_point = sys.argv[1]
    sg = ServeGateway()

    try:
        sg.run(command=[sys.executable, "-m", "cpsl.runner", entry_point])
    except BaseException:
        print(f"Error occurred: {traceback.format_exc()}")
        sg.exit_code = 1

    if sg.exit_code != 0:
        sys.exit(sg.exit_code)
