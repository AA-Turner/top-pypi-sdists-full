#!/usr/bin/env bash
# ============================================================================
# bench_modules.sh -- time and memory of every module at two volumes.
#
# Each module runs twice on the G0 / G2 pair: one day and six days, the same
# selection as test_coherence.sh (Monde and Canada, assimilee, stations and
# channels pooled, MATCH=on), under bench_run.py, which samples the memory
# of the whole process tree. bench_table.py turns the results into the
# table: seconds per GB, peak memory, the node to ask for.
#
#   pikobs/build_doc/bench_modules.sh                 # every module
#   pikobs/build_doc/bench_modules.sh zone scatter    # some
#
# Run it as a batch job on the node size you want to characterise (the
# peak memory depends on the number of workers, see N_CPUS below). From the
# repository root. Outputs in /home/$USER/sites8/pikobs_bench_<module>_<n>d.
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPTS="${REPO}/pikobs/script"
BASE="/home/${USER}/sites8"
N_CPUS="${N_CPUS:-80}"
CTL_PATH="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
EXP_PATH="/home/smco500/.suites/gdps/g2/hub/ppp7/monitoring/banco/postalt"
PERIODS=("1:2026092000:2026092018" "6:2026091700:2026092218")

families_of () {
    case "$1" in
        timeserie|cardio|histogram|obscountdb|flags|mapobs) echo "sw ua iasi" ;;
        zone)         echo "sw ua iasi ro" ;;
        scatter)      echo "sw iasi" ;;
        vdedr)        echo "iasi" ;;
        profile)      echo "ua ro" ;;
        verifprofile) echo "ro" ;;
        *)            echo "" ;;
    esac
}

set_value () {
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
    src="${SCRIPTS}/run_${m}_cont_exp.sh"
    [ -f "$src" ] || src="${SCRIPTS}/run_${m}_exp.sh"
    [ -f "$src" ] || src="${SCRIPTS}/run_${m}.sh"
    fams="$(families_of "$m")"
    [ -f "$src" ] && [ -n "$fams" ] || { echo "== $m: skipped"; continue; }
    for p in "${PERIODS[@]}"; do
        IFS=: read -r days d0 d1 <<< "$p"
        out="${BASE}/pikobs_bench_${m}_${days}d"
        run="${BASE}/run_bench_${m}_${days}d.sh"
        cp "$src" "$run"
        set_value "$run" FAMILY "$fams"
        set_value "$run" REGION "Monde Canada"
        set_value "$run" FLAGS_CRITERIA "assimilee"
        set_value "$run" MATCH "on"
        set_value "$run" DATESTART "$d0"
        set_value "$run" DATEEND "$d1"
        set_value "$run" PATHWORK "$out"
        set_value "$run" PATH_CONTROL_FILES "$CTL_PATH"
        set_value "$run" CONTROL_NAME "G0"
        set_value "$run" PATH_EXPERIENCE_FILES "$EXP_PATH"
        set_value "$run" EXPERIENCE_NAME "G2"
        set_value "$run" PATH_FILES "$EXP_PATH"
        set_value "$run" NAME "G2"
        set_value "$run" ID_STN "join"
        set_value "$run" CHANNEL "join"
        set_value "$run" N_CPUS "$N_CPUS"
        set_value "$run" N_CPU "$N_CPUS"
        echo "== $m, ${days} day(s)"
        python "${REPO}/pikobs/build_doc/bench_run.py" \
            --out "${BASE}/bench_${m}_${days}d_mem.json" -- bash "$run" \
            > "${out}.log" 2>&1
        grep -E "done --|Traceback|FAILED|\[bench\]" "${out}.log" | sed 's/^/     /'
    done
done

python "${REPO}/pikobs/build_doc/bench_table.py"
