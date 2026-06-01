# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import subprocess32 as subprocess
import sys

from threading import Lock

__print_lock = Lock()


def safe_print(message):
    """
    Grab the lock and print to stdout.
    The lock is to serialize messages from
    different thread. 'stty sane' is to
    clean up any hiden space.
    """
    with __print_lock:
        subprocess.call('stty sane', shell=True)
        sys.stdout.write(message)
        sys.stdout.flush()
        subprocess.call('stty sane', shell=True)
