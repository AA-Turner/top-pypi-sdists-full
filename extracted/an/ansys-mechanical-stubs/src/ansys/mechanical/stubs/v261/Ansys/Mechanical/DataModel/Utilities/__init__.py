"""Utilities module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.Mechanical.DataModel.Utilities.TabularData as TabularData
import ansys.mechanical.stubs.v261.Ansys.Mechanical.DataModel.Utilities.Dataset as Dataset
import ansys.mechanical.stubs.v261.Ansys.Mechanical.DataModel.Utilities.Charts as Charts


class RigidBodyTransformationMatrix(object):
    """
    
             A 4x4 transformation matrix, to be used explicitly for rigid body transformations. The
             transformation matrix is in column-major format. Elements 0-3 represent, respectively,
             the x-components of the X axis, Y axis, Z axis, and translation with respect to global.
             Identically, elements 4-7 represent the y components and elements 8-11 the z components.
             Elements 2-15, per rigid-body requirements, are expected to be [0.0, 0.0, 0.0, 1.0].
            
             The ability to piecewise set rotation and translation components precludes the option of
             validating the matrix data at every operation. Thus, these values ***must*** be checked
             before the data is used.
            
             The class `Ansys.ACT.Common.SimpleTransform` provides a simplified mechanism for working
             with rigid body transformations and getting a `RigidBodyTransformationMatrix` object.
             
    """

    @property
    def Data(self) -> typing.Optional[typing.List[typing.Any]]:
        """
        
            A 16-value list representing a linearized 4x4 transformation matrix.
            
        """
        return None

    @Data.setter
    def Data(self, value: typing.Optional[typing.List[typing.Any]]) -> None:
        """
        
            A 16-value list representing a linearized 4x4 transformation matrix.
            
        """
        pass

    @property
    def X_x(self) -> typing.Optional[float]:
        """
        
            Element 0: the x component of the X axis rotation.
            
        """
        return None

    @X_x.setter
    def X_x(self, value: typing.Optional[float]) -> None:
        """
        
            Element 0: the x component of the X axis rotation.
            
        """
        pass

    @property
    def X_y(self) -> typing.Optional[float]:
        """
        
            Element 4: the y component of the X axis rotation.
            
        """
        return None

    @X_y.setter
    def X_y(self, value: typing.Optional[float]) -> None:
        """
        
            Element 4: the y component of the X axis rotation.
            
        """
        pass

    @property
    def X_z(self) -> typing.Optional[float]:
        """
        
            Element 8: the z component of the X axis rotation.
            
        """
        return None

    @X_z.setter
    def X_z(self, value: typing.Optional[float]) -> None:
        """
        
            Element 8: the z component of the X axis rotation.
            
        """
        pass

    @property
    def Y_x(self) -> typing.Optional[float]:
        """
        
            Element 1: the x component of the Y axis rotation.
            
        """
        return None

    @Y_x.setter
    def Y_x(self, value: typing.Optional[float]) -> None:
        """
        
            Element 1: the x component of the Y axis rotation.
            
        """
        pass

    @property
    def Y_y(self) -> typing.Optional[float]:
        """
        
            Element 5: the y component of the Y axis rotation.
            
        """
        return None

    @Y_y.setter
    def Y_y(self, value: typing.Optional[float]) -> None:
        """
        
            Element 5: the y component of the Y axis rotation.
            
        """
        pass

    @property
    def Y_z(self) -> typing.Optional[float]:
        """
        
            Element 9: the z component of the Y axis rotation.
            
        """
        return None

    @Y_z.setter
    def Y_z(self, value: typing.Optional[float]) -> None:
        """
        
            Element 9: the z component of the Y axis rotation.
            
        """
        pass

    @property
    def Z_x(self) -> typing.Optional[float]:
        """
        
            Element 2: the x component of the Z axis rotation.
            
        """
        return None

    @Z_x.setter
    def Z_x(self, value: typing.Optional[float]) -> None:
        """
        
            Element 2: the x component of the Z axis rotation.
            
        """
        pass

    @property
    def Z_y(self) -> typing.Optional[float]:
        """
        
            Element 6: the y component of the Z axis rotation.
            
        """
        return None

    @Z_y.setter
    def Z_y(self, value: typing.Optional[float]) -> None:
        """
        
            Element 6: the y component of the Z axis rotation.
            
        """
        pass

    @property
    def Z_z(self) -> typing.Optional[float]:
        """
        
            Element 10: the z component of the Z axis rotation.
            
        """
        return None

    @Z_z.setter
    def Z_z(self, value: typing.Optional[float]) -> None:
        """
        
            Element 10: the z component of the Z axis rotation.
            
        """
        pass

    @property
    def T_x(self) -> typing.Optional[float]:
        """
        
            Element 3: the x component of the translation.
            
        """
        return None

    @T_x.setter
    def T_x(self, value: typing.Optional[float]) -> None:
        """
        
            Element 3: the x component of the translation.
            
        """
        pass

    @property
    def T_y(self) -> typing.Optional[float]:
        """
        
            Element 7: the y component of the translation.
            
        """
        return None

    @T_y.setter
    def T_y(self, value: typing.Optional[float]) -> None:
        """
        
            Element 7: the y component of the translation.
            
        """
        pass

    @property
    def T_z(self) -> typing.Optional[float]:
        """
        
            Element 11: the z component of the translation.
            
        """
        return None

    @T_z.setter
    def T_z(self, value: typing.Optional[float]) -> None:
        """
        
            Element 11: the z component of the translation.
            
        """
        pass

    @property
    def tau_x(self) -> typing.Optional[float]:
        """
        
            Element 12: the x component of the shear, which must be '0.0' for rigid body
            transformations.
            
        """
        return None

    @property
    def tau_y(self) -> typing.Optional[float]:
        """
        
            Element 13: the y component of the shear, which must be '0.0' for rigid body
            transformations.
            
        """
        return None

    @property
    def tau_z(self) -> typing.Optional[float]:
        """
        
            Element 14: the z component of the shear, which must be '0.0' for rigid body
            transformations.
            
        """
        return None

    @property
    def S(self) -> typing.Optional[float]:
        """
        
            Element 15: the transformation scale, which must be '1.0' for rigid body
            transformations.
            
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, data: typing.List[typing.Any]) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def IsMatrixWellFormed(self) -> bool:
        """
        
            Verify that the data meets the following criteria for a rigid-body transformation:
              1) The rotation matrix contains three orthonormal orientations
              2) The transformation components are valid values
              3) The shear components are all zero
              4) The scale value is unity
            
        """
        pass

    def IsRotationValid(self) -> bool:
        """
        IsRotationValid method.
        """
        pass

    def IsTranslationValid(self) -> bool:
        """
        IsTranslationValid method.
        """
        pass

    def IsShearValid(self) -> bool:
        """
        IsShearValid method.
        """
        pass

    def IsScaleValid(self) -> bool:
        """
        IsScaleValid method.
        """
        pass


class BeamCoordinateSystem(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


class CenterOfGravityCoordinateSystem(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


