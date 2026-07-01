#!/bin/bash
# Teardown script — runs after verification, regardless of pass/fail.
# See: https://docs.dreadnode.io/evaluations/tasks/
#
# Contract (TSK-TEAR-001..005):
#   - Runs alongside the task services, same as provision.
#   - Has access to evaluation secrets via env vars.
#   - Best-effort: failures are logged but do not change the verification result.
#   - Default timeout: 120 seconds.
#
# Examples:
#
# # Tear down a lab instance created by provision
# python3 teardown_lab.py \
#   --username "$SERVICE_USERNAME" \
#   --password "$SERVICE_PASSWORD" \
#   --lab-url "$LAB_URL"

set -euo pipefail

# TODO: replace with your cleanup logic.
exit 0
