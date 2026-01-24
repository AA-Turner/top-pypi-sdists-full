from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Stream,
)

from .core import (
    GroupId,
    OrganizationId,
)


@dataclass(frozen=True)
class OrgsClient:
    all_orgs: Stream[OrganizationId]


@dataclass(frozen=True)
class GroupsClient:
    get_groups: Callable[[OrganizationId], Stream[GroupId]]
