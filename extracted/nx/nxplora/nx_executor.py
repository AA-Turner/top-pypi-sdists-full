"""
nx_executor.py — NX Execution Mode
When NX is doing code/file work, stream the output inline in the terminal
like Codex does — diffs, commands, results — not just a chat response.
"""

import difflib
import hashlib
import subprocess
from typing import Optional, Callable, List, Dict, Any
from dataclasses import dataclass, field

from nx_canvas import NXCanvas
# SECURITY-CRITICAL import — NOT swallowed. The coding-lane gate is a safety control; a missing gate is a
# FATAL condition, never a degraded one. If nx_code_gate can't import (e.g. dropped from py_modules — the
# nx_browse / nx_code_gate ship-omission class), this raises at module load and the CLI fails loudly, instead
# of run_command silently shipping with no PROHIBITED enforcement (a fake-success generator). Pinned by
# tests/test_packaging_invariants.py.
from nx_code_gate import classify_code_action


def is_execution_task(user_input: str, world: str) -> bool:
    """Only trigger execution mode for explicit execution requests in code worlds."""
    code_worlds = {"nx-code", "code", "devops"}
    if world not in code_worlds:
        return False

    execution_keywords = [
        "create file",
        "write file",
        "build",
        "deploy",
        "implement",
        "run script",
        "execute",
    ]
    text = (user_input or "").lower()
    return any(keyword in text for keyword in execution_keywords)


def stream_plan(steps: list[str]):
    """Print the execution plan before starting."""
    print("\n✦ Plan")
    for index, step in enumerate(steps, 1):
        print(f"  {index}. {step}")
    print()


def stream_file_write(path: str, content: str, original: Optional[str] = None):
    """Stream a file write with diff output."""
    print(f"  ✦ {path}")
    if original:
        diff = difflib.unified_diff(
            original.splitlines(),
            content.splitlines(),
            lineterm="",
        )
        for line in list(diff)[2:]:
            if line.startswith("+"):
                print(f"  \033[32m{line}\033[0m")
            elif line.startswith("-"):
                print(f"  \033[31m{line}\033[0m")
            else:
                print(f"  {line}")
    else:
        lines = content.splitlines()[:10]
        for line in lines:
            print(f"  \033[32m+ {line}\033[0m")
        remaining = len(content.splitlines()) - len(lines)
        if remaining > 0:
            print(f"  \033[90m  ... {remaining} more lines\033[0m")
    print()


def stream_command(cmd: str, cwd: Optional[str] = None) -> int:
    """Run a shell command and stream output inline."""
    print(f"  \033[90m$ {cmd}\033[0m")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    for line in result.stdout.splitlines():
        print(f"  {line}")
    if result.returncode != 0:
        print(f"  \033[31m✗ exited {result.returncode}\033[0m")
    else:
        print("  \033[32m✓ done\033[0m")
    print()
    return result.returncode


def stream_result(message: str, success: bool = True):
    """Print final result."""
    icon = "✦" if success else "✗"
    color = "\033[32m" if success else "\033[31m"
    print(f"{color}{icon} {message}\033[0m\n")


def execution_header(task: str):
    """Print execution mode header."""
    print("\n\033[90m── executing ──────────────────────────\033[0m")
    print(f"  {task}")
    print("\033[90m───────────────────────────────────────\033[0m\n")


def execution_footer():
    """Print execution mode footer."""
    print("\033[90m── done ───────────────────────────────\033[0m\n")



# ── Local execution tools ─────────────────────────────────────────────────────
# NX can read, write, list, grep, and run commands directly in the local repo.

import base64
import os as _os
import re
import shlex
from pathlib import Path as _Path
from typing import Optional as _Optional


def get_cwd() -> str:
    return _os.getcwd()


_SENSITIVE_PREFIXES = (
    "/etc", "/usr", "/bin", "/sbin", "/var", "/System", "/Library",
    "/private", "/dev", "/root", "/boot", "/proc", "/sys",
)

