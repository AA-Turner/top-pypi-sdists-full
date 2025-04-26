# Copyright 2024 StreamSets Inc.


def test_deployment_acl(sch, sdc_deployment):
    NEW_ACTION = ["READ"]
    deployment_acl = sdc_deployment.acl
    permission = deployment_acl.permissions[0]
    original_actions = permission.actions
    try:
        assert permission.actions != NEW_ACTION
        permission.actions = NEW_ACTION
        assert permission.actions == NEW_ACTION
        deployment_acl.add_permission(permission)
        assert deployment_acl._data["permissions"][0]["actions"] == NEW_ACTION
        # Double check that the deployment was actually updated
        deployment = sch.deployments.get(deployment_id=sdc_deployment.deployment_id)
        assert deployment.acl._data["permissions"][0]["actions"] == NEW_ACTION
    finally:
        permission.actions = original_actions
        deployment_acl.add_permission(permission)


def test_environment_acl(sch, test_environment):
    NEW_ACTION = ["READ"]
    environment_acl = test_environment.acl
    permission = environment_acl.permissions[0]
    original_actions = permission.actions
    try:
        assert permission.actions != NEW_ACTION
        permission.actions = NEW_ACTION
        assert permission.actions == NEW_ACTION
        environment_acl.add_permission(permission)
        assert environment_acl._data["permissions"][0]["actions"] == NEW_ACTION
        # Double check that the deployment was actually updated
        environment = sch.environments.get(environment_id=test_environment.environment_id)
        assert environment.acl._data["permissions"][0]["actions"] == NEW_ACTION
    finally:
        permission.actions = original_actions
        environment_acl.add_permission(permission)
