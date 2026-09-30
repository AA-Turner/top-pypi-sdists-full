# -*- coding: utf-8 -*-
"""
CommandVectorMagnet.py has the information required to
get and set the vector field for the OptiCool using cartesian
coordinates.

@author: djackson
"""

import math
import re
import time
from abc import abstractmethod
from enum import IntEnum
from sys import platform
from typing import cast, Dict, List, Tuple, Union

import numpy as np

from .check_windows_esc import _check_windows_esc
from .exceptions import MultiPyVuError, PythoncomImportError
from .ICommand import (ICommand, ICommandImp, ICommandObserverSim,
                       ISimulateChange, floats_equal)
from .IEventManager import IObserver
from .project_vars import CLOCK_TIME

if platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError:
        raise PythoncomImportError


class ApproachEnum(IntEnum):
    linear = 0
    no_overshoot = 1
    oscillate = 2


# Field state code dictionary
STATE_DICT = {
    0: 'Unknown',
    1: 'Stable',
    2: 'Switch Warming',
    3: 'Switch Cooling',
    4: 'Holding (driven)',
    5: 'Iterate',
    6: 'Ramping',
    7: 'Ramping',
    8: 'Resetting',
    9: 'Current Error',
    10: 'Switch Error',
    11: 'Quenching',
    12: 'Charging Error',
    14: 'PSU Error',
    15: 'General Failure',
}


units = 'Oe'


############################
#
# Base Class
#
############################


