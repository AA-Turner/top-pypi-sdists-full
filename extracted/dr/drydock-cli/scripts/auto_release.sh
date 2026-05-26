#!/bin/bash
# Auto-release DryDock every 6 hours
# Checks if there are new commits since last release, builds, publishes, deploys
set -euo pipefail

export PATH="/home/bobef/miniconda3/bin:$PATH"
PYTHON="/home/bobef/miniconda3/bin/python3"
DRYDOCK="/data3/drydock"
LOCKFILE="$DRYDOCK/.auto_release.lock"

# Pause file: if present, skip auto-release entirely (used during manual debugging)
if [ -f "$DRYDOCK/.pause_auto_release" ]; then
    echo "[$(date)] Auto-release paused via .pause_auto_release file"
    exit 0
fi

# Prevent concurrent runs
if [ -f "$LOCKFILE" ]; then
    pid=$(cat "$LOCKFILE")
    if kill -0 "$pid" 2>/dev/null; then
        exit 0
    fi
    rm -f "$LOCKFILE"
fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

cd "$DRYDOCK"

# Check if there are commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
COMMITS_SINCE=$(git rev-list "$LAST_TAG"..HEAD --count 2>/dev/null || echo "0")

if [ "$COMMITS_SINCE" -eq 0 ]; then
    echo "[$(date)] No new commits since $LAST_TAG. Skipping release."
    exit 0
fi

echo "[$(date)] $COMMITS_SINCE commits since $LAST_TAG. Building release..."

# Syntax check all modified .py files
ERRORS=0
for f in $(git diff --name-only "$LAST_TAG"..HEAD -- '*.py' 2>/dev/null); do
    if [ -f "$f" ]; then
        $PYTHON -c "import ast; ast.parse(open('$f').read())" 2>/dev/null || {
            echo "SYNTAX ERROR: $f"
            ERRORS=$((ERRORS + 1))
        }
    fi
done

if [ "$ERRORS" -gt 0 ]; then
    echo "[$(date)] $ERRORS syntax errors found. Aborting release."
    $PYTHON "$DRYDOCK/scripts/notify_release.py" "release" "Auto-release ABORTED: $ERRORS syntax errors in modified files" 2>/dev/null
    exit 1
fi

# Get current version. Usual path bumps PATCH; DRYDOCK_FORCE_VERSION
# overrides that (used for minor/major bumps like 2.6.x → 2.7.0 where
# PATCH+1 is the wrong arithmetic).
CURRENT=$(grep 'version = ' "$DRYDOCK/pyproject.toml" | head -1 | grep -oP '\d+\.\d+\.\d+')
if [ -n "${DRYDOCK_FORCE_VERSION:-}" ]; then
    if ! echo "$DRYDOCK_FORCE_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "ERROR: DRYDOCK_FORCE_VERSION=$DRYDOCK_FORCE_VERSION is not N.N.N"
        exit 1
    fi
    NEW_VERSION="$DRYDOCK_FORCE_VERSION"
    echo "[$(date)] Forcing $CURRENT -> $NEW_VERSION via DRYDOCK_FORCE_VERSION"
else
    MAJOR=$(echo "$CURRENT" | cut -d. -f1)
    MINOR=$(echo "$CURRENT" | cut -d. -f2)
    PATCH=$(echo "$CURRENT" | cut -d. -f3)
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"
    echo "[$(date)] Bumping $CURRENT -> $NEW_VERSION"
fi

# Update version
sed -i "s/version = \"$CURRENT\"/version = \"$NEW_VERSION\"/" "$DRYDOCK/pyproject.toml"
git add "$DRYDOCK/pyproject.toml"
git commit -m "v$NEW_VERSION: Auto-release (${COMMITS_SINCE} commits)" --no-verify 2>/dev/null || true

# Build
rm -rf dist/
$PYTHON -m build 2>/dev/null

# Publish to PyPI
# PYTHONNOUSERSITE=1 avoids a jaraco.functools circular-import that occurs
# when ~/.local/lib/python3.12/site-packages/setuptools conflicts with the
# miniconda3 vendored copy; set +e so a twine failure doesn't kill the
# script before the local-wheel fallback can run.
PYPI_TOKEN=$(cat ~/.config/drydock/pypi_token)
set +e
TWINE_OUT=$(PYTHONNOUSERSITE=1 $PYTHON -m twine upload dist/drydock_cli-${NEW_VERSION}* -u __token__ -p "$PYPI_TOKEN" 2>&1)
TWINE_EXIT=$?
set -e
echo "[$(date)] twine exit=$TWINE_EXIT: $TWINE_OUT" >> "$DRYDOCK/logs/auto_release.log"

