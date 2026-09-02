"""
Scheduler Manager.

API View for Managing the Scheduler.
"""
from typing import Any, TypeVar
from collections import defaultdict
from collections.abc import Callable
import asyncio
from functools import wraps
from aiohttp import web, hdrs
from datamodel import BaseModel
from navigator_session import get_session
from navigator.views import (
    BaseView,
    ModelView
)
from navigator.conf import AUTH_SESSION_OBJECT
from ...exceptions import FlowTaskError, NotFound
from ...conf import SCHEDULER_SERVICE_GROUPS, SCHEDULER_ADMIN_GROUPS
from .models import Job


F = TypeVar("F", bound=Callable[..., Any])


class SchedulerManager(BaseView):
    """Scheduler Manager Facility.

    get: getting Scheduler and Jobs information, for Jobs or a single job
    post: editing existing jobs
    put: inserting a new task into the jobstore
    delete: removing (or pausing) some jobs from the scheduler
    patch: reload all jobs.
    """

    async def get_session(self):
        self._session = None
        try:
            self._session = await get_session(self.request)
        except (ValueError, RuntimeError) as err:
            return self.critical(
                response={"message": "Error Decoding Session", "error": str(err)},
                exception=err,
            )
        if not self._session:
            self.error(
                response={
                    "error": "Unauthorized",
                    "message": "Hint: maybe need to login and pass Authorization token.",
                },
                status=403,
            )

    async def get_userid(self, session, idx: str = "user_id") -> int:
        if not session:
            self.error(response={"error": "Unauthorized"}, status=403)
        try:
            if AUTH_SESSION_OBJECT in session:
                return session[AUTH_SESSION_OBJECT][idx]
            else:
                return session[idx]
        except KeyError:
            self.error(
                response={
                    "error": "Unauthorized",
                    "message": "Hint: maybe you need to pass an Authorization token.",
                },
                status=403,
            )

    @staticmethod
    def service_auth(groups: list, *args, **kwargs):
        def _wrapper(fn: F) -> Any:
            @wraps(fn)
            async def _wrap(self, *args, **kwargs) -> web.StreamResponse:
                ## get User Session:
                await self.get_session()
                request = self.request
                if request.get("authenticated", False) is False:
                    # check credentials:
                    raise web.HTTPUnauthorized(
                        reason="Access Denied",
                        headers={
                            hdrs.CONTENT_TYPE: "application/json",
                            hdrs.CONNECTION: "keep-alive",
                        },
                    )
                self._userid = await self.get_userid(self._session)
                self.logger.info(f"Scheduler: Authenticated User: {self._userid}")
                # already a superuser?
                userinfo = self._session[AUTH_SESSION_OBJECT]
                if userinfo.get("superuser", False) is True:
                    self.logger.info(f"Audit: User {self._userid} is calling {fn!r}")
                    return await fn(self, *args, **kwargs)
                # Checking User Permissions:
                if await self._post_auth(groups, *args, **kwargs):
                    self.logger.info(f"Audit: User {self._userid} is calling {fn!r}")
                    return await fn(self, *args, **kwargs)
                else:
                    raise web.HTTPUnauthorized(
                        reason="Access Denied",
                        headers={
                            hdrs.CONTENT_TYPE: "application/json",
                            hdrs.CONNECTION: "keep-alive",
                        },
                    )

            return _wrap

        return _wrapper

    async def _post_auth(self, groups: list, *args, **kwargs):
        """Post-authorization Model."""
        member = False
        userinfo = {}
        try:
            userinfo = self._session[AUTH_SESSION_OBJECT]
        except KeyError:
            member = False
        if "groups" in userinfo:
            member = bool(not set(userinfo["groups"]).isdisjoint(groups))
        else:
            user = self._session.decode("user")
            for group in user.groups:
                if group.group in groups:
                    member = True
        if member is True:
            ## Check Groups belong to User
            return True
        else:
            return False

    @service_auth(groups=SCHEDULER_SERVICE_GROUPS)
    async def get(self):
        app = self.request.app
        scheduler = app["scheduler"]
        args = self.match_parameters(self.request)
        qs = self.query_parameters(self.request)
        try:
            job = args["job"]
        except KeyError:
            job = None
        if job is None:
            if qs.get("calendar"):
                filter_day = qs.get("day", None)
                jobs_data = []
                for job in scheduler.get_all_jobs():
                    if job:
                        ts = job.next_run_time
                        jobs_data.append(
                            {
                                "id": job.id,
                                "name": job.name,
                                "next_run_time": job.next_run_time,
                                "date": ts.date(),
                                "hour": ts.time(),
                                "day": ts.strftime("%a"),
                                "trigger": f"{job.trigger!r}",
                            }
                        )
                # Organize by day
                jobs_by_day = defaultdict(list)
                job_data = sorted(jobs_data, key=lambda x: x["hour"])
                if filter_day:
                    for job in job_data:
                        if job["day"] == filter_day:
                            jobs_by_day[filter_day].append(job)
                    return self.json_response(response=jobs_by_day, state=200)
                else:
                    # returning all days data:
                    for job in job_data:
                        day_key = job["day"]
                        jobs_by_day[day_key].append(job)
                    days_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    job_data = {
                        day: jobs_by_day[day]
                        for day in days_order
                        if day in jobs_by_day
                    }
                return self.json_response(response=job_data, state=200)
            elif qs.get("tabular"):
                job_list = []
                for job in scheduler.get_all_jobs():
                    j = scheduler.get_job(job.id)
                    ts = job.next_run_time
                    obj = {
                        "job_id": job.id,
                        "name": job.name,
                        "trigger": f"{job.trigger!r}",
                        "next_run_time": job.next_run_time,
                        "date": ts.date(),
                        "hour": ts.time(),
                        "day": ts.strftime("%a"),
                        "function": f"{job.func!r}",
                        "last_status": "paused"
                        if not job.next_run_time
                        else j["status"],
                    }
                    job_list.append(obj)
                return self.json_response(response=job_list, state=200)
            job_list = []
            try:
                for job in scheduler.get_all_jobs():
                    j = scheduler.get_job(job.id)
                    if j is None:
                        continue
                    obj = {}
                    obj[job.id] = {
                        "job_id": job.id,
                        "name": job.name,
                        "trigger": f"{job.trigger!r}",
                        "next_run_time": job.next_run_time,
                        "function": f"{job.func!r}",
                        "last_status": "paused" if not job.next_run_time else j["status"],
                    }
                    job_list.append(obj)
            except Exception as err:
                self.logger.exception(f"Error getting Job Scheduler info: {err!s}")
                return self.error(
                    response={"message": f"Error getting Job Scheduler info: {err!s}"},
                    state=406,
                )
            return self.json_response(response=job_list, state=200)
        else:
            # getting all information about a single job.
            try:
                obj = scheduler.get_job(job)
                if not obj:
                    raise NotFound(f"There is no Job {job}")
                data = obj["data"]
                print(obj["data"], obj["status"])
                job = obj["job"]
                if job.next_run_time is None:
                    status = "Paused"
                else:
                    status = obj["status"]
                result = {
                    "job_id": job.id,
                    "name": job.name,
                    "trigger": f"{job.trigger!r}",
                    "next_run_time": job.next_run_time,
                    "last_exec_time": data["last_exec_time"],
                    "function": f"{job.func!r}",
                    "last_status": status,
                    "last_traceback": data["job_state"],
                }
                print(result)
                return self.json_response(response=result, state=200)
            except NotFound as exc:
                return self.error(response={"message": f"{exc}"}, state=400)
            except Exception as err:
                self.logger.exception(f"Error getting Job Scheduler info: {err!s}")
                return self.error(
                    response={"message": f"Error getting Job Scheduler info: {err!s}"},
                    state=406,
                )

    async def put(self):
        app = self.request.app
        scheduler = app["scheduler"]
        return self.json_response(response="Empty", state=204)

    async def reload_jobs(self, scheduler):
        try:
            return await scheduler.create_jobs()
        except Exception as err:
            raise FlowTaskError(f"{err!s}") from err

    @service_auth(groups=SCHEDULER_ADMIN_GROUPS)
    async def patch(self):
        app = self.request.app
        scheduler = app["scheduler"]
        args = self.match_parameters(self.request)
        try:
            job = args["job"]
        except KeyError:
            job = None
        if job is None:
            self.logger.info(
                f"Audit: User {self._userid} is Tearing down the JobStore (removing Jobs)"
            )
            try:
                # Teardown the JobStore using the scheduler's own method
                # so internal state (events, wakeups) stays consistent.
                # Pass no jobstore arg to clear ALL jobstores (default + db).
                scheduler.scheduler.remove_all_jobs()
                scheduler._jobs.clear()
            except Exception as err:
                self.logger.exception(
                    f"Error Teardown the Scheduler {err!r}"
                )
                return self.error(
                    response={"message": f"Error Tearing down Scheduler: {err!r}"}, state=406
                )
            await asyncio.sleep(0.1)
            try:
                self.logger.info("Reloading the Scheduler JobStore ...")
                error = None
                result = []
                try:
                    result = await self.reload_jobs(scheduler)
                except Exception as exc:
                    error = exc
                    self.logger.error(
                        f"Failed to reload jobs: {exc}"
                    )
                result = {
                    "status": "Done",
                    "description": "Scheduler was reloaded.",
                    "reloaded_by": self._userid,
                    "errors": f"{error}",
                    "jobs_loaded": len(result)
                }
                return self.json_response(response=result, state=202)
            except Exception as err:
                self.logger.exception(f"Error Reloading Scheduler {err!r}")
                return self.error(
                    response={"message": f"Error Reloading Scheduler: {err!r}"}, state=406
                )
        else:
            try:
                job_struc = scheduler.get_job(job)
                job = job_struc["job"]
                # getting info about will be paused or removed (TODO removed).
                job.resume()
                return self.json_response(
                    response=f"Job {job} was Resumed from Pause state.", state=202
                )
            except Exception as err:
                self.logger.exception(f"Invalid Job Id {job!s}: {err!s}")
                return self.error(
                    response={"error": f"Invalid Job Id {job!s}: {err!s}"}, state=406
                )

    @service_auth(groups=SCHEDULER_ADMIN_GROUPS)
    async def delete(self):
        app = self.request.app
        scheduler = app["scheduler"]
        args = self.match_parameters(self.request)
        try:
            job = args["job"]
        except KeyError:
            job = None
        if job is None:
            self.logger.info(
                f"Audit: User {self._userid} is shutting down the Scheduler."
            )
            try:
                # Remove all jobs BEFORE shutdown so the scheduler can
                # properly clean up its internal state.
                scheduler.scheduler.remove_all_jobs()
                scheduler._jobs.clear()
                # Now stop the scheduler
                scheduler.scheduler.shutdown(wait=False)
            except Exception as err:
                self.logger.exception(f"Error shutting down Scheduler: {err!r}")
                return self.error(
                    response={"message": f"Error shutting down Scheduler: {err!r}"}, state=406
                )
            self.logger.info("Restarting the Scheduler...")
            try:
                # Restart the scheduler first, then reload jobs
                await scheduler.start()
                await asyncio.sleep(0.1)
                error = None
                result = []
                try:
                    result = await self.reload_jobs(scheduler)
                except Exception as e:
                    error = e
                result = {
                    "status": "Done",
                    "description": "Scheduler was restarted.",
                    "restarted_by": self._userid,
                    "jobs_loaded": len(result),
                    "errors": f"{error}",
                }
                return self.json_response(response=result, state=202)
            except Exception as err:
                self.logger.exception(f"Error Restarting Scheduler {err!r}")
                return self.error(
                    response={"message": f"Error Restarting Scheduler: {err!r}"}, state=406
                )
        else:
            try:
                job_struc = scheduler.get_job(job)
                job = job_struc["job"]
                # getting info about will be paused or removed (TODO removed).
                job.pause()
                return self.json_response(response=f"Job {job} was Paused.", state=202)
            except Exception as err:
                self.logger.exception(
                    f"Invalid Job Id {job!s}: {err!s}"
                )
                return self.error(
                    response={"message": f"Invalid Job Id {job!s}: {err!s}"}, state=406
                )


