"""The daemon's shell: the safe-list classifier and the runner (daemon v2, D15 / S9 / E6).

Part 1 ports Codex CLI's own unit tests for the list this classifier starts from:
    openai/codex  codex-rs/shell-command/src/command_safety/is_safe_command.rs
    (and is_dangerous_command.rs) at 9ca99b51713066681cce211184c0ff9035496979,
    the parent of 942af8447 (2026-08-19), which retired is_safe_command.rs.
    Copyright OpenAI, Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
Codex tests take an argv; ours take the command string the daemon's tool receives,
so each argv is joined with `shlex.join` (which quotes exactly as needed), and a
Codex `bash -lc SCRIPT` case is ported as SCRIPT. Every verdict that differs on
purpose says so in a comment marked OURS.

Part 2 is adversarial: every escape the plan (E6) and the review named.
Part 3 runs commands: the environment, the time limit, the output cap, and a git
repository armed with hooks, fsmonitor, filters, textconv, an external diff and a
gpg program — each trap proven live by a control run first, then shown not to
fire through `run`.
"""

from __future__ import annotations

import asyncio
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pytest

from probe.daemon.shell import Step, Verdict, classify, minimal_env, run

LINUX = sys.platform.startswith("linux")


@dataclass
class Box:
    home: Path
    work: Path
    outside: Path

    def verdict(self, command: str, *, cwd: Path | None = None, **kw) -> Verdict:
        return classify(
            command, workdirs=[self.work], home=self.home, cwd=cwd or self.work, **kw
        )

    def safe(self, command: str, **kw) -> bool:
        return self.verdict(command, **kw).safe


@pytest.fixture
def box(tmp_path: Path) -> Box:
    home = tmp_path / "home"
    work = home / "proj"
    (work / "nested").mkdir(parents=True)
    (work / "file.txt").write_text("hello\n")
    (work / "Cargo.toml").write_text("[package]\n")
    (work / "data.json").write_text('{"a": 1}\n')
    # The working folder is its own repository. git looks upward for `.git`, and
    # the classifier refuses a repository that starts outside the working
    # folders -- so without this, any stray `.git` above the temp folder (an
    # empty /tmp/.git appeared on the shared box) turns every git case red.
    subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", str(work)], check=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("secret\n")
    return Box(home=home, work=work, outside=outside)


def codex(argv: list[str]) -> str:
    return shlex.join(argv)


# --- Part 1: Codex's own tests, ported -------------------------------------


def test_codex_known_safe_examples(box: Box) -> None:
    assert box.safe(codex(["ls"]))
    # OURS: base64 only decodes; encoding hides text from the output scrubber.
    assert not box.safe(codex(["base64"]))
    assert box.safe(codex(["base64", "-d"]))
    assert box.safe(codex(["sed", "-n", "1,5p", "file.txt"]))
    assert box.safe(codex(["nl", "-nrz", "Cargo.toml"]))
    # Safe `find` command (no unsafe options).
    assert box.safe(codex(["find", ".", "-name", "file.txt"]))
    if LINUX:
        assert box.safe(codex(["numfmt", "1000"]))
        assert box.safe(codex(["tac", "Cargo.toml"]))
    else:
        assert not box.safe(codex(["numfmt", "1000"]))
        assert not box.safe(codex(["tac", "Cargo.toml"]))


def test_codex_git_commands_are_not_known_safe(box: Box) -> None:
    # Codex: "Git must not be trusted from its arguments alone" — every case unsafe.
    # OURS: git read verbs are allowed, hardened (flags required here, programs
    # neutralised by `run`, see Part 3), so three of these are safe on purpose.
    assert box.safe(codex(["git", "status", "--short"]))  # OURS: safe
    assert box.safe(codex(["git", "branch", "--show-current"]))  # OURS: safe
    assert box.safe("cd nested && git status")  # OURS: the zsh -lc case's script, safe
    for argv, why in [
        (["git", "log", "-p", "-1"], "--no-textconv"),  # OURS: safe once the flags are added
        (["git", "diff"], "--no-textconv"),
        (["git", "show", "HEAD"], "--no-textconv"),
        (["git", "branch"], "--show-current"),
        (["git", "--version"], "--version"),
        (["/usr/bin/git", "status"], "by its path"),
        (["bash", "-lc", "git status"], "runs another command"),
        (["zsh", "-lc", "cd nested && git status"], "runs another command"),
        (["bash", "-lc", "git diff | head -20"], "runs another command"),
    ]:
        verdict = box.verdict(codex(argv))
        assert not verdict.safe, argv
        assert why in verdict.reason, (argv, verdict.reason)
    assert "--no-textconv" in box.verdict("git diff | head -20").reason
    assert box.safe("git log -p -1 --no-textconv --no-ext-diff")


def test_codex_cargo_check_is_not_safe(box: Box) -> None:
    assert not box.safe(codex(["cargo", "check"]))


def test_codex_zsh_lc_safe_command_sequence(box: Box) -> None:
    # OURS: the wrapper itself is refused; the script inside it is what we check.
    assert not box.safe(codex(["zsh", "-lc", "ls"]))
    assert box.safe("ls")


def test_codex_unknown_or_partial(box: Box) -> None:
    assert not box.safe(codex(["foo"]))
    assert not box.safe(codex(["git", "fetch"]))
    assert not box.safe(codex(["sed", "-n", "xp", "file.txt"]))
    # Unsafe `find` commands.
    for argv in [
        ["find", ".", "-name", "file.txt", "-exec", "rm", "{}", ";"],
        ["find", ".", "-name", "*.py", "-execdir", "python3", "{}", ";"],
        ["find", ".", "-name", "file.txt", "-ok", "rm", "{}", ";"],
        ["find", ".", "-name", "*.py", "-okdir", "python3", "{}", ";"],
        ["find", ".", "-delete", "-name", "file.txt"],
        ["find", ".", "-fls", "/etc/passwd"],
        ["find", ".", "-fprint", "/etc/passwd"],
        ["find", ".", "-fprint0", "/etc/passwd"],
        ["find", ".", "-fprintf", "/root/suid.txt", "%#m %u %p\n"],
    ]:
        verdict = box.verdict(codex(argv))
        assert not verdict.safe, argv
        # Refused for the find option itself, not for some other part of the line.
        assert "find -" in verdict.reason, (argv, verdict.reason)


def test_codex_base64_output_options_are_unsafe(box: Box) -> None:
    for argv in [
        ["base64", "-o", "out.bin"],
        ["base64", "--output", "out.bin"],
        ["base64", "--output=out.bin"],
        ["base64", "-ob64.txt"],
    ]:
        verdict = box.verdict(codex(argv))
        assert not verdict.safe and "writes to a file" in verdict.reason, argv


def test_codex_ripgrep_rules(box: Box) -> None:
    # Safe ripgrep invocations – none of the unsafe flags are present.
    assert box.safe(codex(["rg", "Cargo.toml", "-n"]))
    # Unsafe flags that do not take an argument (present verbatim).
    for argv in [["rg", "--search-zip", "files"], ["rg", "-z", "files"]]:
        assert not box.safe(codex(argv)), argv
    # Unsafe flags that expect a value, provided in both split and = forms.
    for argv in [
        ["rg", "--pre", "pwned", "files"],
        ["rg", "--pre=pwned", "files"],
        ["rg", "--hostname-bin", "pwned", "files"],
        ["rg", "--hostname-bin=pwned", "files"],
    ]:
        verdict = box.verdict(codex(argv))
        assert not verdict.safe and "runs another program" in verdict.reason, argv


def test_codex_windows_cases_on_posix(box: Box) -> None:
    # windows_powershell_full_path_is_safe returns early off Windows; the other
    # two assert "not safe" off Windows, as here.
    assert not box.safe(codex(["Get-Content", "Cargo.toml"]))
    assert not box.safe(codex(["C:\\Program Files\\Git\\cmd\\git.exe", "status"]))


def test_codex_classification_does_not_spawn_a_path(box: Box, tmp_path: Path) -> None:
    fake = tmp_path / "pwsh"
    marker = tmp_path / "marker"
    fake.write_text(f"#!/bin/sh\nprintf spawned > {shlex.quote(str(marker))}\nexit 0\n")
    fake.chmod(0o755)
    assert not box.safe(codex([str(fake), "-Command", "Get-ChildItem"]))
    assert not marker.exists(), "classification must never run anything"


