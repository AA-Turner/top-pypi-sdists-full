# Copyright 2022 StreamSets Inc.

# fmt: off
import pytest

# fmt: on


def test_update_user(sch, test_user, test_group):
    """Test updating a user's group membership and roles."""
    roles_to_update = ['Engine Administrator', 'Job Operator', 'Pipeline Editor', 'Deployment Manager']
    test_user.roles = roles_to_update
    all_group = sch.groups.get(display_name='all')
    test_user.groups = [all_group, test_group]
    sch.update_user(test_user)

    updated_user = sch.users.get(email_address=test_user.email_address)
    for role in roles_to_update:
        assert role in updated_user.roles
    assert len(updated_user.roles) == len(roles_to_update)
    assert updated_user.groups.get(group_id=test_group.group_id)
    assert updated_user.groups.get(group_id=all_group.group_id)


def test_activate_and_deactivate_user(sch, test_user):
    """Test activation and deactivation of a user."""
    try:
        # Grabbing user again to make sure we have the latest activation status, rather than making two API calls below
        user = sch.users.get(email_address=test_user.email_address)
        if user.active:
            sch.deactivate_user(user)
            assert not sch.users.get(email_address=user.email_address).active
            sch.activate_user(user)
            assert sch.users.get(email_address=user.email_address).active
        else:
            sch.activate_user(user)
            assert sch.users.get(email_address=user.email_address).active
            sch.deactivate_user(user)
            assert not sch.users.get(email_address=user.email_address).active
    finally:
        # Put the user back into an 'ACTIVE' state as expected at the start of tests
        if not sch.users.get(email_address=test_user.email_address).active:
            sch.activate_user(test_user)


def test_user_org_admin_role(sch, test_user):
    """Test assigning and removing the Org Admin role for a user."""
    sch.assign_administrator_role(test_user)
    updated_test_user = sch.users.get(email_address=test_user.email_address)
    assert 'Organization Administrator' in updated_test_user.roles
    assert 'org-admin' in updated_test_user._data['roles']

    sch.remove_administrator_role(test_user)
    updated_test_user = sch.users.get(email_address=test_user.email_address)
    assert 'Organization Administrator' not in updated_test_user.roles
    assert 'org-user' in updated_test_user._data['roles']


def test_update_group(sch, test_user, test_group):
    """Test updating a group's assigned roles and membership."""
    try:
        role_to_add = 'Topology User'
        assert test_user not in test_group.users
        assert role_to_add not in test_group.roles
        test_group.users.append(test_user)
        test_group.roles.append(role_to_add)
        sch.update_group(test_group)
        # update_group updates the in-memory representation directly
        assert test_group.users.get(email_address=test_user.email_address)
        assert role_to_add in test_group.roles
    finally:
        # Put the group back to its original state
        # Retrieve the test user again since its definition was updated via role/group addition
        test_group.users.remove(test_user)
        test_group.roles.remove(role_to_add)
        sch.update_group(test_group)
        # We expect this to throw a ValueError since the user was removed from the group
        with pytest.raises(ValueError) as value_error:
            test_group.users.get(email_address=test_user.email_address)
        assert value_error
        assert role_to_add not in test_group.roles
