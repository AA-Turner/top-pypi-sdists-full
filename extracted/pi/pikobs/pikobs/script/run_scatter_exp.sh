#!/usr/bin/env bash
# ============================================================================
# run_scatter_exp.sh
# ----------------------------------------------------------------------------
# pikobs.scatter, single-run maps: every experience listed below is drawn
# on its own maps (no control, no difference). Use run_scatter_cont_exp.sh
# to compare experiences against a control.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_scatter_exp.sh
#        chmod +x run_scatter_exp.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_scatter_exp.sh
#
# List settings are bash ARRAYS: FAMILY=(sw ai), not FAMILY="sw ai".
# Quote any token that contains '*' or a space: ID_STN=(join "CAS*" "AMDAR (42)").
# ============================================================================
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Experiences -----------------------------------------------------------
# One directory per experience with the 6-h SQLite files YYYYMMDDHH_<family>,
# and one name per directory, same order. Each experience gets its own maps
# and the viewer lets you switch between them.
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/${USER}/sites8/pikobs_scatter_exp"

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
# Boxes (Monde, HemisphereNord, Canada, ...) and polygons carried by
# pikobs (hrdps, hreps, the *_CLIM areas of EMET). List them with:
#   python pikobs/configobs/import_regions.py --list
REGION=(Monde)
FAMILY=(iasi)                       # sw ai sf ua iasi cris to_amsua_allsky ...
FLAGS_CRITERIA=(all assimilee)

# Land filter, one series of maps each: all (no filter), land, ocean.
# land and ocean read the land mask; all does not, and costs nothing.
LAND_OCEAN=(all)

# Functions, one map each:
#   omp oma        mean O-B / O-A per box
#   stdomp stdoma  standard deviation of O-B / O-A
#   obs            mean observed value
#   nobs dens      observations per day / per km2 per day
#   bcorr          mean bias correction (radiance families only, skipped
#                  automatically when the files have no BIAS_CORR column)
FONCTION=(omp oma stdomp stdoma obs nobs dens bcorr)

# Optional varno list; empty = the family default.
VARNOS=()

# ---- Boxes and projection ----------------------------------------------------
BOXSIZEX=2                          # degrees of longitude
BOXSIZEY=2                          # degrees of latitude
PROJECTION=(cyl)                    # cyl OrthoN OrthoS robinson Europe Canada
                                    # AmeriqueNord Npolar Spolar reg
# Vertical layers, one series of maps each, on top of the series with the
# whole column. Each family reads the list of its own coordinate, so
# families of different kinds can be asked for in the same run:
#   pressure families (ua ai sw ch)  PRESSURE_LAYERS, in hPa
#   height families   (ro radar)     HEIGHT_LAYERS, in km
#   radiances                        no layer, use CHANNEL
# Empty means the whole column in one series.
PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)
HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)

# ---- Station / channel grouping ------------------------------------------------
# Every token gives its own series of maps.
#   join          all stations merged
#   all           one map per station (per instrument type for ai sf ua gp csr)
#   CAS  CAS*     every station whose id starts with CAS
#   C%            SQL LIKE pattern on the station id
#   =NENE         exactly station NENE
#   ai sf ua gp csr only: instrument names from DICT_CODTYP
#     pilot       PILOT, PILOT SHIP, PILOT MOBIL merged
#     =PILOT      PILOT only ('_' for spaces: =PILOT_SHIP)
#     32          codtyp 32      "AMDAR (42)"  codtyp 42
ID_STN=(all)

# Channels / vertical coordinates, combinable:
#   join (all merged)   all (one map each)   explicit values, e.g. (join 32 40)
# A value is a level of the family: 32 is a channel of iasi, and a
# radiosonde has none -- join works for every family.
CHANNEL=(join)

# ---- Rendering -----------------------------------------------------------------
POINTS="OFF"                        # ON: print the obs count in each box
SPECIAL_COLUMN="off"                # on: one map per special value
                                    # (wind method, elevation); off: all together

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

# ---- Parallelism ---------------------------------------------------------------
N_CPUS=80                           # Dask workers, match the reserved ncpus

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
python -c 'import pikobs; pikobs.scatter.arg_call()'                \
       --path_experience_files "${PATH_EXPERIENCE_FILES[@]}"        \
       --experience_name       "${EXPERIENCE_NAME[@]}"              \
       --pathwork              "${PATHWORK}"                        \
       --datestart             "${DATESTART}"                       \
       --dateend               "${DATEEND}"                         \
       --region                "${REGION[@]}"                       \
       --family                "${FAMILY[@]}"                       \
       --flags_criteria        "${FLAGS_CRITERIA[@]}"               \
       --land_ocean            "${LAND_OCEAN[@]}"                   \
       --fonction              "${FONCTION[@]}"                     \
       --boxsizex              "${BOXSIZEX}"                        \
       --boxsizey              "${BOXSIZEY}"                        \
       --projection            "${PROJECTION[@]}"                   \
       --pressure_layers       "${PRESSURE_LAYERS[@]}"              \
       --height_layers         "${HEIGHT_LAYERS[@]}"                \
       --id_stn                "${ID_STN[@]}"                       \
       --channel               "${CHANNEL[@]}"                      \
       --Points                "${POINTS}"                          \
       --special_column        "${SPECIAL_COLUMN}"                  \
       --match               "${MATCH}"                           \
       --svg                   "${SVG}"                             \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"
