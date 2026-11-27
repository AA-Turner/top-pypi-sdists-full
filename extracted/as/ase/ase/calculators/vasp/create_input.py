# Copyright (C) 2008 CSC - Scientific Computing Ltd.
"""This module defines an ASE interface to VASP.

Developed on the basis of modules by Jussi Enkovaara and John Kitchin.
The pseudpotentials provided by VASP should be stored in a single directory
that is defined by the environment variable VASP_PP_PATH. The VASP_PP_PATH
should contain subdirectories of the form potpaw_LDA(.version) and
potpaw_PBE(.version). The version of the pseudopotentials can be specified
with the environment variable VASP_PP_VERSION or by the calculator input
parameter 'pp_version'. If neither is set, the default is to use the
unversioned directories to maintain backwards compatability.

The user should also set the environmental flag $VASP_SCRIPT pointing
to a python script looking something like::

   import os
   exitcode = os.system('vasp')

Alternatively, user can set the environmental flag $VASP_COMMAND pointing
to the command use the launch vasp e.g. 'vasp' or 'mpirun -n 16 vasp'

https://www.vasp.at/
"""

import os
import re
import shutil
import warnings
from collections.abc import Callable, Iterable, Sequence
from os.path import join
from typing import Any, TextIO

import numpy as np

import ase
from ase import Atoms
from ase.calculators.calculator import InputError, kpts2ndarray
from ase.calculators.vasp.setups import get_default_setups
from ase.config import cfg
from ase.io.vasp_parsers.incar_writer import write_incar

FLOAT_FORMAT = '5.6f'
EXP_FORMAT = '5.2e'

_T_STRINGS = {'t', 'true', '.true.'}
_F_STRINGS = {'f', 'false', '.false.'}


def check_ichain(ichain, ediffg, iopt):
    ichain_dct = {}
    if ichain > 0:
        ichain_dct['ibrion'] = 3
        ichain_dct['potim'] = 0.0
        if iopt is None:
            warnings.warn('WARNING: optimization is set to LFBGS (IOPT = 1)')
            ichain_dct['iopt'] = 1
        if ediffg is None or float(ediffg > 0.0):
            raise RuntimeError('Please set EDIFFG < 0')
    return ichain_dct


def set_m_constr(atoms, lnoncollinear, m_constr, sorting):
    mag_dict = {}
    if not lnoncollinear or m_constr is None:
        return {}

    m_constr = np.array(m_constr)
    if m_constr.shape != (len(atoms), 3):
        raise InputError(
            f'Expected m_constr tag to be of shape ({len(atoms)}, 3), '
            f'i.e, 1 vector per atom, '
            f'but got {m_constr.shape}'
        )

    m_constr = m_constr[sorting].flatten()
    line = _compactify_magmom_list(m_constr)
    mag_dict['m_constr'] = line
    return mag_dict


def _compactify_magmom_list(magmom):
    lst = [[1, magmom[0]]]
    for n in range(1, len(magmom)):
        if magmom[n] == magmom[n - 1]:
            lst[-1][0] += 1
        else:
            lst.append([1, magmom[n]])
    line = ' '.join(['{:d}*{:.4f}'.format(mom[0], mom[1]) for mom in lst])
    return line


def set_magmom(ispin, spinpol, atoms, magmom_input, sorting, lnoncollinear):
    """Helps to set the magmom tag in the INCAR file with correct formatting"""
    magmom_dct = {}
    if magmom_input is not None:
        if len(magmom_input) != len(atoms):
            msg = (
                'Expected length of magmom tag to be'
                ' {}, i.e. 1 value per atom, but got {}'
            ).format(len(atoms), len(magmom_input))
            raise ValueError(msg)

            # Check if user remembered to specify ispin
            # note: we do not overwrite ispin if ispin=1
            # do not change ispin if lnoncollinear has been set by the user.
            # vasp ispin and lnoncollinear do not go together.
        if not ispin and not lnoncollinear:
            spinpol = True
            # note that ispin is an int key, but for the INCAR it does not
            # matter
            magmom_dct['ispin'] = 2
        magmom = np.array(magmom_input)
        magmom = magmom[sorting]

        if magmom.ndim > 1:
            magmom = magmom.flatten()

    elif spinpol:  # and atoms.get_initial_magnetic_moments().any()):
        # We will write the magnetic moments even if they are zero.
        # but we could still be doing a spinpol calculation
        if not ispin and not lnoncollinear:
            magmom_dct['ispin'] = 2
        # Write out initial magnetic moments
        magmom = atoms.get_initial_magnetic_moments()[sorting]
        # unpack magmom array if three components specified
        if magmom.ndim > 1:
            magmom = [item for sublist in magmom for item in sublist]
    else:
        return spinpol, {}
    # Compactify the magmom list to symbol order
    line = _compactify_magmom_list(magmom)
    magmom_dct['magmom'] = line
    return spinpol, magmom_dct


def set_ldau(ldau_param, luj_params, symbol_count):
    """Helps to set the ldau tag in the INCAR file with correct formatting"""
    ldau_dct = {}
    if ldau_param is None:
        ldau_dct['ldau'] = '.TRUE.'
    llist = []
    ulist = []
    jlist = []
    for symbol in symbol_count:
        #  default: No +U
        luj = luj_params.get(symbol[0], {'L': -1, 'U': 0.0, 'J': 0.0})
        llist.append(int(luj['L']))
        ulist.append(f'{luj["U"]:{".3f"}}')
        jlist.append(f'{luj["J"]:{".3f"}}')
    ldau_dct['ldaul'] = llist
    ldau_dct['ldauu'] = ulist
    ldau_dct['ldauj'] = jlist
    return ldau_dct


