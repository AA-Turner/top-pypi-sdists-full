# ----------------------------------------------------------------------------
# Description    : QCM/QRM QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import math
from functools import partial
from typing import Any, Callable, Optional, Union

from qcodes import Instrument, InstrumentChannel, Parameter
from qcodes import validators as vals

from qblox_instruments import InstrumentType
from qblox_instruments.docstring_helpers import partial_with_numpy_doc
from qblox_instruments.qcodes_drivers.io_channel import IOChannel
from qblox_instruments.qcodes_drivers.io_pulse_channel import IOPulseChannel
from qblox_instruments.qcodes_drivers.quad import Quad
from qblox_instruments.qcodes_drivers.sequencer import Sequencer
from qblox_instruments.types import FrequencyParameter


# -- class -------------------------------------------------------------------
class Module(InstrumentChannel):
    """
    This class represents a QCM/QRM/QTM module. It combines all module specific
    parameters and functions into a single QCoDes InstrumentChannel.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Instrument,
        name: str,
        slot_idx: int,
    ) -> None:
        """
        Creates a QCM/QRM/QTM module class and adds all relevant parameters for
        the module.

        Parameters
        ----------
        parent : Instrument
            The QCoDeS class to which this module belongs.
        name : str
            Name of this module channel
        slot_idx : int
            The index of this module in the parent instrument, representing
            which module is controlled by this class.
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store sequencer index
        self._slot_idx = slot_idx

        MAX_NUM_LO = 2
        MAX_NUM_IN_CHANNELS = 4
        MAX_NUM_OUT_CHANNELS = 4
        MAX_NUM_MARKERS = 4
        for attr_name in Module._get_required_parent_qtm_attr_names():
            self._register(attr_name)
        for attr_name in Module._get_required_parent_qrx_qcm_attr_names(
            num_lo=MAX_NUM_LO,
            num_in_channels=MAX_NUM_IN_CHANNELS,
            num_out_channels=MAX_NUM_OUT_CHANNELS,
            num_markers=MAX_NUM_MARKERS,
        ):
            self._register(attr_name)

        for attr_name in Module._get_required_parent_qrc_attr_names():
            self._register(attr_name)

        # Add required parent attributes for the QCoDeS parameters to function
        try:
            self.parent._present_at_init(self.slot_idx)

        except KeyError:
            pass
        else:
            # CONSTANTS
            # These are some defaults that apply to QCM modules
            # TO DO: Refactor add_qcodes_params to make num_seq and num_dio
            # a constant too
            NUM_MARKERS = 4
            NUM_OUT_CHANNELS = 4
            NUM_IN_CHANNELS = 0
            NUM_SEQ = 6
            NUM_DIO = 0
            if self.is_qrm_type:
                NUM_OUT_CHANNELS = 2
                NUM_IN_CHANNELS = 2
            elif self.is_qrc_type:
                NUM_OUT_CHANNELS = 12
                NUM_MARKERS = 1
                NUM_IN_CHANNELS = 4
                NUM_SEQ = 12
            elif self.is_qtm_type:
                NUM_SEQ = 8
                NUM_DIO = 8

            # Add QCM/QRM/QTM/QDM/LINQ/QRC QCoDeS parameters
            if self.is_qrm_type or self.is_qcm_type or self.is_qtm_type or self.is_qrc_type:
                add_qcodes_params(
                    self,
                    num_seq=NUM_SEQ,
                    num_dio=NUM_DIO,
                    num_in_channels=NUM_IN_CHANNELS,
                    num_out_channels=NUM_OUT_CHANNELS,
                    num_markers=NUM_MARKERS,
                )
            if self.is_qrc_type:
                for channel in (2, 3, 4, 5):
                    self.parent._set_out_nyquist_filter(self.slot_idx, channel, "1")

        # Add module QCoDeS parameters
        self.add_parameter(
            "present",
            label="Module present status",
            docstring="Sets/gets module present status for slot {} in the Cluster.",
            unit="",
            vals=vals.Bool(),
            get_parser=bool,
            get_cmd=self._get_modules_present,
        )

        self.add_parameter(
            "connected",
            label="Module connected status",
            docstring="Gets module connected status for slot {} in the Cluster.",
            unit="",
            vals=vals.Bool(),
            get_parser=bool,
            get_cmd=self._get_modules_connected,
        )

    # ------------------------------------------------------------------------
    @property
    def slot_idx(self) -> int:
        """
        Get slot index.

        Returns
        ----------
        int
            Slot index
        """

        return self._slot_idx

    # ------------------------------------------------------------------------
    @property
    def module_type(self) -> InstrumentType:
        """
        Get module type (e.g. QRM, QCM).

        Returns
        ----------
        InstrumentType
            Module type

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._module_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qcm_type(self) -> bool:
        """
        Return if module is of type QCM.

        Returns
        ----------
        bool
            True if module is of type QCM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qcm_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qrm_type(self) -> bool:
        """
        Return if module is of type QRM.

        Returns
        ----------
        bool:
            True if module is of type QRM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qrm_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qtm_type(self) -> bool:
        """
        Return if module is of type QTM.

        Returns
        ----------
        bool:
            True if module is of type QTM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qtm_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qdm_type(self) -> bool:
        """
        Return if module is of type QDM.

        Returns
        ----------
        bool:
            True if module is of type QDM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qdm_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_eom_type(self) -> bool:
        """
        Return if module is of type EOM.

        Returns
        ----------
        bool:
            True if module is of type EOM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_eom_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_linq_type(self) -> bool:
        """
        Return if module is of type LINQ.

        Returns
        ----------
        bool:
            True if module is of type LINQ.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_linq_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qrc_type(self) -> bool:
        """
        Return if module is of type QRC.

        Returns
        ----------
        bool:
            True if module is of type QRC.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qrc_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_qsm_type(self) -> bool:
        """
        Return if module is of type QSM.

        Returns
        ----------
        bool:
            True if module is of type QSM.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_qsm_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def is_rf_type(self) -> bool:
        """
        Return if module is of type QCM-RF or QRM-RF.

        Returns
        ----------
        bool:
            True if module is of type QCM-RF or QRM-RF.

        Raises
        ----------
        KeyError
            Module is not available.
        """

        return self.parent._is_rf_type(self.slot_idx)

    # ------------------------------------------------------------------------
    @property
    def sequencers(self) -> list:
        """
        Get list of sequencers submodules.

        Returns
        ----------
        list
            List of sequencer submodules.
        """
        sequencers_list = [
            submodule for submodule in self.submodules.values() if "sequencer" in str(submodule)
        ]
        return sequencers_list

    # ------------------------------------------------------------------------
    @property
    def io_channels(self) -> list:
        """
        Get list of digital I/O channels.

        Returns
        ----------
        list
            List of digital I/O channels.
        """
        io_channels_list = [
            submodule for submodule in self.submodules.values() if "io_channel" in str(submodule)
        ]
        return io_channels_list

    # ------------------------------------------------------------------------
    @property
    def io_pulse_channels(self) -> list:
        """
        Get list of digital I/O Pulse channels.

        Returns
        ----------
        list
            List of digital I/O Pulse channels.
        """
        io_pulse_channels_list = [
            submodule
            for submodule in self.submodules.values()
            if "io_pulse_channel" in str(submodule)
        ]
        return io_pulse_channels_list

    # ------------------------------------------------------------------------
    @property
    def quads(self) -> list:
        """
        Get list of digital I/O quads.

        Returns
        ----------
        list
            List of digital I/O quads.
        """
        quads_list = [
            submodule for submodule in self.submodules.values() if "quad" in str(submodule)
        ]
        return quads_list

    @property
    def is_dummy(self) -> bool:
        return self.parent.is_dummy

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_parent_qrx_qcm_attr_names(
        num_lo: int, num_in_channels: int, num_out_channels: int, num_markers: int
    ) -> list:
        """
        Return list of parent attributes names that are required for the
        QCoDeS parameters to function which is common in for QRM/QCM/QRC,
        so that they can be registered to this
        object using the _register method.

        Returns
        ----------
        list
            List of parent attribute names to register.
        """

        attr_names = [
            # Module present attribute
            "_get_modules_present",
            "_get_modules_connected",
            # Channel map attributes
            "disconnect_outputs",
            "disconnect_inputs",
            "_iter_connections",
        ]

        # LO attributes
        for operation in ["set", "get"]:
            for idx in range(0, num_lo):
                attr_names += [
                    f"_{operation}_lo_freq_{idx}",
                    f"_{operation}_lo_pwr_{idx}",
                    f"_{operation}_lo_enable_{idx}",
                ]
        attr_names.append("_run_mixer_lo_calib")

        # Input attributes
        for operation in ["set", "get"]:
            for idx in range(0, num_in_channels):
                attr_names += [
                    f"_{operation}_in_amp_gain_{idx}",
                    f"_{operation}_in_offset_{idx}",
                ]
            for idx in range(0, num_in_channels // 2):
                attr_names.append(f"_{operation}_in_att_{idx}")

        # Output attributes
        for operation in ["set", "get"]:
            for idx in range(0, num_out_channels):
                attr_names += [
                    f"_{operation}_out_amp_offset_{idx}",
                    f"_{operation}_dac_offset_{idx}",
                ]
            for idx in range(0, num_out_channels // 2):
                attr_names += [
                    f"_{operation}_out_att_{idx}",
                    f"_{operation}_max_out_att_{idx}",
                ]

        # Marker attributes
        for operation in ["set", "get"]:
            for idx in range(0, num_markers):
                attr_names.append(f"_{operation}_mrk_inv_en_{idx}")

        # Scope acquisition attributes
        for operation in ["set", "get"]:
            attr_names += [
                f"_{operation}_acq_scope_config",
                f"_{operation}_acq_scope_config_val",
                f"_{operation}_pre_distortion_config_val",
            ]
        attr_names.append("_get_output_latency")

        # Sequencer program attributes
        attr_names += [
            "get_assembler_status",
            "get_assembler_log",
        ]

        # Sequencer attributes
        attr_names += Sequencer._get_required_parent_attr_names()

        return attr_names

    def _get_required_parent_qrc_attr_names() -> list:
        attr_names = [
            "_set_out_ch_comb_en",
            "_set_out_dsa_1",
            "_set_out_mix_dds",
            "_set_out_mix_x2",
            "_set_out_nyq_sel",
            "_set_out_out_sel",
            "_get_out_ch_comb_en",
            "_get_out_dsa_1",
            "_get_out_mix_dds",
            "_get_out_mix_x2",
            "_get_out_nyq_sel",
            "_get_out_out_sel",
            "_set_out_nyquist_filter",
            "_get_out_nyquist_filter",
            "_set_out_mixer_filter_bank",
            "_get_out_mixer_filter_bank",
            "_print_out_gpio_configuration",
            "_set_in_amp_iso_fw",
            "_set_in_ch_splt_en",
            "_set_in_dsa_1",
            "_set_in_dsa_2",
            "_set_in_mix_dds",
            "_set_in_mix_x2",
            "_set_in_nyq_sel",
            "_get_in_amp_iso_fw",
            "_get_in_ch_splt_en",
            "_get_in_dsa_1",
            "_get_in_dsa_2",
            "_get_in_mix_dds",
            "_get_in_mix_x2",
            "_get_in_nyq_sel",
            "_set_in_nyquist_filter",
            "_get_in_nyquist_filter",
            "_print_in_gpio_configuration",
            "_set_out_lo_frequency",
            "_set_out_lo_power",
            "_get_out_lo_power",
            "_init_out_lo",
            "_soft_sync_all_out_lo",
            "_power_down_out_lo_output",
            "_power_down_out_lo",
            "_set_out_att",
            "_get_out_att",
            "_set_in_att1",
            "_set_in_att2",
            "_get_in_att1",
            "_get_in_att2",
            "_get_max_out_att",
            "_set_out_freq",
            "_get_out_freq",
            "_set_output_mode",
            "_get_output_mode",
            "_set_input_mode",
            "_get_input_mode",
            "set_mixer_settings_freq_dac",
            "set_mixer_settings_coarse_delay_dac",
            "reset_duc_phase_dac",
            "set_rfdc_nyquist_zone",
            "set_inv_sync_filter",
            "set_dac_current",
            "set_decoder_mode",
        ]

        return attr_names

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_parent_qtm_attr_names() -> list:
        """
        Return list of parent attributes names that are required for the
        QCoDeS parameters to function for a QTM, so that the can be registered to this
        object using the _register method.

        Returns
        ----------
        list
            List of parent attribute names to register.
        """

        attr_names = [
            # Module present attribute
            "_get_modules_present",
            # Channel map attributes
            "_iter_connections",
            # Sequencer program attributes
            "get_assembler_status",
            "get_assembler_log",
            # Scope trigger logic
            "scope_trigger_arm",
        ]

        # Sequencer attributes
        attr_names += Sequencer._get_required_parent_attr_names()
        attr_names += IOChannel._get_required_parent_attr_names()
        attr_names += IOPulseChannel._get_required_parent_attr_names()
        attr_names += Quad._get_required_parent_attr_names()

        return attr_names

    # ------------------------------------------------------------------------
    def _register(self, attr_name: str) -> None:
        """
        Register parent attribute to this sequencer using functools.partial to
        pre-select the slot index. If the attribute does not exist in the
        parent class, a method that raises a `NotImplementedError` exception
        is registered instead. The docstring of the parent attribute is also
        copied to the registered attribute.

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
                + "This method calls {1}.{0} using functools.partial to set the "
                + "slot index. The docstring above is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func = partial_with_numpy_doc(parent_attr, self.slot_idx, end_with=partial_doc)
            setattr(self, attr_name, partial_func)
        else:

            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'{self.parent.name} does not have "{attr_name}" attribute.'
                )

            setattr(self, attr_name, raise_not_implemented_error)

    # ------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(self, sequencer: Optional[int] = None) -> None:
        """
        Marks the cache of all QCoDeS parameters in the module, including in
        any sequencers the module might have, as invalid. Optionally,
        a sequencer can be specified. This will invalidate the cache of that
        sequencer only in stead of all parameters.

        Parameters
        ----------
        sequencer : Optional[int]
            Sequencer index of sequencer for which to invalidate the QCoDeS
            parameters.
        """

        invalidate_qcodes_parameter_cache(self, sequencer)

    # ------------------------------------------------------------------------
    def __getitem__(self, key: str) -> Union[InstrumentChannel, Parameter, Callable[..., Any]]:
        """
        Get sequencer or parameter using string based lookup.

        Parameters
        ----------
        key : str
            Sequencer, parameter or function to retrieve.

        Returns
        ----------
        Union[InstrumentChannel, Parameter, Callable[..., Any]]
            Sequencer, parameter or function.

        Raises
        ----------
        KeyError
            Sequencer, parameter or function does not exist.
        """

        return get_item(self, key)


