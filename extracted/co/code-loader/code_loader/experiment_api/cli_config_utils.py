from dataclasses import dataclass
import os
from typing import Dict, Optional
import yaml

@dataclass
class AuthConfig:
    api_url: str
    api_key: str

@dataclass
class Config:
    current_env: str
    envs: Dict[str, AuthConfig]

def get_cli_conf_path()-> str:
    cli_conf_path = os.getenv("TL_CLI_CONFIG_FILE") or os.path.join(os.path.expanduser("~"), ".config/tensorleap/config.yaml")
    return cli_conf_path

def get_cli_conf_file() -> Optional[Config]:
    cli_conf_path = get_cli_conf_path()
    if not os.path.exists(cli_conf_path):
        return None
    with open(cli_conf_path) as f:
        config_yaml = yaml.safe_load(f)
        envs_dict = config_yaml.get("envs")
        if envs_dict is None:
            return None
        envs = dict()
        for k, v in envs_dict.items():
            envs[k] = AuthConfig(**v)
        return Config(envs=envs, current_env=config_yaml["current_env"])
    
def get_auth_config() -> Optional[AuthConfig]:
    cli_conf = get_cli_conf_file()
    if cli_conf is None or cli_conf.current_env not in cli_conf.envs:
        return None
    return cli_conf.envs[cli_conf.current_env]


    