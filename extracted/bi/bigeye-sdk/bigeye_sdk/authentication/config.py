import os
import copy
import shlex
import configparser
from pathlib import Path
from typing import OrderedDict, List, Optional

from pydantic.v1 import BaseModel, validator

from bigeye_sdk.log import get_logger
from bigeye_sdk.functions.file_functs import create_subdir_if_not_exists
from bigeye_sdk.exceptions.exceptions import ConfigNotFoundException, ConfigParseException

HOME_DIR = str(Path.home())
DEFAULT_CONFIG_FILE = os.path.join(HOME_DIR, '.bigeye', 'config.ini')


log = get_logger(__name__)


class WorkspaceConfig(BaseModel):
    """
    Configuration specific to a single company workspace.
    """
    workspace_id: int
    """workspace_id to execute all commands [required]"""
    use_default_credential: bool = True
    """Whether or not a unique credential is required for this workspace. Default = True"""
    bigconfig_input_path: Optional[List[str]] = None
    """The path(s) to bigconfig files that are used for the given workspace. 
    e.g. 'path/bigconfig.yml','path2/bigconfig.yml'"""
    bigconfig_output_path: Optional[str] = None
    """The path used to output bigconfig PLAN reports and FIXME files.'"""
    bigconfig_strict_mode: bool = False
    """API errors cause an exception if True. (Validation errors still cause an exception) Default = False"""
    bigconfig_auto_approve: bool = False
    """Bigconfig applies should be allowed to run without explicit plan approvals. Default = False"""
    bigconfig_namespace: Optional[str] = None
    """A default namespace to use for bigconfig. Default = None"""
    dbt_manifest_file: Optional[str] = None
    """The path to the dbt manifest.json file used to ingest model owners into Bigeye."""
    auto_update_enabled: bool = False
    """Whether or not the CLI should automatically update when newer versions are detected."""
    disable_auto_update_message: bool = False
    """Optionally silence warnings for newer versions detected."""

    @validator("bigconfig_input_path", pre=True)
    def validate_input_path_is_list(cls, value):
        if value:
            return value.split(',')
        else:
            return None


