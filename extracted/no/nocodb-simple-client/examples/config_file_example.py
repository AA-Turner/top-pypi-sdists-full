"""
Configuration file examples for NocoDB Simple Client.

This example demonstrates how to load configuration from YAML and TOML files
using the [config] optional dependency group.

INSTALLATION:
    pip install "nocodb-simple-client[config]"

This installs the required dependencies:
    - PyYAML: YAML file support
    - tomli: TOML file support (Python < 3.11 only; Python 3.11+ uses stdlib tomllib)
"""

import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from nocodb_simple_client.config import NocoDBConfig

# =============================================================================
# DEPENDENCY CHECK
# =============================================================================

# Check for YAML support (PyYAML)
YAML_AVAILABLE = importlib.util.find_spec("yaml") is not None

# Check for TOML support (stdlib tomllib for 3.11+ or tomli for older versions)
TOML_AVAILABLE = (
    importlib.util.find_spec("tomllib") is not None or importlib.util.find_spec("tomli") is not None
)

if not YAML_AVAILABLE and not TOML_AVAILABLE:
    print("=" * 60)
    print("ERROR: Config file dependencies not installed!")
    print("=" * 60)
    print()
    print("To use YAML/TOML configuration files, install the [config] extra:")
    print()
    print('    pip install "nocodb-simple-client[config]"')
    print()
    print("This will install: PyYAML, tomli (for Python < 3.11)")
    print()
    print("Note: Python 3.11+ includes tomllib in the standard library.")
    print("=" * 60)
    sys.exit(1)


# =============================================================================
# EXAMPLE 1: YAML Configuration
# =============================================================================
def example_yaml_config():
    """Demonstrate loading configuration from a YAML file."""
    print("\n" + "=" * 60)
    print("Example 1: YAML Configuration")
    print("=" * 60)

    if not YAML_AVAILABLE:
        print("YAML support not available. Install PyYAML:")
        print('    pip install "nocodb-simple-client[config]"')
        return

    # Create a sample YAML configuration file
    yaml_content = """
# NocoDB Configuration
# Save this as: nocodb-config.yaml

base_url: "https://your-nocodb-instance.com"
api_token: "your-api-token-here"

# Connection settings
timeout: 60.0
max_retries: 3
backoff_factor: 0.5

# Connection pooling
pool_connections: 20
pool_maxsize: 50

# Security
verify_ssl: true

# Debugging
debug: false
log_level: "INFO"

# Custom headers (optional)
extra_headers:
  X-Request-Source: "my-application"
  X-Client-Version: "1.0.0"
"""

    with TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nocodb-config.yaml"
        config_path.write_text(yaml_content)

        print(f"Created sample config: {config_path}")
        print()
        print("YAML Content:")
        print("-" * 40)
        print(yaml_content.strip())
        print("-" * 40)
        print()

        # Load configuration from YAML
        config = NocoDBConfig.from_file(config_path)

        print("Loaded configuration:")
        print(f"  Base URL: {config.base_url}")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Max Retries: {config.max_retries}")
        print(f"  Pool Size: {config.pool_connections}/{config.pool_maxsize}")
        print(f"  SSL Verify: {config.verify_ssl}")
        print(f"  Debug: {config.debug}")

    print("\nYAML configuration example completed!")


# =============================================================================
# EXAMPLE 2: TOML Configuration
# =============================================================================
def example_toml_config():
    """Demonstrate loading configuration from a TOML file."""
    print("\n" + "=" * 60)
    print("Example 2: TOML Configuration")
    print("=" * 60)

    if not TOML_AVAILABLE:
        print("TOML support not available.")
        print("For Python < 3.11, install tomli:")
        print('    pip install "nocodb-simple-client[config]"')
        print()
        print("Python 3.11+ includes tomllib in the standard library.")
        return

    # Detect which TOML library is being used
    if importlib.util.find_spec("tomllib") is not None:
        toml_source = "tomllib (stdlib, Python 3.11+)"
    else:
        toml_source = "tomli (third-party)"

    print(f"Using: {toml_source}")
    print()

    # Create a sample TOML configuration file
    toml_content = """
# NocoDB Configuration
# Save this as: nocodb-config.toml

base_url = "https://your-nocodb-instance.com"
api_token = "your-api-token-here"

# Connection settings
timeout = 60.0
max_retries = 3
backoff_factor = 0.5

# Connection pooling
pool_connections = 20
pool_maxsize = 50

# Security
verify_ssl = true

# Debugging
debug = false
log_level = "INFO"

# Custom headers (optional)
[extra_headers]
X-Request-Source = "my-application"
X-Client-Version = "1.0.0"
"""

    with TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nocodb-config.toml"
        config_path.write_text(toml_content)

        print(f"Created sample config: {config_path}")
        print()
        print("TOML Content:")
        print("-" * 40)
        print(toml_content.strip())
        print("-" * 40)
        print()

        # Load configuration from TOML
        config = NocoDBConfig.from_file(config_path)

        print("Loaded configuration:")
        print(f"  Base URL: {config.base_url}")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Max Retries: {config.max_retries}")
        print(f"  Pool Size: {config.pool_connections}/{config.pool_maxsize}")

    print("\nTOML configuration example completed!")


