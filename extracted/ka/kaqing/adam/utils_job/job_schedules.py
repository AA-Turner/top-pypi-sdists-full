from copy import copy
from datetime import datetime
import threading
import time

from adam.utils_context import NULL
from adam.utils_job.job_status import JobStatus

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class JobSchedules:
    _queue: dict[str, JobStatus] = {}
    _completed: dict[str, JobStatus] = {}
    lock = threading.Lock()

    def pending():
        with JobSchedules.lock:
            return copy(JobSchedules._queue)

    def done(job_status: JobStatus, ctx = NULL):
        ctx.log2(f'[{ts()}] Finished {job_status.job_id()}.')

        if job_status.job_id() in JobSchedules._queue:
            del JobSchedules._queue[job_status.job_id()]

        JobSchedules._completed[job_status.job_id()] = job_status.with_ts(time.time())