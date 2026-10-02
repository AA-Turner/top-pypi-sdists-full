#!/usr/bin/env bash
# ============================================================================
# run_profile_ra.sh
# ----------------------------------------------------------------------------
# Wrapper to generate vertical-profile statistics figures (Bias / Std dev /
# N obs / N profiles) for RADAR radial velocity (family ra). For radar the
# vertical-level grouping is the antenna ELEVATION: one image per elevation
# plus a grouped all-elevations image. id_stn groups can pool radars by
# prefix (C% = all radars starting with C, U% = idem for U).
#
# HOW TO RUN (recommended):
#   1. Download the latest copy of this wrapper from GitLab so it stays in
#      sync with the current options:
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_profile_ra.sh
#        chmod +x run_profile_ra.sh
#   2. Open an interactive compute node (do NOT run heavy jobs on a login
#      node). Adjust ncpus/mem/walltime to your job size:
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below, then launch from inside the node:
#        ./run_profile_ra.sh
# ============================================================================
set -x
set -eo pipefail
# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================
# --- Experiment to evaluate (always required) ------------------------------
# Directory containing the SQLite observation databases (YYYYMMDDHH_<family>).
PATH_EXPERIENCE="/home/dlo001/data_maestro/ppp7/maestro_archives/NAT910E22S100OEBOG/banco/postalt/"
# Label printed on the title of every generated figure.
EXPERIENCE_NAME="100km"
# --- Optional control to compare against (leave BOTH empty for a single run) -
# When set, every profile draws control vs experiment (REF blue, EXP red).
PATH_CONTROL=""
CONTROL_NAME=""
# Output directory where the figures and HTML viewer will be saved.
# WARNING: this directory is wiped on each run to prevent ghost files.
PATHWORK="/home/dlo001/sites8/pikobs_radvel_"
# Start and end dates for the processing window in YYYYMMDDHH format (UTC).
DATESTART="2022053100"
DATEEND="2022060400"
# Region key(s) (space-separated), e.g. "Monde HN HS".
REGION="Monde"
# Observation family (radar radial velocity).
FAMILY="radar"
# Bitmask filter criteria ("all" / "assimilee" / "rejets_qc" ...).
FLAGS_CRITERIA="all"
# Statistic/function(s) to plot (space-separated): omp / oma / obs.
FONCTION="omp"
# Station grouping (space-separated, cumulative tokens):
#   all   = one profile per radar
#   C%    = ONE pooled profile for every radar whose id starts with C
#   U%    = idem for U
#   join  = ONE pooled profile with every radar
# Example: "all C% U%"
ID_STN="C% U%"
# Vertical grouping (radar: per ELEVATION; --channel and --vcoord are aliases):
#   "all"  = per elevation, plus the all-elevations grouped image;
#   "join" = all elevations pooled into one profile.
CHANNEL="all"
# Number of parallel Dask workers.
N_CPU=40
# ============================================================================
# 2. SYSTEM SETUP (Do not edit below this line)
# ============================================================================
# Load the Pikobs Conda environment.
source /home/${USER}/pikobs_install/load_pikobs.sh
which python
# ============================================================================
# 3. EXECUTION
# ============================================================================
# Runs locally on the current (compute) node. It does NOT auto-submit to PBS,
# so make sure you opened a compute node first (see header).
#
# Build the optional control arguments only when PATH_CONTROL is set.
CONTROL_ARGS=()
if [[ -n "${PATH_CONTROL}" ]]; then
    CONTROL_ARGS=(--path_control_files "${PATH_CONTROL}" \
                  --control_name "${CONTROL_NAME}")
fi
python -c 'import pikobs; pikobs.profile.arg_call()' \
       "${CONTROL_ARGS[@]}"                          \
       --path_experience_files ${PATH_EXPERIENCE}  \
       --experience_name       ${EXPERIENCE_NAME}  \
       --pathwork              "${PATHWORK}"          \
       --datestart             "${DATESTART}"         \
       --dateend               "${DATEEND}"           \
       --region                ${REGION}              \
       --family                ${FAMILY}              \
       --flags_criteria        ${FLAGS_CRITERIA}      \
       --fonction              ${FONCTION}            \
       --id_stn                ${ID_STN}              \
       --channel               ${CHANNEL}             \
       --n_cpu                 "${N_CPU}"
