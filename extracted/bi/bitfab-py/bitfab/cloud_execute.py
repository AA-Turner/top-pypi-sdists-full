from __future__ import annotations

import base64
import contextlib
import http.client
import json
import os
import re
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid
import zlib
from collections.abc import Iterator
from pathlib import Path
from types import FrameType
from typing import IO, Any
from urllib.parse import urlencode, urlsplit

WORKFLOW = "bitfab-replay.yml"
WORKFLOW_NAMES = (WORKFLOW, "bitfab-replay.yaml")
WORKFLOW_DIRECTORY = ".github/workflows"
PREFIX = "bitfab-replay/"
REPLAY_COMMAND_ENV = "BITFAB_REPLAY_COMMAND"
CHECK_COMMAND_ENV = "BITFAB_REPLAY_CHECK"
EXECUTION_TARGET_ENV = "BITFAB_REPLAY_EXECUTION_TARGET"
HOSTED_EXECUTION_TARGET = "hosted"
API_KEY_ENV = "BITFAB_REPLAY_BITFAB_API_KEY"
PRINT_API_KEY_FLAG = "--print-api-key"
API_KEY_LINE = "@@bitfab:api-key "
KEY_INPUT = "key_id"
KEY_TOKEN_PREFIX = "bfcr_"
DEFAULT_SERVICE_URL = "https://bitfab.ai"
OIDC_AUDIENCE = "bitfab-cloud-replay"
API_KEY_PROBE_SECONDS = 120
REQUEST_VERSION = 4
PLAIN_REQUEST_VERSION = 3
OLDEST_DISPATCHED_VERSION = 2
RESULT_LINE = "bitfab-replay-result "
RESULT_CHUNK = 4000
OUTPUT_BEGIN = "bitfab-replay-output-begin"
OUTPUT_END = "bitfab-replay-output-end"
OUTPUT_LIMIT = 16 * 1024 * 1024
DISK_LIMIT = 1024 * 1024 * 1024
ITEM_ERROR_FIELDS = (
    "error",
    "traceError",
    "trace_error",
    "replayError",
    "replay_error",
)
ITEM_ID_FIELDS = ("originalTraceId", "original_trace_id", "traceId", "trace_id")
ITEM_ERROR_LINES = 20
ITEM_ERROR_LENGTH = 500
SUMMARY_ERROR_ITEMS = 100
EXPERIMENT_FIELDS = {
    "experimentId": ("experimentId", "experiment_id"),
    "experimentUrl": ("experimentUrl", "experiment_url"),
    "testRunId": ("testRunId", "test_run_id"),
    "testRunUrl": ("testRunUrl", "test_run_url"),
    "attempts": ("attempts",),
}
UUID = re.compile(r"^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
ARRAY_INDEX = re.compile(r"0|[1-9][0-9]*")
LONE_SURROGATE = re.compile("[\ud800-\udfff]")
MISSING = object()
CANCELLED = "the GitHub run was cancelled"
EXPERIMENT_LINE = re.compile(rb"^\[replay\] Experiment ([0-9a-f-]{36}):")
PROGRESS_PREFIX = b"@@bitfab:progress "
PROGRESS_PAYLOAD_FIELDS = (
    "input",
    "result",
    "originalOutput",
    "original_output",
    "selectiveReplay",
    "selective_replay",
)
SECRET_REFERENCE = re.compile(
    r"[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?[ \t]*:[ \t]*[\"']?\$\{\{\s*secrets(?:\.([A-Za-z_][A-Za-z0-9_]*)|\[\s*[\"']([A-Za-z_][A-Za-z0-9_]*)[\"']\s*\])\s*\}\}"
)
BRANCH_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*")
ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RESERVED_ENV_PREFIXES = ("GITHUB_", "RUNNER_", "ACTIONS_", "BITFAB_REPLAY_")
SECRET_ENV_NAME = re.compile(
    r"(?:^|_)(?:KEY|SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIALS?)(?:_|$)", re.IGNORECASE
)
ENV_FLAG = "--cloud-env"
URL_PASSWORD = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^/\s:@]*:[^/\s@]+@")
CODE_CHANGE_FLAG = "--code-change"
CODE_CHANGE_BASE_FLAG = "--code-change-base"
BRANCH_CODE_CHANGES = ("last-branch", "default-branch", "ref")
FETCHED_CODE_CHANGES = ("default-branch", "ref")
CHECKOUT_ONLY_CODE_CHANGES = ("working-tree", "last-branch")
GIT_TOKEN_ENV = "BITFAB_REPLAY_GIT_TOKEN"
FETCH_SECONDS = 600
DESCRIBED_REF = re.compile(r"[^\x00-\x1f\x7f]{1,200}")
CODE_CHANGE_PATH_ENV = "BITFAB_CODE_CHANGE_PATH"
CODE_CHANGE_MAX_FILES = 60
CODE_CHANGE_MAX_FILE_BYTES = 500_000
CODE_CHANGE_MAX_TOTAL_BYTES = 2_000_000
DETACHED = "Detached. A GitHub run that already started continues; follow it with --cloud-watch and the printed execution UUID, or stop it with --cloud-cancel and remove its snapshot branch with --cloud-cleanup once it completes"


class CommandError(RuntimeError):
    pass


class KeepMethodOnRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: IO[bytes],
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        if code not in (307, 308):
            return super().redirect_request(req, fp, code, msg, headers, newurl)
        same_host = urlsplit(newurl).netloc == urlsplit(req.full_url).netloc
        kept = {
            name: value
            for name, value in req.header_items()
            if same_host or name.lower() != "authorization"
        }
        return urllib.request.Request(
            newurl, data=req.data, headers=kept, method=req.get_method()
        )

    http_error_308 = urllib.request.HTTPRedirectHandler.http_error_302


