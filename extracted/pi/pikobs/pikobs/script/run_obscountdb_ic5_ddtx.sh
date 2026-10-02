#!/usr/bin/env bash
# ============================================================================
# run_obscountdb_ic5_ddtx.sh
# ----------------------------------------------------------------------------
# pikobs.obscountdb: observation volume diagnostics. Compares the volume
# of assimilated observations between a Control (reference) and an Experience.
#
# HOW TO RUN:
#   1. Download the latest copy (it follows the installed module options):
#        wget https://gitlab.science.gc.ca/dlo001/Pikobs/-/raw/master/pikobs/script/run_obscountdb_ic5_ddtx.sh
#        chmod +x run_obscountdb_ic5_ddtx.sh
#   2. Open a compute node (never run this on a login node):
#        qsub -I -lselect=1:ncpus=80:mem=185gb -lwalltime=2:0:0
#   3. Edit the USER SETTINGS below and launch from the node:
#        ./run_obscountdb_ic5_ddtx.sh
#
# List settings are bash ARRAYS: FAMILY=(sw ai), not FAMILY="sw ai".
# ============================================================================
set -eo pipefail

# ============================================================================
# 1. USER SETTINGS
# ============================================================================

# ---- Experience ------------------------------------------------------------
# Directory containing the SQLite observation databases for the experiment.
PATH_EXPERIENCE_FILES="/home/ata000/ppp8/codedir/osrv/inputSQLITEs/oneMonthExperiments/DDTX/postalt/"
EXPERIENCE_NAME="DDTX"

# ---- Control ---------------------------------------------------------------
# Directory containing the SQLite observation databases for the control.
PATH_CONTROL_FILES="/home/ata000/ppp8/codedir/osrv/inputSQLITEs/oneMonthExperiments/CTL/postalt/"
CONTROL_NAME="CTL"

# ---- Output ----------------------------------------------------------------
# WIPED at every run (per family). To open the viewer in a browser, link
# this folder once under ~/public_html; the run prints the command.
PATHWORK="/home/dlo001/sites8/obscountdb_ice5_expDDTX"

# ---- Period ----------------------------------------------------------------
# YYYYMMDDHH, UTC, both ends included, one file every 6 h.
DATESTART="2025061500"
DATEEND="2025073112"

# ---- Selection -------------------------------------------------------------
REGION=(Monde ExtratropiquesNord ExtratropiquesSud Tropiques)                         # Monde ExtratropiquesNord ExtratropiquesSud Tropiques
FAMILY=(atms_allsky ssmis cris csr to_amsua_allsky iasi mwhs2 to_amsub_allsky)
FLAGS_CRITERIA="assimilee"             # assimilee, rejets_qc, all, etc. (Single string)

# Optional departure overlay: omp / oma (Leave empty to disable)
# Example: AGR=(oma omp)
AGR=( )

# ---- Parallelism -----------------------------------------------------------
N_CPUS=80                              # Dask workers, match the reserved ncpus


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

OPTIONAL_ARGS=()
if [ "${#AGR[@]}" -gt 0 ]; then
    OPTIONAL_ARGS+=(--agr "${AGR[@]}")
fi

# ============================================================================
# 3. EXECUTION
# ============================================================================
python -c 'import pikobs; pikobs.obscountdb.arg_call()'                \
       --path_experience_files "${PATH_EXPERIENCE_FILES}"              \
       --experience_name       "${EXPERIENCE_NAME}"                    \
       --path_control_files    "${PATH_CONTROL_FILES}"                 \
       --control_name          "${CONTROL_NAME}"                       \
       --pathwork              "${PATHWORK}"                           \
       --datestart             "${DATESTART}"                          \
       --dateend               "${DATEEND}"                            \
       --region                "${REGION[@]}"                          \
       --family                "${FAMILY[@]}"                          \
       --flags_criteria        "${FLAGS_CRITERIA}"                     \
       --n_cpus                "${N_CPUS}"                             \
       --no_submit                                                     \
       "${OPTIONAL_ARGS[@]}"

# ============================================================================
# 4. REPORT LINKS
# ============================================================================
echo "----------------------------------------------------------------------"
case "${PATHWORK}" in
    /home/${USER}/sites8/*)
        WEB_BASE="https://goc-dx-u3.science.gc.ca/~${USER}/${PATHWORK#/home/${USER}/}"
        echo "Web reports generated:"
        for REG in "${REGION[@]}"; do
            echo "  ${WEB_BASE}/Full_Report_${REG}_${FLAGS_CRITERIA}.html"
        done
        ;;
    *)
        echo "Outputs saved locally in:"
        echo "  ${PATHWORK}"
        ;;
esac
echo "----------------------------------------------------------------------"
