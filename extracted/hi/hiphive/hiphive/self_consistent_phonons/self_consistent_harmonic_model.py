import numpy as np
from hiphive.force_constant_model import ForceConstantModel
from hiphive import StructureContainer
from hiphive.utilities import prepare_structures
from hiphive.structure_generation import generate_rattled_structures, \
                                         generate_phonon_rattled_structures
from trainstation import Optimizer


def self_consistent_harmonic_model(atoms_ideal, calc, cs, T, alpha,
                                   n_iterations, n_structures,
                                   QM_statistics=False, parameters_start=None,
                                   imag_freq_factor=1.0, fit_kwargs={}):
    """
    Constructs a set of self-consistent second-order force constants
    that provides the closest match to the potential energy surface at
    a the specified temperature.

    Parameters
    ----------
    atoms_ideal : ase.Atoms
        ideal structure
    calc : ASE calculator object
        `calculator
        <https://wiki.fysik.dtu.dk/ase/ase/calculators/calculators.html>`_
        to be used as reference potential
    cs : ClusterSpace
        clusterspace onto which to project the reference potential
    T : float
        temperature in K
    alpha : float
        stepsize in optimization algorithm
    n_iterations : int
        number of iterations in poor mans
    n_structures : int
        number of structures to use when fitting
    QM_statistics : bool
        if the amplitude of the quantum harmonic oscillator shoule be used
        instead of the classical amplitude in the phonon rattler
    parameters_start : numpy.ndarray
        parameters from which to start the optimization
    image_freq_factor: float
        If a squared frequency, w2, is negative then it is set to
        w2 = imag_freq_factor * np.abs(w2)
    fit_kwargs : dict
        kwargs to be used in the fitting process (via Optimizer)

    Returns
    -------
    list(numpy.ndarray)
        sequence of parameter vectors generated while iterating to
        self-consistency
    """

    if not 0 < alpha <= 1:
        raise ValueError('alpha must be between 0.0 and 1.0')

    if max(cs.cutoffs.orders) != 2:
        raise ValueError('ClusterSpace must be second order')

    # initialize things
    sc = StructureContainer(cs)
    fcm = ForceConstantModel(atoms_ideal, cs)

    # generate initial model
    if parameters_start is None:
        print('Creating initial model')
        rattled_structures = generate_rattled_structures(atoms_ideal, n_structures, 0.03)
        rattled_structures = prepare_structures(rattled_structures, atoms_ideal, calc, False)
        for structure in rattled_structures:
            sc.add_structure(structure)
        opt = Optimizer(sc.get_fit_data(), train_size=1.0, **fit_kwargs)
        opt.train()
        parameters_start = opt.parameters
        sc.delete_all_structures()

    # run poor mans self consistent
    parameters_old = parameters_start.copy()
    parameters_traj = [parameters_old]

    for i in range(n_iterations):
        # generate structures with old model
        print('Iteration {}'.format(i))
        fcm.parameters = parameters_old
        fc2 = fcm.get_force_constants().get_fc_array(order=2, format='ase')
        phonon_rattled_structures = generate_phonon_rattled_structures(
            atoms_ideal, fc2, n_structures, T, QM_statistics=QM_statistics,
            imag_freq_factor=imag_freq_factor)
        phonon_rattled_structures = prepare_structures(
            phonon_rattled_structures, atoms_ideal, calc, False)

        # fit new model
        for structure in phonon_rattled_structures:
            sc.add_structure(structure)
        opt = Optimizer(sc.get_fit_data(), train_size=1.0, **fit_kwargs)
        opt.train()
        sc.delete_all_structures()

        # update parameters
        parameters_new = alpha * opt.parameters + (1-alpha) * parameters_old

        # print iteration summary
        disps = [atoms.get_array('displacements') for atoms in phonon_rattled_structures]
        disp_ave = np.mean(np.abs(disps))
        disp_max = np.max(np.abs(disps))
        x_new_norm = np.linalg.norm(parameters_new)
        delta_x_norm = np.linalg.norm(parameters_old-parameters_new)
        print('    |x_new| = {:.5f}, |delta x| = {:.8f}, disp_ave = {:.5f}, disp_max = {:.5f}, '
              'rmse = {:.5f}'.format(x_new_norm, delta_x_norm, disp_ave, disp_max, opt.rmse_train))
        parameters_traj.append(parameters_new)
        parameters_old = parameters_new

    return parameters_traj
