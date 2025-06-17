######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.858425                                                            #
######################################################################################################

from __future__ import annotations

import typing
_A = typing.TypeVar("_A", contravariant=False, covariant=False)
_R = typing.TypeVar("_R", contravariant=False, covariant=False)


class MulticoreException(Exception, metaclass=type):
    ...

def parallel_imap_unordered(func: typing.Callable[[_A], _R], iterable: typing.Iterable[_A], max_parallel: typing.Optional[int] = None, dir: typing.Optional[str] = None) -> typing.Iterator[_R]:
    """
    Parallelizes execution of a function using multiprocessing. The result
    order is not guaranteed.
    
    Parameters
    ----------
    func : Callable[[Any], Any]
        Function taking a single argument and returning a result
    iterable : Iterable[Any]
        Iterable over arguments to pass to fun
    max_parallel int, optional, default None
        Maximum parallelism. If not specified, it uses the number of CPUs
    dir : str, optional, default None
        If specified, it's the directory where temporary files are created
    
    Yields
    ------
    Any
        One result from calling func on one argument
    """
    ...

def parallel_map(func: typing.Callable[[_A], _R], iterable: typing.Iterable[_A], max_parallel: typing.Optional[int] = None, dir: typing.Optional[str] = None) -> typing.List[_R]:
    """
    Parallelizes execution of a function using multiprocessing. The result
    order is that of the arguments in `iterable`.
    
    Parameters
    ----------
    func : Callable[[Any], Any]
        Function taking a single argument and returning a result
    iterable : Iterable[Any]
        Iterable over arguments to pass to fun
    max_parallel int, optional, default None
        Maximum parallelism. If not specified, it uses the number of CPUs
    dir : str, optional, default None
        If specified, it's the directory where temporary files are created
    
    Returns
    -------
    List[Any]
        Results. The items in the list are in the same order as the items
        in `iterable`.
    """
    ...

