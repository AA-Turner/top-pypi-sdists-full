# -*- coding: utf-8 -*-
import os

from cleo.commands.command import Command as BaseCommand
from cleo.io.inputs.option import Option as InputOption
import yaml

from orator import DatabaseManager


class Command(BaseCommand):

    needs_config = True

    def __init__(self, resolver=None):
        self.resolver = resolver
        self.input = None
        self.output = None

        super(Command, self).__init__()

    def configure(self):
        super(Command, self).configure()

        if self.needs_config and not self.resolver:
            # Checking if a default config file is present
            if not self._check_config():
                self._definition.add_option(
                    InputOption(
                        name="config",
                        shortcut="c",
                        flag=False,
                        requires_value=True,
                        description="The config file path"
                    )
                )

    def execute(self, io):
        """
        Executes the command.
        """
        self._io = io
        self.add_style("question", fg="blue")

        if self.needs_config and not self.resolver:
            self._handle_config(self.option("config"))

        return self.handle()

    def call(self, name, options=None):
        command = self.application.get(name)
        command.resolver = self.resolver

        return super(Command, self).call(name, options)

    def call_silent(self, name, options=None):
        command = self.application.get(name)
        command.resolver = self.resolver

        return super(Command, self).call_silent(name, options)

    def confirm_to_proceed(self, message=None):
        if message is None:
            message = "Do you really wish to run this command?: "

        if self.option("force"):
            return True

        confirmed = self.confirm(message)

        if not confirmed:
            self.comment("Command Cancelled!")

            return False

        return True

    def _get_migration_path(self):
        return os.path.join(os.getcwd(), "migrations")

    def _check_config(self):
        """
        Check presence of default config files.

        :rtype: bool
        """
        current_path = os.path.relpath(os.getcwd())

        accepted_files = ["orator.yml", "orator.py"]
        for accepted_file in accepted_files:
            config_file = os.path.join(current_path, accepted_file)
            if os.path.exists(config_file):
                if self._handle_config(config_file):
                    return True

        return False

    def _handle_config(self, config_file):
        """
        Check and handle a config file.

        :param config_file: The path to the config file
        :type config_file: str

        :rtype: bool
        """
        config = self._get_config(config_file)

        self.resolver = DatabaseManager(
            config.get("databases", config.get("DATABASES", {}))
        )

        return True

    def _get_config(self, path=None):
        """
        Get the config.

        :rtype: dict
        """
        if not path and not self.option("config"):
            raise Exception("The --config|-c option is missing.")

        if not path:
            path = self.option("config")

        filename, ext = os.path.splitext(path)
        if ext in [".yml", ".yaml"]:
            with open(path) as fd:
                config = yaml.load(fd, yaml.FullLoader)
        elif ext in [".py"]:
            config = {}

            with open(path) as fh:
                exec(fh.read(), {}, config)
        else:
            raise RuntimeError("Config file [%s] is not supported." % path)

        return config
