#!/usr/bin/env bash
# Everything the documentation needs: the reference runs, the figures
# they leave behind, and the pages. An hour is a long time to stare at a
# blank terminal, so each run says where the batch is and how long it
# has taken; the detail of each one is in the log.
set -uo pipefail

cd /fs/homeu3/eccc/cmd/cmda/dlo001/python/Pikobs || exit 1
source ~/pikobs_install/load_pikobs.sh

LOG=/tmp/doc_runs.log
: > "${LOG}"
START=$(date +%s)

cd pikobs/script
JOBS=$(./run_doc_examples.sh --dry-run 2>/dev/null | grep -c "^ [a-z]")
echo "=== reference runs: ${JOBS} to do, output in ${LOG}"

./run_doc_examples.sh < /dev/null 2>&1 | tee -a "${LOG}" | while read -r line; do
    case "${line}" in
        \ [a-z]*\ -\>\ *)                      # the header of a run
            done_n=$(grep -c "^ [a-z].* -> " "${LOG}")
            el=$(( $(date +%s) - START ))
            printf '[%2d/%2d  %3d%%  %2dm%02ds]  %s\n' \
                   "${done_n}" "${JOBS}" $(( done_n * 100 / JOBS )) \
                   $(( el / 60 )) $(( el % 60 )) "${line# }"
            ;;
        *FAILED*|*"done:"*) echo "${line}" ;;
    esac
done

cd ..
cd ..
echo "=== figures"
./build_images.sh 2>&1 | tee /tmp/doc_images.log | grep -E "skip|FAIL" \
    || echo "  every figure found"

echo "=== pages"
./pikobs_doc.sh

el=$(( $(date +%s) - START ))
printf '=== finished in %dm%02ds\n' $(( el / 60 )) $(( el % 60 ))
