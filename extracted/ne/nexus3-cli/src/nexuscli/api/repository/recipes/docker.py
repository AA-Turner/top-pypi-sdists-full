from nexuscli import exception
from nexuscli.api import validations
from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository
from nexuscli.api.repository.base_models import GroupRepository

__all__ = ['DockerGroupRepository', 'DockerHostedRepository', 'DockerProxyRepository']


class _DockerRepository(Repository):
    RECIPE_NAME = 'docker'

    def __init__(self, *args, **kwargs):
        self.http_port: int = kwargs.get('http_port', 8084)
        self.https_port: int = kwargs.get('https_port', 8085)
        self.v1_enabled: bool = kwargs.get('v1_enabled', False)
        self.force_basic_auth: bool = kwargs.get('force_basic_auth', False)

        super().__init__(*args, **kwargs)

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        repo_config['attributes'].update({
            'docker': {
                'httpPort': self.http_port,
                'httpsPort': self.https_port,
                'v1Enabled': self.v1_enabled,
                'forceBasicAuth': self.force_basic_auth
            }
        })

        return repo_config


class DockerHostedRepository(HostedRepository, _DockerRepository):
    pass


class DockerProxyRepository(ProxyRepository, _DockerRepository):
    INDEX_TYPES = ('REGISTRY', 'HUB', 'CUSTOM')

    def __init__(self, *args, **kwargs):
        self.index_type: str = kwargs.get('index_type', 'REGISTRY')
        self.use_trust_store_for_index_access: bool = kwargs.get(
            'use_trust_store_for_index_access', False)
        self.index_url: str = kwargs.get('index_url', 'https://index.docker.io/')

        super().__init__(*args, **kwargs)

    def _validate_params(self):
        validations.ensure_known('index_type', self.index_type, self.INDEX_TYPES)
        super()._validate_params()

    @property
    def configuration(self):
        """
        As per :py:obj:`Repository.configuration` but specific to this
        repository recipe and type.

        :rtype: str
        """
        repo_config = super().configuration

        if self.index_type == 'REGISTRY':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type
                },
            })
        if self.index_type == 'HUB':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type,
                    "useTrustStoreForIndexAccess":
                        self.use_trust_store_for_index_access

                },
            })
        if self.index_type == 'CUSTOM':
            repo_config['attributes'].update({
                'dockerProxy': {
                    'indexType': self.index_type,
                    "useTrustStoreForIndexAccess":
                        self.use_trust_store_for_index_access,
                    "indexUrl": self.index_url,
                },
            })
        return repo_config


class DockerGroupRepository(GroupRepository, _DockerRepository):
    def __init__(self, *args, **kwargs):
        raise exception.FeatureNotImplemented
