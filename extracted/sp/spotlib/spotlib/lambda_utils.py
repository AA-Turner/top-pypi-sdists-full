"""

lambda_utils (python3)

    Common functionality for use with AWS Lambda Service

Author:
    Blake Huber
    Copyright Blake Huber, All Rights Reserved.

License:
    Permission to use, copy, modify, and distribute this software and its
    documentation for any purpose and without fee is hereby granted,
    provided that the above copyright notice appear in all copies and that
    both the copyright notice and this permission notice appear in
    supporting documentation

    Additional terms may be found in the complete license agreement:
    https://bitbucket.org/blakeca00/lambda-library-python/src/master/LICENSE.md

"""

import os
import re
import json
import time
import inspect
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from spotlib.core import session_selector
from spotlib._version import __version__

logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)


def read_env_variable(arg, default=None, patterns=None):
    """
    Summary:
        Parse environment variables, validate characters, convert
        type(s). default should be used to avoid conversion of an
        variable and retain string type

    Example usage:

    >>> from lambda_utils import read_env_variable
    >>> os.environ['DBUGMODE'] = 'True'
    >>> myvar = read_env_variable('DBUGMODE')
    >>> type(myvar)
    True

    >>> from lambda_utils import read_env_variable
    >>> os.environ['MYVAR'] = '1345'
    >>> myvar = read_env_variable('MYVAR', 'default')
    >>> type(myvar)
    str
    """
    if patterns is None:
        patterns = (
            (re.compile('^[-+]?[0-9]+$'), int),
            (re.compile('\d+\.\d+'), float),
            (re.compile(r'^(true|false)$', flags=re.IGNORECASE), lambda x: x.lower() == 'true'),
            (re.compile('[a-z/]+', flags=re.IGNORECASE), str),
            (re.compile('[a-z/]+\.[a-z/]+', flags=re.IGNORECASE), str),
        )

    if arg in os.environ:
        var = os.environ[arg]
        if var is None:
            ex = KeyError('environment variable %s not set' % arg)
            logger.exception(ex)
            raise ex
        else:
            if default:
                return str(var)     # force default type (str)
            else:
                for pattern, func in patterns:
                    if pattern.match(var):
                        return func(var)
            # type not identified
            logger.warning(
                '%s: failed to identify environment variable [%s] type. May contain \
                special characters' % (inspect.stack()[0][3], arg)
                 )
            return str(var)
    else:
        ex = KeyError('environment variable %s not set' % arg)
        logger.exception(ex)
        raise ex


def get_account_info(account_profile=None):
    """
    Summary:
        Queries AWS iam and sts services to discover account id information
        in the form of account name and account alias (if assigned)

    Returns:
        TYPE: tuple

    Example usage:

    >>> account_number, account_name = lambda_utils.get_account_info()
    >>> print(account_number, account_name)
    103562488773 tooling-prod

    """
    if account_profile:
        session = boto3.Session(profile_name=account_profile)
        sts_client = session.client('sts')
        iam_client = session.client('iam')
    else:
        sts_client = boto3.client('sts')
        iam_client = boto3.client('iam')

    try:
        number = sts_client.get_caller_identity()['Account']
        name = iam_client.list_account_aliases()['AccountAliases'][0]

    except IndexError as e:
        name = '<no_alias_assigned>'
        logger.info('Error: %s. No account alias defined. account_name set to %s' % (e, name))
        return (number, name)
    except ClientError as e:
        logger.warning(
            "%s: problem retrieving caller identity (Code: %s Message: %s)" %
            (inspect.stack()[0][3], e.response['Error']['Code'], e.response['Error']['Message'])
            )
        raise e
    return (number, name)


def get_regions(profile=None):
    """
    Summary
        Returns list of region codes for all AWS regions worldwide

    Returns:
        TYPE: list

    """
    try:

        session = session_selector(profile)
        client = session.client('ec2')
        response = client.describe_regions()

    except ClientError as e:
        if e.response['Error']['Code'] == 'AuthFailure':
            return ['us-east-1']
        else:
            logger.critical(
                "%s: problem retrieving aws regions (Code: %s Message: %s)" %
                (inspect.stack()[0][3], e.response['Error']['Code'],
                e.response['Error']['Message']))
            raise e

    except NoCredentialsError:
            return ['us-east-1']
    return [region['RegionName'] for region in response['Regions']]


def sns_notification(topic_arn, subject, message, account_id=None, account_name=None):
    """
    Summary:
        Sends message to AWS sns service topic provided as a
        parameter

    Args:
        topic_arn (str): sns topic arn
        subject (str): subject of sns message notification
        message (str): message body

    Returns:
        TYPE: Boolean | Success or Failure
    """
    if not (account_id or account_name):
        account_id, account_name = get_account_info()

    # assemble msg
    header = 'AWS Account: %s (%s) | %s' % \
        (str(account_name).upper(), str(account_id), subject)
    msg = '\n%s\n\n%s' % (time.strftime('%c'), message)
    msg_dict = {'default': msg}

    # client
    region = (topic_arn.split('sns:', 1)[1]).split(":", 1)[0]
    client = boto3.client('sns', region_name=region)

    try:
        # sns publish
        response = client.publish(
            TopicArn=topic_arn,
            Subject=header,
            Message=json.dumps(msg_dict),
            MessageStructure='json'
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except ClientError as e:
        logger.exception(
            '%s: problem sending sns msg (Code: %s Message: %s)' %
            (inspect.stack()[0][3], e.response['Error']['Code'],
                e.response['Error']['Message']))
        return False


def import_file_object(filename):
    """

    Summary: imports block fs object

    Args: block filesystem object

    Returns:
        dictionary obj (valid json file), file data object

    """
    try:
        with open(filename, 'r') as handle:
            file_obj = handle.read()
            dict_obj = json.loads(file_obj)

    except OSError as e:
        logger.critical(
            'import_file_object: %s error opening %s' % (str(e), str(filename))
        )
        raise e
    except ValueError:
        logger.info(
            '%s: import_file_object: %s not json. file object returned' %
            (inspect.stack()[0][3], str(filename))
        )
        return file_obj    # reg file, not valid json
    return dict_obj


def range_bind(min_value, max_value, value):
    """ binds number to a type and range """
    if value not in range(min_value, max_value + 1):
        value = min(value, max_value)
        value = max(min_value, value)
    return int(value)
