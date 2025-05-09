# fmt: off

"""This module defines an ASE interface to GULP.

Written by:

Andy Cuko <andi.cuko@upmc.fr>
Antoni Macia <tonimacia@gmail.com>

EXPORT ASE_GULP_COMMAND="/path/to/gulp < PREFIX.gin > PREFIX.got"

Keywords
Options

"""
import os
import re

import numpy as np

from ase.calculators.calculator import FileIOCalculator, ReadError
from ase.units import Ang, eV


class GULPOptimizer:
    def __init__(self, atoms, calc):
        self.atoms = atoms
        self.calc = calc

    def todict(self):
        return {'type': 'optimization',
                'optimizer': 'GULPOptimizer'}

    def run(self, fmax=None, steps=None, **gulp_kwargs):
        if fmax is not None:
            gulp_kwargs['gmax'] = fmax
        if steps is not None:
            gulp_kwargs['maxcyc'] = steps

        self.calc.set(**gulp_kwargs)
        self.atoms.calc = self.calc
        self.atoms.get_potential_energy()
        self.atoms.cell = self.calc.get_atoms().cell
        self.atoms.positions[:] = self.calc.get_atoms().positions


class GULP(FileIOCalculator):
    implemented_properties = ['energy', 'free_energy', 'forces', 'stress']
    _legacy_default_command = 'gulp < PREFIX.gin > PREFIX.got'
    discard_results_on_any_change = True
    default_parameters = dict(
        keywords='conp gradients',
        options=[],
        shel=[],
        library="ffsioh.lib",
        conditions=None)

    def get_optimizer(self, atoms):
        gulp_keywords = self.parameters.keywords.split()
        if 'opti' not in gulp_keywords:
            raise ValueError('Can only create optimizer from GULP calculator '
                             'with "opti" keyword.  Current keywords: {}'
                             .format(gulp_keywords))

        opt = GULPOptimizer(atoms, self)
        return opt

    def __init__(self, restart=None,
                 ignore_bad_restart_file=FileIOCalculator._deprecated,
                 label='gulp', atoms=None, optimized=None,
                 Gnorm=1000.0, steps=1000, conditions=None, **kwargs):
        """Construct GULP-calculator object."""
        FileIOCalculator.__init__(self, restart, ignore_bad_restart_file,
                                  label, atoms, **kwargs)
        self.optimized = optimized
        self.Gnorm = Gnorm
        self.steps = steps
        self.conditions = conditions
        self.library_check()
        self.atom_types = []

        # GULP prints the fractional coordinates before the Final
        # lattice vectors so they need to be stored and then atoms
        # positions need to be set after we get the Final lattice
        # vectors
        self.fractional_coordinates = None

    def write_input(self, atoms, properties=None, system_changes=None):
        FileIOCalculator.write_input(self, atoms, properties, system_changes)
        p = self.parameters

        # Build string to hold .gin input file:
        s = p.keywords
        s += '\ntitle\nASE calculation\nend\n\n'

        if all(self.atoms.pbc):
            cell_params = self.atoms.cell.cellpar()
            # Formating is necessary since Gulp max-line-length restriction
            s += 'cell\n{:9.6f} {:9.6f} {:9.6f} ' \
                 '{:8.5f} {:8.5f} {:8.5f}\n'.format(*cell_params)
            s += 'frac\n'
            coords = self.atoms.get_scaled_positions()
        else:
            s += 'cart\n'
            coords = self.atoms.get_positions()

        if self.conditions is not None:
            c = self.conditions
            labels = c.get_atoms_labels()
            self.atom_types = c.get_atom_types()
        else:
            labels = self.atoms.get_chemical_symbols()

        for xyz, symbol in zip(coords, labels):
            s += ' {:2} core' \
                 ' {:10.7f}  {:10.7f}  {:10.7f}\n' .format(symbol, *xyz)
            if symbol in p.shel:
                s += ' {:2} shel' \
                     ' {:10.7f}  {:10.7f}  {:10.7f}\n' .format(symbol, *xyz)

        if p.library:
            s += f'\nlibrary {p.library}\n'

        if p.options:
            for t in p.options:
                s += f'{t}\n'

        gin_path = os.path.join(self.directory, self.prefix + '.gin')
        with open(gin_path, 'w') as fd:
            fd.write(s)

    def read_results(self):
        FileIOCalculator.read(self, self.label)
        got_path = os.path.join(self.directory, self.label + '.got')
        if not os.path.isfile(got_path):
            raise ReadError

        with open(got_path) as fd:
            lines = fd.readlines()

        cycles = -1
        self.optimized = None
        for i, line in enumerate(lines):
            m = re.match(r'\s*Total lattice energy\s*=\s*(\S+)\s*eV', line)
            if m:
                energy = float(m.group(1))
                self.results['energy'] = energy
                self.results['free_energy'] = energy

            elif line.find('Optimisation achieved') != -1:
                self.optimized = True

            elif line.find('Final Gnorm') != -1:
                self.Gnorm = float(line.split()[-1])

            elif line.find('Cycle:') != -1:
                cycles += 1

            elif line.find('Final Cartesian derivatives') != -1:
                s = i + 5
                forces = []
                while True:
                    s = s + 1
                    if lines[s].find("------------") != -1:
                        break
                    if lines[s].find(" s ") != -1:
                        continue
                    g = lines[s].split()[3:6]
                    G = [-float(x) * eV / Ang for x in g]
                    forces.append(G)
                forces = np.array(forces)
                self.results['forces'] = forces

            elif line.find('Final internal derivatives') != -1:
                s = i + 5
                forces = []
                while True:
                    s = s + 1
                    if lines[s].find("------------") != -1:
                        break
                    g = lines[s].split()[3:6]

                    # Uncomment the section below to separate the numbers when
                    # there is no space between them, in the case of long
                    # numbers. This prevents the code to break if numbers are
                    # too big.

                    '''for t in range(3-len(g)):
                        g.append(' ')
                    for j in range(2):
                        min_index=[i+1 for i,e in enumerate(g[j][1:])
                                   if e == '-']
                        if j==0 and len(min_index) != 0:
                            if len(min_index)==1:
                                g[2]=g[1]
                                g[1]=g[0][min_index[0]:]
                                g[0]=g[0][:min_index[0]]
                            else:
                                g[2]=g[0][min_index[1]:]
                                g[1]=g[0][min_index[0]:min_index[1]]
                                g[0]=g[0][:min_index[0]]
                                break
                        if j==1 and len(min_index) != 0:
                            g[2]=g[1][min_index[0]:]
                            g[1]=g[1][:min_index[0]]'''

                    G = [-float(x) * eV / Ang for x in g]
                    forces.append(G)
                forces = np.array(forces)
                self.results['forces'] = forces

            elif line.find('Final cartesian coordinates of atoms') != -1:
                s = i + 5
                positions = []
                while True:
                    s = s + 1
                    if lines[s].find("------------") != -1:
                        break
                    if lines[s].find(" s ") != -1:
                        continue
                    xyz = lines[s].split()[3:6]
                    XYZ = [float(x) * Ang for x in xyz]
                    positions.append(XYZ)
                positions = np.array(positions)
                self.atoms.set_positions(positions)

            elif line.find('Final stress tensor components') != -1:
                res = [0., 0., 0., 0., 0., 0.]
                for j in range(3):
                    var = lines[i + j + 3].split()[1]
                    res[j] = float(var)
                    var = lines[i + j + 3].split()[3]
                    res[j + 3] = float(var)
                stress = np.array(res)
                self.results['stress'] = stress

            elif line.find('Final Cartesian lattice vectors') != -1:
                lattice_vectors = np.zeros((3, 3))
                s = i + 2
                for j in range(s, s + 3):
                    temp = lines[j].split()
                    for k in range(3):
                        lattice_vectors[j - s][k] = float(temp[k])
                self.atoms.set_cell(lattice_vectors)
                if self.fractional_coordinates is not None:
                    self.fractional_coordinates = np.array(
                        self.fractional_coordinates)
                    self.atoms.set_scaled_positions(
                        self.fractional_coordinates)

            elif line.find('Final fractional coordinates of atoms') != -1:
                s = i + 5
                scaled_positions = []
                while True:
                    s = s + 1
                    if lines[s].find("------------") != -1:
                        break
                    if lines[s].find(" s ") != -1:
                        continue
                    xyz = lines[s].split()[3:6]
                    XYZ = [float(x) for x in xyz]
                    scaled_positions.append(XYZ)
                self.fractional_coordinates = scaled_positions

        self.steps = cycles

    def get_opt_state(self):
        return self.optimized

    def get_opt_steps(self):
        return self.steps

    def get_Gnorm(self):
        return self.Gnorm

    def library_check(self):
        if self.parameters['library'] is not None:
            if 'GULP_LIB' not in self.cfg:
                raise RuntimeError("Be sure to have set correctly $GULP_LIB "
                                   "or to have the force field library.")


