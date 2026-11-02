"""CDB module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CDBCommand(object):

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCommand: Ansys.Common.Interop.FECommandsModel.ICommand) -> None:
        """
        __init__ method.
        """
        pass


class BeamSecBlockCommand(object):
    """
    
            Represents a beam SECBLOCK command.
            
    """

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Gets the section type.
            
        """
        return None

    @property
    def Nodes(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandNode]]:
        """
        
            Gets the nodes of the section.
            
        """
        return None

    @property
    def Cells(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandCell]]:
        """
        
            Gets the cells of the section.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iBeamSecBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IBeamSecBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class BFBlockCommand(object):
    """
    
            Represents a BFBLOCK command.
            
    """

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def NodalBodyForceCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of nodal body-force loads.
            
        """
        return None

    @property
    def NodalBodyForces(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandNodalBodyForce]]:
        """
        
            Gets the nodal body-force loads.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iBFBlockCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.IBFBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class BFCommand(object):
    """
    
            Represents a BF command.
            
    """

    @property
    def Node(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def ValCount(self) -> typing.Optional[typing.Any]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iBFCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IBFCommand) -> None:
        """
        __init__ method.
        """
        pass


class BFECommand(object):
    """
    
            Represents a BFE command.
            
    """

    @property
    def Elem(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def Stloc(self) -> typing.Optional[int]:
        """
        
            Gets the starting location.
            
        """
        return None

    @property
    def ValCount(self) -> typing.Optional[typing.Any]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iBFECommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IBFECommand) -> None:
        """
        __init__ method.
        """
        pass


class BFEBlockCommand(object):
    """
    
            Represents a BFEBLOCK command.
            
    """

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def ElementBodyForceCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of element body-force loads.
            
        """
        return None

    @property
    def ElementBodyForces(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandElementBodyForce]]:
        """
        
            Gets the element body-force loads.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iBFEBlockCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.IBFEBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class CECommand(object):
    """
    
            Represents a CE command.
            
    """

    @property
    def Nce(self) -> typing.Optional[int]:
        """
        
            Gets the constraint equation number.
            
        """
        return None

    @property
    def Constant(self) -> typing.Optional[float]:
        """
        
            Gets the constant term of the equation.
            
        """
        return None

    @property
    def Terms(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandCETerm]]:
        """
        
            Gets the equation terms.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCECommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICECommand) -> None:
        """
        __init__ method.
        """
        pass


class CECMODCommand(object):
    """
    
            Represents a CECMOD command.
            
    """

    @property
    def Nce(self) -> typing.Optional[int]:
        """
        
            Gets the constraint equation number.
            
        """
        return None

    @property
    def Constant(self) -> typing.Optional[float]:
        """
        
            Gets the constant term of the equation.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCECMODCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICECMODCommand) -> None:
        """
        __init__ method.
        """
        pass


class CMBlockCommand(object):
    """
    
            Represents a CMBLOCK command.
            
    """

    @property
    def Cmname(self) -> typing.Optional[str]:
        """
        
            Gets the component name.
            
        """
        return None

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Gets the type of entities (node or elem).
            
        """
        return None

    @property
    def Elements(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the type of entities.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCMBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICMBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class CMEDITCommand(object):
    """
    
            Represents a CMEDIT command.
            
    """

    @property
    def Aname(self) -> typing.Optional[str]:
        """
        
            Gets the assembly name.
            
        """
        return None

    @property
    def Oper(self) -> typing.Optional[str]:
        """
        
            Gets the operation label (add or dele).
            
        """
        return None

    @property
    def Cnames(self) -> typing.Optional[tuple[str]]:
        """
        
            Gets the component names.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCMEDITCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICMEDITCommand) -> None:
        """
        __init__ method.
        """
        pass


class CMGRPCommand(object):
    """
    
            Represents a CMGRP command.
            
    """

    @property
    def Aname(self) -> typing.Optional[str]:
        """
        
            Gets the assembly name.
            
        """
        return None

    @property
    def Cnames(self) -> typing.Optional[tuple[str]]:
        """
        
            Gets the component and/or assembly names.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCMGRPCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICMGRPCommand) -> None:
        """
        __init__ method.
        """
        pass


class CPCommand(object):
    """
    
            Represents a CP command.
            
    """

    @property
    def Ncp(self) -> typing.Optional[int]:
        """
        
            Gets the number of coupled nodes.
            
        """
        return None

    @property
    def Dof(self) -> typing.Optional[str]:
        """
        
            Gets the degree of freedom label.
            
        """
        return None

    @property
    def Nodes(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the nodes.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iCPCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICPCommand) -> None:
        """
        __init__ method.
        """
        pass


