"""Velocity Verlet."""

from ase.md.md import MolecularDynamics


class VelocityVerlet(MolecularDynamics):
    """
    MD with NVE ensemble and velocity Verlet time integration.

    Notes
    -----
    The ``VelocityVerlet`` dynamics class implements the NVE ensemble.
    It requires two arguments, the atoms and the time step.  Choosing
    too large a time step will immediately be obvious, as the energy will
    increase with time, often very rapidly.

    A longer example is given in the tutorial :ref:`md_tutorial`.

    It is also possible to use :class:`ase.md.langevinbaoab.LangevinBAOAB`
    for NVE or NPH (variable cell) by running without a target temperature;
    see :ref:`langevin-baoab-description`.

    Example
    -------
    >>> from ase import units
    >>> from ase.build import bulk
    >>> from ase.calculators.emt import EMT
    >>> from ase.md.verlet import VelocityVerlet
    >>> atoms = bulk('Cu', cubic=True)
    >>> atoms.calc = EMT()
    >>> dyn = VelocityVerlet(atoms, timestep=5.0 * units.fs,
    ...                      trajectory='md.traj', logfile='md.log')
    >>> dyn.run(10)  # take 10 steps
    True
    """

    def step(self, forces=None):

        atoms = self.atoms

        if forces is None:
            forces = atoms.get_forces(md=True)

        p = atoms.get_momenta()
        p += 0.5 * self.dt * forces
        masses = atoms.get_masses()[:, None]
        r = atoms.get_positions()

        # if we have constraints then this will do the first part of the
        # RATTLE algorithm:
        atoms.set_positions(r + self.dt * p / masses)
        if atoms.constraints:
            p = (atoms.get_positions() - r) * masses / self.dt

        # We need to store the momenta on the atoms before calculating
        # the forces, as in a parallel Asap calculation atoms may
        # migrate during force calculations, and the momenta need to
        # migrate along with the atoms.
        atoms.set_momenta(p, apply_constraint=False)

        forces = atoms.get_forces(md=True)

        # Second part of RATTLE will be done here:
        atoms.set_momenta(atoms.get_momenta() + 0.5 * self.dt * forces)
        return forces