class Conditions:
    """Atomic labels for the GULP calculator.

    This class manages an array similar to
    atoms.get_chemical_symbols() via get_atoms_labels() method, but
    with atomic labels in stead of atomic symbols.  This is useful
    when you need to use calculators like GULP or lammps that use
    force fields. Some force fields can have different atom type for
    the same element.  In this class you can create a set_rule()
    function that assigns labels according to structural criteria."""

    def __init__(self, atoms):
        self.atoms = atoms
        self.atoms_symbols = atoms.get_chemical_symbols()
        self.atoms_labels = atoms.get_chemical_symbols()
        self.atom_types = []

    def min_distance_rule(self, sym1, sym2,
                          ifcloselabel1=None, ifcloselabel2=None,
                          elselabel1=None, max_distance=3.0):
        """Find pairs of atoms to label based on proximity.

        This is for, e.g., the ffsioh or catlow force field, where we
        would like to identify those O atoms that are close to H
        atoms.  For each H atoms, we must specially label one O atom.

        This function is a rule that allows to define atom labels (like O1,
        O2, O_H etc..)  starting from element symbols of an Atoms
        object that a force field can use and according to distance
        parameters.

        Example:
        atoms = read('some_xyz_format.xyz')
        a = Conditions(atoms)
        a.set_min_distance_rule('O', 'H', ifcloselabel1='O2',
                                ifcloselabel2='H', elselabel1='O1')
        new_atoms_labels = a.get_atom_labels()

        In the example oxygens O are going to be labeled as O2 if they
        are close to a hydrogen atom othewise are labeled O1.

        """

        if ifcloselabel1 is None:
            ifcloselabel1 = sym1
        if ifcloselabel2 is None:
            ifcloselabel2 = sym2
        if elselabel1 is None:
            elselabel1 = sym1

        # self.atom_types is a list of element types  used instead of element
        # symbols in orger to track the changes made. Take care of this because
        # is very important.. gulp_read function that parse the output
        # has to know which atom_type it has to associate with which
        # atom_symbol
        #
        # Example: [['O','O1','O2'],['H', 'H_C', 'H_O']]
        # this because Atoms oject accept only atoms symbols
        self.atom_types.append([sym1, ifcloselabel1, elselabel1])
        self.atom_types.append([sym2, ifcloselabel2])

        dist_mat = self.atoms.get_all_distances()
        index_assigned_sym1 = []
        index_assigned_sym2 = []

        for i in range(len(self.atoms_symbols)):
            if self.atoms_symbols[i] == sym2:
                dist_12 = 1000
                index_assigned_sym2.append(i)
                for t in range(len(self.atoms_symbols)):
                    if (self.atoms_symbols[t] == sym1
                        and dist_mat[i, t] < dist_12
                            and t not in index_assigned_sym1):
                        dist_12 = dist_mat[i, t]
                        closest_sym1_index = t
                index_assigned_sym1.append(closest_sym1_index)

        for i1, i2 in zip(index_assigned_sym1, index_assigned_sym2):
            if dist_mat[i1, i2] > max_distance:
                raise ValueError('Cannot unambiguously apply minimum-distance '
                                 'rule because pairings are not obvious.  '
                                 'If you wish to ignore this, then increase '
                                 'max_distance.')

        for s in range(len(self.atoms_symbols)):
            if s in index_assigned_sym1:
                self.atoms_labels[s] = ifcloselabel1
            elif s not in index_assigned_sym1 and self.atoms_symbols[s] == sym1:
                self.atoms_labels[s] = elselabel1
            elif s in index_assigned_sym2:
                self.atoms_labels[s] = ifcloselabel2

    def get_atom_types(self):
        return self.atom_types

    def get_atoms_labels(self):
        labels = np.array(self.atoms_labels)
        return labels
