"""Concrete publisher adapters.

Each one is ~30-50 lines because they only generate text files (deploy
scripts + CI workflows). No publisher-side state is touched by sage —
the user provides their own API keys at deploy time. This keeps sage
auth-free for the publishing step.

CLI references:
  itch.io    → butler push <dir> <user>/<game>:<channel>
  Steam      → steamcmd +login +run_app_build_http +quit
  GitHub Pgs → gh-pages branch + workflow that copies build/ to it
  Google Play → fastlane supply or play-publisher
  App Store  → fastlane pilot (TestFlight) or xcrun altool
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

from .base import PublisherAdapter, PublisherSpec, ProgressFn


# ───────────────────────── itch.io ────────────────────────────────────


class ItchAdapter:
    """Indie game distribution via itch.io's butler CLI."""

    name = "itch.io"

    def detect(self) -> Optional[Path]:
        p = shutil.which("butler")
        return Path(p) if p else None

    def install_hint(self) -> str:
        return (
            "Install butler from https://itch.io/docs/butler/installing.html\n"
            "  macOS / Linux: `curl -L -o butler.zip <url> && unzip butler.zip`\n"
            "  Windows:       download butler.exe, add to PATH"
        )

    def scaffold(self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn) -> list[Path]:
        deploy_dir = out_dir / "deploy" / "itch"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        user_slug = spec.project_id or "YOUR_USER/YOUR_GAME"
        channel = _channel_for(spec.artifact_kind)
        # build/ is the directory butler uploads — whatever the engine produced.
        artifact_dir = str(Path(spec.artifact_path).parent or "build")

        script_sh = (
            "#!/usr/bin/env bash\n"
            "# Deploy this game to itch.io via butler.\n"
            "# 1) Install butler: https://itch.io/docs/butler/installing.html\n"
            "# 2) Run `butler login` once (cached at ~/.config/itch).\n"
            "# 3) Replace YOUR_USER/YOUR_GAME below.\n"
            f"set -euo pipefail\n"
            f"butler push {artifact_dir} {user_slug}:{channel}\n"
        )
        script_bat = (
            "@echo off\n"
            "REM Deploy this game to itch.io via butler.\n"
            "REM 1) Install butler from https://itch.io/docs/butler/installing.html\n"
            "REM 2) Run `butler login` once.\n"
            f"butler push {artifact_dir} {user_slug}:{channel}\n"
        )
        workflow = _itch_github_actions(user_slug, channel, artifact_dir)
        readme = (
            "# itch.io deploy\n\n"
            f"This game is configured for itch.io distribution as `{user_slug}`\n"
            f"on the `{channel}` channel.\n\n"
            "## First-time setup\n"
            "1. Create an itch.io account and a project page.\n"
            "2. Install butler: https://itch.io/docs/butler/installing.html\n"
            "3. Run `butler login` and follow the browser prompt.\n"
            "4. Edit `deploy.sh` (or `deploy.bat` on Windows) and replace\n"
            "   `YOUR_USER/YOUR_GAME` with your itch.io slug.\n"
            "5. Run `./deploy.sh` (or `deploy.bat`).\n\n"
            "## CI auto-deploy\n"
            "Set the `BUTLER_API_KEY` secret in your GitHub repo settings.\n"
            "The included workflow at `.github/workflows/itch-deploy.yml`\n"
            "will publish every push to main.\n"
        )
        written: list[Path] = []
        for filename, body in (
            ("deploy.sh", script_sh),
            ("deploy.bat", script_bat),
            ("README.md", readme),
        ):
            p = deploy_dir / filename
            p.write_text(body, encoding="utf-8")
            written.append(p)
        # GitHub Actions workflow goes into .github/workflows/
        wf_path = out_dir / ".github" / "workflows" / "itch-deploy.yml"
        wf_path.parent.mkdir(parents=True, exist_ok=True)
        wf_path.write_text(workflow, encoding="utf-8")
        written.append(wf_path)

        log(f"  [itch.io] scaffolded {len(written)} files in deploy/itch/")
        return written


# ───────────────────────── Steam ──────────────────────────────────────


