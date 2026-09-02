#!/usr/bin/env python
import os
import sys
import traceback

from novita_sandbox.core.sandbox_sync.main import Sandbox


TEMPLATE = sys.argv[1] if len(sys.argv) > 1 else "5b0ibzq8yv6oqsaa3xdh"
CMD = "whoami; id -u; id -un; pwd"


def main() -> int:
    api_url = os.environ.get("NOVITA_API_URL") or f"https://api.{os.environ['NOVITA_DOMAIN']}"
    opts = {
        "api_key": os.environ["NOVITA_API_KEY"],
        "domain": os.environ["NOVITA_DOMAIN"],
        "api_url": api_url,
    }

    print("== novita sdk ==")
    print(f"template={TEMPLATE}")
    print(f"domain={opts['domain']}")
    print(f"api_url={opts['api_url']}")

    sbx = None
    try:
        sbx = Sandbox.create(template=TEMPLATE, timeout=300, **opts)
        print(f"sandbox_id={sbx.sandbox_id}")
        print(f"envd_version={getattr(sbx, '_envd_version', None)}")

        res = sbx.commands.run(CMD, timeout=120, request_timeout=120)
        print(f"exit_code={res.exit_code}")
        print("stdout:")
        print(res.stdout, end="" if res.stdout.endswith("\n") else "\n")
        print(f"stderr={res.stderr!r}")
        print(f"error={getattr(res, 'error', '')!r}")
        return int(res.exit_code or 0)
    except Exception as exc:
        print(f"ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        traceback.print_exc(limit=2)
        return 1
    finally:
        if sbx is not None:
            try:
                print(f"killed={sbx.kill()}")
            except Exception as exc:
                print(f"kill_error {type(exc).__name__}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