class CommandVectorBase(ICommand):
    # class variables
    _set_point: tuple = (0.0, 0.0, 0.0)
    _current_val: tuple = (0.0, 0.0, 0.0)
    _rate: float = 1
    _state: int = 1
    _approach: ApproachEnum = ApproachEnum.no_overshoot

    def __init__(self, instrument_name: str, cart_coord: bool = True):
        super().__init__()
        self.instrument_name = instrument_name
        self.cart_coord = cart_coord

        self.units = units

    def cartesian_to_spherical(self, x, y, z) -> Tuple[float, float, float]:
        """
        Convert Cartesian coordinates to spherical coordinates (degrees).
        Returns (r, theta, phi):
        - r: radius
        - theta: polar angle in degrees (0 <= theta <= 180)
        - phi: azimuthal angle in degrees (-180 < phi <= 180)
        """
        r = math.sqrt(x**2 + y**2 + z**2)
        theta = math.acos(z / r) if r != 0 else 0.0
        theta_deg = math.degrees(theta)
        phi = math.atan2(y, x)
        phi_deg = math.degrees(phi)
        # Ensure phi is in [-180, 180]
        if phi_deg > 180:
            phi_deg -= 360
        elif phi_deg <= -180:
            phi_deg += 360
        return r, theta_deg, phi_deg

    def spherical_degrees_to_cartesian(self, r, theta_deg, phi_deg) -> Tuple[float, float, float]:
        """
        Convert spherical coordinates (degrees) to Cartesian coordinates.
        - r: radius
        - theta_deg: polar angle in degrees (0 <= theta <= 180)
        - phi_deg: azimuthal angle in degrees (-180 < phi <= 180)
        Returns (x, y, z)
        """
        theta = math.radians(theta_deg)
        phi = math.radians(phi_deg)
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        return x, y, z

    @property
    def current_val(self):
        return CommandVectorBase._current_val

    @current_val.setter
    def current_val(self, new):
        CommandVectorBase._current_val = new

    @property
    def set_point(self):
        return CommandVectorBase._set_point

    @set_point.setter
    def set_point(self, new):
        CommandVectorBase._set_point = new

    @property
    def rate(self):
        return CommandVectorBase._rate

    @rate.setter
    def rate(self, new):
        CommandVectorBase._rate = new

    @property
    def state(self):
        return CommandVectorBase._state

    @state.setter
    def state(self, new):
        CommandVectorBase._state = new

    @property
    def approach_mode(self):
        return CommandVectorBase._approach

    @approach_mode.setter
    def approach_mode(self, new):
        CommandVectorBase._approach = new

    def convert_result(self, response: Dict[str, str]) -> Tuple[Tuple[float, float, float],
                                                                str]:
        """
        Converts the CommandMultiVu response from get_state()
        to something usable for the user.

        Parameters:
        -----------
        response: Dict:
            Message.response['content']

        Returns:
        --------
        Tuple of the set point and error status returned from read/write
        """
        num = r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
        search_str = rf'\(({num}),[ ]?({num}),[ ]?({num})\),[ ]?([a-zA-Z]*),[ ]?([ \(\)a-zA-Z]*)'
        r = re.findall(search_str, response['result'])
        if len(r[0]) != 5:
            msg = f'Invalid response: {response}'
            raise MultiPyVuError(msg)
        h_x, h_y, h_z, units, status = r[0]
        field_x = float(h_x)
        field_y = float(h_y)
        field_z = float(h_z)
        return (field_x, field_y, field_z), status

    def prepare_query(self, *args) -> str:
        """
        Makes the correct query given the inputs

        Arguments:
            (h_a, h_b, h_c) -- field
            rate_per_sec -- ramp rate
            approach -- ApproachEnum

        Raises:
            ValueError: incorrect input types

        Returns:
            A string of the form,
                'h_x, h_y, h_z,rate_per_sed,ApproachEnum.value'
        """
        if len(args) != 3:
            err_msg = "Expected 3 arguments: a 3-element tuple "
            err_msg += "for the field, rate_per_sec, approach"
            raise ValueError(err_msg)
        h_x: float
        h_y: float
        h_z: float
        rate_per_sec: float
        approach: ApproachEnum
        (h_x, h_y, h_z), rate_per_sec, approach = args
        try:
            h_x = float(h_x)
            h_y = float(h_y)
            h_z = float(h_z)
        except ValueError as e:
            set_point = (h_x, h_y, h_z)
            err_msg = "The set points must be floats "
            err_msg += f"(set_point = '{set_point}')"
            raise ValueError(err_msg) from e

        try:
            rate_per_sec = float(rate_per_sec)
            rate_per_sec = abs(rate_per_sec)
        except ValueError as e:
            err_msg = 'rate_per_sec must be a float '
            err_msg += f'(rate_per_sec = \'{rate_per_sec}\')'
            raise ValueError(err_msg) from e

        try:
            approach_mode = approach.value
        except AttributeError:
            err_msg = 'Invalid approach mode type (must be '
            err_msg += ' client.magnet.approach_mode)'
            raise ValueError(err_msg)

        return f'{h_x},{h_y},{h_z},{rate_per_sec},{approach_mode}'

    def convert_state_dictionary(self, status_number):
        if isinstance(status_number, str):
            return status_number
        else:
            return STATE_DICT.get(status_number, status_number)

    @abstractmethod
    def _get_state_imp(self,
                       value_x_variant,
                       state_variant,
                       params='') -> Tuple[Tuple[float], int]:
        raise NotImplementedError

    def get_state_server(self,
                         value_variant,
                         state_variant,
                         params='') -> Tuple:
        # Check this is being used on an OptiCool
        if self.instrument_name != 'OPTICOOL':
            err_msg = 'The vector magnet only works with OptiCool'
            raise MultiPyVuError(err_msg)
        value_x_variant = value_variant
        return self._get_state_imp(value_x_variant,
                                   state_variant,
                                   params)

    @abstractmethod
    def _set_state_imp(self,
                       field: Tuple[float, float, float],
                       set_rate_per_sec: float,
                       set_approach: ApproachEnum,
                       ) -> Union[str, int]:
        raise NotImplementedError

    def set_state_server(self, arg_string) -> Union[str, int]:
        # Check this is being used on a valid instrument
        if self.instrument_name != 'OPTICOOL':
            err_msg = 'The vector magnet only works with OptiCool'
            raise MultiPyVuError(err_msg)

        num = r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
        search_str = rf'({num}),[ ]?({num}),[ ]?({num}),[ ]?({num}),[ ]?([0-9])'
        commands = re.findall(search_str, arg_string)
        if len(commands[0]) != 5:
            error_msg = f'Bad query: "{search_str}"'
            error_msg += 'Should be of the format '
            error_msg += '(h_a, h_b, h_c),rate,approach'
            raise ValueError(error_msg)
        h_a, h_b, h_c, rate, approach = commands[0]
        # If these conversions fail, it will throw a ValueError
        h_a = float(h_a)
        h_b = float(h_b)
        h_c = float(h_c)
        field = (h_a, h_b, h_c)
        set_rate_per_sec = float(rate)
        set_approach_number = int(approach)
        if set_approach_number > len(ApproachEnum) - 1:
            err_msg = f'The approach, {set_approach_number}, is out of bounds.  '
            err_msg += 'Must be one of the following:'
            for mode in ApproachEnum:
                print(f'\n\t{mode.value}: {mode.name}')
            raise MultiPyVuError(err_msg)
        set_approach = ApproachEnum(set_approach_number)

        error = self._set_state_imp(field,
                                    set_rate_per_sec,
                                    set_approach,
                                    )
        return error

    def state_code_dict(self):
        return STATE_DICT


