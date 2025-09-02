# ----------------------------------------------------------------------------
# Description    : IOChannel QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------

# -- include -----------------------------------------------------------------

from functools import partial
from typing import Final, Union

from qcodes import Instrument, InstrumentChannel
from qcodes import validators as vals

from qblox_instruments.docstring_helpers import partial_with_numpy_doc
from qblox_instruments.qcodes_drivers.component import Component
from qblox_instruments.qcodes_drivers.truth_table import TruthTable

# -- class -------------------------------------------------------------------


class IOChannel(Component):
    """
    This class represents a single IO channel. It combines all IO channel
    specific parameters and functions into a single QCoDes InstrumentChannel.
    """

    DISPLAY_TO_INTERNAL_MODE_MAP: Final[dict[str, str]] = {
        "input": "disabled",
        "force_off": "low",
        "force_on": "high",
        "output": "sequencer",
    }

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Union[Instrument, InstrumentChannel],
        name: str,
        io_channel_idx: int,
    ) -> None:
        """
        Creates a IO channel class and adds all relevant parameters for the
        IO channel.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this IO channel belongs.
        name : str
            Name of this IO channel
        io_channel_idx : int
            The index of this IO channel in the parent instrument, representing
            which IO channel is controlled by this class.
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store IO channel index
        self._io_channel_idx = io_channel_idx

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in IOChannel._get_required_parent_attr_names():
            self._register(attr_name)

        # Add parameters
        # -- Channel map -----------------------------------------------------
        # -- TBD

        # -- IOChannel (QTM-only) --------------------------------------------
        self.add_parameter(
            "mode",
            label="Output function of the I/O port for the given channel",
            docstring="Sets/gets the output function of the I/O Port for the given"
            "channel ('input' = port is in 50Ohm mode, "
            "'force_off' = the port drives low-impedance 0V, 'force_on' = the port "
            "drives low-impedance ~3.3V, 'output' = enables the port "
            "to output digital values according to the sequencer)",
            unit="",
            vals=vals.Enum(*self.DISPLAY_TO_INTERNAL_MODE_MAP),
            set_cmd=self._set_io_channel_mode,
            get_cmd=self._get_io_channel_mode,
        )

        self.add_parameter(
            "analog_threshold",
            label="primary threshold voltage used for digitization of the "
            "input signal for the given channel",
            docstring="Sets/gets the primary threshold voltage used for "
            "digitization of the input signal on the given channel",
            unit="V",
            vals=vals.Numbers(),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_threshold_primary"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_threshold_primary"],
            ),
        )

        self.add_parameter(
            "binned_acq_time_source",
            label="timetag data source for acquisitions made on the given channel",
            docstring="Sets/gets the timetag data source for acquisitions made on this channel "
            "using the acquire_timetags instruction",
            unit="",
            vals=vals.Enum("first", "second", "last"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_time_source"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_time_source"],
            ),
        )

        self.add_parameter(
            "binned_acq_time_ref",
            label="time reference that the timetag recorded for each acquire_timetags instruction "
            "is recorded in relation to",
            docstring="""
            Selects which time reference is used when each timetag is recorded.

            Parameters
            ----------
            value | args[0] : str
                One of the following values:
                    - `start` (default): Record relative to the start of the window.
                    - `end`: Record relative to the end of the window (always yields a negative timetag).
                    - `first0`: Record relative to the first recorded timetag of the most recently closed window on channel 0.
                    - `first1`: Record relative to the first recorded timetag of the most recently closed window on channel 1.
                    - `first2`: Record relative to the first recorded timetag of the most recently closed window on channel 2.
                    - `first3`: Record relative to the first recorded timetag of the most recently closed window on channel 3.
                    - `first4`: Record relative to the first recorded timetag of the most recently closed window on channel 4.
                    - `first5`: Record relative to the first recorded timetag of the most recently closed window on channel 5.
                    - `first6`: Record relative to the first recorded timetag of the most recently closed window on channel 6.
                    - `first7`: Record relative to the first recorded timetag of the most recently closed window on channel 7.
                    - `sequencer`: Record relative to the timestamp marked using the `set_time_ref` Q1 instruction.
