"""
This provides an interface for MultiVu commands (CommandTemperature,
                                                 CommandField,
                                                 and CommandChamber)
as well as an interface to track setting changes which can be used
by the wait_for() command.

It requires ABCplus (Abstract Base Class plus), which is found here:
    https://pypi.org/project/abcplus/

Created on Tue May 18 12:59:24 2021

@author: djackson
"""

import logging
import traceback
from abc import ABC, abstractmethod
from sys import platform
from threading import Lock, Thread, enumerate
from time import sleep, time
from typing import (Callable, Dict, Generic, Optional, Tuple, Type,
                    TypeVar, Union)

from .exceptions import PythoncomImportError
from .IEventManager import IObserver, Publisher
from .project_vars import CLOCK_TIME, SERVER_NAME

if platform == 'win32':
    try:
        import pythoncom
        import win32com.client as win32
        from pywintypes import com_error as pywin_com_error
    except ImportError:
        raise PythoncomImportError

T = TypeVar('T', bound='ISimulateChange')


# Flavors whose Get*Setpoints COM methods return 1 for success and 0
# for failure, rather than the 0-for-success convention used by most of
# the interface.
#
# What is going on, from reading MultiVu's own source:
#
#   Most getters follow MDISTD.H's GOOD == FALSE == 0.  GetTemperature()
#   ends with "return FALSE; // no error" and returns TRUE from its
#   failure branch.  GetChamber() returns its Err flag the same way.
#
#   The set point getters do the opposite.  They are written as
#
#       if (CommErr = pMagnet->GetLastTempSetpoint(f, r, a, m))
#       {
#           *field = f; ...          // only assigned here
#       }
#       return CommErr;
#
#   and the inner call returns "(err == false)", i.e. true for success.
#   So the COM return is 1 when it worked, 0 when it did not -- and on
#   failure the out-parameters are never written at all, so the caller
#   silently keeps whatever it passed in.  That is the dangerous part:
#   a failed read leaves a set point of 0.0, and wait_for() would then
#   judge stability against zero.
#
#   The MPMS3 is the exception.  Its GetLastTempSetpoint() calls
#   SendTempQuery(), a GPIB query which returns FALSE on success, so
#   that one flavor keeps the 0-for-success convention under the same
#   method name.
#
# Verified by reading IMultiVuPpmsServer.cpp, MAGNET.CPP, TEMP.CPP and
# MagPsuHwComm.cpp in each flavor's own MultiVu source:
#
#   DYNACOOL   GetTemperatureSetpoints / GetFieldSetpoints    1 == success
#   OPTICOOL   GetTemperatureSetpoints / GetFieldSetpoints*   1 == success
#   VERSALAB   GetLastTempSetpoint    / GetLastFieldSetpoint  1 == success
#   MPMS3      GetLastTempSetpoint                            0 == success
#   PPMS       -- reaches none of these; it uses SendPpmsCommand instead
#
# This is why the old "raise only if can_error > 1" test appeared to be
# the only thing that worked:  it accepts both 0 and 1, so it never
# fired on any flavor.  It removed the false negatives by removing the
# check.
SETPOINT_GETTERS_RETURN_TRUE_ON_SUCCESS = ('DYNACOOL', 'OPTICOOL', 'VERSALAB')


# How long a set command will wait for MultiVu to report back the set
# point it was just given.  This is a handshake, not a settle time: it
# is over as soon as the set point is confirmed, and one COM getter
# costs about 0.2 ms (measured against a live MPMS3), so a healthy
# system spends well under a millisecond here.  The ceiling only
# matters when MultiVu never adopts the set point, and in that case the
# wait is abandoned with a log entry rather than an error.
SET_POINT_CONFIRM_SEC = 2.0


