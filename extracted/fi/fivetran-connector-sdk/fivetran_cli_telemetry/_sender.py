"""
Detached telemetry sender, run as a child process by Telemetry._spawn_detached_sender.

Reads the webhook URL (first line) and JSON payload (the rest) from stdin and POSTs the
payload. Kept dependency-free (stdlib urllib only) so the child needn't import the SDK or
`requests` — it must survive the parent CLI process exiting.

The parent delivers this module to the child as `python -I -c <source of this file>`, not as
`python -m fivetran_cli_telemetry._sender`: `-I` implies `-s` and `-P`, which strip the user
site-packages and the cwd from sys.path, so `-m` would fail to import the package under
`pip install --user` or a source checkout and silently drop telemetry. Passing the source
inline needs no import at all while still isolating the child from stray local modules. The
`__name__ == "__main__"` guard still fires because `-c` runs with `__name__` set to `__main__`.
"""

import sys
import urllib.request


def main():
    webhook_url, payload_json = sys.stdin.read().split("\n", 1)
    req = urllib.request.Request(
        webhook_url,
        data=payload_json.encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass


if __name__ == "__main__":
    main()
