#!/usr/bin/env python3
"""
debug_minimax_m3.py — diagnostic harness for the "M3 doesn't work on Windows" bug.

This script bypasses ALL of CVC's code path and hits MiniMax directly with raw
httpx, three separate ways. Whichever one fails first tells you exactly which
layer is broken on your machine.

Usage (on the Windows PC where M3 is failing):
    python scripts/debug_minimax_m3.py

If it hangs, press Ctrl-C and report the last line printed.

The script is read-only — it does not modify any files, only talks to:
    https://api.minimax.io/anthropic/v1/messages
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import platform
import traceback

import httpx


MINIMAX_INTL = "https://api.minimax.io/anthropic/v1/messages"
MINIMAX_CN = "https://api.minimaxi.com/anthropic/v1/messages"
DEFAULT_MODEL = "MiniMax-M3"

TEST_BODY = {
    "model": DEFAULT_MODEL,
    "max_tokens": 64,
    "messages": [
        {"role": "user", "content": "Respond with exactly one short sentence saying hello."}
    ],
}


def env_or_die() -> str:
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        print(
            "ERROR: MINIMAX_API_KEY environment variable is not set.\n"
            "Set it in PowerShell with:  $env:MINIMAX_API_KEY = \"...\"\n"
            "Or in cmd with:             set MINIMAX_API_KEY=...\n"
        )
        sys.exit(2)
    return api_key


def banner(label: str) -> None:
    print("\n" + "=" * 60)
    print(label)
    print("=" * 60)


def env_report() -> None:
    banner("ENVIRONMENT")
    print(f"  python        : {sys.version.split()[0]}")
    print(f"  platform      : {platform.platform()}")
    print(f"  httpx         : {httpx.__version__}")
    try:
        import h2  # type: ignore
        print(f"  h2 (HTTP/2)   : INSTALLED ({h2.__version__})")
    except ImportError:
        print("  h2 (HTTP/2)   : NOT INSTALLED — http2 disabled at runtime")
    print(f"  MINIMAX key   : {'present' if os.environ.get('MINIMAX_API_KEY') else 'MISSING'}")
    print(f"  CURL_CA_BUNDLE: {os.environ.get('CURL_CA_BUNDLE') or '(unset)'}")


async def ping(url: str, body: dict, api_key: str, *, http2: bool, label: str) -> tuple[float, str, str]:
    """Returns (elapsed_seconds, status_or_error, body_or_truncated_text)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "anthropic-beta": "interleaved-thinking-2025-05-14",
        "content-type": "application/json",
    }
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(
            base_url=url.rsplit("/v1/messages", 1)[0],
            headers=headers,
            timeout=httpx.Timeout(connect=15.0, read=60.0, write=30.0, pool=10.0),
            http2=http2,
        ) as client:
            r = await client.post("/v1/messages", json=body)
        elapsed = time.perf_counter() - start
        text = r.text
        if len(text) > 600:
            text = text[:600] + "... [truncated]"
        return elapsed, f"HTTP {r.status_code}", text
    except httpx.ConnectError as e:
        elapsed = time.perf_counter() - start
        return elapsed, "ConnectError", repr(e)
    except httpx.ConnectTimeout as e:
        elapsed = time.perf_counter() - start
        return elapsed, "ConnectTimeout", repr(e)
    except httpx.ReadTimeout as e:
        elapsed = time.perf_counter() - start
        return elapsed, "ReadTimeout", repr(e)
    except httpx.RemoteProtocolError as e:
        elapsed = time.perf_counter() - start
        return elapsed, "RemoteProtocolError", repr(e)
    except Exception as e:  # noqa: BLE001
        elapsed = time.perf_counter() - start
        return elapsed, type(e).__name__, repr(e)


async def tool_call_ping(url: str, api_key: str, *, http2: bool) -> tuple[float, str, str]:
    """Same as ping() but with a tiny tool definition — proves M3 tools work."""
    body = {
        "model": DEFAULT_MODEL,
        "max_tokens": 256,
        "tools": [
            {
                "name": "echo",
                "description": "Echo a string back to the user.",
                "input_schema": {
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"],
                },
            }
        ],
        "messages": [
            {"role": "user", "content": "Use the echo tool to say 'm3-tools-ok'."}
        ],
    }
    return await ping(url, body, api_key, http2=http2, label="TOOLCALL")


