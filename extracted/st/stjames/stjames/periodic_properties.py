"""Data models for periodic system properties."""

from typing import Annotated

from pydantic import AfterValidator, BaseModel

from .base import round_float
from .types import round_list, round_list_of_float_pairs, round_list_of_lists, round_list_of_str_float_pairs


class BandStructure(BaseModel):
    """
    Electronic band structure for a periodic system.

    Eigenvalues are shifted so the Fermi level is at 0.

    :param kpoint_distances: cumulative distances along the k-path, in units of 2π/Å; length = n_kpoints
    :param eigenvalues: eigenvalues in Hartree (Fermi level = 0); shape (n_bands, n_kpoints)
    :param high_symmetry_points: high-symmetry k-point labels and their cumulative path distances in 2π/Å (e.g. [("Γ", 0.0), ("X", 1.23)])
    :param total_density_of_states: density of states from a separate uniform k-mesh; list of (energy in Hartree, k-weighted count) pairs (Fermi level = 0)
    :param band_gap: band gap in Hartree
    :param valence_band_maximum: valence band maximum in Hartree (Fermi level = 0)
    :param conduction_band_minimum: conduction band minimum in Hartree (Fermi level = 0)
    """

    kpoint_distances: Annotated[list[float], AfterValidator(round_list(6))]
    eigenvalues: Annotated[list[list[float]], AfterValidator(round_list_of_lists(6))]
    high_symmetry_points: Annotated[list[tuple[str, float]], AfterValidator(round_list_of_str_float_pairs(6))]
    total_density_of_states: Annotated[list[tuple[float, float]], AfterValidator(round_list_of_float_pairs(6))]
    band_gap: Annotated[float, AfterValidator(round_float(6))]
    valence_band_maximum: Annotated[float, AfterValidator(round_float(6))]
    conduction_band_minimum: Annotated[float, AfterValidator(round_float(6))]
