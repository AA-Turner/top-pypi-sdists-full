"""
CommandTemperature.py has the information required to get and set the
temperature state.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import time
from abc import abstractmethod
from enum import IntEnum
from sys import platform
from typing import Dict, List, Tuple, Union

from .check_windows_esc import _check_windows_esc
from .exceptions import MultiPyVuError, PythoncomImportError
from .ICommand import (ICommand, ICommandImp, ICommandObserverSim,
                       ISimulateChange)
from .IEventManager import IObserver
from .project_vars import CLOCK_TIME

if platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError:
        raise PythoncomImportError


class ApproachEnum(IntEnum):
    fast_settle = 0
    no_overshoot = 1


# Temperature state code dictionary
STATE_DICT = {
    1: "Stable",
    2: "Tracking",
    5: "Near",
    6: "Chasing",
    7: "Pot Operation",
    10: "Standby",
    13: "Diagnostic",
    14: "Impedance Control Error",
    15: "General Failure",
}

# The status codes MultiVu treats as "still moving."
#
# This mirrors IMultiVuPpmsServer::CheckStability(), which is what
# MultiVu's own WaitFor() uses.  Two things about it are worth knowing,
# because both differ from what this file used to do:
#
#   - It is a blacklist, not a whitelist.  Every code not listed here
#     counts as settled, including the error states (13 Diagnostic,
#     14 Impedance Control Error, 15 General Failure) and 10 Standby.
#     MultiVu does that on purpose; its comment reads "set to TRUE so
#     the task does not block on an unknown or error situation."
#     Waiting for "Stable" alone means a failed system never releases
#     the wait, and with the default timeout of 0 that is forever.
#   - It compares nothing against the set point.  MultiVu trusts the
#     status code by itself.
#
# Verified identical in all four MultiVu flavors in this working copy
# (Dynacool, OptiCool, SQUIDVsm, Versalab), so one list is correct for
# every flavor.  The PPMS is the one supported flavor whose MultiVu
# source is not in this working copy and so could not be checked.
#
# One thing to know about dropping the set point comparison:  it was
# also, accidentally, protecting against a race.  Right after a
# set_temperature() the controller may still be reporting the previous
# "Stable" while it takes up the new set point, and a status-only test
# would call that settled.  The old comparison could not be fooled that
# way, because the reading was still far from the new set point.
#
# Two things stand in its way instead of a tolerance:  the
# time.sleep(CLOCK_TIME) wait_for() does before its first check, and
# REQUIRED_SETTLED_POLLS in CommandWaitFor.py, which makes a settled
# reading repeat before it is believed.  See the comment on that
# constant -- it is the reachable stand-in for the busy-flag handshake
# MultiVu uses on the field in CMagnetBase::IsFieldStableForWait().
#
# Note this is a status-only test by design.  If a wait is ever seen
# ending early on real hardware, raise REQUIRED_SETTLED_POLLS rather
# than bringing back a set point tolerance:  the tolerances that used
# to live here were fitted to observed behavior, not to anything
# MultiVu actually does.
UNSTABLE_STATE_CODES = (
    0,      # unknown, which MultiVu treats as a transition state
    2,      # tracking
    5,      # near
    6,      # chasing
    7,      # pot fill
)


units = 'K'

############################
#
# Base Class
#
############################


class CommandTemperatureBase(ICommand):
    _set_point: float = 300.0
    _current_val: float = 300.0
    _state: int = 1
    _rate: float = 1.0
    _approach: ApproachEnum = ApproachEnum.fast_settle

    def __init__(self):
        super().__init__()
        self.approach_mode = ApproachEnum

        self.units = units

    @property
    def current_val(self):
        return CommandTemperatureBase._current_val

    @current_val.setter
    def current_val(self, new):
        CommandTemperatureBase._current_val = new

    @property
    def set_point(self):
        return CommandTemperatureBase._set_point

    @set_point.setter
    def set_point(self, new):
        CommandTemperatureBase._set_point = new

    @property
    def state(self):
        return CommandTemperatureBase._state

    @state.setter
    def state(self, new):
        CommandTemperatureBase._state = new

    @property
    def rate(self):
        return CommandTemperatureBase._rate

    @rate.setter
    def rate(self, new):
        CommandTemperatureBase._rate = new

    @property
    def approach(self) -> ApproachEnum:
        return CommandTemperatureBase._approach

    @approach.setter
    def approach(self, new):
        CommandTemperatureBase._approach = new

    def convert_result(self, response: Dict[str, str]) -> Tuple[float, str]:
        """
        Converts the CommandMultiVu response from get_state_server()
        to something usable for the user.

        Parameters:
        -----------
        response: Dict:
            Message.response['content']

        Returns:
        --------
        Value and error status returned from read/write
        """
        r = response['result'].split(',')
        if len(r) == 3:
            t, _, status = r
        elif len(r) == 1:
            t = '0.0'
            [status] = r
        else:
            msg = f'Invalid response: {response}'
            raise MultiPyVuError(msg)
        temperature = float(t)
        return temperature, status

    def prepare_query(self,
                      set_point: float,
                      rate_per_minute: float,
                      approach_mode: IntEnum) -> str:
        try:
            set_point = float(set_point)
        except ValueError:
            err_msg = 'set_point must be a float (set_point = '
            err_msg += "'{set_point}')"
            raise ValueError(err_msg)
        try:
            rate_per_minute = float(rate_per_minute)
            rate_per_minute = abs(rate_per_minute)
        except ValueError:
            err_msg = 'rate_per_minute must be a float '
            err_msg += f'(rate_per_minute = \'{rate_per_minute}\')'
            raise ValueError(err_msg)
        if (rate_per_minute < 0.01) or (rate_per_minute > 20):
            err_msg = f'Rate ({rate_per_minute} K/min) out of '
            err_msg += 'bounds.  Must be between 0.01 and 20 K/min'
            raise MultiPyVuError(err_msg)

        return f'{set_point},{rate_per_minute},{approach_mode.value}'

    def convert_state_dictionary(self, status_number) -> str:
        if isinstance(status_number, str):
            return status_number
        else:
            return STATE_DICT[status_number]

    def state_code_dict(self):
        return STATE_DICT

    @abstractmethod
    def get_state_server(self, value_variant, state_variant,  params=''):
        raise NotImplementedError

    @abstractmethod
    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: ApproachEnum
                       ) -> Union[str, int]:
        raise NotImplementedError

    def set_state_server(self, arg_string: str) -> Union[str, int]:
        if len(arg_string.split(',')) != 3:
            err_msg = 'Setting the temperature requires three numeric inputs, '
            err_msg += 'separated by a comma: '
            err_msg += 'Set Point (K), '
            err_msg += 'rate (K/min), '
            err_msg += 'approach:'
            for mode in self.approach_mode:
                err_msg += f'\n\t{mode.value}: approach_mode.{mode.name}'
            return err_msg
        temperature, rate, approach = arg_string.split(',')
        temperature = float(temperature)
        if temperature < 0:
            err_msg = "Temperature must be a positive number."
            return err_msg
        set_rate_per_min = float(rate)
        set_approach_number = int(approach)
        if set_approach_number > len(self.approach_mode) - 1:
            err_msg = f'The approach, {set_approach_number}, is out of bounds.  Must be '
            err_msg += 'one of the following'
            for mode in self.approach_mode:
                err_msg += f'\n\t{mode.value}: approach_mode.{mode.name}'
            return err_msg

        # Hand on the enum member, the way CommandField does, so
        # that the approach mode does not travel as a bare int.
        set_approach = ApproachEnum(set_approach_number)

        err = self._set_state_imp(temperature,
                                  set_rate_per_min,
                                  set_approach)
        return err


############################
#
# Standard Implementation
#
############################


class CommandTemperatureImp(ICommandImp, CommandTemperatureBase):
    def __init__(self, multivu_win32com, instrument_name):
        """
        Parameters:
        ----------
        multivu_win32com: win32.dynamic.CDispatch
        instrument_name: str
        """
        super().__init__()
        self._mvu = multivu_win32com
        self.instrument_name = instrument_name

    def get_state_server(self,
                         value_variant,
                         state_variant,
                         params='') -> Tuple[float, int]:
        """
        Retrieves information from MultiVu

        Parameters:
        -----------
        value_variant: VARIANT: set up by pywin32com for getting the value
        state_variant: VARIANT: set up by pywin32com for getting the state
        params: str (optional)
            optional parameters that may be required to query MultiVu

        Returns:
        --------
        Tuple(float, int)
            The value and state number
        """
        can_error = self._mvu.GetTemperature(value_variant, state_variant)
        # On 6/10/25, I found that the PPMS was returning something greater
        # than 1 with this command.  After talking with Mark, I have decided
        # to only check for a value greater than 1 for all systems.
        if can_error > 1:
            raise MultiPyVuError('Error when calling GetTemperature()')
        self.current_val = value_variant.value
        self.state = int(state_variant.value)

        return self.current_val, self.state

    def _read_set_point(self) -> float:
        """
        The temperature set point MultiVu currently reports.

        Used by ._confirm_set_point() to tell a set point MultiVu has
        adopted from one it has not.  The import is local because
        CommandTempSetPoints imports this module, so a top-level import
        would be circular.
        """
        from .CommandTempSetPoints import CommandTempSetpointsImp
        t_set = CommandTempSetpointsImp(self.instrument_name, self._mvu)
        (reported, _, _), _ = t_set.get_state_server(
            win32.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0),
            win32.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0),
            )
        return reported

    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: ApproachEnum
                       ) -> Union[str, int]:
        can_error = self._mvu.SetTemperature(temperature,
                                             set_rate_per_min,
                                             set_approach,
                                             )
        self.set_point = temperature
        self.rate = set_rate_per_min
        self.approach = set_approach

        if can_error <= 1:
            self._confirm_set_point(temperature,
                                    self._read_set_point,
                                    'temperature',
                                    ' K',
                                    )

        if self.instrument_name in ('PPMS', 'MPMS3'):
            if can_error > 1:
                raise MultiPyVuError('Error when calling SetTemperature()')
            else:
                # returning this string makes CommandMultiVu_base happy
                return 'Call was successful'
        elif can_error > 1:
            raise MultiPyVuError('Error when calling SetTemperature()')
        return can_error

    def test(self) -> bool:
        """
        Report whether the temperature has stopped moving.

        This asks the same question MultiVu's own WaitFor() asks, in the
        same way:  the status code alone decides, and every code outside
        UNSTABLE_STATE_CODES counts as settled.  See the comment on that
        constant for why it is a blacklist and why no set point
        comparison happens here.

        Returns:
        --------
        bool
        """
        self._get_values()
        return int(self.state) not in UNSTABLE_STATE_CODES


############################
#
# Scaffolding Implementation
#
############################

class SimulateTemperatureChange(ISimulateChange):
    # These are class variables, not instance variables, so that the
    # simulated instrument keeps its condition from one change
    # thread to the next.  See ISimulateChange for the reasoning.
    _stop_flag: bool = False
    _state_dict = STATE_DICT
    # The starting values come from the Command*Base class so that
    # the scaffolding and the real implementation begin in the
    # same place.
    _current_val: float = CommandTemperatureBase._current_val
    _state: int = CommandTemperatureBase._state
    _set_point: float = CommandTemperatureBase._set_point
    _rate: float = CommandTemperatureBase._rate
    _approach: ApproachEnum = ApproachEnum.fast_settle
    _observers: List[IObserver] = []

    def __init__(self):
        super().__init__('SimulateTemperatureChange')

    @property
    def current_val(self):
        return SimulateTemperatureChange._current_val

    @current_val.setter
    def current_val(self, new):
        SimulateTemperatureChange._current_val = new

    @property
    def set_point(self):
        return SimulateTemperatureChange._set_point

    @set_point.setter
    def set_point(self, new):
        SimulateTemperatureChange._set_point = new

    @property
    def rate(self):
        return SimulateTemperatureChange._rate

    @rate.setter
    def rate(self, new):
        SimulateTemperatureChange._rate = new

    @property
    def approach(self):
        return SimulateTemperatureChange._approach

    @approach.setter
    def approach(self, new):
        SimulateTemperatureChange._approach = new

    def stop_requested(self):
        return SimulateTemperatureChange._stop_flag

    def stop_thread(self, set_stop=True):
        SimulateTemperatureChange._stop_flag = set_stop

    def check_esc(self):
        try:
            _check_windows_esc()
        except KeyboardInterrupt:
            self.stop_thread()

    def _monitor(self):
        """
        This private method is used to simulate the temperature change.
        """
        starting_temp = self.current_val
        self.state = 1
        self.notify_observers(self.current_val, self.state)

        # simulate a pause before changing the temperature
        start_time = time.time()
        while time.time() - start_time < 1:
            time.sleep(CLOCK_TIME)

            # check if the main thread has killed this process
            if self.stop_requested():
                return
            # check the escape key
            self.check_esc()

        # set up the ramp
        delta_temp = self.set_point - starting_temp
        rate_per_sec = self.rate / 60
        rate_per_sec *= -1 if delta_temp < 0 else 1
        rate_time = delta_temp / rate_per_sec
        ramp_start_time = time.time()
        self.state = 2
        self.notify_observers(self.current_val, self.state)

        # simulate the ramp
        while (time.time() - ramp_start_time) < rate_time:
            if self.stop_requested():
                return
            time.sleep(CLOCK_TIME)
            self.acquire_mutex()
            self.current_val += CLOCK_TIME * rate_per_sec
            # The ramp points are discrete, so they can
            # pass over the set point.  This check ensures
            # that there is no overshoot.
            if rate_per_sec > 0:
                self.current_val = min(self.current_val,
                                       self.set_point)
            else:
                self.current_val = max(self.current_val,
                                       self.set_point)
            self.release_mutex()
            self.notify_observers(self.current_val, self.state)

            # check the escape key
            self.check_esc()

        # set the final values
        self.current_val = self.set_point
        self.state = 5
        self.notify_observers(self.current_val, self.state)
        stable_start_time = time.time()
        # simulate coming to stability
        while time.time() - stable_start_time < 5.0:
            time.sleep(CLOCK_TIME)
            if self.stop_requested():
                return
            # check the escape key
            self.check_esc()

        self.state = 1
        self.notify_observers(self.current_val, self.state)

        # unsubscribe from all observers before exiting
        for o in self._observers:
            self.unsubscribe(o)
        return


class CommandTemperatureSim(CommandTemperatureBase,
                            ICommandObserverSim,
                            ):

    def __init__(self):
        CommandTemperatureBase.__init__(self)
        ICommandObserverSim.__init__(self,
                                     SimulateTemperatureChange,
                                     )

    def get_state_server(self,
                         value_variant,
                         state_variant,
                         params='') -> Tuple[float, int]:
        return self.current_val, self.state

    def _set_state_imp(self,
                       temperature: float,
                       set_rate_per_min: float,
                       set_approach: ApproachEnum
                       ) -> Union[str, int]:
        # Get an instance of SimulateTemperatureChange.
        self.change_thread: SimulateTemperatureChange = self.get_sim_instance()
        self.change_thread.set_params(self.current_val,
                                      temperature,
                                      set_rate_per_min,
                                      self.state,
                                      )
        self.set_point = temperature
        self.rate = set_rate_per_min
        self.approach = set_approach
        self.change_thread.approach = set_approach

        self.change_thread.subscribe(self)
        self.change_thread.start()
        error = 0
        return error

    def update(self, value, state):
        self.current_val = value
        self.state = state
