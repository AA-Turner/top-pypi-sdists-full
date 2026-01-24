import multiprocessing as mp
import numpy as np
import pytest

from ase import Atoms
from ase.calculators.lj import LennardJones
from ase.db import connect


# Global handle that will be shared (via fork) with subprocesses
DB = None  # Will be set inside the test function before spawning processes
# Snapshot of existing ids (may be non-contiguous due to prior deletions):
ID_LIST = []


def _worker(seed: int, n_reads: int, id_list):
    """Worker that performs random reads and computes LJ energies.

    Parameters
    ----------
    seed : int
            Seed to make the random access order deterministic per process.
    n_reads : int
            Number of random molecules to sample.
    n_mols : int
            Total number of molecules in the database (id space is 1..n_mols).
    """
    # global DB
    assert DB is not None, "Global DB handle not set in worker"

    rng = np.random.default_rng(seed)
    avg_energy = 0.0
    n_ids = len(id_list)
    for i in range(n_reads):
        # Pick a random valid existing id (ids may not be contiguous)
        idx = id_list[int(rng.integers(0, n_ids))]
        atoms = DB.get_atoms(idx)
        # Reconstruct Atoms object: ensure a Calculator is (re)attached
        atoms.calc = LennardJones()
        e = atoms.get_potential_energy()
        # Online mean update to avoid storing all energies
        avg_energy += (e - avg_energy) / (i + 1)
        # Basic sanity checks
        assert np.isfinite(e)
        assert len(atoms) > 0
    return avg_energy


def test_aselmdb_concurrent_random_reads(get_db_name):
    """Create 4096 random Ar clusters and read them concurrently.

    The LMDB database handle is created once and then shared across 8 forked
    subprocesses which perform random read access with deterministic seeds
    while reconstructing full Atoms objects and computing Lennard-Jones
    potential energies.
    """

    # This test is only meaningful on platforms that support 'fork'.
    if mp.get_start_method(allow_none=True) not in (None, "fork"):
        pytest.skip(
            "Requires 'fork' start method to share handle via copy-on-write")

    name = get_db_name('aselmdb')  # ensures a clean LMDB database file

    n_mols = 4096
    max_atoms = 10  # per random cluster

    # Populate the database with random Ar clusters ("molecules").
    # Use a context manager for fewer transaction commits.
    with connect(name) as c:
        rng = np.random.default_rng(20251008)
        for _ in range(n_mols):
            n = int(rng.integers(2, max_atoms + 1))
            positions = rng.random((n, 3)) * 5.0  # spread out atoms
            atoms = Atoms('Ar' * n, positions=positions)
            c.write(atoms)

    # Open a (read-only) handle we'll share with subprocesses via fork.
    global DB, ID_LIST
    DB = connect(name, readonly=True)
    ID_LIST = list(DB.ids)

    n_proc = 8
    reads_per_proc = 256
    seeds = [123456 + i for i in range(n_proc)]

    # This will very likely segmentation fault if we are not
    # reinitializing lmdb
    # environment correctly in the subprocesses.
    with mp.Pool(processes=n_proc) as pool:
        _ = pool.starmap(
            _worker, [(s, reads_per_proc, ID_LIST) for s in seeds])
