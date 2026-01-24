from urllib.parse import urlparse
from typing import Optional

from nexuscli.api.repository.base_models.repository import Repository


class ProxyRepository(Repository):
    """
    A proxy Nexus repository.

    :param name: name of the repository.
    :param remote_url: The URL of the repository being proxied, including the
        protocol scheme.
    :param auto_block: Auto-block outbound connections on the repository if
        remote peer is detected as unreachable/unresponsive.
    :param content_max_age: How long (in minutes) to cache artifacts before
        rechecking the remote repository. Release repositories should use -1.
    :param metadata_max_age: How long (in minutes) to cache metadata before
        rechecking the remote repository.
    :param negative_cache_enabled: Cache responses for content not present in
        the proxied repository
    :param negative_cache_ttl: How long to cache the fact that a file was not
        found in the repository (in minutes)
    :param kwargs: see :class:`Repository`
    """

    TYPE = 'proxy'

    def __init__(self, *args, **kwargs):
        self.remote_url: Optional[str] = kwargs.get('remote_url')
        self.auto_block: bool = kwargs.get('auto_block', True)
        self.content_max_age: int = kwargs.get('content_max_age', 1440)
        self.metadata_max_age: int = kwargs.get('metadata_max_age', 1440)
        self.negative_cache_enabled: bool = kwargs.get('negative_cache_enabled', True)
        self.negative_cache_ttl: int = kwargs.get('negative_cache_ttl', 1440)
        self.remote_username: Optional[str] = kwargs.get('remote_username')
        self.remote_password: Optional[str] = kwargs.get('remote_password')
        self.remote_auth_type: Optional[str] = kwargs.get('remote_auth_type')

        super().__init__(*args, **kwargs)

    def _validate_params(self):
        super()._validate_params()
        if not isinstance(self.remote_url, str):
            raise ValueError('remote_url must be a str')

        parsed_url = urlparse(self.remote_url)
        if not (parsed_url.scheme and parsed_url.netloc):
            raise ValueError(
                f'remote_url={self.remote_url} is not a valid URL')

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes'].update({
            'httpclient': {
                'connection': {
                    'blocked': False,
                    'autoBlock': self.auto_block,
                },
            },
            'proxy': {
                'remoteUrl': self.remote_url,
                'contentMaxAge': self.content_max_age,
                'metadataMaxAge': self.metadata_max_age,
            },
            'negativeCache': {
                'enabled': self.negative_cache_enabled,
                'timeToLive': self.negative_cache_ttl,
            },
        })

        if self.remote_auth_type == 'username':
            repo_config['attributes']['httpclient'].update({
                'authentication': {
                    'type': self.remote_auth_type,
                    'username': self.remote_username,
                    'password': self.remote_password
                }
            })
        return repo_config

    def upload(self, *args, **kwargs):
        raise NotImplementedError('Proxy repositories do not allow uploading')

    def upload_directory(self, *args, **kwargs):
        raise NotImplementedError('Proxy repositories do not allow uploading')
