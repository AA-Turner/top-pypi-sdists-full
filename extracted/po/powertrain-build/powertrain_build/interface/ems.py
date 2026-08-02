# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for extraction Energy Management System"""
import os

from powertrain_build.interface.base import BaseApplication, Signal
from powertrain_build.lib import logger
from powertrain_build.signal_interfaces import CsvSignalInterfaces
from powertrain_build.build_proj_config import BuildProjConfig

LOGGER = logger.create_logger(__file__)


class CsvEMS(BaseApplication, CsvSignalInterfaces):
    """Supplier part of the ECM"""
    def __init__(self):
        self._signals = {}
        self.interfaces = {}
        self._insignals = None
        self._outsignals = None
        self.projects = {}

    def parse_definition(self, definition):
        """Read the interface files.

        Args:
            definition (Path): Path to ProjectCfg.json
        """
        self.build_cfg = BuildProjConfig(os.path.normpath(str(definition)))
        CsvSignalInterfaces.__init__(self, self.build_cfg, [])
        self.projects[self.build_cfg.name] = self.build_cfg
        self.config_path = self.build_cfg.get_if_cfg_dir()
        self.name = self.build_cfg.name  # Set name for CsvSignalInterfaces
        self._parse_io_cnfg(self.config_path)
        self.name = 'Supplier_' + self.build_cfg.name  # set name for BaseApplication

    def _get_signals(self):
        """Look through interfaces and create Signal objects"""
        self._insignals = set()
        self._outsignals = set()
        for interface_name, data in self.interfaces.items():
            for signal_name, signal_data in data.items():
                if signal_data['IOType'] == '-':
                    # Signal is inactive
                    continue
                if signal_name in self._signals:
                    signal = self._signals[signal_name]
                else:
                    signal = Signal(signal_name, self)
                    self._signals.update({signal_name: signal})
                if 'output' in interface_name.lower():
                    # outport from ECM. Inport in EMS (from SPM)
                    self._insignals.add(signal_name)
                    signal.consumers = interface_name
                else:
                    signal.producers = interface_name
                    self._outsignals.add(signal_name)

    def get_signal_properties(self, signal):
        """Find properties for a signal from interface files"""
        for interface_name, interface_data in self.interfaces.items():
            if signal.name in interface_data.keys():
                properties = interface_data[signal.name]
                properties['interface'] = interface_name
                return properties
        return {}
