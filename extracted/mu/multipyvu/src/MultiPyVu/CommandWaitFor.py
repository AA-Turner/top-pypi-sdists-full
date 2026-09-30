"""
CommandWaitFor.py calls the MultiVu command of the same name

Created on Tue May 18 13:14:28 2021

@author: djackson
"""

import logging
import math
import time
from abc import abstractmethod
from enum import IntEnum
from sys import platform
from typing import Dict, List, Tuple, Union

from .check_windows_esc import _check_windows_esc
from .CommandChamber import SimulateChamberChange
from .CommandField import SimulateFieldChange, CommandFieldImp
from .CommandFieldSetPoints import CommandFieldSetPointsImp
from .CommandTemperature import SimulateTemperatureChange, CommandTemperatureImp
from .CommandTempSetPoints import CommandTempSetpointsImp
from .CommandVectorMagnet import SimulateVectorChange
from .exceptions import (CanError, MultiPyVuError, PythoncomImportError,
                         can_err_enum)
from .ICommand import ICommand, ICommandImp, ISimulateChange
from .IEventManager import IObserver
from .project_vars import CLOCK_TIME, SERVER_NAME

if platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
    except ImportError:
        raise PythoncomImportError


class MaskEnum(IntEnum):
    """
    Which subsystems wait_for() should wait on.

    These are MultiVu's own bit assignments, taken from
    IMultiVuPpmsServer::WaitFor():

        BOOL bTemp    = 0x00000001L & mask;
        BOOL bField   = 0x00000002L & mask;
        BOOL bPos     = 0x00000004L & mask;
        BOOL bChamber = 0x00000008L & mask;

    Verified identical in all four MultiVu flavors in this working copy
    (Dynacool, OptiCool, SQUIDVsm, Versalab).

    Note that chamber was 4 here until this branch, which collided with
    MultiVu's position bit.  Nothing was actually mis-waited, because
    the mask has never been handed to MultiVu -- wait_for() has always
    evaluated it locally -- but the numbers had to agree before the
    return codes below could mean anything, and before the mask could
    ever be forwarded.  A script that passed a bare 4 rather than
    MaskEnum.chamber now selects position, which is rejected as
    unsupported rather than quietly waiting on the chamber.
    """
    no_system = 0
    temperature = 1
    field = 2
    position = 4
    chamber = 8
    # MultiVuClient used to expose this member under the name
    # no_subsystem, so keep that spelling working.  Repeating a value
    # in an IntEnum makes an alias, not a new member.
    no_subsystem = 0


class WaitForStatus(IntEnum):
    """
    How a wait_for() call ended.

    The values are MultiVu's own WaitFor() return codes, defined in
    IMultiVuPpmsServer.cpp, so that a wait reports its outcome in the
    same vocabulary whether it was carried out here or (eventually) by
    MultiVu itself.  The member names are this module's; the C++ macro
    each one corresponds to is named beside it below.

    Two of the values are worth knowing the provenance of, because
    neither is an arbitrary choice and neither is obvious from the
    number:  zero for success comes from MDISTD.H, where GOOD is
    FALSE; and 258 is the Win32 WAIT_TIMEOUT macro, which MultiVu
    reuses rather than defining a code of its own.
    """
    good = 0                    # GOOD
    no_items_selected = 200     # NO_ITEMS_SELECTED_TO_CHECK
    invalid_mask = 202          # INVALID_MASK
    invalid_delay = 203         # INVALID_DELAY_TIME
    invalid_timeout = 204       # INVALID_TIME_TO_WAIT_LIMIT
    timed_out = 258             # WAIT_TIMEOUT


