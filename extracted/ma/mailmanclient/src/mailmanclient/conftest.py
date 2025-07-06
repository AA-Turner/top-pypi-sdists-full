# Copyright (C) 2017-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Testing utilities."""

import pytest
import subprocess
import socket
from contextlib import closing


def check_core():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(('localhost', 9001)) == 0:
            return True
        else:
            return False


@pytest.fixture(scope='module', autouse=True)
def mailman_core(request, watcher_getter):
    """Mailman Core instance which is ready to be used by the tests"""
    def teardown_core():
        print('Stopping Mailman Server')
        subprocess.run(['mailman', 'stop'])
        subprocess.run(['rm', '-rf', 'var/'])
    request.addfinalizer(teardown_core)

    print('Starting Mailman Server')

    return watcher_getter(
        name='master',
        arguments=['-C', 'mailman_test.cfg'],
        checker=check_core,
        request=request,
    )
