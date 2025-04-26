#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

from xenv import Variable


def test_recursion_expansion():
    x = Variable.Scalar('x')
    output = Variable.EnvExpander({'x': '${x}'}).process(x, '${x}')
    assert output == '${x}'

    output = Variable.EnvExpander({
        'x': '${y}',
        'y': '${x}'
    }).process(x, '${y}')
    assert output == '${y}'