def test_codex_bash_lc_safe_examples(box: Box) -> None:
    assert box.safe("ls")
    assert box.safe("ls -1")
    # OURS: `grep -R` follows symlinks out of the working folders, and `grep -r`
    # reads every file under the folder (.env and keys too), so both ask; rg,
    # which skips hidden and ignored files, is the way to search a tree.
    verdict = box.verdict('grep -R "Cargo.toml" -n')
    assert not verdict.safe and "symlinks" in verdict.reason
    verdict = box.verdict('grep -r "Cargo.toml" -n')
    assert not verdict.safe and "every file under the folder" in verdict.reason
    assert box.safe("sed -n 1,5p file.txt")
    assert box.safe("sed -n '1,5p' file.txt")
    assert box.safe("find . -name file.txt")


def test_codex_bash_lc_safe_examples_with_operators(box: Box) -> None:
    assert not box.safe('grep -R "Cargo.toml" -n || true')  # OURS: -R, as above
    assert not box.safe('grep -r "Cargo.toml" -n || true')  # OURS: -r, as above
    assert box.safe("ls && pwd")
    assert box.safe("echo 'hi' ; ls")
    assert box.safe("ls | wc -l")


def test_codex_bash_lc_unsafe_examples(box: Box) -> None:
    # Four-arg version: `bash -lc git status`.
    assert not box.safe(codex(["bash", "-lc", "git", "status"]))
    # The extra quoting makes it a program named 'git status'.
    assert not box.safe("'git status'")
    assert not box.safe("find . -name file.txt -delete")
    assert not box.safe("ls && rm -rf /")
    assert not box.safe("(ls)")
    assert not box.safe("ls || (pwd && echo hi)")
    assert not box.safe("ls > out.txt")


# Codex's is_dangerous_command.rs flags `rm -f` wherever it hides. None of these
# is on the safe list, so every one of them asks here — including the ones Codex
# does not call dangerous (a plain `rm -r` still deletes).
@pytest.mark.parametrize(
    "command",
    [
        codex(["rm", "-rf", "/"]),
        codex(["rm", "-f", "/"]),
        codex(["/bin/rm", "-fr", "/tmp/example"]),
        codex(["rm", "-r", "-f", "/tmp/example"]),
        codex(["rm", "--force", "/tmp/example"]),
        codex(["rm", "/tmp/example", "-f"]),
        codex(["sudo", "rm", "-rf", "/tmp/example"]),
        codex(["env", "TARGET=/tmp/example", "rm", "-rf", "/tmp/example"]),
        codex(["env"] * 9 + ["rm", "-rf", "/tmp/example"]),
        "printf x | rm -rf /tmp/example",
        "if test -d /tmp/example; then rm --force /tmp/example; fi",
        'rm -rf "$TARGET" >/dev/null',
        'for target in /tmp/a /tmp/b; do rm -r -f "$target"; done',
        'echo "$(rm -rf /tmp/example)"',
        "bash -c 'rm -rf /tmp/example'",
        "trap 'rm -rf /tmp/example' EXIT",
        # Codex's "not dangerous" cases: still not on our safe list.
        codex(["rm", "-r", "/tmp/example"]),
        codex(["rm", "--", "-f"]),
        codex(["bash", "-lc", "echo 'rm -rf /tmp/example'"]),
        "cmd=rm; $cmd -rf /tmp/example",
        "if then rm -rf /tmp/example",
        codex(["env", "TARGET=/tmp/example", "rm", "-r", "/tmp/example"]),
        "trap 'echo rm -rf /tmp/example' EXIT",
    ],
)
def test_codex_dangerous_command_cases_are_not_safe(box: Box, command: str) -> None:
    assert not box.safe(command)


def test_codex_quoted_rm_text_is_only_text(box: Box) -> None:
    # The script inside Codex's `bash -lc "echo 'rm -rf /tmp/example'"`: echo prints it.
    assert box.safe("echo 'rm -rf /tmp/example'")


# --- Part 2: adversarial ---------------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        "ls",
        "ls -la nested",
        "pwd",
        "cat file.txt | head -n 5 | wc -l",
        "stat file.txt",
        "tail -n 3 file.txt",
        "grep -n hello file.txt",
        "rg -n hello nested",
        "find nested -type f",
        "find . -path './nested/*' -name '*.txt'",
        "jq -r '.a' data.json",
        "jq '.a/2' data.json",
        "jq -n --args '$ARGS' a b",
        "jq --arg p /etc/passwd '.a' data.json",
        "sort -t/ -k2 file.txt",
        "uniq file.txt",
        "base64 -d file.txt",
        "sed -n 5p file.txt",
        "cut -d/ -f1 file.txt",
        "echo '$HOME and `backticks` stay text'",
        "echo /etc/passwd",
        'echo "a b" | tr a-z A-Z',
        "which python3",
        "cd nested && pwd",
        "cd nested && cat ../file.txt",
        "cd nested; ls",
        "ls\npwd",
        "ls ;",
        "ls |\n wc -l",
        "ls 2>&1 | head",
        "ls 2>/dev/null",
        "ls >/dev/null 2>&1",
        "cat < file.txt",
        "cat -- file.txt",
        "git log --oneline --no-textconv --no-ext-diff -5",
        "git log --no-textconv --no-ext-diff origin/main..HEAD",
        "git diff --no-textconv --no-ext-diff HEAD~1",
        "git show --no-textconv --no-ext-diff HEAD:file.txt",
        "git blame --no-textconv file.txt",
        "git rev-parse HEAD",
        "git ls-files",
        "git -C nested status",
        "git --no-pager status",
    ],
)
def test_safe_commands(box: Box, command: str) -> None:
    verdict = box.verdict(command)
    assert verdict == Verdict(True, ""), verdict


