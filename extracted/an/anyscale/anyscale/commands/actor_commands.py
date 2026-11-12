"""`anyscale actor aggregate`.

The actor twin of `anyscale task aggregate`: the same source (the observability API on the
cloud's system cluster), the same flags and the same rendering; see `task_commands`. The
API returns every actor group at once, so --max-items cuts the list on the client.

The group is `hidden=True` for now: it runs when typed, but is left out of `anyscale
--help`, the committed doc spec and the reference docs. Removing the flag (and the
matching one on the Actors module in `_private/docgen/__main__.py`) publishes it.
"""

from typing import List, Optional, Tuple

import click

import anyscale
from anyscale.actor.models import (
    ActorAggregateBy,
    ActorAggregateMetrics,
    ActorExitDetailAggregate,
    ActorJobAggregate,
    ActorNameAggregate,
)
from anyscale.commands.doc_metadata import CommandExample
from anyscale.commands.gpu_commands import (
    beta_metadata,
    option_output,
    option_resource,
    resource_ids,
)
from anyscale.commands.task_commands import (
    group_columns,
    option_by,
    option_max_items,
    option_ray_session,
    option_start_cluster,
    print_groups,
)
from anyscale.commands.util import AnyscaleCommand


@click.group("actor", help="Inspect the Ray actors of a cluster.", hidden=True)
def actor_cli() -> None:
    pass


_ACTOR_GROUP_TYPES = {
    ActorAggregateBy.NAME: ActorNameAggregate,
    ActorAggregateBy.JOB: ActorJobAggregate,
    ActorAggregateBy.EXIT_DETAIL: ActorExitDetailAggregate,
}
ACTOR_COLUMNS: Tuple[Tuple[ActorAggregateBy, List[str]], ...] = tuple(
    (by, group_columns(group_type, ActorAggregateMetrics))
    for by, group_type in _ACTOR_GROUP_TYPES.items()
)


@beta_metadata(
    CommandExample(
        description="Why the actors of a job died, grouped by reason, with counts.",
        command="anyscale actor aggregate --by exit-detail --job-id <job-id>",
    ),
    CommandExample(
        description="Every actor name and class of a service's cluster, one row each.",
        command="anyscale actor aggregate --by name --service-id <service-id> -o table",
    ),
    CommandExample(
        description="Actors per Ray job of a cluster, without waking a stopped system cluster.",
        command="anyscale actor aggregate --by job --cluster-id <cluster-id> --no-start-cluster",
    ),
)
@actor_cli.command(
    name="aggregate", cls=AnyscaleCommand, short_help="Group the actors of a cluster."
)
@option_by(
    ["name", "job", "exit-detail"],
    "Group the actors by name and class, by Ray job, or by the reason they died.",
)
@option_resource
@option_ray_session
@option_max_items
@option_start_cluster
@option_output
def aggregate(  # noqa: PLR0913
    by: str,
    cluster_id: Optional[str],
    workspace_id: Optional[str],
    job_id: Optional[str],
    service_id: Optional[str],
    ray_session: Optional[str],
    max_items: int,
    start_cluster: bool,
    output_format: str,
) -> None:
    """Group the Ray actors of a cluster, workspace, job or service by name, job or exit
    detail, with counts per state.

    The data is read from the cloud's system cluster, as the console's Actors tab does,
    so a cold system cluster is started first and the command waits for it. Needs a user
    token: a cluster CLI token cannot start a system cluster.
    """
    ids = resource_ids(cluster_id, workspace_id, job_id, service_id)
    page = anyscale.actor.aggregate(
        by=by.replace("-", "_"),
        **ids,
        ray_session=ray_session,
        max_items=max_items,
        start_cluster=start_cluster,
    )
    print_groups(page, output_format, dict(ACTOR_COLUMNS)[page.by])


__all__: List[str] = ["ACTOR_COLUMNS", "actor_cli", "aggregate"]
