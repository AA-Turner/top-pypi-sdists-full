"""Hydrogen-bond-basicity workflow."""

from ..base import Base
from ..types import UUID
from .workflow import MoleculeWorkflow


class HydrogenBondAcceptorSite(Base):
    """A hydrogen-bond-acceptor site.

    Attributes:
        atom_idx: index of the atom
        pkbhx: Hydrogen-bond basicity
        position: position of the atom
        name: name of the atom
    """

    atom_idx: int  # zero-indexed
    pkbhx: float
    position: tuple[float, float, float]
    name: str | None = None


class HydrogenBondDonorSite(Base):
    """A hydrogen-bond-donor site.

    Attributes:
        atom_idx: index of the atom
        pk_alpha: Hydrogen-bond acidity
        position: position of the atom
    """

    atom_idx: int  # zero-indexed
    pk_alpha: float
    position: tuple[float, float, float]


class HydrogenBondBasicityWorkflow(MoleculeWorkflow):
    """Workflow for calculating hydrogen-bond basicity and acidity.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)

        do_csearch: perform a conformational search when true
        do_optimization: perform an optimization when true

        optimization: UUID of optimization
        hba_sites: hydrogen-bond-acceptor sites
        hbd_sites: hydrogen-bond-donor sites
    """

    do_csearch: bool = True
    do_optimization: bool = True

    optimization: UUID | None = None
    hba_sites: list[HydrogenBondAcceptorSite] = []
    hbd_sites: list[HydrogenBondDonorSite] = []
