import logging
import time
import requests

from .scheduler import ThreadedScheduler, method


# from .utils import load_class_from_name


# import basemodule


class TaskManager(object):
    """
    Class
    """

    def __init__(self, enable, reload_interval, instance_details):
        self.log = logging.getLogger('spotmax-agent')
        self.log.setLevel(logging.DEBUG)
        self.enable = enable
        self.reload_interval = reload_interval
        self.scheduler = ThreadedScheduler()
        self.running = True
        self.tasks = {}
        self.instance_details = instance_details

    def start(self):
        # modules_folder = '/etc/spotmax/agent/modules'
        self.log.debug("service is %s" % self.enable)

        # Search for modules in folder
        # modules = self.load_modules(modules_folder)

        # Setup Modules
        # for module in modules.values():
        # Initialize Module
        # c = self.init_module(module['cls'])
        # Schedule Module
        # self.schedule_module(c, module)

        if self.reload_interval < 0:
            should_reload = False
        else:
            should_reload = True

        # Start mainloop
        self.mainloop(should_reload)

    def mainloop(self, should_reload=True):

        # Start scheduler
        self.scheduler.start()

        # Log
        self.log.info('Started task scheduler.')

        # Initialize reload timer
        time_since_reload = 0

        self.schedule_module()

        self.log.info('Starting Main loop.')
        # Main Loop
        while self.running:
            time.sleep(1)
            time_since_reload += 1

            # Check if its time to reload modules
            if should_reload and time_since_reload > self.reload_interval:
                # Log
                self.log.debug("Reloading all 'unknown' modules.")

                # Search for modules in folder
                # modules_folder = '/etc/spotinst/agent/modules'
                # modules = self.load_modules(modules_folder)

                # Setup Modules
                # for module in modules.values():
                # Initialize Module
                # c = self.init_module(module['cls'])
                # Schedule Module
                # self.schedule_module(c, module)

                # Reset reload timer
                time_since_reload = 0

        # Log
        self.log.debug('Stopping task scheduler.')
        # Stop scheduler
        self.scheduler.stop()
        # Log
        self.log.info('Stopped task scheduler.')
        # Log
        self.log.debug("Exiting.")

    def schedule_module(self):
        def ping(arg):
            # print(">>>TASK", arg, "sleeping 3 seconds")
            # time.sleep(3)
            # print("<<<END_TASK", arg)
            res = requests.get('https://api.spotmaxtech.com/health/ready', auth=('user', 'pass'))
            self.log.debug("ping: %s" % res.json())

        self.log.info("Scheduled task {0} to run every {1}s (delayed of {2}s)".format("ping", 10, 3))
        task = self.scheduler.add_interval_task(ping, "ping", 3, 10, method.sequential, ["spotmax api"], None, True)

        self.log.debug("Scheduled task: %s" % "ping")
        # Add task to list
        self.tasks["ping"] = {'task': task}

    def stop(self):
        """
        Close and stop all tasks.
        """
        # Set Running Flag
        self.running = False

        self.log.info('Stopped task scheduler.')

        for key, task in self.tasks.iteritems():
            try:
                self.scheduler.cancel(task['task'])
                # Log
                self.log.info("Canceled task: %s" % key)
            except ValueError as e:
                self.log.error("Cancel task exception '{0}' - {1}".format(key, e))


def isModule(given_class):
    try:
        return given_class.isModule
    except (AttributeError, TypeError) as e:
        return False


if __name__ == "__main__":
    logging.basicConfig()
    r = TaskManager(True, 20, "instance_details")
    r.start()
