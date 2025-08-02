"""Azure Management Configuration for the azpaddypy library.

This module provides a centralized configuration for Azure services required by the
azpaddypy library and associated applications. It uses the azpaddypy builder
pattern to set up identity, logging, key vaults, storage, and Cosmos DB.

The configuration follows this sequence:
1. Environment Detection: Determines if running locally or in Docker.
2. Management Services: Configures logging, identity, and Key Vault clients.
3. Resource Services: Sets up Storage and Cosmos DB clients using secrets from Key Vault.

Required Environment Variables:
    - key_vault_uri: The URL of the primary application Key Vault.
    - head_key_vault_uri: The URL of the head/admin Key Vault.

Optional Environment Variables:
    - LOGGER_LOG_LEVEL: Sets the logging level (e.g., "INFO", "DEBUG").
    - APPLICATIONINSIGHTS_CONNECTION_STRING: For connecting to Application Insights.

Exported Services:
    - logger: Centralized logger for the application.
    - identity: Azure identity credential for authentication.
    - keyvaults: A dictionary of Key Vault clients ("main", "head").
    - storage_accounts: A dictionary of storage clients ("main").
    - cosmos_dbs: A dictionary of Cosmos DB clients ("promptmgmt").
    - prompt_manager: A client for managing prompts in Cosmos DB.

Usage Example:
    from mgmt_config import logger, keyvaults

    logger.info("Service started.")
    secret = keyvaults.get("main").get_secret("my-secret")
"""

import os
from typing import Optional

from azpaddypy.builder import (
    ConfigurationSetupBuilder,
    AzureManagementBuilder,
    AzureResourceBuilder,
    AzureManagementConfiguration,
    AzureResourceConfiguration,
)


# =============================================================================
# Environment Configuration
# =============================================================================

# These settings enable local Azure Functions development with the Azurite storage emulator.
LOCAL_DEVELOPMENT_STORAGE_CONFIG = {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AzureWebJobsDashboard": "UseDevelopmentStorage=true",
    "input_queue_connection__queueServiceUri": "UseDevelopmentStorage=true",
    "AzureWebJobsStorage__accountName": "UseDevelopmentStorage=true",
    "AzureWebJobsStorage__blobServiceUri": "UseDevelopmentStorage=true",
    "AZURE_CLIENT_ID": "aa7...",
    "AZURE_TENANT_ID": "e55...",
    "AZURE_CLIENT_SECRET": "IQ0..."
}

# Build the environment configuration using the recommended azpaddypy pattern.
environment_configuration = (
    ConfigurationSetupBuilder()
    .with_local_env_management()  # FIRST: Load .env files and environment variables.
    .with_environment_detection()  # Detect Docker vs. local environment.
    .with_environment_variables(
        LOCAL_DEVELOPMENT_STORAGE_CONFIG,
        in_docker=True,  # Only apply when running inside a Docker container.
        in_machine=True  # Only apply when running on the host machine.
    )
    .with_service_configuration()    # Parse service settings (name, version, etc.).
    .with_logging_configuration()    # Set up Application Insights and console logging.
    .with_identity_configuration()   # Configure Azure Identity with token caching.
    .build()
)


# =============================================================================
# Key Vault URIs from Environment
# =============================================================================

# The primary Key Vault for application secrets.
primary_key_vault_uri: Optional[str] = os.getenv('key_vault_uri')

# The head/admin Key Vault for elevated permissions and admin secrets.
head_key_vault_uri: Optional[str] = os.getenv('head_key_vault_uri')

# Validate that the required environment variables are set.
if not primary_key_vault_uri:
    raise ValueError(
        "key_vault_uri environment variable is required. "
        "Set it to your primary Key Vault URL (e.g., https://my-vault.vault.azure.net/)"
    )

if not head_key_vault_uri:
    raise ValueError(
        "head_key_vault_uri environment variable is required. "
        "Set it to your head/admin Key Vault URL (e.g., https://my-head-vault.vault.azure.net/)"
    )


# =============================================================================
# Azure Management Services Configuration
# =============================================================================