class Config:
    """Advanced configuration for Bigeye clients."""

    OPTION_DEFAULTS = OrderedDict(
        [
            ('workspace_id', None),
            ('use_default_credential', True),
            ('bigconfig_input_path', None),
            ('bigconfig_output_path', None),
            ('bigconfig_strict_mode', False),
            ('bigconfig_auto_approve', False),
            ('dbt_manifest_file', None),
            ('auto_update_enabled', False),
            ('disable_auto_update_message', False)
        ]
    )

    def __init__(self, *args, **kwargs):
        self._user_provided_options = self._record_user_provided_options(args, kwargs)
        # Each section and their settings should be treated independently unless otherwise
        # specified so removing the concept of default section from parser
        # Our concept of 'DEFAULT' indicates the workspace to use by default 
        # and not default settings for all workspaces.
        self._config_parser = configparser.ConfigParser(default_section=None)

    def _record_user_provided_options(self, args, kwargs):
        option_order = list(self.OPTION_DEFAULTS)
        user_provided_options = {}

        # Iterate through the kwargs passed through to the constructor and map valid keys to the dictionary
        for key, value in kwargs.items():
            if key in self.OPTION_DEFAULTS:
                user_provided_options[key] = value
            else:
                raise TypeError(f"Got unexpected keyword argument '{key}'")

        # The number of args should not be longer than the allowed options
        if len(args) > len(option_order):
            raise TypeError(f"Takes at most {len(option_order)} arguments ({len(args)} given)")

        # Iterate through args passed to constructor and map to appropriate keys.
        for i, arg in enumerate(args):
            # If multiple kwargs was specified for the arg, then error out
            if option_order[i] in user_provided_options:
                raise TypeError(f"Got multiple values for keyword argument '{option_order[i]}'")
            user_provided_options[option_order[i]] = arg

        return user_provided_options
    
    @staticmethod
    def find_config_file(config_file: str = None) -> str:
        if config_file and os.path.isfile(config_file):
            return config_file
        elif 'BIGEYE_API_CONFIG_FILE' in os.environ:
            return os.environ['BIGEYE_API_CONFIG_FILE']
        elif os.path.exists(DEFAULT_CONFIG_FILE):
            return DEFAULT_CONFIG_FILE
        else:
            create_subdir_if_not_exists(path=DEFAULT_CONFIG_FILE, includes_file=True)
            return DEFAULT_CONFIG_FILE
        
    @classmethod
    def load_config(cls, config_file: str):
        """Parse a INI config with workspaces.

        This will parse an INI config file and map all workspaces into top level keys of a dictionary.
        """
        file = cls.find_config_file(config_file)
        parsed = cls._raw_config_parse(file)
        return cls._build_workspace_map(parsed)

    @classmethod
    def _raw_config_parse(cls, config_file: str, parse_subsections=True):
        """Returns the parsed INI config contents.

        :param config_file: The name of the INI file to parse

        :returns: A dict with keys for each workspace found in the config

        :raises: ConfigNotFound, ConfigParseError
        """
        config = {}
        path = config_file
        if path is not None:
            path = os.path.expandvars(path)
            path = os.path.expanduser(path)
            if not os.path.isfile(path):
                raise ConfigNotFoundException(f"No config files found at {path}. Please run the bigeye configure command.")
            cp = configparser.ConfigParser(default_section=None)
            try:
                cp.read([path])
            except:
                raise ConfigParseException(f"Failed to parse the config file")
            else:
                for section in cp.sections():
                    config[section] = {}
                     # Set default values for all workspaces
                    for option in cls.OPTION_DEFAULTS:
                        config[section][option] = cls.OPTION_DEFAULTS[option]
                    # Override default values for specific config user has provided
                    for option in cp.options(section): 
                        config_value = cp.get(section, option)
                        if parse_subsections and config_value.startswith('\n'):
                            try:
                                config_value = cls._parse_nested(config_value)
                            except ValueError as e:
                                raise ConfigParseException(f"Failed to parse the config file.")
                        config[section][option] = config_value
        return config

    @staticmethod
    def _parse_nested(config_value):
        # Given a value like this:
        # \n
        # foo = bar
        # bar = baz
        # We need to parse this into
        # {'foo': 'bar', 'bar': 'baz}
        parsed = {}
        for line in config_value.splitlines():
            line = line.strip()
            if not line:
                continue
            # The caller will catch ValueError
            # and raise an appropriate error
            # if this fails.
            key, value = line.split('=', 1)
            parsed[key.strip()] = value.strip()
        return parsed

    @staticmethod
    def _build_workspace_map(parsed_ini_config):
        """Convert the parsed INI config into a workspace map.

        The build_workspace_map will convert the parsed INI config into a format where all
        the workspaces are equivalent top level objects with consistent naming and each key
        in the sub dictionary is a config setting for that workspace.  For example, 
        the above config file would be converted from::

            {"DEFAULT": {"workspace_id": "foo", "other_setting": "bar"},
            "workspace data-science": {"workspace_id": "foo", "other_setting": "bar"}}

        into::

            {"DEFAULT": {"workspace_id": "foo", "other_setting": "bar"},
            "data-science": {"workspace_id": "foo", "other_setting": "bar"}}

        If there are no workspaces in the provided parsed INI contents, then
        an empty dict will be the value associated with the ``workspaces`` key.

        """
        parsed_config = copy.deepcopy(parsed_ini_config)
        workspaces = {}
        for key, values in parsed_config.items():
            if key.startswith("workspace"):
                try:
                    parts = shlex.split(key)
                except ValueError:
                    continue
                if len(parts) == 2:
                    workspaces[parts[1]] = values
            elif key.lower() == 'default':
                workspaces[key] = values
            else:
                raise ConfigParseException(f'Failed to parse section {key}. '
                                           f'Each non-default section should start with `workspace {key}`')
        return workspaces


    def upsert_workspace_config(self, config_file: str, workspace: str) -> None:
        """
        Read a users current config file and based on the workspace provided, either
        update the user provided options in an existing section or add a new section that includes
        all of the options passed into the constructor.
        """
        cp = self._config_parser
        file = self.find_config_file(config_file)
        cp.read(file)
        if workspace == 'DEFAULT':
            cp[workspace] = self._user_provided_options
        elif cp.has_section(f'workspace {workspace}'):
            # must be strings, type conversion will be handled when converted to workspace config
            for key, value in self._user_provided_options.items():
                cp.set(f'workspace {workspace}',key,str(value))
        else:
            cp.add_section(f'workspace {workspace}')
            cp[f'workspace {workspace}'] = self._user_provided_options

        # Write changes to users config file
        with open(file,'w+') as configfile:
            cp.write(configfile)


    def set_workspace_config(self, config_file: str, setting: dict, workspace: str) -> None:
        """
        Read a users current config file and sets the value of a provided key/pair accordingly.

        Args:
            config_file: file containing the configuration.  If none will look for environment 
            var BIGEYE_API_CONFIG_FILE or the default config file.
            setting : a key/pair that will be set in the config. e.g. { 'workspace_id': '123' }
            workspace: the name of the workspace to identify the config section
        """
        cp = self._config_parser
        file = self.find_config_file(config_file)
        cp.read(file)
        (k, v), = setting.items()

        # ensure that boolean settings are being set properly to boolean values
        valid_type = type(self.OPTION_DEFAULTS[k])
        if valid_type == bool:
            if str(v).lower() == 'true':
                v = True
            elif str(v).lower() == 'false':
                v = False
            else:
                raise TypeError(f"Got unexpected value '{v}' for setting '{k}'. Expected true or false")

        # record the setting in the ini file - must be strings, type conversion will be handled when converted
        # to workspace config
        if workspace == 'DEFAULT':
            cp.set(f'DEFAULT',k,str(v))
        else:
            cp.set(f'workspace {workspace}',k,str(v))
        with open(file,'w+') as configfile:
            cp.write(configfile)


    def get_workspace_config(self, config_file: str, setting: str, workspace: str) -> str:
        """
        Read a users current config file and gets the value of a provided key name accordingly.

        Args:
            config_file: file containing the configuration.  If none will look for environment 
            var BIGEYE_API_CONFIG_FILE or the default config file.
            setting : a key name that can be foung in the config. e.g. 'workspace_id'
            workspace: the name of the workspace to identify the config section
        """
        cp = self._config_parser
        file = self.find_config_file(config_file)
        cp.read(file)
        if workspace == 'DEFAULT':
            return cp.get(section=workspace,
                          option=setting,
                          fallback=self.OPTION_DEFAULTS.get(setting))
        else:
            return cp.get(section=f'workspace {workspace}',
                            option=setting,
                            fallback=self.OPTION_DEFAULTS.get(setting))  