async def streaming_ping(url: str, api_key: str, *, http2: bool) -> tuple[float, str, str]:
    """Stream a response. If the stream stalls before any byte, that's the bug."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "anthropic-beta": "interleaved-thinking-2025-05-14",
        "content-type": "application/json",
    }
    body = {"model": DEFAULT_MODEL, "max_tokens": 32, "messages": [
        {"role": "user", "content": "Say one word: ping."}
    ], "stream": True}
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(
            base_url=url.rsplit("/v1/messages", 1)[0],
            headers=headers,
            timeout=httpx.Timeout(connect=15.0, read=60.0, write=30.0, pool=10.0),
            http2=http2,
        ) as client:
            async with client.stream("POST", "/v1/messages", json=body) as r:
                first_byte = None
                async for line in r.aiter_lines():
                    if line.startswith("data: "):
                        first_byte = time.perf_counter() - start
                        return first_byte, f"HTTP {r.status_code}", line[:200]
        elapsed = time.perf_counter() - start
        return elapsed, "EmptyStream", "no first SSE line arrived"
    except httpx.ConnectError as e:
        elapsed = time.perf_counter() - start
        return elapsed, "ConnectError", repr(e)
    except Exception as e:  # noqa: BLE001
        elapsed = time.perf_counter() - start
        return elapsed, type(e).__name__, repr(e)


async def main() -> int:
    env_report()
    api_key = env_or_die()

    banner("TEST 1 — non-streaming (HTTP/1.1)")
    elapsed, status, body = await ping(MINIMAX_INTL, TEST_BODY, api_key, http2=False, label="NON-STREAM HTTP1")
    print(f"  status  : {status}   ({elapsed:.2f}s)")
    print(f"  body    : {body[:500]}")

    banner("TEST 2 — non-streaming (HTTP/2 if installed)")
    elapsed, status, body = await ping(MINIMAX_INTL, TEST_BODY, api_key, http2=True, label="NON-STREAM HTTP2")
    print(f"  status  : {status}   ({elapsed:.2f}s)")
    print(f"  body    : {body[:500]}")

    banner("TEST 3 — tool-call (the path that breaks on agent prompt)")
    elapsed, status, body = await tool_call_ping(MINIMAX_INTL, api_key, http2=True)
    print(f"  status  : {status}   ({elapsed:.2f}s)")
    print(f"  body    : {body[:500]}")

    banner("TEST 4 — streaming first-byte (the path that breaks in chat_stream)")
    elapsed, status, body = await streaming_ping(MINIMAX_INTL, api_key, http2=True)
    print(f"  status  : {status}   ({elapsed:.2f}s for first SSE line)")
    print(f"  body    : {body[:200]}")

    banner("TEST 5 — China endpoint (only if INTL failed)")
    print("  Re-running Test 1 against api.minimaxi.com ...")
    elapsed, status, body = await ping(MINIMAX_CN, TEST_BODY, api_key, http2=False, label="NON-STREAM HTTP1 CN")
    print(f"  status  : {status}   ({elapsed:.2f}s)")
    print(f"  body    : {body[:500]}")

    banner("INTERPRETATION")
    print("""
Read the table below to know what failed and where:

  TEST 1 fail (ConnectError / ReadTimeout)  -> TLS, DNS, or proxy is broken.
                                              Check antivirus, corporate firewall,
                                              and the Windows cert store. Try
                                              `curl https://api.minimax.io` from
                                              PowerShell to confirm.

  TEST 1 ok, TEST 2 fail                      -> HTTP/2 is the problem. Run
                                              `pip install httpx[http2]` in your
                                              venv. CVC auto-detects h2; without
                                              it, you fall back to HTTP/1.1 which
                                              is what just worked in TEST 1, so
                                              this is unlikely.

  TEST 1 ok, TEST 3 fail                      -> Tool-call format mismatch. The
                                              Anthropic-Messages wire MiniMax
                                              promises may differ for tools.
                                              Run with --verbose and report the
                                              status code + body.

  TEST 1 ok, TEST 4 fail                      -> Streaming broken on your machine.
                                              This is the MOST COMMON Windows
                                              failure. The fix in CVC 3.5.8 is
                                              exactly this — transparent retry
                                              on connect-time and stream-start
                                              stalls for anthropic-compat providers.

  TEST 5 ok, TEST 1 fail                      -> You're on the China endpoint and
                                              need MINIMAX_BASE_URL. Set it:
                                                $env:MINIMAX_BASE_URL = "https://api.minimaxi.com/anthropic"

No failures at all                              -> Your network + MiniMax are fine.
                                              The CVC agent is the bug. Run
                                              `cvc setup` and re-test, or
                                              pull the 3.5.8 fix.
""")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n[HARNESS: cancelled by Ctrl-C]")
        sys.exit(130)
    except Exception as e:  # noqa: BLE001
        print(f"\nUNEXPECTED HARNESS ERROR: {e!r}")
        traceback.print_exc()
        sys.exit(1)
