# coding: utf-8

# Copyright © 2011-2013 Julian Mehnle <julian@mehnle.net>,
# Copyright © 2011-2013 Scott Kitterman <scott@kitterman.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Package for parsing ``Authentication-Results`` headers as defined in RFC
5451/7001/7601.  Optional support for authentication methods defined in RFCs
5617, 6008, 6212, 7281, 7489, and draft-ietf-dmarc-arc-protocol-05.
"""

__author__  = 'Julian Mehnle, Scott Kitterman'
__email__   = 'scott@kitterman.com'

def _test():
    import doctest
    import authres
    doctest.testfile("tests")
    return doctest.testmod(authres)

_test()

# vim:sw=4 sts=4
