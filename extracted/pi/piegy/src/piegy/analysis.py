'''
This file contains pre-processing, post-processing, and analytical tools for simulations.

Public Funcions:
- check_convergence:    Check whether a simulation result converges. i.e. whether U, V's fluctuation are very small.
- combine_mod:          Combine two model objects and return a new one (the first two unchanged).
                        Intended usage: say you have mod1, mod2 with same parameters except for sim_time, say 10 and 20.
                                        Then combine_mod takes a weighted average (with ratio 1:2) of results and return a new sim3.
                                        So that you now have sim3 with 30 sim_time.

Private Functions:
- rounds_expected:      Roughly calculates how many rounds are expected in a single simulation (which reflects runtime).
                        NOTE: Not well-developed. Not recommending to use.
- scale_maxtime:        Given two simulation objects, scale first one's maxtime towards the second, so that the two have the same expected rounds.
                        Intended to possibly decrease maxtime and save runtime.
                        NOTE: Not well-developed. Not recommending to use.

'''

from . import simulation as simulation
from . import figures as figures
from .tools import figure_tools as figure_t

import numpy as np
import math




def rounds_expected(mod):
    '''
    NOTE: Not well-developed. Not recommending to use.

    Predict how many rounds will run in single_test. i.e., how many for loops from time = 0 to mod.maxtime.
    Calculated based on expected_UV. 
    '''

    N = mod.N
    M = mod.M
    U_expected, V_expected = figures.UV_expected_val(mod)

    rates = []
    patch0 = None  # simulate patch i, j
    patch0_nb = []  # simulate neighbors of patch i, j
    
    # loop through N, M, create a sample patch to calculate rates, store them
    for i in range(N):
        for j in range(M):
            patch0 = simulation.patch(U_expected[i][j], V_expected[i][j], mod.matrices[i][j], mod.patch_params[i][j])

            nb_indices = None
            if mod.boundary:
                nb_indices = simulation.find_nb_zero_flux(N, M, i, j)
            else:
                nb_indices = simulation.find_nb_periodical(N, M, i, j)
            
            for k in range(4):
                if nb_indices[k] != None:
                    i_nb = nb_indices[k][0]
                    j_nb = nb_indices[k][1]
                    patch0_nb_k = simulation.patch(U_expected[i_nb][j_nb], V_expected[i_nb][j_nb], mod.matrices[i_nb][j_nb], mod.patch_params[i_nb][j_nb])
                    patch0_nb_k.update_pi_k()
                    patch0_nb.append(patch0_nb_k)

                else:
                    patch0_nb.append(None)

            patch0.nb = patch0_nb
            patch0.update_pi_k()
            patch0.update_mig()

            rates += patch0.pi_death_rates
            rates += patch0.mig_rates
    
    delta_t_expected = (1 / sum(rates)) * math.log(1 / 0.5)
    r_expected = round(mod.maxtime / delta_t_expected)

    return r_expected




def scale_maxtime(mod1, mod2, scale_interval = True):
    '''
    NOTE: Not well-developed. Not recommending to use.

    Scale mod1's maxtime towards mod2's, so they will run similar number of rounds in single_test, and hence similar runtime.
    Intended to reduce the effect of changing params on runtime. 
    
    Input:
    - scale_interval decides whether to scale mod1's interval as well, so that the same number of data will be stored.
    '''

    r_expected1 = rounds_expected(mod1)
    r_expected2 = rounds_expected(mod2)
    ratio = r_expected2 / r_expected1

    new_maxtime = mod1.maxtime * ratio
    old_max_record = mod1.maxtime / mod1.interval

    if scale_interval:
        mod1.interval = new_maxtime / old_max_record

    mod1.change_maxtime(new_maxtime)