############################
#
# Standard Implementation
#
############################


class CommandVectorImp(ICommandImp, CommandVectorBase):
    def __init__(self,
                 multivu_win32com,
                 instrument_name: str,
                 cartesian_coord: bool = True):
        """
        Parameters:
        ----------
        multivu_win32com: win32.dynamic.CDispatch
        instrument_name: str
        """
        CommandVectorBase.__init__(self, instrument_name, cartesian_coord)
        self._mvu = multivu_win32com

    def _get_state_imp(self,
                       value_x_variant,
                       state_variant,
                       params='') -> Tuple:
        """
        Retrieves information from MultiVu

        Parameters:
        -----------
        value_x_variant: VARIANT: set up by pywin32com for getting the value
        state_variant: VARIANT: set up by pywin32com for getting the state
        params: str (optional)
            optional parameters that may be required to query MultiVu

        Returns:
        --------
        Tuple(Tuple[float], int)
            The value and state number
        """
        # Setting up a by-reference (VT_BYREF) double (VT_R8)
        # variant.  This is used to get the value.
        value_y_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0))
        # Setting up a by-reference (VT_BYREF) double (VT_R8)
        # variant.  This is used to get the value.
        value_z_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0))
        if self.cart_coord:
            can_error = self._mvu.GetFieldCartesian(value_x_variant,
                                                    value_y_variant,
                                                    value_z_variant,
                                                    state_variant
                                                    )
        else:
            can_error = self._mvu.GetFieldSpherical(value_x_variant,
                                                    value_y_variant,
                                                    value_z_variant,
                                                    state_variant
                                                    )
        if can_error > 0:
            raise MultiPyVuError('Error when calling GetPosition()')
        h_x = value_x_variant.value
        h_y = value_y_variant.value
        h_z = value_z_variant.value
        self.current_val = (h_x, h_y, h_z)
        self.state = int(state_variant.value)

        return self.current_val, self.state

    def _set_state_imp(self,
                       field: Tuple[float, float, float],
                       set_rate_per_sec: float,
                       set_approach: ApproachEnum,
                       ) -> Union[str, int]:
        # Note: Mode is reserved for future use
        mode = 0
        if self.cart_coord:
            can_error = self._mvu.SetFieldCartesian(*field,
                                                    set_rate_per_sec,
                                                    set_approach,
                                                    mode
                                                    )
        else:
            can_error = self._mvu.SetFieldSpherical(*field,
                                                    set_rate_per_sec,
                                                    set_approach,
                                                    mode
                                                    )
        self.set_point = field
        self.rate = set_rate_per_sec
        self.approach_mode = set_approach

        if can_error > 0:
            err_msg = 'Error when calling setPosition(), is the '
            err_msg += 'Rotator Option active?'
            raise MultiPyVuError(err_msg)
        else:
            # returning this string makes CommandMultiVu_base happy
            return can_error

    def test(self) -> bool:
        """
        This method is used to monitor the field. It waits for
        the status to become 'stable' at the set point

        Returns:
        --------
        bool
        """
        accept_pct = 0.005
        abs_tol = 0.4

        steady = False
        self._get_values()
        state_name = self.convert_state_dictionary(self.state)
        if state_name in ('Holding (driven)', 'Stable'):
            h_x, h_y, h_z = self.current_val
            set_x, set_y, set_z = self.set_point
            steady = floats_equal(h_x,
                                  set_x,
                                  accept_pct,
                                  abs_tol,
                                  )
            steady &= floats_equal(h_y,
                                   set_y,
                                   accept_pct,
                                   abs_tol,
                                   )
            steady &= floats_equal(h_z,
                                   set_z,
                                   accept_pct,
                                   abs_tol,
                                   )
        return steady


############################
#
# Scaffolding Implementation
#
############################

