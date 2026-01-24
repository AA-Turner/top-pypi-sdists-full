# These tests do not ensure anything that the type system already ensures
# It is only present to increase coverage metrics
import pytest
from fa_purity import (
    Cmd,
    FrozenList,
    PureIterFactory,
    StreamFactory,
    Unsafe,
)

from fluidattacks_integrates_dal.client import (
    GroupsClient,
    OrgsClient,
)
from fluidattacks_integrates_dal.core import (
    GroupId,
    OrganizationId,
)
from fluidattacks_integrates_dal.list_groups import (
    list_all_groups,
)


def test_list_groups() -> None:
    orgs = PureIterFactory.from_list(
        (
            OrganizationId.new("aaaaaaaa-aaaa-4aaa-baaa-aaaaaaaaaaaa", "foo")
            .alt(Unsafe.raise_exception)
            .to_union(),
        ),
    )
    mock_group = GroupId.new("foo_group").alt(Unsafe.raise_exception).to_union()
    groups = PureIterFactory.from_list((mock_group,))
    mock = OrgsClient(StreamFactory.from_commands(orgs.map(lambda o: Cmd.wrap_value(o))))
    mock_2 = GroupsClient(
        lambda _: StreamFactory.from_commands(groups.map(lambda i: Cmd.wrap_value(i))),
    )

    def check(items: FrozenList[GroupId]) -> None:
        assert items == (mock_group,)

    with pytest.raises(SystemExit):
        list_all_groups(mock, mock_2).map(lambda f: check(f)).compute()
