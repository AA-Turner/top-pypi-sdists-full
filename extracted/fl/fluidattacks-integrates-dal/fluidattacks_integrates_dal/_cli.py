import logging
import sys

import click
from fa_purity import (
    Cmd,
)

from fluidattacks_integrates_dal._typing import (
    NoReturn,
)

from . import (
    list_groups,
)
from .clients.group import (
    new_client as new_group_client,
)
from .clients.organization import (
    new_client as new_org_client,
)
from .utils import (
    new_client,
    new_resource,
    new_session,
)

LOG = logging.getLogger(__name__)


@click.command(help="Requires AWS authentication (retrieved from the environment)")
def list_all_groups() -> NoReturn:
    clients = new_session().bind(
        lambda s: new_client(s)
        .map(new_org_client)
        .bind(lambda o: new_resource(s).map(new_group_client).map(lambda g: (o, g))),
    )
    cmd: Cmd[None] = clients.bind(
        lambda t: list_groups.list_all_groups(t[0], t[1])
        .map(lambda gs: "\n".join(g.name for g in gs))
        .bind(
            lambda s: Cmd.wrap_impure(
                lambda: sys.stdout.write(s + "\n"),  # type: ignore[misc]
            ).map(
                lambda _: None,  # type: ignore[misc]
            ),
        ),
    )
    cmd.compute()


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(list_all_groups)
