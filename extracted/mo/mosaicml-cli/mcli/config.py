"""Global Singleton Config Store"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import ruamel.yaml
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from mcli.utils.utils_yaml import StringDumpYAML

logging.getLogger('urllib3.connectionpool').disabled = True
logger = logging.getLogger(__name__)


def env_path_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = Path(os.environ[config_value])


def env_str_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = os.environ[config_value]


MCLI_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic'))
env_path_override_config('MCLI_CONFIG_DIR')

MOSAICML_API_ENDPOINT: str = 'https://api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_STAGING: str = 'https://staging.api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_DEV: str = 'https://dev.api.mosaicml.com/graphql'
MOSAICML_API_ENDPOINT_LOCAL: str = 'http://localhost:3001/graphql'
MOSAICML_API_ENDPOINT_ENV: str = 'MOSAICML_API_ENDPOINT'
DATABRICKS_API_ENDPOINT_AWS_STAGING: str = 'https://oregon.staging.cloud.databricks.com/api/2.0/genai-mapi/graphql'
DATABRICKS_API_ENDPOINT_AZURE_STAGING: str = 'https://westus.staging.azuredatabricks.net/api/2.0/genai-mapi/graphql'
env_str_override_config(MOSAICML_API_ENDPOINT_ENV)

MOSAICML_MINT_ENDPOINT: str = 'wss://mint.mosaicml.com/v1/shell'
MOSAICML_MINT_ENDPOINT_STAGING: str = 'wss://staging.mint.mosaicml.com/v1/shell'
MOSAICML_MINT_ENDPOINT_DEV: str = 'wss://dev.mint.mosaicml.com/v1/shell'
MOSAICML_MINT_ENDPOINT_LOCAL: str = 'ws://localhost:3004/v1/shell'
MOSAICML_MINT_ENDPOINT_ENV: str = 'MOSAICML_MINT_ENDPOINT'
env_str_override_config(MOSAICML_MINT_ENDPOINT_ENV)

MCLI_CONFIG_PATH: Path = MCLI_CONFIG_DIR / 'mcli_config'
env_path_override_config('MCLI_CONFIG_PATH')

UPDATE_CHECK_FREQUENCY_DAYS: float = 2

MCLI_MODE_ENV: str = 'MCLI_MODE'
env_str_override_config(MCLI_MODE_ENV)

MCLI_TIMEOUT_ENV = 'MCLI_TIMEOUT'
env_str_override_config(MCLI_TIMEOUT_ENV)

MCLI_DISABLE_UPGRADE_CHECK_ENV: str = 'MCLI_DISABLE_UPGRADE_CHECK'
env_str_override_config(MCLI_DISABLE_UPGRADE_CHECK_ENV)

# Used for local dev and testing
MOSAICML_API_KEY_ENV: str = 'MOSAICML_API_KEY'

MOSAICML_ACCESS_TOKEN_FILE_ENV: str = 'MOSAICML_ACCESS_TOKEN_FILE'

ADMIN_MODE = False


def get_timeout(default_timeout: Optional[float] = None) -> Optional[float]:
    timeout_env = os.environ.get(MCLI_TIMEOUT_ENV)

    if timeout_env:
        return float(timeout_env)

    return default_timeout


class FeatureFlag(Enum):
    """Enum for mcli feature flags
    """
    ALPHA_TESTER = 'ALPHA_TESTER'

    @staticmethod
    def get_external_features() -> Set[FeatureFlag]:
        return set()


class MCLIMode(Enum):
    """Enum for mcli user modes
    """
    PROD = 'PROD'
    DEV = 'DEV'
    LOCAL = 'LOCAL'
    STAGING = 'STAGING'
    DBX_AWS_STAGING = 'DBX_AWS_STAGING'
    DBX_AZURE_STAGING = 'DBX_AZURE_STAGING'

    def is_internal(self) -> bool:
        """True if this mode is an internal mode
        """
        internal_modes = {
            MCLIMode.DEV, MCLIMode.LOCAL, MCLIMode.STAGING, MCLIMode.DBX_AWS_STAGING, MCLIMode.DBX_AZURE_STAGING
        }
        return self in internal_modes

    def available_feature_flags(self) -> List[FeatureFlag]:
        if self.is_internal():
            # All features are available to internal users
            return list(FeatureFlag)

        return list(FeatureFlag.get_external_features())

    @classmethod
    def from_env(cls) -> MCLIMode:
        """If the user's mcli mode is set in the environment, return it
        """
        found_mode = os.environ.get(MCLI_MODE_ENV, None)
        if found_mode:
            found_mode = found_mode.upper()
            for mode in MCLIMode:
                if found_mode == mode.value:
                    return mode

        return MCLIMode.PROD

    @property
    def endpoint(self) -> str:
        """The MAPI endpoint value for the given environment
        """
        if self is MCLIMode.DEV:
            return MOSAICML_API_ENDPOINT_DEV
        elif self is MCLIMode.LOCAL:
            return MOSAICML_API_ENDPOINT_LOCAL
        elif self is MCLIMode.STAGING:
            return MOSAICML_API_ENDPOINT_STAGING
        elif self is MCLIMode.DBX_AWS_STAGING:
            return DATABRICKS_API_ENDPOINT_AWS_STAGING
        elif self is MCLIMode.DBX_AZURE_STAGING:
            return DATABRICKS_API_ENDPOINT_AZURE_STAGING

        return MOSAICML_API_ENDPOINT

    @property
    def mint_endpoint(self) -> str:
        """The MINT endpoint value for the given environment
        """
        if self is MCLIMode.DEV:
            return MOSAICML_MINT_ENDPOINT_DEV
        elif self is MCLIMode.LOCAL:
            return MOSAICML_MINT_ENDPOINT_LOCAL
        elif self is MCLIMode.STAGING:
            return MOSAICML_MINT_ENDPOINT_STAGING
        return MOSAICML_MINT_ENDPOINT

    def is_alternate(self) -> bool:
        """True if the mode is a valid alternate mcloud environment
        """
        alternate_env_modes = {MCLIMode.DEV, MCLIMode.LOCAL, MCLIMode.STAGING}
        return self in alternate_env_modes

    @staticmethod
    def get_dbx_modes() -> List[MCLIMode]:
        return [MCLIMode.DBX_AWS_STAGING, MCLIMode.DBX_AZURE_STAGING]


@dataclass
class MCLIConfig:
    """Global Config Store persisted on local disk"""

    MOSAICML_API_KEY: str = ''  # pylint: disable=invalid-name Global Stored within Singleton

    feature_flags: Dict[str, bool] = field(default_factory=dict)
    last_update_check: datetime = field(default_factory=datetime.now)

    # MCloud environments w/ API keys
    # Most users will be in PROD, so this will likely only be touched internally
    mcloud_envs: Dict[str, str] = field(default_factory=dict)

    _user_id: Optional[str] = None
    _organization_id: Optional[str] = None

    @property
    def user_id(self):
        # User id is only relevant in admin mode. If using normal mcli, it should always
        # set to be blank and the user just needs to authenticate through their api key
        if ADMIN_MODE:
            return self._user_id
        return None

    @user_id.setter
    def user_id(self, value: Optional[str]):
        self._user_id = value

    @property
    def organization_id(self):
        if ADMIN_MODE:
            return self._organization_id
        return None

    @organization_id.setter
    def organization_id(self, value: Optional[str]):
        self._organization_id = value

    def update_entity(
        self,
        variables: Dict[str, Any],
        *,
        set_user: bool = True,
        set_org: bool = True,
    ):
        if not ADMIN_MODE:
            return

        set_user &= (self.user_id is not None)
        set_org &= (self.organization_id is not None)

        if not set_user and not set_org:
            return

        variables['entity'] = variables.get('entity', {})

        if set_user:
            variables['entity']['userIds'] = [self.user_id]

        if set_org:
            variables['entity']['organizationIds'] = [self.organization_id]

        logger.info(f'Making mapi query with entity {variables["entity"]}')

    @classmethod
    def empty(cls) -> MCLIConfig:
        conf = MCLIConfig()
        return conf

    @property
    def internal(self) -> bool:
        return self.mcli_mode.is_internal()

    @property
    def mcli_mode(self) -> MCLIMode:
        return MCLIMode.from_env()

    @property
    def disable_upgrade(self) -> bool:
        disable_env = os.environ.get(MCLI_DISABLE_UPGRADE_CHECK_ENV, 'false').lower()
        return disable_env == 'true'

    @property
    def endpoint(self) -> str:
        """The user's MAPI endpoint
        """
        env_endpoint = os.environ.get(MOSAICML_API_ENDPOINT_ENV, None)
        return env_endpoint or self.mcli_mode.endpoint

    @property
    def mint_endpoint(self) -> str:
        """The user's MINT endpoint
        """
        env_endpoint = os.environ.get(MOSAICML_MINT_ENDPOINT_ENV, None)
        return env_endpoint or self.mcli_mode.mint_endpoint

    @property
    def api_key(self):
        """The user's configured MCloud API key
        """
        return self.get_api_key(env_override=True)

    @property
    def access_token(self):
        access_token_file = os.environ.get(MOSAICML_ACCESS_TOKEN_FILE_ENV, None)
        if access_token_file:
            with open(access_token_file, 'r', encoding='UTF-8') as f:
                access_token = f.read()
                return access_token.strip()
        return ''

    @api_key.setter
    def api_key(self, value: str):
        if self.mcli_mode.is_alternate():
            # If the user is using an alternative mcloud, set that API key
            self.mcloud_envs[self.mcli_mode.value] = value
        else:
            self.MOSAICML_API_KEY = value

    def get_api_key(self, env_override: bool = True):
        """Get the user's current API key

        Args:
            env_override (bool, optional): If True, allow an environment variable to
                override the configured value, otherwise pull only from the user's config
                file. Defaults to True.

        Returns:
            str: The user's API key, if set, otherwise an empty string
        """
        api_key_env = os.environ.get(MOSAICML_API_KEY_ENV, None)
        if api_key_env is not None and env_override:
            return api_key_env
        elif self.mcli_mode.is_alternate():
            return self.mcloud_envs.get(self.mcli_mode.value, '')
        elif self.MOSAICML_API_KEY:
            return self.MOSAICML_API_KEY
        return ''

    def to_dict(self) -> Dict[str, Any]:
        """Converts the config to a dictionary

        Returns:
            Dict[str, Any]: The dictionary representation of the config
        """
        res: Dict[str, Any] = {
            'last_update_check': self.last_update_check,
        }

        # Only add configs if they are filled
        if self.MOSAICML_API_KEY:
            res['MOSAICML_API_KEY'] = self.MOSAICML_API_KEY

        if self.feature_flags:
            res['feature_flags'] = self.feature_flags

        if self.mcloud_envs:
            res['mcloud_envs'] = self.mcloud_envs

        if self._user_id:
            res['_user_id'] = self._user_id

        if self._organization_id:
            res['_organization_id'] = self._organization_id

        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MCLIConfig:
        # Remove any unknown or false feature flags
        known_feature_flags = {f.value for f in FeatureFlag}
        feature_flags = {k: v for k, v in data.get('feature_flags', {}).items() if k in known_feature_flags and v}

        if isinstance(data.get('last_update_check'), str):
            last_update_check = datetime.fromisoformat(data['last_update_check'])
        elif isinstance(data.get('last_update_check'), datetime):
            last_update_check = data['last_update_check']
        else:
            last_update_check = datetime.now()

        return MCLIConfig(
            MOSAICML_API_KEY=data.get('MOSAICML_API_KEY', ''),
            feature_flags=feature_flags,
            last_update_check=last_update_check,
            mcloud_envs=data.get('mcloud_envs', {}),
            _user_id=data.get('_user_id', None),
            _organization_id=data.get('_organization_id', None),
        )

    @classmethod
    def load_config(cls) -> MCLIConfig:
        """Loads the MCLIConfig from local disk

        Return:
            Returns the MCLIConfig, if not found, returns a new empty config
        """
        try:
            with open(MCLI_CONFIG_PATH, 'r', encoding='utf8') as f:
                data: Dict[str, Any] = yaml.full_load(f)
            conf = cls.from_dict(data)
        except FileNotFoundError:
            conf = MCLIConfig.empty()

        return conf

    def save_config(self) -> bool:
        """Saves the MCLIConfig to local disk

        Return:
            Returns true if successful
        """
        logger.debug(f'Saving config to {MCLI_CONFIG_PATH}')
        data = self._get_formatted_dump()
        y = YAML()
        y.explicit_start = True  # type: ignore
        os.makedirs(os.path.dirname(MCLI_CONFIG_PATH), exist_ok=True)
        with open(MCLI_CONFIG_PATH, 'w', encoding='utf8') as f:
            y.dump(data, f)
        return True

    def _get_formatted_dump(self) -> CommentedMap:
        """Gets the ruamel yaml formatted dump of the config
        """
        raw_data = self.to_dict()
        y = ruamel.yaml.YAML(typ='rt', pure=True)
        # pylint: disable=unreachable
        data: CommentedMap = y.load(yaml.dump(raw_data))  # pylint: enable=unreachable
        return data

    def feature_enabled(self, feature: FeatureFlag) -> bool:
        """Checks if the feature flag is enabled

        Args:
            feature (FeatureFlag): The feature to check
        """

        if not self.internal and feature not in FeatureFlag.get_external_features():
            # Only enable select features for external use
            return False

        if feature.value in self.feature_flags:
            enabled = self.feature_flags.get(feature.value, False)
            return bool(enabled)

        return False

    def __str__(self) -> str:
        data = self._get_formatted_dump()
        y = StringDumpYAML()
        return y.dump(data)


def feature_enabled(feature: FeatureFlag) -> bool:
    conf = MCLIConfig.load_config()
    return conf.feature_enabled(feature=feature)
