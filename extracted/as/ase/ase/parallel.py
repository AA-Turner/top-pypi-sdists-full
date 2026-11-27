import atexit
import functools
import os
import pickle
import sys
import time
import warnings
from abc import abstractmethod
from typing import Protocol

import numpy as np


def paropen(name, mode='r', buffering=-1, encoding=None, comm=None):
    """MPI-safe version of open function.

    In read mode, the file is opened on all nodes.  In write and
    append mode, the file is opened on the master only, and /dev/null
    is opened on all other nodes.
    """
    if comm is None:
        comm = world
    if comm.rank > 0 and mode[0] != 'r':
        name = os.devnull
    return open(name, mode, buffering, encoding)


def parprint(*args, comm=None, **kwargs):
    """MPI-safe print - prints only from master."""
    if comm is None:
        comm = world
    if comm.rank == 0:
        print(*args, **kwargs)


class MPICommunicator(Protocol):
    """Limited interface to MPI communicator for ASE."""

    rank: int
    """Rank of this process on the communicator."""
    size: int
    """Number of processes on this communicator."""

    @property
    def backend(self) -> str:
        """A string identifier for this Python MPI interface.

        The purpose of this string is to be able to check that the
        correct MPI implementation is in use.

        Each implementing subclass of this protocol should normally
        try to pick a string that will be distinct from those of other
        implementations, whereas wrappers should normally return the
        backend of the wrapped communicator.

        ASE already provides the implementations 'serial' and 'ase-mpi4py'.
        """
        raise NotImplementedError

    @abstractmethod
    def sum(self, a: np.ndarray, root: int = -1) -> None:
        """In-place sum over ranks.

        The sum is computed only on the rank specified by root,
        or all ranks if root is -1."""
        raise NotImplementedError

    @abstractmethod
    def sum_scalar(self, a, root: int = -1):
        """Return the sum over ranks of a scalar.

        See sum() for rules about root."""
        raise NotImplementedError

        # Input could be any kind of scalar, and we presumably want to
        # return the same kind of scalar.  But actually, probably a
        # python scalar becomes a numpy scalar in our various
        # implementations.

    def product(self, a: np.ndarray, root: int = -1) -> None:
        """In-place product over ranks.

        See sum() for rules about root."""
        # This should be abstract, but due to an oversight,
        # MPI4Py does not have it.  So now it is effectively optional.
        raise NotImplementedError

    @abstractmethod
    def broadcast(self, a: np.ndarray, root: int) -> None:
        """Broadcast array from root across all ranks."""
        raise NotImplementedError

    @abstractmethod
    def barrier(self) -> None:
        """Wait until all ranks reach barrier."""
        raise NotImplementedError

    @abstractmethod
    def abort(self, code: int) -> None:
        """Abort runtime with given error code."""
        raise NotImplementedError

    # The mpi4py communicator actually defines .split() as well, but
    # probably we don't want to advertise that.


class DummyMPI(MPICommunicator):
    rank = 0
    size = 1
    backend = 'serial'

    def _returnval(self, a, root=-1):
        # MPI interface works either on numbers, in which case a number is
        # returned, or on arrays, in-place.
        if np.isscalar(a):
            return a
        if hasattr(a, '__array__'):
            a = a.__array__()
        assert isinstance(a, np.ndarray)
        return None

    def sum(self, a, root=-1):
        if np.isscalar(a):
            warnings.warn(
                'Please use sum_scalar(...) for scalar arguments', FutureWarning
            )
        return self._returnval(a)

    def sum_scalar(self, a, root=-1):
        return a

    def product(self, a, root=-1):
        return self._returnval(a)

    def broadcast(self, a, root):
        assert root == 0
        return self._returnval(a)

    def barrier(self):
        pass

    def abort(self, code: int):
        # Note: in practice we do not register an abort() call in serial.
        raise SystemExit(code)