class EBlockCommand(object):
    """
    
            Represents an EBLOCK command.
            
    """

    @property
    def Elements(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandElement]]:
        """
        
            Gets the elements.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iEBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IEBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class ENCommand(object):
    """
    
            Represents an EN command.
            
    """

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Gets the type (attribute or node).
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iENCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IENCommand) -> None:
        """
        __init__ method.
        """
        pass


class ETCommand(object):
    """
    
            Represents an ET command.
            
    """

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Ename(self) -> typing.Optional[int]:
        """
        
            Gets the element name.
            
        """
        return None

    @property
    def Keyopts(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandKeyOpt]]:
        """
        
            Gets the key options.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iETCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IETCommand) -> None:
        """
        __init__ method.
        """
        pass


class GenericCommand(object):
    """
    
            Represents a generic command.
            
    """

    @property
    def Arguments(self) -> typing.Optional[tuple[str]]:
        """
        
            Gets the arguments.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iGenericCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IGenericCommand) -> None:
        """
        __init__ method.
        """
        pass


class LocalCommand(object):
    """
    
            Represents a LOCAL command.
            
    """

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Gets the type of the data to be defined.
            
        """
        return None

    @property
    def Ncsy(self) -> typing.Optional[int]:
        """
        
            Gets the system number.
            
        """
        return None

    @property
    def Cstyp(self) -> typing.Optional[int]:
        """
        
            Gets the system type.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iLocalCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ILocalCommand) -> None:
        """
        __init__ method.
        """
        pass


class MPCommand(object):
    """
    
            Represents a MP command.
            
    """

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def C0(self) -> typing.Optional[float]:
        """
        
            Gets the temperature-independent term of the property.
            
        """
        return None

    @property
    def C1(self) -> typing.Optional[float]:
        """
        
            Gets the coefficient of the linear term in the property-versus-temperature polynomial.
            
        """
        return None

    @property
    def C2(self) -> typing.Optional[float]:
        """
        
            Gets the coefficient of the quadratic term in the property-versus-temperature polynomial.
            
        """
        return None

    @property
    def C3(self) -> typing.Optional[float]:
        """
        
            Gets the coefficient of the cubic term in the property-versus-temperature polynomial.
            
        """
        return None

    @property
    def C4(self) -> typing.Optional[float]:
        """
        
            Gets the coefficient of the quartic term in the property-versus-temperature polynomial.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iMPCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IMPCommand) -> None:
        """
        __init__ method.
        """
        pass


class MPDataCommand(object):
    """
    
            Represents a MPDATA command.
            
    """

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def Temps(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the temperatures.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iMPDataCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IMPDataCommand) -> None:
        """
        __init__ method.
        """
        pass


class NBlockCommand(object):
    """
    
            Represents a NBLOCK command.
            
    """

    @property
    def Nodes(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandNode]]:
        """
        
            Gets the nodes.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iNBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.INBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class NCommand(object):
    """
    
            Represents a N command.
            
    """

    @property
    def Node(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Gets the type of the data to be defined.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iNCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.INCommand) -> None:
        """
        __init__ method.
        """
        pass


class PreadCommand(object):
    """
    
            Represents a *PREAD command.
            
    """

    @property
    def Aname(self) -> typing.Optional[str]:
        """
        
            Gets the table name.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iPreadCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IPreadCommand) -> None:
        """
        __init__ method.
        """
        pass


class RCommand(object):
    """
    
            Represents a R command.
            
    """

    @property
    def Nset(self) -> typing.Optional[int]:
        """
        
            Gets the set number.
            
        """
        return None

    @property
    def Stloc(self) -> typing.Optional[int]:
        """
        
            Gets the starting location.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iRCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IRCommand) -> None:
        """
        __init__ method.
        """
        pass


class RLBlockCommand(object):
    """
    
            Represents a RLBLOCK command.
            
    """

    @property
    def Reals(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandReal]]:
        """
        
            Gets the real constant sets.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iRLBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IRLBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class SecdataCommand(object):
    """
    
            Represents a SECDATA command.
            
    """

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSecdataCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISecdataCommand) -> None:
        """
        __init__ method.
        """
        pass


