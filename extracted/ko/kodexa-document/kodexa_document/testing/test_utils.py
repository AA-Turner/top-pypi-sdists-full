"""
Testing utilities for Kodexa extensions and assistants.
"""
import importlib
import logging

from addict import Dict

from kodexa_document.model.objects import ExceptionDetails

logger = logging.getLogger()


class OptionException(Exception):
    """
    An exception that is raised when there is a problem with a requests option
    """


class ExceptionBuilder:
    """
    A helper to build an exception details from the last exception
    """

    @staticmethod
    def build_exception_details():
        import sys
        import better_exceptions

        et, ev, tb = sys.exc_info()
        return ExceptionDetails(
            **{
                "errorType": et.__name__,
                "errorMessage": str(ev),
                "message": "An unexpected exception has occurred",
                "help": "\n".join(better_exceptions.format_exception(*sys.exc_info())),
            }
        )


class ExtensionPackUtil:
    """
    A utility that can be used to access an action defined in a kodexa.yml.

    This allows you to use the kodexa.yml in unit tests to ensure it matches your current action code

    >>> from kodexa_document.testing import ExtensionPackUtil
    >>> util = ExtensionPackUtil("../kodexa.yml")
    >>> step = util.get_step("my-action", {"my-option": "cheese"})

    """

    def __init__(self, file_path="kodexa.yml"):
        self.file_path = file_path

        if file_path.endswith(".yml"):
            import yaml

            with open(file_path, "r") as stream:
                self.kodexa_metadata = yaml.safe_load(stream)

        if file_path.endswith(".json"):
            import json

            with open(file_path, "r") as stream:
                self.kodexa_metadata = Dict(json.load(stream))

    def get_step(self, action_slug, options=None):
        """
        Get a step instance from the extension pack metadata.

        Args:
          action_slug (str): the slug to the action (ie. pdf-parser)
          options (dict):  the options for the action as a dictionary (Default value = None)

        Returns:
          The step instance
        """
        if options is None:
            options = {}

        for service in self.kodexa_metadata["services"]:
            if service["type"] == "action" and service["slug"] == action_slug:
                # Validate and apply default options
                if len(service["metadata"]["options"]) > 0:
                    option_names = []
                    for option in service["metadata"]["options"]:
                        option_names.append(option["name"])
                        if option["name"] not in options and "default" in option and option["default"] is not None:
                            options[option["name"]] = option["default"]
                        if option["required"] and option["name"] not in options:
                            raise OptionException(
                                f"Missing required option {option['name']}"
                            )

                    for option_name in options.keys():
                        if option_name not in option_names:
                            # Check if this is a group
                            is_group = False
                            for check_option in service["metadata"]["options"]:
                                if "group" in check_option and check_option["group"] is not None:
                                    if check_option["group"]["name"] == option_name:
                                        is_group = True

                            if not is_group:
                                raise OptionException(
                                    f"Unexpected option {option_name}"
                                )

                # Create and return the action instance
                module = importlib.import_module(service["step"]["package"])
                klass = getattr(module, service["step"]["class"])
                new_instance = klass(**options)

                # Add to_dict method for metadata access
                import types

                def general_to_dict(self):
                    return {"ref": f"./{action_slug}", "options": options}

                new_instance.to_dict = types.MethodType(general_to_dict, new_instance)
                return new_instance

        raise Exception("Unable to find the action " + action_slug)

    def get_assistant(self, assistant_slug, options=None):
        """
        Create an instance of an assistant from the Kodexa metadata

        Args:
          assistant_slug: the slug of the assistant
          options: the options for the assistant (Default value = None)

        Returns:
          The assistant instance
        """
        if options is None:
            options = {}

        for service in self.kodexa_metadata["services"]:
            if service["type"] == "assistant" and service["slug"] == assistant_slug:
                logger.info(f"Creating new assistant {service['assistant']}")
                module = importlib.import_module(service["assistant"]["package"])
                klass = getattr(module, service["assistant"]["class"])
                return klass(**options)

        raise Exception("Unable to find the assistant " + assistant_slug)
