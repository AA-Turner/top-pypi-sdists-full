"""
CommandTempSetPoints.py has the information required to get the
temperature set points.

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import re
from abc import abstractmethod
from enum import IntEnum
from sys import platform
from typing import Dict, Tuple, Union

from .CommandTemperature import CommandTemperatureSim
from .exceptions import MultiPyVuError, PythoncomImportError
from .ICommand import ICommand, setpoint_read_failed

if platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError:
        raise PythoncomImportError


class ApproachEnum(IntEnum):
    fast_settle = 0
    no_overshoot = 1


units = 'K'

############################
#
# Base Class
#
############################


class CommandTempSetpointsBase(ICommand):
    _set_point: float = 300.0
    _rate: float = 1.0
    _approach: ApproachEnum = ApproachEnum.fast_settle

    def __init__(self):
        super().__init__()

        self.units = units

    def set_point(self):
        return CommandTempSetpointsBase._set_point

    def rate(self):
        return CommandTempSetpointsBase._rate

    def approach(self):
        return CommandTempSetpointsBase._approach

    def convert_result(self, response: Dict[str, str]) -> Tuple[float,
                                                                float,
                                                                ApproachEnum]:
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
        search_str = rf'\(({num}),[ ]?({num}),[ ]?([0-9]*)\),[ ]?([a-zA-Z]*),[ ]?([ a-zA-Z]*)'
        r = re.findall(search_str, response['result'])
        if len(r[0]) != 5:
            msg = f'Invalid response: {response}'
            raise MultiPyVuError(msg)
        temp_str, rate_str, appr_str, units, _ = r[0]
        temp = float(temp_str)
        rate = float(rate_str)
        appr_num = int(appr_str)
        appr_mode = ApproachEnum(appr_num)
        return temp, rate, appr_mode

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
                                           int]:
        """
        Gets the temperature set points

        Returns:
            [temperature, rate, approach mode as an int]
        """
        raise NotImplementedError

    def get_state_server(self, value_variant, state_variant,  params=''):
        temp, rate, approach = self._get_state_imp(value_variant,
                                                   state_variant,
                                                   params)
        self._set_point = temp
        self._rate = rate
        self._approach = ApproachEnum(approach)
        return (temp, rate, approach), 0

    def set_state_server(self, arg_string: str) -> Union[str, int]:
        raise NotImplementedError


############################
#
# Standard Implementation
#
############################


class CommandTempSetpointsImp(CommandTempSetpointsBase):
    def __init__(self, instrument_name, multivu_win32com):
        """
        Parameters:
        ----------
        instrument_name: str
        multivu_win32com: win32.dynamic.CDispatch
        """
        super().__init__()
        self._mvu = multivu_win32com
        self.instrument_name = instrument_name

    def _get_state_imp(self,
                       value_variant,
                       state_variant,
                       params='') -> Tuple[float, float, int]:
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
        Tuple(float, float, int)
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

            command = 'TEMP?'
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
            if len(response) != 3:
                # Strip out any garbage/non-ASCII bytes so this stays
                # safely printable/loggable. This can happen on a PPMS
                # in simulation mode with no Model6000 attached.
                error = error_variant.value.encode('ascii', errors='backslashreplace').decode('ascii')
                err_msg = 'Invalid response while getting '
                err_msg += f'temperature setpoints: "{response}"'
                err_msg += f' error = "{error}"'
                raise MultiPyVuError(err_msg)
            set_point, rate, approach = response
            set_point = float(set_point)
            rate = float(rate)
            approach = int(approach)
            return set_point, rate, approach
        else:
            # Setting up a by-reference (VT_BYREF) double (VT_R8)
            # variant.  This is used to get the value.
            rate_variant = (win32.VARIANT(
                pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0))
            if self.instrument_name in ['VERSALAB', 'MPMS3']:
                can_error = self._mvu.GetLastTempSetpoint(value_variant,
                                                          rate_variant,
                                                          state_variant)
            else:
                can_error = self._mvu.GetTemperatureSetpoints(value_variant,
                                                              rate_variant,
                                                              state_variant)
        # The set point getters do not use the same success value on
        # every flavor; see setpoint_read_failed() for the per-flavor
        # table and why.  The PPMS never reaches here -- its branch
        # above returns -- so this cannot reintroduce the PPMS false
        # negatives that motivated the old 'can_error > 1' test.
        if setpoint_read_failed(self.instrument_name, can_error):
            err_msg = 'Error when calling GetTemperatureSetpoints() '
            err_msg += f'(returned {can_error}).  The set point could not '
            err_msg += 'be read, so it must not be used.'
            raise MultiPyVuError(err_msg)
        set_point = value_variant.value
        rate = rate_variant.value
        approach = state_variant.value

        return set_point, rate, approach


############################
#
# Scaffolding Implementation
#
############################

class CommandTempSetpointsSim(CommandTempSetpointsBase):

    def __init__(self):
        CommandTempSetpointsBase.__init__(self)

    def _get_state_imp(self,
                       value_variant,
                       state_variant,
                       params='') -> Tuple[float, float, int]:
        temp = CommandTemperatureSim()
        return temp.set_point, temp.rate, temp.approach.value