# Home-directory secrets — blocked even though they're under $HOME. These hold
# SSH keys, cloud creds, GPG keys, NX's own auth tokens + MCP credentials, and
# package-registry tokens. A model must never read or write these.
_HOME_SECRET_SUFFIXES = (
    ".ssh", ".aws", ".gnupg", ".config/gh", ".docker/config.json",
    ".netrc", ".pypirc", ".npmrc", ".kube", ".azure", ".gcloud",
    ".nx/config.json", ".nx/credentials", ".nx/mcp_credentials.json",
    ".nx/auth.json", ".config/nx",
    # The canonical NX CLI + nexplora-v2 source repos. Whatever a given
    # operator does (create a skill, save a file, run a command) must only
    # ever affect THEIR OWN account/data — never the shared product repos
    # that every other operator depends on. These only exist on the
    # developer's own machine, but the rule holds regardless of whose
    # machine it is.
    "Nx", "nexplora-v2",
)

# Exact secret-bearing filenames blocked ANYWHERE (not only under $HOME) — a project
# may carry its own key/credential/registry-auth file, and its contents must never be
# read into the model. Extension/prefix matches (*.pem, id_rsa*, service-account*) are
# handled inline in _is_home_secret alongside this set.
_SECRET_FILENAMES = frozenset({
    "credentials", "credentials.json", ".git-credentials", ".htpasswd",
    "id_rsa", "id_ed25519", "id_ecdsa", "id_dsa",
    ".npmrc", ".pypirc", ".netrc", ".pgpass", ".dockercfg",
    "gcloud-service-key.json", "firebase-adminsdk.json", "kubeconfig",
    "secrets.yaml", "secrets.yml", "secrets.json",
    "terraform.tfstate", "terraform.tfvars",
})


def _is_home_secret(resolved: _Path) -> bool:
    """True if the resolved path is (or is inside) a home-secret location."""
    try:
        home = _Path(_os.path.expanduser("~")).resolve()
        rs = str(resolved)
        for suf in _HOME_SECRET_SUFFIXES:
            secret = str((home / suf))
            if rs == secret or rs.startswith(secret + "/"):
                return True
        # Any .env / .env.* / *.env file anywhere is sensitive (prod.env, staging.env too).
        name = resolved.name.lower()
        if name == ".env" or name.startswith(".env.") or name.endswith(".env"):
            return True
        # Secret-bearing files by name/extension ANYWHERE — including inside a cwd project
        # NX is otherwise allowed to read. Their contents get fed to the model, so a private
        # key or credential dump must never be readable. Extensions are the clearly-private
        # key/cert/keystore set only (.asc/.gpg/.pub dropped — often public/signatures).
        if (name in _SECRET_FILENAMES
                or name.startswith(("id_rsa", "id_ed25519", "id_ecdsa", "id_dsa",
                                    "service-account", "serviceaccount"))
                or name.endswith((".pem", ".key", ".p12", ".pfx", ".pkcs12", ".keystore",
                                  ".jks", ".ppk", ".pk8"))):
            return True
        # Block reaching into OTHER users' home dirs.
        for base in ("/Users/", "/home/"):
            if rs.startswith(base):
                # /Users/<someone>/... — allow only the current user's tree.
                rel = rs[len(base):]
                first = rel.split("/", 1)[0] if rel else ""
                if first and (home.name != first):
                    return True
    except Exception:
        return True  # fail closed
    return False

def _resolve_safe_path(path: str) -> _Optional[_Path]:
    """Resolve `path` under cwd (or absolute under a safe prefix).
    Returns None if the resolved path escapes cwd or hits a sensitive prefix
    (system path OR home secret).
    """
    try:
        cwd = _Path(get_cwd()).resolve()
        if path.startswith("~"):
            p = _Path(_os.path.expanduser(path))
        elif path.startswith("/"):
            p = _Path(path)
        else:
            p = (cwd / path)
        resolved = p.resolve()
        # Block parent-traversal escapes: a relative path containing ".." that
        # resolves OUTSIDE the cwd tree is a traversal attack — refuse it.
        if (".." in path.replace("\\", "/").split("/")) and not str(resolved).startswith(str(cwd)):
            return None
        # Block sensitive system prefixes outright.
        for pref in _SENSITIVE_PREFIXES:
            if str(resolved).startswith(pref + "/") or str(resolved) == pref:
                return None
        # Block home secrets (SSH/AWS/GPG/NX tokens/registry creds/.env/other homes).
        if _is_home_secret(resolved):
            return None
        return resolved
    except Exception:
        return None


