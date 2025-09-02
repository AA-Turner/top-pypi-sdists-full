from warnings import warn
from collections.abc import Iterable
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
from ase import Atoms
from ase.io import read, write
from pandas import DataFrame


def read_kappa(filename: str) -> DataFrame:
    """Parses a file in ``kappa.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/kappa_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in kappa.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'kx_in kx_out ky_in ky_out kz_tot'.split()
    if len(data[0]) != len(tags):
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            f' Expected {len(tags)} columns.'
        )
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    return df


def read_msd(filename: str) -> DataFrame:
    """Parses a file in ``msd.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/msd_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in msd.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'time msd_x msd_y msd_z sdc_x sdc_y sdc_z'.split()
    if len(data[0]) != len(tags):
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            f' Expected {len(tags)} columns.'
        )
    df = DataFrame(data=data, columns=tags)
    return df


def read_hac(filename: str,
             exclude_currents: bool = True,
             exclude_in_out: bool = True) -> DataFrame:
    """Parses a file in ``hac.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/hac_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    exclude_currents
        Do not include currents in output to save memory.
    exclude_in_out
        Do not include `in` and `out` parts of conductivity in output to save memory.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in hac.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'time'
    tags += ' jin_jtot_x jout_jtot_x jin_jtot_y jout_jtot_y jtot_jtot_z'
    tags += ' kx_in kx_out ky_in ky_out kz_tot'
    tags = tags.split()
    if len(data[0]) != len(tags):
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            f' Expected {len(tags)} columns.'
        )
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    df['jjx_tot'] = df.jin_jtot_x + df.jout_jtot_x
    df['jjy_tot'] = df.jin_jtot_y + df.jout_jtot_y
    df['jjz_tot'] = df.jtot_jtot_z
    del df['jtot_jtot_z']
    if exclude_in_out:
        # remove columns with in/out data to save space
        for col in df:
            if 'in' in col or 'out' in col:
                del df[col]
    if exclude_currents:
        # remove columns with currents to save space
        for col in df:
            if col.startswith('j'):
                del df[col]
    return df


def read_thermo(filename: str, natoms: int = 1) -> DataFrame:
    """Parses a file in ``thermo.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/thermo_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    natoms
        Number of atoms; used to normalize energies.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in loss.out, append a dimension
        data = data.reshape(1, -1)
    if len(data[0]) == 9:
        # orthorhombic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 12:
        # orthorhombic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 15:
        # triclinic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += (
            ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
        )
    elif len(data[0]) == 18:
        # triclinic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += (
            ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
        )
    else:
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            ' Expected 9, 12, 15 or 18 columns.'
        )
    df = DataFrame(data=data, columns=tags.split())
    assert natoms > 0, 'natoms must be positive'
    df.kinetic_energy /= natoms
    df.potential_energy /= natoms
    return df


def read_xyz(filename: str) -> Atoms:
    """
    Reads the structure input file (``model.xyz``) for GPUMD and returns the
    structure.

    This is a wrapper function around :func:`ase.io.read_xyz` since the ASE implementation does
    not read velocities properly.

    Parameters
    ----------
    filename
        Name of file from which to read the structure.

    Returns
    -------
        Structure as ASE Atoms object with additional per-atom arrays
        representing atomic masses, velocities etc.
    """
    structure = read(filename, format='extxyz')
    if structure.has('vel'):
        structure.set_velocities(structure.get_array('vel'))
    return structure


def read_runfile(filename: str) -> List[Tuple[str, list]]:
    """
    Parses a GPUMD input file in ``run.in`` format and returns the
    content in the form a list of keyword-value pairs.

    Parameters
    ----------
    filename
        Input file name.

    Returns
    -------
        List of keyword-value pairs.
    """
    data = []
    with open(filename, 'r') as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            if len(flds) == 0:
                continue
            elif len(flds) == 1:
                raise ValueError(f'Line {k} contains only one field:\n{line}')
            keyword = flds[0]
            values = tuple(flds[1:])
            if keyword in ['time_step', 'velocity']:
                values = float(values[0])
            elif keyword in ['dump_thermo', 'dump_position', 'dump_restart', 'run']:
                values = int(values[0])
            elif len(values) == 1:
                values = values[0]
            data.append((keyword, values))
    return data


def write_runfile(
    file: Path, parameters: List[Tuple[str, Union[int, float, Tuple[str, float]]]]
):
    """Write a file in run.in format to define input parameters for MD simulation.

    Parameters
    ----------
    file
        Path to file to be written.

    parameters
        Defines all command-parameter(s) pairs used in run.in file
        (see GPUMD documentation for a complete list).
        Values can be either floats, integers, or lists/tuples.
    """

    with open(file, 'w') as f:
        # Write all keywords with parameter(s)
        for key, val in parameters:
            f.write(f'{key} ')
            if isinstance(val, Iterable) and not isinstance(val, str):
                for v in val:
                    f.write(f'{v} ')
            else:
                f.write(f'{val}')
            f.write('\n')


