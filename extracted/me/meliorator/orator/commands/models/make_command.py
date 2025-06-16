# -*- coding: utf-8 -*-
import os
import inflection

from cleo.commands.command import Command
from cleo.helpers import argument, option

from .stubs import MODEL_DEFAULT_STUB
from ...utils import mkdir_p


class ModelMakeCommand(Command):
    name = 'make model'
    description = 'Creates a new Model class.'

    # Deprecated command name. It will be removed in 1.x
    aliases = ['make:model']

    arguments = [
        argument(
            name="name",
            description='The name of the model to create.',
        ),
    ]

    options = [
        option(
            long_name='migration',
            short_name='m',
            description='Create a new migration file for the model.',
            flag=True,
            value_required=False,
        ),
        option(
            long_name='path',
            short_name='p',
            description='Path to models directory',
            flag=False,
            value_required=False,
        ),
    ]

    def handle(self):
        name = self.argument("name")
        singular = inflection.singularize(inflection.tableize(name))
        directory = self._get_path()
        filepath = self._get_path(singular + ".py")

        if os.path.exists(filepath):
            raise RuntimeError("The model file already exists.")

        mkdir_p(directory)

        parent = os.path.join(directory, "__init__.py")
        if not os.path.exists(parent):
            with open(parent, "w"):
                pass

        stub = self._get_stub()
        stub = self._populate_stub(name, stub)

        with open(filepath, "w") as f:
            f.write(stub)

        self.info("Model <comment>%s</> successfully created." % name)

        if self.option("migration"):
            table = inflection.tableize(name)

            # FIXME: Cleo has a issue in self.call that uses the first argument as command name
            # https://github.com/python-poetry/cleo/issues/130
            self.call(
                "make:migration",
                f' make:migration create_{table}_table --table {table} --create',
            )

    def _get_stub(self):
        """
        Get the model stub template

        :rtype: str
        """
        return MODEL_DEFAULT_STUB

    def _populate_stub(self, name, stub):
        """
        Populate the placeholders in the migration stub.

        :param name: The name of the model
        :type name: str

        :param stub: The stub
        :type stub: str

        :rtype: str
        """
        stub = stub.replace("DummyClass", name)

        return stub

    def _get_path(self, name=None):
        if self.option("path"):
            directory = self.option("path")
        else:
            directory = os.path.join(os.getcwd(), "models")

        if name:
            return os.path.join(directory, name)

        return directory