class MPI:
    """Wrapper for MPI world object.

    Decides at runtime (after all imports) which one to use:

    * MPI4Py
    * GPAW
    * Asap
    * a dummy implementation for serial runs

    """

    def __init__(self):
        self.comm = None

    def __getattr__(self, name):
        # Pickling of objects that carry instances of MPI class
        # (e.g. NEB) raises RecursionError since it tries to access
        # the optional __setstate__ method (which we do not implement)
        # when unpickling. The two lines below prevent the
        # RecursionError. This also affects modules that use pickling
        # e.g. multiprocessing.  For more details see:
        # https://gitlab.com/ase/ase/-/merge_requests/2695
        if name == '__setstate__':
            raise AttributeError(name)

        if self.comm is None:
            self.comm = _get_comm()

        gpaw_asap_specific_attrs = {
            'scatter',
            'min',
            'min_scalar',
            'max',
            'max_scalar',
            'send',
            'gather',
            'all_gather',
            'alltoallv',
            'new_communicator',
            'test',
            'testall',
            'wait',
            'waitall',
            'get_members',
            'compare',
            'translate_ranks',
            'get_c_object',
        }

        if name in gpaw_asap_specific_attrs:
            warnings.warn(
                'In the future, unless ASE_PARALLEL_WORLD_HOOK is specified, '
                'ase.parallel.world will provide only the '
                'ase.parallel.MPICommunicator interface, '
                f'and this does not include a {name!r} attribute.',
                FutureWarning,
            )

        return getattr(self.comm, name)


def deprecated_mpi(name):
    warnings.warn(
        'MPI was initialized in ase.parallel using a legacy mechanism.  '
        'In the future, this will result in a serial runtime '
        'as far as ase.parallel is concerned.  Please use the '
        'ASE_PARALLEL_WORLD_HOOK mechanism instead.  The legacy '
        'initialization was triggered because no hook was specified, '
        f'and the module {name} module was imported.',
        FutureWarning,
    )


def _get_comm():
    """Get the correct MPI world object."""
    if 'mpi4py' in sys.modules:
        deprecated_mpi('mpi4py')
        return MPI4PY()
    if '_gpaw' in sys.modules:
        world = _gpaw_world()
        if world is not None and getattr(world, 'backend', None) != 'serial':
            deprecated_mpi('_gpaw')
            return world
    if '_asap' in sys.modules:
        world = _asap_world()
        if world is not None:
            deprecated_mpi('_asap')
            return world
    return DummyMPI()