def setpoint_read_failed(instrument_name: str, can_error: int) -> bool:
    """
    Decide whether a Get*Setpoints call actually failed.

    Parameters:
    -----------
    instrument_name: str
        The MultiVu flavor, as in InstrumentList.
    can_error: int
        Whatever the COM call returned.

    Returns:
    --------
    True if the call failed and its out-parameters must not be trusted.
    """
    if instrument_name in SETPOINT_GETTERS_RETURN_TRUE_ON_SUCCESS:
        return int(can_error) != 1
    return int(can_error) != 0


def floats_equal(current_val: float,
                 set_point: float,
                 rel_tol: float,
                 abs_tol: float,
                 ) -> bool:
    """
    Use a combination of relative tolerance and absolute tolerance
    to determine if the values are equal
    """
    diff = abs(current_val - set_point)
    pass_absolute = diff <= abs_tol
    if pass_absolute:
        return pass_absolute

    ave = 0.5 * (current_val + set_point)
    rel_diff = diff / max(abs(ave), 1)
    return rel_diff <= rel_tol


class ICommand(ABC):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'convert_result')
            and callable(subclass.convert_result)
            and
            hasattr(subclass, 'prepare_query')
            and callable(subclass.prepare_query)
            and
            hasattr(subclass, 'convert_state_dictionary')
            and callable(subclass.convert_state_dictionary)
            and
            hasattr(subclass, 'get_state_server')
            and callable(subclass.get_state_server)
            and
            hasattr(subclass, 'set_state_server')
            and callable(subclass.set_state_server)
            and
            hasattr(subclass, 'state_code_dict')
            and callable(subclass.state_code_dict)

            or NotImplemented)

    @abstractmethod
    def __init__(self):
        self.units = ''

    @abstractmethod
    def convert_result(self, response: Dict) -> Tuple:
        raise NotImplementedError

    @abstractmethod
    def prepare_query(self, *args):
        raise NotImplementedError

    @abstractmethod
    def convert_state_dictionary(self, status_number):
        raise NotImplementedError

    @abstractmethod
    def get_state_server(self,
                         value_variant,
                         state_variant,
                         params: str = '') -> Tuple[float, int]:
        raise NotImplementedError

    @abstractmethod
    def set_state_server(self, arg_string: str) -> Union[str, int]:
        raise NotImplementedError

    @abstractmethod
    def state_code_dict(self) -> Dict:
        raise NotImplementedError


