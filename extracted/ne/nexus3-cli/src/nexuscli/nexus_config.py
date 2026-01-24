import json
import typing
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Union


DEFAULT_CONFIG = str(Path.home().joinpath('.nexus-cli').absolute())

# when adding entries to DEFAULTS, check if to_dict() would still make sense
DEFAULTS = {
    'api_version': 'v1',
    'username': 'admin',
    'password': '',
    'url': 'http://localhost:8081',
    'x509_verify': True,
    'groovy_enabled': True,
}


class NexusConfig:
    """
    A class to hold Nexus 3's configuration.

    Unless keyword arguments ``url``, ``user`` and ``password`` are
    supplied, the class will attempt to read the configuration file and,
    if unsuccessful, use defaults.

    Args:
        username (str): username for Nexus service at given url.
        password (str): password for username above.
        url (str): URL to Nexus 3 OSS service.
        x509_verify (bool): toggle certificate validation.
        api_version (str): Nexus REST API version to be used.
        config_path (str): local file containing configuration above in JSON
            format with these keys: ``nexus_url``, ``nexus_user``,
            ``nexus_pass`` and ``nexus_verify``.
        groovy_enabled (bool): toggle use of groovy scripts.
    """
    def __init__(self,
                 username=DEFAULTS['username'],
                 password=DEFAULTS['password'],
                 url=DEFAULTS['url'],
                 x509_verify=DEFAULTS['x509_verify'],
                 api_version=DEFAULTS['api_version'],
                 config_path=None,
                 groovy_enabled=DEFAULTS['groovy_enabled']):

        self._api_version = api_version
        self._username = username
        self._password = password
        self._url = url
        if not self._url.endswith('/'):
            self._url += '/'
        self._x509_verify = x509_verify
        self._config_path = Path(config_path or DEFAULT_CONFIG)
        self._groovy_enabled = groovy_enabled

    @property
    def to_dict(self):
        """
        Current instance configuration.

        :rtype: dict
        """
        config = {}
        for key in DEFAULTS.keys():
            config[key] = getattr(self, f'_{key}')
        return config

    @property
    def auth(self):
        """
        Current username and password as a tuple.

        :rtype: tuple[str, str]
        """
        return self._username, self._password

    @property
    def api_version(self):
        """
        Current API version in use.

        :rtype: str
        """
        return self._api_version

    @property
    def url(self):
        """
        The Nexus service URL

        :rtype: str
        """
        return self._url

    @property
    def x509_verify(self):
        """
        Whether to validate the x509 certificate when using https to
        access the Nexus service

        :rtype: str
        """
        return self._x509_verify

    @property
    def groovy_enabled(self):
        """
        Whether the use of Nexus Groovy scripts is allowed

        :rtype: bool
        """
        return self._groovy_enabled

    @property
    def config_path(self) -> Path:
        """
        Path to configuration file, as given by ``config_path`` during
        instantiation.
        """
        return self._config_path

    @property
    def config_file(self):
        """
        Path to configuration file, as given by ``config_path`` during
        instantiation.

        :rtype: str
        """
        warnings.warn('use `str(obj.config_path)` instead', DeprecationWarning)
        return str(self.config_path)

    @staticmethod
    @contextmanager
    def _open_dump(dst_path) -> typing.Iterator[typing.IO]:
        dst_path.touch(mode=0o600)
        try:
            with dst_path.open(mode='w+', encoding='utf-8') as fh:
                yield fh
        finally:
            pass

    def dump_env(self):
        """
        Writes the current configuration to disk under property:`config_file`.env.

        If a file already exists, it will be overwritten. The permission will
        be set to read/write to the owner only.

        return: name of the file written
        """
        from nexuscli.cli.constants import ENV_VAR_PREFIX  # avoid circular dependency
        with self._open_dump(self.config_path.with_suffix('.env')) as fh:
            for k, v in sorted(self.to_dict.items()):
                fh.write(f'{ENV_VAR_PREFIX}_{k.upper()}={v}\n')
            return fh.name

    def dump(self) -> str:
        """
        Writes the current configuration to disk under property:`config_file`.

        If a file already exists, it will be overwritten. The permission will
        be set to read/write to the owner only.

        return: name of the file written
        """
        with self._open_dump(self.config_path) as fh:
            json.dump(self.to_dict, fh, ensure_ascii=False, indent=4, sort_keys=True)
            return fh.name

    def load(self):
        """
        Load the configuration settings from the file specified by
        :attr:`config_file`.

        The configuration file is in JSON format and expects these keys:
        ``nexus_user``, ``nexus_pass``, ``nexus_url``, ``nexus_verify``.
        """
        with self.config_path.open(mode='r', encoding='utf-8') as fh:
            config = json.load(fh)

        for key, default_value in DEFAULTS.items():
            setattr(self, f'_{key}', config.get(key, default_value))

    def merge_with_dict(self, kwargs: Dict[str, Union[bool, str]]) -> None:
        """
        Merge the configuration from ``kwargs`` into the existing one. The

        :param kwargs: configuration values to load. Keys should match arguments to the class init.
        """
        for key in DEFAULTS.keys():
            value = kwargs.get(key)
            if value is not None:
                setattr(self, f'_{key}', value)
