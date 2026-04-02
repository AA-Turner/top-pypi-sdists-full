"""
Environment file (.env) examples for NocoDB Simple Client.

This example demonstrates how to use .env files for configuration
using the [dotenv] optional dependency group.

INSTALLATION:
    pip install "nocodb-simple-client[dotenv]"

This installs the required dependency:
    - python-dotenv: .env file support

WHY USE .env FILES?
    - Keep secrets out of source code
    - Easy environment switching (dev/staging/prod)
    - Standard practice for 12-factor apps
    - Works with Docker and cloud platforms
"""

import importlib.util
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from nocodb_simple_client.config import NocoDBConfig

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================

DOTENV_AVAILABLE = importlib.util.find_spec("dotenv") is not None

if not DOTENV_AVAILABLE:
    print("=" * 60)
    print("ERROR: python-dotenv not installed!")
    print("=" * 60)
    print()
    print("To use .env file support, install the [dotenv] extra:")
    print()
    print('    pip install "nocodb-simple-client[dotenv]"')
    print()
    print("This will install: python-dotenv")
    print("=" * 60)
    sys.exit(1)

# Import after check
from dotenv import dotenv_values, load_dotenv  # noqa: E402


# =============================================================================
# EXAMPLE 1: Basic .env File Usage
# =============================================================================
def example_basic_dotenv():
    """Demonstrate basic .env file loading."""
    print("\n" + "=" * 60)
    print("Example 1: Basic .env File Usage")
    print("=" * 60)

    # Sample .env file content
    env_content = """
# NocoDB Configuration
# Save this as: .env

NOCODB_BASE_URL=https://your-nocodb-instance.com
NOCODB_API_TOKEN=your-api-token-here
NOCODB_TIMEOUT=60.0
NOCODB_MAX_RETRIES=3
NOCODB_DEBUG=false
"""

    with TemporaryDirectory() as tmpdir:
        env_path = Path(tmpdir) / ".env"
        env_path.write_text(env_content)

        print(".env Content:")
        print("-" * 40)
        print(env_content.strip())
        print("-" * 40)
        print()

        # Load .env file into environment
        load_dotenv(env_path)

        # Now NocoDBConfig.from_env() can read these values
        config = NocoDBConfig.from_env()

        print("Loaded configuration:")
        print(f"  Base URL: {config.base_url}")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Max Retries: {config.max_retries}")
        print(f"  Debug: {config.debug}")

    print("\nBasic .env example completed!")


# =============================================================================
# EXAMPLE 2: Multiple Environment Files
# =============================================================================
def example_multiple_environments():
    """Demonstrate using different .env files for different environments."""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Environment Files")
    print("=" * 60)

    # Development environment
    dev_env = """
NOCODB_BASE_URL=http://localhost:8080
NOCODB_API_TOKEN=dev-token-12345
NOCODB_TIMEOUT=10.0
NOCODB_DEBUG=true
NOCODB_LOG_LEVEL=DEBUG
"""

    # Staging environment
    staging_env = """
NOCODB_BASE_URL=https://staging.nocodb.example.com
NOCODB_API_TOKEN=staging-token-67890
NOCODB_TIMEOUT=30.0
NOCODB_DEBUG=false
NOCODB_LOG_LEVEL=INFO
"""

    # Production environment
    prod_env = """
NOCODB_BASE_URL=https://nocodb.example.com
NOCODB_API_TOKEN=prod-token-secure
NOCODB_TIMEOUT=120.0
NOCODB_DEBUG=false
NOCODB_LOG_LEVEL=WARNING
NOCODB_VERIFY_SSL=true
"""

    with TemporaryDirectory() as tmpdir:
        envs = {
            ".env.development": dev_env,
            ".env.staging": staging_env,
            ".env.production": prod_env,
        }

        for filename, content in envs.items():
            env_path = Path(tmpdir) / filename
            env_path.write_text(content)

        print("File structure:")
        print("  .env.development  <- Local development")
        print("  .env.staging      <- Staging environment")
        print("  .env.production   <- Production environment")
        print()

        # Load based on APP_ENV environment variable
        app_env = os.getenv("APP_ENV", "development")
        env_file = Path(tmpdir) / f".env.{app_env}"

        print(f"Loading: .env.{app_env}")
        load_dotenv(env_file, override=True)

        config = NocoDBConfig.from_env()
        print(f"  Base URL: {config.base_url}")
        print(f"  Debug: {config.debug}")

    print("\nMultiple environments example completed!")


# =============================================================================
# EXAMPLE 3: .env with Secrets Management
# =============================================================================
def example_secrets_management():
    """Demonstrate secure secrets handling with .env files."""
    print("\n" + "=" * 60)
    print("Example 3: Secrets Management Best Practices")
    print("=" * 60)

    print(
        """
BEST PRACTICES FOR .env FILES:

1. NEVER commit .env files to version control:

   # .gitignore
   .env
   .env.*
   !.env.example

2. Create an .env.example template (safe to commit):

   # .env.example
   NOCODB_BASE_URL=https://your-instance.com
   NOCODB_API_TOKEN=<your-api-token>
   NOCODB_TIMEOUT=60.0

3. Use different files for different environments:

   .env                 <- Local overrides (gitignored)
   .env.development     <- Development defaults
   .env.production      <- Production settings
   .env.example         <- Template (committed)

4. Load with precedence (local overrides defaults):

   from dotenv import load_dotenv

   # Load base configuration
   load_dotenv('.env.development')

   # Override with local settings
   load_dotenv('.env', override=True)

5. Validate required variables:

   import os

   required = ['NOCODB_BASE_URL', 'NOCODB_API_TOKEN']
   missing = [var for var in required if not os.getenv(var)]

   if missing:
       raise ValueError(f"Missing required env vars: {missing}")
"""
    )

    print("Secrets management best practices shown!")


