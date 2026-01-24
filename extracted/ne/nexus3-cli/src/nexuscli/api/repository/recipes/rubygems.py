from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['RubygemsHostedRepository', 'RubygemsProxyRepository', 'RubygemsGroupRepository']


class _RubygemsRepository(Repository):
    RECIPE_NAME = 'rubygems'


class RubygemsGroupRepository(_RubygemsRepository, GroupRepository):
    pass


class RubygemsHostedRepository(_RubygemsRepository, HostedRepository):
    pass


class RubygemsProxyRepository(_RubygemsRepository, ProxyRepository):
    pass