def read_file(path: str) -> dict:
    """Read a file. Blocks reads from sensitive system paths."""
    try:
        p = _resolve_safe_path(path)
        if p is None:
            return {"error": f"Refused: path is in a restricted location"}
        if not p.exists():
            return {"error": f"File not found: {path}"}
        if not p.is_file():
            return {"error": f"Not a file: {path}"}
        content = p.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")
        return {
            "path": str(p),
            "content": content,
            "lines": len(lines),
            "size": len(content),
        }
    except Exception as e:
        return {"error": str(e)}


def list_files(path: str = ".") -> dict:
    """List files in a directory. Blocks listing sensitive system paths."""
    try:
        p = _resolve_safe_path(path)
        if p is None:
            return {"error": f"Refused: path is in a restricted location"}
        if not p.exists():
            return {"error": f"Directory not found: {path}"}
        files = []
        for item in sorted(p.iterdir()):
            files.append({
                "name": item.name,
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0,
            })
        return {"path": str(p), "files": files, "count": len(files)}
    except Exception as e:
        return {"error": str(e)}


def write_file(path: str, content: str) -> dict:
    """Write content to a file. Blocks writes to sensitive system paths."""
    try:
        p = _resolve_safe_path(path)
        if p is None:
            return {"error": f"Refused: path is in a restricted location"}
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return {"success": True, "path": str(p), "bytes": len(content)}
    except Exception as e:
        return {"error": str(e)}


# Defense-in-depth blocklist. NOTE: the PRIMARY protection is the approve_gate
# in nx_cli.py — every command is shown to the operator before it runs. This
# list is a secondary safety net that refuses obviously-catastrophic commands
# even if approved by mistake. It is NOT relied upon as the security boundary.
_RUN_COMMAND_BLOCKED = (
    "rm -rf /", "rm -rf ~", "rm -rf $home", "rm -rf /*", "sudo ", "doas ",
    "mkfs", "dd if=", "> /dev/", "shutdown", "halt", "reboot",
    "diskutil erasedisk", "diskutil erasevolume",
    "chmod -r 777 /", "chown -r", "killall ",
    ":(){:|:&};:",                     # fork bomb
    " && rm ", "; rm ", "| rm ",
)
# Sensitive paths that must never be touched by a shell command, even one the
# operator approves in a hurry. Matched as substrings (lowercased).
_RUN_COMMAND_SECRET_PATHS = (
    "/.ssh/", "/.aws/", "/.gnupg/", "/.pypirc", "/.netrc", "/.npmrc",
    "/.nx/config", "/.nx/credentials", "/.nx/mcp_credentials", "/.nx/auth",
    "id_rsa", "id_ed25519", "credentials.json",
)
# The canonical NX CLI + nexplora-v2 source repos. An operator asking NX to
# "save a skill" or do any other ordinary personal-data action must never be
# able to read/explore/write into the shared product repos every other
# operator depends on — only their own account/data. The check runs on the
# RAW command string (before the shell expands `~`), so both the literal
# `~/...` form a model would actually write AND the fully-resolved absolute
# path (expanduser, in case a command spells it out) are matched.
_RUN_COMMAND_PROTECTED_REPOS = ("~/nx", "~/nexplora-v2") + tuple(
    _os.path.expanduser(p).lower() for p in ("~/Nx", "~/nexplora-v2")
)

