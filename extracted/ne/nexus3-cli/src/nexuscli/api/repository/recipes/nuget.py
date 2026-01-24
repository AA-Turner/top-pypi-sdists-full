from nexuscli.api.repository.base_models import Repository
from nexuscli.api.repository.base_models import GroupRepository
from nexuscli.api.repository.base_models import HostedRepository
from nexuscli.api.repository.base_models import ProxyRepository

__all__ = ['NugetHostedRepository', 'NugetProxyRepository', 'NugetGroupRepository']


class _NugetRepository(Repository):
    RECIPE_NAME = 'nuget'


class NugetGroupRepository(_NugetRepository, GroupRepository):
    pass


class NugetHostedRepository(_NugetRepository, HostedRepository):
    pass


class NugetProxyRepository(_NugetRepository, ProxyRepository):
    pass
