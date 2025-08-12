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

import matplotlib as mpl
# switched to Agg in make_video
import matplotlib.pyplot as plt
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
CMP_COLOR_DICT = {'Greens': 'green', 'Purples': 'purple', 'BuPu': 'violet', 'YlGn': 'yellowgreen'}
# Map regular colors to color maps
COLOR_CMP_DICT = {'green': 'Greens', 'purple': 'Purples', 'violet': 'BuPu', 'yellowgreen': 'YlGn'}




def convert_color(func_name, color_H, color_D):
    '''
    Converts some invalid colors.
    If making heatmap videos but gave single colors, map to color maps.
    If making barplot or histogram videos but gave single colors, map to Matplotlib
    '''

    if 'hmap' in func_name:
        # if making heatmaps but give regular colors
        if color_H in COLOR_CMP_DICT.keys():
            print('Making heatmaps, changed \'' + color_H + '\' to \'' + COLOR_CMP_DICT[color_H] + '\'')
            color_H = COLOR_CMP_DICT[color_H]
        if color_D in COLOR_CMP_DICT.keys():
            print('Making heatmaps, changed \'' + color_D + '\' to \'' + COLOR_CMP_DICT[color_D] + '\'')
            color_D = COLOR_CMP_DICT[color_D]
        
        return color_H, color_D

    elif 'hmap' not in func_name:
        # if making barplots or histogram
        if color_H in CMP_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + color_H + '\' to \'' + CMP_COLOR_DICT[color_H] + '\'')
            color_H = CMP_COLOR_DICT[color_H]
        if color_D in CMP_COLOR_DICT.keys():
            print('Not making heatmaps, changed \'' + color_D + '\' to \'' + CMP_COLOR_DICT[color_D] + '\'')
            color_D = CMP_COLOR_DICT[color_D]

        return color_H, color_D



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
    H_xlist = []
    H_ylist = []
    V_xlist = []
    V_ylist = []
    
    for i in range(10):
        fig_H, ax_H = plt.subplots()
        fig_D, ax_D = plt.subplots()
        ax_H, ax_D = func(mod, ax_H = ax_H, ax_D = ax_D, start = i / 10, end = (i / 10 + 1 / frames))

        H_xlist.append(ax_H.get_xlim())
        H_ylist.append(ax_H.get_ylim())
        V_xlist.append(ax_D.get_xlim())
        V_ylist.append(ax_D.get_ylim())

        plt.close(fig_H)
        plt.close(fig_D)
    
    # get the largest 'range' based on the lists
    H_xlim = get_max_lim(H_xlist)
    H_ylim = get_max_lim(H_ylist)
    V_xlim = get_max_lim(V_xlist)
    V_ylim = get_max_lim(V_ylist)

    return H_xlim, H_ylim, V_xlim, V_ylim




def frame_heatmap_lim(mod, func, frames):
    '''
    Find a large enough color bar lim for frames, if heatmaps.

    Inputs:
        mod:        A simulation.model object, the simulation results.
        frames:     How many frame to make for the video.
    
    Returns:
        clim for U and V
    '''

    H_list = []
    V_list = []

    for i in range(10):
        fig_H, ax_H = plt.subplots()
        fig_D, ax_D = plt.subplots()
        func(mod, ax_H = ax_H, ax_D = ax_D, start = i / 10, end = (i / 10 + 1 / frames))

        H_list.append(ax_H.images[0].get_clim())
        V_list.append(ax_D.images[0].get_clim())

        plt.close(fig_H)
        plt.close(fig_D)

    H_clim = get_max_lim(H_list)
    D_clim = get_max_lim(V_list)

    return H_clim, D_clim




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