# -- functions ---------------------------------------------------------------


def add_qcodes_params(
    parent: Union[Instrument, Module],
    num_seq: int,
    num_dio: int,
    num_in_channels: int,
    num_out_channels: int,
    num_markers: int,
) -> None:
    """
    Add all QCoDeS parameters for a single QCM/QRM module.

    Parameters
    ----------
    parent : Union[Instrument, Module]
        Parent object to which the parameters need to be added.
    num_seq : int
        Number of sequencers to add as submodules.
    num_dio: int
        Number of DIO units. Applies to QTM
    num_in_channels:
        Number of input channels. Does not apply to QTM since its channels are in/out
    num_out_channels: int
        Number of output channels. Does not apply to QTM since its channels are in/out
    num_markers: int
        Number of markers.
    """

    if parent.is_rf_type:
        num_out = num_out_channels // 2
        num_in = num_in_channels // 2
    else:
        num_out = num_out_channels
        num_in = num_in_channels

    # -- LO frequencies (RF-modules only) ------------------------------------
    if parent.is_rf_type:
        if parent.is_qrm_type:
            parent.add_parameter(
                "out0_in0_lo_freq_cal_type_default",
                label="Default automatic mixer calibration setting",
                docstring="Sets/gets the Default automatic mixer"
                "calibration while setting local oscillator"
                "frequency for output and input 0.",
                unit="Hz",
                vals=vals.Enum("off", "lo only", "lo and sidebands"),
                set_cmd=None,
                get_cmd=None,
                initial_value="off",
            )

            out0_in0_lo_freq = Parameter(
                "_out0_in0_lo_freq",
                label="Local oscillator frequency",
                docstring="Sets/gets the local oscillator frequency for output 0 and input 0.",
                unit="Hz",
                vals=vals.Numbers(2e9, 18e9),
                set_parser=int,
                get_parser=int,
                set_cmd=parent._set_lo_freq_1,
                get_cmd=parent._get_lo_freq_1,
            )

            parent.add_parameter(
                "out0_in0_lo_freq",
                parameter_class=FrequencyParameter,
                source=out0_in0_lo_freq,
                calibration_function=partial(_calibrate_lo, parent, 1),
            )

            parent.out0_in0_lo_cal = partial(parent._run_mixer_lo_calib, 1)
        elif parent.is_qcm_type:
            parent.add_parameter(
                "out0_lo_freq_cal_type_default",
                label="Default automatic mixer calibration setting",
                docstring="Sets/gets the Default automatic mixer"
                "calibration while setting local oscillator"
                "frequency for output 0.",
                unit="Hz",
                vals=vals.Enum("off", "lo only", "lo and sidebands"),
                set_cmd=None,
                get_cmd=None,
                initial_value="off",
            )

            out0_lo_freq = Parameter(
                "_out0_lo_freq",
                label="Output 0 local oscillator frequency",
                docstring="Sets/gets the local oscillator frequency for output 0.",
                unit="Hz",
                vals=vals.Numbers(2e9, 18e9),
                set_parser=int,
                get_parser=int,
                set_cmd=parent._set_lo_freq_0,
                get_cmd=parent._get_lo_freq_0,
            )

            parent.add_parameter(
                "out0_lo_freq",
                parameter_class=FrequencyParameter,
                source=out0_lo_freq,
                calibration_function=partial(_calibrate_lo, parent, 0),
            )

            parent.out0_lo_cal = partial(parent._run_mixer_lo_calib, 0)

            parent.add_parameter(
                "out1_lo_freq_cal_type_default",
                label="Default automatic mixer calibration setting",
                docstring="Sets/gets the Default automatic mixer"
                "calibration while setting local oscillator"
                "frequency for output 1.",
                unit="Hz",
                vals=vals.Enum("off", "lo only", "lo and sidebands"),
                set_cmd=None,
                get_cmd=None,
                initial_value="off",
            )

            out1_lo_freq = Parameter(
                "out1_lo_freq",
                label="Output 1 local oscillator frequency",
                docstring="Sets/gets the local oscillator frequency for output 1.",
                unit="Hz",
                vals=vals.Numbers(2e9, 18e9),
                set_parser=int,
                get_parser=int,
                set_cmd=parent._set_lo_freq_1,
                get_cmd=parent._get_lo_freq_1,
            )

            parent.add_parameter(
                "out1_lo_freq",
                parameter_class=FrequencyParameter,
                source=out1_lo_freq,
                calibration_function=partial(_calibrate_lo, parent, 1),
            )

            parent.out1_lo_cal = partial(parent._run_mixer_lo_calib, 1)
        elif parent.is_qrc_type:
            # mapping from output channel to DAC tile and block
            output_mapping = {
                2: (3, 2),
                3: (2, 0),
                4: (2, 2),
                5: (3, 0),
            }

            def _set_output_freq(channel, freq) -> None:
                tile, block = output_mapping[channel]
                parent.parent._set_mixer_settings_freq_dac(
                    parent.slot_idx, tile, block, int(freq / 1e6)
                )
                parent.parent._sync_dac(
                    parent.slot_idx, 0xF, -1
                )  # run MTS on all 4 DAC Tiles (0xF) with minimal delay (-1)
                parent.parent._sync_adc(
                    parent.slot_idx, 0xF, -1
                )  # run MTS on all 4 ADCs Tiles (0xF) with minimal delay (-1)
                parent.parent._reset_duc_phase_all(
                    parent.slot_idx
                )  # sync all DUC, DDC phases to 10 MHz clock

            for channel in output_mapping:
                parent.add_parameter(
                    f"out{channel}_freq",
                    label=f"Output {channel} frequency",
                    docstring=(f"Sets/gets output {channel} frequency."),
                    initial_cache_value=1e9,
                    unit="Hz",
                    # For the beta release only DDS path with nyquist zone 1 is allowed.
                    vals=vals.Numbers(0.5e9, 1.7e9),
                    set_cmd=partial(_set_output_freq, channel),
                )

            input_mapping = {
                0: (3, 0),
                1: (2, 0),
            }

            def _set_input_freq(channel, freq) -> None:
                tile, block = input_mapping[channel]
                parent.parent._set_mixer_settings_freq_adc(
                    parent.slot_idx, tile, block, int(-freq / 1e6)
                )
                parent.parent._set_adc_dsa(parent.slot_idx, tile, block, 0.0)
                parent.parent._reset_duc_phase_all(
                    parent.slot_idx
                )  # sync all DUC, DDC phases to 10 MHz clock

            for channel in input_mapping:
                parent.add_parameter(
                    f"in{channel}_freq",
                    label=f"Output {channel} frequency",
                    docstring=(f"Sets/gets output {channel} frequency."),
                    initial_cache_value=1e9,
                    unit="Hz",
                    # For the beta release only DDS path with nyquist zone 1 is allowed.
                    vals=vals.Numbers(0.5e9, 1.7e9),
                    set_cmd=partial(_set_input_freq, channel),
                )

    # -- LO enables (RF-modules only) ----------------------------------------
    if parent.is_rf_type:
        if parent.is_qrm_type:
            parent.add_parameter(
                "out0_in0_lo_en",
                label="Local oscillator enable",
                docstring="Sets/gets the local oscillator enable for output 0 and input 0.",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=parent._set_lo_enable_1,
                get_cmd=parent._get_lo_enable_1,
            )
        elif parent.is_qcm_type:
            for i, set_lo_enable, get_lo_enable in zip(
                range(num_out),
                [f"_set_lo_enable_{n}" for n in range(num_out)],
                [f"_get_lo_enable_{n}" for n in range(num_out)],
            ):
                parent.add_parameter(
                    f"out{i}_lo_en",
                    label=f"Output {i} local oscillator enable",
                    docstring="Sets/gets the local oscillator enable for output {i}.",
                    vals=vals.Bool(),
                    set_parser=bool,
                    get_parser=bool,
                    set_cmd=getattr(parent, set_lo_enable),
                    get_cmd=getattr(parent, get_lo_enable),
                )

    # -- Attenuation settings (RF-modules only) ------------------------------
    if parent.is_rf_type:
        if parent.is_qrm_type:
            parent.add_parameter(
                "in0_att",
                label="Input 0 attenuation",
                docstring=(
                    "Sets/gets input attenuation in a range of 0dB to 30dB with a resolution "
                    "of 2dB per step."
                ),
                unit="dB",
                vals=vals.Multiples(2, min_value=0, max_value=30),
                set_parser=int,
                get_parser=int,
                set_cmd=parent._set_in_att_0,
                get_cmd=parent._get_in_att_0,
            )

        if parent.is_qcm_type or parent.is_qrm_type:
            for x in range(0, num_out):
                max_att = getattr(parent, f"_get_max_out_att_{x}")()
                parent.add_parameter(
                    f"out{x}_att",
                    label=f"Output {x} attenuation",
                    docstring="Sets/gets output attenuation in a range of 0 dB to "
                    f"{max_att} dB with a resolution of 2dB per step.",
                    unit="dB",
                    vals=vals.Multiples(
                        2,
                        min_value=0,
                        max_value=max_att,
                    ),
                    set_parser=int,
                    get_parser=int,
                    set_cmd=getattr(parent, f"_set_out_att_{x}"),
                    get_cmd=getattr(parent, f"_get_out_att_{x}"),
                )
        elif parent.is_qrc_type:
            # Getters are currently not implemented for QRC attenuation.
            # Indexing of the channels start from 1 instead of 0
            # for QRC output attenuation on the SCPI layer.
            for channel in range(0, num_out):
                parent.add_parameter(
                    f"out{channel}_att",
                    label=f"Output {channel} attenuation",
                    docstring=(
                        f"Sets/gets output attenuation in steps of 0.5 dB "
                        f"from 0 dB to {parent._get_max_out_att(channel)}."
                    ),
                    unit="dB",
                    vals=vals.Numbers(
                        min_value=0.0,
                        max_value=parent._get_max_out_att(channel),
                    ),
                    set_parser=float,
                    get_parser=float,
                    set_cmd=partial(parent._set_out_att, channel),
                    get_cmd=partial(parent._get_out_att, channel),
                )

    # -- Input gain (AWG baseband modules only) ------------------------------
    if not parent.is_rf_type:
        for i, set_in_amp_gain, get_in_amp_gain in zip(
            range(num_in),
            [f"_set_in_amp_gain_{n}" for n in range(num_in)],
            [f"_get_in_amp_gain_{n}" for n in range(num_in)],
        ):
            parent.add_parameter(
                f"in{i}_gain",
                label=f"Input {i} gain",
                docstring=(
                    f"Sets/gets input {i} gain in a range of -6dB to 26dB with a resolution "
                    f"of 1dB per step."
                ),
                unit="dB",
                vals=vals.Numbers(-6, 26),
                set_parser=int,
                get_parser=int,
                set_cmd=getattr(parent, set_in_amp_gain),
                get_cmd=getattr(parent, get_in_amp_gain),
            )

    # -- Input offset (AWG modules only) ------------------------------
    if parent.is_qrm_type:
        for i, set_in_offset, get_in_offset in zip(
            range(num_in_channels),
            [f"_set_in_offset_{n}" for n in range(num_in_channels)],
            [f"_get_in_offset_{n}" for n in range(num_in_channels)],
        ):
            if parent.is_rf_type:
                parent.add_parameter(
                    f"in{i // 2}_offset_path{i % 2}",
                    label=f"Input 0 offset for path {i}",
                    docstring="Sets/gets input 0 offset for path 0 in a range of -0.09V to 0.09V",
                    unit="V",
                    vals=vals.Numbers(-0.09, 0.09),
                    set_parser=float,
                    get_parser=float,
                    set_cmd=getattr(parent, set_in_offset),
                    get_cmd=getattr(parent, get_in_offset),
                )
            else:
                parent.add_parameter(
                    f"in{i}_offset",
                    label=f"Input {i} offset",
                    docstring=f"Sets/gets input {i} offset in a range of -0.09V to 0.09V",
                    unit="V",
                    vals=vals.Numbers(-0.09, 0.09),
                    set_parser=float,
                    get_parser=float,
                    set_cmd=getattr(parent, set_in_offset),
                    get_cmd=getattr(parent, get_in_offset),
                )

    # -- Output offsets (All modules) ----------------------------------------
    if parent.is_rf_type and not parent.is_qrc_type:
        for i, set_out_amp_offset, get_out_amp_offset in zip(
            range(num_out_channels),
            [f"_set_out_amp_offset_{n}" for n in range(num_out_channels)],
            [f"_get_out_amp_offset_{n}" for n in range(num_out_channels)],
        ):
            out = i // 2
            path = i % 2
            parent.add_parameter(
                f"out{out}_offset_path{path}",
                label=f"Output {out} offset for path {path}",
                docstring=f"Sets/gets output 0 offset for path {path}.",
                unit="mV",
                vals=vals.Numbers(-84.0, 73.0),
                set_parser=float,
                get_parser=float,
                set_cmd=getattr(parent, set_out_amp_offset),
                get_cmd=getattr(parent, get_out_amp_offset),
            )

    elif parent.is_qrm_type or parent.is_qcm_type:
        for i, set_dac_offset, get_dac_offset in zip(
            range(num_out_channels),
            [f"_set_dac_offset_{n}" for n in range(num_out_channels)],
            [f"_get_dac_offset_{n}" for n in range(num_out_channels)],
        ):
            parent.add_parameter(
                f"out{i}_offset",
                label=f"Output {i} offset",
                docstring=f"Sets/gets output {i} offset",
                unit="V",
                vals=(vals.Numbers(-2.5, 2.5) if parent.is_qcm_type else vals.Numbers(-0.5, 0.5)),
                set_parser=float,
                get_parser=float,
                set_cmd=getattr(parent, set_dac_offset),
                get_cmd=getattr(parent, get_dac_offset),
            )

    # -- Scope acquisition settings (QRM modules only) -----------------------
    if parent.is_qrm_type or parent.is_qrc_type:
        for x in range(0, num_in_channels):
            parent.add_parameter(
                f"scope_acq_trigger_mode_path{x}",
                label=f"Scope acquisition trigger mode for input path {x}",
                docstring=(
                    f"Sets/gets scope acquisition trigger mode for input path {x} "
                    f"('sequencer' = triggered by sequencer, 'level' = triggered by input level)."
                ),
                unit="",
                vals=vals.Bool(),
                val_mapping={"level": True, "sequencer": False},
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(parent._set_acq_scope_config_val, ["trig", "mode_path", x]),
                get_cmd=partial(parent._get_acq_scope_config_val, ["trig", "mode_path", x]),
            )

            parent.add_parameter(
                f"scope_acq_trigger_level_path{x}",
                label=f"Scope acquisition trigger level for input path {x}",
                docstring=(
                    f"Sets/gets scope acquisition trigger level when using input level "
                    f"trigger mode for input path {x}."
                ),
                unit="",
                vals=vals.Numbers(-1.0, 1.0),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(parent._set_acq_scope_config_val, ["trig", "lvl_path", x]),
                get_cmd=partial(parent._get_acq_scope_config_val, ["trig", "lvl_path", x]),
            )

            parent.add_parameter(
                f"scope_acq_avg_mode_en_path{x}",
                label=f"Scope acquisition averaging mode enable for input path {x}",
                docstring=f"Sets/gets scope acquisition averaging mode enable for input path {x}.",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=partial(parent._set_acq_scope_config_val, ["avg_en_path", x]),
                get_cmd=partial(parent._get_acq_scope_config_val, ["avg_en_path", x]),
            )

        scope_acq_sequencer_param_args = dict(
            name="scope_acq_sequencer_select",
            label="Scope acquisition sequencer select",
            docstring="Sets/gets sequencer select that specifies which "
            "sequencer triggers the scope acquisition when using "
            "sequencer trigger mode.",
            unit="",
            vals=vals.Numbers(0, num_seq - 1),
            set_parser=int,
            get_parser=int,
            get_cmd=partial(parent._get_acq_scope_config_val, "sel_acq"),
        )

        if parent.is_qrc_type:

            def _set_qrc_scope_sequencer(seq: int) -> None:
                parent._set_acq_scope_config_val("sel_acq", seq)
                for ch in range(num_in_channels):
                    parent._set_acq_scope_config_val(["sel_path", ch], seq)

            scope_acq_sequencer_param_args["set_cmd"] = _set_qrc_scope_sequencer
        else:
            scope_acq_sequencer_param_args["set_cmd"] = partial(
                parent._set_acq_scope_config_val, "sel_acq"
            )

        parent.add_parameter(**scope_acq_sequencer_param_args)

    # -- Marker settings (All modules, only 2 markers for RF modules) --------
    if parent.is_qcm_type or parent.is_qrm_type:
        num_markers_inv_en = 2 if parent.is_rf_type else num_markers
        for x in range(num_markers_inv_en):
            parent.add_parameter(
                f"marker{x}_inv_en",
                label=f"Output {x} marker invert enable",
                docstring=f"Sets/gets output {x} marker invert enable",
                unit="",
                vals=vals.Bool(),
                set_parser=bool,
                get_parser=bool,
                set_cmd=getattr(parent, f"_set_mrk_inv_en_{x}"),
                get_cmd=getattr(parent, f"_get_mrk_inv_en_{x}"),
            )

    # -- Pre-distortion configuration settings
    # Only QCMs and QRMs have predistortions for now
    if parent.is_qcm_type or parent.is_qrm_type or parent.is_qrc_type:
        _add_rtp_qcodes_params(parent, num_out=num_out, num_markers=num_markers)

    # Add sequencers
    for seq_idx in range(0, num_seq):
        seq = Sequencer(parent, f"sequencer{seq_idx}", seq_idx)
        parent.add_submodule(f"sequencer{seq_idx}", seq)

    # Add dio-related components
    for dio_idx in range(0, num_dio):
        io_channel = IOChannel(parent, f"io_channel{dio_idx}", dio_idx)
        parent.add_submodule(f"io_channel{dio_idx}", io_channel)
    for quad_idx in range(0, int(math.ceil(num_dio / 4))):
        quad = Quad(parent, f"quad{quad_idx}", quad_idx)
        parent.add_submodule(f"quad{quad_idx}", quad)

    # Add QTM-Pulse components
    if parent.is_eom_type:
        # For now QTM pulse only have 1 output
        io_pulse_channel = IOPulseChannel(parent, "io_pulse_channel0", 0)
        parent.add_submodule("io_pulse_channel", io_pulse_channel)


