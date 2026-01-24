from fluidattacks_integrates_dal.core import (
    GroupId,
    OrganizationId,
)


def test_group() -> None:
    assert GroupId.new("foo")


def test_org() -> None:
    assert OrganizationId.new("aaaaaaaa-aaaa-4aaa-baaa-aaaaaaaaaaaa", "foo_org")
