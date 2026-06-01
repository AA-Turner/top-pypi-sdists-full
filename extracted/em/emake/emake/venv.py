"""Virtual environment management for emake."""

import os
import subprocess
import sys

SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class VirtualEnvironment:
    """Manages a virtual environment."""

    def __init__(self, path: str) -> None:
        """Initialize virtual environment manager.

        Args:
            path: Path to virtual environment. Defaults to .venv in cwd.
        """
        self.path: str = os.path.realpath(os.path.abspath(path))
        binpath = (
            os.path.join(self.path, "Scripts")
            if os.name == "nt"
            else os.path.join(self.path, "bin")
        )
        self.activate: str = os.path.join(binpath, "activate")
        self.python: str = os.path.join(
            binpath, "python.exe" if os.name == "nt" else "python"
        )
        self.ensure()
        self.ensure_pip()

    @property
    def exists(self) -> bool:
        """Check if virtual environment exists."""
        return (
            os.path.exists(self.path)
            and os.path.exists(self.activate)
            and os.path.exists(self.python)
        )

    def _chronic(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            env={**(env or os.environ), "EMAKE": "1"},
        )
        if proc.returncode != 0:
            if proc.stdout:
                print(proc.stdout)

            if proc.stderr:
                print(proc.stderr, file=sys.stderr)

            if check:
                raise subprocess.CalledProcessError(
                    proc.returncode,
                    proc.args,  # pyright: ignore[reportAny]
                    proc.stdout,
                    proc.stderr,
                )

        return proc

    def _spinner(
        self,
        action: str,
        *args: str,
        chronic: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        if not sys.stdout.isatty():
            print(f"{action}...")
            if chronic:
                return self._chronic(*args)

            return subprocess.run(
                args,
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "EMAKE": "1"},
            )

        print(f"{action}: [{SPINNER_FRAMES[0]}]", end="", flush=True)
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "EMAKE": "1"},
        )
        spinner_idx = 0
        while True:
            try:
                _ = proc.wait(0.1)
                break

            except subprocess.TimeoutExpired:
                pass

            spinner_idx = (spinner_idx + 1) % len(SPINNER_FRAMES)
            print(
                f"\r{action}: [{SPINNER_FRAMES[spinner_idx]}]",
                end="",
                flush=True,
            )

        print(
            "\r" + " " * (len(action) + 4 + len(SPINNER_FRAMES[spinner_idx])) + "\r",
            end="",
        )

        stdout = None
        if proc.stdout is not None:
            stdout = proc.stdout.read()

        stderr = None
        if proc.stderr is not None:
            stderr = proc.stderr.read()

        if chronic and proc.returncode:
            if proc.stdout:
                print(stdout)

            if proc.stderr:
                print(stderr, file=sys.stderr)

            raise subprocess.CalledProcessError(proc.returncode, args, stdout, stderr)

        return subprocess.CompletedProcess(args, proc.returncode, stdout, stderr)

    def ensure(self) -> None:
        if self.exists:
            return

        _ = self._spinner(
            "Creating virtual environment",
            "python" if "__compiled__" in globals() else sys.executable,
            "-m",
            "venv",
            "--system-site-packages",
            self.path,
            chronic=True,
        )

    def ensure_pip(self) -> None:
        _ = self._spinner(
            "Ensuring pip is installed",
            self.python,
            "-um",
            "ensurepip",
            chronic=True,
        )
        _ = self._spinner(
            "Upgrading pip",
            self.python,
            "-um",
            "pip",
            "install",
            "--upgrade",
            "pip",
            chronic=True,
        )

    def ensure_build_tools(self) -> None:
        """Ensure build and wheel are installed in the venv."""
        _ = self._spinner(
            "Installing build tools",
            self.python,
            "-um",
            "pip",
            "install",
            "build",
            "wheel",
            chronic=True,
        )

    def ensure_test_tools(self) -> None:
        """Ensure pytest is installed in the venv."""
        _ = self._spinner(
            "Installing test tools",
            self.python,
            "-um",
            "pip",
            "install",
            "-e",
            ".[test]",
            chronic=True,
        )

    def ensure_lint_tools(self, extras: list[str]) -> None:
        """Ensure linting tools are installed in the venv."""
        _ = self._spinner(
            "Installing lint tools",
            self.python,
            "-um",
            "pip",
            "install",
            "ruff",
            "vulture",
            "basedpyright",
            "dodgy",
            "pyroma",
            *(["-e", f".[{','.join(extras)}]"] if extras else []),
            chronic=True,
        )

    def install(self, *extras: str) -> None:
        """Install the package with optional extras.

        Args:
            extras: List of extra dependency groups to install.
        """
        _ = self._spinner(
            "Installing requirements",
            self.python,
            "-um",
            "pip",
            "install",
            "--quiet",
            "--editable",
            f".[{','.join(extras)}]" if extras else ".",
            chronic=True,
        )

    def run(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        chronic: bool = False,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """Run a command in the virtual environment.

        Args:
            *args: Command and arguments to run.
            env: Environment variables.

        Returns:
            CompletedProcess instance.
        """
        if chronic:
            return self._chronic(
                self.python,
                *args,
                env=env,
            )

        return subprocess.run(
            [self.python, *args],
            check=False,
            env={**(env or os.environ), "EMAKE": "1"},
            text=True,
            capture_output=capture_output,
        )


def get_venv() -> VirtualEnvironment:
    """Get a VirtualEnvironment instance.

    Args:
        path: Optional path to .venv directory.

    Returns:
        VirtualEnvironment instance.
    """
    return VirtualEnvironment(".venv")
