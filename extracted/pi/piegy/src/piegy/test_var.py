'''
Test how certain variables influence simulation result.

Public Functions:

Test influence of one variable:
- test_var1:    Test how a certain patch variable (mu, w, kappa) influences results.
                Run simulations across different values of that variable and save data.
- var_UV1:      Plot how U, V change across different values of a specified variable.
- var_pi1:      Plot how Upi, V_pi change across different values of a specified variable.
                    

Test influence of two variables:
- test_var2:    Test how two patch variables influence results.
                Run simulations across different values of the two specified variables and save data.
- var_UV2:      Plot how U, V change across the two variables.
                x-axis is values of the variable 2, y-axis is U or V. Values of variable 1 are shown by multiple curves.
- var_pi2:      Plot how Upi & V_pi change across the two variables.


Additional tools (can be called directly):
- get_dirs1:   test_var1 returns directories in a certain format based on var and values. This function mimics that format and 
                        returns a 1D list of directories, where all data are stored.
                        This 1D list is intended to pass to var_UV1 and var_pi1 directly.
    
- var_convergence1: Find the simulatoin results of test_var1 that diverge.

- get_dirs2:   test_var2 returns directories in a certain format based on vars and values. This function mimics that format and
                    returns a 2D list of directories, where all data are stored.
                    This 2D list is intended to pass to var_UV2 and var_pi2 directly.
- var_convergence2: Find the simulatoin results of test_var2 that diverge.
'''

from . import simulation
from .tools import figure_tools as figure_t
from . import analysis as analysis
from . import data_tools as data_t

import matplotlib.pyplot as plt
import numpy as np



# curve type used by var_UV, var2_UV, var_pi, var2_pi
# can be 'o-', 'x-', ...
DOTTED_CURVE_TYPE = 'o-'

# map patch_var name to index in the patch class (in simulation.py)
PATCH_VAR_DICT = {'mu1': 0, 'mu2': 1, 'w1': 2, 'w2': 3, 'kappa1': 4, 'kappa2': 5}

# display name (in latex)
PATCH_VAR_DISP = {'mu1': r'$\mu_U$', 'mu2': r'$\mu_V$', 'w1': r'$w_U$', 'w2': r'$w_V$', 
                  'kappa1': r'$\kappa_U$', 'kappa2': r'$\kappa_V$'}



def test_var1(mod, var, values, dirs, compress_itv = None):
    '''
    Test the influence of one patch variable on simulation results.

    Inputs::
    - sim:                a simulation.model object. All tests will use parameters of mod, except for the variable to test.
    - var:                str, which patch variable to test. e.g. var can be 'mu1', 'w2', 'kappa2', ...
    - values:             1D np.array or list, what values of var to test.
    - dirs:               str, where to save data.
    - compress_itv:         int, whether to reduce data size (if not 1), passed to simulation.model.compress_data function.
    - predict_runtime:    bool, whether to predict how much time left for each test.          

    Returns::
    - var_dirs:           a 1D list of directories (str) where all the data are stored. 
                        Directories have form 'mu1=0.1'. 
                        NOTE: if you accidentally lost this return value, you can retrieve it by get_dirs1.
    '''

    if var not in PATCH_VAR_DICT.keys():
        raise ValueError('Please enter a valid patch variable: mu1, mu2, w1, w2, kappa1, or kappa2')

    # var_dirs is where data will be stored
    var_dirs = []
    
    for k in range(len(values)):
        sim2 = mod.copy(copy_data = False)
        current_var_str = var + '=' + str(values[k])    # e.g., 'mu1=0.1'
        var_dirs.append(dirs + '/' + current_var_str)
        
        for i in range(mod.N):
            for j in range(mod.M):
                sim2.P[i][j][PATCH_VAR_DICT[var]] = values[k]

        try:
            simulation.run(sim2, message = current_var_str + ', ')
            if compress_itv != None:
                sim2.compress_data(compress_itv)
            data_t.save(sim2, var_dirs[k], print_msg = False)
            del sim2
        except (OverflowError, RuntimeError):
            print(current_var_str + ' raised error, skipped')
            continue

    return var_dirs



