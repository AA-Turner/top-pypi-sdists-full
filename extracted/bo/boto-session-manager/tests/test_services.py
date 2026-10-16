# -*- coding: utf-8 -*-

from boto_session_manager.services import AwsServiceEnum

import boto3


def get_enum_members() -> dict[str, str]:
    return {k: v for k, v in vars(AwsServiceEnum).items() if not k.startswith("_")}


def test_aws_service_enum():
    members = get_enum_members()
    assert AwsServiceEnum.S3 == "s3"
    assert AwsServiceEnum.ACMPCA == "acm-pca"
    # generated from the boto3 docs: one member per service, no duplicate ids
    assert len(members) > 400
    assert len(set(members.values())) == len(members)


def test_aws_service_enum_matches_botocore():
    """
    Almost every service id is a real boto3 client id. The docs can be ahead
    of the installed botocore, so only a few unknown ids are allowed.
    """
    available = set(boto3.session.Session().get_available_services())
    unknown = set(get_enum_members().values()) - available
    assert len(unknown) < 50


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.services",
        preview=False,
    )
