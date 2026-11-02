"""Shared constants for cube-mcp ecosystem."""

# EdgescaleAI Teleport proxy URL
DEFAULT_PROXY = "edgescaleai.teleport.sh"

# Apollo Container Registry (ACR) configuration
ACR_REGISTRY = "edgescaleai.palantirapollo.com"
ACR_DOCKER_PREFIX = f"{ACR_REGISTRY}/com.edgescaleai-cube"
ACR_HELM_PREFIX = f"oci://{ACR_REGISTRY}/charts/com.edgescaleai-cube"
ACR_TOKEN_URL = f"https://{ACR_REGISTRY}/multipass/api/oauth2/token"
APOLLO_URL = f"https://{ACR_REGISTRY}"
APOLLO_GRAPHQL_URL = f"https://{ACR_REGISTRY}/graphql-gateway/api/graphql"
APOLLO_GRAPHQL_USER_AGENT = "apollo-sdk/0.0.15 forge-graphql-client/4.93.0"
APOLLO_GROUP_ID = "com.edgescaleai-cube"
