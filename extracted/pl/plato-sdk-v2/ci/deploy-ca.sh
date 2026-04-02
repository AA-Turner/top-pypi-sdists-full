#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

DOMAIN="plato"
DOMAIN_OWNER="383806609161"
REPO="pypi-store"
REGION="us-west-2"

# Get CodeArtifact auth token using local AWS creds
CA_TOKEN=$(aws codeartifact get-authorization-token \
  --domain "$DOMAIN" \
  --domain-owner "$DOMAIN_OWNER" \
  --region "$REGION" \
  --query authorizationToken \
  --output text)

CA_URL="https://${DOMAIN}-${DOMAIN_OWNER}.d.codeartifact.${REGION}.amazonaws.com/pypi/${REPO}/"

# Build only if dist/ doesn't already exist (caller may have already built)
if [ ! -d dist ] || [ -z "$(ls -A dist)" ]; then
  rm -rf dist
  uv build
fi
unset UV_PUBLISH_TOKEN
uv publish --publish-url "$CA_URL" --username aws --password "$CA_TOKEN"
