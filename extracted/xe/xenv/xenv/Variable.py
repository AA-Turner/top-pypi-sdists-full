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
'''
Created on Jun 27, 2011

@author: mplajner
'''
import re
import os
import logging
import functools
from os import listdir
from os.path import normpath
from zipfile import is_zipfile
from string import Template


try:
    from functools import cache
except ImportError:  # py < 3.9

    def cache(func):
        """
        Memoization decorator for a function taking a single argument.
        """

        cache = func.cache = {}

        @functools.wraps(func)
        def memoizer(arg):
            try:
                return cache[arg]
            except KeyError:
                return cache.setdefault(arg, func(arg))

        return memoizer


class VariableProcessor(object):
    '''
    Base class for the objects used to process the variables.
    '''

    def __init__(self, env):
        '''
        @param env: dictionary with the reference environment to use
        '''
        if env is None:
            env = {}
        self._env = env

    def isTarget(self, variable):
        '''
        Return True if this processor can operate on the given variable.
        '''
        return True

    def process(self, variable, value):
        '''
        Process the variable.

        @param value: the content of the variable to be processed
        @return: the processed value
        '''
        # by default do nothing
        return value

    def __call__(self, variable, value):
        return self.process(variable, value)


class ListProcessor(VariableProcessor):
    '''
    Base class for processors operating only on lists.
    '''

    def isTarget(self, variable):
        '''
        Return True if this variable is a list.
        '''
        return isinstance(variable, List)


class ScalarProcessor(VariableProcessor):
    '''
    Base class for processors operating only on scalars.
    '''

    def isTarget(self, variable):
        '''
        Return True if this variable is a scalar.
        '''
        return isinstance(variable, Scalar)


class ExpanderEngine(Template):
    idpattern = r'[_a-z][_a-z0-9]*|\.'


class EnvExpander(VariableProcessor):
    '''
    Variable processor to expand the reference to environment variables.
    '''

    def isTarget(self, variable):
        return (super(EnvExpander, self).isTarget(variable)
                and variable.expandVars)

    def _repl(self, value):
        '''
        Recursive expansion of variables in value.
        '''
        old_value = None
        expanded = set()  # remember variables already expanded
        while value != old_value:
            old_value = value
            to_expand = set(m[1] or m[2]
                            for m in ExpanderEngine.pattern.findall(value)
                            if m[1] or m[2])
            if not expanded.isdisjoint(to_expand):
                # refuse to further expand variables already expanded to avoid
                # infinite recursion
                break
            expanded.update(to_expand)
            value = ExpanderEngine(value).safe_substitute(self._env)
        return value

    def process(self, variable, value):
        if isinstance(value, str):
            value = self._repl(value)
        else:
            # expand only in the elements that are new
            old_values = set(variable.val)
            value = [v if v in old_values else self._repl(v) for v in value]
        return value


class PathNormalizer(VariableProcessor):
    '''
    Call os.path.normpath for all the entries of the variable.
    '''

    def process(self, variable, value):
        if not value:  # do not process empty strings/lists
            return value
        if isinstance(value, str):
            if '://' not in value:  # this might be a URL
                value = normpath(value)
        else:
            value = [normpath(v) for v in value if v]
        return value


class DuplicatesRemover(ListProcessor):
    '''
    Remove duplicates entries from lists.
    '''

    def process(self, variable, value):
        val = []
        for s in value:
            if s not in val:
                val.append(s)
        return val


normpath = cache(normpath)
is_zipfile = cache(is_zipfile)


@cache
def isnonemptydir(path):
    '''
    Return whether a path is a list-able non-empty directory.
    '''

    try:
        return bool(listdir(path))
    except OSError:
        return False


class EmptyDirsRemover(ListProcessor):
    '''
    Remove empty or not existing directories from lists.
    '''

    def process(self, variable, value):
        return [s for s in value if s.endswith('.zip') or isnonemptydir(s)]


class UsePythonZip(ListProcessor):
    '''
    Use .zip files instead of regular directories in PYTHONPATH when possible.
    '''

    def isTarget(self, variable):
        return (super(UsePythonZip, self).isTarget(variable)
                and variable.varName == 'PYTHONPATH')

    def process(self, variable, value):
        val = []
        for s in value:
            z = s + '.zip'
            if is_zipfile(z):
                val.append(z)
            else:
                val.append(s)
        return val


# Default (minimal) set of processors.
processors = [
    EnvExpander,
    PathNormalizer,
    DuplicatesRemover,
    # special processors
    EmptyDirsRemover,
    UsePythonZip
]

# FIXME: these are back-ward compatibility hacks: we need a proper way to add/remove processors
if ('no-strip-path' in os.environ.get('CMTEXTRATAGS', '')
        or 'GAUDI_NO_STRIP_PATH' in os.environ
        or 'LB_NO_STRIP_PATH' in os.environ):
    processors.remove(EmptyDirsRemover)

if 'no-pyzip' in os.environ.get('CMTEXTRATAGS', ''):
    processors.remove(UsePythonZip)


class VariableBase(object):
    '''
    Base class for the classes used to manipulate the environment.
    '''

    def __init__(self, name, local=False):
        self.varName = name
        self.local = local
        self.expandVars = True
        self.log = logging.getLogger('Variable')

    def process(self, value, env):
        '''
        Call all the processors defined in the processors list on 'value'.

        @return: the processed value
        '''
        for p in [c(env) for c in processors]:
            if p.isTarget(self):
                value = p(self, value)
        return value