class SecoffsetCommand(object):
    """
    
            Represents a SECOFFSET command.
            
    """

    @property
    def Location(self) -> typing.Optional[str]:
        """
        
            Gets the location of nodes in the section.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSecoffsetCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISecoffsetCommand) -> None:
        """
        __init__ method.
        """
        pass


class SectypeCommand(object):
    """
    
            Represents a SECTYPE command.
            
    """

    @property
    def Secid(self) -> typing.Optional[int]:
        """
        
            Gets the section type number.
            
        """
        return None

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Get the type.
            
        """
        return None

    @property
    def Subtype(self) -> typing.Optional[str]:
        """
        
            Gets the subtype.
            
        """
        return None

    @property
    def Secname(self) -> typing.Optional[str]:
        """
        
            Gets the section name.
            
        """
        return None

    @property
    def RefineKey(self) -> typing.Optional[int]:
        """
        
            Mesh refinement level for thin-walled beam sections. Default is zero. Meaningless if type is not BEAM.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSectypeCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISectypeCommand) -> None:
        """
        __init__ method.
        """
        pass


class SeccontrolCommand(object):
    """
    
            Represents a SECCONTROL command.
            
    """

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSeccontrolCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISeccontrolCommand) -> None:
        """
        __init__ method.
        """
        pass


class SFEBlockCommand(object):
    """
    
            Represents a SFEBLOCK command.
            
    """

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the surface load label.
            
        """
        return None

    @property
    def ElementSurfaceLoadCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of element surface loads.
            
        """
        return None

    @property
    def ElementSurfaceLoads(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandElementSurfaceLoad]]:
        """
        
            Get the element surface loads.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSFEBlockCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISFEBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class SFECommand(object):
    """
    
            Represents a SFE command.
            
    """

    @property
    def Elem(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def LKey(self) -> typing.Optional[int]:
        """
        
            Get the load key.
            
        """
        return None

    @property
    def Key(self) -> typing.Optional[int]:
        """
        
            Gets the value key.
            
        """
        return None

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the load label.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iSFECommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.ISFECommand) -> None:
        """
        __init__ method.
        """
        pass


class ShellSecBlockCommand(object):
    """
    
            Represents a shell SECBLOCK command.
            
    """

    @property
    def Type(self) -> typing.Optional[str]:
        """
        
            Get the section type.
            
        """
        return None

    @property
    def Layers(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandLayer]]:
        """
        
            Gets the layers.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iShellSecBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IShellSecBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class CommandCell(object):
    """
    
            Represents cell data associated to a beam SECBLOCK command.
            
    """

    @property
    def MatId(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Nodes(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the nodes.
            
        """
        return None

    def __init__(self, iCell: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICell) -> None:
        """
        __init__ method.
        """
        pass


