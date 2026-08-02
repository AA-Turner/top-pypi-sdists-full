import logging
from abc import ABCMeta, abstractmethod

from python_agent.packages.six import add_metaclass

log = logging.getLogger(__name__)


@add_metaclass(ABCMeta)
class FootprintsCollector(object):
    @abstractmethod
    def get_footprints_and_clear(self, test_coverage):
        raise NotImplementedError("Please Implement this method")
