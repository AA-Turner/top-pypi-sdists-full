# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest

from inators import imp as inators_imp


@pytest.mark.parametrize('name, object', [
    ('inators.imp.import_object', inators_imp.import_object)
])
def test_import_object(name, object):
    assert inators_imp.import_object(name) == object
