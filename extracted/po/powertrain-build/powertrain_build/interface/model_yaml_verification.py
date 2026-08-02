# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for verifying the model yaml files."""

import argparse
import logging
import sys
import typing
from pathlib import Path
from voluptuous import All, MultipleInvalid, Optional, Required, Schema
from ruamel.yaml import YAML
from powertrain_build.interface.application import Application
from powertrain_build.interface.base import BaseApplication

PARSER_HELP = "Verify the model yaml files."


class ModelYmlVerification(BaseApplication):
    """Class for verifying the model yaml files."""

    def __init__(self, base_application):
        self.base_application = base_application
        self.raw = {}
        self.app_insignals = self.get_insignals_name()
        self.app_outsignals = self.get_outsignals_name()
        self.signal_properties = {}
        self.model_name = None
        self.error_printed = False

    def read_translation(self, translation_file):
        """Read specification of the yaml file.

        Args:
            translation_file (Path): file with specs.
        """

        if not translation_file.is_file():
            return {}
        with open(translation_file, encoding="utf-8") as translation:
            try:
                yaml = YAML(typ='safe', pure=True)
                self.raw = yaml.load(translation)
            except yaml.YAMLError as e:
                self.raw = {}
                if hasattr(e, 'problem_mark'):
                    mark = e.problem_mark
                    self.error("Error while reading model file, verification of this file cannot continue until this "
                               f"is fixed:\nFile: {translation_file}\nLine: {mark.line + 1}\nColumn: {mark.column + 1}")
                else:
                    self.error("Error while reading model file, verification of this file cannot continue until this "
                               f"is fixed:\nFile: {translation_file}")

    def validate_signal_schema(self, signal_spec, signal_direction, is_hal, is_service):
        """Validate if signal have a correct schema in model yaml file.

        Args:
            signal_spec (dict): signal specification.
            signal_direction (str): insignal or outsignal.
            is_hal (Bool): signal comming from hal
            is_service (Bool): signal comming from service
        """
        if is_hal:
            signal_schema = Schema({Required('insignal'): All(str), Optional('property'): All(str)})
        elif is_service:
            signal_schema = Schema({Required(signal_direction): All(str), Optional('property'): All(str)})
        else:
            signal_schema = Schema({Required(signal_direction): All(str), Required('property'): All(str)})
        try:
            signal_schema(signal_spec)
        except MultipleInvalid as e:
            self.error(f"{e} in {self.model_name}")

    def validate_group_schema(self, group_spec):
        """Validate if device proxy signal group and hal endpoint
        have correct schema.

        Args:
            group_spec (dict): dp signal group or hal endpoint.
        """
        group_schema = Schema({Required(str): [{Required(str): list}]})
        try:
            group_schema(group_spec)
        except MultipleInvalid as e:
            self.error(self.model_name + ' ' + str(e))

    def validate_service_schema(self, service_spec):
        """Validate if service schema in model yaml file.

        Args:
            service_spec (dict): service in model yaml file.
        """
        service_schema = Schema(
            {
                Required(str): {
                    Optional('properties'): [{Required(str): list}],
                    Optional('methods'): [{Required(str): list}]
                }
            }
        )
        try:
            service_schema(service_spec)
        except MultipleInvalid as e:
            self.error(self.model_name + ' ' + str(e))

    def validate_schema(self):
        """Validate interface schema in model yaml file.

        Interface could be hal, dp(signal/signal group) and serivece.
        """
        schema = Schema({
            Optional('hal'): dict, Optional('signal_groups'): dict,
            Optional('service'): dict, Optional('signals'): dict})
        try:
            schema(self.raw)
        except MultipleInvalid as e:
            self.error(self.model_name + ' ' + str(e))

    def parse_hal_definition(self, hal):
        """Parse hal definition.

        Args:
            hal (dict): hal specification in model yaml file.
        """
        self.parse_group_definitions(hal, is_hal=True)

    def parse_service_definitions(self, service):
        """Parse service.

        Args:
            service (dict): service in model yaml file.
        """
        if service:
            self.validate_service_schema(service)
        for service_name, definition in service.items():
            for endpoints in definition.get('properties', []):
                for endpoint, signals in endpoints.items():
                    self.verify_signals({service_name: signals}, is_service=True, endpoint=endpoint)
            for endpoints in definition.get('methods', []):
                for endpoint, signals in endpoints.items():
                    self.verify_signals({service_name: signals}, is_service=True, endpoint=endpoint)

    def parse_group_definitions(self, signal_groups, is_hal=False):
        """Parse signal groups.

        Args:
            signal_groups (dict): Hal/dp signal group in yaml file.
            is_hal (Bool): hal signal
        """
        if signal_groups:
            self.validate_group_schema(signal_groups)
        for interface, group_definitions in signal_groups.items():
            for group in group_definitions:
                for group_name, signals in group.items():
                    self.verify_signals({interface: signals}, is_hal, group=group_name)

    def verify_signals(self, signals_definition, is_hal=False, is_service=False, endpoint=None, group=None):
        """verify signal in-signal and out-signal in model yaml file.

        Args:
            signals_definition (dict): parsed signals in model yaml file.
            is_hal (Bool): hal signal.
            is_service (Bool): service signal.
            endpoint (str): service endpoint.
            group(str): hal group.
        """
        for interface, specifications in signals_definition.items():
            for specification in specifications:
                in_out_signal = [key for key in specification.keys() if 'signal' in key]
                signal_name = specification[in_out_signal[0]]
                self.validate_signal_schema(specification, in_out_signal[0], is_hal, is_service)
                if in_out_signal == []:
                    self.error(f"signal is not defined for {interface} in {self.model_name}!")
                if 'in' not in in_out_signal[0] and 'out' not in in_out_signal[0]:
                    self.error(f"in and out signal must be added to signal {specification['signal']}")
                elif 'in' in in_out_signal[0] and specification[in_out_signal[0]] not in self.app_insignals:
                    self.error(
                        f"{specification['insignal']} is not defined as an insignal in json file")
                elif "out" in in_out_signal[0] and specification[in_out_signal[0]] not in self.app_outsignals:
                    self.error(
                        f"{specification['outsignal']} is not defined as an outsignal in json file")
                else:
                    if is_service:
                        if specification.get('property') is None:
                            self.verify_primitive(f"{interface}.{endpoint}.{signal_name}", in_out_signal[0])
                        else:
                            self.verify_primitive(
                                f"{interface}.{endpoint}.{specification['property']}.{signal_name}",
                                in_out_signal[0])
                    elif is_hal:
                        if specification.get('property') is None:
                            self.verify_primitive(f"{interface}.{group}.{signal_name}", in_out_signal[0])
                        else:
                            self.verify_primitive(f"{interface}.{group}.{specification['property']}.{signal_name}",
                                                  in_out_signal[0])
                    else:
                        self.verify_primitive(f"{interface}.{specification['property']}.{signal_name}",
                                              in_out_signal[0])

    def check_duplicate_signals(self, property_spec, in_out):
        """Check if each signal appears only once for each model.
        It is ok for two insignals with the same name to be mapped to the same primitive
        if they are in different models.
        It is not ok for a outsignal to map to the same interface twice, but it is ok to map to
        different interfaces (with same or different property name).

        Args:
            property_spec (str): property specification.
            in_out (str): whether it is an in- or outsignal.
        """
        signal_name = property_spec.split('.')[-1]
        interface_name = property_spec.split('.')[0]
        for model, spec in self.signal_properties.items():
            for primitive in spec:
                if signal_name in primitive.split('.'):
                    if property_spec not in primitive:
                        if "in" in in_out:
                            self.error(
                                f"You can't connect a signal {signal_name} in {self.model_name} model to two "
                                f"different primitives. It's already connected in {model} model")
                        else:
                            if interface_name in primitive.split('.'):
                                self.error(
                                    f"You can't connect a signal {signal_name} in {self.model_name} model "
                                    f"to the same interface ({interface_name}) twice. "
                                    f"It's already connected as {primitive} in model {model}.")

                    else:
                        if model == self.model_name:
                            self.error(f"You can't connect signal {signal_name} in {self.model_name} model twice.")
                        elif "out" in in_out:
                            self.error(
                                f"You can't connect signal {signal_name} in {self.model_name} model to the same "
                                f"primitive as in another model. It is already defined in {model}")

    def check_property(self, property_spec):
        """Check if we have only one signal written for the same property.

        Args:
            property_spec (str): property specification.
        """
        signal_name = property_spec.split('.')[-1]
        for model, spec in self.signal_properties.items():
            for primitive in spec:
                if ('.'.join(property_spec.split('.')[:-1]) == '.'.join(primitive.split('.')[:-1])
                        and signal_name != primitive.split('.')[-1]):
                    self.error(
                            f"You can't connect another signal to the existing property {property_spec} in "
                            f"{self.model_name} model, because it is already defined in {model} model.")

    def verify_primitive(self, property_spec, in_out):
        """Runs the necessary tests.

        Args:
            property_spec (str): property specification.
            in_out (str): whether it is an in- or outsignal.
        """
        self.check_duplicate_signals(property_spec, in_out)
        self.check_property(property_spec)
        self.signal_properties[self.model_name].append(property_spec)

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
            definition (list(Path)): model yaml files.
        """
        for translation in definition:
            path = Path(translation)
            self.model_name = path.name.replace(".yaml", "")
            self.signal_properties[self.model_name] = []
            self.read_translation(translation)
            self.validate_schema()
            self.verify_signals(self.raw.get("signals", {}))
            self.parse_group_definitions(self.raw.get("signal_groups", {}))
            self.parse_hal_definition(self.raw.get("hal", {}))
            self.parse_service_definitions(self.raw.get("service", {}))

    def error(self, msg):
        """ Prints an error message to the terminal.

        Args:
            msg (string): The message to be printed.
        """
        self.error_printed = True
        logging.error(f"{msg}\n")

    def print_success_msg(self):
        """ Prints a success message if no error messages have been printed.
        """
        if not self.error_printed:
            print('Yaml verification done without any errors.')


def get_app(project_config):
    """ Get an app specification for the current project.

    Args:
        config (pathlib.Path): Path to the ProjectCfg.json.
    Returns:
        app (Application): powertrain-build project.
    """
    app = Application()
    app.parse_definition(project_config)
    return app


def configure_parser(parser: argparse.ArgumentParser):
    """Configure the argument parser."""
    parser.add_argument("config", help="The SPA2 project config file", type=Path)
    parser.set_defaults(func=model_yaml_verification_cli)


def model_yaml_verification_cli(args: argparse.Namespace):
    """CLI function for model yaml verification."""
    app = get_app(args.config)
    model_yamls = app.get_translation_files()
    model_yaml_ver = ModelYmlVerification(app)
    model_yaml_ver.parse_definition(model_yamls)
    model_yaml_ver.print_success_msg()


def main(argv: typing.Optional[typing.List[str]] = None):
    """Main function for model yaml verification."""
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
