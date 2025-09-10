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
    PyCommandArguments,
    PyTextualCommandArgumentsSubItem,
    PyNumericalCommandArgumentsSubItem,
    PyDictionaryCommandArgumentsSubItem,
    PyParameterCommandArgumentsSubItem,
    PySingletonCommandArgumentsSubItem
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.Case = self.__class__.Case(service, rules, path + [("Case", "")])
        super().__init__(service, rules, path)

    class Case(PyMenu):
        """
        Singleton Case.
        """
        def __init__(self, service, rules, path):
            self.App = self.__class__.App(service, rules, path + [("App", "")])
            self.AppLocal = self.__class__.AppLocal(service, rules, path + [("AppLocal", "")])
            self.AuxiliaryInfo = self.__class__.AuxiliaryInfo(service, rules, path + [("AuxiliaryInfo", "")])
            self.CaseInfo = self.__class__.CaseInfo(service, rules, path + [("CaseInfo", "")])
            self.MeshInfo = self.__class__.MeshInfo(service, rules, path + [("MeshInfo", "")])
            self.Results = self.__class__.Results(service, rules, path + [("Results", "")])
            self.ResultsInfo = self.__class__.ResultsInfo(service, rules, path + [("ResultsInfo", "")])
            self.Setup = self.__class__.Setup(service, rules, path + [("Setup", "")])
            self.Solution = self.__class__.Solution(service, rules, path + [("Solution", "")])
            self.Streaming = self.__class__.Streaming(service, rules, path + [("Streaming", "")])
            self.AppName = self.__class__.AppName(service, rules, path + [("AppName", "")])
            self.ClearDatamodel = self.__class__.ClearDatamodel(service, rules, "ClearDatamodel", path)
            self.ReadCase = self.__class__.ReadCase(service, rules, "ReadCase", path)
            self.ReadCaseAndData = self.__class__.ReadCaseAndData(service, rules, "ReadCaseAndData", path)
            self.ReadData = self.__class__.ReadData(service, rules, "ReadData", path)
            self.SendCommand = self.__class__.SendCommand(service, rules, "SendCommand", path)
            self.WriteCase = self.__class__.WriteCase(service, rules, "WriteCase", path)
            self.WriteCaseAndData = self.__class__.WriteCaseAndData(service, rules, "WriteCaseAndData", path)
            self.WriteData = self.__class__.WriteData(service, rules, "WriteData", path)
            super().__init__(service, rules, path)

        class App(PyMenu):
            """
            Singleton App.
            """
            def __init__(self, service, rules, path):
                super().__init__(service, rules, path)

        class AppLocal(PyMenu):
            """
            Singleton AppLocal.
            """
            def __init__(self, service, rules, path):
                super().__init__(service, rules, path)

        class AuxiliaryInfo(PyMenu):
            """
            Singleton AuxiliaryInfo.
            """
            def __init__(self, service, rules, path):
                self.DefaultField = self.__class__.DefaultField(service, rules, path + [("DefaultField", "")])
                self.DefaultVectorField = self.__class__.DefaultVectorField(service, rules, path + [("DefaultVectorField", "")])
                self.FluentBoundaryZones = self.__class__.FluentBoundaryZones(service, rules, path + [("FluentBoundaryZones", "")])
                self.IsCourantNumberActive = self.__class__.IsCourantNumberActive(service, rules, path + [("IsCourantNumberActive", "")])
                self.IsDPMWallFilmBC = self.__class__.IsDPMWallFilmBC(service, rules, path + [("IsDPMWallFilmBC", "")])
                self.IsOversetReadOnly = self.__class__.IsOversetReadOnly(service, rules, path + [("IsOversetReadOnly", "")])
                self.IsPVCouplingActive = self.__class__.IsPVCouplingActive(service, rules, path + [("IsPVCouplingActive", "")])
                self.IsSgPDFTransport = self.__class__.IsSgPDFTransport(service, rules, path + [("IsSgPDFTransport", "")])
                self.IsUnsteadyParticleTracking = self.__class__.IsUnsteadyParticleTracking(service, rules, path + [("IsUnsteadyParticleTracking", "")])
                self.MultiPhaseDomainList = self.__class__.MultiPhaseDomainList(service, rules, path + [("MultiPhaseDomainList", "")])
                self.MultiPhaseModel = self.__class__.MultiPhaseModel(service, rules, path + [("MultiPhaseModel", "")])
                self.TimeStepSpecification = self.__class__.TimeStepSpecification(service, rules, path + [("TimeStepSpecification", "")])
                super().__init__(service, rules, path)

            class DefaultField(PyTextual):
                """
                Parameter DefaultField of value type str.
                """
                pass

            class DefaultVectorField(PyTextual):
                """
                Parameter DefaultVectorField of value type str.
                """
                pass

            class FluentBoundaryZones(PyTextual):
                """
                Parameter FluentBoundaryZones of value type list[str].
                """
                pass

            class IsCourantNumberActive(PyParameter):
                """
                Parameter IsCourantNumberActive of value type bool.
                """
                pass

            class IsDPMWallFilmBC(PyParameter):
                """
                Parameter IsDPMWallFilmBC of value type bool.
                """
                pass

            class IsOversetReadOnly(PyParameter):
                """
                Parameter IsOversetReadOnly of value type bool.
                """
                pass

            class IsPVCouplingActive(PyParameter):
                """
                Parameter IsPVCouplingActive of value type bool.
                """
                pass

            class IsSgPDFTransport(PyParameter):
                """
                Parameter IsSgPDFTransport of value type bool.
                """
                pass

            class IsUnsteadyParticleTracking(PyParameter):
                """
                Parameter IsUnsteadyParticleTracking of value type bool.
                """
                pass

            class MultiPhaseDomainList(PyTextual):
                """
                Parameter MultiPhaseDomainList of value type list[str].
                """
                pass

            class MultiPhaseModel(PyTextual):
                """
                Parameter MultiPhaseModel of value type str.
                """
                pass

            class TimeStepSpecification(PyParameter):
                """
                Parameter TimeStepSpecification of value type bool.
                """
                pass

        class CaseInfo(PyMenu):
            """
            Singleton CaseInfo.
            """
            def __init__(self, service, rules, path):
                self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                self.CaseFileNameDirStripped = self.__class__.CaseFileNameDirStripped(service, rules, path + [("CaseFileNameDirStripped", "")])
                self.Configuration = self.__class__.Configuration(service, rules, path + [("Configuration", "")])
                self.Dimension = self.__class__.Dimension(service, rules, path + [("Dimension", "")])
                self.HostName = self.__class__.HostName(service, rules, path + [("HostName", "")])
                self.IsEduOnlyLogo = self.__class__.IsEduOnlyLogo(service, rules, path + [("IsEduOnlyLogo", "")])
                self.IsStudentOnly = self.__class__.IsStudentOnly(service, rules, path + [("IsStudentOnly", "")])
                self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                super().__init__(service, rules, path)

            class CaseFileName(PyTextual):
                """
                Parameter CaseFileName of value type str.
                """
                pass

            class CaseFileNameDirStripped(PyTextual):
                """
                Parameter CaseFileNameDirStripped of value type str.
                """
                pass

            class Configuration(PyTextual):
                """
                Parameter Configuration of value type str.
                """
                pass

            class Dimension(PyTextual):
                """
                Parameter Dimension of value type str.
                """
                pass

            class HostName(PyTextual):
                """
                Parameter HostName of value type str.
                """
                pass

            class IsEduOnlyLogo(PyParameter):
                """
                Parameter IsEduOnlyLogo of value type bool.
                """
                pass

            class IsStudentOnly(PyParameter):
                """
                Parameter IsStudentOnly of value type bool.
                """
                pass

            class SolverName(PyTextual):
                """
                Parameter SolverName of value type str.
                """
                pass

        class MeshInfo(PyMenu):
            """
            Singleton MeshInfo.
            """
            def __init__(self, service, rules, path):
                self.MeshExtents = self.__class__.MeshExtents(service, rules, path + [("MeshExtents", "")])
                super().__init__(service, rules, path)

            class MeshExtents(PyMenu):
                """
                Singleton MeshExtents.
                """
                def __init__(self, service, rules, path):
                    self.XMax = self.__class__.XMax(service, rules, path + [("XMax", "")])
                    self.XMin = self.__class__.XMin(service, rules, path + [("XMin", "")])
                    self.YMax = self.__class__.YMax(service, rules, path + [("YMax", "")])
                    self.YMin = self.__class__.YMin(service, rules, path + [("YMin", "")])
                    self.ZMax = self.__class__.ZMax(service, rules, path + [("ZMax", "")])
                    self.ZMin = self.__class__.ZMin(service, rules, path + [("ZMin", "")])
                    super().__init__(service, rules, path)

                class XMax(PyNumerical):
                    """
                    Parameter XMax of value type float.
                    """
                    pass

                class XMin(PyNumerical):
                    """
                    Parameter XMin of value type float.
                    """
                    pass

                class YMax(PyNumerical):
                    """
                    Parameter YMax of value type float.
                    """
                    pass

                class YMin(PyNumerical):
                    """
                    Parameter YMin of value type float.
                    """
                    pass

                class ZMax(PyNumerical):
                    """
                    Parameter ZMax of value type float.
                    """
                    pass

                class ZMin(PyNumerical):
                    """
                    Parameter ZMin of value type float.
                    """
                    pass

        class Results(PyMenu):
            """
            Singleton Results.
            """
            def __init__(self, service, rules, path):
                self.Reports = self.__class__.Reports(service, rules, path + [("Reports", "")])
                self.SurfaceDefs = self.__class__.SurfaceDefs(service, rules, path + [("SurfaceDefs", "")])
                self.View = self.__class__.View(service, rules, path + [("View", "")])
                self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                self.Plots = self.__class__.Plots(service, rules, path + [("Plots", "")])
                self.ResultsExternalInfo = self.__class__.ResultsExternalInfo(service, rules, path + [("ResultsExternalInfo", "")])
                self.CreateCellZoneSurfaces = self.__class__.CreateCellZoneSurfaces(service, rules, "CreateCellZoneSurfaces", path)
                self.CreateMultipleIsosurfaces = self.__class__.CreateMultipleIsosurfaces(service, rules, "CreateMultipleIsosurfaces", path)
                self.CreateMultiplePlanes = self.__class__.CreateMultiplePlanes(service, rules, "CreateMultiplePlanes", path)
                self.GetFieldMinMax = self.__class__.GetFieldMinMax(service, rules, "GetFieldMinMax", path)
                self.GetXYData = self.__class__.GetXYData(service, rules, "GetXYData", path)
                super().__init__(service, rules, path)

            class Reports(PyNamedObjectContainer):
                """
                .
                """
                class _Reports(PyMenu):
                    """
                    Singleton _Reports.
                    """
                    def __init__(self, service, rules, path):
                        self.DensityConstant = self.__class__.DensityConstant(service, rules, path + [("DensityConstant", "")])
                        self.DensityField = self.__class__.DensityField(service, rules, path + [("DensityField", "")])
                        self.DensitySpecification = self.__class__.DensitySpecification(service, rules, path + [("DensitySpecification", "")])
                        self.Expression = self.__class__.Expression(service, rules, path + [("Expression", "")])
                        self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                        self.ForEach = self.__class__.ForEach(service, rules, path + [("ForEach", "")])
                        self.Quantity = self.__class__.Quantity(service, rules, path + [("Quantity", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self.VelocityField = self.__class__.VelocityField(service, rules, path + [("VelocityField", "")])
                        self.VolumeFractionField = self.__class__.VolumeFractionField(service, rules, path + [("VolumeFractionField", "")])
                        self.Volumes = self.__class__.Volumes(service, rules, path + [("Volumes", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.GetReport = self.__class__.GetReport(service, rules, "GetReport", path)
                        self.PlotReport = self.__class__.PlotReport(service, rules, "PlotReport", path)
                        self.PrintReport = self.__class__.PrintReport(service, rules, "PrintReport", path)
                        self.SaveReport = self.__class__.SaveReport(service, rules, "SaveReport", path)
                        super().__init__(service, rules, path)

                    class DensityConstant(PyNumerical):
                        """
                        Parameter DensityConstant of value type float.
                        """
                        pass

                    class DensityField(PyTextual):
                        """
                        Parameter DensityField of value type str.
                        """
                        pass

                    class DensitySpecification(PyTextual):
                        """
                        Parameter DensitySpecification of value type str.
                        """
                        pass

                    class Expression(PyTextual):
                        """
                        Parameter Expression of value type str.
                        """
                        pass

                    class Field(PyTextual):
                        """
                        Parameter Field of value type str.
                        """
                        pass

                    class ForEach(PyParameter):
                        """
                        Parameter ForEach of value type bool.
                        """
                        pass

                    class Quantity(PyTextual):
                        """
                        Parameter Quantity of value type str.
                        """
                        pass

                    class Surfaces(PyTextual):
                        """
                        Parameter Surfaces of value type list[str].
                        """
                        pass

                    class Type(PyTextual):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class VelocityField(PyTextual):
                        """
                        Parameter VelocityField of value type str.
                        """
                        pass

                    class VolumeFractionField(PyTextual):
                        """
                        Parameter VolumeFractionField of value type str.
                        """
                        pass

                    class Volumes(PyTextual):
                        """
                        Parameter Volumes of value type list[str].
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class GetReport(PyCommand):
                        """
                        Command GetReport.

                        Parameters
                        ----------
                        TimestepSelection : dict[str, Any]

                        Returns
                        -------
                        list[float]
                        """
                        class _GetReportCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.TimestepSelection = self._TimestepSelection(self, "TimestepSelection", service, rules, path)

                            class _TimestepSelection(PySingletonCommandArgumentsSubItem):
                                """
                                Argument TimestepSelection.
                                """

                                def __init__(self, parent, attr, service, rules, path):
                                    super().__init__(parent, attr, service, rules, path)
                                    self.Increment = self._Increment(self, "Increment", service, rules, path)
                                    self.Option = self._Option(self, "Option", service, rules, path)
                                    self.Begin = self._Begin(self, "Begin", service, rules, path)
                                    self.End = self._End(self, "End", service, rules, path)

                                class _Increment(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Increment.
                                    """

                                class _Option(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Option.
                                    """

                                class _Begin(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Begin.
                                    """

                                class _End(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument End.
                                    """

                        def create_instance(self) -> _GetReportCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._GetReportCommandArguments(*args)

                    class PlotReport(PyCommand):
                        """
                        Command PlotReport.

                        Parameters
                        ----------
                        TimestepSelection : dict[str, Any]
                        Title : str
                        XAxis : str
                        XAxisLabel : str
                        YAxisLabel : str

                        Returns
                        -------
                        None
                        """
                        class _PlotReportCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.TimestepSelection = self._TimestepSelection(self, "TimestepSelection", service, rules, path)
                                self.Title = self._Title(self, "Title", service, rules, path)
                                self.XAxis = self._XAxis(self, "XAxis", service, rules, path)
                                self.XAxisLabel = self._XAxisLabel(self, "XAxisLabel", service, rules, path)
                                self.YAxisLabel = self._YAxisLabel(self, "YAxisLabel", service, rules, path)

                            class _TimestepSelection(PySingletonCommandArgumentsSubItem):
                                """
                                Argument TimestepSelection.
                                """

                                def __init__(self, parent, attr, service, rules, path):
                                    super().__init__(parent, attr, service, rules, path)
                                    self.Increment = self._Increment(self, "Increment", service, rules, path)
                                    self.Option = self._Option(self, "Option", service, rules, path)
                                    self.Begin = self._Begin(self, "Begin", service, rules, path)
                                    self.End = self._End(self, "End", service, rules, path)

                                class _Increment(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Increment.
                                    """

                                class _Option(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Option.
                                    """

                                class _Begin(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Begin.
                                    """

                                class _End(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument End.
                                    """

                            class _Title(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Title.
                                """

                            class _XAxis(PyTextualCommandArgumentsSubItem):
                                """
                                Argument XAxis.
                                """

                            class _XAxisLabel(PyTextualCommandArgumentsSubItem):
                                """
                                Argument XAxisLabel.
                                """

                            class _YAxisLabel(PyTextualCommandArgumentsSubItem):
                                """
                                Argument YAxisLabel.
                                """

                        def create_instance(self) -> _PlotReportCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._PlotReportCommandArguments(*args)

                    class PrintReport(PyCommand):
                        """
                        Command PrintReport.

                        Parameters
                        ----------
                        TimestepSelection : dict[str, Any]

                        Returns
                        -------
                        None
                        """
                        class _PrintReportCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.TimestepSelection = self._TimestepSelection(self, "TimestepSelection", service, rules, path)

                            class _TimestepSelection(PySingletonCommandArgumentsSubItem):
                                """
                                Argument TimestepSelection.
                                """

                                def __init__(self, parent, attr, service, rules, path):
                                    super().__init__(parent, attr, service, rules, path)
                                    self.Increment = self._Increment(self, "Increment", service, rules, path)
                                    self.Option = self._Option(self, "Option", service, rules, path)
                                    self.Begin = self._Begin(self, "Begin", service, rules, path)
                                    self.End = self._End(self, "End", service, rules, path)

                                class _Increment(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Increment.
                                    """

                                class _Option(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Option.
                                    """

                                class _Begin(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Begin.
                                    """

                                class _End(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument End.
                                    """

                        def create_instance(self) -> _PrintReportCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._PrintReportCommandArguments(*args)

                    class SaveReport(PyCommand):
                        """
                        Command SaveReport.

                        Parameters
                        ----------
                        Filename : str
                        TimestepSelection : dict[str, Any]

                        Returns
                        -------
                        None
                        """
                        class _SaveReportCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.Filename = self._Filename(self, "Filename", service, rules, path)
                                self.TimestepSelection = self._TimestepSelection(self, "TimestepSelection", service, rules, path)

                            class _Filename(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Filename.
                                """

                            class _TimestepSelection(PySingletonCommandArgumentsSubItem):
                                """
                                Argument TimestepSelection.
                                """

                                def __init__(self, parent, attr, service, rules, path):
                                    super().__init__(parent, attr, service, rules, path)
                                    self.Increment = self._Increment(self, "Increment", service, rules, path)
                                    self.Option = self._Option(self, "Option", service, rules, path)
                                    self.Begin = self._Begin(self, "Begin", service, rules, path)
                                    self.End = self._End(self, "End", service, rules, path)

                                class _Increment(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Increment.
                                    """

                                class _Option(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Option.
                                    """

                                class _Begin(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Begin.
                                    """

                                class _End(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument End.
                                    """

                        def create_instance(self) -> _SaveReportCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._SaveReportCommandArguments(*args)

                def __getitem__(self, key: str) -> _Reports:
                    return super().__getitem__(key)

            class SurfaceDefs(PyNamedObjectContainer):
                """
                .
                """
                class _SurfaceDefs(PyMenu):
                    """
                    Singleton _SurfaceDefs.
                    """
                    def __init__(self, service, rules, path):
                        self.IsoClipSettings = self.__class__.IsoClipSettings(service, rules, path + [("IsoClipSettings", "")])
                        self.IsosurfaceSettings = self.__class__.IsosurfaceSettings(service, rules, path + [("IsosurfaceSettings", "")])
                        self.LineSettings = self.__class__.LineSettings(service, rules, path + [("LineSettings", "")])
                        self.PlaneSettings = self.__class__.PlaneSettings(service, rules, path + [("PlaneSettings", "")])
                        self.PointSettings = self.__class__.PointSettings(service, rules, path + [("PointSettings", "")])
                        self.RakeSettings = self.__class__.RakeSettings(service, rules, path + [("RakeSettings", "")])
                        self.ZoneSettings = self.__class__.ZoneSettings(service, rules, path + [("ZoneSettings", "")])
                        self.GroupName = self.__class__.GroupName(service, rules, path + [("GroupName", "")])
                        self.SurfaceDim = self.__class__.SurfaceDim(service, rules, path + [("SurfaceDim", "")])
                        self.SurfaceId = self.__class__.SurfaceId(service, rules, path + [("SurfaceId", "")])
                        self.SurfaceType = self.__class__.SurfaceType(service, rules, path + [("SurfaceType", "")])
                        self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.Display = self.__class__.Display(service, rules, "Display", path)
                        self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                        self.Ungroup = self.__class__.Ungroup(service, rules, "Ungroup", path)
                        super().__init__(service, rules, path)

                    class IsoClipSettings(PyMenu):
                        """
                        Singleton IsoClipSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Maximum(PyNumerical):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class Minimum(PyNumerical):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            class _UpdateMinMaxCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _UpdateMinMaxCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._UpdateMinMaxCommandArguments(*args)

                    class IsosurfaceSettings(PyMenu):
                        """
                        Singleton IsosurfaceSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.IsoValue = self.__class__.IsoValue(service, rules, path + [("IsoValue", "")])
                            self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                            self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                            self.RestrictToSpecificSurfaces = self.__class__.RestrictToSpecificSurfaces(service, rules, path + [("RestrictToSpecificSurfaces", "")])
                            self.RestrictToSpecificZones = self.__class__.RestrictToSpecificZones(service, rules, path + [("RestrictToSpecificZones", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.Zones = self.__class__.Zones(service, rules, path + [("Zones", "")])
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class IsoValue(PyNumerical):
                            """
                            Parameter IsoValue of value type float.
                            """
                            pass

                        class Maximum(PyNumerical):
                            """
                            Parameter Maximum of value type float.
                            """
                            pass

                        class Minimum(PyNumerical):
                            """
                            Parameter Minimum of value type float.
                            """
                            pass

                        class RestrictToSpecificSurfaces(PyParameter):
                            """
                            Parameter RestrictToSpecificSurfaces of value type bool.
                            """
                            pass

                        class RestrictToSpecificZones(PyParameter):
                            """
                            Parameter RestrictToSpecificZones of value type bool.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class Zones(PyTextual):
                            """
                            Parameter Zones of value type list[str].
                            """
                            pass

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            class _UpdateMinMaxCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _UpdateMinMaxCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._UpdateMinMaxCommandArguments(*args)

                    class LineSettings(PyMenu):
                        """
                        Singleton LineSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                    class PlaneSettings(PyMenu):
                        """
                        Singleton PlaneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.FirstPoint = self.__class__.FirstPoint(service, rules, path + [("FirstPoint", "")])
                            self.Normal = self.__class__.Normal(service, rules, path + [("Normal", "")])
                            self.SecondPoint = self.__class__.SecondPoint(service, rules, path + [("SecondPoint", "")])
                            self.ThirdPoint = self.__class__.ThirdPoint(service, rules, path + [("ThirdPoint", "")])
                            self.Bounded = self.__class__.Bounded(service, rules, path + [("Bounded", "")])
                            self.CreationMode = self.__class__.CreationMode(service, rules, path + [("CreationMode", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class FirstPoint(PyMenu):
                            """
                            Singleton FirstPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class Normal(PyMenu):
                            """
                            Singleton Normal.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class SecondPoint(PyMenu):
                            """
                            Singleton SecondPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class ThirdPoint(PyMenu):
                            """
                            Singleton ThirdPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class Bounded(PyParameter):
                            """
                            Parameter Bounded of value type bool.
                            """
                            pass

                        class CreationMode(PyTextual):
                            """
                            Parameter CreationMode of value type str.
                            """
                            pass

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class PointSettings(PyMenu):
                        """
                        Singleton PointSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.LbClipping = self.__class__.LbClipping(service, rules, path + [("LbClipping", "")])
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class LbClipping(PyParameter):
                            """
                            Parameter LbClipping of value type bool.
                            """
                            pass

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class RakeSettings(PyMenu):
                        """
                        Singleton RakeSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.EndPoint = self.__class__.EndPoint(service, rules, path + [("EndPoint", "")])
                            self.StartPoint = self.__class__.StartPoint(service, rules, path + [("StartPoint", "")])
                            self.NumberOfPoints = self.__class__.NumberOfPoints(service, rules, path + [("NumberOfPoints", "")])
                            super().__init__(service, rules, path)

                        class EndPoint(PyMenu):
                            """
                            Singleton EndPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class StartPoint(PyMenu):
                            """
                            Singleton StartPoint.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class NumberOfPoints(PyNumerical):
                            """
                            Parameter NumberOfPoints of value type int.
                            """
                            pass

                    class ZoneSettings(PyMenu):
                        """
                        Singleton ZoneSettings.
                        """
                        def __init__(self, service, rules, path):
                            self.IdList = self.__class__.IdList(service, rules, path + [("IdList", "")])
                            self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                            self.ZId = self.__class__.ZId(service, rules, path + [("ZId", "")])
                            self.ZType = self.__class__.ZType(service, rules, path + [("ZType", "")])
                            super().__init__(service, rules, path)

                        class IdList(PyParameter):
                            """
                            Parameter IdList of value type list[int].
                            """
                            pass

                        class Type(PyTextual):
                            """
                            Parameter Type of value type str.
                            """
                            pass

                        class ZId(PyNumerical):
                            """
                            Parameter ZId of value type int.
                            """
                            pass

                        class ZType(PyTextual):
                            """
                            Parameter ZType of value type str.
                            """
                            pass

                    class GroupName(PyTextual):
                        """
                        Parameter GroupName of value type str.
                        """
                        pass

                    class SurfaceDim(PyTextual):
                        """
                        Parameter SurfaceDim of value type list[str].
                        """
                        pass

                    class SurfaceId(PyNumerical):
                        """
                        Parameter SurfaceId of value type int.
                        """
                        pass

                    class SurfaceType(PyTextual):
                        """
                        Parameter SurfaceType of value type str.
                        """
                        pass

                    class Surfaces(PyTextual):
                        """
                        Parameter Surfaces of value type list[str].
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class Display(PyCommand):
                        """
                        Command Display.


                        Returns
                        -------
                        bool
                        """
                        class _DisplayCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)

                        def create_instance(self) -> _DisplayCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._DisplayCommandArguments(*args)

                    class SaveImage(PyCommand):
                        """
                        Command SaveImage.

                        Parameters
                        ----------
                        FileName : str
                        Format : str
                        FileType : str
                        Coloring : str
                        Orientation : str
                        UseWhiteBackground : bool
                        Resolution : dict[str, Any]

                        Returns
                        -------
                        bool
                        """
                        class _SaveImageCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.FileName = self._FileName(self, "FileName", service, rules, path)
                                self.Format = self._Format(self, "Format", service, rules, path)
                                self.FileType = self._FileType(self, "FileType", service, rules, path)
                                self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                            class _FileName(PyTextualCommandArgumentsSubItem):
                                """
                                Argument FileName.
                                """

                            class _Format(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Format.
                                """

                            class _FileType(PyTextualCommandArgumentsSubItem):
                                """
                                Argument FileType.
                                """

                            class _Coloring(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Coloring.
                                """

                            class _Orientation(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Orientation.
                                """

                            class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                """
                                Argument UseWhiteBackground.
                                """

                            class _Resolution(PySingletonCommandArgumentsSubItem):
                                """
                                Argument Resolution.
                                """

                                def __init__(self, parent, attr, service, rules, path):
                                    super().__init__(parent, attr, service, rules, path)
                                    self.DPI = self._DPI(self, "DPI", service, rules, path)
                                    self.Option = self._Option(self, "Option", service, rules, path)
                                    self.Width = self._Width(self, "Width", service, rules, path)
                                    self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                    self.Height = self._Height(self, "Height", service, rules, path)

                                class _DPI(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument DPI.
                                    """

                                class _Option(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Option.
                                    """

                                class _Width(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Width.
                                    """

                                class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWindowResolution.
                                    """

                                class _Height(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument Height.
                                    """

                        def create_instance(self) -> _SaveImageCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._SaveImageCommandArguments(*args)

                    class Ungroup(PyCommand):
                        """
                        Command Ungroup.


                        Returns
                        -------
                        bool
                        """
                        class _UngroupCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)

                        def create_instance(self) -> _UngroupCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._UngroupCommandArguments(*args)

                def __getitem__(self, key: str) -> _SurfaceDefs:
                    return super().__getitem__(key)

            class View(PyNamedObjectContainer):
                """
                .
                """
                class _View(PyMenu):
                    """
                    Singleton _View.
                    """
                    def __init__(self, service, rules, path):
                        self.Camera = self.__class__.Camera(service, rules, path + [("Camera", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.RestoreView = self.__class__.RestoreView(service, rules, "RestoreView", path)
                        super().__init__(service, rules, path)

                    class Camera(PyMenu):
                        """
                        Singleton Camera.
                        """
                        def __init__(self, service, rules, path):
                            self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                            self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                            self.UpVector = self.__class__.UpVector(service, rules, path + [("UpVector", "")])
                            self.Height = self.__class__.Height(service, rules, path + [("Height", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.Width = self.__class__.Width(service, rules, path + [("Width", "")])
                            super().__init__(service, rules, path)

                        class Position(PyMenu):
                            """
                            Singleton Position.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Target(PyMenu):
                            """
                            Singleton Target.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class UpVector(PyMenu):
                            """
                            Singleton UpVector.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Height(PyNumerical):
                            """
                            Parameter Height of value type float.
                            """
                            pass

                        class Projection(PyTextual):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class Width(PyNumerical):
                            """
                            Parameter Width of value type float.
                            """
                            pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class RestoreView(PyCommand):
                        """
                        Command RestoreView.


                        Returns
                        -------
                        bool
                        """
                        class _RestoreViewCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)

                        def create_instance(self) -> _RestoreViewCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._RestoreViewCommandArguments(*args)

                def __getitem__(self, key: str) -> _View:
                    return super().__getitem__(key)

            class Graphics(PyMenu):
                """
                Singleton Graphics.
                """
                def __init__(self, service, rules, path):
                    self.Contour = self.__class__.Contour(service, rules, path + [("Contour", "")])
                    self.LIC = self.__class__.LIC(service, rules, path + [("LIC", "")])
                    self.Mesh = self.__class__.Mesh(service, rules, path + [("Mesh", "")])
                    self.ParticleTracks = self.__class__.ParticleTracks(service, rules, path + [("ParticleTracks", "")])
                    self.Pathlines = self.__class__.Pathlines(service, rules, path + [("Pathlines", "")])
                    self.Scene = self.__class__.Scene(service, rules, path + [("Scene", "")])
                    self.Vector = self.__class__.Vector(service, rules, path + [("Vector", "")])
                    self.XYPlot = self.__class__.XYPlot(service, rules, path + [("XYPlot", "")])
                    self.CameraSettings = self.__class__.CameraSettings(service, rules, path + [("CameraSettings", "")])
                    self.GridColors = self.__class__.GridColors(service, rules, path + [("GridColors", "")])
                    self.GraphicsCreationCount = self.__class__.GraphicsCreationCount(service, rules, path + [("GraphicsCreationCount", "")])
                    self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                    super().__init__(service, rules, path)

                class Contour(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Contour(PyMenu):
                        """
                        Singleton _Contour.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.BoundaryValues = self.__class__.BoundaryValues(service, rules, path + [("BoundaryValues", "")])
                            self.Coloring = self.__class__.Coloring(service, rules, path + [("Coloring", "")])
                            self.ContourLines = self.__class__.ContourLines(service, rules, path + [("ContourLines", "")])
                            self.DisplayLIC = self.__class__.DisplayLIC(service, rules, path + [("DisplayLIC", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.Filled = self.__class__.Filled(service, rules, path + [("Filled", "")])
                            self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class BoundaryValues(PyParameter):
                            """
                            Parameter BoundaryValues of value type bool.
                            """
                            pass

                        class Coloring(PyTextual):
                            """
                            Parameter Coloring of value type str.
                            """
                            pass

                        class ContourLines(PyParameter):
                            """
                            Parameter ContourLines of value type bool.
                            """
                            pass

                        class DisplayLIC(PyParameter):
                            """
                            Parameter DisplayLIC of value type bool.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class Filled(PyParameter):
                            """
                            Parameter Filled of value type bool.
                            """
                            pass

                        class NodeValues(PyParameter):
                            """
                            Parameter NodeValues of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _AddToViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _AddToViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._AddToViewportCommandArguments(*args)

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _DisplayInViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _DisplayInViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayInViewportCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            class _UpdateMinMaxCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _UpdateMinMaxCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._UpdateMinMaxCommandArguments(*args)

                    def __getitem__(self, key: str) -> _Contour:
                        return super().__getitem__(key)

                class LIC(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _LIC(PyMenu):
                        """
                        Singleton _LIC.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.FastLic = self.__class__.FastLic(service, rules, path + [("FastLic", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.GrayScale = self.__class__.GrayScale(service, rules, path + [("GrayScale", "")])
                            self.ImageFilter = self.__class__.ImageFilter(service, rules, path + [("ImageFilter", "")])
                            self.ImageToDisplay = self.__class__.ImageToDisplay(service, rules, path + [("ImageToDisplay", "")])
                            self.IntensityAlpha = self.__class__.IntensityAlpha(service, rules, path + [("IntensityAlpha", "")])
                            self.IntensityFactor = self.__class__.IntensityFactor(service, rules, path + [("IntensityFactor", "")])
                            self.LicColor = self.__class__.LicColor(service, rules, path + [("LicColor", "")])
                            self.LicColorByField = self.__class__.LicColorByField(service, rules, path + [("LicColorByField", "")])
                            self.LicMaxSteps = self.__class__.LicMaxSteps(service, rules, path + [("LicMaxSteps", "")])
                            self.LicNormalize = self.__class__.LicNormalize(service, rules, path + [("LicNormalize", "")])
                            self.LicPixelInterp = self.__class__.LicPixelInterp(service, rules, path + [("LicPixelInterp", "")])
                            self.OrientedLic = self.__class__.OrientedLic(service, rules, path + [("OrientedLic", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.TextureSize = self.__class__.TextureSize(service, rules, path + [("TextureSize", "")])
                            self.TextureSpacing = self.__class__.TextureSpacing(service, rules, path + [("TextureSpacing", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class FastLic(PyParameter):
                            """
                            Parameter FastLic of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class GrayScale(PyParameter):
                            """
                            Parameter GrayScale of value type bool.
                            """
                            pass

                        class ImageFilter(PyTextual):
                            """
                            Parameter ImageFilter of value type str.
                            """
                            pass

                        class ImageToDisplay(PyTextual):
                            """
                            Parameter ImageToDisplay of value type str.
                            """
                            pass

                        class IntensityAlpha(PyParameter):
                            """
                            Parameter IntensityAlpha of value type bool.
                            """
                            pass

                        class IntensityFactor(PyNumerical):
                            """
                            Parameter IntensityFactor of value type int.
                            """
                            pass

                        class LicColor(PyTextual):
                            """
                            Parameter LicColor of value type str.
                            """
                            pass

                        class LicColorByField(PyParameter):
                            """
                            Parameter LicColorByField of value type bool.
                            """
                            pass

                        class LicMaxSteps(PyNumerical):
                            """
                            Parameter LicMaxSteps of value type int.
                            """
                            pass

                        class LicNormalize(PyParameter):
                            """
                            Parameter LicNormalize of value type bool.
                            """
                            pass

                        class LicPixelInterp(PyParameter):
                            """
                            Parameter LicPixelInterp of value type bool.
                            """
                            pass

                        class OrientedLic(PyParameter):
                            """
                            Parameter OrientedLic of value type bool.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class TextureSize(PyNumerical):
                            """
                            Parameter TextureSize of value type int.
                            """
                            pass

                        class TextureSpacing(PyNumerical):
                            """
                            Parameter TextureSpacing of value type int.
                            """
                            pass

                        class VectorField(PyTextual):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _LIC:
                        return super().__getitem__(key)

                class Mesh(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Mesh(PyMenu):
                        """
                        Singleton _Mesh.
                        """
                        def __init__(self, service, rules, path):
                            self.EdgeOptions = self.__class__.EdgeOptions(service, rules, path + [("EdgeOptions", "")])
                            self.MeshColoring = self.__class__.MeshColoring(service, rules, path + [("MeshColoring", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.DisplayLIC = self.__class__.DisplayLIC(service, rules, path + [("DisplayLIC", "")])
                            self.ShrinkFactor = self.__class__.ShrinkFactor(service, rules, path + [("ShrinkFactor", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class EdgeOptions(PyMenu):
                            """
                            Singleton EdgeOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                super().__init__(service, rules, path)

                            class FeatureAngle(PyNumerical):
                                """
                                Parameter FeatureAngle of value type float.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                        class MeshColoring(PyMenu):
                            """
                            Singleton MeshColoring.
                            """
                            def __init__(self, service, rules, path):
                                self.Automatic = self.__class__.Automatic(service, rules, path + [("Automatic", "")])
                                self.ColorBy = self.__class__.ColorBy(service, rules, path + [("ColorBy", "")])
                                self.ColorEdgesBy = self.__class__.ColorEdgesBy(service, rules, path + [("ColorEdgesBy", "")])
                                self.ColorFacesBy = self.__class__.ColorFacesBy(service, rules, path + [("ColorFacesBy", "")])
                                self.ColorNodesBy = self.__class__.ColorNodesBy(service, rules, path + [("ColorNodesBy", "")])
                                super().__init__(service, rules, path)

                            class Automatic(PyParameter):
                                """
                                Parameter Automatic of value type bool.
                                """
                                pass

                            class ColorBy(PyTextual):
                                """
                                Parameter ColorBy of value type str.
                                """
                                pass

                            class ColorEdgesBy(PyTextual):
                                """
                                Parameter ColorEdgesBy of value type str.
                                """
                                pass

                            class ColorFacesBy(PyTextual):
                                """
                                Parameter ColorFacesBy of value type str.
                                """
                                pass

                            class ColorNodesBy(PyTextual):
                                """
                                Parameter ColorNodesBy of value type str.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.Edges = self.__class__.Edges(service, rules, path + [("Edges", "")])
                                self.Faces = self.__class__.Faces(service, rules, path + [("Faces", "")])
                                self.Nodes = self.__class__.Nodes(service, rules, path + [("Nodes", "")])
                                self.Overset = self.__class__.Overset(service, rules, path + [("Overset", "")])
                                self.Partitions = self.__class__.Partitions(service, rules, path + [("Partitions", "")])
                                super().__init__(service, rules, path)

                            class Edges(PyParameter):
                                """
                                Parameter Edges of value type bool.
                                """
                                pass

                            class Faces(PyParameter):
                                """
                                Parameter Faces of value type bool.
                                """
                                pass

                            class Nodes(PyParameter):
                                """
                                Parameter Nodes of value type bool.
                                """
                                pass

                            class Overset(PyParameter):
                                """
                                Parameter Overset of value type bool.
                                """
                                pass

                            class Partitions(PyParameter):
                                """
                                Parameter Partitions of value type bool.
                                """
                                pass

                        class DisplayLIC(PyParameter):
                            """
                            Parameter DisplayLIC of value type bool.
                            """
                            pass

                        class ShrinkFactor(PyNumerical):
                            """
                            Parameter ShrinkFactor of value type float.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _AddToViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _AddToViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._AddToViewportCommandArguments(*args)

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _DisplayInViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _DisplayInViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayInViewportCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _Mesh:
                        return super().__getitem__(key)

                class ParticleTracks(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _ParticleTracks(PyMenu):
                        """
                        Singleton _ParticleTracks.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Filter = self.__class__.Filter(service, rules, path + [("Filter", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.TrackSingleParticleStream = self.__class__.TrackSingleParticleStream(service, rules, path + [("TrackSingleParticleStream", "")])
                            self.VectorStyle = self.__class__.VectorStyle(service, rules, path + [("VectorStyle", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.FreeStreamParticles = self.__class__.FreeStreamParticles(service, rules, path + [("FreeStreamParticles", "")])
                            self.Injections = self.__class__.Injections(service, rules, path + [("Injections", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.ParticleTracksField = self.__class__.ParticleTracksField(service, rules, path + [("ParticleTracksField", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.TrackPDFParticles = self.__class__.TrackPDFParticles(service, rules, path + [("TrackPDFParticles", "")])
                            self.WallFilmParticles = self.__class__.WallFilmParticles(service, rules, path + [("WallFilmParticles", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Filter(PyMenu):
                            """
                            Singleton Filter.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.FilterField = self.__class__.FilterField(service, rules, path + [("FilterField", "")])
                                self.Inside = self.__class__.Inside(service, rules, path + [("Inside", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class FilterField(PyTextual):
                                """
                                Parameter FilterField of value type str.
                                """
                                pass

                            class Inside(PyParameter):
                                """
                                Parameter Inside of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyTextual):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.Sphere = self.__class__.Sphere(service, rules, path + [("Sphere", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class Sphere(PyMenu):
                                """
                                Singleton Sphere.
                                """
                                def __init__(self, service, rules, path):
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.SphereField = self.__class__.SphereField(service, rules, path + [("SphereField", "")])
                                    self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                    self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                    self.VariableSize = self.__class__.VariableSize(service, rules, path + [("VariableSize", "")])
                                    super().__init__(service, rules, path)

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                        self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class MaxValue(PyNumerical):
                                        """
                                        Parameter MaxValue of value type float.
                                        """
                                        pass

                                    class MinValue(PyNumerical):
                                        """
                                        Parameter MinValue of value type float.
                                        """
                                        pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class SphereField(PyTextual):
                                    """
                                    Parameter SphereField of value type str.
                                    """
                                    pass

                                class SphereLod(PyNumerical):
                                    """
                                    Parameter SphereLod of value type int.
                                    """
                                    pass

                                class SphereSize(PyNumerical):
                                    """
                                    Parameter SphereSize of value type float.
                                    """
                                    pass

                                class VariableSize(PyParameter):
                                    """
                                    Parameter VariableSize of value type bool.
                                    """
                                    pass

                            class ArrowScale(PyNumerical):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class ArrowSpace(PyNumerical):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyNumerical):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class MarkerSize(PyNumerical):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class Radius(PyNumerical):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class TrackSingleParticleStream(PyMenu):
                            """
                            Singleton TrackSingleParticleStream.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.StreamId = self.__class__.StreamId(service, rules, path + [("StreamId", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class StreamId(PyNumerical):
                                """
                                Parameter StreamId of value type int.
                                """
                                pass

                        class VectorStyle(PyMenu):
                            """
                            Singleton VectorStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.VectorAttribute = self.__class__.VectorAttribute(service, rules, path + [("VectorAttribute", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class VectorAttribute(PyMenu):
                                """
                                Singleton VectorAttribute.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.ConstantColor = self.__class__.ConstantColor(service, rules, path + [("ConstantColor", "")])
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.Length = self.__class__.Length(service, rules, path + [("Length", "")])
                                    self.LengthToHeadRatio = self.__class__.LengthToHeadRatio(service, rules, path + [("LengthToHeadRatio", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    self.VariableLength = self.__class__.VariableLength(service, rules, path + [("VariableLength", "")])
                                    self.VectorsOf = self.__class__.VectorsOf(service, rules, path + [("VectorsOf", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class ConstantColor(PyParameter):
                                    """
                                    Parameter ConstantColor of value type bool.
                                    """
                                    pass

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class Length(PyNumerical):
                                    """
                                    Parameter Length of value type float.
                                    """
                                    pass

                                class LengthToHeadRatio(PyNumerical):
                                    """
                                    Parameter LengthToHeadRatio of value type float.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                                class VariableLength(PyParameter):
                                    """
                                    Parameter VariableLength of value type bool.
                                    """
                                    pass

                                class VectorsOf(PyTextual):
                                    """
                                    Parameter VectorsOf of value type str.
                                    """
                                    pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class Coarsen(PyNumerical):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class FreeStreamParticles(PyParameter):
                            """
                            Parameter FreeStreamParticles of value type bool.
                            """
                            pass

                        class Injections(PyTextual):
                            """
                            Parameter Injections of value type list[str].
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class ParticleTracksField(PyTextual):
                            """
                            Parameter ParticleTracksField of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class TrackPDFParticles(PyParameter):
                            """
                            Parameter TrackPDFParticles of value type bool.
                            """
                            pass

                        class WallFilmParticles(PyParameter):
                            """
                            Parameter WallFilmParticles of value type bool.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _ParticleTracks:
                        return super().__getitem__(key)

                class Pathlines(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Pathlines(PyMenu):
                        """
                        Singleton _Pathlines.
                        """
                        def __init__(self, service, rules, path):
                            self.AccuracyControl = self.__class__.AccuracyControl(service, rules, path + [("AccuracyControl", "")])
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.Plot = self.__class__.Plot(service, rules, path + [("Plot", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Coarsen = self.__class__.Coarsen(service, rules, path + [("Coarsen", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.OnZone = self.__class__.OnZone(service, rules, path + [("OnZone", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.PathlinesField = self.__class__.PathlinesField(service, rules, path + [("PathlinesField", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Step = self.__class__.Step(service, rules, path + [("Step", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.VelocityDomain = self.__class__.VelocityDomain(service, rules, path + [("VelocityDomain", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class AccuracyControl(PyMenu):
                            """
                            Singleton AccuracyControl.
                            """
                            def __init__(self, service, rules, path):
                                self.AccuracyControlOn = self.__class__.AccuracyControlOn(service, rules, path + [("AccuracyControlOn", "")])
                                self.StepSize = self.__class__.StepSize(service, rules, path + [("StepSize", "")])
                                self.Tolerance = self.__class__.Tolerance(service, rules, path + [("Tolerance", "")])
                                super().__init__(service, rules, path)

                            class AccuracyControlOn(PyParameter):
                                """
                                Parameter AccuracyControlOn of value type bool.
                                """
                                pass

                            class StepSize(PyNumerical):
                                """
                                Parameter StepSize of value type float.
                                """
                                pass

                            class Tolerance(PyNumerical):
                                """
                                Parameter Tolerance of value type float.
                                """
                                pass

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                self.OilFlow = self.__class__.OilFlow(service, rules, path + [("OilFlow", "")])
                                self.Relative = self.__class__.Relative(service, rules, path + [("Relative", "")])
                                self.Reverse = self.__class__.Reverse(service, rules, path + [("Reverse", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                            class OilFlow(PyParameter):
                                """
                                Parameter OilFlow of value type bool.
                                """
                                pass

                            class Relative(PyParameter):
                                """
                                Parameter Relative of value type bool.
                                """
                                pass

                            class Reverse(PyParameter):
                                """
                                Parameter Reverse of value type bool.
                                """
                                pass

                        class Plot(PyMenu):
                            """
                            Singleton Plot.
                            """
                            def __init__(self, service, rules, path):
                                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                                self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                                super().__init__(service, rules, path)

                            class Enabled(PyParameter):
                                """
                                Parameter Enabled of value type bool.
                                """
                                pass

                            class XAxisFunction(PyTextual):
                                """
                                Parameter XAxisFunction of value type str.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Style(PyMenu):
                            """
                            Singleton Style.
                            """
                            def __init__(self, service, rules, path):
                                self.Ribbon = self.__class__.Ribbon(service, rules, path + [("Ribbon", "")])
                                self.ArrowScale = self.__class__.ArrowScale(service, rules, path + [("ArrowScale", "")])
                                self.ArrowSpace = self.__class__.ArrowSpace(service, rules, path + [("ArrowSpace", "")])
                                self.LineWidth = self.__class__.LineWidth(service, rules, path + [("LineWidth", "")])
                                self.MarkerSize = self.__class__.MarkerSize(service, rules, path + [("MarkerSize", "")])
                                self.Radius = self.__class__.Radius(service, rules, path + [("Radius", "")])
                                self.SphereLod = self.__class__.SphereLod(service, rules, path + [("SphereLod", "")])
                                self.SphereSize = self.__class__.SphereSize(service, rules, path + [("SphereSize", "")])
                                self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                                super().__init__(service, rules, path)

                            class Ribbon(PyMenu):
                                """
                                Singleton Ribbon.
                                """
                                def __init__(self, service, rules, path):
                                    self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                    self.ScaleFactor = self.__class__.ScaleFactor(service, rules, path + [("ScaleFactor", "")])
                                    super().__init__(service, rules, path)

                                class Field(PyTextual):
                                    """
                                    Parameter Field of value type str.
                                    """
                                    pass

                                class ScaleFactor(PyNumerical):
                                    """
                                    Parameter ScaleFactor of value type float.
                                    """
                                    pass

                            class ArrowScale(PyNumerical):
                                """
                                Parameter ArrowScale of value type float.
                                """
                                pass

                            class ArrowSpace(PyNumerical):
                                """
                                Parameter ArrowSpace of value type float.
                                """
                                pass

                            class LineWidth(PyNumerical):
                                """
                                Parameter LineWidth of value type float.
                                """
                                pass

                            class MarkerSize(PyNumerical):
                                """
                                Parameter MarkerSize of value type float.
                                """
                                pass

                            class Radius(PyNumerical):
                                """
                                Parameter Radius of value type float.
                                """
                                pass

                            class SphereLod(PyNumerical):
                                """
                                Parameter SphereLod of value type int.
                                """
                                pass

                            class SphereSize(PyNumerical):
                                """
                                Parameter SphereSize of value type float.
                                """
                                pass

                            class Style(PyTextual):
                                """
                                Parameter Style of value type str.
                                """
                                pass

                        class Coarsen(PyNumerical):
                            """
                            Parameter Coarsen of value type int.
                            """
                            pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class OnZone(PyTextual):
                            """
                            Parameter OnZone of value type list[str].
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class PathlinesField(PyTextual):
                            """
                            Parameter PathlinesField of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class Step(PyNumerical):
                            """
                            Parameter Step of value type int.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class UID(PyTextual):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class VelocityDomain(PyTextual):
                            """
                            Parameter VelocityDomain of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _Pathlines:
                        return super().__getitem__(key)

                class Scene(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Scene(PyMenu):
                        """
                        Singleton _Scene.
                        """
                        def __init__(self, service, rules, path):
                            self.GraphicsObjects = self.__class__.GraphicsObjects(service, rules, path + [("GraphicsObjects", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class GraphicsObjects(PyDictionary):
                            """
                            Parameter GraphicsObjects of value type dict[str, Any].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _Scene:
                        return super().__getitem__(key)

                class Vector(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _Vector(PyMenu):
                        """
                        Singleton _Vector.
                        """
                        def __init__(self, service, rules, path):
                            self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                            self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                            self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                            self.VectorOptions = self.__class__.VectorOptions(service, rules, path + [("VectorOptions", "")])
                            self.DrawMesh = self.__class__.DrawMesh(service, rules, path + [("DrawMesh", "")])
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            self.OverlayedMesh = self.__class__.OverlayedMesh(service, rules, path + [("OverlayedMesh", "")])
                            self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                            self.Style = self.__class__.Style(service, rules, path + [("Style", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.VectorField = self.__class__.VectorField(service, rules, path + [("VectorField", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.AddToViewport = self.__class__.AddToViewport(service, rules, "AddToViewport", path)
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.DisplayInViewport = self.__class__.DisplayInViewport(service, rules, "DisplayInViewport", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveAnimation = self.__class__.SaveAnimation(service, rules, "SaveAnimation", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            self.UpdateMinMax = self.__class__.UpdateMinMax(service, rules, "UpdateMinMax", path)
                            super().__init__(service, rules, path)

                        class ColorMap(PyMenu):
                            """
                            Singleton ColorMap.
                            """
                            def __init__(self, service, rules, path):
                                self.ColorMap = self.__class__.ColorMap(service, rules, path + [("ColorMap", "")])
                                self.IsLogScale = self.__class__.IsLogScale(service, rules, path + [("IsLogScale", "")])
                                self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                                self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                self.ShowAll = self.__class__.ShowAll(service, rules, path + [("ShowAll", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Skip = self.__class__.Skip(service, rules, path + [("Skip", "")])
                                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                                super().__init__(service, rules, path)

                            class ColorMap(PyTextual):
                                """
                                Parameter ColorMap of value type str.
                                """
                                pass

                            class IsLogScale(PyParameter):
                                """
                                Parameter IsLogScale of value type bool.
                                """
                                pass

                            class Position(PyTextual):
                                """
                                Parameter Position of value type str.
                                """
                                pass

                            class Precision(PyNumerical):
                                """
                                Parameter Precision of value type int.
                                """
                                pass

                            class ShowAll(PyParameter):
                                """
                                Parameter ShowAll of value type bool.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type int.
                                """
                                pass

                            class Skip(PyNumerical):
                                """
                                Parameter Skip of value type int.
                                """
                                pass

                            class Type(PyTextual):
                                """
                                Parameter Type of value type str.
                                """
                                pass

                            class Visible(PyParameter):
                                """
                                Parameter Visible of value type bool.
                                """
                                pass

                        class Range(PyMenu):
                            """
                            Singleton Range.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                self.ClipToRange = self.__class__.ClipToRange(service, rules, path + [("ClipToRange", "")])
                                self.GlobalRange = self.__class__.GlobalRange(service, rules, path + [("GlobalRange", "")])
                                self.MaxValue = self.__class__.MaxValue(service, rules, path + [("MaxValue", "")])
                                self.MinValue = self.__class__.MinValue(service, rules, path + [("MinValue", "")])
                                super().__init__(service, rules, path)

                            class AutoRange(PyParameter):
                                """
                                Parameter AutoRange of value type bool.
                                """
                                pass

                            class ClipToRange(PyParameter):
                                """
                                Parameter ClipToRange of value type bool.
                                """
                                pass

                            class GlobalRange(PyParameter):
                                """
                                Parameter GlobalRange of value type bool.
                                """
                                pass

                            class MaxValue(PyNumerical):
                                """
                                Parameter MaxValue of value type float.
                                """
                                pass

                            class MinValue(PyNumerical):
                                """
                                Parameter MinValue of value type float.
                                """
                                pass

                        class Scale(PyMenu):
                            """
                            Singleton Scale.
                            """
                            def __init__(self, service, rules, path):
                                self.AutoScale = self.__class__.AutoScale(service, rules, path + [("AutoScale", "")])
                                self.Scale = self.__class__.Scale(service, rules, path + [("Scale", "")])
                                super().__init__(service, rules, path)

                            class AutoScale(PyParameter):
                                """
                                Parameter AutoScale of value type bool.
                                """
                                pass

                            class Scale(PyNumerical):
                                """
                                Parameter Scale of value type float.
                                """
                                pass

                        class VectorOptions(PyMenu):
                            """
                            Singleton VectorOptions.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.FixedLength = self.__class__.FixedLength(service, rules, path + [("FixedLength", "")])
                                self.HeadScale = self.__class__.HeadScale(service, rules, path + [("HeadScale", "")])
                                self.InPlane = self.__class__.InPlane(service, rules, path + [("InPlane", "")])
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class FixedLength(PyParameter):
                                """
                                Parameter FixedLength of value type bool.
                                """
                                pass

                            class HeadScale(PyNumerical):
                                """
                                Parameter HeadScale of value type float.
                                """
                                pass

                            class InPlane(PyParameter):
                                """
                                Parameter InPlane of value type bool.
                                """
                                pass

                            class XComponent(PyParameter):
                                """
                                Parameter XComponent of value type bool.
                                """
                                pass

                            class YComponent(PyParameter):
                                """
                                Parameter YComponent of value type bool.
                                """
                                pass

                            class ZComponent(PyParameter):
                                """
                                Parameter ZComponent of value type bool.
                                """
                                pass

                        class DrawMesh(PyParameter):
                            """
                            Parameter DrawMesh of value type bool.
                            """
                            pass

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                        class OverlayedMesh(PyTextual):
                            """
                            Parameter OverlayedMesh of value type str.
                            """
                            pass

                        class Skip(PyNumerical):
                            """
                            Parameter Skip of value type int.
                            """
                            pass

                        class Style(PyTextual):
                            """
                            Parameter Style of value type str.
                            """
                            pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class VectorField(PyTextual):
                            """
                            Parameter VectorField of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class AddToViewport(PyCommand):
                            """
                            Command AddToViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _AddToViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _AddToViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._AddToViewportCommandArguments(*args)

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class DisplayInViewport(PyCommand):
                            """
                            Command DisplayInViewport.

                            Parameters
                            ----------
                            Viewport : str

                            Returns
                            -------
                            bool
                            """
                            class _DisplayInViewportCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.Viewport = self._Viewport(self, "Viewport", service, rules, path)

                                class _Viewport(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Viewport.
                                    """

                            def create_instance(self) -> _DisplayInViewportCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayInViewportCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveAnimation(PyCommand):
                            """
                            Command SaveAnimation.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FPS : float
                            AntiAliasingPasses : str
                            Quality : str
                            H264 : bool
                            Compression : str
                            BitRate : int
                            JPegQuality : int
                            PPMFormat : str
                            UseWhiteBackground : bool
                            Orientation : str
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            None
                            """
                            class _SaveAnimationCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FPS = self._FPS(self, "FPS", service, rules, path)
                                    self.AntiAliasingPasses = self._AntiAliasingPasses(self, "AntiAliasingPasses", service, rules, path)
                                    self.Quality = self._Quality(self, "Quality", service, rules, path)
                                    self.H264 = self._H264(self, "H264", service, rules, path)
                                    self.Compression = self._Compression(self, "Compression", service, rules, path)
                                    self.BitRate = self._BitRate(self, "BitRate", service, rules, path)
                                    self.JPegQuality = self._JPegQuality(self, "JPegQuality", service, rules, path)
                                    self.PPMFormat = self._PPMFormat(self, "PPMFormat", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FPS(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument FPS.
                                    """

                                class _AntiAliasingPasses(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument AntiAliasingPasses.
                                    """

                                class _Quality(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Quality.
                                    """

                                class _H264(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument H264.
                                    """

                                class _Compression(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Compression.
                                    """

                                class _BitRate(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument BitRate.
                                    """

                                class _JPegQuality(PyNumericalCommandArgumentsSubItem):
                                    """
                                    Argument JPegQuality.
                                    """

                                class _PPMFormat(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument PPMFormat.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveAnimationCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveAnimationCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                        class UpdateMinMax(PyCommand):
                            """
                            Command UpdateMinMax.


                            Returns
                            -------
                            None
                            """
                            class _UpdateMinMaxCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _UpdateMinMaxCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._UpdateMinMaxCommandArguments(*args)

                    def __getitem__(self, key: str) -> _Vector:
                        return super().__getitem__(key)

                class XYPlot(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _XYPlot(PyMenu):
                        """
                        Singleton _XYPlot.
                        """
                        def __init__(self, service, rules, path):
                            self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                            self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                            self.DirectionVectorInternal = self.__class__.DirectionVectorInternal(service, rules, path + [("DirectionVectorInternal", "")])
                            self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                            self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                            self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                            self.Surfaces = self.__class__.Surfaces(service, rules, path + [("Surfaces", "")])
                            self.SyncStatus = self.__class__.SyncStatus(service, rules, path + [("SyncStatus", "")])
                            self.UID = self.__class__.UID(service, rules, path + [("UID", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Diff = self.__class__.Diff(service, rules, "Diff", path)
                            self.ExportData = self.__class__.ExportData(service, rules, "ExportData", path)
                            self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                            self.Pull = self.__class__.Pull(service, rules, "Pull", path)
                            self.Push = self.__class__.Push(service, rules, "Push", path)
                            self.SaveImage = self.__class__.SaveImage(service, rules, "SaveImage", path)
                            super().__init__(service, rules, path)

                        class Axes(PyMenu):
                            """
                            Singleton Axes.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                super().__init__(service, rules, path)

                            class X(PyMenu):
                                """
                                Singleton X.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyNumerical):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyTextual):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class Log(PyParameter):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyParameter):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyParameter):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyNumerical):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyNumerical):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class Label(PyTextual):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                            class Y(PyMenu):
                                """
                                Singleton Y.
                                """
                                def __init__(self, service, rules, path):
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                    self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                    self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                    self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                    super().__init__(service, rules, path)

                                class MajorRules(PyMenu):
                                    """
                                    Singleton MajorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class MinorRules(PyMenu):
                                    """
                                    Singleton MinorRules.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                        self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                        super().__init__(service, rules, path)

                                    class Color(PyTextual):
                                        """
                                        Parameter Color of value type str.
                                        """
                                        pass

                                    class Weight(PyNumerical):
                                        """
                                        Parameter Weight of value type float.
                                        """
                                        pass

                                class NumberFormat(PyMenu):
                                    """
                                    Singleton NumberFormat.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                        super().__init__(service, rules, path)

                                    class Precision(PyNumerical):
                                        """
                                        Parameter Precision of value type int.
                                        """
                                        pass

                                    class Type(PyTextual):
                                        """
                                        Parameter Type of value type str.
                                        """
                                        pass

                                class Options(PyMenu):
                                    """
                                    Singleton Options.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                        self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                        self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                        self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                        super().__init__(service, rules, path)

                                    class AutoRange(PyParameter):
                                        """
                                        Parameter AutoRange of value type bool.
                                        """
                                        pass

                                    class Log(PyParameter):
                                        """
                                        Parameter Log of value type bool.
                                        """
                                        pass

                                    class MajorRules(PyParameter):
                                        """
                                        Parameter MajorRules of value type bool.
                                        """
                                        pass

                                    class MinorRules(PyParameter):
                                        """
                                        Parameter MinorRules of value type bool.
                                        """
                                        pass

                                class Range(PyMenu):
                                    """
                                    Singleton Range.
                                    """
                                    def __init__(self, service, rules, path):
                                        self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                        self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                        super().__init__(service, rules, path)

                                    class Maximum(PyNumerical):
                                        """
                                        Parameter Maximum of value type float.
                                        """
                                        pass

                                    class Minimum(PyNumerical):
                                        """
                                        Parameter Minimum of value type float.
                                        """
                                        pass

                                class Label(PyTextual):
                                    """
                                    Parameter Label of value type str.
                                    """
                                    pass

                        class Curves(PyMenu):
                            """
                            Singleton Curves.
                            """
                            def __init__(self, service, rules, path):
                                self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                                self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                                super().__init__(service, rules, path)

                            class LineStyle(PyMenu):
                                """
                                Singleton LineStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Pattern(PyTextual):
                                    """
                                    Parameter Pattern of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MarkerStyle(PyMenu):
                                """
                                Singleton MarkerStyle.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                    self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Size(PyNumerical):
                                    """
                                    Parameter Size of value type float.
                                    """
                                    pass

                                class Symbol(PyTextual):
                                    """
                                    Parameter Symbol of value type str.
                                    """
                                    pass

                        class DirectionVectorInternal(PyMenu):
                            """
                            Singleton DirectionVectorInternal.
                            """
                            def __init__(self, service, rules, path):
                                self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                super().__init__(service, rules, path)

                            class XComponent(PyNumerical):
                                """
                                Parameter XComponent of value type float.
                                """
                                pass

                            class YComponent(PyNumerical):
                                """
                                Parameter YComponent of value type float.
                                """
                                pass

                            class ZComponent(PyNumerical):
                                """
                                Parameter ZComponent of value type float.
                                """
                                pass

                        class Options(PyMenu):
                            """
                            Singleton Options.
                            """
                            def __init__(self, service, rules, path):
                                self.NodeValues = self.__class__.NodeValues(service, rules, path + [("NodeValues", "")])
                                super().__init__(service, rules, path)

                            class NodeValues(PyParameter):
                                """
                                Parameter NodeValues of value type bool.
                                """
                                pass

                        class XAxisFunction(PyMenu):
                            """
                            Singleton XAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.XAxisFunctionInternal = self.__class__.XAxisFunctionInternal(service, rules, path + [("XAxisFunctionInternal", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

                                class XComponent(PyNumerical):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyNumerical):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class ZComponent(PyNumerical):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class Field(PyTextual):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyParameter):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class XAxisFunctionInternal(PyTextual):
                                """
                                Parameter XAxisFunctionInternal of value type str.
                                """
                                pass

                        class YAxisFunction(PyMenu):
                            """
                            Singleton YAxisFunction.
                            """
                            def __init__(self, service, rules, path):
                                self.DirectionVector = self.__class__.DirectionVector(service, rules, path + [("DirectionVector", "")])
                                self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                                self.PositionOnCurrentAxis = self.__class__.PositionOnCurrentAxis(service, rules, path + [("PositionOnCurrentAxis", "")])
                                self.YAxisFunctionInternal = self.__class__.YAxisFunctionInternal(service, rules, path + [("YAxisFunctionInternal", "")])
                                super().__init__(service, rules, path)

                            class DirectionVector(PyMenu):
                                """
                                Singleton DirectionVector.
                                """
                                def __init__(self, service, rules, path):
                                    self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                                    self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                                    self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                                    super().__init__(service, rules, path)

                                class XComponent(PyNumerical):
                                    """
                                    Parameter XComponent of value type float.
                                    """
                                    pass

                                class YComponent(PyNumerical):
                                    """
                                    Parameter YComponent of value type float.
                                    """
                                    pass

                                class ZComponent(PyNumerical):
                                    """
                                    Parameter ZComponent of value type float.
                                    """
                                    pass

                            class Field(PyTextual):
                                """
                                Parameter Field of value type str.
                                """
                                pass

                            class PositionOnCurrentAxis(PyParameter):
                                """
                                Parameter PositionOnCurrentAxis of value type bool.
                                """
                                pass

                            class YAxisFunctionInternal(PyTextual):
                                """
                                Parameter YAxisFunctionInternal of value type str.
                                """
                                pass

                        class Surfaces(PyTextual):
                            """
                            Parameter Surfaces of value type list[str].
                            """
                            pass

                        class SyncStatus(PyTextual):
                            """
                            Parameter SyncStatus of value type str.
                            """
                            pass

                        class UID(PyTextual):
                            """
                            Parameter UID of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Diff(PyCommand):
                            """
                            Command Diff.


                            Returns
                            -------
                            bool
                            """
                            class _DiffCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DiffCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DiffCommandArguments(*args)

                        class ExportData(PyCommand):
                            """
                            Command ExportData.

                            Parameters
                            ----------
                            FileName : str

                            Returns
                            -------
                            bool
                            """
                            class _ExportDataCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                            def create_instance(self) -> _ExportDataCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._ExportDataCommandArguments(*args)

                        class Plot(PyCommand):
                            """
                            Command Plot.


                            Returns
                            -------
                            bool
                            """
                            class _PlotCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PlotCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PlotCommandArguments(*args)

                        class Pull(PyCommand):
                            """
                            Command Pull.


                            Returns
                            -------
                            bool
                            """
                            class _PullCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PullCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PullCommandArguments(*args)

                        class Push(PyCommand):
                            """
                            Command Push.


                            Returns
                            -------
                            bool
                            """
                            class _PushCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PushCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PushCommandArguments(*args)

                        class SaveImage(PyCommand):
                            """
                            Command SaveImage.

                            Parameters
                            ----------
                            FileName : str
                            Format : str
                            FileType : str
                            Coloring : str
                            Orientation : str
                            UseWhiteBackground : bool
                            Resolution : dict[str, Any]

                            Returns
                            -------
                            bool
                            """
                            class _SaveImageCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)
                                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                                    self.Format = self._Format(self, "Format", service, rules, path)
                                    self.FileType = self._FileType(self, "FileType", service, rules, path)
                                    self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                                    self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                                    self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                                    self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                                class _FileName(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileName.
                                    """

                                class _Format(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Format.
                                    """

                                class _FileType(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument FileType.
                                    """

                                class _Coloring(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Coloring.
                                    """

                                class _Orientation(PyTextualCommandArgumentsSubItem):
                                    """
                                    Argument Orientation.
                                    """

                                class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                                    """
                                    Argument UseWhiteBackground.
                                    """

                                class _Resolution(PySingletonCommandArgumentsSubItem):
                                    """
                                    Argument Resolution.
                                    """

                                    def __init__(self, parent, attr, service, rules, path):
                                        super().__init__(parent, attr, service, rules, path)
                                        self.DPI = self._DPI(self, "DPI", service, rules, path)
                                        self.Option = self._Option(self, "Option", service, rules, path)
                                        self.Width = self._Width(self, "Width", service, rules, path)
                                        self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                        self.Height = self._Height(self, "Height", service, rules, path)

                                    class _DPI(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument DPI.
                                        """

                                    class _Option(PyTextualCommandArgumentsSubItem):
                                        """
                                        Argument Option.
                                        """

                                    class _Width(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Width.
                                        """

                                    class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                        """
                                        Argument UseWindowResolution.
                                        """

                                    class _Height(PyNumericalCommandArgumentsSubItem):
                                        """
                                        Argument Height.
                                        """

                            def create_instance(self) -> _SaveImageCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._SaveImageCommandArguments(*args)

                    def __getitem__(self, key: str) -> _XYPlot:
                        return super().__getitem__(key)

                class CameraSettings(PyMenu):
                    """
                    Singleton CameraSettings.
                    """
                    def __init__(self, service, rules, path):
                        self.Position = self.__class__.Position(service, rules, path + [("Position", "")])
                        self.Target = self.__class__.Target(service, rules, path + [("Target", "")])
                        super().__init__(service, rules, path)

                    class Position(PyMenu):
                        """
                        Singleton Position.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                    class Target(PyMenu):
                        """
                        Singleton Target.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                            super().__init__(service, rules, path)

                        class X(PyNumerical):
                            """
                            Parameter X of value type float.
                            """
                            pass

                        class Y(PyNumerical):
                            """
                            Parameter Y of value type float.
                            """
                            pass

                        class Z(PyNumerical):
                            """
                            Parameter Z of value type float.
                            """
                            pass

                class GridColors(PyMenu):
                    """
                    Singleton GridColors.
                    """
                    def __init__(self, service, rules, path):
                        self.ColorGridAxis = self.__class__.ColorGridAxis(service, rules, path + [("ColorGridAxis", "")])
                        self.ColorGridFar = self.__class__.ColorGridFar(service, rules, path + [("ColorGridFar", "")])
                        self.ColorGridFreeSurface = self.__class__.ColorGridFreeSurface(service, rules, path + [("ColorGridFreeSurface", "")])
                        self.ColorGridInlet = self.__class__.ColorGridInlet(service, rules, path + [("ColorGridInlet", "")])
                        self.ColorGridInterior = self.__class__.ColorGridInterior(service, rules, path + [("ColorGridInterior", "")])
                        self.ColorGridInternal = self.__class__.ColorGridInternal(service, rules, path + [("ColorGridInternal", "")])
                        self.ColorGridOutlet = self.__class__.ColorGridOutlet(service, rules, path + [("ColorGridOutlet", "")])
                        self.ColorGridOverset = self.__class__.ColorGridOverset(service, rules, path + [("ColorGridOverset", "")])
                        self.ColorGridPeriodic = self.__class__.ColorGridPeriodic(service, rules, path + [("ColorGridPeriodic", "")])
                        self.ColorGridRansLesInterface = self.__class__.ColorGridRansLesInterface(service, rules, path + [("ColorGridRansLesInterface", "")])
                        self.ColorGridSymmetry = self.__class__.ColorGridSymmetry(service, rules, path + [("ColorGridSymmetry", "")])
                        self.ColorGridTraction = self.__class__.ColorGridTraction(service, rules, path + [("ColorGridTraction", "")])
                        self.ColorGridWall = self.__class__.ColorGridWall(service, rules, path + [("ColorGridWall", "")])
                        self.ColorInterface = self.__class__.ColorInterface(service, rules, path + [("ColorInterface", "")])
                        self.ColorSurface = self.__class__.ColorSurface(service, rules, path + [("ColorSurface", "")])
                        super().__init__(service, rules, path)

                    class ColorGridAxis(PyTextual):
                        """
                        Parameter ColorGridAxis of value type str.
                        """
                        pass

                    class ColorGridFar(PyTextual):
                        """
                        Parameter ColorGridFar of value type str.
                        """
                        pass

                    class ColorGridFreeSurface(PyTextual):
                        """
                        Parameter ColorGridFreeSurface of value type str.
                        """
                        pass

                    class ColorGridInlet(PyTextual):
                        """
                        Parameter ColorGridInlet of value type str.
                        """
                        pass

                    class ColorGridInterior(PyTextual):
                        """
                        Parameter ColorGridInterior of value type str.
                        """
                        pass

                    class ColorGridInternal(PyTextual):
                        """
                        Parameter ColorGridInternal of value type str.
                        """
                        pass

                    class ColorGridOutlet(PyTextual):
                        """
                        Parameter ColorGridOutlet of value type str.
                        """
                        pass

                    class ColorGridOverset(PyTextual):
                        """
                        Parameter ColorGridOverset of value type str.
                        """
                        pass

                    class ColorGridPeriodic(PyTextual):
                        """
                        Parameter ColorGridPeriodic of value type str.
                        """
                        pass

                    class ColorGridRansLesInterface(PyTextual):
                        """
                        Parameter ColorGridRansLesInterface of value type str.
                        """
                        pass

                    class ColorGridSymmetry(PyTextual):
                        """
                        Parameter ColorGridSymmetry of value type str.
                        """
                        pass

                    class ColorGridTraction(PyTextual):
                        """
                        Parameter ColorGridTraction of value type str.
                        """
                        pass

                    class ColorGridWall(PyTextual):
                        """
                        Parameter ColorGridWall of value type str.
                        """
                        pass

                    class ColorInterface(PyTextual):
                        """
                        Parameter ColorInterface of value type str.
                        """
                        pass

                    class ColorSurface(PyTextual):
                        """
                        Parameter ColorSurface of value type str.
                        """
                        pass

                class GraphicsCreationCount(PyNumerical):
                    """
                    Parameter GraphicsCreationCount of value type int.
                    """
                    pass

                class SaveImage(PyCommand):
                    """
                    Command SaveImage.

                    Parameters
                    ----------
                    FileName : str
                    Format : str
                    FileType : str
                    Coloring : str
                    Orientation : str
                    UseWhiteBackground : bool
                    Resolution : dict[str, Any]

                    Returns
                    -------
                    bool
                    """
                    class _SaveImageCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)
                            self.FileName = self._FileName(self, "FileName", service, rules, path)
                            self.Format = self._Format(self, "Format", service, rules, path)
                            self.FileType = self._FileType(self, "FileType", service, rules, path)
                            self.Coloring = self._Coloring(self, "Coloring", service, rules, path)
                            self.Orientation = self._Orientation(self, "Orientation", service, rules, path)
                            self.UseWhiteBackground = self._UseWhiteBackground(self, "UseWhiteBackground", service, rules, path)
                            self.Resolution = self._Resolution(self, "Resolution", service, rules, path)

                        class _FileName(PyTextualCommandArgumentsSubItem):
                            """
                            Argument FileName.
                            """

                        class _Format(PyTextualCommandArgumentsSubItem):
                            """
                            Argument Format.
                            """

                        class _FileType(PyTextualCommandArgumentsSubItem):
                            """
                            Argument FileType.
                            """

                        class _Coloring(PyTextualCommandArgumentsSubItem):
                            """
                            Argument Coloring.
                            """

                        class _Orientation(PyTextualCommandArgumentsSubItem):
                            """
                            Argument Orientation.
                            """

                        class _UseWhiteBackground(PyParameterCommandArgumentsSubItem):
                            """
                            Argument UseWhiteBackground.
                            """

                        class _Resolution(PySingletonCommandArgumentsSubItem):
                            """
                            Argument Resolution.
                            """

                            def __init__(self, parent, attr, service, rules, path):
                                super().__init__(parent, attr, service, rules, path)
                                self.DPI = self._DPI(self, "DPI", service, rules, path)
                                self.Option = self._Option(self, "Option", service, rules, path)
                                self.Width = self._Width(self, "Width", service, rules, path)
                                self.UseWindowResolution = self._UseWindowResolution(self, "UseWindowResolution", service, rules, path)
                                self.Height = self._Height(self, "Height", service, rules, path)

                            class _DPI(PyNumericalCommandArgumentsSubItem):
                                """
                                Argument DPI.
                                """

                            class _Option(PyTextualCommandArgumentsSubItem):
                                """
                                Argument Option.
                                """

                            class _Width(PyNumericalCommandArgumentsSubItem):
                                """
                                Argument Width.
                                """

                            class _UseWindowResolution(PyParameterCommandArgumentsSubItem):
                                """
                                Argument UseWindowResolution.
                                """

                            class _Height(PyNumericalCommandArgumentsSubItem):
                                """
                                Argument Height.
                                """

                    def create_instance(self) -> _SaveImageCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._SaveImageCommandArguments(*args)

            class Plots(PyMenu):
                """
                Singleton Plots.
                """
                def __init__(self, service, rules, path):
                    self.PlotFromFile = self.__class__.PlotFromFile(service, rules, path + [("PlotFromFile", "")])
                    super().__init__(service, rules, path)

                class PlotFromFile(PyMenu):
                    """
                    Singleton PlotFromFile.
                    """
                    def __init__(self, service, rules, path):
                        self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                        self.Curves = self.__class__.Curves(service, rules, path + [("Curves", "")])
                        self.XAxisFunction = self.__class__.XAxisFunction(service, rules, path + [("XAxisFunction", "")])
                        self.YAxisFunction = self.__class__.YAxisFunction(service, rules, path + [("YAxisFunction", "")])
                        self.Filename = self.__class__.Filename(service, rules, path + [("Filename", "")])
                        self.Plot = self.__class__.Plot(service, rules, "Plot", path)
                        super().__init__(service, rules, path)

                    class Axes(PyMenu):
                        """
                        Singleton Axes.
                        """
                        def __init__(self, service, rules, path):
                            self.X = self.__class__.X(service, rules, path + [("X", "")])
                            self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                            super().__init__(service, rules, path)

                        class X(PyMenu):
                            """
                            Singleton X.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    super().__init__(service, rules, path)

                                class Precision(PyNumerical):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                                class Type(PyTextual):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    super().__init__(service, rules, path)

                                class AutoRange(PyParameter):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class Log(PyParameter):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                                class MajorRules(PyParameter):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                                class MinorRules(PyParameter):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    super().__init__(service, rules, path)

                                class Maximum(PyNumerical):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                                class Minimum(PyNumerical):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                            class Label(PyTextual):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                        class Y(PyMenu):
                            """
                            Singleton Y.
                            """
                            def __init__(self, service, rules, path):
                                self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                self.NumberFormat = self.__class__.NumberFormat(service, rules, path + [("NumberFormat", "")])
                                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                                self.Range = self.__class__.Range(service, rules, path + [("Range", "")])
                                self.Label = self.__class__.Label(service, rules, path + [("Label", "")])
                                super().__init__(service, rules, path)

                            class MajorRules(PyMenu):
                                """
                                Singleton MajorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class MinorRules(PyMenu):
                                """
                                Singleton MinorRules.
                                """
                                def __init__(self, service, rules, path):
                                    self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                    self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                    super().__init__(service, rules, path)

                                class Color(PyTextual):
                                    """
                                    Parameter Color of value type str.
                                    """
                                    pass

                                class Weight(PyNumerical):
                                    """
                                    Parameter Weight of value type float.
                                    """
                                    pass

                            class NumberFormat(PyMenu):
                                """
                                Singleton NumberFormat.
                                """
                                def __init__(self, service, rules, path):
                                    self.Precision = self.__class__.Precision(service, rules, path + [("Precision", "")])
                                    self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                                    super().__init__(service, rules, path)

                                class Precision(PyNumerical):
                                    """
                                    Parameter Precision of value type int.
                                    """
                                    pass

                                class Type(PyTextual):
                                    """
                                    Parameter Type of value type str.
                                    """
                                    pass

                            class Options(PyMenu):
                                """
                                Singleton Options.
                                """
                                def __init__(self, service, rules, path):
                                    self.AutoRange = self.__class__.AutoRange(service, rules, path + [("AutoRange", "")])
                                    self.Log = self.__class__.Log(service, rules, path + [("Log", "")])
                                    self.MajorRules = self.__class__.MajorRules(service, rules, path + [("MajorRules", "")])
                                    self.MinorRules = self.__class__.MinorRules(service, rules, path + [("MinorRules", "")])
                                    super().__init__(service, rules, path)

                                class AutoRange(PyParameter):
                                    """
                                    Parameter AutoRange of value type bool.
                                    """
                                    pass

                                class Log(PyParameter):
                                    """
                                    Parameter Log of value type bool.
                                    """
                                    pass

                                class MajorRules(PyParameter):
                                    """
                                    Parameter MajorRules of value type bool.
                                    """
                                    pass

                                class MinorRules(PyParameter):
                                    """
                                    Parameter MinorRules of value type bool.
                                    """
                                    pass

                            class Range(PyMenu):
                                """
                                Singleton Range.
                                """
                                def __init__(self, service, rules, path):
                                    self.Maximum = self.__class__.Maximum(service, rules, path + [("Maximum", "")])
                                    self.Minimum = self.__class__.Minimum(service, rules, path + [("Minimum", "")])
                                    super().__init__(service, rules, path)

                                class Maximum(PyNumerical):
                                    """
                                    Parameter Maximum of value type float.
                                    """
                                    pass

                                class Minimum(PyNumerical):
                                    """
                                    Parameter Minimum of value type float.
                                    """
                                    pass

                            class Label(PyTextual):
                                """
                                Parameter Label of value type str.
                                """
                                pass

                    class Curves(PyMenu):
                        """
                        Singleton Curves.
                        """
                        def __init__(self, service, rules, path):
                            self.LineStyle = self.__class__.LineStyle(service, rules, path + [("LineStyle", "")])
                            self.MarkerStyle = self.__class__.MarkerStyle(service, rules, path + [("MarkerStyle", "")])
                            super().__init__(service, rules, path)

                        class LineStyle(PyMenu):
                            """
                            Singleton LineStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Pattern = self.__class__.Pattern(service, rules, path + [("Pattern", "")])
                                self.Weight = self.__class__.Weight(service, rules, path + [("Weight", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Pattern(PyTextual):
                                """
                                Parameter Pattern of value type str.
                                """
                                pass

                            class Weight(PyNumerical):
                                """
                                Parameter Weight of value type float.
                                """
                                pass

                        class MarkerStyle(PyMenu):
                            """
                            Singleton MarkerStyle.
                            """
                            def __init__(self, service, rules, path):
                                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                                self.Size = self.__class__.Size(service, rules, path + [("Size", "")])
                                self.Symbol = self.__class__.Symbol(service, rules, path + [("Symbol", "")])
                                super().__init__(service, rules, path)

                            class Color(PyTextual):
                                """
                                Parameter Color of value type str.
                                """
                                pass

                            class Size(PyNumerical):
                                """
                                Parameter Size of value type float.
                                """
                                pass

                            class Symbol(PyTextual):
                                """
                                Parameter Symbol of value type str.
                                """
                                pass

                    class XAxisFunction(PyMenu):
                        """
                        Singleton XAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class YAxisFunction(PyMenu):
                        """
                        Singleton YAxisFunction.
                        """
                        def __init__(self, service, rules, path):
                            self.Field = self.__class__.Field(service, rules, path + [("Field", "")])
                            super().__init__(service, rules, path)

                        class Field(PyTextual):
                            """
                            Parameter Field of value type str.
                            """
                            pass

                    class Filename(PyTextual):
                        """
                        Parameter Filename of value type str.
                        """
                        pass

                    class Plot(PyCommand):
                        """
                        Command Plot.


                        Returns
                        -------
                        None
                        """
                        class _PlotCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)

                        def create_instance(self) -> _PlotCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._PlotCommandArguments(*args)

            class ResultsExternalInfo(PyMenu):
                """
                Singleton ResultsExternalInfo.
                """
                def __init__(self, service, rules, path):
                    super().__init__(service, rules, path)

            class CreateCellZoneSurfaces(PyCommand):
                """
                Command CreateCellZoneSurfaces.


                Returns
                -------
                list[int]
                """
                class _CreateCellZoneSurfacesCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _CreateCellZoneSurfacesCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateCellZoneSurfacesCommandArguments(*args)

            class CreateMultipleIsosurfaces(PyCommand):
                """
                Command CreateMultipleIsosurfaces.

                Parameters
                ----------
                NameFormat : str
                Field : str
                SpecifyBy : str
                FirstValue : float
                Increment : float
                Steps : int
                LastValue : float

                Returns
                -------
                None
                """
                class _CreateMultipleIsosurfacesCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NameFormat = self._NameFormat(self, "NameFormat", service, rules, path)
                        self.Field = self._Field(self, "Field", service, rules, path)
                        self.SpecifyBy = self._SpecifyBy(self, "SpecifyBy", service, rules, path)
                        self.FirstValue = self._FirstValue(self, "FirstValue", service, rules, path)
                        self.Increment = self._Increment(self, "Increment", service, rules, path)
                        self.Steps = self._Steps(self, "Steps", service, rules, path)
                        self.LastValue = self._LastValue(self, "LastValue", service, rules, path)

                    class _NameFormat(PyTextualCommandArgumentsSubItem):
                        """
                        Argument NameFormat.
                        """

                    class _Field(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Field.
                        """

                    class _SpecifyBy(PyTextualCommandArgumentsSubItem):
                        """
                        Argument SpecifyBy.
                        """

                    class _FirstValue(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument FirstValue.
                        """

                    class _Increment(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument Increment.
                        """

                    class _Steps(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument Steps.
                        """

                    class _LastValue(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument LastValue.
                        """

                def create_instance(self) -> _CreateMultipleIsosurfacesCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateMultipleIsosurfacesCommandArguments(*args)

            class CreateMultiplePlanes(PyCommand):
                """
                Command CreateMultiplePlanes.

                Parameters
                ----------
                NameFormat : str
                NumberOfPlanes : int
                Option : str
                NormalSpecification : str
                NormalVector : dict[str, Any]
                StartPoint : dict[str, Any]
                EndPoint : dict[str, Any]
                Spacing : float

                Returns
                -------
                None
                """
                class _CreateMultiplePlanesCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NameFormat = self._NameFormat(self, "NameFormat", service, rules, path)
                        self.NumberOfPlanes = self._NumberOfPlanes(self, "NumberOfPlanes", service, rules, path)
                        self.Option = self._Option(self, "Option", service, rules, path)
                        self.NormalSpecification = self._NormalSpecification(self, "NormalSpecification", service, rules, path)
                        self.NormalVector = self._NormalVector(self, "NormalVector", service, rules, path)
                        self.StartPoint = self._StartPoint(self, "StartPoint", service, rules, path)
                        self.EndPoint = self._EndPoint(self, "EndPoint", service, rules, path)
                        self.Spacing = self._Spacing(self, "Spacing", service, rules, path)

                    class _NameFormat(PyTextualCommandArgumentsSubItem):
                        """
                        Argument NameFormat.
                        """

                    class _NumberOfPlanes(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument NumberOfPlanes.
                        """

                    class _Option(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Option.
                        """

                    class _NormalSpecification(PyTextualCommandArgumentsSubItem):
                        """
                        Argument NormalSpecification.
                        """

                    class _NormalVector(PySingletonCommandArgumentsSubItem):
                        """
                        Argument NormalVector.
                        """

                        def __init__(self, parent, attr, service, rules, path):
                            super().__init__(parent, attr, service, rules, path)
                            self.X = self._X(self, "X", service, rules, path)
                            self.Z = self._Z(self, "Z", service, rules, path)
                            self.Y = self._Y(self, "Y", service, rules, path)

                        class _X(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument X.
                            """

                        class _Z(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Z.
                            """

                        class _Y(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Y.
                            """

                    class _StartPoint(PySingletonCommandArgumentsSubItem):
                        """
                        Argument StartPoint.
                        """

                        def __init__(self, parent, attr, service, rules, path):
                            super().__init__(parent, attr, service, rules, path)
                            self.X = self._X(self, "X", service, rules, path)
                            self.Z = self._Z(self, "Z", service, rules, path)
                            self.Y = self._Y(self, "Y", service, rules, path)

                        class _X(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument X.
                            """

                        class _Z(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Z.
                            """

                        class _Y(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Y.
                            """

                    class _EndPoint(PySingletonCommandArgumentsSubItem):
                        """
                        Argument EndPoint.
                        """

                        def __init__(self, parent, attr, service, rules, path):
                            super().__init__(parent, attr, service, rules, path)
                            self.X = self._X(self, "X", service, rules, path)
                            self.Z = self._Z(self, "Z", service, rules, path)
                            self.Y = self._Y(self, "Y", service, rules, path)

                        class _X(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument X.
                            """

                        class _Z(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Z.
                            """

                        class _Y(PyNumericalCommandArgumentsSubItem):
                            """
                            Argument Y.
                            """

                    class _Spacing(PyNumericalCommandArgumentsSubItem):
                        """
                        Argument Spacing.
                        """

                def create_instance(self) -> _CreateMultiplePlanesCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateMultiplePlanesCommandArguments(*args)

            class GetFieldMinMax(PyCommand):
                """
                Command GetFieldMinMax.

                Parameters
                ----------
                Field : str
                Surfaces : list[str]

                Returns
                -------
                list[float]
                """
                class _GetFieldMinMaxCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Field = self._Field(self, "Field", service, rules, path)
                        self.Surfaces = self._Surfaces(self, "Surfaces", service, rules, path)

                    class _Field(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Field.
                        """

                    class _Surfaces(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Surfaces.
                        """

                def create_instance(self) -> _GetFieldMinMaxCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._GetFieldMinMaxCommandArguments(*args)

            class GetXYData(PyCommand):
                """
                Command GetXYData.

                Parameters
                ----------
                Surfaces : list[str]
                Fields : list[str]

                Returns
                -------
                None
                """
                class _GetXYDataCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Surfaces = self._Surfaces(self, "Surfaces", service, rules, path)
                        self.Fields = self._Fields(self, "Fields", service, rules, path)

                    class _Surfaces(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Surfaces.
                        """

                    class _Fields(PyTextualCommandArgumentsSubItem):
                        """
                        Argument Fields.
                        """

                def create_instance(self) -> _GetXYDataCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._GetXYDataCommandArguments(*args)

        class ResultsInfo(PyMenu):
            """
            Singleton ResultsInfo.
            """
            def __init__(self, service, rules, path):
                self.DPMInjections = self.__class__.DPMInjections(service, rules, path + [("DPMInjections", "")])
                self.DPMParticleVectorFields = self.__class__.DPMParticleVectorFields(service, rules, path + [("DPMParticleVectorFields", "")])
                self.Fields = self.__class__.Fields(service, rules, path + [("Fields", "")])
                self.ParticleTracksFields = self.__class__.ParticleTracksFields(service, rules, path + [("ParticleTracksFields", "")])
                self.ParticleVariables = self.__class__.ParticleVariables(service, rules, path + [("ParticleVariables", "")])
                self.PathlinesFields = self.__class__.PathlinesFields(service, rules, path + [("PathlinesFields", "")])
                self.VectorFields = self.__class__.VectorFields(service, rules, path + [("VectorFields", "")])
                super().__init__(service, rules, path)

            class DPMInjections(PyNamedObjectContainer):
                """
                .
                """
                class _DPMInjections(PyMenu):
                    """
                    Singleton _DPMInjections.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMInjections:
                    return super().__getitem__(key)

            class DPMParticleVectorFields(PyNamedObjectContainer):
                """
                .
                """
                class _DPMParticleVectorFields(PyMenu):
                    """
                    Singleton _DPMParticleVectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _DPMParticleVectorFields:
                    return super().__getitem__(key)

            class Fields(PyNamedObjectContainer):
                """
                .
                """
                class _Fields(PyMenu):
                    """
                    Singleton _Fields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self.UnitQuantity = self.__class__.UnitQuantity(service, rules, path + [("UnitQuantity", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Rank(PyNumerical):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class UnitQuantity(PyTextual):
                        """
                        Parameter UnitQuantity of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Fields:
                    return super().__getitem__(key)

            class ParticleTracksFields(PyNamedObjectContainer):
                """
                .
                """
                class _ParticleTracksFields(PyMenu):
                    """
                    Singleton _ParticleTracksFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleTracksFields:
                    return super().__getitem__(key)

            class ParticleVariables(PyNamedObjectContainer):
                """
                .
                """
                class _ParticleVariables(PyMenu):
                    """
                    Singleton _ParticleVariables.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _ParticleVariables:
                    return super().__getitem__(key)

            class PathlinesFields(PyNamedObjectContainer):
                """
                .
                """
                class _PathlinesFields(PyMenu):
                    """
                    Singleton _PathlinesFields.
                    """
                    def __init__(self, service, rules, path):
                        self.DisplayName = self.__class__.DisplayName(service, rules, path + [("DisplayName", "")])
                        self.Domain = self.__class__.Domain(service, rules, path + [("Domain", "")])
                        self.Rank = self.__class__.Rank(service, rules, path + [("Rank", "")])
                        self.Section = self.__class__.Section(service, rules, path + [("Section", "")])
                        self.SolverName = self.__class__.SolverName(service, rules, path + [("SolverName", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class DisplayName(PyTextual):
                        """
                        Parameter DisplayName of value type str.
                        """
                        pass

                    class Domain(PyTextual):
                        """
                        Parameter Domain of value type str.
                        """
                        pass

                    class Rank(PyNumerical):
                        """
                        Parameter Rank of value type int.
                        """
                        pass

                    class Section(PyTextual):
                        """
                        Parameter Section of value type str.
                        """
                        pass

                    class SolverName(PyTextual):
                        """
                        Parameter SolverName of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _PathlinesFields:
                    return super().__getitem__(key)

            class VectorFields(PyNamedObjectContainer):
                """
                .
                """
                class _VectorFields(PyMenu):
                    """
                    Singleton _VectorFields.
                    """
                    def __init__(self, service, rules, path):
                        self.IsCustomVector = self.__class__.IsCustomVector(service, rules, path + [("IsCustomVector", "")])
                        self.XComponent = self.__class__.XComponent(service, rules, path + [("XComponent", "")])
                        self.YComponent = self.__class__.YComponent(service, rules, path + [("YComponent", "")])
                        self.ZComponent = self.__class__.ZComponent(service, rules, path + [("ZComponent", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class IsCustomVector(PyParameter):
                        """
                        Parameter IsCustomVector of value type bool.
                        """
                        pass

                    class XComponent(PyTextual):
                        """
                        Parameter XComponent of value type str.
                        """
                        pass

                    class YComponent(PyTextual):
                        """
                        Parameter YComponent of value type str.
                        """
                        pass

                    class ZComponent(PyTextual):
                        """
                        Parameter ZComponent of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _VectorFields:
                    return super().__getitem__(key)

        class Setup(PyMenu):
            """
            Singleton Setup.
            """
            def __init__(self, service, rules, path):
                self.Boundary = self.__class__.Boundary(service, rules, path + [("Boundary", "")])
                self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
                self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                self.Beta = self.__class__.Beta(service, rules, path + [("Beta", "")])
                super().__init__(service, rules, path)

            class Boundary(PyNamedObjectContainer):
                """
                .
                """
                class _Boundary(PyMenu):
                    """
                    Singleton _Boundary.
                    """
                    def __init__(self, service, rules, path):
                        self.Flow = self.__class__.Flow(service, rules, path + [("Flow", "")])
                        self.Thermal = self.__class__.Thermal(service, rules, path + [("Thermal", "")])
                        self.Turbulence = self.__class__.Turbulence(service, rules, path + [("Turbulence", "")])
                        self.BoundaryId = self.__class__.BoundaryId(service, rules, path + [("BoundaryId", "")])
                        self.BoundaryType = self.__class__.BoundaryType(service, rules, path + [("BoundaryType", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class Flow(PyMenu):
                        """
                        Singleton Flow.
                        """
                        def __init__(self, service, rules, path):
                            self.Direction = self.__class__.Direction(service, rules, path + [("Direction", "")])
                            self.FlowDirection = self.__class__.FlowDirection(service, rules, path + [("FlowDirection", "")])
                            self.RotationAxisDirection = self.__class__.RotationAxisDirection(service, rules, path + [("RotationAxisDirection", "")])
                            self.RotationAxisOrigin = self.__class__.RotationAxisOrigin(service, rules, path + [("RotationAxisOrigin", "")])
                            self.TranslationalDirection = self.__class__.TranslationalDirection(service, rules, path + [("TranslationalDirection", "")])
                            self.TranslationalVelocityComponents = self.__class__.TranslationalVelocityComponents(service, rules, path + [("TranslationalVelocityComponents", "")])
                            self.VelocityCartesianComponents = self.__class__.VelocityCartesianComponents(service, rules, path + [("VelocityCartesianComponents", "")])
                            self.AverageMassFlux = self.__class__.AverageMassFlux(service, rules, path + [("AverageMassFlux", "")])
                            self.DirectionSpecificationMethod = self.__class__.DirectionSpecificationMethod(service, rules, path + [("DirectionSpecificationMethod", "")])
                            self.GaugePressure = self.__class__.GaugePressure(service, rules, path + [("GaugePressure", "")])
                            self.GaugeTotalPressure = self.__class__.GaugeTotalPressure(service, rules, path + [("GaugeTotalPressure", "")])
                            self.IsMotionBC = self.__class__.IsMotionBC(service, rules, path + [("IsMotionBC", "")])
                            self.IsRotating = self.__class__.IsRotating(service, rules, path + [("IsRotating", "")])
                            self.MachNumber = self.__class__.MachNumber(service, rules, path + [("MachNumber", "")])
                            self.MassFlowRate = self.__class__.MassFlowRate(service, rules, path + [("MassFlowRate", "")])
                            self.MassFlowSpecificationMethod = self.__class__.MassFlowSpecificationMethod(service, rules, path + [("MassFlowSpecificationMethod", "")])
                            self.MassFlux = self.__class__.MassFlux(service, rules, path + [("MassFlux", "")])
                            self.RotationalSpeed = self.__class__.RotationalSpeed(service, rules, path + [("RotationalSpeed", "")])
                            self.SupersonicOrInitialGaugePressure = self.__class__.SupersonicOrInitialGaugePressure(service, rules, path + [("SupersonicOrInitialGaugePressure", "")])
                            self.TranslationalVelocityMagnitude = self.__class__.TranslationalVelocityMagnitude(service, rules, path + [("TranslationalVelocityMagnitude", "")])
                            self.TranslationalVelocitySpecification = self.__class__.TranslationalVelocitySpecification(service, rules, path + [("TranslationalVelocitySpecification", "")])
                            self.VelocityMagnitude = self.__class__.VelocityMagnitude(service, rules, path + [("VelocityMagnitude", "")])
                            self.VelocitySpecification = self.__class__.VelocitySpecification(service, rules, path + [("VelocitySpecification", "")])
                            self.WallVelocitySpecification = self.__class__.WallVelocitySpecification(service, rules, path + [("WallVelocitySpecification", "")])
                            super().__init__(service, rules, path)

                        class Direction(PyMenu):
                            """
                            Singleton Direction.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class FlowDirection(PyMenu):
                            """
                            Singleton FlowDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class RotationAxisDirection(PyMenu):
                            """
                            Singleton RotationAxisDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class RotationAxisOrigin(PyMenu):
                            """
                            Singleton RotationAxisOrigin.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class TranslationalDirection(PyMenu):
                            """
                            Singleton TranslationalDirection.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class TranslationalVelocityComponents(PyMenu):
                            """
                            Singleton TranslationalVelocityComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class VelocityCartesianComponents(PyMenu):
                            """
                            Singleton VelocityCartesianComponents.
                            """
                            def __init__(self, service, rules, path):
                                self.X = self.__class__.X(service, rules, path + [("X", "")])
                                self.Y = self.__class__.Y(service, rules, path + [("Y", "")])
                                self.Z = self.__class__.Z(service, rules, path + [("Z", "")])
                                super().__init__(service, rules, path)

                            class X(PyNumerical):
                                """
                                Parameter X of value type float.
                                """
                                pass

                            class Y(PyNumerical):
                                """
                                Parameter Y of value type float.
                                """
                                pass

                            class Z(PyNumerical):
                                """
                                Parameter Z of value type float.
                                """
                                pass

                        class AverageMassFlux(PyNumerical):
                            """
                            Parameter AverageMassFlux of value type float.
                            """
                            pass

                        class DirectionSpecificationMethod(PyTextual):
                            """
                            Parameter DirectionSpecificationMethod of value type str.
                            """
                            pass

                        class GaugePressure(PyNumerical):
                            """
                            Parameter GaugePressure of value type float.
                            """
                            pass

                        class GaugeTotalPressure(PyNumerical):
                            """
                            Parameter GaugeTotalPressure of value type float.
                            """
                            pass

                        class IsMotionBC(PyNumerical):
                            """
                            Parameter IsMotionBC of value type int.
                            """
                            pass

                        class IsRotating(PyParameter):
                            """
                            Parameter IsRotating of value type bool.
                            """
                            pass

                        class MachNumber(PyNumerical):
                            """
                            Parameter MachNumber of value type float.
                            """
                            pass

                        class MassFlowRate(PyNumerical):
                            """
                            Parameter MassFlowRate of value type float.
                            """
                            pass

                        class MassFlowSpecificationMethod(PyTextual):
                            """
                            Parameter MassFlowSpecificationMethod of value type str.
                            """
                            pass

                        class MassFlux(PyNumerical):
                            """
                            Parameter MassFlux of value type float.
                            """
                            pass

                        class RotationalSpeed(PyNumerical):
                            """
                            Parameter RotationalSpeed of value type float.
                            """
                            pass

                        class SupersonicOrInitialGaugePressure(PyNumerical):
                            """
                            Parameter SupersonicOrInitialGaugePressure of value type float.
                            """
                            pass

                        class TranslationalVelocityMagnitude(PyNumerical):
                            """
                            Parameter TranslationalVelocityMagnitude of value type float.
                            """
                            pass

                        class TranslationalVelocitySpecification(PyTextual):
                            """
                            Parameter TranslationalVelocitySpecification of value type str.
                            """
                            pass

                        class VelocityMagnitude(PyNumerical):
                            """
                            Parameter VelocityMagnitude of value type float.
                            """
                            pass

                        class VelocitySpecification(PyTextual):
                            """
                            Parameter VelocitySpecification of value type str.
                            """
                            pass

                        class WallVelocitySpecification(PyTextual):
                            """
                            Parameter WallVelocitySpecification of value type str.
                            """
                            pass

                    class Thermal(PyMenu):
                        """
                        Singleton Thermal.
                        """
                        def __init__(self, service, rules, path):
                            self.ExternalEmissivity = self.__class__.ExternalEmissivity(service, rules, path + [("ExternalEmissivity", "")])
                            self.ExternalRadiationTemperature = self.__class__.ExternalRadiationTemperature(service, rules, path + [("ExternalRadiationTemperature", "")])
                            self.FreeStreamTemperature = self.__class__.FreeStreamTemperature(service, rules, path + [("FreeStreamTemperature", "")])
                            self.HeatFlux = self.__class__.HeatFlux(service, rules, path + [("HeatFlux", "")])
                            self.HeatGenerationRate = self.__class__.HeatGenerationRate(service, rules, path + [("HeatGenerationRate", "")])
                            self.HeatTransferCoefficient = self.__class__.HeatTransferCoefficient(service, rules, path + [("HeatTransferCoefficient", "")])
                            self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                            self.ThermalConditions = self.__class__.ThermalConditions(service, rules, path + [("ThermalConditions", "")])
                            self.TotalTemperature = self.__class__.TotalTemperature(service, rules, path + [("TotalTemperature", "")])
                            self.WallThickness = self.__class__.WallThickness(service, rules, path + [("WallThickness", "")])
                            super().__init__(service, rules, path)

                        class ExternalEmissivity(PyNumerical):
                            """
                            Parameter ExternalEmissivity of value type float.
                            """
                            pass

                        class ExternalRadiationTemperature(PyNumerical):
                            """
                            Parameter ExternalRadiationTemperature of value type float.
                            """
                            pass

                        class FreeStreamTemperature(PyNumerical):
                            """
                            Parameter FreeStreamTemperature of value type float.
                            """
                            pass

                        class HeatFlux(PyNumerical):
                            """
                            Parameter HeatFlux of value type float.
                            """
                            pass

                        class HeatGenerationRate(PyNumerical):
                            """
                            Parameter HeatGenerationRate of value type float.
                            """
                            pass

                        class HeatTransferCoefficient(PyNumerical):
                            """
                            Parameter HeatTransferCoefficient of value type float.
                            """
                            pass

                        class Temperature(PyNumerical):
                            """
                            Parameter Temperature of value type float.
                            """
                            pass

                        class ThermalConditions(PyTextual):
                            """
                            Parameter ThermalConditions of value type str.
                            """
                            pass

                        class TotalTemperature(PyNumerical):
                            """
                            Parameter TotalTemperature of value type float.
                            """
                            pass

                        class WallThickness(PyNumerical):
                            """
                            Parameter WallThickness of value type float.
                            """
                            pass

                    class Turbulence(PyMenu):
                        """
                        Singleton Turbulence.
                        """
                        def __init__(self, service, rules, path):
                            self.HydraulicDiameter = self.__class__.HydraulicDiameter(service, rules, path + [("HydraulicDiameter", "")])
                            self.SpecificationMethod = self.__class__.SpecificationMethod(service, rules, path + [("SpecificationMethod", "")])
                            self.TurbulentIntensity = self.__class__.TurbulentIntensity(service, rules, path + [("TurbulentIntensity", "")])
                            self.TurbulentLengthScale = self.__class__.TurbulentLengthScale(service, rules, path + [("TurbulentLengthScale", "")])
                            self.TurbulentViscosityRatio = self.__class__.TurbulentViscosityRatio(service, rules, path + [("TurbulentViscosityRatio", "")])
                            super().__init__(service, rules, path)

                        class HydraulicDiameter(PyNumerical):
                            """
                            Parameter HydraulicDiameter of value type float.
                            """
                            pass

                        class SpecificationMethod(PyTextual):
                            """
                            Parameter SpecificationMethod of value type str.
                            """
                            pass

                        class TurbulentIntensity(PyNumerical):
                            """
                            Parameter TurbulentIntensity of value type float.
                            """
                            pass

                        class TurbulentLengthScale(PyNumerical):
                            """
                            Parameter TurbulentLengthScale of value type float.
                            """
                            pass

                        class TurbulentViscosityRatio(PyNumerical):
                            """
                            Parameter TurbulentViscosityRatio of value type float.
                            """
                            pass

                    class BoundaryId(PyNumerical):
                        """
                        Parameter BoundaryId of value type int.
                        """
                        pass

                    class BoundaryType(PyTextual):
                        """
                        Parameter BoundaryType of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _Boundary:
                    return super().__getitem__(key)

            class CellZone(PyNamedObjectContainer):
                """
                .
                """
                class _CellZone(PyMenu):
                    """
                    Singleton _CellZone.
                    """
                    def __init__(self, service, rules, path):
                        self.CellZoneId = self.__class__.CellZoneId(service, rules, path + [("CellZoneId", "")])
                        self.Material = self.__class__.Material(service, rules, path + [("Material", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        super().__init__(service, rules, path)

                    class CellZoneId(PyNumerical):
                        """
                        Parameter CellZoneId of value type int.
                        """
                        pass

                    class Material(PyTextual):
                        """
                        Parameter Material of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                def __getitem__(self, key: str) -> _CellZone:
                    return super().__getitem__(key)

            class Material(PyNamedObjectContainer):
                """
                .
                """
                class _Material(PyMenu):
                    """
                    Singleton _Material.
                    """
                    def __init__(self, service, rules, path):
                        self.CpSpecificHeat = self.__class__.CpSpecificHeat(service, rules, path + [("CpSpecificHeat", "")])
                        self.Density = self.__class__.Density(service, rules, path + [("Density", "")])
                        self.MolecularWeight = self.__class__.MolecularWeight(service, rules, path + [("MolecularWeight", "")])
                        self.ThermalConductivity = self.__class__.ThermalConductivity(service, rules, path + [("ThermalConductivity", "")])
                        self.ThermalExpansionCoefficient = self.__class__.ThermalExpansionCoefficient(service, rules, path + [("ThermalExpansionCoefficient", "")])
                        self.Viscosity = self.__class__.Viscosity(service, rules, path + [("Viscosity", "")])
                        self.FluentName = self.__class__.FluentName(service, rules, path + [("FluentName", "")])
                        self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                        self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                        self.LoadFromDatabase = self.__class__.LoadFromDatabase(service, rules, "LoadFromDatabase", path)
                        super().__init__(service, rules, path)

                    class CpSpecificHeat(PyMenu):
                        """
                        Singleton CpSpecificHeat.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class Density(PyMenu):
                        """
                        Singleton Density.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class MolecularWeight(PyMenu):
                        """
                        Singleton MolecularWeight.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class ThermalConductivity(PyMenu):
                        """
                        Singleton ThermalConductivity.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class ThermalExpansionCoefficient(PyMenu):
                        """
                        Singleton ThermalExpansionCoefficient.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class Viscosity(PyMenu):
                        """
                        Singleton Viscosity.
                        """
                        def __init__(self, service, rules, path):
                            self.Method = self.__class__.Method(service, rules, path + [("Method", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            super().__init__(service, rules, path)

                        class Method(PyTextual):
                            """
                            Parameter Method of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                    class FluentName(PyTextual):
                        """
                        Parameter FluentName of value type str.
                        """
                        pass

                    class Type(PyTextual):
                        """
                        Parameter Type of value type str.
                        """
                        pass

                    class _name_(PyTextual):
                        """
                        Parameter _name_ of value type str.
                        """
                        pass

                    class LoadFromDatabase(PyCommand):
                        """
                        Command LoadFromDatabase.

                        Parameters
                        ----------
                        MaterialName : str

                        Returns
                        -------
                        None
                        """
                        class _LoadFromDatabaseCommandArguments(PyCommandArguments):
                            def __init__(self, service, rules, command, path, id):
                                super().__init__(service, rules, command, path, id)
                                self.MaterialName = self._MaterialName(self, "MaterialName", service, rules, path)

                            class _MaterialName(PyTextualCommandArgumentsSubItem):
                                """
                                Argument MaterialName.
                                """

                        def create_instance(self) -> _LoadFromDatabaseCommandArguments:
                            args = self._get_create_instance_args()
                            if args is not None:
                                return self._LoadFromDatabaseCommandArguments(*args)

                def __getitem__(self, key: str) -> _Material:
                    return super().__getitem__(key)

            class Beta(PyParameter):
                """
                Parameter Beta of value type bool.
                """
                pass

        class Solution(PyMenu):
            """
            Singleton Solution.
            """
            def __init__(self, service, rules, path):
                self.Calculation = self.__class__.Calculation(service, rules, path + [("Calculation", "")])
                self.CalculationActivities = self.__class__.CalculationActivities(service, rules, path + [("CalculationActivities", "")])
                self.Controls = self.__class__.Controls(service, rules, path + [("Controls", "")])
                self.Methods = self.__class__.Methods(service, rules, path + [("Methods", "")])
                self.Monitors = self.__class__.Monitors(service, rules, path + [("Monitors", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                super().__init__(service, rules, path)

            class Calculation(PyMenu):
                """
                Singleton Calculation.
                """
                def __init__(self, service, rules, path):
                    self.AnalysisType = self.__class__.AnalysisType(service, rules, path + [("AnalysisType", "")])
                    self.MaxIterationsPerTimeStep = self.__class__.MaxIterationsPerTimeStep(service, rules, path + [("MaxIterationsPerTimeStep", "")])
                    self.NumberOfIterations = self.__class__.NumberOfIterations(service, rules, path + [("NumberOfIterations", "")])
                    self.NumberOfTimeSteps = self.__class__.NumberOfTimeSteps(service, rules, path + [("NumberOfTimeSteps", "")])
                    self.TimeStepSize = self.__class__.TimeStepSize(service, rules, path + [("TimeStepSize", "")])
                    self.Calculate = self.__class__.Calculate(service, rules, "Calculate", path)
                    self.Initialize = self.__class__.Initialize(service, rules, "Initialize", path)
                    self.Interrupt = self.__class__.Interrupt(service, rules, "Interrupt", path)
                    self.Pause = self.__class__.Pause(service, rules, "Pause", path)
                    self.Resume = self.__class__.Resume(service, rules, "Resume", path)
                    super().__init__(service, rules, path)

                class AnalysisType(PyTextual):
                    """
                    Parameter AnalysisType of value type str.
                    """
                    pass

                class MaxIterationsPerTimeStep(PyNumerical):
                    """
                    Parameter MaxIterationsPerTimeStep of value type int.
                    """
                    pass

                class NumberOfIterations(PyNumerical):
                    """
                    Parameter NumberOfIterations of value type int.
                    """
                    pass

                class NumberOfTimeSteps(PyNumerical):
                    """
                    Parameter NumberOfTimeSteps of value type int.
                    """
                    pass

                class TimeStepSize(PyNumerical):
                    """
                    Parameter TimeStepSize of value type float.
                    """
                    pass

                class Calculate(PyCommand):
                    """
                    Command Calculate.


                    Returns
                    -------
                    bool
                    """
                    class _CalculateCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)

                    def create_instance(self) -> _CalculateCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._CalculateCommandArguments(*args)

                class Initialize(PyCommand):
                    """
                    Command Initialize.


                    Returns
                    -------
                    bool
                    """
                    class _InitializeCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)

                    def create_instance(self) -> _InitializeCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._InitializeCommandArguments(*args)

                class Interrupt(PyCommand):
                    """
                    Command Interrupt.


                    Returns
                    -------
                    bool
                    """
                    class _InterruptCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)

                    def create_instance(self) -> _InterruptCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._InterruptCommandArguments(*args)

                class Pause(PyCommand):
                    """
                    Command Pause.


                    Returns
                    -------
                    bool
                    """
                    class _PauseCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)

                    def create_instance(self) -> _PauseCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._PauseCommandArguments(*args)

                class Resume(PyCommand):
                    """
                    Command Resume.


                    Returns
                    -------
                    bool
                    """
                    class _ResumeCommandArguments(PyCommandArguments):
                        def __init__(self, service, rules, command, path, id):
                            super().__init__(service, rules, command, path, id)

                    def create_instance(self) -> _ResumeCommandArguments:
                        args = self._get_create_instance_args()
                        if args is not None:
                            return self._ResumeCommandArguments(*args)

            class CalculationActivities(PyMenu):
                """
                Singleton CalculationActivities.
                """
                def __init__(self, service, rules, path):
                    self.SolutionAnimations = self.__class__.SolutionAnimations(service, rules, path + [("SolutionAnimations", "")])
                    super().__init__(service, rules, path)

                class SolutionAnimations(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _SolutionAnimations(PyMenu):
                        """
                        Singleton _SolutionAnimations.
                        """
                        def __init__(self, service, rules, path):
                            self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
                            self.IntegerIndex = self.__class__.IntegerIndex(service, rules, path + [("IntegerIndex", "")])
                            self.Projection = self.__class__.Projection(service, rules, path + [("Projection", "")])
                            self.RealIndex = self.__class__.RealIndex(service, rules, path + [("RealIndex", "")])
                            self.RecordAfter = self.__class__.RecordAfter(service, rules, path + [("RecordAfter", "")])
                            self.Sequence = self.__class__.Sequence(service, rules, path + [("Sequence", "")])
                            self.StorageDirectory = self.__class__.StorageDirectory(service, rules, path + [("StorageDirectory", "")])
                            self.StorageType = self.__class__.StorageType(service, rules, path + [("StorageType", "")])
                            self.View = self.__class__.View(service, rules, path + [("View", "")])
                            self.WindowId = self.__class__.WindowId(service, rules, path + [("WindowId", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                            self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                            self.Display = self.__class__.Display(service, rules, "Display", path)
                            self.PlayBack = self.__class__.PlayBack(service, rules, "PlayBack", path)
                            super().__init__(service, rules, path)

                        class Graphics(PyTextual):
                            """
                            Parameter Graphics of value type str.
                            """
                            pass

                        class IntegerIndex(PyNumerical):
                            """
                            Parameter IntegerIndex of value type int.
                            """
                            pass

                        class Projection(PyTextual):
                            """
                            Parameter Projection of value type str.
                            """
                            pass

                        class RealIndex(PyNumerical):
                            """
                            Parameter RealIndex of value type float.
                            """
                            pass

                        class RecordAfter(PyTextual):
                            """
                            Parameter RecordAfter of value type str.
                            """
                            pass

                        class Sequence(PyNumerical):
                            """
                            Parameter Sequence of value type int.
                            """
                            pass

                        class StorageDirectory(PyTextual):
                            """
                            Parameter StorageDirectory of value type str.
                            """
                            pass

                        class StorageType(PyTextual):
                            """
                            Parameter StorageType of value type str.
                            """
                            pass

                        class View(PyTextual):
                            """
                            Parameter View of value type str.
                            """
                            pass

                        class WindowId(PyNumerical):
                            """
                            Parameter WindowId of value type int.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                        class Apply(PyCommand):
                            """
                            Command Apply.


                            Returns
                            -------
                            bool
                            """
                            class _ApplyCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _ApplyCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._ApplyCommandArguments(*args)

                        class Delete(PyCommand):
                            """
                            Command Delete.


                            Returns
                            -------
                            bool
                            """
                            class _DeleteCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DeleteCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DeleteCommandArguments(*args)

                        class Display(PyCommand):
                            """
                            Command Display.


                            Returns
                            -------
                            bool
                            """
                            class _DisplayCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _DisplayCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._DisplayCommandArguments(*args)

                        class PlayBack(PyCommand):
                            """
                            Command PlayBack.


                            Returns
                            -------
                            bool
                            """
                            class _PlayBackCommandArguments(PyCommandArguments):
                                def __init__(self, service, rules, command, path, id):
                                    super().__init__(service, rules, command, path, id)

                            def create_instance(self) -> _PlayBackCommandArguments:
                                args = self._get_create_instance_args()
                                if args is not None:
                                    return self._PlayBackCommandArguments(*args)

                    def __getitem__(self, key: str) -> _SolutionAnimations:
                        return super().__getitem__(key)

            class Controls(PyMenu):
                """
                Singleton Controls.
                """
                def __init__(self, service, rules, path):
                    self.UnderRelaxationFactors = self.__class__.UnderRelaxationFactors(service, rules, path + [("UnderRelaxationFactors", "")])
                    self.CourantNumber = self.__class__.CourantNumber(service, rules, path + [("CourantNumber", "")])
                    super().__init__(service, rules, path)

                class UnderRelaxationFactors(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _UnderRelaxationFactors(PyMenu):
                        """
                        Singleton _UnderRelaxationFactors.
                        """
                        def __init__(self, service, rules, path):
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class DomainId(PyNumerical):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class InternalName(PyTextual):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class Value(PyNumerical):
                            """
                            Parameter Value of value type float.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _UnderRelaxationFactors:
                        return super().__getitem__(key)

                class CourantNumber(PyNumerical):
                    """
                    Parameter CourantNumber of value type float.
                    """
                    pass

            class Methods(PyMenu):
                """
                Singleton Methods.
                """
                def __init__(self, service, rules, path):
                    self.DiscretizationSchemes = self.__class__.DiscretizationSchemes(service, rules, path + [("DiscretizationSchemes", "")])
                    self.PVCouplingScheme = self.__class__.PVCouplingScheme(service, rules, path + [("PVCouplingScheme", "")])
                    self.PVCouplingSchemeAllowedValues = self.__class__.PVCouplingSchemeAllowedValues(service, rules, path + [("PVCouplingSchemeAllowedValues", "")])
                    super().__init__(service, rules, path)

                class DiscretizationSchemes(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _DiscretizationSchemes(PyMenu):
                        """
                        Singleton _DiscretizationSchemes.
                        """
                        def __init__(self, service, rules, path):
                            self.AllowedValues = self.__class__.AllowedValues(service, rules, path + [("AllowedValues", "")])
                            self.DomainId = self.__class__.DomainId(service, rules, path + [("DomainId", "")])
                            self.InternalName = self.__class__.InternalName(service, rules, path + [("InternalName", "")])
                            self.Value = self.__class__.Value(service, rules, path + [("Value", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class AllowedValues(PyTextual):
                            """
                            Parameter AllowedValues of value type list[str].
                            """
                            pass

                        class DomainId(PyNumerical):
                            """
                            Parameter DomainId of value type int.
                            """
                            pass

                        class InternalName(PyTextual):
                            """
                            Parameter InternalName of value type str.
                            """
                            pass

                        class Value(PyTextual):
                            """
                            Parameter Value of value type str.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _DiscretizationSchemes:
                        return super().__getitem__(key)

                class PVCouplingScheme(PyTextual):
                    """
                    Parameter PVCouplingScheme of value type str.
                    """
                    pass

                class PVCouplingSchemeAllowedValues(PyTextual):
                    """
                    Parameter PVCouplingSchemeAllowedValues of value type list[str].
                    """
                    pass

            class Monitors(PyMenu):
                """
                Singleton Monitors.
                """
                def __init__(self, service, rules, path):
                    self.ReportPlots = self.__class__.ReportPlots(service, rules, path + [("ReportPlots", "")])
                    self.Residuals = self.__class__.Residuals(service, rules, path + [("Residuals", "")])
                    super().__init__(service, rules, path)

                class ReportPlots(PyNamedObjectContainer):
                    """
                    .
                    """
                    class _ReportPlots(PyMenu):
                        """
                        Singleton _ReportPlots.
                        """
                        def __init__(self, service, rules, path):
                            self.Active = self.__class__.Active(service, rules, path + [("Active", "")])
                            self.Frequency = self.__class__.Frequency(service, rules, path + [("Frequency", "")])
                            self.FrequencyOf = self.__class__.FrequencyOf(service, rules, path + [("FrequencyOf", "")])
                            self.IsValid = self.__class__.IsValid(service, rules, path + [("IsValid", "")])
                            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                            self.Print = self.__class__.Print(service, rules, path + [("Print", "")])
                            self.ReportDefinitions = self.__class__.ReportDefinitions(service, rules, path + [("ReportDefinitions", "")])
                            self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                            self.UnitInfo = self.__class__.UnitInfo(service, rules, path + [("UnitInfo", "")])
                            self.XLabel = self.__class__.XLabel(service, rules, path + [("XLabel", "")])
                            self.YLabel = self.__class__.YLabel(service, rules, path + [("YLabel", "")])
                            self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                            super().__init__(service, rules, path)

                        class Active(PyParameter):
                            """
                            Parameter Active of value type bool.
                            """
                            pass

                        class Frequency(PyNumerical):
                            """
                            Parameter Frequency of value type int.
                            """
                            pass

                        class FrequencyOf(PyTextual):
                            """
                            Parameter FrequencyOf of value type str.
                            """
                            pass

                        class IsValid(PyParameter):
                            """
                            Parameter IsValid of value type bool.
                            """
                            pass

                        class Name(PyTextual):
                            """
                            Parameter Name of value type str.
                            """
                            pass

                        class Print(PyParameter):
                            """
                            Parameter Print of value type bool.
                            """
                            pass

                        class ReportDefinitions(PyTextual):
                            """
                            Parameter ReportDefinitions of value type list[str].
                            """
                            pass

                        class Title(PyTextual):
                            """
                            Parameter Title of value type str.
                            """
                            pass

                        class UnitInfo(PyTextual):
                            """
                            Parameter UnitInfo of value type str.
                            """
                            pass

                        class XLabel(PyTextual):
                            """
                            Parameter XLabel of value type str.
                            """
                            pass

                        class YLabel(PyTextual):
                            """
                            Parameter YLabel of value type str.
                            """
                            pass

                        class _name_(PyTextual):
                            """
                            Parameter _name_ of value type str.
                            """
                            pass

                    def __getitem__(self, key: str) -> _ReportPlots:
                        return super().__getitem__(key)

                class Residuals(PyMenu):
                    """
                    Singleton Residuals.
                    """
                    def __init__(self, service, rules, path):
                        self.Equation = self.__class__.Equation(service, rules, path + [("Equation", "")])
                        self.ConvergenceCriterionType = self.__class__.ConvergenceCriterionType(service, rules, path + [("ConvergenceCriterionType", "")])
                        super().__init__(service, rules, path)

                    class Equation(PyNamedObjectContainer):
                        """
                        .
                        """
                        class _Equation(PyMenu):
                            """
                            Singleton _Equation.
                            """
                            def __init__(self, service, rules, path):
                                self.AbsoluteCriterion = self.__class__.AbsoluteCriterion(service, rules, path + [("AbsoluteCriterion", "")])
                                self.CheckConvergence = self.__class__.CheckConvergence(service, rules, path + [("CheckConvergence", "")])
                                self.IsMonitored = self.__class__.IsMonitored(service, rules, path + [("IsMonitored", "")])
                                self.RelativeCriterion = self.__class__.RelativeCriterion(service, rules, path + [("RelativeCriterion", "")])
                                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                                super().__init__(service, rules, path)

                            class AbsoluteCriterion(PyNumerical):
                                """
                                Parameter AbsoluteCriterion of value type float.
                                """
                                pass

                            class CheckConvergence(PyParameter):
                                """
                                Parameter CheckConvergence of value type bool.
                                """
                                pass

                            class IsMonitored(PyParameter):
                                """
                                Parameter IsMonitored of value type bool.
                                """
                                pass

                            class RelativeCriterion(PyNumerical):
                                """
                                Parameter RelativeCriterion of value type float.
                                """
                                pass

                            class _name_(PyTextual):
                                """
                                Parameter _name_ of value type str.
                                """
                                pass

                        def __getitem__(self, key: str) -> _Equation:
                            return super().__getitem__(key)

                    class ConvergenceCriterionType(PyTextual):
                        """
                        Parameter ConvergenceCriterionType of value type str.
                        """
                        pass

            class State(PyMenu):
                """
                Singleton State.
                """
                def __init__(self, service, rules, path):
                    self.AeroOn = self.__class__.AeroOn(service, rules, path + [("AeroOn", "")])
                    self.CaseFileName = self.__class__.CaseFileName(service, rules, path + [("CaseFileName", "")])
                    self.CaseId = self.__class__.CaseId(service, rules, path + [("CaseId", "")])
                    self.CaseValid = self.__class__.CaseValid(service, rules, path + [("CaseValid", "")])
                    self.DataId = self.__class__.DataId(service, rules, path + [("DataId", "")])
                    self.DataValid = self.__class__.DataValid(service, rules, path + [("DataValid", "")])
                    self.GridId = self.__class__.GridId(service, rules, path + [("GridId", "")])
                    self.IcingOn = self.__class__.IcingOn(service, rules, path + [("IcingOn", "")])
                    super().__init__(service, rules, path)

                class AeroOn(PyParameter):
                    """
                    Parameter AeroOn of value type bool.
                    """
                    pass

                class CaseFileName(PyTextual):
                    """
                    Parameter CaseFileName of value type str.
                    """
                    pass

                class CaseId(PyNumerical):
                    """
                    Parameter CaseId of value type int.
                    """
                    pass

                class CaseValid(PyParameter):
                    """
                    Parameter CaseValid of value type bool.
                    """
                    pass

                class DataId(PyNumerical):
                    """
                    Parameter DataId of value type int.
                    """
                    pass

                class DataValid(PyParameter):
                    """
                    Parameter DataValid of value type bool.
                    """
                    pass

                class GridId(PyNumerical):
                    """
                    Parameter GridId of value type int.
                    """
                    pass

                class IcingOn(PyParameter):
                    """
                    Parameter IcingOn of value type bool.
                    """
                    pass

        class Streaming(PyMenu):
            """
            Singleton Streaming.
            """
            def __init__(self, service, rules, path):
                self.Ack = self.__class__.Ack(service, rules, path + [("Ack", "")])
                super().__init__(service, rules, path)

            class Ack(PyParameter):
                """
                Parameter Ack of value type bool.
                """
                pass

        class AppName(PyTextual):
            """
            Parameter AppName of value type str.
            """
            pass

        class ClearDatamodel(PyCommand):
            """
            Command ClearDatamodel.


            Returns
            -------
            None
            """
            class _ClearDatamodelCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _ClearDatamodelCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ClearDatamodelCommandArguments(*args)

        class ReadCase(PyCommand):
            """
            Command ReadCase.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            class _ReadCaseCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadCaseCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadCaseCommandArguments(*args)

        class ReadCaseAndData(PyCommand):
            """
            Command ReadCaseAndData.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            class _ReadCaseAndDataCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadCaseAndDataCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadCaseAndDataCommandArguments(*args)

        class ReadData(PyCommand):
            """
            Command ReadData.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            bool
            """
            class _ReadDataCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadDataCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadDataCommandArguments(*args)

        class SendCommand(PyCommand):
            """
            Command SendCommand.

            Parameters
            ----------
            Command : str
            PythonCommand : bool

            Returns
            -------
            bool
            """
            class _SendCommandCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Command = self._Command(self, "Command", service, rules, path)
                    self.PythonCommand = self._PythonCommand(self, "PythonCommand", service, rules, path)

                class _Command(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Command.
                    """

                class _PythonCommand(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PythonCommand.
                    """

            def create_instance(self) -> _SendCommandCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._SendCommandCommandArguments(*args)

        class WriteCase(PyCommand):
            """
            Command WriteCase.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            class _WriteCaseCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                    self.Binary = self._Binary(self, "Binary", service, rules, path)
                    self.Overwrite = self._Overwrite(self, "Overwrite", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

                class _Binary(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Binary.
                    """

                class _Overwrite(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Overwrite.
                    """

            def create_instance(self) -> _WriteCaseCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteCaseCommandArguments(*args)

        class WriteCaseAndData(PyCommand):
            """
            Command WriteCaseAndData.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            class _WriteCaseAndDataCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                    self.Binary = self._Binary(self, "Binary", service, rules, path)
                    self.Overwrite = self._Overwrite(self, "Overwrite", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

                class _Binary(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Binary.
                    """

                class _Overwrite(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Overwrite.
                    """

            def create_instance(self) -> _WriteCaseAndDataCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteCaseAndDataCommandArguments(*args)

        class WriteData(PyCommand):
            """
            Command WriteData.

            Parameters
            ----------
            FileName : str
            Binary : bool
            Overwrite : bool

            Returns
            -------
            bool
            """
            class _WriteDataCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                    self.Binary = self._Binary(self, "Binary", service, rules, path)
                    self.Overwrite = self._Overwrite(self, "Overwrite", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

                class _Binary(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Binary.
                    """

                class _Overwrite(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Overwrite.
                    """

            def create_instance(self) -> _WriteDataCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteDataCommandArguments(*args)

