from fa_purity import (
    Cmd,
)

from fluidattacks_integrates_dal.client import (
    GroupsClient,
    OrgsClient,
)
from fluidattacks_integrates_dal.utils import (
    new_client,
    new_resource,
    new_session,
)

from .group import (
    new_client as _new_group_client,
)
from .organization import (
    new_client as _new_org_client,
)


def new_group_client() -> Cmd[GroupsClient]:
    return new_session().bind(new_resource).map(_new_group_client)


def new_org_client() -> Cmd[OrgsClient]:
    return new_session().bind(new_client).map(_new_org_client)