REDIRECTING_OPENER = urllib.request.build_opener(KeepMethodOnRedirect)


def js_truthy(value: Any) -> bool:
    if value is None or value is False or value == "":
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value == value and value != 0
    return True


def js_integer(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and value.is_integer()


def compact_json(value: Any) -> str:
    return json.dumps(js_ordered(value), separators=(",", ":"), ensure_ascii=False)


def say(message: str) -> None:
    print(message, flush=True)


def command(
    args: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: float = 60,
    input: str | None = None,
) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        input=input,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        capture_output=True,
        timeout=timeout,
    )
    if result.returncode:
        status = re.search(r"\bHTTP (\d{3})\b", result.stderr or "")
        raise CommandError(
            f"{args[0]} {args[1]} failed (exit {result.returncode}"
            + (f", HTTP {status[1]}" if status else "")
            + "); check authentication and permissions"
        )
    return result.stdout.strip()


def git(root: Path, *args: str, env: dict[str, str] | None = None) -> str:
    return command(["git", "-C", str(root), *args], env=env)


def quiet_git(root: Path, *args: str) -> str:
    try:
        return git(root, *args)
    except CommandError:
        return ""


def root_directory() -> Path:
    return Path(command(["git", "rev-parse", "--show-toplevel"])).resolve()


def relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("Expected a repository-relative path")
    if Path(value).is_absolute() or ".." in Path(value).parts or value.startswith("-"):
        raise ValueError("Paths must stay inside the repository")
    return value


def within(root: Path, value: Any) -> Path:
    path = (root / relative_path(value)).resolve()
    path.relative_to(root)
    return path


def replay_command() -> list[str]:
    configured = os.environ.get(REPLAY_COMMAND_ENV)
    if configured is None:
        return [sys.executable, "-m", "bitfab.replay_cli"]
    try:
        value = json.loads(configured)
    except ValueError:
        value = None
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(part, str) and part for part in value)
    ):
        raise ValueError(
            f"{REPLAY_COMMAND_ENV} must be a JSON list of the command that starts the replay"
        )
    return value


def flag_value(args: list[str], flag: str) -> str | None:
    for index, value in enumerate(args):
        if value.startswith(f"{flag}="):
            return value.partition("=")[2]
        if value == flag and index + 1 < len(args):
            return args[index + 1]
    return None


def replay_name(args: list[str]) -> str | None:
    return flag_value(args, "--name")


def validate_arguments(args: Any) -> None:
    if not isinstance(args, list) or not all(isinstance(value, str) for value in args):
        raise ValueError("Replay arguments must be a list of strings")
    for value in args:
        if "\x00" in value or "\n" in value:
            raise ValueError("Replay options must be single-line values")
        if value.startswith("--cloud"):
            raise ValueError("The runner replays locally and never dispatches again")
    if sum(len(value) for value in args) > 16000:
        raise ValueError("Replay options exceed 16000 characters")


def validate_environment(values: Any) -> None:
    if not isinstance(values, dict) or not all(
        isinstance(name, str) and isinstance(value, str)
        for name, value in values.items()
    ):
        raise ValueError("Replay environment must map names to string values")
    for name, value in values.items():
        if not ENV_NAME.fullmatch(name):
            raise ValueError(
                f"{name!r} is not an environment variable name; use letters, digits, and underscores"
            )
        if name.upper().startswith(RESERVED_ENV_PREFIXES) or name.upper() == "CI":
            raise ValueError(
                f"{name} belongs to GitHub Actions or the cloud runner and cannot be set per replay"
            )
        if SECRET_ENV_NAME.search(name):
            raise ValueError(
                f"{name} looks like a secret, and {ENV_FLAG} values are stored in the snapshot commit on GitHub. Map it in the workflow's replay step env from a GitHub secret instead, then set it with bitfab-replay --cloud-secrets"
            )
        if "\x00" in value or "\n" in value or "\r" in value:
            raise ValueError(f"{name} must be a single-line value")
        if URL_PASSWORD.search(value):
            raise ValueError(
                f"{name} holds a URL with a password, and {ENV_FLAG} values are stored in the snapshot commit on GitHub. Map it in the workflow's replay step env from a GitHub secret instead, then set it with bitfab-replay --cloud-secrets"
            )
    if sum(len(name) + len(value) for name, value in values.items()) > 16000:
        raise ValueError("Replay environment exceeds 16000 characters")


def refuse_git_code_change(replay: list[str], where: str) -> None:
    kind = flag_value(replay, CODE_CHANGE_FLAG)
    if kind in CHECKOUT_ONLY_CODE_CHANGES:
        raise ValueError(
            f"{where} as it is on GitHub, with no snapshot of a checkout, so --code-change {kind} has nothing to compare against there; pass --code-change default-branch, --code-change ref with {CODE_CHANGE_BASE_FLAG}, --code-change skip, or --code-change manual with --code-change-file, or start it with bitfab-replay --cloud and no --cloud-ref, which resolves {kind} from your checkout before upload"
        )
    if kind == "ref" and not BRANCH_NAME.fullmatch(
        flag_value(replay, CODE_CHANGE_BASE_FLAG) or ""
    ):
        raise ValueError(
            f"{where} as it is on GitHub, so --code-change ref needs {CODE_CHANGE_BASE_FLAG} naming a branch or commit SHA on GitHub to fetch there"
        )


def find_workflow(root: Path) -> str | None:
    for name in WORKFLOW_NAMES:
        if within(root, f"{WORKFLOW_DIRECTORY}/{name}").is_file():
            return name
    return None


