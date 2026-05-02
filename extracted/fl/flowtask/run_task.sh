#!/bin/bash

for ((i = 1; i <= 1000; i++))
do
    echo "Running Task iteration $i"
    task --program=icims --task=download_forms --debug --no-worker
    if ((i < 100)); then
        echo "Pausing for 2 seconds..."
        sleep 2
    fi
done