class ICommandImp(ICommand):
    """This is the base class for the command implementations
    which talk to real hardware through MultiVu.

    This is not a thread.  Its methods are called synchronously
    from ServerMessage._do_work(), which runs on the ServerMessage
    thread, so anything raised here is caught and logged by the
    catch_thread_error decorator on
    ServerMessage.monitor_socket_connection().

    ISimulateChange is the scaffolding counterpart, and that one
    really is a thread.
    """
    # Whether the last set command's set point was seen to take.  True
    # by default so a command which never confirms anything is not
    # reported as a failure.  CommandMultiVu.set_state() reads this and
    # passes a note back to the client, because the log entry
    # ._confirm_set_point() writes lands on the *server*, which may be a
    # different machine from the script that issued the set.
    set_point_confirmed: bool = True

    def _confirm_set_point(self,
                           requested: float,
                           read_set_point: Callable[[], Optional[float]],
                           label: str,
                           units: str = '',
                           ) -> bool:
        """
        Wait for MultiVu to report back the set point it was just given.

        A Set* call returns as soon as MultiVu has taken the command,
        not once the controller has adopted it.  A wait_for() issued
        immediately afterwards can therefore read the *previous* set
        point, and the system is still sitting at that one, so it looks
        settled and the wait ends at once.  Confirming here closes that
        window at its source, which is the one thing
        REQUIRED_SETTLED_POLLS in CommandWaitFor.py cannot do -- two
        polls of a stale set point are still stale.

        This deliberately never raises.  A MultiPyVuError raised on the
        server closes the client's socket, so failing here would turn a
        set that MultiVu already accepted into a dropped connection.  If
        the set point cannot be confirmed, that is logged and the caller
        carries on as it did before this existed.

        Parameters:
        -----------
        requested: float
            The set point that was just asked for.
        read_set_point: callable
            Returns the set point MultiVu currently reports, or None if
            this flavor cannot report one.
        label: str
            What is being confirmed, for the log ('temperature').
        units: str, optional

        Returns:
        --------
        True if MultiVu reported the requested set point in time.
        """
        logger = logging.getLogger(SERVER_NAME)
        deadline = time() + SET_POINT_CONFIRM_SEC
        reported = None
        while time() < deadline:
            try:
                reported = read_set_point()
            except Exception as e:
                # Including a flavor which cannot report a set point at
                # all.  Nothing here is worth failing a set over.
                msg = f'Could not read the {label} set point back to '
                msg += f'confirm it: {e}'
                logger.debug(msg)
                self.set_point_confirmed = True
                return False
            if reported is None:
                # This flavor does not report one; nothing to confirm.
                self.set_point_confirmed = True
                return False
            if floats_equal(reported, requested, 1e-4, 1e-3):
                self.set_point_confirmed = True
                return True
            sleep(CLOCK_TIME)

        msg = f'The {label} set point was set to {requested}{units}, but '
        msg += f'MultiVu still reported {reported}{units} after '
        msg += f'{SET_POINT_CONFIRM_SEC} s.  A wait_for() issued now may '
        msg += 'see the system as already settled at the previous set '
        msg += 'point.'
        logger.info(msg)
        # The only case the client is told about:  MultiVu answered, and
        # kept answering with a different set point.  A set point that
        # simply cannot be read back is not a failure of the set.
        self.set_point_confirmed = False
        return False

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'test')
                and callable(subclass.test)
                or NotImplemented)

    def __init__(self):
        super().__init__()

    def _get_values(self):
        """
        Queries the server
        """
        # Setting up a by-reference (VT_BYREF) double (VT_R8)
        # variant.  This is used to get the value.
        value_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_R8, 0.0)
            )
        # Setting up a by-reference (VT_BYREF) integer (VT_I4)
        # variant.  This is used to get the status code.
        state_variant = (win32.VARIANT(
            pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
            )
        current_info = self.get_state_server(value_variant,
                                             state_variant,
                                             )
        self.current_val, self.state = current_info

    @abstractmethod
    def test(self):
        raise NotImplementedError


class ISimulateChange(Thread, Publisher):
    """This interface is used to monitor changes in settings
    in order to help the wait_for() method to see when changes
    have been completed.

    Implement the ._monitor() method, and then start a thread by
    calling .start().  That works because this class overrides the
    Thread.run() method which is called by Thread.start(), and
    .run() calls ._monitor().

    This class inherits Publisher, which is used to broadcast the
    value and status settings.

    The subclasses keep _current_val, _set_point, _rate and _state
    as class variables rather than instance variables, and that is
    deliberate.  These classes stand in for an instrument, and a
    real instrument simply holds whatever the last command left it
    in.  The server only ever talks to one piece of hardware, so
    state shared by every instance is what matches the real
    behavior.  It also has to be shared because .get_sim_instance()
    builds a new change thread for each set operation, and the
    simulated instrument has to keep its condition across that.
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, '_monitor')
                and callable(subclass._monitor)
                and
                hasattr(subclass, 'stop_requested')
                and callable(subclass.stop_requested)
                and
                hasattr(subclass, 'stop_thread')
                and callable(subclass.stop_thread)
                or NotImplemented)

    # Each subclass points this at its module STATE_DICT so that a
    # status code can be reported by name.
    _state_dict: Dict[int, str] = {}

    def __init__(self,
                 name: str = 'ISimulateChange',
                 ):
        Thread.__init__(self)
        Publisher.__init__(self)
        self.name = name
        self.daemon = True
        self.mutex = Lock()
        self._stop_flag = False

    def acquire_mutex(self):
        if self.mutex is not None:
            self.mutex.acquire()

    def release_mutex(self):
        if self.mutex is not None:
            self.mutex.release()

    def notify_observers(self, *args) -> None:
        """
        Since the publishers are running in threads,
        do a thread lock before notifying everyone.
        """
        self.acquire_mutex()
        super().notify_observers(*args)
        self.release_mutex()

    def is_sim_alive(self):
        alive = False
        for t in enumerate():
            if t.name == self.name:
                alive = True
                break
        return alive

    @abstractmethod
    def stop_thread(self, set_stop=True):
        self.acquire_mutex()
        self._stop_flag = set_stop
        self.release_mutex()

    @abstractmethod
    def stop_requested(self):
        return self._stop_flag

    def run(self):
        """
        The thread entry point, called by Thread.start().

        This is the only place a simulation thread's errors can be
        caught.  Anything escaping ._monitor() would otherwise go to
        threading.excepthook and the thread would die without
        explanation, leaving wait_for() to block until it times out.
        The real-hardware counterpart of this guard is the
        catch_thread_error decorator on
        ServerMessage.monitor_socket_connection().
        """
        # Turn off the stop flag
        self.stop_thread(False)
        try:
            self._monitor()
        # ignore keyboard interrupts
        except KeyboardInterrupt:
            pass
        except BaseException:
            msg = f'Exception in simulation thread \'{self.name}\':\n'
            msg += traceback.format_exc()
            logging.getLogger(SERVER_NAME).info(msg)

    @property
    def set_point(self):
        return self._set_point

    @set_point.setter
    def set_point(self, new):
        self._set_point = new

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, new):
        self._rate = new

    @property
    def current_val(self):
        return self._current_val

    @current_val.setter
    def current_val(self, new):
        self._current_val = new

    def convert_state_dictionary(self, status_number) -> str:
        """
        The name of a status code.  wait_for() logs the monitored
        subsystems by name on timeout, and the scaffolding hands it
        these change threads where the real implementation hands it
        the Command objects, so both need to be able to do this.
        """
        return self._state_dict.get(status_number, str(status_number))

    @property
    def state(self) -> int:
        return self._state

    @state.setter
    def state(self, new: int):
        # Write the class attribute rather than an instance one, so
        # that the simulated instrument's state is shared the way its
        # value, set point and rate are.  get_sim_instance() builds a
        # new change thread per set operation, and wait_for() reports
        # on the one it was handed, which has to see the same state.
        type(self)._state = new

    def set_params(self,
                   current_val: Union[float, str, tuple],
                   set_point: Union[float, tuple],
                   rate: float,
                   state: int,
                   ):
        self.current_val = current_val
        self.set_point = set_point
        self.rate = abs(rate)
        self.state = state

    @abstractmethod
    def _monitor(self):
        raise NotImplementedError


class ICommandObserverSim(IObserver, Generic[T]):
    def __init__(self,
                 i_sim_change: Type[T],
                 ):
        super().__init__()
        self._change_thread_type = i_sim_change
        self.change_thread = i_sim_change()

    @property
    def change_thread(self) -> T:
        return self._change_thread

    @change_thread.setter
    def change_thread(self, new: T):
        self._change_thread = new

    def get_sim_instance(self) -> T:
        """
        Instantiates the sim_class change thread.  This checks to see
        if the thread is already running, and stops it if so.
        """
        # if running, stop the thread
        self.change_thread.stop_thread()
        # the while loop just makes sure that the
        # thread eventually ends.
        start_time = time()
        while self.change_thread.is_sim_alive():
            sleep(CLOCK_TIME)
            # this should take less than 2 seconds
            if time() - start_time > 2.0:
                break
        self.change_thread.unsubscribe(self)
        self.change_thread = self._change_thread_type()
        return self.change_thread
