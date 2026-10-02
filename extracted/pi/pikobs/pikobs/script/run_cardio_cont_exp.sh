#!/usr/bin/env bash
# ============================================================================
# run_cardio_cont_exp.sh
# ----------------------------------------------------------------------------
# pikobs.cardio: cardiogram time series of one or several experiences,
# against a control when one is given.
# Every region and flag criteria is computed in a single pass over the
# input files; the HTML viewer lets you switch between them.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_cardio_cont_exp.sh
#        chmod +x run_cardio_cont_exp.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_cardio_cont_exp.sh
#
# List settings are bash ARRAYS: FAMILY=(iasi cris), not FAMILY="iasi cris".
# ============================================================================
# ----------------------------------------------------------------------------
# Control against experience: every experience listed below is compared
# with the control, observation by observation where the module can, and
# the figures show the difference and what the tests make of it. Use
# run_cardio_exp.sh to draw a run on its own.
# ----------------------------------------------------------------------------
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Control (optional) ----------------------------------------------------
# With a control, every experience is drawn on the same panels as it and
# each cycle is tested: a circle marks the cycles where the change passes
# 95 %, red when the experience wins and blue when the control does.
# Leave it empty for plain time series of each run on its own.
PATH_CONTROL_FILES="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
CONTROL_NAME="control"

# ---- Experiences -----------------------------------------------------------
# One directory per experience, one name per directory, same order.
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/${USER}/sites8/pikobs_cardio_cont_exp"

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
FLAGS_CRITERIA=(assimilee)

# Land filter, one series of figures each: all (no filter), land, ocean.
# land and ocean read the land mask; all does not, and costs nothing.
LAND_OCEAN=(all)

# The special column of a family, one series of figures per value: the
# wind computation method of sw (IR, visible, water vapour...), the
# elevation of the radar. off (default): everything together.
SPECIAL_COLUMN="off"

FAMILY=(ai sw ua to_amsua_allsky iasi cris)

# Station grouping, one series of figures per token:
#   join        every station merged
#   all         one figure per station
#   METOP       stations whose id starts with METOP
#   =NOAA-20    exactly that station
#   C%          SQL LIKE pattern
ID_STN=(join all)

# Channels / vertical levels:
#   join (all merged)   all (one figure each)   an explicit list (5 8 10)
CHANNEL=(join)

# Figure shape: wide or narrow.
PLOT_TYPE="wide"

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
python -c 'import pikobs; pikobs.cardio.arg_call()'                 \
       ${PATH_CONTROL_FILES:+--path_control_files "${PATH_CONTROL_FILES}"} \
       ${PATH_CONTROL_FILES:+--control_name       "${CONTROL_NAME}"}       \
       --path_experience_files "${PATH_EXPERIENCE_FILES[@]}"        \
       --experience_name       "${EXPERIENCE_NAME[@]}"              \
       --pathwork              "${PATHWORK}"                        \
       --datestart             "${DATESTART}"                       \
       --dateend               "${DATEEND}"                         \
       --region                "${REGION[@]}"                       \
       --family                "${FAMILY[@]}"                       \
       --flags_criteria        "${FLAGS_CRITERIA[@]}"               \
       --land_ocean            "${LAND_OCEAN[@]}"                   \
       --special_column        "${SPECIAL_COLUMN}"                    \
       --id_stn                "${ID_STN[@]}"                       \
       --channel               "${CHANNEL[@]}"                      \
       --plot_type             "${PLOT_TYPE}"                       \
       --match               "${MATCH}"                           \
       --svg                   "${SVG}"                             \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"
