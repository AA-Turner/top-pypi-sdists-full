"""Start OSO Energy Session."""

import sys
import traceback
from os.path import expanduser
from typing import Optional

from aiohttp import ClientSession
from loguru import logger
from apyosoenergyapi.sensor import Sensor
from apyosoenergyapi.binary_sensor import BinarySensor
from apyosoenergyapi.switch import Switch

from .session import OSOEnergySession
from .waterheater import WaterHeater
from .device_attributes import OSOEnergyAttributes

debug = []
home = expanduser("~")
logger.add(
    home + "/pyosoenergyapi_debug.log", filter=lambda record: record["level"].name == "DEBUG"
)
logger.add(
    home + "/pyosoenergyapi_info.log", filter=lambda record: record["level"].name == "INFO"
)
logger.add(
    home + "/pyosoenergyapi_error.log", filter=lambda record: record["level"].name == "ERROR"
)


def exception_handler(exctype, value, tb):
    # pylint: disable=unused-argument
    # pylint: disable=invalid-name
    """Handle custom exceptions.

    Args:
        exctype ([type]): [description]
        value ([type]): [description]
        tb ([type]): [description]
    """
    last = len(traceback.extract_tb(tb)) - 1
    logger.error(
        f"-> \n"
        f"Error in {traceback.extract_tb(tb)[last].filename}\n"
        f"when running {traceback.extract_tb(tb)[last].name} function\n"
        f"on line {traceback.extract_tb(tb)[last].lineno} - "
        f"{traceback.extract_tb(tb)[last].line} \n"
        f"with vars {traceback.extract_tb(tb)[last].locals}"
    )
    traceback.print_exc(tb)


sys.excepthook = exception_handler


def trace_debug(frame, event, arg):
    """Trace functions.

    Args:
        frame (object): The current frame being debugged.
        event (str): The event type
        arg (dict): arguments in debug function..
    Returns:
        object: returns itself as per tracing docs
    """
    if "pyosoenergyapi/" in str(frame):
        code = frame.f_code
        func_name = code.co_name
        func_line_no = frame.f_lineno
        if func_name in debug:
            if event == "call":
                func_filename = code.co_filename.rsplit("/", 1)
                caller = frame.f_back
                caller_line_no = caller.f_lineno
                caller_filename = caller.f_code.co_filename.rsplit("/", 1)

                logger.debug(
                    f"Call to {func_name} on line {func_line_no} "
                    f"of {func_filename[1]} from line {caller_line_no} "
                    f"of {caller_filename[1]}"
                )
            elif event == "return":
                logger.debug(f"returning {arg}")

        return trace_debug

    return None


class OSOEnergy(OSOEnergySession):
    """OSO Energy class.

    Args:
        OSOEnergySession (object): Interact with OSO Energy
    """

    def __init__(
            self,
            subscription_key,
            websession: Optional[ClientSession] = None):
        """Initialize OSO Energy."""
        super().__init__(subscription_key=subscription_key, websession=websession)
        self.session = self
        self.attr = OSOEnergyAttributes(self.session)
        self.hotwater = WaterHeater(self.session)
        self.sensor = Sensor(self.session)
        self.binary_sensor = BinarySensor(self.session)
        self.switch = Switch(self.session)
        self.logger = logger
        if debug:
            sys.settrace(trace_debug)

    def setDebugging(self, debugger: list):
        # pylint: disable=no-self-use
        # pylint: disable=global-statement
        # pylint: disable=invalid-name
        """Set function to debug.

        Args:
            debugger (list): a list of functions to debug

        Returns:
            object: Returns traceback object.
        """
        global debug
        debug = debugger
        if debug:
            return sys.settrace(trace_debug)
        return sys.settrace(None)
