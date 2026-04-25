""" Helpers to support json encoding of session data """

from datetime import datetime


def set_last_activity(session, dt):
    """Set the last activity datetime as a string in the session.

    >>> session = {}
    >>> set_last_activity(session, datetime(2024, 1, 15, 10, 30, 45, 123456))
    >>> session['_session_security']
    '2024-01-15T10:30:45.123456'
    """
    session['_session_security'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')


def get_last_activity(session):
    """Return the last activity datetime stored in the session.

    Handles both microsecond and non-microsecond formats, and falls back
    gracefully when the key is missing or the value is malformed.

    >>> get_last_activity({'_session_security': '2024-01-15T10:30:45.123456'})
    datetime.datetime(2024, 1, 15, 10, 30, 45, 123456)
    >>> get_last_activity({'_session_security': '2024-01-15T10:30:45'})
    datetime.datetime(2024, 1, 15, 10, 30, 45)
    >>> type(get_last_activity({}))
    <class 'datetime.datetime'>
    """
    try:
        return datetime.strptime(session['_session_security'],
                '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        # Sessions written by older versions may lack microseconds.
        try:
            return datetime.strptime(session['_session_security'],
                    '%Y-%m-%dT%H:%M:%S')
        except (ValueError, TypeError):
            return datetime.now()
    except (AttributeError, TypeError, KeyError):
        # AttributeError: _strptime is a known Python threading bug
        # (http://bugs.python.org/issue7980); fall back gracefully.
        # KeyError: session key absent.
        return datetime.now()