def _calc_nelect_from_charge(
    nelect: float | None,
    charge: float | None,
    nelect_from_ppp: float,
) -> float | None:
    """Determine nelect resulting from a given charge if charge != 0.0.

    If nelect is additionally given explicitly, then we need to determine it
    even for net charge of 0 to check for conflicts.

    """
    if charge is not None and charge != 0.0:
        nelect_from_charge = nelect_from_ppp - charge
        if nelect and nelect != nelect_from_charge:
            raise ValueError(
                'incompatible input parameters: '
                f'nelect={nelect}, but charge={charge} '
                f'(neutral nelect is {nelect_from_ppp})'
            )
        return nelect_from_charge
    return nelect  # NELECT explicitly given in INCAR (`None` if not given)


def get_pp_setup(setup) -> tuple[dict, Sequence[int]]:
    """
    Get the pseudopotential mapping based on the "setpus" input.

    Parameters
    ----------
    setup : [str, dict]
        The setup to use for the calculation. This can be a string
        shortcut, or a dict of atom identities and suffixes.
        In the dict version it is also possible to select a base setup
        e.g.: {'base': 'minimal', 'Ca': '_sv', 2: 'O_s'}
        If the key is an integer, this means an atom index.
        For the string version, 'minimal', 'recommended' and 'GW' are
        available. The default is 'minimal

    Returns
    -------
    setups : dict
        The setup dictionary, with atom indices as keys and suffixes
        as values.
    special_setups : list
        A list of atom indices that have a special setup.
    """
    special_setups = []

    # Avoid mutating the module dictionary, so we use a copy instead
    # Note, it is a nested dict, so a regular copy is not enough
    setups_defaults = get_default_setups()

    # Default to minimal basis
    if setup is None:
        setup = {'base': 'minimal'}

    # String shortcuts are initialised to dict form
    elif isinstance(setup, str):
        if setup.lower() in setups_defaults.keys():
            setup = {'base': setup}

    # Dict form is then queried to add defaults from setups.py.
    if 'base' in setup:
        setups = setups_defaults[setup['base'].lower()]
    else:
        setups = {}

    # Override defaults with user-defined setups
    if setup is not None:
        setups.update(setup)

    for m in setups:
        try:
            special_setups.append(int(m))
        except ValueError:
            pass
    return setups, special_setups


def format_kpoints(kpts, atoms, reciprocal=False, gamma=False):
    tokens = []
    append = tokens.append

    append('KPOINTS created by Atomic Simulation Environment\n')

    if isinstance(kpts, dict):
        kpts = kpts2ndarray(kpts, atoms=atoms)
        reciprocal = True

    shape = np.array(kpts).shape

    # Wrap scalar in list if necessary
    if shape == ():
        kpts = [kpts]
        shape = (1,)

    if len(shape) == 1:
        append('0\n')
        if shape == (1,):
            append('Auto\n')
        elif gamma:
            append('Gamma\n')
        else:
            append('Monkhorst-Pack\n')
        append(' '.join(f'{kpt:d}' for kpt in kpts))
        append('\n0 0 0\n')
    elif len(shape) == 2:
        append('%i \n' % (len(kpts)))
        if reciprocal:
            append('Reciprocal\n')
        else:
            append('Cartesian\n')
        for n in range(len(kpts)):
            [append('%f ' % kpt) for kpt in kpts[n]]
            if shape[1] == 4:
                append('\n')
            elif shape[1] == 3:
                append('1.0 \n')
    return ''.join(tokens)


exp_keys = [
    'ediff',  # stopping-criterion for electronic upd.
    'ediffg',  # stopping-criterion for ionic upd.
    'symprec',  # precession in symmetry routines
    # The next keywords pertain to the VTST add-ons from Graeme Henkelman's
    # group at UT Austin
    'fdstep',  # Finite diference step for IOPT = 1 or 2
]

dict_keys = [
    'ldau_luj',  # dictionary with L(S)DA+U parameters, e.g. {'Fe':{'L':2,
    # 'U':4.0, 'J':0.9}, ...}
]


