import os
import time
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from gigaml_secrets.secrets_manager import SecretsManager


class CachedSecretsManager:
    def __init__(self, env, ttl=300, fallback_region=None):
        """
        Initialize CachedSecretsManager with caching and optional fallback region.

        Args:
            env: Environment prefix for secrets (e.g., 'dev', 'prod')
            ttl: Cache time-to-live in seconds (default: 300)
            fallback_region: Optional fallback region for high availability.
        """
        self.env = env
        self.secrets_manager = SecretsManager(fallback_region=fallback_region)
        self.ttl = ttl
        # Store cache in memory as a dictionary
        self.cache = {}

    def get_secret(self, secret_name):
        prefixed_secret_name = f"{self.env}/{secret_name}"
        current_time = time.time()

        if prefixed_secret_name in self.cache:
            secret, timestamp = self.cache[prefixed_secret_name]
            if current_time - timestamp < self.ttl:
                os.environ[secret_name] = secret  # Ensure the environment variable is set
                return secret

        secret = self.secrets_manager.get_secret(prefixed_secret_name)
        self.cache[prefixed_secret_name] = (secret, current_time)
        os.environ[secret_name] = secret  # Store without the prefix in environment variables
        return secret

    def update_cache_timestamp(self, secret_name):
        prefixed_secret_name = f"{self.env}/{secret_name}"
        current_time = time.time()
        if prefixed_secret_name in self.cache:
            secret, _ = self.cache[prefixed_secret_name]
            self.cache[prefixed_secret_name] = (secret, current_time)

    def upload_secret(self, secret_name, secret_value):
        prefixed_secret_name = f"{self.env}/{secret_name}"
        self.secrets_manager.upload_secret(prefixed_secret_name, secret_value)
        self.update_cache_timestamp(secret_name)


def load_secrets(env, secret_names, fallback_region=None):
    """
    Load secrets from AWS Secrets Manager and set them as environment variables.

    Args:
        env: Environment prefix for secrets (e.g., 'dev', 'prod')
        secret_names: List of secret names to load
        fallback_region: Optional fallback region for high availability.
    """
    cached_secrets_manager = CachedSecretsManager(
        env,
        fallback_region=fallback_region
    )

    for secret_name in secret_names:
        try:
            secret = cached_secrets_manager.get_secret(secret_name)
            os.environ[secret_name] = secret
            cached_secrets_manager.update_cache_timestamp(secret_name)
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {e}")
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
