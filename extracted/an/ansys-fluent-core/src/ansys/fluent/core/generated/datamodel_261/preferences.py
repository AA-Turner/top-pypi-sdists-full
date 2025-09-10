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
        self.AnsysCloudBurst = self.__class__.AnsysCloudBurst(service, rules, path + [("AnsysCloudBurst", "")])
        self.Appearance = self.__class__.Appearance(service, rules, path + [("Appearance", "")])
        self.GPUApp = self.__class__.GPUApp(service, rules, path + [("GPUApp", "")])
        self.General = self.__class__.General(service, rules, path + [("General", "")])
        self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
        self.MatProApp = self.__class__.MatProApp(service, rules, path + [("MatProApp", "")])
        self.MeshingWorkflow = self.__class__.MeshingWorkflow(service, rules, path + [("MeshingWorkflow", "")])
        self.Navigation = self.__class__.Navigation(service, rules, path + [("Navigation", "")])
        self.ParametricStudy = self.__class__.ParametricStudy(service, rules, path + [("ParametricStudy", "")])
        self.PrjApp = self.__class__.PrjApp(service, rules, path + [("PrjApp", "")])
        self.PythonConsole = self.__class__.PythonConsole(service, rules, path + [("PythonConsole", "")])
        self.Simulation = self.__class__.Simulation(service, rules, path + [("Simulation", "")])
        self.TurboSetup = self.__class__.TurboSetup(service, rules, path + [("TurboSetup", "")])
        self.TurboWorkflow = self.__class__.TurboWorkflow(service, rules, path + [("TurboWorkflow", "")])
        super().__init__(service, rules, path)

    class AnsysCloudBurst(PyMenu):
        """
        Singleton AnsysCloudBurst.
        """
        def __init__(self, service, rules, path):
            self.AuthenticationMethod = self.__class__.AuthenticationMethod(service, rules, path + [("AuthenticationMethod", "")])
            super().__init__(service, rules, path)

        class AuthenticationMethod(PyTextual):
            """
            Parameter AuthenticationMethod of value type str.
            """
            pass

    class Appearance(PyMenu):
        """
        Singleton Appearance.
        """
        def __init__(self, service, rules, path):
            self.AnsysLogo = self.__class__.AnsysLogo(service, rules, path + [("AnsysLogo", "")])
            self.Charts = self.__class__.Charts(service, rules, path + [("Charts", "")])
            self.Selections = self.__class__.Selections(service, rules, path + [("Selections", "")])
            self.AllowInterfaceBoundsFlags = self.__class__.AllowInterfaceBoundsFlags(service, rules, path + [("AllowInterfaceBoundsFlags", "")])
            self.ApplicationFontSize = self.__class__.ApplicationFontSize(service, rules, path + [("ApplicationFontSize", "")])
            self.AxisTriad = self.__class__.AxisTriad(service, rules, path + [("AxisTriad", "")])
            self.ColorTheme = self.__class__.ColorTheme(service, rules, path + [("ColorTheme", "")])
            self.Completer = self.__class__.Completer(service, rules, path + [("Completer", "")])
            self.CustomTitleBar = self.__class__.CustomTitleBar(service, rules, path + [("CustomTitleBar", "")])
            self.DefaultView = self.__class__.DefaultView(service, rules, path + [("DefaultView", "")])
            self.GraphicsBackgroundColor1 = self.__class__.GraphicsBackgroundColor1(service, rules, path + [("GraphicsBackgroundColor1", "")])
            self.GraphicsBackgroundColor2 = self.__class__.GraphicsBackgroundColor2(service, rules, path + [("GraphicsBackgroundColor2", "")])
            self.GraphicsBackgroundStyle = self.__class__.GraphicsBackgroundStyle(service, rules, path + [("GraphicsBackgroundStyle", "")])
            self.GraphicsColorTheme = self.__class__.GraphicsColorTheme(service, rules, path + [("GraphicsColorTheme", "")])
            self.GraphicsDefaultManualFaceColor = self.__class__.GraphicsDefaultManualFaceColor(service, rules, path + [("GraphicsDefaultManualFaceColor", "")])
            self.GraphicsDefaultManualNodeColor = self.__class__.GraphicsDefaultManualNodeColor(service, rules, path + [("GraphicsDefaultManualNodeColor", "")])
            self.GraphicsEdgeColor = self.__class__.GraphicsEdgeColor(service, rules, path + [("GraphicsEdgeColor", "")])
            self.GraphicsForegroundColor = self.__class__.GraphicsForegroundColor(service, rules, path + [("GraphicsForegroundColor", "")])
            self.GraphicsPartitionBoundaryColor = self.__class__.GraphicsPartitionBoundaryColor(service, rules, path + [("GraphicsPartitionBoundaryColor", "")])
            self.GraphicsSurfaceColor = self.__class__.GraphicsSurfaceColor(service, rules, path + [("GraphicsSurfaceColor", "")])
            self.GraphicsTitleWindowFramecolor = self.__class__.GraphicsTitleWindowFramecolor(service, rules, path + [("GraphicsTitleWindowFramecolor", "")])
            self.GraphicsView = self.__class__.GraphicsView(service, rules, path + [("GraphicsView", "")])
            self.GraphicsWallFaceColor = self.__class__.GraphicsWallFaceColor(service, rules, path + [("GraphicsWallFaceColor", "")])
            self.GroupByTreeView = self.__class__.GroupByTreeView(service, rules, path + [("GroupByTreeView", "")])
            self.GroupPhysicsByTreeView = self.__class__.GroupPhysicsByTreeView(service, rules, path + [("GroupPhysicsByTreeView", "")])
            self.ModelColorScheme = self.__class__.ModelColorScheme(service, rules, path + [("ModelColorScheme", "")])
            self.NumberOfFilesRecentlyUsed = self.__class__.NumberOfFilesRecentlyUsed(service, rules, path + [("NumberOfFilesRecentlyUsed", "")])
            self.NumberOfPastelColors = self.__class__.NumberOfPastelColors(service, rules, path + [("NumberOfPastelColors", "")])
            self.PastelColorSaturation = self.__class__.PastelColorSaturation(service, rules, path + [("PastelColorSaturation", "")])
            self.PastelColorValue = self.__class__.PastelColorValue(service, rules, path + [("PastelColorValue", "")])
            self.PyConsoleCompleter = self.__class__.PyConsoleCompleter(service, rules, path + [("PyConsoleCompleter", "")])
            self.QuickPropertyView = self.__class__.QuickPropertyView(service, rules, path + [("QuickPropertyView", "")])
            self.Ruler = self.__class__.Ruler(service, rules, path + [("Ruler", "")])
            self.ShowDefaultInterior = self.__class__.ShowDefaultInterior(service, rules, path + [("ShowDefaultInterior", "")])
            self.ShowEnabledModels = self.__class__.ShowEnabledModels(service, rules, path + [("ShowEnabledModels", "")])
            self.ShowInterfaceNonOverlappingBoundaries = self.__class__.ShowInterfaceNonOverlappingBoundaries(service, rules, path + [("ShowInterfaceNonOverlappingBoundaries", "")])
            self.ShowModelEdges = self.__class__.ShowModelEdges(service, rules, path + [("ShowModelEdges", "")])
            self.SolutionModeEdgeColorInMeshingMode = self.__class__.SolutionModeEdgeColorInMeshingMode(service, rules, path + [("SolutionModeEdgeColorInMeshingMode", "")])
            self.SurfaceEmissivity = self.__class__.SurfaceEmissivity(service, rules, path + [("SurfaceEmissivity", "")])
            self.SurfaceSpecularity = self.__class__.SurfaceSpecularity(service, rules, path + [("SurfaceSpecularity", "")])
            self.SurfaceSpecularityForContours = self.__class__.SurfaceSpecularityForContours(service, rules, path + [("SurfaceSpecularityForContours", "")])
            self.Titles = self.__class__.Titles(service, rules, path + [("Titles", "")])
            self.TitlesBorderOffset = self.__class__.TitlesBorderOffset(service, rules, path + [("TitlesBorderOffset", "")])
            super().__init__(service, rules, path)

        class AnsysLogo(PyMenu):
            """
            Singleton AnsysLogo.
            """
            def __init__(self, service, rules, path):
                self.Color = self.__class__.Color(service, rules, path + [("Color", "")])
                self.Visible = self.__class__.Visible(service, rules, path + [("Visible", "")])
                super().__init__(service, rules, path)

            class Color(PyTextual):
                """
                Parameter Color of value type str.
                """
                pass

            class Visible(PyParameter):
                """
                Parameter Visible of value type bool.
                """
                pass

        class Charts(PyMenu):
            """
            Singleton Charts.
            """
            def __init__(self, service, rules, path):
                self.Font = self.__class__.Font(service, rules, path + [("Font", "")])
                self.TextColor = self.__class__.TextColor(service, rules, path + [("TextColor", "")])
                self.CurveColors = self.__class__.CurveColors(service, rules, path + [("CurveColors", "")])
                self.EnableOpenGLForModernPlots = self.__class__.EnableOpenGLForModernPlots(service, rules, path + [("EnableOpenGLForModernPlots", "")])
                self.LegendAlignment = self.__class__.LegendAlignment(service, rules, path + [("LegendAlignment", "")])
                self.LegendVisibility = self.__class__.LegendVisibility(service, rules, path + [("LegendVisibility", "")])
                self.ModernPlotsEnabled = self.__class__.ModernPlotsEnabled(service, rules, path + [("ModernPlotsEnabled", "")])
                self.ModernPlotsPointsThreshold = self.__class__.ModernPlotsPointsThreshold(service, rules, path + [("ModernPlotsPointsThreshold", "")])
                self.PlotsBehavior = self.__class__.PlotsBehavior(service, rules, path + [("PlotsBehavior", "")])
                self.PrintPlotData = self.__class__.PrintPlotData(service, rules, path + [("PrintPlotData", "")])
                self.PrintResidualsData = self.__class__.PrintResidualsData(service, rules, path + [("PrintResidualsData", "")])
                self.Threshold = self.__class__.Threshold(service, rules, path + [("Threshold", "")])
                self.TooltipInterpolation = self.__class__.TooltipInterpolation(service, rules, path + [("TooltipInterpolation", "")])
                super().__init__(service, rules, path)

            class Font(PyMenu):
                """
                Singleton Font.
                """
                def __init__(self, service, rules, path):
                    self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                    self.AxesTitles = self.__class__.AxesTitles(service, rules, path + [("AxesTitles", "")])
                    self.Legend = self.__class__.Legend(service, rules, path + [("Legend", "")])
                    self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                    super().__init__(service, rules, path)

                class Axes(PyTextual):
                    """
                    Parameter Axes of value type str.
                    """
                    pass

                class AxesTitles(PyTextual):
                    """
                    Parameter AxesTitles of value type str.
                    """
                    pass

                class Legend(PyTextual):
                    """
                    Parameter Legend of value type str.
                    """
                    pass

                class Title(PyTextual):
                    """
                    Parameter Title of value type str.
                    """
                    pass

            class TextColor(PyMenu):
                """
                Singleton TextColor.
                """
                def __init__(self, service, rules, path):
                    self.Axes = self.__class__.Axes(service, rules, path + [("Axes", "")])
                    self.AxesTitles = self.__class__.AxesTitles(service, rules, path + [("AxesTitles", "")])
                    self.Legend = self.__class__.Legend(service, rules, path + [("Legend", "")])
                    self.Title = self.__class__.Title(service, rules, path + [("Title", "")])
                    super().__init__(service, rules, path)

                class Axes(PyTextual):
                    """
                    Parameter Axes of value type str.
                    """
                    pass

                class AxesTitles(PyTextual):
                    """
                    Parameter AxesTitles of value type str.
                    """
                    pass

                class Legend(PyTextual):
                    """
                    Parameter Legend of value type str.
                    """
                    pass

                class Title(PyTextual):
                    """
                    Parameter Title of value type str.
                    """
                    pass

            class CurveColors(PyTextual):
                """
                Parameter CurveColors of value type str.
                """
                pass

            class EnableOpenGLForModernPlots(PyParameter):
                """
                Parameter EnableOpenGLForModernPlots of value type bool.
                """
                pass

            class LegendAlignment(PyTextual):
                """
                Parameter LegendAlignment of value type str.
                """
                pass

            class LegendVisibility(PyParameter):
                """
                Parameter LegendVisibility of value type bool.
                """
                pass

            class ModernPlotsEnabled(PyParameter):
                """
                Parameter ModernPlotsEnabled of value type bool.
                """
                pass

            class ModernPlotsPointsThreshold(PyParameter):
                """
                Parameter ModernPlotsPointsThreshold of value type bool.
                """
                pass

            class PlotsBehavior(PyTextual):
                """
                Parameter PlotsBehavior of value type str.
                """
                pass

            class PrintPlotData(PyParameter):
                """
                Parameter PrintPlotData of value type bool.
                """
                pass

            class PrintResidualsData(PyNumerical):
                """
                Parameter PrintResidualsData of value type int.
                """
                pass

            class Threshold(PyNumerical):
                """
                Parameter Threshold of value type int.
                """
                pass

            class TooltipInterpolation(PyParameter):
                """
                Parameter TooltipInterpolation of value type bool.
                """
                pass

        class Selections(PyMenu):
            """
            Singleton Selections.
            """
            def __init__(self, service, rules, path):
                self.EnableHighlightEdgeTransparency = self.__class__.EnableHighlightEdgeTransparency(service, rules, path + [("EnableHighlightEdgeTransparency", "")])
                self.GeneralDisplacement = self.__class__.GeneralDisplacement(service, rules, path + [("GeneralDisplacement", "")])
                self.HighlightEdgeColor = self.__class__.HighlightEdgeColor(service, rules, path + [("HighlightEdgeColor", "")])
                self.HighlightEdgeWeight = self.__class__.HighlightEdgeWeight(service, rules, path + [("HighlightEdgeWeight", "")])
                self.HighlightFaceColor = self.__class__.HighlightFaceColor(service, rules, path + [("HighlightFaceColor", "")])
                self.HighlightGloss = self.__class__.HighlightGloss(service, rules, path + [("HighlightGloss", "")])
                self.HighlightSpecularComponent = self.__class__.HighlightSpecularComponent(service, rules, path + [("HighlightSpecularComponent", "")])
                self.HighlightTransparency = self.__class__.HighlightTransparency(service, rules, path + [("HighlightTransparency", "")])
                self.MouseHoverProbeValuesEnabled = self.__class__.MouseHoverProbeValuesEnabled(service, rules, path + [("MouseHoverProbeValuesEnabled", "")])
                self.MouseOverHighlightEnabled = self.__class__.MouseOverHighlightEnabled(service, rules, path + [("MouseOverHighlightEnabled", "")])
                self.ProbeTooltipHideDelayTimer = self.__class__.ProbeTooltipHideDelayTimer(service, rules, path + [("ProbeTooltipHideDelayTimer", "")])
                self.ProbeTooltipShowDelayTimer = self.__class__.ProbeTooltipShowDelayTimer(service, rules, path + [("ProbeTooltipShowDelayTimer", "")])
                super().__init__(service, rules, path)

            class EnableHighlightEdgeTransparency(PyParameter):
                """
                Parameter EnableHighlightEdgeTransparency of value type bool.
                """
                pass

            class GeneralDisplacement(PyNumerical):
                """
                Parameter GeneralDisplacement of value type int.
                """
                pass

            class HighlightEdgeColor(PyTextual):
                """
                Parameter HighlightEdgeColor of value type str.
                """
                pass

            class HighlightEdgeWeight(PyNumerical):
                """
                Parameter HighlightEdgeWeight of value type int.
                """
                pass

            class HighlightFaceColor(PyTextual):
                """
                Parameter HighlightFaceColor of value type str.
                """
                pass

            class HighlightGloss(PyNumerical):
                """
                Parameter HighlightGloss of value type float.
                """
                pass

            class HighlightSpecularComponent(PyTextual):
                """
                Parameter HighlightSpecularComponent of value type str.
                """
                pass

            class HighlightTransparency(PyNumerical):
                """
                Parameter HighlightTransparency of value type float.
                """
                pass

            class MouseHoverProbeValuesEnabled(PyParameter):
                """
                Parameter MouseHoverProbeValuesEnabled of value type bool.
                """
                pass

            class MouseOverHighlightEnabled(PyParameter):
                """
                Parameter MouseOverHighlightEnabled of value type bool.
                """
                pass

            class ProbeTooltipHideDelayTimer(PyNumerical):
                """
                Parameter ProbeTooltipHideDelayTimer of value type int.
                """
                pass

            class ProbeTooltipShowDelayTimer(PyNumerical):
                """
                Parameter ProbeTooltipShowDelayTimer of value type int.
                """
                pass

        class AllowInterfaceBoundsFlags(PyParameter):
            """
            Parameter AllowInterfaceBoundsFlags of value type bool.
            """
            pass

        class ApplicationFontSize(PyNumerical):
            """
            Parameter ApplicationFontSize of value type int.
            """
            pass

        class AxisTriad(PyParameter):
            """
            Parameter AxisTriad of value type bool.
            """
            pass

        class ColorTheme(PyTextual):
            """
            Parameter ColorTheme of value type str.
            """
            pass

        class Completer(PyParameter):
            """
            Parameter Completer of value type bool.
            """
            pass

        class CustomTitleBar(PyParameter):
            """
            Parameter CustomTitleBar of value type bool.
            """
            pass

        class DefaultView(PyTextual):
            """
            Parameter DefaultView of value type str.
            """
            pass

        class GraphicsBackgroundColor1(PyTextual):
            """
            Parameter GraphicsBackgroundColor1 of value type str.
            """
            pass

        class GraphicsBackgroundColor2(PyTextual):
            """
            Parameter GraphicsBackgroundColor2 of value type str.
            """
            pass

        class GraphicsBackgroundStyle(PyTextual):
            """
            Parameter GraphicsBackgroundStyle of value type str.
            """
            pass

        class GraphicsColorTheme(PyTextual):
            """
            Parameter GraphicsColorTheme of value type str.
            """
            pass

        class GraphicsDefaultManualFaceColor(PyTextual):
            """
            Parameter GraphicsDefaultManualFaceColor of value type str.
            """
            pass

        class GraphicsDefaultManualNodeColor(PyTextual):
            """
            Parameter GraphicsDefaultManualNodeColor of value type str.
            """
            pass

        class GraphicsEdgeColor(PyTextual):
            """
            Parameter GraphicsEdgeColor of value type str.
            """
            pass

        class GraphicsForegroundColor(PyTextual):
            """
            Parameter GraphicsForegroundColor of value type str.
            """
            pass

        class GraphicsPartitionBoundaryColor(PyTextual):
            """
            Parameter GraphicsPartitionBoundaryColor of value type str.
            """
            pass

        class GraphicsSurfaceColor(PyTextual):
            """
            Parameter GraphicsSurfaceColor of value type str.
            """
            pass

        class GraphicsTitleWindowFramecolor(PyTextual):
            """
            Parameter GraphicsTitleWindowFramecolor of value type str.
            """
            pass

        class GraphicsView(PyTextual):
            """
            Parameter GraphicsView of value type str.
            """
            pass

        class GraphicsWallFaceColor(PyTextual):
            """
            Parameter GraphicsWallFaceColor of value type str.
            """
            pass

        class GroupByTreeView(PyTextual):
            """
            Parameter GroupByTreeView of value type str.
            """
            pass

        class GroupPhysicsByTreeView(PyTextual):
            """
            Parameter GroupPhysicsByTreeView of value type str.
            """
            pass

        class ModelColorScheme(PyTextual):
            """
            Parameter ModelColorScheme of value type str.
            """
            pass

        class NumberOfFilesRecentlyUsed(PyNumerical):
            """
            Parameter NumberOfFilesRecentlyUsed of value type int.
            """
            pass

        class NumberOfPastelColors(PyTextual):
            """
            Parameter NumberOfPastelColors of value type str.
            """
            pass

        class PastelColorSaturation(PyNumerical):
            """
            Parameter PastelColorSaturation of value type float.
            """
            pass

        class PastelColorValue(PyNumerical):
            """
            Parameter PastelColorValue of value type float.
            """
            pass

        class PyConsoleCompleter(PyParameter):
            """
            Parameter PyConsoleCompleter of value type bool.
            """
            pass

        class QuickPropertyView(PyParameter):
            """
            Parameter QuickPropertyView of value type bool.
            """
            pass

        class Ruler(PyParameter):
            """
            Parameter Ruler of value type bool.
            """
            pass

        class ShowDefaultInterior(PyParameter):
            """
            Parameter ShowDefaultInterior of value type bool.
            """
            pass

        class ShowEnabledModels(PyParameter):
            """
            Parameter ShowEnabledModels of value type bool.
            """
            pass

        class ShowInterfaceNonOverlappingBoundaries(PyParameter):
            """
            Parameter ShowInterfaceNonOverlappingBoundaries of value type bool.
            """
            pass

        class ShowModelEdges(PyParameter):
            """
            Parameter ShowModelEdges of value type bool.
            """
            pass

        class SolutionModeEdgeColorInMeshingMode(PyParameter):
            """
            Parameter SolutionModeEdgeColorInMeshingMode of value type bool.
            """
            pass

        class SurfaceEmissivity(PyNumerical):
            """
            Parameter SurfaceEmissivity of value type float.
            """
            pass

        class SurfaceSpecularity(PyNumerical):
            """
            Parameter SurfaceSpecularity of value type float.
            """
            pass

        class SurfaceSpecularityForContours(PyNumerical):
            """
            Parameter SurfaceSpecularityForContours of value type float.
            """
            pass

        class Titles(PyParameter):
            """
            Parameter Titles of value type bool.
            """
            pass

        class TitlesBorderOffset(PyNumerical):
            """
            Parameter TitlesBorderOffset of value type float.
            """
            pass

    class GPUApp(PyMenu):
        """
        Singleton GPUApp.
        """
        def __init__(self, service, rules, path):
            self.AlphaFeatures = self.__class__.AlphaFeatures(service, rules, path + [("AlphaFeatures", "")])
            super().__init__(service, rules, path)

        class AlphaFeatures(PyParameter):
            """
            Parameter AlphaFeatures of value type bool.
            """
            pass

    class General(PyMenu):
        """
        Singleton General.
        """
        def __init__(self, service, rules, path):
            self.StartupMessages = self.__class__.StartupMessages(service, rules, path + [("StartupMessages", "")])
            self.AdvancedPartition = self.__class__.AdvancedPartition(service, rules, path + [("AdvancedPartition", "")])
            self.AutomaticTranscript = self.__class__.AutomaticTranscript(service, rules, path + [("AutomaticTranscript", "")])
            self.DefaultIOFormat = self.__class__.DefaultIOFormat(service, rules, path + [("DefaultIOFormat", "")])
            self.DockEditor = self.__class__.DockEditor(service, rules, path + [("DockEditor", "")])
            self.FlowModel = self.__class__.FlowModel(service, rules, path + [("FlowModel", "")])
            self.IdleTimeout = self.__class__.IdleTimeout(service, rules, path + [("IdleTimeout", "")])
            self.ImportPhysicsVolumeDefinitions = self.__class__.ImportPhysicsVolumeDefinitions(service, rules, path + [("ImportPhysicsVolumeDefinitions", "")])
            self.InitialPhysicsVolumeDefinitions = self.__class__.InitialPhysicsVolumeDefinitions(service, rules, path + [("InitialPhysicsVolumeDefinitions", "")])
            self.SkipCreationOfGroupsPointingToSingleEntity = self.__class__.SkipCreationOfGroupsPointingToSingleEntity(service, rules, path + [("SkipCreationOfGroupsPointingToSingleEntity", "")])
            self.UTLCreateDefaultObjectIfPossible = self.__class__.UTLCreateDefaultObjectIfPossible(service, rules, path + [("UTLCreateDefaultObjectIfPossible", "")])
            self.UTLMode = self.__class__.UTLMode(service, rules, path + [("UTLMode", "")])
            super().__init__(service, rules, path)

        class StartupMessages(PyMenu):
            """
            Singleton StartupMessages.
            """
            def __init__(self, service, rules, path):
                self.ColorThemeChangeMessage = self.__class__.ColorThemeChangeMessage(service, rules, path + [("ColorThemeChangeMessage", "")])
                self.KeyBehavioralChangesMessage = self.__class__.KeyBehavioralChangesMessage(service, rules, path + [("KeyBehavioralChangesMessage", "")])
                self.QAServiceMessage = self.__class__.QAServiceMessage(service, rules, path + [("QAServiceMessage", "")])
                super().__init__(service, rules, path)

            class ColorThemeChangeMessage(PyParameter):
                """
                Parameter ColorThemeChangeMessage of value type bool.
                """
                pass

            class KeyBehavioralChangesMessage(PyParameter):
                """
                Parameter KeyBehavioralChangesMessage of value type bool.
                """
                pass

            class QAServiceMessage(PyParameter):
                """
                Parameter QAServiceMessage of value type bool.
                """
                pass

        class AdvancedPartition(PyTextual):
            """
            Parameter AdvancedPartition of value type str.
            """
            pass

        class AutomaticTranscript(PyParameter):
            """
            Parameter AutomaticTranscript of value type bool.
            """
            pass

        class DefaultIOFormat(PyTextual):
            """
            Parameter DefaultIOFormat of value type str.
            """
            pass

        class DockEditor(PyParameter):
            """
            Parameter DockEditor of value type bool.
            """
            pass

        class FlowModel(PyTextual):
            """
            Parameter FlowModel of value type str.
            """
            pass

        class IdleTimeout(PyNumerical):
            """
            Parameter IdleTimeout of value type int.
            """
            pass

        class ImportPhysicsVolumeDefinitions(PyTextual):
            """
            Parameter ImportPhysicsVolumeDefinitions of value type str.
            """
            pass

        class InitialPhysicsVolumeDefinitions(PyTextual):
            """
            Parameter InitialPhysicsVolumeDefinitions of value type str.
            """
            pass

        class SkipCreationOfGroupsPointingToSingleEntity(PyParameter):
            """
            Parameter SkipCreationOfGroupsPointingToSingleEntity of value type bool.
            """
            pass

        class UTLCreateDefaultObjectIfPossible(PyParameter):
            """
            Parameter UTLCreateDefaultObjectIfPossible of value type bool.
            """
            pass

        class UTLMode(PyParameter):
            """
            Parameter UTLMode of value type bool.
            """
            pass

    class Graphics(PyMenu):
        """
        Singleton Graphics.
        """
        def __init__(self, service, rules, path):
            self.BoundaryMarkers = self.__class__.BoundaryMarkers(service, rules, path + [("BoundaryMarkers", "")])
            self.ColormapSettings = self.__class__.ColormapSettings(service, rules, path + [("ColormapSettings", "")])
            self.DisplayLists = self.__class__.DisplayLists(service, rules, path + [("DisplayLists", "")])
            self.EmbeddedWindows = self.__class__.EmbeddedWindows(service, rules, path + [("EmbeddedWindows", "")])
            self.ExportVideoSettings = self.__class__.ExportVideoSettings(service, rules, path + [("ExportVideoSettings", "")])
            self.GraphicsEffects = self.__class__.GraphicsEffects(service, rules, path + [("GraphicsEffects", "")])
            self.HardcopySettings = self.__class__.HardcopySettings(service, rules, path + [("HardcopySettings", "")])
            self.Lighting = self.__class__.Lighting(service, rules, path + [("Lighting", "")])
            self.ManageHoopsMemory = self.__class__.ManageHoopsMemory(service, rules, path + [("ManageHoopsMemory", "")])
            self.MaterialEffects = self.__class__.MaterialEffects(service, rules, path + [("MaterialEffects", "")])
            self.MeshingMode = self.__class__.MeshingMode(service, rules, path + [("MeshingMode", "")])
            self.Performance = self.__class__.Performance(service, rules, path + [("Performance", "")])
            self.RayTracingOptions = self.__class__.RayTracingOptions(service, rules, path + [("RayTracingOptions", "")])
            self.Transparency = self.__class__.Transparency(service, rules, path + [("Transparency", "")])
            self.VectorSettings = self.__class__.VectorSettings(service, rules, path + [("VectorSettings", "")])
            self.AnimationOption = self.__class__.AnimationOption(service, rules, path + [("AnimationOption", "")])
            self.BackfaceCull = self.__class__.BackfaceCull(service, rules, path + [("BackfaceCull", "")])
            self.CameraNearLimit = self.__class__.CameraNearLimit(service, rules, path + [("CameraNearLimit", "")])
            self.DoubleBuffering = self.__class__.DoubleBuffering(service, rules, path + [("DoubleBuffering", "")])
            self.EnableCameraNearLimitToAvoidZFighting = self.__class__.EnableCameraNearLimitToAvoidZFighting(service, rules, path + [("EnableCameraNearLimitToAvoidZFighting", "")])
            self.EnableNonObjectBasedWorkflow = self.__class__.EnableNonObjectBasedWorkflow(service, rules, path + [("EnableNonObjectBasedWorkflow", "")])
            self.EventPollInterval = self.__class__.EventPollInterval(service, rules, path + [("EventPollInterval", "")])
            self.EventPollTimeout = self.__class__.EventPollTimeout(service, rules, path + [("EventPollTimeout", "")])
            self.ForceKeyFrameAnimationMarkersToOff = self.__class__.ForceKeyFrameAnimationMarkersToOff(service, rules, path + [("ForceKeyFrameAnimationMarkersToOff", "")])
            self.GraphicsWindowLineWidth = self.__class__.GraphicsWindowLineWidth(service, rules, path + [("GraphicsWindowLineWidth", "")])
            self.GraphicsWindowPointSymbol = self.__class__.GraphicsWindowPointSymbol(service, rules, path + [("GraphicsWindowPointSymbol", "")])
            self.HiddenSurfaceRemovalMethod = self.__class__.HiddenSurfaceRemovalMethod(service, rules, path + [("HiddenSurfaceRemovalMethod", "")])
            self.HigherResolutionGraphicsWindowLineWidth = self.__class__.HigherResolutionGraphicsWindowLineWidth(service, rules, path + [("HigherResolutionGraphicsWindowLineWidth", "")])
            self.LowerResolutionGraphicsWindowLineWidth = self.__class__.LowerResolutionGraphicsWindowLineWidth(service, rules, path + [("LowerResolutionGraphicsWindowLineWidth", "")])
            self.MarkerDrawingMode = self.__class__.MarkerDrawingMode(service, rules, path + [("MarkerDrawingMode", "")])
            self.MaxGraphicsTextSize = self.__class__.MaxGraphicsTextSize(service, rules, path + [("MaxGraphicsTextSize", "")])
            self.MinGraphicsTextSize = self.__class__.MinGraphicsTextSize(service, rules, path + [("MinGraphicsTextSize", "")])
            self.PlotLegendMargin = self.__class__.PlotLegendMargin(service, rules, path + [("PlotLegendMargin", "")])
            self.PointToolSize = self.__class__.PointToolSize(service, rules, path + [("PointToolSize", "")])
            self.RemovePartitionLines = self.__class__.RemovePartitionLines(service, rules, path + [("RemovePartitionLines", "")])
            self.RemovePartitionLinesTolerance = self.__class__.RemovePartitionLinesTolerance(service, rules, path + [("RemovePartitionLinesTolerance", "")])
            self.RotationCenterpointVisible = self.__class__.RotationCenterpointVisible(service, rules, path + [("RotationCenterpointVisible", "")])
            self.ScrollWheelEventEndTimer = self.__class__.ScrollWheelEventEndTimer(service, rules, path + [("ScrollWheelEventEndTimer", "")])
            self.SelectionHighlightWindow = self.__class__.SelectionHighlightWindow(service, rules, path + [("SelectionHighlightWindow", "")])
            self.SetCameraNormalToSurfaceIncrements = self.__class__.SetCameraNormalToSurfaceIncrements(service, rules, path + [("SetCameraNormalToSurfaceIncrements", "")])
            self.ShowHiddenLines = self.__class__.ShowHiddenLines(service, rules, path + [("ShowHiddenLines", "")])
            self.ShowHiddenSurfaces = self.__class__.ShowHiddenSurfaces(service, rules, path + [("ShowHiddenSurfaces", "")])
            self.SurfaceGeneralDisplacement = self.__class__.SurfaceGeneralDisplacement(service, rules, path + [("SurfaceGeneralDisplacement", "")])
            self.SwitchToOpenGLForRemoteVisualization = self.__class__.SwitchToOpenGLForRemoteVisualization(service, rules, path + [("SwitchToOpenGLForRemoteVisualization", "")])
            self.TestUseExternalFunction = self.__class__.TestUseExternalFunction(service, rules, path + [("TestUseExternalFunction", "")])
            self.TextWindowLineWidth = self.__class__.TextWindowLineWidth(service, rules, path + [("TextWindowLineWidth", "")])
            super().__init__(service, rules, path)

        class BoundaryMarkers(PyMenu):
            """
            Singleton BoundaryMarkers.
            """
            def __init__(self, service, rules, path):
                self.AutomaticMarkerScaling = self.__class__.AutomaticMarkerScaling(service, rules, path + [("AutomaticMarkerScaling", "")])
                self.ColorOption = self.__class__.ColorOption(service, rules, path + [("ColorOption", "")])
                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                self.ExcludeFromBounding = self.__class__.ExcludeFromBounding(service, rules, path + [("ExcludeFromBounding", "")])
                self.InletColor = self.__class__.InletColor(service, rules, path + [("InletColor", "")])
                self.MarkerFraction = self.__class__.MarkerFraction(service, rules, path + [("MarkerFraction", "")])
                self.MarkerSizeLimitingScaleMultiplier = self.__class__.MarkerSizeLimitingScaleMultiplier(service, rules, path + [("MarkerSizeLimitingScaleMultiplier", "")])
                self.MarkersLimit = self.__class__.MarkersLimit(service, rules, path + [("MarkersLimit", "")])
                self.OutletColor = self.__class__.OutletColor(service, rules, path + [("OutletColor", "")])
                self.ScaleMarker = self.__class__.ScaleMarker(service, rules, path + [("ScaleMarker", "")])
                self.ShowInletMarkers = self.__class__.ShowInletMarkers(service, rules, path + [("ShowInletMarkers", "")])
                self.ShowOutletMarkers = self.__class__.ShowOutletMarkers(service, rules, path + [("ShowOutletMarkers", "")])
                super().__init__(service, rules, path)

            class AutomaticMarkerScaling(PyParameter):
                """
                Parameter AutomaticMarkerScaling of value type bool.
                """
                pass

            class ColorOption(PyTextual):
                """
                Parameter ColorOption of value type str.
                """
                pass

            class Enabled(PyParameter):
                """
                Parameter Enabled of value type bool.
                """
                pass

            class ExcludeFromBounding(PyParameter):
                """
                Parameter ExcludeFromBounding of value type bool.
                """
                pass

            class InletColor(PyTextual):
                """
                Parameter InletColor of value type str.
                """
                pass

            class MarkerFraction(PyNumerical):
                """
                Parameter MarkerFraction of value type float.
                """
                pass

            class MarkerSizeLimitingScaleMultiplier(PyNumerical):
                """
                Parameter MarkerSizeLimitingScaleMultiplier of value type float.
                """
                pass

            class MarkersLimit(PyNumerical):
                """
                Parameter MarkersLimit of value type int.
                """
                pass

            class OutletColor(PyTextual):
                """
                Parameter OutletColor of value type str.
                """
                pass

            class ScaleMarker(PyNumerical):
                """
                Parameter ScaleMarker of value type float.
                """
                pass

            class ShowInletMarkers(PyParameter):
                """
                Parameter ShowInletMarkers of value type bool.
                """
                pass

            class ShowOutletMarkers(PyParameter):
                """
                Parameter ShowOutletMarkers of value type bool.
                """
                pass

        class ColormapSettings(PyMenu):
            """
            Singleton ColormapSettings.
            """
            def __init__(self, service, rules, path):
                self.Alignment = self.__class__.Alignment(service, rules, path + [("Alignment", "")])
                self.AspectRatioWhenHorizontal = self.__class__.AspectRatioWhenHorizontal(service, rules, path + [("AspectRatioWhenHorizontal", "")])
                self.AspectRatioWhenVertical = self.__class__.AspectRatioWhenVertical(service, rules, path + [("AspectRatioWhenVertical", "")])
                self.AutoRefitOnResize = self.__class__.AutoRefitOnResize(service, rules, path + [("AutoRefitOnResize", "")])
                self.AutomaticResize = self.__class__.AutomaticResize(service, rules, path + [("AutomaticResize", "")])
                self.BorderStyle = self.__class__.BorderStyle(service, rules, path + [("BorderStyle", "")])
                self.Colormap = self.__class__.Colormap(service, rules, path + [("Colormap", "")])
                self.IsolinesPositionOffset = self.__class__.IsolinesPositionOffset(service, rules, path + [("IsolinesPositionOffset", "")])
                self.Labels = self.__class__.Labels(service, rules, path + [("Labels", "")])
                self.Levels = self.__class__.Levels(service, rules, path + [("Levels", "")])
                self.LogScale = self.__class__.LogScale(service, rules, path + [("LogScale", "")])
                self.MajorLengthToScreenRatioWhenHorizontal = self.__class__.MajorLengthToScreenRatioWhenHorizontal(service, rules, path + [("MajorLengthToScreenRatioWhenHorizontal", "")])
                self.MajorLengthToScreenRatioWhenVertical = self.__class__.MajorLengthToScreenRatioWhenVertical(service, rules, path + [("MajorLengthToScreenRatioWhenVertical", "")])
                self.MarginFromEdgeToScreenRatio = self.__class__.MarginFromEdgeToScreenRatio(service, rules, path + [("MarginFromEdgeToScreenRatio", "")])
                self.MaxSizeScaleFactor = self.__class__.MaxSizeScaleFactor(service, rules, path + [("MaxSizeScaleFactor", "")])
                self.MinSizeScaleFactor = self.__class__.MinSizeScaleFactor(service, rules, path + [("MinSizeScaleFactor", "")])
                self.NumberFormatPrecision = self.__class__.NumberFormatPrecision(service, rules, path + [("NumberFormatPrecision", "")])
                self.NumberFormatType = self.__class__.NumberFormatType(service, rules, path + [("NumberFormatType", "")])
                self.PreserveAspectRatioForHardcopy = self.__class__.PreserveAspectRatioForHardcopy(service, rules, path + [("PreserveAspectRatioForHardcopy", "")])
                self.ShowColormap = self.__class__.ShowColormap(service, rules, path + [("ShowColormap", "")])
                self.SkipValue = self.__class__.SkipValue(service, rules, path + [("SkipValue", "")])
                self.TextBehavior = self.__class__.TextBehavior(service, rules, path + [("TextBehavior", "")])
                self.TextFontAutomaticHorizontalSize = self.__class__.TextFontAutomaticHorizontalSize(service, rules, path + [("TextFontAutomaticHorizontalSize", "")])
                self.TextFontAutomaticSize = self.__class__.TextFontAutomaticSize(service, rules, path + [("TextFontAutomaticSize", "")])
                self.TextFontAutomaticUnits = self.__class__.TextFontAutomaticUnits(service, rules, path + [("TextFontAutomaticUnits", "")])
                self.TextFontAutomaticVerticalSize = self.__class__.TextFontAutomaticVerticalSize(service, rules, path + [("TextFontAutomaticVerticalSize", "")])
                self.TextFontFixedHorizontalSize = self.__class__.TextFontFixedHorizontalSize(service, rules, path + [("TextFontFixedHorizontalSize", "")])
                self.TextFontFixedSize = self.__class__.TextFontFixedSize(service, rules, path + [("TextFontFixedSize", "")])
                self.TextFontFixedUnits = self.__class__.TextFontFixedUnits(service, rules, path + [("TextFontFixedUnits", "")])
                self.TextFontFixedVerticalSize = self.__class__.TextFontFixedVerticalSize(service, rules, path + [("TextFontFixedVerticalSize", "")])
                self.TextFontName = self.__class__.TextFontName(service, rules, path + [("TextFontName", "")])
                self.TextTruncationLimitForHorizontalColormaps = self.__class__.TextTruncationLimitForHorizontalColormaps(service, rules, path + [("TextTruncationLimitForHorizontalColormaps", "")])
                self.TextTruncationLimitForVerticalColormaps = self.__class__.TextTruncationLimitForVerticalColormaps(service, rules, path + [("TextTruncationLimitForVerticalColormaps", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self.UseNoSubWindows = self.__class__.UseNoSubWindows(service, rules, path + [("UseNoSubWindows", "")])
                super().__init__(service, rules, path)

            class Alignment(PyTextual):
                """
                Parameter Alignment of value type str.
                """
                pass

            class AspectRatioWhenHorizontal(PyNumerical):
                """
                Parameter AspectRatioWhenHorizontal of value type float.
                """
                pass

            class AspectRatioWhenVertical(PyNumerical):
                """
                Parameter AspectRatioWhenVertical of value type float.
                """
                pass

            class AutoRefitOnResize(PyParameter):
                """
                Parameter AutoRefitOnResize of value type bool.
                """
                pass

            class AutomaticResize(PyParameter):
                """
                Parameter AutomaticResize of value type bool.
                """
                pass

            class BorderStyle(PyTextual):
                """
                Parameter BorderStyle of value type str.
                """
                pass

            class Colormap(PyTextual):
                """
                Parameter Colormap of value type str.
                """
                pass

            class IsolinesPositionOffset(PyNumerical):
                """
                Parameter IsolinesPositionOffset of value type float.
                """
                pass

            class Labels(PyParameter):
                """
                Parameter Labels of value type bool.
                """
                pass

            class Levels(PyNumerical):
                """
                Parameter Levels of value type int.
                """
                pass

            class LogScale(PyParameter):
                """
                Parameter LogScale of value type bool.
                """
                pass

            class MajorLengthToScreenRatioWhenHorizontal(PyNumerical):
                """
                Parameter MajorLengthToScreenRatioWhenHorizontal of value type float.
                """
                pass

            class MajorLengthToScreenRatioWhenVertical(PyNumerical):
                """
                Parameter MajorLengthToScreenRatioWhenVertical of value type float.
                """
                pass

            class MarginFromEdgeToScreenRatio(PyNumerical):
                """
                Parameter MarginFromEdgeToScreenRatio of value type float.
                """
                pass

            class MaxSizeScaleFactor(PyNumerical):
                """
                Parameter MaxSizeScaleFactor of value type float.
                """
                pass

            class MinSizeScaleFactor(PyNumerical):
                """
                Parameter MinSizeScaleFactor of value type float.
                """
                pass

            class NumberFormatPrecision(PyNumerical):
                """
                Parameter NumberFormatPrecision of value type int.
                """
                pass

            class NumberFormatType(PyTextual):
                """
                Parameter NumberFormatType of value type str.
                """
                pass

            class PreserveAspectRatioForHardcopy(PyParameter):
                """
                Parameter PreserveAspectRatioForHardcopy of value type bool.
                """
                pass

            class ShowColormap(PyParameter):
                """
                Parameter ShowColormap of value type bool.
                """
                pass

            class SkipValue(PyNumerical):
                """
                Parameter SkipValue of value type int.
                """
                pass

            class TextBehavior(PyTextual):
                """
                Parameter TextBehavior of value type str.
                """
                pass

            class TextFontAutomaticHorizontalSize(PyNumerical):
                """
                Parameter TextFontAutomaticHorizontalSize of value type float.
                """
                pass

            class TextFontAutomaticSize(PyNumerical):
                """
                Parameter TextFontAutomaticSize of value type float.
                """
                pass

            class TextFontAutomaticUnits(PyTextual):
                """
                Parameter TextFontAutomaticUnits of value type str.
                """
                pass

            class TextFontAutomaticVerticalSize(PyNumerical):
                """
                Parameter TextFontAutomaticVerticalSize of value type float.
                """
                pass

            class TextFontFixedHorizontalSize(PyNumerical):
                """
                Parameter TextFontFixedHorizontalSize of value type int.
                """
                pass

            class TextFontFixedSize(PyNumerical):
                """
                Parameter TextFontFixedSize of value type int.
                """
                pass

            class TextFontFixedUnits(PyTextual):
                """
                Parameter TextFontFixedUnits of value type str.
                """
                pass

            class TextFontFixedVerticalSize(PyNumerical):
                """
                Parameter TextFontFixedVerticalSize of value type int.
                """
                pass

            class TextFontName(PyTextual):
                """
                Parameter TextFontName of value type str.
                """
                pass

            class TextTruncationLimitForHorizontalColormaps(PyNumerical):
                """
                Parameter TextTruncationLimitForHorizontalColormaps of value type int.
                """
                pass

            class TextTruncationLimitForVerticalColormaps(PyNumerical):
                """
                Parameter TextTruncationLimitForVerticalColormaps of value type int.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class UseNoSubWindows(PyParameter):
                """
                Parameter UseNoSubWindows of value type bool.
                """
                pass

        class DisplayLists(PyMenu):
            """
            Singleton DisplayLists.
            """
            def __init__(self, service, rules, path):
                self.Options = self.__class__.Options(service, rules, path + [("Options", "")])
                super().__init__(service, rules, path)

            class Options(PyTextual):
                """
                Parameter Options of value type str.
                """
                pass

        class EmbeddedWindows(PyMenu):
            """
            Singleton EmbeddedWindows.
            """
            def __init__(self, service, rules, path):
                self.DefaultEmbeddedMeshWindowsView = self.__class__.DefaultEmbeddedMeshWindowsView(service, rules, path + [("DefaultEmbeddedMeshWindowsView", "")])
                self.DefaultEmbeddedWindowsView = self.__class__.DefaultEmbeddedWindowsView(service, rules, path + [("DefaultEmbeddedWindowsView", "")])
                self.SaveEmbeddedWindowLayout = self.__class__.SaveEmbeddedWindowLayout(service, rules, path + [("SaveEmbeddedWindowLayout", "")])
                self.ShowBorderForEmbeddedWindow = self.__class__.ShowBorderForEmbeddedWindow(service, rules, path + [("ShowBorderForEmbeddedWindow", "")])
                super().__init__(service, rules, path)

            class DefaultEmbeddedMeshWindowsView(PyParameter):
                """
                Parameter DefaultEmbeddedMeshWindowsView of value type bool.
                """
                pass

            class DefaultEmbeddedWindowsView(PyParameter):
                """
                Parameter DefaultEmbeddedWindowsView of value type bool.
                """
                pass

            class SaveEmbeddedWindowLayout(PyParameter):
                """
                Parameter SaveEmbeddedWindowLayout of value type bool.
                """
                pass

            class ShowBorderForEmbeddedWindow(PyParameter):
                """
                Parameter ShowBorderForEmbeddedWindow of value type bool.
                """
                pass

        class ExportVideoSettings(PyMenu):
            """
            Singleton ExportVideoSettings.
            """
            def __init__(self, service, rules, path):
                self.AdvancedVideoQualityOptions = self.__class__.AdvancedVideoQualityOptions(service, rules, path + [("AdvancedVideoQualityOptions", "")])
                self.VideoFPS = self.__class__.VideoFPS(service, rules, path + [("VideoFPS", "")])
                self.VideoFormat = self.__class__.VideoFormat(service, rules, path + [("VideoFormat", "")])
                self.VideoQuality = self.__class__.VideoQuality(service, rules, path + [("VideoQuality", "")])
                self.VideoResoutionX = self.__class__.VideoResoutionX(service, rules, path + [("VideoResoutionX", "")])
                self.VideoResoutionY = self.__class__.VideoResoutionY(service, rules, path + [("VideoResoutionY", "")])
                self.VideoScale = self.__class__.VideoScale(service, rules, path + [("VideoScale", "")])
                self.VideoSmoothScaling = self.__class__.VideoSmoothScaling(service, rules, path + [("VideoSmoothScaling", "")])
                self.VideoUseFrameResolution = self.__class__.VideoUseFrameResolution(service, rules, path + [("VideoUseFrameResolution", "")])
                super().__init__(service, rules, path)

            class AdvancedVideoQualityOptions(PyMenu):
                """
                Singleton AdvancedVideoQualityOptions.
                """
                def __init__(self, service, rules, path):
                    self.BitRateQuality = self.__class__.BitRateQuality(service, rules, path + [("BitRateQuality", "")])
                    self.Bitrate = self.__class__.Bitrate(service, rules, path + [("Bitrate", "")])
                    self.CompressionMethod = self.__class__.CompressionMethod(service, rules, path + [("CompressionMethod", "")])
                    self.EnableH264 = self.__class__.EnableH264(service, rules, path + [("EnableH264", "")])
                    super().__init__(service, rules, path)

                class BitRateQuality(PyTextual):
                    """
                    Parameter BitRateQuality of value type str.
                    """
                    pass

                class Bitrate(PyNumerical):
                    """
                    Parameter Bitrate of value type int.
                    """
                    pass

                class CompressionMethod(PyTextual):
                    """
                    Parameter CompressionMethod of value type str.
                    """
                    pass

                class EnableH264(PyParameter):
                    """
                    Parameter EnableH264 of value type bool.
                    """
                    pass

            class VideoFPS(PyNumerical):
                """
                Parameter VideoFPS of value type int.
                """
                pass

            class VideoFormat(PyTextual):
                """
                Parameter VideoFormat of value type str.
                """
                pass

            class VideoQuality(PyTextual):
                """
                Parameter VideoQuality of value type str.
                """
                pass

            class VideoResoutionX(PyNumerical):
                """
                Parameter VideoResoutionX of value type int.
                """
                pass

            class VideoResoutionY(PyNumerical):
                """
                Parameter VideoResoutionY of value type int.
                """
                pass

            class VideoScale(PyTextual):
                """
                Parameter VideoScale of value type str.
                """
                pass

            class VideoSmoothScaling(PyParameter):
                """
                Parameter VideoSmoothScaling of value type bool.
                """
                pass

            class VideoUseFrameResolution(PyParameter):
                """
                Parameter VideoUseFrameResolution of value type bool.
                """
                pass

        class GraphicsEffects(PyMenu):
            """
            Singleton GraphicsEffects.
            """
            def __init__(self, service, rules, path):
                self.AmbientOcclusionEnabled = self.__class__.AmbientOcclusionEnabled(service, rules, path + [("AmbientOcclusionEnabled", "")])
                self.AmbientOcclusionQuality = self.__class__.AmbientOcclusionQuality(service, rules, path + [("AmbientOcclusionQuality", "")])
                self.AmbientOcclusionStrength = self.__class__.AmbientOcclusionStrength(service, rules, path + [("AmbientOcclusionStrength", "")])
                self.AntiAliasing = self.__class__.AntiAliasing(service, rules, path + [("AntiAliasing", "")])
                self.BloomBlur = self.__class__.BloomBlur(service, rules, path + [("BloomBlur", "")])
                self.BloomEnabled = self.__class__.BloomEnabled(service, rules, path + [("BloomEnabled", "")])
                self.BloomStrength = self.__class__.BloomStrength(service, rules, path + [("BloomStrength", "")])
                self.GridColor = self.__class__.GridColor(service, rules, path + [("GridColor", "")])
                self.GridPlaneCount = self.__class__.GridPlaneCount(service, rules, path + [("GridPlaneCount", "")])
                self.GridPlaneEnabled = self.__class__.GridPlaneEnabled(service, rules, path + [("GridPlaneEnabled", "")])
                self.GridPlaneOffset = self.__class__.GridPlaneOffset(service, rules, path + [("GridPlaneOffset", "")])
                self.GridPlaneSizeFactor = self.__class__.GridPlaneSizeFactor(service, rules, path + [("GridPlaneSizeFactor", "")])
                self.PlaneDirection = self.__class__.PlaneDirection(service, rules, path + [("PlaneDirection", "")])
                self.ReflectionsEnabled = self.__class__.ReflectionsEnabled(service, rules, path + [("ReflectionsEnabled", "")])
                self.ShadowMapEnabled = self.__class__.ShadowMapEnabled(service, rules, path + [("ShadowMapEnabled", "")])
                self.ShowEdgeReflections = self.__class__.ShowEdgeReflections(service, rules, path + [("ShowEdgeReflections", "")])
                self.ShowMarkerReflections = self.__class__.ShowMarkerReflections(service, rules, path + [("ShowMarkerReflections", "")])
                self.SimpleShadowsEnabled = self.__class__.SimpleShadowsEnabled(service, rules, path + [("SimpleShadowsEnabled", "")])
                self.UpdateAfterMouseRelease = self.__class__.UpdateAfterMouseRelease(service, rules, path + [("UpdateAfterMouseRelease", "")])
                super().__init__(service, rules, path)

            class AmbientOcclusionEnabled(PyParameter):
                """
                Parameter AmbientOcclusionEnabled of value type bool.
                """
                pass

            class AmbientOcclusionQuality(PyTextual):
                """
                Parameter AmbientOcclusionQuality of value type str.
                """
                pass

            class AmbientOcclusionStrength(PyNumerical):
                """
                Parameter AmbientOcclusionStrength of value type int.
                """
                pass

            class AntiAliasing(PyParameter):
                """
                Parameter AntiAliasing of value type bool.
                """
                pass

            class BloomBlur(PyNumerical):
                """
                Parameter BloomBlur of value type int.
                """
                pass

            class BloomEnabled(PyParameter):
                """
                Parameter BloomEnabled of value type bool.
                """
                pass

            class BloomStrength(PyNumerical):
                """
                Parameter BloomStrength of value type int.
                """
                pass

            class GridColor(PyTextual):
                """
                Parameter GridColor of value type str.
                """
                pass

            class GridPlaneCount(PyNumerical):
                """
                Parameter GridPlaneCount of value type int.
                """
                pass

            class GridPlaneEnabled(PyParameter):
                """
                Parameter GridPlaneEnabled of value type bool.
                """
                pass

            class GridPlaneOffset(PyNumerical):
                """
                Parameter GridPlaneOffset of value type int.
                """
                pass

            class GridPlaneSizeFactor(PyNumerical):
                """
                Parameter GridPlaneSizeFactor of value type int.
                """
                pass

            class PlaneDirection(PyTextual):
                """
                Parameter PlaneDirection of value type str.
                """
                pass

            class ReflectionsEnabled(PyParameter):
                """
                Parameter ReflectionsEnabled of value type bool.
                """
                pass

            class ShadowMapEnabled(PyParameter):
                """
                Parameter ShadowMapEnabled of value type bool.
                """
                pass

            class ShowEdgeReflections(PyParameter):
                """
                Parameter ShowEdgeReflections of value type bool.
                """
                pass

            class ShowMarkerReflections(PyParameter):
                """
                Parameter ShowMarkerReflections of value type bool.
                """
                pass

            class SimpleShadowsEnabled(PyParameter):
                """
                Parameter SimpleShadowsEnabled of value type bool.
                """
                pass

            class UpdateAfterMouseRelease(PyParameter):
                """
                Parameter UpdateAfterMouseRelease of value type bool.
                """
                pass

        class HardcopySettings(PyMenu):
            """
            Singleton HardcopySettings.
            """
            def __init__(self, service, rules, path):
                self.ExportEdgesForAVZ = self.__class__.ExportEdgesForAVZ(service, rules, path + [("ExportEdgesForAVZ", "")])
                self.HardcopyDriver = self.__class__.HardcopyDriver(service, rules, path + [("HardcopyDriver", "")])
                self.HardcopyLineWidth = self.__class__.HardcopyLineWidth(service, rules, path + [("HardcopyLineWidth", "")])
                self.HardwareImageAccel = self.__class__.HardwareImageAccel(service, rules, path + [("HardwareImageAccel", "")])
                self.PostScriptPermissionOverride = self.__class__.PostScriptPermissionOverride(service, rules, path + [("PostScriptPermissionOverride", "")])
                self.RetainColormapPosForAVZ = self.__class__.RetainColormapPosForAVZ(service, rules, path + [("RetainColormapPosForAVZ", "")])
                self.SaveEmbeddedHardcopiesSeparately = self.__class__.SaveEmbeddedHardcopiesSeparately(service, rules, path + [("SaveEmbeddedHardcopiesSeparately", "")])
                self.SaveEmbeddedWindowsInHardcopy = self.__class__.SaveEmbeddedWindowsInHardcopy(service, rules, path + [("SaveEmbeddedWindowsInHardcopy", "")])
                self.TransparentEmbeddedWindows = self.__class__.TransparentEmbeddedWindows(service, rules, path + [("TransparentEmbeddedWindows", "")])
                super().__init__(service, rules, path)

            class ExportEdgesForAVZ(PyParameter):
                """
                Parameter ExportEdgesForAVZ of value type bool.
                """
                pass

            class HardcopyDriver(PyTextual):
                """
                Parameter HardcopyDriver of value type str.
                """
                pass

            class HardcopyLineWidth(PyNumerical):
                """
                Parameter HardcopyLineWidth of value type float.
                """
                pass

            class HardwareImageAccel(PyParameter):
                """
                Parameter HardwareImageAccel of value type bool.
                """
                pass

            class PostScriptPermissionOverride(PyParameter):
                """
                Parameter PostScriptPermissionOverride of value type bool.
                """
                pass

            class RetainColormapPosForAVZ(PyParameter):
                """
                Parameter RetainColormapPosForAVZ of value type bool.
                """
                pass

            class SaveEmbeddedHardcopiesSeparately(PyParameter):
                """
                Parameter SaveEmbeddedHardcopiesSeparately of value type bool.
                """
                pass

            class SaveEmbeddedWindowsInHardcopy(PyParameter):
                """
                Parameter SaveEmbeddedWindowsInHardcopy of value type bool.
                """
                pass

            class TransparentEmbeddedWindows(PyParameter):
                """
                Parameter TransparentEmbeddedWindows of value type bool.
                """
                pass

        class Lighting(PyMenu):
            """
            Singleton Lighting.
            """
            def __init__(self, service, rules, path):
                self.AmbientLightIntensity = self.__class__.AmbientLightIntensity(service, rules, path + [("AmbientLightIntensity", "")])
                self.Headlight = self.__class__.Headlight(service, rules, path + [("Headlight", "")])
                self.HeadlightIntensity = self.__class__.HeadlightIntensity(service, rules, path + [("HeadlightIntensity", "")])
                self.LightingMethod = self.__class__.LightingMethod(service, rules, path + [("LightingMethod", "")])
                super().__init__(service, rules, path)

            class AmbientLightIntensity(PyNumerical):
                """
                Parameter AmbientLightIntensity of value type float.
                """
                pass

            class Headlight(PyTextual):
                """
                Parameter Headlight of value type str.
                """
                pass

            class HeadlightIntensity(PyNumerical):
                """
                Parameter HeadlightIntensity of value type float.
                """
                pass

            class LightingMethod(PyTextual):
                """
                Parameter LightingMethod of value type str.
                """
                pass

        class ManageHoopsMemory(PyMenu):
            """
            Singleton ManageHoopsMemory.
            """
            def __init__(self, service, rules, path):
                self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                self.HSFImportLimit = self.__class__.HSFImportLimit(service, rules, path + [("HSFImportLimit", "")])
                super().__init__(service, rules, path)

            class Enabled(PyParameter):
                """
                Parameter Enabled of value type bool.
                """
                pass

            class HSFImportLimit(PyNumerical):
                """
                Parameter HSFImportLimit of value type int.
                """
                pass

        class MaterialEffects(PyMenu):
            """
            Singleton MaterialEffects.
            """
            def __init__(self, service, rules, path):
                self.DecimationFilter = self.__class__.DecimationFilter(service, rules, path + [("DecimationFilter", "")])
                self.ParameterizationSource = self.__class__.ParameterizationSource(service, rules, path + [("ParameterizationSource", "")])
                self.TilingStyle = self.__class__.TilingStyle(service, rules, path + [("TilingStyle", "")])
                super().__init__(service, rules, path)

            class DecimationFilter(PyTextual):
                """
                Parameter DecimationFilter of value type str.
                """
                pass

            class ParameterizationSource(PyTextual):
                """
                Parameter ParameterizationSource of value type str.
                """
                pass

            class TilingStyle(PyTextual):
                """
                Parameter TilingStyle of value type str.
                """
                pass

        class MeshingMode(PyMenu):
            """
            Singleton MeshingMode.
            """
            def __init__(self, service, rules, path):
                self.GraphicsWindowDisplayTimeout = self.__class__.GraphicsWindowDisplayTimeout(service, rules, path + [("GraphicsWindowDisplayTimeout", "")])
                self.GraphicsWindowDisplayTimeoutValue = self.__class__.GraphicsWindowDisplayTimeoutValue(service, rules, path + [("GraphicsWindowDisplayTimeoutValue", "")])
                super().__init__(service, rules, path)

            class GraphicsWindowDisplayTimeout(PyParameter):
                """
                Parameter GraphicsWindowDisplayTimeout of value type bool.
                """
                pass

            class GraphicsWindowDisplayTimeoutValue(PyNumerical):
                """
                Parameter GraphicsWindowDisplayTimeoutValue of value type float.
                """
                pass

        class Performance(PyMenu):
            """
            Singleton Performance.
            """
            def __init__(self, service, rules, path):
                self.FastDisplayMode = self.__class__.FastDisplayMode(service, rules, path + [("FastDisplayMode", "")])
                self.MinimumFrameRate = self.__class__.MinimumFrameRate(service, rules, path + [("MinimumFrameRate", "")])
                self.OptimizeInputData = self.__class__.OptimizeInputData(service, rules, path + [("OptimizeInputData", "")])
                self.OptimizeFor = self.__class__.OptimizeFor(service, rules, path + [("OptimizeFor", "")])
                self.RatioOfTargetFrameRateToClassifyHeavyGeometry = self.__class__.RatioOfTargetFrameRateToClassifyHeavyGeometry(service, rules, path + [("RatioOfTargetFrameRateToClassifyHeavyGeometry", "")])
                self.RatioOfTargetFrameRateToDeclassifyHeavyGeometry = self.__class__.RatioOfTargetFrameRateToDeclassifyHeavyGeometry(service, rules, path + [("RatioOfTargetFrameRateToDeclassifyHeavyGeometry", "")])
                self.SurfaceCaching = self.__class__.SurfaceCaching(service, rules, path + [("SurfaceCaching", "")])
                super().__init__(service, rules, path)

            class FastDisplayMode(PyMenu):
                """
                Singleton FastDisplayMode.
                """
                def __init__(self, service, rules, path):
                    self.Culling = self.__class__.Culling(service, rules, path + [("Culling", "")])
                    self.FacesShown = self.__class__.FacesShown(service, rules, path + [("FacesShown", "")])
                    self.MarkersDecimation = self.__class__.MarkersDecimation(service, rules, path + [("MarkersDecimation", "")])
                    self.NodesShown = self.__class__.NodesShown(service, rules, path + [("NodesShown", "")])
                    self.PerimeterEdgesShown = self.__class__.PerimeterEdgesShown(service, rules, path + [("PerimeterEdgesShown", "")])
                    self.SilhouetteShown = self.__class__.SilhouetteShown(service, rules, path + [("SilhouetteShown", "")])
                    self.Status = self.__class__.Status(service, rules, path + [("Status", "")])
                    self.Transparency = self.__class__.Transparency(service, rules, path + [("Transparency", "")])
                    super().__init__(service, rules, path)

                class Culling(PyNumerical):
                    """
                    Parameter Culling of value type int.
                    """
                    pass

                class FacesShown(PyParameter):
                    """
                    Parameter FacesShown of value type bool.
                    """
                    pass

                class MarkersDecimation(PyNumerical):
                    """
                    Parameter MarkersDecimation of value type float.
                    """
                    pass

                class NodesShown(PyParameter):
                    """
                    Parameter NodesShown of value type bool.
                    """
                    pass

                class PerimeterEdgesShown(PyParameter):
                    """
                    Parameter PerimeterEdgesShown of value type bool.
                    """
                    pass

                class SilhouetteShown(PyParameter):
                    """
                    Parameter SilhouetteShown of value type bool.
                    """
                    pass

                class Status(PyTextual):
                    """
                    Parameter Status of value type str.
                    """
                    pass

                class Transparency(PyParameter):
                    """
                    Parameter Transparency of value type bool.
                    """
                    pass

            class MinimumFrameRate(PyMenu):
                """
                Singleton MinimumFrameRate.
                """
                def __init__(self, service, rules, path):
                    self.DynamicAdjustment = self.__class__.DynamicAdjustment(service, rules, path + [("DynamicAdjustment", "")])
                    self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                    self.FixedCullingValue = self.__class__.FixedCullingValue(service, rules, path + [("FixedCullingValue", "")])
                    self.MaximumCullingThreshold = self.__class__.MaximumCullingThreshold(service, rules, path + [("MaximumCullingThreshold", "")])
                    self.MinimumCullingThreshold = self.__class__.MinimumCullingThreshold(service, rules, path + [("MinimumCullingThreshold", "")])
                    self.TargetFPS = self.__class__.TargetFPS(service, rules, path + [("TargetFPS", "")])
                    super().__init__(service, rules, path)

                class DynamicAdjustment(PyParameter):
                    """
                    Parameter DynamicAdjustment of value type bool.
                    """
                    pass

                class Enabled(PyParameter):
                    """
                    Parameter Enabled of value type bool.
                    """
                    pass

                class FixedCullingValue(PyNumerical):
                    """
                    Parameter FixedCullingValue of value type int.
                    """
                    pass

                class MaximumCullingThreshold(PyNumerical):
                    """
                    Parameter MaximumCullingThreshold of value type int.
                    """
                    pass

                class MinimumCullingThreshold(PyNumerical):
                    """
                    Parameter MinimumCullingThreshold of value type int.
                    """
                    pass

                class TargetFPS(PyNumerical):
                    """
                    Parameter TargetFPS of value type int.
                    """
                    pass

            class OptimizeInputData(PyMenu):
                """
                Singleton OptimizeInputData.
                """
                def __init__(self, service, rules, path):
                    self.Enabled = self.__class__.Enabled(service, rules, path + [("Enabled", "")])
                    self.MaximumFacetsPerShell = self.__class__.MaximumFacetsPerShell(service, rules, path + [("MaximumFacetsPerShell", "")])
                    super().__init__(service, rules, path)

                class Enabled(PyParameter):
                    """
                    Parameter Enabled of value type bool.
                    """
                    pass

                class MaximumFacetsPerShell(PyNumerical):
                    """
                    Parameter MaximumFacetsPerShell of value type int.
                    """
                    pass

            class OptimizeFor(PyTextual):
                """
                Parameter OptimizeFor of value type str.
                """
                pass

            class RatioOfTargetFrameRateToClassifyHeavyGeometry(PyNumerical):
                """
                Parameter RatioOfTargetFrameRateToClassifyHeavyGeometry of value type float.
                """
                pass

            class RatioOfTargetFrameRateToDeclassifyHeavyGeometry(PyNumerical):
                """
                Parameter RatioOfTargetFrameRateToDeclassifyHeavyGeometry of value type float.
                """
                pass

            class SurfaceCaching(PyParameter):
                """
                Parameter SurfaceCaching of value type bool.
                """
                pass

        class RayTracingOptions(PyMenu):
            """
            Singleton RayTracingOptions.
            """
            def __init__(self, service, rules, path):
                self.VolumeRenderingMethod = self.__class__.VolumeRenderingMethod(service, rules, path + [("VolumeRenderingMethod", "")])
                super().__init__(service, rules, path)

            class VolumeRenderingMethod(PyTextual):
                """
                Parameter VolumeRenderingMethod of value type str.
                """
                pass

        class Transparency(PyMenu):
            """
            Singleton Transparency.
            """
            def __init__(self, service, rules, path):
                self.AlgorithmForModernDrivers = self.__class__.AlgorithmForModernDrivers(service, rules, path + [("AlgorithmForModernDrivers", "")])
                self.DepthPeelingLayers = self.__class__.DepthPeelingLayers(service, rules, path + [("DepthPeelingLayers", "")])
                self.DepthPeelingPreference = self.__class__.DepthPeelingPreference(service, rules, path + [("DepthPeelingPreference", "")])
                self.QuickMoves = self.__class__.QuickMoves(service, rules, path + [("QuickMoves", "")])
                self.ZSortOptions = self.__class__.ZSortOptions(service, rules, path + [("ZSortOptions", "")])
                super().__init__(service, rules, path)

            class AlgorithmForModernDrivers(PyTextual):
                """
                Parameter AlgorithmForModernDrivers of value type str.
                """
                pass

            class DepthPeelingLayers(PyNumerical):
                """
                Parameter DepthPeelingLayers of value type int.
                """
                pass

            class DepthPeelingPreference(PyTextual):
                """
                Parameter DepthPeelingPreference of value type str.
                """
                pass

            class QuickMoves(PyTextual):
                """
                Parameter QuickMoves of value type str.
                """
                pass

            class ZSortOptions(PyTextual):
                """
                Parameter ZSortOptions of value type str.
                """
                pass

        class VectorSettings(PyMenu):
            """
            Singleton VectorSettings.
            """
            def __init__(self, service, rules, path):
                self.Arrow3DRadius1Factor = self.__class__.Arrow3DRadius1Factor(service, rules, path + [("Arrow3DRadius1Factor", "")])
                self.Arrow3DRadius2Factor = self.__class__.Arrow3DRadius2Factor(service, rules, path + [("Arrow3DRadius2Factor", "")])
                self.Arrowhead3DRadius1Factor = self.__class__.Arrowhead3DRadius1Factor(service, rules, path + [("Arrowhead3DRadius1Factor", "")])
                self.LineArrow3DPerpendicularRadius = self.__class__.LineArrow3DPerpendicularRadius(service, rules, path + [("LineArrow3DPerpendicularRadius", "")])
                super().__init__(service, rules, path)

            class Arrow3DRadius1Factor(PyNumerical):
                """
                Parameter Arrow3DRadius1Factor of value type float.
                """
                pass

            class Arrow3DRadius2Factor(PyNumerical):
                """
                Parameter Arrow3DRadius2Factor of value type float.
                """
                pass

            class Arrowhead3DRadius1Factor(PyNumerical):
                """
                Parameter Arrowhead3DRadius1Factor of value type float.
                """
                pass

            class LineArrow3DPerpendicularRadius(PyNumerical):
                """
                Parameter LineArrow3DPerpendicularRadius of value type float.
                """
                pass

        class AnimationOption(PyTextual):
            """
            Parameter AnimationOption of value type str.
            """
            pass

        class BackfaceCull(PyParameter):
            """
            Parameter BackfaceCull of value type bool.
            """
            pass

        class CameraNearLimit(PyNumerical):
            """
            Parameter CameraNearLimit of value type float.
            """
            pass

        class DoubleBuffering(PyParameter):
            """
            Parameter DoubleBuffering of value type bool.
            """
            pass

        class EnableCameraNearLimitToAvoidZFighting(PyParameter):
            """
            Parameter EnableCameraNearLimitToAvoidZFighting of value type bool.
            """
            pass

        class EnableNonObjectBasedWorkflow(PyParameter):
            """
            Parameter EnableNonObjectBasedWorkflow of value type bool.
            """
            pass

        class EventPollInterval(PyNumerical):
            """
            Parameter EventPollInterval of value type int.
            """
            pass

        class EventPollTimeout(PyNumerical):
            """
            Parameter EventPollTimeout of value type int.
            """
            pass

        class ForceKeyFrameAnimationMarkersToOff(PyParameter):
            """
            Parameter ForceKeyFrameAnimationMarkersToOff of value type bool.
            """
            pass

        class GraphicsWindowLineWidth(PyTextual):
            """
            Parameter GraphicsWindowLineWidth of value type str.
            """
            pass

        class GraphicsWindowPointSymbol(PyTextual):
            """
            Parameter GraphicsWindowPointSymbol of value type str.
            """
            pass

        class HiddenSurfaceRemovalMethod(PyTextual):
            """
            Parameter HiddenSurfaceRemovalMethod of value type str.
            """
            pass

        class HigherResolutionGraphicsWindowLineWidth(PyNumerical):
            """
            Parameter HigherResolutionGraphicsWindowLineWidth of value type float.
            """
            pass

        class LowerResolutionGraphicsWindowLineWidth(PyNumerical):
            """
            Parameter LowerResolutionGraphicsWindowLineWidth of value type float.
            """
            pass

        class MarkerDrawingMode(PyTextual):
            """
            Parameter MarkerDrawingMode of value type str.
            """
            pass

        class MaxGraphicsTextSize(PyNumerical):
            """
            Parameter MaxGraphicsTextSize of value type int.
            """
            pass

        class MinGraphicsTextSize(PyNumerical):
            """
            Parameter MinGraphicsTextSize of value type int.
            """
            pass

        class PlotLegendMargin(PyNumerical):
            """
            Parameter PlotLegendMargin of value type float.
            """
            pass

        class PointToolSize(PyNumerical):
            """
            Parameter PointToolSize of value type float.
            """
            pass

        class RemovePartitionLines(PyParameter):
            """
            Parameter RemovePartitionLines of value type bool.
            """
            pass

        class RemovePartitionLinesTolerance(PyNumerical):
            """
            Parameter RemovePartitionLinesTolerance of value type float.
            """
            pass

        class RotationCenterpointVisible(PyParameter):
            """
            Parameter RotationCenterpointVisible of value type bool.
            """
            pass

        class ScrollWheelEventEndTimer(PyNumerical):
            """
            Parameter ScrollWheelEventEndTimer of value type int.
            """
            pass

        class SelectionHighlightWindow(PyParameter):
            """
            Parameter SelectionHighlightWindow of value type bool.
            """
            pass

        class SetCameraNormalToSurfaceIncrements(PyNumerical):
            """
            Parameter SetCameraNormalToSurfaceIncrements of value type int.
            """
            pass

        class ShowHiddenLines(PyParameter):
            """
            Parameter ShowHiddenLines of value type bool.
            """
            pass

        class ShowHiddenSurfaces(PyParameter):
            """
            Parameter ShowHiddenSurfaces of value type bool.
            """
            pass

        class SurfaceGeneralDisplacement(PyNumerical):
            """
            Parameter SurfaceGeneralDisplacement of value type int.
            """
            pass

        class SwitchToOpenGLForRemoteVisualization(PyParameter):
            """
            Parameter SwitchToOpenGLForRemoteVisualization of value type bool.
            """
            pass

        class TestUseExternalFunction(PyTextual):
            """
            Parameter TestUseExternalFunction of value type str.
            """
            pass

        class TextWindowLineWidth(PyTextual):
            """
            Parameter TextWindowLineWidth of value type str.
            """
            pass

    class MatProApp(PyMenu):
        """
        Singleton MatProApp.
        """
        def __init__(self, service, rules, path):
            self.CheckExpression = self.__class__.CheckExpression(service, rules, path + [("CheckExpression", "")])
            self.Statistics = self.__class__.Statistics(service, rules, path + [("Statistics", "")])
            self.BetaFeatures = self.__class__.BetaFeatures(service, rules, path + [("BetaFeatures", "")])
            self.CheckCrash = self.__class__.CheckCrash(service, rules, path + [("CheckCrash", "")])
            self.Debug = self.__class__.Debug(service, rules, path + [("Debug", "")])
            self.Focus = self.__class__.Focus(service, rules, path + [("Focus", "")])
            self.MeshNaming = self.__class__.MeshNaming(service, rules, path + [("MeshNaming", "")])
            self.Tracking = self.__class__.Tracking(service, rules, path + [("Tracking", "")])
            self.Warning = self.__class__.Warning(service, rules, path + [("Warning", "")])
            super().__init__(service, rules, path)

        class CheckExpression(PyMenu):
            """
            Singleton CheckExpression.
            """
            def __init__(self, service, rules, path):
                self.Cdot = self.__class__.Cdot(service, rules, path + [("Cdot", "")])
                self.Coordinates = self.__class__.Coordinates(service, rules, path + [("Coordinates", "")])
                self.Dvv = self.__class__.Dvv(service, rules, path + [("Dvv", "")])
                self.Edot = self.__class__.Edot(service, rules, path + [("Edot", "")])
                self.Gdot = self.__class__.Gdot(service, rules, path + [("Gdot", "")])
                self.Giesekus = self.__class__.Giesekus(service, rules, path + [("Giesekus", "")])
                self.Pressure = self.__class__.Pressure(service, rules, path + [("Pressure", "")])
                self.Species = self.__class__.Species(service, rules, path + [("Species", "")])
                self.Temperature = self.__class__.Temperature(service, rules, path + [("Temperature", "")])
                self.Time = self.__class__.Time(service, rules, path + [("Time", "")])
                self.Velocities = self.__class__.Velocities(service, rules, path + [("Velocities", "")])
                self.Vorticity = self.__class__.Vorticity(service, rules, path + [("Vorticity", "")])
                super().__init__(service, rules, path)

            class Cdot(PyNumerical):
                """
                Parameter Cdot of value type float.
                """
                pass

            class Coordinates(PyNumerical):
                """
                Parameter Coordinates of value type float.
                """
                pass

            class Dvv(PyNumerical):
                """
                Parameter Dvv of value type float.
                """
                pass

            class Edot(PyNumerical):
                """
                Parameter Edot of value type float.
                """
                pass

            class Gdot(PyNumerical):
                """
                Parameter Gdot of value type float.
                """
                pass

            class Giesekus(PyNumerical):
                """
                Parameter Giesekus of value type float.
                """
                pass

            class Pressure(PyNumerical):
                """
                Parameter Pressure of value type float.
                """
                pass

            class Species(PyNumerical):
                """
                Parameter Species of value type float.
                """
                pass

            class Temperature(PyNumerical):
                """
                Parameter Temperature of value type float.
                """
                pass

            class Time(PyNumerical):
                """
                Parameter Time of value type float.
                """
                pass

            class Velocities(PyNumerical):
                """
                Parameter Velocities of value type float.
                """
                pass

            class Vorticity(PyNumerical):
                """
                Parameter Vorticity of value type float.
                """
                pass

        class Statistics(PyMenu):
            """
            Singleton Statistics.
            """
            def __init__(self, service, rules, path):
                self.MaxPositions = self.__class__.MaxPositions(service, rules, path + [("MaxPositions", "")])
                self.PointSize = self.__class__.PointSize(service, rules, path + [("PointSize", "")])
                self.PointSymbol = self.__class__.PointSymbol(service, rules, path + [("PointSymbol", "")])
                self.QuickSlicing = self.__class__.QuickSlicing(service, rules, path + [("QuickSlicing", "")])
                self.VectorSize = self.__class__.VectorSize(service, rules, path + [("VectorSize", "")])
                self.VectorSymbol = self.__class__.VectorSymbol(service, rules, path + [("VectorSymbol", "")])
                super().__init__(service, rules, path)

            class MaxPositions(PyNumerical):
                """
                Parameter MaxPositions of value type int.
                """
                pass

            class PointSize(PyNumerical):
                """
                Parameter PointSize of value type float.
                """
                pass

            class PointSymbol(PyTextual):
                """
                Parameter PointSymbol of value type str.
                """
                pass

            class QuickSlicing(PyParameter):
                """
                Parameter QuickSlicing of value type bool.
                """
                pass

            class VectorSize(PyNumerical):
                """
                Parameter VectorSize of value type float.
                """
                pass

            class VectorSymbol(PyTextual):
                """
                Parameter VectorSymbol of value type str.
                """
                pass

        class BetaFeatures(PyParameter):
            """
            Parameter BetaFeatures of value type bool.
            """
            pass

        class CheckCrash(PyParameter):
            """
            Parameter CheckCrash of value type bool.
            """
            pass

        class Debug(PyParameter):
            """
            Parameter Debug of value type bool.
            """
            pass

        class Focus(PyParameter):
            """
            Parameter Focus of value type bool.
            """
            pass

        class MeshNaming(PyTextual):
            """
            Parameter MeshNaming of value type str.
            """
            pass

        class Tracking(PyParameter):
            """
            Parameter Tracking of value type bool.
            """
            pass

        class Warning(PyParameter):
            """
            Parameter Warning of value type bool.
            """
            pass

    class MeshingWorkflow(PyMenu):
        """
        Singleton MeshingWorkflow.
        """
        def __init__(self, service, rules, path):
            self.CadLogOption = self.__class__.CadLogOption(service, rules, path + [("CadLogOption", "")])
            self.DrawSettings = self.__class__.DrawSettings(service, rules, path + [("DrawSettings", "")])
            self.CheckpointingOption = self.__class__.CheckpointingOption(service, rules, path + [("CheckpointingOption", "")])
            self.SaveCheckpointFiles = self.__class__.SaveCheckpointFiles(service, rules, path + [("SaveCheckpointFiles", "")])
            self.SaveWftFileWithMesh = self.__class__.SaveWftFileWithMesh(service, rules, path + [("SaveWftFileWithMesh", "")])
            self.TempFolder = self.__class__.TempFolder(service, rules, path + [("TempFolder", "")])
            self.TemplatesFolder = self.__class__.TemplatesFolder(service, rules, path + [("TemplatesFolder", "")])
            self.Verbosity = self.__class__.Verbosity(service, rules, path + [("Verbosity", "")])
            super().__init__(service, rules, path)

        class CadLogOption(PyMenu):
            """
            Singleton CadLogOption.
            """
            def __init__(self, service, rules, path):
                self.Location = self.__class__.Location(service, rules, path + [("Location", "")])
                self.Prefix = self.__class__.Prefix(service, rules, path + [("Prefix", "")])
                self.Write = self.__class__.Write(service, rules, path + [("Write", "")])
                super().__init__(service, rules, path)

            class Location(PyTextual):
                """
                Parameter Location of value type str.
                """
                pass

            class Prefix(PyTextual):
                """
                Parameter Prefix of value type str.
                """
                pass

            class Write(PyTextual):
                """
                Parameter Write of value type str.
                """
                pass

        class DrawSettings(PyMenu):
            """
            Singleton DrawSettings.
            """
            def __init__(self, service, rules, path):
                self.AutoDraw = self.__class__.AutoDraw(service, rules, path + [("AutoDraw", "")])
                self.FaceZoneLimit = self.__class__.FaceZoneLimit(service, rules, path + [("FaceZoneLimit", "")])
                self.FacetLimit = self.__class__.FacetLimit(service, rules, path + [("FacetLimit", "")])
                super().__init__(service, rules, path)

            class AutoDraw(PyTextual):
                """
                Parameter AutoDraw of value type str.
                """
                pass

            class FaceZoneLimit(PyNumerical):
                """
                Parameter FaceZoneLimit of value type int.
                """
                pass

            class FacetLimit(PyNumerical):
                """
                Parameter FacetLimit of value type int.
                """
                pass

        class CheckpointingOption(PyTextual):
            """
            Parameter CheckpointingOption of value type str.
            """
            pass

        class SaveCheckpointFiles(PyParameter):
            """
            Parameter SaveCheckpointFiles of value type bool.
            """
            pass

        class SaveWftFileWithMesh(PyParameter):
            """
            Parameter SaveWftFileWithMesh of value type bool.
            """
            pass

        class TempFolder(PyTextual):
            """
            Parameter TempFolder of value type str.
            """
            pass

        class TemplatesFolder(PyTextual):
            """
            Parameter TemplatesFolder of value type str.
            """
            pass

        class Verbosity(PyTextual):
            """
            Parameter Verbosity of value type str.
            """
            pass

    class Navigation(PyMenu):
        """
        Singleton Navigation.
        """
        def __init__(self, service, rules, path):
            self.MouseMapping = self.__class__.MouseMapping(service, rules, path + [("MouseMapping", "")])
            super().__init__(service, rules, path)

        class MouseMapping(PyMenu):
            """
            Singleton MouseMapping.
            """
            def __init__(self, service, rules, path):
                self.Additional = self.__class__.Additional(service, rules, path + [("Additional", "")])
                self.Basic = self.__class__.Basic(service, rules, path + [("Basic", "")])
                self.MOUSEMAPTHEME = self.__class__.MOUSEMAPTHEME(service, rules, path + [("MOUSEMAPTHEME", "")])
                super().__init__(service, rules, path)

            class Additional(PyMenu):
                """
                Singleton Additional.
                """
                def __init__(self, service, rules, path):
                    self.CTRLLMBCLICK = self.__class__.CTRLLMBCLICK(service, rules, path + [("CTRLLMBCLICK", "")])
                    self.CTRLLMBDRAG = self.__class__.CTRLLMBDRAG(service, rules, path + [("CTRLLMBDRAG", "")])
                    self.CTRLMMBCLICK = self.__class__.CTRLMMBCLICK(service, rules, path + [("CTRLMMBCLICK", "")])
                    self.CTRLMMBDRAG = self.__class__.CTRLMMBDRAG(service, rules, path + [("CTRLMMBDRAG", "")])
                    self.CTRLRMBCLICK = self.__class__.CTRLRMBCLICK(service, rules, path + [("CTRLRMBCLICK", "")])
                    self.CTRLRMBDRAG = self.__class__.CTRLRMBDRAG(service, rules, path + [("CTRLRMBDRAG", "")])
                    self.MOUSEPROBE = self.__class__.MOUSEPROBE(service, rules, path + [("MOUSEPROBE", "")])
                    self.MOUSEWHEEL = self.__class__.MOUSEWHEEL(service, rules, path + [("MOUSEWHEEL", "")])
                    self.MOUSEWHEELSENSITIVITY = self.__class__.MOUSEWHEELSENSITIVITY(service, rules, path + [("MOUSEWHEELSENSITIVITY", "")])
                    self.REVERSEWHEELDIRECTION = self.__class__.REVERSEWHEELDIRECTION(service, rules, path + [("REVERSEWHEELDIRECTION", "")])
                    self.SHIFTLMBCLICK = self.__class__.SHIFTLMBCLICK(service, rules, path + [("SHIFTLMBCLICK", "")])
                    self.SHIFTLMBDRAG = self.__class__.SHIFTLMBDRAG(service, rules, path + [("SHIFTLMBDRAG", "")])
                    self.SHIFTMMBCLICK = self.__class__.SHIFTMMBCLICK(service, rules, path + [("SHIFTMMBCLICK", "")])
                    self.SHIFTMMBDRAG = self.__class__.SHIFTMMBDRAG(service, rules, path + [("SHIFTMMBDRAG", "")])
                    self.SHIFTRMBCLICK = self.__class__.SHIFTRMBCLICK(service, rules, path + [("SHIFTRMBCLICK", "")])
                    self.SHIFTRMBDRAG = self.__class__.SHIFTRMBDRAG(service, rules, path + [("SHIFTRMBDRAG", "")])
                    super().__init__(service, rules, path)

                class CTRLLMBCLICK(PyTextual):
                    """
                    Parameter CTRLLMBCLICK of value type str.
                    """
                    pass

                class CTRLLMBDRAG(PyTextual):
                    """
                    Parameter CTRLLMBDRAG of value type str.
                    """
                    pass

                class CTRLMMBCLICK(PyTextual):
                    """
                    Parameter CTRLMMBCLICK of value type str.
                    """
                    pass

                class CTRLMMBDRAG(PyTextual):
                    """
                    Parameter CTRLMMBDRAG of value type str.
                    """
                    pass

                class CTRLRMBCLICK(PyTextual):
                    """
                    Parameter CTRLRMBCLICK of value type str.
                    """
                    pass

                class CTRLRMBDRAG(PyTextual):
                    """
                    Parameter CTRLRMBDRAG of value type str.
                    """
                    pass

                class MOUSEPROBE(PyTextual):
                    """
                    Parameter MOUSEPROBE of value type str.
                    """
                    pass

                class MOUSEWHEEL(PyTextual):
                    """
                    Parameter MOUSEWHEEL of value type str.
                    """
                    pass

                class MOUSEWHEELSENSITIVITY(PyNumerical):
                    """
                    Parameter MOUSEWHEELSENSITIVITY of value type float.
                    """
                    pass

                class REVERSEWHEELDIRECTION(PyParameter):
                    """
                    Parameter REVERSEWHEELDIRECTION of value type bool.
                    """
                    pass

                class SHIFTLMBCLICK(PyTextual):
                    """
                    Parameter SHIFTLMBCLICK of value type str.
                    """
                    pass

                class SHIFTLMBDRAG(PyTextual):
                    """
                    Parameter SHIFTLMBDRAG of value type str.
                    """
                    pass

                class SHIFTMMBCLICK(PyTextual):
                    """
                    Parameter SHIFTMMBCLICK of value type str.
                    """
                    pass

                class SHIFTMMBDRAG(PyTextual):
                    """
                    Parameter SHIFTMMBDRAG of value type str.
                    """
                    pass

                class SHIFTRMBCLICK(PyTextual):
                    """
                    Parameter SHIFTRMBCLICK of value type str.
                    """
                    pass

                class SHIFTRMBDRAG(PyTextual):
                    """
                    Parameter SHIFTRMBDRAG of value type str.
                    """
                    pass

            class Basic(PyMenu):
                """
                Singleton Basic.
                """
                def __init__(self, service, rules, path):
                    self.LMB = self.__class__.LMB(service, rules, path + [("LMB", "")])
                    self.LMBCLICK = self.__class__.LMBCLICK(service, rules, path + [("LMBCLICK", "")])
                    self.MMB = self.__class__.MMB(service, rules, path + [("MMB", "")])
                    self.MMBCLICK = self.__class__.MMBCLICK(service, rules, path + [("MMBCLICK", "")])
                    self.RMB = self.__class__.RMB(service, rules, path + [("RMB", "")])
                    self.RMBCLICK = self.__class__.RMBCLICK(service, rules, path + [("RMBCLICK", "")])
                    super().__init__(service, rules, path)

                class LMB(PyTextual):
                    """
                    Parameter LMB of value type str.
                    """
                    pass

                class LMBCLICK(PyTextual):
                    """
                    Parameter LMBCLICK of value type str.
                    """
                    pass

                class MMB(PyTextual):
                    """
                    Parameter MMB of value type str.
                    """
                    pass

                class MMBCLICK(PyTextual):
                    """
                    Parameter MMBCLICK of value type str.
                    """
                    pass

                class RMB(PyTextual):
                    """
                    Parameter RMB of value type str.
                    """
                    pass

                class RMBCLICK(PyTextual):
                    """
                    Parameter RMBCLICK of value type str.
                    """
                    pass

            class MOUSEMAPTHEME(PyTextual):
                """
                Parameter MOUSEMAPTHEME of value type str.
                """
                pass

    class ParametricStudy(PyMenu):
        """
        Singleton ParametricStudy.
        """
        def __init__(self, service, rules, path):
            self.LayoutOptions = self.__class__.LayoutOptions(service, rules, path + [("LayoutOptions", "")])
            self.UpdateOptions = self.__class__.UpdateOptions(service, rules, path + [("UpdateOptions", "")])
            super().__init__(service, rules, path)

        class LayoutOptions(PyMenu):
            """
            Singleton LayoutOptions.
            """
            def __init__(self, service, rules, path):
                self.CurrentCaseParameters = self.__class__.CurrentCaseParameters(service, rules, path + [("CurrentCaseParameters", "")])
                self.ParametricStudyTree = self.__class__.ParametricStudyTree(service, rules, path + [("ParametricStudyTree", "")])
                super().__init__(service, rules, path)

            class CurrentCaseParameters(PyParameter):
                """
                Parameter CurrentCaseParameters of value type bool.
                """
                pass

            class ParametricStudyTree(PyParameter):
                """
                Parameter ParametricStudyTree of value type bool.
                """
                pass

        class UpdateOptions(PyMenu):
            """
            Singleton UpdateOptions.
            """
            def __init__(self, service, rules, path):
                self.AutoRefreshTime = self.__class__.AutoRefreshTime(service, rules, path + [("AutoRefreshTime", "")])
                self.CaptureSimReportData = self.__class__.CaptureSimReportData(service, rules, path + [("CaptureSimReportData", "")])
                self.EnableAutoRefresh = self.__class__.EnableAutoRefresh(service, rules, path + [("EnableAutoRefresh", "")])
                self.ParameterValuePrecision = self.__class__.ParameterValuePrecision(service, rules, path + [("ParameterValuePrecision", "")])
                self.SaveProjectAfterDPUpdate = self.__class__.SaveProjectAfterDPUpdate(service, rules, path + [("SaveProjectAfterDPUpdate", "")])
                self.WriteData = self.__class__.WriteData(service, rules, path + [("WriteData", "")])
                super().__init__(service, rules, path)

            class AutoRefreshTime(PyNumerical):
                """
                Parameter AutoRefreshTime of value type int.
                """
                pass

            class CaptureSimReportData(PyParameter):
                """
                Parameter CaptureSimReportData of value type bool.
                """
                pass

            class EnableAutoRefresh(PyParameter):
                """
                Parameter EnableAutoRefresh of value type bool.
                """
                pass

            class ParameterValuePrecision(PyNumerical):
                """
                Parameter ParameterValuePrecision of value type int.
                """
                pass

            class SaveProjectAfterDPUpdate(PyParameter):
                """
                Parameter SaveProjectAfterDPUpdate of value type bool.
                """
                pass

            class WriteData(PyParameter):
                """
                Parameter WriteData of value type bool.
                """
                pass

    class PrjApp(PyMenu):
        """
        Singleton PrjApp.
        """
        def __init__(self, service, rules, path):
            self.AdvancedFlag = self.__class__.AdvancedFlag(service, rules, path + [("AdvancedFlag", "")])
            self.BetaFlag = self.__class__.BetaFlag(service, rules, path + [("BetaFlag", "")])
            self.UnitSystem = self.__class__.UnitSystem(service, rules, path + [("UnitSystem", "")])
            super().__init__(service, rules, path)

        class AdvancedFlag(PyParameter):
            """
            Parameter AdvancedFlag of value type bool.
            """
            pass

        class BetaFlag(PyParameter):
            """
            Parameter BetaFlag of value type bool.
            """
            pass

        class UnitSystem(PyTextual):
            """
            Parameter UnitSystem of value type str.
            """
            pass

    class PythonConsole(PyMenu):
        """
        Singleton PythonConsole.
        """
        def __init__(self, service, rules, path):
            self.ConsoleSuggestion = self.__class__.ConsoleSuggestion(service, rules, path + [("ConsoleSuggestion", "")])
            self.ConsoleSuggestionActiveOnly = self.__class__.ConsoleSuggestionActiveOnly(service, rules, path + [("ConsoleSuggestionActiveOnly", "")])
            self.PrettyPrintDict = self.__class__.PrettyPrintDict(service, rules, path + [("PrettyPrintDict", "")])
            self.QuickSearchResultsActiveOnly = self.__class__.QuickSearchResultsActiveOnly(service, rules, path + [("QuickSearchResultsActiveOnly", "")])
            super().__init__(service, rules, path)

        class ConsoleSuggestion(PyParameter):
            """
            Parameter ConsoleSuggestion of value type bool.
            """
            pass

        class ConsoleSuggestionActiveOnly(PyParameter):
            """
            Parameter ConsoleSuggestionActiveOnly of value type bool.
            """
            pass

        class PrettyPrintDict(PyParameter):
            """
            Parameter PrettyPrintDict of value type bool.
            """
            pass

        class QuickSearchResultsActiveOnly(PyParameter):
            """
            Parameter QuickSearchResultsActiveOnly of value type bool.
            """
            pass

    class Simulation(PyMenu):
        """
        Singleton Simulation.
        """
        def __init__(self, service, rules, path):
            self.ReportDefinitions = self.__class__.ReportDefinitions(service, rules, path + [("ReportDefinitions", "")])
            self.FlowModel = self.__class__.FlowModel(service, rules, path + [("FlowModel", "")])
            self.LocalResidualScaling = self.__class__.LocalResidualScaling(service, rules, path + [("LocalResidualScaling", "")])
            self.PdfCombustionRobustNumerics = self.__class__.PdfCombustionRobustNumerics(service, rules, path + [("PdfCombustionRobustNumerics", "")])
            super().__init__(service, rules, path)

        class ReportDefinitions(PyMenu):
            """
            Singleton ReportDefinitions.
            """
            def __init__(self, service, rules, path):
                self.AutomaticPlotFile = self.__class__.AutomaticPlotFile(service, rules, path + [("AutomaticPlotFile", "")])
                self.ReportPlotHistoryDataSize = self.__class__.ReportPlotHistoryDataSize(service, rules, path + [("ReportPlotHistoryDataSize", "")])
                super().__init__(service, rules, path)

            class AutomaticPlotFile(PyParameter):
                """
                Parameter AutomaticPlotFile of value type bool.
                """
                pass

            class ReportPlotHistoryDataSize(PyNumerical):
                """
                Parameter ReportPlotHistoryDataSize of value type int.
                """
                pass

        class FlowModel(PyTextual):
            """
            Parameter FlowModel of value type str.
            """
            pass

        class LocalResidualScaling(PyParameter):
            """
            Parameter LocalResidualScaling of value type bool.
            """
            pass

        class PdfCombustionRobustNumerics(PyParameter):
            """
            Parameter PdfCombustionRobustNumerics of value type bool.
            """
            pass

    class TurboSetup(PyMenu):
        """
        Singleton TurboSetup.
        """
        def __init__(self, service, rules, path):
            self.FaceZoneSettings = self.__class__.FaceZoneSettings(service, rules, path + [("FaceZoneSettings", "")])
            self.GraphicsSettings = self.__class__.GraphicsSettings(service, rules, path + [("GraphicsSettings", "")])
            self.CheckpointingOption = self.__class__.CheckpointingOption(service, rules, path + [("CheckpointingOption", "")])
            self.SaveCheckpointFiles = self.__class__.SaveCheckpointFiles(service, rules, path + [("SaveCheckpointFiles", "")])
            super().__init__(service, rules, path)

        class FaceZoneSettings(PyMenu):
            """
            Singleton FaceZoneSettings.
            """
            def __init__(self, service, rules, path):
                self.BladeRegion = self.__class__.BladeRegion(service, rules, path + [("BladeRegion", "")])
                self.FZSearchOrder = self.__class__.FZSearchOrder(service, rules, path + [("FZSearchOrder", "")])
                self.HubRegion = self.__class__.HubRegion(service, rules, path + [("HubRegion", "")])
                self.InletRegion = self.__class__.InletRegion(service, rules, path + [("InletRegion", "")])
                self.InteriorRegion = self.__class__.InteriorRegion(service, rules, path + [("InteriorRegion", "")])
                self.OutletRegion = self.__class__.OutletRegion(service, rules, path + [("OutletRegion", "")])
                self.Periodic1Region = self.__class__.Periodic1Region(service, rules, path + [("Periodic1Region", "")])
                self.Periodic2Region = self.__class__.Periodic2Region(service, rules, path + [("Periodic2Region", "")])
                self.ShroudRegion = self.__class__.ShroudRegion(service, rules, path + [("ShroudRegion", "")])
                self.SymmetryRegion = self.__class__.SymmetryRegion(service, rules, path + [("SymmetryRegion", "")])
                self.Tip1Region = self.__class__.Tip1Region(service, rules, path + [("Tip1Region", "")])
                self.Tip2Region = self.__class__.Tip2Region(service, rules, path + [("Tip2Region", "")])
                super().__init__(service, rules, path)

            class BladeRegion(PyTextual):
                """
                Parameter BladeRegion of value type str.
                """
                pass

            class FZSearchOrder(PyTextual):
                """
                Parameter FZSearchOrder of value type str.
                """
                pass

            class HubRegion(PyTextual):
                """
                Parameter HubRegion of value type str.
                """
                pass

            class InletRegion(PyTextual):
                """
                Parameter InletRegion of value type str.
                """
                pass

            class InteriorRegion(PyTextual):
                """
                Parameter InteriorRegion of value type str.
                """
                pass

            class OutletRegion(PyTextual):
                """
                Parameter OutletRegion of value type str.
                """
                pass

            class Periodic1Region(PyTextual):
                """
                Parameter Periodic1Region of value type str.
                """
                pass

            class Periodic2Region(PyTextual):
                """
                Parameter Periodic2Region of value type str.
                """
                pass

            class ShroudRegion(PyTextual):
                """
                Parameter ShroudRegion of value type str.
                """
                pass

            class SymmetryRegion(PyTextual):
                """
                Parameter SymmetryRegion of value type str.
                """
                pass

            class Tip1Region(PyTextual):
                """
                Parameter Tip1Region of value type str.
                """
                pass

            class Tip2Region(PyTextual):
                """
                Parameter Tip2Region of value type str.
                """
                pass

        class GraphicsSettings(PyMenu):
            """
            Singleton GraphicsSettings.
            """
            def __init__(self, service, rules, path):
                self.AutoDraw = self.__class__.AutoDraw(service, rules, path + [("AutoDraw", "")])
                super().__init__(service, rules, path)

            class AutoDraw(PyParameter):
                """
                Parameter AutoDraw of value type bool.
                """
                pass

        class CheckpointingOption(PyTextual):
            """
            Parameter CheckpointingOption of value type str.
            """
            pass

        class SaveCheckpointFiles(PyParameter):
            """
            Parameter SaveCheckpointFiles of value type bool.
            """
            pass

    class TurboWorkflow(PyMenu):
        """
        Singleton TurboWorkflow.
        """
        def __init__(self, service, rules, path):
            self.FaceZoneSettings = self.__class__.FaceZoneSettings(service, rules, path + [("FaceZoneSettings", "")])
            self.GraphicsSettings = self.__class__.GraphicsSettings(service, rules, path + [("GraphicsSettings", "")])
            self.CheckpointingOption = self.__class__.CheckpointingOption(service, rules, path + [("CheckpointingOption", "")])
            self.SaveCheckpointFiles = self.__class__.SaveCheckpointFiles(service, rules, path + [("SaveCheckpointFiles", "")])
            super().__init__(service, rules, path)

        class FaceZoneSettings(PyMenu):
            """
            Singleton FaceZoneSettings.
            """
            def __init__(self, service, rules, path):
                self.BladeRegion = self.__class__.BladeRegion(service, rules, path + [("BladeRegion", "")])
                self.FZSearchOrder = self.__class__.FZSearchOrder(service, rules, path + [("FZSearchOrder", "")])
                self.HubRegion = self.__class__.HubRegion(service, rules, path + [("HubRegion", "")])
                self.InletRegion = self.__class__.InletRegion(service, rules, path + [("InletRegion", "")])
                self.InteriorRegion = self.__class__.InteriorRegion(service, rules, path + [("InteriorRegion", "")])
                self.OutletRegion = self.__class__.OutletRegion(service, rules, path + [("OutletRegion", "")])
                self.Periodic1Region = self.__class__.Periodic1Region(service, rules, path + [("Periodic1Region", "")])
                self.Periodic2Region = self.__class__.Periodic2Region(service, rules, path + [("Periodic2Region", "")])
                self.ShroudRegion = self.__class__.ShroudRegion(service, rules, path + [("ShroudRegion", "")])
                self.SymmetryRegion = self.__class__.SymmetryRegion(service, rules, path + [("SymmetryRegion", "")])
                self.Tip1Region = self.__class__.Tip1Region(service, rules, path + [("Tip1Region", "")])
                self.Tip2Region = self.__class__.Tip2Region(service, rules, path + [("Tip2Region", "")])
                super().__init__(service, rules, path)

            class BladeRegion(PyTextual):
                """
                Parameter BladeRegion of value type str.
                """
                pass

            class FZSearchOrder(PyTextual):
                """
                Parameter FZSearchOrder of value type str.
                """
                pass

            class HubRegion(PyTextual):
                """
                Parameter HubRegion of value type str.
                """
                pass

            class InletRegion(PyTextual):
                """
                Parameter InletRegion of value type str.
                """
                pass

            class InteriorRegion(PyTextual):
                """
                Parameter InteriorRegion of value type str.
                """
                pass

            class OutletRegion(PyTextual):
                """
                Parameter OutletRegion of value type str.
                """
                pass

            class Periodic1Region(PyTextual):
                """
                Parameter Periodic1Region of value type str.
                """
                pass

            class Periodic2Region(PyTextual):
                """
                Parameter Periodic2Region of value type str.
                """
                pass

            class ShroudRegion(PyTextual):
                """
                Parameter ShroudRegion of value type str.
                """
                pass

            class SymmetryRegion(PyTextual):
                """
                Parameter SymmetryRegion of value type str.
                """
                pass

            class Tip1Region(PyTextual):
                """
                Parameter Tip1Region of value type str.
                """
                pass

            class Tip2Region(PyTextual):
                """
                Parameter Tip2Region of value type str.
                """
                pass

        class GraphicsSettings(PyMenu):
            """
            Singleton GraphicsSettings.
            """
            def __init__(self, service, rules, path):
                self.AutoDraw = self.__class__.AutoDraw(service, rules, path + [("AutoDraw", "")])
                super().__init__(service, rules, path)

            class AutoDraw(PyParameter):
                """
                Parameter AutoDraw of value type bool.
                """
                pass

        class CheckpointingOption(PyTextual):
            """
            Parameter CheckpointingOption of value type str.
            """
            pass

        class SaveCheckpointFiles(PyParameter):
            """
            Parameter SaveCheckpointFiles of value type bool.
            """
            pass

