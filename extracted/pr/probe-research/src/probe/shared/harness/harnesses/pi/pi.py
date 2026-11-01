"""The pi settings.json `packages` array entry this CLI owns. Details: DESIGN.md."""

from __future__ import annotations
import shutil
import subprocess
from functools import lru_cache

# One of the two non-stdlib imports here (`durable` below is the other), and free:
# claude_cli.py is itself stdlib-only (shutil/subprocess/dataclasses, see its
# own docstring), so importing it adds no dependency weight and, critically,
# no import cycle -- it does not import agent_rules, pi_config, or anything
# else in this package back. It is imported for `Result`, and for the bounded
# way to run a binary (`claude_cli.capture`, `pi_binary_available`'s sniff).
# setup.py's install_plugin/uninstall_plugin already return claude_cli.Result,
# and a later task wires pi's install/remove into the SAME call sites
# (apply_capture, apply_tracking) that already know how to read `.ok` and
# `.detail` off one. Inventing a second, differently-shaped result type here
# would make that wiring a translation layer instead of a drop-in.
from probe.shared.harness.harnesses.claude_code import binary as claude_cli

HARNESS_ID = "pi"


def pi_on_path() -> bool:
    """Whether a `pi` resolves on PATH at all -- no sniff, no subprocess
    (`setup.detectable_sources(sniff=False)`). `pi_binary_available` is the
    answer that tells pi from a two-letter impostor."""
    return shutil.which("pi") is not None


@lru_cache(maxsize=1)
def pi_binary_available() -> bool:
    """Whether the `pi` binary is on PATH and is really pi.

    ONCE PER PROCESS. The sniff below spawns `pi --help` with a 3s cap, and
    `backfill.which_agent(Agent.PI)` is its caller; the retired per-transcript
    digest lane asked once per transcript -- hundreds in a run -- which is
    when an uncached answer became minutes of subprocess spawning to re-derive
    a fact that cannot change mid-run. This is
    the same trade `backfill._supported_flags_cached` and `_agent_version_cached`
    already make for claude/codex, and the same reason. It is deliberately NOT
    what `plugin_cli.available` does for those two: that is a bare
    `shutil.which` costing nothing, so it has nothing to cache.

    The cost is that a pi installed DURING a wizard session is not noticed until
    the next one. `pi_binary_available.cache_clear()` is the escape hatch, and
    the tests that exercise the real sniff use it.

    HERE rather than in `setup.py`, where it was written, because two callers
    now need it and neither can reach the other: `backfill.which_agent` needs
    the sniff to tell a real pi from a two-letter impostor, and setup.py is a
    wizard module that reaches INTO backfill. `pi_config` imports neither, so
    it is the one place both can import from without a cycle.
    `setup.pi_binary_available` re-exports it, so the wizard and its tests are
    unaffected.

    The ONE `shutil.which` call for pi, kept as its own function rather than
    inlined in `detectable_sources` for two reasons: it is the single seam a
    caller (or a test) mocks to control pi detection without also touching
    `plugin_cli.available`'s claude/codex behaviour -- and it is NOT routed
    through `plugin_cli.available`/`binary_name` on purpose, because
    `plugin_cli.binary_name` RAISES for pi (see that module's docstring: pi has
    no marketplace CLI to route through). pi's binary is real even though its
    marketplace is not, and this is where that distinction is drawn.

    `which` alone is not enough here, unlike for `claude`/`codex`: "pi" is
    two letters, and an unrelated binary of that name on someone's PATH
    would put a phantom pi checkbox in every wizard run. So a hit is
    confirmed by running `pi --help` (3s cap) and looking for "coding" in
    the output -- pi 0.84.3's (and 0.86.0's) first help line is "pi - AI coding assistant
    with read, bash, edit, write tools", and the loose match is deliberate
    so forks that reword it still detect. The failure direction matters: a
    false NEGATIVE only hides the auto-detected row, and `--agent pi` still
    works; a false POSITIVE offers an install the machine cannot use.
    """
    path = shutil.which("pi")
    if path is None:
        return False
    # `probe status --refresh` bounds the sniff like every agent-CLI call.
    timeout = claude_cli.call_timeout(3)
    if timeout <= 0:
        return False
    try:
        completed = claude_cli.capture([path, "--help"], timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return False
    return completed.returncode == 0 and "coding" in completed.stdout.lower()


class PiIntegration:
    """pi's integration (HarnessIntegration): a package in its settings, never a marketplace CLI; its session log."""

    harness_id = HARNESS_ID
    extra_names = ()
    plugin_cli = None
    should_audit_inline = False
    has_plugin_ledger = False

    @property
    def session_log(self):
        from .session_log import Pi

        return Pi


INTEGRATION = PiIntegration()
