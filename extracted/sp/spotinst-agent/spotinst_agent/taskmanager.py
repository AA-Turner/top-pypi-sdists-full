import inspect
import logging
import os
import sys
import time
import traceback

from scheduler import ThreadedScheduler, method
from utils import load_class_from_name
import basemodule


class TaskManager(object):
    """
    Class
    """

    def __init__(self, enable, reload_interval, instance_details):
        self.log = logging.getLogger('spotinst-agent')
        self.enable = enable
        self.reload_interval = reload_interval
        self.scheduler = ThreadedScheduler()
        self.running = True
        self.tasks = {}
        self.instance_details = instance_details

    def start(self):
        time.sleep(5)
        initiators_folder = '/etc/spotinst/agent/initiators/modules'

        # Search for initiators in folder
        initiators = self.load_modules(initiators_folder)

        # Setup Modules
        for initiator in initiators.values():
            c = self.init_module(initiator['cls'])
            self.schedule_initiator_module(c, initiator)

        modules_folder = '/etc/spotinst/agent/modules'
        self.log.debug("service is %s" % self.enable)

        # Search for modules in folder
        modules = self.load_modules(modules_folder)

        # Setup Modules
        for module in modules.values():
            # Initialize Module
            c = self.init_module(module['cls'])
            # Schedule Module
            self.schedule_module(c, module)

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
                modules_folder = '/etc/spotinst/agent/modules'
                modules = self.load_modules(modules_folder)

                # Setup Modules
                for module in modules.values():
                    # Initialize Module
                    c = self.init_module(module['cls'])
                    # Schedule Module
                    self.schedule_module(c, module)

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

    def load_modules(self, path, filter=None):
        """
        Scan for modules to load from path
        """
        # Initialize return value
        modules = {}

        # Get a list of files in the directory, if the directory exists
        if not os.path.exists(path):
            raise OSError("Directory does not exist: %s" % path)

        # Log
        self.log.info("Loading Modules from: %s" % path)

        # Add path to the system path
        sys.path.append(path)
        # Load all the files in path
        for f in os.listdir(path):
            # Ignore anything that isn't a .py file
            if len(f) > 3 and f[-3:] == '.py':

                # Check filter
                if filter and os.path.join(path, f) != filter:
                    continue

                modname = f[:-3]
                mod_modification_time = os.path.getmtime(os.path.join(path, f))
                mod_modification_time_str = str(mod_modification_time)
                self.log.info("Py file found: %s" % modname)

                modules_list = [x.lower() for x in self.tasks.keys()]
                if modname in modules_list:
                    if self.tasks[modname]['modification_time'] == mod_modification_time_str:
                        self.log.info("Module '{0}' already loaded".format(modname))
                        continue

                if modname == "utils" or modname == "basemodule":
                    continue

                # import module only if it exists for more than 1 second (had enough time to write the entire content)
                now = time.time()
                if now - mod_modification_time < 1:
                    self.log.info("Not loading file since it was created too recently: modified at %s, now is %s" % (mod_modification_time, now))
                    continue

                try:
                    # Import the module
                    self.log.info("Importing %s" % modname)
                    mod = __import__(modname, globals(), locals(), ['*'])
                except Exception as e:
                    # Log error
                    self.log.error("Failed to import module: %s. %s" % (modname, traceback.format_exc()))
                    continue

                # Find all classes defined in the module
                self.log.info("Finding classes defined in module " + str(modname))
                for attrname in dir(mod):
                    attr = getattr(mod, attrname)
                    # Only attempt to load classes that are infact classes but not the base Module class
                    self.log.debug("Checking " + str(modname) + " Attribute " + str(attrname))

                    if inspect.isclass(attr) and isModule(attr) and attr != basemodule.Module:
                        # Get class name
                        fqcn = '.'.join([modname, attrname])
                        self.log.info("Module loaded : " + fqcn)
                        try:
                            # Load Module class
                            cls = load_class_from_name(fqcn)
                            # Add Module class
                            modules[cls.__name__] = {'cls': cls, 'file_name': modname, 'modification_time': mod_modification_time_str}
                        except Exception as e:
                            # Log error
                            self.log.error("Failed to load Module: %s. %s" % (e, traceback.format_exc()))
                            continue

        # Return Module classes
        self.log.info("Finished Loading Modules from: " + path + " . Found " + str(len(modules)) + " modules.")
        return modules

    def init_module(self, cls):
        """
        Initialize module
        """
        module = None
        try:
            # Initialize Module
            module = cls(**self.instance_details)
            # Log
            self.log.info("Initialized Module: %s" % cls.__name__)
        except Exception:
            # Log error
            self.log.error("Failed to initialize Module: %s. %s" % (cls.__name__, traceback.format_exc()))

        # Return module
        return module

    def schedule_module(self, c, module):
        """
        Schedule module
        """
        # Check module is for real

        if c is None:
            self.log.warning("Skipped loading invalid Module: %s" % c.__class__.__name__)
            return

        if not c.get_enable():
            self.log.info("Skipped loading Module '%s' since it is disabled" % c.__class__.__name__)
            return

        # Get Module schedule
        for name, schedule in c.get_schedule().items():
            # Get scheduler args
            func, args, splay, interval = schedule

            # Check if a module with same name has already been scheduled
            if module['file_name'] in self.tasks:
                try:
                    self.scheduler.cancel(self.tasks[module['file_name']]['task'])
                    # Log
                    self.log.info("Canceled task: %s" % name)
                except ValueError as e:
                    self.log.error("Unable to cancel task '{0}' - {1}".format(self.tasks[name], e))

            # Schedule Collector
            self.log.info("Scheduled task {0} to run every {1}s (delayed of {2}s)".format(name, interval, splay))
            task = self.scheduler.add_interval_task(func, name, splay, interval, method.sequential,
                                                    args, None, True)

            self.log.debug("Scheduled task: %s" % name)
            # Add task to list
            self.tasks[module['file_name']] = {'task': task, 'modification_time': module['modification_time']}

    def schedule_initiator_module(self, c, module):
        """
        Schedule module
        """
        if c is None:
            self.log.warning("Skipped loading invalid Module: %s" % c.__class__.__name__)
            return

        if not c.get_enable():
            self.log.info("Skipped loading Module '%s' since it is disabled" % c.__class__.__name__)
            return

        # Get Module schedule
        for name, schedule in c.get_schedule().items():
            # Get scheduler args
            func, args, splay, interval = schedule

            # Check if a module with same name has already been scheduled
            if module['file_name'] in self.tasks:
                try:
                    self.scheduler.cancel(self.tasks[module['file_name']]['task'])
                    # Log
                    self.log.info("Canceled task: %s" % name)
                except ValueError as e:
                    self.log.error("Unable to cancel task '{0}' - {1}".format(self.tasks[name], e))

            # Schedule Collector
            self.log.info("Scheduled task {0} to run once. (delay of {1})".format(name, splay))
            task = self.scheduler.add_single_task(func, name, splay, method.sequential,
                                                  args, None)

            self.log.debug("Scheduled task: %s" % name)
            # Add task to list
            self.tasks[module['file_name']] = {'task': task, 'modification_time': module['modification_time']}

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
