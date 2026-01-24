from typing import Optional

from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['AptHostedRepository', 'AptProxyRepository', 'AptGroupRepository']


class _AptRepository(Repository):
    RECIPE_NAME = 'apt'

    def __init__(self, *args, **kwargs):
        self.distribution: str = kwargs.get('distribution', 'bionic')

        super().__init__(*args, **kwargs)

    @property
    def configuration(self):
        repo_config = super().configuration

        repo_config['attributes'].update({
            'apt': {
                'distribution': self.distribution,
            }
        })

        return repo_config


class AptHostedRepository(_AptRepository, HostedRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpg_keypair: Optional[str] = kwargs.get('gpg_keypair')
        self.passphrase: Optional[str] = kwargs.get('passphrase')

    @property
    def configuration(self):
        repo_config = super().configuration
        repo_config['attributes'].update({
            'aptSigning': {
                'keypair': self.gpg_keypair,
                'passphrase': self.passphrase
            }
        })

        return repo_config


class AptProxyRepository(_AptRepository, ProxyRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flat: bool = kwargs.get('flat', False)

    @property
    def configuration(self):
        repo_config = super().configuration

        repo_config['attributes']['apt']['flat'] = self.flat

        return repo_config


class AptGroupRepository:
    def __init__(self):
        raise NotImplementedError