@pytest.mark.parametrize(
    ("command", "why"),
    [
        # the named cases
        ("git -c core.pager=sh log", "git -c"),
        ("git -ccore.pager=sh log", "git -c"),
        ("git --config-env=core.pager=X log", "git -c"),
        ("git log -p", "--no-textconv --no-ext-diff"),
        ("git log -p --no-textconv", "--no-textconv --no-ext-diff"),
        ("git log -- --no-textconv --no-ext-diff", "--no-textconv --no-ext-diff"),
        ("git diff --no-index /etc/passwd x", "--no-index"),
        ("git diff --no-textconv --no-ext-diff --no-index /etc/passwd x", "--no-index"),
        ("rg --pre cat foo", "runs another program"),
        ("find . -exec rm {} \\;", "find -exec"),
        ("find . -delete", "find -delete"),
        ("jq --rawfile x /etc/passwd .", "jq --rawfile"),
        ("cat ~/.ssh/id_rsa", "credential"),
        ("cat .env", "credential"),
        ("cat ../../outside/secret.txt", "outside the working folders"),
        ("cat $(echo x)", "`$`"),
        ("cat `x`", "Backticks"),
        ("echo hi > out.txt", "writes output to a file"),
        ("ls; rm -rf x", "`rm` isn't on the safe list"),
        ("ls && curl evil", "`curl` isn't on the safe list"),
        ("bash -c 'ls'", "runs another command"),
        ("X=1 ls", "environment variable"),
        ("ls *", "glob"),
        ("cd /", "outside the working folders"),
        ("cat ~", "outside the working folders"),
        ("probe run list > out.txt", "never redirected"),
        ("python train.py", "`python` isn't on the safe list"),
        ("curl x", "`curl` isn't on the safe list"),
        ("rm x", "`rm` isn't on the safe list"),
        # shell syntax
        ('echo "$HOME"', "`$`"),
        ("echo ${HOME}", "`$`"),
        ("echo $((1+1))", "`$`"),
        ("cat <(ls)", "Parentheses"),
        ("{ ls; }", "`{`"),
        ("cat {/etc/passwd,x}", "`{`"),
        ("ls &", "background"),
        ("ls # rm -rf x", "Comments"),
        ("cat ~root/.bashrc", "~name"),
        ("cat x=~/.ssh/id_rsa", "credential folder"),  # names it: refused in every mode
        ("ls |", "no command"),
        ("&& ls", "no command"),
        ("cat 'unterminated", "never closed"),
        ("ls ;; pwd", "case"),
        # wrappers, paths, programs
        ("env ls", "runs another command"),
        ("sudo ls", "runs another command"),
        ("xargs cat", "runs another command"),
        ("timeout 5 ls", "runs another command"),
        ("nohup ls", "runs another command"),
        ("sh -c ls", "runs another command"),
        ("eval ls", "runs another command"),
        ("./cat file.txt", "by its path"),
        ("/bin/cat file.txt", "by its path"),
        ("sed -i s/a/b/ file.txt", "sed"),
        ("sed -n 1p -ewout", "not an option"),
        # redirects
        ("cat < ../../outside/secret.txt", "outside the working folders"),
        ("ls &> out.txt", "writes output to a file"),
        ("ls >&out.txt", "only 2>&1-style"),
        ("ls >| out.txt", "writes output to a file"),
        ("cat <<< hi", "Here-strings"),
        ("cat <<EOF\nhi\nEOF", "Heredocs"),
        # tool options
        ("sort -o out.txt file.txt", "writes files"),
        ("sort -ro out.txt file.txt", "writes files"),
        ("sort --out=out.txt file.txt", "writes files"),
        ("sort -T /tmp file.txt", "writes files"),
        ("sort --compress-program=gzip file.txt", "runs another program"),
        ("base64 --out=x", "writes to a file"),
        ("base64 -do x", "writes to a file"),
        ("rg -nz foo", "runs another program"),
        ("rg --pre=cat foo", "runs another program"),
        ("rg -L foo", "symlinks"),
        ("rg --follow foo", "symlinks"),
        ("rg --hidden foo", "hidden files"),
        ("rg --hid foo", "hidden files"),
        ("rg -. foo", "hidden files"),
        ("rg -uu foo", "hidden files"),
        ("rg -u -u foo", "hidden files"),
        ("find -L . -name x", "follows symlinks"),
        ("find . -follow -name x", "follows symlinks"),
        ("find . -files0-from list.txt", "start folders"),
        ("grep -R foo .", "symlinks"),
        ("grep -nR foo .", "symlinks"),
        ("grep --dereference-recursive foo .", "symlinks"),
        ("wc --files0-from=list.txt", "list of files"),
        ("uniq file.txt out.txt", "writes its output"),
        ("jq -f prog.jq data.json", "jq -f"),
        ("jq -L /tmp '.' data.json", "jq -f / -L"),
        ("jq --slurpfile x /etc/passwd .", "jq --slurpfile"),
        ("jq 'import \"a\" as $a; .' data.json", "import"),
        ("jq --debug-trace .", "isn't on the safe list"),
        ("jq . ../../outside/secret.txt", "outside the working folders"),
        ("cat -f/etc/passwd", "outside the working folders"),
        ("grep --file=/etc/passwd x file.txt", "outside the working folders"),
        ("cd", "exactly one folder"),
        ("cd -", "exactly one folder"),
        ("cd -P nested", "exactly one folder"),
        ("cd nested file.txt", "exactly one folder"),
        ("cd ~", "outside the working folders"),
        ("cd nested && cat ../../../outside/secret.txt", "outside the working folders"),
        # git
        ("git log --no-textconv --no-ext-diff --output=out.txt", "writes to a file"),
        ("git log --no-textconv --no-ext-diff --out=out.txt", "writes to a file"),
        ("git log --no-textconv --no-ext-diff --ext-diff", "external diff"),
        ("git log --no-textconv --no-ext-diff --textconv", "textconv"),
        ("git log --no-textconv --no-ext-diff --show-signature", "gpg"),
        ("git show --no-textconv --no-ext-diff --submodule=diff", "submodules"),
        ("git status -v", "-v prints diffs"),
        ("git blame file.txt", "--no-textconv"),
        ("git branch -D main", "--show-current"),
        ("git push", "read-only git verb"),
        ("git checkout main", "read-only git verb"),
        ("git --git-dir=/tmp/x status", "isn't on the safe list"),
        ("git --work-tree=/tmp status", "isn't on the safe list"),
        ("git -p status", "isn't on the safe list"),
        ("git -C / status", "outside the working folders"),
        ("git -C .. status", "outside the working folders"),
        ("git", "without a read verb"),
    ],
)
def test_refused_commands(box: Box, command: str, why: str) -> None:
    verdict = box.verdict(command)
    assert not verdict.safe, command
    assert verdict.probe_argv is None
    assert why in verdict.reason, verdict.reason


def test_probe_command_is_handed_back(box: Box) -> None:
    verdict = box.verdict("probe run list --json 'a b'")
    assert verdict == Verdict(False, "probe command", probe_argv=["run", "list", "--json", "a b"])
    assert box.verdict("probe run list > out.txt").probe_argv is None
    assert box.verdict("ls && probe run list").probe_argv is None


def test_symlink_inside_pointing_outside(box: Box) -> None:
    (box.work / "link").symlink_to(box.outside / "secret.txt")
    (box.work / "-link").symlink_to(box.outside / "secret.txt")
    (box.work / "outdir").symlink_to(box.outside)
    (box.work / "dangling").symlink_to(box.outside / "not-yet")
    for command in [
        "cat link",
        "cat -- -link",
        "cat file.txt -link",  # a tool that stops reading options early opens it
        "cat outdir/secret.txt",
        "ls outdir",
        "cat dangling",
        "cd outdir && cat secret.txt",
        "wc -l < link",
    ]:
        verdict = box.verdict(command)
        assert not verdict.safe, command
        assert "outside the working folders" in verdict.reason, (command, verdict.reason)
    assert box.verdict("cat link").reason == "It reads link: outside the working folders."


def test_hidden_folders_and_the_harness_files(box: Box) -> None:
    home, work = box.home, box.work
    for path in [
        work / ".venv" / "pyvenv.cfg",
        work / ".gitignore",
        work / ".claude" / "CLAUDE.md",
        home / ".claude" / "CLAUDE.md",
        home / ".claude" / "settings.json",
        home / ".claude" / ".credentials.json",
        home / ".claude" / "projects" / "-home-me" / "memory" / "MEMORY.md",
        home / ".claude" / "skills" / "probe" / "SKILL.md",
        home / ".claude" / "skills" / "probe" / ".env",
        home / ".codex" / "AGENTS.md",
        home / ".pi" / "agent" / "AGENTS.md",
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x\n")
    assert box.safe("cat .gitignore")  # a hidden FILE is fine
    assert box.safe("cat .claude/CLAUDE.md")
    assert box.safe("cat ~/.claude/CLAUDE.md")
    assert box.safe("cat ~/.claude/projects/-home-me/memory/MEMORY.md")
    assert box.safe("ls ~/.claude/skills")
    assert box.safe("cat ~/.claude/skills/probe/SKILL.md")
    assert box.safe("cat ~/.codex/AGENTS.md")
    assert box.safe("cat ~/.pi/agent/AGENTS.md")
    assert "hidden folder (.venv)" in box.verdict("cat .venv/pyvenv.cfg").reason
    assert "hidden folder (.venv)" in box.verdict("ls .venv").reason
    assert "outside" in box.verdict("cat ~/.claude/settings.json").reason
    assert "outside" in box.verdict("cat ~/.claude/.credentials.json").reason
    assert "credential" in box.verdict("cat ~/.claude/skills/probe/.env").reason


def test_credential_shapes_inside_the_folder(box: Box, monkeypatch) -> None:
    for name in [".env.local", "server.pem", "tls.key", "id_ed25519", ".netrc", "probe-key.json"]:
        (box.work / name).write_text("x\n")
    for name in [".env.local", "server.pem", "tls.key", "id_ed25519", ".netrc"]:
        assert "credential" in box.verdict(f"cat {name}").reason, name
    # `protected` works on a file that is otherwise fine (control first).
    assert box.safe("cat probe-key.json")
    refused = box.verdict("cat probe-key.json", protected=[box.work / "probe-key.json"])
    assert not refused.safe and "credential" in refused.reason
    # Probe's config under $XDG_CONFIG_HOME, even inside a working folder.
    (box.work / "xdg" / "probe").mkdir(parents=True)
    (box.work / "xdg" / "probe" / "config.toml").write_text("x\n")
    assert box.safe("cat xdg/probe/config.toml")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(box.work / "xdg"))
    assert "credential" in box.verdict("cat xdg/probe/config.toml").reason


