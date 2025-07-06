"""Error dignity protocols."""

from pathlib import Path

ERROR_DIR = Path("errors")

def activate_error_dignity(verbose: bool = False) -> None:
    """Activate error dignity protocols.

    Parameters
    ----------
    verbose : bool, optional
        If True, print status messages. Defaults to False.
    """
    if verbose:
        print("✺ Activating error dignity protocols...")
        print("💥 → ✨ Transforming errors into gifts")
    ERROR_DIR.mkdir(exist_ok=True)
    if verbose:
        print("🌀 Mad monkey learning: ENABLED")
