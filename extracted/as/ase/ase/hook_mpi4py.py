def ASE_PARALLEL_WORLD_HOOK():
    from ase.parallel import MPI4PY

    return MPI4PY()