class JobManager(ModelView):
    model: BaseModel = Job
    path: str = "/api/v1/scheduler/jobs"
    pk: str = 'job_id'

    async def _get_created_by(self, value, column, data):
        return await self.get_userid(session=self._session)

    async def _set_created_by(self, value, column, data):
        return await self.get_userid(session=self._session)

    async def _patch_response(self, result, status: int = 202) -> web.Response:
        """_patch_data.

        Post-processing data after saved and before summit.
        """
        try:
            scheduler = self.request.app["scheduler"]
        except KeyError:
            return self.error(
                response={"message": "Scheduler is not available"},
                status=500
            )
        job = result.job_id
        job_status = result.enabled
        job_struc = scheduler.get_job(job)
        if job_status is False:
            # Job need to be paused
            if not job_struc:
                # there is no jobs in the scheduler
                return self.json_response(result, status=status)
            job_obj = job_struc.get('job', None)
            if job_obj:
                # Remove Job from Jobstore
                job_obj.remove()
        if job_status is True:
            # Job need to be resumed
            if not job_struc:
                # there is no jobs in the scheduler, add it:
                await scheduler.add_job(result.to_dict())
                return self.json_response(result, status=status)
            job_obj = job_struc.get('job', None)
            if not job_obj:
                # Add this job to the Jobstore
                await scheduler.add_job(result.to_dict())
        # I change the job and job is on the scheduler running:
        if job_status is True and job_struc:
            job_obj = job_struc.get('job', None)
            if job_obj:
                # Remove the job, and re-add it.
                job_obj.remove()
                await scheduler.add_job(result.to_dict())
        return self.json_response(result, status=status)

    async def _post_response(
            self,
            response: Any,
            fields: list = None,
            headers: dict = None,
            status: int = 200
    ) -> web.Response:
        """_post_response.

        Post-processing data after saved and before summit.
        """
        try:
            scheduler = self.request.app["scheduler"]
        except KeyError:
            return self.error(
                response={"message": "Scheduler is not available"},
                status=500
            )
        job = response.job_id
        job_status = response.enabled
        job_struc = scheduler.get_job(job)
        if job_status is False and not job_struc:
            # there is no jobs in the scheduler, nothing to do
            return self.json_response(response, status=status)
        # Check if the job alredy exists in the scheduler
        job_obj = job_struc.get('job', None)
        if job_obj:
            # Remove Job from Jobstore before add-it
            try:
                job_obj.remove()
            except Exception:
                pass
            if job_status is True:
                await scheduler.add_job(response.to_dict())
        elif job_obj is None and job_status is True:
            # Job doesn't exists, please add it
            await scheduler.add_job(response.to_dict())
        elif job_status is True and not job_struc:
            # there is no jobs in the scheduler, add it:
            await scheduler.add_job(response.to_dict())
        return self.json_response(response, status=status, headers=headers)
