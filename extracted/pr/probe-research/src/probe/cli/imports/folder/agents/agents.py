"""pick the importing agent: which agents exist, which the importer offers, which are installed (launch.py launches one)."""

from __future__ import annotations
import shutil
from probe.foundation.compat.compat import StrEnum

# For `which_agent`'s pi branch only. Module-level and cheap: `pi_config` is
# stdlib plus `claude_cli` (itself stdlib), so this costs the lazy-import
# discipline in the docstring above nothing.
from .....shared.harness.harnesses import pi as pi_config


class Agent(StrEnum):
    """Which coding agent reads the folder.

    The importer's two are driven headlessly, do the work the same way, and are
    held to the SAME rule -- see CONFINEMENT below. Only the mechanism differs.
    """

    CLAUDE = "claude"
    CODEX = "codex"
    #: A RECOGNISED BINARY THE IMPORTER REFUSES. pi never runs the file
    #: importer: that lane needs the probe CLI via Bash, which pi's
    #: `DIGEST_TOOLS` allowlist deliberately lacks, so an import run on pi
    #: would read the whole folder and land nothing. `IMPORTER_AGENTS` below
    #: keeps the importer's picker off it and `resolve_agent` refuses
    #: `--agent pi` by name. The per-transcript digest lane that used to
    #: launch it retired server-side; no lane launches pi today.
    PI = "pi"


#: The agents the FILE IMPORTER offers, and the reason this is a tuple rather
#: than `list(Agent)`: enumerating the enum silently adopts whatever is added to
#: it, and `Agent.PI` is not an importer. Stated once, HERE, so a new
#: non-importer agent is opted in deliberately instead of leaking into every
#: picker that happened to iterate. Never filter PI out downstream -- that is
#: the same bug written once per call site.
IMPORTER_AGENTS: tuple[Agent, ...] = (Agent.CLAUDE, Agent.CODEX)


#: CONFINEMENT, and it is one property for both IMPORTER agents:
#:
#:     the imported folder is READ-ONLY; the agent writes only its own
#:     scratch directory, which is somewhere else entirely.
#:
#: This is the whole safety story, and stating it that way is what fixed it. The
#: earlier version confused "must not modify the folder" with "must not write at
#: all", so Claude ran with no Write tool while the import prompt instructed it
#: to write a manifest -- an impossible job, and every unit failed. Meanwhile
#: Codex ran `workspace-write` over the imported folder itself, which is the
#: property inverted: the customer's data was the one writable thing on disk.
#:
#: A scratch directory resolves both. The agent needs somewhere to put the
#: manifest; it does not need that somewhere to be the folder it is reading.
#:
#: The two mechanisms, and why each is the right instrument for its agent:
#:
#:   Claude   a PERMISSION RULE. `Edit(<folder>/**)` in a generated settings
#:            file, with the folder handed over read-only via `--add-dir` and
#:            the process cwd set to the scratch dir.
#:
#:            The rule MUST be spelled `Edit(...)`. A `Write(...)` deny rule is
#:            a silent no-op -- Claude Code prints "is not matched by file
#:            permission checks ... only Edit(path) rules are" and carries on.
#:            `Edit` covers every file-editing tool, Write included. Verified
#:            2026-08-06 against the real binary, both ways: with the rule the
#:            write is refused, without it the identical prompt succeeds.
#:
#:   Codex    the OS SANDBOX. `workspace-write` scoped by `-C <scratch>`.
#:            Codex confines where commands may WRITE, not which commands run,
#:            and reads are unrestricted -- so pointing the workspace at the
#:            scratch dir leaves the folder readable and unwritable in one move,
#:            with no pattern to get wrong. Verified the same day: read outside
#:            the workspace succeeded, write outside it was blocked.
#:
#: `workspace-write` rather than `read-only` because the agent writes its plan
#: state and JSONL in the scratch dir. NO NETWORK for its commands: code does
#: every upload, `probe-backfill-plan` is local, and a Codex agent with network
#: and a signed-in `probe` uploaded files a second time (2026-10-26). The
#: sandbox governs the agent's commands, not Codex's own model traffic.
#: `--skip-git-repo-check` is REQUIRED,
#: not tidiness: Codex refuses to run outside a git repo, and neither a research
#: folder on a shared mount nor a scratch dir under XDG state is one.
#:
#: The DIGEST lane restates the property rather than weakening it: there is no
#: second tree at all. The agent is pointed at its own scratch dir, containing a
#: rendered view and nothing else, so "read the folder, write elsewhere" becomes
#: "the only readable thing is already derived". That is why `agent_argv` skips
#: the Claude pair when folder == workdir, and why pi -- which has neither a
#: permission file nor an OS sandbox -- can be launched here at all.
#:
#: Say precisely what pi's mechanism IS, because it is easy to over-claim. The
#: confinement is the `--tools` VALUE THIS CALL SENDS, whatever the caller
#: passed: pi has no rule file to fall back on, so an allowlist with `bash` in
#: it is an unconfined pi and nothing else refuses it. `DIGEST_TOOLS[Agent.PI]`
#: is the value the digest lane sends and the value this branch falls back to
#: -- it is the safe default, not the enforcement. And even that is only
#: sufficient because there is nothing outside the scratch dir to reach: pi is
#: launched for digests, never for an import over a researcher's folder.
AGENT_COPY: dict[Agent, tuple[str, str]] = {
    Agent.CLAUDE: (
        "Claude Code",
        "Imports files from the selected folder.",
    ),
    Agent.CODEX: (
        "Codex",
        "Imports files from the selected folder.",
    ),
    # Not an importer row, and no longer any picker's row: this copy is what
    # `too_old` and the launcher's not-on-PATH message name it as. pi is a
    # binary the folder importer recognises and refuses (`resolve_agent`); the
    # per-transcript digest lane that offered it retired server-side.
    Agent.PI: (
        "pi",
        "Not offered: its tool allowlist has no shell to run a folder import.",
    ),
}


def which_agent(agent: Agent) -> str | None:
    """The agent's real binary, or None.

    `shutil.which`, never a shell: `codex` in particular is commonly SHADOWED by
    a shell alias (a local wrapper here), and an alias would silently swallow
    the arguments below. A PATH lookup with no shell cannot see one.

    pi needs a second question asked. "pi" is two letters and anything can be
    named that, so a bare `which` hit is not evidence -- the `--help` "coding"
    sniff is the impostor guard the wizard already uses, and this is the same
    one, so pi is detected by one rule in one place.
    """
    if agent is Agent.PI:
        path = shutil.which("pi")
        return path if path and pi_config.pi_binary_available() else None
    return shutil.which(agent.value)


def available_agents() -> list[Agent]:
    """Installed IMPORTER agents, in menu order. Empty means backfill cannot run.

    `IMPORTER_AGENTS`, not the enum: the digest lane has its own resolver and
    its own idea of what is usable, and a picker that walked every enum member
    would offer a folder import to an agent with no shell to run `probe` in.
    """
    return [a for a in IMPORTER_AGENTS if which_agent(a) is not None]