class GenerateVaspInput:
    # Parameters corresponding to 'xc' settings.  This may be modified
    # by the user in-between loading calculators.vasp submodule and
    # instantiating the calculator object with calculators.vasp.Vasp()
    xc_defaults = {
        'lda': {'pp': 'LDA'},
        # GGAs
        'blyp': {  # https://www.vasp.at/forum/viewtopic.php?p=17234
            'pp': 'PBE',
            'gga': 'B5',
            'aldax': 1.00,
            'aggax': 1.00,
            'aggac': 1.00,
            'aldac': 0.00,
        },
        'pbe': {'pp': 'PBE', 'gga': 'PE'},
        'pw91': {'gga': '91'},
        'pbesol': {'gga': 'PS'},
        'revpbe': {'gga': 'RE'},
        'rpbe': {'gga': 'RP'},
        'am05': {'gga': 'AM'},
        # Meta-GGAs
        'tpss': {'metagga': 'TPSS'},
        'revtpss': {'metagga': 'RTPSS'},
        'm06l': {'metagga': 'M06L'},
        'ms0': {'metagga': 'MS0'},
        'ms1': {'metagga': 'MS1'},
        'ms2': {'metagga': 'MS2'},
        'scan': {'metagga': 'SCAN'},
        'rscan': {'metagga': 'RSCAN'},
        'r2scan': {'metagga': 'R2SCAN'},
        'mbj': {
            # Modified Becke-Johnson
            'metagga': 'MBJ',
        },
        'tb09': {
            # Alias for MBJ
            'metagga': 'MBJ',
        },
        # vdW-DFs
        'vdw-df': {'gga': 'RE', 'luse_vdw': True, 'aggac': 0.0},
        'vdw-df-cx': {'gga': 'CX', 'luse_vdw': True, 'aggac': 0.0},
        'vdw-df-cx0p': {
            'gga': 'CX',
            'luse_vdw': True,
            'aggac': 0.0,
            'lhfcalc': True,
            'aexx': 0.2,
            'aggax': 0.8,
        },
        'vdw-df3-opt1': {
            'gga': 'BO',
            'param1': 0.1122334456,
            'param2': 0.1234568,
            'aggac': 0.0,
            'luse_vdw': True,
            'ivdw_nl': 3,
            'alpha_vdw': 0.94950,
            'gamma_vdw': 1.12,
        },
        'vdw-df3-opt2': {
            'gga': 'MK',
            'param1': 0.1234568,
            'param2': 0.58,
            'aggac': 0.0,
            'luse_vdw': True,
            'ivdw_nl': 4,
            'zab_vdw': -1.8867,
            'alpha_vdw': 0.28248,
            'gamma_vdw': 1.29,
        },
        'rvv10': {
            'gga': 'ML',
            'luse_vdw': True,
            'ivdw_nl': 2,
            'bparam': 6.3,
            'cparam': 0.0093,
        },
        'scan+rvv10': {
            'metagga': 'SCAN',
            'luse_vdw': True,
            'bparam': 15.7,
            'cparam': 0.0093,
        },
        'pbe+rvv10l': {
            'gga': 'PE',
            'luse_vdw': True,
            'bparam': 10,
            'cparam': 0.0093,
        },
        'r2scan+rvv10': {
            'metagga': 'R2SCAN',
            'luse_vdw': True,
            'bparam': 11.95,
            'cparam': 0.0093,
        },
        'optpbe-vdw': {'gga': 'OR', 'luse_vdw': True, 'aggac': 0.0},
        'optb88-vdw': {
            'gga': 'BO',
            'luse_vdw': True,
            'aggac': 0.0,
            'param1': 1.1 / 6.0,
            'param2': 0.22,
        },
        'optb86b-vdw': {
            'gga': 'MK',
            'luse_vdw': True,
            'aggac': 0.0,
            'param1': 0.1234,
            'param2': 1.0,
        },
        'vdw-df2': {
            'gga': 'ML',
            'luse_vdw': True,
            'aggac': 0.0,
            'zab_vdw': -1.8867,
        },
        'rev-vdw-df2': {
            'gga': 'MK',
            'luse_vdw': True,
            'param1': 0.1234,
            'param2': 0.711357,
            'zab_vdw': -1.8867,
            'aggac': 0.0,
        },
        'beef-vdw': {'gga': 'BF', 'luse_vdw': True, 'zab_vdw': -1.8867},
        # Hartree-Fock and hybrids
        'hf': {'lhfcalc': True, 'aexx': 1.0, 'aldac': 0.0, 'aggac': 0.0},
        'b3lyp': {
            'gga': 'B3',
            'lhfcalc': True,
            'aexx': 0.2,
            'aggax': 0.72,
            'aggac': 0.81,
            'aldac': 0.19,
        },
        'pbe0': {'gga': 'PE', 'lhfcalc': True},
        'hse03': {'gga': 'PE', 'lhfcalc': True, 'hfscreen': 0.3},
        'hse06': {'gga': 'PE', 'lhfcalc': True, 'hfscreen': 0.2},
        'hsesol': {'gga': 'PS', 'lhfcalc': True, 'hfscreen': 0.2},
        # MN-VFM functionals
        'sogga': {'gga': 'SA'},
        'sogga11': {'gga': 'S1'},
        'sogga11-x': {'gga': 'SX', 'lhfcalc': True, 'aexx': 0.401},
        'n12': {'gga': 'N2'},
        'n12-sx': {'gga': 'NX', 'lhfcalc': True, 'lhfscreen': 0.2},
        'mn12l': {'metagga': 'MN12L'},
        'gam': {'gga': 'GA'},
        'mn15l': {'metagga': 'MN15L'},
        'hle17': {'metagga': 'HLE17'},
        'revm06l': {'metagga': 'revM06L'},
        'm06sx': {
            'metagga': 'M06SX',
            'lhfcalc': True,
            'hfscreen': 0.189,
            'aexx': 0.335,
        },
    }

    # environment variable for PP paths
    VASP_PP_PATH = 'VASP_PP_PATH'
    VASP_PP_VERSION = 'VASP_PP_VERSION'

    def __init__(self, restart=None):
        self.float_params = {}
        self.exp_params = {}
        self.string_params = {}
        self.int_params = {}
        self.bool_params = {}
        self.list_bool_params = {}
        self.list_int_params = {}
        self.list_float_params = {}
        self.special_params = {}
        self.dict_params = {}
        self.atoms = None
        for key in exp_keys:
            self.exp_params[key] = None
        for key in dict_keys:
            self.dict_params[key] = None

        # Initialize internal dictionary of input parameters which are
        # not regular VASP keys
        self.input_params = {
            'xc': None,  # Exchange-correlation recipe (e.g. 'B3LYP')
            'pp': None,  # Pseudopotential file (e.g. 'PW91')
            'pp_version': None,  # pseudopotential version (e.g. '52', '64')
            'setups': None,  # Special setups (e.g pv, sv, ...)
            'txt': '-',  # Where to send information
            'kpts': (1, 1, 1),  # k-points
            'kpts_opt': None,  # optional NSCF k-points
            'gamma_opt': False,
            'reciprocal_opt': False,
            # Option to use gamma-sampling instead of Monkhorst-Pack:
            'gamma': False,
            # number of points between points in band structures:
            'kpts_nintersections': None,
            # Option to write explicit k-points in units
            # of reciprocal lattice vectors:
            'reciprocal': False,
            # Switch to disable writing constraints to POSCAR
            'ignore_constraints': False,
            # Net charge for the whole system; determines nelect if not 0
            'charge': None,
            # Deprecated older parameter which works just like "charge" but
            # with the sign flipped
            'net_charge': None,
            # Custom key-value pairs, written to INCAR with *no* type checking
            'custom': {},
        }

    def set_xc_params(self, xc):
        """Set parameters corresponding to XC functional"""
        xc = xc.lower()
        if xc is None:
            pass
        elif xc not in self.xc_defaults:
            xc_allowed = ', '.join(self.xc_defaults.keys())
            raise ValueError(
                '{} is not supported for xc! Supported xc valuesare: {}'.format(
                    xc, xc_allowed
                )
            )
        else:
            # XC defaults to PBE pseudopotentials
            if 'pp' not in self.xc_defaults[xc]:
                self.set(pp='PBE')
            self.set(**self.xc_defaults[xc])

    def set(self, **kwargs):

        if (
            ('ldauu' in kwargs)
            and ('ldaul' in kwargs)
            and ('ldauj' in kwargs)
            and ('ldau_luj' in kwargs)
        ):
            raise NotImplementedError(
                'You can either specify ldaul, ldauu, and ldauj OR '
                'ldau_luj. ldau_luj is not a VASP keyword. It is a '
                'dictionary that specifies L, U and J for each '
                'chemical species in the atoms object. '
                'For example for a water molecule:'
                """ldau_luj={'H':{'L':2, 'U':4.0, 'J':0.9},
                      'O':{'L':2, 'U':4.0, 'J':0.9}}"""
            )

        if 'xc' in kwargs:
            self.set_xc_params(kwargs['xc'])
        for key, value in kwargs.items():
            if key in self.float_params:
                self.float_params[key] = value
            elif key in self.exp_params:
                self.exp_params[key] = value
            elif key in self.string_params:
                self.string_params[key] = value
            elif key in self.int_params:
                self.int_params[key] = value
            elif key in self.bool_params:
                self.bool_params[key] = value
            elif key in self.list_bool_params:
                self.list_bool_params[key] = value
            elif key in self.list_int_params:
                self.list_int_params[key] = value
            elif key in self.list_float_params:
                self.list_float_params[key] = value
            elif key in self.special_params:
                self.special_params[key] = value
            elif key in self.dict_params:
                self.dict_params[key] = value
            elif key in self.input_params:
                self.input_params[key] = value
            elif value is None:
                # There is no value to write, and no existing typed parameter
                # to clear.  Existing parameters are cleared above.
                continue
            elif isinstance(value, str):
                self.string_params[key] = value
            # `bool` is a subclass of `int` and should be checked earlier.
            # https://docs.python.org/3/c-api/bool.html
            elif isinstance(value, bool):
                self.bool_params[key] = value
            elif isinstance(value, (int, np.integer)):
                self.int_params[key] = value
            elif isinstance(value, (float, np.floating)):
                self.float_params[key] = value
            elif isinstance(value, Iterable) and not isinstance(
                value, (str, bytes)
            ):
                if len(value) == 0:
                    msg = f'empty list is given for {key}'
                    raise ValueError(msg)
                if isinstance(_flatten(value)[0], bool):
                    self.list_bool_params[key] = value
                elif isinstance(_flatten(value)[0], (int, np.integer)):
                    self.list_int_params[key] = value
                elif isinstance(_flatten(value)[0], (float, np.floating)):
                    self.list_float_params[key] = value
                else:
                    msg = f'cannot handle type of value for {key} = {value!r}'
                    raise TypeError(msg)
            else:
                msg = f'cannot handle type of value for {key} = {value!r}'
                raise TypeError(msg)

    def check_xc(self):
        """Make sure the calculator has functional & pseudopotentials set up

        If no XC combination, GGA functional or POTCAR type is specified,
        default to PW91. Otherwise, try to guess the desired pseudopotentials.
        """

        p = self.input_params

        # There is no way to correctly guess the desired
        # set of pseudopotentials without 'pp' being set.
        # Usually, 'pp' will be set by 'xc'.
        if 'pp' not in p or p['pp'] is None:
            if self.string_params.get('gga') is None:
                p.update({'pp': 'lda'})
            elif self.string_params['gga'].lower() == 'pe':
                p.update({'pp': 'pbe'})
            else:
                raise NotImplementedError(
                    'Unable to guess the desired set of pseudopotential'
                    '(POTCAR) files. Please do one of the following: \n'
                    "1. Use the 'xc' parameter to define your XC functional."
                    "These 'recipes' determine the pseudopotential file as "
                    'well as setting the INCAR parameters.\n'
                    "2. Use the 'gga' settings None (default) or 'PE'; "
                    'these correspond to LDA and PBE, respectively.\n'
                    "3. Set the POTCAR explicitly with the 'pp' flag. The "
                    'value should be the name of a folder on the VASP_PP_PATH'
                    ", and the aliases 'LDA' and 'PBE' are also accepted.\n"
                )

        if (
            p['xc'] is not None
            and p['xc'].lower() == 'lda'
            and p['pp'].lower() != 'lda'
        ):
            warnings.warn(
                'XC is set to LDA, but PP is set to '
                '{0}. \nThis calculation is using the {0} '
                'POTCAR set. \n Please check that this is '
                'really what you intended!'
                '\n'.format(p['pp'].upper())
            )

    def _make_sort(
        self, atoms: ase.Atoms, special_setups: Sequence[int] = ()
    ) -> tuple[list[int], list[int]]:
        symbols, _ = count_symbols(atoms, exclude=special_setups)

        # Create sorting list
        srt = []  # type: list[int]
        srt.extend(special_setups)

        for symbol in symbols:
            for m, atom in enumerate(atoms):
                if m in special_setups:
                    continue
                if atom.symbol == symbol:
                    srt.append(m)
        # Create the resorting list
        resrt = list(range(len(srt)))
        for n in range(len(resrt)):
            resrt[srt[n]] = n
        return srt, resrt

    def _set_spinpol(self, atoms):
        if self.int_params.get('ispin') is None:
            self.spinpol = atoms.get_initial_magnetic_moments().any()
        else:
            # VASP runs non-spin-polarized calculations when `ispin=1`,
            # regardless if `magmom` is specified or not.
            self.spinpol = self.int_params['ispin'] == 2

    def _build_pp_list(
        self, atoms, setups=None, special_setups: Sequence[int] = ()
    ):
        """Build the pseudopotential lists"""

        p = self.input_params

        if p['pp_version'] is not None:
            pp_version = p['pp_version']
        elif self.VASP_PP_VERSION in cfg:
            pp_version = cfg[self.VASP_PP_VERSION]
        else:
            pp_version = ''

        if setups is None:
            setups, special_setups = get_pp_setup(p['setups'])

        symbols, _ = count_symbols(atoms, exclude=special_setups)

        # Potpaw folders may be identified by an alias or full name
        for pp_alias, pp_folder in (
            ('lda', f'potpaw_LDA.{pp_version}' if pp_version else 'potpaw'),
            ('pbe', f'potpaw_PBE.{pp_version}' if pp_version else 'potpaw_PBE'),
        ):
            if p['pp'].lower() == pp_alias:
                break
        else:
            pp_folder = p['pp']

        if self.VASP_PP_PATH in cfg:
            pppath = cfg[self.VASP_PP_PATH]
            if not os.path.exists(pppath):
                raise RuntimeError(f'VASP_PP_PATH does not exist: {pppath}')
        else:
            pppath = None
        ppp_list = []
        # Setting the pseudopotentials, first special setups and
        # then according to symbols
        for m in special_setups:
            if m in setups:
                special_setup_index = m
            elif str(m) in setups:
                special_setup_index = str(m)  # type: ignore[assignment]
            else:
                raise Exception(
                    'Having trouble with special setup index {}.'
                    ' Please use an int.'.format(m)
                )
            potcar = join(pp_folder, setups[special_setup_index], 'POTCAR')
            potcar_path = join(pppath, potcar) if pppath is not None else potcar

            if os.path.exists(potcar_path):
                ppp_list.append(potcar_path)
            elif os.path.exists(potcar_path + '.Z'):
                ppp_list.append(potcar_path + '.Z')
            else:
                msg = """Looking for {}.
                No pseudopotential for symbol{} with setup {} """.format(
                    potcar_path, atoms.symbols[m], setups[special_setup_index]
                )
                raise RuntimeError(msg)

        for symbol in symbols:
            try:
                potcar = join(pp_folder, symbol + setups[symbol], 'POTCAR')
            except (TypeError, KeyError):
                potcar = join(pp_folder, symbol, 'POTCAR')

            potcar_path = join(pppath, potcar) if pppath is not None else potcar

            if os.path.exists(potcar_path):
                ppp_list.append(potcar_path)
            elif os.path.exists(potcar_path + '.Z'):
                ppp_list.append(potcar_path + '.Z')
            else:
                msg = """Looking for {}
                        The pseudopotentials are expected to be in:
                        LDA:  $VASP_PP_PATH/potpaw_LDA(.52|.54|.64)
                                or $VASP_PP_PATH/potpaw
                        PBE:  $VASP_PP_PATH/potpaw_PBE(.52|.54|.64)

                        No pseudopotential for {}!""".format(
                    potcar_path, symbol
                )
                raise RuntimeError(msg)
        return ppp_list

    def initialize(self, atoms: Atoms) -> None:
        """Initialize a VASP calculation

        Constructs the POTCAR file (does not actually write it).
        User should specify the PATH
        to the pseudopotentials in VASP_PP_PATH environment variable

        The pseudopotentials are expected to be in:
        LDA:  $VASP_PP_PATH/potpaw_LDA(.52|.54|.64) or $VASP_PP_PATH/potpaw
        PBE:  $VASP_PP_PATH/potpaw_PBE(.52|.54|.64)

        if your pseudopotentials are somewhere else, or named
        differently you may make symlinks at the paths above that
        point to the right place. Alternatively, you may pass the full
        name of a folder on the VASP_PP_PATH to the 'pp' parameter.
        """

        self.check_xc()
        self.atoms = atoms
        self.all_symbols = atoms.get_chemical_symbols()
        self.natoms = len(atoms)

        self._set_spinpol(atoms)

        setups, special_setups = get_pp_setup(self.input_params['setups'])

        # Determine the number of atoms of each atomic species
        # sorted after atomic species
        symbols, symbolcount = count_symbols(atoms, exclude=special_setups)
        self.sort, self.resort = self._make_sort(
            atoms, special_setups=special_setups
        )

        self.atoms_sorted = atoms[self.sort]

        # Check if the necessary POTCAR files exists and
        # create a list of their paths.
        atomtypes = atoms.get_chemical_symbols()
        self.symbol_count: list[tuple[str, int]] = []
        for m in special_setups:
            self.symbol_count.append((atomtypes[m], 1))
        for s in symbols:
            self.symbol_count.append((s, symbolcount[s]))

        # create pseudopotential list
        self.ppp_list = self._build_pp_list(
            atoms,
            setups=setups,
            special_setups=special_setups,
        )

        self.converged = None
        self.setups_changed = None

    def default_nelect_from_ppp(self) -> float:
        """Get default number of electrons from ppp_list and symbol_count

        "Default" here means that the resulting cell would be neutral.
        """
        symbol_valences: list[tuple[str, float]] = []
        for filename in self.ppp_list:
            with open_potcar(filename=filename) as ppp_file:
                r = read_potcar_numbers_of_electrons(ppp_file)
                symbol_valences.extend(r)
        assert len(self.symbol_count) == len(symbol_valences)
        default_nelect = 0.0
        for (symbol1, count), (symbol2, valence) in zip(
            self.symbol_count, symbol_valences
        ):
            assert symbol1 == symbol2
            default_nelect += count * valence
        return default_nelect

    def write_input(self, atoms, directory='./'):
        from ase.io.vasp import write_vasp

        write_vasp(
            join(directory, 'POSCAR'),
            self.atoms_sorted,
            symbol_count=self.symbol_count,
            ignore_constraints=self.input_params['ignore_constraints'],
        )
        self.write_incar(atoms, directory=directory)
        self.write_potcar(directory=directory)
        self.write_kpoints(atoms=atoms, directory=directory)
        self.write_sort_file(directory=directory)
        self.copy_vdw_kernel(directory=directory)

    def copy_vdw_kernel(self, directory='./'):
        """Method to copy the vdw_kernel.bindat file.
        Set ASE_VASP_VDW environment variable to the vdw_kernel.bindat
        folder location. Checks if LUSE_VDW is enabled, and if no location
        for the vdW kernel is specified, a warning is issued."""

        vdw_env = 'ASE_VASP_VDW'
        kernel = 'vdw_kernel.bindat'
        dst = os.path.join(directory, kernel)

        # No need to copy the file again
        if os.path.isfile(dst):
            return

        if self.bool_params.get('luse_vdw'):
            src = None
            if vdw_env in cfg:
                src = os.path.join(cfg[vdw_env], kernel)

            if not src or not os.path.isfile(src):
                warnings.warn(
                    (
                        'vdW has been enabled, however no'
                        ' location for the {} file'
                        ' has been specified.'
                        ' Set {} environment variable to'
                        ' copy the vdW kernel.'
                    ).format(kernel, vdw_env)
                )
            else:
                shutil.copyfile(src, dst)

    def clean(self):
        """Method which cleans up after a calculation.

        The default files generated by Vasp will be deleted IF this
        method is called.

        """
        files = [
            'CHG',
            'CHGCAR',
            'POSCAR',
            'INCAR',
            'CONTCAR',
            'DOSCAR',
            'EIGENVAL',
            'IBZKPT',
            'KPOINTS',
            'OSZICAR',
            'OUTCAR',
            'PCDAT',
            'POTCAR',
            'vasprun.xml',
            'WAVECAR',
            'XDATCAR',
            'PROCAR',
            'ase-sort.dat',
            'LOCPOT',
            'AECCAR0',
            'AECCAR1',
            'AECCAR2',
        ]
        for f in files:
            try:
                os.remove(f)
            except OSError:
                pass

    def write_incar(self, atoms, directory='./', **kwargs):
        """Writes the INCAR file."""
        incar_params = {}

        # float params
        float_dct = {
            key: f'{val:{FLOAT_FORMAT}}'
            for key, val in self.float_params.items()
            if val is not None
        }

        if (
            'charge' in self.input_params
            and self.input_params['charge'] is not None
        ):
            nelect_val = _calc_nelect_from_charge(
                self.float_params['nelect'],
                self.input_params['charge'],
                self.default_nelect_from_ppp(),
            )
            if nelect_val:
                float_dct['nelect'] = f'{nelect_val:{FLOAT_FORMAT}}'
        incar_params.update(float_dct)

        # exp params
        exp_dct = {
            key: f'{val:{EXP_FORMAT}}'
            for key, val in self.exp_params.items()
            if val is not None
        }
        incar_params.update(exp_dct)

        # string_params
        string_dct = {
            key: val
            for key, val in self.string_params.items()
            if val is not None
        }
        incar_params.update(string_dct)

        # int params
        int_dct = {
            key: val for key, val in self.int_params.items() if val is not None
        }
        if 'ichain' in int_dct.keys():
            ichain_dict = check_ichain(
                ichain=int_dct['ichain'],
                ediffg=self.exp_params.get('ediffg', None),
                iopt=int_dct.get('iopt', None),
            )
            int_dct.update(ichain_dict)
        incar_params.update(int_dct)

        # list_bool_params
        bool_dct = {
            key: val
            for key, val in self.list_bool_params.items()
            if val is not None
        }
        for key, val in bool_dct.items():
            bool_dct[key] = [_to_vasp_bool(x) for x in val]
        incar_params.update(bool_dct)

        # list_int_params
        int_dct = {
            key: val
            for key, val in self.list_int_params.items()
            if val is not None
        }
        if (
            'ldaul' in int_dct.keys()
            and self.dict_params['ldau_luj'] is not None
        ):
            del int_dct['ldaul']
        incar_params.update(int_dct)

        # list_float_params
        float_dct = {
            key: val
            for key, val in self.list_float_params.items()
            if val is not None
        }
        if (
            'ldauu' in float_dct.keys()
            and self.dict_params['ldau_luj'] is not None
        ):
            del float_dct['ldauu']
        if (
            'ldauj' in float_dct.keys()
            and self.dict_params['ldau_luj'] is not None
        ):
            del float_dct['ldauj']
        incar_params.update(float_dct)

        # bool params
        bool_dct = {
            key: _to_vasp_bool(val)
            for key, val in self.bool_params.items()
            if val is not None
        }
        incar_params.update(bool_dct)

        # special params
        special_dct = {
            key: val
            for key, val in self.special_params.items()
            if val is not None
        }
        incar_params.update(special_dct)

        # dict params
        dict_dct = {
            key: val for key, val in self.dict_params.items() if val is not None
        }
        if 'ldau_luj' in dict_dct.keys():
            ldau_dict = set_ldau(
                ldau_param=self.bool_params.get('ldau'),
                luj_params=dict_dct['ldau_luj'],
                symbol_count=self.symbol_count,
            )
            dict_dct.update(ldau_dict)
            del dict_dct['ldau_luj']
        incar_params.update(dict_dct)

        # set magmom based on input or initial atoms object
        spinpol, magmom_dct = set_magmom(
            atoms=atoms,
            ispin=self.int_params.get('ispin'),
            spinpol=self.spinpol,
            magmom_input=incar_params.get('magmom'),
            sorting=self.sort,
            lnoncollinear=self.bool_params.get('lnoncollinear', False),
        )
        self.spinpol = spinpol
        incar_params.update(magmom_dct)

        # set non-llinear magmoms m_constr.
        magm_constr_dct = set_m_constr(
            atoms=atoms,
            lnoncollinear=self.bool_params.get('lnoncollinear', False),
            m_constr=incar_params.get('m_constr'),
            sorting=self.sort,
        )
        incar_params.update(magm_constr_dct)

        # Custom key-value pairs, which receive no formatting
        # Use the comment "# <Custom ASE key>" to denote such
        # a custom key-value pair, as we cannot otherwise
        # reliably and easily identify such non-standard entries

        cust_dict = {
            key: str(val) + '  # <Custom ASE key>'
            for key, val in self.input_params['custom'].items()
            if val is not None
        }
        incar_params.update(cust_dict)

        write_incar(directory=directory, parameters=incar_params)

    def write_kpoints(self, atoms=None, directory='./', **kwargs):
        """Write KPOINTS and, when requested, KPOINTS_OPT."""

        if atoms is None:
            atoms = self.atoms

        for suffix in ('', '_opt'):
            spacing = self.float_params.get('kspacing' + suffix)
            if spacing is not None and not spacing > 0:
                raise ValueError(
                    f'KSPACING{suffix.upper()} value {spacing} '
                    'is not allowable. '
                    'Please use None or a positive number.'
                )
            if spacing is not None:
                continue
            kpts = self.input_params['kpts' + suffix]
            if kpts is None:
                continue
            kpointstring = format_kpoints(
                kpts=kpts,
                atoms=atoms,
                reciprocal=self.input_params['reciprocal' + suffix],
                gamma=self.input_params['gamma' + suffix],
            )
            with open(join(directory, 'KPOINTS' + suffix.upper()), 'w') as fd:
                fd.write(kpointstring)

    def write_potcar(self, suffix='', directory='./'):
        """Writes the POTCAR file."""

        with open(join(directory, 'POTCAR' + suffix), 'w') as potfile:
            for filename in self.ppp_list:
                with open_potcar(filename=filename) as ppp_file:
                    for line in ppp_file:
                        potfile.write(line)

    def write_sort_file(self, directory='./'):
        """Writes a sortings file.

        This file contains information about how the atoms are sorted in
        the first column and how they should be resorted in the second
        column. It is used for restart purposes to get sorting right
        when reading in an old calculation to ASE."""

        with open(join(directory, 'ase-sort.dat'), 'w') as fd:
            for n in range(len(self.sort)):
                fd.write('%5i %5i \n' % (self.sort[n], self.resort[n]))

    # The below functions are used to restart a calculation

    @staticmethod
    def set_if_none(collection: dict[str, Any], key: str, value: Any) -> None:
        collection[key] = (
            value if collection.get(key) is None else collection[key]
        )

    def read_incar(self, filename):
        """Method that imports settings from INCAR file.

        Typically named INCAR."""

        self.spinpol = False
        with open(filename) as fd:
            lines = fd.readlines()

        for line in lines:
            try:
                # Make multiplication, comments, and parameters easier to spot
                line = line.replace('*', ' * ')
                line = line.replace('=', ' = ')
                line = line.replace('#', '# ')
                data = line.split()
                # Skip empty and commented lines.
                if len(data) == 0:
                    continue
                elif data[0][0] in ['#', '!']:
                    continue
                key = data[0].lower()
                if '<Custom ASE key>' in line:
                    # This key was added with custom key-value pair formatting.
                    # Unconditionally add it, no type checking
                    # Get value between "=" and the comment, e.g.
                    # key = 1 2 3  # <Custom ASE key>
                    # value should be '1 2 3'

                    # Split at first occurence of "="
                    value = line.split('=', 1)[1]
                    # First "#" denotes beginning of comment
                    # Add everything before comment as a string to custom dict
                    value = value.split('#', 1)[0].strip()
                    self.set_if_none(self.inputs_params['custom'], key, value)
                elif key in exp_keys:
                    self.set_if_none(self.exp_params, key, float(data[2]))
                elif key == 'ispin':
                    self.set_if_none(self.int_params, key, int(data[2]))
                    if int(data[2]) == 2:
                        self.spinpol = True
                elif key == 'ldaul':
                    lst = _parse_list_value(data[2:], int)
                    self.set_if_none(self.list_int_params, key, lst)
                elif key in {'magmom', 'ldauu', 'ldauj'}:
                    lst = _parse_list_value(data[2:], float)
                    self.set_if_none(self.list_float_params, key, lst)
                    if key == 'magmom' and self.atoms is not None:
                        lst = np.array(lst)
                        self.atoms.set_initial_magnetic_moments(
                            lst[self.resort]
                        )

                # non-registered keys
                elif len(_args_without_comment(data)) > 3:  # multiple values
                    data = _args_without_comment(data)
                    if data[2].lower() in _T_STRINGS | _F_STRINGS:
                        value = [_from_vasp_bool(x) for x in data[2:]]
                        self.set_if_none(self.list_bool_params, key, value)
                    elif data[2].isdigit():
                        value = [int(x) for x in data[2:]]
                        self.set_if_none(self.list_int_params, key, value)
                    else:
                        value = [float(x) for x in data[2:]]
                        self.set_if_none(self.list_float_params, key, value)
                elif data[2].lower() in _T_STRINGS | _F_STRINGS:
                    value = _from_vasp_bool(data[2])
                    self.set_if_none(self.bool_params, key, value)
                elif data[2].isdigit():
                    self.set_if_none(self.int_params, key, int(data[2]))
                else:
                    try:
                        self.set_if_none(self.float_params, key, float(data[2]))
                    except ValueError:
                        self.set_if_none(self.string_params, key, data[2])

            except KeyError as exc:
                raise KeyError(
                    f'Keyword "{key}" in INCAR is not known by calculator.'
                ) from exc
            except IndexError as exc:
                raise IndexError(f'Value missing for keyword "{key}".') from exc

    def read_kpoints(self, filename, opt=False):
        """Read kpoints file, typically named KPOINTS."""
        # If we used VASP builtin kspacing,
        suffix = '_opt' if opt else ''
        if self.float_params.get('kspacing' + suffix) is not None:
            # Don't update kpts array
            return

        with open(filename) as fd:
            lines = fd.readlines()

        ktype = lines[2].split()[0].lower()[0]
        if ktype in ['g', 'm', 'a']:
            if ktype == 'g':
                self.set(**{'gamma' + suffix: True})
                kpts = np.array([int(lines[3].split()[i]) for i in range(3)])
            elif ktype == 'a':
                kpts = np.array([int(lines[3].split()[i]) for i in range(1)])
            elif ktype == 'm':
                self.set(**{'gamma' + suffix: False})
                kpts = np.array([int(lines[3].split()[i]) for i in range(3)])
        else:
            if ktype in ['c', 'k']:
                self.set(**{'reciprocal' + suffix: False})
            else:
                self.set(**{'reciprocal' + suffix: True})
            kpts = np.array(
                [list(map(float, line.split())) for line in lines[3:]]
            )
        self.set(**{'kpts' + suffix: kpts})

    def read_potcar(self, filename):
        """Read the pseudopotential XC functional from POTCAR file."""

        # Search for key 'LEXCH' in POTCAR
        xc_flag = None
        with open(filename) as fd:
            for line in fd:
                key = line.split()[0].upper()
                if key == 'LEXCH':
                    xc_flag = line.split()[-1].upper()
                    break

        if xc_flag is None:
            raise ValueError('LEXCH flag not found in POTCAR file.')

        # Values of parameter LEXCH and corresponding XC-functional
        xc_dict = {'PE': 'PBE', '91': 'PW91', 'CA': 'LDA'}

        if xc_flag not in xc_dict.keys():
            raise ValueError(
                'Unknown xc-functional flag found in POTCAR, LEXCH=%s' % xc_flag
            )

        self.input_params['pp'] = xc_dict[xc_flag]

    def todict(self):
        """Returns a dictionary of all parameters
        that can be used to construct a new calculator object"""
        dict_list = [
            'float_params',
            'exp_params',
            'string_params',
            'int_params',
            'bool_params',
            'list_bool_params',
            'list_int_params',
            'list_float_params',
            'special_params',
            'dict_params',
            'input_params',
        ]
        dct = {}
        for item in dict_list:
            dct.update(getattr(self, item))
        dct = {key: value for key, value in dct.items() if value is not None}
        return dct


