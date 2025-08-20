#!/bin/bash
set -euo pipefail

# Simplified test connection runner that just handles memory limits and executes datahub test
# All venv setup is handled in Python before calling this script

# Script arguments
venv_path="$1"
recipe_file="$2"
report_out_file="$3"

# Validate that the venv exists and has required components
if [ ! -f "$venv_path/bin/python" ]; then
    echo "ERROR: Python binary not found in venv: $venv_path/bin/python" >&2
    exit 1
fi

if [ ! -f "$venv_path/bin/datahub" ]; then
    echo "ERROR: DataHub CLI not found in venv: $venv_path/bin/datahub" >&2
    exit 1
fi

# Activate the venv
export VIRTUAL_ENV="$venv_path"
export PATH="$venv_path/bin:$PATH"

# Apply memory limit if set (this is what shell excels at!)
if [ -n "${EXECUTOR_TASK_MEMORY_LIMIT-}" ]; then
  echo "Setting memory limit to ${EXECUTOR_TASK_MEMORY_LIMIT}"
  ulimit -v "${EXECUTOR_TASK_MEMORY_LIMIT}"
fi

echo "recipe is at $recipe_file"

# Check if test-source-connection feature is available
if (datahub ingest run --help | grep -q test-source-connection); then
  echo "This version of datahub supports test-source-connection functionality"
  rm -f "$report_out_file"
  
  # Execute DataHub test connection (show command with set -x like original)
  set -x
  exec datahub ingest -c "${recipe_file}" --test-source-connection --report-to "${report_out_file}"
else
  echo "datahub ingest doesn't seem to have test_connection feature. You are likely running an old version"
  cat << EOF > "$report_out_file"
{
  "internal_failure": true,
  "internal_failure_reason": "datahub library doesn't have test_connection feature. You are likely running an old version."
}
EOF
  exit 0 # success here means we have succeeded at trying and we know why we failed
fi 