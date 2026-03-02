#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Amazon Software License (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/asl/
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.


import logging
import sys
from datetime import datetime
import os
from six import PY3
import time
from dateutil.tz import *

ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
ISO8601_FORMAT2 = '%Y-%m-%dT%H:%M:%S.%f%z'

logger = logging.getLogger(__name__)


def epoch(dt):
    """
    Return the number of milliseconds since January 1, 1970, 00:00:00 GMT.
    If tzinfo is not timezone aware, treat it as UTC time.
    """
    if dt.tzinfo:
        delta = (dt - datetime(1970, 1, 1, tzinfo=tzutc()))
    else:
        delta = (dt - datetime(1970, 1, 1))
    return delta.days*24*3600*1000 + delta.seconds*1000 +\
        delta.microseconds//1000


def iso8601_to_epoch(utc_dt_str):
    dt = datetime.strptime(utc_dt_str, ISO8601_FORMAT)
    dt = dt.replace(tzinfo=tzutc())
    return epoch(dt)


def get_current_millis():
    return int(time.time() * 1000)


def get_current_time_str():
    return datetime.now().replace(tzinfo=tzlocal()).strftime(ISO8601_FORMAT2)


def print_stdout(content):
    """
    This function is used to properly write unicode to stdout.  It
    ensures that the proper encoding is used if the statement is
    not in a version type of string.  The initial check is to
    allow if ``sys.stdout`` does not use an encoding
    """
    encoding = getattr(sys.stdout, 'encoding', None)
    if encoding is not None and not PY3:
        sys.stdout.write(content.encode(sys.stdout.encoding))
    else:
        try:
            sys.stdout.write(content)
        except UnicodeEncodeError:
            if not PY3:
                sys.stdout.write(content.encode('utf-8'))
            else:
                # str.encode returns type bytes in python3, so we need to convert
                # this back to encoded string to avoid a type error
                sys.stdout.write(str(content.encode('utf-8'), encoding='utf-8'))
    sys.stdout.write('\n')
    sys.stdout.flush()

def print_stderr(content):
    """
    This function is used to properly write unicode to stderr.  It
    ensures that the proper encoding is used if the statement is
    not in a version type of string.  The initial check is to
    allow if ``sys.stderr`` does not use an encoding
    """
    encoding = getattr(sys.stderr, 'encoding', None)
    if encoding is not None and not PY3:
        sys.stderr.write(content.encode(sys.stderr.encoding))
    else:
        try:
            sys.stderr.write(content)
        except UnicodeEncodeError:
            if not PY3:
                sys.stderr.write(content.encode('utf-8'))
            else:
                # str.encode returns type bytes in python3, so we need to convert
                # this back to encoded string to avoid a type error
                sys.stderr.write(str(content.encode('utf-8'), encoding='utf-8'))
    sys.stderr.write('\n')
    sys.stderr.flush()


def validate_file_readable(file):
    if not os.access(file, os.F_OK):
        raise ValueError("File '%s' does not exist" % file)
    if not os.access(file, os.R_OK):
        raise ValueError("File '%s' is not readable" % file)
    if not os.path.isfile(file):
        raise ValueError("File '%s' is not a file" % file)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time() * 1000
        result = method(*args, **kw)
        te = time.time() * 1000
        logger.info('Timing=%s=%d', method.__name__, te-ts)
        return result
    return timed
