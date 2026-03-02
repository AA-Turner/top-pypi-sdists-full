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

import functools
import sys
import random
import time
from threading import Event


class ExponentialBackoff(object):

    """
    Decorator which performs exponential backoff and retry of a function for up
    to a maximum of max_retries every time the function returns an exception.
    If max_retries is exceeded, raise an exception with the traceback of the
    last exception thrown.

    Customize using:
     * max_retries:
       set to the number of times to retry a failing method call
       Default: 5
     * logger:
       supply a logging.Logger object to send exception information to
       this stream
       Default: None
     * exception:
       to catch only a subset of exceptions. Use a tuple to catch
       multiple exceptions
       Default: None (catches all exceptions)
     * stderr:
       set to True to print exception information to sys.stderr.
       Default: False
     * initial_backoff:
       set the number of seconds for the first backoff.
       Default: 1s
     * rand_factor:
       randomize the backoff to a value which is between
       backoff * (1-rand_factor) and backoff * (1+rand_factor)
       Default: 0.5
     * max_backoff:
       set the number of seconds for the max backoff.
       Default: 60s
     * stop_flag:
       supply an Event object to stop the retry.
       Default: None
    """

    def __init__(self, max_retries=5, logger=None, exception=Exception,
                 stderr=False, initial_backoff=1, quiet=False,
                 rand_factor=0.5, max_backoff=60, stop_flag=None):
        self.max_retries = max_retries
        self.logger = logger
        self.exception = exception
        self.stderr = stderr
        self.quiet = quiet
        self.rand_factor = rand_factor
        self.max_backoff = max_backoff
        self.stop_flag = stop_flag

        if not self.stop_flag:
            self.stop_flag = Event()
        if initial_backoff <= 0:
            raise ValueError('initial_backoff must be larger than zero: %s' %
                             initial_backoff)
        else:
            self.initial_backoff = initial_backoff
        if self.rand_factor < 0 or self.rand_factor > 1:
            raise ValueError('rand_factor must be between 0 and 1')

    def __call__(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            retry = 0
            while retry < self.max_retries:
                try:
                    return f(*args, **kwargs)
                except self.exception as e:
                    if self.logger:
                        self.logger.warning(e)
                if self.stop_flag.is_set():
                    break
                backoff = self._calc_backoff(retry)
                # Requested logging
                if retry < self.max_retries - 1:
                    msg = 'Method "%s" failed, backing off %s seconds, ' \
                          'and retrying' % (f.__name__, backoff)
                else:
                    msg = 'Method "%s" has failed for the last time.' \
                          % (f.__name__)
                if self.quiet:
                    pass
                else:
                    if self.logger:
                        self.logger.warning(msg)
                    if self.stderr:
                        sys.stderr.write('%s\n' % msg)
                # Sleep, except after the last failed attempt
                if retry < self.max_retries - 1:
                    self.stop_flag.wait(backoff)
                retry += 1

            # Dropped out of the while loop so we've exhausted all retries
            raise RuntimeError(
                'Method "%s" has failed after %s unsuccessful '
                'attempts.' % (f.__name__, retry))

        return wrapper

    def _calc_backoff(self, retry):
        backoff = self.initial_backoff * (2 ** retry)
        if self.rand_factor:
            rand_value = random.uniform(1 - self.rand_factor,
                                        1 + self.rand_factor)
            backoff = backoff * rand_value
        if backoff >= self.max_backoff:
            return self.max_backoff
        else:
            return backoff
