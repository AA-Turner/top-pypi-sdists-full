"""Run a full release for the current repository.

Ports the logic from the shell ``release.sh`` scripts (api, op, driver) into
a single reusable command. Steps:

1. Setup GPG signing if ``RELEASE_GPG_PRIVATE_KEY`` is set (CI only).
2. Validate ``TAG`` is strict semver (``vMAJOR.MINOR.PATCH``).
3. Validate the current branch is ``main``, ``develop`` or matches a
   ``support/*`` / ``release/*`` pattern.
4. In CI detached-HEAD mode, re-checkout the ref to a real branch so that
   ``git commit`` / ``git push`` work.
5. Check the working tree is clean (tracked files only).
6. Pull from remote (skipped in CI — the runner already has the latest ref).
7. Check the tag does not already exist.
8. Merge ``changelogs/*.md`` into ``CHANGELOG.md`` (delegated to
   ``pysae_ai_tools.code.changelog.release``).
9. Run all executable scripts under ``release.d/`` in alphabetical order.
   Each script gets the tag as ``argv[1]`` and ``$RELEASE_TAG`` in the env.
   This is how per-project steps (e.g. ``yarn run version``) are plugged in.
10. ``git add --all``, commit ``release: TAG``, create an annotated tag with
    the changelog section as body, then ``git push --follow-tags``.

Usage:
    pysae-ai-tools ci release run vMAJOR.MINOR.PATCH [--yes]
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Annotated

import typer

from ...code.changelog import release as merge_changelog_release
from ...code.release_content import gitlab_release_description
from ...code.versioning import tag_base
from ...common.project_config import effective_config
from .verify import verify_release

SEMVER_RE = re.compile(r"^v\d+\.\d+\.\d+(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?$")


def _info(msg: str) -> None:
    typer.echo(f" * {msg}")


def _check(msg: str) -> None:
    _info(f"[check] {msg}...")


def _error(msg: str, *, code: int = 1) -> None:
    typer.secho(f"ERROR: {msg}", fg=typer.colors.RED, err=True)
    raise typer.Exit(code=code)


def _run(
    cmd: list[str],
    *,
    check: bool = True,
    capture: bool = True,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    res = subprocess.run(
        cmd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=capture,
        cwd=str(cwd) if cwd else None,
        env=env,
    )
    if check and res.returncode != 0:
        if capture and res.stderr:
            sys.stderr.write(res.stderr)
        _error(f"command failed ({' '.join(cmd)})")
    return res


def _git(*args: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return _run(["git", *args], check=check, capture=capture)


def _action(msg: str, *, auto: bool) -> None:
    if auto:
        typer.echo(f" * [action] {msg} (auto-confirmed)")
        return
    ans = typer.prompt(f" * [action] {msg} (Y/n)", default="Y", show_default=False)
    if ans and ans.strip().lower() == "n":
        _error("Canceled")


def _setup_gpg() -> None:
    key = os.environ.get("RELEASE_GPG_PRIVATE_KEY")
    if not key:
        return
    _info("Setting up GPG signing...")
    for tool in ("gpg", "gpg-agent"):
        if _run(["which", tool], check=False).returncode != 0:
            _error(f"{tool} is required but not installed")
    _run(["gpg", "--batch", "--import", key])
    res = _run(["gpg", "--list-secret-keys", "--keyid-format", "long"], check=False)
    key_id = ""
    for line in res.stdout.splitlines():
        if line.startswith("sec"):
            m = re.search(r"/([0-9A-Fa-f]+)", line)
            if m:
                key_id = m.group(1)
                break
    if not key_id:
        _error("GPG key import failed")
    _git("config", "commit.gpgsign", "true")
    _git("config", "tag.gpgsign", "true")
    _git("config", "user.signingkey", key_id)
    _info(f"GPG signing configured with key {key_id}")


def _current_branch() -> str:
    ref = os.environ.get("CI_COMMIT_REF_NAME")
    if ref:
        return ref
    return _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def _branch_allowed(
    branch: str,
    main: str,
    develop: str,
    support_prefix: str,
    release_prefix: str,
) -> bool:
    return branch == main or branch == develop or branch.startswith(support_prefix) or branch.startswith(release_prefix)


def _run_release_d(root: Path, tag: str, auto: bool) -> list[Path]:
    """Execute scripts under ``release.d/`` in alphabetical order.

    Only executable regular files are run. Each receives the tag as
    ``argv[1]`` and ``$RELEASE_TAG`` in its environment.

    Returns the list of scripts that were run.
    """
    d = root / "release.d"
    if not d.is_dir():
        return []
    scripts = sorted(p for p in d.iterdir() if p.is_file() and os.access(p, os.X_OK))
    if not scripts:
        return []
    env = dict(os.environ)
    env["RELEASE_TAG"] = tag
    for script in scripts:
        _action(f"run release.d/{script.name} {tag}", auto=auto)
        res = subprocess.run([str(script), tag], env=env, cwd=str(root))
        if res.returncode != 0:
            _error(f"release.d/{script.name} failed (exit {res.returncode})")
    return scripts


def release(
    tag: str,
    *,
    root: Path,
    yes: bool = False,
    main_branch: str = "main",
    develop_branch: str = "develop",
    support_prefix: str = "support/",
    release_prefix: str = "release/",
    check_release_notes: bool = True,
) -> None:
    """Run the full release flow in ``root``.

    Raises ``typer.Exit`` on any validation failure.
    """
    auto = yes or os.environ.get("CI") is not None or os.environ.get("RELEASE_YES") == "1"

    previous_cwd = Path.cwd()
    os.chdir(root)
    try:
        _release_impl(
            tag,
            root=root,
            auto=auto,
            main_branch=main_branch,
            develop_branch=develop_branch,
            support_prefix=support_prefix,
            release_prefix=release_prefix,
            check_release_notes=check_release_notes,
        )
    finally:
        os.chdir(previous_cwd)


def _release_impl(
    tag: str,
    *,
    root: Path,
    auto: bool,
    main_branch: str,
    develop_branch: str,
    support_prefix: str,
    release_prefix: str,
    check_release_notes: bool,
) -> None:
    _setup_gpg()

    _check("tag is valid semver")
    if not SEMVER_RE.match(tag):
        _error(f"Invalid tag: {tag}. It must start with 'v' and be valid semver")

    # Prereleases (e.g. v6.0.0-beta.1) require an explicit opt-in per repo.
    if tag_base(tag) != tag and not effective_config(root).release.allow_prerelease:
        _error(
            f"{tag} is a prerelease but release.allow_prerelease is false for this repo. "
            "Enable the flag in .pysae-ai-tools.yaml to allow prereleases."
        )

    _check(f"current branch is {main_branch} or {develop_branch}")
    branch = _current_branch()

    if os.environ.get("CI") and _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "HEAD":
        _info(f"CI detached HEAD detected, checking out {branch}")
        _git("checkout", "-B", branch)
        _git("branch", "--set-upstream-to", f"origin/{branch}", branch)

    if not _branch_allowed(branch, main_branch, develop_branch, support_prefix, release_prefix):
        _error(
            f"release must be done on {main_branch}, {develop_branch}, "
            f"{support_prefix}* or {release_prefix}* branch"
        )

    _check("working directory is clean")
    if _git("status", "--porcelain", "--untracked-files=no").stdout.strip():
        _error("your working directory must be clean for release")

    _action("pull from remote", auto=auto)
    if not os.environ.get("CI"):
        _git("pull")

    _check("tag does not exist")
    if tag in _git("tag").stdout.splitlines():
        _error(f"{tag} already exists")

    new_content, section_raw, consumed = merge_changelog_release(tag=tag, repo_root=root)
    typer.echo(section_raw)

    _action("merge changelogs to CHANGELOG.md", auto=auto)
    (root / "CHANGELOG.md").write_text(new_content, encoding="utf-8")
    for path in consumed:
        path.unlink()

    # Verify the release is complete BEFORE the tag is created — a failure here
    # aborts the job (non-zero exit) so no incomplete release ever gets tagged.
    _check("release is complete (changelog + release notes)")
    problems = [c for c in verify_release(root, tag, check_release_notes=check_release_notes) if not c.ok]
    if problems:
        _error("release verification failed:\n" + "\n".join(f"  - {c.name}: {c.detail}" for c in problems))

    _run_release_d(root, tag, auto=auto)

    _action("commit changes and create tag", auto=auto)
    _git("add", "--all")
    _git("commit", "-m", f"release: {tag}")
    # --cleanup=whitespace preserves '#' lines (default 'strip' would drop the
    # '## [vX.Y.Z] YYYY-MM-DD' changelog header from section_raw, which then
    # breaks the Slack changelog formatter — no version link, no date.
    _git("tag", "-a", "--cleanup=whitespace", tag, "-m", tag, "-m", section_raw)
    _info(f"tag {tag} created.")

    _action("push changes to remote", auto=auto)
    push = subprocess.run(["git", "push", "--follow-tags"], cwd=str(root))
    if push.returncode != 0:
        _error("failed to push changes to remote")
    _info(f"tag {tag} pushed.")

    _create_gitlab_release(root, tag)


def _create_gitlab_release(root: Path, tag: str) -> None:
    """Create (or update) the GitLab release for ``tag``.

    The release description carries every configured language's user-facing notes
    (FR first with no label, then 🇬🇧 English / 🇮🇹 Italiano), each separated by a
    horizontal rule, with the changelog quoted once at the bottom — assembled by
    :func:`gitlab_release_description`. ``released_at`` is left unset so GitLab dates
    the release at creation time (avoids the "Historical" badge). Upserts: updates
    the release if it already exists.

    Needs a CI API context (``CI_API_V4_URL`` + ``CI_PROJECT_ID``) and a token
    (``RELEASE_TOKEN`` — already present for the protected push — else
    ``GITLAB_TOKEN``/``CI_JOB_TOKEN``). When the CI context/token or the
    changelog content is absent the step is skipped silently (e.g. local runs);
    but once it actually tries to publish, any API/network failure is fatal and
    fails the job — same contract as the tag creation. The git tag is already
    pushed at that point, so a retry re-attempts the release upsert.
    """
    api = os.environ.get("CI_API_V4_URL")
    project = os.environ.get("CI_PROJECT_ID")
    token = os.environ.get("RELEASE_TOKEN") or os.environ.get("GITLAB_TOKEN") or os.environ.get("CI_JOB_TOKEN")
    if not (api and project and token):
        _info("GitLab release: no CI API context/token — skipping")
        return

    # No version heading: the GitLab release is already titled with the tag, so the
    # description opens straight on the first notes section (Nouveautés/…).
    desc = gitlab_release_description(root, tag)
    if desc is None:
        _info(f"GitLab release: no changelog/release-notes content for {tag} — skipping")
        return

    base = f"{api}/projects/{urllib.parse.quote(str(project), safe='')}/releases"
    tag_q = urllib.parse.quote(tag, safe="")
    headers = {"PRIVATE-TOKEN": token, "Content-Type": "application/json"}

    # Do not set released_at: let GitLab use the creation time (the day of the
    # release). Forcing the changelog date — which is in the past relative to the
    # creation instant — makes GitLab badge the release "Historical".
    payload: dict[str, str] = {"name": tag, "description": desc.markdown}

    def _send(method: str, url: str, body: dict[str, str]) -> None:
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method=method, headers=headers)
        urllib.request.urlopen(req, timeout=20).close()

    try:
        exists = True
        try:
            urllib.request.urlopen(
                urllib.request.Request(f"{base}/{tag_q}", headers={"PRIVATE-TOKEN": token}), timeout=20
            ).close()
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
            exists = False

        if exists:
            _send("PUT", f"{base}/{tag_q}", payload)
            _info(f"GitLab release {tag} updated.")
        else:
            _send("POST", base, {"tag_name": tag, **payload})
            _info(f"GitLab release {tag} created.")
    except (urllib.error.URLError, OSError) as exc:
        _error(f"could not create/update the GitLab release for {tag}: {exc}")


def main(
    tag: Annotated[str, typer.Argument(help="Release tag (vMAJOR.MINOR.PATCH)")],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip interactive confirmations (also implied in CI)"),
    ] = False,
    root: Annotated[
        Path,
        typer.Option("--root", help="Project root (defaults to current directory)"),
    ] = Path("."),
    main_branch: Annotated[
        str,
        typer.Option("--main-branch", envvar="RELEASE_MAIN_BRANCH"),
    ] = "main",
    develop_branch: Annotated[
        str,
        typer.Option("--develop-branch", envvar="RELEASE_DEVELOP_BRANCH"),
    ] = "develop",
    support_prefix: Annotated[
        str,
        typer.Option("--support-prefix", envvar="RELEASE_SUPPORT_BRANCH"),
    ] = "support/",
    release_prefix: Annotated[
        str,
        typer.Option("--release-prefix", envvar="RELEASE_RELEASE_BRANCH"),
    ] = "release/",
    check_release_notes: Annotated[
        bool,
        typer.Option(
            "--check-release-notes/--no-check-release-notes",
            envvar="RELEASE_CHECK_RELEASE_NOTES",
            help=(
                "Require docs/release-notes/ entries for the version "
                "(set false only for repos without a docs/release-notes/ convention)."
            ),
        ),
    ] = True,
) -> None:
    """Run the full release flow for the current repository.

    Custom per-project steps can be plugged in by dropping executable scripts
    in ``release.d/`` at the repo root — they are run in alphabetical order
    after the CHANGELOG merge and before the release commit. Each script
    gets the tag as ``argv[1]`` and ``$RELEASE_TAG`` in its environment.
    """
    release(
        tag,
        root=root.resolve(),
        yes=yes,
        main_branch=main_branch,
        develop_branch=develop_branch,
        support_prefix=support_prefix,
        release_prefix=release_prefix,
        check_release_notes=check_release_notes,
    )
