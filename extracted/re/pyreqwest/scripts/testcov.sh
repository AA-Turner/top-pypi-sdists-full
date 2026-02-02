#!/bin/bash
set -euo pipefail

rm -f python/pyreqwest/*.so
rm -f *.profraw
rm -rf coverage/

RUSTFLAGS='-C instrument-coverage' make test

OUTPUT_ARGS=("--output-type" "html" "--output-path" "./coverage" "--html-resources" "cdn")
if [[ "${CI:-0}" == "1" ]]; then
  OUTPUT_ARGS=("--output-type" "lcov" "--output-path" "./coverage/lcov.info")
  mkdir coverage
fi

grcov . \
  --binary-path ./python/pyreqwest/*.so \
  --source-dir ./src \
  "${OUTPUT_ARGS[@]}" \
  --branch \
  --ignore-not-existing \
  --ignore '**/build.rs' \
  --excl-start ':NOCOV_START' \
  --excl-stop ':NOCOV_END' \
  --excl-line ':NOCOV|^( )+}$|unreachable!|^#\['

rm -f *.profraw
