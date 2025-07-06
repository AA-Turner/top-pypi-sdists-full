# Copyright (c) 2018-2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

"""
A(n almost) drop-in replacement for the :mod:`logging` module of the standard
library with support for two new log levels (:data:`TRACE` and :data:`DISABLE`),
mapping of textual log levels to numeric values, and loggers with a ``trace()``
method.

Use it as:

.. code-block:: python

    from inators import log as logging

Known issues:

  - The logger returned by :meth:`~logging.Logger.getChild` has no ``trace()``
    method, even if the parent logger has.
  - No new level names are registered via :func:`logging.addLevelName` to avoid
    global state pollution. This means that functions and methods that accept a
    string representation of the level will not work with ``'TRACE'`` or
    ``'DISABLE'``. However, :data:`levels` can be used to map both original and
    new level names to numerical values.
"""

from logging import *


TRACE = DEBUG // 2      #: A logging level below ``DEBUG``.
DISABLE = CRITICAL * 2  #: A logging level way above ``CRITICAL``.


#: A mapping of log level names to numeric values. It contains all predefined
#: levels from :mod:`logging`, plus :data:`TRACE` and :data:`DISABLE`.
levels = {
    'TRACE': TRACE,
    'DEBUG': DEBUG,
    'INFO': INFO,
    'WARNING': WARNING,
    'ERROR': ERROR,
    'CRITICAL': CRITICAL,
    'DISABLE': DISABLE,
}


__getLogger = getLogger


def getLogger(name=None):
    """
    Return a logger as in :func:`logging.getLogger`, but extended with a method
    ``trace(msg, *args, **kwargs)`` that logs a message with level
    :data:`TRACE`. The arguments are interpreted as for
    :meth:`logging.Logger.debug`.
    """
    logger = __getLogger(name)
    logger.trace = lambda msg, *args, **kwargs: logger.log(TRACE, msg, *args, **kwargs)
    return logger
