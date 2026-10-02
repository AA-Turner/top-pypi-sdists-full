#!/usr/bin/env bash
# ============================================================================
# test_match_modes.sh -- does MATCH work in its three forms, end to end?
#
#   ./test_match_modes.sh                     # timeserie and cardio
#   ./test_match_modes.sh zone histogram      # any comparing module
#
# For each module the comparison wrapper (run_<m>_cont_exp.sh) is copied,
# set to one day of sw, and run three times:
#
#   MATCH="on"                              the default key, with id_stn
#   MATCH="off"                             no pairing: Welch and F-test
#   MATCH="lat lon date time varno vcoord"  no id_stn: in sw a few winds
#                                           per cycle share that key, so
#                                           the run must WARN and still
#                                           pair them one to one
#
# Only what matters is shown: the key the run says it uses, warnings,
# the end, and any traceback. Full logs next to the outputs.
# Run from a compute node, from the repository root.
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPTS="${REPO}/pikobs/script"
WORK="/home/${USER}/sites8/pikobs_matchtest"
FAMILY="sw"
DAY_START="2026092000"
DAY_END="2026092018"
MODULES=("$@")
[ ${#MODULES[@]} -eq 0 ] && MODULES=(timeserie cardio)

set_value () {   # set_value <file> <name> <value>: plain or bash array
    local file="$1" name="$2" value="$3"
    if grep -qE "^${name}=\(" "$file"; then
        sed -i -E "s|^${name}=\(.*|${name}=(${value})|" "$file"
    elif grep -qE "^${name}=" "$file"; then
        sed -i -E "s|^${name}=.*|${name}=\"${value}\"|" "$file"
    else
        echo "  (no ${name}= in $(basename "$file"))"
    fi
}

mkdir -p "$WORK"
for m in "${MODULES[@]}"; do
    src="${SCRIPTS}/run_${m}_cont_exp.sh"
    if [ ! -f "$src" ]; then
        echo "== $m: no $src"; continue
    fi
    echo "==================== $m ===================="
    echo "how the wrapper passes MATCH:"
    grep -nE "^MATCH=|--match|MATCH" "$src" | grep -v "^[0-9]*:#" | head -5
    for mode in "on" "off" "lat lon date time varno vcoord"; do
        tag=$(echo "$mode" | tr ' ' '_')
        run="${WORK}/run_${m}_${tag}.sh"
        out="${WORK}/${m}_${tag}"
        log="${WORK}/${m}_${tag}.log"
        cp "$src" "$run"
        set_value "$run" MATCH "$mode"
        set_value "$run" FAMILY "$FAMILY"
        set_value "$run" DATESTART "$DAY_START"
        set_value "$run" DATEEND "$DAY_END"
        set_value "$run" PATHWORK "$out"
        echo "--- MATCH=\"$mode\""
        bash "$run" > "$log" 2>&1
        grep -E "key:|--match|WARNING|matched|NOT matched|done --|Traceback|Error" "$log" \
            | grep -v "^\[pikobs\] [a-z]*: [0-9]" | head -12
        echo "    (log: $log)"
    done
done
