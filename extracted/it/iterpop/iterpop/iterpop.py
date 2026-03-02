"""Main module."""

from collections.abc import Iterable

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

from itertools import tee

def _iterable(obj):
    '''
    Is obj iterable?
    '''
    return isinstance(obj, Iterable)

def _pairwise(iterable):
    '''
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def _empty(iterable):
    '''
    Is iterable empty?
    '''
    try:
        return bool(iterable)
    # handle "The truth value of a [Pandas] Series is ambiguous."
    except ValueError:
        return len(iterable)

def popsingleton(
    container,
    catch_empty=False,
    catch_overfull=False,
    default=None,
):
    '''
    Extract the value of a single-element iterator.
    Raise exceptions or return default value if iterator is not single-element.
    '''
    try:
        res, = container
        return res
    except ValueError:
        if not _iterable(container):
            raise TypeError(container, 'is not iterable')
        elif _empty(container) and not catch_overfull:
            raise ValueError(container, 'is overfull')
        elif not _empty(container) and not catch_empty:
            raise ValueError(container, 'is empty')

        return default



def pophomogeneous(
    container,
    catch_empty=False,
    catch_heterogeneous=False,
    default=None,
):
    '''
    Extract the value of a homogeneous iterator.
    Raise exceptions or return default value if iterator is not homogeneous.
    '''

    if not _iterable(container):
        raise TypeError(container, 'is not iterable')

    handle1, handle2, handle3 = tee(container, 3)
    res = default
    not_empty = any(True for _ in handle1)
    is_empty = not not_empty

    if is_empty and (not catch_empty):
        raise ValueError(container, 'is empty')
    elif not_empty and all(
        a == b
        for a, b in _pairwise(handle2)
    ):
        res = next(handle3)
    elif not_empty and (not catch_heterogeneous):
        raise ValueError(container, 'is heterogeneous')

    return res

def poursingleton(container, default=None):
    '''
    Extract the value of a single-element iterator that might be empty.
    Return default if iterator is empty.
    '''
    return popsingleton(
        container,
        catch_empty=True,
        default=default,
    )

def pourhomogeneous(container, default=None):
    '''
    Extract the value of a homogeneous iterator that might be empty.
    Return default if iterator is empty.
    '''
    return pophomogeneous(
        container,
        catch_empty=True,
        default=default,
    )
