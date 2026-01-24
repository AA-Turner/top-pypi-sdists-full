from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['BowerHostedRepository', 'BowerProxyRepository', 'BowerGroupRepository']


class _BowerRepository(Repository):
    RECIPE_NAME = 'bower'


class BowerGroupRepository(_BowerRepository, GroupRepository):
    pass


class BowerHostedRepository(_BowerRepository, HostedRepository):
    pass


class BowerProxyRepository(_BowerRepository, ProxyRepository):
    pass
