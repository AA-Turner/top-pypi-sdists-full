'''
Contains all the major plot functions. 

Plots for population:
- UV_hmap:       Used for 2D space (both N, M > 1), plot distribution of U, V in all patches within a specified time interval.
                    Average population over that interval is taken.
- UV_bar:           Used for 1D space (N or M == 1), counterpart of UV_hmap.
                    Plot average distribution of U, V in a specified time interval in a barplot.
- UV_dyna:         Plot change of total U, V overtime.
- UV_hist:          Make a histogram of U, V in a specified time interval.
- UV_std:           Plot change of standard deviation of U, V over time.
- UV_expected:      Calculate expected distribution of U, V based on matrices, assuming no migration.


Plots for payoff:
- pi_hmap:       Used for 2D space, plot distribution of Hpi & Dpiwithin a specified time interval.
                    Average payoff over that interval is taken.
- pi_bar:           Used for 1D space, counterpart of pi_hmap.
                    Plot average distribution of Hpi & Dpiin a specified time interval in a bar plot.
- pi_dyna:         Plot change of total Hpi, Dpiovertime.
- pi_hist:          Make a histogram of Hpi, Dpiin a specified time interval.
- pi_std:           Plot change of standard deviation of Hpi, Dpiover time.


Popu-payoff correlation:
- UV_pi:            Make two scatter plots: x-axes are U, V, y-axes are U's and V's payoff, in a specified time interval.
                    Reveals relationship between population and payoff.

'''


from .tools import figure_tools as figure_t
from . import simulation

import matplotlib.pyplot as plt
import numpy as np


# curve type in plot
# used by UV_dyna, UV_std, and pi_dyna
CURVE_TYPE = '-'

# default heatmap value range, which is None
DEFAULT_HMAP_DRANGE = (None, None)



def UV_hmap(mod, ax_H = None, ax_D = None, color_H = 'Purples', color_D = 'Greens', start = 0.95, end = 1.0, vrange_H = DEFAULT_HMAP_DRANGE, vrange_D = DEFAULT_HMAP_DRANGE):
    '''
    Makes two heatmaps for U, V average distribution over a time interval, respectively. Works best for 2D space.
    1D works as well, but figures look bad.

    Inputs:
        mod:        A simulation.model object.
        ax_H, ax_D: matplotlib axes to plot on. New axes will be created if None is given.
        color_H:    Color for U's heatmap, uses matplotlib color maps.
        color_D:    Color for V's heatmap.
        start:      (0,1) float, where the interval should start from. Intended as a 'percentage'. 
                    For example, start = 0.8 means the interval should start from the 80% point of mod.maxtime.
        end:        (0,1) float, where the interval ends.

    Returns:
        ax_H, ax_D: matplotlib axes with heatmaps of U, V distribution plotted upon.
    '''
    
    start_index = int(start * mod.max_record)
    end_index = int(end * mod.max_record)
    
    # see ave_interval below
    U_ave = figure_t.ave_interval(mod.U, start_index, end_index)
    V_ave = figure_t.ave_interval(mod.V, start_index, end_index)
    
    #### plot ####
    
    U_title = figure_t.gen_title('Popu U', start, end)
    U_text = figure_t.gen_text(np.mean(U_ave), np.std(U_ave))
    V_title = figure_t.gen_title('Popu V', start, end)
    V_text = figure_t.gen_text(np.mean(V_ave), np.std(V_ave))

    figure_t.hmap(U_ave, ax_H, color_H, U_title, U_text, vmin = vrange_H[0], vmax = vrange_H[1])
    figure_t.hmap(V_ave, ax_D, color_D, V_title, V_text, vmin = vrange_D[0], vmax = vrange_D[1])
        
    return ax_H, ax_D
    


