"""Utility to wait if CPU or memory usage is high."""
import time
import psutil

from t_nextgen.utils.logger import logger


def wait_if_high_usage(
    cpu_threshold: int = 80, memory_threshold: int = 80, check_interval: int = 5, timeout: int = 300
) -> None:
    """Checks CPU and memory usage and waits if usage exceeds the specified thresholds.

    :param cpu_threshold: CPU usage percentage threshold to trigger wait.
    :param memory_threshold: Memory usage percentage threshold to trigger wait.
    :param check_interval: Time in seconds to wait before rechecking.
    :param timeout: Maximum time in seconds to wait before exiting the loop.
    """
    start_time = time.time()
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        if cpu_usage < cpu_threshold and memory_usage < memory_threshold:
            break

        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            logger.info(f"Timeout reached. CPU: {cpu_usage}%, Memory: {memory_usage}%. Exiting wait.")
            break

        logger.info(f"High usage detected. CPU: {cpu_usage}%, Memory: {memory_usage}%. Waiting...")
        time.sleep(check_interval)