class MPI4PY(MPICommunicator):
    backend = 'ase-mpi4py'

    def __init__(self, mpi4py_comm=None):
        if mpi4py_comm is None:
            from mpi4py import MPI

            mpi4py_comm = MPI.COMM_WORLD
        self.comm = mpi4py_comm

    @property
    def rank(self):
        return self.comm.rank

    @property
    def size(self):
        return self.comm.size

    def _returnval(self, a, b):
        """Behave correctly when working on scalars/arrays.

        Either input is an array and we in-place write b (output from
        mpi4py) back into a, or input is a scalar and we return the
        corresponding output scalar."""
        if np.isscalar(a):
            assert np.isscalar(b)
            return b
        else:
            assert not np.isscalar(b)
            a[:] = b
            return None

    def sum(self, a, root=-1):
        if root == -1:
            b = self.comm.allreduce(a)
        else:
            b = self.comm.reduce(a, root)
        if np.isscalar(a):
            warnings.warn(
                'Please use sum_scalar(...) for scalar arguments', FutureWarning
            )
        return self._returnval(a, b)

    def sum_scalar(self, a, root=-1):
        if root == -1:
            b = self.comm.allreduce(a)
        else:
            b = self.comm.reduce(a, root)
        return b

    def split(self, split_size=None):
        """Divide the communicator."""
        # color - subgroup id
        # key - new subgroup rank
        if not split_size:
            split_size = self.size
        color = int(self.rank // (self.size / split_size))
        key = int(self.rank % (self.size / split_size))
        comm = self.comm.Split(color, key)
        return MPI4PY(comm)

    def barrier(self):
        self.comm.barrier()

    def abort(self, code):
        self.comm.Abort(code)

    def broadcast(self, a, root):
        b = self.comm.bcast(a, root=root)
        if self.rank == root:
            if np.isscalar(a):
                return a
            return None
        return self._returnval(a, b)


def _asap_world():
    import _asap

    try:
        world = _asap.Communicator()
    except (AttributeError, RuntimeError):
        return None

    return world


def _gpaw_world():
    import _gpaw

    if not hasattr(_gpaw, 'Communicator'):
        return None

    # Return the actual public (possibly wrapper) object
    from gpaw.mpi import world

    return world


# Note to implementors:
#   Whoever sets this variable MUST check that it was not already set!
#   If it is set in two places, there are two competing parallel
#   mechanisms and that must be avoided.
mpiworld_importpath = os.environ.get('ASE_PARALLEL_WORLD_HOOK')

world: MPI | MPICommunicator

if mpiworld_importpath is None:
    # In the future this will be always serial!
    # We should detect if we would set a real communicator here
    # and issue a FutureWarning there.
    mpiworld_module = None
    world = MPI()

    # Once we remove these MPI behaviours, all other MPI initialization
    # code in ASE can be removed.
else:
    import importlib

    mpiworld_module = importlib.import_module(mpiworld_importpath)
    world = mpiworld_module.ASE_PARALLEL_WORLD_HOOK()
    if world is None:
        # The application declined to make a parallel MPI communicator
        world = DummyMPI()


def barrier():
    world.barrier()


def broadcast(obj, root=0, comm=world):
    """Broadcast a Python object across an MPI communicator and return it."""
    if comm.rank == root:
        string = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
        n = np.array([len(string)], int)
    else:
        string = None
        n = np.empty(1, int)
    comm.broadcast(n, root)
    if comm.rank == root:
        string = np.frombuffer(string, np.int8)
    else:
        string = np.zeros(n, np.int8)
    comm.broadcast(string, root)
    if comm.rank == root:
        return obj
    else:
        return pickle.loads(string.tobytes())


def parallel_function(func):
    """Decorator for broadcasting from master to slaves using MPI.

    Disable by passing parallel=False to the function.  For a method,
    you can also disable the parallel behavior by giving the instance
    a self.serial = True.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        parallel = kwargs.pop('parallel', True)
        if (
            world.size == 1
            or (args and getattr(args[0], 'serial', False))
            or not parallel
        ):
            # Disable:
            return func(*args, **kwargs)

        ex = None
        result = None
        if world.rank == 0:
            try:
                result = func(*args, **kwargs)
            except Exception as x:
                ex = x
        ex, result = broadcast((ex, result))
        if ex is not None:
            raise ex
        return result

    return new_func


def parallel_generator(generator):
    """Decorator for broadcasting yields from master to slaves using MPI.

    Disable by passing parallel=False to the function.  For a method,
    you can also disable the parallel behavior by giving the instance
    a self.serial = True.
    """

    @functools.wraps(generator)
    def new_generator(*args, **kwargs):
        parallel = kwargs.pop('parallel', True)
        if (
            world.size == 1
            or (args and getattr(args[0], 'serial', False))
            or not parallel
        ):
            # Disable:
            for result in generator(*args, **kwargs):
                yield result
            return

        if world.rank == 0:
            try:
                for result in generator(*args, **kwargs):
                    broadcast((None, result))
                    yield result
            except Exception as ex:
                broadcast((ex, None))
                raise ex
            broadcast((None, None))
        else:
            ex2, result = broadcast((None, None))
            if ex2 is not None:
                raise ex2
            while result is not None:
                yield result
                ex2, result = broadcast((None, None))
                if ex2 is not None:
                    raise ex2

    return new_generator


def register_parallel_cleanup_function():
    """Call MPI_Abort if python crashes.

    This will terminate the processes on the other nodes."""

    if world.size == 1:
        return

    def cleanup(sys=sys, time=time, world=world):
        error = getattr(sys, 'last_type', None)
        if error:
            sys.stdout.flush()
            sys.stderr.write(
                (
                    'ASE CLEANUP (node %d): %s occurred.  '
                    + 'Calling MPI_Abort!\n'
                )
                % (world.rank, error)
            )
            sys.stderr.flush()
            # Give other nodes a moment to crash by themselves (perhaps
            # producing helpful error messages):
            time.sleep(3)
            world.abort(42)

    atexit.register(cleanup)


def distribute_cpus(size, comm):
    """Distribute cpus to tasks and calculators.

    Input:
    size: number of nodes per calculator
    comm: total communicator object

    Output:
    communicator for this rank, number of calculators, index for this rank
    """

    assert size <= comm.size
    assert comm.size % size == 0

    tasks_rank = comm.rank // size

    r0 = tasks_rank * size
    ranks = np.arange(r0, r0 + size)
    mycomm = comm.new_communicator(ranks)

    return mycomm, comm.size // size, tasks_rank


def myslice(ntotal, comm):
    """Return the slice of your tasks for ntotal jobs"""
    n = -(-ntotal // comm.size)  # ceil divide
    return slice(n * comm.rank, n * (comm.rank + 1))
