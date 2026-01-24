# Copyright 2008-2022 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.delegates.
#
# lazr.delegates is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.delegates is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.delegates.  If not, see <http://www.gnu.org/licenses/>.

"""Decorator helpers that simplify class composition."""

__all__ = [
    'Passthrough',
    'delegate_to',
    ]

from zope.interface import classImplements


def delegate_to(*interfaces, context='context'):
    """Make an adapter into a decorator.

    Use like:

        @implementer(IRosettaProject)
        @delegate_to(IProject)
        class RosettaProject:
            def __init__(self, context):
                self.context = context

            def methodFromRosettaProject(self):
                return self.context.methodFromIProject()

    If you want to use a different name than "context" then you can explicitly
    say so:

        @implementer(IRosettaProject)
        @delegate_to(IProject, context='project')
        class RosettaProject:
            def __init__(self, project):
                self.project = project

            def methodFromRosettaProject(self):
                return self.project.methodFromIProject()

    The adapter class will implement the interface it is decorating.

    The minimal decorator looks like this:

    @delegate_to(IProject)
    class RosettaProject:
        def __init__(self, context):
            self.context = context
    """
    if len(interfaces) == 0:
        raise TypeError('At least one interface is required')

    def _decorator(cls):
        missing = object()
        for interface in interfaces:
            classImplements(cls, interface)
            for name in interface:
                if getattr(cls, name, missing) is missing:
                    setattr(cls, name, Passthrough(name, context))
        return cls
    return _decorator


class Passthrough:
    """Call the delegated class for the decorator class.

    If the ``adaptation`` argument is not None, it should be a callable. It
    will be called with the context, and should return an object that will
    have the delegated attribute. The ``adaptation`` argument is expected to
    be used with an interface, to adapt the context.
    """
    def __init__(self, name, contextvar, adaptation=None):
        self.name = name
        self.contextvar = contextvar
        self.adaptation = adaptation

    def __get__(self, inst, cls=None):
        if inst is None:
            return self
        else:
            context = getattr(inst, self.contextvar)
            if self.adaptation is not None:
                context = self.adaptation(context)
            return getattr(context, self.name)

    def __set__(self, inst, value):
        context = getattr(inst, self.contextvar)
        if self.adaptation is not None:
            context = self.adaptation(context)
        setattr(context, self.name, value)

    def __delete__(self, inst):
        raise NotImplementedError
