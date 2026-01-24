from fa_purity import (
    Cmd,
    FrozenList,
)

from .client import (
    GroupsClient,
    OrgsClient,
)
from .core import (
    GroupId,
)


def list_all_groups(orgs_cli: OrgsClient, grp_cli: GroupsClient) -> Cmd[FrozenList[GroupId]]:
    return orgs_cli.all_orgs.bind(grp_cli.get_groups).to_list()