def test_var2(mod, var1, var2, values1, values2, dirs, compress_itv = None):
    '''
    Two-variable version of test_var1. Test the influence of two varibles on simulation results.

    Inputs:
    - sim:      a simulation.model object. All tests will use the parameters of mod, except for the two vars to be tested.
    - var1:     str, the first variable to test.
    - var2:     str, the second variable to test.
    - values1:  1D list or np.array, values for var1.
    - values2:  1D list or np.array, values for var2.
    - dirs, compress_itv, scale_maxtime, predict_runtime: same as in test_var1

    Returns:
    - var_dirs:   2D list of directories, where all the data are stored.
                Directories have form 'mu1=0.1, mu2=0.2'.
                NOTE: if you accidentally lost this return value, you can retrieve by get_dirs2.
    '''

    if (var1 not in PATCH_VAR_DICT.keys()) or (var2 not in PATCH_VAR_DICT.keys()):
        raise ValueError('Please enter a valid patch variable: mu1, mu2, w1, w2, kappa1, or kappa2')

    var_dirs = [[] for k1 in range(len(values1))]

    for k1 in range(len(values1)):
        for k2 in range(len(values2)):
            sim2 = mod.copy(copy_data = False)
            current_var_str = var1 + '=' + str(values1[k1]) + ', ' + var2 + '=' + str(values2[k2])   # e.g., mu1=0.1, mu2=0.2
            var_dirs[k1].append(dirs + '/' + current_var_str)

            for i in range(mod.N):
                for j in range(mod.M):
                    sim2.P[i][j][PATCH_VAR_DICT[var1]] = values1[k1]
                    sim2.P[i][j][PATCH_VAR_DICT[var2]] = values2[k2]

            try:
                simulation.run(sim2, message = current_var_str + ', ')
                if compress_itv != None:
                    sim2.compress_data(compress_itv)
                data_t.save(sim2, var_dirs[k1][k2], print_msg = False)
                del sim2
            except (OverflowError, RuntimeError):
                print(current_var_str + ' raised error, skipped')
                continue

    return var_dirs




def var_UV1(var, values, var_dirs, ax_U = None, ax_V = None, start = 0.95, end = 1.0, U_color = 'purple', V_color = 'green'):
    '''
    Plot function for test_var1, plot how var influences U, V population.
    Make U, V - var curve in two figures, with y-axis being total population at the end of simulations, x-axis being var's values.

    Inputs:
    - var:        str, which variable was tested.
    - values:     1D list or np.array, which values were tested.
    - var_dirs:   return value of test_var1, a 1D list of directories where all data are stored.
    - ax_U, ax_V:   matplotlib axes to plot on.
    - start, end: floats, give an interval of time over which to take average and make plot.
                For example, start = 0.95, end = 1.0 are to take average over the last 5% time of results; 
                essentially plots how var influences equilibrium population.
    
    Returns:
    - ax_U, ax_V: axes for U, V, respectively.
    '''

    # average value of U, V over the interval. One entry for one value of var
    U_ave = []
    V_ave = []
    values = sorted(values)

    for k in range(len(var_dirs)):
        try:
            simk = data_t.load(var_dirs[k])
        except FileNotFoundError:
            print(var + '=' + str(values[k]) + ' not found, skipped')
            U_ave.append(None)
            V_ave.append(None)
            continue
        start_index = int(simk.max_record * start)
        end_index = int(simk.max_record * end)
        NM = int(simk.N * simk.M)

        U_ave.append(sum(figure_t.ave_interval_1D(simk.U, start_index, end_index)) / NM)
        V_ave.append(sum(figure_t.ave_interval_1D(simk.V, start_index, end_index)) / NM)
        del simk
        
    #### plot ####
    if ax_U == None:
        _, ax_U = plt.subplots()
    if ax_V == None:
        _, ax_V = plt.subplots()
    var_disp = PATCH_VAR_DISP[var]
    
    ax_U.set_xlabel(var_disp)
    ax_U.set_ylabel('Population ' + r'$U$')
    ax_U.plot(values, U_ave, DOTTED_CURVE_TYPE, color = U_color)
    ax_U.set_title(figure_t.gen_title(var_disp + r'$\,-\,U$', start, end))
    
    ax_V.set_xlabel(var_disp)
    ax_V.set_ylabel('Population ' + r'$V$')
    ax_V.plot(values, V_ave, DOTTED_CURVE_TYPE, color = V_color)
    ax_V.set_title(figure_t.gen_title(var_disp + r'$\,-\,V$', start, end))
    
    return ax_U, ax_V




