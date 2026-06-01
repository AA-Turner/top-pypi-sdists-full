#!/usr/bin/env bash
# Capture README screenshots from real eval-harness run artifacts.
#
# Usage:
#   bash scripts/capture-screenshots.sh
#
# Requirements:
#   - Google Chrome installed at the standard macOS path (or override
#     CHROME_BIN).
#   - A completed eval-harness run under
#     evals/results/csp-starter-cfn/<timestamp>/.
#
# This script regenerates docs/screenshots/gap-report-csp-starter.png
# from the latest validation-run output. Run it after any future
# `python -m evals run --fixture evals/fixtures/csp-starter-cfn`
# dispatch to refresh the README hero shot.
#
# v0.1.82 shipped the initial screenshot using the
# evals/results/csp-starter-cfn/20260513T143530Z/ run artifacts (the
# v0.1.81 maintainer-validation baseline at 22/22 = 100/100).

set -euo pipefail

CHROME_BIN="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_ROOT="${REPO_ROOT}/evals/results/csp-starter-cfn"
SCREENSHOTS_DIR="${REPO_ROOT}/docs/screenshots"

mkdir -p "${SCREENSHOTS_DIR}"

if [ ! -x "${CHROME_BIN}" ]; then
  echo "error: Google Chrome not found at ${CHROME_BIN}" >&2
  echo "  install Chrome or override CHROME_BIN to point at the binary." >&2
  exit 1
fi

if [ ! -d "${RESULTS_ROOT}" ]; then
  echo "error: no eval-harness results at ${RESULTS_ROOT}" >&2
  echo "  run first: AWS_PROFILE=bedrock-test uv run python -m evals run \\" >&2
  echo "    --fixture evals/fixtures/csp-starter-cfn" >&2
  exit 1
fi

# Pick the most recent timestamped run directory.
latest_run="$(ls -td "${RESULTS_ROOT}"/*/ 2>/dev/null | head -1)"
if [ -z "${latest_run}" ]; then
  echo "error: no timestamped run directories under ${RESULTS_ROOT}" >&2
  exit 1
fi

reports_dir="${latest_run}workspace/.efterlev/reports"
gap_html="$(ls "${reports_dir}"/gap-*.html 2>/dev/null | tail -1)"
if [ -z "${gap_html}" ]; then
  echo "error: no gap-*.html in ${reports_dir}" >&2
  exit 1
fi

echo "[capture] using ${gap_html}"
"${CHROME_BIN}" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --hide-scrollbars \
  --window-size=1280,800 \
  --screenshot="${SCREENSHOTS_DIR}/gap-report-csp-starter.png" \
  "file://${gap_html}" >/dev/null 2>&1
echo "[capture] wrote ${SCREENSHOTS_DIR}/gap-report-csp-starter.png"
ls -la "${SCREENSHOTS_DIR}/gap-report-csp-starter.png"
