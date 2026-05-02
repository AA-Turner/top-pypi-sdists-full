"""
NavScheduler.

Job for attaching tasks to the Scheduler.
"""
import asyncio
import locale
import os
import socket
import sys
import traceback
import zoneinfo
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor as ThreadExecutor
from datetime import datetime, timedelta
from functools import partial
from redis import asyncio as aioredis
from aiohttp import web
from apscheduler.events import (
    EVENT_JOB_ADDED,
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MAX_INSTANCES,
    EVENT_JOB_MISSED,
    EVENT_JOB_SUBMITTED,
    EVENT_SCHEDULER_SHUTDOWN,
    EVENT_SCHEDULER_STARTED,
    JobExecutionEvent,
)
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.debug import DebugExecutor
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError

# Jobstores
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.rethinkdb import RethinkDBJobStore

# apscheduler library  #
# Default Scheduler:
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
# from apscheduler.util import utc
from pytz import utc

# Triggers
from apscheduler.triggers.interval import IntervalTrigger

# navconfig
from navconfig import config as navConfig
from navconfig.logging import logging

# asyncdb:
from asyncdb import AsyncDB
from navigator.connections import PostgresPool
from querysource.types.validators import Entity

# Queue Worker Client: lazy-loaded to avoid importing notify at startup.
# from qw.client import QClient  # deferred to set_workers()

# Configuration
from ..conf import (
    CACHE_HOST,
    CACHE_PORT,
    ENABLE_JOBS,
    ENVIRONMENT,
    SCHEDULER_GRACE_TIME,
    SCHEDULER_MAX_INSTANCES,
    SYSTEM_LOCALE,
    TIMEZONE,
    WORKER_HIGH_LIST,
    WORKER_LIST,
    default_dsn,
    USE_TIMEZONE,
    PUBSUB_REDIS,
    ERROR_CHANNEL,
    ALLOW_RESCHEDULE,
    SCHEDULER_STARTUP_JOB
)
from ..utils.json import json_decoder

# Handler
from .handlers import SchedulerManager, JobManager
from .functions import TaskScheduler, get_function


# disable logging of APScheduler
logging.getLogger("apscheduler").setLevel(logging.WARNING)


jobstores = {
    "default": MemoryJobStore(),
    "db": RedisJobStore(
        db=3,
        jobs_key="apscheduler.jobs",
        run_times_key="apscheduler.run_times",
        host=CACHE_HOST,
        port=CACHE_PORT,
    ),
    # "rethink": RethinkDBJobStore(
    #     database="scheduler",
    #     table="jobs",
    # )
}

job_defaults = {
    "coalesce": True,
    "max_instances": SCHEDULER_MAX_INSTANCES,
    "misfire_grace_time": SCHEDULER_GRACE_TIME,
}


# SCHEDULER_LOCK_KEY = "navigator_singleton_lock"


