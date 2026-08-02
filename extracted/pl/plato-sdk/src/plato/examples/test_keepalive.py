"""Verify keepalive=True keeps an env alive without client-side heartbeats.

Launches an espocrm env with keepalive=True and timeout=1800s (30 min), then
sits idle — sending NO heartbeats — and polls job status periodically to confirm
the env stays in `running` state. With the recent SDK change, the heartbeat task
is not started when keepalive=True, so this script exercises the server-side
keepalive path directly.

Run:
    cd python && uv run python -m plato.examples.test_keepalive
"""

import argparse
import asyncio
import time

from dotenv import load_dotenv

from plato.sdk import Plato

load_dotenv(".env")

ENV_ID = "espocrm"
TIMEOUT_SECONDS = 1800  # 30 min — also the server-side env timeout
POLL_INTERVAL = 60  # seconds between status polls
WATCH_DURATION = 1500  # how long to keep watching after ready (stop before server timeout)


async def main(base_url: str | None) -> None:
    client = Plato(base_url=base_url) if base_url else Plato()

    print(f"Creating {ENV_ID} env (keepalive=True, timeout={TIMEOUT_SECONDS}s)")
    env = await client.make_environment(
        ENV_ID,
        keepalive=True,
        timeout=TIMEOUT_SECONDS,
    )
    print(f"job_id={env.id}")

    try:
        print("Waiting for environment to be ready...")
        ready_start = time.time()
        await env.wait_for_ready(timeout=300.0)
        print(f"Ready in {time.time() - ready_start:.1f}s")

        # Confirm the SDK change took effect: no heartbeat task should exist.
        assert env._heartbeat_task is None, (
            f"expected no heartbeat task when keepalive=True, got {env._heartbeat_task!r}"
        )
        print("Confirmed: no client-side heartbeat task started (keepalive path).")

        watch_start = time.time()
        last_poll = 0.0
        while True:
            elapsed = time.time() - watch_start
            if elapsed >= WATCH_DURATION:
                print(f"Reached watch duration {WATCH_DURATION}s — env stayed alive without heartbeats.")
                break

            if time.time() - last_poll >= POLL_INTERVAL:
                last_poll = time.time()
                try:
                    status = await client.get_job_status(env.id)
                    state = status.get("status", "<unknown>")
                    print(f"[t+{elapsed:6.0f}s] status={state}")
                    if str(state).lower() != "running":
                        print(f"Env exited running state at t+{elapsed:.0f}s. Full status: {status}")
                        break
                except Exception as e:
                    print(f"[t+{elapsed:6.0f}s] status poll failed: {e!r}")

            await asyncio.sleep(5)

    finally:
        print("Closing env...")
        try:
            await env.close()
            print("Env closed.")
        except Exception as e:
            print(f"close() raised: {e!r}")
        await client.close()
        print("Client closed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default=None,
        help="Plato API base URL (e.g. https://staging.plato.so/api). Defaults to config.",
    )
    args = parser.parse_args()
    asyncio.run(main(args.base_url))