# ----------------------------------------------------------------------------
def invalidate_qcodes_parameter_cache(
    parent: Union[Instrument, Module],
    sequencer: Optional[int] = None,
    quad: Optional[int] = None,
    io_channel: Optional[int] = None,
    io_pulse_channel: Optional[int] = None,
) -> None:
    """
    Marks the cache of all QCoDeS parameters in the module as invalid,
    including in any sequencer submodules the module might have. Optionally,
    a sequencer can be specified. This will invalidate the cache of that
    sequencer only in stead of all parameters.

    Parameters
    ----------
    parent : Union[Instrument, Module]
        The parent module object for which to invalidate the QCoDeS parameters.
    sequencer : Optional[int]
        The sequencer index for which to invalidate the QCoDeS parameters.
    quad : Optional[int]
        The quad index for which to invalidate the QCoDeS parameters.
    io_channel : Optional[int]
        The IO channel index for which to invalidate the QCoDeS parameters.
    """

    # Invalidate module parameters
    if sequencer is None:
        for param in parent.parameters.values():
            param.cache.invalidate()
        sequencer_list = parent.sequencers
    else:
        sequencer_list = [parent.sequencers[sequencer]]

    quad_list = parent.quads if quad is None else [parent.quads[quad]]

    io_channel_list = parent.io_channels if io_channel is None else [parent.io_channels[io_channel]]

    if io_pulse_channel is None:
        io_pulse_channel_list = parent.io_pulse_channels
    else:
        io_pulse_channel_list = [parent.io_pulse_channels[io_pulse_channel]]

    # Invalidate sequencer parameters
    for seq in sequencer_list:
        seq._invalidate_qcodes_parameter_cache()
    for q in quad_list:
        q._invalidate_qcodes_parameter_cache()
    for io_ch in io_channel_list:
        io_ch._invalidate_qcodes_parameter_cache()
    for io_pulse_ch in io_pulse_channel_list:
        io_pulse_ch._invalidate_qcodes_parameter_cache()