def check_convergence(mod, interval = 20, start = 0.8, fluc = 0.05):
    '''
    Check whether a simulation converges or not.
    Based on whether the fluctuation of U, V, pi all < 'fluc' in the later 'tail' portion of time.
    
    Essentially find the max and min values (of population) in every small interval, and then check whether their difference > min * fluc.

    Inputs:
    - sim: a simulation.model object
    - interval: int, how many records to take average over,
                and then compare this "local mean" with "whole-tail mean" and expect the difference to be less than fluc.
    - start: (0, 1) float, decides where you expect to check convergence from. Smaller start needs earlier convergence.
    - fluc: (0, 1) float. How much fluctuation is allowed between the average value of a small interval and the mean.
    '''

    if (start < 0) or (start > 1):
        raise ValueError("start should be a float in (0, 1)")
    if (fluc < 0) or (fluc > 1):
        raise ValueError("fluc should be a float in (0, 1)")
    if (type(interval) != int) or (interval < 1):
        raise ValueError("interval should be an int >= 1")
    
    interval = figure_t.scale_interval(interval, mod.compress_ratio)

    start_index = int(mod.max_record * start)  # where the tail starts
    num_interval = int((mod.max_record - start_index) / interval)  # how many intervals in total

    # find the max and min value of the small intervals 
    # initiate as average of the first interval
    min_U = np.mean(mod.U[:, :, start_index : start_index + interval])
    max_U = np.mean(mod.U[:, :, start_index : start_index + interval])
    min_V = np.mean(mod.V[:, :, start_index : start_index + interval])
    max_V = np.mean(mod.V[:, :, start_index : start_index + interval])

    for i in range(1, num_interval):
        # lower and upper bound of current interval
        lower = start_index + i * interval
        upper = lower + interval

        ave_U = np.mean(mod.U[:, :, lower : upper])
        ave_V = np.mean(mod.V[:, :, lower : upper])

        # Compare with min, max
        if ave_U > max_U:
            max_U = ave_U
        if ave_U < min_U:
            min_U = ave_U

        if ave_V > max_V:
            max_V = ave_V
        if ave_V < min_V:
            min_V = ave_V

        # check whether (max - min) > min * fluc
        if (max_U - min_U) > min_U * fluc:
            return False
        if (max_V - min_V) > min_V * fluc:
            return False
            
    return True




def combine_mod(mod1, mod2, force_combine = False):
    '''
    Combine data of mod1 and mod2. 
    Intended usage: assume mod1 and mod2 has the same N, M, maxtime, interval, boundary, max_record, and X, P
    combine_mod then combines the two results and calculate a new weighted average of the two data, return a new sim object. 
    Essentially allows breaking up many rounds of simulations into several smaller pieces, and then put together.

    Inputs:
    - mod1, mod2: both simulation.model objects. All input parameters the same except for sim_time, print_pct and seed.
            Raises error if not.
    - force_combine: ignore all parameter checks for mod1 and mod2 and combine the results of two models.

    Returns:

    - mod3:     a new model object whose U, V, Hpi, Dpi are weighted averages of mod1 and mod2
                (weighted by sim_time). 
                mod3.print_pct is set to mod1's, seed set to None, sim_time set to sum of mod1's and mod2's. All other params same as mod1
    '''

    if not force_combine:
        if not (mod1.N == mod2.N and
                mod1.M == mod2.M and
                mod1.maxtime == mod2.maxtime and
                mod1.record_itv == mod2.record_itv and
                mod1.boundary == mod2.boundary and
                mod1.max_record == mod2.max_record and
                mod1.compress_ratio == mod2.compress_ratio and
                np.array_equal(mod1.init_popu, mod2.init_popu) and
                np.array_equal(mod1.matrices, mod2.matrices) and
                np.array_equal(mod1.patch_params, mod2.patch_params)):
            
            raise ValueError('mod1 and mod2 have different input parameters (N, M, maxtime, interval, boundary, max_record, init_popu, matrices, or patch_params.)')

        if mod1.seed == mod2.seed:
            raise ValueError('Cannot combine two simulations with the same seed.')
    
    # copy mod1, except for no data and a different sim_time
    N = mod1.N
    M = mod1.M
    combined_sim_time = mod1.sim_time + mod2.sim_time
    mod3 = mod1.copy(copy_data = False)
    mod3.sim_time = combined_sim_time
    mod3.seed = None
    mod3.set_data(data_empty = False, max_record = mod1.max_record, compress_ratio = mod1.compress_ratio, 
                  U = np.zeros((N, M, mod1.max_record)), V = np.zeros((N, M, mod1.max_record)), 
                  Hpi = np.zeros((N, M, mod1.max_record)), Dpi = np.zeros((N, M, mod1.max_record)))

    for i in range(N):
        for j in range(M):
            for k in range(mod3.max_record):
                mod3.U[i][j][k] = (mod1.U[i][j][k] * mod1.sim_time + mod2.U[i][j][k] * mod2.sim_time) / combined_sim_time
                mod3.V[i][j][k] = (mod1.V[i][j][k] * mod1.sim_time + mod2.V[i][j][k] * mod2.sim_time) / combined_sim_time
                mod3.Hpi[i][j][k] = (mod1.Hpi[i][j][k] * mod1.sim_time + mod2.Hpi[i][j][k] * mod2.sim_time) / combined_sim_time
                mod3.Dpi[i][j][k] = (mod1.Dpi[i][j][k] * mod1.sim_time + mod2.Dpi[i][j][k] * mod2.sim_time) / combined_sim_time

    return mod3



