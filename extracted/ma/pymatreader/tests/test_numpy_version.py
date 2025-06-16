"""Test whether the correct version of numpy is installed."""

import os

import numpy as np


def test_numpy_version():
    """Test whether the correct version of numpy is installed."""
    pixi_env = os.environ.get('PIXI_ENVIRONMENT', 'default')
    if pixi_env.startswith('testpy'):
        assert np.__version__[0] == pixi_env[-1]
