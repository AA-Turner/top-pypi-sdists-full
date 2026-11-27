from typing import IO

import numpy as np

from ase import Atoms
from ase.optimize.optimize import Optimizer
from ase.utils import deprecate_positionals


class MDMin(Optimizer):
    # default parameters
    defaults = {**Optimizer.defaults, 'dt': 0.2}

    @deprecate_positionals(2)
    def __init__(
        self,
        atoms: Atoms,
        restart: str | None = None,
        logfile: IO | str = '-',
        trajectory: str | None = None,
        dt: float | None = None,
        maxstep: float | None = None,
        **kwargs,
    ):
        """

        Parameters
        ----------
        atoms: :class:`~ase.Atoms`
            The Atoms object to relax.

        restart: str
            JSON file used to store hessian matrix. If set, file with
            such a name will be searched and hessian matrix stored will
            be used, if the file exists.

        trajectory: str
            Trajectory file used to store optimisation path.

        logfile: str
            Text file used to write summary information.

        dt: float
            Time step for integrating the equation of motion.

        maxstep: float
            Spatial step limit in Angstrom. This allows larger values of dt
            while being more robust to instabilities in the optimization.

        kwargs : dict, optional
            Extra arguments passed to
            :class:`~ase.optimize.optimize.Optimizer`.

        Examples
        --------

        >>> from ase import Atoms
        >>> from ase.optimize import MDMin
        >>> from ase.calculators.emt import EMT
        ...
        >>> system = Atoms(
        ... 'N2',
        ... positions = [(0.0, 0.0, 0.0), (0.0, 0.0, 1.1)],
        ... calculator=EMT()
        ... )
        >>> dyn = MDMin(system)
        >>> dyn.run(fmax=0.05) # doctest:+ELLIPSIS
               Step     Time          Energy          fmax
        MDMin:    0 ...        0.440344        3.251800
        MDMin:    1 ...        0.278778        1.160079
        MDMin:    2 ...        0.269160        0.689054
        MDMin:    3 ...        0.264472        0.368254
        MDMin:    4 ...        0.263357        0.211246
        MDMin:    5 ...        0.262951        0.117040
        MDMin:    6 ...        0.262833        0.066207
        MDMin:    7 ...        0.262795        0.037033
        ...
        """
        super().__init__(atoms, restart, logfile, trajectory, **kwargs)

        self.dt = dt or self.defaults['dt']
        self.maxstep = maxstep or self.defaults['maxstep']

    def initialize(self):
        self.v = None

    def read(self):
        self.v, self.dt = self.load()

    def step(self, forces=None):
        forces = -self._get_gradient(forces)

        optimizable = self.optimizable

        if self.v is None:
            self.v = np.zeros(optimizable.ndofs())
        else:
            self.v += 0.5 * self.dt * forces
            # Correct velocities:
            vf = np.vdot(self.v, forces)
            if vf < 0.0:
                self.v[:] = 0.0
            else:
                self.v[:] = forces * vf / np.vdot(forces, forces)

        self.v += 0.5 * self.dt * forces
        pos = optimizable.get_x()
        dpos = self.dt * self.v

        # For any dpos magnitude larger than maxstep, scaling
        # is <1. We add a small float to prevent overflows/zero-div errors.
        # All displacement vectors (rows) of dpos which have a norm larger
        # than self.maxstep are scaled to it.

        # XXX Here we are using gradient_norm() to get the norm of positions
        maxstep = self.optimizable.gradient_norm(dpos)
        scaling = self.maxstep / (1e-6 + maxstep)
        dpos *= np.clip(scaling, 0.0, 1.0)
        optimizable.set_x(pos + dpos)
        self.dump((self.v, self.dt))
