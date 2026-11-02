"""Utilities module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class GeometryImportPreferences(object):
    """
    
             
             This is used to provide import and reload (refresh) preferences for geometry file import.
             These preferences are identical to those exposed in the WB2 project schematic and Mechanical
             Geometry preferences. More information can be found in the “Geometry Preferences” section of
             the “CAD Integration” documentation. Both general and advanced preferences are provided.
             
            
             
             Default values will be taken from the Mechanical preferences. This allows user-specified
             default values to propagate to these preferences.
             
             
    """

    @property
    def ProcessSolids(self) -> typing.Optional[bool]:
        """
        
            Import solid bodies.
            
        """
        return None

    @ProcessSolids.setter
    def ProcessSolids(self, value: typing.Optional[bool]) -> None:
        """
        
            Import solid bodies.
            
        """
        pass

    @property
    def ProcessSurfaces(self) -> typing.Optional[bool]:
        """
        
            Import surface bodies.
            
        """
        return None

    @ProcessSurfaces.setter
    def ProcessSurfaces(self, value: typing.Optional[bool]) -> None:
        """
        
            Import surface bodies.
            
        """
        pass

    @property
    def ProcessLines(self) -> typing.Optional[bool]:
        """
        
            Import lines bodies.
            
        """
        return None

    @ProcessLines.setter
    def ProcessLines(self, value: typing.Optional[bool]) -> None:
        """
        
            Import lines bodies.
            
        """
        pass

    @property
    def ProcessAttributes(self) -> typing.Optional[bool]:
        """
        
            Import CAD system attributes.
            
        """
        return None

    @ProcessAttributes.setter
    def ProcessAttributes(self, value: typing.Optional[bool]) -> None:
        """
        
            Import CAD system attributes.
            
        """
        pass

    @property
    def AttributeKey(self) -> typing.Optional[str]:
        """
        
            If `ProcessAttributes` is `true`, import only those attributes with this prefix.
            Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        return None

    @AttributeKey.setter
    def AttributeKey(self, value: typing.Optional[str]) -> None:
        """
        
            If `ProcessAttributes` is `true`, import only those attributes with this prefix.
            Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        pass

    @property
    def ProcessParameters(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Parameters]:
        """
        
            Enum to specify how parameters should be processed.
            
        """
        return None

    @ProcessParameters.setter
    def ProcessParameters(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Parameters]) -> None:
        """
        
            Enum to specify how parameters should be processed.
            
        """
        pass

    @property
    def ParameterKey(self) -> typing.Optional[str]:
        """
        
            If `ProcessParameters` is not `None`, this specifies the prefix or postfix filtering
            that will be used to identify enabled Workbench parameters. Multiple semicolon-delimited
            filters may be specified.
            
        """
        return None

    @ParameterKey.setter
    def ParameterKey(self, value: typing.Optional[str]) -> None:
        """
        
            If `ProcessParameters` is not `None`, this specifies the prefix or postfix filtering
            that will be used to identify enabled Workbench parameters. Multiple semicolon-delimited
            filters may be specified.
            
        """
        pass

    @property
    def ProcessNamedSelections(self) -> typing.Optional[bool]:
        """
        
            Import/create named selections.
            
        """
        return None

    @ProcessNamedSelections.setter
    def ProcessNamedSelections(self, value: typing.Optional[bool]) -> None:
        """
        
            Import/create named selections.
            
        """
        pass

    @property
    def NamedSelectionKey(self) -> typing.Optional[str]:
        """
        
            If `ProcessNamedSelections` is `true`, import only those named selections with this
            prefix. Multiple semicolon-delimited filters may be specified.
            
        """
        return None

    @NamedSelectionKey.setter
    def NamedSelectionKey(self, value: typing.Optional[str]) -> None:
        """
        
            If `ProcessNamedSelections` is `true`, import only those named selections with this
            prefix. Multiple semicolon-delimited filters may be specified.
            
        """
        pass

    @property
    def ProcessMaterialProperties(self) -> typing.Optional[bool]:
        """
        
            Import primary material data defined in the CAD source.
            
        """
        return None

    @ProcessMaterialProperties.setter
    def ProcessMaterialProperties(self, value: typing.Optional[bool]) -> None:
        """
        
            Import primary material data defined in the CAD source.
            
        """
        pass

    @property
    def AnalysisType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.AnalysisType]:
        """
        
            Specify the analysis type to target during import.
            
        """
        return None

    @AnalysisType.setter
    def AnalysisType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.AnalysisType]) -> None:
        """
        
            Specify the analysis type to target during import.
            
        """
        pass

    @property
    def CADAssociativity(self) -> typing.Optional[bool]:
        """
        
            Allow associativity.
            
        """
        return None

    @CADAssociativity.setter
    def CADAssociativity(self, value: typing.Optional[bool]) -> None:
        """
        
            Allow associativity.
            
        """
        pass

    @property
    def ProcessCoordinateSystems(self) -> typing.Optional[bool]:
        """
        
            Import coordinate systems defined in the CAD source.
            
        """
        return None

    @ProcessCoordinateSystems.setter
    def ProcessCoordinateSystems(self, value: typing.Optional[bool]) -> None:
        """
        
            Import coordinate systems defined in the CAD source.
            
        """
        pass

    @property
    def CoordinateSystemKey(self) -> typing.Optional[str]:
        """
        
            If `ProcessCoordinateSystems` is `true`, import only those coordinate systems with this
            prefix. Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        return None

    @CoordinateSystemKey.setter
    def CoordinateSystemKey(self, value: typing.Optional[str]) -> None:
        """
        
            If `ProcessCoordinateSystems` is `true`, import only those coordinate systems with this
            prefix. Multiple semicolon-delimited filters may be specified. An empty string matches
            everything.
            
        """
        pass

    @property
    def ProcessWorkPoints(self) -> typing.Optional[bool]:
        """
        
            Import work points.
            
        """
        return None

    @ProcessWorkPoints.setter
    def ProcessWorkPoints(self, value: typing.Optional[bool]) -> None:
        """
        
            Import work points.
            
        """
        pass

    @property
    def ReaderSaveFile(self) -> typing.Optional[bool]:
        """
        
            Save the part file of a model after the import.
            
        """
        return None

    @ReaderSaveFile.setter
    def ReaderSaveFile(self, value: typing.Optional[bool]) -> None:
        """
        
            Save the part file of a model after the import.
            
        """
        pass

    @property
    def ProcessInstances(self) -> typing.Optional[bool]:
        """
        
            Honor part instance specifications.
            
        """
        return None

    @ProcessInstances.setter
    def ProcessInstances(self, value: typing.Optional[bool]) -> None:
        """
        
            Honor part instance specifications.
            
        """
        pass

    @property
    def DoSmartUpdate(self) -> typing.Optional[bool]:
        """
        
            Speed up refreshes for models with unmodified components. Causes changes to other import
            preferences to be ignored during refresh.
            
        """
        return None

    @DoSmartUpdate.setter
    def DoSmartUpdate(self, value: typing.Optional[bool]) -> None:
        """
        
            Speed up refreshes for models with unmodified components. Causes changes to other import
            preferences to be ignored during refresh.
            
        """
        pass

    @property
    def ComparePartsOnUpdate(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsOnUpdate]:
        """
        
            Enable mesh preservation on refresh for unmodified entities.
            
        """
        return None

    @ComparePartsOnUpdate.setter
    def ComparePartsOnUpdate(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsOnUpdate]) -> None:
        """
        
            Enable mesh preservation on refresh for unmodified entities.
            
        """
        pass

    @property
    def ComparePartsTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsTolerance]:
        """
        
            Specifies the tolerance to use when comparing parts.
            
        """
        return None

    @ComparePartsTolerance.setter
    def ComparePartsTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.ComparePartsTolerance]) -> None:
        """
        
            Specifies the tolerance to use when comparing parts.
            
        """
        pass

    @property
    def EnclosureSymmetryProcessing(self) -> typing.Optional[bool]:
        """
        
            Enable the processing of enclosure and symmetry named selections.
            
        """
        return None

    @EnclosureSymmetryProcessing.setter
    def EnclosureSymmetryProcessing(self, value: typing.Optional[bool]) -> None:
        """
        
            Enable the processing of enclosure and symmetry named selections.
            
        """
        pass

    @property
    def DecomposeDisjointGeometry(self) -> typing.Optional[bool]:
        """
        
            Enable the decomposition of disjoint geometries for the following associative geometry
            interfaces:
            
            
            Creo Parametric (faces only)
            
            
            Autodesk Inventor (bodies only)
            
            
            
        """
        return None

    @DecomposeDisjointGeometry.setter
    def DecomposeDisjointGeometry(self, value: typing.Optional[bool]) -> None:
        """
        
            Enable the decomposition of disjoint geometries for the following associative geometry
            interfaces:
            
            
            Creo Parametric (faces only)
            
            
            Autodesk Inventor (bodies only)
            
            
            
        """
        pass

    @property
    def MixedImportResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.MixedImportResolution]:
        """
        
            Allows mixed-dimension parts to be imported as assembly components with parts of
            different dimensions.
            
        """
        return None

    @MixedImportResolution.setter
    def MixedImportResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.MixedImportResolution]) -> None:
        """
        
            Allows mixed-dimension parts to be imported as assembly components with parts of
            different dimensions.
            
        """
        pass

    @property
    def Clean(self) -> typing.Optional[bool]:
        """
        
            Clean unwanted features when importing geometry.
            
        """
        return None

    @Clean.setter
    def Clean(self, value: typing.Optional[bool]) -> None:
        """
        
            Clean unwanted features when importing geometry.
            
        """
        pass

    @property
    def StitchType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.StitchSurfacesOnImport]:
        """
        
            Specifies how surfaces should be stitched together.
            
        """
        return None

    @StitchType.setter
    def StitchType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.StitchSurfacesOnImport]) -> None:
        """
        
            Specifies how surfaces should be stitched together.
            
        """
        pass

    @property
    def StitchTolerance(self) -> typing.Optional[float]:
        """
        
            If `StitchType` is `User`, specifies the tolerance to use for stitching detection.
            
        """
        return None

    @StitchTolerance.setter
    def StitchTolerance(self, value: typing.Optional[float]) -> None:
        """
        
            If `StitchType` is `User`, specifies the tolerance to use for stitching detection.
            
        """
        pass

    @property
    def FacetQuality(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.FacetQuality]:
        """
        
            Specifies what facet quality should be used for the import. 
            The default value is Source meaning that the facets as represented in the CAD 
            system or use a Normal option for those that do not have display. 
            The others are relative settings compared to "normal" facet quality. 
            Typically, better facet quality requires more memory and may take additional time to import/update.
            
        """
        return None

    @FacetQuality.setter
    def FacetQuality(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.FacetQuality]) -> None:
        """
        
            Specifies what facet quality should be used for the import. 
            The default value is Source meaning that the facets as represented in the CAD 
            system or use a Normal option for those that do not have display. 
            The others are relative settings compared to "normal" facet quality. 
            Typically, better facet quality requires more memory and may take additional time to import/update.
            
        """
        pass

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    @typing.overload
    def GetScriptedPropertySetter(cls, variableName: str, preferencesToChange: Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences, preferencesToMirror: Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences) -> str:
        ...

    @classmethod
    @typing.overload
    def GetScriptedPropertySetter(cls, variableName: str, propertiesChanged: dict[str,typing.Any]) -> str:
        ...

    @classmethod
    def GetScriptedPropertySetter(cls, *args: typing.Any) -> str:
        """
        
            Get a string containing script-executable commands to set the properties on a
            preferences instance preferencesToChange, with the scripted name
            variableName, to match the properties on another preferences instance
            preferencesToMirror. Only the properties that are different will be used.
            
        """
        pass


