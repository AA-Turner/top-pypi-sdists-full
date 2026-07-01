#!/usr/bin/env python3
"""Environment variables with secrets and interpolation"""

import os
import sys
import random
import string

from koyeb import Sandbox
from koyeb.api.models.create_secret import CreateSecret
from koyeb.sandbox.utils import get_api_clients


def main():
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    secret_name = f"test-secret-{suffix}"
    secret_value = "secret-value-123"

    secrets_api = get_api_clients(api_token).secrets

    sandbox = None
    secret_id = None
    try:
        # Create a secret
        secret_response = secrets_api.create_secret(
            secret=CreateSecret(name=secret_name, value=secret_value)
        )
        secret_id = secret_response.secret.id
        print(f"Created secret: {secret_name}")

        # Create sandbox with env vars referencing the secret and using interpolation
        sandbox = Sandbox.create(
            image="koyeb/sandbox:slim",
            name=f"env-vars-{suffix}",
            wait_ready=True,
            api_token=api_token,
            env={
                "SECRET_VAL": "{{ secret." + secret_name + " }}",
                "X": "2",
                "Y": "{{ X }}",
            },
        )

        # Check secret reference
        result = sandbox.exec('echo "$SECRET_VAL"')
        assert result.stdout.strip() == secret_value, (
            f"Expected '{secret_value}', got '{result.stdout.strip()}'"
        )
        print(f"SECRET_VAL={result.stdout.strip()}")

        # Check direct value
        result = sandbox.exec('echo "$X"')
        assert result.stdout.strip() == "2", (
            f"Expected '2', got '{result.stdout.strip()}'"
        )
        print(f"X={result.stdout.strip()}")

        # Check interpolation
        result = sandbox.exec('echo "$Y"')
        assert result.stdout.strip() == "2", (
            f"Expected '2', got '{result.stdout.strip()}'"
        )
        print(f"Y={result.stdout.strip()}")

        return 0
    finally:
        if sandbox:
            sandbox.delete()
        if secret_id:
            secrets_api.delete_secret(id=secret_id)


if __name__ == "__main__":
    sys.exit(main())
