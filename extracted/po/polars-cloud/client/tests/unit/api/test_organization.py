# mypy: disable-error-code="attr-defined,return-value,no-untyped-def"
import pytest
from polars_cloud import Organization
from polars_cloud.exceptions import OrganizationResolveError


@pytest.mark.usefixtures("_mock_organization_by_name")
def test_get_organization_by_name(organization_name, organization_id) -> None:
    org = Organization(name=organization_name)
    assert org.name == organization_name
    assert org.id == organization_id


@pytest.mark.usefixtures("_mock_organization_by_name")
def test_err_get_workspace_by_name() -> None:
    name = "DOES NOT EXIST"
    with pytest.raises(
        OrganizationResolveError, match=f"Organization {name!r} does not exist"
    ):
        Organization(name=name)


@pytest.mark.usefixtures("_mock_organization_by_id")
def test_get_organization_by_id(organization_id, organization_name) -> None:
    w = Organization(id=organization_id)
    assert w.id == organization_id
    assert w.name == organization_name