def _args_without_comment(data, marks=None):
    """Check split arguments list for a comment, return data up to marker

    INCAR reader splits list arguments on spaces and leaves comment markers as
    individual items. This function returns only the data portion of the list.

    """
    if marks is None:
        marks = ['!', '#']
    comment_locs = [data.index(mark) for mark in marks if mark in data]
    if comment_locs == []:
        return data
    else:
        return data[: min(comment_locs)]


def _from_vasp_bool(x):
    """Cast vasp boolean to Python bool

    VASP files sometimes use T or F as shorthand for the preferred Boolean
    notation .TRUE. or .FALSE. As capitalisation is pretty inconsistent in
    practice, we allow all cases to be cast to a Python bool.

    """
    assert isinstance(x, str)
    if re.search(r'^\.?[tT]', x):
        return True
    elif re.search(r'^\.?[fF]', x):
        return False
    else:
        raise ValueError(f'Value "{x}" not recognized as bool')


def _to_vasp_bool(x):
    """Convert Python boolean to string for VASP input

    In case the value was modified to a string already, appropriate strings
    will also be accepted and cast to a standard .TRUE. / .FALSE. format.

    """
    if isinstance(x, str):
        if x.lower() in ('.true.', 't'):
            x = True
        elif x.lower() in ('.false.', 'f'):
            x = False
        else:
            raise ValueError('"%s" not recognised as VASP Boolean')
    assert isinstance(x, bool)
    if x:
        return '.TRUE.'
    else:
        return '.FALSE.'