def running_workflow(root: Path) -> Path:
    reference = os.environ.get("GITHUB_WORKFLOW_REF", "")
    match = re.search(r"(\.github/workflows/[^@]+)@", reference)
    if match:
        return within(root, match[1])
    return within(root, f"{WORKFLOW_DIRECTORY}/{find_workflow(root) or WORKFLOW}")


def workflow_secrets(text: str) -> dict[str, str]:
    return {
        name: dotted or bracketed
        for name, dotted, bracketed in SECRET_REFERENCE.findall(text)
    }


def mapped_secrets(root: Path) -> dict[str, str]:
    path = running_workflow(root)
    return workflow_secrets(path.read_text()) if path.is_file() else {}


def workflow_environment_conflicts(root: Path, values: dict[str, str]) -> None:
    mapped = mapped_secrets(root)
    conflicts = sorted(name for name in values if name in mapped)
    if conflicts:
        raise ValueError(
            f"The workflow already reads {', '.join(conflicts)} from a GitHub secret, so a replay cannot set it; update the secret with bitfab-replay --cloud-secrets"
        )


def check_secrets(root: Path) -> None:
    targets = mapped_secrets(root)
    empty = [name for name in targets if os.environ.get(name) == ""]
    if empty:
        raise ValueError(
            "These replay environment variables are empty on the runner: "
            + ", ".join(f"{name} (secret {targets[name]})" for name in empty)
            + ". GitHub passes a secret that does not exist as an empty string. Create each one under Settings, Secrets and variables, Actions, in the repository or in the job's Environment"
        )
    for name in targets:
        if any(
            0 < len(line.strip()) < 4
            for line in os.environ.get(name, "").splitlines()[1:]
        ):
            say(
                f"::warning title=Bitfab replay::{name} has a line of three characters or fewer, such as a lone brace in multi-line JSON, and GitHub masks that text everywhere in this log. Store it on one line; bitfab-replay --cloud-secrets does this for JSON"
            )


def snapshot_request(root: Path, commit: str) -> dict[str, Any]:
    message = git(root, "log", "-1", "--format=%B", commit)
    _, _, body = message.partition("\n\n")
    try:
        request = json.loads(body)
    except ValueError:
        request = None
    if not isinstance(request, dict) or request.get("version") not in (
        PLAIN_REQUEST_VERSION,
        REQUEST_VERSION,
    ):
        version = request.get("version", 0) if isinstance(request, dict) else 0
        newer = js_integer(version) and version > REQUEST_VERSION
        raise ValueError(
            "This replay was submitted by a "
            + ("newer" if newer else "different")
            + " SDK than the one the snapshot installs; match the SDK you run locally to the one in the lockfile"
        )
    if os.environ.get("GITHUB_REF_NAME") != PREFIX + str(request.get("id")):
        raise ValueError(
            "The runner replays only the snapshot branch its request names; start replays with bitfab-replay --cloud"
        )
    validate_arguments(request.get("args"))
    if "env" in request:
        validate_environment(request["env"])
    return request


def dispatch_event() -> dict[str, Any]:
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path or not Path(path).is_file():
        return {}
    event = json.loads(Path(path).read_text())
    return event if isinstance(event, dict) else {}


def dispatched_inputs() -> dict[str, Any]:
    inputs = dispatch_event().get("inputs")
    return inputs if isinstance(inputs, dict) else {}


def event_default_branch() -> str:
    repository = dispatch_event().get("repository")
    branch = repository.get("default_branch") if isinstance(repository, dict) else None
    if not isinstance(branch, str) or not BRANCH_NAME.fullmatch(branch):
        raise ValueError(
            "The run's event names no default branch, so --code-change default-branch has nothing to compare against; pass --code-change ref with --code-change-base"
        )
    return branch


def decode_request(text: str) -> Any:
    try:
        return json.loads(text)
    except ValueError:
        pass
    try:
        return json.loads(base64.b64decode(text, validate=True))
    except ValueError as error:
        raise ValueError(
            "The request input is neither JSON nor base64-encoded JSON"
        ) from error


def dispatched_request() -> dict[str, Any]:
    branch = os.environ.get("GITHUB_REF_NAME", "")
    inputs = dispatched_inputs()
    supplied = inputs.get("request")
    text = (str(supplied) if js_truthy(supplied) else "").strip()
    if text in ("", "-"):
        raise ValueError(
            f"A replay of {branch} takes its request from the workflow_dispatch request input, and this run has none; start replays with bitfab-replay --cloud, or --cloud --cloud-ref {branch} to replay the branch as it is"
        )
    request = decode_request(text)
    if not isinstance(request, dict):
        raise ValueError("The request input must be a JSON object")
    version = request.get("version", REQUEST_VERSION)
    if not js_integer(version) or version < OLDEST_DISPATCHED_VERSION:
        raise ValueError(
            f"Request version {version!r} is not supported; send version {REQUEST_VERSION}, or leave version out"
        )
    version = int(version)
    if version > REQUEST_VERSION:
        raise ValueError(
            f"This replay was submitted by a newer SDK than the one {branch} installs; the request is version {version} and this SDK reads up to {REQUEST_VERSION}"
        )
    execution_id = next(
        (
            value
            for value in (request.get("id"), inputs.get("execution_id"))
            if js_truthy(value)
        ),
        str(uuid.uuid4()),
    )
    if not isinstance(execution_id, str) or not UUID.fullmatch(execution_id):
        raise ValueError("The request id must be a UUID")
    if js_truthy(inputs.get("execution_id")) and inputs["execution_id"] != execution_id:
        raise ValueError("The request id does not match the execution_id input")
    args = request.get("args")
    validate_arguments(args)
    refuse_git_code_change(args, f"A dispatched replay runs {branch}")
    if request.get("check") is True and "--dry-run" not in args:
        args = [*args, "--dry-run"]
    normalized = {
        "version": REQUEST_VERSION,
        "id": execution_id,
        "cwd": request.get("cwd") if js_truthy(request.get("cwd")) else ".",
        "args": args,
    }
    timeout = request.get("timeoutMinutes")
    if timeout is not None:
        if not js_integer(timeout) or not 1 <= timeout <= 7200:
            raise ValueError("timeoutMinutes must be 1..7200")
        normalized["timeoutMinutes"] = int(timeout)
    if request.get("fullOutput") is True:
        normalized["fullOutput"] = True
    env = request.get("env")
    if js_truthy(env) and not (isinstance(env, dict) and not env):
        validate_environment(env)
        normalized["env"] = env
    return normalized