# ----------------------------------------------------------------------------
def get_item(
    parent: Union[Instrument, Module], key: str
) -> Union[InstrumentChannel, Parameter, Callable[[Any], Any]]:
    """
    Get submodule or parameter using string based lookup.

    Parameters
    ----------
    parent : Union[Instrument, Module]
        Parent module object to search.
    key : str
        submodule, parameter or function to retrieve.

    Returns
    ----------
    Union[InstrumentChannel, Parameter, Callable[[Any], Any]]
        Submodule, parameter or function.

    Raises
    ----------
    KeyError
        Submodule, parameter or function does not exist.
    """

    # Check for submodule
    try:
        return parent.submodules[key]
    except KeyError:
        try:
            return parent.parameters[key]
        except KeyError:
            return parent.functions[key]


# ----------------------------------------------------------------------------
def _add_rtp_qcodes_params(parent: Union[Instrument, Module], num_out, num_markers) -> None:
    NUM_IIR = 4

    if not parent.is_qcm_type and not parent.is_qrm_type and not parent.is_qrc_type:
        raise TypeError("RTP parameters can only be declared for QRC, QRM and QCM modules.")
    predistortion_val_mapping_filter = {
        "bypassed": "disabled",
        "delay_comp": "enabled",
    }
    predist_mapping_docstring = (
        "If 'bypassed', the filter is disabled.\n"
        "If 'delay_comp', the filter is bypassed, but the output is delayed as if it were applied."
    )

    def add_distortion_parameters(output) -> None:
        parent.add_parameter(
            f"out{output}_fir_coeffs",
            label=f"Coefficients for the FIR filter for output {output}",
            docstring=f"Sets/gets the coefficients for the FIR filter for output {output}",
            unit="",
            vals=vals.Sequence(elt_validator=vals.Numbers(-2, 1.99), length=32),
            set_cmd=partial(
                parent._set_pre_distortion_config_val,
                [f"out{output}", "FIR", "stage0"],
            ),
            get_cmd=partial(
                parent._get_pre_distortion_config_val,
                [f"out{output}", "FIR", "stage0"],
            ),
        )
        for i in range(NUM_IIR):
            parent.add_parameter(
                f"out{output}_exp{i}_time_constant",
                label=f"Time constant of the exponential overshoot filter {i} for output {output}",
                docstring=(
                    f"Sets/gets the time constant of the exponential overshoot filter {i} "
                    f"for output {output}"
                ),
                unit="",
                vals=vals.Numbers(6, float("inf")),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(
                    parent._set_pre_distortion_config_val,
                    [f"out{output}", "IIR", f"stage{i}", "tau"],
                ),
                get_cmd=partial(
                    parent._get_pre_distortion_config_val,
                    [f"out{output}", "IIR", f"stage{i}", "tau"],
                ),
            )
            parent.add_parameter(
                f"out{output}_exp{i}_amplitude",
                label=f"Amplitude of the exponential overshoot filter {i} for output {output}",
                docstring=(
                    f"Sets/gets the amplitude of the exponential overshoot filter {i} "
                    f"for output {output}"
                ),
                unit="",
                vals=vals.Numbers(-1, 1),
                set_parser=float,
                get_parser=float,
                set_cmd=partial(
                    parent._set_pre_distortion_config_val,
                    [f"out{output}", "IIR", f"stage{i}", "amp"],
                ),
                get_cmd=partial(
                    parent._get_pre_distortion_config_val,
                    [f"out{output}", "IIR", f"stage{i}", "amp"],
                ),
            )

    def add_output_parameters(output) -> None:
        parent.add_parameter(
            f"out{output}_latency",
            label=f"Gets the latency in output path {output}",
            docstring=(
                f"Gets the latency in output path {output}.\n"
                "The output path can change depending on the filter configuration of the output."
            ),
            unit="s",
            set_cmd=False,
            get_cmd=partial(
                parent._get_output_latency,
                2 * output if parent.is_rf_type else output,
            ),
        )
        if parent.is_rf_type:
            parent.add_parameter(
                f"out{output}_fir_config",
                label=f"Configuration of FIR filter for output {output}",
                docstring=(
                    f"Sets/gets the configuration of FIR filter for output {output}."
                    f"\n{predist_mapping_docstring}"
                ),
                unit="",
                val_mapping=predistortion_val_mapping_filter,
                set_cmd=partial(
                    lambda output, val: parent.parent._set_pre_distortion_config(
                        parent.slot_idx,
                        {
                            f"out{2 * output}": {"state": {"stage5": val}},
                            f"out{2 * output + 1}": {"state": {"stage5": val}},
                        },
                    ),
                    output,
                ),
                get_cmd=partial(
                    parent._get_pre_distortion_config_val,
                    [f"out{output}", "state", "stage5"],
                ),
            )
            for i in range(NUM_IIR):
                parent.add_parameter(
                    f"out{output}_exp{i}_config",
                    label=f"Configuration of exponential overshoot filter {i} for output {output}",
                    docstring=(
                        f"Sets/gets configuration of exponential overshoot filter {i} "
                        f"for output {output}.\n{predist_mapping_docstring}"
                    ),
                    unit="",
                    val_mapping=predistortion_val_mapping_filter,
                    set_cmd=partial(
                        lambda output,
                        val,
                        stage_idx=i + 1: parent.parent._set_pre_distortion_config(
                            parent.slot_idx,
                            {
                                f"out{2 * output}": {"state": {f"stage{stage_idx}": val}},
                                f"out{2 * output + 1}": {"state": {f"stage{stage_idx}": val}},
                            },
                        ),
                        output,
                    ),
                    get_cmd=partial(
                        parent._get_pre_distortion_config_val,
                        [f"out{2 * output}", "state", f"stage{i + 1}"],
                    ),
                )
        else:
            parent.add_parameter(
                f"out{output}_fir_config",
                label=f"Configuration of FIR filter for output {output}",
                docstring=(
                    f"Sets/gets the configuration of FIR filter for output {output}.\n"
                    f"{predist_mapping_docstring}"
                ),
                unit="",
                val_mapping=predistortion_val_mapping_filter,
                set_cmd=partial(
                    parent._set_pre_distortion_config_val,
                    [f"out{output}", "state", "stage5"],
                ),
                get_cmd=partial(
                    parent._get_pre_distortion_config_val,
                    [f"out{output}", "state", "stage5"],
                ),
            )
            for i in range(NUM_IIR):
                parent.add_parameter(
                    f"out{output}_exp{i}_config",
                    label=f"Configuration of exponential overshoot filter {i} for output {output}",
                    docstring=(
                        f"Sets/gets configuration of exponential overshoot filter {i} "
                        f"for output {output}.\n{predist_mapping_docstring}"
                    ),
                    unit="",
                    val_mapping=predistortion_val_mapping_filter,
                    set_cmd=partial(
                        parent._set_pre_distortion_config_val,
                        [f"out{output}", "state", f"stage{i + 1}"],
                    ),
                    get_cmd=partial(
                        parent._get_pre_distortion_config_val,
                        [f"out{output}", "state", f"stage{i + 1}"],
                    ),
                )

    def add_marker_parameters(x) -> None:
        parent.add_parameter(
            f"marker{x}_fir_config",
            label=f"Delay compensation config for the FIR filter on marker {x}",
            docstring=(
                f"Delay compensation config for the FIR filter on marker {x}. If 'bypassed', "
                f"the marker is not delayed. If 'enabled', the marker is delayed."
            ),
            unit="",
            val_mapping=predistortion_val_mapping_marker,
            set_cmd=partial(
                parent._set_pre_distortion_config_val,
                [f"out{x}", "markers", "state", "stage5"],
            ),
            get_cmd=partial(
                parent._get_pre_distortion_config_val,
                [f"out{x}", "markers", "state", "stage5"],
            ),
        )
        for i in range(NUM_IIR):
            parent.add_parameter(
                f"marker{x}_exp{i}_config",
                label=(
                    f"Delay compensation config for the exponential overshoot filter {i} "
                    f"on marker {x}"
                ),
                docstring=(
                    f"Delay compensation config for the exponential overshoot filter {i} "
                    f"on marker {x}. If 'bypassed', the marker is not delayed. If 'enabled', "
                    f"the marker is delayed."
                ),
                unit="",
                val_mapping=predistortion_val_mapping_marker,
                set_cmd=partial(
                    parent._set_pre_distortion_config_val,
                    [f"out{x}", "markers", "state", f"stage{i + 1}"],
                ),
                get_cmd=partial(
                    parent._get_pre_distortion_config_val,
                    [f"out{x}", "markers", "state", f"stage{i + 1}"],
                ),
            )

    if not parent.is_rf_type:
        if parent.is_qcm_type:
            predist_mapping_docstring += "\nIf 'enabled', the filter is enabled."
            predistortion_val_mapping_filter["enabled"] = "enabled"
            predistortion_val_mapping_filter["delay_comp"] = "comp_delay"

        for output in range(num_out):
            add_output_parameters(output)
            if parent.is_qcm_type:
                add_distortion_parameters(output)
    else:
        for output in range(num_out):
            add_output_parameters(output)

    predistortion_val_mapping_marker = {
        "bypassed": "disabled",
        "delay_comp": "enabled",
    }

    for x in range(num_markers):
        add_marker_parameters(x)


