#!/usr/bin/env bash
# Release script for textcharts.
#
# Usage:
#   ./scripts/release.sh              # release current dev branch, auto-increment patch
#   ./scripts/release.sh 0.2.0        # release current dev branch, next cycle = 0.2.0
#
# Steps performed:
#   1. Validate preconditions (on dev-* branch, clean tree, gh auth)
#   2. Open PR: dev-X.Y.Z -> main
#   3. Squash-merge the PR
#   4. Tag the merge commit on main
#   5. Push the tag (triggers CI: PyPI publish + docs deploy)
#   6. Create next dev branch with bumped version
set -euo pipefail

# --- helpers ----------------------------------------------------------------

die()  { echo "error: $*" >&2; exit 1; }
info() { echo "==> $*"; }
ask()  { read -rp "$* [y/N] " ans; [[ "$ans" =~ ^[Yy] ]] || die "aborted"; }

# Increment patch version: 0.1.0 -> 0.1.1
bump_patch() {
    local IFS=.
    read -r major minor patch <<< "$1"
    echo "${major}.${minor}.$((patch + 1))"
}

# --- preconditions ----------------------------------------------------------

branch=$(git branch --show-current)
[[ "$branch" == dev-* ]] || die "not on a dev-* branch (current: $branch)"

current_version="${branch#dev-}"
info "releasing v${current_version} from branch ${branch}"

# Validate version consistency
toml_version=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
init_version=$(python3 -c "import re; print(re.search(r'__version__ = \"(.+)\"', open('src/textcharts/__init__.py').read()).group(1))")
[[ "$toml_version" == "$current_version" ]] || die "pyproject.toml version ($toml_version) != branch version ($current_version)"
[[ "$init_version" == "$current_version" ]] || die "__init__.py version ($init_version) != branch version ($current_version)"

# Lint (auto-fix then verify)
info "running ruff auto-fix and lint check"
uv run --group dev -- ruff check --fix src/ tests/ || true
uv run --group dev -- ruff check src/ tests/ || die "lint errors remain after auto-fix — resolve manually"

# Clean working tree
if [[ -n "$(git status --porcelain)" ]]; then
    info "lint fixes applied — committing"
    git add -u
    git commit -m "style: auto-fix lint errors"
fi

# gh CLI authenticated
gh auth status >/dev/null 2>&1 || die "gh CLI not authenticated — run 'gh auth login'"

# Determine next version
next_version="${1:-$(bump_patch "$current_version")}"
info "next development cycle: v${next_version}"

ask "proceed with release v${current_version} and next cycle dev-${next_version}?"

# --- release ----------------------------------------------------------------

# Push latest changes
info "pushing ${branch} to origin"
git push origin "$branch"

# Open PR (or reuse existing)
info "opening PR: ${branch} -> main"
if pr_url=$(gh pr view "$branch" --json url --jq .url 2>/dev/null); then
    info "using existing PR: ${pr_url}"
else
    pr_url=$(gh pr create \
        --base main \
        --head "$branch" \
        --title "release: v${current_version}" \
        --body "$(cat <<BODY
## Release v${current_version}

Squash-merge of \`${branch}\` into \`main\`.

See [CHANGELOG.md](https://github.com/joeharris76/textcharts/blob/${branch}/CHANGELOG.md) for details.
BODY
)") || die "failed to create PR"
fi
info "PR: ${pr_url}"

# Squash-merge
ask "squash-merge the PR now?"
info "squash-merging PR"
gh pr merge "$branch" --squash --delete-branch=false

# Tag
info "tagging v${current_version} on main"
git switch main
git pull origin main
git tag "v${current_version}"
git push origin "v${current_version}"
info "tag v${current_version} pushed — CI will publish to PyPI and deploy docs"

# --- next cycle -------------------------------------------------------------

ask "create dev-${next_version} branch and bump version?"

info "creating dev-${next_version} from main"
git switch -c "dev-${next_version}" main

# Bump version in both files
sed -i '' "s/^version = \".*\"/version = \"${next_version}\"/" pyproject.toml
sed -i '' "s/^__version__ = \".*\"/__version__ = \"${next_version}\"/" src/textcharts/__init__.py

# Add Unreleased section to CHANGELOG.md
sed -i '' "/^## \[${current_version}\]/i\\
## [Unreleased]\\
\\
" CHANGELOG.md

git add pyproject.toml src/textcharts/__init__.py CHANGELOG.md
git commit -m "chore: start v${next_version} development cycle"
git push -u origin "dev-${next_version}"

info "done! now on dev-${next_version}"
echo ""
echo "  release:  v${current_version} tagged and publishing via CI"
echo "  next:     dev-${next_version} branch ready for development"
echo "  monitor:  gh run list --branch main"