""",  # noqa: E501
            unit="",
            vals=vals.Enum("start", "end", "first", *[f"first{x}" for x in range(8)], "sequencer"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_time_ref"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_time_ref"],
            ),
        )

        self.add_parameter(
            "binned_acq_on_invalid_time_delta",
            label="averaging and binning logic behavior if/when no valid time delta is available",
            docstring="Sets/gets averaging and binning logic behavior if/when no valid time delta "
            "is available, typically because no event occurred in the window",
            unit="",
            vals=vals.Enum(
                "error",
                "record_0",
                "discard",
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_on_invalid_time_delta"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_on_invalid_time_delta"],
            ),
        )

        self.add_parameter(
            "binned_acq_count_source",
            label="event count source for acquire_timetags instructions",
            docstring="Sets/gets the way events are counted during acquire_timetags windows. In "
            "'timetags' mode, the timetags themselves are counted, limiting repetition rate and "
            "latency to the capabilities of the time-to-digital converter. In 'low-latency' mode, "
            "a dedicated, low-latency counter is used instead. This counter is not limited by "
            "repetition rate, but uses a less accurate window. In 'combined' mode, both counters "
            "are used redundantly, and a disagreement in their counts is treated as an invalid "
            "count.",
            unit="",
            vals=vals.Enum(
                "timetags",
                "low-latency",
                "combined",
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_count_source"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_count_source"],
            ),
        )

        self.add_parameter(
            "binned_acq_on_invalid_count",
            label="averaging and binning logic behavior if/when no valid event count is available",
            docstring="Sets/gets averaging and binning logic behavior if/when no valid event count "
            "is available, typically due to counter disagreement for binned_acq_count_source = "
            "combined",
            unit="",
            vals=vals.Enum(
                "error",
                "record_0",
                "discard",
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_on_invalid_count"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_on_invalid_count"],
            ),
        )

        self.add_parameter(
            "binned_acq_on_invalid_threshold",
            label=(
                "averaging and binning logic behavior if/when no valid count threshold is available"
            ),
            docstring=(
                "Sets/gets averaging and binning logic behavior if/when no valid count threshold "
                "is available, typically due to counter disagreement for "
                "binned_acq_count_source = combined"
            ),
            unit="",
            vals=vals.Enum(
                "error",
                "record_0",
                "discard",
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_on_invalid_threshold"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_on_invalid_threshold"],
            ),
        )

        self.add_parameter(
            "binned_acq_threshold_source",
            label="data source of the threshold recorded by acquire_timetags",
            docstring="Sets/gets the data source of the threshold recorded by acquire timetags",
            unit="",
            vals=vals.Enum("thresh0", "thresh1"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_threshold_source"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_threshold_source"],
            ),
        )

        self.add_parameter(
            "is_above_threshold",
            label="current level of the input",
            docstring="Gets the current level of the input. Returns False if the input "
            "level is below analog_threshold, or True if it's above"
            "acquire timetags",
            unit="",
            set_cmd=False,
            get_cmd=lambda: bool(
                self._get_io_channel_status_val(["io_monitor"])  # internally it's 0 or 1
            ),
            max_val_age=0.0,  # disable read cache
        )

        self.add_parameter(
            "forward_trigger_en",
            label="sending triggers to the trigger network automatically",
            docstring="Sets/gets the enable that controls sending triggers "
            "to the trigger network automatically or based on direct sampling "
            "of the inputs. The mode is configured by forward_trigger_mode, and the "
            "address by forward_trigger_address",
            unit="",
            vals=vals.Bool(),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_en"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_en"],
            ),
        )

        self.add_parameter(
            "forward_trigger_mode",
            label="which event causes a trigger to be sent if forward_trigger_en is enabled",
            docstring="Sets/gets which event causes a trigger to be sent if forward_trigger_en "
            "is enabled ",
            unit="",
            vals=vals.Enum("rising", "falling", "sampled-high", "sampled-low"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_mode"],
            ),
        )

        self.add_parameter(
            "forward_trigger_address",
            label="which event causes a trigger to be sent if forward_trigger_en is enabled",
            docstring="Sets/gets which event causes a trigger to be sent if forward_trigger_en "
            "is enabled ",
            unit="",
            vals=vals.Ints(1, 15),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_address"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_address"],
            ),
        )

        self.add_parameter(
            "scope_trigger_mode",
            label="how the scope/trace unit for this channel is triggered",
            docstring="Sets/gets how the scope/trace unit for this channel is triggered "
            "is enabled ",
            unit="",
            vals=vals.Enum("sequencer", "external"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_trigger_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_trigger_mode"],
            ),
        )

        self.add_parameter(
            "scope_trigger_level",
            label="how the scope/trace unit for this channel is triggered",
            docstring="Sets/gets how the scope/trace unit for this channel is triggered "
            "is enabled ",
            unit="",
            vals=vals.Enum("any", "low", "high", "rising", "falling"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_trigger_level"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_trigger_level"],
            ),
        )

        self.add_parameter(
            "scope_mode",
            label="what type of data is traced when the scope/trace unit for this channel"
            "is triggered",
            docstring="Sets/gets what type of data is traced when the scope/trace unit for "
            "this channel is triggered",
            unit="",
            vals=vals.Enum("scope", "timetags", "timetags-windowed"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_mode"],
            ),
        )

        self.add_parameter(
            "thresholded_acq_trigger_en",
            label="whether the thresholded acquisition result of acquire_timetags is mapped "
            "to the trigger network for feedback purposes",
            docstring="Sets/gets whether the thresholded acquisition result of acquire_timetags "
            "is mapped to the trigger network for feedback purposes",
            unit="",
            vals=vals.Bool(),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["thresholded_acq_trigger_en"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["thresholded_acq_trigger_en"],
            ),
        )

        for result in ["low", "mid", "high", "invalid"]:
            self.add_parameter(
                f"thresholded_acq_trigger_address_{result}",
                label=(
                    f"whether a trigger is to be sent and which trigger address is to be used "
                    f"when the result is {result}"
                ),
                docstring=(
                    f"Sets/gets whether a trigger is to be sent and which trigger address "
                    f"is to be used when the result is {result}"
                ),
                unit="",
                vals=vals.Ints(0, 15),
                set_cmd=partial(
                    self._set_io_channel_config_val,
                    [f"thresholded_acq_trigger_address_{result}"],
                ),
                get_cmd=partial(
                    self._get_io_channel_config_val,
                    [f"thresholded_acq_trigger_address_{result}"],
                ),
            )

        self.add_parameter(
            "truth_table_en",
            label="enable/disable Truth Table usage",
            docstring="Enable/disable Truth Table usage in the local channel",
            unit="",
            vals=vals.Bool(),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["thresholded_acq_lut_en"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["thresholded_acq_lut_en"],
            ),
        )

    # ------------------------------------------------------------------------
    def _set_io_channel_mode(self, val: str) -> None:
        """
        Custom setter for the io_channel_mode parameter of the object.
        Acts as a wrapper.
        Uses the DISPLAY_TO_INTERNAL_MODE_MAP to match the available options of
        the user to the internally used equivalent.

        Parameters
        -----------
        val: str
            key of DISPLAY_TO_INTERNAL_MODE_MAP
        """
        internal_val = self.DISPLAY_TO_INTERNAL_MODE_MAP[val]
        self._set_io_channel_config_val(["out_mode"], internal_val)

    # ------------------------------------------------------------------------
    def _get_io_channel_mode(self) -> str:
        """
        Custom getter for the io_channel_mode_parameter of the obnect.
        Acts as a wrapper.
        Uses the INTERNAL_TO_DISPLAY_MODE_MAP to match the internally used terms
        to the ones the user is familiar with.

        Returns
        ------------
        mode: str
        """
        INTERNAL_TO_DISPLAY_MODE_MAP: Final[dict[str, str]] = {
            v: k for k, v in self.DISPLAY_TO_INTERNAL_MODE_MAP.items()
        }

        internal_val = self._get_io_channel_config_val(["out_mode"])
        return INTERNAL_TO_DISPLAY_MODE_MAP[internal_val]

    @property
    def io_channel_idx(self) -> int:
        """
        Get IO channel index.

        Returns
        ----------
        int
            IOChannel index
        """

        return self._io_channel_idx

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_parent_attr_names() -> list:
        """
        Return list of parent attribute names that are required for the QCoDeS
        parameters to function, so that the can be registered to this object
        using the _register method.

        Returns
        ----------
        list
            List of parent attribute names to register.
        """

        # IOChannel attributes
        attr_names = []
        for operation in ["set", "get"]:
            attr_names.append(f"_{operation}_io_channel_config")
            attr_names.append(f"_{operation}_io_channel_config_val")
        attr_names.append("_get_io_channel_status")
        attr_names.append("_get_io_channel_status_val")
        attr_names.append("get_scope_data")

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
                + "This method calls {1}.{0} using functools.partial to set the "
                + "IO channel index. The docstring above is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func = partial_with_numpy_doc(
                parent_attr, self.io_channel_idx, end_with=partial_doc
            )
            setattr(self, attr_name, partial_func)
        else:

            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'{self.parent.name} does not have "{attr_name}" attribute.'
                )

            setattr(self, attr_name, raise_not_implemented_error)

        # ------------------------------------------------------------------------

    def truth_table_data(
        self,
        input_src: Union[list, TruthTable],
        default_trg_addr: int = 0,
        overwrite_conflict: bool = False,
    ) -> None:
        """
        Generates Truth Table configuration to be sent to the instrument.

        Parameters
        ----------
        input_src : Union[list, TruthTable]
            List of rules used to build the Truth Table or a Truth Table object.
        """
        if isinstance(input_src, list):
            tt = TruthTable.from_config(input_src, default_trg_addr, overwrite_conflict)
        elif isinstance(input_src, TruthTable):
            tt = input_src
        else:
            raise ValueError("input_src must be a list or a TruthTable object.")
        self._set_io_channel_config_val("thresholded_acq_lut_data", tt.lut)
