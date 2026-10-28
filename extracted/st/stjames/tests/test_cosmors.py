"""Test cosmors behavior and validation."""

from pytest import mark

from stjames import COSMORSParameterization, Molecule, Solvent

COSMORS: dict[str, float | str] = {
    "solvent": "water",
    "temperature": 298.15,
    "parameterization": "opencosmo_rs_24a",
    "e_diel": -0.02,
    "mu_res": 0.006,
    "mu_comb": 0.001,
    "g_disp": 0.001,
    "ring_correction": 0.0,
    "standard_state": 0.002,
    "eta": -0.001,
    "n_rings": 0,
    "gas_phase_energy": -76.4,
}


@mark.parametrize("parameterization", list(COSMORSParameterization))
def test_molecule_cosmors_round_trip(parameterization: COSMORSParameterization) -> None:
    """Merging COSMO-RS results into a Molecule, as condor's engine_result_to_stjames does."""
    water = Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")
    assert water.cosmo_rs_data is None

    mol = Molecule.model_validate(water.model_dump() | {"cosmo_rs_data": COSMORS | {"parameterization": parameterization.value}})
    assert mol.cosmo_rs_data is not None
    assert mol.cosmo_rs_data.solvation_free_energy == -0.011
    assert mol.cosmo_rs_data.solvent is Solvent.WATER
    assert mol.cosmo_rs_data.parameterization is parameterization

    dumped = mol.model_dump(mode="json")
    assert dumped["cosmo_rs_data"]["solvation_free_energy"] == -0.011
    assert Molecule.model_validate(dumped).cosmo_rs_data == mol.cosmo_rs_data