def var_UV2(var1, var2, values1, values2, var_dirs, ax_U = None, ax_V = None, var1_on_xaxis = True, start = 0.95, end = 1.0, U_color = 'viridis', V_color = 'viridis', rgb_alpha = 1):
    '''
    Plot function for test_var2, plot how two variables influence U, V population.
    Make U, V - var1, var2 curves. y-axis is population, x-axis is var2's values, 
    and var1's values are represented by different curves, one curve corresponds to one value of var1.

    Inputs:
    - var1:       str, the first variable tested.
    - var2:       str, the second variable tested.
    - values1:    1D list or np.array, values for var1.
    - values2:    1D list or np.array, values for var2.
    - var_dirs:   return value of test_var2, a 2D list of directories where all data are stored.
    - ax_U, ax_V:   matplotlib axes to plot on.
    - var1_on_xaxis:    whether to put var1 on x-axis. Set to False if not.
    - start, end: floats, give an interval of time over which to take average and make plot.
                For example, start = 0.95, end = 1.0 plots the near-end population (equilibrium, if converged).
    - color:      str, what colors to use for different value of var1. Uses Matplotlib color maps. 
                See available color maps at: https://matplotlib.org/stable/users/explain/colors/colormaps.html
    - rgb_alpha:  the alpha value for color. Thr curves might have overlaps, recommend set a small alpha value if so.
    
    Returns:
    - ax_U, ax_V: axes for U, V, respectively.
    '''

    # average value of U, V over the interval. One entry for one values of var1, var2
    U_ave = [[] for k1 in range(len(var_dirs))]
    V_ave = [[] for k1 in range(len(var_dirs))]
    values1 = sorted(values1)
    values2 = sorted(values2)

    for k1 in range(len(var_dirs)):
        for k2 in range(len(var_dirs[k1])):
            try:
                simk = data_t.load(var_dirs[k1][k2])
            except FileNotFoundError:
                print(var1 + '=' + str(values1[k1]) + ', ' + var2 + '=' + str(values2[k2]) + ' not found, skipped')
                U_ave[k1].append(None)
                V_ave[k1].append(None)
                continue
            start_index = int(simk.max_record * start)
            end_index = int(simk.max_record * end)
            NM = int(simk.N * simk.M)

            U_ave[k1].append(sum(figure_t.ave_interval_1D(simk.U, start_index, end_index)) / NM)
            V_ave[k1].append(sum(figure_t.ave_interval_1D(simk.V, start_index, end_index)) / NM)
            del simk

    U_ave = np.array(U_ave)
    V_ave = np.array(V_ave)
    
    #### plot ####
    if ax_U == None:
        _, ax_U = plt.subplots()
    if ax_V == None:
        _, ax_V = plt.subplots()

    var1_disp = PATCH_VAR_DISP[var1]
    var2_disp = PATCH_VAR_DISP[var2]
    

    cmap_U = plt.get_cmap(U_color)
    if var1_on_xaxis:
        for k in range(len(values2)):
            label = var2_disp + '=' + str(values2[k])
            color_k = cmap_U(k / len(values2))[:3] + (rgb_alpha,)
            ax_U.plot(values1, U_ave[:, k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_U.set_xlabel(var1_disp)
    else:
        for k in range(len(values1)):
            label = var1_disp + '=' + str(values1[k])
            color_k = cmap_U(k / len(values1))[:3] + (rgb_alpha,)
            ax_U.plot(values2, U_ave[k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_U.set_xlabel(var2_disp)
    ax_U.set_ylabel('Population ' + r'$U$')
    ax_U.set_title(figure_t.gen_title(var1_disp + ',' + var2_disp + r'$\,-\,U$', start, end))
    ax_U.legend()
    
    cmap_V = plt.get_cmap(V_color)
    if var1_on_xaxis:
        for k in range(len(values2)):
            label = var2_disp + '=' + str(values2[k])
            color_k = cmap_V(k / len(values2))[:3] + (rgb_alpha,)
            ax_V.plot(values1, V_ave[:, k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_V.set_xlabel(var1_disp)
    else:
        for k in range(len(values1)):
            label = var1_disp + '=' + str(values1[k])
            color_k = cmap_V(k / len(values1))[:3] + (rgb_alpha,)
            ax_V.plot(values2, V_ave[k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_V.set_xlabel(var2_disp)
    ax_V.set_ylabel('Population ' + r'$V$')
    ax_V.set_title(figure_t.gen_title(var1_disp + ',' + var2_disp + r'$\,-\,V$', start, end))
    ax_V.legend()
    
    return ax_U, ax_V



def var_pi1(var, values, var_dirs, ax_U = None, ax_V = None, start = 0.95, end = 1.0, U_color = 'violet', V_color  = 'yellowgreen'):
    '''
    Plot function for test_var1. Plot influence of var on U, V's payoff.
    Make Upi, V_pi - var curves. y-axis is payoff, x-axis is values of var.

    Inputs:
    - var_dirs:   return value of test_var1. A 1D list of directories where all data are stored.
    - var:        str, which variable as tested.
    - values:     1D list or np.array, what values were used.
    - ax_U, ax_V:   matplotlib axes to plot on.
    - start, end: floats, define an interval of time over which to calculate average payoff and make plots.
    
    Returns:
    - ax_U, ax_V: axes for U, V, respectively.
    '''
    
    # take average value of payoff over an interval of time
    U_ave = []
    V_ave = []
    values = sorted(values)
    
    for k in range(len(var_dirs)):
        try:
            simk = data_t.load(var_dirs[k])
        except FileNotFoundError:
            print(var + '=' + str(values[k]) + ' not found, skipped')
            U_ave.append(None)
            V_ave.append(None)
            continue
        start_index = int(simk.max_record * start)
        end_index = int(simk.max_record * end)
        NM = int(simk.N * simk.M)

        U_ave.append(np.sum(figure_t.ave_interval(simk.Upi, start_index, end_index)) / NM)
        V_ave.append(np.sum(figure_t.ave_interval(simk.Vpi, start_index, end_index)) / NM)
        del simk
            
    #### plot ####
    if ax_U == None:
        _, ax_U = plt.subplots()
    if ax_V == None:
        _, ax_V = plt.subplots()
    var_disp = PATCH_VAR_DISP[var]
    
    ax_U.set_xlabel(var_disp)
    ax_U.set_ylabel('Payoff ' + r'$p_H$')
    ax_U.plot(values, U_ave, DOTTED_CURVE_TYPE, color = U_color)
    ax_U.set_title(figure_t.gen_title(var_disp + r'$\,-\,p_U$', start, end))
    
    ax_V.set_xlabel(var_disp)
    ax_V.set_ylabel('Payoff ' + r'$p_D$')
    ax_V.plot(values, V_ave, DOTTED_CURVE_TYPE, color = V_color)
    ax_V.set_title(figure_t.gen_title(var_disp  + r'$\,-\,p_V$', start, end))

    return ax_U, ax_V




def var_pi2(var1, var2, values1, values2, var_dirs, ax_U = None, ax_V = None, var1_on_xaxis = True, start = 0.95, end = 1.0, U_color = 'viridis', V_color = 'viridis', rgb_alpha = 1):
    '''
    Plot function for test_var2. Plot how var1 and var2 influence payoff.
    Make Upi, V_pi - var2 curves. y-axis is payoff, x-axis is values of var2,
    var1 is represented by different curves. One curve corresponds to one value of var1.

    Inputs:
    - var_dirs:           return value of test_var2. A 2D list of directories where all data are stored.
    - var1, var2:         str, what variables were tested.
    - values1, values2:   1D lists or np.array, what values were tested.
    - ax_U, ax_V:           matplotlib axes to plot on.
    - var1_on_xaxis:    whether to put var1 on x-axis. Set to False if not.
    - start, end:         floats, define a time inteval over which to make average and make plots.
    - color:              str, Matplotlib color maps.
    - rgb_alpha:          set alpha value for curves.
    
    Returns:
    - ax_U, ax_V:         U, V's payoff figures, respectively.
    '''
    
    # take average value of payoff over an interval of time
    U_ave = [[] for k1 in range(len(var_dirs))]
    V_ave = [[] for k1 in range(len(var_dirs))]
    values1 = sorted(values1)
    values2 = sorted(values2)

    for k1 in range(len(var_dirs)):
        for k2 in range(len(var_dirs[k1])):
            try:
                simk = data_t.load(var_dirs[k1][k2])
            except FileNotFoundError:
                print(var1 + '=' + str(values1[k1]) + ', ' + var2 + '=' + str(values2[k2]) + ' not found, skipped')
                U_ave[k1].append(None)
                V_ave[k1].append(None)
                continue
            start_index = int(simk.max_record * start)
            end_index = int(simk.max_record * end)
            NM = int(simk.N * simk.M)

            U_ave[k1].append(np.sum(figure_t.ave_interval(simk.Upi, start_index, end_index)) / NM)
            V_ave[k1].append(np.sum(figure_t.ave_interval(simk.Vpi, start_index, end_index)) / NM)
            del simk

    U_ave = np.array(U_ave)
    V_ave = np.array(V_ave)
    
    #### plot ####
    if ax_U == None:
        _, ax_U = plt.subplots()
    if ax_V == None:
        _, ax_V = plt.subplots()

    var1_disp = PATCH_VAR_DISP[var1]
    var2_disp = PATCH_VAR_DISP[var2]
    
    cmap_U = plt.get_cmap(U_color)
    if var1_on_xaxis:
        for k in range(len(values2)):
            label = var2_disp + '=' + str(values2[k])
            color_k = cmap_U(k / len(values2))[:3] + (rgb_alpha,)
            ax_U.plot(values1, U_ave[:, k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_U.set_xlabel(var1_disp)
    else:
        for k in range(len(values1)):
            label = var1_disp + '=' + str(values1[k])
            color_k = cmap_U(k / len(values1))[:3] + (rgb_alpha,)
            ax_U.plot(values2, U_ave[k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_U.set_xlabel(var2_disp)
    ax_U.set_ylabel('Payoff ' + r'$p_{V}$')
    ax_U.set_title(figure_t.gen_title(var1_disp + ',' + var2_disp + r'$\,-\,p_U$', start, end))
    ax_U.legend()
    
    cmap_V = plt.get_cmap(V_color)
    if var1_on_xaxis:
        for k in range(len(values2)):
            label = var2_disp + '=' + str(values2[k])
            color_k = cmap_V(k / len(values2))[:3] + (rgb_alpha,)
            ax_V.plot(values1, V_ave[:, k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_V.set_xlabel(var1_disp)
    else:
        for k in range(len(values1)):
            label = var1_disp + '=' + str(values1[k])
            color_k = cmap_V(k / len(values1))[:3] + (rgb_alpha,)
            ax_V.plot(values2, V_ave[k], DOTTED_CURVE_TYPE, label = label, color = color_k)
            ax_V.set_xlabel(var2_disp)
    ax_V.set_ylabel('Payoff ' + r'$p_{U}$')
    ax_V.set_title(figure_t.gen_title(var1_disp + ',' + var2_disp + r'$\,-\,p_V$', start, end))
    ax_V.legend()
    
    return ax_U, ax_V




def get_dirs1(var, values, dirs):
    '''
    Mimics the return value format of test_var1 and returns a 1D list of directories where test_var1 saved data.
    Intended usage: retrieve the directories if you accidentally lost the return value of test_var1.

    Inputs:
    - var:        what variable was tested.
    - values:     what values were testsed.
    - dirs:  the directory you passed to test_var1 as 'dirs' parameter. 
                Essentially the root directories where data were stored.

    Returns:
    - var_dirs:   a 1D list of directories where data were stored. Has the same format as the return value of test_var1.
    '''

    var_dirs = []
    values_sorted = sorted(values)
    if dirs[-1] != '/':
        dirs += '/'

    for val in values_sorted:
            var_dirs.append(dirs + var + '=' + str(val))

    return var_dirs




def var_convergence1(var_dirs, interval = 20, start = 0.8, fluc = 0.07):
    '''
    Find the simulatoin results of test_var1 that diverge. 

    Inputs:
    - var_dirs:       Return value of test_var1
    - interval:       int. One of the inputs of analysis.check_convergence.
                    The size of interval to take average over.
    - start:          (0,1) float. One of the inputs of analysis.check_convergence. 
                    Convergence is expected to start from at least this point.
    - fluc:           (0,1) float. One of the inputs of analysis.check_convergence. 
                    Expect the difference between any two small intervals (a quotient-form difference) should be less than fluc.

    Returns:
    - diverge_list:   A list directories where the simulation data diverge.
    '''

    diverge_list = []

    for k in range(len(var_dirs)):
        dirs = var_dirs[k]
        try:
            simk = data_t.load(dirs)
        except FileNotFoundError:
            print(dirs + ' data not found, skipped')
            continue
        if not analysis.check_convergence(simk, interval, start, fluc):
            diverge_list.append(dirs)
        del simk

    return diverge_list




def get_dirs2(var1, var2, values1, values2, dirs):
    '''
    Mimics the return value format of test_var2 and returns a 2D list of directories where test_var2 saved data.
    Intended usage: retrieve the directories if you accidentally lost the return value of test_var2.

    Inputs:
    - var1, var2:         what variables were tested.
    - values1, values2:   what values were testsed.
    - dirs:          the directory you passed to test_var2 as 'dirs' parameter. 
                        Essentially the root directories where data were stored.

    Returns:
    - var_dirs:   a 2D list of directories where data were stored. Has the same format as the return value of test_var2.
    '''

    var_dirs = [[] for i in range(len(values1))]
    values1_sorted = sorted(values1)
    values2_sorted = sorted(values2)
    if dirs[-1] != '/':
        dirs += '/'

    for i in range(len(values1)):
        for j in range(len(values2)):
            v1 = values1_sorted[i]
            v2 = values2_sorted[j]
            dirs_ij = dirs + var1 + '=' + str(v1) + ', ' + var2 + '=' + str(v2)
            var_dirs[i].append(dirs_ij)

    return var_dirs




def var_convergence2(var_dirs, interval = 20, start = 0.8, fluc = 0.07):
    '''
    Find the simulatoin results of test_var2 that diverge.

    Inputs:
    - var_dirs:       Return value of test_var2
    - interval:       int. One of the inputs of analysis.check_convergence.
                    The size of interval to take average over.
    - start:          (0,1) float. One of the inputs of analysis.check_convergence. 
                    Convergence is expected to start from at least this point.
    - fluc:           (0,1) float. One of the inputs of analysis.check_convergence. 
                    Expect the difference between any two small intervals (a quotient-form difference) should be less than fluc.

    Returns:
    - diverge_list:   A list directories where the simulation data diverge.
    '''

    diverge_list = []

    for sublist in var_dirs:
        for k in range(len(sublist)):
            dirs = sublist[k]
            try:
                simk = data_t.load(dirs)
            except FileNotFoundError:
                print(dirs + ' data not found, skipped')
                continue
            if not analysis.check_convergence(simk, interval, start, fluc):
                diverge_list.append(dirs)
            del simk

    return diverge_list



