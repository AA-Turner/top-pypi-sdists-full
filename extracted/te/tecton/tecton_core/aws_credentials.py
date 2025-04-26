from typing import Optional

import boto3
import botocore.credentials
import botocore.session

from tecton_proto.common.aws_credentials__client_pb2 import AwsIamRole


def assume_role_fetcher(
    role: AwsIamRole, session_name: str, session: Optional[boto3.Session] = None
) -> botocore.credentials.AssumeRoleCredentialFetcher:
    """Creates a credential fetcher for the given role with the given session_name.

    If session is provided, it will be used to make the AssumeRole calls. Otherwise, a default session will be used.
    """
    session = session or boto3.Session()
    if role.HasField("intermediate_role"):
        session = session_for_role(role=role.intermediate_role, session_name=session_name, session=session)
    assume_role_params = {"RoleSessionName": session_name}
    if role.HasField("external_id"):
        assume_role_params.update(ExternalId=role.external_id)
    return botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator=session.client,
        source_credentials=session.get_credentials(),
        role_arn=role.role_arn,
        extra_args=assume_role_params,
    )


def session_for_fetcher(fetcher: botocore.credentials.CachedCredentialFetcher, method: str) -> boto3.Session:
    """Create a boto3 session with the given credential fetcher"""
    botocore_session = botocore.session.Session()
    if fetcher is not None:
        botocore_session._credentials = botocore.credentials.DeferredRefreshableCredentials(
            method=method,
            refresh_using=fetcher.fetch_credentials,
        )
    return boto3.Session(botocore_session=botocore_session)


def session_for_role(role: AwsIamRole, session_name: str, session: Optional[boto3.Session] = None) -> boto3.Session:
    """Create a boto3 session for the given role with the given session name."""
    return session_for_fetcher(
        assume_role_fetcher(role=role, session_name=session_name, session=session), method="assume-role"
    )
