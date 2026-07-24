######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-07-23T20:46:32.715749                                                            #
######################################################################################################

from __future__ import annotations

import typing
_A = typing.TypeVar("_A", contravariant=False, covariant=False)
_R = typing.TypeVar("_R", contravariant=False, covariant=False)


class MulticoreException(Exception, metaclass=type):
    ...

def parallel_imap_unordered(func: typing.Callable[[_A], _R], iterable: typing.Iterable[_A], max_parallel: typing.Union[int, None] = None, dir: typing.Union[str, None] = None) -> typing.Iterator[_R]:
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

def parallel_map(func: typing.Callable[[_A], _R], iterable: typing.Iterable[_A], max_parallel: typing.Union[int, None] = None, dir: typing.Union[str, None] = None) -> typing.List[_R]:
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