class SteamAdapter:
    """PC distribution via Valve's Steam (steamcmd + Steam Pipe)."""

    name = "steam"

    def detect(self) -> Optional[Path]:
        # Steam CLI is `steamcmd`, sometimes named `steamcmd.sh` on Linux.
        for name in ("steamcmd", "steamcmd.sh", "steamcmd.exe"):
            p = shutil.which(name)
            if p:
                return Path(p)
        return None

    def install_hint(self) -> str:
        return (
            "Steam distribution requires Steamworks Partner access AND steamcmd.\n"
            "  Sign up: https://partner.steamgames.com (one-time $100/title fee)\n"
            "  Install steamcmd: https://developer.valvesoftware.com/wiki/SteamCMD"
        )

    def scaffold(self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn) -> list[Path]:
        deploy_dir = out_dir / "deploy" / "steam"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        app_id = spec.project_id or "1234567"
        depot_id = str(int(app_id) + 1) if app_id.isdigit() else "1234568"
        artifact_dir = str(Path(spec.artifact_path).parent or "build")

        app_vdf = (
            f'"AppBuild"\n{{\n'
            f'    "AppID" "{app_id}"\n'
            f'    "Desc"  "sage build"\n'
            f'    "BuildOutput" "deploy/steam/output/"\n'
            f'    "ContentRoot" "../../{artifact_dir}/"\n'
            f'    "Depots"\n    {{\n'
            f'        "{depot_id}" "depot.vdf"\n'
            f'    }}\n'
            f'}}\n'
        )
        depot_vdf = (
            f'"DepotBuild"\n{{\n'
            f'    "DepotID" "{depot_id}"\n'
            f'    "FileMapping"\n    {{\n'
            f'        "LocalPath" "*"\n'
            f'        "DepotPath" "."\n'
            f'        "recursive" "1"\n'
            f'    }}\n'
            f'}}\n'
        )
        script_sh = (
            "#!/usr/bin/env bash\n"
            "# Upload this build to Steam via steamcmd.\n"
            "# Requires STEAM_USERNAME and STEAM_PASSWORD (or use cached login).\n"
            "set -euo pipefail\n"
            "steamcmd +login \"$STEAM_USERNAME\" \"$STEAM_PASSWORD\" \\\n"
            "         +run_app_build_http \"$(realpath deploy/steam/app.vdf)\" \\\n"
            "         +quit\n"
        )
        script_bat = (
            "@echo off\n"
            "REM Upload this build to Steam via steamcmd.\n"
            "steamcmd +login %STEAM_USERNAME% %STEAM_PASSWORD% "
            "+run_app_build_http deploy\\steam\\app.vdf +quit\n"
        )
        readme = (
            "# Steam deploy\n\n"
            f"App ID: `{app_id}` — replace in `app.vdf` and `depot.vdf` with\n"
            "your real Steamworks app ID.\n\n"
            "## First-time setup\n"
            "1. Steamworks Partner account (https://partner.steamgames.com)\n"
            "2. Generate Steam Guard backup codes for steamcmd login\n"
            "3. Set $STEAM_USERNAME and $STEAM_PASSWORD env vars\n"
            "4. Run `./deploy.sh`\n\n"
            "Builds upload to the 'default' branch by default. To push to a\n"
            "preview branch, add `SetLive=\"<branch>\"` to app.vdf.\n"
        )
        written: list[Path] = []
        for filename, body in (
            ("app.vdf",   app_vdf),
            ("depot.vdf", depot_vdf),
            ("deploy.sh", script_sh),
            ("deploy.bat", script_bat),
            ("README.md", readme),
        ):
            p = deploy_dir / filename
            p.write_text(body, encoding="utf-8")
            written.append(p)
        log(f"  [steam] scaffolded {len(written)} files in deploy/steam/")
        return written


# ───────────────────────── GitHub Pages ───────────────────────────────


class GitHubPagesAdapter:
    """Free static hosting for web builds. The included workflow pushes
    the `build/` directory to the `gh-pages` branch on every main commit."""

    name = "github-pages"

    def detect(self) -> Optional[Path]:
        # gh-pages is workflow-based; only need git on PATH.
        p = shutil.which("git")
        return Path(p) if p else None

    def install_hint(self) -> str:
        return ("Git is required (`git --version`). Enable GitHub Pages in your\n"
                "repo settings → Pages → source: gh-pages branch, root.")

    def scaffold(self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn) -> list[Path]:
        if spec.artifact_kind != "web":
            # GitHub Pages only hosts static web content.
            return []
        deploy_dir = out_dir / "deploy" / "github-pages"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        workflow = """name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish web build
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
"""
        readme = (
            "# GitHub Pages deploy\n\n"
            "Free hosting for the web build at\n"
            "`https://<your-user>.github.io/<your-repo>/`.\n\n"
            "## Setup\n"
            "1. Push the repo to GitHub.\n"
            "2. Build the game so `build/` exists (sage's pipeline does this).\n"
            "3. Settings → Pages → Source → gh-pages / root → Save.\n"
            "4. The included workflow at `.github/workflows/pages.yml`\n"
            "   publishes on every push to main.\n"
        )
        wf_path = out_dir / ".github" / "workflows" / "pages.yml"
        wf_path.parent.mkdir(parents=True, exist_ok=True)
        wf_path.write_text(workflow, encoding="utf-8")
        readme_path = deploy_dir / "README.md"
        readme_path.write_text(readme, encoding="utf-8")
        log(f"  [github-pages] scaffolded workflow + README")
        return [wf_path, readme_path]


# ───────────────────────── Google Play ────────────────────────────────


