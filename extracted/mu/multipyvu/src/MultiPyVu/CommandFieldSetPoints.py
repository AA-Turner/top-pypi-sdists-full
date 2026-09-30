"""
CommandFieldSetPoints.py has the information required to get the
temperature set points.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import math
import re
from abc import abstractmethod
from enum import IntEnum
from sys import platform
from typing import Dict, Tuple, Union

from .CommandField import CommandFieldSim
from .CommandVectorMagnet import CommandVectorSim
from .exceptions import MultiPyVuError, PythoncomImportError
from .ICommand import ICommand, setpoint_read_failed

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


# the PPMS is the only flavor which can run persistent
class drivenEnum(IntEnum):
    persistent = 0
    driven = 1


units = 'Oe'

############################
#
# Base Class
#
############################


class CommandFieldSetPointsBase(ICommand):
    _cart_x_val: float = 0.0
    _cart_y_val: float = 0.0
    _cart_z_val: float = 300.0
    _rate_x_val: float = 0.0
    _rate_y_val: float = 0.0
    _rate_z_val: float = 1.0
    _approach: ApproachEnum = ApproachEnum.linear
    _driven = drivenEnum.driven

    def __init__(self, instrument_name: str, axis:str='Z'):
        super().__init__()
        self.instrument_name = instrument_name
        self.axis = axis

        self.units = units

    def set_point_x(self):
        return CommandFieldSetPointsBase._cart_x_val

    def set_point_y(self):
        return CommandFieldSetPointsBase._cart_y_val

    def set_point_z(self):
        return CommandFieldSetPointsBase._cart_z_val

    def set_point(self):
        return self.set_point_z()

    def rate_x(self):
        return CommandFieldSetPointsBase._rate_x_val

    def rate_y(self):
        return CommandFieldSetPointsBase._rate_y_val

    def rate_z(self):
        return CommandFieldSetPointsBase._rate_z_val

    def rate(self):
        return self.rate_z()

    def approach(self):
        return CommandFieldSetPointsBase._approach

    def driven_mode(self) -> drivenEnum:
        return CommandFieldSetPointsBase._driven

    def convert_result(self, response: Dict[str, str]) -> Tuple[float,
                                                                float,
                                                                ApproachEnum,
                                                                drivenEnum]:
        """
        Converts the CommandMultiVu response from get_state_server()
        to something usable for the user.

        Parameters:
        -----------
        response: Dict:
            Message.response['content']

        Returns:
        --------
        Tuple of value, rate, and approach mode.
        """
        num = r'[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?'
        search_str = rf'\(({num}),[ ]?({num}),[ ]?([0-9]*),[ ]?([0-9]*)\),[ ]?([a-zA-Z]*),[ ]?([ a-zA-Z]*)'
        r = re.findall(search_str, response['result'])
        if len(r[0]) != 6:
            msg = f'Invalid response: {response}'
            raise MultiPyVuError(msg)
        temp_str, rate_str, appr_str, driven, units, _ = r[0]
        temp = float(temp_str)
        rate = float(rate_str)
        appr_num = int(appr_str)
        driven_num = int(driven)
        # These numbers come from MultiVu itself, so a value outside
        # the enum means the response was not understood.  Report it
        # as a MultiPyVuError naming the value rather than letting
        # the enum ValueError escape to the caller.
        try:
            appr_mode = ApproachEnum(appr_num)
            driven_mode = drivenEnum(driven_num)
        except ValueError as err:
            msg = f'Invalid response: {response}  ({err})'
            raise MultiPyVuError(msg) from err
        return temp, rate, appr_mode, driven_mode

    def prepare_query(self, *args):
        raise NotImplementedError

    def convert_state_dictionary(self, status_number) -> str:
        """
        This query has no state dictionary. The status number
        is ignored and it returns a simple string.

        Arguments:
            status_number -- unused

        Returns:
            'Call was successful'
        """
        return 'Call was successful'

    def state_code_dict(self):
        raise NotImplementedError

    @abstractmethod
    def _get_state_imp(self,
                       value_variant,
                       state_variant,
                       params='') -> Tuple[float,
                                           float,
                                           int,
                                           int]:
        """
        Gets the temperature set points

        Returns:
            [temperature, rate, approach mode as int, drive mode as int]
        """
        raise NotImplementedError

    def get_state_server(self, value_variant, state_variant,  params=''):
        # The MPMS3 COM interface has no GetFieldSetpoints(), so this
        # has to be caught before the call is attempted.  Otherwise
        # CommandMultiVu turns the missing method into a much less
        # helpful 'Command not found' error.
        if self.instrument_name == 'MPMS3':
            raise MultiPyVuError('MPMS3 does not support getting field set points')
        field, rate, approach, driven = self._get_state_imp(value_variant,
                                                            state_variant,
                                                            params)
        if self.instrument_name == 'OPTICOOL' and self.axis in ('X', 'Y'):
            if self.axis == 'X':
                self._cart_x_val = field
                self._rate_x_val = rate
            elif self.axis == 'Y':
                self._cart_y_val = field
                self._rate_y_val = rate
        else:
            self._cart_z_val = field
            self._rate_z_val = rate
        self._approach = ApproachEnum(approach)
        self._driven = drivenEnum(driven)
        return (field, rate, approach, driven), 0

    def set_state_server(self, arg_string: str) -> Union[str, int]:
        raise NotImplementedError


############################
#
# Standard Implementation
#
############################


class CommandFieldSetPointsImp(CommandFieldSetPointsBase):
    def __init__(self, instrument_name, multivu_win32com, axis:str='Z'):
        """
        Parameters:
        ----------
        instrument_name: str
        multivu_win32com: win32.dynamic.CDispatch
        axis: str (optional)
            'X', 'Y', or 'Z' to indicate which axis of the vector magnet
            is being controlled.  Default is 'Z'.
        """
        super().__init__(instrument_name, axis)
        self._mvu = multivu_win32com

    def _get_state_imp(self,
                       value_variant,
                       state_variant,
                       params='') -> Tuple[float,
                                           float,
                                           int,
                                           int]:
        """
        Retrieves information from MultiVu

        Parameters:
        -----------
        value_variant: VARIANT: set up by pywin32com for getting the value
        state_variant: VARIANT: set up by pywin32com for getting the approach mode
        params: str (optional)
            optional parameters that may be required to query MultiVu

        Returns:
        --------
        Tuple(str, str, str, str)
            The value and state number
        """
        if self.instrument_name == 'PPMS':
            # Setting up a by-reference (VT_BYREF) string (VT_BSTR)
            # variant.  This is used to get the response.
            string_variant = (win32.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_BSTR, ""))

            # Setting up a by-reference (VT_BYREF) string (VT_BSTR)
            # variant.  This is used to get the error.
            error_variant = (win32.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_BSTR, ""))

            command = 'FIELD?'
            device = 0
            timeout = 0
            # This command returns nonsense if there is no Model6000 attached.
            can_error = self._mvu.SendPpmsCommand(command,
                                                  string_variant,
                                                  error_variant,
                                                  device,
                                                  timeout,
                                                  )
            response = string_variant.value.split(',')
            if len(response) != 4:
                # Strip out any garbage/non-ASCII bytes so this stays
                # safely printable/loggable. This can happen on a PPMS
                # in simulation mode with no Model6000 attached.
                error = error_variant.value.encode('ascii', errors='backslashreplace').decode('ascii')
                err_msg = 'Invalid response while getting '
                err_msg += f'field setpoints: "{response}"'
                err_msg += f' error = "{error}"'
                raise MultiPyVuError(err_msg)
            set_point, rate, approach, mode = response
            set_point = float(set_point)
            rate = float(rate)
            approach = int(approach)
            mode = int(mode)
            return set_point, rate, approach, mode
        else:
            # Setting up a by-reference (VT_BYREF) double (VT_R8)
            # variant.  This is used to get the value.
            rate_variant = (win32.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0))
            # Setting up a by-reference (VT_BYREF) integer (VT_I4)
            # variant.  This is used to get the status code.
            mode_variant = (win32.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_I4, 0))
            if self.instrument_name == 'VERSALAB':
                can_error = self._mvu.GetLastFieldSetpoint(value_variant,
                                                           rate_variant,
                                                           state_variant,
                                                           mode_variant)
            elif self.instrument_name == 'OPTICOOL' and self.axis in ('X', 'Y'):
                if self.axis == 'X':
                    can_error = self._mvu.GetFieldSetpointsX(value_variant,
                                                             rate_variant,
                                                             state_variant,
                                                             mode_variant)
                if self.axis == 'Y':
                    can_error = self._mvu.GetFieldSetpointsY(value_variant,
                                                             rate_variant,
                                                             state_variant,
                                                             mode_variant)
                # The Z axis gets its value from the regular field setpoints
            else:
                can_error = self._mvu.GetFieldSetpoints(value_variant,
                                                        rate_variant,
                                                        state_variant,
                                                        mode_variant)
            # The set point getters do not use the same success value on
            # every flavor; see setpoint_read_failed() for the per-flavor
            # table and why.  The PPMS never reaches here -- it takes the
            # SendPpmsCommand branch above -- so this cannot reintroduce
            # the PPMS false negatives that motivated the old
            # 'can_error > 1' test.
            #
            # This one matters more than most:  on failure MultiVu leaves
            # the out-parameters untouched, so carrying on would hand
            # wait_for() a field set point of 0.0 and it would judge
            # stability against zero field.
            if setpoint_read_failed(self.instrument_name, can_error):
                err_msg = 'Error when calling GetFieldSetpoints() '
                err_msg += f'(returned {can_error}).  The set point could '
                err_msg += 'not be read, so it must not be used.'
                raise MultiPyVuError(err_msg)
            set_point = value_variant.value
            rate = rate_variant.value
            approach = state_variant.value
            driven = mode_variant.value
            return set_point, rate, approach, driven


############################
#
# Scaffolding Implementation
#
############################

class CommandFieldSetPointsSim(CommandFieldSetPointsBase):

    def __init__(self, instrument_name: str, axis:str='Z'):
        CommandFieldSetPointsBase.__init__(self, instrument_name, axis)

    @property
    def _cart_x(self) -> float:
        return self.__cart_x_val

    @_cart_x.setter
    def _cart_x(self, value: float) -> None:
        self.__cart_x_val = value

    @property
    def _cart_y(self) -> float:
        return self.__cart_y_val

    @_cart_y.setter
    def _cart_y(self, value: float) -> None:
        self.__cart_y_val = value

    @property
    def _cart_z(self) -> float:
        return self.__cart_z_val

    @_cart_z.setter
    def _cart_z(self, value: float) -> None:
        self.__cart_z_val = value

    def _get_state_imp(self,
                       value_variant,
                       state_variant,
                       params='') -> Tuple[float,
                                           float,
                                           int,
                                           int]:
        # The code is retrieving the values and the specific mvu flavor
        # does not matter, so picking the PPMS
        field = CommandFieldSim('PPMS')
        # A NaN set point would be formatted into the response and
        # then fail to parse, so report it plainly instead.
        if math.isnan(field.set_point):
            err_msg = 'No field set point has been established.  Call '
            err_msg += 'set_field() before asking for the set points.'
            raise MultiPyVuError(err_msg)
        # This part converts the enum types from CommandField to CommandFieldSetPoints
        approach = field.approach.value
        drive = field.driven.value
        if self.axis == 'X':
            set_point = field.set_point
            rate = field.rate
        elif self.axis == 'Y':
            set_point = field.set_point
            rate = field.rate
        else:
            set_point = field.set_point
            rate = field.rate
        return set_point, rate, approach, drive