# How many consecutive polls a subsystem must report settled before
# wait_for() believes it.
#
# One poll is not enough, because a set command and the wait that
# follows it are two separate COM round trips, and in the gap MultiVu
# can still be reporting the state it was in before the set.  Requiring
# the answer to repeat throws away a single stale sample at a cost of
# one CLOCK_TIME.
#
# MultiVu does not need this for temperature -- its SetTemperature and
# WaitFor run in the same process -- but it does need it for the field,
# and CMagnetBase::IsFieldStableForWait() solves it there with a
# busy-flag handshake.  That handshake is not reachable from here: the
# busy flag is not on the COM surface.  This is the blunt equivalent.
#
# Both monitored subsystems are exposed, by different routes:
#   - temperature, since the set point no longer takes part in the
#     verdict (see UNSTABLE_STATE_CODES in CommandTemperature.py), so a
#     stale "Stable" is enough to end the wait on its own.
#   - field, because .test() compares against a set point this class
#     reads from MultiVu once at the start of the wait.  A stale read
#     there returns the *previous* set point, which the field is still
#     sitting at, and that also looks settled.
#
# What this does not fix is that stale set point read itself -- two
# polls of a stale target are still stale.  The time.sleep(CLOCK_TIME)
# before the set points are read is what covers that, imperfectly.
REQUIRED_SETTLED_POLLS: int = 2

units = ''

############################
#
# Base Class
#
############################