def test_home_is_never_a_working_folder(box: Box) -> None:
    # The session started in ~ (E6: every session here did). ~ is not a root, so
    # commands that read the current folder by themselves ask; named paths inside
    # the working folder still run.
    at_home = {"cwd": box.home}
    for command in ["ls", "rg foo", "find -name x", "git status"]:
        verdict = box.verdict(command, **at_home)
        assert not verdict.safe and "current folder" in verdict.reason, (command, verdict.reason)
    # An option value ls doesn't know lands in ~ and is refused there, not skipped.
    assert "outside" in box.verdict("ls -w 80", **at_home).reason
    (box.home / "notes.txt").write_text("x\n")
    assert "outside" in box.verdict("cat notes.txt", **at_home).reason
    assert box.safe("cat ~/proj/file.txt", **at_home)
    assert box.safe("ls ~/proj", **at_home)
    assert box.safe("cd ~/proj && ls", **at_home)
    assert box.safe("cd proj && rg hello", **at_home)
    # After `;` the cd may have failed, so ~ is still a possible current folder.
    assert not box.safe("cd ~/proj; ls", **at_home)
    # A working folder given as ~ or / counts for nothing.
    verdict = classify("cat ~/x", workdirs=[box.home, Path("/")], home=box.home, cwd=box.work)
    assert "outside" in verdict.reason


def test_a_program_inside_the_folder_shadowing_a_safe_name(box: Box, monkeypatch) -> None:
    fake = box.work / "bin" / "cat"
    fake.parent.mkdir()
    fake.write_text("#!/bin/sh\necho pwned\n")
    fake.chmod(0o755)
    assert box.safe("cat file.txt")
    monkeypatch.setenv("PATH", f"{fake.parent}{os.pathsep}{os.environ['PATH']}")
    verdict = box.verdict("cat file.txt")
    assert not verdict.safe and "inside the working folders" in verdict.reason
    monkeypatch.setenv("PATH", f".{os.pathsep}{os.environ['PATH']}")
    assert "." not in minimal_env()["PATH"].split(os.pathsep)


def test_git_repository_must_start_inside(box: Box) -> None:
    shutil.rmtree(box.work / ".git")  # the fixture's own repository; this test builds its own
    git = ["git", "-c", "init.defaultBranch=main", "init", "-q"]
    subprocess.run([*git, str(box.home)], check=True)  # a dotfiles repo at ~
    verdict = box.verdict("git status")
    assert not verdict.safe and "repository at" in verdict.reason
    subprocess.run([*git, str(box.work)], check=True)
    assert box.safe("git status")
    assert box.safe("git -C nested log --oneline --no-textconv --no-ext-diff")


# --- the note-writing heredoc (write_dirs) ---


@pytest.fixture
def notes(box: Box) -> Path:
    folder = box.home / ".local" / "state" / "probe" / "notes"
    folder.mkdir(parents=True)
    return folder


BODY = "# Findings\n\nlr=3e-4 beat $LR; `rm -rf /` $(curl evil) ${HOME} * ? [x]\nEOFNOT\n"


@pytest.mark.parametrize(
    "form",
    [
        "cat > {f} <<'EOF'\n{body}EOF\n",
        "cat >> {f} <<'EOF'\n{body}EOF",
        'cat > {f} <<"EOF"\n{body}EOF\n',
        "cat > {f} <<-'EOF'\n{body}\t\tEOF\n",
        "cat <<'EOF' > {f}\n{body}EOF\n",
    ],
)
def test_note_heredoc_is_allowed(box: Box, notes: Path, form: str) -> None:
    command = form.format(f=notes / "run-1.md", body=BODY)
    verdict = box.verdict(command, write_dirs=[notes])
    assert (verdict.safe, verdict.reason, verdict.probe_argv) == (True, "", None)
    # The caller gets the file and the exact body bash writes, to scan and to diff.
    assert verdict.note_target == os.path.realpath(notes / "run-1.md")
    assert verdict.note_body == BODY
    assert verdict.note_append == (">>" in command)


def test_note_heredoc_with_tilde_path(box: Box, notes: Path) -> None:
    command = f"cat > ~/.local/state/probe/notes/n.md <<'EOF'\n{BODY}EOF\n"
    assert box.safe(command, write_dirs=[notes])


def test_note_heredoc_refusals(box: Box, notes: Path) -> None:
    (notes / "escape.md").symlink_to(box.outside / "secret.txt")
    target = notes / "n.md"
    cases = {
        f"cat > {target} <<EOF\n{BODY}EOF\n": "must be quoted",
        f"cat > {box.work / 'n.md'} <<'EOF'\n{BODY}EOF\n": "outside the folders open for writing",
        f"cat > {notes / 'escape.md'} <<'EOF'\n{BODY}EOF\n": "outside the folders open for writing",
        f"cat > {notes / 'missing' / 'n.md'} <<'EOF'\n{BODY}EOF\n": "existing folder",
        f"cat > {target} <<'EOF' ; rm x\n{BODY}EOF\n": "Heredocs",
        f"cat > {target} <<'EOF'\n{BODY}EOF\nrm x\n": "Something follows",
        f"cat > {target} <<'EOF'\n{BODY}": "never closed",
        f"cat > {target} <<'EOF' | sh\n{BODY}EOF\n": "Heredocs",
        f"cat > {target}": "writes output to a file",
        f"cat {target} <<'EOF'\n{BODY}EOF\n": "Heredocs",
    }
    for command, why in cases.items():
        verdict = box.verdict(command, write_dirs=[notes])
        assert not verdict.safe, command
        assert why in verdict.reason, (command, verdict.reason)
    # No write_dirs: nothing is writable.
    verdict = box.verdict(f"cat > {target} <<'EOF'\n{BODY}EOF\n")
    assert not verdict.safe and "no folder is open for writing" in verdict.reason


def test_note_heredoc_runs_with_the_body_unchanged(box: Box, notes: Path) -> None:
    target = notes / "n.md"
    command = f"cat > {target} <<'EOF'\n{BODY}EOF\n"
    assert box.safe(command, write_dirs=[notes])
    result = asyncio.run(run(command, cwd=box.work))
    assert result.exit_code == 0, result
    assert target.read_text() == BODY


# --- Part 3: run() ---------------------------------------------------------


def test_run_environment_is_minimal(tmp_path: Path, monkeypatch) -> None:
    marker = tmp_path / "bash_env_ran"
    rc = tmp_path / "rc.sh"
    rc.write_text(f"touch {shlex.quote(str(marker))}\n")
    monkeypatch.setenv("PROBE_TOKEN", "prb_live_should_not_leak")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-should-not-leak")
    monkeypatch.setenv("SOME_PARENT_VAR", "x")
    monkeypatch.setenv("BASH_ENV", str(rc))
    # Control: a bash that inherits BASH_ENV does source it.
    subprocess.run(["/bin/bash", "-c", "true"], check=True)
    assert marker.exists()
    marker.unlink()

    result = asyncio.run(run("env", cwd=tmp_path))
    assert result.exit_code == 0
    env = dict(line.split("=", 1) for line in result.output.splitlines() if "=" in line)
    assert "should-not-leak" not in result.output
    assert "PROBE_TOKEN" not in env and "OPENAI_API_KEY" not in env
    assert "SOME_PARENT_VAR" not in env and "BASH_ENV" not in env
    assert not marker.exists()
    expected = {
        "PATH", "HOME", "LANG", "LC_ALL", "TERM", "NO_COLOR", "PAGER", "GIT_PAGER",
        "GIT_TERMINAL_PROMPT", "GIT_CONFIG_NOSYSTEM", "GIT_OPTIONAL_LOCKS", "GIT_CONFIG_COUNT",
        "PROBE_CONFIG_PATH", "PROBE_TELEMETRY",  # a `probe` started here has no key
    }  # fmt: skip
    bash_own = {"PWD", "SHLVL", "_"}
    ours = {k for k in env if not k.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))}
    assert ours - bash_own == expected
    assert env["LANG"] == env["LC_ALL"] == "C.UTF-8"
    keys = {env[f"GIT_CONFIG_KEY_{n}"]: env[f"GIT_CONFIG_VALUE_{n}"]
            for n in range(int(env["GIT_CONFIG_COUNT"]))}  # fmt: skip
    assert keys["core.hooksPath"] == "/dev/null"
    assert keys["core.fsmonitor"] == "false"
    assert keys["core.pager"] == "cat"
    assert keys["diff.external"] == ""
    assert keys["core.sshCommand"] == "false"
    assert keys["protocol.allow"] == "never"
    assert minimal_env({"EXTRA": "1"})["EXTRA"] == "1"