def command_safety_error(cmd: str):
    """The shared shell-command safety gate. Returns a refusal STRING (the "Refused: …" reason)
    when the command must not run, else None. Extracted so run_command AND the background runner
    (nx_background) enforce the IDENTICAL policy from ONE source — no drift between the two shells.

    Enforces the never-fire tier only: the PROHIBITED semantic class (force-push, history rewrite,
    rm -rf, secret write, env/secret exfiltration, remote-exec, sudo/system destroy — fail-closed,
    homoglyph-folded), the static substring blocklist (belt-and-suspenders), protected secret paths,
    and the canonical product repos. The GATED / GATED_MAIN tiers stay the approve_gate's job upstream
    in nx_cli.py (staged-as-a-diff)."""
    low = cmd.lower()
    _cv = classify_code_action(cmd)
    if _cv.prohibited:
        return f"Refused: {_cv.reason}"
    for b in _RUN_COMMAND_BLOCKED:
        if b in low:
            return f"Refused: command contains blocked token ({b!r})"
    # Refuse commands that reference home-secret paths (key/cred exfiltration).
    for sp in _RUN_COMMAND_SECRET_PATHS:
        if sp in low:
            return "Refused: command references a protected secret path"
    # Refuse commands that reference the canonical product repos.
    for rp in _RUN_COMMAND_PROTECTED_REPOS:
        if rp in low:
            return "Refused: command references a protected repo (not your account's data)"
    return None


def run_command(cmd: str, timeout: int = 30) -> dict:
    """Run a shell command in cwd. Defense-in-depth blocklist (the approve_gate
    in nx_cli.py is the primary control — this is a secondary net)."""
    _err = command_safety_error(cmd)
    if _err:
        return {"error": _err}
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=get_cwd(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "stdout": result.stdout[:4000],
            "stderr": result.stderr[:2000],
            "returncode": result.returncode,
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"error": str(e)}


def grep_files(pattern: str, path: str = ".", file_ext: str = "") -> dict:
    """Search for a pattern across files."""
    try:
        cmd = f"grep -rn '{pattern}' {path}"
        if file_ext:
            cmd += f" --include='*.{file_ext}'"
        result = run_command(cmd, timeout=10)
        matches = []
        for line in result.get("stdout", "").split("\n"):
            if line.strip():
                matches.append(line.strip())
        return {"matches": matches[:50], "count": len(matches)}
    except Exception as e:
        return {"error": str(e)}


# ── File edit parsing ─────────────────────────────────────────────────────────


# Language-AGNOSTIC by construction — NX does not special-case a stack (React over Rust). This allowlist
# covers the common source, web, systems, scripting, config, data, and docs extensions across languages;
# it deliberately EXCLUDES secret/binary shapes (.env, .pem, .key, executables) — those are refused, not
# edited. Missing a niche extension over-refuses an edit (safe); it can never let a secret write through.
VALID_EDIT_EXTENSIONS = (
    # JS / TS / web frameworks
    ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro",
    ".css", ".scss", ".sass", ".less", ".html", ".htm", ".ejs", ".hbs", ".pug",
    # Python
    ".py", ".pyi", ".pyx",
    # systems / compiled
    ".rs", ".go", ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".cs", ".java",
    ".kt", ".kts", ".swift", ".m", ".mm", ".scala", ".zig", ".dart", ".ex", ".exs", ".erl", ".hs",
    # scripting
    ".rb", ".php", ".pl", ".lua", ".r", ".jl", ".sh", ".bash", ".zsh", ".fish", ".ps1", ".groovy",
    # config / data / schema
    ".json", ".jsonc", ".json5", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".properties",
    ".xml", ".csv", ".tsv", ".sql", ".graphql", ".gql", ".proto", ".prisma", ".tf", ".hcl",
    # docs
    ".md", ".mdx", ".txt", ".rst", ".adoc", ".tex",
    # build
    ".gradle", ".cmake", ".mk", ".bazel", ".bzl", ".gemspec", ".podspec",
)


def _is_valid_edit_path(file_path: str) -> bool:
    """Reject hallucinated, unsupported, or unsafe file paths.

    Hard rejects:
      - hallucinated placeholders like 'relative/path/to/...'
      - absolute paths (cannot be written outside the working dir)
      - paths containing '..' segments (path traversal)
      - paths starting with '~' (home expansion bypass)
      - non-allowlisted extensions
    """
    import os as _os
    if not isinstance(file_path, str) or not file_path.strip():
        return False
    if "relative/path" in file_path:
        return False
    if file_path.startswith(("/", "~")):
        return False
    norm = _os.path.normpath(file_path)
    if norm.startswith(".."):
        return False
    if any(part == ".." for part in norm.split(_os.sep)):
        return False
    if not any(file_path.endswith(ext) for ext in VALID_EDIT_EXTENSIONS):
        return False
    return True


