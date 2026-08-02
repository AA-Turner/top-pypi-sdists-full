"""Single shared ``gh`` runner — the one place the package shells out to ``gh``.

Mirror of :mod:`pysae_ai_tools.common.glab.runner` for GitHub. Neutral in
dependencies (never imports a command group) so every layer can consume it. It
never calls ``sys.exit`` nor raises on a ``gh`` failure: :func:`run_gh` always
returns a :class:`GhResult` and :func:`gh_api` returns ``None`` on failure,
leaving the reaction to the caller. Every invocation carries a timeout and
handles a missing binary, so no call can hang. Auth is delegated to ``gh``,
which reads ``GH_TOKEN`` / ``GITHUB_TOKEN`` from the environment.
"""

import json
import subprocess
from dataclasses import dataclass
from typing import Any

GH_MISSING_RC = 127
GH_TIMEOUT_RC = 124


@dataclass
class GhResult:
    """Outcome of a ``gh`` invocation. ``returncode`` is ``127`` when the binary
    is absent and ``124`` on timeout, so a caller can react without a hang or an
    exception ever escaping the runner."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


class GithubApiError(RuntimeError):
    """A ``gh api`` call that failed, carrying the real cause. Raised only by the
    ``check=True`` path (:func:`gh_api`) so a caller can surface the HTTP status
    and GitHub's message — the default path still returns ``None`` silently."""

    def __init__(self, path: str, result: GhResult) -> None:
        self.path = path
        self.returncode = result.returncode
        self.stderr = result.stderr
        detail = result.stderr or "no error output"
        super().__init__(f"gh api {path} failed (rc={result.returncode}): {detail}")


def run_gh(*args: str, timeout: int = 30, stdin_data: str | None = None) -> GhResult:
    """Run ``gh <args>`` and return a :class:`GhResult`.

    Encoding is forced to utf-8 with ``errors="replace"`` so a CLI emitting
    cp1252/cp850 bytes (Windows FR locale) never crashes the reader thread.
    ``stdin`` is closed (``DEVNULL``) unless ``stdin_data`` is provided, so an
    interactive prompt can never block the call.
    """
    try:
        result = subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            input=stdin_data,
            stdin=None if stdin_data is not None else subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return GhResult(GH_MISSING_RC, "", "gh is not installed or not in PATH")
    except subprocess.TimeoutExpired:
        return GhResult(GH_TIMEOUT_RC, "", f"gh timed out after {timeout}s")
    return GhResult(result.returncode, (result.stdout or "").strip(), (result.stderr or "").strip())


def gh_api(
    path: str,
    *extra: str,
    method: str = "",
    input_json: Any | None = None,
    timeout: int = 30,
    check: bool = False,
) -> Any | None:
    """Call ``gh api <path>`` and parse the JSON response, or ``None`` on failure.

    ``method`` maps to ``-X`` (e.g. ``POST``/``PATCH``); ``input_json`` is sent as
    a JSON request body via ``--input -`` (robust for arrays and special
    characters, unlike ``-f key[]=value``); ``extra`` are passed verbatim. Returns
    ``None`` silently on a failed call, empty body, or invalid JSON — callers that
    care about the reason should use :func:`run_gh` directly.

    With ``check=True``, a failed call raises :class:`GithubApiError` (carrying the
    return code and GitHub's ``stderr``) instead of returning ``None`` — use it on
    write paths where a silent ``None`` masks the real cause (permission denied,
    validation error). A successful call with an empty body still returns ``None``
    (e.g. ``204 No Content``); only the *failure* is surfaced.
    """
    args = ["api"]
    if method:
        args += ["-X", method]
    args.append(path)
    args += list(extra)
    stdin_data: str | None = None
    if input_json is not None:
        args += ["--input", "-"]
        stdin_data = json.dumps(input_json)
    res = run_gh(*args, timeout=timeout, stdin_data=stdin_data)
    if not res.ok:
        if check:
            raise GithubApiError(path, res)
        return None
    if not res.stdout:
        return None
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError as err:
        if check:
            raise GithubApiError(path, res) from err
        return None


def gh_graphql(query: str, *, variables: dict[str, str] | None = None, timeout: int = 30) -> Any | None:
    """Run a GraphQL query/mutation via ``gh api graphql`` and parse the response.

    ``variables`` are passed as raw string fields (``-f name=value``), so they
    arrive typed by the query's own ``$name`` declarations — the right shape for
    node IDs, which must not be coerced to numbers. Needed for the operations the
    GitHub REST API cannot express (e.g. ``markPullRequestReadyForReview``).
    Returns ``None`` on failure, like :func:`gh_api`.
    """
    args = ["api", "graphql", "-f", f"query={query}"]
    for name, value in (variables or {}).items():
        args += ["-f", f"{name}={value}"]
    res = run_gh(*args, timeout=timeout)
    if not res.ok or not res.stdout:
        return None
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return None


def gh_api_paginated(endpoint: str, per_page: int = 100, timeout: int = 60) -> list[dict[str, Any]]:
    """Fetch every page of a GitHub API list endpoint via ``gh api --paginate``.

    ``--paginate`` concatenates the per-page JSON arrays into a single array.
    Returns an empty list on any failure.
    """
    sep = "&" if "?" in endpoint else "?"
    res = run_gh("api", "--paginate", f"{endpoint}{sep}per_page={per_page}", timeout=timeout)
    if not res.ok or not res.stdout:
        return []
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []
