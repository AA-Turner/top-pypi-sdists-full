#!/usr/bin/env python3
"""Config files with secrets and interpolation (async variant)"""

import asyncio
import os
import sys
import random
import string

from koyeb import AsyncSandbox, ConfigFile
from koyeb.api import ApiClient, Configuration
from koyeb.api.api.secrets_api import SecretsApi
from koyeb.api.models.create_secret import CreateSecret


async def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    secret_name = f"test-secret-{suffix}"
    secret_value = "secret-value-123"

    # Setup API client for secrets
    api_host = os.getenv("KOYEB_API_HOST", "https://app.koyeb.com")
    configuration = Configuration(host=api_host)
    configuration.api_key["Bearer"] = api_token
    configuration.api_key_prefix["Bearer"] = "Bearer"
    api_client = ApiClient(configuration)
    secrets_api = SecretsApi(api_client)

    sandbox = None
    secret_id = None
    try:
        # Create a secret
        secret_response = secrets_api.create_secret(
            secret=CreateSecret(name=secret_name, value=secret_value)
        )
        secret = secret_response.secret
        secret_id = secret.id
        print(f"Created secret: {secret_name}")

        # Create sandbox with config files referencing the secret and using interpolation
        sandbox = await AsyncSandbox.create(
            image="koyeb/sandbox:slim",
            name=f"config-files-{suffix}",
            wait_ready=True,
            api_token=api_token,
            env={
                "X": "2",
                # Secret reference: rendered as "{{ secret.<name> }}"
                "MY_SECRET": secret,
            },
            config_files={
                # Plain string: uses default permissions (0644)
                "/tmp/secret_config.txt": "{{ secret." + secret_name + " }}",
                "/tmp/interpolation.txt": "{{ X }}",
                # ConfigFile object: custom permissions
                "/tmp/restricted.txt": ConfigFile(
                    content="only-owner-readable", permissions="0600"
                ),
            },
        )

        # Check secret reference in config file
        result = await sandbox.exec("cat /tmp/secret_config.txt")
        assert result.stdout.strip() == secret_value, (
            f"Expected '{secret_value}', got '{result.stdout.strip()}'"
        )
        print(f"/tmp/secret_config.txt={result.stdout.strip()}")

        # Check env var interpolation in config file
        result = await sandbox.exec("cat /tmp/interpolation.txt")
        assert result.stdout.strip() == "2", (
            f"Expected '2', got '{result.stdout.strip()}'"
        )
        print(f"/tmp/interpolation.txt={result.stdout.strip()}")

        # Check custom permissions
        result = await sandbox.exec("stat -c '%a' /tmp/restricted.txt")
        assert result.stdout.strip() == "600", (
            f"Expected '600', got '{result.stdout.strip()}'"
        )
        print(f"/tmp/restricted.txt permissions={result.stdout.strip()}")

        # Check Secret env var was resolved
        result = await sandbox.exec("printenv MY_SECRET")
        assert result.stdout.strip() == secret_value, (
            f"Expected '{secret_value}', got '{result.stdout.strip()}'"
        )
        print(f"MY_SECRET={result.stdout.strip()}")

        return 0
    finally:
        if sandbox:
            await sandbox.delete()
        if secret_id:
            secrets_api.delete_secret(id=secret_id)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
