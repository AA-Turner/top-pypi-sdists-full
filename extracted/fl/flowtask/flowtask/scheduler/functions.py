import asyncio
from typing import Any
from collections.abc import Callable
import time
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from redis import asyncio as aioredis
from querysource.types.validators import Entity
# Queue Worker Client: lazy-loaded to avoid importing notify/pandas at startup.
# from qw.wrappers import TaskWrapper  # deferred to _create_wrapper()
# from qw.client import QClient  # deferred to __call__()
from ..conf import (
    DEBUG,
    default_pg,
    SCHEDULER_WORKER_TIMEOUT,
    SCHEDULER_RETRY_ENQUEUE,
    SCHEDULER_MAX_RETRY_ENQUEUE,
    SCHEDULER_DEFAULT_NOTIFY,
    PUBSUB_REDIS,
    WORKERS_LIST
)
from ..exceptions import (
    FileError,
    FileNotFound,
    NotSupported,
    TaskFailed,
    TaskNotFound,
    DataNotFound,
)
def send_notification(event_loop, message, provider):
    """Lazy wrapper that defers the import of notify until actually needed."""
    from .notifications import send_notification as _send
    # Replace ourselves so subsequent calls go direct
    globals()["send_notification"] = _send
    return _send(event_loop, message, provider)


def import_from_path(path):
    """Import a module / class from a path string.
    :param str path: class path, e.g., ndscheduler.corescheduler.job
    :return: class object
    :rtype: class
    """
    components = path.split(".")
    module = __import__(".".join(components[:-1]))
    for comp in components[1:-1]:
        module = getattr(module, comp)
    return getattr(module, components[-1])


