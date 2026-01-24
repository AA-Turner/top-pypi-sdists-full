#!/usr/bin/env bash

# echo commands, and fail early
set -xeuo pipefail

# make sure we are in the same directory as the script
cd "$(dirname "$0")"

rm -f vg_*

# Run test server through valgrind, storing results for each child process in separate XML file
PYTHONMALLOC=malloc valgrind \
  --leak-check=yes --show-leak-kinds=definite --trace-children=yes \
  --xml=yes --xml-file=vg_%p.xml \
  python memory_test.py

# Check all files, but don't exit early or echo commands
set +ex
error=0
for file in vg_*.xml
do
  echo + python check_valgrind_result.py "$file" --max-blocks=1
  python check_valgrind_result.py "$file" --max-blocks=1
  if [ $? -ne 0 ]; then
    error=1
  fi
done
if [ $error -ne 0 ]; then
  echo "Error: At least one Valgrind problem found!"
  exit 1
fi
