#!/bin/bash
# count_obsvalue_neg1.sh
# Cuenta cuantas filas tienen OBSVALUE = -1 en uno o mas ficheros SQLite.
#
# Uso:
#   ./count_obsvalue_neg1.sh fichero.sqlite
#   ./count_obsvalue_neg1.sh /ruta/2026081800_*     # varios de golpe

for f in "$@"; do
    [ -f "$f" ] || continue
    total=$(sqlite3 "$f" "SELECT COUNT(*) FROM data;" 2>/dev/null)
    neg1=$(sqlite3 "$f" "SELECT COUNT(*) FROM data WHERE OBSVALUE = -1;" 2>/dev/null)
    if [ -z "$total" ]; then
        echo "$(basename "$f")  -- no se pudo leer (no es sqlite valido o falta tabla data)"
        continue
    fi
    pct=$(awk -v n="$neg1" -v t="$total" 'BEGIN{ if(t>0) printf "%.2f", 100*n/t; else print "0.00" }')
    printf "%-40s  OBSVALUE=-1: %8s / %8s  (%s%%)\n" "$(basename "$f")" "$neg1" "$total" "$pct"
done