# Build the management configuration with a logger, identity, and Key Vaults.
azure_management_configuration: AzureManagementConfiguration = (
    AzureManagementBuilder(environment_configuration)
    .with_logger()  # Application Insights + console logging.
    .with_identity()  # Azure Identity with token caching.
    .with_keyvault(vault_url=primary_key_vault_uri, name="main")  # Primary Key Vault.
    .with_keyvault(vault_url=head_key_vault_uri, name="head")        # Admin Key Vault.
    .build()
)

# =============================================================================
# Exported Core Services for Application Use
# =============================================================================

# Application logger with Application Insights integration.
# Use this for all application logging: logger.info(), logger.error(), etc.
logger = azure_management_configuration.logger

# Azure Identity for authenticating to Azure services.
# Automatically handles Managed Identity in production and Azure CLI in development.
identity = azure_management_configuration.identity

# Key Vault clients for accessing secrets.
# A dictionary of clients, e.g., keyvaults.get("main") or keyvaults.get("head").
keyvaults = azure_management_configuration.keyvaults

# =============================================================================
# Azure Resource Services Configuration
# =============================================================================
# Construct resource names and URLs from secrets stored in the main Key Vault.
project_code = keyvaults.get("main").get_secret("project-code")
azure_environment = keyvaults.get("main").get_secret("resource-group-environment")
storage_account_name = f"stqueue{project_code}{azure_environment}"
storage_account_url = f"https://{storage_account_name}.blob.core.windows.net/"

# Cosmos DB endpoint for the prompt management database.
cosmos_db_endpoint = f"https://coscas-promptmgmt-{project_code}-{azure_environment}.documents.azure.com:443/"


# Build the resource configuration with storage and Cosmos DB clients.
azure_resource_configuration: AzureResourceConfiguration = (
    AzureResourceBuilder(
        management_config=azure_management_configuration,
        env_config=environment_configuration
    )
    .with_storage(name="main", account_url=storage_account_url)  # Azure Storage (blob, file, queue).
    .with_cosmosdb(name="promptmgmt", endpoint=cosmos_db_endpoint)  # Azure Cosmos DB for prompt management.
    .build()
)

# =============================================================================
# Exported Services for Application Use
# =============================================================================

# Storage account clients for accessing Azure Storage (blob, file, queue).
# A dictionary of clients, e.g., storage_accounts.get("main").
storage_accounts = azure_resource_configuration.storage_accounts

# Cosmos DB clients for database operations.
# A dictionary of clients, e.g., cosmos_dbs.get("promptmgmt").
cosmos_dbs = azure_resource_configuration.cosmosdb_clients

# =============================================================================
# Exported Tools for Application Use
# =============================================================================

from azpaddypy.tools.configuration_manager import create_configuration_manager

# A centralized client for managing configurations from environment variables and JSON files.
# Access with: configuration_manager.get_config(), print(configuration_manager), etc.
configuration_manager = create_configuration_manager(
    environment_configuration=environment_configuration,
    configs_dir="./configs",
    auto_reload=False,
    include_env_vars=True,
    env_var_prefix=None, # Include all environment variables
    keyvault_clients=keyvaults,
    logger=logger
)

# A centralized client for managing prompts stored in Cosmos DB.
# Access with: prompt_manager.get_prompt(), prompt_manager.save_prompt(), etc.
from azpaddypy.tools.cosmos_prompt_manager import create_cosmos_prompt_manager

prompt_manager = create_cosmos_prompt_manager(
    cosmos_client=cosmos_dbs.get("promptmgmt"),
    database_name="prompts",
    container_name=project_code,
    service_name="azure_cosmos_prompt_manager",
    service_version="1.0.0",
    logger=logger
)

# =============================================================================
# Configuration Validation
# =============================================================================

# Validate that all required services are properly initialized.
try:
    azure_management_configuration.validate()
    azure_resource_configuration.validate()
    logger.info("Azure management configuration initialized successfully")
    logger.info(f"Connected to key vaults: {list(azure_management_configuration.keyvaults.keys())}")
except Exception as config_error:
    # Log configuration errors for debugging purposes.
    if 'logger' in locals():
        logger.error(f"Configuration validation failed: {config_error}")
    else:
        print(f"CRITICAL: Configuration validation failed: {config_error}")
    raise


# Export all services for convenient importing across the application.
__all__ = [
    "logger",
    "identity",
    "keyvaults",
    "storage_accounts",
    "cosmos_dbs",
    "prompt_manager",
    "configuration_manager",
]
