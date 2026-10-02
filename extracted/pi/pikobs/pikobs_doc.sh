#!/usr/bin/env bash
# ============================================================================
# pikobs_doc.sh
# ----------------------------------------------------------------------------
# Regenerate the whole documentation, in one go:
#
#   1. the docstring of every module, from its wrapper and its own code
#   2. the configuration pages: families, varnos, regions
#   3. the example figures, copied from the reference runs
#   4. the HTML
#
# Run it from the root of the repository:
#
#   ./pikobs_doc.sh              everything
#   ./pikobs_doc.sh zone flags   only those modules, then images and HTML
#   ./pikobs_doc.sh --no-images  skip the figures (they take a while)
#   ./pikobs_doc.sh --no-html    stop before make html
#
# A module whose builder is missing is reported and skipped, so a new
# module does not break the run before its documentation exists.
# ============================================================================
set -uo pipefail

# the builders that read the package must see THIS repository, not an
# installed copy: regions would list no polygon and zone would not import
export PYTHONPATH="${PWD}${PYTHONPATH:+:${PYTHONPATH}}"

BUILD_DIR="pikobs/build_doc"
SCRIPTS="pikobs/script"
# whichever of the two names this repository uses
IMAGES="./build_images.sh"
[ -f "${IMAGES}" ] || IMAGES="./pikobs_doc_images.sh"
DOCS="docs"

# module -> the file holding its docstring. A module not listed here has
# no page of its own (infrastructure: obsdb, figures, parallel).
MODULES=(cardio flags histogram mapobs obscountdb profile timeserie
         vdedr verifprofile zone scatter)

do_images=1
do_html=1
wanted=()
for arg in "$@"; do
    case "${arg}" in
        --no-images) do_images=0 ;;
        --no-html)   do_html=0 ;;
        -h|--help)   sed -n '3,22p' "$0"; exit 0 ;;
        *)           wanted+=("${arg}") ;;
    esac
done
[ "${#wanted[@]}" -gt 0 ] && MODULES=("${wanted[@]}")

if [ ! -d "${BUILD_DIR}" ]; then
    echo "ERROR: ${BUILD_DIR} not found: run this from the root of the" \
         "repository." >&2
    exit 1
fi

ok=0; skipped=0; failed=0

run_builder() {   # run_builder <label> <script> <args...>
    local label="$1" script="$2"; shift 2
    if [ ! -f "${script}" ]; then
        echo "  skip  ${label}  (no ${script})"
        skipped=$((skipped + 1))
        return
    fi
    local out
    if out="$(python "${script}" "$@" 2>&1)"; then
        echo "  ok    ${label}  ${out##*$'\n'}"
        ok=$((ok + 1))
    else
        echo "  FAIL  ${label}"
        echo "${out}" | sed 's/^/          /' | tail -5
        failed=$((failed + 1))
    fi
}

# ---- run-time tables -------------------------------------------------------
# What the stats page claims, checked against the code. A module that
# stopped pairing its observations would leave the page saying something
# untrue, and nobody would notice until someone recomputed a number by
# hand. It costs a second.
# The wrappers are what people actually run, and an option a module no
# longer has stops the run on its first line. Cheap to check here.
if [ -f "${BUILD_DIR}/check_wrappers.py" ]; then
    echo "wrappers:"
    python "${BUILD_DIR}/check_wrappers.py" "${SCRIPTS}" | sed 's/^/  /'
fi

if [ -f "${BUILD_DIR}/verify_tests.py" ]; then
    echo "significance tests:"
    if python "${BUILD_DIR}/verify_tests.py" pikobs | sed 's/^/  /'; then
        :
    else
        echo "  the stats page no longer matches the code" >&2
        failed=$((failed + 1))
    fi
fi

# Every module against the shared conventions -- the defaults of LAND_OCEAN
# and SPECIAL_COLUMN in wrappers and argparse, no retired special-column
# function, the land mask of mapobs equal to the SQL one: the static half of
# check_modules.py, a few seconds. Its runs are check_modules.py --submit.
if [ -f "${BUILD_DIR}/check_modules.py" ]; then
    echo "module conventions:"
    if out=$(python "${BUILD_DIR}/check_modules.py" --static 2>&1); then
        rc=0
    else
        rc=$?
    fi
    printf '%s\n' "$out" | sed -n '/ checks, /,$p' | sed 's/^/  /'
    if [ "$rc" -ne 0 ]; then
        echo "  a module left the shared conventions:" \
             "python ${BUILD_DIR}/check_modules.py --static" >&2
        failed=$((failed + 1))
    fi
fi

echo "docstrings:"
for m in "${MODULES[@]}"; do
    module_file="pikobs/${m}/${m}.py"
    [ -f "${module_file}" ] || { echo "  skip  ${m}  (no ${module_file})"
                                 skipped=$((skipped + 1)); continue; }
    run_builder "${m}" "${BUILD_DIR}/build_${m}.py" \
                "${module_file}" "${SCRIPTS}"
done

# the configuration pages are not modules: families and varnos come from
# one builder, the regions from another
if [ "${#wanted[@]}" -eq 0 ]; then
    echo "configuration:"
    # the varnos each family carries, read in the files every time (a new
    # one shows up by itself); without the files, the CSV of the repository
    # stays, and the search is rebuilt from it
    if out="$(python "${BUILD_DIR}/make_varno_csv.py" 2>&1)"; then
        echo "  varnos  ${out#\[varno\] }"
    else
        echo "  varnos  kept: ${out##*\] }"
    fi
    python "${BUILD_DIR}/make_varno_search.py" 2>&1 | tail -1 | sed "s/^/  search  /"
    run_builder "families, varnos" "${BUILD_DIR}/build_config.py" \
                "pikobs/configobs"
    run_builder "regions" "${BUILD_DIR}/build_regions.py" \
                "pikobs/configobs/regionsobs.py"
fi

if [ "${do_images}" -eq 1 ]; then
    echo "figures:"
    if [ -x "${IMAGES}" ]; then
        bash "${IMAGES}" | sed 's/^/  /'
    else
        echo "  skip  ${IMAGES} not found or not executable"
    fi
fi

if [ "${do_html}" -eq 1 ]; then
    echo "html:"
    if [ -d "${DOCS}" ]; then
        # Not a pipe: grep leaves early, make writes into a pipe that
        # is already closed, and that broken pipe used to be reported as
        # "Error 2" on a build that had in fact succeeded.
        # make clean empties build/, so the log can only be created
        # after it, not before
        log="${DOCS}/build/sphinx.log"
        (cd "${DOCS}" && make clean > /dev/null 2>&1 \
            && mkdir -p build && make html > build/sphinx.log 2>&1)
        html_status=$?
        grep -E "warning|WARNING|build succeeded|ERROR|Error" "${log}" \
            | sed 's/^/  /'
        if [ "${html_status}" -ne 0 ]; then
            echo "  FAILED -- the whole log is in ${log}"
            failed=$((failed + 1))
        fi
    else
        echo "  skip  ${DOCS} not found"
    fi
fi

echo "----------------------------------------------------------------"
echo "${ok} built, ${skipped} skipped, ${failed} failed"
[ "${do_html}" -eq 1 ] && [ -d "${DOCS}" ] && \
    echo "open ${DOCS}/build/html/index.html"
exit $((failed > 0))