def test_run_timeout_kills_the_process_group(tmp_path: Path) -> None:
    started = time.monotonic()
    result = asyncio.run(run("sleep 30 & echo $!; wait", cwd=tmp_path, timeout_s=1))
    assert time.monotonic() - started < 10
    assert result.timed_out and result.exit_code is None
    child = int(result.output.split()[0])
    for _ in range(50):  # the background sleep dies with its group
        if not _alive(child):
            break
        time.sleep(0.1)
    else:
        pytest.fail(f"background child {child} survived the timeout")


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    if LINUX:  # killed but not yet reaped by init counts as dead
        try:
            state = Path(f"/proc/{pid}/stat").read_text().rsplit(") ", 1)[-1][:1]
        except FileNotFoundError:
            return False
        return state not in ("Z", "X")
    return True


def test_run_output_cap_keeps_head_and_tail(tmp_path: Path) -> None:
    result = asyncio.run(run("seq 1 200000", cwd=tmp_path, max_output_chars=1000))
    assert result.exit_code == 0 and result.truncated and not result.timed_out
    assert result.output.startswith("1\n2\n3\n")
    assert result.output.endswith("199999\n200000\n")
    assert "bytes of output left out" in result.output
    assert len(result.output) < 1200

    small = asyncio.run(run("echo out; echo err >&2; exit 3", cwd=tmp_path))
    assert (small.exit_code, small.output, small.truncated) == (3, "out\nerr\n", False)


# --- a repository armed with every program git could run during a read ---


def _hook_script(path: Path, marker: Path, then: str = "") -> str:
    path.write_text(f"#!/bin/sh\ntouch {shlex.quote(str(marker))}\n{then}\n")
    path.chmod(0o755)
    return str(path)


def _trap_repo(root: Path) -> tuple[Path, Path, dict[str, str]]:
    """A repository whose own settings run a program (touching a marker) on reads."""
    repo, traps = root / "repo", root / "traps"
    repo.mkdir(parents=True)
    traps.mkdir()
    env = {"PATH": os.environ["PATH"], "HOME": str(root), "GIT_CONFIG_NOSYSTEM": "1"}

    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True)

    git("-c", "init.defaultBranch=main", "init", "-q")
    git("config", "user.email", "a@b")
    git("config", "user.name", "a")
    (repo / "a.txt").write_text("hello\n")
    (repo / "b.txt").write_text("hello\n")
    git("add", "-A")
    git("commit", "-qm", "init")
    (repo / ".gitattributes").write_text("a.txt filter=evil diff=evil\nb.txt filter=proc\n")
    hooks = traps / "hooks"
    hooks.mkdir()
    for hook in ("post-index-change", "pre-commit", "post-checkout", "reference-transaction"):
        _hook_script(hooks / hook, traps / "hook.ran")
    git("config", "core.hooksPath", str(hooks))
    git("config", "core.fsmonitor", _hook_script(traps / "fsmon.sh", traps / "fsmonitor.ran"))
    git("config", "core.pager", _hook_script(traps / "pager.sh", traps / "pager.ran"))
    for key, name, then in [
        ("filter.evil.clean", "clean", "cat"),
        ("filter.evil.smudge", "smudge", "cat"),
        ("diff.evil.textconv", "textconv", 'cat "$1"'),
        ("diff.evil.command", "extdiff", ""),
        ("filter.proc.process", "process", ""),  # a long-running filter; this one just exits
    ]:
        git("config", key, _hook_script(traps / f"{name}.sh", traps / f"{name}.ran", then))
    git("config", "gpg.program", _hook_script(traps / "gpg.sh", traps / "gpg.ran"))
    git("config", "log.showSignature", "true")
    # A commit carrying a (fake) signature, so `git log` verifies it with gpg.program.
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, env=env, check=True,
                          capture_output=True, text=True).stdout.strip()  # fmt: skip
    parent = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, env=env, check=True,
                            capture_output=True, text=True).stdout.strip()  # fmt: skip
    commit = (
        f"tree {tree}\nparent {parent}\nauthor a <a@b> 1700000000 +0000\n"
        "committer a <a@b> 1700000000 +0000\ngpgsig -----BEGIN PGP SIGNATURE-----\n \n"
        " -----END PGP SIGNATURE-----\n\nsigned\n"
    )
    sha = subprocess.run(["git", "hash-object", "-t", "commit", "-w", "--stdin"], cwd=repo,
                         env=env, input=commit, check=True, capture_output=True,
                         text=True).stdout.strip()  # fmt: skip
    git("update-ref", "refs/heads/main", sha)
    # Dirty the working tree without changing sizes, and leave the index's stat data
    # stale, so even `git status` has to read the files (through the clean filter).
    (repo / "a.txt").write_text("jello\n")
    (repo / "b.txt").write_text("jello\n")
    later = time.time() + 5
    for name in ("a.txt", "b.txt"):
        os.utime(repo / name, (later, later))
    for marker in traps.glob("*.ran"):  # `update-ref` above fired reference-transaction
        marker.unlink()
    return repo, traps, env


READS = [
    "git status",
    "git status --short",
    "git diff --no-textconv --no-ext-diff",
    "git log -p --no-textconv --no-ext-diff",
    "git log -1 --no-textconv --no-ext-diff",  # a signed commit; log.showSignature is on
    "git show --no-textconv --no-ext-diff",
    "git blame --no-textconv a.txt",
    "git ls-files -m",
]


def test_git_traps_are_live_without_the_safeguards(tmp_path: Path) -> None:
    """Control: the same repository, read with plain git, runs every trap.

    The process filter makes plain git abort ("the remote end hung up"), so each
    trap gets its own read, with a pathspec keeping b.txt out where needed.
    """
    repo, traps, env = _trap_repo(tmp_path)
    fired = {}
    for command in [
        "git status -- a.txt",  # fsmonitor, clean filter, then an index write: the hook
        "git status -- b.txt",  # the long-running (process) filter
        "git diff -- a.txt",  # external diff
        "git log -1",  # gpg, via log.showSignature (HEAD is a signed commit)
        "git log -p",  # textconv
    ]:
        before = {p.stem for p in traps.glob("*.ran")}
        subprocess.run(command.split(), cwd=repo, env=env, capture_output=True)
        fired[command] = {p.stem for p in traps.glob("*.ran")} - before
    assert {"hook", "fsmonitor", "clean"} <= fired["git status -- a.txt"], fired
    assert "process" in fired["git status -- b.txt"], fired
    assert "extdiff" in fired["git diff -- a.txt"], fired
    assert "textconv" in fired["git log -p"], fired
    assert "gpg" in fired["git log -1"], fired


def test_git_reads_through_run_fire_no_trap(tmp_path: Path) -> None:
    repo, traps, _ = _trap_repo(tmp_path)
    for command in READS:
        verdict = classify(command, workdirs=[repo], home=tmp_path, cwd=repo)
        assert verdict.safe, (command, verdict.reason)
        result = asyncio.run(run(command, cwd=repo))
        assert result.exit_code == 0, (command, result.output)
        assert not list(traps.glob("*.ran")), (command, [p.name for p in traps.glob("*.ran")])
    diff = asyncio.run(run("git diff --no-textconv --no-ext-diff", cwd=repo)).output
    assert "+jello" in diff  # the reads still work
    log = asyncio.run(run("git log -1 --no-textconv --no-ext-diff", cwd=repo)).output
    assert "signed" in log