# =============================================================================
# EXAMPLE 4: Reading .env Without Modifying Environment
# =============================================================================
def example_dotenv_values():
    """Demonstrate reading .env without polluting the environment."""
    print("\n" + "=" * 60)
    print("Example 4: Read .env Without Modifying os.environ")
    print("=" * 60)

    env_content = """
NOCODB_BASE_URL=https://isolated-example.com
NOCODB_API_TOKEN=isolated-token
NOCODB_TIMEOUT=45.0
"""

    with TemporaryDirectory() as tmpdir:
        env_path = Path(tmpdir) / ".env"
        env_path.write_text(env_content)

        # Read values without modifying os.environ
        config_dict = dotenv_values(env_path)

        print("Read without modifying environment:")
        for key, value in config_dict.items():
            print(f"  {key}={value}")

        # Verify os.environ was not modified
        print()
        print("os.environ['NOCODB_BASE_URL'] =", os.getenv("NOCODB_BASE_URL", "(not set)"))

        # Create config manually from dotenv_values
        config = NocoDBConfig(
            base_url=config_dict.get("NOCODB_BASE_URL", ""),
            api_token=config_dict.get("NOCODB_API_TOKEN", ""),
            timeout=float(config_dict.get("NOCODB_TIMEOUT", "30.0")),
        )
        print()
        print(f"Created config with timeout: {config.timeout}s")

    print("\ndotenv_values example completed!")


# =============================================================================
# EXAMPLE 5: Combining .env with Config Files
# =============================================================================
def example_combined_config():
    """Demonstrate combining .env for secrets with config files for settings."""
    print("\n" + "=" * 60)
    print("Example 5: Combining .env with Config Files")
    print("=" * 60)

    print(
        """
RECOMMENDED PATTERN: Separate secrets from configuration

1. .env file (gitignored) - Contains ONLY secrets:

   NOCODB_API_TOKEN=secret-token-here
   NOCODB_PROTECTION_AUTH=protection-secret

2. config.yaml (committed) - Contains non-secret settings:

   base_url: "https://nocodb.example.com"
   timeout: 60.0
   max_retries: 3
   pool_connections: 20

3. Load both in your application:

   from dotenv import load_dotenv
   from nocodb_simple_client.config import NocoDBConfig
   import os

   # Load secrets into environment
   load_dotenv()

   # Load settings from config file
   config = NocoDBConfig.from_file(Path('config.yaml'))

   # Override with environment secrets
   config.api_token = os.getenv('NOCODB_API_TOKEN')

This approach:
   - Keeps secrets out of config files
   - Allows config files to be version controlled
   - Works seamlessly with CI/CD pipelines
   - Supports Docker secrets and cloud KMS
"""
    )

    print("Combined configuration pattern shown!")


# =============================================================================
# EXAMPLE 6: Docker and Cloud Compatibility
# =============================================================================
def example_docker_cloud():
    """Demonstrate .env usage with Docker and cloud platforms."""
    print("\n" + "=" * 60)
    print("Example 6: Docker and Cloud Compatibility")
    print("=" * 60)

    print(
        """
DOCKER USAGE:

1. docker-compose.yml:

   services:
     app:
       image: my-app
       env_file:
         - .env
       environment:
         - NOCODB_BASE_URL=https://nocodb.example.com

2. Docker run:

   docker run --env-file .env my-app

3. In your Python code:

   # No need to call load_dotenv() - Docker already loaded vars
   config = NocoDBConfig.from_env()


CLOUD PLATFORMS:

AWS ECS/Lambda:
   - Use AWS Secrets Manager or Parameter Store
   - Set environment variables in task definition

Google Cloud Run:
   - Use Secret Manager
   - Set environment variables in service config

Azure:
   - Use Azure Key Vault
   - Set in App Service configuration

Kubernetes:
   - Use ConfigMaps for settings
   - Use Secrets for tokens
   - Mount as environment variables


LOCAL DEVELOPMENT with dotenv:

   from dotenv import load_dotenv

   # Only load .env in development
   if os.getenv('ENVIRONMENT') != 'production':
       load_dotenv()

   config = NocoDBConfig.from_env()
"""
    )

    print("Docker and cloud patterns shown!")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
def main():
    """Run all dotenv examples."""
    print("\n" + "=" * 60)
    print("NOCODB SIMPLE CLIENT - DOTENV EXAMPLES")
    print("=" * 60)
    print()
    print("These examples demonstrate the [dotenv] optional dependency group.")
    print()
    print("Installation: pip install 'nocodb-simple-client[dotenv]'")
    print()
    print(f"python-dotenv available: {DOTENV_AVAILABLE}")

    # Run examples
    example_basic_dotenv()
    example_multiple_environments()
    example_secrets_management()
    example_dotenv_values()
    example_combined_config()
    example_docker_cloud()

    print("\n" + "=" * 60)
    print("All dotenv examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
