# -*- coding: utf-8 -*-
"""
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This class holds example code how to use the FAST algorithm
"""

import numpy as np
import pandas as pd

import spotpy
from spotpy.examples.spot_setup_hymod_python import spot_setup

if __name__ == "__main__":
    parallel = "seq"
    # Initialize the Hymod example
    spot_setup = spot_setup()

    # Select number of maximum repetitions
    # CHeck out https://spotpy.readthedocs.io/en/latest/Sensitivity_analysis_with_FAST/
    # How to determine an appropriate number of repetitions
    rep = 2245

    # Start a sensitivity analysis
    sampler = spotpy.algorithms.morris(
        spot_setup, dbname="MORRIS_hymod", dbformat="csv", db_precision=np.float32
    )
    #sampler.sample(rep)

    # Load the results gained with the fast sampler, stored in FAST_hymod.csv
    results = spotpy.analyser.load_csv_results("MORRIS_hymod")
    # results = pd.read_csv("MORRIS_hymod.csv")
    # Example plot to show the sensitivity index of each parameter
    spotpy.analyser.plot_morris_sensitivity(results, spot_setup)

    # Example to get the sensitivity index of each parameter
    # SI = spotpy.analyser.get_sensitivity_of_morris(results)