def test_git_hooks_stay_off_even_when_status_writes_the_index(tmp_path: Path) -> None:
    # GIT_OPTIONAL_LOCKS=0 already stops `git status` writing the index (which
    # fires post-index-change); switch it back on to prove hooksPath holds alone.
    repo, traps, _ = _trap_repo(tmp_path)
    result = asyncio.run(run("git status", cwd=repo, env_extra={"GIT_OPTIONAL_LOCKS": "1"}))
    assert result.exit_code == 0, result.output
    assert not list(traps.glob("*.ran")), [p.name for p in traps.glob("*.ran")]


def test_git_reads_after_cd_and_dash_c_fire_no_trap(tmp_path: Path) -> None:
    repo, traps, _ = _trap_repo(tmp_path / "inner")
    here = tmp_path / "inner"
    for command in ["cd repo && git status", "git -C repo status", "git -C repo diff "
                    "--no-textconv --no-ext-diff"]:  # fmt: skip
        assert classify(command, workdirs=[here], home=tmp_path, cwd=here).safe, command
        result = asyncio.run(run(command, cwd=here))
        assert result.exit_code == 0, (command, result.output)
        assert not list(traps.glob("*.ran")), (command, [p.name for p in traps.glob("*.ran")])


# --- Review fixes (D3, D4, D5, cleanup): each failed on the code before it ------


@pytest.mark.parametrize(
    "command",
    [
        "cat a{},b}",  # `{}` inside a longer word pairs with a later `,` and `}`: bash expands it
        "ls }",  # a bare closing brace
        "ls x}",  # a closing brace inside a word
    ],
)
def test_a_brace_anywhere_but_the_whole_word_braces_is_refused(box: Box, command: str) -> None:
    verdict = box.verdict(command)
    assert not verdict.safe and "{" in verdict.reason, (command, verdict.reason)


def test_the_whole_word_braces_still_passes(box: Box) -> None:
    assert box.safe("echo {}")
    assert box.safe("echo '{a,b}'")  # quoted: bash expands nothing


@pytest.mark.parametrize(
    "command, why",
    [
        ("grep -r foo .", "every file under the folder"),  # reads every file below, keys included
        ("grep --directories recurse foo .", "every file under the folder"),
        ("rg -u foo", "ignored"),  # .env and keys are usually ignored
        ("rg --no-ignore foo", "ignored"),
        ("git show --no-textconv --no-ext-diff HEAD:.env", "credentials"),  # a secret file, from history
        ("git show --no-textconv --no-ext-diff HEAD:keys/id_ed25519", "credentials"),
        ("git log -p --no-textconv --no-ext-diff -- server.pem", "credentials"),
        ("git log -p --no-textconv --no-ext-diff -- .aws/config", "hidden"),
        ("diff -r nested nested", "folder"),
        ("diff nested nested", "folder"),
    ],
)
def test_recursive_and_history_readers_that_reach_secrets_ask(box: Box, command: str, why: str) -> None:
    verdict = box.verdict(command)
    assert not verdict.safe and why in verdict.reason, (command, verdict.reason)


def test_ordinary_history_reads_still_pass(box: Box) -> None:
    for command in ["git show --no-textconv --no-ext-diff HEAD:file.txt",
                    "git log --no-textconv --no-ext-diff origin/main..HEAD",
                    "rg -n hello nested", "diff file.txt data.json"]:
        verdict = box.verdict(command)
        assert verdict.safe, (command, verdict.reason)


def test_checked_out_notes_can_be_read_back(box: Box) -> None:
    notes = box.home / ".local" / "state" / "probe" / "notes"
    notes.mkdir(parents=True)
    (notes / "run-1.md").write_text("# Findings\n")
    (notes / "run-2.md").write_text("# Other\n")
    for command in [f"cat {notes / 'run-1.md'}", f"head -5 {notes / 'run-1.md'}",
                    f"wc -l {notes / 'run-1.md'}", f"diff {notes / 'run-1.md'} {notes / 'run-2.md'}"]:
        assert not box.safe(command), command  # a hidden folder outside the working folders...
        assert box.safe(command, write_dirs=[notes]), command  # ...unless it is the notes folder


def test_probe_config_is_protected_without_xdg_config_home(box: Box, monkeypatch) -> None:
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    config = box.home / ".config" / "probe"
    config.mkdir(parents=True)
    (config / "config.json").write_text("{}\n")
    verdict = box.verdict(f"cat {config / 'config.json'}", write_dirs=[config])
    assert not verdict.safe and "credential" in verdict.reason, verdict.reason


# --- Review round 2 (G-2, G-8, G-9, G-10): each failed on the code before it ----


@pytest.mark.parametrize(
    "command, why",
    [
        # [G-2] a `--` right after an option may be that option's value: what follows
        # it is then read as options again, by the tool if not by the check.
        ("rg -e -- --no-ignore foo", "ignored"),
        ("rg -e -- --hidden foo", "hidden files"),
        ("grep -e -- -r foo .", "every file under the folder"),
        ("sort -k -- -o out.txt file.txt", "writes files"),
        ("git log --no-textconv --no-ext-diff -S -- --output=out.txt", "writes to a file"),
        ("git show --no-textconv --no-ext-diff -S -- HEAD:.env", "credentials"),
        # [G-2] an encoder turns a secret into text the output scrubber cannot see.
        ("cat file.txt | base64", "scrubber"),
        ("base64 file.txt", "scrubber"),
        ("base64 -w0 file.txt", "scrubber"),
        ("xxd file.txt", "isn't on the safe list"),
        ("od -c file.txt", "isn't on the safe list"),
        ("hexdump -C file.txt", "isn't on the safe list"),
    ],
)
def test_a_dashdash_that_may_be_a_value_and_encoders_ask(box: Box, command: str, why: str) -> None:
    verdict = box.verdict(command)
    assert not verdict.safe and why in verdict.reason, (command, verdict.reason)


def test_a_dashdash_that_ends_the_options_still_passes(box: Box) -> None:
    for command in ["git diff --no-textconv --no-ext-diff -- file.txt", "rg -- hello file.txt",
                    "grep -e hello -- file.txt", "cat -- file.txt", "echo aGk= | base64 -d",
                    "base64 --decode file.txt",
                    # [R3-10] the `--`-as-value reading's empty value is not a name or a path.
                    "diff -u -- file.txt data.json", "uniq -c -- file.txt"]:
        verdict = box.verdict(command)
        assert verdict.safe, (command, verdict.reason)
    # [R3-10] ...nor the current folder ($HOME here), nor what makes jq's filter read as a file.
    for command in ["ls -la -- proj", "jq -r -- .a proj/data.json"]:
        verdict = box.verdict(command, cwd=box.home)
        assert verdict.safe, (command, verdict.reason)


def test_a_note_write_checks_the_program_it_runs(box: Box, notes: Path, monkeypatch) -> None:
    """[G-10] the note heredoc runs `cat` through PATH like any other command."""
    command = f"cat > {notes / 'n.md'} <<'EOF'\n{BODY}EOF\n"
    assert box.safe(command, write_dirs=[notes])
    fake = box.work / "bin" / "cat"
    fake.parent.mkdir()
    fake.write_text("#!/bin/sh\necho pwned\n")
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake.parent}{os.pathsep}{os.environ['PATH']}")
    verdict = box.verdict(command, write_dirs=[notes])
    assert not verdict.safe and "inside the working folders" in verdict.reason, verdict
    assert verdict.note_target is None


def _wait_dead(pid: int) -> bool:
    for _ in range(50):
        if not _alive(pid):
            return True
        time.sleep(0.1)
    return False


def test_run_stops_the_group_when_its_watch_says_so(tmp_path: Path, monkeypatch) -> None:
    """[G-8] the researcher moves the switch while a command runs: it is killed."""
    monkeypatch.setattr("probe.daemon.shell.WATCH_POLL_S", 0.05)
    pidfile = tmp_path / "pid"
    calls = {"n": 0}

    def watch() -> str | None:
        calls["n"] += 1
        return "the switch moved" if pidfile.exists() and pidfile.read_text().strip() else None

    started = time.monotonic()
    result = asyncio.run(run(f"sleep 30 & echo $! > {pidfile}; wait", cwd=tmp_path, timeout_s=20, watch=watch))
    assert time.monotonic() - started < 10 and calls["n"] >= 1
    assert result.stopped == "the switch moved" and result.exit_code is None and not result.timed_out
    assert _wait_dead(int(pidfile.read_text())), "the background child survived"


