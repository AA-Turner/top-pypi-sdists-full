from pathlib import Path
from typing import Dict

from dotenv import dotenv_values

from tinybird.tb.client import TinyB
from tinybird.tb.modules.exceptions import CLISecretException


def load_secrets(project_folder: str, client: TinyB):
    try:
        env_vars: Dict[str, str] = {}

        # Load secrets from .env file
        env_file = ".env"
        env_path = Path(project_folder) / env_file

        if env_path.exists():
            env_values = dotenv_values(env_path)
            if env_values:
                env_vars.update({k: v for k, v in env_values.items() if v is not None})

        # Load secrets from .env.local file
        env_file = ".env.local"
        env_path = Path(project_folder) / env_file

        if env_path.exists():
            env_values = dotenv_values(env_path)
            if env_values:
                env_vars.update({k: v for k, v in env_values.items() if v is not None})

        if len(env_vars.keys()) == 0:
            return

        for name, value in env_vars.items():
            if not value:
                continue

            try:
                existing_secret = client.get_secret(name)
            except Exception:
                existing_secret = None
            try:
                if existing_secret:
                    client.update_secret(name, value)
                else:
                    client.create_secret(name, value)
            except Exception as e:
                raise Exception(f"Error setting secret '{name}': {e}")

    except Exception as e:
        raise CLISecretException(str(e))