def parse_file_edits(response_text: str) -> list[dict]:
    """
    Parse file edit blocks from an LLM response.
    Format:
        ```file: path/to/file.py
        # old_code
        ...
        # new_code
        ...
        ```
    Rejects hallucinated paths such as `relative/path/to/file.py` and files
    without a supported extension.
    """
    import re
    edits = []
    # Format 1: explicit # old_code / # new_code markers
    pattern1 = re.compile(
        r"```file:\s*(.+?)\n"
        r"#\s*old_code\n"
        r"(.*?)\n"
        r"#\s*new_code\n"
        r"(.*?)\n```",
        re.DOTALL,
    )
    # Format 2: content before # new_code (no explicit # old_code marker)
    pattern2 = re.compile(
        r"```file:\s*(.+?)\n"
        r"(.*?)\n"
        r"#\s*new_code\n"
        r"(.*?)\n```",
        re.DOTALL,
    )
    seen = set()
    # Process explicit old/new blocks first
    for match in pattern1.finditer(response_text):
        file_path = match.group(1).strip()
        if not _is_valid_edit_path(file_path):
            continue
        old_code = match.group(2)
        if (file_path, hashlib.sha256(old_code.encode("utf-8", "replace")).hexdigest()) in seen:
            continue
        seen.add((file_path, hashlib.sha256(old_code.encode("utf-8", "replace")).hexdigest()))
        new_code = match.group(3)
        edits.append({
            "file": file_path,
            "old_code": old_code,
            "new_code": new_code,
        })
    # Then process implicit blocks, skipping any that overlap with explicit ones
    explicit_ranges = set()
    for edit in edits:
        start = response_text.find(edit["old_code"])
        if start != -1:
            explicit_ranges.add((start, start + len(edit["old_code"])))
    for match in pattern2.finditer(response_text):
        file_path = match.group(1).strip()
        if not _is_valid_edit_path(file_path):
            continue
        old_code = match.group(2)
        # Skip if this block contains an explicit old_code marker (handled by pattern1)
        if "# old_code" in old_code or "#old_code" in old_code:
            continue
        # Skip if it overlaps with an already-extracted explicit block
        overlap = False
        for start, end in explicit_ranges:
            if start <= match.start() < end or start < match.end() <= end:
                overlap = True
                break
        if overlap:
            continue
        if (file_path, hashlib.sha256(old_code.encode("utf-8", "replace")).hexdigest()) in seen:
            continue
        seen.add((file_path, hashlib.sha256(old_code.encode("utf-8", "replace")).hexdigest()))
        new_code = match.group(3)
        edits.append({
            "file": file_path,
            "old_code": old_code,
            "new_code": new_code,
        })
    return edits


def apply_file_edits(edits: list[dict], source_dir: str = None, canvas=None) -> list[dict]:
    """Apply parsed file edits. Returns result dicts.

    Defence-in-depth: re-validate every edit['file'] path before joining onto
    the source dir, and verify the resolved target stays under that source dir.
    parse_file_edits already runs _is_valid_edit_path, but a downstream caller
    could call apply_file_edits with hand-built edits, so we re-check.
    """
    base = (_Path(source_dir) if source_dir else _Path(get_cwd())).resolve()
    results = []
    for edit in edits:
        rel = edit.get("file", "")
        if not _is_valid_edit_path(rel):
            results.append({"file": rel, "error": "Refused: invalid edit path"})
            if canvas:
                canvas.step(f"Refused {rel}", "error")
            continue
        target = (base / rel).resolve()
        # Sandbox containment — target must stay under base.
        try:
            target.relative_to(base)
        except ValueError:
            results.append({"file": rel, "error": "Refused: resolved outside source_dir"})
            if canvas:
                canvas.step(f"Refused {rel}", "error")
            continue
        result = self_edit(str(target), edit["old_code"], edit["new_code"])
        results.append({"file": str(target), **result})
        if canvas and result.get("success"):
            canvas.step(f"Edited {rel}", "done")
        elif canvas:
            canvas.step(f"Failed to edit {rel}", "error")
    return results


