from ..imports import *
from .manager import FlanManager
# ----------------------------------------------------------------------
# Convenience accessors
# ----------------------------------------------------------------------
def get_flan_manager():
    """Return singleton FlanManager instance."""
    return FlanManager()
def get_flan_title(content):
    mgr = get_flan_manager()
    return mgr.generate_title(content)


def get_flan_summary(
    text: str,
    max_chunk: int = 512,
    min_length: int = 100,
    max_length: int = 512,
    do_sample: bool = False,
) -> str:
    """Generate a summary via the shared FlanManager."""
    mgr = get_flan_manager()
    return mgr.summarize(
        text=text,
        max_chunk=max_chunk,
        min_length=min_length,
        max_length=max_length,
        do_sample=do_sample,
    )
