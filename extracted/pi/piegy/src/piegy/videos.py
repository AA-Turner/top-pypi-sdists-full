'''
Make mp4 videos for simulation results.

Videos are made by:
make every frame by figures.py functions, then put frames together into a video.

Public Function:
- make_video:   make video based simulation results.

Private Functions
- get_max_lim:  Get the max lim (interval) over many lims, and then expand it a bit for better accommodation.
                Essentially takes union of those intervals. 
- video_lim:    Find a large enough xlim and ylim for video.
- make_mp4:     Put frames together into a mp4.
others not documented here.

'''


from . import figures
from .tools import file_tools as file_t
from .tools import figure_tools as figure_t

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import os
from cv2 import imread, VideoWriter, VideoWriter_fourcc


# a list of supported figures
SUPPORTED_FIGURES = ['UV_hmap', 'pi_hmap', 'UV_bar', 'pi_bar', 'UV_hist', 'pi_hist', 'UV_pi']


# map function name to functios in figures.py
# functions not in this dictionary is not supported for videos.
FUNC_DICT = {'UV_hmap': figures.UV_hmap, 'UV_bar': figures.UV_bar, 'UV_hist': figures.UV_hist, 
             'pi_hmap': figures.pi_hmap, 'pi_bar': figures.pi_bar, 'pi_hist': figures.pi_hist, 'UV_pi': figures.UV_pi}


# Map some color maps to regular colors, used to change colors when an invalid color name is given
SNS_PLT_COLOR_DICT = {'Greens': 'green', 'Purples': 'purple', 'BuPu': 'violet', 'YlGn': 'yellowgreen'}
# Map regular colors to color maps
PLT_SNS_COLOR_DICT = {'green': 'Greens', 'purple': 'Purples', 'violet': 'BuPu', 'yellowgreen': 'YlGn'}




def convert_color(func_name, U_color, V_color):
    '''
    Converts some invalid colors.
    If making heatmap videos but gave single colors, map to color maps.
    If making barplot or histogram videos but gave single colors, map to Matplotlib
    '''

    if 'hmap' in func_name:
        # if making heatmaps but give regular colors
        if U_color in PLT_SNS_COLOR_DICT.keys():
            print('Making heatmaps, changed \'' + U_color + '\' to \'' + PLT_SNS_COLOR_DICT[U_color] + '\'')
            U_color = PLT_SNS_COLOR_DICT[U_color]
        if V_color in PLT_SNS_COLOR_DICT.keys():
            print('Making heatmaps, changed \'' + V_color + '\' to \'' + PLT_SNS_COLOR_DICT[V_color] + '\'')
            V_color = PLT_SNS_COLOR_DICT[V_color]
        
        return U_color, V_color

    elif 'hmap' not in func_name:
        # if making barplots or histogram
        if U_color in SNS_PLT_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + U_color + '\' to \'' + SNS_PLT_COLOR_DICT[U_color] + '\'')
            U_color = SNS_PLT_COLOR_DICT[U_color]
        if V_color in SNS_PLT_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + V_color + '\' to \'' + SNS_PLT_COLOR_DICT[V_color] + '\'')
            V_color = SNS_PLT_COLOR_DICT[V_color]

        return U_color, V_color



def get_max_lim(lims):
    '''
    Get the max lim over many lims, i.e., the lowest lower bound and highest upper bound.
    And then expand it a bit for better accommodation.

    Input:
        lim:    list or np.array, has form [lim1, lim2, ...]
    
    Returns:
        A max lim which contains all lims.
    '''

    lims = np.array(lims)
    
    lim_min = np.min(lims[:, 0]) # min of min
    lim_max = np.max(lims[:, 1]) # max of max
    r = lim_max - lim_min

    if lim_min != 0:
        # negative values are reached
        # extend both upper bound and lower bound 
        return [lim_min - r * 0.05, lim_max + r * 0.05]
    else:
        # only extend upper bound
        return [0, lim_max + r * 0.05]




def frame_lim(mod, func, frames):
    '''
    Find a large enough xlim and ylim for frames, if not heatmaps.

    Inputs:
        mod:        A simulation.model object, the simulation results.
        frames:     How many frame to make for the video.
    
    Returns:
        xlim and ylim for U and V, 4 in total.
    '''
    
    # take 10 samples and store their lims in list
    U_xlist = []
    U_ylist = []
    V_xlist = []
    V_ylist = []
    
    for i in range(10):
        fig_U, ax_U = plt.subplots()
        fig_V, ax_V = plt.subplots()
        ax_U, ax_V = func(mod, ax_U = ax_U, ax_V = ax_V, start = i / 10, end = (i / 10 + 1 / frames))

        U_xlist.append(ax_U.get_xlim())
        U_ylist.append(ax_U.get_ylim())
        V_xlist.append(ax_V.get_xlim())
        V_ylist.append(ax_V.get_ylim())

        plt.close(fig_U)
        plt.close(fig_V)
    
    # get the largest 'range' based on the lists
    U_xlim = get_max_lim(U_xlist)
    U_ylim = get_max_lim(U_ylist)
    V_xlim = get_max_lim(V_xlist)
    V_ylim = get_max_lim(V_ylist)

    return U_xlim, U_ylim, V_xlim, V_ylim




def frame_heatmap_lim(mod, func, frames):
    '''
    Find a large enough color bar lim for frames, if heatmaps.

    Inputs:
        mod:        A simulation.model object, the simulation results.
        frames:     How many frame to make for the video.
    
    Returns:
        clim for U and V
    '''

    U_list = []
    V_list = []

    for i in range(10):
        fig_U, ax_U = plt.subplots()
        fig_V, ax_V = plt.subplots()
        func(mod, ax_U = ax_U, ax_V = ax_V, start = i / 10, end = (i / 10 + 1 / frames))

        U_list.append(ax_U.images[0].get_clim())
        V_list.append(ax_V.images[0].get_clim())

        plt.close(fig_U)
        plt.close(fig_V)

    U_clim = get_max_lim(U_list)
    V_clim = get_max_lim(V_list)

    return U_clim, V_clim




