from os.path import exists
from os.path import join as join_path
from typing import Any, Iterable, NamedTuple, TextIO
from warnings import warn

import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.stress import voigt_6_to_full_3x3_stress
from pandas import DataFrame


def read_loss(filename: str) -> DataFrame:
    """Parses a file in `loss.out` format from GPUMD and returns the
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
    elif len(data[0]) == 14:
        tags = 'total_loss L1 L2'
        tags += ' RMSE_E_train RMSE_F_train RMSE_V_train RMSE_Q_train RMSE_Z_train'
        tags += ' RMSE_E_test RMSE_F_test RMSE_V_test RMSE_Q_test RMSE_Z_test'
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


def write_structures(outfile: str, structures: list[Atoms]) -> None:
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


def read_nepfile(filename: str) -> dict[str, Any]:
    """Returns the content of a configuration file (`nep.in`) as a dictionary.

    Parameters
    ----------
    filename
        input file name
    """
    int_vals = ['version', 'neuron', 'generation', 'batch', 'population',
                'mode', 'model_type', 'charge_mode']
    float_vals = ['lambda_1', 'lambda_2', 'lambda_e', 'lambda_f', 'lambda_v',
                  'lambda_q', 'lambda_shear', 'force_delta']
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
        if key in int_vals:
            settings[key] = int(val)
        elif key in float_vals:
            settings[key] = float(val)
        elif key in ['cutoff', 'n_max', 'l_max', 'basis_size', 'zbl', 'type_weight']:
            settings[key] = [float(v) for v in val.split()]
        elif key == 'type':
            types = val.split()
            types[0] = int(types[0])
            settings[key] = types
    return settings


def read_structures(dirname: str) -> tuple[list[Atoms], list[Atoms]]:
    """Parses the output files with training and test data from a nep run and returns their
    content as two lists of structures, representing training and test data, respectively.
    Target and predicted data are included in the :attr:`info` dict of the :class:`Atoms`
    objects.

    Parameters
    ----------
    dirname
        Directory from which to read output files.

    """
    path = join_path(dirname)
    if not exists(path):
        raise FileNotFoundError(f'Directory {path} does not exist')

    # fetch model type from nep input file
    nep_info = read_nepfile(f'{path}/nep.in')
    model_type = nep_info.get('model_type', 0)

    # set up which files to parse, what dimensions to expect etc
    # depending on the type of model that is parsed
    if model_type == 0:
        charge_mode = int(nep_info.get('charge_mode', 0))
        if charge_mode not in [0, 1, 2]:
            raise ValueError(f'Unknown charge_mode: {charge_mode}')
        # files to parse: (sname, size, mandatory, includes_target, per_atom)
        files_to_parse = [
            ('energy', 1, True, True, False),
            ('force', 3, True, True, True),
            ('virial', 6, True, True, False),
            ('stress', 6, True, True, False),
        ]
        if charge_mode in [1, 2]:
            # files to parse: (sname, size, includes_target, per_atom)
            files_to_parse += [
                ('charge', 1, True, False, True),
                ('bec', 9, False, True, True),
            ]
    elif model_type == 1:
        # files to parse: (sname, size, includes_target, per_atom)
        files_to_parse = [('dipole', 3, True, True, False)]
    elif model_type == 2:
        # files to parse: (sname, size, includes_target, per_atom)
        files_to_parse = [('polarizability', 6, True, True, False)]
    else:
        raise ValueError(f'Unknown model_type: {model_type}')

    # read training and test data
    structures = {}
    for stype in ['train', 'test']:
        filename = join_path(dirname, f'{stype}.xyz')
        try:
            structures[stype] = read(filename, format='extxyz', index=':')
        except FileNotFoundError:
            warn(f'File {filename} not found.')
            structures[stype] = []
            continue

        n_structures = len(structures[stype])

        # loop over files from which to read target data and predictions
        for sname, size, mandatory, includes_target, per_atom in files_to_parse:
            infile = f'{sname}_{stype}.out'
            path = join_path(dirname, infile)
            if not exists(path):
                if mandatory:
                    raise FileNotFoundError(f'File {path} does not exist')
                else:
                    continue
            ts, ps = _read_data_file(path, includes_target=includes_target)

            if ts is not None:
                if ts.shape[1] != size:
                    raise ValueError(f'Target data in {infile} has unexpected shape:'
                                     f' {ts.shape}  (expected: (-1, {size}))')
            if ps.shape[1] != size:
                raise ValueError(f'Predicted data in {infile} has unexpected shape:'
                                 f' {ps.shape}  (expected: (-1, {size}))')

            if per_atom:
                # data per-atom, e.g., forces, per-atom-virials, Born effective charges ...
                n_atoms_total = sum([len(s) for s in structures[stype]])
                if len(ps) != n_atoms_total:
                    raise ValueError(f'Number of atoms in {infile} ({len(ps)})'
                                     f' and {stype}.xyz ({n_atoms_total}) inconsistent.')
                n = 0
                for structure in structures[stype]:
                    nat = len(structure)
                    if ts is not None:
                        structure.info[f'{sname}_target'] = \
                            np.array(ts[n: n + nat]).reshape(nat, size)
                    structure.info[f'{sname}_predicted'] = \
                        np.array(ps[n: n + nat]).reshape(nat, size)
                    n += nat
            else:
                # data per structure, e.g., energy, virials, stress
                if len(ps) != n_structures:
                    raise ValueError(f'Number of structures in {infile} ({len(ps)})'
                                     f' and {stype}.xyz ({n_structures}) inconsistent.')
                for k, structure in enumerate(structures[stype]):
                    assert ts is not None, 'This should not occur. Please report.'
                    t = ts[k]
                    assert np.shape(t) == (size,)
                    structure.info[f'{sname}_target'] = t
                    p = ps[k]
                    assert np.shape(p) == (size,)
                    structure.info[f'{sname}_predicted'] = p

        # special handling of target data for BECs
        # The target data for BECs need not be complete. In this case nep writes
        # zeros for every component (not optimal). If we encounter such a case we set
        # all components to nan instead in order to be able to quickly filter for
        # this case when analyzing data.
        for s in structures[stype]:
            if 'bec_target' in s.info and np.allclose(s.info['bec_target'], 0):
                nat = len(s)
                size = 9
                s.info['bec_target'] = np.array(size * nat * [np.nan]).reshape(nat, size)

    return structures['train'], structures['test']


def _read_data_file(
    path: str,
    includes_target: bool = True,
):
    """Private function that parses *.out files and
    returns their content for further processing.
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    target, predicted = [], []
    for line in lines:
        flds = line.split()
        if includes_target:
            if len(flds) % 2 != 0:
                raise ValueError(f'Incorrect number of columns in {path} ({len(flds)}).')
            n = len(flds) // 2
            predicted.append([float(s) for s in flds[:n]])
            target.append([float(s) for s in flds[n:]])
        else:
            predicted.append([float(s) for s in flds])
            target = None
    if target is not None:
        target = np.array(target)
    predicted = np.array(predicted)
    return target, predicted


