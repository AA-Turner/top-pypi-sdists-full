import multiprocessing
import time


class Scheduler:
    def __init__(self, function, interval):
        self.function = function
        self.interval = interval
        self.process = multiprocessing.Process(target=self.run, daemon=True)
        self.stop_event = multiprocessing.Event()

    def run(self):
        """
        The method to be run in a separate process; calls the function at the specified interval.
        """
        next_run_time = time.time() + self.interval
        while not self.stop_event.is_set():
            current_time = time.time()
            if current_time >= next_run_time:
                self.function()
                next_run_time = current_time + self.interval
            time.sleep(0.1)

    def start(self):
        """
        Starts the scheduler by initiating the process.
        """
        self.process.start()

    def stop(self):
        """
        Stops the scheduler by setting the stop event.
        """
        self.stop_event.set()
        self.process.join()


class SchedulerManager:
    def __init__(self):
        self.schedulers = []
        self.is_running = False
        self.is_running_lock = multiprocessing.Lock()

    def add_job(self, function, interval):
        """
        Creates a Scheduler and adds it to the list of managed schedulers.

        :param function: The function to be scheduled.
        :param interval: The scheduling interval in seconds.
        """
        scheduler = Scheduler(function, interval)
        self.schedulers.append(scheduler)
        with self.is_running_lock:
            if self.is_running:
                scheduler.start()

    def start(self):
        """
        Starts all schedulers in the list.
        """
        for scheduler in self.schedulers:
            scheduler.start()
        with self.is_running_lock:
            self.is_running = True

    def shutdown(self):
        """
        Stops all schedulers in the list.
        """
        for scheduler in self.schedulers:
            scheduler.stop()
        with self.is_running_lock:
            self.is_running = False

    def running(self):
        """
        Returns True if any of the schedulers are running.
        """
        with self.is_running_lock:
            return self.is_running