class SimulateVectorChange(ISimulateChange):
    # These are class variables, not instance variables, so that the
    # simulated instrument keeps its condition from one change
    # thread to the next.  See ISimulateChange for the reasoning.
    _stop_flag: bool = False
    _state_dict = STATE_DICT
    # The starting values come from the Command*Base class so that
    # the scaffolding and the real implementation begin in the
    # same place.
    _current_val: Tuple[float, float, float] = CommandVectorBase._current_val
    _state: int = CommandVectorBase._state
    _set_point: Tuple[float, float, float] = CommandVectorBase._set_point
    # The _rate variable gives the user requested rate
    _rate: float = CommandVectorBase._rate
    _approach: ApproachEnum = ApproachEnum.no_overshoot
    _observers: List[IObserver] = []

    def __init__(self):
        super().__init__('SimulateVectorChange')
        self._cart_coord: bool = True

    @property
    def current_val(self) -> Tuple[float, float, float]:
        return SimulateVectorChange._current_val

    @current_val.setter
    def current_val(self, new: Tuple[float, float, float]):
        SimulateVectorChange._current_val = new

    @property
    def set_point(self) -> Tuple[float, float, float]:
        return SimulateVectorChange._set_point

    @set_point.setter
    def set_point(self, new: Tuple[float, float, float]):
        SimulateVectorChange._set_point = new

    @property
    def rate(self) -> float:
        return SimulateVectorChange._rate

    @rate.setter
    def rate(self, new: float):
        SimulateVectorChange._rate = new

    @property
    def approach(self) -> ApproachEnum:
        return SimulateVectorChange._approach

    @approach.setter
    def approach(self, new: ApproachEnum):
        SimulateVectorChange._approach = new

    @property
    def use_cart_coord(self) -> bool:
        return self._cart_coord

    @use_cart_coord.setter
    def use_cart_coord(self, new: bool):
        self._cart_coord = new

    def stop_requested(self):
        return SimulateVectorChange._stop_flag

    def stop_thread(self, set_stop=True):
        SimulateVectorChange._stop_flag = set_stop

    def tuples_equal(self, tuple1: Tuple, tuple2: Tuple) -> bool:
        """
        Checks if tuples with float members are equal.

        Arguments:
            tuple1 -- Tuple made up of floats
            tuple2 -- Tuple made up of floats

        Returns:
            True if the tuples are equal
        """
        accept_pct = 0.005
        abs_tol = 0.4
        for item1, item2 in zip(tuple1, tuple2):
            if not isinstance(item1, float):
                return False
            if not isinstance(item2, float):
                return False
            if not floats_equal(item1, item2, accept_pct, abs_tol):
                return False
        # If we get here, then the items in the tuple must be equal
        return True

    def _vector_rates(self) -> Tuple[float, float, float]:
        if self.use_cart_coord:
            return self._vector_rates_cart()
        else:
            return self._vector_rates_spherical()

    def _vector_rates_cart(self) -> Tuple[float, float, float]:
        """Calculate the rate of change for each Cartesian
        coordinate.
        """
        start = np.array(self.current_val)
        end = np.array(self.set_point)
        direction = end - start
        magnitude = np.linalg.norm(direction)

        if magnitude == 0.0:
            return (0.0, 0.0, 0.0)

        unit_direction = direction / magnitude
        rates = self.rate * unit_direction

        return tuple(rates)

    def _vector_rates_spherical(self) -> Tuple[float, float, float]:
        """Calculate the rate of change for each spherical
        coordinate.
        """
        r1, theta1, phi1 = self.current_val
        r2, theta2, phi2 = self.set_point

        # # Handle angle wrapping for theta
        dtheta = theta2 - theta1
        # # Handle angle wrapping for phi
        dphi = phi2 - phi1

        direction = np.array([r2 - r1, dtheta, dphi])
        magnitude = np.linalg.norm(direction)

        if magnitude == 0.0:
            return (0.0, 0.0, 0.0)

        unit_direction = direction / magnitude
        rates = self.rate * unit_direction

        return tuple(rates)

    def _vector_times(self, vector_rate) -> Tuple[float, float, float]:
        if self.use_cart_coord:
            return self._vector_time_cart(vector_rate)
        else:
            return self._vector_time_spherical(vector_rate)

    def _vector_time_cart(self, vector_rate) -> Tuple[float, float, float]:
        """Calculate the time for each Cartesian
        coordinate to complete its movement.
        """
        times = []
        for i in range(3):
            dist = abs(self.set_point[i] - self.current_val[i])
            rate = abs(vector_rate[i])

            if rate == 0.0:
                times.append(float('inf') if dist > 0.0 else 0.0)
            else:
                times.append(dist / rate)

        return tuple(times)

    def _vector_time_spherical(self, vector_rate) -> Tuple[float, float, float]:
        """Calculate the time for each spherical
        coordinate to complete its movement.
        """
        r1, theta1, phi1 = self.current_val
        r2, theta2, phi2 = self.set_point

        # # Handle angle wrapping for theta
        dtheta = theta2 - theta1
        # # Handle angle wrapping for phi
        dphi = phi2 - phi1

        dist = [abs(r2 - r1), abs(dtheta), abs(dphi)]

        times = []
        for i in range(3):
            rate = abs(vector_rate[i])

            if rate == 0.0:
                times.append(float('inf') if dist[i] > 0.0 else 0.0)
            else:
                times.append(dist[i] / rate)

        return tuple(times)

    def _monitor(self):
        vector_rate = self._vector_rates()
        vector_time = self._vector_times(vector_rate)

        self.state = 1
        self.notify_observers(self.current_val, self.state)

        # simulate a pause before changing the field
        start_time = time.time()
        elapsed_time = time.time() - start_time
        while elapsed_time < 1:
            time.sleep(CLOCK_TIME)
            if self.stop_requested():
                return
            # check the escape key
            _check_windows_esc()
            elapsed_time = time.time() - start_time

        # set state to ramping
        start_time = time.time()
        self.state = 6
        self.notify_observers(self.current_val, self.state)
        # simulate the ramp
        while not self.tuples_equal(self.current_val, self.set_point):
            if self.stop_requested():
                return
            time.sleep(CLOCK_TIME)
            self.acquire_mutex()
            current_val = tuple(
                float(val + CLOCK_TIME * rate)
                for val, rate in zip(self.current_val, vector_rate)
            )
            # Cast this to let linters know the size of the tuple
            self.current_val = cast(Tuple[float, float, float], current_val)
            # The ramp points are discrete, so they can
            # pass over the set point.  This check ensures
            # that there is no overshoot.
            final_val = list(self.current_val)
            for i in range(3):
                val = self.current_val[i]
                set_pnt = self.set_point[i]
                if vector_rate[i] > 0:
                    final_val[i] = min(val, set_pnt)
                else:
                    final_val[i] = max(val, set_pnt)
            # Cast this to let linters know the size of the tuple
            self.current_val = cast(Tuple[float, float, float], final_val)
            self.release_mutex()
            self.notify_observers(self.current_val, self.state)
            # check the escape key
            _check_windows_esc()
            if (time.time() - start_time) > max(vector_time):
                break

        # Set the final values
        self.current_val = self.set_point
        self.state = 5
        self.notify_observers(self.current_val, self.state)
        start_time = time.time()
        # simulate coming to stability
        while time.time() - start_time < 0.5:
            time.sleep(CLOCK_TIME)
            if self.stop_requested():
                return
            _check_windows_esc()

        # at the set point
        self.state = 1
        self.notify_observers(self.current_val, self.state)
        # unsubscribe from all observers before exiting
        for o in self._observers:
            self.unsubscribe(o)
        return


