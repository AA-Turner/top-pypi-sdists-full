# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for handling the update of model yaml files."""


import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ruamel.yaml import YAML
from powertrain_build.interface.application import Application
from powertrain_build.interface.base import BaseApplication

PARSER_HELP = "Update model yaml files."


class BadYamlFormat(Exception):
    """Exception to raise when signal is not in/out signal."""
    def __init__(self, signal):
        self.message = f"{signal} is not in-signal or out-signal."


class UpdateYmlFormat(BaseApplication):
    """Class to handle the update of model yaml files."""

    def __init__(self, base_application):
        self.base_application = base_application
        self.raw = {}
        self.app_insignals = self.get_insignals_name()
        self.app_outsignals = self.get_outsignals_name()

    def read_translation(self, translation_file):
        """Read specification of the yaml file.

        Args:
            translation_file (Path): file with specs.
        """
        if not translation_file.is_file():
            return {}
        with open(translation_file, encoding="utf-8") as translation:
            yaml = YAML(typ='safe', pure=True)
            self.raw = yaml.load(translation)

    def parse_groups(self, signal_groups):
        """Parse signal groups.

        Args:
            signal_groups (dict): Hal/dp signal group in yaml file.
        """
        for interface_type, group_definitions in signal_groups.items():
            for group in group_definitions:
                for signals in group.values():
                    self.check_signals({interface_type: signals})

    def parse_hal_definitions(self, hal):
        """Parse hal.

        Args:
            hal (dict): hal in yaml file.
        """
        self.parse_groups(hal)

    def parse_service_definitions(self, service):
        """Parse service.

        Args:
            service (dict): service in yaml file.
        """
        for interface, definition in service.items():
            for apis in definition['properties']:
                for signals in apis.values():
                    self.check_signals({interface: signals})

    def check_signals(self, signals_definition):
        """check signal direction(in-signal or out-signal).

        Args:
            signals_definition (dict): parsed yaml file.
        """
        for specifications in signals_definition.values():
            for specification in specifications:
                in_out_signal = [key for key in specification.keys() if 'signal' in key]
                if in_out_signal == []:
                    raise ValueError(f"signal is not defined for property: {specification['property']} !")
                if "in" in in_out_signal[0]:
                    if specification[in_out_signal[0]] not in self.app_insignals:
                        if specification[in_out_signal[0]] in self.app_outsignals:
                            specification["outsignal"] = specification[in_out_signal[0]]
                        else:
                            raise BadYamlFormat(specification[in_out_signal[0]])
                if "out" in in_out_signal[0]:
                    if specification[in_out_signal[0]] not in self.app_outsignals:
                        if specification[in_out_signal[0]] in self.app_insignals:
                            specification["insignal"] = specification[in_out_signal[0]]
                        else:
                            raise BadYamlFormat(specification[in_out_signal[0]])
                if in_out_signal[0] == "signal":
                    if specification["signal"] in self.app_insignals:
                        specification["insignal"] = specification["signal"]
                        del specification["signal"]
                    elif specification["signal"] in self.app_outsignals:
                        specification["outsignal"] = specification["signal"]
                        del specification["signal"]
                    else:
                        raise BadYamlFormat(specification[in_out_signal[0]])

    def get_insignals_name(self):
        """Base application in-signals.
        """
        app_insignals = []
        for signal in self.base_application.insignals:
            app_insignals.append(signal.name)
        return app_insignals

    def get_outsignals_name(self):
        """Base application out-signals.
        """
        app_outsignals = []
        for signal in self.base_application.outsignals:
            app_outsignals.append(signal.name)
        return app_outsignals

    def parse_definition(self, definition):
        """Parses all definition files

        Args:
            definition (list(Path)): Definition files
        """
        for translation in definition:
            self.read_translation(translation)
            self.check_signals(self.raw.get("signals", {}))
            self.parse_groups(self.raw.get("signal_groups", {}))
            self.parse_hal_definitions(self.raw.get("hal", {}))
            self.parse_service_definitions(self.raw.get("service", {}))
            self.write_to_file(translation)

    def write_to_file(self, translation):
        """Write in/out signals to file
        Args:
            spec (dict): Specification
            output (Path): File to write
        """
        with open(translation, "w", encoding="utf-8") as new_file:
            yaml = YAML()
            yaml.dump(self.raw, new_file)


def get_app(config):
    """ Get an app specification for the current project

    Args:
        config (pathlib.Path): Path to the ProjectCfg.json.
    Returns:
        app (Application): powertrain_build project.
    """
    app = Application()
    app.parse_definition(config)
    return app


def update_model_yaml_cli(args: argparse.Namespace):
    """CLI for update model yaml."""
    app = get_app(args.config)
    translation_files = app.get_translation_files()
    uymlf = UpdateYmlFormat(app)
    uymlf.parse_definition(translation_files)


def configure_parser(parser: argparse.ArgumentParser):
    """Configure parser for update model yaml."""
    parser.add_argument("config", help="The SPA2 project config file", type=Path)
    parser.set_defaults(func=update_model_yaml_cli)


def main(argv: Optional[List[str]] = None):
    """Main function for update model yaml."""
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