class CommandWaitForBase(ICommand):
    def __init__(self, instrument_name: str):
        super().__init__()

        self.units = units
        self.instrument_name = instrument_name

        # The subsystems this flavor can be asked to wait on.  Position
        # is deliberately absent:  MultiVu defines the bit, but nothing
        # here monitors the rotator yet, so accepting it would make
        # wait_for() return straight away instead of waiting.  Asking
        # for it raises rather than doing that quietly.
        self._supported_masks = [MaskEnum.temperature, MaskEnum.field]
        if self.instrument_name != 'OPTICOOL':
            # The OptiCool has no sample chamber.
            self._supported_masks.append(MaskEnum.chamber)

        self._max_bitmask = 0
        for mask in self._supported_masks:
            self._max_bitmask = self._max_bitmask | mask

        self.logger = logging.getLogger(SERVER_NAME)

        # Listing every supported subsystem, which is what the error
        # messages using this text claim to do.  This used to append
        # only the chamber line, and only for non-OptiCool flavors, so
        # a bad mask was reported without naming any valid choice.
        self._mask_options_text = ''
        for m in self._supported_masks:
            self._mask_options_text += f'\n\t{m.name} = {m.value}'

    def _monitored_subsystems(self) -> list:
        """
        The objects wait_for() is currently watching.

        The real implementation keeps them in a list called i_cmds and the
        scaffolding one in a dict called monitors, so normalize both.
        """
        cmds = getattr(self, 'i_cmds', None)
        if cmds:
            return list(cmds)
        monitors = getattr(self, 'monitors', None)
        if monitors:
            return list(monitors.values())
        return []

    def _pending_state_msg(self,
                           elapsed_time: float,
                           timeout_sec: float,
                           ) -> str:
        """
        Describe what wait_for() was still waiting on when it gave up.

        wait_for() returns nothing whether it stabilized or timed out, so
        without this a timeout leaves no trace at the call site.

        Parameters:
        -----------
        elapsed_time: float
            Seconds spent waiting.
        timeout_sec: float
            The timeout which was exceeded.

        Returns:
        --------
        A multi-line description of every monitored subsystem.
        """
        msg = f'wait_for() timed out after {elapsed_time:.1f} s '
        msg += f'(timeout = {timeout_sec:.1f} s).  Monitored subsystems:'
        subsystems = self._monitored_subsystems()
        if not subsystems:
            msg += '\n\tnone were being monitored'
            return msg
        for cmd in subsystems:
            name = getattr(cmd, 'name', None) or type(cmd).__name__
            try:
                if hasattr(cmd, 'test'):
                    steady = cmd.test()
                elif hasattr(cmd, 'is_sim_alive'):
                    steady = not cmd.is_sim_alive()
                else:
                    steady = 'unknown'
            except Exception as e:
                msg += f'\n\t{name}:  could not be queried ({e})'
                continue
            try:
                status = cmd.convert_state_dictionary(cmd.state)
            except Exception:
                status = str(getattr(cmd, 'state', 'unknown'))
            reading = getattr(cmd, 'current_val', 'n/a')
            set_point = getattr(cmd, 'set_point', 'n/a')
            msg += f'\n\t{name}:  steady = {steady}'
            msg += f', reading = {reading}'
            msg += f', set point = {set_point}'
            msg += f', status = "{status}"'
        return msg

    def convert_result(self, response: Dict) -> Tuple[float, str]:
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

        if len(r) != 3:
            msg = f'Invalid response: {response}'
            raise MultiPyVuError(msg)
        return (r[0], r[2])

    def convert_set_result(self, response: Dict) -> 'WaitForStatus':
        """
        Pull the wait status out of a 'WAITFOR' set response.

        CommandMultiVu.set_state() formats it as
            'WAITFOR Command Received,<code>'

        Parameters:
        -----------
        response: Dict
            Message.response['content']

        Returns:
        --------
        The WaitForStatus for the wait which just finished.  An older
        server, or one which answered without a code, is reported as
        .good so that this never invents a failure.
        """
        result = str(response.get('result', ''))
        _, _, code = result.rpartition(',')
        try:
            return WaitForStatus(int(code.strip()))
        except ValueError:
            msg = 'wait_for() could not read a status code from the '
            msg += f'server response "{result}", so it is being reported '
            msg += 'as successful.'
            self.logger.debug(msg)
            return WaitForStatus.good

    def prepare_query(self,
                      delay_sec: float,
                      timeout_sec: float = 0.0,
                      bitmask: int = 0,
                      ) -> str:
        delay_sec, timeout_sec, bitmask = self._check_args(delay_sec,
                                                           timeout_sec,
                                                           bitmask,
                                                           )

        return f'{delay_sec},{timeout_sec},{bitmask}'

    def _check_args(self,
                    delay_sec: Union[float, int, str],
                    timeout_sec: Union[float, int, str] = 0.0,
                    bitmask: Union[float, int, str] = 0,
                    ) -> Tuple[float, float, int]:
        """
        Check that the incoming values are of the correct type.

        Parameters:
        -----------
        delay_sec: number or string
        timeout_sec: number or string
        bitmask: number or string

        Returns:
        --------
        (delay_sec, timeout_sec, bitmask): Tuple[float, float, int]
        """
        try:
            delay_sec = float(delay_sec)
        except ValueError:
            err_msg = 'delay_sec must be a float (delay_sec = '
            err_msg += "'{delay_sec}')"
            raise ValueError(err_msg)

        try:
            timeout_sec = float(timeout_sec)
        except ValueError:
            err_msg = 'timeout_sec must be a float (timeout_sec = '
            err_msg += "'{timeout_sec}')"
            raise ValueError(err_msg)

        try:
            bitmask = int(bitmask)
            bitmask = abs(bitmask)
        except ValueError:
            err_msg = 'bitmask must be an int '
            err_msg += f'(bitmask = \'{bitmask}\')'
            err_msg += self._mask_options_text
            raise ValueError(err_msg)
        self._check_bitmask(bitmask)
        return delay_sec, timeout_sec, bitmask

    def _check_bitmask(self, bitmask: int) -> None:
        """
        Reject a mask asking for a subsystem this flavor cannot wait on.

        This looks at the individual bits rather than comparing the mask
        against a maximum.  A magnitude test cannot tell an unsupported
        subsystem from a supported one:  with MultiVu's numbering, the
        position bit (4) is smaller than the chamber bit (8), so
        'bitmask > max' would let position through on any flavor that
        supports the chamber.

        Parameters:
        -----------
        bitmask: int

        Raises:
        -------
        MultiPyVuError
            If any bit outside self._supported_masks is set.
        """
        unsupported = bitmask & ~self._max_bitmask
        if not unsupported:
            return

        named = [m.name for m in MaskEnum
                 if m.value and (unsupported & m.value) == m.value]
        if MaskEnum.position.name in named:
            err_msg = 'wait_for() cannot wait on the position subsystem.  '
            err_msg += 'MultiVu defines that bit, but MultiPyVu does not '
            err_msg += 'monitor the rotator, so waiting on it would return '
            err_msg += 'immediately.  Poll get_position() instead.'
        elif (MaskEnum.chamber.name in named) \
                and (self.instrument_name == 'OPTICOOL'):
            err_msg = 'Chamber control is not available for the OptiCool'
        elif named:
            err_msg = f'The mask, {bitmask}, asks for a subsystem which is '
            err_msg += f'not available on the {self.instrument_name}: '
            err_msg += ', '.join(named) + '.'
            err_msg += self._mask_options_text
        else:
            err_msg = f'The mask, {bitmask}, is out of bounds.'
            err_msg += self._mask_options_text
        raise MultiPyVuError(err_msg)

    def convert_state_dictionary(self, status_number: int) -> str:
        """
        Takes a string with the can error and abort error in the form
        of (can_error;abort_error) and returns a human readable
        description of the error.

        Parameters:
        -----------
        status_number: int
            can error returned from calling MultiVu

        Returns:
        -------
        A string of the error in words.
        """
        return str(CanError(status_number, 0))

    def state_code_dict(self):
        state_dict = {}
        for can_num in can_err_enum:
            state_dict[can_num, 0] = str(CanError(can_num, 0))
        return state_dict

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
            int(bool)
        """
        try:
            bitmask = int(params)
            bitmask = abs(bitmask)
        except ValueError:
            err_msg = 'bitmask must be an int '
            err_msg += f'(bitmask = \'{bitmask}\')'
            err_msg += self._mask_options_text
            raise ValueError(err_msg)
        self._check_bitmask(bitmask)

        # Add a brief delay before moving on so that the setpoints
        # can get sent to MultiVu and it has time to internally
        # set them.
        time.sleep(CLOCK_TIME)

        return self._get_state(bitmask)

    @abstractmethod
    def _get_state(self, bitmask: int) -> Tuple[float, int]:
        """
        Monitors the state of the system and returns int(bool) for stability

        Parameters:
        -----------
        bitmask: int
            This is used with bite-wise or to know which sub-system
            is monitored for stability

        Returns:
        --------
        Tuple(float, int)
            int(bool)
        """
        raise NotImplementedError

    @abstractmethod
    def _set_state_imp(self,
                       delay_sec: float,
                       timeout_sec: float = 0.0,
                       bitmask: int = 0,
                       ) -> str:
        raise NotImplementedError

    def set_state_server(self, arg_string: str) -> Union[str, int]:
        """
        Sets up the waitfor based on the bitmask, then calls ._wait_for()

        bitmask : int, optional
            This tells wait_for which parameters to wait on.  The best way
            to set this parameter is to byte-wise or the three possibilities:
              client.temperature.waitfor
              client.field.waitfor
              client.chamber.waitfor
            For example, to wait for the temperature and field to stabilize,
            one would set
              bitmask = client.temperature.waitfor | client.field.waitfor
            The default is client.no_subsystem (which is 0).

        Returns:
        --------
        A WaitForStatus code saying how the wait ended, or an error
        string if the arguments could not be parsed.  CommandMultiVu
        .set_state() passes the code through to the client rather than
        treating a non-zero value as a failure, because a timeout is a
        legitimate outcome a script may want to branch on.
        """
        if len(arg_string.split(',')) > 3:
            err_msg = 'wait_for() requires between one and three '
            err_msg += 'numeric inputs, separated by a comma: '
            err_msg += 'delay after stability is reached (s), '
            err_msg += 'timeout to wait for stability (s), '
            err_msg += 'bitmask:'
            err_msg += self._mask_options_text
            return err_msg

        # Add a brief delay before moving on so that the setpoints
        # can get sent to MultiVu and it has time to internally
        # set them.
        time.sleep(CLOCK_TIME)

        delay_sec, timeout_sec, bitmask = self._check_args(*arg_string.split(','))
        err = self._set_state_imp(delay_sec, timeout_sec, bitmask)

        return err


############################
#
# Standard Implementation
#
############################

class CommandWaitForImp(CommandWaitForBase):
    def __init__(self,
                 multivu_win32com,
                 instrument_name,
                 t_obj: CommandTemperatureImp,
                 h_obj: CommandFieldImp,
                 c_obj: ICommandImp
                 ):
        super().__init__(instrument_name)
        self.t = t_obj
        self.h = h_obj
        self.c = c_obj
        self.current_vals: Dict[str, Tuple] = {}
        self._mvu = multivu_win32com

    def _build_monitor_list(self, bitmask: int) -> List[ICommandImp]:
        """
        The command objects a wait with this bitmask has to watch, with
        each one's set point refreshed from MultiVu first.

        Both ._get_state() and ._set_state_imp() need exactly this, and
        each used to carry its own verbatim copy.

        Parameters:
        -----------
        bitmask: int
            Which subsystems to watch.  Already checked by
            ._check_bitmask().

        Returns:
        --------
        The Command*Imp objects to poll, in temperature, field, chamber
        order.  Also stored on .i_cmds, which ._pending_state_msg()
        reads in order to describe a timeout.
        """
        # Setting up by-reference (VT_BYREF) double (VT_R8)
        # variants.  These will be used to get values.
        set_point_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0))
        # Setting up a by-reference (VT_BYREF) integer (VT_I4)
        # variant.  This is used to get the status code.
        appr_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_I4, 0))

        self.i_cmds: List[ICommandImp] = []
        if (bitmask & MaskEnum.temperature == MaskEnum.temperature):
            t_set = CommandTempSetpointsImp(self.instrument_name, self._mvu)
            (t, rate, approach), _ = t_set.get_state_server(set_point_variant, appr_variant)
            self.t.set_point = t
            self.t.rate = rate
            self.t.approach = self.t.approach_mode(approach)
            self.i_cmds.append(self.t)
        if bitmask & MaskEnum.field == MaskEnum.field:
            if self.instrument_name == 'MPMS3':
                # The MPMS3 does not appear to have a way to get the field setpoint.
                # Customers will want to set the field before calling wait_for()
                # when telling the system to wait for field stability.
                # Stability is therefore judged against whatever set point
                # an earlier set_field() left behind, so record it:  a
                # stale or default set point is what makes a field wait
                # run all the way to its timeout.
                # Without a set point there is nothing to compare the
                # field against, so the wait would run to its timeout
                # and then report success.  Say so instead of waiting.
                if math.isnan(self.h.set_point):
                    err_msg = 'The MPMS3 cannot report its field set '
                    err_msg += 'point, so wait_for() has no target to '
                    err_msg += 'judge field stability against.  Call '
                    err_msg += 'set_field() before waiting on the field.'
                    raise MultiPyVuError(err_msg)
                msg = 'The MPMS3 cannot report its field set point, so '
                msg += 'wait_for() is judging field stability against '
                msg += f'set point = {self.h.set_point} {self.h.units}.  '
                msg += 'Call set_field() before wait_for() if that is not '
                msg += 'the intended target.'
                self.logger.debug(msg)
            else:
                h_set = CommandFieldSetPointsImp(self.instrument_name, self._mvu)
                (h, rate, approach, driven), _ = h_set.get_state_server(set_point_variant, appr_variant)
                self.h.set_point = h
                self.h.rate = rate
                self.h.approach = self.h.approach_mode(approach)
                self.h.driven = self.h.drive_mode(driven)
            self.i_cmds.append(self.h)
        if bitmask & MaskEnum.chamber == MaskEnum.chamber:
            self.i_cmds.append(self.c)
        return self.i_cmds


    def _get_state(self, bitmask: int) -> Tuple[float, int]:
        """
        Monitors the state of the system and returns int(bool) for stability

        Parameters:
        -----------
        bitmask: int
            This is used with bite-wise or to know which sub-system
            is monitored for stability

        Returns:
        --------
        Tuple(float, int)
            int(bool)
        """
        self.i_cmds = self._build_monitor_list(bitmask)

        # check if changes have finished
        stable = [c for c in self.i_cmds if not c.test()]
        # check if all threads have finished
        result = (len(stable) == 0)
        return (int(result), 0)

    def _set_state_imp(self,
                       delay_sec: float,
                       timeout_sec: float = 0.0,
                       bitmask: int = 0,
                       ) -> int:
        """
        This command pauses the code until the specified criteria are met.

        Parameters
        ----------
        delay_sec : float
            Time in seconds to wait after stability is reached.
        timeout_sec : float, optional
            If stability is not reached within timeout (in seconds), the
            wait is abandoned. The default timeout is 0, which indicates this
            feature is turned off (i.e., to wait forever for stability).
        bitmask : int, optional
            This tells wait_for which parameters to wait on.  The best way
            to set this parameter is to use the MultiVuClient.subsystem enum,
            using bite-wise or to wait for multiple parameters.  For example,
            to wait for the temperature and field to stabilize, one would set
            bitmask = (Client.temperature.waitfor
                       | MultiVuClient.field.waitfor).
            The default is MultiVuClient.no_subsystem (which is 0).

        """
        self.i_cmds = self._build_monitor_list(bitmask)

        # A settled reading has to repeat before it is believed; see
        # REQUIRED_SETTLED_POLLS.  Counted here in the loop rather than
        # on the command objects so that .test() stays a plain question
        # with no memory -- ._pending_state_msg() calls it again for its
        # diagnostics, and that must not be able to disturb a wait.
        settled_polls = [0] * len(self.i_cmds)

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if (timeout_sec > 0.0) and (elapsed_time > timeout_sec):
                self.logger.info(self._pending_state_msg(elapsed_time,
                                                         timeout_sec,
                                                         ))
                return WaitForStatus.timed_out
            else:
                time.sleep(CLOCK_TIME)
            _check_windows_esc()

            # check if changes have finished
            for i, cmd in enumerate(self.i_cmds):
                if cmd.test():
                    settled_polls[i] += 1
                else:
                    # Moving again, so start counting over.
                    settled_polls[i] = 0
            # quit once every subsystem has held still long enough.
            # An empty i_cmds (bitmask 0) satisfies all() and falls
            # straight through to the delay loop, as it always did.
            if all(n >= REQUIRED_SETTLED_POLLS for n in settled_polls):
                break

        # delay loop
        start_delay_time = time.time()
        while (time.time() - start_delay_time) < delay_sec:
            if (timeout_sec > 0.0) \
                    and ((time.time() - start_time) > timeout_sec):
                # Stability was reached, but the overall timeout cut
                # the post-stability delay short, so this still counts
                # as a timeout rather than a completed wait.
                self.logger.info(self._pending_state_msg(
                    time.time() - start_time,
                    timeout_sec,
                    ))
                return WaitForStatus.timed_out
            _check_windows_esc()
            time.sleep(CLOCK_TIME)
        return WaitForStatus.good


############################
#
# Scaffolding Implementation
#
############################


class CommandWaitForSim(CommandWaitForBase, IObserver):
    def __init__(self,
                 instrument_name,
                 t_obj: SimulateTemperatureChange,
                 h_obj: SimulateFieldChange,
                 c_obj: SimulateChamberChange,
                 ):
        super().__init__(instrument_name)
        self.t = t_obj
        self.h = h_obj
        self.c = c_obj

    def _get_state(self, bitmask: int) -> Tuple[float, int]:
        """
        Monitors the state of the system and returns int(bool) for stability

        Parameters:
        -----------
        bitmask: int
            This is used with bite-wise or to know which sub-system
            is monitored for stability

        Returns:
        --------
        Tuple(float, int)
            int(bool)
        """
        # subscribe to the changes.
        self.monitors: Dict[str, ISimulateChange] = {}
        if (bitmask & MaskEnum.temperature) == MaskEnum.temperature:
            self.monitors[self.t.name] = self.t
        if (bitmask & MaskEnum.field) == MaskEnum.field:
            self.monitors[self.h.name] = self.h
        if (bitmask & MaskEnum.chamber) == MaskEnum.chamber:
            self.monitors[self.c.name] = self.c

        for m in self.monitors.values():
            # see if the set_point has been defined
            try:
                m.set_point
            except AttributeError:
                m.set_point = m.current_val
            m.subscribe(self)

        # check if changes have finished
        stable = [name for name,
                  m in self.monitors.items()
                  if not m.is_sim_alive()]
        # remove the stable items
        for m in stable:
            del self.monitors[m]
        # quit if all threads have finished
        result = (len(self.monitors) == 0)
        return int(result), 0

    def _set_state_imp(self,
                       delay_sec: float,
                       timeout_sec: float = 0.0,
                       bitmask: int = 0,
                       ) -> int:
        # subscribe to the changes.
        self.monitors: Dict[str, ISimulateChange] = {}
        if (bitmask & MaskEnum.temperature) == MaskEnum.temperature:
            self.monitors[self.t.name] = self.t
        if (bitmask & MaskEnum.field) == MaskEnum.field:
            self.monitors[self.h.name] = self.h
        if (bitmask & MaskEnum.chamber) == MaskEnum.chamber:
            self.monitors[self.c.name] = self.c

        for m in self.monitors.values():
            # see if the set_point has been defined
            try:
                m.set_point
            except AttributeError:
                m.set_point = m.current_val
            m.subscribe(self)

        err = self._wait_for(delay_sec, timeout_sec)

        # unsubscribe from all the monitors
        for m in self.monitors.values():
            m.unsubscribe(self)
        return err

    def _wait_for(self,
                  delay_sec: float,
                  timeout_sec: float = 0.0,
                  ) -> int:
        """
        This command pauses the code until the specified criteria are met.

        Parameters
        ----------
        delay_sec : float
            Time in seconds to wait after stability is reached.
        timeout_sec : float, optional
            If stability is not reached within timeout (in seconds), the
            wait is abandoned. The default timeout is 0, which indicates this
            feature is turned off (i.e., to wait forever for stability).
        """
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if (timeout_sec > 0.0) and (elapsed_time > timeout_sec):
                self.logger.info(self._pending_state_msg(elapsed_time,
                                                         timeout_sec,
                                                         ))
                return WaitForStatus.timed_out
            else:
                time.sleep(CLOCK_TIME)
            _check_windows_esc()

            # check if changes have finished
            stable = [name for name, m in self.monitors.items() if not m.is_sim_alive()]
            # remove the stable items
            for m in stable:
                del self.monitors[m]
            # quit if all threads have finished
            if len(self.monitors) == 0:
                break

        # delay loop
        start_delay_time = time.time()
        while (time.time() - start_delay_time) < delay_sec:
            if (timeout_sec > 0.0) \
                    and (time.time() - start_time) > timeout_sec:
                # Stability was reached, but the overall timeout cut
                # the post-stability delay short, so this still counts
                # as a timeout rather than a completed wait.
                self.logger.info(self._pending_state_msg(
                    time.time() - start_time,
                    timeout_sec,
                    ))
                return WaitForStatus.timed_out
            _check_windows_esc()
            time.sleep(CLOCK_TIME)
        return WaitForStatus.good

    def update(self, value, state):
        pass
