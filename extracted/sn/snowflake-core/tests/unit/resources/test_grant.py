from snowflake.core.grant import Grant, Grantee, Privileges, Securable


def test_to_dict():
    grant = Grant(
        grantee=Grantee(name="test_role", grantee_type="foo"),
        securable=Securable(name="test_securable", securable_type="bar"),
        privileges=[Privileges.add_search_optimization, Privileges.read],
        grant_option=False,
    )
    assert grant.to_dict() == {
        'grant_option': False,
        'privileges': ['ADD SEARCH OPTIMIZATION', 'READ'],
        'securable_type': 'bar'
    }
