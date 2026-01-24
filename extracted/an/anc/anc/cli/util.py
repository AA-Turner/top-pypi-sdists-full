import sys
import os
from typing import Any, Optional
from urllib.parse import urlparse
from pathlib import Path
import click
import yaml
from typing import Dict

from rich.console import Console

from anc.conf.remote import remote_storage_prefix

console = Console(highlight=False)


def click_group(*args, **kwargs):
    class ClickAliasedGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            rv = click.Group.get_command(self, ctx, cmd_name)
            if rv is not None:
                return rv

            def is_abbrev(x, y):
                # first char must match
                if x[0] != y[0]:
                    return False
                it = iter(y)
                return all(any(c == ch for c in it) for ch in x)

            matches = [x for x in self.list_commands(ctx) if is_abbrev(cmd_name, x)]

            if not matches:
                return None
            elif len(matches) == 1:
                return click.Group.get_command(self, ctx, matches[0])
            ctx.fail(f"'{cmd_name}' is ambiguous: {', '.join(sorted(matches))}")

        def resolve_command(self, ctx, args):
            # always return the full command name
            _, cmd, args = super().resolve_command(ctx, args)
            return cmd.name, cmd, args

    return click.group(*args, cls=ClickAliasedGroup, **kwargs)

def is_valid_source_path(path: str, personal: str) -> bool:
    """Check if the source path is valid."""
    if not os.path.exists(path):
        print(f"Your source {path} is invalid, path not exists")
        return False
    if not os.access(path, os.R_OK):
        print(f"Your source {path} is invalid, path not access")
        return False
    if not path.startswith(remote_storage_prefix):
        print(f"Your source {path} is invalid, path is not prefix of {remote_storage_prefix} ")
        return False
    if path.startswith("/mnt/personal") and not personal:
        print(f"We can't get your personal information as you want to use {path}, so please reach out infra team to setup.")
        return False
    return True

def convert_to_absolute_path(path: str) -> str:
    """Convert a relative path to an absolute path."""
    return os.path.abspath(path)

def get_file_or_folder_name(path: str) -> str:
    """Get the file name with extension or folder name from the given path."""
    if os.path.isdir(path):
        return os.path.basename(path)  # Return folder name
    elif os.path.isfile(path):
        return os.path.basename(path)  # Return file name with extension
    else:
        raise ValueError(f"Invalid path {path}")


class ConfigManager:
    """Configuration management class that handles priority between environment variables and local config files"""

    def __init__(self):
        # Define environment variable names
        self.ENV_USER = "MLP_USER"
        self.ENV_PROJECT = "MLP_PROJECT"
        self.ENV_CLUSTER = "MLP_CLUSTER"
        self.cluster_config_path = '/mnt/project/.anc_profile'
        self.personal_config_path = '~/.anc_personal'

    def _read_anc_cluster_profile(self):
        """Read cluster configuration file
        Returns:
            dict: Cluster configuration dictionary
        """
        # Check if .anc_profile file exists
        if not os.path.isfile(self.cluster_config_path):
            return {}

        # Read and parse the YAML file
        try:
            with open(self.cluster_config_path, 'r') as file:
                profile_data = yaml.safe_load(file)
            return profile_data if profile_data else {}
        except yaml.YAMLError as e:
            return {}
        except IOError as e:
            return {}

    def _read_anc_personal_profile(self):
        """Read personal configuration file
        Returns:
            dict: Personal configuration dictionary
        """
        # Implement actual file reading logic here
        # e.g. personal: xuguang.zhao
        # Check if .anc_profile file exists
        profile_path = os.path.expanduser(self.personal_config_path)

        if not os.path.isfile(profile_path):
            return {}

        try:
            with open(profile_path, 'r') as file:
                profile_data = yaml.safe_load(file)
            return profile_data or {}
        except yaml.YAMLError as e:
            return {}
        except IOError as e:
            return {}

    def get_environment(self):
        """Get environment configuration information
        Priority: First try to get from environment variables,
        if not found, then read from configuration files

        Returns:
            tuple: (project, cluster, personal) configuration values
        """
        # Get values from environment variables
        cluster_info = self._read_anc_cluster_profile()
        user_info = self._read_anc_personal_profile()

        personal = os.environ.get(self.ENV_USER) or user_info.get('personal', '')
        cluster = os.environ.get(self.ENV_CLUSTER) or cluster_info.get('cluster', '')
        project = os.environ.get(self.ENV_PROJECT) or cluster_info.get('project', '')

        return project, cluster, personal

def validate_path_exists(path: str) -> bool:
    """Validate if the path exists"""
    if not os.path.exists(path):
        print(f"Your path {path} is invalid, path not exists")
        return False
    return True


def get_custom_code_base_from_env() -> str:
    custom_code_base_string = ""
    # Read code base paths from environment variables
    harness_code_base = os.getenv("HARNESS_CODE_BASE", "")
    ocean_code_base = os.getenv("OCEAN_CODE_BASE", "")
    nemo_code_base = os.getenv("NEMO_CODE_BASE", "")
    megatron_code_base = os.getenv("MEGATRON_CODE_BASE", "")
    anc_omni_code_base = os.getenv("ANC_OMNI_CODE_BASE", "")
    
    path_list = [path for path in [harness_code_base, ocean_code_base, nemo_code_base, megatron_code_base, anc_omni_code_base] if path != ""]
    
    for path in path_list:
        if not validate_path_exists(path):
            print(f"Your path {path} is invalid, path not exists")
            sys.exit(1)
   
    custom_code_base_string += f"OCEAN={ocean_code_base}," if ocean_code_base else ""
    custom_code_base_string += f"NEMO={nemo_code_base}," if nemo_code_base else ""
    custom_code_base_string += f"MEGATRON={megatron_code_base}," if megatron_code_base else ""
    custom_code_base_string += f"LM_EVALUATION_HARNESS={harness_code_base}," if harness_code_base else ""
    custom_code_base_string += f"ANC_OMNI={anc_omni_code_base}," if anc_omni_code_base else ""
    if custom_code_base_string.endswith(","):
        custom_code_base_string = custom_code_base_string[:-1]
    return custom_code_base_string


def is_hf_ckpt(ckpt_path: str) -> bool:
    d = Path(ckpt_path)
    has_config = (d / "config.json").is_file()
    has_safetensors = any(d.glob("*.safetensors"))
    return has_config and has_safetensors