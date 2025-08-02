"""Utility functions for CQC QuAM State."""

import os
from importlib.resources import files


def get_quam_state_path():
    """
    Get the path to the QuAM state directory.

    Returns:
        str: The absolute path to the QuAM state directory.
    """
    try:
        # For Python 3.9+
        # Access quam_state as a resource within the cqc_quam_state package
        p = files('quam_state')
        # p = files('cqc_quam_state').joinpath('quam_state')
        quam_state_path = str(p._paths[0])
    except Exception as e:
        # Fallback for older Python versions
        # This fallback might also need adjustment if __file__ is not reliable
        # depending on how the package is installed/used.
        # For now, assuming it's a simple local structure.
        libs_dir = os.path.dirname(os.path.dirname(__file__))
        quam_state_path = os.path.join(libs_dir, 'quam_state')
        # print(f"Warning: Using fallback path for quam_state: {quam_state_path}")
        quam_state_path = str(quam_state_path)

    return quam_state_path
