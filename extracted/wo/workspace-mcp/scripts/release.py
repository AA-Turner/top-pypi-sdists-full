# ruff: noqa

import argparse
import configparser
import getpass
import json
import os
import shutil
import subprocess
import sys
import re
import webbrowser
from pathlib import Path

import sync_site_docs

# Optional: only some machines keep the PyPI token in the system keyring.
try:
    import keyring
except ImportError:
    keyring = None


# Check for required dependencies before importing them
def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []

    # Check for tomlkit
    try:
        import tomlkit
    except ImportError:
        missing.append("tomlkit")

    # Check for twine
    try:
        result = subprocess.run(["twine", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            missing.append("twine")
    except FileNotFoundError:
        missing.append("twine")

    # Check for MCPB CLI
    try:
        result = subprocess.run(["mcpb", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            missing.append("mcpb")
    except FileNotFoundError:
        missing.append("mcpb")

    if missing:
        print("❌ Error: Required dependencies are missing:", file=sys.stderr)
        for dep in missing:
            print(f"  - {dep}", file=sys.stderr)
        print("\nPlease install them with:", file=sys.stderr)
        print("  uv pip install --extra dev", file=sys.stderr)
        print("or:", file=sys.stderr)
        print("  uv sync --extra dev", file=sys.stderr)
        if "mcpb" in missing:
            print("and:", file=sys.stderr)
            print("  npm install -g @anthropic-ai/mcpb", file=sys.stderr)
        sys.exit(1)


check_dependencies()
import tomlkit

# --- Configuration ---
REPO_ROOT = Path(__file__).parent.parent
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
SERVER_JSON_PATH = REPO_ROOT / "server.json"
README_PATH = REPO_ROOT / "README.md"
DIST_DIR = REPO_ROOT / "dist"
MCPB_SAFE_PACK = REPO_ROOT / "mcpb-safe-pack.sh"
SEMVER_RE = re.compile(r"\d+\.\d+\.\d+")

# Artifact kinds that must exist in dist/ and be attached to the GitHub release.
REQUIRED_ARTIFACT_GLOBS = ("*.whl", "*.tar.gz", "*.mcpb")

# Where a PyPI token may live, most explicit first.
PYPI_REPOSITORY_URL = "https://upload.pypi.org/legacy/"
PYPI_TOKEN_ENV_VARS = (
    "TWINE_PASSWORD",
    "PYPI_API_TOKEN",
    "PYPI_TOKEN",
    "UV_PUBLISH_TOKEN",
)

# mcp-publisher writes its login to the working directory, falling back to $HOME.
MCP_REGISTRY_TOKEN_FILES = (
    REPO_ROOT / ".mcpregistry_registry_token",
    Path.home() / ".mcp_publisher_token",
)

# --- Helper Functions ---


def run_command(command, check=True, interactive=False, env=None):
    """Executes a command, allowing for interactive input if specified.

    `env` is merged over the inherited environment and is the only channel for
    secrets: the command line is echoed and is visible to anyone running `ps`,
    so a token must never be passed as an argument.
    """
    try:
        print(f"🏃 Running: {' '.join(command)}")
        kwargs = {"check": check, "text": True, "encoding": "utf-8"}
        if not interactive:
            kwargs["capture_output"] = True
        if env:
            kwargs["env"] = {**os.environ, **env}

        result = subprocess.run(command, **kwargs)

        if not interactive:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        return result
    except FileNotFoundError:
        print(
            f"❌ Error: Command '{command[0]}' not found. Is it installed and in your PATH?",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}", file=sys.stderr)
        if not interactive and hasattr(e, "stderr"):
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


# --- Credentials ---
#
# Every publishing step is checked for credentials during pre-flight, before the
# first irreversible action. The old script discovered a missing PyPI token at
# step 7 — after the tag had already been force-pushed — which left the release
# half-shipped and needing manual repair. Nothing here ever prints a secret or
# puts one on a command line.


class PypiCredentials:
    """A resolved way to authenticate to PyPI, and where it came from."""

    def __init__(self, source, env):
        self.source = source
        self.env = env  # Extra environment for twine; empty when twine self-serves.


def _pypirc_has_credentials():
    """True when ~/.pypirc holds a password twine can use unprompted."""
    pypirc = Path.home() / ".pypirc"
    if not pypirc.exists():
        return False
    parser = configparser.ConfigParser()
    try:
        parser.read(pypirc)
    except configparser.Error:
        return False
    return any(parser.has_option(section, "password") for section in parser.sections())


def _keyring_token():
    """The PyPI token from the system keyring, if there is a keyring at all."""
    if keyring is None:
        return None
    try:
        return keyring.get_password(PYPI_REPOSITORY_URL, "__token__")
    except Exception:
        return None


def _token_env(token):
    """Environment that authenticates twine with an API token."""
    return {
        "TWINE_USERNAME": os.environ.get("TWINE_USERNAME", "__token__").strip()
        or "__token__",
        "TWINE_PASSWORD": token,
        "TWINE_NON_INTERACTIVE": "1",
    }


def resolve_pypi_credentials(allow_prompt=True):
    """Finds a PyPI credential, or returns None if there is nothing to find.

    Ordered by how deliberate the intent is: an environment variable set for
    this run beats a file on disk, which beats the keyring, which beats asking.
    Prompting is a last resort and only possible on a terminal — which is why
    this can be called during pre-flight and trusted to fail early in CI.
    """
    for var in PYPI_TOKEN_ENV_VARS:
        token = os.environ.get(var, "").strip()
        if token:
            return PypiCredentials(f"${var}", _token_env(token))

    if _pypirc_has_credentials():
        return PypiCredentials("~/.pypirc", {"TWINE_NON_INTERACTIVE": "1"})

    token = (_keyring_token() or "").strip()
    if token:
        return PypiCredentials("system keyring", _token_env(token))

    if allow_prompt and sys.stdin.isatty():
        print("🔑 No stored PyPI credential found.")
        token = getpass.getpass("   PyPI API token (input hidden): ").strip()
        if token:
            return PypiCredentials("interactive prompt", _token_env(token))

    return None


def check_pypi_credentials():
    """Pre-flight: resolve a PyPI credential or refuse to start the release."""
    credentials = resolve_pypi_credentials()
    if credentials is None:
        print("❌ Error: no PyPI credential available.", file=sys.stderr)
        print(
            "   Set one of "
            + ", ".join(f"${v}" for v in PYPI_TOKEN_ENV_VARS)
            + ", add a password to ~/.pypirc, store one in your keyring,",
            file=sys.stderr,
        )
        print(
            "   or run this from a terminal so it can prompt. Refusing to start:"
            " the tag would be pushed before the upload could fail.",
            file=sys.stderr,
        )
        sys.exit(1)

    token = credentials.env.get("TWINE_PASSWORD", "")
    if token and not token.startswith("pypi-"):
        print(
            "⚠️ Warning: that token does not look like a PyPI API token (no 'pypi-' prefix)."
        )

    print(f"✅ PyPI credential resolved from {credentials.source}.")
    return credentials


def check_registry_credentials():
    """Pre-flight: warn early if mcp-publisher has no saved login."""
    if any(path.exists() for path in MCP_REGISTRY_TOKEN_FILES):
        print("✅ MCP Registry login found.")
        return True
    print(
        "⚠️ Warning: no MCP Registry token found "
        f"({', '.join(str(p) for p in MCP_REGISTRY_TOKEN_FILES)})."
    )
    print("   Run 'mcp-publisher login github' first, or the publish step will fail.")
    return False


def get_current_version():
    """Reads the current version from pyproject.toml."""
    if not PYPROJECT_PATH.exists():
        print(
            f"❌ Error: pyproject.toml not found at {PYPROJECT_PATH}", file=sys.stderr
        )
        sys.exit(1)
    with open(PYPROJECT_PATH, "r") as f:
        data = tomlkit.load(f)
    return data["project"]["version"]


def update_pyproject_version(new_version):
    """Updates the version in pyproject.toml."""
    with open(PYPROJECT_PATH, "r") as f:
        data = tomlkit.load(f)
    data["project"]["version"] = new_version
    with open(PYPROJECT_PATH, "w") as f:
        tomlkit.dump(data, f)
    print(f"✅ Version updated to {new_version} in pyproject.toml")


def update_server_json_version(new_version):
    """Updates the version fields in server.json."""
    if not SERVER_JSON_PATH.exists():
        print(f"❌ Error: server.json not found at {SERVER_JSON_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(SERVER_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    server_name = data.get("name", "").strip()
    if not server_name:
        print("❌ Error: server.json is missing a valid 'name' field.", file=sys.stderr)
        sys.exit(1)

    data["version"] = new_version

    packages = data.get("packages", [])
    if isinstance(packages, list):
        for package in packages:
            if package.get("registryType") == "pypi":
                package["version"] = new_version

    with open(SERVER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"✅ Version updated to {new_version} in server.json")
    return server_name


def verify_readme_mcp_marker(server_name):
    """Ensure README contains the mcp-name ownership marker for PyPI validation."""
    if not README_PATH.exists():
        print(f"❌ Error: README.md not found at {README_PATH}", file=sys.stderr)
        sys.exit(1)

    expected_marker = f"mcp-name: {server_name}"
    readme_content = README_PATH.read_text(encoding="utf-8")
    if expected_marker not in readme_content:
        print(
            "❌ Error: README.md is missing the required MCP ownership marker.",
            file=sys.stderr,
        )
        print(f"Expected to find: {expected_marker}", file=sys.stderr)
        sys.exit(1)

    print("✅ README.md contains MCP ownership marker.")


def update_manifest_version(new_version):
    """Updates the version in manifest.json."""
    manifest_path = REPO_ROOT / "manifest.json"
    if not manifest_path.exists():
        print(f"⚠️ Warning: manifest.json not found at {manifest_path}, skipping")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["version"] = new_version

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"✅ Version updated to {new_version} in manifest.json")


def build_mcpb(new_version):
    """Builds the MCPB bundle using the safe pack script."""
    if not MCPB_SAFE_PACK.exists():
        print(
            f"❌ Error: {MCPB_SAFE_PACK} not found. Cannot build MCPB bundle.",
            file=sys.stderr,
        )
        sys.exit(1)

    mcpb_output = DIST_DIR / f"workspace-mcp-{new_version}.mcpb"
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    run_command([str(MCPB_SAFE_PACK), str(mcpb_output)])
    print(f"✅ MCPB bundle built: {mcpb_output}")
    return mcpb_output


def get_next_versions(current_version):
    """Calculates next patch, minor, and major versions."""
    major, minor, patch = map(int, current_version.split("."))
    return {
        "patch": f"{major}.{minor}.{patch + 1}",
        "minor": f"{major}.{minor + 1}.0",
        "major": f"{major + 1}.0.0",
    }


def select_version(current_version):
    """Prompts the user to select the next version."""
    next_versions = get_next_versions(current_version)
    print(f"\nCurrent version is {current_version}. Choose the next version:")
    options = list(next_versions.items())
    for i, (level, version) in enumerate(options):
        print(f"  {i + 1}) {level.capitalize()}: {version}")

    while True:
        try:
            choice = input(f"Enter your choice (1-{len(options)}): ")
            if 1 <= int(choice) <= len(options):
                return options[int(choice) - 1][1]
        except (ValueError, IndexError):
            pass
        print("Invalid choice. Please try again.")


def resolve_version(current_version, bump=None, explicit_version=None):
    """Determines the next version from flags, falling back to the interactive prompt."""
    if explicit_version:
        if not SEMVER_RE.fullmatch(explicit_version):
            print(
                f"❌ Error: --version must be X.Y.Z, got '{explicit_version}'.",
                file=sys.stderr,
            )
            sys.exit(1)
        return explicit_version
    if bump:
        return get_next_versions(current_version)[bump]
    return select_version(current_version)


def collect_dist_artifacts():
    """Returns the release artifacts in dist/, failing if any required kind is absent."""
    artifacts = []
    for glob in REQUIRED_ARTIFACT_GLOBS:
        matches = sorted(DIST_DIR.glob(glob))
        if not matches:
            print(f"❌ Error: no {glob} artifact found in {DIST_DIR}.", file=sys.stderr)
            sys.exit(1)
        artifacts.extend(matches)
    return artifacts


def get_attached_asset_names(tag_name):
    """Returns the set of asset filenames currently attached to a release."""
    result = run_command(
        ["gh", "release", "view", tag_name, "--json", "assets", "-q", ".assets[].name"]
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def verify_release_assets(tag_name, artifacts):
    """Ensures every dist artifact is attached to the release, re-uploading if needed."""
    attached = get_attached_asset_names(tag_name)
    missing = [f for f in artifacts if f.name not in attached]

    if missing:
        print(f"⚠️ {len(missing)} artifact(s) missing from the release, uploading...")
        run_command(
            ["gh", "release", "upload", tag_name, "--clobber"]
            + [str(f) for f in missing]
        )
        attached = get_attached_asset_names(tag_name)
        missing = [f for f in artifacts if f.name not in attached]

    if missing:
        print("❌ Error: release is still missing artifacts:", file=sys.stderr)
        for f in missing:
            print(f"  - {f.name}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ All {len(artifacts)} artifact(s) attached to {tag_name}:")
    for f in artifacts:
        print(f"  - {f.name}")


def export_release_notes(tag_name):
    """Writes GitHub's autogenerated release notes to a file for downstream editing."""
    result = run_command(
        ["gh", "release", "view", tag_name, "--json", "body", "-q", ".body"]
    )
    notes_path = DIST_DIR / f"release-notes-{tag_name}.md"
    notes_path.write_text(result.stdout.strip() + "\n", encoding="utf-8")
    print(f"✅ Autogenerated release notes written to {notes_path}")
    return notes_path


def sync_website_docs(tag_name, previous_tag, site_repo):
    """Re-pins the site's docs version and reports what the release left stale.

    The site is a separate repository, so this edits and reports but never
    stages or commits — the changes are left in its working tree for review.
    """
    try:
        result = sync_site_docs.sync(
            tag_name, previous_tag=previous_tag, site_repo=site_repo
        )
    except RuntimeError as error:
        print(f"⚠️ Skipping website docs sync: {error}")
        return None

    report = sync_site_docs.render_report(result)
    report_path = DIST_DIR / f"site-docs-sync-{tag_name}.md"
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"📄 Report written to {report_path}")

    if sync_site_docs.needs_review(result):
        print("⚠️ The site docs need a human pass — see the report above.")
    else:
        print("✅ Website docs are consistent with this release.")

    result["report_file"] = str(report_path)
    return result


def get_repo_slug():
    """Returns (owner, repo) parsed from the origin remote, or (None, None)."""
    remote_url = run_command(["git", "remote", "get-url", "origin"]).stdout.strip()
    match = re.search(r"github\.com[/:](.+?)/(.+?)(?:\.git)?$", remote_url)
    if not match:
        return None, None
    return match.groups()


# --- Main Release Logic ---


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Release google-workspace-mcp")
    parser.add_argument(
        "--registry",
        action="store_true",
        help="Also publish to the MCP Registry",
    )
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help="Bump level to apply without prompting",
    )
    version_group.add_argument(
        "--version",
        dest="explicit_version",
        help="Exact version to release (X.Y.Z), skipping the prompt",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the draft release in a browser",
    )
    parser.add_argument(
        "--site-repo",
        help=(
            "Path to the workspacemcp.com checkout to re-sync "
            f"(default: ${sync_site_docs.SITE_REPO_ENV} or {sync_site_docs.DEFAULT_SITE_REPO})"
        ),
    )
    parser.add_argument(
        "--no-site-sync",
        action="store_true",
        help="Do not touch the website docs",
    )
    parser.add_argument(
        "--json",
        dest="json_summary",
        action="store_true",
        help="Print a machine-readable summary of the release at the end",
    )
    return parser.parse_args()


def main():
    """Main function to orchestrate the release process."""
    args = parse_args()
    print("🚀 Starting the release process for google-workspace-mcp...")

    # 1. Pre-flight checks
    print("\n--- 1. Running Pre-flight Checks ---")
    git_status_output = run_command(["git", "status", "--porcelain"]).stdout
    if git_status_output:
        # Allow untracked files, but fail on modified or staged files.
        is_dirty = any(
            not line.startswith("??")
            for line in git_status_output.strip().split("\n")
            if line
        )
        if is_dirty:
            print(
                "❌ Error: Your git working directory has modified or staged files. Please commit or stash them.",
                file=sys.stderr,
            )
            print(git_status_output, file=sys.stderr)
            sys.exit(1)
    print("✅ Git working directory is clean (untracked files are ignored).")
    run_command(["git", "fetch", "--tags"])
    print("✅ Fetched latest git tags.")

    # Resolve every credential up front. Step 6 force-pushes a tag, and there is
    # no graceful way back from a tag that ships without the package it names.
    pypi_credentials = check_pypi_credentials()
    if args.registry:
        check_registry_credentials()

    previous_tag = run_command(
        ["git", "describe", "--tags", "--abbrev=0"], check=False
    ).stdout.strip()

    # 2. Version selection
    print("\n--- 2. Selecting Version ---")
    current_version = get_current_version()
    new_version = resolve_version(current_version, args.bump, args.explicit_version)
    print(f"📌 Releasing {current_version} → {new_version}")

    # 3. Update release metadata
    print("\n--- 3. Updating Version ---")
    update_pyproject_version(new_version)
    server_name = update_server_json_version(new_version)
    update_manifest_version(new_version)
    verify_readme_mcp_marker(server_name)

    # 4. Build the project
    print("\n--- 4. Building Project ---")
    if DIST_DIR.exists():
        print(f"🧹 Cleaning up old build artifacts in {DIST_DIR}...")
        shutil.rmtree(DIST_DIR)
    run_command(["uv", "build"])
    print(f"✅ Project built successfully in {DIST_DIR}")

    # 4b. Build MCPB bundle (git-tracked files only)
    print("\n--- 4b. Building MCPB Bundle (safe pack) ---")
    build_mcpb(new_version)

    # 5. Git commit and tag
    print("\n--- 5. Committing and Tagging ---")
    tag_name = f"v{new_version}"
    manifest_json = REPO_ROOT / "manifest.json"
    run_command(
        ["git", "add", str(PYPROJECT_PATH), str(SERVER_JSON_PATH), str(manifest_json)]
    )
    run_command(["git", "commit", "-m", f"chore: release {tag_name}"])
    run_command(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"])
    print(f"✅ Committed and tagged release {tag_name}")

    # 6. Push to GitHub
    print("\n--- 6. Pushing to GitHub ---")
    print("⚠️ Forcing push to overwrite remote branch history.")
    run_command(["git", "push", "--force", "origin", "HEAD", "--follow-tags"])
    print("✅ Pushed commit and tags to origin.")

    # 7. Upload to PyPI (only wheels and tarballs, not .mcpb)
    print("\n--- 7. Uploading to PyPI ---")
    print(f"🔑 Authenticating with the credential from {pypi_credentials.source}.")
    pypi_files = list(DIST_DIR.glob("*.whl")) + list(DIST_DIR.glob("*.tar.gz"))
    run_command(
        ["twine", "upload", "--skip-existing"] + [str(f) for f in pypi_files],
        env=pypi_credentials.env,
    )
    print("✅ Successfully uploaded to PyPI (or skipped if already present).")

    # 8. Publish to MCP Registry (opt-in via --registry)
    if args.registry:
        print("\n--- 8. Publishing to MCP Registry ---")
        run_command(["mcp-publisher", "--version"])
        run_command(["mcp-publisher", "publish"])
        print("✅ Successfully published to MCP Registry.")
    else:
        print("\n--- 8. Skipping MCP Registry (use --registry to publish) ---")

    # 9. Create GitHub Release
    print("\n--- 9. Creating GitHub Release ---")
    print("📝 Creating a draft release on GitHub...")

    artifacts = collect_dist_artifacts()
    print(f"📦 Attaching {len(artifacts)} distribution file(s) to the release:")
    for artifact in artifacts:
        print(f"  - {artifact.name}")

    release_command = [
        "gh",
        "release",
        "create",
        tag_name,
        "--draft",
        "--generate-notes",
        "--title",
        tag_name,
    ]
    release_command.extend(str(f) for f in artifacts)
    run_command(release_command, interactive=True)
    print(f"✅ GitHub draft release for {tag_name} created.")

    # 10. Verify artifacts landed and export the autogenerated notes for editing
    print("\n--- 10. Verifying Release Artifacts ---")
    verify_release_assets(tag_name, artifacts)

    print("\n--- 11. Exporting Autogenerated Release Notes ---")
    notes_path = export_release_notes(tag_name)

    print("\n--- 12. Syncing Website Documentation ---")
    if args.no_site_sync:
        site_sync = None
        print("⏭️ Skipped (--no-site-sync).")
    else:
        site_sync = sync_website_docs(tag_name, previous_tag, args.site_repo)

    owner, repo = get_repo_slug()
    edit_url = (
        f"https://github.com/{owner}/{repo}/releases/edit/{tag_name}" if owner else None
    )

    if edit_url and not args.no_browser:
        try:
            print(f"🌍 Opening your browser to edit the release: {edit_url}")
            webbrowser.open(edit_url)
        except Exception as e:
            print(f"⚠️ Could not open browser to edit release: {e}")
    elif not edit_url:
        print("⚠️ Could not determine repository URL for the release edit link.")

    print("\n🎉 Release process complete! 🎉")

    if args.json_summary:
        print("\n--- RELEASE SUMMARY (JSON) ---")
        print(
            json.dumps(
                {
                    "version": new_version,
                    "previous_version": current_version,
                    "tag": tag_name,
                    "previous_tag": previous_tag,
                    "draft": True,
                    "assets": [f.name for f in artifacts],
                    "notes_file": str(notes_path),
                    "edit_url": edit_url,
                    "registry_published": bool(args.registry),
                    "pypi_credential_source": pypi_credentials.source,
                    "site_docs": site_sync,
                },
                indent=2,
            )
        )
        print("--- END RELEASE SUMMARY ---")


if __name__ == "__main__":
    main()
