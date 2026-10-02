#!/usr/bin/env bash
# ============================================================================
# run_vdedr_ic5_a120.sh
# ----------------------------------------------------------------------------
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================

# Directory containing the SQLite observation databases for the experiment.
PATH_EXPERIENCE_FILES="/home/ata000/ppp8/codedir/osrv/inputSQLITEs/oneMonthExperiments/A125/postalt/ /home/ata000/ppp8/codedir/osrv/inputSQLITEs/oneMonthExperiments/A120/postalt/"
# Label for the experiment data.
EXPERIENCE_NAME="A125 A120"

# Directory containing the SQLite observation databases for the control.
PATH_CONTROL_FILES="/home/ata000/ppp8/codedir/osrv/inputSQLITEs/oneMonthExperiments/CTL/postalt/"
# Label for the control data.
CONTROL_NAME="CTL"

# Output directory where the generated results will be saved.
PATHWORK="/home/dlo001/sites8/obscountdb_ice5_expA"

# Start and end dates for the processing window in YYYYMMDDHH format (UTC).
DATESTART="2025061500"
DATEEND="2025073112"

# Region to process.
REGION=" Monde ExtratropiquesNord ExtratropiquesSud Tropiques"
#Monde ExtratropiquesNord ExtratropiquesSud Tropiques
# Observation families to process (space-separated list).
#FAMILY="ai sc atms_allsky sf ch ssmis cris sw csr gp to_amsua_allsky iasi mwhs2 to_amsub_allsky ro ua"
FAMILY="atms_allsky ssmis cris csr to_amsua_allsky iasi mwhs2 to_amsub_allsky"
#FAMILY="atms_allsky"
# Bitmask filter criteria.
FLAGS_CRITERIA="assimilee"

# Number of parallel Dask workers to use.
N_CPU=80


# ============================================================================
# 2. SYSTEM SETUP (Do not edit below this line)
# ============================================================================

# --- Load Pikobs Conda Environment ---
source /home/${USER}/pikobs_install/load_pikobs.sh

# ============================================================================
# 3. EXECUTION
# ============================================================================
# Pikobs will automatically submit this to PBS if run on a login node.

python -c 'import pikobs; pikobs.vdedr.arg_call()' \
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
       --id_stn all \
       --n_cpu "${N_CPU}" 
