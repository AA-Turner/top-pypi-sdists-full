#!/usr/bin/env bash

# script to setup kind cluster for local development

set -ex

# for CI to setup kind separately so we don't need to worry about installing kind
if [[ $SKIP_KIND_CLUSTER_SETUP -eq 1 ]]; then
  echo "Skipping kind cluster setup"
  exit 0
fi

if command -v "kind" &> /dev/null; then
  echo "Found that 'kind' exists."
else
  echo "'kind' is not found, please refer to DEVELOPMENT.md and setup kind cli locally"
  exit 1
fi

force=0

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -f|--force)
      force=1
      shift
      ;;
    *)
      echo "Unknown option: $1"
      shift
      ;;
  esac
done

# check if cluster exist
existing_cluster=$(kind get clusters | grep geneva | wc -l)

if [[ $existing_cluster -gt 0 ]]; then
  if [[ $force -eq 1 ]]; then
    echo "Deleting existing cluster"
    kind delete cluster --name geneva
  else
    echo "Cluster already exists. Use -f to force delete and recreate"
    exit 0
  fi
fi

# Create a kind cluster
kind create cluster --name geneva --config .github/workflows/test.yml.kind
