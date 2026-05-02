import os
from importlib import metadata
from pathlib import Path

import toml
from dotenv import load_dotenv

load_dotenv(".env")
LOG_LEVEL = os.environ.get("LOG_LEVEL", 30)


def get_package_version(package_name):
    try:
        version = metadata.version(package_name)
        return version
    except metadata.PackageNotFoundError:
        return "Pacote não encontrado"


def load_env_config():
    try:
        current_dir = Path.cwd()
        config_file_path = current_dir / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado em: {config_file_path}"
            )

        with open(config_file_path, "r") as config_file:
            config = toml.load(config_file)

        # Atribuir as variáveis de configuração do ambiente
        env_config = {
            "API_BASE_URL": config["params"]["api_base_url"],
            "VERSION": config["params"]["version"],
            "NOTIFY_ALIVE_INTERVAL": config["params"]["notify_alive_interval"],
            "API_AUTHORIZATION": config["params"]["api_auth"],
            "LOG_LEVEL": config["params"]["log_level"],
            "DRIVE_URL": config["params"]["drive_url"],
            "XML_DEFAULT_FOLDER": config["params"]["xml_default_folder"],
            "GIT_ASSETS_URL": config["params"]["git_assets_url"],
        }

        # Atribuir as credenciais do Google
        google_credentials = config["google_credentials"]

        return env_config, google_credentials

    except Exception as e:
        raise Exception(f"Erro ao carregar o arquivo de configuração do ambiente: {e}")


def load_worker_config():
    try:
        current_dir = Path.cwd()
        config_file_path = current_dir / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_file_path}")

        with open(config_file_path, "r") as config_file:
            config = toml.load(config_file)

        # Atribuir as variáveis de configuração do worker
        worker_config = {
            "NOME_ROBO": config["id"]["worker_name"],
            "UUID_ROBO": config["id"]["worker_uuid"],
        }

        return worker_config

    except Exception as e:
        print(f"Erro ao carregar o arquivo de configuração do worker: {e}")
        return None
