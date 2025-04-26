import datetime
import logging

import botocore.exceptions
import dask.config
from dask.utils import parse_timedelta

from coiled.utils import COILED_LOGGER_NAME, supress_logs

from ..core import AWSSessionCredentials

logger = logging.getLogger(COILED_LOGGER_NAME)


def get_aws_local_session_token(duration_seconds=None, log: bool = True):
    token_creds = AWSSessionCredentials(
        AccessKeyId="",
        SecretAccessKey="",
        SessionToken=None,
        Expiration=None,
        DefaultRegion=None,
    )

    try:
        from boto3.session import Session

        aws_loggers = [
            "botocore.client",
            "botocore.configprovider",
            "botocore.credentials",
            "botocore.endpoint",
            "botocore.hooks",
            "botocore.loaders",
            "botocore.regions",
            "botocore.utils",
            "urllib3.connectionpool",
        ]
        with supress_logs(aws_loggers):
            session = Session()
            sts = session.client("sts")
            try:
                kwargs = {"DurationSeconds": duration_seconds} if duration_seconds else {}
                credentials = sts.get_session_token(**kwargs)

                credentials = credentials["Credentials"]
                token_creds = AWSSessionCredentials(
                    AccessKeyId=credentials.get("AccessKeyId", ""),
                    SecretAccessKey=credentials.get("SecretAccessKey", ""),
                    SessionToken=credentials.get("SessionToken"),
                    Expiration=credentials.get("Expiration"),
                    DefaultRegion=session.region_name,
                )
            except botocore.exceptions.ClientError as e:
                if "session credentials" in str(e):
                    # Credentials are already an STS token, which gives us this error:
                    # > Cannot call GetSessionToken with session credentials
                    # In this case we'll just use the existing STS token for the active, local session.
                    # Note that in some cases this will have a shorter TTL than the default 12 hour tokens.
                    credentials = session.get_credentials()
                    frozen_creds = credentials.get_frozen_credentials()

                    expiration = credentials._expiry_time if hasattr(credentials, "_expiry_time") else None

                    if log:
                        logger.debug(
                            "Local AWS session is already using STS token, this will be used since we can't "
                            f"generate a new STS token from this. Expiration: {expiration}."
                        )

                    if not expiration:
                        duration = datetime.timedelta(
                            seconds=parse_timedelta(
                                dask.config.get("coiled.aws-sts-expiration-duration-if-unknown", "6m")
                            )
                        )
                        expiration = datetime.datetime.now(tz=datetime.timezone.utc) + duration
                        if log:
                            logger.debug(
                                "Unable to get expiration for existing AWS session, we'll say token expires in "
                                f"{duration.total_seconds()}s and ship refreshed token before that expiration."
                            )

                    token_creds = AWSSessionCredentials(
                        AccessKeyId=frozen_creds.access_key,
                        SecretAccessKey=frozen_creds.secret_key,
                        SessionToken=frozen_creds.token,
                        Expiration=expiration,
                        DefaultRegion=session.region_name,
                    )

    except (
        botocore.exceptions.ProfileNotFound,
        botocore.exceptions.NoCredentialsError,
    ):
        # no AWS credentials (maybe not running against AWS?), fail gracefully
        if not token_creds["AccessKeyId"]:
            if log:
                logger.debug("No local AWS credentials found, so not shipping STS token to cluster")
    except Exception as e:
        # for some aiobotocore versions (e.g. 2.3.4) we get one of these errors
        # rather than NoCredentialsError
        if "Could not connect to the endpoint URL" in str(e):
            pass
        elif "Connect timeout on endpoint URL" in str(e):
            pass
        else:
            if log:
                # warn, but don't crash
                logger.warning(f"Error getting STS token from client AWS session: {e}")

    return token_creds