def test_a_cancelled_run_kills_and_reaps_its_group(tmp_path: Path) -> None:
    """[G-9] the bite is cancelled (the session's end) while a command runs."""
    pidfile = tmp_path / "pid"

    async def main() -> None:
        task = asyncio.ensure_future(run(f"sleep 30 & echo $! > {pidfile}; wait", cwd=tmp_path, timeout_s=20))
        for _ in range(100):
            await asyncio.sleep(0.05)
            if pidfile.exists() and pidfile.read_text().strip():
                break
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(main())
    assert _wait_dead(int(pidfile.read_text())), "the background child survived the cancellation"


# --- Review round 3 (R3-1, R3-6, R3-14): each failed on the code before it -----


@pytest.mark.parametrize(
    "command, why",
    [
        # [R3-1] a glob, a type or an ignore file picks hidden and ignored files by name.
        ("rg -g .env SECRET", "by name"),
        ("rg --glob=.env SECRET", "by name"),
        ("rg --iglob .ENV SECRET", "by name"),
        ("rg -ng .env SECRET", "by name"),
        ("rg -t sh SECRET", "by name"),  # the sh type matches .zshenv, .profile...
        ("rg --type-add e:.env -t e SECRET", "by name"),
        ("rg --ignore-file file.txt SECRET", "by name"),  # a `!.env` line un-ignores it
        ("rg -e -- -g .env SECRET", "by name"),
        # [R3-1] transforms the output scrubber cannot see through.
        ("jq -r '.a|@base64' data.json", "scrubber"),
        ("jq -r '@base32' data.json", "scrubber"),
        ("jq -r '@uri' data.json", "scrubber"),
        ("jq -r '@sh' data.json", "scrubber"),
        ("jq -r '.a|tostring|explode' data.json", "scrubber"),
        ("jq -r '.a|format(\"base64\")' data.json", "scrubber"),
        ("rev file.txt", "scrubber"),
        ("cat file.txt | rev", "scrubber"),
        ("tr a-z n-za-m < file.txt", "scrubber"),
        ("cat file.txt | tr a-z n-za-m", "scrubber"),
        ("head file.txt | cut -c1-5 | tr a b", "scrubber"),
    ],
)
def test_selectors_and_scramblers_ask(box: Box, command: str, why: str) -> None:
    verdict = box.verdict(command)
    assert not verdict.safe and why in verdict.reason, (command, verdict.reason)


@pytest.mark.parametrize(
    "command",
    [
        # [T11] a file printed in pieces: characters or bytes...
        "cut -c1-5 file.txt",
        "cut -b 1-5 file.txt",
        "cut --characters=1-5 file.txt",
        "cut -sc1 file.txt",
        "cut -d -- -c1-5 file.txt",  # `--` as -d's value: -c1-5 is still an option
        "cat file.txt | cut -c1-5",
        "head -c 20 file.txt",
        "head -c20 file.txt",
        "tail --bytes=20 file.txt",
        "head -5c file.txt",  # the old byte form
        # ...only the match, or a rewrite of it...
        "grep -o 'sk-[a-z]*' file.txt",
        "grep -noE x file.txt",
        "grep --only-matching x file.txt",
        "rg -o x file.txt",
        "rg -r '$1' 'k(.)' file.txt",
        "rg --replace=x y file.txt",
        # ...or a string cut by jq.
        "jq -r '.a[0:5]' data.json",
        "jq -r '.a[:5]' data.json",
        "jq -r '.a | split(\"\")' data.json",
        "jq -r '.a|sub(\"sk-\";\"\")' data.json",
        "jq -r '.a|ltrimstr(\"sk-\")' data.json",
        "jq -r '.a|ascii_upcase' data.json",
        "jq -r '[.a|scan(\".\")]' data.json",
    ],
)
def test_printing_a_file_in_slices_asks(box: Box, command: str) -> None:
    """[T11] a key printed a few characters at a time, or without its prefix, is
    text the output scrubber can't recognise: a question in normal mode."""
    verdict = box.verdict(command)
    assert not verdict.safe and not verdict.refused and "scrubber" in verdict.reason, (command, verdict.reason)


def test_whole_line_readers_still_pass(box: Box) -> None:
    for command in ["cut -d, -f1 file.txt", "cut -f2 file.txt", "head -n 5 file.txt", "head -5 file.txt",
                    "tail -n 3 file.txt", "grep -n hello file.txt", "grep -c hello file.txt", "rg -n hello nested",
                    "jq '.a' data.json", "jq '[.[] | {a: .b}]' data.json", "jq -r '.format' data.json",
                    "jq '.items | limit(5; .[])' data.json", "jq '.[\"a:b\"]' data.json"]:
        verdict = box.verdict(command)
        assert verdict.safe, (command, verdict.reason)


def test_plain_searches_and_transforms_still_pass(box: Box) -> None:
    for command in ["rg -n hello nested", "rg -T js hello nested", "echo 'a b' | tr a-z A-Z",
                    "echo x | tr x y | tr y z", "jq -r '.format' data.json", "jq -r '.a|@base64d' data.json",
                    "jq -r '.a|@json' data.json"]:
        verdict = box.verdict(command)
        assert verdict.safe, (command, verdict.reason)


@pytest.mark.skipif(shutil.which("rg") is None, reason="needs ripgrep")
def test_rg_selectors_really_reach_hidden_files(tmp_path: Path) -> None:
    """[R3-1] the control: what the selectors do when they DO run."""
    (tmp_path / ".env").write_text("SECRET=1\n")
    (tmp_path / ".zshenv").write_text("export K=SECRET\n")
    (tmp_path / "ign").write_text("!.env\n")
    (tmp_path / "a.txt").write_text("SECRET\n")

    def found(*args: str) -> set[str]:
        out = subprocess.run(["rg", "-l", *args, "SECRET"], cwd=tmp_path, capture_output=True, text=True)
        return set(out.stdout.split())

    assert found() == {"a.txt"}
    assert ".env" in found("-g", ".env") and ".zshenv" in found("-t", "sh")
    assert ".env" in found("--ignore-file", "ign")


def test_a_stop_before_the_launch_starts_nothing(tmp_path: Path) -> None:
    """[R3-6] the watch was first asked a second AFTER the launch: a command that
    finishes in that second ran after the stop."""
    marker = tmp_path / "ran"
    result = asyncio.run(run(f"touch {marker}", cwd=tmp_path, watch=lambda: "the switch moved"))
    assert result.stopped == "the switch moved" and result.exit_code is None
    assert not marker.exists()


def test_the_git_forms_the_daemon_is_told_run_at_once(box: Box) -> None:
    """[R3-14] its instructions said plain `git log` runs at once; the classifier asks.
    The read-only forms run at once, and so does every git form its instructions
    (the job and the researcher's skills) name."""
    from probe.daemon import bite

    named = re.findall(r"`(git [^`]+)`", bite.instructions_for(""))
    forms = ["git log --no-textconv --no-ext-diff", "git diff --no-textconv --no-ext-diff",
             "git show --no-textconv --no-ext-diff", "git blame --no-textconv file.txt", "git status",
             "git branch --show-current", "git rev-parse HEAD", "git ls-files", *named]
    assert "git log" not in named, "plain `git log` asks"
    for form in forms:
        verdict = box.verdict(form)
        assert verdict.safe, (form, verdict.reason)


# --- refused in every mode (bypass included) ---


