"""Install shell completion for pysae-ai-tools (bash, zsh, fish).

Idempotent — skips if the marker comment is already present in the rc file.

Usage:
    pysae-ai-tools install-completion
"""

import os
import subprocess
import sys
from pathlib import Path

COMPLETION_MARKER = "# pysae-ai-tools completion"


def install_completion() -> None:
    """Install shell completion if not already present."""
    shell = os.environ.get("SHELL", "")
    shell_name = Path(shell).name if shell else "bash"

    rc_file: Path | None = None
    comp_var = ""
    if shell_name == "bash":
        rc_file = Path.home() / ".bashrc"
        comp_var = "bash_source"
    elif shell_name == "zsh":
        rc_file = Path.home() / ".zshrc"
        comp_var = "zsh_source"
    elif shell_name == "fish":
        rc_file = Path.home() / ".config" / "fish" / "completions" / "pysae-ai-tools.fish"
        comp_var = "fish_source"
    else:
        print(f"Shell {shell_name!r} not supported for completion.", file=sys.stderr)
        return

    if rc_file.exists() and COMPLETION_MARKER in rc_file.read_text(encoding="utf-8"):
        print(f"Completion already installed in {rc_file}", file=sys.stderr)
        return

    env = {**os.environ, "_PYSAE_AI_TOOLS_COMPLETE": comp_var}
    result = subprocess.run(
        ["pysae-ai-tools"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=10,
        env=env,
    )
    if result.returncode != 0 or not result.stdout.strip():
        print("Failed to generate completion script.", file=sys.stderr)
        return

    if shell_name == "fish":
        rc_file.parent.mkdir(parents=True, exist_ok=True)
        rc_file.write_text(f"{COMPLETION_MARKER}\n{result.stdout}", encoding="utf-8")
    else:
        with rc_file.open("a", encoding="utf-8") as f:
            f.write(f"\n{COMPLETION_MARKER}\n{result.stdout}\n")

    print(f"Shell completion installed for {shell_name} ({rc_file})", file=sys.stderr)


def main() -> None:
    """CLI entry point."""
    install_completion()
