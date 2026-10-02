#!/bin/bash

CYCLE="2026081800"
DIR_CUT="/home/dlo001/sites8/pikobs_rdb_cutoff/g2ops"
DIR_POS="/home/dlo001/sites8/pikobs_rdb_postalt/g2ops"

# Temporary files
TMP_RAW=$(mktemp)
TMP_RANK=$(mktemp)

# Global variables
G_TOT_CUT=0
G_MINUS_ONE=0
G_TOT_POS=0
G_ASSIM=0

# 1. DATA COLLECTION
for FILE_POS in ${DIR_POS}/${CYCLE}_*; do
    
    filename=$(basename "$FILE_POS")
    FAMILY=${filename#${CYCLE}_}
    SEARCH_FAMILY=${FAMILY/_allsky/}

    TOT_CUT=0
    CUT_MINUS_ONE=0
    
    for file in ${DIR_CUT}/${CYCLE}*${SEARCH_FAMILY}*; do
        if [ -f "$file" ]; then
            res=$(sqlite3 "$file" "SELECT COUNT(*), COUNT(CASE WHEN obsvalue = -1 THEN 1 END) FROM data;" 2>/dev/null)
            count=${res%|*}
            count_minus=${res#*|}
            
            [[ "$count" =~ ^[0-9]+$ ]] && TOT_CUT=$((TOT_CUT + count))
            [[ "$count_minus" =~ ^[0-9]+$ ]] && CUT_MINUS_ONE=$((CUT_MINUS_ONE + count_minus))
        fi
    done

    res_pos=$(sqlite3 "$FILE_POS" "SELECT COUNT(*), COUNT(CASE WHEN (flag & 4096) = 4096 THEN 1 END) FROM data;" 2>/dev/null)
    TOT_POS=${res_pos%|*}
    ASSIM=${res_pos#*|}

    [[ -z "$TOT_POS" ]] && TOT_POS=0
    [[ -z "$ASSIM" ]] && ASSIM=0

    # Add to global counters
    G_TOT_CUT=$((G_TOT_CUT + TOT_CUT))
    G_MINUS_ONE=$((G_MINUS_ONE + CUT_MINUS_ONE))
    G_TOT_POS=$((G_TOT_POS + TOT_POS))
    G_ASSIM=$((G_ASSIM + ASSIM))

    # Calculate percentages (Post/Cut, Assim/Post, Assim/Cut)
    if [ "$TOT_CUT" -gt 0 ]; then
        PCT_MINUS=$(awk "BEGIN {printf \"%.3f\", ($CUT_MINUS_ONE * 100) / $TOT_CUT}")
        PCT_POS=$(awk "BEGIN {printf \"%.3f\", ($TOT_POS * 100) / $TOT_CUT}")
        PCT_ASIM_CUT=$(awk "BEGIN {printf \"%.3f\", ($ASSIM * 100) / $TOT_CUT}")
    else
        PCT_MINUS="0.000"
        PCT_POS="0.000"
        PCT_ASIM_CUT="0.000"
    fi

    if [ "$TOT_POS" -gt 0 ]; then
        PCT_ASIM=$(awk "BEGIN {printf \"%.2f\", ($ASSIM * 100) / $TOT_POS}")
    else
        PCT_ASIM="0.00"
    fi

    # Save to temporary file
    echo "$FAMILY $TOT_CUT $CUT_MINUS_ONE $PCT_MINUS $TOT_POS $PCT_POS $ASSIM $PCT_ASIM $PCT_ASIM_CUT" >> "$TMP_RAW"

done

# 2. CALCULATE ASSIMILATION RANKING (Sort by column 7: ASSIM, descending)
sort -k7,7nr "$TMP_RAW" | awk '{print $1, NR}' > "$TMP_RANK"

# 3. PRINT THE SORTED TABLE (Sort by column 2: CUTOFF, descending)
echo "================================================================================================================================================="
echo " ASSIMILATION SUMMARY (Sorted descending by TOT CUTOFF) - Cycle: $CYCLE"
echo "================================================================================================================================================="
printf "%-18s | %-11s | %-10s | %-9s | %-11s | %-10s | %-11s | %-4s | %-11s | %-10s\n" "FAMILY" "TOT CUTOFF" "OBS=-1 (N)" "% OBS=-1" "TOT POSTALT" "% POST/CUT" "ASSIMILATED" "RANK" "% ASSIM/POS" "% ASSIM/CUT"
echo "-------------------------------------------------------------------------------------------------------------------------------------------------"

sort -k2,2nr "$TMP_RAW" | while read -r FAM TC CM PM TP PP AS PA PAC; do
    RANK=$(awk -v f="$FAM" '$1==f {print $2}' "$TMP_RANK")
    printf "%-18s | %-11d | %-10d | %-7s %% | %-11d | %-8s %% | %-11d | #%-3d | %-9s %% | %-8s %%\n" "$FAM" "$TC" "$CM" "$PM" "$TP" "$PP" "$AS" "$RANK" "$PA" "$PAC"
done

echo "-------------------------------------------------------------------------------------------------------------------------------------------------"

# 4. PRINT GLOBAL TOTALS
if [ "$G_TOT_CUT" -gt 0 ]; then
    G_PCT_MINUS=$(awk "BEGIN {printf \"%.3f\", ($G_MINUS_ONE * 100) / $G_TOT_CUT}")
    G_PCT_POS=$(awk "BEGIN {printf \"%.3f\", ($G_TOT_POS * 100) / $G_TOT_CUT}")
    G_PCT_ASIM_CUT=$(awk "BEGIN {printf \"%.3f\", ($G_ASSIM * 100) / $G_TOT_CUT}")
else
    G_PCT_MINUS="0.000"
    G_PCT_POS="0.000"
    G_PCT_ASIM_CUT="0.000"
fi

if [ "$G_TOT_POS" -gt 0 ]; then
    G_PCT_ASIM=$(awk "BEGIN {printf \"%.2f\", ($G_ASSIM * 100) / $G_TOT_POS}")
else
    G_PCT_ASIM="0.00"
fi

printf "%-18s | %-11d | %-10d | %-7s %% | %-11d | %-8s %% | %-11d | %-4s | %-9s %% | %-8s %%\n" "GLOBAL TOTAL" "$G_TOT_CUT" "$G_MINUS_ONE" "$G_PCT_MINUS" "$G_TOT_POS" "$G_PCT_POS" "$G_ASSIM" "-" "$G_PCT_ASIM" "$G_PCT_ASIM_CUT"
echo "================================================================================================================================================="

rm -f "$TMP_RAW" "$TMP_RANK"
