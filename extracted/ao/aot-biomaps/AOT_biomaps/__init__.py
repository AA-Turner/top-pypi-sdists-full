from .AOT_Acoustic import *
from .AOT_Optic import *
from .AOT_Reconstruction import *
from .AOT_Experiment import *
from .config import config

__version__ = '2.6.7'

if config.get_process() == 'gpu':
    __process__ = 'gpu'
else:
    __process__ = 'cpu'

def initialize(process='cpu'):
    config.set_process(process)
    if process == 'gpu':
        config.select_best_gpu()
        print(f"Initialized with process: {config.get_process()} using GPU: {config.bestGPU}")
    else:
        print(f"Initialized with process: {config.get_process()}")

