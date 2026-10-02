#!/usr/bin/env bash
# ============================================================================
# run_doc_examples.sh
# ----------------------------------------------------------------------------
# The reference runs of the documentation: the operational suite as the
# control and the parallel one as the experience, one viewer per module,
# all over the same days. Scatter has had a pair of live examples on its
# page for a while and they are what people actually click on; this gives
# every module the same.
#
# It does not repeat each module's arguments. It copies the module's own
# wrapper, rewrites the handful of settings that make it a reference run
# -- the two suites, the period, the output directory, the families --
# and runs that. So a wrapper that gains an option keeps working here
# without anyone remembering to update this file.
#
#   ./run_doc_examples.sh                 asks which modules to run again
#   ./run_doc_examples.sh zone histogram  only those
#   ./run_doc_examples.sh all             every module -- only when asked
#   ./run_doc_examples.sh --dry-run zone  show what would run
#
# A reference is a page people click on: it is run again on purpose,
# one module at a time, never all of them by accident.
#
# Open a compute node first: several modules read every 6-h file of the
# period in parallel.
#
#   qsub -I -lselect=1:ncpus=80:mem=200gb -lwalltime=3:0:0
# ============================================================================
set -uo pipefail

# ---- The two suites --------------------------------------------------------
CONTROL_PATH="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
CONTROL_LABEL="G0"
EXPERIENCE_PATH="/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
EXPERIENCE_LABEL="G2"

# ---- The period ------------------------------------------------------------
# Five days ending three days ago: long enough for the tests to have
# something to say, short enough to redo in an afternoon.
DAYS_BACK_END=3
WINDOW_DAYS=5
DATESTART=""
DATEEND=""

# ---- Where the viewers go --------------------------------------------------
# Under sites8 so each one has a web address to put in the documentation.
USER="${USER:-$(id -un)}"
BASE="/home/${USER}/sites8/pikobs_doc"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
N_CPUS=80

# ---- What each module runs on ----------------------------------------------
# Kept small on purpose: a page wants a figure that can be read, not every
# family of the system.
families_of () {
    case "$1" in
        timeserie)    echo "sw ua iasi" ;;
        histogram)    echo "sw ua" ;;
        profile)      echo "iasi cris csr atms_allsky ssmis mwhs2 mwhs2_rars to_amsua_allsky to_amsua_allsky_rars to_amsub_allsky to_amsub_allsky_rars ua sw" ;;
        zone)         echo "ro sw iasi" ;;
        verifprofile) echo "ua ro ch" ;;
        vdedr)        echo "iasi" ;;
        obscountdb)   echo "to_amsua_allsky iasi" ;;
        cardio)       echo "iasi cris csr atms_allsky ssmis mwhs2 mwhs2_rars to_amsua_allsky to_amsua_allsky_rars to_amsub_allsky to_amsub_allsky_rars" ;;
        scatter)      echo "ro sw iasi" ;;
        *)            echo "sw" ;;
    esac
}

# A few settings a page needs and a daily run does not: the histogram
# page wants the split by flag combination and both criteria, timeserie
# the paired comparison. Anything not named here keeps whatever the
# wrapper says.
extras_of () {
    case "$1" in
        histogram) echo "QC_SPLIT=on FLAGS_CRITERIA=all assimilee" ;;
        profile)   echo "ID_STN=join REGION=Monde Tropiques Canada hrdps FLAGS_CRITERIA=assimilee SPECIAL_COLUMN=on" ;;
        scatter)   echo "ID_STN=join PRESSURE_LAYERS=1100 850 500 250 100 10 1 0 HEIGHT_LAYERS=0 5 10 20 30 40 60 100 CHANNEL=join 32 33 PROJECTION=cyl robinson npolar canada REGION=Monde Tropiques hrdps Boreal_CLIM" ;;
        timeserie) echo "MATCH=on FONCTION=omp oma ID_STN=join CHANNEL=join REGION=Monde Tropiques Canada hrdps" ;;
        verifprofile) echo "FONCTION=oma FLAGS_CRITERIA=assimilee ID_STN=join REGION=Monde Tropiques Canada hrdps" ;;
        zone)      echo "ID_STN=join REGION=Monde Tropiques hrdps Boreal_CLIM CHANNEL=all 32 FONCTION=omp oma SPECIAL_COLUMN=on" ;;
        cardio)    echo "CHANNEL=join all ID_STN=join" ;;
        *)         echo "" ;;
    esac
}

