from itertools import combinations_with_replacement, product
import numpy as np
from ase import Atoms
from ase.units import GPa
from .structures import relax_structure


def get_elastic_stiffness_tensor(structure: Atoms,
                                 clamped: bool = False,
                                 epsilon: float = 1e-3,
                                 **kwargs) -> np.ndarray:
    """Calculate and return the elastic stiffness tensor in units of GPa for the
    given structure in `Voigt form <https://en.wikipedia.org/wiki/Voigt_notation>`_.

    Parameters
    ----------
    structure
        input structure; should be fully relaxed
    clamped
        if ``False`` (default) return the *relaxed* elastic stiffness tensor;
        if ``True`` return the *clamped ion* elastic stiffness tensor
    epsilon
        magnitude of the applied strain
    kwargs
        keyword arguments forwarded to the :func:`relax_structure
        <calorine.tools.relax_structure>` function used for relaxing the
        structure when computing the relaxed stiffness tensor; it should not be
        necessary to change the default for the vast majority of use cases; use
        with care

    Returns
    -------
    Stiffness tensor in units of GPa
    """

    # set up of deformations
    deformations = []
    for i, j in combinations_with_replacement(range(9), r=2):
        for s1, s2 in product([-1, 1], repeat=2):
            S = np.zeros((3, 3))
            S.flat[i] = s1
            S.flat[j] = s2
            deformations.append(S)
    deformations = np.array(deformations)
    deformations *= epsilon

    # compute strain energies
    reference_energy = structure.get_potential_energy()
    energies = []
    for S in deformations:
        cell = structure.get_cell()
        cell += cell @ S.T
        deformed_structure = structure.copy()
        deformed_structure.calc = structure.calc
        deformed_structure.set_cell(cell, scale_atoms=True)
        if not clamped:
            relax_structure(deformed_structure, constant_cell=True, **kwargs)
        energy = deformed_structure.get_potential_energy()
        energies.append(energy - reference_energy)
    energies = np.array(energies)

    # extract stiffness tensor (full rank)
    SS = np.einsum('nij,nkl->nijkl', deformations, deformations)
    M = SS.reshape(len(SS), -1)
    M *= 0.5
    C, *_ = np.linalg.lstsq(M, energies, rcond=None)
    C = C.reshape(3, 3, 3, 3)
    C /= (structure.cell.volume * GPa)

    # convert stiffness tensor to Voigt form
    voigts = np.array([1, 1, 2, 2, 3, 3, 2, 3, 3, 1, 1, 2]).reshape(-1, 2) - 1
    Cv = np.zeros((6, 6))
    for i, j in product(range(6), repeat=2):
        v1 = voigts[i]
        v2 = voigts[j]
        Cv[i, j] = C[(*v1, *v2)]

    return Cv