def write_xyz(filename: str, structure: Atoms, groupings: List[List[List[int]]] = None):
    """
    Writes a structure into GPUMD input format (`model.xyz`).

    Parameters
    ----------
    filename
        Name of file to which the structure should be written.
    structure
        Input structure.
    groupings
        Groups into which the individual atoms should be divided in the form of
        a list of list of lists. Specifically, the outer list corresponds to
        the grouping methods, of which there can be three at the most, which
        contains a list of groups in the form of lists of site indices. The
        sum of the lengths of the latter must be the same as the total number
        of atoms.

    Raises
    ------
    ValueError
        Raised if parameters are incompatible.
    """
    # Make a local copy of the atoms object
    _structure = structure.copy()

    # Check velocties parameter
    velocities = _structure.get_velocities()
    if velocities is None or np.max(np.abs(velocities)) < 1e-6:
        has_velocity = 0
    else:
        has_velocity = 1

    # Check groupings parameter
    if groupings is None:
        number_of_grouping_methods = 0
    else:
        number_of_grouping_methods = len(groupings)
        if number_of_grouping_methods > 3:
            raise ValueError('There can be no more than 3 grouping methods!')
        for g, grouping in enumerate(groupings):
            all_indices = [i for group in grouping for i in group]
            if len(all_indices) != len(_structure) or set(all_indices) != set(
                range(len(_structure))
            ):
                raise ValueError(
                    f'The indices listed in grouping method {g} are'
                    ' not compatible with the input structure!'
                )

    # Allowed keyword=value pairs. Use ASEs extyz write functionality.
    #   pbc="pbc_a pbc_b pbc_c"
    #   lattice="ax ay az bx by bz cx cy cz"
    #   properties=property_name:data_type:number_of_columns
    #       species:S:1
    #       pos:R:3
    #       mass:R:1
    #       vel:R:3
    #       group:I:number_of_grouping_methods
    if _structure.has('mass'):
        # If structure already has masses set, use those
        warn('Structure already has array "mass"; will use existing values.')
    else:
        _structure.new_array('mass', _structure.get_masses())

    if has_velocity:
        _structure.new_array('vel', _structure.get_velocities())
    if groupings is not None:
        group_indices = np.array(
            [
                [
                    [
                        group_index
                        for group_index, group in enumerate(grouping)
                        if structure_idx in group
                    ]
                    for grouping in groupings
                ]
                for structure_idx in range(len(_structure))
            ]
        ).squeeze()  # pythoniccc
        _structure.new_array('group', group_indices)

    write(filename=filename, images=_structure, write_info=True, format='extxyz')


