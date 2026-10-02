#!/usr/bin/env bash
# ============================================================================
# refresh_doc.sh -- run the reference runs of some modules, refresh the
# figures of their pages, rebuild the documentation, and (on request)
# commit and push the result.
#
#   ./refresh_doc.sh zone                 # one module
#   ./refresh_doc.sh zone cardio          # several
#   ./refresh_doc.sh                      # all of them (about an hour)
#   ./refresh_doc.sh --push zone          # same, then commit + push
#
# Run it from a compute node (qsub -I ... -lwalltime=4:0:0): the reference
# runs use 80 workers, and a login node is not the place for that.
#
# The viewers need nothing more: they live under ~/sites8, which the web
# server shows as is, so they are live the moment a run ends. What this
# script adds is the figures inside the .rst pages and the rebuilt HTML.
#
# To also copy the HTML somewhere (a web folder), set PUBLISH_DIR:
#   PUBLISH_DIR=/path/to/web/pikobs_doc ./refresh_doc.sh zone
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
PUSH=0
MODULES=()
for arg in "$@"; do
    case "$arg" in
        --push)    PUSH=1 ;;
        -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
        *)         MODULES+=("$arg") ;;
    esac
done

case "$(hostname)" in
    *login*) echo "[refresh] this is a login node ($(hostname)); open a" \
                  "compute node first: qsub -I -lselect=1:ncpus=80:mem=200gb" \
                  "-lwalltime=4:0:0" >&2
             exit 1 ;;
esac

LOG="${REPO}/refresh_doc_$(date +%Y%m%d_%H%M).log"
echo "[refresh] modules: ${MODULES[*]:-all}"
echo "[refresh] full log: ${LOG}"

# ---- 1. reference runs (foreground: the next steps need their output) ----
cd "${REPO}/pikobs/script" || exit 1
./run_doc_examples.sh "${MODULES[@]}" 2>&1 | tee "${LOG}" \
    | grep --line-buffered -E "^\[pikobs\] [a-z]+:|done:|FAILED|Traceback"
if grep -q "FAILED" "${LOG}"; then
    echo "[refresh] a run failed -- see ${LOG}; stopping before the docs" >&2
    grep -E "FAILED" "${LOG}" | tail -3 >&2
    exit 1
fi
if ! grep -q "done:" "${LOG}"; then
    echo "[refresh] the runs did not finish (walltime?) -- see ${LOG}" >&2
    exit 1
fi

# ---- 2. figures into the pages -------------------------------------------
cd "${REPO}" || exit 1
echo "[refresh] copying figures"
./build_images.sh >> "${LOG}" 2>&1
grep -E "^\s+(skip|FAIL)" "${LOG}" | tail -20 || true

# ---- 3. tables, docstrings, checks, HTML ---------------------------------
echo "[refresh] rebuilding the documentation"
./pikobs_doc.sh >> "${LOG}" 2>&1
summary="$(grep -E "built, .* skipped, .* failed" "${LOG}" | tail -1)"
echo "[refresh] ${summary:-no build summary -- see ${LOG}}"
case "$summary" in
    *" 0 failed"*) ;;
    *) echo "[refresh] the build reported failures; not publishing" >&2
       exit 1 ;;
esac

# ---- 4. optional: copy the HTML to a web folder ---------------------------
if [ -n "${PUBLISH_DIR:-}" ]; then
    echo "[refresh] publishing HTML to ${PUBLISH_DIR}"
    mkdir -p "${PUBLISH_DIR}"
    rsync -a --delete "${REPO}/docs/build/html/" "${PUBLISH_DIR}/"
fi

# ---- 5. optional: commit and push ----------------------------------------
# Only what the doc build rewrites: docs/ and the modules' docstrings.
# pikobs/script is left out on purpose -- personal edits to a wrapper
# (dates, paths) must never ride along.
echo "[refresh] changed files:"
git status --short -- docs pikobs ':!pikobs/script'
if [ "${PUSH}" -eq 1 ]; then
    git add -u -- docs pikobs ':!pikobs/script'
    if git diff --cached --quiet; then
        echo "[refresh] nothing to commit"
    else
        git commit -m "Docs: refresh ${MODULES[*]:-all modules}"
        git push
    fi
else
    echo "[refresh] not committed; run again with --push, or commit by hand"
fi
echo "[refresh] done"
