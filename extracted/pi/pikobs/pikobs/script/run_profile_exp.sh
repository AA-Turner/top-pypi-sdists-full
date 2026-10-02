#!/usr/bin/env bash
# ============================================================================
# run_profile_exp.sh
# ----------------------------------------------------------------------------
# pikobs.profile: vertical profiles -- bias,
# sigma, assigned observation error and number of observations, level by
# level.
#
# One figure per run, on the same axes; with a control, one more figure per
# experience with the change and the tests, matched observation by
# observation.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_exp.sh
#        chmod +x run_profile_exp.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_profile_exp.sh
#
# List settings are bash ARRAYS: FAMILY=(iasi cris), not FAMILY="iasi cris".
# ============================================================================
# ----------------------------------------------------------------------------
# One run on its own: every experience listed below gets its own figures,
# with no control and no difference. Use run_profile_cont_exp.sh to
# compare them against a reference.
# ----------------------------------------------------------------------------
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Control (optional) ----------------------------------------------------
# With a control, every experience gets one more figure: the change of
# the bias and of the sigma, level by level, matched observation by
# observation, with the tests of pikobs.stats.
# Leave it empty for the profile of each run on its own.
PATH_CONTROL_FILES=""
CONTROL_NAME="control"

# ---- Experiences -----------------------------------------------------------
# One directory per experience, one name per directory, same order.
# Directory containing the SQLite observation databases (YYYYMMDDHH_<family>).
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/${USER}/sites8/pikobs_profile_exp"

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
# Regions and criteria are computed in ONE pass, so adding more of them
# costs almost nothing. Both become selectors in the viewer.
REGION=(Monde HemisphereNord HemisphereSud Tropiques Canada)

# Land filter, one series of figures each: all (no filter), land, ocean.
# land and ocean read the land mask; all does not, and costs nothing.
LAND_OCEAN=(all)

# The special column of a family, one series of figures per value: the
# wind computation method of sw. The radar is always split by elevation.
# off (default): everything together.
SPECIAL_COLUMN="off"
FLAGS_CRITERIA=(assimilee)

FAMILY=(ua ai)

# Which departure to look at: omp, oma. One figure each.
FONCTION=(omp)



# A level resting on fewer observations than this is dropped.
MIN_OBS=30

# Station grouping, one series of figures per token:
#   join        every station merged
#   all         one figure per station
#   METOP       stations whose id starts with METOP
#   =NOAA-20    exactly that station
#   C%          SQL LIKE pattern
ID_STN=(join)


# Optional varno list; empty = the family default.
VARNOS=()

# Match the observations of the two runs before comparing: with a
# control, "on" keeps only what both runs hold and tests the change pair
# by pair, which is what sees a small systematic change; "off" lets each
# run keep all its observations and falls back on the independent tests.
# On is the normal mode; turn it off when the matching is the slow part
# of the run and you only want the curves.
MATCH="on"

# Also write every figure as SVG next to the PNG, for editing before a
# presentation (Inkscape, Illustrator): on / off. The viewer always uses
# the PNG. An SVG keeps every element, so ask for it on a small selection.
SVG="off"

# ---- Parallelism -----------------------------------------------------------
N_CPUS=80

# ---- Resolve the period ----------------------------------------------------
# date -u: the cycles are UTC, and near midnight local time a plain date
# would land on the wrong day.
# the error curves beside the OBS_ERROR of the files, always drawn:
# desroziers, and on radar model and model_fit
ERROR_CURVES=()
# radar: fit the observation-error model on each run -- a calibration, off
# for daily use -- aiming at desroziers (needs O-A), sigma or sigma3
FIT_RADAR="off"
FIT_RADAR_TARGET="desroziers"
OBS_ERROR_MODEL="off"   # radar: the current model in the calibration table

if [ -z "${DATESTART}" ] || [ -z "${DATEEND}" ]; then
    [ -z "${DATEEND}" ] && \
        DATEEND="$(date -u -d "${DAYS_BACK_END} days ago" +%Y%m%d)18"
    [ -z "${DATESTART}" ] && \
        DATESTART="$(date -u -d "$((DAYS_BACK_END + WINDOW_DAYS)) days ago" +%Y%m%d)00"
    echo "[wrapper] period resolved from today: ${DATESTART} .. ${DATEEND}"
fi

# The module still reads it; the families of this wrapper never use it.

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

# load_pikobs.sh activates mamba/conda; some of its commands return a
# non-zero status, which would kill this script under 'set -e'
set +e
source /home/${USER}/pikobs_install/load_pikobs.sh
rc=$?
set -e
if ! python -c "import pikobs" 2> /dev/null; then
    echo "ERROR: pikobs environment not ready (load_pikobs.sh returned ${rc})" >&2
    exit 1
fi

if [ "${#PATH_EXPERIENCE_FILES[@]}" -ne "${#EXPERIENCE_NAME[@]}" ]; then
    echo "ERROR: PATH_EXPERIENCE_FILES (${#PATH_EXPERIENCE_FILES[@]}) and" \
         "EXPERIENCE_NAME (${#EXPERIENCE_NAME[@]}) must have the same" \
         "number of entries." >&2
    exit 1
fi

OPTIONAL_ARGS=()
if [ "${#VARNOS[@]}" -gt 0 ]; then
    OPTIONAL_ARGS+=(--varnos "${VARNOS[@]}")
fi

# ============================================================================
# 3. EXECUTION
# ============================================================================
python -c 'import pikobs; pikobs.profile.arg_call()'                \
       ${PATH_CONTROL_FILES:+--path_control_files "${PATH_CONTROL_FILES}"} \
       ${PATH_CONTROL_FILES:+--control_name       "${CONTROL_NAME}"}       \
       --path_experience_files "${PATH_EXPERIENCE_FILES[@]}"        \
       --experience_name       "${EXPERIENCE_NAME[@]}"              \
       --pathwork              "${PATHWORK}"                        \
       --datestart             "${DATESTART}"                       \
       --dateend               "${DATEEND}"                         \
       --region                "${REGION[@]}"                       \
       --land_ocean            "${LAND_OCEAN[@]}"                   \
       --special_column        "${SPECIAL_COLUMN}"                    \
       --family                "${FAMILY[@]}"                       \
       --flags_criteria        "${FLAGS_CRITERIA[@]}"               \
       --fonction              "${FONCTION[@]}"                     \
       --min_obs               "${MIN_OBS}"                         \
       --obs_error_model       "${OBS_ERROR_MODEL}"                 \
       --fit_radar       "${FIT_RADAR}"                 \
       --fit_radar_target       "${FIT_RADAR_TARGET}"                 \
       --error_curves       "${ERROR_CURVES[@]}"                 \
       --id_stn                "${ID_STN[@]}"                       \
       --match               "${MATCH}"                           \
       --svg                   "${SVG}"                             \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"
