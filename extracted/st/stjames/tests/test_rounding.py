from stjames import Atom, BandStructure, Molecule, VibrationalMode


def test_vibrational_mode_rounding() -> None:
    test_vectors = [(1.23456789345346, 2.34567890346346, 3.45678901346346436), (4.567890126343636, 5.678901236346436, 6.7890123436436436)]
    mode = VibrationalMode(frequency=1.1234567, reduced_mass=1.1234567, force_constant=1.1234567, displacements=test_vectors)

    expected_vectors = [(1.234568, 2.345679, 3.456789), (4.567890, 5.678901, 6.789012)]
    assert mode.displacements == expected_vectors
    assert mode.frequency == 1.123
    assert mode.reduced_mass == 1.123
    assert mode.force_constant == 1.123


def test_band_structure_rounding() -> None:
    band_structure = BandStructure(
        kpoint_distances=[0.1234567890, 1.2345678901],
        eigenvalues=[[1.2345678901, 2.3456789012], [3.4567890123, 4.5678901234]],
        high_symmetry_points=[("Γ", 0.0), ("X", 1.2345678901)],
        total_density_of_states=[(1.2345678901, 2.3456789012)],
        band_gap=0.1234567890,
        valence_band_maximum=-0.1234567890,
        conduction_band_minimum=0.1234567890,
    )

    assert band_structure.kpoint_distances == [0.123457, 1.234568]
    assert band_structure.eigenvalues == [[1.234568, 2.345679], [3.456789, 4.56789]]
    assert band_structure.band_gap == 0.123457
    assert band_structure.valence_band_maximum == -0.123457
    assert band_structure.conduction_band_minimum == 0.123457
    assert band_structure.high_symmetry_points == [("Γ", 0.0), ("X", 1.234568)]
    assert band_structure.total_density_of_states == [(1.234568, 2.345679)]


def test_atom_rounding() -> None:
    atom = Atom(atomic_number=2, position=(0.1111111112222222, 1.1111111112222222, 2.1111111112222222))

    rounded_position = (0.11111111, 1.11111111, 2.11111111)

    assert atom.position == rounded_position


def test_molecule_rounding() -> None:
    mol = Molecule(
        charge=0,
        multiplicity=1,
        atoms=[Atom(atomic_number=2, position=(0.1111111112222222, 1.1111111112222222, 2.1111111112222222))],
        energy=1.23456789345346,
        zero_point_energy=2.34567890346346,
        thermal_energy_corr=3.45678901346346436,
        elapsed=4.567890126343636,
        thermal_enthalpy_corr=3.45678901346346436,
        thermal_free_energy_corr=3.45678901346346436,
        homo_lumo_gap=5.12345678,
        dipole=(1.23456789345346, 2.34567890346346, 3.45678901346346436),
        stress=(
            (1.23456789345346, 2.34567890346346, 3.45678901346346436),
            (4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (4.567890126343636, 5.678901236346436, 6.7890123436436436),
        ),
        elastic_tensor=(
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
            (1.23456789345346, 2.34567890346346, 3.45678901346346436, 4.567890126343636, 5.678901236346436, 6.7890123436436436),
        ),
    )

    assert mol.atoms[0].position == (0.11111111, 1.11111111, 2.11111111)
    assert mol.energy == 1.234568
    assert mol.zero_point_energy == 2.345679
    assert mol.thermal_energy_corr == 3.456789
    assert mol.elapsed == 4.568
    assert mol.thermal_enthalpy_corr == 3.456789
    assert mol.thermal_free_energy_corr == 3.456789
    assert mol.homo_lumo_gap == 5.123457
    assert mol.dipole == (1.234568, 2.345679, 3.456789)
    assert mol.stress == ((1.234568, 2.345679, 3.456789), (4.567890, 5.678901, 6.789012), (4.567890, 5.678901, 6.789012))
    assert mol.elastic_tensor == (
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
        (1.235, 2.346, 3.457, 4.568, 5.679, 6.789),
    )