# ----------------------------------------------------------------------------
def _calibrate_lo(
    parent: Union[Instrument, Module],
    output: int,
    cal_type: Optional[str] = None,
) -> None:
    """
    Calibrate the mixer according to the calibration type.

    Parameters
    ----------
    parent : Union[Instrument, Module]
        Parent module object to search.
    output : str
        Output of the module.
    cal_type : Optional[str]
        Automatic mixer calibration to perform after
        setting the frequency. Can be one of
        'off', 'lo only' or 'lo and sidebands'.

    Raises
    ----------
    ValueError
        cal_type is not one of
        'off', 'lo only' or 'lo and sidebands'.
    """
    if cal_type is None:
        if parent.is_qrm_type:
            cal_type = parent.out0_in0_lo_freq_cal_type_default()
        else:
            cal_type = parent.parameters[f"out{output}_lo_freq_cal_type_default"]()
    if cal_type == "lo only":
        parent._run_mixer_lo_calib(output)
        return
    elif cal_type == "lo and sidebands":
        if parent.is_qrm_type:
            connected_sequencers = [
                sequencer
                for sequencer in parent.sequencers
                if sequencer.parameters["connect_out0"]() == "IQ"
            ]
        else:
            connected_sequencers = [
                sequencer
                for sequencer in parent.sequencers
                if (
                    sequencer.parameters[f"connect_out{output}"]() == "IQ"
                    and sequencer.parameters[f"connect_out{(output + 1) % 2}"]() == "off"
                )
            ]
        parent._run_mixer_lo_calib(output)
        for sequencer in connected_sequencers:
            sequencer.sideband_cal()
        return
    if cal_type != "off":
        raise ValueError("cal_type must be one of 'off', 'lo only' or 'lo and sidebands'.")
