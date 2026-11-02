"""Find the skills already in a sandbox, such as those of a repository a sandbox hook cloned.

The skills stay where they are: the SDK finds them once the sandbox hooks ran, and the catalog
points at their own ``SKILL.md``. The agent author does not control their content, so a skill that
cannot be served is skipped and logged rather than failing the Session.

One program runs in the sandbox and returns, for each candidate, only what the catalog needs, so
its result stays small in the Workflow history whatever the size of the skills.
"""

from __future__ import annotations

import base64
import codecs
import json
import shlex
from collections.abc import Collection, Sequence
from typing import Protocol

import structlog
from pydantic import Base64Bytes, BaseModel, ConfigDict, ValidationError
from temporalio.exceptions import ApplicationError

from mistralai.vibe.harness.app_server.session import MaterializedSkillDefinition
from mistralai.vibe.harness.runtime.capabilities.skills import SkillSourceFile, local_skill_folder
from mistralai.vibe.harness.runtime.hosts.workflows import workflow_is_replaying
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox import (
    WorkflowSandboxExecuteRequest,
    WorkflowSandboxExecuteResult,
)
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.skills import SandboxWorkspaceSkills

logger = structlog.get_logger(__name__)

MAX_WORKSPACE_SKILLS = 64
"""Every skill found puts its name and description in the system prompt."""
MAX_WORKSPACE_SKILL_CANDIDATES = 256
"""The ``SKILL.md`` files the search reads, valid or not."""
WORKSPACE_SKILL_HEAD_BYTES = 8 * 1024
"""The most the search reads of one ``SKILL.md``, for a file whose frontmatter does not close."""
MAX_WORKSPACE_SKILL_HEADS_BYTES = 512 * 1024
"""The most the search returns in all, so its result stays far under the Temporal payload limit."""
MAX_WORKSPACE_SKILL_FILE_BYTES = 512 * 1024
"""The largest ``SKILL.md`` served: the skill tool later reads it whole, as base64 in one result."""
MAX_WORKSPACE_SKILL_DESCRIPTION_LENGTH = 1024
"""The Agent Skills limit, which the vibe CLI also applies."""
_FIND_WORKSPACE_SKILLS_TIMEOUT_SECONDS = 60
_FIND_WORKSPACE_SKILLS_PROGRAM = """
import base64, json, os, sys

root, dirs = sys.argv[1], json.loads(sys.argv[2])
limit, head_bytes, heads_bytes, file_bytes = map(int, sys.argv[3:7])
root_real = os.path.realpath(root)


def folders(path):
    try:
        with os.scandir(path) as entries:
            return sorted(entry.path for entry in entries if not entry.name.startswith(".") and entry.is_dir())
    except OSError:
        return []


def head(path):
    # The frontmatter and the first body line are all the catalog needs.
    data, state = b"", "start"
    with open(path, "rb") as file:
        while len(data) < head_bytes:
            line = file.readline(head_bytes - len(data))
            if not line:
                break
            data += line
            text = line.strip()
            if state == "start":
                if text != b"---":
                    break  # no frontmatter: the parser refuses the skill anyway
                state = "frontmatter"
            elif state == "frontmatter":
                if text == b"---":
                    state = "body"
            elif text:
                break  # the first body line
    return data


def report(truncated):
    print(json.dumps({"skills": found, "skipped": skipped, "truncated": truncated}))
    sys.exit()


def skip(path, reason):
    if len(skipped) < limit:
        skipped.append({"path": path, "reason": reason})


repositories = [path for path in folders(root) if os.path.exists(os.path.join(path, ".git"))]
found, skipped, seen, total = [], [], set(), 0
for project in [root, *repositories]:
    for skills_dir in dirs:
        for folder in folders(os.path.join(project, skills_dir)):
            entry = os.path.join(folder, "SKILL.md")
            real = os.path.realpath(entry)
            if real in seen or not os.path.isfile(real):
                continue
            seen.add(real)
            if os.path.commonpath([root_real, real]) != root_real:
                skip(entry, "it links outside " + root)
                continue
            try:
                if os.stat(real).st_size > file_bytes:
                    skip(entry, "it is larger than " + str(file_bytes) + " bytes")
                    continue
                if len(found) == limit:
                    report(True)
                data = head(real)
            except OSError as error:
                skip(entry, "it cannot be read: " + error.strerror)
                continue
            total += len(data)
            if total > heads_bytes:
                report(True)
            found.append({"path": entry, "head": base64.b64encode(data).decode("ascii")})
report(False)
"""


