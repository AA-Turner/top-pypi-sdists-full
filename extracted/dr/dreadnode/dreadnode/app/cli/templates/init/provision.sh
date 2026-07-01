#!/bin/bash
# Provision script — runs before the agent receives its instruction.
# See: https://docs.dreadnode.io/evaluations/tasks/
#
# Contract (TSK-PROV-002):
#   - The script must output a single JSON object to stdout.
#   - Each top-level key becomes a {{template_var}} in the instruction.
#   - Secrets from the evaluation's secret_ids are injected as env vars.
#   - Default timeout: 120 seconds.
#
# Examples:
#
# # Spin up a remote lab and return its URL
# LAB_URL=$(python3 provision_lab.py \
#   --username "$SERVICE_USERNAME" \
#   --password "$SERVICE_PASSWORD")
# echo "{\"lab_url\": \"$LAB_URL\"}"
#
# # Generate a per-attempt random token
# TOKEN=$(openssl rand -hex 16)
# echo "{\"attempt_token\": \"$TOKEN\"}"

set -euo pipefail

# TODO: replace with your provisioning logic.
# Output MUST be a JSON object on stdout. Stderr is ignored by the platform.
echo '{}'
