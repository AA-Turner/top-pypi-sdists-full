from qcodes import InstrumentChannel


class Component(InstrumentChannel):
    # ------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(self) -> None:
        """
        Marks the cache of all QCoDeS parameters on this component as invalid.
        """

        for param in self.parameters.values():
            param.cache.invalidate()
