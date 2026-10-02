#!/usr/bin/env bash
# ============================================================================
# run_mapobs.sh
# ----------------------------------------------------------------------------
# pikobs.mapobs: where the observations are. Nine panels per time window:
# the map, its longitude and latitude profiles, the two cross-sections,
# the vertical distribution and the per-station contributions.
#
# One set of figures per cycle plus one per sub-interval, always
# coloured by station.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_mapobs.sh
#        chmod +x run_mapobs.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_mapobs.sh
#
# List settings are bash ARRAYS: FAMILY=(iasi cris), not FAMILY="iasi cris".
# ============================================================================
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Experiences -----------------------------------------------------------
# One directory per experience, one name per directory, same order. Each one
# gets its own time series; the viewer switches between them.
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/${USER}/sites8/pikobs_mapobs"

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
# Regions are computed in ONE pass, so adding more of them costs almost
# nothing; each becomes a selector in the viewer.
# Regions here are map projections: cyl, npolar, spolar, canada, europe,
# orthon, orthos, robinson. A polar or rotated projection is drawn inside
# a square cell, so the profiles around it stay aligned in lat/lon.
REGION=(Monde)       # which observations: the regions of Pikobs, polygons included;
                     # name:projection draws one in that projection only, e.g. hrdps:canada
PROJECTION=(cyl)     # how the map is drawn: cyl robinson npolar spolar orthon orthos canada ameriquenord europe

# Land filter, one series of dashboards each: all (no filter), land, ocean.
# land and ocean read the land mask; all does not, and costs nothing.
LAND_OCEAN=(all)

# The special column of a family, one series of dashboards per value: the
# wind computation method of sw, the elevation of the radar. off (default):
# everything together.
SPECIAL_COLUMN="off"

FAMILY=(sw ro)

# Flag criteria, one dashboard series each.
FLAGS_CRITERIA=(assimilee)

# Station grouping, one series of figures per token:
#   join        every station merged
#   all         one figure per station
#   METOP       stations whose id starts with METOP
#   =NOAA-20    exactly that station
#   C%          SQL LIKE pattern
ID_STN=(join)

# Channels / vertical levels:
#   join (all merged)   all (one figure each)   an explicit list (5 8 10)
CHANNEL=(join)
PRESSURE_LAYERS=()   # pressure families: layer bounds in hPa, e.g. (1100 850 500 250 100 10)
HEIGHT_LAYERS=()     # height families: layer bounds in km, e.g. (0 5 10 20 30 40)

# Optional varno list; empty = the family default.
VARNOS=()

# Sub-cycle length in minutes: 15 gives 24 dashboards per cycle, 60 gives 6.
INTERVAL_MIN=15

# Which panels to draw; each one is its own figure, so a map stays wide
# and the vertical distribution of an interferometer can be as tall as it
# needs. The viewer has a Panel selector.
#   map cross vertical stations   the four, separately
#   ... all                       and one more with them stacked together
#   all                           only the stacked one
PANELS=(map cross vertical stations all)

# Also write every figure as SVG next to the PNG, for editing before a
# presentation (Inkscape, Illustrator): on / off. The viewer always uses
# the PNG. An SVG keeps every element, so ask for it on a small selection.
SVG="off"

# The 6-h dashboard: every observation of a cycle in one image, next to the
# 15-minute slices. It is the heaviest piece on the radiances (10 to 16 MB
# an image on iasi). auto draws it for 4 cycles or fewer (a day); on draws
# it always -- over a longer period, ask a node with much more memory; off
# never draws it.
DASHBOARD_6H="auto"

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
python -c 'import pikobs; pikobs.mapobs.arg_call()'                 \
       --path_experience_files "${PATH_EXPERIENCE_FILES[@]}"        \
       --experience_name       "${EXPERIENCE_NAME[@]}"              \
       --pathwork              "${PATHWORK}"                        \
       --datestart             "${DATESTART}"                       \
       --dateend               "${DATEEND}"                         \
       --region                "${REGION[@]}"                       \
       --projection "${PROJECTION[@]}" \
       --land_ocean            "${LAND_OCEAN[@]}"                   \
       --special_column        "${SPECIAL_COLUMN}"                    \
       --family                "${FAMILY[@]}"                       \
       --flags_criteria        "${FLAGS_CRITERIA[@]}"               \
       --interval_min          "${INTERVAL_MIN}"                     \
       --panels                "${PANELS[@]}"                       \
       --id_stn                "${ID_STN[@]}"                       \
       --pressure_layers "${PRESSURE_LAYERS[@]}" \
       --height_layers "${HEIGHT_LAYERS[@]}" \
       --channel               "${CHANNEL[@]}"                      \
       --svg                   "${SVG}"                             \
       --dashboard_6h          "${DASHBOARD_6H}"                     \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"