def runner_request(root: Path, commit: str) -> dict[str, Any]:
    if os.environ.get("GITHUB_REF_NAME", "").startswith(PREFIX):
        return snapshot_request(root, commit)
    return dispatched_request()


def check_out_snapshot_base(root: Path, commit: str, branch: Any) -> str | None:
    try:
        base = git(root, "rev-parse", "--verify", "-q", f"{commit}^")
    except CommandError:
        say(
            "This checkout does not include the commit the snapshot was taken on, so the experiment records no code change and the snapshot commit instead of your branch; set fetch-depth: 2 on the workflow's checkout step, or run bitfab-replay --cloud-update"
        )
        return None
    if isinstance(branch, str) and BRANCH_NAME.fullmatch(branch):
        try:
            git(root, "update-ref", f"refs/heads/{branch}", base)
            git(root, "symbolic-ref", "HEAD", f"refs/heads/{branch}")
            return base
        except CommandError:
            pass
    git(root, "reset", "-q", "--soft", base)
    return base


def git_blob(root: Path, ref: str, path: str) -> str | None:
    try:
        size = int(git(root, "cat-file", "-s", f"{ref}:{path}"))
    except (CommandError, ValueError):
        return None
    if size > CODE_CHANGE_MAX_FILE_BYTES:
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{ref}:{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode or b"\x00" in result.stdout[:8000]:
        return None
    return result.stdout.decode("utf-8", "replace").replace("\r\n", "\n")


def changed_paths(root: Path, base: str, commit: str) -> Iterator[tuple[str, str, str]]:
    raw = git(
        root,
        "diff",
        "--name-status",
        "--find-renames",
        "-z",
        base,
        commit,
        "--",
        ":!.bitfab",
    )
    parts = [part for part in raw.split("\x00") if part]
    index = 0
    while index + 1 < len(parts):
        status, before_path = parts[index][0], parts[index + 1]
        index += 2
        path = before_path
        if status in "RC" and index < len(parts):
            path = parts[index]
            index += 1
        yield status, before_path, path


def snapshot_code_change(
    root: Path,
    base: str,
    commit: str,
    name: str | None,
    against: str = "uncommitted (vs HEAD)",
    subject_ref: str | None = None,
) -> dict[str, Any] | None:
    files, total = [], 0
    for status, before_path, path in changed_paths(root, base, commit):
        if len(files) >= CODE_CHANGE_MAX_FILES:
            break
        before = "" if status == "A" else git_blob(root, base, before_path)
        after = "" if status == "D" else git_blob(root, commit, path)
        if before is None or after is None or before == after:
            continue
        size = len(before.encode()) + len(after.encode())
        if total + size > CODE_CHANGE_MAX_TOTAL_BYTES:
            continue
        total += size
        files.append({"path": path, "before": before, "after": after})
    if not files:
        return None
    head = (name or "").strip() or git(
        root, "log", "-1", "--format=%s", subject_ref or base
    )
    word = "file" if len(files) == 1 else "files"
    return {
        "description": f"{head or 'Working-tree change'} ({len(files)} {word} changed {against})",
        "files": files,
    }


def branch_code_change(
    root: Path, base: str, commit: str, request: dict[str, Any]
) -> dict[str, Any] | None:
    code_change_base = request.get("codeChangeBase")
    if not isinstance(code_change_base, dict):
        return None
    sha, ref = code_change_base.get("sha"), code_change_base.get("ref")
    if not (
        isinstance(sha, str)
        and SHA.fullmatch(sha)
        and isinstance(ref, str)
        and DESCRIBED_REF.fullmatch(ref)
        and (
            sha == base
            or quiet_git(root, "rev-parse", "--verify", "-q", f"{commit}^2") == sha
        )
    ):
        return None
    return snapshot_code_change(
        root, sha, commit, replay_name(request["args"]), f"vs {ref}", base
    )


def runner_code_change(
    root: Path, base: str, commit: str, request: dict[str, Any]
) -> dict[str, Any] | None:
    kind = flag_value(request["args"], CODE_CHANGE_FLAG)
    if kind == "working-tree":
        change = snapshot_code_change(root, base, commit, replay_name(request["args"]))
    elif kind in BRANCH_CODE_CHANGES:
        change = branch_code_change(root, base, commit, request)
    else:
        return None
    return change or {"files": []}


def git_token_environment(token: str | None) -> dict[str, str]:
    environment = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    if not token:
        return environment
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    return {
        **environment,
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
        "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: basic {basic}",
    }


def fetched_base(root: Path, ref: str, token: str | None) -> str:
    shallow = quiet_git(root, "rev-parse", "--is-shallow-repository") == "true"
    try:
        command(
            [
                "git",
                "-C",
                str(root),
                "fetch",
                "-q",
                "--no-tags",
                *(["--unshallow"] if shallow else []),
                "origin",
                ref,
            ],
            env=git_token_environment(token),
            timeout=FETCH_SECONDS,
        )
    except (CommandError, subprocess.TimeoutExpired) as error:
        hint = (
            "check that it exists on GitHub"
            if token
            else f"the workflow passes no {GIT_TOKEN_ENV} to fetch it with, so run bitfab-replay --cloud-update and commit the workflow it updates"
        )
        raise ValueError(
            f"Could not fetch {ref} from origin to compare against ({error}); {hint}, or pass --code-change skip"
        ) from None
    base = quiet_git(root, "merge-base", "HEAD", "FETCH_HEAD")
    if not base:
        raise ValueError(
            f"This branch shares no history with {ref}, so there is nothing to compare against"
        )
    return base


def dispatched_code_change(
    root: Path, commit: str, request: dict[str, Any], token: str | None
) -> dict[str, Any] | None:
    args = request["args"]
    kind = flag_value(args, CODE_CHANGE_FLAG)
    if kind not in FETCHED_CODE_CHANGES:
        return None
    ref = (
        flag_value(args, CODE_CHANGE_BASE_FLAG)
        if kind == "ref"
        else event_default_branch()
    )
    say(f"Fetching {ref} to record the code change against it")
    base = fetched_base(root, ref, token)
    change = snapshot_code_change(
        root, base, commit, replay_name(args), f"vs {ref}", commit
    )
    return change or {"files": []}


def write_code_change(change: dict[str, Any]) -> str:
    handle, path = tempfile.mkstemp(
        prefix="bitfab-code-change-",
        suffix=".json",
        dir=os.environ.get("RUNNER_TEMP") or None,
    )
    with os.fdopen(handle, "w") as out:
        json.dump(change, out)
    return path


def runner_warning(message: str) -> None:
    say(f"::warning title=Bitfab replay::{message}")


def warn_if_workflow_outdated() -> None:
    problems = []
    if API_KEY_ENV in os.environ:
        problems.append(
            f"still sets {API_KEY_ENV} from a secret named by the run's inputs, which makes GitHub give this run every secret in the repository"
        )
    if not os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL"):
        problems.append(
            "does not grant id-token: write, so replays use the workflow's BITFAB_API_KEY secret instead of running as the person who started them"
        )
    if problems:
        runner_warning(
            f"This workflow {' and '.join(problems)}. Run bitfab-replay --cloud-update and commit the workflow it updates"
        )


def local_client(root: Path, request: dict[str, Any]) -> dict[str, str] | None:
    try:
        output = command(
            [*replay_command(), *request["args"], PRINT_API_KEY_FLAG],
            cwd=within(root, request["cwd"]),
            timeout=API_KEY_PROBE_SECONDS,
            input="",
        )
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError):
        return None
    for line in reversed(output.splitlines()):
        if not line.startswith(API_KEY_LINE):
            continue
        try:
            reported = json.loads(line.removeprefix(API_KEY_LINE))
        except ValueError:
            return None
        if not isinstance(reported, dict):
            return None
        key = reported.get("apiKey")
        if not isinstance(key, str) or not key.strip():
            return None
        url = reported.get("serviceUrl")
        if not isinstance(url, str) or not url.strip():
            url = DEFAULT_SERVICE_URL
        return {"apiKey": key, "serviceUrl": url.rstrip("/")}
    return None


