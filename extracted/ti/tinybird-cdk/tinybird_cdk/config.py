import os

from . import errors


def get(key, **kwargs):
    '''
    Returns the value for the given configuration key.

        * The function first checks the system environment.
        * If not found and there is a ``default`` keyword argument, returns its
          associated value, even if it is ``None``.
        * If there is no default but an ``optional`` true keyword argument is
          passed, the function returns ``None``.
        * Otherwise, raises ``tinybird_cdk.errors.MissingConfiguration``.
    '''
    value = os.getenv(key)
    if value is None:
        if 'default' in kwargs:
            return kwargs['default']
        if kwargs.get('optional'):
            return None
        raise errors.MissingConfiguration(key)
    return value
