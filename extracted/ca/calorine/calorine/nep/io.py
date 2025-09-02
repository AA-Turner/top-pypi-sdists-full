from os.path import exists
from os.path import join as join_path
from typing import Any, Dict, Iterable, List, NamedTuple, TextIO, Tuple
from warnings import warn

import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.stress import voigt_6_to_full_3x3_stress
from ase.units import GPa
from pandas import DataFrame


def read_loss(filename: str) -> DataFrame:
    """Parses a file in ``loss.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/nep/output_files/loss_out.html>`__.

    Parameters
    ----------
    filename
        input file name

    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in loss.out, append a dimension
        data = data.reshape(1, -1)
    if len(data[0]) == 6:
        tags = 'total_loss L1 L2'
        tags += ' RMSE_P_train'
        tags += ' RMSE_P_test'
    elif len(data[0]) == 10:
        tags = 'total_loss L1 L2'
        tags += ' RMSE_E_train RMSE_F_train RMSE_V_train'
        tags += ' RMSE_E_test RMSE_F_test RMSE_V_test'
    else:
        raise ValueError(
            f'Input file contains {len(data[0])} data columns. Expected 6 or 10 columns.'
        )
    generations = range(100, len(data) * 100 + 1, 100)
    df = DataFrame(data=data[:, 1:], columns=tags.split(), index=generations)
    return df


def _write_structure_in_nep_format(structure: Atoms, f: TextIO) -> None:
    """Write structure block into a file-like object in format readable by nep executable.

    Parameters
    ----------
    structure
        input structure; must hold information regarding energy and forces
    f
        file-like object to which to write
    """

    # Allowed keyword=value pairs. Use ASEs extyz write functionality.:
    #   lattice="ax ay az bx by bz cx cy cz"                    (mandatory)
    #   energy=energy_value                                     (mandatory)
    #   virial="vxx vxy vxz vyx vyy vyz vzx vzy vzz"            (optional)
    #   weight=relative_weight                                  (optional)
    #   properties=property_name:data_type:number_of_columns
    #       species:S:1                      (mandatory)
    #       pos:R:3                          (mandatory)
    #       force:R:3 or forces:R:3          (mandatory)
    try:
        structure.get_potential_energy()
        structure.get_forces()  # calculate forces to have them on the Atoms object
    except RuntimeError:
        raise RuntimeError('Failed to retrieve energy and/or forces for structure')
    if np.isclose(structure.get_volume(), 0):
        raise ValueError('Structure cell must have a non-zero volume!')
    try:
        structure.get_stress()
    except RuntimeError:
        warn('Failed to retrieve stresses for structure')
    write(filename=f, images=structure, write_info=True, format='extxyz')


def write_structures(outfile: str, structures: List[Atoms]) -> None:
    """Writes structures for training/testing in format readable by nep executable.

    Parameters
    ----------
    outfile
        output filename
    structures
        list of structures with energy, forces, and (possibly) stresses
    """
    with open(outfile, 'w') as f:
        for structure in structures:
            _write_structure_in_nep_format(structure, f)


def write_nepfile(parameters: NamedTuple, dirname: str) -> None:
    """Writes parameters file for NEP construction.

    Parameters
    ----------
    parameters
        input parameters; see `here <https://gpumd.org/nep/input_parameters/index.html>`__
    dirname
        directory in which to place input file and links
    """
    with open(join_path(dirname, 'nep.in'), 'w') as f:
        for key, val in parameters.items():
            f.write(f'{key}  ')
            if isinstance(val, Iterable):
                f.write(' '.join([f'{v}' for v in val]))
            else:
                f.write(f'{val}')
            f.write('\n')


def read_nepfile(filename: str) -> Dict[str, Any]:
    """Returns the content of a configuration file (`nep.in`) as a dictionary.

    Parameters
    ----------
    filename
        input file name
    """
    settings = {}
    with open(filename) as f:
        for line in f.readlines():
            # remove comments - throw away everything after a '#'
            cleaned = line.split('#', 1)[0].strip()
            flds = cleaned.split()
            if len(flds) == 0:
                continue
            settings[flds[0]] = ' '.join(flds[1:])
    for key, val in settings.items():
        if key in ['version', 'neuron', 'generation', 'batch', 'population', 'mode', 'model_type']:
            settings[key] = int(val)
        elif key in [
            'lambda_1',
            'lambda_2',
            'lambda_e',
            'lambda_f',
            'lambda_v',
            'lambda_shear',
            'force_delta',
        ]:
            settings[key] = float(val)
        elif key in ['cutoff', 'n_max', 'l_max', 'basis_size', 'zbl', 'type_weight']:
            settings[key] = [float(v) for v in val.split()]
        elif key == 'type':
            types = val.split()
            types[0] = int(types[0])
            settings[key] = types
    return settings


def read_structures(dirname: str) -> Tuple[List[Atoms], List[Atoms]]:
    """Parses the ``energy_*.out``, ``force_*.out``, ``virial_*.out``,
    ``polarizability_*.out`` and ``dipole_*.out`` files from a nep run and
    returns their content as lists. The first and second list contain the structures
    from the training and test sets, respectively. Each list entry corresponds to an ASE
    Atoms object, which in turn contains predicted and target energies, forces and virials/stresses
    or polarizability/diople stored in the `info` property.

    Parameters
    ----------
    dirname
        directory from which to read output files

    """
    path = join_path(dirname)
    if not exists(path):
        raise ValueError(f'Directory {path} does not exist')
    nep_info = read_nepfile(f'{path}/nep.in')
    if 'mode' in nep_info or 'model_type' in nep_info:
        ftype = nep_info.get('mode', nep_info.get('model_type'))
        if ftype == 2 or ftype == 1:
            return _read_structures_tensors(dirname, ftype)
    return _read_structures_potential(dirname)


def _read_structures_tensors(dirname: str, ftype: int) \
        -> Tuple[List[Atoms], List[Atoms]]:
    """Parses the ``polarizability_*.out`` and ``dipole_*.out``
    files from a nep run and returns their content as lists.
    The first and second list contain the structures from the training and
    test sets, respectively. Each list entry corresponds to an ASE
    Atoms object, which in turn contains predicted and target
    dipole or polarizability stored in the `info`
    property.

    Parameters
    ----------
    dirname
        directory from which to read output files

    """
    path = join_path(dirname)
    structures = {}

    if ftype == 1:
        sname = 'dipole'
    else:
        sname = 'polarizability'

    for stype in ['train', 'test']:
        filename = join_path(dirname, f'{stype}.xyz')
        try:
            structures[stype] = read(filename, format='extxyz', index=':')
        except FileNotFoundError:
            warn(f'File {filename} not found.')
            structures[stype] = []
            continue

        n_structures = len(structures[stype])
        ts, ps = _read_data_file(path, f'{sname}_{stype}.out')
        if ftype == 1:
            ts = np.array(ts).reshape((-1, 3))
            ps = np.array(ps).reshape((-1, 3))
        else:
            ts = np.array(ts).reshape((-1, 6))
            ps = np.array(ps).reshape((-1, 6))
        assert len(ts) == n_structures, \
            f'Number of structures in {sname}_{stype}.out ({len(ts)})' \
            f' and {stype}.xyz ({n_structures}) inconsistent'
        for structure, t, p in zip(structures[stype], ts, ps):
            if ftype == 1:
                assert np.shape(t) == (3,)
                assert np.shape(p) == (3,)
            else:
                assert np.shape(t) == (6,)
                assert np.shape(p) == (6,)
            structure.info[f'{sname}_target'] = t
            structure.info[f'{sname}_predicted'] = p

    return structures['train'], structures['test']


def _read_structures_potential(dirname: str) -> Tuple[List[Atoms], List[Atoms]]:
    """Parses the ``energy_*.out``, ``force_*.out``, ``virial_*.out``
    files from a nep run and returns their content as lists.
    The first and second list contain the structures from the training and
    test sets, respectively. Each list entry corresponds to an ASE
    Atoms object, which in turn contains predicted and target
    energies, forces and virials/stresses stored in the `info`
    property.

    Parameters
    ----------
    dirname
        directory from which to read output files

    """
    path = join_path(dirname)
    structures = {}

    for stype in ['train', 'test']:
        file_path = join_path(dirname, f'{stype}.xyz')
        if not exists(file_path):
            warn(f'File {file_path} not found.')
            structures[stype] = []
            continue

        structures[stype] = read(
            file_path, format='extxyz', index=':'
        )

        ts, ps = _read_data_file(path, f'energy_{stype}.out')
        n_structures = len(structures[stype])
        assert len(ts) == n_structures, (
            f'Number of structures in energy_{stype}.out ({len(ts)})'
            f' and {stype}.xyz ({n_structures}) inconsistent'
        )
        for structure, t, p in zip(structures[stype], ts, ps):
            structure.info['energy_target'] = t
            structure.info['energy_predicted'] = p

        ts, ps = _read_data_file(path, f'force_{stype}.out')
        n_atoms_total = sum([len(s) for s in structures[stype]])
        assert len(ts) == n_atoms_total, (
            f'Number of structures in force_{stype}.out ({len(ts)})'
            f' and {stype}.xyz ({n_structures}) inconsistent'
        )
        n = 0
        for structure in structures[stype]:
            nat = len(structure)
            structure.info['force_target'] = np.array(ts[n: n + nat]).reshape(nat, 3)
            structure.info['force_predicted'] = np.array(ps[n: n + nat]).reshape(
                nat, 3
            )
            n += nat

        ts, ps = _read_data_file(path, f'virial_{stype}.out')
        ts, ps = np.array(ts), np.array(ps)
        N = len(structures[stype])
        if ts.shape == (6*N,):
            # GPUMD <=v3.6 style virial_*.out
            # First column are NEP predictions, second are targets
            # Order: First N values are xx, second are yy etc.
            ts = np.array(ts).reshape((6, -1)).T  # GPUMD 3.6 compatibility
            ps = np.array(ps).reshape((6, -1)).T
        elif ts.shape == (N, 6):
            # GPUMD >=v3.7 style virial_*.out
            # First 6 columns are NEP predictions, last 6 are targets
            # Order: xx, yy, zz, xy, yz, zx
            pass
        else:
            raise ValueError(f'virial_*.out has invalid shape, {ts.shape}')

        assert len(ts) == n_structures, \
            f'Number of structures in virial_{stype}.out ({len(ts)})' \
            f' and {stype}.xyz ({n_structures}) inconsistent'
        for structure, t, p in zip(structures[stype], ts, ps):
            assert np.shape(t) == (6,)
            structure.info['virial_target'] = t
            structure.info['virial_predicted'] = p
            conv = len(structure) / structure.get_volume() / GPa
            structure.info['stress_target'] = t * conv
            structure.info['stress_predicted'] = p * conv

    return structures['train'], structures['test']


def _read_data_file(dirname: str, fname: str):
    """Private function that parses energy/force/virial_*.out files and
    returns their content for further processing.
    """
    path = join_path(dirname, fname)
    if not exists(path):
        raise ValueError(f'Directory {path} does not exist')
    with open(path, 'r') as f:
        lines = f.readlines()
    target, predicted = [], []
    for line in lines:
        flds = line.split()
        if len(flds) == 12:  # Virial after GPUMD 3.7
            predicted.append([float(s) for s in flds[0:6]])
            target.append([float(s) for s in flds[6:12]])
        elif len(flds) == 6:  # Force
            predicted.append([float(s) for s in flds[0:3]])
            target.append([float(s) for s in flds[3:6]])
        elif len(flds) == 2:  # Energy, virial before GPUMD 3.7
            predicted.append(float(flds[0]))
            target.append(float(flds[1]))
        else:
            raise ValueError(f'Malformed file: {path}')
    return target, predicted


def get_parity_data(
    structures: List[Atoms],
    property: str,
    selection: List[str] = None,
    flatten: bool = True,
) -> DataFrame:
    """Returns the predicted and target energies, forces, virials or stresses
    from a list of structures in a format suitable for generating parity plots.

    The structures should  have been read using :func:`read_structures
    <calorine.nep.read_structures>`, such that the ``info``-object is
    populated with keys on the form ``<property>_<type>`` where ``<property>``
    is one of ``energy``, ``force``, ``virial``, and stress, and ``<type>`` is one
    of ``predicted`` or ``target``.

    The resulting parity data is returned as a tuple of dicts, where each entry
    corresponds to a list.

    Parameters
    ----------
    structures
        List of structures as read with :func:`read_structures <calorine.nep.read_structures>`.
    property
        One of ``energy``, ``force``, ``virial``, ``stress``, ``polarizability``, ``dipole``.
    selection
        A list containing which components to return, and/or the absolute value.
        Possible values are ``x``, ``y``, ``z``, ``xx``, ``yy``,
        ``zz``, ``yz``, ``xz``, ``xy``, ``abs``, ``pressure``.
    flatten
        if True return flattened lists; this is useful for flattening
        the components of force or virials into a simple list
    """
    data = {'predicted': [], 'target': []}
    voigt_mapping = {
        'x': 0,
        'y': 1,
        'z': 2,
        'xx': 0,
        'yy': 1,
        'zz': 2,
        'yz': 3,
        'xz': 4,
        'xy': 5,
    }
    if property not in ('energy', 'force', 'virial', 'stress', 'polarizability', 'dipole'):
        raise ValueError(
            "`property` must be one of 'energy', 'force', 'virial', 'stress',"
            " 'polarizability', 'dipole'."
        )
    if property == 'energy' and selection:
        raise ValueError('Selection does nothing for scalar-valued `energy`.')
    if property != 'stress' and selection and 'pressure' in selection:
        raise ValueError(f'Cannot calculate pressure for `{property}`.')
    for structure in structures:
        for stype in data:
            property_with_stype = f'{property}_{stype}'
            if property_with_stype not in structure.info.keys():
                raise KeyError(f'{property_with_stype} does not exist in info object!')
            extracted_property = np.array(structure.info[property_with_stype])

            if selection is None or len(selection) == 0:
                data[stype].append(extracted_property)
                continue

            selected_values = []
            for select in selection:
                if property == 'force':
                    # flip to get (n_components, n_structures)
                    extracted_property = extracted_property.T
                if select == 'abs':
                    if property == 'force':
                        selected_values.append(np.linalg.norm(extracted_property, axis=0))
                    else:
                        # property can only be in ('virial', 'stress')
                        full_tensor = voigt_6_to_full_3x3_stress(extracted_property)
                        selected_values.append(np.linalg.norm(full_tensor))
                    continue

                if select == 'pressure' and property == 'stress':
                    total_stress = extracted_property
                    selected_values.append(-np.sum(total_stress[:3]) / 3)
                    continue

                if select not in voigt_mapping:
                    raise ValueError(f'Selection `{select}` is not allowed.')
                index = voigt_mapping[select]
                if index >= extracted_property.shape[0]:
                    raise ValueError(
                        f'Selection `{select}` is not compatible with property `{property}`.'
                    )
                selected_values.append(extracted_property[index])
            data[stype].append(selected_values)
    if flatten:
        for key, value in data.items():
            if len(np.shape(value[0])) > 0:
                data[key] = np.concatenate(value).ravel().tolist()
    df = DataFrame(data)
    # In case of flatten, cast to float64 for compatibility
    # with e.g. seaborn.
    # Casting in this way breaks tensorial properties though,
    # so skip it there.
    if flatten:
        df['target'] = df.target.astype('float64')
        df['predicted'] = df.predicted.astype('float64')
    return df