# Deploy to GitHub — NOT silent. If the token is invalid this should scream.
TMPDIR=$(mktemp -d)
GITHUB_TOKEN=$(tr -d '\n' < ~/.config/drydock/github_token)
if ! curl -s -m 10 -o /dev/null -w "%{http_code}" \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        https://api.github.com/user | grep -q "^200$"; then
    echo "[$(date)] ERROR: GitHub token at ~/.config/drydock/github_token is INVALID" >&2
    echo "[$(date)]   Skipping GitHub push. Rotate the token to resume deployment." >&2
    rm -rf "$TMPDIR"
else
    if git clone --depth 1 "https://${GITHUB_TOKEN}@github.com/fbobe321/drydock.git" "$TMPDIR/repo" 2>&1; then
        rsync -a --delete \
            --exclude='.git' --exclude='.github/workflows' --exclude='logs/' \
            --exclude='__pycache__/' --exclude='*.pyc' --exclude='.pytest_cache/' \
            --exclude='*.egg-info/' --exclude='dist/' \
            --exclude='.pause_*' --exclude='log_analyzer/' \
            --exclude='.auto_release.lock' --exclude='.perf_baseline_done' \
            --exclude='.gauntlet_runs/' --exclude='.test_harness_runs/' \
            --exclude='.test_harness_runs_autogoal/' \
            --exclude='.test_harness_runs_baseline/' \
            --exclude='.lifecycle_runs/' --exclude='.stress_runs/' \
            --exclude='.100_projects/' --exclude='.eval_loop/' \
            --exclude='.drydock/' --exclude='.tui_observability/' \
            --exclude='.claude/' --exclude='.venv/' --exclude='.vscode/' \
            --exclude='hle_results/' --exclude='hle_results_iter/' \
            --exclude='medium/' --exclude='test_harness/' \
            --exclude='test_bank_results/' --exclude='baseline_history/' \
            --exclude='research/' --exclude='perf_results/' \
            --exclude='trip_log.md' \
            "$DRYDOCK/" "$TMPDIR/repo/"
        cd "$TMPDIR/repo"
        git remote set-url origin "https://${GITHUB_TOKEN}@github.com/fbobe321/drydock.git"
        git add -A
        # Drop already-tracked paths that match the rsync excludes (the
        # excluded files are still on disk in the clone — rsync --exclude
        # neither copies them in nor deletes them, so `git add -A` keeps
        # them staged). Must run AFTER `git add -A` or the rm-cached
        # removals get re-added by the same `git add -A`. shopt -s
        # nullglob makes `.pause_*` expand to nothing when no sentinels
        # exist instead of leaving a literal `.pause_*` arg.
        ( shopt -s nullglob
          for path in test_bank_results baseline_history research perf_results \
                      hle_results hle_results_iter medium test_harness \
                      trip_log.md .auto_release.lock .perf_baseline_done \
                      .gauntlet_runs .test_harness_runs \
                      .test_harness_runs_autogoal .test_harness_runs_baseline \
                      .lifecycle_runs .stress_runs .100_projects .eval_loop \
                      .drydock .tui_observability .claude .venv .vscode \
                      .pause_*; do
              git ls-files --error-unmatch -- "$path" >/dev/null 2>&1 \
                  && git rm -r --cached --quiet -- "$path" 2>/dev/null || true
          done )
        if git -c user.name="Drydock Deploy" -c user.email="deploy@drydock" \
               commit -m "v$NEW_VERSION: Auto-release"; then
            if git push origin main; then
                echo "[$(date)] GitHub push: OK"
            else
                echo "[$(date)] ERROR: GitHub push FAILED (token may lack write scope)" >&2
            fi
        else
            echo "[$(date)] GitHub commit: no changes (already in sync)"
        fi
        rm -rf "$TMPDIR"
    else
        echo "[$(date)] ERROR: GitHub clone FAILED" >&2
        rm -rf "$TMPDIR"
    fi
fi
cd "$DRYDOCK"

# Install on user's env — try PyPI first, fall back to local wheel
INSTALLED=0
if [ $TWINE_EXIT -eq 0 ]; then
    for i in 1 2 3; do
        sleep 60
        /home/bobef/miniforge3/envs/drydock/bin/pip install --force-reinstall --no-deps --no-cache-dir "drydock-cli==$NEW_VERSION" 2>/dev/null && INSTALLED=1 && break
    done
fi
if [ $INSTALLED -eq 0 ]; then
    # PyPI upload failed or propagation timed out — install from local wheel
    LOCAL_WHEEL="$DRYDOCK/dist/drydock_cli-${NEW_VERSION}-py3-none-any.whl"
    if [ -f "$LOCAL_WHEEL" ]; then
        /home/bobef/miniforge3/envs/drydock/bin/pip install --force-reinstall --no-deps "$LOCAL_WHEEL" 2>/dev/null \
            && echo "[$(date)] Installed v$NEW_VERSION from local wheel (PyPI upload failed)" >> "$DRYDOCK/logs/auto_release.log" \
            || echo "[$(date)] ERROR: local wheel install also failed for v$NEW_VERSION" >> "$DRYDOCK/logs/auto_release.log"
    fi
