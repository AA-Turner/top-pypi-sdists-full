#!/usr/bin/env python3
"""
CVC override patch: hermes_cli/platforms.py
============================================

Adds the `cvc-dashboard` platform registration to the ref's
hermes_cli/platforms.py. Without this, the runtime doesn't know about
the CVC dashboard platform and falls back to `hermes-cli` defaults.

What this replaces:
  The CVC vendor copy of this file is wholesale-preserved across sync.
  That breaks when the ref adds new entries to the platforms list —
  this patch is the surgical alternative.

Anchor:
  Ref's last platform entry ends with `],)`. We insert one line before.

Format: a function that takes the ref's file contents and returns the
patched contents. No imports from the file itself — pure text surgery.
"""
from __future__ import annotations


def apply(content: str) -> str:
    """Insert the cvc-dashboard platform entry into the platforms list.

    Idempotent: if the entry already exists (re-running the patch), the
    file is returned unchanged.
    """
    if "cvc-dashboard" in content:
        return content

    # Find the platforms list ending pattern: "    (\"name\", ...),)\n"
    # We insert before that closing "    )," line.
    sentinel = "    (\"cron\","
    if sentinel not in content:
        raise RuntimeError(
            "CVC patch anchor not found in hermes_cli/platforms.py — "
            "ref changed its platforms list format. Update this patch."
        )

    cvc_line = '    ("cvc-dashboard",  PlatformInfo(label="🧠 CVC Dashboard",  default_toolset="hermes-cli")),\n'
    return content.replace(sentinel, cvc_line + sentinel)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: cvc_dashboard_platform.py <path-to-platforms.py>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        before = f.read()
    after = apply(before)
    if after == before:
        print(f"already patched: {path}")
    else:
        with open(path, "w") as f:
            f.write(after)
        print(f"patched: {path} (+{len(after) - len(before)} bytes)")
