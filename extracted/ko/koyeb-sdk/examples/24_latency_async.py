"""Koyeb latency benchmark (async): exec, health check, and HTTP round-trip.

Measures:
  1. is_healthy() latency
  2. get_from_id() + exec('true') latency (new instance each time)
  3. get_from_id() once + exec('true') latency (cached instance)
  4. HTTP POST round-trip (new TLS conn each)
  5. HTTP POST round-trip (cached session)

Usage:
    KOYEB_API_TOKEN=<token> uv run python examples/24_latency_async.py
    KOYEB_API_TOKEN=<token> uv run python examples/24_latency_async.py --debug
"""

import argparse
import asyncio
import logging
import os
import statistics
import time

import httpx

from koyeb import AsyncSandbox

TOKEN = os.environ["KOYEB_API_TOKEN"]
IMAGE = "koyeb/sandbox"
N = 10

SERVER_SCRIPT = """\
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        subprocess.run(["true"], check=True)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"received": len(body)}).encode())

    def log_message(self, format, *args):
        pass

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
"""


def print_stats(times: list[float], unit: str = "ms") -> None:
    scale = 1000 if unit == "ms" else 1
    print(f"\n  median={statistics.median(times)*scale:.1f}{unit}  "
          f"min={min(times)*scale:.1f}{unit}  max={max(times)*scale:.1f}{unit}\n")


async def bench_health(sandbox: AsyncSandbox) -> None:
    print(f"--- is_healthy() x{N} ---")
    times: list[float] = []
    for i in range(N):
        t0 = time.perf_counter()
        healthy = await sandbox.is_healthy()
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        print(f"  [{i+1:2d}] {elapsed*1000:7.1f}ms  healthy={healthy}")
    print_stats(times)


async def bench_exec(sandbox: AsyncSandbox, sandbox_id: str) -> None:
    print(f"--- get_from_id() + exec('true') x{N} ---")
    times: list[float] = []
    for i in range(N):
        t0 = time.perf_counter()
        sb = await AsyncSandbox.get_from_id(id=sandbox_id, api_token=TOKEN)
        t1 = time.perf_counter()
        await sb.exec("true")
        t2 = time.perf_counter()
        times.append(t2 - t0)
        print(f"  [{i+1:2d}] get={t1-t0:.3f}s  exec={t2-t1:.3f}s  total={t2-t0:.3f}s")
    print_stats(times, unit="s")


async def bench_exec_cached(sandbox: AsyncSandbox, sandbox_id: str) -> None:
    print(f"--- get_from_id() once + exec('true') x{N} ---")
    sb = await AsyncSandbox.get_from_id(id=sandbox_id, api_token=TOKEN)
    times: list[float] = []
    for i in range(N):
        t0 = time.perf_counter()
        await sb.exec("true")
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        print(f"  [{i+1:2d}] {elapsed*1000:7.1f}ms")
    print_stats(times)


async def bench_http_post(sandbox: AsyncSandbox) -> None:
    await sandbox.filesystem.write_file("/tmp/server.py", SERVER_SCRIPT)
    print("  Starting HTTP server on :8080...")
    await sandbox.launch_process("python3 /tmp/server.py")
    await asyncio.sleep(2)

    print("  Exposing port 8080...")
    exposed = await sandbox.expose_port(8080)
    base_url = exposed.exposed_at
    print(f"  URL: {base_url}")
    await asyncio.sleep(2)

    payload = b'{"ping": true}'

    # Warm-up
    resp = httpx.post(f"{base_url}/echo", content=payload,
                    headers={"Content-Type": "application/json"}, timeout=10)
    print(f"  Warm-up: {resp.status_code}\n")

    # New TLS connection each request
    print(f"--- HTTP POST x{N} (new TLS conn each) ---")
    times: list[float] = []
    for i in range(N):
        t0 = time.perf_counter()
        resp = httpx.post(
            f"{base_url}/echo",
            content=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        print(f"  [{i+1:2d}] {elapsed*1000:7.1f}ms  status={resp.status_code}  body={len(resp.content)}B")
    print_stats(times)

    # Cached session (connection reuse)
    print(f"--- HTTP POST x{N} (cached session) ---")
    client = httpx.Client()
    # Warm-up the client
    client.post(f"{base_url}/echo", content=payload,
                headers={"Content-Type": "application/json"}, timeout=10)
    times = []
    for i in range(N):
        t0 = time.perf_counter()
        resp = client.post(
            f"{base_url}/echo",
            content=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        t1 = time.perf_counter()
        elapsed = t1 - t0
        times.append(elapsed)
        print(f"  [{i+1:2d}] {elapsed*1000:7.1f}ms  status={resp.status_code}  body={len(resp.content)}B")
    print_stats(times)

    client.close()
    await sandbox.unexpose_port()


async def main(debug: bool = False) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(name)s %(levelname)s: %(message)s")
        logging.getLogger("koyeb").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)

    print(f"Creating sandbox (image={IMAGE})...")
    sandbox = await AsyncSandbox.create(
        image=IMAGE,
        name="exec-latency-repro",
        wait_ready=True,
        api_token=TOKEN,
        instance_type="medium",
        delete_after_delay=300,
        _experimental_enable_light_sleep=False,
    )
    sandbox_id = sandbox.id
    print(f"Ready: {sandbox_id}\n")

    try:
        await bench_health(sandbox)
        await bench_exec(sandbox, sandbox_id)
        await bench_exec_cached(sandbox, sandbox_id)
        await bench_http_post(sandbox)
    finally:
        await sandbox.delete()
        print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Koyeb latency benchmark (async)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()
    asyncio.run(main(debug=args.debug))
