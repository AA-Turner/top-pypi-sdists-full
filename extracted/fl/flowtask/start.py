import subprocess
import sys
from flowtask.conf import (
    DASK_SCHEDULER_PORT
)

def start_dask_scheduler():
    return subprocess.Popen(
        ['dask', 'scheduler', '--port', str(DASK_SCHEDULER_PORT)],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE
    )

def start_gunicorn():
    return subprocess.Popen([
        'gunicorn',
        'nav:navigator',
        '-c',
        'gunicorn_config.py',
        '-k',
        'aiohttp.GunicornUVLoopWebWorker',
        '--log-level',
        'debug',
        '--preload'
    ])  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    # Start services
    dask_scheduler_process = start_dask_scheduler()
    gunicorn_process = start_gunicorn()
    try:
        # Wait for processes to complete
        dask_scheduler_process.wait()
        gunicorn_process.wait()
    except KeyboardInterrupt:
        # Terminate processes on interrupt
        dask_scheduler_process.terminate()
        gunicorn_process.terminate()
        sys.exit(0)

if __name__ == '__main__':
    main()