class CommandCETerm(object):
    """
    
            Represents a term associated to a CE command.
            
    """

    @property
    def Node(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def Dof(self) -> typing.Optional[str]:
        """
        
            Gets the degree of freedom.
            
        """
        return None

    @property
    def Coefficient(self) -> typing.Optional[float]:
        """
        
            Gets the coefficient.
            
        """
        return None

    def __init__(self, iCETerm: Ansys.Common.Interop.FEParsePlugin_ANSYS.ICETerm) -> None:
        """
        __init__ method.
        """
        pass


class CommandElement(object):
    """
    
            Represents an element associated to an EBLOCK command.
            
    """

    @property
    def Csys(self) -> typing.Optional[int]:
        """
        
            Gets the coordinate system number.
            
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Real(self) -> typing.Optional[int]:
        """
        
            Gets the real constant set number.
            
        """
        return None

    @property
    def Section(self) -> typing.Optional[int]:
        """
        
            Gets the section number.
            
        """
        return None

    @property
    def Type(self) -> typing.Optional[int]:
        """
        
            Gets the element type number.
            
        """
        return None

    @property
    def ElementShapeFlag(self) -> typing.Optional[int]:
        """
        
            Gets the element shape flag used for contact element types.
            
        """
        return None

    @property
    def NodeCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of nodes.
            
        """
        return None

    @property
    def Nodes(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the nodes.
            
        """
        return None

    def __init__(self, iElement: Ansys.Common.Interop.FEParsePlugin_ANSYS.IElement) -> None:
        """
        __init__ method.
        """
        pass


class CommandElementType(object):
    """
    
            Represents an element type associated to an ETBLOCK command.
            
    """

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Ename(self) -> typing.Optional[int]:
        """
        
            Gets the element name.
            
        """
        return None

    @property
    def Keyopts(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandKeyOpt]]:
        """
        
            Gets the key options.
            
        """
        return None

    def __init__(self, iElementType: Ansys.Common.Interop.FEParsePlugin_ANSYS.IAnsysElementType) -> None:
        """
        __init__ method.
        """
        pass


class CommandNodalLoad(object):
    """
    
            Represents an nodal load  associated to an F BLOCK or D Block  command.
            
    """

    @property
    def Node(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def Dof(self) -> typing.Optional[str]:
        """
        
            Gets the dof.
            
        """
        return None

    @property
    def ValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iNodalLoad: Ansys.Common.Interop.FEParsePlugin_ANSYS.INodalLoad) -> None:
        """
        __init__ method.
        """
        pass


class CommandElementBodyForce(object):
    """
    
            Represents element body-force loads associated to BFEBLOCK command.
            
    """

    @property
    def Elem(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of element body-force loads.
            
        """
        return None

    @property
    def Stlocs(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the starting locations.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iElementBodyForce: Ansys.Common.Interop.FEParsePlugin_ANSYS.IElementBodyForce) -> None:
        """
        __init__ method.
        """
        pass


class CommandElementSurfaceLoad(object):
    """
    
            Represents an element surface load associated to a SFEBLOCK command.
            
    """

    @property
    def Elem(self) -> typing.Optional[int]:
        """
        
            Gets the element number.
            
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of element surface loads.
            
        """
        return None

    @property
    def LKeys(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the load keys.
            
        """
        return None

    @property
    def Keys(self) -> typing.Optional[tuple[int]]:
        """
        
            Gets the keys.
            
        """
        return None

    @property
    def ElementSurfaceLoadValues(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandElementSurfaceLoadValues]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iElementSurfaceLoad: Ansys.Common.Interop.FEParsePlugin_ANSYS.IElementSurfaceLoad) -> None:
        """
        __init__ method.
        """
        pass


class CommandElementSurfaceLoadValues(object):
    """
    
            Values associated to an element surface load from a SFEBLOCK command.
            
    """

    @property
    def ValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iElementSurfaceLoadValues: Ansys.Common.Interop.FEParsePlugin_ANSYS.IElementSurfaceLoadValues) -> None:
        """
        __init__ method.
        """
        pass


class CommandKeyOpt(object):
    """
    
            Represents a KEYOPT command.
            
    """

    @property
    def Knum(self) -> typing.Optional[int]:
        """
        
            Gets the key option number.
            
        """
        return None

    @property
    def Value(self) -> typing.Optional[int]:
        """
        
            Gets the value.
            
        """
        return None

    def __init__(self, iKeyOpt: Ansys.Common.Interop.FEParsePlugin_ANSYS.IKeyopt) -> None:
        """
        __init__ method.
        """
        pass


class CommandLayer(object):
    """
    
            Represents a layer associated to a shell SECBLOCK command.
            
    """

    @property
    def Thick(self) -> typing.Optional[float]:
        """
        
            Gets the thickness.
            
        """
        return None

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Theta(self) -> typing.Optional[float]:
        """
        
            Gets the layer orientation angle.
            
        """
        return None

    @property
    def Numpt(self) -> typing.Optional[int]:
        """
        
            Gets the number of integration points in the layer.
            
        """
        return None

    def __init__(self, iLayer: Ansys.Common.Interop.FEParsePlugin_ANSYS.ILayer) -> None:
        """
        __init__ method.
        """
        pass


class CommandNodalBodyForce(object):
    """
    
            Represents a nodal body force associated to a BFBLOCK command.
            
    """

    @property
    def Node(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def ValCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[typing.Any]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iNodalBodyForce: Ansys.Common.Interop.FEParsePlugin_ANSYS.INodalBodyForce) -> None:
        """
        __init__ method.
        """
        pass


class CommandNode(object):
    """
    
            Represents a node associated to a NBLOCK command.
            
    """

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the node number.
            
        """
        return None

    @property
    def Location(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the coordinates.
            
        """
        return None

    @property
    def Rotation(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the rotation angles.
            
        """
        return None

    def __init__(self, iNode: Ansys.Common.Interop.FEParsePlugin_ANSYS.INode) -> None:
        """
        __init__ method.
        """
        pass


class CommandReal(object):
    """
    
            Represent a real constant set associated to a RLBLOCK command.
            
    """

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the real constant set number.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iReal: Ansys.Common.Interop.FEParsePlugin_ANSYS.IReal) -> None:
        """
        __init__ method.
        """
        pass


class TBDataValues(object):
    """
    
            Represents data for a given temperature.
            
    """

    @property
    def Temp(self) -> typing.Optional[float]:
        """
        
            Gets the temperature.
            
        """
        return None

    @property
    def ValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, iTbDataValues: Ansys.Common.Interop.FEParsePlugin_ANSYS.ITBDataValues) -> None:
        """
        __init__ method.
        """
        pass


class TBDataCommand(object):
    """
    
            Represents a TBDATA command.
            
    """

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Ntemp(self) -> typing.Optional[int]:
        """
        
            Gets the number of temperature, if provided.
            
        """
        return None

    @property
    def Npts(self) -> typing.Optional[int]:
        """
        
            Gets the number of points, if provided.
            
        """
        return None

    @property
    def Tbopt(self) -> typing.Optional[str]:
        """
        
            Gets the option.
            
        """
        return None

    @property
    def DataValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of data values.
            
        """
        return None

    @property
    def DataValues(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.TBDataValues]]:
        """
        
            Gets the data values.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iTBDataCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.ITBDataCommand) -> None:
        """
        __init__ method.
        """
        pass


class TBPTValues(object):
    """
    
            Represents a tuple of values for the TBPT commmand.
            
    """

    @property
    def ValueCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[tuple[float]]:
        """
        
            Gets the values.
            
        """
        return None

    def __init__(self, _tbptValues: Ansys.Common.Interop.FEParsePlugin_ANSYS.ITBPTValues) -> None:
        """
        __init__ method.
        """
        pass


class TBPTData(object):
    """
    
            Represents data for the TBPT command.
            
    """

    @property
    def Temp(self) -> typing.Optional[float]:
        """
        
            Gets the temperature.
            
        """
        return None

    @property
    def TBPTCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of values.
            
        """
        return None

    @property
    def TBPTValues(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.TBPTValues]]:
        """
        
            Gets the TBPT values.
            
        """
        return None

    def __init__(self, iTbptData: Ansys.Common.Interop.FEParsePlugin_ANSYS.ITBPTData) -> None:
        """
        __init__ method.
        """
        pass


class TBPTCommand(object):
    """
    
            Represents a TBPT command.
            
    """

    @property
    def Lab(self) -> typing.Optional[str]:
        """
        
            Gets the label.
            
        """
        return None

    @property
    def Mat(self) -> typing.Optional[int]:
        """
        
            Gets the material number.
            
        """
        return None

    @property
    def Ntemp(self) -> typing.Optional[int]:
        """
        
            Gets the number of temperature, if provided.
            
        """
        return None

    @property
    def Npts(self) -> typing.Optional[int]:
        """
        
            Gets the number of points, if provided.
            
        """
        return None

    @property
    def Tbopt(self) -> typing.Optional[str]:
        """
        
            Gets the option.
            
        """
        return None

    @property
    def TBPTDataCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of TBPT data.
            
        """
        return None

    @property
    def TBPTData(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.TBPTData]]:
        """
        
            Gets TBPT data items.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iTBPTCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.ITBPTCommand) -> None:
        """
        __init__ method.
        """
        pass


class ETBlockCommand(object):
    """
    
            Represents a ETBLOCK command.
            
    """

    @property
    def ElementTypeCount(self) -> typing.Optional[int]:
        """
        
            Gets the element type count.
            
        """
        return None

    @property
    def ElementTypes(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandElementType]]:
        """
        
            Gets the element types.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iEtBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IETBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class FBlockCommand(object):
    """
    
            Represents a FBlock command.
            
    """

    @property
    def NodalLoadsCount(self) -> typing.Optional[int]:
        """
        
            Gets the element type count.
            
        """
        return None

    @property
    def NodalLoads(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandNodalLoad]]:
        """
        
            Gets the element types.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iFBlockCommand: Ansys.Common.Interop.FEParsePlugin_ANSYS.IFBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


class DBlockCommand(object):
    """
    
            Represents a DBlock command.
            
    """

    @property
    def NodalLoadsCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of element surface loads.
            
        """
        return None

    @property
    def NodalLoads(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.FE.CDB.CommandNodalLoad]]:
        """
        
            Get the element surface loads.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the command name.
            
        """
        return None

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets the command index.
            
        """
        return None

    def __init__(self, iDBlockCommandObj: Ansys.Common.Interop.FEParsePlugin_ANSYS.IDBlockCommand) -> None:
        """
        __init__ method.
        """
        pass


