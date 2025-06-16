"""
Utility Dettails class
"""

import os
import sys
import json
from .frog_params import Params


class UtilityDetails:
    """
    Class to hold details of a utility - for ease of use in Details() functions
    """

    def __init__(self) -> None:
        self.description = "This utility has not been given a description"
        self.params: Params = Params()

        # Currently applicable to system utilities only
        self.category: str = ""
        self.host: str = None
        self.machine_size: str = None

    def to_json(self) -> str:
        # Name is taken automatically from the name of the utility script being run
        if hasattr(sys.modules["__main__"], "__file__"):
            name = os.path.splitext(os.path.basename(sys.modules["__main__"].__file__))[0]
        else:
            name = "Utility name error"

        result = {
            "Name": name,
            "Category": self.category,
            "Description": self.description,
            "Params": self.params.result(),
        }

        if self.host is not None:
            result["Host"] = self.host
            if self.machine_size is not None:
                result["Machine"] = self.machine_size
            else:
                self.machine_size = "3XS"

        return json.dumps(result)
