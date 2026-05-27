"""Publisher / distributor scaffolding coverage.

These tests assert each publisher adapter generates a usable deploy
artifact: a script, the right credential placeholders, a GitHub Actions
workflow where appropriate, and clear setup docs. Sage doesn't upload —
the user does — so what we verify is that the scaffolded files are
syntactically correct, contain real CLI invocations, and don't bake
secrets into the repo.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sage.games.publishers import (
    REGISTRY,
    PublisherSpec,
    get_publisher,
)


def _spec(artifact_kind: str = "windows", artifact_path: str = "build/game.exe",
          project_id: str | None = None) -> PublisherSpec:
    return PublisherSpec(
        publisher="(set by adapter)",
        artifact_kind=artifact_kind,
        artifact_path=artifact_path,
        project_id=project_id,
    )


# ───────────────────────── registry ───────────────────────────────────


def test_every_registered_publisher_resolves_to_an_adapter():
    for name in REGISTRY:
        adapter = get_publisher(name)
        assert hasattr(adapter, "name")
        assert hasattr(adapter, "detect")
        assert hasattr(adapter, "scaffold")


def test_get_publisher_unknown_raises_value_error():
    """Unlike engines (which silently fall back to Godot), publishing to
    the wrong store is a user error worth surfacing loudly. Don't 'default'
    an intended Steam upload to itch.io."""
    with pytest.raises(ValueError) as exc:
        get_publisher("nintendo-eshop")
    assert "unknown publisher" in str(exc.value).lower()
    # Error must list the available options so users can fix the typo.
    assert "steam" in str(exc.value)
    assert "itch.io" in str(exc.value)


@pytest.mark.parametrize("alias,canonical", [
    ("itch",       "itch.io"),
    ("itch.io",    "itch.io"),
    ("steam",      "steam"),
    ("gh-pages",   "github-pages"),
    ("github-pages","github-pages"),
    ("play",       "google-play"),
    ("google-play","google-play"),
    ("testflight", "app-store"),
    ("app-store",  "app-store"),
])
def test_publisher_aliases_resolve_to_the_same_adapter(alias, canonical):
    """Users will type both 'itch' and 'itch.io'. Both must resolve to
    the same adapter."""
    assert get_publisher(alias).name == canonical


# ───────────────────────── itch.io ────────────────────────────────────


def test_itch_scaffold_produces_deploy_script_and_workflow(tmp_path):
    pub = get_publisher("itch.io")
    written = pub.scaffold(
        _spec(artifact_kind="web", artifact_path="build/index.html",
              project_id="sage-dev/cool-game"),
        tmp_path, log=lambda _: None,
    )
    assert written, "itch.io scaffold produced no files"

    # Local deploy scripts for both shells
    sh = tmp_path / "deploy" / "itch" / "deploy.sh"
    bat = tmp_path / "deploy" / "itch" / "deploy.bat"
    assert sh.is_file()
    assert bat.is_file()
    sh_body = sh.read_text(encoding="utf-8")
    assert "butler push" in sh_body
    assert "sage-dev/cool-game" in sh_body
    # Web channel maps to "html5" per butler's convention.
    assert ":html5" in sh_body

    # README explains setup
    readme = (tmp_path / "deploy" / "itch" / "README.md").read_text("utf-8")
    assert "BUTLER_API_KEY" in readme
    assert "butler login" in readme

    # GitHub Actions workflow uses the secret, not a hardcoded key
    wf = (tmp_path / ".github" / "workflows" / "itch-deploy.yml").read_text("utf-8")
    assert "secrets.BUTLER_API_KEY" in wf
    # The workflow must reference the same channel as the local script
    assert ":html5" in wf


def test_itch_scaffold_with_no_project_id_uses_placeholder(tmp_path):
    pub = get_publisher("itch.io")
    pub.scaffold(_spec(artifact_kind="windows", artifact_path="build/game.exe"),
                 tmp_path, log=lambda _: None)
    sh = (tmp_path / "deploy" / "itch" / "deploy.sh").read_text("utf-8")
    # Placeholder is obviously fake so the user can't ship it accidentally.
    assert "YOUR_USER/YOUR_GAME" in sh


def test_itch_channel_mapping_per_artifact_kind(tmp_path):
    """Channel names matter — the per-OS download button on the itch
    game page is driven by the channel suffix (windows / osx / linux / html5)."""
    pub = get_publisher("itch.io")
    for kind, channel in [("web", "html5"), ("windows", "windows"),
                          ("mac", "osx"), ("linux", "linux"),
                          ("android", "android")]:
        out = tmp_path / kind
        out.mkdir()
        pub.scaffold(_spec(artifact_kind=kind, artifact_path=f"build/x.{kind}"),
                     out, log=lambda _: None)
        sh = (out / "deploy" / "itch" / "deploy.sh").read_text("utf-8")
        assert f":{channel}" in sh, f"expected channel {channel} for kind {kind}"


# ───────────────────────── Steam ──────────────────────────────────────


def test_steam_scaffold_writes_vdf_files_with_app_id(tmp_path):
    """Steam's content-management uses VDF files. The build script needs
    an AppBuild VDF (the top-level config) and at least one DepotBuild
    VDF (declares which files go where)."""
    pub = get_publisher("steam")
    pub.scaffold(_spec(artifact_kind="windows", artifact_path="build/game.exe",
                       project_id="9876543"),
                 tmp_path, log=lambda _: None)

    app_vdf = (tmp_path / "deploy" / "steam" / "app.vdf").read_text("utf-8")
    depot_vdf = (tmp_path / "deploy" / "steam" / "depot.vdf").read_text("utf-8")

    assert '"AppBuild"' in app_vdf
    assert '"AppID" "9876543"' in app_vdf
    assert '"ContentRoot"' in app_vdf
    assert '"DepotBuild"' in depot_vdf
    # Depot ID auto-derived as appid+1 (Steam's convention for the main depot).
    assert '"DepotID" "9876544"' in depot_vdf


def test_steam_deploy_script_uses_env_vars_not_hardcoded_creds(tmp_path):
    """Critical: deploy scripts MUST read credentials from the env, not
    bake them into the script. We'd ship a real password into a git repo
    otherwise."""
    pub = get_publisher("steam")
    pub.scaffold(_spec(project_id="111111"), tmp_path, log=lambda _: None)
    sh = (tmp_path / "deploy" / "steam" / "deploy.sh").read_text("utf-8")
    bat = (tmp_path / "deploy" / "steam" / "deploy.bat").read_text("utf-8")
    assert "$STEAM_USERNAME" in sh
    assert "$STEAM_PASSWORD" in sh
    assert "%STEAM_USERNAME%" in bat
    assert "%STEAM_PASSWORD%" in bat
    # Sanity: no literal password placeholder in the script
    assert "password=" not in sh.lower().replace("steam_password", "")


def test_steam_readme_documents_partner_fee(tmp_path):
    """Users need to know about Steamworks' $100 fee + the manual
    partner-portal setup before sage can help them deploy."""
    pub = get_publisher("steam")
    pub.scaffold(_spec(), tmp_path, log=lambda _: None)
    readme = (tmp_path / "deploy" / "steam" / "README.md").read_text("utf-8")
    assert "partner.steamgames.com" in readme
    assert "STEAM_USERNAME" in readme


# ───────────────────────── GitHub Pages ───────────────────────────────


def test_github_pages_scaffolds_only_for_web_artifacts(tmp_path):
    """GitHub Pages serves static HTML only — there's no point scaffolding
    it for desktop builds. Adapter must return [] in those cases."""
    pub = get_publisher("github-pages")
    for kind in ("windows", "mac", "linux", "android", "ios"):
        out = tmp_path / kind
        out.mkdir()
        written = pub.scaffold(_spec(artifact_kind=kind), out, log=lambda _: None)
        assert written == [], f"github-pages should skip {kind} artifacts"


def test_github_pages_web_scaffold_writes_workflow(tmp_path):
    pub = get_publisher("github-pages")
    written = pub.scaffold(_spec(artifact_kind="web", artifact_path="build/index.html"),
                           tmp_path, log=lambda _: None)
    assert written
    wf = (tmp_path / ".github" / "workflows" / "pages.yml").read_text("utf-8")
    assert "actions/checkout@v" in wf
    assert "peaceiris/actions-gh-pages@" in wf
    assert "publish_dir: ./build" in wf


# ───────────────────────── Google Play ────────────────────────────────


def test_google_play_scaffold_uses_supply_lane_pattern(tmp_path):
    pub = get_publisher("google-play")
    pub.scaffold(_spec(artifact_kind="android",
                       artifact_path="build/game.aab",
                       project_id="com.example.coolgame"),
                 tmp_path, log=lambda _: None)
    fastfile = (tmp_path / "deploy" / "google-play" / "Fastfile").read_text("utf-8")
    appfile = (tmp_path / "deploy" / "google-play" / "Appfile").read_text("utf-8")

    assert "com.example.coolgame" in fastfile
    assert "com.example.coolgame" in appfile
    assert "upload_to_play_store" in fastfile
    # Both internal and production lanes (so users can iterate before
    # promoting to the production track).
    assert "lane :internal" in fastfile
    assert "lane :production" in fastfile
    # service-account.json reference matches the README's instructions.
    assert "service-account.json" in appfile


def test_google_play_excludes_service_account_json_from_git(tmp_path):
    """The service-account.json is a credential. It MUST be in
    .gitignore so a careless `git add deploy/` doesn't leak it."""
    pub = get_publisher("google-play")
    pub.scaffold(_spec(artifact_kind="android"), tmp_path, log=lambda _: None)
    gitignore = (tmp_path / "deploy" / "google-play" / ".gitignore").read_text("utf-8")
    assert "service-account.json" in gitignore


# ───────────────────────── App Store ──────────────────────────────────


def test_app_store_scaffold_uses_fastlane_pilot_pattern(tmp_path):
    pub = get_publisher("app-store")
    pub.scaffold(_spec(artifact_kind="ios", artifact_path="build/game.ipa",
                       project_id="com.example.cool"),
                 tmp_path, log=lambda _: None)
    fastfile = (tmp_path / "deploy" / "app-store" / "Fastfile").read_text("utf-8")
    # TestFlight lane + App Store release lane — every iOS dev needs both.
    assert "lane :beta" in fastfile
    assert "upload_to_testflight" in fastfile
    assert "lane :release" in fastfile
    assert "deliver(" in fastfile
    assert "com.example.cool" in fastfile


def test_app_store_install_hint_mentions_macos_requirement(tmp_path):
    """App Store deployment fundamentally requires Xcode on macOS. We
    must surface that BEFORE the user runs the install command."""
    pub = get_publisher("app-store")
    hint = pub.install_hint()
    assert "macOS" in hint
    assert "Xcode" in hint
