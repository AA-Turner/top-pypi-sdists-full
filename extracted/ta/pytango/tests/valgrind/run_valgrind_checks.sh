#!/usr/bin/env bash

# echo commands, and fail early
set -xeuo pipefail

# make sure we are in the same directory as the script
cd "$(dirname "$0")"

# Valgrind cannot handle Docker's very large file descriptor limits.
ulimit -n 1024

# Sanity check:
#  - run forced leak through valgrind, store result in XML file
#  - verify that our result parser finds the leak
PYTHONMALLOC=malloc valgrind \
  --leak-check=yes --show-leak-kinds=definite \
  --xml=yes --xml-file=vg_forced_leak.xml \
  python -c "import tango; tango._tango._force_mem_leak_1234_blocks()"

set +ex  # ignore errors
output="$(python check_valgrind_result.py vg_forced_leak.xml --max-blocks=1)"
if [ "$?" -eq 0 ]; then
  echo "check_valgrind_result.py output:"
  printf '%s\n' "$output"
  echo
  echo "Error: check_valgrind_result exited with code 0, expected non-zero due to forced leak."
  echo "Are you using a debug build? Did the extension .so filename change?"
  exit 1
fi
if ! grep ".*force_mem_leak_1234_blocks.*mem_leak_test.cpp.*_tango.*\.so" <<<"$output"; then
  echo "check_valgrind_result.py output:"
  printf '%s\n' "$output"
  echo
  echo "Error: check_valgrind_result did not report expected leak."
  echo "Are you using a debug build? Did the extension .so filename change?"
  exit 1
fi
echo "Sanity check for known leak was successful"
set -ex  # re-enable error checking

rm -f vg_*

# Run test server through valgrind, storing results for each child process in separate XML file
PYTHONMALLOC=malloc valgrind \
  --leak-check=yes --show-leak-kinds=definite --trace-children=yes \
  --xml=yes --xml-file=vg_%p.xml \
  python memory_test.py

# Python multiprocess.forkserver may have launched some processes that are still running,
# so we need to wait for them to complete
# don't exit early or echo commands
set +ex
MAX_ITERATIONS=240
SLEEP_INTERVAL=0.5

# Extract PIDs from filenames like vg_12345.xml
get_pids_from_xml() {
    for f in vg_*.xml; do
        [[ $f =~ ^vg_([0-9]+)\.xml$ ]] && echo "${BASH_REMATCH[1]}"
    done
}

# Check whether any of the PIDs are still running
any_pid_alive() {
    local pid
    for pid in "$@"; do
        if kill -0 "$pid" 2>/dev/null; then
            return 0  # at least one PID still alive
        fi
    done
    return 1  # none alive
}

# Wait for all processes to exit
echo "Waiting for Valgrind-traced processes to exit..."
iteration=0
while (( iteration < MAX_ITERATIONS )); do
    mapfile -t PIDS < <(get_pids_from_xml)

    if (( ${#PIDS[@]} == 0 )); then
        echo "No Valgrind XML files found - nothing to wait for."
        break
    fi

    if ! any_pid_alive "${PIDS[@]}"; then
        echo "All Valgrind-traced processes have exited."
        break
    fi

    sleep "$SLEEP_INTERVAL"
    ((++iteration))
done

if (( iteration >= MAX_ITERATIONS )); then
    echo "Timeout reached before all Valgrind-traced processes exited"
    ps aux | grep python
fi

# Check all files, and report errors at the end
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
