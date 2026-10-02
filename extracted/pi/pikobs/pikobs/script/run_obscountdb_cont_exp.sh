#!/usr/bin/env bash
# ============================================================================
# run_obscountdb_cont_exp.sh
# ----------------------------------------------------------------------------
# pikobs.obscountdb: volume of observations, control vs experience.
# One run covers every region and every flag criteria listed below; the HTML
# report lets you switch between them.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_obscountdb_cont_exp.sh
#        chmod +x run_obscountdb_cont_exp.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=256:mem=650gb,place=scatter:excl -lwalltime=6:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_obscountdb_cont_exp.sh
#
# List settings are bash ARRAYS: FAMILY=(ai sw), not FAMILY="ai sw".
# ============================================================================
# ----------------------------------------------------------------------------
# Control against experience: every experience listed below is compared
# with the control, observation by observation where the module can, and
# the figures show the difference and what the tests make of it. Use
# run_obscountdb_exp.sh to draw a run on its own.
# ----------------------------------------------------------------------------
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Runs ------------------------------------------------------------------
# Directories with the 6-h SQLite files YYYYMMDDHH_<family>.
PATH_CONTROL_FILES="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
CONTROL_NAME="Control"
PATH_EXPERIENCE_FILES="/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
EXPERIENCE_NAME="Experience"

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). Under /home/<user>/sites8 the report is
# served at https://goc-dx-u3.science.gc.ca/~<user>/sites8/<dir>/
PATHWORK="/home/${USER}/sites8/pikobs_obscountdb_cont_exp"

# ---- Period ----------------------------------------------------------------
# YYYYMMDDHH, UTC, both ends included, one file every 6 h. The run stops
# before doing anything if a single 6-h file is missing.
#
# Leave both empty to work backwards from today, which is what a daily
# run wants: a source that only keeps the last days has nothing older,
# and the newest cycles may not be written yet.
DATESTART=""
DATEEND=""

# Used only when the two above are empty. DAYS_BACK_END is how far back
# the last cycle sits (1 or more, so the day is complete); WINDOW_DAYS is
# how many days the window covers.
DAYS_BACK_END=3
WINDOW_DAYS=5

# ---- Selection -------------------------------------------------------------
# Regions and criteria are computed in ONE pass over the input files, so
# adding more of them costs almost nothing. Both become selectors in the
# report.
REGION=(Monde HemisphereNord HemisphereSud Tropiques Canada)
FLAGS_CRITERIA=(assimilee rejets_qc)

FAMILY=(ai sw sf ua to_amsua_allsky iasi cris atms)

# ---- Options ---------------------------------------------------------------
# Departure panels in the station time series: omp, oma, or both. Each
# metric adds two rows to every station plot: mean and std per cycle, then
# min and max per cycle. Empty disables them and makes the run faster.
AGR=(oma omp)

# Also write every figure as SVG next to the PNG, for editing before a
# presentation (Inkscape, Illustrator): on / off. The viewer always uses
# the PNG. An SVG keeps every element, so ask for it on a small selection.
SVG="off"

# ---- Parallelism -----------------------------------------------------------
N_CPUS=80

# ---- Resolve the period ----------------------------------------------------
# date -u: the cycles are UTC, and near midnight local time a plain date
# would land on the wrong day.
if [ -z "${DATESTART}" ] || [ -z "${DATEEND}" ]; then
    [ -z "${DATEEND}" ] && \
        DATEEND="$(date -u -d "${DAYS_BACK_END} days ago" +%Y%m%d)18"
    [ -z "${DATESTART}" ] && \
        DATESTART="$(date -u -d "$((DAYS_BACK_END + WINDOW_DAYS)) days ago" +%Y%m%d)00"
    echo "[wrapper] period resolved from today: ${DATESTART} .. ${DATEEND}"
fi

# ============================================================================
# 2. SYSTEM SETUP (do not edit below this line)
# ============================================================================
# the folder qsub was called from, when this node can see it: a session
# opened from /tmp on a login node points to a folder this node lacks
if [ -n "${PBS_O_WORKDIR}" ]; then
    if [ -d "${PBS_O_WORKDIR}" ]; then
        cd "${PBS_O_WORKDIR}"
    else
        echo "[wrapper] ${PBS_O_WORKDIR} is not reachable from $(hostname); staying in $(pwd)"
    fi
fi
source /home/${USER}/pikobs_install/load_pikobs.sh

OPTIONAL_ARGS=()
if [ "${#AGR[@]}" -gt 0 ]; then
    OPTIONAL_ARGS+=(--agr "${AGR[@]}")
fi

# ============================================================================
# 3. EXECUTION
# ============================================================================
python -c 'import pikobs; pikobs.obscountdb.arg_call()'             \
       --path_control_files    "${PATH_CONTROL_FILES}"              \
       --control_name          "${CONTROL_NAME}"                    \
       --path_experience_files "${PATH_EXPERIENCE_FILES}"           \
       --experience_name       "${EXPERIENCE_NAME}"                 \
       --pathwork              "${PATHWORK}"                        \
       --datestart             "${DATESTART}"                       \
       --dateend               "${DATEEND}"                         \
       --region                "${REGION[@]}"                       \
       --family                "${FAMILY[@]}"                       \
       --flags_criteria        "${FLAGS_CRITERIA[@]}"               \
       --svg                   "${SVG}"                             \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"

REPORT="${PATHWORK}/pikobs_obscountdb_viewer.html"
echo "Report: ${REPORT}"
case "${PATHWORK}" in
    /home/${USER}/sites8/*)
        echo "Web:    to open it in a browser, link the folder under public_html once:"
        echo "          ln -s ${PATHWORK} /home/${USER}/public_html/"
        echo "        then: https://goc-dx-u3.science.gc.ca/~${USER}/$(basename "${PATHWORK}")/pikobs_obscountdb_viewer.html"
        ;;
esac