# =============================================================================
# EXAMPLE 3: JSON Configuration (Built-in, no extra dependencies)
# =============================================================================
def example_json_config():
    """Demonstrate loading configuration from a JSON file (no extra dependencies)."""
    print("\n" + "=" * 60)
    print("Example 3: JSON Configuration (Built-in)")
    print("=" * 60)

    # JSON is always available (stdlib)
    json_content = """{
    "base_url": "https://your-nocodb-instance.com",
    "api_token": "your-api-token-here",
    "timeout": 60.0,
    "max_retries": 3,
    "backoff_factor": 0.5,
    "pool_connections": 20,
    "pool_maxsize": 50,
    "verify_ssl": true,
    "debug": false,
    "log_level": "INFO",
    "extra_headers": {
        "X-Request-Source": "my-application"
    }
}"""

    with TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "nocodb-config.json"
        config_path.write_text(json_content)

        print("Note: JSON support requires NO extra dependencies!")
        print()
        print("JSON Content:")
        print("-" * 40)
        print(json_content)
        print("-" * 40)
        print()

        # Load configuration from JSON
        config = NocoDBConfig.from_file(config_path)

        print("Loaded configuration:")
        print(f"  Base URL: {config.base_url}")
        print(f"  Timeout: {config.timeout}s")

    print("\nJSON configuration example completed!")


# =============================================================================
# EXAMPLE 4: Environment-Specific Configurations
# =============================================================================
def example_environment_configs():
    """Demonstrate managing multiple environment configurations."""
    print("\n" + "=" * 60)
    print("Example 4: Environment-Specific Configurations")
    print("=" * 60)

    if not YAML_AVAILABLE:
        print("YAML support required for this example.")
        return

    # Development configuration
    dev_config = """
base_url: "http://localhost:8080"
api_token: "dev-token"
timeout: 10.0
max_retries: 1
verify_ssl: false
debug: true
log_level: "DEBUG"
"""

    # Staging configuration
    staging_config = """
base_url: "https://staging.nocodb.example.com"
api_token: "staging-token"
timeout: 30.0
max_retries: 3
verify_ssl: true
debug: false
log_level: "INFO"
"""

    # Production configuration
    prod_config = """
base_url: "https://nocodb.example.com"
api_token: "prod-token"
timeout: 120.0
max_retries: 5
backoff_factor: 1.0
pool_connections: 50
pool_maxsize: 100
verify_ssl: true
debug: false
log_level: "WARNING"
"""

    with TemporaryDirectory() as tmpdir:
        configs = {
            "development": dev_config,
            "staging": staging_config,
            "production": prod_config,
        }

        for env_name, content in configs.items():
            config_path = Path(tmpdir) / f"config.{env_name}.yaml"
            config_path.write_text(content)

            config = NocoDBConfig.from_file(config_path)
            print(f"\n{env_name.upper()}:")
            print(f"  URL: {config.base_url}")
            print(f"  Timeout: {config.timeout}s")
            print(f"  Debug: {config.debug}")
            print(f"  Log Level: {config.log_level}")

    print("\nEnvironment configurations example completed!")


# =============================================================================
# EXAMPLE 5: Graceful Fallback Pattern
# =============================================================================
def example_graceful_fallback():
    """Demonstrate graceful fallback when config dependencies are missing."""
    print("\n" + "=" * 60)
    print("Example 5: Graceful Fallback Pattern")
    print("=" * 60)

    print(
        """
This pattern allows your application to work with or without
the [config] extra installed:

    from pathlib import Path
    from nocodb_simple_client.config import NocoDBConfig

    def load_configuration(config_path: Path | None = None):
        '''Load config with graceful fallback.'''

        # Try file-based configuration first
        if config_path and config_path.exists():
            suffix = config_path.suffix.lower()

            if suffix == '.json':
                # JSON always works (stdlib)
                return NocoDBConfig.from_file(config_path)

            elif suffix in ['.yaml', '.yml']:
                try:
                    return NocoDBConfig.from_file(config_path)
                except ValueError as e:
                    if 'PyYAML' in str(e):
                        print("YAML not available, falling back to env")
                    else:
                        raise

            elif suffix == '.toml':
                try:
                    return NocoDBConfig.from_file(config_path)
                except ValueError as e:
                    if 'tomli' in str(e):
                        print("TOML not available, falling back to env")
                    else:
                        raise

        # Fallback to environment variables
        return NocoDBConfig.from_env()
"""
    )

    print("\nGraceful fallback pattern demonstrated!")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================
def main():
    """Run all configuration file examples."""
    print("\n" + "=" * 60)
    print("NOCODB SIMPLE CLIENT - CONFIG FILE EXAMPLES")
    print("=" * 60)
    print()
    print("These examples demonstrate the [config] optional dependency group.")
    print()
    print("Installation: pip install 'nocodb-simple-client[config]'")
    print()
    print("Dependency status:")
    print(f"  YAML support (PyYAML): {'Available' if YAML_AVAILABLE else 'Not installed'}")
    print(f"  TOML support: {'Available' if TOML_AVAILABLE else 'Not installed'}")

    # Run examples
    example_json_config()  # Always works (no extra deps)
    example_yaml_config()  # Requires PyYAML
    example_toml_config()  # Requires tomli (< 3.11) or stdlib tomllib (3.11+)
    example_environment_configs()
    example_graceful_fallback()

    print("\n" + "=" * 60)
    print("All configuration file examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