class WorkspaceSkillSearchError(ApplicationError):
    """The search for the skills already in the sandbox did not run, or returned an unusable result.

    Raised in Workflow code, it fails the Session: any other error would retry the Workflow task
    forever on the same recorded activity result.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, type=type(self).__name__, non_retryable=True)


class _FoundSkill(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    path: str
    head: Base64Bytes


class _SkippedSkill(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    path: str
    reason: str


class _FoundSkills(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    skills: list[_FoundSkill]
    skipped: list[_SkippedSkill]
    truncated: bool


class SandboxCommandRunner(Protocol):
    @property
    def workspace(self) -> str | None: ...

    async def execute(self, request: WorkflowSandboxExecuteRequest) -> WorkflowSandboxExecuteResult: ...


async def find_workspace_skills(
    sandbox: SandboxCommandRunner,
    sources: Sequence[SandboxWorkspaceSkills],
    *,
    taken: Collection[str] = (),
) -> list[MaterializedSkillDefinition]:
    """Return the catalog of the skills already in the sandbox, skipping any whose name is ``taken``."""

    catalog: list[MaterializedSkillDefinition] = []
    names = set(taken)
    for source in sources:
        root = source.root or sandbox.workspace
        if root is None:
            raise RuntimeError("a sandbox that holds files has a workspace")
        found = await _find_skill_entries(sandbox, root, source.dirs)
        for skipped in found.skipped:
            _skipped_workspace_skill(skipped.path, skipped.reason)
        for skill in found.skills:
            if len(catalog) == MAX_WORKSPACE_SKILLS:
                _skipped_workspace_skill(skill.path, f"only the first {MAX_WORKSPACE_SKILLS} skills are served")
                return catalog
            try:
                entry = _workspace_skill_entry(skill)
            # A frontmatter nested deep enough makes the YAML parser exceed the recursion limit.
            except (ValueError, RecursionError) as error:
                _skipped_workspace_skill(skill.path, str(error) or type(error).__name__)
                continue
            if entry.name in names:
                _skipped_workspace_skill(skill.path, f"the catalog already has a skill named {entry.name!r}")
                continue
            names.add(entry.name)
            catalog.append(entry)
        if found.truncated:
            _skipped_workspace_skill(root, "the search stopped at its limit, so later SKILL.md files were not read")
    return catalog


async def _find_skill_entries(sandbox: SandboxCommandRunner, root: str, dirs: Sequence[str]) -> _FoundSkills:
    result = await sandbox.execute(
        WorkflowSandboxExecuteRequest(
            command=shlex.join(
                [
                    "python3",
                    "-I",
                    "-c",
                    _FIND_WORKSPACE_SKILLS_PROGRAM,
                    root,
                    json.dumps(list(dirs)),
                    str(MAX_WORKSPACE_SKILL_CANDIDATES),
                    str(WORKSPACE_SKILL_HEAD_BYTES),
                    str(MAX_WORKSPACE_SKILL_HEADS_BYTES),
                    str(MAX_WORKSPACE_SKILL_FILE_BYTES),
                ]
            ),
            operation_name="find_workspace_skills",
            arguments={"root": root, "dirs": list(dirs)},
            cwd=sandbox.workspace or root,
            timeout_seconds=_FIND_WORKSPACE_SKILLS_TIMEOUT_SECONDS,
            retry_mode="retry_safe",
        )
    )
    if result.exit_code != 0:
        raise WorkspaceSkillSearchError(
            f"looking for skills under {root} failed with exit code {result.exit_code}: {result.stderr.strip()}"
        )
    try:
        return _FoundSkills.model_validate_json(result.stdout)
    except ValidationError as error:
        raise WorkspaceSkillSearchError(
            f"looking for skills under {root} returned output that is not a list of skills"
        ) from error


def _workspace_skill_entry(found: _FoundSkill) -> MaterializedSkillDefinition:
    head = found.head
    if len(head) == WORKSPACE_SKILL_HEAD_BYTES:
        # The read can stop inside a UTF-8 character; drop only that incomplete character.
        head = codecs.getincrementaldecoder("utf-8")().decode(head, final=False).encode()
    folder = local_skill_folder(
        [SkillSourceFile(path=contracts.SKILL_ENTRY_FILE, content_base64=base64.b64encode(head).decode("ascii"))]
    )
    if len(folder.description) > MAX_WORKSPACE_SKILL_DESCRIPTION_LENGTH:
        raise ValueError(f"its description is longer than {MAX_WORKSPACE_SKILL_DESCRIPTION_LENGTH} characters")
    return MaterializedSkillDefinition(name=folder.name, description=folder.description, path=found.path)


def _skipped_workspace_skill(path: str, reason: str) -> None:
    # Workflow code replays, and the skip was logged the first time.
    if not workflow_is_replaying():
        logger.warning("Skipped a sandbox workspace skill", path=path, reason=reason)


__all__ = [
    "MAX_WORKSPACE_SKILLS",
    "MAX_WORKSPACE_SKILL_CANDIDATES",
    "MAX_WORKSPACE_SKILL_DESCRIPTION_LENGTH",
    "MAX_WORKSPACE_SKILL_FILE_BYTES",
    "MAX_WORKSPACE_SKILL_HEADS_BYTES",
    "WORKSPACE_SKILL_HEAD_BYTES",
    "SandboxCommandRunner",
    "WorkspaceSkillSearchError",
    "find_workspace_skills",
]
