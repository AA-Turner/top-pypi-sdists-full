from builtins import object
import logging
import traceback


class Module(object):
    isModule = True
    """
    This Module class is a base class for all modules.
    """

    def __init__(self, *args):
        """
        Create a new worker
        """
        # Initialize Logger
        self.log = logging.getLogger('spotinst-agent')

    def _run(self):
        """
        Run the collector
        """
        # Log
        self.log.info("%s in running..." % self.__class__.__name__)
        try:
            self.run()
        except Exception:
            # Log Error
            self.log.error(traceback.format_exc())

    def get_schedule(self):
        """
        Return schedule for the worker
        """
        # Return a dict of tuples containing (collector function, collector function args, splay, interval)
        return {self.__class__.__name__: (self._run, None, self.load_splay(), self.load_interval())}

    def get_enable(self):
        """
        Return if the worker is enabled or disabled
        :return:
        """
        return False

    def load_splay(self):
        pass

    def load_interval(self):
        pass