def bitfab_api(
    client: dict[str, str],
    path: str,
    *,
    method: str = "POST",
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None if payload is None else json.dumps(payload).encode()
    try:
        request = urllib.request.Request(
            f"{client['serviceUrl']}/api/sdk/{path}",
            method=method,
            data=data,
            headers={
                **(
                    {"Authorization": f"Bearer {client['apiKey']}"}
                    if client.get("apiKey")
                    else {}
                ),
                "User-Agent": "bitfab-cloud-replay",
                **({"Content-Type": "application/json"} if data is not None else {}),
            },
        )
        with REDIRECTING_OPENER.open(request, timeout=60) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        try:
            reason = json.loads(error.read()).get("error")
        except (ValueError, AttributeError, OSError):
            reason = None
        raise CommandError(
            f"Bitfab {method} {path} failed (HTTP {error.code})"
            + (f": {reason}" if reason else "")
        ) from None
    except (
        urllib.error.URLError,
        OSError,
        ValueError,
        http.client.HTTPException,
    ) as error:
        raise CommandError(
            f"Could not reach {client['serviceUrl']}: {getattr(error, 'reason', error)}"
        ) from None
    try:
        return json.loads(body) if body.strip() else {}
    except ValueError:
        raise CommandError(
            f"Bitfab {method} {path} returned a response that is not JSON"
        ) from None


def github_run_identity() -> str:
    url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    bearer = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    if not url or not bearer:
        raise CommandError(
            "The workflow does not grant id-token: write, so this run cannot prove to Bitfab which run it is; run bitfab-replay --cloud-update to add it"
        )
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}{urlencode({'audience': OIDC_AUDIENCE})}",
        headers={
            "Authorization": f"Bearer {bearer}",
            "User-Agent": "bitfab-cloud-replay",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            value = json.loads(response.read()).get("value")
    except urllib.error.HTTPError as error:
        raise CommandError(
            f"GitHub did not issue this run's OIDC token: HTTP Error {error.code}"
        ) from None
    except (
        urllib.error.URLError,
        OSError,
        ValueError,
        AttributeError,
        http.client.HTTPException,
    ) as error:
        raise CommandError(
            f"GitHub did not issue this run's OIDC token: {getattr(error, 'reason', error)}"
        ) from None
    if not isinstance(value, str) or not value:
        raise CommandError("GitHub returned no OIDC token for this run")
    return value


def starter_key(root: Path, request: dict[str, Any]) -> dict[str, str] | None:
    warn_if_workflow_outdated()
    if os.environ.get(API_KEY_ENV, "").strip():
        say("Replaying with the Bitfab API key of the person who started this run")
        return None
    token = str(dispatched_inputs().get(KEY_INPUT) or "").strip()
    if not token.startswith(KEY_TOKEN_PREFIX):
        return None
    shared = "so this run uses the workflow's BITFAB_API_KEY secret"
    runner = local_client(root, request)
    if runner is None:
        runner_warning(
            f"The replay's Bitfab client resolved no API key on the runner, {shared}"
        )
        return None
    try:
        identity = github_run_identity()
    except CommandError as error:
        runner_warning(f"{error}, {shared}")
        return None
    timeout = request.get("timeoutMinutes")
    try:
        redeemed = bitfab_api(
            {"serviceUrl": runner["serviceUrl"]},
            "replay/cloudKey/redeem",
            payload={
                "token": token,
                "oidcToken": identity,
                **({"minutes": timeout} if timeout else {}),
            },
        )
    except CommandError as error:
        runner_warning(f"{error}, {shared}")
        return None
    key = redeemed.get("apiKey") if isinstance(redeemed, dict) else None
    if not isinstance(key, str) or not key.strip():
        runner_warning(f"Bitfab returned no key for the replay token, {shared}")
        return None
    say(f"::add-mask::{key}")
    os.environ[API_KEY_ENV] = key
    say(
        "Replaying as the person who started this run, with a key that is turned off when the replay ends"
    )
    return {"apiKey": key, "serviceUrl": runner["serviceUrl"]}


def revoke_starter_key(starter: dict[str, str] | None) -> None:
    if starter is None:
        return
    try:
        bitfab_api(starter, "replay/cloudKey", method="DELETE")
    except CommandError as error:
        runner_warning(
            f"Could not turn off this replay's key ({error}); it expires on its own 30 minutes after the replay's timeout"
        )


def run_check_command(directory: Path, environment: dict[str, str]) -> None:
    check = os.environ.get(CHECK_COMMAND_ENV, "").strip()
    if not check:
        return
    say(f"Running {CHECK_COMMAND_ENV}: {check}")
    code = subprocess.run(
        shlex.split(check),
        cwd=directory,
        env={**os.environ, **environment},
        stdin=subprocess.DEVNULL,
        check=False,
    ).returncode
    if code:
        raise ValueError(f"{CHECK_COMMAND_ENV} exited {code}; its output is above")


def item_errored(item: Any) -> bool:
    return isinstance(item, dict) and any(
        item.get(field) is not None for field in ITEM_ERROR_FIELDS
    )


def carried_over(item: Any) -> bool:
    return isinstance(item, dict) and (
        item.get("carriedOver") is True or item.get("carried_over") is True
    )


def item_errors(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    errors = []
    for item in items:
        if not item_errored(item):
            continue
        error = next(
            item[field] for field in ITEM_ERROR_FIELDS if item.get(field) is not None
        )
        if isinstance(error, dict):
            message = error.get("message")
            error = message if js_truthy(message) else json.dumps(error)
        trace = next(
            (
                item[field]
                for field in ITEM_ID_FIELDS
                if isinstance(item.get(field), str)
            ),
            "unknown trace",
        )
        text = " ".join(python_text(error).split())
        if len(text) > ITEM_ERROR_LENGTH:
            text = text[:ITEM_ERROR_LENGTH] + "..."
        errored = {"originalTraceId": trace, "error": text}
        if js_integer(item.get("attempt")):
            errored["attempt"] = int(item["attempt"])
        errors.append(errored)
    return errors


def python_text(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, str):
        return value
    return json.dumps(value)


def item_field(item: dict[str, Any], camel: str, snake: str) -> Any:
    return item[camel] if camel in item else item.get(snake)


def js_ordered(value: Any) -> Any:
    if isinstance(value, dict):
        indexes = sorted(
            (
                key
                for key in value
                if ARRAY_INDEX.fullmatch(key) and int(key) < 2**32 - 1
            ),
            key=int,
        )
        named = [key for key in value if key not in set(indexes)]
        return {key: js_ordered(value[key]) for key in [*indexes, *named]}
    if isinstance(value, list):
        return [js_ordered(item) for item in value]
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            return None
        if value.is_integer():
            return int(value)
    return value


def canonical(value: Any) -> str:
    return json.dumps(js_ordered(value), separators=(",", ":"), ensure_ascii=False)


def experiment_fields(parsed: dict[str, Any]) -> dict[str, Any]:
    fields = {}
    for name, spellings in EXPERIMENT_FIELDS.items():
        value = next(
            (parsed[key] for key in spellings if parsed.get(key) is not None), None
        )
        if value is not None:
            fields[name] = value
    return fields


def replay_summary(parsed: dict[str, Any]) -> dict[str, Any]:
    items = [item for item in parsed["items"] if isinstance(item, dict)]
    replayed = [item for item in items if not carried_over(item)]
    errors = item_errors(replayed)
    counts = {
        "replayed": len(replayed),
        "carriedOver": len(items) - len(replayed),
        "same": 0,
        "changed": 0,
        "matchedExpected": 0,
        "missedExpected": 0,
        "errored": len(errors),
    }
    for item in replayed:
        if item_errored(item):
            continue
        equal = canonical(item.get("result")) == canonical(
            item_field(item, "originalOutput", "original_output")
        )
        if item_field(item, "ingestionType", "ingestion_type") == "seeded":
            counts["matchedExpected" if equal else "missedExpected"] += 1
        else:
            counts["same" if equal else "changed"] += 1
    summary = {
        "cloudSummary": True,
        **experiment_fields(parsed),
        "counts": counts,
        "erroredItems": errors[:SUMMARY_ERROR_ITEMS],
    }
    if len(errors) > SUMMARY_ERROR_ITEMS:
        summary["erroredItemsOmitted"] = len(errors) - SUMMARY_ERROR_ITEMS
    return summary


def trailing_json(text: str) -> tuple[int | None, dict[str, Any] | None]:
    decoder = json.JSONDecoder()
    for offset in [0, *[i + 1 for i, value in enumerate(text) if value == "\n"]]:
        if text.startswith("{", offset):
            try:
                value, end = decoder.raw_decode(text, offset)
            except json.JSONDecodeError:
                continue
            if not text[end:].strip() and isinstance(value, dict):
                return offset, value
    return None, None


def last_json(text: str) -> dict[str, Any] | None:
    return trailing_json(text)[1]


def result_summary(stdout: str) -> dict[str, Any] | None:
    parsed = last_json(stdout) or {}
    if parsed.get("cloudSummary") is True:
        return parsed
    if isinstance(parsed.get("items"), list):
        return replay_summary(parsed)
    return None


def without_item_payload(line: bytes) -> bytes:
    try:
        event = json.loads(line[len(PROGRESS_PREFIX) :])
    except ValueError:
        return line
    item = event.get("item") if isinstance(event, dict) else None
    if not isinstance(item, dict):
        return line
    event["item"] = {
        key: value for key, value in item.items() if key not in PROGRESS_PAYLOAD_FIELDS
    }
    return (
        PROGRESS_PREFIX
        + compact_json(event).encode("utf-8", "backslashreplace")
        + b"\n"
    )


def forward_stderr(
    stream: IO[bytes], experiment: dict[str, str], summarize: bool
) -> None:
    for line in iter(stream.readline, b""):
        if summarize and line.startswith(PROGRESS_PREFIX):
            with contextlib.suppress(Exception):
                line = without_item_payload(line)
        sys.stdout.write(line.decode(errors="replace"))
        sys.stdout.flush()
        if "id" not in experiment:
            match = EXPERIMENT_LINE.match(line)
            if match:
                experiment["id"] = match[1].decode()


def relayed_stdout(output: IO[bytes], code: int, summarize: bool) -> tuple[str, int]:
    if summarize:
        output.seek(0)
        parsed = last_json(output.read().decode(errors="replace"))
        if isinstance(parsed, dict) and isinstance(parsed.get("items"), list):
            return compact_json({**replay_summary(parsed), "exitCode": code}) + "\n", 0
    return carried_stdout(output)


def carried_stdout(output: IO[bytes]) -> tuple[str, int]:
    start = max(0, os.fstat(output.fileno()).st_size - OUTPUT_LIMIT)
    output.seek(start)
    text = output.read().decode(errors="replace")
    if not start:
        return text, 0
    offset = trailing_json(text)[0] or 0
    return text[offset:], start + len(text[:offset].encode())


def js_text(value: Any) -> str:
    if value is MISSING:
        return "undefined"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, dict):
        return "[object Object]"
    if isinstance(value, list):
        return ",".join("" if item is None else js_text(item) for item in value)
    return str(value)


def js_field(value: Any, key: str) -> Any:
    return value.get(key, MISSING) if isinstance(value, dict) else MISSING


def js_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip() or "0")
        except ValueError:
            return None
    return None


