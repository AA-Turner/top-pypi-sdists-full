import dotenv
import typer


class EnvManager:
    """Class to manage environment variables."""

    def __init__(self):
        from ipfabric_snow.utils.logger import ipf_logger

        self.logger = ipf_logger

    def read_env_file(self) -> dict:
        """Reads the .env file and returns a dictionary of its contents."""
        try:
            filepath = dotenv.find_dotenv(usecwd=True)
            self.logger.info(f"env file path: {filepath}")
            if filepath:
                return dotenv.dotenv_values(dotenv_path=filepath)
            else:
                raise FileNotFoundError("No .env file found.")
        except Exception as e:
            self.logger.error(f"Error reading .env file: {e}")
            return {}

    def write_env_file(self, env_vars: dict, sensitive_vars: list = None) -> None:
        """
        Writes the updated environment variables to the .env file.
        Prompts user for each sensitive variable to confirm if it should be stored.
        """
        try:
            filepath = dotenv.find_dotenv(usecwd=True)
            self.logger.info(f"env file path: {filepath}")
            if filepath:
                current_env_vars = dotenv.dotenv_values(dotenv_path=filepath)
                updated_env_vars = {**current_env_vars, **env_vars}

                for key, value in updated_env_vars.items():
                    if sensitive_vars and key in sensitive_vars:
                        store_var = typer.confirm(
                            f"Do you want to store {key} in the .env file?"
                        )
                        if not store_var:
                            continue
                        dotenv.set_key(filepath, key, value)
            else:
                raise FileNotFoundError("No .env file found.")
        except Exception as e:
            self.logger.error(f"Error writing to .env file: {e}")