def _flatten(values: Iterable) -> Iterable:
    result: list[Any] = []
    for value in values:
        if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
            result.extend(_flatten(value))
        else:
            result.append(value)
    return result


def _parse_list_value(data: list[str], converter: Callable) -> list:
    value: list = []
    i = 0
    while i < len(data):
        if data[i] in ['#', '!']:
            break
        if data[i] == '*':
            b = value.pop()
            i += 1
            for _ in range(int(b)):
                value.append(converter(data[i]))
        else:
            value.append(converter(data[i]))
        i += 1
    return value


def open_potcar(filename):
    """Open POTCAR file with transparent decompression if archive (.Z)"""
    import gzip

    if filename.endswith('R'):
        return open(filename)
    elif filename.endswith('.Z'):
        return gzip.open(filename)
    else:
        raise ValueError(f'Invalid POTCAR filename: "{filename}"')


def read_potcar_numbers_of_electrons(fd: TextIO, /) -> list[tuple[str, float]]:
    """Read number of valence electrons for each atomtype from a POTCAR file.

    Returns
    -------
    list[tuple[str, float]]
        List of (atomic symbol, number of valence electrons).

    """
    nelect: list[tuple[str, float]] = []
    lines = fd.readlines()
    for n, line in enumerate(lines):
        if 'TITEL' in line:
            symbol = line.split('=')[1].split()[1].split('_')[0].strip()
            linep4 = lines[n + 4]
            zval = float(linep4.split(';')[1].split('=')[1].split()[0].strip())
            nelect.append((symbol, zval))
    return nelect


def count_symbols(atoms: Atoms, exclude=()) -> tuple[list[str], dict[str, int]]:
    """Count symbols in atoms object, excluding a set of indices

    Parameters
    ----------
        atoms: Atoms object to be grouped
        exclude: List of indices to be excluded from the counting

    Returns
    -------
        Tuple of (symbols, symbolcount)
        symbols: The unique symbols in the included list
        symbolscount: Count of symbols in the included list

    Example:

    >>> from ase.build import bulk
    >>> atoms = bulk('NaCl', crystalstructure='rocksalt', a=4.1, cubic=True)
    >>> count_symbols(atoms)
    (['Na', 'Cl'], {'Na': 4, 'Cl': 4})
    >>> count_symbols(atoms, exclude=(1, 2, 3))
    (['Na', 'Cl'], {'Na': 3, 'Cl': 2})
    """
    symbols: list[str] = []
    symbolcount: dict[str, int] = {}
    for m, symbol in enumerate(atoms.symbols):
        if m in exclude:
            continue
        if symbol not in symbols:
            symbols.append(symbol)
            symbolcount[symbol] = 1
        else:
            symbolcount[symbol] += 1
    return symbols, symbolcount