def summary_markdown(result: dict[str, Any]) -> str:
    summary = result_summary(result["stdout"]) or {}
    counts = summary.get("counts")
    counts = counts if isinstance(counts, dict) else {}
    test_run = result.get("testRunId") or summary.get("testRunId")
    errors = summary.get("erroredItems")
    errors = errors if isinstance(errors, list) else []
    lines = [f"Commit: `{result['commitSha']}`", f"Exit code: {result['exitCode']}"]
    if test_run:
        lines.insert(0, f"Test run: `{test_run}`")
    if result.get("stoppedEarly"):
        lines.append(f"Stopped early: {result['stoppedEarly']}")
    elif js_truthy(counts.get("replayed")) or js_truthy(counts.get("carriedOver")):
        lines.append(
            "Replayed: {}, same: {}, changed: {}, errored: {}".format(
                *(
                    js_text(js_field(counts, key))
                    for key in ("replayed", "same", "changed", "errored")
                )
            )
        )
    text = "### Bitfab replay\n\n" + "\n\n".join(lines) + "\n"
    if errors:
        shown = [
            f"trace {js_text(js_field(error, 'originalTraceId'))}: {js_text(js_field(error, 'error'))}"
            for error in errors[:ITEM_ERROR_LINES]
        ]
        errored = js_number(counts.get("errored")) or 0
        if errored > len(shown):
            shown.append(f"and {js_text(errored - len(shown))} more errored items")
        text += "\n#### Errored items\n\n" + "".join(
            f"- `{line.replace('`', chr(39))}`\n" for line in shown
        )
    return text


