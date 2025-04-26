import agilicus
from .. import column_builder


def test_simple():
    assert column_builder.make_columns(None, [], "") == []


def test_show_single_column():
    results = [
        agilicus.User._from_openapi_data(
            email=agilicus.Email("foo@bar.com"), type="user"
        )
    ]
    columns = column_builder.make_columns(None, results, "[email]")
    assert len(columns) == 1
    assert columns[0].in_name == "email"
    assert columns[0].out_name == "email"


def test_show_multi_column():
    results = [
        agilicus.User._from_openapi_data(
            id="one", email=agilicus.Email("foo@bar.com"), type="user"
        )
    ]
    columns = column_builder.make_columns(None, results, "[id,email]")
    assert len(columns) == 2
    assert columns[0].in_name == "id"
    assert columns[0].out_name == "id"

    assert columns[1].in_name == "email"
    assert columns[1].out_name == "email"


def test_rename_col():
    results = [
        agilicus.User._from_openapi_data(
            id="one", email=agilicus.Email("foo@bar.com"), type="user"
        )
    ]
    columns = column_builder.make_columns(
        None, results, "[id(newname=blah),email(newname=huh)]"
    )
    assert len(columns) == 2
    assert columns[0].in_name == "id"
    assert columns[0].out_name == "blah"

    assert columns[1].in_name == "email"
    assert columns[1].out_name == "huh"


def test_subtable():
    spec = agilicus.UpstreamUserIdentitySpec(
        upstream_user_id="user-id", upstream_idp_id="idp-id", local_user_id="local-id"
    )
    identities = [agilicus.UpstreamUserIdentity(spec)]
    results = [
        agilicus.User._from_openapi_data(
            id="one",
            email=agilicus.Email("foo@bar.com"),
            type="user",
            upstream_user_identites=identities,
        )
    ]
    columns = column_builder.make_columns(
        None,
        results,
        "[id,email,upstream_user_identities: [upstream_user_id,local_user_id]]",
    )
    assert len(columns) == 3
    assert columns[2].in_name == "upstream_user_identities"
    assert columns[2].out_name == "upstream_user_identities"
