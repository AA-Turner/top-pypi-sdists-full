#!/usr/bin/env bash
# ============================================================================
# test_coherence.sh -- the same selection through every comparing module.
#
# Each module's comparison wrapper is copied and set to the same day, the
# same regions (one global, one polygon), the same criterion and MATCH=on,
# with the families it supports. Then coherence.py compares the totals of
# the pairs: one family, region and criterion must give the same N and the
# same moments whichever module summed them.
#
#   pikobs/build_doc/test_coherence.sh            # all modules below
#   pikobs/build_doc/test_coherence.sh cardio zone
#
# Run from a compute node with room (400 GB for scatter), from the
# repository root. Outputs in /home/$USER/sites8/pikobs_coh_<module>.
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPTS="${REPO}/pikobs/script"
BASE="/home/${USER}/sites8"
DAY_START="${COH_DAY:-$(date -u -d "4 days ago" +%Y%m%d)}00"   # COH_DAY=YYYYMMDD to repeat a given day
DAY_END="${DAY_START:0:8}18"
REGIONS="Monde Canada"
FLAG="assimilee"
CTL_NAME="G0"
CTL_PATH="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
EXP_NAME="G2"
EXP_PATH="/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"

families_of () {      # the families each module is run on
    case "$1" in
        timeserie)    echo "sw ua iasi" ;;
        cardio)       echo "sw ua iasi" ;;
        zone)         echo "sw ua iasi ro ch" ;;
        scatter)      echo "sw iasi" ;;
        vdedr)        echo "iasi" ;;
        profile)      echo "ua ro ch" ;;
        verifprofile) echo "ro ch" ;;
        histogram)    echo "sw ua iasi" ;;
        obscountdb)   echo "sw ua iasi" ;;
        flags)        echo "sw ua iasi" ;;
        mapobs)       echo "sw ua iasi" ;;
        *)            echo "" ;;
    esac
}

set_value () {   # plain or bash-array assignment; silent if absent
    local file="$1" name="$2" value="$3"
    if grep -qE "^${name}=\(" "$file"; then
        sed -i -E "s|^${name}=\(.*|${name}=(${value})|" "$file"
    elif grep -qE "^${name}=" "$file"; then
        sed -i -E "s|^${name}=.*|${name}=\"${value}\"|" "$file"
    fi
}

MODULES=("$@")
[ ${#MODULES[@]} -eq 0 ] && MODULES=(timeserie cardio zone scatter vdedr profile verifprofile histogram obscountdb flags mapobs)

for m in "${MODULES[@]}"; do
    rm -rf "${BASE}/pikobs_coh_${m}"      # no old result stands in for a run that failed
    # the comparison wrapper when the module compares, else the single run
    src="${SCRIPTS}/run_${m}_cont_exp.sh"
    [ -f "$src" ] || src="${SCRIPTS}/run_${m}_exp.sh"
    [ -f "$src" ] || src="${SCRIPTS}/run_${m}.sh"
    fams="$(families_of "$m")"
    [ -f "$src" ] && [ -n "$fams" ] || { echo "== $m: skipped"; continue; }
    run="${BASE}/run_coh_${m}.sh"
    out="${BASE}/pikobs_coh_${m}"
    cp "$src" "$run"
    set_value "$run" FAMILY "$fams"
    set_value "$run" REGION "$REGIONS"
    set_value "$run" REGIONS "$REGIONS"
    set_value "$run" FLAGS_CRITERIA "$FLAG"
    set_value "$run" FLAG_CRITERIA "$FLAG"
    set_value "$run" MATCH "on"
    # the same two runs everywhere (a wrapper may default to another suite)
    set_value "$run" PATH_CONTROL_FILES "$CTL_PATH"
    set_value "$run" CONTROL_NAME "$CTL_NAME"
    set_value "$run" PATH_EXPERIENCE_FILES "$EXP_PATH"
    set_value "$run" EXPERIENCE_NAME "$EXP_NAME"
    set_value "$run" PATH_FILES "$EXP_PATH"
    set_value "$run" NAME "$EXP_NAME"
    # every station and every channel pooled, as the pair totals are
    set_value "$run" ID_STN "join"
    set_value "$run" CHANNEL "join"
    set_value "$run" DATESTART "$DAY_START"
    set_value "$run" DATEEND "$DAY_END"
    set_value "$run" PATHWORK "$out"
    echo "== $m: $fams"
    grep -nE "^(FAMILY|REGIONS?|FLAGS?_CRITERIA|MATCH|DATESTART|DATEEND|PATH_CONTROL_FILES|PATH_EXPERIENCE_FILES|ID_STN|CHANNEL)=" "$run" \
        | sed 's/^/     /'
    bash "$run" > "${out}.log" 2>&1
    grep -E "done --|FAILED|Traceback|skipped" "${out}.log" | sort | uniq -c | sed 's/^/     /'
done

dirs=()
for d in "${BASE}"/pikobs_coh_*; do [ -d "$d" ] && dirs+=("$d"); done
echo
echo "================ coherence, O-P ================"
python "${REPO}/pikobs/build_doc/coherence.py" "${dirs[@]}"
echo
echo "================ coherence, O-A ================"
python "${REPO}/pikobs/build_doc/coherence.py" --q oma "${dirs[@]}" | tail -30

# ---- tasks lost: a module that lost tasks produced an incomplete output ----
lost=$(grep -l "INCOMPLETE:\|tasks lost" "$HOME"/sites8/pikobs_coh_*.log 2>/dev/null)
if [ -n "$lost" ]; then
  echo
  echo "WARNING: tasks lost (incomplete output) in:"
  for f in $lost; do echo "  $f: $(grep -m1 'tasks lost' "$f" | cut -c1-100)"; done
fi