def write_result(result: dict[str, Any]) -> None:
    encoded = base64.b64encode(zlib.compress(json.dumps(result).encode())).decode()
    for start in range(0, len(encoded), RESULT_CHUNK):
        print(RESULT_LINE + encoded[start : start + RESULT_CHUNK])
    sys.stdout.flush()
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as file:
            file.write(LONE_SURROGATE.sub("\ufffd", summary_markdown(result)))


def annotate(result: dict[str, Any]) -> None:
    if result.get("stoppedEarly"):
        message = f"Replay stopped early: {result['stoppedEarly']}"
    elif result["exitCode"]:
        message = f"Replay exited {result['exitCode']}, so this job exits with it too"
    else:
        return
    runner_warning(message)


def runner_exit_code(result: dict[str, Any]) -> int:
    if result.get("stoppedEarly"):
        return result["exitCode"] or 1
    return result["exitCode"]


def raise_interrupt(signum: int, frame: FrameType | None) -> None:
    raise KeyboardInterrupt


def stop(child: subprocess.Popen[bytes]) -> None:
    with contextlib.suppress(ProcessLookupError):
        os.killpg(child.pid, signal.SIGTERM)
    with contextlib.suppress(subprocess.TimeoutExpired):
        child.wait(timeout=30)
    with contextlib.suppress(ProcessLookupError):
        os.killpg(child.pid, signal.SIGKILL)
    child.wait()