class TaskScheduler:
    def __init__(
        self,
        program,
        task,
        job_id: str,
        priority: str = "low",
        worker: Callable = None,
        **kwargs,
    ):
        self.task = task
        self.program = program
        self.priority = priority
        self.worker = worker
        self._scheduled: bool = False
        self._wrapper_kwargs = kwargs
        self.task_id = None
        self.job_id = job_id
        self.logger = logging.getLogger(
            f"Job.{job_id}"
        )

    def _create_wrapper(self):
        """Create a fresh TaskWrapper with a new UUID per dispatch."""
        from qw.wrappers import TaskWrapper
        return TaskWrapper(
            program=self.program,
            task=self.task,
            ignore_results=True,
            **self._wrapper_kwargs
        )

    async def set_task_status(self, state, error):
        # TODO: migrate to Prepared statements
        _new = False
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            _new = True
        trace = Entity.escapeString(error)
        sentence = f"""UPDATE {self.program}.tasks
        SET task_state='{state}', traceback='{trace}'
        WHERE task = '{self.task}';"""
        result = None
        options = {
            "server_settings": {
                "application_name": "Flowtask.Scheduler",
                "client_min_messages": "notice",
            }
        }
        conn = AsyncDB(
            "pg",
            dsn=default_pg,
            loop=event_loop,
            **options
        )
        try:
            async with await conn.connection() as conn:
                result, error = await conn.execute(sentence)
                if error:
                    self.logger.error(str(error))
            return result
        except Exception as err:
            self.logger.error(f"Task State Error: {err}")
        finally:
            if _new:
                event_loop.stop()

    async def _schedule_task(self, wrapper, queue):
        start_time = time.time()
        try:
            while True:
                try:
                    return await asyncio.wait_for(
                        queue.queue(wrapper), timeout=SCHEDULER_WORKER_TIMEOUT
                    )
                except asyncio.QueueFull as exc:
                    self.logger.error(
                        f"Task {wrapper!r} was missed for enqueue due Queue Full {exc}"
                    )
                    # Set Task State as Discarded:
                    await self.set_task_status(13, str(exc))
                    raise TaskFailed(
                        f"Task {wrapper!r} was discarded due Queue Full {exc}"
                    ) from exc
                except asyncio.TimeoutError as exc:
                    elapsed_time = time.time() - start_time
                    # If more than SCHEDULER_MAX_RETRY_ENQUEUE seconds have passed
                    if elapsed_time >= SCHEDULER_MAX_RETRY_ENQUEUE:
                        self.logger.error(
                            f"Task Discarded {self.program}.{self.task}: {exc}"
                        )
                        # Set Task State as Discarded:
                        await self.set_task_status(13, str(exc))
                        raise TaskFailed(
                            f"Task {wrapper!r} was discarded due timeout {exc}"
                        ) from exc
                    self.logger.warning(
                        f"Task {wrapper!r} could not be enqueued.\
                        Retrying in {SCHEDULER_RETRY_ENQUEUE} seconds."
                    )
                    # Wait for 10 seconds before retrying
                    await asyncio.sleep(SCHEDULER_RETRY_ENQUEUE)
                except OSError as exc:
                    self.logger.error(
                        f"Task {wrapper!r} can't be enqueued Due OS Error: {exc}"
                    )
                    raise
                except Exception as exc:
                    msg = f"Task {wrapper!r} can't be enqueued Due Error: {exc}"
                    await self.set_task_status(13, str(msg))
                    self.logger.error(
                        f"Task {wrapper!r} can't be enqueued by Error: {exc}"
                    )
                    raise
        except KeyboardInterrupt:
            return None

    async def _send_task(self, wrapper, queue):
        """_send_task.

        Send a Task directly to Worker avoiding Worker Queue.
        """
        try:
            result = await queue.run(wrapper)
            await asyncio.sleep(0.01)
            return result
        except (OSError, asyncio.TimeoutError):
            raise
        except Exception as exc:
            self.logger.error(f"{exc}")
            raise

    async def _publish_task(self, wrapper, queue):
        try:
            result = await queue.publish(wrapper)
            await asyncio.sleep(0.01)
            return result
        except asyncio.TimeoutError:
            raise
        except Exception as exc:
            self.logger.error(f"{exc}")
            raise

    async def save_task_id(self):
        try:
            redis = aioredis.from_url(
                PUBSUB_REDIS, encoding="utf-8", decode_responses=True
            )
            # Expire the key after 1 hour (3600 seconds)
            await redis.setex(str(self.task_id), 3600, self.job_id)
        except Exception as exc:
            self.logger.error(
                f"Task ID {self.task_id!r} can't be saved due Error: {exc}"
            )
            raise
        finally:
            await redis.close()
            try:
                await redis.connection_pool.disconnect()
            except Exception:
                pass

    def __call__(self, *args, **kwargs):
        # Create a fresh TaskWrapper per invocation to get a unique UUID
        wrapper = self._create_wrapper()
        self.task_id = wrapper.id
        try:
            try:
                loop = asyncio.new_event_loop()
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Unable to create a New Event Loop for Dispatching Tasks: {exc}"
                ) from exc
            asyncio.set_event_loop(loop)
            self.logger.info(
                f":::: Calling Task {self.program}.{self.task} [{self.task_id}]: priority {self.priority!s}"
            )
            if self.priority == "direct":
                # Direct connection to worker (avoid Worker Queue)
                task = loop.create_task(
                    self._send_task(wrapper, self.worker)
                )
            elif self.priority == "pub":
                # Using Channel Group mechanism (avoid queueing)
                task = loop.create_task(
                    self._publish_task(wrapper, self.worker)
                )
            elif self.priority in ('high', 'low'):
                task = loop.create_task(
                    self._schedule_task(wrapper, self.worker)
                )
                self._scheduled = True
            elif self.priority is None:
                task = loop.create_task(
                    self._schedule_task(wrapper, self.worker)
                )
                self._scheduled = True
            else:
                # Extract which worker to use:
                try:
                    from qw.client import QClient
                    w = WORKERS_LIST[self.priority]
                    worker = QClient(worker_list=w)
                except KeyError:
                    self.logger.error(
                        f"Worker {self.priority!r} not found in Workers List"
                    )
                    worker = self.worker
                task = loop.create_task(
                    self._schedule_task(wrapper, worker)
                )
                self._scheduled = True
            try:
                result = loop.run_until_complete(task)
                if hasattr(result, "get"):
                    message = result.get("message", None)
                    self.logger.info(f"SCHED: {message!r}")
                else:
                    self.logger.info(
                        f"Executed: {self.program}.{self.task} with status {result!r}"
                    )
                # Save UUID of task execution:
                loop.run_until_complete(self.save_task_id())
                return result
            except asyncio.TimeoutError:  # pragma: no cover
                self.logger.error(
                    f"Scheduler: Cannot add task {self.program}.{self.task} to Queue Worker due Timeout."
                )
                send_notification(
                    loop,
                    message=f"Scheduler: Error sending task {self.program}.{self.task} to Worker",
                    provider=SCHEDULER_DEFAULT_NOTIFY,
                )
        except KeyboardInterrupt:
            self._scheduled = True
        except OSError as exc:
            self.logger.error(
                f"Connection Error: {exc}"
            )
            send_notification(
                loop,
                message=f"Scheduler: Task {self.program}.{self.task} Connection Refused: {exc!s}",
                provider=SCHEDULER_DEFAULT_NOTIFY,
            )
            raise
        except Exception as exc:
            self.logger.exception(
                f"Scheduler Queue Error: {exc}",
                stack_info=True
            )
            send_notification(
                loop,
                message=f"Scheduler: Exception on Enqueue {self.program}.{self.task}: {exc!s}",
                provider=SCHEDULER_DEFAULT_NOTIFY,
            )
            raise
        finally:
            try:
                loop.close()
            except Exception:
                pass


