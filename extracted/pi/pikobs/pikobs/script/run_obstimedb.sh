#!/usr/bin/env bash
# ============================================================================
# run_obstimedb.sh
# ----------------------------------------------------------------------------
set -eo pipefail
# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================
# Directory containing the SQLite observation databases for the (single)
# experiment. obstimedb tracks ONE run over time — no control/reference.
PATH_EXPERIENCE_FILES="/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt/"
# Label for the experiment data.
EXPERIENCE_NAME="GDPS-SN"
# Output directory where the generated results will be saved.
PATHWORK="/home/dlo001/sites8/pikobs_obstimedb2"
# Start and end dates for the processing window in YYYYMMDDHH format (UTC).
DATESTART="2026090500"
DATEEND="2026091500"
# Region to process.
REGION="Monde"
# Observation families to process (space-separated list).
FAMILY="ai atms_allsky ch cris csr gp iasi mwhs2 mwhs2_rars  ro sc sf ssmis sw to_amsua_allsky to_amsub_allsky_rars to_amsua_allsky_rars to_amsub_allsky ua"
# Bitmask filter criteria.
FLAGS_CRITERIA="assimilee"
# Baseline look-back window, in calendar days, for the same synoptic hour
# (00/06/12/18). Each cycle is compared against the mean of this many
# previous days at the SAME hour.
WINDOW_DAYS=10
# Drop thresholds (percent) vs the same-hour baseline that flag a
# mosaic cell YELLOW / ORANGE / RED (increasing severity). A total
# outage (Nobs=0) is always RED, regardless of these values.
ALERT_YELLOW=10.0
ALERT_ORANGE=15.0
ALERT_RED=20.0
# Number of parallel Dask workers to use.
N_CPU=120
# Optional departure overlay on the time series: omp / oma / "oma omp".
# Leave EMPTY (default) to keep the report to Nobs only, as it's clearer
# to read and faster to generate.
AGR=""
# ============================================================================
# 2. SYSTEM SETUP (Do not edit below this line)
# ============================================================================
# --- Load Pikobs Conda Environment ---
source /home/${USER}/pikobs_install/load_pikobs.sh
# ============================================================================
# 3. EXECUTION
# ============================================================================
# Pikobs will automatically submit this to PBS if run on a login node.
python -c 'import pikobs; pikobs.obstimedb.arg_call()' \
       --path_experience_files "${PATH_EXPERIENCE_FILES}" \
       --experience_name "${EXPERIENCE_NAME}" \
       --pathwork "${PATHWORK}" \
       --datestart "${DATESTART}" \
       --dateend "${DATEEND}" \
       --region "${REGION}" \
       --family ${FAMILY} \
       --flags_criteria "${FLAGS_CRITERIA}" \
       --window_days "${WINDOW_DAYS}" \
       --alert_yellow "${ALERT_YELLOW}" \
       --alert_orange "${ALERT_ORANGE}" \
       --alert_red "${ALERT_RED}" \
       --n_cpu "${N_CPU}" \
       ${AGR:+--agr ${AGR}}
