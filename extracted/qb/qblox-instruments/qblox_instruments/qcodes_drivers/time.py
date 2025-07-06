# ----------------------------------------------------------------------------
# Description    : time block QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import time
from enum import IntEnum
from typing import Optional, Union

from qcodes import Instrument, InstrumentChannel

from qblox_instruments.docstring_helpers import partial_with_numpy_doc
from qblox_instruments.qcodes_drivers.component import Component
from qblox_instruments.qcodes_drivers.io_channel import IOChannel


class Polarity(IntEnum):
    FALLING_EDGE = 0
    RISING_EDGE = 1


class SyncRef(IntEnum):
    OFF = 0
    ON = 1


# -- class -------------------------------------------------------------------


class Time(Component):
    """
    This class represents the time block, used to contain time-related functionality.
    It is not a physical block, in the way that quad, module or sequencer are.
    """

    # ------------------------------------------------------------------------
    def __init__(self, parent: Union[Instrument, InstrumentChannel]) -> None:
        """
        Creates a Time class and adds all relevant time-related parameters.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this Time class belongs.
        """

        # Initialize instrument channel.
        # Name is not variable because there can only be one time block.
        super().__init__(parent, "time")

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in Time._get_required_cluster_attr_names():
            self._register(attr_name)

        # Add parameters

        self.add_parameter(
            "status",
            label="Synchronization status",
            docstring="TBD",
            unit="",
            get_parser=str,
            get_cmd=self._get_timekeeping_status,
        )

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_cluster_attr_names() -> list:
        """
        Return list of parent attribute names that are required for the QCoDeS
        parameters to function, so that they can be registered to this object
        using the _register method.

        Returns
        ----------
        list
            List of parent attribute names to register.
        """

        # Time attributes
        attr_names = [
            "_adjust_timekeeping",
            "_arm_timekeeping_capture_slot",
            "_get_current_timestamp",
            "_get_timekeeping_capture_slot",
            "_get_timekeeping_status",
            "_sync_to_ntp",
        ]

        return attr_names

    # ------------------------------------------------------------------------
    def _register(self, attr_name: str) -> None:
        """
        Register parent attribute to this IO channel using functools.partial
        to pre-select the IO channel index. If the attribute does not exist in
        the parent class, a method that raises a `NotImplementedError`
        exception is registered instead. The docstring of the parent attribute
        is also copied to the registered attribute.

        Parameters
        ----------
        attr_name : str
            Attribute name of parent to register.
        """

        if hasattr(self.parent, attr_name):
            parent_attr = getattr(self.parent, attr_name)
            partial_doc = (
                "Note\n"
                + "----------\n"
                + "This method calls {1}.{0} using functools.partial "
                + "The docstring above is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func = partial_with_numpy_doc(parent_attr, end_with=partial_doc)
            setattr(self, attr_name, partial_func)
        else:

            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'{self.parent.name} does not have "{attr_name}" attribute.'
                )

            setattr(self, attr_name, raise_not_implemented_error)

    # ----------------------------------------------------------------------------
    @staticmethod
    def _convert_time_format(
        time_obj: Union[int, float, dict],
        from_format: str = "json",
        to_format: str = "s",
    ) -> Union[int, float, dict]:
        """
        Translates time from one format to another.

        Parameters
        ----------
        time_obj: Any
            Incoming timestamp in the format specified by from_format.
        from_format: str
            The source format; "s" for int/float seconds, "ns" for int/float nanoseconds,
            "raw" for the internal time format as an integer, or "json" for the JSON serialization
            (respecting max 64-bit integers and avoiding float rounding error).
        to_format: str
            The destination format. Same options as from_format.

        Returns
        ----------
        Union[int, float, dict]
            The converted timestamp, according to to_format.

        Raises
        ----------
        ValueError
            If one of the format strings is unknown.
        """

        NS_PER_S = 1000000000
        TICKS_PER_NS = 2048
        TICKS_PER_S = TICKS_PER_NS * NS_PER_S

        if from_format == "json":
            raw = int((time_obj["ns"] << 11) + time_obj["sub"])
        elif from_format == "s":
            raw = int(round(time_obj * TICKS_PER_S))
        elif from_format == "ns":
            raw = int(round(time_obj * TICKS_PER_NS))
        elif from_format == "raw":
            raw = int(round(time_obj))
        else:
            raise ValueError(f"Unknown source format {from_format}. Options are: s, ns, raw, json")

        if to_format == "raw":
            return raw
        elif to_format == "ns":
            return raw / TICKS_PER_NS
        elif to_format == "s":
            return raw / TICKS_PER_S
        elif to_format == "json":
            return {"ns": raw // TICKS_PER_NS, "sub": raw % TICKS_PER_NS}
        raise ValueError(f"Unknown destination format {to_format}. Options are: s, ns, raw, json")

    # ----------------------------------------------------------------------------
    def get_current(self, format: str = "s") -> Union[int, float]:
        """
        Gets current timestamp in the given format

        Parameters
        ----------
        format: str
             "s", "ns" or "raw". Defaults to "s"

        Returns
        ----------
        Union[int, float]
            Current timestamp in seconds.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        return self._convert_time_format(self._get_current_timestamp(), to_format=format)

    # ----------------------------------------------------------------------------
    def get_capture(self, slot: int, format: str = "s") -> Union[int, float]:
        """
        Gets latest available capture (if any) in the given format

        Parameters
        ----------
        slot: int
            Slot number
        format: str
             "s", "ns" or "raw". Defaults to "s"

        Returns
        ----------
        Union[int, float]
            Current timestamp in the requested format.

        Raises
        ----------
        ValueError
            If the given format is not contemplated
        """
        return self._convert_time_format(self._get_timekeeping_capture_slot(slot), to_format=format)

    # ----------------------------------------------------------------------------
    def adjust(self, format: str, amount: Union[int, float]) -> None:
        """
        Adjusts the current time

        Parameters
        ----------
        ...
        """
        return self._adjust_timekeeping(
            self._convert_time_format(time_obj=amount, from_format=format, to_format="json")
        )

    def arm(
        self,
        slot: int,
        channel: int,
        edge_polarity: Polarity = Polarity.RISING_EDGE,
        sync_ref: SyncRef = SyncRef.OFF,
    ) -> None:
        """
        Arms a time capture on the given slot and channel. Edge polarity (rising,
        falling) and whether to synchronize to the 10 MHz clock can also be
        specified

        Parameters
        ----------
        ...
        """
        return self._arm_timekeeping_capture_slot(slot, channel, int(edge_polarity), int(sync_ref))

    # ----------------------------------------------------------------------------
    def sync_ext_trigger(
        self,
        slot: int,
        channel: int,
        trigger_timestamp: Union[float, int] = 0,
        timeout: Union[float, int] = 1,
        format: str = "s",
        edge_polarity: Polarity = Polarity.RISING_EDGE,
        sync_ref: SyncRef = SyncRef.OFF,
    ) -> float:
        """
        Synchronize based on external trigger

        Parameters
        ----------
        slot: int
            Slot number
        channel: int
            Channel number (0-8)
        trigger_timestamp: Union[float, int]
            When the trigger pulse will be generated. Will be set to 0 as default.
        timeout: Union[float, int]
            How long to wait for a capture while synchronizing, expressed in the unit
            given by the format argument
        format: Time format used throughout this method

        Returns
        ----------
        float
            Capture timestamp in the given format (if any)

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        TimeoutError
            No capture completed in the given timeout.
        """

        t_trigger = self._convert_time_format(
            time_obj=trigger_timestamp, from_format=format, to_format="raw"
        )

        self._arm_timekeeping_capture_slot(slot, channel, int(edge_polarity), int(sync_ref))

        start_time = time.time()

        while time.time() - start_time < self._convert_time_format(
            timeout, from_format=format, to_format="s"
        ):
            try:
                t_capture = self._convert_time_format(
                    time_obj=self._get_timekeeping_capture_slot(slot), to_format="raw"
                )
                self.adjust(amount=t_trigger - t_capture, format="raw")
                return self._convert_time_format(
                    t_trigger - t_capture, from_format="raw", to_format=format
                )
            except Exception:  # noqa: PERF203
                time.sleep(0.001)  # Polling every 1 ms (0.001 seconds)
        print("No capture completed in the given timeout.")
        raise TimeoutError

    # ----------------------------------------------------------------------------
    def set_epoch(
        self,
        epoch: Union[float, int, str] = "unix",
        epoch_format: str = "s",
        authority: Optional[str] = None,
        pps: IOChannel = None,
    ) -> None:
        """
        Sets epoch

        Parameters
        ----------
        epoch: str
            unix vs now. unix:  CTC counter will be set to how many
            milliseconds (due to Linux time precision) had passed since
            00:00:00 on January 1, 1970  in the moment that the command is
            executed using CMM local system time.
            now: CTC counter will be set to 0.
        epoch_format: str
            s, ns or raw
        authority: str
            The IP of an NTP server
        pps: None vs moduleX.channel. If provided, it will wait for the PPS
            signal and send the adjust for all modules after doing setting the
            epoch using NTP

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        # Helpful units in the raw format.
        one_nanosecond = 2048
        one_second = one_nanosecond * 1000000000

        # Get current system time in raw timetag format.
        now = int(round(time.time() * one_second))

        # Desugar provided epoch value, relative to unix epoch.
        if epoch == "unix":
            epoch = 0
        elif epoch == "now":
            epoch = now
        if epoch_format == "s":
            epoch_seconds = int(round(epoch * one_second))
        elif epoch_format == "ns":
            epoch_nanoseconds = int(round(epoch * one_nanosecond))
        elif epoch_format == "raw":
            epoch = int(epoch)
        else:
            raise ValueError("Invalid epoch specification")

        # If we don"t have a time authority, we compute the adjustment in qblox-instruments.
        if authority is None:
            if pps is not None:
                raise ValueError("NTP server is needed for PPS-based adjustments")
            current_ctc = self.get_current(format="raw")
            desired_ctc = now - epoch
            self.adjust(amount=desired_ctc - current_ctc, format="raw")
            return
        else:
            # If we do have a time authority, the cluster must do the adjustment.
            # The user will use a specific IP and no DNS, this is just for testing
            # and will be removed
            self._sync_to_ntp(authority)
            # The CMM does this:
            #  - Query the given NTP server (authority is an IP address)
            #    for the time difference between the CMM system clock and the NTP time.
            #    Normally you would use this to adjust the system clock, but we don't
            #    do that here; the user could have a local NTP server that is not
            #    synced to UTC at all and we don't want to mess up our system time.
            #  - As quick as possible:
            #     - cur_ctc = read_ctc()
            #     - cur_system_time = read_system_time()
            #  - Adjust CTC by cur_system_time + ntp_adjustment - cur_ctc

        # The cluster will have used the unix epoch, so if the user wants a
        # different one, we need to adjust.
        if "epoch_seconds" in locals():
            self.adjust(amount=-epoch_seconds, format="raw")
        if "epoch_nanoseconds" in locals():
            self.adjust(amount=-epoch_nanoseconds, format="raw")

        # If no PPS signal is provided, this is the best we can do.
        if pps is None:
            return

        # Figure out channel information based on `pps` somehow.
        pps_slot = pps.parent.slot_idx
        pps_io = pps.io_channel_idx

        # Synchronize to the PPS signal.
        current_ctc = self.get_current(format="raw")

        # Figure out a CTC value that's in the future and is right in the middle
        # between two PPS pulses.
        sync_ctc = current_ctc
        sync_ctc -= current_ctc % one_second  # align to previous full second
        sync_ctc += one_second  # add one second so it's in the future
        sync_ctc += one_second // 2  # add half a second more to align to middle of a second

        # TO DO: Implement
        # Start a capture as soon as possible after sync_ctc.
        self.arm_timekeeping_capture_after(
            slot=pps_slot,
            source=pps_io,
            polarity=True,
            sync_ref=True,
            after=sync_ctc,
            after_format="raw",
        )
        # The module in the given slot does this:
        #  - Get the current CTC value and throw an exception if it is greater than
        #    or equal to `after` (because the arm deadline has been missed), or if
        #    `after` is more than 3 seconds after the current CTC value (because
        #    then it would take too long and network timeouts would become an issue).
        #  - Busy-wait until the current CTC value *is* greater than or equal to
        #    `after`.
        #  - Arm a timekeeping capture the same way the normal arm command would.
        # The module has to do this so there is minimal latency between the
        # busy-wait and arming the CTC capture. For PPS we technically have half a
        # second for it but still, network latency can be significant especially
        # over a VPN and whatnot.

        # We should now get a time capture nominally half a second after the arm
        # command was given, but *exactly* half a second after sync_cyc in the
        # desired time format.
        desired_ctc = sync_ctc + one_second // 2

        # It should take at most one second to do the capture.
        time.sleep(1)
        captured_ctc = self.get_capture(slot=pps_slot, format="raw")

        # Make the final adjustment.
        self.adjust(amount=desired_ctc - captured_ctc, format="raw")