async def launch_task(program, task_id, loop, ENV, *args, **kwargs):
    from ..tasks.task import Task
    task = Task(
        task=task_id,
        program=program,
        loop=loop,
        ignore_results=True,
        ENV=ENV,
        debug=DEBUG,
        **kwargs,
    )
    try:
        await task.start()
    except Exception as err:
        logging.error(f"Failing Task Start: {program}.{task_id} with error: {err}")
        raise TaskFailed(f"{err!s}") from err
    try:
        result = await task.run()
        return result
    except (NotSupported, FileNotFound, NoDataFound, DataNotFound):
        raise
    except TaskNotFound as err:
        raise TaskNotFound(f"Task: {task_id}: {err!s}") from err
    except TaskFailed as err:
        raise TaskFailed(f"Task {task_id} failed: {err}") from err
    except FileError as err:
        raise FileError(f"Task {task_id}, File Not Found: {err}") from err
    except Exception as err:
        raise TaskFailed(f"Error: Task {task_id} failed: {err}") from err
    finally:
        try:
            await task.close()
        except Exception as err:
            logging.error(err)


def thread_wrapper(program, task_id, loop, *args, **kwargs):
    logging.info(
        f"Calling Task: {program}.{task_id} on ThreadPool Executor."
    )

    def run_task(loop: asyncio.AbstractEventLoop):
        from ..tasks.task import Task
        asyncio.set_event_loop(loop)
        result = None
        task = Task(
            program=program, task=task_id, ignore_results=True, loop=loop, debug=DEBUG
        )
        try:
            loop.run_until_complete(task.start())
            result = loop.run_until_complete(task.run())
            return result
        except (NotSupported, FileNotFound, NoDataFound):
            raise
        except TaskNotFound as err:
            raise TaskNotFound(
                f"Task: {task_id}: {err!s}"
            ) from err
        except TaskFailed as err:
            raise TaskFailed(
                f"Task {task_id} failed: {err}"
            ) from err
        except FileError as err:
            raise FileError(
                f"Task {task_id}, File Not Found: {err}"
            ) from err
        except Exception as err:
            logging.error(
                f"Error running Task: {program}.{task_id} from Process: {err!s}"
            )
            raise TaskFailed(f"{err!s}") from err
        finally:
            loop.run_until_complete(task.close())

    try:
        loop = asyncio.new_event_loop()
        with ThreadPoolExecutor(max_workers=10) as pool:
            result = loop.run_in_executor(pool, run_task)
        return result
    except (NotSupported, FileNotFound, FileError, NoDataFound, DataNotFound):
        raise
    except TaskFailed:
        raise
    except Exception as err:
        raise TaskFailed(
            f"Error: Task {program}.{task_id} failed: {err}"
        ) from err
    # finally:
    #     loop.stop()


def process_wrapper(program, task_id, *args, **kwargs):
    logging.info(
        f"Calling Task: {program}.{task_id} on ProcessPool Executor."
    )
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def run_task():
        from ..tasks.task import Task
        result = None
        task = Task(
            program=program,
            task=task_id,
            ignore_results=True,
            loop=loop,
            debug=DEBUG
        )
        try:
            loop.run_until_complete(task.start())
            result = loop.run_until_complete(task.run())
            return result
        except (NotSupported, FileNotFound, NoDataFound):
            raise
        except TaskNotFound as err:
            raise TaskNotFound(f"Task: {task_id}: {err!s}") from err
        except TaskFailed as err:
            raise TaskFailed(f"Task {task_id} failed: {err}") from err
        except FileError as err:
            raise FileError(f"Task {task_id}, File Not Found: {err}") from err
        except Exception as err:
            logging.error(
                f"Error running Task: {program}.{task_id} from Process: {err!s}"
            )
            raise TaskFailed(f"{err!s}") from err
        finally:
            loop.run_until_complete(task.close())

    try:
        return run_task()  # This function will be called in the child process
    finally:
        loop.close()


def get_function(job: dict, priority: str = "low", worker: Callable = None):
    fn = job["job"]
    if not fn:
        raise ValueError(
            f"Job with bad syntax: {job!r}"
        )
    try:
        job_id = job["job_id"]
    except KeyError:
        raise RuntimeError(
            f"Job with bad syntax: {job!r}"
        )
    # default is a task function
    t = fn.get('type', 'task')
    params = job.get('params', {})
    if not params:
        params = {}
    try:
        func = fn[t]
    except KeyError as ex:
        raise RuntimeError(
            f"Error getting Function on Schedule {t}: {ex}"
        ) from ex
    if t == "function":
        try:
            fn = globals()[func]
            return fn
        except Exception as err:
            raise RuntimeError(f"Error: {err!s}") from err
    elif t == "package":
        try:
            fn = import_from_path(func)
            return fn
        except Exception as err:
            raise RuntimeError(f"Error: {err!s}") from err
    elif t == "task":
        task, program = fn["task"].values()
        if priority == "local":
            # run in a function wrapper
            func = partial(launch_task, program, task)
            return func
        else:
            executor = job["executor"]
            if executor == "default":
                # Using asyncio Executor
                sched = TaskScheduler(
                    program,
                    task,
                    job_id,
                    priority,
                    worker,
                    **params
                )
                sched.__class__.__name__ = f"Task({program}.{task})"
                return sched
            elif executor == "process":
                return process_wrapper
            elif executor == "thread":
                func = partial(thread_wrapper, program, task, **params)
                return func
            else:
                raise RuntimeError(f"Error: Executor {executor!r} not supported")
    else:
        return None
