# Copyright 2023 StreamSets Inc.


def test_ec2_deployment(test_aws_environment, sch):
    deployment_builder = sch.get_deployment_builder(deployment_type='EC2')
    deployment = deployment_builder.build(
        deployment_name='Sample Test EC2 Deployment',
        environment=test_aws_environment,
        engine_type='DC',
        engine_version='4.1.0',
        deployment_tags=['ec2-deployment-tag'],
    )
    deployment.desired_instances = 1
    deployment.ec2_instance_type = 'm4.large'
    deployment.aws_tags = {}
    sch.add_deployment(deployment)

    assert deployment.is_complete()
    sch.delete_deployment(deployment)
