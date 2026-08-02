#!/usr/bin/env python3
import argparse
import subprocess
import sys
import re
from enum import Enum

def run(cmd, dry_run=False, capture=False):
    print(f"🔧 {cmd}")
    if dry_run:
        print("🧪 (dry run)")
        return ""
    result = subprocess.run(
        cmd, shell=True, check=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True
    )
    return result.stdout.strip() if capture else ""


def ensure_clean_git():
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        print("❌ Working directory not clean. Please commit or stash changes.")
        sys.exit(1)


def get_exact_tag():
    try:
        return subprocess.check_output(["git", "describe", "--tags", "--exact-match"], text=True).strip()
    except subprocess.CalledProcessError:
        return None


def confirm(prompt):
    try:
        response = input(f"{prompt} (y/N): ")
        return response.strip().lower() == 'y'
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)


def get_current_branch():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()


def ensure_bump2version_installed():
    try:
        subprocess.run(
            ["bump2version", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 bump2version not found. Installing it with uv...")
        try:
            # First ensure uv is available
            try:
                subprocess.run(
                    ["uv", "--version"],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("📦 uv not found. Installing uv first...")
                subprocess.run(
                    "curl -LsSf https://astral.sh/uv/install.sh | sh",
                    check=True,
                    shell=True
                )
                print("✅ uv installed.")
            
            # Now use uv to install bump2version
            subprocess.run(
                ["uv", "pip", "install", "bump2version"],
                check=True
            )
            print("✅ bump2version installed.")
        except subprocess.CalledProcessError:
            print("❌ Failed to install bump2version. Please install it manually.")
            sys.exit(1)


def bump_version(part, dry_run=False):
    """Bump version on current branch and return the new tag."""
    print(f"📦 Bumping version ({part})...")
    BUMP_CFG = "./.bump2version.cfg"
    run(f"bump2version {part} --config-file {BUMP_CFG} {'--dry-run --verbose' if dry_run else ''}")

    tag = get_exact_tag()
    if not tag and not dry_run:
        print("❌ No Git tag found on current commit. Did bump2version create it?")
        sys.exit(1)

    if not dry_run and not re.match(r"^v\d+\.\d+\.\d+$", tag):
        print(f"❌ Tag '{tag}' does not match semantic versioning (vX.Y.Z).")
        sys.exit(1)

    return tag


def get_current_version():
    """Get the current version from .bump2version.cfg"""
    try:
        with open('./.bump2version.cfg', 'r') as f:
            for line in f:
                if line.startswith('current_version'):
                    return line.strip().split('=')[1].strip()
    except Exception as e:
        print(f"❌ Error reading version: {e}")
        return None
        
def calculate_next_version(current_version, part):
    """Calculate the next version based on the bump part."""
    if not current_version:
        return None
        
    try:
        # Parse the version
        major, minor, patch = map(int, current_version.split('.'))
        
        if part == "major":
            return f"{major + 1}.0.0"
        elif part == "minor":
            return f"{major}.{minor + 1}.0"
        elif part == "patch":
            return f"{major}.{minor}.{patch + 1}"
        else:
            return None
    except Exception as e:
        print(f"❌ Error calculating next version: {e}")
        return None

def create_tag_for_version(version, dry_run=False):
    """Create a tag for the current version without bumping"""
    if not version:
        print("❌ Could not determine current version")
        sys.exit(1)
    
    tag = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(["git", "tag", "-l", tag], capture_output=True, text=True)
    if result.stdout.strip():
        print(f"⚠️ Tag {tag} already exists. Re-using existing tag.")
        
        if not dry_run:
            # Force update the tag to point to the current commit
            current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            run(f"git tag -f {tag} {current_commit}")
    else:
        if not dry_run:
            run(f"git tag {tag}")
    
    return tag

def main():
    parser = argparse.ArgumentParser(
        description="Release to PyPI, with optional version bumping.")
    
    # Create a mutually exclusive group for version operations
    version_group = parser.add_mutually_exclusive_group()
    version_group.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        help=(
            "Bump version before releasing:\n"
            "  patch → 1.0.0 → 1.0.1 (bugfixes, safe changes)\n"
            "  minor → 1.0.0 → 1.1.0 (new features, backward-compatible)\n"
            "  major → 1.0.0 → 2.0.0 (breaking changes)"
        )
    )
    version_group.add_argument(
        "--retag",
        action="store_true",
        help="Re-tag the current version without bumping, useful for re-running a release"
    )
    version_group.add_argument(
        "--version",
        metavar="VERSION",
        help="Specify a specific version to tag (e.g., 1.2.3)"
    )
    
    parser.add_argument("--skip-testpypi", action="store_true", 
                      help="Skip TestPyPI publishing (useful when re-running a release)")
    parser.add_argument("--dry-run", action="store_true", 
                      help="Show actions without executing")

    args = parser.parse_args()

    ensure_clean_git()
    original_branch = get_current_branch()

    # Only allow releases from master
    if original_branch != "master":
        print(f"❌ Current branch is '{original_branch}', but releases are only allowed from 'master'.")
        sys.exit(1)

    # Show version information and get confirmation
    current_version = get_current_version()
    print(f"📋 Current version: {current_version}")
    
    # Calculate and show the next version if bumping
    if args.bump:
        next_version = calculate_next_version(current_version, args.bump)
        print(f"📈 Next version will be: {next_version}")
    elif args.retag:
        print(f"🔄 Re-tagging current version: {current_version}")
    elif args.version:
        print(f"📌 Tagging specific version: {args.version}")
    
    # Show additional options
    if args.skip_testpypi:
        print("⏭️  TestPyPI publish will be skipped")
    
    # Get confirmation for creating release
    if not args.dry_run:
        if not confirm("⚠️ Are you sure you want to create a release?"):
            print("Aborted.")
            sys.exit(0)

    tag = None
    try:
        # Determine which action to take
        if args.bump:
            # Bump version and create tag
            ensure_bump2version_installed()
            tag = bump_version(args.bump, args.dry_run)
            if not args.dry_run:
                run("git push origin master")  # Push the version bump to master
                run(f"git push origin {tag}")  # Push the tag
                if args.skip_testpypi:
                    run(f"gh workflow run release.yml --ref {tag} -f skip_testpypi=true || echo 'Manual workflow trigger failed, but tag push will still trigger workflow'")
            print(f"✅ Bumped version and created tag: {tag}")
            if args.skip_testpypi:
                print("✅ GitHub Actions will skip TestPyPI and request approval for PyPI directly.")
            else:
                print("✅ GitHub Actions will now publish to TestPyPI and request approval for PyPI.")
            
        elif args.retag:
            # Re-tag the current version without bumping
            current_version = get_current_version()
            tag = create_tag_for_version(current_version, args.dry_run)
            skip_arg = "--skip-testpypi" if args.skip_testpypi else ""
            if not args.dry_run:
                run(f"git push origin {tag} --force")  # Force push the tag
                if args.skip_testpypi:
                    run(f"gh workflow run release.yml --ref {tag} -f skip_testpypi=true || echo 'Manual workflow trigger failed, but tag push will still trigger workflow'")
            print(f"✅ Re-tagged current version: {tag}")
            if args.skip_testpypi:
                print("✅ GitHub Actions will skip TestPyPI and request approval for PyPI directly.")
            else:
                print("✅ GitHub Actions will now publish to TestPyPI and request approval for PyPI.")
            
        elif args.version:
            # Tag a specific version
            tag = create_tag_for_version(args.version, args.dry_run)
            if not args.dry_run:
                run(f"git push origin {tag} --force")  # Force push the tag
                if args.skip_testpypi:
                    run(f"gh workflow run release.yml --ref {tag} -f skip_testpypi=true || echo 'Manual workflow trigger failed, but tag push will still trigger workflow'")
            print(f"✅ Tagged specific version: {tag}")
            if args.skip_testpypi:
                print("✅ GitHub Actions will skip TestPyPI and request approval for PyPI directly.")
            else:
                print("✅ GitHub Actions will now publish to TestPyPI and request approval for PyPI.")
            
        else:
            print("No version action requested. To trigger a release, you need to:")
            print("1. Use --bump to bump the version and create a tag")
            print("2. Use --retag to re-use the current version and create/update its tag")
            print("3. Use --version to tag a specific version")
            
    finally:
        # Always return to original branch
        if not args.dry_run and original_branch != get_current_branch():
            run(f"git checkout {original_branch}")


if __name__ == "__main__":
    main()