def read_mcmd(filename: str, accumulate: bool = True) -> DataFrame:
    """Parses a Monte Carlo output file in ``mcmd.out`` format
    and returns the content in the form of a DataFrame.

    Parameters
    ----------
    filename
        Path to file to be parsed.
    accumulate
        If ``True`` the MD steps between subsequent Monte Carlo
        runs in the same output file will be accumulated.

    Returns
    -------
        DataFrame containing acceptance ratios and concentrations (if available),
        as well as key Monte Carlo parameters.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = []
    offset = 0
    step = 0
    accummulated_step = 0
    for line in lines:
        if line.startswith('# mc'):
            flds = line.split()
            mc_type = flds[2]
            md_steps = int(flds[3])
            mc_trials = int(flds[4])
            temperature_initial = float(flds[5])
            temperature_final = float(flds[6])
            if mc_type.endswith('sgc'):
                ntypes = int(flds[7])
                species = [flds[8+2*k] for k in range(ntypes)]
                phis = {f'phi_{flds[8+2*k]}': float(flds[9+2*k]) for k in range(ntypes)}
            kappa = float(flds[8+2*ntypes]) if mc_type == 'vcsgc' else np.nan
        elif line.startswith('# num_MD_steps'):
            continue
        else:
            flds = line.split()
            previous_step = step
            step = int(flds[0])
            if step <= previous_step and accumulate:
                offset += previous_step
            accummulated_step = step + offset
            record = dict(
                step=accummulated_step,
                mc_type=mc_type,
                md_steps=md_steps,
                mc_trials=mc_trials,
                temperature_initial=temperature_initial,
                temperature_final=temperature_final,
                acceptance_ratio=float(flds[1]),
            )
            if mc_type.endswith('sgc'):
                record.update(phis)
                if mc_type == 'vcsgc':
                    record['kappa'] = kappa
                concentrations = {f'conc_{s}': float(flds[k])
                                  for k, s in enumerate(species, start=2)}
                record.update(concentrations)
            data.append(record)
    df = DataFrame.from_dict(data)
    return df


def read_thermodynamic_data(
    directory_name: str,
    normalize: bool = False,
) -> DataFrame:
    """Parses the data in a GPUMD output directory
    and returns the content in the form of a :class:`DataFrame`.
    This function reads the ``thermo.out``, ``run.in``, and ``model.xyz``
    (optionally) files, and returns the thermodynamic data including the
    time (in ps), the pressure (in GPa), the side lengths of the simulation
    cell (in Å), and the volume (in Å:sup:`3` or Å:sup:`3`/atom).

    Parameters
    ----------
    directory_name
        Path to directory to be parsed.
    normalize
        Normalize thermodynamic quantities per atom.
        This requires the ``model.xyz`` file to be present.

    Returns
    -------
        :class:`DataFrame` containing (augmented) thermodynamic data.
    """

    try:
        params = read_runfile(f'{directory_name}/run.in')
    except FileNotFoundError:
        raise FileNotFoundError(f'No `run.in` file found in {directory_name}')

    if normalize:
        try:
            structure = read(f'{directory_name}/model.xyz')
        except FileNotFoundError:
            raise FileNotFoundError(f'No `model.xyz` file found in {directory_name}')
        natoms = len(structure)
    else:
        natoms = 1

    blocks = []
    time_step = 1.0  # GPUMD default
    dump_thermo = None
    for p, v in params:
        if p == 'time_step':
            time_step = v
        elif p == 'dump_thermo':
            dump_thermo = v
        elif p == 'run':
            if dump_thermo is None:
                raise ValueError(
                    'Could not extract value of `dump_thermo` keyword from `run.in` file.')
            # We do not require dump_thermo to exist for subsequent
            # runs if it has been used for atleast one before.
            # But if there has been no new dump_thermo, we
            # should not create a block.
            if (dump_thermo != 'DEFINEDONCE'):
                blocks.append(dict(
                    nsteps=v,
                    time_step=time_step,
                    dump_thermo=dump_thermo,
                ))
                dump_thermo = 'DEFINEDONCE'

    try:
        df = read_thermo(f'{directory_name}/thermo.out', natoms=natoms)
    except FileNotFoundError:
        raise FileNotFoundError(f'No `thermo.out` file found in {directory_name}')

    expected_rows = sum([int(round(b['nsteps'] / b['dump_thermo'], 0))
                         for b in blocks if b['dump_thermo'] is not None])
    if len(df) != expected_rows:
        warn(f'Number of rows in `thermo.out` file ({len(df)}) does not match'
             f' expectation based on `run.in` file ({expected_rows}).')
    if len(df) > expected_rows:
        raise ValueError(f'Too many rows in `thermo.out` file ({len(df)}) compared to'
                         f' expectation based on `run.in` file ({expected_rows}).')

    # Fewer rows than expected should be ok, since the run may have crashed/not completed yet.
    times = []
    offset = 0.0
    for b in blocks:
        ns = int(round(b['nsteps'] / b['dump_thermo'], 0))
        block_times = np.array(range(1, 1 + ns)) \
            * b['dump_thermo'] * b['time_step'] * 1e-3   # in ps
        block_times += offset
        times.extend(block_times)
        offset = times[-1]
    df['time'] = times[:len(df)]

    df['pressure'] = (df.stress_xx + df.stress_yy + df.stress_zz) / 3
    if 'cell_xy' in df:
        df['alat'] = np.sqrt(df.cell_xx ** 2 + df.cell_xy ** 2 + df.cell_xz ** 2)
        df['blat'] = np.sqrt(df.cell_yx ** 2 + df.cell_yy ** 2 + df.cell_yz ** 2)
        df['clat'] = np.sqrt(df.cell_zx ** 2 + df.cell_zy ** 2 + df.cell_zz ** 2)
        volume = (df.cell_xx * df.cell_yy * df.cell_zz +
                  df.cell_xy * df.cell_yz * df.cell_xz +
                  df.cell_xz * df.cell_yx * df.cell_zy -
                  df.cell_xx * df.cell_yz * df.cell_zy -
                  df.cell_xy * df.cell_yx * df.cell_zz -
                  df.cell_xz * df.cell_yy * df.cell_zx)
    else:
        df['alat'] = df.cell_xx
        df['blat'] = df.cell_yy
        df['clat'] = df.cell_zz
        volume = (df.cell_xx * df.cell_yy * df.cell_zz)
    df['volume'] = volume
    if normalize:
        df.volume /= natoms

    return df
