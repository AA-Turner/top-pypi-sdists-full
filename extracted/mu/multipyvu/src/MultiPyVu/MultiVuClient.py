#!/usr/bin/env python3
"""
Created on Mon Jun 7 23:47:19 2021

MultiVuClient.py is a module for use on a network that has access to a
computer running MultiVuServer.py.  By running this client, a python script
can be used to control a Quantum Design cryostat.

This inherits the MultiVuClientBase class.  The base has the basic 
communication commands, and this has specific commands for communicating
with MultiVu.

@author: D. Jackson
"""

import traceback
from enum import IntEnum
from sys import exc_info
from typing import Tuple, Union

from . import CommandFactory as _CommandFactory
from .BRT import Brt as _brt
from .CommandChamber import modeEnum as _chamber_mode
from .CommandChamber import units as _chamber_units
from .CommandField import ApproachEnum as _field_approach_mode
from .CommandField import drivenEnum as _field_driven_mode
from .CommandField import units as _field_units
from .CommandFieldSetPoints import CommandFieldSetPointsSim as _CommandFieldSetPointsSim
from .CommandMultiVu import SET_POINT_UNCONFIRMED as _set_point_unconfirmed
from .CommandRotator import units as _rotator_units
from .CommandTemperature import STATE_DICT as _temperature_state_dict
from .CommandTemperature import ApproachEnum as _temperature_approach_mode
from .CommandTemperature import units as _temperature_units
from .CommandWaitFor import MaskEnum as _wait_for_enum
from .CommandWaitFor import WaitForStatus as _wait_for_status
from .exceptions import (CanError, MultiPyVuError, ServerCloseError,
                         abort_err_enum, can_err_enum)
from .instrument import InstrumentList
from .MultiVuClient_base import ClientBase as _ClientBase
from .project_vars import HOST_CLIENT, PORT
from .sdo_object import SdoObject
from .sdo_object import val_type as _sdo_val_type


