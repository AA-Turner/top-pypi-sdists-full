#!/bin/bash

for i in {1..1000}
do
    echo "Run #$i"
    ENV=prod task --program=networkninja --task=test_nn --debug --no-worker
    echo "Sleeping for 5 seconds..."
    sleep 5
done