class List(VariableBase):
    '''
    Class for manipulating with environment lists.

    It holds its name and values represented by a list.
    Some operations are done with separator, which is usually colon. For windows use semicolon.
    '''

    def __init__(self, name, local=False):
        super(List, self).__init__(name, local)
        self.val = []

    def name(self):
        '''Returns the name of the List.'''
        return self.varName

    def set(self, value, separator=':', environment=None, process=True):
        '''Sets the value of the List. Any previous value is overwritten.'''
        if isinstance(value, str):
            value = EnvExpander(environment).process(self, value).split(separator)
        if process:
            value = self.process(value, environment)
        self.val = value

    def unset(self, value, separator=':', environment=None):  # pylint: disable=W0613
        '''Sets the value of the List to empty. Any previous value is overwritten.'''
        self.val = []

    def value(self, asString=False, separator=':'):
        '''Returns values of the List. Either as a list or string with desired separator.'''
        if asString:
            return separator.join(self.val)
        else:
            # clone the list
            return list(self.val)

    def remove_regexp(self, value, separator=':'):
        self.remove(value, separator, True)

    def remove(self, value, separator=':', regexp=False):
        '''Removes value(s) from List. If value is not found, removal is canceled.'''
        if regexp:
            value = self.search(value, True)

        elif isinstance(value, str):
            value = value.split(separator)

        for i in range(len(value)):
            val = value[i]
            if val not in value:
                self.log.info(
                    'Value "%s" not found in List: "%s". Removal canceled.',
                    val, self.varName)
            while val in self.val:
                self.val.remove(val)

    def append(self, value, separator=':', environment=None):
        '''Adds value(s) at the end of the list.'''
        if isinstance(value, str):
            value = EnvExpander(environment).process(self, value).split(separator)
        self.val = self.process(self.val + value, environment)

    def prepend(self, value, separator=':', environment=None):
        '''Adds value(s) at the beginning of the list.
        resolve references and duplications'''
        if isinstance(value, str):
            value = EnvExpander(environment).process(self, value).split(separator)
        self.val = self.process(value + self.val, environment)

    def search(self, expr, regExp):
        '''Searches in List's values for a match

        Use string value or set regExp to True.
        In the first case search is done only for an exact match for one of List`s value ('^' and '$' added).
        '''
        if not regExp:
            expr = '^' + expr + '$'
        v = re.compile(expr)
        res = []
        for val in self.val:
            if v.search(val):
                res.append(val)

        return res

    def __getitem__(self, key):
        return self.val[key]

    def __setitem__(self, key, value):
        if value in self.val:
            self.log.info(
                'Var: "%s" value: "%s". Addition canceled because of duplicate entry.',
                self.varName, value)
        else:
            self.val.insert(key, value)

    def __delitem__(self, key):
        self.remove(self.val[key])

    def __iter__(self):
        for i in self.val:
            yield i

    def __contains__(self, item):
        return item in self.val

    def __len__(self):
        return len(self.val)

    def __str__(self):
        return ':'.join(self.val)


class Scalar(VariableBase):
    '''Class for manipulating with environment scalars.'''

    def __init__(self, name, local=False):
        super(Scalar, self).__init__(name, local)
        self.val = ''

    def name(self):
        '''Returns the name of the scalar.'''
        return self.varName

    def set(self, value, separator=':', environment=None, process=True):  # pylint: disable=W0613
        '''Sets the value of the scalar. Any previous value is overwritten.'''
        if process:
            value = self.process(value, environment)
        self.val = value

    def unset(self, value, separator=':', environment=None):  # pylint: disable=W0613
        '''Sets the value of the variable to empty. Any previous value is overwritten.'''
        self.val = ''

    def value(self, asString=False, separator=':'):  # pylint: disable=W0613
        '''Returns values of the scalar.'''
        return self.val

    def remove_regexp(self, value, separator=':'):
        self.remove(value, separator, True)

    def remove(self, value, separator=':', regexp=True):  # pylint: disable=W0613
        '''Removes value(s) from the scalar. If value is not found, removal is canceled.'''
        value = self.search(value)
        for val in value:
            self.val = self.val.replace(val, '')

    def append(self, value, separator=':', environment=None):  # pylint: disable=W0613
        '''Adds value(s) at the end of the scalar.'''
        self.val += self.process(value, environment)

    def prepend(self, value, separator=':', environment=None):  # pylint: disable=W0613
        '''Adds value(s) at the beginning of the scalar.'''
        self.val = self.process(value, environment) + self.val

    def search(self, expr):
        '''Searches in scalar`s values for a match'''
        return re.findall(expr, self.val)

    def __str__(self):
        return self.val


class EnvError(Exception):
    '''Class which defines errors for locals operations.'''

    def __init__(self, value, code):
        super(EnvError, self).__init__()
        self.val = value
        self.code = code

    def __str__(self):
        if self.code == 'undefined':
            return 'Reference to undefined environment element: "' + self.val + '".'
        elif self.code == 'ref2var':
            return 'Reference to list from the middle of string.'
        elif self.code == 'redeclaration':
            return 'Wrong redeclaration of environment element "' + self.val + '".'