def make_mp4(video_dir, frame_dir, fps):
    '''
    Read .png from the frames folder and make into a mp4
    Inputs:
        video_dir:  where to save the video
        frame_dirs: where to read frames from
        fps:        frames per second
    '''

    frame_paths_incomplete = os.listdir(frame_dir)
    frame_paths_incomplete.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    frame_path = []
    for file in frame_paths_incomplete:
        if (file[-4:] == '.png') and ('frame' in file):
            frame_path.append(os.path.join(frame_dir, file))

    # setup cv2 video writer
    first_frame = imread(frame_path[0])
    height, width, _ = first_frame.shape
    fourcc = VideoWriter_fourcc(*'mp4v')
    video_writer = VideoWriter(video_dir, fourcc, fps, (width, height))

    for file in frame_path:
        frame = imread(file)
        video_writer.write(frame)
    video_writer.release()




def make_video(mod, func_name = 'UV_hmap', frames = 100, dpi = 200, fps = 30, U_color = 'Greens', V_color = 'Purples', del_frames = False, dirs = 'videos'):
    '''
    Make a mp4 video based on simulation results.

    Inputs:
    - mod:            a simulation.model object, the simulation results.
    - func_name:      what function to use to make the frames. Should be one of the functions in figures.py
    - frames:         how many frames to make. Use more frames for more smooth evolutions.
    - dpi:            dots per inch.
    - fps:            frames per second.
    - U_color:        color for U's videos. Color maps or regular colors, based on what function you use.
    - V_color:        color for V's videos.
    - del_frames:     whether to delete frames after making video.
    - dirs:           where to store the frames and videos.
    '''
    
    if func_name not in FUNC_DICT.keys():
        raise ValueError(func_name + ' not supported for videos.')
    func = FUNC_DICT[func_name]

    # convert color if invalid colors are given
    U_color, V_color = convert_color(func_name, U_color, V_color)

    # set Agg backend for faster speed
    original_backend = mpl.get_backend()
    mpl.use("Agg")
    
    # print progress
    one_progress = frames / 100
    current_progress = one_progress
    
    if 'hmap' in func_name:
        # make sure a fixed color bar for all frames
        U_clim, V_clim = frame_heatmap_lim(mod, func, frames)
    else:
        # make sure y axis not changing if not making heatmaps
        U_xlim, U_ylim, V_xlim, V_ylim = frame_lim(mod, func, frames)

    
    U_frame_dirs = dirs + '/U-' + func_name
    V_frame_dirs = dirs + '/V-' + func_name
    
    if os.path.exists(U_frame_dirs):
        file_t.del_dirs(U_frame_dirs)
    os.makedirs(U_frame_dirs)
    if os.path.exists(V_frame_dirs):
        file_t.del_dirs(V_frame_dirs)
    os.makedirs(V_frame_dirs)

    figsize = (6.4, 4.8)
        

    #### for loop ####
    
    for i in range(frames):
        if i > current_progress:
            print('making frames', round(i / frames * 100), '%', end = '\r')
            current_progress += one_progress
        
        if ('bar' in func_name) and (mod.M > 60):
            figsize = (min(mod.M * 0.12, 7.2), 4.8)
            fig_U, ax_U = plt.subplots(figsize = figsize)
            fig_V, ax_V = plt.subplots(figsize = figsize)
        else:
            fig_U, ax_U = plt.subplots(figsize = figsize)
            fig_V, ax_V = plt.subplots(figsize = figsize)
            
        if 'hmap' in func_name:
            func(mod, ax_U = ax_U, ax_V = ax_V, U_color = U_color, V_color = V_color, start = i / frames, end = (i + 1) / frames, vrange_U = U_clim, vrange_V = V_clim)
        else:
            func(mod, ax_U = ax_U, ax_V = ax_V, U_color = U_color, V_color = V_color, start = i / frames, end = (i + 1) / frames)
        
        if 'hmap' in func_name:
            # color map lim already set at function call
            pass
        else:
            # make sure y axis not changing if not heatmap and not UV_pi
            ax_U.set_ylim(U_ylim)
            ax_V.set_ylim(V_ylim)
            if ('hist' in func_name) or (func_name == 'UV_pi'):
                # need to set xlim as well for UV_pi and histograms
                ax_V.set_xlim(U_xlim)
                ax_V.set_xlim(V_xlim)

        fig_U.savefig(U_frame_dirs + '/' + 'U_frame_' + str(i) + '.png', pad_inches = 0.25, dpi = dpi)
        fig_V.savefig(V_frame_dirs + '/' + 'V_frame_' + str(i) + '.png', pad_inches = 0.25, dpi = dpi)
        
        plt.close(fig_U)
        plt.close(fig_V)
        
    #### for loop ends ####

    # reset to original backend
    mpl.use(original_backend)
    
    # frames done
    print('making mp4...      ', end = '\r')
    
    # make videos based on frames
    make_mp4(dirs + '/U-' + func_name + '.mp4', U_frame_dirs, fps)
    make_mp4(dirs + '/V-' + func_name + '.mp4', V_frame_dirs, fps)
    
    if del_frames:
        file_t.del_dirs(U_frame_dirs)
        file_t.del_dirs(V_frame_dirs)
        print('video saved: ' + dirs + ', frames deleted')
    else:
        print('video saved: ' + dirs + '      ')



