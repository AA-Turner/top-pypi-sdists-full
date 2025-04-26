def clear_default_grant(grants):
    new_grants = []
    for grant in grants:
        if not (grant.securable_type == "DATABASE" and grant.privileges == ["USAGE"]):
            new_grants.append(grant)
    return new_grants


def assert_basic_grant(grant, check_granted_by=True):
    if check_granted_by:
        assert grant.granted_by is not None
    assert grant.created_on is not None
    assert grant.containing_scope is None
    assert grant.privileges is not None
    assert grant.securable is not None