def UV_bar(mod, ax_H = None, ax_D = None, color_H = 'purple', color_D = 'green', start = 0.95, end = 1.0):
    '''
    Makes two barplots for U, V average distribution over a time interval. Works best for 1D space.
    2D works as well, but figures look bad.

    Inputs:
        mod:        A simulation.model object.
        ax_H, ax_D: matplotlib axes to plot on. New axes will be created if None is given.
        color_H:    Color of U's barplot. Uses Matplotlib colors.
                    See available colors at: https://matplotlib.org/stable/gallery/color/named_colors.html
        color_D:    Color of V's barplot. Uses Matplotlib colors.
        start:      (0,1) float. How much proportion of mod.maxtime you want the interval to start from.
        end:        (0,1) float. Where you want the interval to end.

    Returns:
        ax_H, ax_D: matplotlib axes with bar plots for U and V plotted upon.
    '''
    
    start_index = int(start * mod.max_record)
    end_index = int(end * mod.max_record)
    
    U_ave = figure_t.ave_interval_1D(mod.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(mod.V, start_index, end_index)

    #### plot ####

    U_title = figure_t.gen_title('Population U', start, end)
    U_text = figure_t.gen_text(np.mean(U_ave), np.std(U_ave))
    V_title = figure_t.gen_title('Population V', start, end)
    V_text = figure_t.gen_text(np.mean(V_ave), np.std(V_ave))

    ax_H = figure_t.bar(U_ave, ax = ax_H, color = color_H, xlabel = 'patches', ylabel = 'U', title = U_title, text = U_text)
    ax_D = figure_t.bar(V_ave, ax = ax_D, color = color_D, xlabel = 'patches', ylabel = 'V', title = V_title, text = V_text)

    return ax_H, ax_D




def UV_dyna(mod, ax = None, interval = 20):
    '''
    Plots how total U, V change overtime.
    The curves are not directly based on every single data point. 
    Rather, it takes the average over many intervals of points to smooth out local fluctuations.
        For example, interval = 20 means the first point on the curves are based on the average value of data points 0~19.
        So if there are 2000 data points in total, then there will be 2000 / 20 = 100 points on the curves.

    Inputs:
        mod:        A simulation.model object.
        ax:         matplotlib ax to plot on. New ax will be created if None is given.
        interval:   How many data points to take average over. Larger value makes curves smoother, but also loses local fluctuations.
                    NOTE: this interval doesn't overlap with mod.compress_ratio. 
                    e.g. you already took average over every 20 data points, then using interval <= 20 here has no smoothing effect.
        grid:       Whether to add grid lines to plot.
    
    Returns:
        ax:        matplotlib ax, contains U's, V's, and sum of U & V population.
    '''
    
    # store the average values in lists
    H_curve = []
    D_curve = []
    total_curve = []

    interval = figure_t.scale_interval(interval, mod.compress_ratio)
    interval_num = int(mod.max_record / interval)
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(mod.U, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(mod.V, i * interval, (i + 1) * interval)
        
        H_curve.append(np.sum(U_ave))
        D_curve.append(np.sum(V_ave))
        total_curve.append(H_curve[-1] + D_curve[-1])
        
    #### plot ####   
    xaxis = np.linspace(0, mod.maxtime, len(H_curve))

    if ax == None:
        _, ax = plt.subplots()
    ax.plot(xaxis, H_curve, CURVE_TYPE, label = 'U')
    ax.plot(xaxis, D_curve, CURVE_TYPE, label = 'V')
    ax.plot(xaxis, total_curve, CURVE_TYPE, label = 'total')
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.set_title('Population U & V Over Time')
    ax.legend()

    return ax




def UV_hist(mod, ax_H = None, ax_D = None, color_H = 'purple', color_D = 'green', start = 0.95, end = 1.0):
    '''
    Makes density histograms for U, V's average distribution over an interval.
    Sometimes it may not be shown in density plots due to matplotlib features.

    Returns:
        ax_H, ax_D: matplotlib axes with heatmaps of U, V population density plotted upon.
    '''

    start_index = int(start * mod.max_record)
    end_index = int(end * mod.max_record)
    
    U_ave = figure_t.ave_interval_1D(mod.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(mod.V, start_index, end_index)
    
    #### plot ####
    
    if ax_H == None:
        _, ax_H = plt.subplots()
    ax_H.set_xlabel('Population U')
    ax_H.set_ylabel('Density')
    ax_H.hist(U_ave, color = color_H, density = True)
    ax_H.set_title(figure_t.gen_title('U Hist', start, end))
    
    if ax_D == None:
        _, ax_D = plt.subplots()
    ax_D.set_xlabel('Population V')
    ax_D.set_ylabel('Density')
    ax_D.hist(V_ave, color = color_D, density = True)
    ax_D.set_title(figure_t.gen_title('V Hist', start, end))

    return ax_H, ax_D




def UV_std(mod, ax = None, interval = 20):
    '''
    Plots how standard deviation of U, V change over time.
    Takes average over many small interval to smooth out local fluctuations.

    Returns:
        ax:    matplotlib ax, contains U's and V's std curves.
    '''

    interval = figure_t.scale_interval(interval, mod.compress_ratio)
    interval_num = int(mod.max_record / interval)
    
    U_std = []
    V_std = []
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(mod.U, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(mod.V, i * interval, (i + 1) * interval)
        
        U_std.append(np.std(U_ave))
        V_std.append(np.std(V_ave))
    
    #### plot ####
    xaxis = np.linspace(0, mod.maxtime, len(U_std))

    if ax == None:
        _, ax = plt.subplots()
    ax.plot(xaxis, U_std, CURVE_TYPE, label = 'U std')
    ax.plot(xaxis, V_std, CURVE_TYPE, label = 'V std')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Std Dev')
    ax.set_title('Population Std-Dev Dynamics')

    return ax



def UV_expected(mod, ax_H = None, ax_D = None, color_H = 'Purples', color_D = 'Greens', vrange_H = DEFAULT_HMAP_DRANGE, vrange_D = DEFAULT_HMAP_DRANGE):
    '''
    Calculate expected population distribution based on matrices, assuming no migration.
    For the formulas, see stochastic_mode.expected_HV

    Some Inputs:
        Note the colors are color maps.
    
    Returns:
    ax_H, ax_D: If 2D (N and M both > 1), then ax_H and ax_D are heatmaps.
                If 1D (N or M == 1), then ax_H and ax_D are barplots.
    '''
    
    U_expected, V_expected = simulation.UV_expected_val(mod)
    
    U_text = figure_t.gen_text(np.mean(U_expected), np.std(U_expected))
    V_text = figure_t.gen_text(np.mean(V_expected), np.std(V_expected))
    
    #### plot ####
    
    if (mod.N != 1) and (mod.M != 1):
        # 2D
        figure_t.hmap(U_expected, ax_H, color_H, title = 'Expected U', text = U_text, vmin = vrange_H[0], vmax = vrange_H[1])
        figure_t.hmap(V_expected, ax_D, color_D, title = 'Expected V', text = V_text, vmin = vrange_D[0], vmax = vrange_D[1])

    else:
        # 1D     
        ax_H = figure_t.bar(U_expected.flatten(), ax_H, color = color_H, xlabel = 'patches', ylabel = 'popu', title = 'Expected Population U', text = U_text)
        ax_D = figure_t.bar(V_expected.flatten(), ax_D, color = color_D, xlabel = 'patches', ylabel = 'popu', title = 'Expected Population V', text = V_text)

    return ax_H, ax_D




def pi_hmap(mod, ax_H = None, ax_D = None, color_H = 'BuPu', color_D = 'YlGn', start = 0.95, end = 1.0, vrange_H = DEFAULT_HMAP_DRANGE, vrange_D = DEFAULT_HMAP_DRANGE):
    '''
    Make heatmaps for payoff in a specified interval.
    Works best for 2D. 1D works as well, but figures look bad.

    Some Inputs:.
        Note the colors are matplotlib color maps.

    Returns:
        ax_H, ax_D: matplotlibrn heatmaps, for U's & V's payoff distribution, respectively.
    '''
    
    start_index = int(mod.max_record * start)
    end_index = int(mod.max_record * end)
    
    Hpi_ave = figure_t.ave_interval(mod.Hpi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval(mod.Dpi, start_index, end_index)
    
    U_title = figure_t.gen_title('Payoff ' + r'$p_H$', start, end)
    U_text = figure_t.gen_text(np.mean(Hpi_ave), np.std(Hpi_ave))
    V_title = figure_t.gen_title('Payoff ' + r'$p_D$', start, end)
    V_text = figure_t.gen_text(np.mean(V_pi_ave), np.std(V_pi_ave))
    
    figure_t.hmap(Hpi_ave, ax_H, color_H, U_title, U_text, vmin = vrange_H[0], vmax = vrange_H[1])
    figure_t.hmap(V_pi_ave, ax_D, color_D, V_title, V_text, vmin = vrange_D[0], vmax = vrange_D[1])

    return ax_H, ax_D




def pi_bar(mod, ax_H = None, ax_D = None, color_H = 'violet', color_D = 'yellowgreen', start = 0.95, end = 1.0):
    '''
    Make barplot for payoff in a specified interval.
    Works best for 1D. 2D works as well, but figures look bad.

    Returns:
        ax_H, ax_D: matplotlib axes with barplots of U and V payoff distribution plotted upon.
    '''
    
    start_index = int(mod.max_record * start)
    end_index = int(mod.max_record * end)
    
    Hpi_ave = figure_t.ave_interval_1D(mod.Hpi, start_index, end_index)
    Dpi_ave = figure_t.ave_interval_1D(mod.Dpi, start_index, end_index)
    
    U_title = figure_t.gen_title(r'$p_H$', start, end)
    U_text = figure_t.gen_text(np.mean(Hpi_ave), np.std(Hpi_ave))
    V_title = figure_t.gen_title(r'$p_D$', start, end)
    V_text = figure_t.gen_text(np.mean(Dpi_ave), np.std(Dpi_ave))
    
    ax_H = figure_t.bar(Hpi_ave, ax_H, color_H, 'Patches', 'Payoff ' + r'$p_H$', U_title, U_text)
    ax_D = figure_t.bar(Dpi_ave, ax_D, color_D, 'Patches', 'Payoff ' + r'$p_D$', V_title, V_text)

    return ax_H, ax_D




def pi_dyna(mod, ax = None, interval = 20):
    '''
    Plot how payoffs change over time.

    Returns:
        ax:    matplotlib ax of U's, V's, and sum of U & V payoff.
    '''
    
    H_curve = []
    D_curve = []
    total_curve = []

    interval = figure_t.scale_interval(interval, mod.compress_ratio)
    interval_num = int(mod.max_record / interval)
    
    for i in range(interval_num):
        U_ave = figure_t.ave_interval(mod.Hpi, i * interval, (i + 1) * interval)
        V_ave = figure_t.ave_interval(mod.Dpi, i * interval, (i + 1) * interval)
    
        H_curve.append(np.sum(U_ave))
        D_curve.append(np.sum(V_ave))
        total_curve.append(H_curve[-1] + D_curve[-1])
        
    #### plot ####    
    xaxis = np.linspace(0, mod.maxtime, len(H_curve))
    
    if ax == None:
        _, ax = plt.subplots()
    ax.plot(xaxis, H_curve, CURVE_TYPE, label = r'$p_H$')
    ax.plot(xaxis, D_curve, CURVE_TYPE, label = r'$p_D$')
    ax.plot(xaxis, total_curve, CURVE_TYPE, label = 'total')
    ax.set_xlabel('Time')
    ax.set_ylabel('Payoff')
    ax.set_title('Payoff ' + r'$p_H$' + ' & ' + r'$p_D$' + ' over time')
    ax.legend()

    return ax




def pi_hist(mod, ax_H = None, ax_D = None, color_H = 'violet', color_D = 'yellowgreen', start = 0.95, end = 1.0):
    '''
    Makes deensity histograms of U's and V's payoffs in a sepcified interval.
    Sometimes it may not be shown in density plots due to matplotlib features.
    
    Returns:
        ax_H, ax_D:     histogram of U's and V's payoff.
    '''

    start_index = int(start * mod.max_record)
    end_index = int(end * mod.max_record)

    Hpi_ave = figure_t.ave_interval_1D(mod.Hpi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval_1D(mod.Dpi, start_index, end_index)
    
    #### plot ####
    
    if ax_H == None:
        _, ax_H = plt.subplots()
    ax_H.set_xlabel('Payoff ' + r'$p_H$')
    ax_H.set_ylabel('Density')
    ax_H.hist(Hpi_ave, color = color_H, density = True)
    ax_H.set_title(figure_t.gen_title('Payoff ' + r'$p_H$' + ' Hist', start, end))
    
    if ax_D == None:
        _, ax_D = plt.subplots()
    ax_D.set_xlabel('Payoff ' + r'$p_D$')
    ax_D.set_ylabel('Density')
    ax_D.hist(V_pi_ave, color = color_D, density = True)
    ax_D.set_title(figure_t.gen_title('Payoff ' + r'$p_D$' + ' Hist', start, end))

    return ax_H, ax_D




def pi_std(mod, ax = None, interval = 20):
    '''
    Plots how standard deviation of payoff change over time.

    Returns:
        ax:    matplotlib ax of the std of payoffs.
    '''
    
    
    interval = figure_t.scale_interval(interval, mod.compress_ratio)
    interval_num = int(mod.max_record / interval)
    
    Hpi_std = []
    V_pi_std = []
    
    for i in range(interval_num):
        Hpi_ave = figure_t.ave_interval(mod.Hpi, i * interval, (i + 1) * interval)
        V_pi_ave = figure_t.ave_interval(mod.Dpi, i * interval, (i + 1) * interval)
        
        Hpi_std.append(np.std(Hpi_ave))
        V_pi_std.append(np.std(V_pi_ave))
    
    #### plot ####
    xaxis = np.linspace(0, mod.maxtime, len(Hpi_std))
    
    if ax == None:
        _, ax = plt.subplots()
    ax.plot(xaxis, Hpi_std, CURVE_TYPE, label = r'$p_H$' + ' std')
    ax.plot(xaxis, V_pi_std, CURVE_TYPE, label = r'$p_D$' + ' std')
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Std Dev')
    ax.set_title('Payoff Std-Dev Dynamics')
    
    return ax




def UV_pi(mod, ax_H = None, ax_D = None, color_H = 'violet', color_D = 'yellowgreen', alpha = 0.5, start = 0.95, end = 1.0):
    '''
    Make two scatter plots: x-axes are population and y-axes are payoff in a specified time interval.
    Reveals relationship between population and payoff.

    Returns:
        ax_H, ax_D: matplotlib axes with U and V population-payoff scatter plots.
    '''
    
    start_index = int(start * mod.max_record)
    end_index = int(end * mod.max_record)
    
    U_ave = figure_t.ave_interval_1D(mod.U, start_index, end_index)
    V_ave = figure_t.ave_interval_1D(mod.V, start_index, end_index)

    Hpi_ave = figure_t.ave_interval(mod.Hpi, start_index, end_index)
    V_pi_ave = figure_t.ave_interval(mod.Dpi, start_index, end_index)
    
    
    ax_H = figure_t.scatter(U_ave, Hpi_ave, ax_H, color_H, alpha, xlabel = 'U', ylabel = 'Payoff ' + r'$p_H$', title = 'U - ' + r'$p_H$')
    ax_D = figure_t.scatter(V_ave, V_pi_ave, ax_D, color_D, alpha, xlabel = 'V', ylabel = 'Payoff ' + r'$p_D$', title = 'V - ' + r'$p_D$')
    
    return ax_H, ax_D



def video_fig(mod, ax_list = None, num_grid = 100, color_H = 'Purples', color_D = 'Greens'):
    '''
    Plot distribution dynamics over time, of U, V population and payoff.

    mod: simulation.model object
    ax_list: a 2*2 list of ax, or None (a new 2*2 ax_list will be created)
    num_grid: how many grid for the time axis
    color_H & color_D: matplotlib color map, color for U, V population and payoff.
    '''

    if num_grid > mod.max_record:
        raise ValueError('num_grid too large, larger than mod.max_record')
    idx_step = int(mod.max_record / num_grid)
    ave_H = []
    ave_D = []
    ave_Hpi = []
    ave_Dpi = []

    for lower_idx in range(0, mod.max_record, idx_step):
        ave_H.append(figure_t.ave_interval_1D(mod.U, lower_idx, lower_idx + idx_step))
        ave_D.append(figure_t.ave_interval_1D(mod.V, lower_idx, lower_idx + idx_step))
        ave_Hpi.append(figure_t.ave_interval_1D(mod.Hpi, lower_idx, lower_idx + idx_step))
        ave_Dpi.append(figure_t.ave_interval_1D(mod.Dpi, lower_idx, lower_idx + idx_step))

    if ax_list == None:

        _, ax_list = plt.subplots(2, 2, figsize = (9.6, 12.8), dpi = 300)

    for i in range(2):
        for j in range(2):
            ax_list[i, j].spines['top'].set_visible(False)
            ax_list[i, j].spines['right'].set_visible(False)
            ax_list[i, j].set_xlabel('Patches')
            ax_list[i, j].set_ylabel('Time')
            ax_list[i, j].set_xlim([0, mod.M])
            ax_list[i, j].set_ylim([0, mod.maxtime])
    

    im = ax_list[0, 0].imshow(ave_H, cmap = color_H)
    ax_list[0, 0].get_figure().colorbar(im, ax = ax_list[0, 0], extent = [0, mod.N * mod.M, 0, mod.maxtime], origin='lower', aspect = 'auto')
    ax_list[0, 0].set_title('Population U over time')
        
    im = ax_list[0, 1].imshow(ave_D, cmap = color_D)
    ax_list[0, 1].get_figure().colorbar(im, ax = ax_list[0, 1], extent = [0, mod.N * mod.M, 0, mod.maxtime], origin='lower', aspect = 'auto')
    ax_list[0, 1].set_title('Population V over time')

    im = ax_list[1, 0].imshow(ave_Hpi, cmap = color_H)
    ax_list[1, 0].get_figure().colorbar(im, ax = ax_list[1, 0], extent = [0, mod.N * mod.M, 0, mod.maxtime], origin='lower', aspect = 'auto')
    ax_list[1, 0].set_title('Payoff ' + r'$p_H$' + ' over time')

    im = ax_list[1, 1].imshow(ave_Dpi, cmap = color_D)
    ax_list[1, 1].get_figure().colorbar(im, ax = ax_list[1, 1], extent = [0, mod.N * mod.M, 0, mod.maxtime], origin='lower', aspect = 'auto')
    ax_list[1, 1].set_title('Payoff ' + r'$p_D$' + ' over time')

    return ax_list

