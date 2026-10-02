#!/usr/bin/env bash
# ============================================================================
# run_verifcorr.sh — Spatial correlogram of OmP/OmA vs distance
# ----------------------------------------------------------------------------
# Wraps pikobs.verifcorr: for one or more datasets (each a directory of
# converted SQLite files, exactly like pikobs.progps's
# --path_experience_files), estimates how the correlation of OmP/OmA/
# obsvalue decays with the great-circle distance between observation
# pairs (the Hollingsworth-Lönnberg method). Each dataset gets its own
# independent correlogram; when more than one is given, they are
# overlaid on the same figure so a change in spatial correlation
# structure between e.g. Control and an Experience is directly visible.
# ============================================================================
set -eo pipefail
# ============================================================================
# 1. USER SETTINGS (Edit these parameters)
# ============================================================================

# One or more dataset directories + matching labels, as ARRAYS. Each
# is analysed independently and overlaid on the same figure. A single
# dataset works too -- just give each array one entry.
#   PATH_FILES=(/path/to/control/)                    # single dataset
#   NAME=(Control)
#   PATH_FILES=(/path/to/control/ /path/to/exp1/)      # compare two
#   NAME=(Control Exp1)
PATH_FILES=(
    "/home/sprj700/data_maestro/ppp8/maestro_archives/G2FC910V1E25/monitoring/banco/bgckalt/"
    "/home/lco000/data_maestro/ppp8/maestro_archives/OSEE25ALLOBS200_sel4/monitoring/banco/bgckalt/"
)
NAME=(Control Exp1)

# Output directory (wiped on each run).
PATHWORK="/home/dlo001/sites8/pikobs_verifcorr"

# Processing window YYYYMMDDHH (UTC).
DATESTART="2025061500"
DATEEND="2025063018"

# Region(s) and family(ies) -- ARRAYS, several can be requested
# together (one correlogram figure per combination). PREFER AS WIDE A
# REGION AS THE ANALYSIS ALLOWS -- fitting the correlation length
# scale over a small region under-estimates it (a known statistical
# effect, see the module docstring); "Monde" is ideal unless you have
# a specific reason to restrict it.
REGION=(Monde)
FAMILY=(ro)

# An ordinary pikobs.flag_criteria() value (e.g. "all", "assimilee"),
# plain string (not an array).
FLAGS_CRITERIA="all"

# omp / oma / obsvalue -- ARRAY, each gets its own combined figure.
FONCTION=(omp)

# Maximum pair separation to consider, in km. Correlation beyond this
# is assumed negligible; this also keeps runtime bounded.
MAX_DIST_KM=200

# Number of distance bins between 0 and MAX_DIST_KM.
N_BINS=30

# Random-subsample cap: if more than this many observations remain
# after filters for one dataset/family/region/fonction, a random
# subsample of this size is used instead -- keeps runtime and memory
# bounded regardless of how large the input files are (e.g. IASI's
# 10+ million rows per date).
MAX_OBS=50000

# Number of parallel Dask workers.
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
python -c 'import pikobs; pikobs.spatial.arg_call()' \
       --path_files "${PATH_FILES[@]}" \
       --name "${NAME[@]}" \
       --pathwork "${PATHWORK}" \
       --datestart "${DATESTART}" \
       --dateend "${DATEEND}" \
       --region "${REGION[@]}" \
       --family "${FAMILY[@]}" \
       --flags_criteria "${FLAGS_CRITERIA}" \
       --fonction "${FONCTION[@]}" \
       --max_dist_km "${MAX_DIST_KM}" \
       --n_bins "${N_BINS}" \
       --max_obs "${MAX_OBS}" \
       --n_cpu "${N_CPU}"
