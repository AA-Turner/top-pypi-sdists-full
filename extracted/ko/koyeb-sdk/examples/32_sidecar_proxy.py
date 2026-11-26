#!/usr/bin/env python3
"""Sidecar proxy: inject a credential without the sandbox holding it

A mitmproxy sidecar runs next to the sandbox, on a private mesh. The sandbox
sends its HTTPS traffic through the proxy (HTTPS_PROXY=http://proxy:8080).
The proxy adds an Authorization header for one destination only, from a
token that lives in the sidecar's environment: code in the sandbox never
sees it.

The proxy decides on the real destination (host, port, HTTPS), never on the
Host header, which the sandbox controls. https://httpbin.org/bearer accepts
any bearer token and replies only whether one was sent, so the token doesn't
come back to the sandbox. Real upstreams can echo headers: inject only into
destinations you trust.

The sandbox fetches the proxy's public CA certificate through the proxy
(mitmproxy serves it at http://mitm.it) and trusts it; the CA's private key
stays in the sidecar.

The sandbox keeps normal egress: the proxy is opt-in for code in the sandbox.
"""

import os
import random
import string
import sys
import textwrap

from koyeb import Sandbox, Sidecar

INJECT_HOST = "httpbin.org"

# mitmproxy addon, mounted in the sidecar. Injects the token for one
# destination only: a proxy that adds credentials to every request would
# hand them to any host the sandbox chooses. It checks the connection's real
# destination, not pretty_host, which comes from the client's Host header,
# and rejects requests whose Host header disagrees with it.
ADDON = textwrap.dedent(
    f"""\
    import os

    TOKEN = os.environ["DEMO_TOKEN"]

    def request(flow):
        req = flow.request
        if (
            req.scheme == "https"
            and req.host == "{INJECT_HOST}"
            and req.port == 443
            and req.host_header in (None, "{INJECT_HOST}")
        ):
            req.headers["Authorization"] = f"Bearer {{TOKEN}}"
        else:
            req.headers.pop("Authorization", None)
    """
)

PROXY = "http://proxy:8080"
TRUST_PROXY_CA = (
    f"curl -sf -x {PROXY} http://mitm.it/cert/pem "
    "-o /usr/local/share/ca-certificates/sidecar-proxy.crt "
    "&& update-ca-certificates >/dev/null"
)
# 200 only if the proxy injected a bearer token; the token isn't echoed.
REQUEST = f"curl -s -m 20 -o /dev/null -w '%{{http_code}}' https://{INJECT_HOST}/bearer"
# Spoofing the Host header must not get a token. httpbin.org/headers echoes
# what it received, so the check can see whether a token was added: once over
# plain HTTP with a forged Host, once over HTTPS with a mismatched Host.
SPOOFED = (
    f"curl -s -m 20 -H 'Host: {INJECT_HOST}' http://{INJECT_HOST}/headers; "
    f"curl -s -m 20 -H 'Host: attacker.example' https://{INJECT_HOST}/headers"
)


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    # In production, pass Secret(name="my-api-key") so the platform injects a
    # stored secret at deploy time.
    token = "demo-" + "".join(random.choices(string.ascii_lowercase, k=12))
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))

    proxy = Sidecar(
        name="proxy",
        image="mitmproxy/mitmproxy:latest",
        ports=[8080],
        command="mitmdump",
        args=["--listen-port", "8080", "-s", "/etc/sidecar/inject.py"],
        config_files={"/etc/sidecar/inject.py": ADDON},
        env={"DEMO_TOKEN": token},
    )

    sandbox = None
    try:
        print("Creating a sandbox with a proxy sidecar...")
        sandbox = Sandbox.create(
            image="koyeb/sandbox",
            name=f"sidecar-proxy-{suffix}",
            wait_ready=True,
            api_token=api_token,
            env={"HTTPS_PROXY": PROXY, "NO_PROXY": "localhost,127.0.0.1"},
            sidecars=[proxy],
            timeout=600,
        )
        print(f"Sidecar reachable from the sandbox at {sandbox.sidecar('proxy').url()}")

        result = sandbox.exec(TRUST_PROXY_CA)
        if not result.success:
            print(f"Could not trust the proxy CA: {result.stderr}")
            return 1
        print("Sandbox trusts the proxy's CA")

        result = sandbox.exec(REQUEST)
        if result.stdout.strip() != "200":
            print(f"The proxy did not inject the token (HTTP {result.stdout.strip()})")
            return 1
        print(f"{INJECT_HOST} accepted the token the proxy injected")

        result = sandbox.exec(SPOOFED)
        if token in result.stdout or "Bearer" in result.stdout:
            print("The proxy injected the token for a spoofed Host header")
            return 1
        print("No token for a spoofed Host header")

        result = sandbox.exec(f"env | grep -c {token} || true")
        if result.stdout.strip() != "0":
            print("The token is visible in the sandbox")
            return 1
        print("The token is not in the sandbox's environment")
        return 0
    finally:
        if sandbox:
            sandbox.delete()
            print("Deleted the sandbox and its sidecar")


if __name__ == "__main__":
    sys.exit(main())
