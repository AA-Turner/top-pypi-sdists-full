from typing import Dict

import boto3


async def gather(hub, profiles):
    """
    Load profiles from AWS credential files

    If no aws profiles were found in the acct_file, profiles will be extrapolated from awscli credentials.

    Example:
    .. code-block:: yaml

        aws:
          profile_name:
            region_name: us-west-1
            endpoint_url: localhost:992
            aws_access_key_id: my_key_id
            aws_secret_access_key: my_key
            aws_session_token: my_token
    """
    sub_profiles = {}

    # Use the profiles from an acct_file
    if profiles:
        for profile, ctx in profiles.get("aws", {}).items():
            sub_profiles[profile] = ctx
    # If there were no aws profiles in the acct_file, fallback to credentials from awscli
    else:
        default_idem_profile = hub.OPT.idem.get("acct_profile", hub.acct.DEFAULT)
        # Create a new session with the credentials boto3 uses by default (awscli)
        session = boto3.Session()

        # Add profiles based on the profile names available in awscli/creds
        for profile in session.available_profiles:
            new_profile = _profile_from_session(boto3.Session(profile_name=profile))
            if new_profile:
                sub_profiles[profile] = new_profile

        # Create a default profile
        if default_idem_profile not in sub_profiles:
            # Get the credentials for the default profile
            new_profile = _profile_from_session(session)
            if new_profile:
                sub_profiles[default_idem_profile] = new_profile

    return sub_profiles


def _profile_from_session(session: boto3.Session) -> Dict[str, str]:
    """
    Get credentials from a boto3 session and return an acct profile
    """
    result = {}
    credentials = session.get_credentials()
    if credentials:
        # Put the credentials into a plain dictionary
        if credentials.access_key:
            result["aws_access_key_id"] = credentials.access_key
        if credentials.secret_key:
            result["aws_secret_access_key"] = credentials.secret_key
        if credentials.token:
            result["aws_session_token"] = credentials.token
    return result
