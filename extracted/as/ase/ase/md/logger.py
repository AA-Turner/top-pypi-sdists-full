"""Logging for molecular dynamics."""

import weakref
from typing import IO, Any

from ase import Atoms, units
from ase.parallel import world
from ase.utils import IOContext


class MDLogger(IOContext):
    """Class for logging molecular dynamics simulations.

    A logging mechanism is provided, printing time; total, potential and
    kinetic energy; and temperature (calculated from the kinetic energy).
    It is enabled by giving the ``logfile`` argument when the dynamics
    object is created, ``logfile`` may be an open file, a filename or the
    string '-' meaning standard output.  By default, a line is printed
    for each timestep, specifying the ``loginterval`` argument will change
    this to a more reasonable frequency.

    The logging can be customized by explicitly attaching an
    :class:`MDLogger` to the dynamics object, see the example below.

    Parameters
    ----------
    dyn : :class:`~ase.md.md.MolecularDynamics`
        ASE :class:`~ase.md.md.MolecularDynamics` object.
        Only a weak reference is kept.
    atoms : :class:`~ase.Atoms`
        ASE :class:`~ase.Atoms` object.
    logfile : IO | str
        File name or open file, "-" meaning standard output.
    header : bool, default: :obj:`True`
        If :obj:`True`, a header line defining the columns is written when
        the logger is created.
    stress : bool, default: :obj:`False`
        If :obj:`True`, the logger also writes the six components of the
        stress tensor, in GPa.
    peratom : bool, default: :obj:`False`
        If :obj:`True`, the logger writes energies per atom instead of total
        energies.
    mode : str, default: ``'a'``
        If 'a', append to existing file, if 'w' overwrite
        existing file.
    comm : MPI communicator, default: :data:`ase.parallel.world`
        Only the process with rank 0 writes to the file.

    Notes
    -----
    Attaching a logger as in the example below does *not* create a cyclic
    reference to the dynamics object.

    If building your own logging class, be sure not to attach the dynamics
    object directly to the logging object. Instead, create a weak reference
    using the ``proxy`` method of the ``weakref`` package. See the
    :class:`MDLogger` source code for an example. (If this is not done, a
    cyclic reference may be created which can cause certain calculators
    to not terminate correctly.)

    Example
    -------
    Skip the header line and write energies per atom instead of total
    energies:

    >>> from ase import units
    >>> from ase.build import bulk
    >>> from ase.calculators.emt import EMT
    >>> from ase.md import MDLogger
    >>> from ase.md.verlet import VelocityVerlet
    >>> atoms = bulk('Cu', cubic=True)
    >>> atoms.calc = EMT()
    >>> dyn = VelocityVerlet(atoms, timestep=2 * units.fs)
    >>> dyn.attach(MDLogger(dyn, atoms, 'md.log', header=False, stress=False,
    ...            peratom=True, mode='a'), interval=1000)
    >>> dyn.run(10)  # take 10 steps
    True
    """

    def __init__(
        self,
        dyn: Any,  # not fully annotated so far to avoid a circular import
        atoms: Atoms,
        logfile: IO | str,
        header: bool = True,
        stress: bool = False,
        peratom: bool = False,
        mode: str = 'a',
        comm=world,
    ):
        self.dyn = weakref.proxy(dyn) if hasattr(dyn, 'get_time') else None
        self.atoms = atoms
        global_natoms = atoms.get_global_number_of_atoms()
        self.logfile = self.openfile(file=logfile, mode=mode, comm=comm)
        self.stress = stress
        self.peratom = peratom
        if self.dyn is not None:
            self.hdr = '%-9s ' % ('Time[ps]',)
            self.fmt = '%-10.4f '
        else:
            self.hdr = ''
            self.fmt = ''
        if self.peratom:
            self.hdr += '%12s %12s %12s  %6s' % (
                'Etot/N[eV]',
                'Epot/N[eV]',
                'Ekin/N[eV]',
                'T[K]',
            )
            self.fmt += '%12.4f %12.4f %12.4f  %6.1f'
        else:
            self.hdr += '%12s %12s %12s  %6s' % (
                'Etot[eV]',
                'Epot[eV]',
                'Ekin[eV]',
                'T[K]',
            )
            # Choose a sensible number of decimals
            if global_natoms <= 100:
                digits = 4
            elif global_natoms <= 1000:
                digits = 3
            elif global_natoms <= 10000:
                digits = 2
            else:
                digits = 1
            self.fmt += 3 * ('%%12.%df ' % (digits,)) + ' %6.1f'
        if self.stress:
            self.hdr += (
                '      ---------------------- stress [GPa] '
                '-----------------------'
            )
            self.fmt += 6 * ' %10.3f'
        self.fmt += '\n'
        if header:
            self.logfile.write(self.hdr + '\n')

    def __del__(self):
        self.close()

    def __call__(self):
        epot = self._potential_energy()
        ekin = self.atoms.get_kinetic_energy()
        temp = self.atoms.get_temperature()
        global_natoms = self.atoms.get_global_number_of_atoms()
        if self.peratom:
            epot /= global_natoms
            ekin /= global_natoms
        if self.dyn is not None:
            t = self.dyn.get_time() / (1000 * units.fs)
            dat = (t,)
        else:
            dat = ()
        dat += (epot + ekin, epot, ekin, temp)
        if self.stress:
            dat += tuple(self._stress() / units.GPa)
        self.logfile.write(self.fmt % dat)
        self.logfile.flush()

    def _potential_energy(self):
        return self.atoms.get_potential_energy()

    def _stress(self):
        return self.atoms.get_stress(include_ideal_gas=True)