class NavScheduler:
    """NavScheduler.

    Demonstrates how to use the asyncio compatible scheduler to schedule jobs.
    """

    def __init__(self, event_loop=None):
        self.db = None
        self._pool = None
        self._connection = None
        self._redis = None
        self._jobs: dict = {}
        self._loop = None
        self.scheduler = None
        self._args = None
        self._event = asyncio.Event()
        if event_loop:
            self._loop = event_loop
        else:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        # logging
        self.logger = logging.getLogger(name="Flowtask.Scheduler")
        # asyncio scheduler
        if TIMEZONE == 'UTC':
            self._timezone = utc
        else:
            self._timezone = zoneinfo.ZoneInfo(key=TIMEZONE)
        self.jobstores = jobstores
        # defining Locale
        try:
            locale.setlocale(locale.LC_ALL, SYSTEM_LOCALE)
        except locale.Error as e:
            self.logger.exception(e, exc_info=True)
        # # Cluster lock attributes (disabled — cluster feature has design flaws)
        # self._renewal_interval: int = 60
        # self._scheduler_ttl: int = 180
        # self._lock_check_interval: int = 120
        self.set_workers()

    def setup(self, app: web.Application):
        self.db = PostgresPool(
            dsn=default_dsn,
            name="FlowTask.Scheduler",
            startup=self.startup
        )
        self.db.configure(app, register="database")  # pylint: disable=E1123
        # add the scheduler to the current app
        app["scheduler"] = self
        # add the routes:
        app.router.add_view("/api/v2/scheduler", SchedulerManager)
        app.router.add_view("/api/v2/scheduler/{job}", SchedulerManager)
        # Job Manager:
        JobManager.configure(app)
        # define subscribers
        app.on_startup.append(self.start_subscriber)
        app.on_cleanup.append(self.stop_subscriber)

    async def _start_redis(self):
        self._redis = aioredis.from_url(
            PUBSUB_REDIS, encoding="utf-8", decode_responses=True
        )

    async def _stop_redis(self):
        try:
            await self._redis.close()
            await self._redis.connection_pool.disconnect()
        except Exception:
            pass

    async def listen_task_events(self):
        try:
            async with self._redis.pubsub() as pubsub:
                await pubsub.subscribe(ERROR_CHANNEL)
                future = asyncio.create_task(self.event_reader(pubsub))
                await future
        except Exception as exc:
            print(exc)

    async def start_subscriber(self, app):
        ## listen subscriber:
        self.logger.notice(':: Starting Task Subscriber :: ')
        app["redis_listener"] = asyncio.get_event_loop().create_task(
            self.listen_task_events()
        )

    async def stop_subscriber(self, app):
        self.logger.notice("Stopping subscriber")
        self._event.set()
        app["redis_listener"].cancel()

    async def get_job_id(self, task_id: str) -> str:
        try:
            if job := await self._redis.get(task_id):
                # delete this task id from redis:
                await self._redis.delete(task_id)
                return job
        except Exception as err:
            self.logger.warning(f"Error Getting Task ID from Redis: {err}")
        return None

    async def event_reader(self, channel: aioredis.client.PubSub):
        try:
            while not self._event.is_set():
                msg = await channel.get_message(ignore_subscribe_messages=True)
                if msg is not None:
                    message = json_decoder(msg["data"])
                    status = message.get("status", "error")
                    task = message.get("task", None)
                    task_id = message.get("task_id", None)
                    if status != "task not found":
                        # check if the task was dispatched by me:
                        if job_id := await self.get_job_id(task_id):
                            self.logger.error(f"Received Failed Task: {msg}")
                            self.process_failed_task(task, job_id)
        except Exception as err:
            self.logger.warning(
                f"Stopping Task Event Subscription {err}"
            )
        finally:
            await channel.unsubscribe(ERROR_CHANNEL)

    def process_failed_task(self, task_name: str, job_id: str = None):
        program, task = task_name.split(".")
        if not job_id:
            job_id = f"{program}_{task}"
        try:
            info = self._jobs[job_id]
            job_info = info.get("data", None)
            if not job_info:
                return
            _max = job_info.get("rescheduled_max", None)
            if ALLOW_RESCHEDULE is True and job_info["reschedule"] is True:
                if info["status"] not in ("dispatched", "success", "retry"):
                    # This task was not dispatched by me, returning
                    return
                job = self.scheduler.get_job(job_id)
                if info["retry"] > 0 and _max is None:
                    # we need to stop the rescheduling:
                    return
                if _max is not None and info["retry"] >= _max:
                    # We cannot reschedule this task again, returning
                    return
                # Jitter for re-scheduling in minutes
                jitter = job_info.get("reschedule_jitter", 5)
                old_trigger = job.trigger
                if not info["trigger"]:
                    # only set if not already set:
                    self._jobs[job_id]["trigger"] = old_trigger
                job.reschedule(trigger=IntervalTrigger(minutes=jitter))
                self._jobs[job_id]["retry"] += 1
                self._jobs[job_id]["status"] = "retry"
                self.logger.warning(
                    f"Job {job_id} was re-scheduled to {jitter} minutes"
                )
        except KeyError:
            return

    # # --- Cluster lock methods (disabled — cluster feature has design flaws) ---
    # async def acquire_scheduler_lock(self):
    #     if await self._redis.set(
    #         SCHEDULER_LOCK_KEY,
    #         "locked",
    #         ex=self._scheduler_ttl,
    #         nx=True
    #     ):
    #         return True
    #     return False
    #
    # async def renew_scheduler_lock(self):
    #     await self._redis.expire(SCHEDULER_LOCK_KEY, self._scheduler_ttl)
    #     print("Scheduler lock key renewed.")

    def _create_scheduler(self) -> AsyncIOScheduler:
        """_create_scheduler.

        Create a new APScheduler AsyncIOScheduler instance.
        """
        return AsyncIOScheduler(
            jobstores=self.jobstores,
            executors={
                "default": AsyncIOExecutor(),
                "process": ProcessPoolExecutor(max_workers=12),
                "asyncio": AsyncIOExecutor(),
                "thread": ThreadPoolExecutor(max_workers=16),
                "debug": DebugExecutor(),
            },
            job_defaults=job_defaults,
            timezone=self._timezone,
        )

    async def start_scheduler(self):
        self.scheduler = self._create_scheduler()
        # getting Jobs
        await self.create_jobs()
        # # --- Cluster renewal lock job (disabled — cluster feature has design flaws) ---
        # job_id = 'renewal_lock'
        # job = self.scheduler.add_job(
        #     self.renew_scheduler_lock,
        #     id=job_id,
        #     name="renewal_lock",
        #     logger=self.logger,
        #     jobstore_retry_interval=30,
        #     jobstore="default",
        #     executor="default",
        #     trigger=IntervalTrigger(
        #         seconds=self._renewal_interval
        #     ),
        #     replace_existing=True,
        #     remove_job_on_completion=True,
        # )
        # self._jobs[job_id] = {
        #     "data": None,
        #     "job": job,
        #     "status": "idle",
        #     "trigger": None,
        #     "retry": 0,
        # }
        # adding listeners
        self.add_listeners()
        self.logger.info(
            f"Scheduled Started at {datetime.now()}"
        )
        try:
            # starting scheduler
            self.scheduler.start()
        except Exception as err:
            st = self.get_stacktrace()
            message = f"Error Starting Scheduler: {err!s} {st!s}"
            self.send_message(message)
            raise RuntimeError(
                f"Error Starting Scheduler {err!r}"
            ) from err

    def send_message(self, message: str) -> None:
        from .notifications import send_notification
        try:
            # send notification:
            event_loop = asyncio.new_event_loop()
            fn = partial(
                send_notification,
                event_loop=event_loop,
                message=message,
                provider="telegram",
            )
            # sending function coroutine to a thread
            with ThreadExecutor(max_workers=1) as pool:
                event_loop.run_in_executor(pool, fn)
        finally:
            event_loop.close()

    def set_workers(self) -> None:
        """
        Create the instance of Queue Workers.
        """
        from qw.client import QClient
        if WORKER_LIST:
            self.qworker = QClient(worker_list=WORKER_LIST)
            self.qworker_high = QClient(worker_list=WORKER_HIGH_LIST)
        else:
            self.qworker = QClient()  # auto-discovering of workers
            self.qworker_high = self.qworker

    async def startup(self, app: web.Application, conn: Callable):
        """
        Scheduler Startup.
        """
        await self._start_redis()
        try:
            self._pool = conn
        except Exception as err:
            self.logger.exception(err)
            raise RuntimeError(
                f"{err!s}"
            ) from err
        # auxiliary connection
        if self._pool:
            self._connection = await self._pool.acquire()
            # set Zoneinfo:
        if USE_TIMEZONE is True:
            tz = f"SET timezone TO '{TIMEZONE}'"
            await self._connection.execute(tz)
        # # --- Cluster lock gating (disabled — cluster feature has design flaws) ---
        # if await self.acquire_scheduler_lock() is True:
        #     await self.start_scheduler()
        #     app["_scheduler_"] = self.scheduler
        # else:
        #     self.logger.warning(
        #         ":: Another worker is running the scheduler. Checking again shortly ::"
        #     )
        # asyncio.create_task(self.periodic_lock_check(app))

        # Always start the scheduler (no cluster lock)
        await self.start_scheduler()
        app["_scheduler_"] = self.scheduler

    # # --- Cluster periodic lock check (disabled — cluster feature has design flaws) ---
    # async def periodic_lock_check(self, app: web.Application):
    #     """Periodically checks if the lock is available, attempting to acquire if not held."""
    #     while True:
    #         if not await self._redis.exists(SCHEDULER_LOCK_KEY):
    #             self.logger.info(
    #                 "Scheduler lock key was lost, trying to acquire again."
    #             )
    #             try:
    #                 self.scheduler.shutdown(wait=True)
    #             except Exception:
    #                 pass
    #             if await self.acquire_scheduler_lock() is True:
    #                 print("Scheduler lock acquired. Starting scheduler.")
    #                 await self.start_scheduler()
    #                 app["_scheduler_"] = self.scheduler
    #         await asyncio.sleep(self._lock_check_interval)

    @property
    def event_loop(self):
        return self._loop

    def set_test_job(self):
        self.logger.debug("Scheduler: Adding a Test job")
        run_date = datetime.now(self._timezone) + timedelta(minutes=1)
        # define Task:
        program = "navigator"
        task = "startup_job"
        job_id = "on_startup_job"
        sched = TaskScheduler(program, task, job_id, worker=self.qworker)
        sched.__class__.__name__ = f"Task({program}.{task})"
        self.scheduler.add_job(
            sched,
            id=job_id,
            name="startup_test_job",
            logger=self.logger,
            jobstore_retry_interval=30,
            jobstore="default",
            executor="default",
            trigger=DateTrigger(run_date=run_date, timezone=self._timezone),
            replace_existing=True,
            remove_job_on_completion=True,
        )

    async def create_jobs(self):
        self._jobs = {}
        jobs = []
        error = None
        if ENABLE_JOBS is True:
            # Job for self-service discovering
            async with await self._pool.acquire() as conn:
                sql_jobs = "SELECT * FROM troc.jobs WHERE enabled = true"
                try:
                    jobs, error = await conn.query(sql_jobs)
                except Exception as err:
                    # try to reconnect to DB:
                    error = f"Error getting Jobs, Unable to Connect to DB: {err!s}"
        if error:
            raise RuntimeError(
                f"[{ENVIRONMENT} - Scheduler] Error getting Jobs: {error!s}"
            )
        # Add a Job for testing purposes.
        if SCHEDULER_STARTUP_JOB is True:
            self.set_test_job()
        for job in jobs:
            try:
                await self.add_job(job)
            except ValueError as err:
                self.logger.error(
                    f"Scheduler: Work Job info {job!r}: {err!s}"
                )
                continue
            except Exception as err:
                self.logger.error(
                    f"Scheduler: Error Adding Job {job['job_id']}: {err!s}"
                )
                continue
        return self._jobs

    async def add_job(self, job: dict):
        """add_job.

        Add a Job to the Scheduler.
        """
        jitter = None
        job_id = job["job_id"]
        if job["jitter"]:
            jitter = job["jitter"]
        # function or other call
        priority = job.get("priority", "low")
        attributes = []
        if priority == "high":
            worker = self.qworker_high
        else:
            worker = self.qworker
        try:
            func = get_function(job, priority=priority, worker=worker)
        except ValueError:
            raise
        if job["executor"] == "process":
            task, program = job["job"]["task"].values()
            attributes = [program, task]
        schedule_type = job["schedule_type"]
        if schedule_type is None:
            raise ValueError(
                f"Schedule Type for job {job_id} is None"
            )
        try:
            if job["schedule"] is None:
                raise ValueError(
                    f"Schedule for job {job_id} is None"
                )
            if schedule_type == "interval":
                t = job["schedule"]
                if job["start_date"]:
                    t = {**t, **{"start_date": job["start_date"]}}
                if job["end_date"]:
                    t = {**t, **{"end_date": job["end_date"]}}
                trigger = IntervalTrigger(**t)
            elif schedule_type == "crontab":
                t = job["schedule"]["crontab"]
                tz = job["schedule"].get("timezone", TIMEZONE)
                trigger = CronTrigger.from_crontab(t, timezone=tz)
            elif schedule_type == "cron":
                # trigger = self.get_cron_params(job['schedule'])
                trigger = job["schedule"]
                if job["start_date"]:
                    trigger = {**trigger, **{"start_date": job["start_date"]}}
                if job["end_date"]:
                    trigger = {**trigger, **{"end_date": job["end_date"]}}
                if jitter:
                    trigger = {**trigger, **{"jitter": jitter}}
                trigger = CronTrigger(**trigger)
            elif schedule_type == "date":
                trigger = DateTrigger(run_date=job["run_date"], timezone=self._timezone)
            elif schedule_type == "combined":
                # syntax:
                # { type="and", "schedule": [{"cron": "cron"}, {"cron": "cron"} ] }
                t = job["schedule"]
                try:
                    jointype = t["type"]
                except KeyError:
                    jointype = "and"
                steps = []
                for trigger in t["schedule"]:
                    # the expression need to be equal to Trigger Requirements
                    for step, value in trigger.items():
                        obj = self.get_trigger(step)
                        tg = obj(**value)
                        steps.append(tg)
                if jointype == "and":
                    trigger = AndTrigger(steps)
                else:
                    trigger = OrTrigger(steps)
            else:
                raise ValueError(f"Unknown schedule type: {schedule_type}")
        except TypeError as err:
            message = f'Error Adding Job with Id {job_id}: {err}'
            self.logger.error(message)
            self.send_message(message)
            return
        ## Building Job for Scheduler:
        job_struct = {
            "id": f"{job_id}",
            "name": f"{job_id}",
            "replace_existing": True,
            "jobstore": job["jobstore"],
            "executor": job["executor"],
        }
        arguments = {}
        if job["params"]:
            arguments = {**job["params"]}
        # agregar al args que recibe la tarea:
        if job["executor"] != "process":
            # we cannot pass an event loop to ProcessPoolExecutor
            arguments["loop"] = self._loop
            arguments["ENV"] = navConfig
        if job["attributes"]:
            attributes = job["attributes"]
        ## add this job
        if job_struct:
            try:
                j = self.scheduler.add_job(
                    func,
                    logger=self.logger,
                    jobstore_retry_interval=30,
                    trigger=trigger,
                    kwargs=arguments,
                    args=attributes,
                    **job_struct,
                )
                info = {
                    "data": job,
                    "job": j,
                    "status": "idle",
                    "trigger": None,
                    "retry": 0,
                }
                self._jobs[job_id] = info
            except TypeError as exc:
                self.logger.error(
                    f"Scheduler: Error Adding Job {job_id}: {exc}"
                )
                return
            except ConflictingIdError as err:
                self.logger.error(
                    f"Scheduler: Conflicting Error with ID {job_id}: {err}"
                )
                return
            except Exception as err:
                self.logger.exception(
                    f"Scheduler: Error Adding Job {job_id}: {err}",
                    stack_info=True
                )
                return
        else:
            self.logger.error(
                "Scheduler: Missing Scheduled Job Structure"
            )

    def add_listeners(self):
        # Asyncio Scheduler
        self.scheduler.add_listener(self.scheduler_status, EVENT_SCHEDULER_STARTED)
        self.scheduler.add_listener(self.scheduler_shutdown, EVENT_SCHEDULER_SHUTDOWN)
        self.scheduler.add_listener(self.job_success, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self.job_status, EVENT_JOB_ERROR | EVENT_JOB_MISSED)
        # job was submitted:
        self.scheduler.add_listener(self.job_submitted, EVENT_JOB_SUBMITTED)
        # a new job was added:
        self.scheduler.add_listener(self.job_added, EVENT_JOB_ADDED)

    def job_added(self, event: JobExecutionEvent, *args, **kwargs):
        try:
            job = self.scheduler.get_job(event.job_id)
            job_name = job.name
            # TODO: using to check if tasks were added
            self.logger.info(f"Job Added: {job_name} with args: {args!s}/{kwargs!r}")
            # self.logger.notice(
            #     f'Job {job_name!s} was added with args: {args!s}/{kwargs!r}'
            # )
        except Exception:
            pass

    def get_jobs(self):
        return [job.id for job in self.scheduler.get_jobs()]

    def get_all_jobs(self):
        if self.scheduler is None:
            raise RuntimeError(
                "Scheduler not started. Please start the scheduler first."
            )
            return None
        try:
            return self.scheduler.get_jobs()
        except AttributeError:
            raise RuntimeError(
                "Scheduler not started. Please start the scheduler first."
            )

    def get_job(self, job_id):
        try:
            return self._jobs[job_id]
        except JobLookupError as err:
            self.logger.warning(f"Error found a Job with ID: {err}")
            return None
        except KeyError:
            return None

    def scheduler_status(self, event):
        print(event)
        self.logger.debug(f"[{ENVIRONMENT} - NAV Scheduler] :: Started.")
        self.logger.info(
            f"[{ENVIRONMENT} - NAV Scheduler] START time is: {datetime.now()}"
        )

    def scheduler_shutdown(self, event):
        self.logger.info(
            f"[{ENVIRONMENT}] Scheduler {event} Stopped at: {datetime.now()}"
        )

    def fix_job_schedule(self, job, job_id):
        """fix_job_schedule.

        Return a re-scheduled Job to current schedule.

        Args:
            job (APscheduler.job.Job): instance of APScheduler Job.
            job_id (str): ID of the job
        """
        if job_id in self._jobs and "trigger" in self._jobs[job_id]:
            try:
                trigger = self._jobs[job_id]["trigger"]
                if trigger and job.trigger != trigger:
                    # This task was rescheduled:
                    job.reschedule(trigger=trigger)
                    self._jobs[job_id]["trigger"] = None
                    self._jobs[job_id]["status"] = "reverted"
                    self.logger.info(f"Job {job_id} reverted to its original schedule.")
            except Exception as err:
                self.logger.warning(
                    f"Error while reverted job {job_id} to original schedule: {err}"
                )

    def job_success(self, event: JobExecutionEvent):
        """Job Success.

        Event when a Job was executed successfully.

        :param apscheduler.events.JobExecutionEvent event: job execution event
        """
        job_id = event.job_id
        try:
            job = self.scheduler.get_job(job_id)
        except JobLookupError as err:
            self.logger.warning(f"Error found a Job with ID: {err}")
            return False
        try:
            self.fix_job_schedule(job, job_id)
            self._jobs[job_id]["status"] = "success"
        except KeyError:
            # Job is missing from the Job Store.
            return False
        job_name = job.name
        self.logger.info(
            f"[Scheduler - {ENVIRONMENT}]: {job_name} with id {event.job_id!s} \
            was queued/executed successfully @ {event.scheduled_run_time!s}"
        )
        # saving into Database
        event_loop = asyncio.new_event_loop()
        fn = partial(self.save_db_event, event_loop=event_loop, event=event, job=job)
        try:
            with ThreadExecutor(max_workers=1) as pool:
                event_loop.run_in_executor(pool, fn)
        finally:
            event_loop.close()

    def job_status(self, event: JobExecutionEvent):
        """React on Error events from scheduler.

        :param apscheduler.events.JobExecutionEvent event: job execution event.

        TODO: add the reschedule_job
        scheduler = sched.scheduler #it returns the native apscheduler instance
        scheduler.reschedule_job('my_job_id', trigger='cron', minute='*/5')

        """
        job_id = event.job_id
        job = self.scheduler.get_job(job_id)
        self.fix_job_schedule(job, job_id)
        try:
            saved_job = self._jobs[job_id]
        except KeyError as exc:
            self.logger.warning(f"Error found a Job with ID: {exc}")
            return
        job_name = job.name
        scheduled = event.scheduled_run_time
        stack = event.traceback
        if event.code == EVENT_JOB_MISSED:
            self._jobs[job_id]["status"] = "missed"
            self.logger.warning(
                f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} \
                was missed for scheduled run at {scheduled}"
            )
            message = f"⚠️ :: [{ENVIRONMENT} - NAV Scheduler] Job {job_name} was missed \
            for scheduled run at {scheduled}"
        elif event.code == EVENT_JOB_ERROR:
            saved_job["status"] = "error"
            self.logger.error(
                f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} scheduled at \
                {scheduled!s} failed with Exception: {event.exception!s}"
            )
            message = f"🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job **{job_name}** \
             scheduled at {scheduled!s} failed with Error {event.exception!s}"
            if stack:
                self.logger.exception(
                    f"[{ENVIRONMENT} - NAV Scheduler] Job {job_name} id: {job_id!s} \
                    StackTrace: {stack!s}"
                )
                message = f"🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job \
                **{job_name}**:**{job_id!s}** failed with Exception {event.exception!s}"
            # send a Notification error from Scheduler
        elif event.code == EVENT_JOB_MAX_INSTANCES:
            saved_job["status"] = "Not Submitted"
            self.logger.exception(
                f"[{ENVIRONMENT} - Scheduler] Job {job_name} could not be submitted \
                Maximum number of running instances was reached."
            )
            message = f"⚠️ :: [{ENVIRONMENT} - NAV Scheduler] Job **{job_name}** was \
            missed for scheduled run at {scheduled}"
        else:
            saved_job["status"] = "exception"
            # will be an exception
            message = f"🛑 :: [{ENVIRONMENT} - NAV Scheduler] Job \
            {job_name}:{job_id!s} failed with Exception {stack!s}"
            # send a Notification Exception from Scheduler
        # send notification:
        from .notifications import send_notification
        event_loop = asyncio.new_event_loop()
        fn = partial(
            send_notification,
            event_loop=event_loop,
            message=message,
            provider="telegram",
        )
        saved = partial(self.save_db_event, event_loop=event_loop, event=event, job=job)
        # sending function coroutine to a thread
        try:
            with ThreadExecutor(max_workers=1) as pool:
                event_loop.run_in_executor(pool, saved)
                event_loop.run_in_executor(pool, fn)
        finally:
            event_loop.close()

    def save_db_event(self, event_loop, event, job):
        asyncio.set_event_loop(event_loop)
        state = Entity.escapeString(event.exception)
        trace = Entity.escapeString(event.traceback)
        if event.code == EVENT_JOB_MISSED:
            status = 3
        elif event.code == EVENT_JOB_ERROR:
            status = 2
        elif event.code == EVENT_JOB_MAX_INSTANCES:
            status = 4
        else:
            state = "null"
            trace = "null"
            status = 1
        status = {
            "last_exec_time": event.scheduled_run_time,
            "next_run_time": job.next_run_time,
            "job_state": state,
            "job_status": status,
            "traceback": trace,
            "job_id": event.job_id,
        }
        try:
            result = event_loop.run_until_complete(
                self.update_task_status(event_loop, status)
            )
            if isinstance(result, Exception):
                self.logger.exception(result)
        except Exception as err:
            print(err)
            self.logger.exception(err)

    async def update_task_status(self, event_loop, status):
        # TODO: migrate to Prepared statements
        asyncio.set_event_loop(event_loop)
        sql = """UPDATE troc.jobs
        SET last_exec_time='{last_exec_time}', next_run_time='{next_run_time}',
        job_status='{job_status}', job_state='{job_state}', traceback='{traceback}'
        WHERE job_id = '{job_id}';"""
        sentence = sql.format(**status)
        result = None
        options = {
            "server_settings": {
                "application_name": "Flowtask.Scheduler",
                "client_min_messages": "notice",
                "jit": "on",
            },
            "timeout": 360,
        }
        conn = AsyncDB("pg", dsn=default_dsn, loop=event_loop, **options)
        try:
            async with await conn.connection() as conn:
                result, error = await conn.execute(sentence)
                if error:
                    self.logger.error(error)
            return result
        except Exception as err:
            self.logger.exception(err, stack_info=True)

    def job_submitted(self, event):
        try:
            job_id = event.job_id
            job = self.scheduler.get_job(job_id)
        except JobLookupError as exc:
            raise RuntimeError(
                f"Scheduler: There is no such Job {job_id}: {exc}"
            ) from exc
        except Exception as err:
            raise RuntimeError(f"Scheduler: Error on {job_id} {err}") from err
        try:
            job_name = job.name
            now = datetime.now()
            self.logger.info(
                f"Sched: Job {job_name} with id {job_id!s} was submitted @ {now}"
            )
            self._jobs[job_id]["status"] = "dispatched"
        except AttributeError as exc:
            # we don't need to worry about startup_job.
            if event.job_id == "on_startup_job":
                return
            raise RuntimeError(f"Scheduler: Error {exc}") from exc

    def get_stacktrace(self):
        """Returns the full stack trace."""

        type_, value_, traceback_ = sys.exc_info()
        return "".join(traceback.format_exception(type_, value_, traceback_))

    def get_hostname(self):
        """Returns the host name."""
        return socket.gethostname()

    def get_pid(self):
        """Returns the process ID"""
        return os.getpid()

    async def start(self):
        try:
            # asyncio scheduler
            self.scheduler.start()
        except Exception as err:
            raise RuntimeError(f"Error Starting Scheduler {err!r}") from err

    async def shutdown(self, app: web.Application):
        try:
            await self._stop_redis()
        except Exception:
            pass
        try:
            self.scheduler.shutdown(wait=True)
        except AttributeError:
            pass
        except Exception as err:
            self.logger.exception(f"Error Shutting Down The Scheduler {err!r}")
        try:
            if self._connection:
                await self._pool.release(self._connection)
            await self.db.shutdown(app)
        except Exception as err:
            self.logger.exception(
                f"Error on Scheduler Shutdown {err!r}"
            )

    def get_cron_params(self, expression):
        trigger = {
            "year": "*",
            "month": "*",
            "day": "*",
            "week": "*",
            "day_of_week": "*",
            "hour": "*",
            "minute": "*",
            "second": "0",
        }
        return {**trigger, **expression}

    def get_cron_strings(self, expression):
        """Returns cron strings.
        :param dict expression: an array of cron structures.
        :return: cron strings
        :rtype: dict
        """
        trigger = expression["cron"]
        return {
            "month": str(trigger[1]),
            "day": str(trigger[2]),
            "week": str(trigger[3]),
            "day_of_week": str(trigger[4]),
            "hour": str(trigger[5]),
            "minute": str(trigger[6]),
        }

    def get_trigger(self, expression):
        if expression == "cron" or expression == "crontab":
            return CronTrigger
        elif expression == "date":
            return DateTrigger
        elif expression == "interval":
            return IntervalTrigger
        else:
            self.logger.exception(f"Wrong Trigger type: {expression}")
            return None