fi

# Tag
git tag "v$NEW_VERSION" 2>/dev/null || true

# 2026-05-25: Docker Hub publish step. Skips silently when:
#   - docker is not installed on this host (e.g. CI runners without docker)
#   - the credential file at ~/.config/drydock/dockerhub_password is missing
#   - PyPI upload failed (TWINE_EXIT != 0) — don't ship a Docker image of
#     a version that isn't on PyPI
# The credential file should be: chmod 600, owned by the cron user, never
# in git. See install_tests/publish/README.md.
DOCKER_PASS_FILE="$HOME/.config/drydock/dockerhub_password"
DOCKER_USERNAME="${DOCKER_HUB_USERNAME:-fbobe3}"
if [ $TWINE_EXIT -eq 0 ] \
        && command -v docker >/dev/null 2>&1 \
        && [ -f "$DOCKER_PASS_FILE" ] \
        && [ ! -f "$DRYDOCK/.pause_docker_publish" ]; then
    echo "[$(date)] Building Docker image for v$NEW_VERSION" >> "$DRYDOCK/logs/auto_release.log"
    DOCKER_HUB_USERNAME="$DOCKER_USERNAME" \
    DOCKER_HUB_PASSWORD="$(cat "$DOCKER_PASS_FILE")" \
        bash "$DRYDOCK/install_tests/publish/publish.sh" \
        --version "$NEW_VERSION" \
        >> "$DRYDOCK/logs/auto_release.log" 2>&1 \
        && echo "[$(date)] Docker image fbobe3/drydock:$NEW_VERSION pushed" >> "$DRYDOCK/logs/auto_release.log" \
        || echo "[$(date)] ERROR: Docker publish failed for v$NEW_VERSION (see log)" >> "$DRYDOCK/logs/auto_release.log"
elif [ $TWINE_EXIT -ne 0 ]; then
    echo "[$(date)] Skipping Docker publish: PyPI upload failed" >> "$DRYDOCK/logs/auto_release.log"
elif ! command -v docker >/dev/null 2>&1; then
    echo "[$(date)] Skipping Docker publish: docker not installed" >> "$DRYDOCK/logs/auto_release.log"
elif [ ! -f "$DOCKER_PASS_FILE" ]; then
    echo "[$(date)] Skipping Docker publish: credential file $DOCKER_PASS_FILE not present" >> "$DRYDOCK/logs/auto_release.log"
fi

# 2026-05-25: Cloudflare Pages deploy step (fourth target — after PyPI,
# Docker Hub, GitHub). Ships the static landing page at web/ to
# https://drydock.pages.dev/. Skips silently when:
#   - the API token at ~/.config/drydock/cloudflare_token is missing
#   - the account ID at ~/.config/drydock/cloudflare_account_id is missing
#   - the .pause_cloudflare_deploy sentinel is present
#   - web/ has no committed changes since the previous release tag
#     (avoids no-op deploys — Cloudflare dedupes internally, but skipping
#     here keeps the log clean and saves ~10s per release)
# Token rotation: edit cloudflare_token in place; no other config to
# update. The token must have Pages:Edit + Account Settings:Read on the
# specific account whose ID lives in cloudflare_account_id.
CF_TOKEN_FILE="$HOME/.config/drydock/cloudflare_token"
CF_ACCOUNT_FILE="$HOME/.config/drydock/cloudflare_account_id"
# Pin Node 20: wrangler v15+ requires it; this host has both 18 and 20
# via nvm and the cron PATH typically resolves to 18.
NODE20_BIN="$HOME/.nvm/versions/node/v20.20.2/bin"
if [ -f "$CF_TOKEN_FILE" ] \
        && [ -f "$CF_ACCOUNT_FILE" ] \
        && [ ! -f "$DRYDOCK/.pause_cloudflare_deploy" ] \
        && [ -d "$DRYDOCK/web" ]; then
    # Only fire if web/ actually changed since the prior tag.
    PRIOR_TAG=$(git -C "$DRYDOCK" describe --tags --abbrev=0 "v$NEW_VERSION^" 2>/dev/null || echo "")
    WEB_CHANGED=1
    if [ -n "$PRIOR_TAG" ]; then
        if git -C "$DRYDOCK" diff --quiet "$PRIOR_TAG" HEAD -- web/ 2>/dev/null; then
            WEB_CHANGED=0
        fi
    fi
    if [ "$WEB_CHANGED" -eq 1 ]; then
        echo "[$(date)] Deploying web/ to Cloudflare Pages (v$NEW_VERSION)" >> "$DRYDOCK/logs/auto_release.log"
        PATH="$NODE20_BIN:$PATH" \
        CLOUDFLARE_API_TOKEN="$(cat "$CF_TOKEN_FILE")" \
        CLOUDFLARE_ACCOUNT_ID="$(cat "$CF_ACCOUNT_FILE")" \
            wrangler pages deploy "$DRYDOCK/web" \
                --project-name drydock --branch main --commit-dirty=true \
                >> "$DRYDOCK/logs/auto_release.log" 2>&1 \
            && echo "[$(date)] Cloudflare Pages deploy: OK (https://drydock.pages.dev/)" >> "$DRYDOCK/logs/auto_release.log" \
            || echo "[$(date)] ERROR: Cloudflare Pages deploy FAILED (token or account scope?)" >> "$DRYDOCK/logs/auto_release.log"
    else
        echo "[$(date)] Skipping Cloudflare Pages: web/ unchanged since $PRIOR_TAG" >> "$DRYDOCK/logs/auto_release.log"
    fi
