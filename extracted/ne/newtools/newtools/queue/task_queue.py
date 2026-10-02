# (c) 2012-2018 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)
import queue
import time
import datetime
import logging


class Task:
    """
    An abstraction representing a Single task
    """

    def __init__(self, name, arguments):
        self.is_complete = False
        self.error = None
        self.arguments = arguments
        self.id = None
        self.retries = 0
        self.name = name


class TaskQueue:
    """
    This is an abstract class that contains all required common functionality to
    support implementation of queues in aws client libraries.

    Two separate queues are maintained:

    active_queue
    ------------

    - Only tasks in this queue are allowed to run.
    - Once tasks are completed they are removed from this queue.
    - No of tasks in active queue <= max_size.

    pending_queue
    -------------

    - Contains tasks that are awaiting execution.
    - Tasks from pending_queue are added to active_queue in FIFO fashion.
    """

    def __init__(self, max_size,
                 retry_limit=3,
                 logger=logging.getLogger("newtools.queue")):
        self.pending_tasks = queue.Queue()
        self.active_queue = []
        self.max_size = max_size
        self.retry_limit = retry_limit
        self._time_first_job_added = datetime.datetime.now()
        self._tasks_completed = 0
        self._logger = logger

    def add_task(self, name, args):
        """This method adds a tasks to the pending_tasks queue"""
        task = Task(name, args)
        self.pending_tasks.put(task)
        self._empty_active_queue()
        self._fill_active_queue()
        return task

    def _empty_active_queue(self):
        """
        Removes completed task from active queue and populates freed spots with tasks
        in the front of pending_tasks queue
        """
        # Remove completed tasks from active queue
        for index, task in enumerate(self.active_queue):
            self._update_task_status(task)
            if task.error:
                if task.retries < self.retry_limit:
                    self._logger.info("Retrying job {0}, previously raised error with error {1}".
                                      format(task.name, task.error))
                    task.retries += 1
                    task.error = None
                    self._trigger_task(task)
                else:
                    self._tasks_completed = self._tasks_completed + 1
                    task.is_complete = True
                    self.active_queue.pop(index)
                    raise TimeoutError("The task exceeded the retry limit: {0} [name: '{1}', id: {2}]".format(
                        task.error, task.name, task.id))

            if task.is_complete:
                self._tasks_completed = self._tasks_completed + 1
                self._logger.debug("Task is complete: ID {0}".format(task.id))
                self.active_queue.pop(index)

    @property
    def number_active(self):
        return len(self.active_queue)

    @property
    def number_pending(self):
        return self.pending_tasks.qsize()

    def _fill_active_queue(self):
        # Add add tasks to active queue if size of queue is less the max query limit
        for i in range(0, self.max_size - self.number_active):
            if not (self.pending_tasks.empty()):
                task = self.pending_tasks.get()
                self.active_queue.append(task)
                self._trigger_task(task)
            else:
                break

    @property
    def time_per_task(self):
        return (datetime.datetime.now() - self._time_first_job_added) / self._tasks_completed

    @property
    def time_remaining(self):
        if self._tasks_completed > 0:
            return self.time_per_task * (self.number_active + self.number_pending)
        else:
            return "Unknown"

    def wait_for_completion(self):
        """
        This method runs until execution of all tasks is completed
        """
        while len(self.active_queue):
            logging.info("{} tasks are awaiting exection".format(self.number_active))
            self._empty_active_queue()
            self._fill_active_queue()
            time.sleep(10)

        self._tasks_completed = 0
        self._time_first_job_added = datetime.datetime.now()

    def _trigger_task(self, task):  # pragma: nocover
        """
           This function should implement functionality to start task
           Once triggered is_active should be set to True
        """
        raise NotImplementedError("must be implemented by subclass")

    def _update_task_status(self, task):  # pragma: nocover
        """Updates task status and returns updated task object
           Also handles retries
        """
        raise NotImplementedError("must be implemented by subclass")

    def _empty_pending_queue(self):
        """
        Empty pending queue of tasks - prevent them from being run
        :return: None
        """
        while not self.pending_tasks.empty():
            self.pending_tasks.get()
