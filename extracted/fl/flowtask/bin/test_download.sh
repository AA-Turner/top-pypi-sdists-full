#!/bin/bash

# Define the end time which is 2 minutes from now
END=$(date -ud "60 minutes" +%s)

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 OFFSET"
    exit 1
fi
OFFSET=$1

while [[ $(date -u +%s) -le $END ]]
do
    task --program=icims --task=download_forms --no-worker --no-notify --ignore-results --conditions OFFSET:$OFFSET
    sleep 2
done
