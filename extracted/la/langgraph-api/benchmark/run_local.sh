#!/bin/bash
cd "$(dirname "$0")"

BACKENDS=(
  "https://benchmark-s-6d17010be8a25023a9eab0a688d29c05.staging.langgraph.app"
  "https://benchmark-m-fd2e770a72f55324b6c59f2664a56d32.staging.langgraph.app"
  "https://benchmark-l-d655833b3cba5fc8a703c95f20045831.staging.langgraph.app"
  "https://benchmark-dr-s-2799835ad04b501a95044223ae72ced7.staging.langgraph.app"
  "https://benchmark-dr-m-ec079ea9f20e5655ab35a4ebc1a0ade8.staging.langgraph.app"
  "https://benchmark-dr-l-e996bbdcfbf15c9e8f547ab74fae93d2.staging.langgraph.app"
)

QUICK_VUS_LIST=(100 250 1000)
LONG_VUS_LIST=(2 5 10)

for backend in "${BACKENDS[@]}"; do
  for quick in "${QUICK_VUS_LIST[@]}"; do
    for long in "${LONG_VUS_LIST[@]}"; do
      echo "=== Running: $backend | QUICK_VUS=$quick LONG_VUS=$long ==="
      BASE_URL="$backend" QUICK_VUS="$quick" LONG_VUS="$long" make benchmark-mixed

      echo "=== Uploading results to Datadog ==="
      BASE_URL="$backend" ../.venv/bin/python reporting/dd_reporting.py "mixed_workload_*.json"
      rm -f mixed_workload_*.json
    done
  done
done