class CommandVectorSim(CommandVectorBase,
                       ICommandObserverSim,
                       ):
    def __init__(self, instrument_name: str, cart_coordinates: bool = True):
        CommandVectorBase.__init__(self, instrument_name, cart_coordinates)
        ICommandObserverSim.__init__(self,
                                     SimulateVectorChange,
                                     )

    def _update_spherical_coord(self, setpoint: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """This takes the user's setpoints and if we are using spherical
        coordinates, it looks to see if theta = [0, 360] and phi = [0, 180].

        Args:
            setpoint (Tuple[float, float, float]): Desired H-vector

        Returns:
            tuple[float, float, float]: Actual H-vector
        """
        if self.cart_coord:
            return setpoint
        else:
            M, theta, phi = setpoint
            new_theta = theta % 360
            new_phi = phi % 180
            return M, new_theta, new_phi

    def _get_state_imp(self,
                       value_x_variant,
                       state_variant,
                       params='') -> Tuple:
        return self.current_val, self.state

    def _set_state_imp(self,
                       field: Tuple[float, float, float],
                       set_rate_per_sec: float,
                       set_approach: ApproachEnum,
                       ) -> Union[str, int]:
        self.change_thread: SimulateVectorChange = self.get_sim_instance()
        self.change_thread.set_params(self.current_val,
                                      self._update_spherical_coord(field),
                                      set_rate_per_sec,
                                      self.state,
                                      )
        self.approach_mode = set_approach
        self.change_thread.approach = set_approach
        self.change_thread.use_cart_coord = self.cart_coord

        self.change_thread.subscribe(self)
        self.change_thread.start()
        if self.cart_coord:
            self.set_point = field
        else:
            # Store the cartesian coordinates in the class variable.
            self.set_point = self.spherical_degrees_to_cartesian(*field)
        error = 0
        return error

    def update(self, *args):
        if len(args) != 2:
            err_msg = "Expected 2 arguments: value and state"
            raise ValueError(err_msg)
        value, state = args
        self.current_val = value
        self.state = state
