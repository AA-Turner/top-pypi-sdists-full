'''
Helper functions for making figures.

Functions:
- heatmap:          Make a heatmap based on input data. Sets title, text ... as well
- bar:              Make a barplot. Sets title, text ... as well.
- scatter:          Make a scatter plot. Sets title, text ... as well.
- gen_title:        Generates a title when the plot is about an interval of time.
- gen_text:         Generates a text about standard deviation info.
- scale_interval:   scale interval if mod's data was already reduced.
- ave_interval:     Calculates average value of data over a time interval.
- ave_interval_1D:  Return in a 1D format.
- config_mpl:       Configure Matplotlib parameters in a nice format
'''


import matplotlib.pyplot as plt
import numpy as np


# move ax a bit left if add text
# default value is [0.125, 0.11, 0.9, 0.88]


def hmap(data, ax = None, cmap = "Greens", title = None, text = None, vmin = None, vmax = None):
    '''
    Helper function for making heatmaps.

    Inputs:
        data:   1D data for which you want to make a heatmap. 
        ax:     matplotlib ax to plot on. 
        cmap:   Color of heatmap. Uses matplotlib color maps
        title:  The title you want to add. None means no title.
        text:   Adds some text in a text block at the top-right corner.

    Returns:
        ax:    matplotlib axes with heatmap plotted upon.
    '''

    if ax == None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    if text != None:
        ax.text(0.86, 1.025, text, size = 11, linespacing = 1.5, transform = ax.transAxes)

    im = ax.imshow(data, cmap = cmap, vmin = vmin, vmax = vmax)
    fig.colorbar(im, ax = ax)
    ax.set_title(title, x = 0.5, y = 1)
    
    return ax



def bar(data, ax = None, color = "green", xlabel = None, ylabel = None, title = None, text = None):
    '''
    Helper Function for making barplots.

    Inputs:
        data:   2D data to make barplot.
        ax:     matplotlib ax to plot on. 
        color:  Uses Matplotlib colors.
        xlabel, y_label: 
                Label for axes.
        title:  Title for the barplot.
        text:   Adds some text in a text block at the top-right corner.
    
    Returns:
        ax:     matplotlib axes with barplot made upon.
    '''

    NM = np.array(data).shape[0]
    xaxis = np.array([i for i in range(NM)])
    
    if ax == None:
        if NM > 60:
            # make figure larger if has more data points
            _, ax = plt.subplots(figsize = (min(NM * 0.12, 7.2), 4.8))
        else:
            _, ax = plt.subplots()
    
    if text != None:
        ax.text(0.76, 1.025, text, size = 11, linespacing = 1.5, transform = ax.transAxes)

    ax.bar(x = xaxis, height = data, color = color)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, x = 0.5, y = 1)
    
    return ax



def scatter(X, Y, ax = None, color = "orange", alpha = 0.25, xlabel = "x", ylabel = "y", title = None):
    '''
    Helper function for makeing scatter plots.

    Inputs:
        X:      x-coordinates of points.
        Y:      y-coordinates of points.
        ax:     matplotlib ax to plot on. 
        Note color is Matplotlib colors.
    
    Returns:
        ax:     matplotlib axes with scatter plot made upon.
    '''
    
    if ax == None:
        _, ax = plt.subplots(figsize = (7.2, 5.4))
    ax.scatter(X, Y, color = color, alpha = alpha)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    return ax



def gen_title(title, start, end):
    '''
    Generate a title for plot when it's about an interval of time.
    '''
    title += ", " + str(round(start * 100, 1)) + "~" + str(round(end * 100, 1)) + "%"
    return title



def gen_text(ave, std):
    '''
    Generate text about standard deviation info.
    '''
    text = "ave = " + str(round(ave, 2)) #  + ", std=" + str(round(std, 2))
    return text



def ave_interval(data, start_index, end_index):
    '''
    Calculate average value of data over an interval. Return a 2D np.array
    Assume data is 3D with shape N x M x K, then takes average on the 3rd axis.

    Input:
        data:       3D np.array or list. Will take average on the 3rd axis.
        start_index, end_index: 
                    over what interval to take average.

    Returns:
        data_ave:   2D np.array with shape N x M, contains average value of data.
    '''
    
    N = len(data)
    M = len(data[0])
    
    # plot a particular record
    if start_index == end_index:
        start_index = end_index - 1
        
    data_ave = np.zeros((N, M))
    
    for i in range(N):
        for j in range(M):
            for k in range(start_index, end_index):
                data_ave[i][j] += data[i][j][k]
            data_ave[i][j] /= (end_index - start_index)
    
    return data_ave



def ave_interval_1D(data, start_index, end_index):
    '''
    Calculate average value of data over an interval. Return a 1D np.array.
    Assume data is 3D and has shape (N x M x K). Then implicitly 'compress' that N x M to 1D (NM) and takes average on the 3rd axis K.

    Input:
        data:       3D np.array or list. One of its dimensions must have size 1. Will take average on the 3rd axis.
        start_index, end_index: 
                    over what interval to take average.

    Returns:
        data_ave:   1D np.array with len N * M, contains average value of data.
    '''
    
    N = len(data)
    M = len(data[0])

    if start_index == end_index:
        end_index = start_index + 1  # exactly one record
        
    data_ave = np.zeros(N * M)
    
    for i in range(N):
        for j in range(M):
            for k in range(start_index, end_index):
                data_ave[i * M + j] += data[i][j][k]
            data_ave[i * M + j] /= (end_index - start_index)
    
    return data_ave



def scale_interval(interval, compress_itv):
    # scale interval if mod's data was already reduced.
    if compress_itv < 1:
        raise ValueError('figures.scale_interval has compress_itv < 1:', compress_itv)

    interval = int(interval / compress_itv)
    if interval == 0:
        print('Warning: data already smoothed by an interval: mod.compress_itv =', compress_itv, 'which is coarser than your', interval)
        interval = 1

    return interval



def config_mpl(mpl):
    '''
    Configure Matplotlib figures
    '''
    mpl.rcParams['savefig.dpi'] = 300
    
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = plt.rcParams['font.serif']
    mpl.rcParams['lines.linewidth'] = 1.75
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['axes.labelsize'] = 12
    mpl.rcParams['xtick.major.size'] = 10
    mpl.rcParams['ytick.major.size'] = 9
    mpl.rcParams['xtick.minor.size'] = 4
    mpl.rcParams['ytick.minor.size'] = 4

    mpl.rcParams['xtick.major.width'] = 1.5
    mpl.rcParams['ytick.major.width'] = 1.5
    mpl.rcParams['xtick.minor.width'] = 1.5
    mpl.rcParams['ytick.minor.width'] = 1.5