# vdedr is not in the list: between G0 and G2 its O-P is the same
# everywhere, and its reference would show nothing. It compares a summer
# experiment with its control instead, made by hand:
#
#   E=~lco000/data_maestro/ppp8/maestro_archives/OSEE25ALLOBS200_sel4/monitoring/banco/postalt
#   C=/home/sprj700/data_maestro/ppp8/maestro_archives/G2FC910V1E25/monitoring/banco/postalt
#   python pikobs/build_doc/mod_run.py vdedr ref 'FAMILY=(iasi)' \
#       "PATH_CONTROL_FILES=$C" 'CONTROL_NAME=G2FC910V1E25' \
#       "PATH_EXPERIENCE_FILES=($E)" 'EXPERIENCE_NAME=(OSEE25ALLOBS200_sel4)' \
#       'DATESTART=2025061500' 'DATEEND=2025062818'
#   then publish ~/sites8/vdedr_ref as ~/sites8/pikobs_doc_vdedr
MODULES=(timeserie histogram profile zone verifprofile cardio
         obscountdb scatter flags mapobs)

DRY=0
WANTED=()
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY=1 ;;
        -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
        *)         WANTED+=("$arg") ;;
    esac
done
# which modules: the ones named, "all" for every one, and none by
# default -- at a terminal it asks; without one (a PBS job) it stops
ALL_MODULES=("${MODULES[@]}")
if [ ${#WANTED[@]} -eq 0 ]; then
    if [ -t 0 ]; then
        echo "[doc] modules: ${ALL_MODULES[*]}"
        read -r -p "[doc] which to run again (names, or all)? " -a WANTED
    fi
    if [ ${#WANTED[@]} -eq 0 ]; then
        echo "[doc] no module chosen, nothing run. Name them:" \
             "$0 zone histogram, or $0 all" >&2
        exit 1
    fi
fi
if [ "${WANTED[*]}" != "all" ]; then
    for m in "${WANTED[@]}"; do
        case " ${ALL_MODULES[*]} " in
            *" ${m} "*) ;;
            *) echo "[doc] unknown module: ${m} (modules: ${ALL_MODULES[*]})" >&2; exit 1 ;;
        esac
    done
    MODULES=("${WANTED[@]}")
fi

# ---- Resolve the period ----------------------------------------------------
# date -u: the cycles are UTC, and near midnight local time a plain date
# would land on the wrong day.
[ -z "${DATEEND}" ] && \
    DATEEND="$(date -u -d "${DAYS_BACK_END} days ago" +%Y%m%d)18"
[ -z "${DATESTART}" ] && \
    DATESTART="$(date -u -d "$((DAYS_BACK_END + WINDOW_DAYS)) days ago" +%Y%m%d)00"

echo "[doc] control    ${CONTROL_LABEL} = ${CONTROL_PATH}"
echo "[doc] experience ${EXPERIENCE_LABEL} = ${EXPERIENCE_PATH}"
echo "[doc] period     ${DATESTART} .. ${DATEEND}"
echo "[doc] modules    ${MODULES[*]}"
echo

TMP="$(mktemp -d "${TMPDIR:-/tmp}/pikobs_doc_runs.XXXXXX")"
trap 'rm -rf "${TMP}"' EXIT

# Rewrite one setting of a wrapper, whatever form it takes: a plain
# assignment or a bash array.
set_value () {   # set_value <file> <name> <value>
    local file="$1" name="$2" value="$3"
    if grep -qE "^${name}=\(" "$file"; then
        sed -i -E "s|^${name}=\(.*|${name}=(${value})|" "$file"
    elif grep -qE "^${name}=" "$file"; then
        sed -i -E "s|^${name}=.*|${name}=\"${value}\"|" "$file"
    else
        return 1
    fi
}

OK=(); FAILED=(); SKIPPED=()

# What each module runs: its comparison wrapper, its single-run wrapper,
# or the plain one when it has no pair. A module that cannot compare
# (flags, mapobs) does the single run; one that can only compare (vdedr,
# obscountdb) does that one; the rest do both. The wrappers that exist
# decide, so nothing has to be kept in step by hand.
jobs_of () {   # jobs_of <module>  ->  "<wrapper>|<suffix>" per line
    local m="$1"
    local found=0
    if [ -f "${SCRIPT_DIR}/run_${m}_cont_exp.sh" ]; then
        echo "${SCRIPT_DIR}/run_${m}_cont_exp.sh|"
        found=1
    fi
    if [ -f "${SCRIPT_DIR}/run_${m}_exp.sh" ]; then
        echo "${SCRIPT_DIR}/run_${m}_exp.sh|_exp"
        found=1
    fi
    [ "${found}" = "0" ] && [ -f "${SCRIPT_DIR}/run_${m}.sh" ] && \
        echo "${SCRIPT_DIR}/run_${m}.sh|"
    return 0
}

for module in "${MODULES[@]}"; do
  jobs="$(jobs_of "$module")"
  if [ -z "${jobs}" ]; then
      echo "[doc] ${module}: no wrapper found, skipped"
      SKIPPED+=("$module"); continue
  fi
  while IFS='|' read -r src suffix; do
    [ -z "$src" ] && continue
    tag="${module}${suffix}"

    work="${BASE}_${tag}"
    run="${TMP}/run_${tag}.sh"
    cp "$src" "$run"

    # the single-run wrapper keeps its control empty: that is what makes
    # it a single run
    if [ -z "${suffix}" ] && grep -q "PATH_CONTROL_FILES" "$run"; then
        set_value "$run" PATH_CONTROL_FILES "${CONTROL_PATH}"       || true
        set_value "$run" CONTROL_NAME       "${CONTROL_LABEL}"      || true
    fi
    set_value "$run" PATH_EXPERIENCE_FILES "${EXPERIENCE_PATH}"     || true
    set_value "$run" EXPERIENCE_NAME       "${EXPERIENCE_LABEL}"    || true
    set_value "$run" PATHWORK              "${work}"                || true
    set_value "$run" DATESTART             "${DATESTART}"           || true
    set_value "$run" DATEEND               "${DATEEND}"             || true
    set_value "$run" FAMILY                "$(families_of "$module")" || true
    set_value "$run" N_CPUS                "${N_CPUS}"              || true

    # the per-page extras: NAME=value, the value running to the next
    # NAME= or the end, so a list can be written plainly
    extras="$(extras_of "$module")"
    if [ -n "$extras" ]; then
        python3 - "$run" "$extras" <<'PY'
import re, sys
path, extras = sys.argv[1], sys.argv[2]
pairs = re.findall(r'(\w+)=([^=]*?)(?=\s+\w+=|$)', extras)
src = open(path).read()
for name, value in pairs:
    value = value.strip()
    if re.search(rf'^{name}=\(', src, re.M):
        src = re.sub(rf'^{name}=\(.*', f'{name}=({value})', src, count=1,
                     flags=re.M)
    elif re.search(rf'^{name}=', src, re.M):
        src = re.sub(rf'^{name}=.*', f'{name}="{value}"', src, count=1,
                     flags=re.M)
open(path, 'w').write(src)
PY
    fi
    chmod +x "$run"

    echo "=============================================================="
    echo " ${tag}: $(families_of "$module")  ->  ${work}"
    echo "        $(basename "$src")"
    echo "=============================================================="
    if [ "$DRY" = "1" ]; then
        grep -E "^(PATH_CONTROL_FILES|CONTROL_NAME|PATH_EXPERIENCE_FILES|EXPERIENCE_NAME|PATHWORK|DATESTART|DATEEND|FAMILY|N_CPUS|QC_SPLIT|MATCH|FLAGS_CRITERIA|ID_STN|PRESSURE_LAYERS|HEIGHT_LAYERS|CHANNEL|PROJECTION|REGION)=" "$run"
        echo
        continue
    fi

    if "$run"; then
        OK+=("$tag")
    else
        echo "[doc] ${tag}: FAILED, see above" >&2
        FAILED+=("$tag")
    fi
    echo
  done <<< "${jobs}"
done

[ "$DRY" = "1" ] && exit 0

echo "=============================================================="
echo " reference runs"
echo "=============================================================="
printf '  done:    %s\n' "${OK[*]:-none}"
[ ${#SKIPPED[@]} -gt 0 ] && printf '  skipped: %s\n' "${SKIPPED[*]}"
[ ${#FAILED[@]} -gt 0 ] && printf '  FAILED:  %s\n' "${FAILED[*]}"
echo
echo "The addresses to put in the documentation:"
for module in "${OK[@]}"; do
    v=$(ls "${BASE}_${module}"/*viewer*.html \
           "${BASE}_${module}"/index.html \
           "${BASE}_${module}"/Full_Report*.html 2>/dev/null | head -1)
    [ -z "$v" ] && continue
    echo "  ${module}: https://goc-dx-u3.science.gc.ca/~${USER}/${v#/home/${USER}/}"
done
echo
echo "Figures for the pages are picked from these directories by"
echo "pikobs_doc_images.sh; run it next if you want the .rst images"
echo "refreshed as well."
