"""
Scheduler Service.

API View for Managing Jobs in NAV Scheduler.
"""
from datetime import datetime
from navigator.views import BaseView


class SchedulerService(BaseView):
    """Scheduler Manager Facility.

    Facility for a remotely accessible Scheduler Service.
    can add, modify, remove, pause or re-schedule jobs, looking for job information, etc.

    TODO: Can we use it also as RPC Service.

    get: Get all information about a Job.
    put: inserting a new Job into the jobstore.
    post: modify a Job or re-schedule a Job.
    delete: removing (or pausing) a Job.
    patch: restart a Job o submitting a Job.
    """

    def next_runtime(self):
        app = self.request.app
        scheduler = app["scheduler"]
        args = self.match_parameters(self.request)
        try:
            job = args["job"]
        except KeyError:
            job = None
        obj = scheduler.get_job(job)
        job = obj["job"]
        if job and job.next_run_time:
            status = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
            result = {"job_id": job.id, "name": job.name, "next_run_time": status}
            return self.json_response(response=result, state=200)
        else:
            return self.error(
                request=self.request,
                response=f"There is not such Job Scheduled {job!s}",
                state=404,
            )

    def time_left(self):
        app = self.request.app
        scheduler = app["scheduler"]
        args = self.match_parameters(self.request)
        try:
            job = args["job"]
        except KeyError:
            job = None
        obj = scheduler.get_job(job)
        job = obj["job"]
        if job and job.next_run_time:
            delta = job.next_run_time.replace(tzinfo=None) - datetime.now()
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            days = f"{delta.days} days, " if delta.days else ""
            result = {
                "job_id": job.id,
                "name": job.name,
                "time_left": f"{days}{hours}h:{minutes}m:{seconds}s",
            }
            return self.json_response(response=result, state=200)
        else:
            return self.error(
                request=self.request,
                response=f"There is not such Job Scheduled {job!s}",
                state=404,
            )
