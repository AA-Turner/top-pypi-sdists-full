__version__ = '2.3.10'

'''
version history:

0.1.0: first publishing, May 11, 2025
0.1.1: fix dependency errors
0.1.2: fixing module not find error
0.1.3: restructuring package
0.1.4 ~ 0.1.6: fixing moviepy import issue
0.1.7: changed name back to 'piegy'
0.1.8: updated installation in README
0.1.9: first round of full debugging

1.0.0: first version in PyPI.
1.1.0: debugging. Updated a range of functions, in the following modules: figures, videos, test_var, model, figure_tools
1.1.1: minor debugging in model module.
1.1.2: fix text bad location in figure_tools, update labeling and titling in figures and test_var. Add dpi param to make_video in videos. Remove reset_data function in model.
1.1.3: update README.
1.1.4: changed name: ``model`` module to ``simulation``, and ``model.simulation`` class to ``simulation.model``. Bug fix in videos.
1.1.5: update README.
1.1.6: change name of variables in model class -- for compatability with the new C core. 1.1.6 is the last verion of v1. From v2 on, the piegy package has C core.

2.0.0: update simulation core to C-based.
2.0.1: re-upload, the C core is not included in package.
2.0.2: update version number in __version__.py and update README.
2.0.3: speed boost & debugging in C core. Add check_overflow feature in simulation module, checks whether overflow/too large numbers might be encountered in simulation.
2.0.4: minor debuggings.
2.0.5: fix error in random number generator.
2.1.0: redo random number generator. Update package upload so that more compatible across platforms.
2.1.1: fix import bug for the C core.
2.1.2 ~ 2.1.9: updating & fixing wheel.
2.1.10: fix print bug in run function.
2.1.11: fix .so duplicate error.
2.2.1: change heatmap plotting tool from Seaborn to Matplotlib. Change video maker to cv2 (opencv-python).
2.2.2: impose stricter overflow error check. Used update_mig_one function (already written before, didn't use). This gives 30% speed improvement.
2.2.3: raised rate calculation to higher accuracy (long double), and switched to 30-bit random number generator.
2.3.1: roll back accuracy update. Decrease toleratable bound for exponent of exp() to 500. 
        Add video_fig function to figures module, which plots change of patch popu/payoff overtime in a 2D figure. Add auto-sorting for values passed to test_var plot functions.
2.3.2: allow play-with-self in payoff calculation. Changed migration function to e^(w*pi) (removed "1+" term).
        Simplified update-migration functions, improve speed by ~10%. Add -march=native flag to Makefile.
2.3.3: fix error in calculation of migration rates.
2.3.4: change back to the mig & payoff rules in version 2.3.2
2.3.5: improved accuracy for simulation, now can better handle large mig rates. Numerical errors are now being checked and reduced automatically based on how large the values are.
2.3.6: index error due to reduced accuracy is now explicitly handled.
2.3.7: update migration rules on the boundary. mu values are scaled based on how many neighbors a patch has. Minor debugging in several modules.
2.3.8: bug fix for 2.3.7 update.
2.3.9: now use xoshiro256+ as RNG.
2.3.10: remove requirement for init population being equal in combine_mod. Change function name to combine_mod (from combine_sim).
2.3.11: debugging and renameed some variables.
'''