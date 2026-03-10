"""Converters for importing training data from external ML potential formats.

The OCP/fairchem converter requires the ``lmdb`` Python package at runtime::

    pip install lmdb
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ferrox.lmdb import TrainingFrame


def convert_ocp_lmdb(
    src_path: str,
    dst_path: str,
    codec: str = "rkyv",
) -> int:
    """Convert an OCP/fairchem LMDB dataset to native ferrox LMDB format.

    OCP LMDB files store pickle-serialized ``torch_geometric.data.Data`` objects
    (or plain dicts) with keys like ``atomic_numbers``, ``pos``, ``cell``,
    ``y``/``energy``, ``force``, ``stress``, ``natoms``, and ``tags``.

    This function reads those entries, extracts the relevant fields, and writes
    them as ``TrainingFrame`` objects into a new ferrox LMDB dataset.

    Args:
        src_path: Path to the source OCP LMDB file/directory.
        dst_path: Path for the new ferrox LMDB dataset directory.
        codec: Serialization codec for the output ("rkyv" or "json").

    Returns:
        Number of frames converted.

    Raises:
        ImportError: If the ``lmdb`` Python package is not installed.
    """
    try:
        import lmdb as lmdb_py
    except ImportError as exc:
        raise ImportError(
            "The 'lmdb' Python package is required for OCP conversion. "
            "Install it with: pip install lmdb"
        ) from exc

    import pickle

    from ferrox.lmdb import LmdbDataset

    src_env = lmdb_py.open(
        src_path, readonly=True, lock=False, subdir=os.path.isdir(src_path)
    )
    try:
        dataset = LmdbDataset.create(dst_path, codec=codec)

        batch: list[TrainingFrame] = []
        batch_size = 1000

        with src_env.begin() as txn:
            # Collect numeric keys and sort to preserve original OCP index order
            # (LMDB cursor iterates in lexicographic byte order, so "10" < "2")
            numeric_keys: list[int] = []
            cursor = txn.cursor()
            for key, _value in cursor:
                key_str = key.decode("ascii", errors="ignore")
                try:
                    numeric_keys.append(int(key_str))
                except ValueError:
                    continue
            numeric_keys.sort()

            for ocp_idx in numeric_keys:
                value = txn.get(str(ocp_idx).encode())
                if value is None:
                    continue

                try:
                    data = pickle.loads(value)  # noqa: S301
                except (
                    pickle.UnpicklingError,
                    EOFError,
                    ModuleNotFoundError,
                    KeyError,
                ):
                    continue

                frame = _ocp_data_to_frame(data)
                if frame is not None:
                    batch.append(frame)

                if len(batch) >= batch_size:
                    dataset.extend(batch)
                    batch.clear()

        if batch:
            dataset.extend(batch)
    finally:
        src_env.close()

    return len(dataset)


def _ocp_data_to_frame(data: object) -> TrainingFrame | None:
    """Extract a TrainingFrame from an OCP Data object or dict."""
    import numpy as np

    from ferrox.lmdb import TrainingFrame

    def _get(obj: object, *keys: str) -> object:  # type: ignore[return-type]
        """Get first non-None attribute or dict value from keys."""
        for key in keys:
            val = obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)  # type: ignore[union-attr]
            if val is not None:
                return val
        return None

    def _to_list(val: object) -> list | None:  # type: ignore[return-type]
        """Convert numpy/torch arrays to plain Python lists."""
        if val is None:
            return None
        if hasattr(val, "detach"):
            val = val.detach().cpu().numpy()  # type: ignore[union-attr]
        if hasattr(val, "tolist"):
            return val.tolist()  # type: ignore[union-attr]
        try:
            return list(val)  # type: ignore[call-overload]
        except TypeError:
            return None

    atomic_numbers_raw = _get(data, "atomic_numbers", "z")
    if atomic_numbers_raw is None:
        return None

    positions_raw = _get(data, "pos", "positions")
    if positions_raw is None:
        return None

    atomic_numbers = _to_list(atomic_numbers_raw)
    positions_flat = _to_list(positions_raw)

    if positions_flat is None or atomic_numbers is None:
        return None

    n_atoms = len(atomic_numbers)
    if n_atoms == 0:
        return None
    if len(positions_flat) == n_atoms and isinstance(positions_flat[0], (list, tuple)):
        positions = [list(pos) for pos in positions_flat]
    elif len(positions_flat) == n_atoms * 3:
        positions = [positions_flat[idx * 3 : idx * 3 + 3] for idx in range(n_atoms)]
    else:
        return None
    if any(len(pos) != 3 for pos in positions):
        return None

    cell_raw = _get(data, "cell")
    cell = None
    if cell_raw is not None:
        cell_list = _to_list(cell_raw)
        if cell_list is not None:
            flat = np.array(cell_list, dtype=float).flatten()
            if len(flat) == 9:
                cell = [flat[0:3].tolist(), flat[3:6].tolist(), flat[6:9].tolist()]

    energy = None
    for energy_key in ("y", "energy", "y_relaxed"):
        energy_raw = _get(data, energy_key)
        if energy_raw is None:
            continue
        try:
            val = _to_list(energy_raw) if hasattr(energy_raw, "__len__") else energy_raw
            if val is None:
                continue
            if isinstance(val, list):
                if not val:
                    continue
                energy = float(val[0])
            else:
                energy = float(val)  # type: ignore[arg-type]
        except (ValueError, TypeError):
            continue
        break

    forces_raw = _get(data, "force", "forces")
    forces = None
    if forces_raw is not None:
        forces_list = _to_list(forces_raw)
        if forces_list is not None:
            if len(forces_list) == n_atoms and isinstance(
                forces_list[0], (list, tuple)
            ):
                if all(len(force) == 3 for force in forces_list):
                    forces = [list(force) for force in forces_list]
            elif len(forces_list) == n_atoms * 3:
                forces = [forces_list[idx * 3 : idx * 3 + 3] for idx in range(n_atoms)]

    stress_raw = _get(data, "stress")
    stress = None
    if stress_raw is not None:
        stress_list = _to_list(stress_raw)
        if stress_list is not None:
            flat = np.array(stress_list, dtype=float).flatten()
            if len(flat) == 6:
                stress = flat.tolist()
            elif len(flat) == 9:
                # Full 3x3 -> Voigt: xx, yy, zz, yz, xz, xy
                # Average off-diagonals for robustness with non-symmetric tensors
                stress = [
                    flat[0],
                    flat[4],
                    flat[8],
                    (flat[5] + flat[7]) / 2,
                    (flat[2] + flat[6]) / 2,
                    (flat[1] + flat[3]) / 2,
                ]

    pbc = [cell is not None] * 3
    pbc_raw = _get(data, "pbc")
    if pbc_raw is not None:
        pbc_list = _to_list(pbc_raw)
        if pbc_list and len(pbc_list) == 3:
            pbc = [bool(p) for p in pbc_list]

    return TrainingFrame(
        atomic_numbers=[int(z) for z in atomic_numbers],
        positions=positions,
        cell=cell,
        pbc=pbc,
        energy=energy,
        forces=forces,
        stress=stress,
    )
