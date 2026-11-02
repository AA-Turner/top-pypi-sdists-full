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
    Angle = 1
    Dimensionless = 2
    Frequency = 3
    Force = 4
    ID = 5
    Pressure = 6
    HeatTransferCoefficient = 7
    Stress = 8
    Temperature = 9
    AverageFilmTemperature = 10
    BulkTemperature = 11
    SurfaceTemperature = 12
    DifferenceBetweenSurfaceAndBulkTemperature = 13
    Length = 14
    ThetaCoordinate = 15
    Time = 16
    XCoordinate = 17
    YCoordinate = 18
    ZCoordinate = 19
    Strain = 20
    StrainScalingFactor = 21
    HeatFlux = 22
    HeatGeneration = 23
    HeatTransferRate = 24
    RotationalVelocityVectorAmplitude = 25
    CyclicSectorNumber = 26
    ElementNumber = 27
    GeometricGap = 28
    HarmonicBasedLoad = 29
    MultistageHarmonicIndex = 30
    NodeNumber = 31
    PhaseShift = 32
    Velocity = 33