# ── Self-editing capability ───────────────────────────────────────────────────
# NX can read, patch, rebuild, and reinstall itself when asked to fix bugs
# or add features. All changes go through the approve gate in nx_cli.py.


def self_edit(file_path: str, old_code: str, new_code: str) -> dict:
    """
    NX edits its own source code.
    Requires approve gate before applying. Atomic write via tempfile+rename.

    Path safety is enforced by the caller (parse_file_edits +
    apply_file_edits) which rejects absolute/traversal paths from model output.
    """
    try:
        p = _Path(file_path)
        if not p.exists():
            return {"error": f"File not found: {file_path}"}

        # Resolve symlinks so the atomic rename writes through to the real file,
        # not replacing the symlink with a regular file.
        real_p = p.resolve()

        # Capture the original mode bits so the atomic rename preserves them.
        try:
            original_mode = _os.stat(real_p).st_mode & 0o777
        except OSError:
            original_mode = 0o644

        content = real_p.read_text(encoding="utf-8")
        if old_code not in content:
            return {"error": "Old code not found in file — may have already been patched"}

        new_content = content.replace(old_code, new_code, 1)
        # Atomic write: tempfile in same dir, then rename. Prevents partial
        # writes if the process is killed mid-edit.
        import tempfile as _tf
        fd, tmp_path = _tf.mkstemp(prefix=f".{real_p.name}.", suffix=".tmp", dir=str(real_p.parent))
        try:
            with _os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(new_content)
                f.flush()
                try:_os.fsync(f.fileno())
                except OSError:pass
            # Restore the original mode bits on the tempfile so rename keeps them.
            try:
                _os.chmod(tmp_path, original_mode)
            except OSError:
                pass
            _os.replace(tmp_path, str(real_p))
            # fsync the parent directory so the rename is durable across crashes.
            try:
                dir_fd = _os.open(str(real_p.parent), _os.O_RDONLY)
                try:
                    _os.fsync(dir_fd)
                finally:
                    _os.close(dir_fd)
            except OSError:
                pass
        except Exception:
            try:_os.unlink(tmp_path)
            except OSError:pass
            raise

        return {
            "success": True,
            "file": str(real_p),
            "changed": True,
            "description": f"Replaced {len(old_code)} chars with {len(new_code)} chars",
        }
    except Exception as e:
        return {"error": str(e)}


def _bump_nx_version(src: str) -> tuple[str, str]:
    """
    Bump NX patch version in setup.py and nx_obfuscate.py.
    Returns (old_version, new_version).
    """
    setup_path = _Path(src) / "setup.py"
    obfuscate_path = _Path(src) / "nx_obfuscate.py"

    setup_text = setup_path.read_text(encoding="utf-8")
    m = re.search(r'version="(\d+)\.(\d+)\.(\d+)"', setup_text)
    if not m:
        raise RuntimeError("Could not parse version from setup.py")

    major, minor, patch = m.group(1), m.group(2), m.group(3)
    old_version = f"{major}.{minor}.{patch}"
    new_version = f"{major}.{minor}.{int(patch) + 1}"

    setup_text = setup_text.replace(f'version="{old_version}"', f'version="{new_version}"')
    setup_path.write_text(setup_text, encoding="utf-8")

    if obfuscate_path.exists():
        obf_text = obfuscate_path.read_text(encoding="utf-8")
        old_b64 = base64.b64encode(old_version.encode()).decode()
        new_b64 = base64.b64encode(new_version.encode()).decode()
        obf_text = obf_text.replace(f'_d("{old_b64}")', f'_d("{new_b64}")')
        obfuscate_path.write_text(obf_text, encoding="utf-8")

    return old_version, new_version


