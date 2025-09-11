from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional
from orionis.foundation.config.testing.enums import ExecutionMode
from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.foundation.config.testing.enums.verbosity import VerbosityMode

class IUnitTest(ABC):

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute all discovered tests.

        Returns
        -------
        dict
            Results of the test execution.
        """
        pass