def run_command(
    directory: Path,
    args: list[str],
    timeout: float | None,
    experiment: dict[str, str],
    *,
    summarize: bool,
    environment: dict[str, str],
) -> tuple[int, str, int, str | None]:
    stopped = None
    with tempfile.TemporaryFile() as output:
        with subprocess.Popen(
            args,
            cwd=directory,
            env={
                **os.environ,
                **environment,
                EXECUTION_TARGET_ENV: HOSTED_EXECUTION_TARGET,
            },
            stdout=output,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        ) as child:
            reader = threading.Thread(
                target=forward_stderr,
                args=(child.stderr, experiment, summarize),
                daemon=True,
            )
            reader.start()
            try:
                minutes = None if timeout is None else js_number(timeout)
                deadline = None if minutes is None else time.monotonic() + minutes * 60
                parent = os.getppid()
                checked = time.monotonic()
                while child.poll() is None:
                    if os.fstat(output.fileno()).st_size > DISK_LIMIT:
                        raise ValueError("Replay printed more than 1 GiB to stdout")
                    if deadline is not None and time.monotonic() >= deadline:
                        stopped = (
                            f"it reached the {js_text(timeout)}-minute --cloud-timeout"
                        )
                        stop(child)
                        break
                    if time.monotonic() - checked >= 1:
                        checked = time.monotonic()
                        if os.getppid() != parent:
                            raise KeyboardInterrupt
                    time.sleep(0.1)
            except KeyboardInterrupt:
                for number in (signal.SIGINT, signal.SIGTERM):
                    signal.signal(number, signal.SIG_IGN)
                stopped = CANCELLED
                stop(child)
            except BaseException:
                stop(child)
                raise
            finally:
                with contextlib.suppress(ProcessLookupError, PermissionError):
                    os.killpg(child.pid, signal.SIGKILL)
                reader.join(timeout=5)
            code = child.returncode if child.returncode >= 0 else 1
        text, omitted = relayed_stdout(output, code, summarize)
    return code, text, omitted, stopped


def execute() -> dict[str, Any]:
    if os.environ.get("GITHUB_RUN_ATTEMPT") != "1":
        raise ValueError("Submit a new replay instead of rerunning an Actions job")
    git_token = os.environ.pop(GIT_TOKEN_ENV, None)
    root = root_directory()
    commit = os.environ.get("GITHUB_SHA")
    if commit is None:
        raise ValueError("'GITHUB_SHA'")
    if git(root, "rev-parse", "HEAD") != commit:
        raise ValueError("Runner checkout does not match the dispatched commit")
    request = runner_request(root, commit)
    snapshot = os.environ.get("GITHUB_REF_NAME", "").startswith(PREFIX)
    base = (
        check_out_snapshot_base(root, commit, request.get("branch"))
        if snapshot
        else None
    )
    directory = within(root, request.get("cwd"))
    check_secrets(root)
    environment = request.get("env") or {}
    if environment:
        workflow_environment_conflicts(root, environment)
        say(f"Setting {', '.join(sorted(environment))} from the request")
    if snapshot:
        change = (
            None if base is None else runner_code_change(root, base, commit, request)
        )
    else:
        change = dispatched_code_change(root, commit, request, git_token)
    run_environment = dict(environment)
    if change is not None:
        run_environment[CODE_CHANGE_PATH_ENV] = write_code_change(change)
    args = [*replay_command(), *request["args"]]
    if "--dry-run" in request["args"]:
        run_check_command(directory, environment)
    experiment = {}
    starter = starter_key(root, request)
    previous = signal.signal(signal.SIGTERM, raise_interrupt)
    say(OUTPUT_BEGIN)
    try:
        code, stdout, omitted, stopped = run_command(
            directory,
            args,
            request.get("timeoutMinutes"),
            experiment,
            summarize=request.get("fullOutput") is not True,
            environment=run_environment,
        )
    finally:
        say(OUTPUT_END)
        if signal.getsignal(signal.SIGTERM) is raise_interrupt:
            signal.signal(signal.SIGTERM, previous)
        revoke_starter_key(starter)
    result = {
        "executionId": request["id"],
        "commitSha": commit,
        "exitCode": code,
        "stdout": stdout,
    }
    if omitted:
        result["stdoutOmittedBytes"] = omitted
    if stopped:
        result["stoppedEarly"] = stopped
        if UUID.fullmatch(experiment.get("id", "")):
            result["testRunId"] = experiment["id"]
    write_result(result)
    return result


def main() -> int:
    try:
        result = execute()
        annotate(result)
        return runner_exit_code(result)
    except KeyboardInterrupt:
        print(f"[cloud] {DETACHED}", file=sys.stderr, flush=True)
        return 130
    except (
        ValueError,
        RuntimeError,
        OSError,
        subprocess.SubprocessError,
        KeyError,
    ) as error:
        sys.stdout.flush()
        print(f"Cloud replay: {error}", file=sys.stderr, flush=True)
        return 1
