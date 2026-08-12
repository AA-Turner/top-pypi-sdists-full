"""arrow_pick — the reusable vertical ↑/↓ + Enter menu behind the sign-in prompt. The prompt_toolkit arrow path is
device-proven (VS Code / Codespaces terminals), so here we prove the TYPED FALLBACK (non-TTY / piped): it must pick
the right key by number and abort cleanly (None) on EOF — never a wrong or silent pick."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_canvas as C  # noqa: E402

fails = []


def check(name, cond):
    print(("PASS" if cond else "FAIL"), name)
    if not cond:
        fails.append(name)


OPTS = [("oauth", "Browser sign-in (OAuth)"), ("apikey", "Paste API key")]

# A StringIO stdin is non-TTY (isatty() == False) → arrow_pick takes the typed fallback.
sys.stdin = io.StringIO("2\n")
check("number 2 -> second key (apikey)", C.arrow_pick("Sign in", OPTS) == "apikey")
sys.stdin = io.StringIO("1\n")
check("number 1 -> first key (oauth)", C.arrow_pick("Sign in", OPTS) == "oauth")
# EOF / empty input aborts to None — never a wrong default pick
sys.stdin = io.StringIO("")
check("EOF -> None (clean abort)", C.arrow_pick("Sign in", OPTS) is None)
# empty option set is a no-op None, never an index error
check("empty options -> None", C.arrow_pick("x", []) is None)

print("\nRESULT:", "ALL PASS" if not fails else ("FAILURES: " + ", ".join(fails)))

# Discover-compatible wrapper — same shape as tests/test_integration_write_honesty.py.
# The checks above run AT IMPORT (pure functions, offline). A bare module-level sys.exit()
# raises SystemExit while pytest is importing the module, which pytest reports as an
# INTERNALERROR and which aborts collection for the WHOLE directory — so a green run of this
# file was silently costing us every other test in the suite. Guarding it keeps `python
# test_arrow_pick.py` working exactly as before while letting the file be collected.
import unittest  # noqa: E402


class ArrowPickChecks(unittest.TestCase):
    def test_all_arrow_pick_checks_pass(self):
        self.assertEqual(fails, [], f"failing checks: {fails}")


if __name__ == "__main__":
    sys.exit(1 if fails else 0)
