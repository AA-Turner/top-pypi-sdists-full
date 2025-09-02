# ----------------------------------------------------------------------------
# Description    : IOPulseChannel QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2024)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

# from functools import partial
from typing import Union

from qcodes import Instrument, InstrumentChannel
from qcodes import validators as vals

from qblox_instruments.docstring_helpers import partial_with_numpy_doc
from qblox_instruments.qcodes_drivers.component import Component

# -- class -------------------------------------------------------------------


class IOPulseChannel(Component):
    """
    This class represents a single IO Pulse channel. It combines all channel
    specific parameters and functions into a single QCoDes InstrumentChannel.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Union[Instrument, InstrumentChannel],
        name: str,
        io_pulse_channel_idx: int,
    ) -> None:
        """
        Creates a IO Pulse channel class and adds all relevant parameters for the
        IO channel.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this IO channel belongs.
        name : str
            Name of this IO channel channel
        io_pulse_channel_idx : int
            The index of this IO channel in the parent instrument, representing
            which IO channel is controlled by this class.
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store IO channel index
        self._io_pulse_channel_idx = io_pulse_channel_idx

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in IOPulseChannel._get_required_parent_attr_names():
            self._register(attr_name)

        # Add parameters
        # -- Channel map -----------------------------------------------------
        # -- TBD

        # -- IOPulseChannel (QTM-Pulse-only) ----------------------------------
        self.add_parameter(
            "output_normalized_amplitude",
            label="Normalized output amplitude of the pulse",
            docstring="""Normalized output amplitude of the pulse. It should
                        range from 0.0 to 1.0 in steps of 1/65535""",
            unit="V",
            vals=vals.Numbers(),
            set_parser=float,
            get_parser=float,
            set_cmd=self._set_output_normalized_amplitude,
            get_cmd=self._get_output_normalized_amplitude,
        )

        self.add_parameter(
            "output_offset",
            label="DC output offset.",
            docstring="DC output offset. It should range from -3.0 to +3.0",
            unit="V",
            vals=vals.Numbers(),
            set_parser=float,
            get_parser=float,
            set_cmd=self._set_io_pulse_output_offset,
            get_cmd=self._get_io_pulse_output_offset,
        )

        self.add_parameter(
            "pulse_width",
            label="Output pulse duration. Configuration must be a dict"
            "containing coarse and fine keywords. Coarse range from 1..128 in unit of ns."
            "Fine range from 1..1000 ps",
            docstring="....",
            unit="ns/ps",
            vals=vals.Dict(),
            set_cmd=self._set_io_pulse_width_config,
            get_cmd=self._get_io_pulse_width_config,
        )

    # ------------------------------------------------------------------------
    @property
    def io_pulse_channel_idx(self) -> int:
        """
        Get IO Pulse channel index.

        Returns
        ----------
        int
            IO Pulse Channel index
        """

        return self._io_pulse_channel_idx

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

        # IOPulseChannel attributes
        attr_names = []
        for operation in ["set", "get"]:
            attr_names.append(f"_{operation}_output_normalized_amplitude")
            attr_names.append(f"_{operation}_io_pulse_output_offset")
            attr_names.append(f"_{operation}_io_pulse_width_config")

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
                parent_attr, self.io_pulse_channel_idx, end_with=partial_doc
            )
            setattr(self, attr_name, partial_func)
        else:

            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'{self.parent.name} does not have "{attr_name}" attribute.'
                )

            setattr(self, attr_name, raise_not_implemented_error)