def rebuild_and_reinstall(source_dir: str = None) -> dict:
    """
    After self-editing NX source files, run tests, bump version, build,
    upload to PyPI, and reinstall into the pipx-managed venv via uv.
    Returns a summary dict on success or an error dict on failure.
    """
    src = source_dir or _os.path.expanduser("~/Nx/nx/cli")
    src_path = _Path(src)
    uv_bin = _os.path.expanduser("~/.local/bin/uv")
    pipx_python = _os.path.expanduser("~/.local/pipx/venvs/nxplora/bin/python")

    # 1. Run tests
    test_result = run_command(
        f"cd {shlex.quote(src)} && PYTHONPATH=. python3 -m unittest discover -s tests",
        timeout=1200,
    )
    if not test_result.get("success"):
        return {
            "error": f"Tests failed (aborting release):\n{test_result.get('stdout', '')}\n{test_result.get('stderr', '')}",
        }
    test_summary = test_result.get("stdout", "").strip().split("\n")[-1]

    # 2. Bump version
    try:
        old_version, new_version = _bump_nx_version(src)
    except Exception as e:
        return {"error": f"Version bump failed: {e}"}

    # 3. Build
    build_result = run_command(
        f"cd {shlex.quote(src)} && rm -rf dist build && python3 -m build",
        timeout=180,
    )
    if not build_result.get("success"):
        return {"error": f"Build failed: {build_result.get('stderr', '')}"}

    # 4. Upload to PyPI
    dist_files = list(src_path.glob(f"dist/nxplora-{new_version}*"))
    if not dist_files:
        return {"error": f"No distribution files found for version {new_version}"}
    upload_targets = " ".join(str(f) for f in dist_files)
    upload_result = run_command(
        f"twine upload {upload_targets}",
        timeout=180,
    )
    if not upload_result.get("success"):
        return {"error": f"PyPI upload failed: {upload_result.get('stderr', '')}"}

    # 5. Reinstall into pipx venv via uv
    wheel = src_path / f"dist/nxplora-{new_version}-py3-none-any.whl"
    if not wheel.exists():
        return {"error": f"Built wheel not found: {wheel}"}
    install_result = run_command(
        f"{uv_bin} pip install {wheel} --force-reinstall --python {pipx_python}",
        timeout=180,
    )
    if not install_result.get("success"):
        return {"error": f"pipx/uv install failed: {install_result.get('stderr', '')}"}

    return {
        "success": True,
        "message": (
            f"NX auto-released: {old_version} → {new_version}. "
            f"Tests: {test_summary}. Uploaded to PyPI and installed into pipx venv."
        ),
        "old_version": old_version,
        "new_version": new_version,
        "test_summary": test_summary,
    }


# ── Autonomous execution loop ─────────────────────────────────────────────────


@dataclass
class Step:
    label: str
    action: Callable[[], Any]
    requires_approval: bool = False
    auto_approve: bool = False


@dataclass
class ExecutionPlan:
    task: str
    steps: List[Step] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


class NXExecutor:
    def __init__(self):
        self._canvas: Optional[NXCanvas] = None
        self._halted = False
        self._results: Dict[str, Any] = {}

    def _gate(self, step: Step) -> bool:
        if step.auto_approve:
            return True
        return self._canvas.request_approval(f"Approve step: {step.label}")

    def _run_step(self, step: Step) -> Any:
        self._canvas.update_step(step.label, "working")
        try:
            result = step.action()
            self._canvas.update_step(step.label, "done")
            self._results[step.label] = result
            return result
        except Exception as e:
            self._canvas.update_step(step.label, "error")
            self._canvas.output(f"Step '{step.label}' failed: {e}")
            raise

    def execute(self, plan: ExecutionPlan, pre_approve: bool = False) -> Dict[str, Any]:
        self._canvas = NXCanvas(plan.task)
        self._canvas.open()

        if not pre_approve:
            if not self._canvas.request_approval(f"Execute: {plan.task}"):
                self._canvas.close("stopped")
                return {}

        for step in plan.steps:
            self._canvas.step(step.label, "pending")

        for step in plan.steps:
            if self._halted:
                break
            if step.requires_approval and not self._gate(step):
                self._canvas.update_step(step.label, "stopped")
                continue
            self._run_step(step)

        any_errors = any(s["status"] == "error" for s in self._canvas.steps)
        self._canvas.close("error" if any_errors else "done")
        return self._results

    def halt(self):
        self._halted = True
