import sys


if sys.version_info < (3, 8):
    from importlib_metadata import distribution
else:
    from importlib.metadata import distribution


def _find_pex3_entrypoint():
    pex_dist = distribution("pex")
    for entrypoint in pex_dist.entry_points:
        if entrypoint.name == "pex3":
            return entrypoint
    msg = "Unable to find entrypoint for `pex3`"
    raise ValueError(msg)


if __name__ == "__main__":
    pex3 = _find_pex3_entrypoint()
    pex3_cli = pex3.load()
    sys.exit(pex3_cli())
