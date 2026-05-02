"""
Summary.

    EC2 SpotPrice Lib, GPL v3 License

    Copyright (c) 2018-2020 Blake Huber

    Python 3 Module Function:  session_selector
        - handles environment-resident credentials utilised
          in deployments such as AWS Lambda.
        - if nothing in the environment, utilises credentials
          tied to a profile_name in the local awscli configuration.

"""
import os
import sys
import inspect
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound
from libtools.oscodes_unix import exit_codes
from spotlib import logger


def authenticated(botosession):
    """
        Tests generic authentication status to AWS Account
        Customised specifically for testing of memory-resident
        credentials stored as environment variables.

    Args:
        :profile (str): iam user name from local awscli configuration

    Returns:
        TYPE: bool, True (Authenticated)| False (Unauthenticated)

    """
    fx = inspect.stack()[0][3]

    try:

        sts_client = botosession.client('sts')
        httpstatus = str(sts_client.get_caller_identity()['ResponseMetadata']['HTTPStatusCode'])

        if httpstatus.startswith('20'):
            # http status code 2XX; successful
            return True

    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            logger.warning(
                '%s: Invalid credentials to authenticate for profile user (%s). Exit. [Code: %d]'
                % (fx, profile, exit_codes['EX_NOPERM']['Code'])
            )
        elif e.response['Error']['Code'] == 'ExpiredToken':
            logger.info(
                '%s: Expired temporary credentials detected for profile user (%s) [Code: %d]'
                % (fx, profile, exit_codes['EX_CONFIG']['Code'])
            )
        else:
            logger.exception(
                f'{fx}: Unknown authentication problem. Error: {e}'
            )
    except NoCredentialsError:
        logger.exception(f'{fx}: Unable to authenicate to AWS: No credentials found')
    except ProfileNotFound:
        logger.exception(f'{fx}: Error during authentication. Unable to locate awscli profile_name')
    except Exception as e:
        logger.exception('{}: Unknown error: {}'.format(fx, e))
    return False


def session_selector(profile):
    """
        Creates a boto3 session object after examining
        available credential set(s).  session selector
        follows the following authenication hierarchy:

            1. Attempts to find memory-resident credentials
               supplied as environment variables (example:
                AWS Lambda service environment)

            2. If (1) fails to find valid credentials, spotlib
               local attempts to utilise awscli credentials
               from local disk.

    Args:
        :profile (str):  Optional awscli profile_name
            corresponding to a set of credentials stored
            in the local awscli configuration

    Returns:
        instantiated session, TYPE:  boto3 object

    """
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    token = os.environ.get('AWS_SESSION_TOKEN')

    fx = inspect.stack()[0][3]

    try:

        if profile is not None:
            session_profile = boto3.Session(profile_name=profile)
            if authenticated(session_profile):
                return session_profile

        elif access_key and secret_key and token:
            session_env1 = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=token
                )
            if authenticated(session_env1):
                return session_env1

        elif access_key and secret_key:
            session_env2 = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key
                )
            if authenticated(session_env2):
                return session_env2

        session = boto3.Session()
        if authenticated(session):
            return session

    except ClientError as e:
        logger.exception(f'{fx}: Boto client error during authentication to AWS: {e}')
    except NoCredentialsError:
        logger.exception(f'{fx}: Unable to authenicate to AWS: No credentials found')
    except ProfileNotFound:
        logger.exception(f'{fx}: Error during authentication. Unable to locate awscli profile_name')
    sys.exit(exit_codes['EX_DEPENDENCY']['Code'])
