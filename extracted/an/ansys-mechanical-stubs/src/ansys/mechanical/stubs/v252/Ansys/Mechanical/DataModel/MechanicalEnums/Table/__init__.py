"""Table module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ImportFormat(Enum):
    """
    
            Specifies how to interpret the variable data source.
            
    """

    Automatic = 0
    Delimited = 1
    FixedWidth = 2

class TableRefreshImportOn(Enum):
    """
    Allows control on when an import should be refreshed.
    """

    BeforeSolve = 1
    None_ = 0

class VariableClassification(Enum):
    """
    
             This enum represents the classification of variables that can be represented by Table
             variables/columns.
            
             A full variable definition requires both a  and an
             .
            
             The explicit enum values need to be kept in-sync with the Typescript enumeration of the
             same name in the frontend Angular project.
             
    """

    Unclassified = 0
    Independent = 1
    Real = 2
    Imaginary = 3
    RealComponentGroup = 200
    Real_i = 201
    Real_j = 202
    Real_k = 203
    ImaginaryComponentGroup = 300
    Imaginary_i = 301
    Imaginary_j = 302
    Imaginary_k = 303

class VariableType(Enum):
    """
    
            An enumeration of the different variable types supported by the tabular data
             implementation "Ansys.ACT.Automation.Mechanical.Table.Column".
            
    """

    Unknown = 0
    Frequency = 1
    Force = 2
    ID = 3
    Pressure = 4
    HeatTransferCoefficient = 5
    Stress = 6
    Temperature = 7
    AverageFilmTemperature = 8
    BulkTemperature = 9
    SurfaceTemperature = 10
    DifferenceBetweenSurfaceAndBulkTemperature = 11
    ThetaCoordinate = 12
    Time = 13
    XCoordinate = 14
    YCoordinate = 15
    ZCoordinate = 16
    StrainScalingFactor = 17

