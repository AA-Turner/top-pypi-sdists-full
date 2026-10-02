#!/usr/bin/env bash
# ============================================================================
# run_pikobsburp2rdb.sh 
# ----------------------------------------------------------------------------
# Wrapper to mass-convert BURP files into SQLite RDB databases.
# This script relies on Pikobs' built-in intelligent PBS job manager to
# automatically submit to the queue if run from a login node.
# ============================================================================
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================

# Space-separated list of directories containing the raw BURP files.
PATH_EXPERIENCE_FILES="/home/mit000/data_maestro/ppp7/data/OPS/operation.ensemble.banco.postens.e2/"

# Space-separated list of labels corresponding to each path above.
# These labels are stored in the database to identify the experiments.
EXPERIENCE_NAME="e2_thomas"

# The directory where the resulting SQLite RDB files will be saved.
PATHWORK="/home/dlo001/sites8/pikobs_rdb_cutoff/"

# Start and end dates for the extraction in YYYYMMDDHH format (UTC).
DATESTART="2023072112"
DATEEND="2023072112"

# Number of parallel Dask workers to use for the conversion.
N_CPUS=30


# ============================================================================
# 2. SYSTEM DEPENDENCIES (Do not edit below this line)
# ============================================================================

# --- Load external ECCC burp2rdb binaries ---
export SSM_PRELOAD=NO
export SSM_ALWAYSEXEC=NO

set +e # Temporarily disable strict error handling for SSM
. r.load.dot "cmd/cmda/utils/20260202/burp2rdb_5.25_rhel-9-amd64-64" < /dev/null
. ssmuse-sh -d "eccc/cmd/cmda/utils/20260202" < /dev/null
. ssmuse-sh -d "eccc/cmo/cmoi/base/20260205" < /dev/null
set -e

# --- Load Pikobs Conda Environment ---
source /home/${USER}/pikobs_install/load_pikobs.sh


# ============================================================================
# 3. EXECUTION
# ============================================================================
# Pikobs will automatically submit this to PBS if run on a login node.

python -c 'import pikobs; pikobs.pikobsburp2rdb.arg_call()' \
       --path_experience_files ${PATH_EXPERIENCE_FILES} \
       --experience_name ${EXPERIENCE_NAME} \
       --pathwork "${PATHWORK}" \
       --datestart "${DATESTART}" \
       --dateend "${DATEEND}" \
       --n_cpus "${N_CPUS}" \
       --force_clean 
#       --no_submit
