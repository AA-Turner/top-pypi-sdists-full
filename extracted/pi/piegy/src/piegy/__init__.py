'''
Payoff-Driven Stochastic Spatial Model for Evolutionary Game Theory
-----------------------------------------------------------------------------

Provides:
    1.  A stochastic spatial model for simulating the interaction and evolution of two species in either 1D or 2D space
    2.  Plot & video functions to visualize simulation results.
    3.  Module to test influence of certain variables on results.
    4.  Data saving & reading module.
    4.  Additional analytical tools.

Websites:
    - The *piegy* documentation: https://piegy.readthedocs.io/en/
    - GitHub repository at: https://github.com/Chenning04/piegy.git
    - PyPI page: https://pypi.org/project/piegy/


Last update: May 12, 2025
'''

from .__version__ import __version__
from .build_info import build_info

from .simulation import model, run, demo_model, UV_expected_val, check_overflow_func
from .videos import make_video, SUPPORTED_FIGURES
from .data_tools import save, load

from .analysis import rounds_expected, scale_maxtime, check_convergence, combine_mod

from .figures import (UV_hmap, UV_bar, UV_dyna, UV_hist, UV_std, UV_expected, 
                      pi_hmap, pi_bar, pi_dyna, pi_hist, pi_std, UV_pi, video_fig)

from .test_var import (test_var1, var_UV1, var_pi1, var_convergence1, get_dirs1, 
                       test_var2, var_UV2, var_pi2, var_convergence2, get_dirs2)


simulation_memebers = ['model', 'run', 'demo_model']

videos_members = ['make_video', 'SUPPORTED_FIGURES']

data_members = ['save', 'load']

analysis_members = ['expected_rounds', 'scale_maxtime', 'check_convergence', 'combine_mod']

figures_members = ['UV_hmap', 'UV_bar', 'UV_dyna', 'UV_hist', 'UV_std', 'UV_expected_val', 'UV_expected', 
                   'pi_hmap', 'pi_bar', 'pi_dyna', 'pi_hist', 'pi_std', 'UV_pi', 'video_fig']

test_var_members = ['test_var1', 'var_UV1', 'var_pi1', 'var_convergence1', 'get_dirs1', 
                    'test_var2', 'var_UV2', 'var_pi2', 'var_convergence2', 'get_dirs2']


__all__ = simulation_memebers + videos_members + data_members + figures_members + analysis_members + test_var_members





