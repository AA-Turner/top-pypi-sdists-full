#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery,
    PyArguments,
    PyArgumentsTextualSubItem,
    PyArgumentsNumericalSubItem,
    PyArgumentsDictionarySubItem,
    PyArgumentsParameterSubItem,
    PyArgumentsSingletonSubItem
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.File = self.__class__.File(service, rules, path + [("File", "")])
        self.FileManager = self.__class__.FileManager(service, rules, path + [("FileManager", "")])
        super().__init__(service, rules, path)

    class File(PyNamedObjectContainer):
        """
        .
        """
        class _File(PyMenu):
            """
            Singleton _File.
            """
            def __init__(self, service, rules, path):
                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                self.Append = self.__class__.Append(service, rules, path + [("Append", "")])
                self.ConvertedPath = self.__class__.ConvertedPath(service, rules, path + [("ConvertedPath", "")])
                self.Dummy = self.__class__.Dummy(service, rules, path + [("Dummy", "")])
                self.FileUnit = self.__class__.FileUnit(service, rules, path + [("FileUnit", "")])
                self.IgnoreSolidNames = self.__class__.IgnoreSolidNames(service, rules, path + [("IgnoreSolidNames", "")])
                self.JtLOD = self.__class__.JtLOD(service, rules, path + [("JtLOD", "")])
                self.Keys = self.__class__.Keys(service, rules, path + [("Keys", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.PartPerBody = self.__class__.PartPerBody(service, rules, path + [("PartPerBody", "")])
                self.Path = self.__class__.Path(service, rules, path + [("Path", "")])
                self.PrefixParentName = self.__class__.PrefixParentName(service, rules, path + [("PrefixParentName", "")])
                self.RemoveEmptyParts = self.__class__.RemoveEmptyParts(service, rules, path + [("RemoveEmptyParts", "")])
                self.Route = self.__class__.Route(service, rules, path + [("Route", "")])
                self.Updated = self.__class__.Updated(service, rules, path + [("Updated", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class Options(PyMenu):
                """
                Singleton Options.
                """
                def __init__(self, service, rules, path):
                    self.Line = self.__class__.Line(service, rules, path + [("Line", "")])
                    self.Solid = self.__class__.Solid(service, rules, path + [("Solid", "")])
                    self.Surface = self.__class__.Surface(service, rules, path + [("Surface", "")])
                    super().__init__(service, rules, path)

                class Line(PyParameter):
                    """
                    Parameter Line of value type bool.
                    """
                    pass

                class Solid(PyParameter):
                    """
                    Parameter Solid of value type bool.
                    """
                    pass

                class Surface(PyParameter):
                    """
                    Parameter Surface of value type bool.
                    """
                    pass

            class Append(PyParameter):
                """
                Parameter Append of value type bool.
                """
                pass

            class ConvertedPath(PyTextual):
                """
                Parameter ConvertedPath of value type str.
                """
                pass

            class Dummy(PyParameter):
                """
                Parameter Dummy of value type bool.
                """
                pass

            class FileUnit(PyTextual):
                """
                Parameter FileUnit of value type str.
                """
                pass

            class IgnoreSolidNames(PyParameter):
                """
                Parameter IgnoreSolidNames of value type bool.
                """
                pass

            class JtLOD(PyTextual):
                """
                Parameter JtLOD of value type str.
                """
                pass

            class Keys(PyParameter):
                """
                Parameter Keys of value type list[int].
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class PartPerBody(PyParameter):
                """
                Parameter PartPerBody of value type bool.
                """
                pass

            class Path(PyTextual):
                """
                Parameter Path of value type str.
                """
                pass

            class PrefixParentName(PyParameter):
                """
                Parameter PrefixParentName of value type bool.
                """
                pass

            class RemoveEmptyParts(PyParameter):
                """
                Parameter RemoveEmptyParts of value type bool.
                """
                pass

            class Route(PyTextual):
                """
                Parameter Route of value type str.
                """
                pass

            class Updated(PyParameter):
                """
                Parameter Updated of value type bool.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _File:
            return super().__getitem__(key)

    class FileManager(PyMenu):
        """
        Singleton FileManager.
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.DeleteCadKey = self.__class__.DeleteCadKey(service, rules, "DeleteCadKey", path)
            self.LoadFiles = self.__class__.LoadFiles(service, rules, "LoadFiles", path)
            self.Reload = self.__class__.Reload(service, rules, "Reload", path)
            self.Unload = self.__class__.Unload(service, rules, "Unload", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            Parameter Children of value type list[str].
            """
            pass

        class Name(PyTextual):
            """
            Parameter Name of value type str.
            """
            pass

        class DeleteCadKey(PyCommand):
            """
            Command DeleteCadKey.

            Parameters
            ----------
            Key : int

            Returns
            -------
            bool
            """
            class _DeleteCadKeyArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Key = self._Key(self, "Key", service, rules, path)

                class _Key(PyArgumentsNumericalSubItem):
                    """
                    Argument Key.
                    """

            def create_instance(self) -> _DeleteCadKeyArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteCadKeyArguments(*args)

        class LoadFiles(PyCommand):
            """
            Command LoadFiles.


            Returns
            -------
            bool
            """
            class _LoadFilesArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _LoadFilesArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._LoadFilesArguments(*args)

        class Reload(PyCommand):
            """
            Command Reload.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            class _ReloadArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReloadArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReloadArguments(*args)

        class Unload(PyCommand):
            """
            Command Unload.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            class _UnloadArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _UnloadArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UnloadArguments(*args)

