import os
import sys
import threading
import time

from statsig_python_core import Statsig, StatsigOptions


callback_entered = threading.Event()
callback_release = threading.Event()
callback_finished = threading.Event()
callback_lock = threading.Lock()


def on_runtime_thread_start() -> None:
    # Keep one Rust runtime worker inside Python while another worker completes
    # initialization. The pre-fork reset must release the GIL so this callback
    # can finish before the runtime is dropped.
    if not callback_lock.acquire(blocking=False):
        return

    try:
        callback_entered.set()
        callback_release.wait(timeout=30)
        callback_finished.set()
    finally:
        callback_lock.release()


def create_statsig(with_callback: bool) -> Statsig:
    options = StatsigOptions(
        disable_all_logging=True,
        disable_network=True,
        output_log_level="none",
        sdk_runtime_thread_count=2,
        runtime_thread_start_callback=on_runtime_thread_start if with_callback else None,
    )
    return Statsig("secret-forking-test", options)


def main() -> None:
    statsig = create_statsig(with_callback=True)
    try:
        assert callback_entered.wait(timeout=5)
        assert statsig.initialize().wait(timeout=5)

        # This is the documented lifecycle for a process that needs to fork.
        # shutdown() drains SDK work but leaves the shared runtime alive.
        assert statsig.shutdown().wait(timeout=5)

        fork_started = threading.Event()

        def release_callback() -> None:
            assert fork_started.wait(timeout=5)
            # Give the main thread time to enter the pre-fork hook. With the
            # old implementation it holds the GIL here, so this thread cannot
            # release the callback and the subprocess watchdog fires.
            time.sleep(0.05)
            callback_release.set()

        releaser = threading.Thread(target=release_callback)
        releaser.start()

        previous_switch_interval = sys.getswitchinterval()
        sys.setswitchinterval(1.0)
        try:
            fork_started.set()
            child_pid = os.fork()
        finally:
            sys.setswitchinterval(previous_switch_interval)

        if child_pid == 0:
            child_statsig = create_statsig(with_callback=False)
            assert child_statsig.initialize().wait(timeout=5)
            assert child_statsig.shutdown().wait(timeout=5)
            os._exit(0)

        releaser.join(timeout=5)
        assert not releaser.is_alive()
        _, child_status = os.waitpid(child_pid, 0)
        assert os.waitstatus_to_exitcode(child_status) == 0

        assert callback_finished.wait(timeout=5)

        replacement = create_statsig(with_callback=False)
        assert replacement.initialize().wait(timeout=5)
        assert replacement.shutdown().wait(timeout=5)
    finally:
        callback_release.set()


if __name__ == "__main__":
    main()