@pytest.mark.parametrize(
    "command, steps",
    [
        ("cd nested && probe notes create --run R --title T",
         [Step("", "cd nested", cd="nested"),
          Step("&&", "probe notes create --run R --title T", probe_argv=["notes", "create", "--run", "R", "--title",
                                                                         "T"])]),
        ("probe run list | jq .items",
         [Step("", "probe run list | jq .items", probe_argv=["run", "list"], filter="jq .items")]),
        ("probe edge add --source run:a --target run:b --relation x; echo done",
         [Step("", "probe edge add --source run:a --target run:b --relation x",
               probe_argv=["edge", "add", "--source", "run:a", "--target", "run:b", "--relation", "x"]),
          Step(";", "echo done")]),
        ("probe run list 2>&1 | head -3\nprobe run get r1 2>/dev/null || ls",
         [Step("", "probe run list 2>&1 | head -3", probe_argv=["run", "list"], filter="head -3", stderr="merge"),
          Step(";", "probe run get r1 2>/dev/null", probe_argv=["run", "get", "r1"], stderr="drop"),
          Step("||", "ls")]),
        ("probe run list 2>&1", [Step("", "probe run list 2>&1", probe_argv=["run", "list"], stderr="merge")]),
        ("cd 'my folder' && probe artifact add ~/x.csv --project p | cat",
         [Step("", "cd 'my folder'", cd="my folder"),
          Step("&&", "probe artifact add ~/x.csv --project p | cat", probe_argv=["artifact", "add", "HOME/x.csv",
                                                                                "--project", "p"], filter="cat")]),
    ],
)
def test_a_compound_command_with_probe_in_it_becomes_steps(box: Box, command: str, steps: list[Step]) -> None:
    """[T7] several commands per call: the caller runs them one by one, every probe
    command through the probe tool's checks. Bash never sees a probe command."""
    expected = [Step(s.before, s.text, [str(box.home) + a[4:] if a.startswith("HOME/") else a for a in s.probe_argv]
                     if s.probe_argv else None, s.filter, s.stderr, s.cd) for s in steps]
    verdict = box.verdict(command)
    assert not verdict.safe and not verdict.refused and verdict.probe_argv is None
    assert verdict.steps == expected


@pytest.mark.parametrize(
    "command, why",
    [
        ("cat notes.md | probe notes create --run R --title T -", "reads no piped input"),
        ("ls && echo x | probe run list", "reads no piped input"),
        ("probe run list > out.json", "never redirected"),
        ("probe run list >> out.json && ls", "never redirected"),
        ("probe notes create --run R --title T - < notes.md", "never redirected"),
        ("probe run list 1>&2 | head", "never redirected"),
    ],
)
def test_a_probe_command_fed_or_redirected_is_refused_outright(box: Box, command: str, why: str) -> None:
    """A probe command reading piped input or writing a file steps around what its
    checks see: refused in every mode, never held."""
    verdict = box.verdict(command)
    assert not verdict.safe and verdict.refused and why in verdict.reason, verdict.reason


def test_a_single_probe_command_still_goes_to_the_probe_tool(box: Box) -> None:
    verdict = box.verdict("probe run list --limit 3")
    assert verdict.probe_argv == ["run", "list", "--limit", "3"] and not verdict.refused


def test_probes_own_config_is_refused_outright_not_asked(box: Box, monkeypatch) -> None:
    config = box.home / ".config" / "probe"
    config.mkdir(parents=True)
    (config / "config.json").write_text("{}")
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    verdict = box.verdict(f"cat {config / 'config.json'}")
    assert not verdict.safe and verdict.refused
    # A credential-shaped file in a working folder is still a question, not a refusal.
    (box.work / ".env").write_text("X=1\n")
    env_verdict = box.verdict("cat .env")
    assert not env_verdict.safe and not env_verdict.refused


def test_a_probe_the_shell_starts_has_no_key(tmp_path) -> None:
    """Backstop for anything the classifier misses (`timeout 5 probe ...`, a
    script): the shell's environment points Probe at a config that does not exist."""
    env = minimal_env()
    assert env["PROBE_CONFIG_PATH"] and not Path(env["PROBE_CONFIG_PATH"]).exists()
    assert not any(k in env for k in ("PROBE_TOKEN", "PROBE_SERVICE_TOKEN", "PROBE_BASE_URL"))


# --- the every-mode refusals see every part (review of daemon v2 tuning) ------------------------
#
# The checks stop at the first part they would ask about, and bypass mode runs whatever is
# asked: so what no mode may run is looked for in EVERY part first, and in the raw text of a
# command too complex to read word by word. The shell has no Probe key on purpose
# (`minimal_env`), so these are the ways it could reach one.


@pytest.mark.parametrize("command", [
    "env FOO=1 true; cat ~/.config/probe/config.json",
    "sleep 1 | cat ~/.config/probe/config.json",
    'cat "$HOME"/.config/probe/config.json',
    "echo $X; cat ~/.config/probe/config.json",
    "env PROBE_CONFIG_PATH=/elsewhere/config.json probe notes create x",
    "PROBE_CONFIG_PATH=/elsewhere/config.json probe run list",
    "env -u PROBE_CONFIG_PATH probe run list",
    "unset PROBE_CONFIG_PATH; true",
    "export PROBE_SERVICE_TOKEN=x",
    "echo $PROBE_CONFIG_PATH",
    "env -i probe notes create x",
    "env -iv true",
    "echo $(env -i true)",
    "timeout 60 probe run list",
    "env -u FOO probe run list",
    "nohup probe notes create x &",
    "xargs -I{} probe run tag {} x < ids.txt",
    "bash -lc 'probe notes create x'",
    'sh -c "env -i probe run list"',
    "eval probe run list",
    "python3 -c \"import subprocess; subprocess.run(['probe', 'run', 'list'], env={})\"",
    "python3 -c \"import os; os.environ.pop('PROBE_CONFIG_PATH')\"",
    "probe run tag r1 done\ncat > summary.md <<'EOF'\ntouch PWNED\nEOF",
    "cd nested 2>/dev/null && probe artifact add a.txt",
    "cd -P nested && probe run list",
    # Codex's re-review: programs that run their arguments, and a process's own folders.
    """awk 'BEGIN{ system("env -u PROBE_CONFIG_PATH probe run list") }'""",
    """awk 'BEGIN{ system("probe run list") }'""",
    "find . -exec env -u PROBE_CONFIG_PATH probe run list ;",
    "find . -maxdepth 0 -exec probe run list ;",
    "git -c core.pager='probe run list' log -1",
    """HOME=/x bash -c 'unset PROBE_CONFIG_PATH; probe run list; echo "$x"'""",
    "cat /proc/self/cwd/../../../../.config/probe/config.json",
    "cat /proc/1/root/etc/hostname",
])
def test_what_no_mode_runs_is_found_in_every_part(box, command):
    verdict = box.verdict(command, protected=[box.home / ".config" / "probe"])
    assert verdict.refused, (command, verdict.reason)


@pytest.mark.parametrize("command", [
    "grep -rn PROBE_BENCH_FIXTURES .",  # asked (grep -r), never refused: a search for a name
    "rg -n probe src",
    "ls nested",
    "echo $HOME",
    "python3 -c 'print(1)'",
    "env FOO=1 python3 train.py",
    "probe run list",
    "probe notes create --body 'set PROBE_CONFIG_PATH in CI' x",
    "cd nested && probe run list | jq .",
    "cat > notes.md <<'EOF'\nhello\nEOF",
    "python3 train.py --name 'probe sweep'",  # "linear probe" is ordinary ML vocabulary
    "python3 eval.py --task 'linear probe accuracy'",
    "cat /proc/cpuinfo",
    "find . -name probe",
    "rg 'probe run list' docs",
    "echo 'use probe run list'",
])
def test_the_every_mode_refusals_leave_ordinary_commands_alone(box, command):
    assert not box.verdict(command, protected=[box.home / ".config" / "probe"]).refused, command


@pytest.mark.parametrize("command", [
    "cut -d- -f2 file.txt",
    "cut -d_ -f2- file.txt",
    "tail +5c file.txt",
    "head -5c file.txt",
    "jq -r '.token | reverse' data.json",
    "jq -r '.token | explode' data.json",
    "diff -y -W 40 file.txt Cargo.toml",
    "rg -M 30 --max-columns-preview KEY file.txt",
])
def test_more_ways_to_print_a_piece_of_a_key_are_asked(box, command):
    verdict = box.verdict(command)
    assert not verdict.safe and not verdict.refused, (command, verdict.reason)
    assert "scrubber can't recognise" in verdict.reason, (command, verdict.reason)


@pytest.mark.parametrize("command", [
    "cut -d, -f2 file.txt", "cut -f1 file.txt", "tail -n 5 file.txt", "jq '.a | length' data.json",
])
def test_whole_line_reads_still_run_at_once(box, command):
    assert box.safe(command), command
