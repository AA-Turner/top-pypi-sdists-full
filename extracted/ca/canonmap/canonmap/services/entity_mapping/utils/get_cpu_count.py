# canonmap/utils/get_cpu_count.py
# Utility module for getting CPU count for parallel processing

import multiprocessing

from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

def get_cpu_count():
    """
    Get the number of CPU cores available for parallel processing.
    
    Returns:
        int: Number of CPU cores
    """
    count = multiprocessing.cpu_count()
    return count