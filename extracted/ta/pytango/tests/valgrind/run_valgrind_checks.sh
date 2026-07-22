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
#
# NOTE: we intentionally fail only on "definite" leaks. Leaked *Python* references
# (e.g. a missing decref in the C++ exception-translation path) are NOT catchable
# here: the orphaned Python objects remain linked in CPython's GC generation list,
# so valgrind classifies them as "still reachable" / "possibly lost", never
# "definitely lost". Widening --show-leak-kinds does not help -- the possibly-lost
# count is dominated by interpreter/pybind11 noise and is non-deterministic (it does
# not even shrink when the leak is fixed). Such reference leaks must be found via
# heap growth over time (heaptrack, or an RSS-plateau test), not leak-check-at-exit.
# memory_test.py has a built-in RSS-plateau check for exactly that -- but it is only
# meaningful WITHOUT valgrind, whose allocator makes RSS climb on its own. So we run
# the script twice: plainly (RSS check on, may fail) and under valgrind (check off).

# Plain run: RSS-plateau check enabled, exits non-zero if RSS grows. Capture the
# result but don't fail yet -- re-thrown together with valgrind errors below.
set +e
python memory_test.py
rss_exit=$?
set -e

# Valgrind run: leak-check only; disable the RSS check (it would false-positive here).
MEMTEST_RSS_CHECK=0 PYTHONMALLOC=malloc valgrind \
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
if [ "${rss_exit:-0}" -ne 0 ]; then
  echo "Error: RSS growth detected by memory_test.py RSS-plateau check (exit ${rss_exit})!"
  error=1
fi
if [ $error -ne 0 ]; then
  echo "Error: At least one Valgrind or RSS problem found!"
  exit 1
fi
