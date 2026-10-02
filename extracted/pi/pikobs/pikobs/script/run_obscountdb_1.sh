#!/usr/bin/env bash
# ============================================================================
# run_obscountdb_1.sh
# ----------------------------------------------------------------------------
# Wrapper to generate observation count statistics and comparisons.
# This script relies on Pikobs' built-in intelligent PBS job manager to
# automatically submit to the queue if run from a login node.
# ============================================================================
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================

# Directory containing the SQLite observation databases for the experiment.
PATH_EXPERIENCE_FILES="/home/lco000/data_maestro/ppp8/outils/outils_2/derialtExperienceEumetsat/feedEumetcastDerialt/"


# Label for the experiment data.
EXPERIENCE_NAME="EumetCastFeedDerialt"
EXPERIENCE_NAME="EumetCastFeedDerialt"
EXPERIENCE_NAME="feedEumetcastDerialt"

# Directory containing the SQLite observation databases for the control.
PATH_CONTROL_FILES="/home/lco000/data_maestro/ppp8/outils/outils_2/derialtExperienceEumetsat/ctlDerialt/"

# Label for the control data.
CONTROL_NAME="GPDSderialt"

# Output directory where the generated results will be saved.
PATHWORK="/home/dlo001/sites8/pikobs_obs/"

# Start and end dates for the processing window in YYYYMMDDHH format (UTC).
DATESTART="2025070100"
DATEEND="2025070200"

# Region to process.
REGION="Monde"

# Observation families to process (space-separated list).
FAMILY=" atms cris  csr to_amsua to_amsub"

# Bitmask filter criteria.
FLAGS_CRITERIA="assimilee"

# Number of parallel Dask workers to use.
N_CPU=20


# ============================================================================
# 2. SYSTEM SETUP (Do not edit below this line)
# ============================================================================

# --- Load Pikobs Conda Environment ---
source /home/${USER}/pikobs_install/load_pikobs.sh


# ============================================================================
# 3. EXECUTION
# ============================================================================
# Pikobs will automatically submit this to PBS if run on a login node.

python -c 'import pikobs; pikobs.obscountdb.arg_call()' \
       --path_experience_files "${PATH_EXPERIENCE_FILES}" \
       --experience_name "${EXPERIENCE_NAME}" \
       --path_control_files "${PATH_CONTROL_FILES}" \
       --control_name "${CONTROL_NAME}" \
       --pathwork "${PATHWORK}" \
       --datestart "${DATESTART}" \
       --dateend "${DATEEND}" \
       --region "${REGION}" \
       --family ${FAMILY} \
       --flags_criteria "${FLAGS_CRITERIA}" \
       --n_cpu "${N_CPU}" \
      #--no_submit
