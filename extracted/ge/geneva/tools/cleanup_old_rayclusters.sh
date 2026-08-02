#!/bin/bash
# Cleanup RayCluster resources older than a specified age
# Usage: cleanup_old_rayclusters.sh [HOURS] [NAMESPACE]
#   HOURS: Delete clusters older than this many hours (default: 12)
#   NAMESPACE: Kubernetes namespace (default: geneva)

set -e

HOURS=${1:-12}
NAMESPACE=${2:-geneva}

echo "Cleaning up RayClusters older than ${HOURS} hours in namespace ${NAMESPACE}"

CUTOFF=$(date -u -d "${HOURS} hours ago" '+%Y-%m-%dT%H:%M:%SZ')

kubectl get raycluster -n "${NAMESPACE}" -o json | \
  jq -r --arg cutoff "$CUTOFF" '.items[] | select(.metadata.creationTimestamp < $cutoff) | .metadata.name' | \
  xargs -r -n1 kubectl delete raycluster -n "${NAMESPACE}" --timeout=30s || {
    echo "Cleanup had errors, continuing..."
    exit 0
  }

echo "Cleanup completed successfully"
