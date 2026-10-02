#!/usr/bin/env bash
# ============================================================================
# check_duplicates.sh -- how often does the match key repeat, per family?
#
# The match key used by pikobs: id_stn, date, time, lat and lon rounded to
# 4 decimals, varno, vcoord. For every family file of one or more cycles,
# counts over the rows that carry a departure (O-P or O-A):
#
#   rows        rows with a departure
#   dup_keys    keys that appear more than once
#   dup_rows    rows inside those keys
#   dup_w_obs   keys still repeated when obsvalue is added to the key
#               (small against dup_keys: obsvalue tells them apart;
#                close to it: true duplicates, the same datum twice)
#
#   ./check_duplicates.sh                             # G0, latest cycle
#   ./check_duplicates.sh -c 2026092000               # one cycle
#   ./check_duplicates.sh -c "2026092000 2026092012"  # several
#   ./check_duplicates.sh -d /path/to/banco/postalt   # another run
#   ./check_duplicates.sh -j 16                       # families in parallel
#   ./check_duplicates.sh -k "lat lon date time varno vcoord"   # another key
#
# Key fields (-k): id_stn date time lat lon varno vcoord codtyp obsvalue
# (lat and lon rounded to 4 decimals, as in the matching).
#
# Read-only: the files are opened immutable, nothing is written next to them.
# ============================================================================
set -uo pipefail

DIR="/home/smco500/.suites/gdps/g0/hub/ppp7/monitoring/banco/postalt"
CYCLES=""
JOBS=8
KEY="id_stn date time lat lon varno vcoord"
while getopts "d:c:j:k:h" opt; do
    case $opt in
        d) DIR="$OPTARG" ;;
        c) CYCLES="$OPTARG" ;;
        j) JOBS="$OPTARG" ;;
        k) KEY="$OPTARG" ;;
        *) sed -n '2,28p' "$0"; exit 0 ;;
    esac
done

if [ -z "$CYCLES" ]; then
    CYCLES=$(ls "$DIR" | grep -oE '^[0-9]{10}' | sort -u | tail -1)
fi

# key fields -> SQL columns
SEL=""; GRP=""; i=0
for f in $KEY; do
    case $f in
        id_stn)   e="h.id_stn" ;;
        date)     e="h.date" ;;
        time)     e="h.time" ;;
        lat)      e="ROUND(h.lat,4)" ;;
        lon)      e="ROUND(h.lon,4)" ;;
        varno)    e="d.varno" ;;
        vcoord)   e="d.vcoord" ;;
        codtyp)   e="h.codtyp" ;;
        obsvalue) e="d.obsvalue" ;;
        *) echo "unknown key field: $f" >&2; exit 1 ;;
    esac
    i=$((i+1)); SEL="$SEL, $e k$i"; GRP="$GRP,k$i"
done
export KSEL="${SEL#, }" KGRP="${GRP#,}"

count_one () {   # count_one <file>
    local f="$1" name cyc fam r
    name=$(basename "$f"); cyc=${name%%_*}; fam=${name#*_}
    r=$(sqlite3 -separator ' ' "file:$f?mode=ro&immutable=1" "
      WITH k AS (SELECT $KSEL, d.obsvalue ov
                 FROM header h JOIN data d USING(id_obs)
                 WHERE d.omp IS NOT NULL OR d.oma IS NOT NULL),
           g AS (SELECT COUNT(*) n FROM k
                 GROUP BY $KGRP HAVING COUNT(*)>1)
      SELECT (SELECT COUNT(*) FROM k), (SELECT COUNT(*) FROM g),
             (SELECT COALESCE(SUM(n),0) FROM g),
             (SELECT COUNT(*) FROM (SELECT 1 FROM k
                 GROUP BY $KGRP,ov HAVING COUNT(*)>1));" 2>/dev/null)
    [ -z "$r" ] && r="- - - -  (not readable as pikobs banco)"
    printf "%-10s %-24s %s\n" "$cyc" "$fam" "$r"
}
export -f count_one

echo "dir:    $DIR"
echo "cycles: $CYCLES"
echo "key:    $KEY"
echo
OUT=$(mktemp)
trap 'rm -f "$OUT"' EXIT
for c in $CYCLES; do ls -1 "$DIR"/${c}_* 2>/dev/null; done \
  | xargs -P "$JOBS" -I{} bash -c 'count_one "$@"' _ {} \
  | sort > "$OUT"

{ printf "%-10s %-24s %s\n" cycle family "rows dup_keys dup_rows dup_w_obs"
  cat "$OUT"; } | { command -v column >/dev/null && column -t || cat; }

echo
echo "families with repeated keys:"
awk '$4 ~ /^[0-9]+$/ && $4 > 0 {print "  " $2 " (" $1 "): " $4 " keys, " $5 " rows, " $6 " still repeated with obsvalue"}' "$OUT"
awk '$4 ~ /^[0-9]+$/ && $4 > 0 {n++} END {if (!n) print "  none"}' "$OUT"
