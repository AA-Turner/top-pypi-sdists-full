import threading
import time
import traceback
from typing import Callable, Union

from adam.commands.command import Command
from adam.config import Config
from adam.utils_repl.repl_session import ReplSession
from adam.utils_repl.repl_state import ReplState
from adam.utils_context import NULL, Context
from adam.utils_job.job import Job
from adam.utils_job.job_schedules import JobSchedules, ts
from adam.utils_job.job_status import JobStatus

class JobScheduler:
    # injected by repl.py
    run_command: Callable[[str, ReplSession, list[Command], Command, callable, Job, Context], Union[ReplState, JobStatus]] = None
    jobs_thread: threading.Thread = None

    def schedule(state: ReplState, cmd: str, job_status: JobStatus, ctx = NULL):
        JobScheduler.start(state, ctx)

        JobScheduler._ctx.log2(f'[{ts()}] {job_status.job_id()} Scheduled for: {cmd}.')
        with JobSchedules.lock:
            JobSchedules._queue[job_status.job_id()] = job_status.with_ts(time.time()).with_state(state)

    def start(state: ReplState, ctx = NULL):
        with JobSchedules.lock:
            if not JobScheduler.jobs_thread:
                # create dedicated context and job
                ctx = Context.new(cmd='job-scheduler', show_out=True, background=True, bg_init_msg=False, history='')

                JobScheduler._ctx = ctx
                JobScheduler.jobs_thread = threading.Thread(target=JobScheduler.loop, args=(state, ctx,), daemon=True)
                JobScheduler.jobs_thread.start()

    def cancel_jobs(state: ReplState, job_ids: list[str]):
        canceled: dict[str, JobStatus] = {}

        # 1. delete from the pending queue first
        for job_id in job_ids:
            with JobSchedules.lock:
                if job_id in JobSchedules._queue:
                    js = JobSchedules._queue[job_id]
                    del JobSchedules._queue[job_id]
                    canceled[job_id] = js

        return canceled

    # single queue pattern
    def loop(state: ReplState, ctx = NULL):
        while True:
            tick_interval = Config().get('job.scheduler.tick-interval-in-secs', 5)

            try:
                while (pendings := JobSchedules.pending()):
                    checked = 0
                    for job_id, status in pendings.items():
                        checked += 1

                        job_ctx = ctx.switch_to_job_context(job_id)

                        status = JobScheduler.reschedule_job(state, status, ctx=job_ctx)
                        if not isinstance(status, JobStatus):
                            job_ctx.log2(f'[{ts()}] {job_id}: Scheduling is ignored as command is not schedulable.')
                            time.sleep(tick_interval)

                            continue

                        if status.all_completed():
                            JobSchedules.done(status, ctx=ctx)

                        time.sleep(tick_interval)
            except:
                if Config().is_debug():
                    traceback.print_exc()

            time.sleep(tick_interval)

    def reschedule_job(state: ReplState, status: JobStatus, ctx = NULL):
        job = Job.job(status.job_id())
        if not job:
            ctx.log2('Job not found.')
            # TODO remove from the schedules
            return state

        cmd = job.scheduled_command
        if status.state:
            # use repl state from when the command was scheduled
            state = status.state

        return JobScheduler.run_command(state, cmd, job=job, ctx=ctx)