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
from threading import Thread
import traceback


logger = logging.getLogger(__name__)


class ExitChecker(Thread):
    """
    This thread periodically checks the stop_flag and leaves when
    stop_flag is set.
    """

    def __init__(self, stop_flag):
        super(ExitChecker, self).__init__()
        self.daemon = True
        self.stop_flag = stop_flag

    def run(self):
        while True:
            if self.stop_flag.is_set():
                break
            else:
                self.stop_flag.wait(2)


class BaseThread(Thread):
    """
    This thread should be extended by concrete thread which overrides
    the _run() method. If it exists accidentally, it sets the group
    stop flag so other threads in the same group could exit as well.
    """

    def __init__(self, stop_flag):
        super(BaseThread, self).__init__()
        self.daemon = True
        # global stop flag which is shared by all threads
        self.stop_flag = stop_flag
        # group stop flag which is shared by a group of threads
        self.group_stop_flag = None

    def run(self):
        try:
            self._run()
        except Exception as e:
            logger.error("Exception caught in %s", self, exc_info=True)
            self.on_run_failed(e)
            self.stop_flag.wait(60)
            # If a thread exits accidentally, other threads in the same group
            # should exit as well.
            if self.group_stop_flag and not self.group_stop_flag.is_set():
                self.group_stop_flag.set()

    def on_run_failed(self, exception):
        # Subclasses can optionally handle failures in custom ways here.
        pass

    def _run(self):
        raise NotImplementedError("_run")

    def _exit_needed(self):
        return (self.stop_flag.is_set() or
                (self.group_stop_flag and self.group_stop_flag.is_set()))