def make_video(mod, func_name = None, frames = 100, dpi = 200, fps = 30, color_H = 'Greens', color_D = 'Purples', del_frames = False, dirs = 'videos'):
    '''
    Make a mp4 video based on simulation results.

    Inputs:
    - mod:            a simulation.model object, the simulation results.
    - func_name:      what function to use to make the frames. Should be one of the functions in figures.py. Default is UV_hmap (for 2D) or UV_bar (1D).
    - frames:         how many frames to make. Use more frames for more smooth evolutions.
    - dpi:            dots per inch.
    - fps:            frames per second.
    - color_H:        color for U's videos. Color maps or regular colors, based on what function you use.
    - color_D:        color for V's videos.
    - del_frames:     whether to delete frames after making video.
    - dirs:           where to store the frames and videos.
    '''
    
    if func_name == None:
        if mod.N == 1:
            func_name = "UV_bar"
        else:
            func_name = "UV_hmap"
    
    if func_name not in FUNC_DICT.keys():
        raise ValueError(func_name + ' not supported for videos.')
    func = FUNC_DICT[func_name]

    # convert color if invalid colors are given
    color_H, color_D = convert_color(func_name, color_H, color_D)

    # set Agg backend for faster speed
    original_backend = mpl.get_backend()
    mpl.use("Agg")
    
    # print progress
    one_progress = frames / 100
    current_progress = one_progress
    
    if 'hmap' in func_name:
        # make sure a fixed color bar for all frames
        H_clim, D_clim = frame_heatmap_lim(mod, func, frames)
    else:
        # make sure y axis not changing if not making heatmaps
        H_xlim, H_ylim, V_xlim, V_ylim = frame_lim(mod, func, frames)

    
    H_frame_dirs = dirs + '/U-' + func_name
    V_frame_dirs = dirs + '/V-' + func_name
    
    if os.path.exists(H_frame_dirs):
        file_t.del_dirs(H_frame_dirs)
    os.makedirs(H_frame_dirs)
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
            fig_H, ax_H = plt.subplots(figsize = figsize)
            fig_D, ax_D = plt.subplots(figsize = figsize)
        else:
            fig_H, ax_H = plt.subplots(figsize = figsize)
            fig_D, ax_D = plt.subplots(figsize = figsize)
            
        if 'hmap' in func_name:
            func(mod, ax_H = ax_H, ax_D = ax_D, color_H = color_H, color_D = color_D, start = i / frames, end = (i + 1) / frames, vrange_H = H_clim, vrange_D = D_clim)
        else:
            func(mod, ax_H = ax_H, ax_D = ax_D, color_H = color_H, color_D = color_D, start = i / frames, end = (i + 1) / frames)
        
        if 'hmap' in func_name:
            # color map lim already set at function call
            pass
        else:
            # make sure y axis not changing if not heatmap and not UV_pi
            ax_H.set_ylim(H_ylim)
            ax_D.set_ylim(V_ylim)
            if ('hist' in func_name) or (func_name == 'UV_pi'):
                # need to set xlim as well for UV_pi and histograms
                ax_D.set_xlim(H_xlim)
                ax_D.set_xlim(V_xlim)

        fig_H.savefig(H_frame_dirs + '/' + 'H_frame_' + str(i) + '.png', pad_inches = 0.25, dpi = dpi)
        fig_D.savefig(V_frame_dirs + '/' + 'V_frame_' + str(i) + '.png', pad_inches = 0.25, dpi = dpi)
        
        plt.close(fig_H)
        plt.close(fig_D)
        
    #### for loop ends ####

    # reset to original backend
    mpl.use(original_backend)
    
    # frames done
    print('making mp4...      ', end = '\r')
    
    # make videos based on frames
    make_mp4(dirs + '/U-' + func_name + '.mp4', H_frame_dirs, fps)
    make_mp4(dirs + '/V-' + func_name + '.mp4', V_frame_dirs, fps)
    
    if del_frames:
        file_t.del_dirs(H_frame_dirs)
        file_t.del_dirs(V_frame_dirs)
        print('video saved: ' + dirs + ', frames deleted')
    else:
        print('video saved: ' + dirs + '      ')