class GooglePlayAdapter:
    """Android distribution via fastlane's supply plugin."""

    name = "google-play"

    def detect(self) -> Optional[Path]:
        for n in ("fastlane", "bundle"):
            p = shutil.which(n)
            if p:
                return Path(p)
        return None

    def install_hint(self) -> str:
        return ("Install fastlane: `brew install fastlane` (mac/linux) or\n"
                "`gem install fastlane` (any platform with Ruby).")

    def scaffold(self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn) -> list[Path]:
        deploy_dir = out_dir / "deploy" / "google-play"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        package = spec.project_id or "com.your.package"
        fastfile = f"""# fastlane Fastfile for Google Play deployment
default_platform(:android)

platform :android do
  desc "Push the current AAB to the internal test track"
  lane :internal do
    upload_to_play_store(
      package_name: "{package}",
      track: "internal",
      aab: "../../build/game.aab",
    )
  end

  desc "Promote internal → production"
  lane :production do
    upload_to_play_store(
      package_name: "{package}",
      track: "production",
      aab: "../../build/game.aab",
    )
  end
end
"""
        appfile = f'package_name "{package}"\n' \
                  'json_key_file "./service-account.json"\n'
        readme = (
            "# Google Play deploy\n\n"
            f"Package: `{package}` — change in Fastfile + Appfile.\n\n"
            "## Setup\n"
            "1. Generate a service-account JSON in the Google Cloud Console\n"
            "   with Play Console Developer access.\n"
            "2. Save it as `service-account.json` in this directory\n"
            "   (excluded from git via the included .gitignore).\n"
            "3. Run `fastlane internal` to push to the internal track.\n"
        )
        gitignore = "service-account.json\n*.p12\n*.jks\n"

        written: list[Path] = []
        for filename, body in (
            ("Fastfile",   fastfile),
            ("Appfile",    appfile),
            ("README.md",  readme),
            (".gitignore", gitignore),
        ):
            p = deploy_dir / filename
            p.write_text(body, encoding="utf-8")
            written.append(p)
        log(f"  [google-play] scaffolded {len(written)} files")
        return written


# ───────────────────────── App Store ──────────────────────────────────


class AppStoreAdapter:
    """iOS distribution via fastlane (TestFlight + App Store)."""

    name = "app-store"

    def detect(self) -> Optional[Path]:
        p = shutil.which("fastlane")
        return Path(p) if p else None

    def install_hint(self) -> str:
        return ("App Store deployment requires macOS + Xcode + a paid Apple\n"
                "Developer account ($99/year). Install fastlane via\n"
                "`brew install fastlane` after the prerequisites are set up.")

    def scaffold(self, spec: PublisherSpec, out_dir: Path, *, log: ProgressFn) -> list[Path]:
        deploy_dir = out_dir / "deploy" / "app-store"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        bundle_id = spec.project_id or "com.your.bundleid"
        fastfile = f"""# fastlane Fastfile for App Store + TestFlight
default_platform(:ios)

platform :ios do
  desc "Push the latest IPA to TestFlight"
  lane :beta do
    upload_to_testflight(
      app_identifier: "{bundle_id}",
      ipa: "../../build/game.ipa",
    )
  end

  desc "Submit to the App Store for review"
  lane :release do
    deliver(
      app_identifier: "{bundle_id}",
      ipa: "../../build/game.ipa",
      submit_for_review: true,
      automatic_release: false,
    )
  end
end
"""
        readme = (
            "# App Store deploy\n\n"
            f"Bundle ID: `{bundle_id}`.\n\n"
            "## Setup (macOS only)\n"
            "1. Apple Developer account + App Store Connect access.\n"
            "2. Generate an App-Specific Password in your Apple ID account.\n"
            "3. `export FASTLANE_PASSWORD=<that password>`\n"
            "4. `fastlane beta` for TestFlight, `fastlane release` for store.\n"
        )
        written: list[Path] = []
        for filename, body in (("Fastfile", fastfile), ("README.md", readme)):
            p = deploy_dir / filename
            p.write_text(body, encoding="utf-8")
            written.append(p)
        log(f"  [app-store] scaffolded {len(written)} files")
        return written


# ───────────────────────── helpers ────────────────────────────────────


def _channel_for(artifact_kind: str) -> str:
    """Map artifact kind → butler channel name. itch.io users see these
    in the per-OS download buttons on the game page."""
    return {
        "web":     "html5",
        "windows": "windows",
        "mac":     "osx",
        "linux":   "linux",
        "android": "android",
    }.get(artifact_kind, artifact_kind)


def _itch_github_actions(user_slug: str, channel: str, artifact_dir: str) -> str:
    return f"""name: Deploy to itch.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Download butler
        run: |
          curl -L -o butler.zip https://broth.itch.zone/butler/linux-amd64/LATEST/archive/default
          unzip butler.zip
          chmod +x butler
      - name: Push to itch.io
        env:
          BUTLER_API_KEY: ${{{{ secrets.BUTLER_API_KEY }}}}
        run: ./butler push {artifact_dir} {user_slug}:{channel}
"""