def get_parity_data(
    structures: list[Atoms],
    property: str,
    selection: list[str] = None,
    flatten: bool = True,
) -> DataFrame:
    """Returns the predicted and target energies, forces, virials or stresses
    from a list of structures in a format suitable for generating parity plots.

    The structures should  have been read using :func:`read_structures
    <calorine.nep.read_structures>`, such that the `info` object is
    populated with keys of the form `<property>_<type>` where `<property>`
    is, e.g., `energy` or `force` and `<type>` is one of `predicted` or `target`.

    The resulting parity data is returned as a tuple of dicts, where each entry
    corresponds to a list.

    Parameters
    ----------
    structures
        List of structures as read with :func:`read_structures <calorine.nep.read_structures>`.
    property
        One of `energy`, `force`, `virial`, `stress`, `bec`, `dipole`, or `polarizability`.
    selection
        A list containing which components to return, and/or the norm.
        Possible values are `x`, `y`, `z`, `xx`, `yy`,
        `zz`, `yz`, `xz`, `xy`, `norm`, `pressure`.
    flatten
        if True return flattened lists; this is useful for flattening
        the components of force or virials into a simple list
    """
    voigt_mapping = {
        'x': 0, 'y': 1, 'z': 2, 'xx': 0, 'yy': 1, 'zz': 2,  'yz': 3, 'xz': 4, 'xy': 5,
    }
    if property not in ('energy', 'force', 'virial', 'stress', 'polarizability', 'dipole', 'bec'):
        raise ValueError(
            "`property` must be one of 'energy', 'force', 'virial', 'stress',"
            " 'polarizability', 'dipole', or 'bec'."
        )
    if property in ['energy'] and selection:
        raise ValueError('Selection cannot be applied to scalars.')
    if property != 'stress' and selection and 'pressure' in selection:
        raise ValueError(f'Cannot calculate pressure for `{property}`.')

    data = {'predicted': [], 'target': []}
    if property in ['force', 'bec'] and flatten:
        size = 3 if property == 'force' else 9
        data['species'] = []
    for structure in structures:
        if 'species' in data:
            data['species'].extend(np.repeat(structure.symbols, size).tolist())
        for stype in ['predicted', 'target']:
            property_with_stype = f'{property}_{stype}'
            if property_with_stype not in structure.info.keys():
                raise KeyError(f'{property_with_stype} not available in info field of structure')
            extracted_property = np.array(structure.info[property_with_stype])

            if selection is None or len(selection) == 0:
                data[stype].append(extracted_property)
                continue

            selected_values = []
            for select in selection:
                if property in ['force', 'bec']:
                    # flip to get (n_components, n_structures)
                    extracted_property = extracted_property.T
                if select == 'norm':
                    if property == 'force':
                        selected_values.append(np.linalg.norm(extracted_property, axis=0))
                    elif property in ['virial', 'stress']:
                        full_tensor = voigt_6_to_full_3x3_stress(extracted_property)
                        selected_values.append(np.linalg.norm(full_tensor))
                    elif property in ['dipole']:
                        selected_values.append(np.linalg.norm(extracted_property))
                    else:
                        raise ValueError(
                            f'Cannot handle selection=`norm` with property=`{property}`.')
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
        for stype in ['target', 'predicted']:
            value = data[stype]
            if len(np.shape(value[0])) > 0:
                data[stype] = np.concatenate(value).ravel().tolist()
        if property in ['force']:
            n = len(data['target']) // 3
            data['component'] = ['x', 'y', 'z'] * n
        elif property in ['virial', 'stress']:
            n = len(data['target']) // 6
            data['component'] = ['xx', 'yy', 'zz', 'yz', 'xz', 'xy'] * n
        elif property in ['bec']:
            n = len(data['target']) // 9
            data['component'] = ['xx', 'xy', 'xz', 'yx', 'yy', 'yz', 'zx', 'zy', 'zz'] * n
    df = DataFrame(data)
    # In case of flatten, cast to float64 for compatibility
    # with e.g. seaborn.
    # Casting in this way breaks tensorial properties though,
    # so skip it there.
    if flatten:
        df['target'] = df.target.astype('float64')
        df['predicted'] = df.predicted.astype('float64')
    return df
