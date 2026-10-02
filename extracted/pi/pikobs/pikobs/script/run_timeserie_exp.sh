#!/usr/bin/env bash
# ============================================================================
# run_timeserie_exp.sh
# ----------------------------------------------------------------------------
# pikobs.timeserie: availability and quality control, cycle by cycle --
# how many observations come in every 6-h cycle, stacked by what the
# quality control did with them, and, when the files carry them, the
# mean and sigma of the departures, the assigned error and the bias
# correction. A file with no O-P gives the counts alone.
#
# With a control, one more figure puts every run on the same axes.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_timeserie_exp.sh
#        chmod +x run_timeserie_exp.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_timeserie_exp.sh
#
# List settings are bash ARRAYS: FAMILY=(iasi cris), not FAMILY="iasi cris".
# ============================================================================
# ----------------------------------------------------------------------------
# One run on its own: every experience listed below gets its own figures,
# with no control and no difference. Use run_timeserie_cont_exp.sh to
# compare them against a reference.
# ----------------------------------------------------------------------------
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Control (optional) ----------------------------------------------------
# With a control, one more figure puts every run on the same axes, the
# control in blue, with the change of the number of assimilated
# observations. Each run keeps all its own observations: for matched
# quality tests, see cardio.
# Leave it empty for the series of each run on its own.
PATH_CONTROL_FILES=()
CONTROL_NAME="control"

# ---- Experiences -----------------------------------------------------------
# One directory per experience, one name per directory, same order.
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/${USER}/sites8/pikobs_timeserie_exp"

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

FAMILY=(sw ua ai)




# Levels: join puts every level in one series; all gives one series per
# channel or level; or a list of levels.
CHANNEL=(join)

# Surface: all (default, no filter), land, ocean -- one series each, and
# a selector in the viewer. land and ocean need the global_land_mask
# package, and cost nothing extra: they are counted in the same pass.
LAND_OCEAN=(all)

# The special column of a family, one series of figures per value: the
# wind computation method of sw, the elevation of the radar. off (default):
# everything together.
SPECIAL_COLUMN="off"

# With ID_STN=(join), or with a group like C%, the figure gains one panel:
# the observations of every station -- or of every instrument type on ai,
# ua, sf, gp and csr -- one colour each, so the weight of each of them is
# read cycle by cycle. A single station gives the three panels only.

# With a control, on: compare the two runs on the SAME observations of
# every cycle, drawn as solid lines beside the dashed ones of each run
# with all of its own, and add two panels with the change of the mean and
# of sigma, cycle by cycle: a bar filled red where the experience is
# better and the test passes, blue where the control is, pale where the
# change is not larger than noise (paired t-test on the mean, Pitman-Morgan on
# sigma). The summary also says how much of the data the runs share.
# It answers the question the counts raise: when an experience assimilates
# more, is its sigma larger because it is worse, or because the
# observations it adds are harder? One more pass over the files, so leave
# it off when you do not need it.
#   off  every run with all of its own observations (the default)
#   on   only the comparison on the same observations
#   all  both, and the Experience selector of the viewer switches between
#        "all runs, same observations" and "all runs, each with its own"
MATCH="on"
FONCTION=(omp)       # the comparison in O-P (omp), O-A (oma), or both
PRESSURE_LAYERS=()   # pressure families: layer bounds in hPa, e.g. (1100 850 500 250 100 10)
HEIGHT_LAYERS=()     # height families: layer bounds in km, e.g. (0 5 10 20 30 40)

# A number, in percent. 0 = no alerts. With ALERT_PCT=50, every cycle whose
# number of observations falls more than 50 % below the median of the SAME
# HOUR on the days before it is marked on the figure and listed in
# timeserie_alerts.csv. The same hour, because a family like ua brings
# thousands of observations at 00 and 12 UTC and a handful at 06 and 18.
# Start around 40 or 50: a small value flags the ordinary swings.
ALERT_PCT=0

# Station grouping, one series of figures per token:
#   join        every station merged
#   all         one figure per station
#   METOP       stations whose id starts with METOP
#   =NOAA-20    exactly that station
#   C%          SQL LIKE pattern
ID_STN=(join all)


# Optional varno list; empty = the family default.
VARNOS=()

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
python -c 'import pikobs; pikobs.timeserie.arg_call()'                \
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
       --id_stn                "${ID_STN[@]}"                       \
       --channel               "${CHANNEL[@]}"                      \
       --land_ocean            "${LAND_OCEAN[@]}"                   \
       --special_column        "${SPECIAL_COLUMN}"                    \
       --pressure_layers "${PRESSURE_LAYERS[@]}" \
       --height_layers "${HEIGHT_LAYERS[@]}" \
       --fonction "${FONCTION[@]}" \
       --match                 "${MATCH}"                           \
       --alert_pct             "${ALERT_PCT}"                       \
       --svg                   "${SVG}"                             \
       --n_cpus                "${N_CPUS}"                          \
       --no_submit                                                  \
       "${OPTIONAL_ARGS[@]}"
