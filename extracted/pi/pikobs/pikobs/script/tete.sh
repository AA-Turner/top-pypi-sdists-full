#!/bin/bash
# diagnose_empty_families.sh
#
# Prueba cada familia que salio vacia (24576 bytes = 0 registros) CON y SIN
# -ade, para ver exactamente cuales lo necesitan. No modifica nada, solo
# muestra "Select Codtyp ... N Records" de cada intento en /tmp.
#
# Uso: ajusta BURP2RDB y CUTOFF_DIR si hace falta, luego:
#   ./diagnose_empty_families.sh

set -u
BURP2RDB="/fs/ssm/eccc/cmd/cmda/utils/20260202/rhel-9-amd64-64/bin/burp2rdb"
CUTOFF_DIR="/home/smco500/.suites/gdps/g2/hub/ppp7/banco/cutoff"
DATE="2026081800"
OUTDIR="/tmp/diag_ade_$$"
mkdir -p "$OUTDIR"

# family:type  -- las que salieron con 0 registros (24576 bytes) en tu listado
FAMILIES=(
  "ua_cmc:ua"
  "to_amsub:amsub"
  "to_amsua:amsua"
  "ssmis:ssmi"
  "ro:ro"
  "rars_mwhs2:mwhs"
  "rars_atms:atms"
  "rars_amsub:amsub"
  "rars_amsua:amsua"
  "pr:pr"
  "mwhs2:mwhs"
  "iasi:iasi"
  "gp_b:gbgps"
  "gp:gbgps"
  "csr:csr"
  "crisfsr:cris"
  "ch_gome:sf"
  "atms:atms"
)

printf "%-16s %-8s %8s %10s %10s   %s\n" "familia" "type" "en_input" "sin_-ade" "con_-ade" "conclusion"
printf '%s\n' "--------------------------------------------------------------------------------------"

for entry in "${FAMILIES[@]}"; do
    fam="${entry%%:*}"
    typ="${entry##*:}"
    infile="${CUTOFF_DIR}/${DATE}_${fam}"

    if [ ! -f "$infile" ]; then
        printf "%-16s %-8s %8s %10s %10s   %s\n" "$fam" "$typ" "n/a" "n/a" "n/a" "fichero de entrada no encontrado"
        continue
    fi

    out_no="${OUTDIR}/${fam}_no_ade.rdb"
    out_yes="${OUTDIR}/${fam}_ade.rdb"
    log_no="${OUTDIR}/${fam}_no_ade.log"
    log_yes="${OUTDIR}/${fam}_ade.log"

    "$BURP2RDB" -in "$infile" -type "$typ" -out "$out_no" > "$log_no" 2>&1
    n_no=$(grep -E "deriBurpSelector|adeBurpSelector" "$log_no" | grep -oE '[0-9]+ Records' | grep -oE '^[0-9]+')

    "$BURP2RDB" -in "$infile" -type "$typ" -out "$out_yes" -ade > "$log_yes" 2>&1
    n_yes=$(grep -E "deriBurpSelector|adeBurpSelector" "$log_yes" | grep -oE '[0-9]+ Records' | grep -oE '^[0-9]+')

    n_in=$(grep "BurpFile contains" "$log_no" | grep -oE '[0-9]+ Records' | grep -oE '^[0-9]+')

    if [ "$n_in" = "0" ]; then
        concl="fichero de entrada VACIO (0 registros) -> no es tema de -ade"
    elif [ "$n_no" = "0" ] && [ "$n_yes" != "0" ] && [ "$n_yes" != "" ]; then
        concl="NECESITA -ade"
    elif [ "$n_no" != "0" ] && [ "$n_no" != "" ]; then
        concl="ya funciona sin -ade (revisar por que salio vacio antes)"
    elif [ "$n_no" = "0" ] && [ "$n_yes" = "0" ]; then
        concl="sigue en 0 CON y SIN -ade, pero el fichero SI tiene datos -> revisar log"
    else
        concl="parseo fallo -- ver log: $log_yes"
    fi

    n_no_disp=${n_no:-ERROR}
    n_yes_disp=${n_yes:-ERROR}
    n_in_disp=${n_in:-?}

    printf "%-16s %-8s %8s %10s %10s   %s\n" "$fam" "$typ" "$n_in_disp" "$n_no_disp" "$n_yes_disp" "$concl"
done

echo ""
echo "RDBs y LOGS de prueba en: $OUTDIR"
echo "  (si alguna fila dice 'parseo fallo', mira su log_yes/log_no directamente:"
echo "   cat $OUTDIR/<familia>_ade.log )"
echo "  borralos cuando termines: rm -rf $OUTDIR"