elif [ ! -f "$CF_TOKEN_FILE" ]; then
    echo "[$(date)] Skipping Cloudflare Pages: credential file $CF_TOKEN_FILE not present" >> "$DRYDOCK/logs/auto_release.log"
elif [ ! -f "$CF_ACCOUNT_FILE" ]; then
    echo "[$(date)] Skipping Cloudflare Pages: account-id file $CF_ACCOUNT_FILE not present" >> "$DRYDOCK/logs/auto_release.log"
fi

# Notify — include the actual change summaries since last release, not
# just a "N commits" placeholder. Pull each meaningful commit subject
# (skip Bump/Auto-release/Daily sync chatter) and the highest step from
# the most recent stress run.
# Filter out cron-only noise (trip log ticks, version bumps, sync commits).
# `chore(log): trip log tick` is the hourly heartbeat commit and should
# never appear in release notes — it caused noisy Telegram pings when no
# real work shipped between releases.
COMMIT_SUMMARIES=$(git log "$LAST_TAG"..HEAD --pretty=format:'%s' 2>/dev/null \
    | grep -vE '^(Bump version|v[0-9]+\.[0-9]+\.[0-9]+:|Daily sync|Auto-release|chore\(log\): trip log tick)' \
    | head -5)
# If after filtering there's nothing real to announce, skip the release
# entirely. Better to wait for the next 6-hour tick than to publish a
# "release" containing only bot heartbeat noise.
if [ -z "$COMMIT_SUMMARIES" ]; then
    echo "[$(date)] No substantive commits since $LAST_TAG (only filtered noise) — skipping release"
    # Roll back the version bump so the next real commit picks up at this number.
    sed -i "s/version = \"$NEW_VERSION\"/version = \"$CURRENT\"/" "$DRYDOCK/pyproject.toml"
    exit 0
fi
NOTIFY_BODY="$COMMIT_SUMMARIES"

# Append previous stress run progress (matches publish_to_pypi.sh).
# Only when the run is still in flight — once it reaches TOTAL/TOTAL the
# signal is stale (the harness exits and the log freezes), so repeating
# "1658/1658 steps before stopping" across every subsequent release is
# misleading.
LAST_STRESS_LOG=$(ls -1t /tmp/stress_2000_*.log 2>/dev/null | head -1)
if [ -n "$LAST_STRESS_LOG" ]; then
    STRESS_MAX=$(grep -oE '^\[ *[0-9]+/[0-9]+\]' "$LAST_STRESS_LOG" 2>/dev/null \
        | tr -d '[] ' | awk -F/ '{print $1}' | sort -n | tail -1)
    STRESS_TOTAL=$(grep -oE '^\[ *[0-9]+/[0-9]+\]' "$LAST_STRESS_LOG" 2>/dev/null \
        | tr -d '[] ' | awk -F/ '{print $2}' | head -1)
    if [ -n "$STRESS_MAX" ] && [ -n "$STRESS_TOTAL" ] && [ "$STRESS_MAX" -lt "$STRESS_TOTAL" ]; then
        STRESS_LOG_NAME=$(basename "$LAST_STRESS_LOG")
        NOTIFY_BODY="${NOTIFY_BODY}

Stress run (${STRESS_LOG_NAME}) at ${STRESS_MAX}/${STRESS_TOTAL} steps."
    fi
fi

$PYTHON "$DRYDOCK/scripts/notify_release.py" "$NEW_VERSION" "$NOTIFY_BODY" 2>/dev/null

echo "[$(date)] Released v$NEW_VERSION successfully"
