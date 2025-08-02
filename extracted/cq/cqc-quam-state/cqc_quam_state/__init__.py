"""CQC QuAM State management package."""

from .utils import get_quam_state_path

# Define QUAM_STATE_PATH that points to the installed quam_state directory
QUAM_STATE_PATH = get_quam_state_path()

# Export the variable in package namespace
__all__ = ['QUAM_STATE_PATH']
