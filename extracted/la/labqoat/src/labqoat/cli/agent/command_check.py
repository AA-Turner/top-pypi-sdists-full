"""Shell commands an agent should not run in a Labqoat project, and what to run instead."""

import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Verdict:
    """A refusal stops the command; a note lets it run and tells the agent how to do better."""

    refused: bool
    reason: str


class CommandCheck:
    """Refuse polling loops and cloud CLIs; note whole-log reads, run-id files, cancels and SDK source reads."""

    lab = re.compile(r"(?:^|[\s;&|(`$])(?:lab|labqoat)\s")
    polling = re.compile(r"\bsleep\s+(?:[5-9]|\d{2,})|\buntil\b|\bseq\s+\d|\bwatch\s+-n\b")
    cloud = re.compile(r"(?:^|[\s;&|(`$])(?:aws|gcloud|kubectl|az)\s")
    whole_log = re.compile(r"\brun\s+logs\b[^|;&]*--all\b")
    filtered = re.compile(r"--grep\b|\|\s*(?:grep|tail|head)\b|\s-n\s+\d")
    id_file = re.compile(r"\brun\b[^;&\n]*(?:>>?|\|\s*tee(?:\s+-a)?)\s*\S+\.(?:txt|tsv|csv|ids|json)\b")
    cancel = re.compile(r"\brun\s+cancel\b")
    source = re.compile(r"site-packages/labqoat\b")
    advice: ClassVar[dict[str, str]] = {
        "polling": (
            "Do not poll Labqoat runs with sleep, until or seq loops: each check costs a whole turn. Block once "
            "with `lab run wait RUN... [--any] --timeout 2h` (one line per run as it ends; exit 3 means still "
            "running), or start the next work and come back."
        ),
        "cloud": (
            "This project reaches compute only through Labqoat: use `lab run placement RUN`, `lab compute quotas`, "
            "`lab compute offerings`, `lab compute usage` and `lab node logs NODE` instead of aws, gcloud, az or "
            "kubectl."
        ),
        "id_file": (
            "Keep runs findable on the platform, not in files: launch them as children of one parent (`lab run "
            "list --owner PARENT`, `lab run compare --owner PARENT`) or tag them (`lab run list --tags T`)."
        ),
        "cancel": (
            "Cancel only a run you started that is wasting money, or one the user named. To change code, launch "
            "the new version beside the running one; repair a failed child with `lab run recover`."
        ),
        "source": (
            "Use `lab GROUP COMMAND --help` and labqoat-runs `reference/sdk.md` (exact signatures and defaults) "
            "instead of reading the SDK's source."
        ),
        "whole_log": (
            "`lab run logs --all` reads a run's whole history into your context. Read `lab run status RUN`, the "
            "last lines with `-n 50`, or matching lines with `--grep TEXT`; metrics with `lab run watch RUN "
            "--metrics 'val/*'`."
        ),
    }

    @classmethod
    def verdict(cls, command: str) -> Verdict | None:
        """What to say about ``command``, or None when it is fine."""
        if cls.cloud.search(command):
            return Verdict(refused=True, reason=cls.advice["cloud"])
        if cls.lab.search(command) and cls.polling.search(command):
            return Verdict(refused=True, reason=cls.advice["polling"])
        if cls.whole_log.search(command) and not cls.filtered.search(command):
            return Verdict(refused=False, reason=cls.advice["whole_log"])
        return cls.note(command)

    @classmethod
    def note(cls, command: str) -> Verdict | None:
        """Advice for commands that are allowed but usually mean the agent is working around a built-in."""
        if cls.source.search(command):
            return Verdict(refused=False, reason=cls.advice["source"])
        if not cls.lab.search(command):
            return None
        for kind in ("id_file", "cancel"):
            if getattr(cls, kind).search(command):
                return Verdict(refused=False, reason=cls.advice[kind])
        return None
