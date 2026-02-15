import threading
import time
import traceback

from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_context import NULL, Context
from adam.utils_job.job_schedules import JobSchedules, ts
from adam.utils_job.job_status import JobStatus
from adam.utils_job.utils_job_results import retry_job

class JobScheduler:
    run_command: callable = None
    jobs_thread: threading.Thread = None

    def schedule(state: ReplState, cmd: str, job_status: JobStatus, ctx = NULL):
        JobScheduler.start(state, ctx)

        JobScheduler._ctx.log2(f'[{ts()}] {job_status.job_id()} Scheduled for: {cmd}.')
        with JobSchedules.lock:
            JobSchedules._queue[job_status.job_id()] = job_status.with_ts(time.time())

    def start(state: ReplState, ctx = NULL):
        with JobSchedules.lock:
            if not JobScheduler.jobs_thread:
                # create dedicated context and job
                ctx = Context.new(cmd='job-scheduler', show_out=True, background=True, bg_init_msg=False, history='')

                JobScheduler._ctx = ctx
                JobScheduler.jobs_thread = threading.Thread(target=JobScheduler.loop, args=(state, ctx,), daemon=True)
                JobScheduler.jobs_thread.start()

    # single queue pattern
    def loop(state: ReplState, ctx = NULL):
        while True:
            try:
                while (pendings := JobSchedules.pending().keys()):
                    checked = 0
                    for job_id in pendings:
                        checked += 1

                        job_ctx = ctx.switch_to_job_context(job_id)

                        status = retry_job(state, job_id, JobScheduler.run_command, ctx=job_ctx)
                        if not isinstance(status, JobStatus):
                            job_ctx.log2(f'[{ts()}] {job_id}: Scheduling is ignored as command is not schedulable.')
                            time.sleep(5)

                            continue

                        if status.all_completed():
                            JobSchedules.done(status, ctx=ctx)

                        time.sleep(5)
            except:
                if Config().is_debug():
                    traceback.print_exc()
