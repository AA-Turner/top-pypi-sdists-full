#!/usr/bin/env bash
# ============================================================================
# run_scatter_check.sh
# ----------------------------------------------------------------------------
# Three short runs that exercise what changed in scatter: the layers read
# in the unit of the family, and the regions that are polygons.
#
#   1. sw    pressure layers, in hPa
#   2. ro    height layers, in km
#   3. cris  channels, no layer
#
# They are separate runs on purpose: LAYER applies to the whole run, so
# the same numbers cannot mean hPa for one family and km for another.
#
# One day of data, one projection, the stations pooled: a few minutes
# each. Open a compute node first.
# ============================================================================
set -eo pipefail

# ---- What to read ----------------------------------------------------------
PATH_EXPERIENCE_FILES=(/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt)
EXPERIENCE_NAME=(experience)

# ---- One day ---------------------------------------------------------------
DATESTART="2026091400"
DATEEND="2026091418"

# ---- Where the maps go (one directory per check) ----------------------------
BASE="/home/${USER}/sites8/pikobs_scatter_check"

# Monde tells you the run is sane; hrdps is the polygon: its maps must
# have boxes inside the model contour and nowhere else.
REGION=(Monde hrdps)

# The layers, read in the unit of each family.
PRESSURE_LAYERS=(1100 850 500 250 100 10 1 0)    # hPa, for sw ua ai ch
HEIGHT_LAYERS=(0 5 10 20 30 40 60 100)           # km, for ro radar

N_CPUS=40

# ============================================================================
# 2. SYSTEM SETUP (Do not edit below this line)
# ============================================================================
source /home/${USER}/pikobs_install/load_pikobs.sh

run_one () {   # run_one <tag> <families> <channel>
    local tag="$1" families="$2" channel="$3"
    echo
    echo "=============================================================="
    echo " ${tag}: family ${families}, channel ${channel}"
    echo "=============================================================="
    python -c 'import pikobs; pikobs.scatter.arg_call()'         \
           --path_experience_files "${PATH_EXPERIENCE_FILES[@]}"  \
           --experience_name       "${EXPERIENCE_NAME[@]}"        \
           --pathwork              "${BASE}_${tag}"               \
           --datestart             "${DATESTART}"                 \
           --dateend               "${DATEEND}"                   \
           --region                "${REGION[@]}"                 \
           --family                ${families}                    \
           --flags_criteria        assimilee                      \
           --fonction              omp stdomp nobs                \
           --boxsizex              5                              \
           --boxsizey              5                              \
           --projection            cyl                            \
           --id_stn                join                           \
           --channel               ${channel}                     \
           --pressure_layers       "${PRESSURE_LAYERS[@]}"        \
           --height_layers         "${HEIGHT_LAYERS[@]}"          \
           --special_column        off                            \
           --n_cpus                "${N_CPUS}"                    \
           --no_submit
}

# 1. the two kinds of family in one run, which is what the change was
#    for: sw takes the pressure layers, ro the height ones, and each is
#    labelled in its own unit.
run_one layers "sw ro" join

# 2. a radiance: no layer at all, and the channels asked for one by one.
run_one channels cris "join 32 40"

echo
echo "=============================================================="
echo " what to check"
echo "=============================================================="
cat <<'EOT'
  * every run wrote a viewer:
        ls -1 /home/$USER/sites8/pikobs_scatter_check_*/pikobs_scatter_viewer.html

  * the polygon region really clips. Compare the counts:
        for d in /home/$USER/sites8/pikobs_scatter_check_pressure/sw/*.db; do
            echo "$d"
            sqlite3 "$d" "SELECT COUNT(*), SUM(n) FROM moyenne;"
        done
    the hrdps databases must hold far fewer boxes than the Monde ones,
    and their maps no box outside the model contour.

  * the layers came out per family. The run prints them when it starts:
        [scatter] sw: 1 | 1100-850 hPa, 2 | 850-500 hPa, ...
        [scatter] ro: 1 | 0-5 km, 2 | 5-10 km, ...
        [scatter] cris: the whole column in one series
    and the Layer selector of the first viewer offers both sets, each in
    its own unit. A layer of ro that comes out empty means the unit is
    still wrong somewhere.
EOT
