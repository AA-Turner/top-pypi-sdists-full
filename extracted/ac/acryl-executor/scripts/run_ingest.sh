#!/bin/bash
set -euo pipefail

# Simplified ingestion runner that just handles memory limits and executes datahub
# All venv setup is handled in Python before calling this script

# Script arguments
venv_path="$1"
recipe_file="$2"
report_out_file="$3"
debug_mode="${4:-false}"

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

# Check for report-to support
if (datahub ingest run --help | grep -q report-to); then
  echo "This version of datahub supports report-to functionality"
  rm -f "$report_out_file"
  report_option="--report-to ${report_out_file}"
else
  report_option=""
fi

# Set debug option if enabled
if [ "$debug_mode" == "true" ]; then 
  debug_option="--debug"
else
  debug_option=""
fi

# Execute DataHub recipe (show command with set -x like original)
set -x
exec datahub ${debug_option} ingest run -c "${recipe_file}" ${report_option} 