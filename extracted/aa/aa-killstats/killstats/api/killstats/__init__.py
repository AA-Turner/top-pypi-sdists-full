from .admin import KillboardAdminApiEndpoints
from .killboard import KillboardApiEndpoints
from .stats import KillboardStatsApiEndpoints


def setup(api):
    KillboardApiEndpoints(api)
    KillboardStatsApiEndpoints(api)
    KillboardAdminApiEndpoints(api)