class Client(_ClientBase):
    """
    This class is used for a client to connect to a computer with
    MultiVu running MultiVuServer.py.

    Parameters:
    -----------
    host: str (optional)
        The IP address for the server.  Default is 'localhost.'
    port: int (optional)
        The port number to use to connect to the server.
    """
    class __TemperatureAdapter():
        """
        Holds enums used for temperature control
        """
        def __init__(self):
            self.units = _temperature_units
            self.approach_mode = _temperature_approach_mode
            self.state_code_dict = lambda: _temperature_state_dict
            self.waitfor = _wait_for_enum.temperature
    temperature = __TemperatureAdapter()

    class __FieldAdapter():
        """
        Holds enums used for field control
        """
        def __init__(self):
            self.units = _field_units
            self.approach_mode = _field_approach_mode
            self.driven_mode = _field_driven_mode
            f_class = _CommandFactory.create_command_field()
            self.state_code_dict = f_class.state_code_dict
            self.waitfor = _wait_for_enum.field
    field = __FieldAdapter()

    class __ChamberAdapter():
        """
        Holds enums used for chamber control
        """
        def __init__(self):
            self.units = _chamber_units
            self.mode = _chamber_mode
            c_class = _CommandFactory.create_command_chamber()
            self.state_code_dict = c_class.state_code_dict
            self.waitfor = _wait_for_enum.chamber
    chamber = __ChamberAdapter()

    class __RotatorAdapter():
        """
        Holds enums used for the horizontal rotator
        """
        def __init__(self) -> None:
            self.units = _rotator_units
            hr_class = _CommandFactory.create_command_position()
            self.state_code_dict = hr_class.state_code_dict
    rotator = __RotatorAdapter()

    def __init__(self,
                 host: str = HOST_CLIENT,
                 port: int = PORT,
                 ):
        super().__init__(host, port)
        self.resistivity = _brt(self)
        """
        The resistivity option provides capabilities to measure
        electrical resistance.  This includes configuring the
        measurements from within python.
        """

        self._thread_running = False

        # Aliased to MaskEnum rather than restated, so the two cannot
        # drift apart.  These are MultiVu's own WaitFor() bit numbers;
        # note that chamber is 8, not 4 -- 4 is MultiVu's position bit.
        self.subsystem = _wait_for_enum
        self.wait_status = _wait_for_status

    ###########################
    #  Command Methods
    ###########################

    def _get_sdo(self, sdo_obj: SdoObject) -> Tuple[Union[float, str], str]:
        """
        This returns the value of an sdo query.

        Parameters:
        -----------
        sdo_obj: sdo_object

        Returns:
        --------
        A tuple of (value, status).
        """
        if self._message is None:
            raise ServerCloseError('Not connected to the server')
        response = self._query_server('SDO?', str(sdo_obj))
        try:
            can_sdo = _CommandFactory.create_command_sdo()
            value, status = can_sdo.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            value = 0
            status = e.value
        return value, status

    def _set_sdo(self,
                 sdo_obj: SdoObject,
                 write_val: Union[str, int, float]) -> None:
        """
        This sets an SDO value.

        Parameters:
        -----------
        sdo_obj: sdo_object

        write_val: str or int or float
            The value to be written.  The type must match the type
            specified in the sdo_object.

        Returns:
        --------
        None
        """
        try:
            can_sdo = _CommandFactory.create_command_sdo()
            query = can_sdo.prepare_query(write_val, sdo_obj)
        except ValueError as e:
            self._logger.info(e)
            raise ValueError

        self._query_server('SDO', query)

    def get_temperature(self) -> Tuple[float, str]:
        """
        This gets the current temperature, in Kelvin, from MultiVu.

        Returns:
        --------
        A tuple of (temperature, status).
        """
        response = self._query_server('TEMP?', '')
        try:
            temperature = _CommandFactory.create_command_temp()
            temperature, status = temperature.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            temperature = 0
            status = e.value
        return temperature, status

    def set_temperature(self,
                        set_point: float,
                        rate_per_min: float,
                        approach_mode: IntEnum
                        ):
        """
        This sets the temperature.

        Parameters:
        -----------
        set_point : float
            The desired temperature, in Kelvin.
        rate_per_min : float
            The rate of change of the temperature in K/min
        approach_mode : IntEnum
            This uses the MultiVuClient.temperature.approach_mode enum.
            Options are:
                temperature.approach_mode.fast_settle
                temperature.approach_mode.no_overshoot

        Returns:
        --------
        None
        """
        temperature = _CommandFactory.create_command_temp()
        try:
            query = temperature.prepare_query(set_point,
                                              rate_per_min,
                                              approach_mode,
                                              )
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            response = self._query_server('TEMP', query)
            self._warn_if_set_point_unconfirmed(response,
                                                'temperature',
                                                )

    def _warn_if_set_point_unconfirmed(self,
                                      response: dict,
                                      what: str,
                                      ) -> None:
        """
        Tell the user when MultiVu took a set command but never
        reported the new set point back.

        Not an error -- the set itself succeeded -- so this warns rather
        than raising.  It is surfaced here, on the client, because the
        server writes its own log entry on the server, which for a
        remote setup is not the machine running the script.

        Parameters:
        -----------
        response: dict
            What _query_server() returned.
        what: str
            'temperature' or 'field', for the message.
        """
        if _set_point_unconfirmed in str(response.get('result', '')):
            msg = f'Warning: MultiVu accepted the {what} set point but '
            msg += 'did not report it back.  A wait_for() issued now may '
            msg += 'see the system as already settled at the previous '
            msg += 'set point.  The server log has the detail.'
            self._logger.warning(msg)

    def get_aux_temperature(self) -> Tuple[float, str]:
        """
        This is used to get the OptiCool auxiliary temperature,
        in Kelvin.  This command gets it's value directly from
        the OptiCool rather than reading the value from MultiVu.

        Returns:
        --------
        A tuple of (temperature, read_status).

        Raises:
        -------
        MultiPyVuException
            This command is only used for OptiCool
        """
        if self.instrument_name != InstrumentList.OPTICOOL.name:
            msg = "'get_aux_temperature()' is only used for OptiCool"
            raise MultiPyVuError(msg)
        sdo = SdoObject(3, 0x6001, 0x4, _sdo_val_type.double_t)
        temperature, status = self._get_sdo(sdo)
        return float(temperature), status

    def get_temperature_setpoints(self) -> Tuple[float, float, str]:
        """
        This gets the temperature set points from MultiVu.

        Returns:
        --------
        A tuple of (temperature, rate, approach mode)
        """
        response = self._query_server('TEMP_SETPOINTS?', '')
        try:
            temp_sp = _CommandFactory.create_command_temp_setpoints()
            t, rate, approach_enum = temp_sp.convert_result(response)
            approach_mode = approach_enum.name
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            t = 0.0
            rate = 0.0
            approach_mode = e.value
        return t, rate, approach_mode

    def get_field(self) -> Tuple[float, str]:
        """
        This gets the current field, in Oe, from MultiVu.

        Returns:
        --------
        A tuple of (field, status)
        """
        response = self._query_server('FIELD?', '')
        try:
            field = _CommandFactory.create_command_field()
            h, status = field.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            field = 0
            status = e.value
        return h, status

    def set_field(self,
                  set_point: float,
                  rate_per_sec: float,
                  approach_mode: _field_approach_mode,
                  driven_mode: _field_driven_mode = _field_driven_mode.driven,
                  ):
        """
        This sets the magnetic field.

        Parameters:
        -----------
        set_point : float
            The desired magnetic field, in Oe.
        rate_per_sec : float
            The ramp rate, in Oe/sec.
        approach_mode : .field.approach_mode enum.  Options are:
                field.approach_mode.linear
                field.approach_mode.no_overshoot
                field.approach_mode.oscillate
        driven_mode :  .field.driven_mode, and is only used
            by the PPMS, for which the options are:
                .field.driven_mode.Persistent
                .field.driven_mode.Driven (Default)

        Raises:
        -------
        ValueError
            Thrown if the set_point and rate_per_sec are not numbers.

        Returns:
        --------
        None
        """
        try:
            field = _CommandFactory.create_command_field()
            query = field.prepare_query(set_point,
                                        rate_per_sec,
                                        approach_mode,
                                        driven_mode)
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            response = self._query_server('FIELD', query)
            self._warn_if_set_point_unconfirmed(response, 'field')

    def get_field_setpoints(self) -> Tuple[float, float, str, str]:
        """
        This gets the magnetic field set points from MultiVu.

        Returns:
        --------
        A tuple of (field, rate, approach mode, driven mode)
        """
        response = self._query_server('FIELD_SETPOINTS?', '')
        try:
            field_sp = _CommandFactory.create_command_field_setpoints()
            f, rate, approach_enum, driven_enum = field_sp.convert_result(response)
            approach_mode = approach_enum.name
            driven_mode = driven_enum.name
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            f = 0.0
            rate = 0.0
            approach_mode = e.value
            driven_mode = 'Unknown'
        return f, rate, approach_mode, driven_mode

    def get_vector_cartesian(self) -> Tuple[Tuple[float, float, float], str]:
        """
        This gets the current vector magnet field in cartesian
        coordinates, in Oe, from MultiVu.

        Returns:
        --------
        A tuple of ((field_x, field_y, field_z), status)
        """
        response = self._query_server('VECTOR_CART?', '')
        try:
            field = _CommandFactory.create_command_vector(cartesian_coordinates=True)
            h, status = field.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            field = (0.0, 0.0, 0.0)
            status = e.value
        return h, status

    def set_vector_cartesian(self,
                             set_point: Tuple[float, float, float],
                             rate_per_sec: float,
                             approach_mode: IntEnum,
                             ):
        """
        This sets the vector magnetic field using cartesian
        coordinates.

        Parameters:
        -----------
        set_point : Tuple[float, float, float]
            The desired magnetic field, in Oe, using cartesian coordinates,
            (H_x, H_y, H_z).
        rate_per_sec : float
            The ramp rate, in Oe/sec.
        approach_mode : IntEnum
            This uses the .field.approach_mode enum.  Options are:
                field.approach_mode.linear
                field.approach_mode.no_overshoot
                field.approach_mode.oscillate

        Raises:
        -------
        ValueError
            Thrown if the set_point and rate_per_sec are not numbers.

        Returns:
        --------
        None
        """
        try:
            field = _CommandFactory.create_command_vector(cartesian_coordinates=True)
            query = field.prepare_query(set_point,
                                        rate_per_sec,
                                        approach_mode,
                                        )
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            self._query_server('VECTOR_CART', query)

    def get_vector_spherical(self) -> Tuple[Tuple[float, float, float], str]:
        """
        This gets the current vector magnet field in spherical
        coordinates, in Oe, from MultiVu.

        Returns:
        --------
        A tuple of ((field_m, field_theta, field_phi), status)
        """
        response = self._query_server('VECTOR_SPHERE?', '')
        try:
            field = _CommandFactory.create_command_vector(cartesian_coordinates=False)
            h, status = field.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            field = 0
            status = e.value
        return h, status

    def set_vector_spherical(self,
                             set_point: Tuple[float, float, float],
                             rate_per_sec: float,
                             approach_mode: IntEnum,
                             ):
        """
        This sets the vector magnetic field using spherical
        coordinates.

        Parameters:
        -----------
        set_point : Tuple[float, float, float]
            The desired magnetic field, in Oe, using spherical coordinates,
            (M, theta, phi).
        rate_per_sec : float
            The ramp rate, in Oe/sec.
        approach_mode : IntEnum
            This uses the .field.approach_mode enum.  Options are:
                field.approach_mode.linear
                field.approach_mode.no_overshoot
                field.approach_mode.oscillate

        Raises:
        -------
        ValueError
            Thrown if the set_point and rate_per_sec are not numbers.

        Returns:
        --------
        None
        """
        try:
            field = _CommandFactory.create_command_vector(cartesian_coordinates=False)
            query = field.prepare_query(set_point,
                                        rate_per_sec,
                                        approach_mode,
                                        )
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            self._query_server('VECTOR_SPHERE', query)

    def get_vector_setpoints_cartesian(self) -> Tuple[
                                                      Tuple[float, float, float],
                                                      Tuple[float, float, float],
                                                      str,
                                                      str]:
        """
        This gets the vector magnetic field set points from MultiVu
        in cartesian coordinates.

        Returns:
        --------
        A tuple of (
                    (field_x, field_y, field_z),
                    (rate_x, rate_y, rate_z),
                    approach mode,
                    driven mode
                    )
        """
        x_field, x_rate, _, _ = self.get_field_setpointsX()
        y_field, y_rate, _, _ = self.get_field_setpointsY()
        z_field, z_rate, approach, driven = self.get_field_setpointsZ()
        field = (x_field, y_field, z_field)
        rate = (x_rate, y_rate, z_rate)
        return field, rate, approach, driven

    def get_vector_setpoints_spherical(self) -> Tuple[
                                                      Tuple[float, float, float],
                                                      Tuple[float, float, float],
                                                      str,
                                                      str]:
        """
        This gets the vector magnetic field set points from MultiVu
        in cartesian coordinates.

        Returns:
        --------
        A tuple of (
                    (field_x, field_y, field_z),
                    (rate_x, rate_y, rate_z),
                    approach mode,
                    driven mode
                    )
        """
        x_field, x_rate, _, _ = self.get_field_setpointsX()
        y_field, y_rate, _, _ = self.get_field_setpointsY()
        z_field, z_rate, approach, driven = self.get_field_setpointsZ()
        field_cart = (x_field, y_field, z_field)
        f = _CommandFieldSetPointsSim('')
        field = f.cartesian_to_spherical(*field_cart)
        rate_cart = (x_rate, y_rate, z_rate)
        rate = f.cartesian_to_spherical(*rate_cart)
        return field, rate, approach, driven

    def get_field_setpointsX(self) -> Tuple[float, float, str, str]:
        """
        This gets the magnetic field set points from MultiVu.

        Returns:
        --------
        A tuple of (field, rate, approach mode, driven mode)
        """
        response = self._query_server('FIELD_SETPOINTS_X?', '')
        try:
            field_sp = _CommandFactory.create_command_field_setpoints()
            f, rate, approach_enum, driven_enum = field_sp.convert_result(response)
            approach_mode = approach_enum.name
            driven_mode = driven_enum.name
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            f = 0.0
            rate = 0.0
            approach_mode = e.value
            driven_mode = 'Unknown'
        return f, rate, approach_mode, driven_mode

    def get_field_setpointsY(self) -> Tuple[float, float, str, str]:
        """
        This gets the magnetic field set points from MultiVu.

        Returns:
        --------
        A tuple of (field, rate, approach mode, driven mode)
        """
        response = self._query_server('FIELD_SETPOINTS_Y?', '')
        try:
            field_sp = _CommandFactory.create_command_field_setpoints()
            f, rate, approach_enum, driven_enum = field_sp.convert_result(response)
            approach_mode = approach_enum.name
            driven_mode = driven_enum.name
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            f = 0.0
            rate = 0.0
            approach_mode = e.value
            driven_mode = 'Unknown'
        return f, rate, approach_mode, driven_mode

    def get_field_setpointsZ(self) -> Tuple[float, float, str, str]:
        """
        This gets the Z axis vector magnetic field set points from MultiVu.

        Returns:
        --------
        A tuple of (field, rate, approach mode, driven mode)
        """
        return self.get_field_setpoints()

    def get_chamber(self) -> str:
        """
        This gets the current chamber setting.

        Returns:
        --------
        str
            The chamber status.
        """
        response = self._query_server('CHAMBER?', '')
        chamber = _CommandFactory.create_command_chamber()
        try:
            status = chamber.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            status = (0, e.value)
        return status[1]

    def set_chamber(self, mode: IntEnum):
        """
        This sets the chamber status.

        Parameters:
        -----------
        mode : IntEnum
            The chamber is set using the MultiVuClient.chamber.Mode enum.
            Options are:
                chamber.mode.seal
                chamber.mode.purge_seal
                chamber.mode.vent_seal
                chamber.mode.pump_continuous
                chamber.mode.vent_continuous
                chamber.mode.high_vacuum

        Raises:
        -------
        MultiVuExeException

        Returns:
        --------
        None
        """
        try:
            chamber = _CommandFactory.create_command_chamber()
            query = chamber.prepare_query(mode)
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            self._query_server('CHAMBER', query)

    def wait_for(self,
                 delay_sec: float = 0.0,
                 timeout_sec: float = 0.0,
                 bitmask: int = 0,
                 ):
        """
        This command pauses the code until the specified criteria are met.

        Parameters:
        -----------
        delay_sec : float, optional
            Time in seconds to wait after stability is reached.  Default is 0.0
        timeout_sec : float, optional
            If stability is not reached within timeout (in seconds), the
            wait is abandoned. The default timeout is 0, which indicates this
            feature is turned off (i.e., to wait forever for stability).
        bitmask : int, optional
            This tells wait_for which parameters to wait on.  The best way
            to set this parameter is to byte-wise or the three possibilities:
              client.temperature.waitfor
              client.field.waitfor
              client.chamber.waitfor
            For example, to wait for the temperature and field to stabilize,
            one would set
              bitmask = client.temperature.waitfor | client.field.waitfor
            The default is client.subsystem.no_system (which is 0);
            client.subsystem also carries .temperature, .field and
            .chamber, using MultiVu's own bit numbers.

        Returns:
        --------
        WaitForStatus
            How the wait ended.  WaitForStatus.good (0) means stability
            was reached and delay_sec elapsed; WaitForStatus.timed_out
            (258) means timeout_sec ran out first.  These are MultiVu's
            own WaitFor() codes, and are also available as
            client.wait_status.

            Note that a timeout is reported, not raised, so a script
            which ignores the return value behaves as it always has.
            Scripts that care should check it:

                if client.wait_for(0, 600, mask) != client.wait_status.good:
                    ...

            Before this was returned, a wait that timed out and a wait
            that succeeded were indistinguishable at the call site.
        """
        try:
            wait_for = _CommandFactory.create_command_wait_for(self.instrument_name)
            query = wait_for.prepare_query(delay_sec,
                                           timeout_sec,
                                           bitmask,
                                           )
        except ValueError as e:
            self._logger.info(e)
            raise ValueError
        else:
            response = self._query_server('WAITFOR', query)
            return wait_for.convert_set_result(response)

    def is_steady(self, bitmask: int = 0) -> bool:
        """
        Query the server to see if the cryostat is in a steady state

        Parameters:
        -----------
        bitmask : Enum, optional
            This tells wait_for which parameters to query.  The best way
            to set this parameter is to byte-wise or the three possibilities:
              client.temperature.waitfor
              client.field.waitfor
              client.chamber.waitfor
            For example, to query the temperature and field for stability,
            one would set
              bitmask = client.temperature.waitfor | client.field.waitfor
            The default is client.subsystem.no_system (which is 0);
            client.subsystem also carries .temperature, .field and
            .chamber, using MultiVu's own bit numbers.

        Returns:
        --------
        bool
            True if system is stable
        """
        param: int = 0

        if isinstance(bitmask, IntEnum):
            param = bitmask.value
        else:
            param = bitmask

        response = self._query_server('WAITFOR?', str(param))
        wait_for = _CommandFactory.create_command_wait_for(self.instrument_name)
        try:
            stable = wait_for.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            # encountered a problem, so return False
            stable = ['0.0000', '']
        value = int(stable[0])
        return bool(value)

    def get_position(self) -> Tuple[float, str]:
        """
        This gets the rotator position, in degrees, from MultiVu.

        Returns:
        --------
        A tuple of (position, status)
        """
        response = self._query_server('POSITION?', '')
        try:
            pos = _CommandFactory.create_command_position()
            position, status = pos.convert_result(response)
        except MultiPyVuError as e:
            tb = traceback.extract_tb(exc_info()[2])
            formatted_traceback = ''.join(traceback.format_list(tb))
            self._logger.info(f'{e}\nTraceback:\n {formatted_traceback}')
            position = 0.0
            status = e.value
        return position, status

    def set_position(self,
                     set_point: float,
                     rate_per_sec: float,
                     ):
        """
        This sets the rotator position.

        Parameters:
        -----------
        set_point : float
            The desired rotator position, in deg.
        rate_per_sec : float
            The ramp rate, in deg/sec.

        Raises:
        -------
        ValueError
            Thrown if the set_point and rate_per_sec are not numbers.

        Returns:
        --------
        None
        """
        try:
            pos = _CommandFactory.create_command_position()
            query = pos.prepare_query(set_point,
                                      rate_per_sec,
                                      )
        except ValueError as e:
            self._logger.info(e)
            raise
        else:
            self._query_server('POSITION', query)
