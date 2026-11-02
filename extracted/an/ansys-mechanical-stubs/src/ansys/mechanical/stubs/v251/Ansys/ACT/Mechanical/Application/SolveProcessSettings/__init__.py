"""SolveProcessSettings module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ILinuxSettings(object):

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        
            Gets or sets whether or not manual linux settings are enable for the configuration.
            
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets whether or not manual linux settings are enable for the configuration.
            
        """
        pass

    @property
    def UserName(self) -> typing.Optional[str]:
        """
        
            Gets or sets the user name field for the manual linux settings.
            
        """
        return None

    @UserName.setter
    def UserName(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the user name field for the manual linux settings.
            
        """
        pass

    @property
    def WorkingFolder(self) -> typing.Optional[str]:
        """
        
            Gets or sets the working folder field for the manual linxus settings.
            
        """
        return None

    @WorkingFolder.setter
    def WorkingFolder(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the working folder field for the manual linxus settings.
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ILinuxSettings) -> None:
        """
        CopyTo method.
        """
        pass


class IQueueSettings(object):

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the name of the current queue for the configuration.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the name of the current queue for the configuration.
            
        """
        pass

    @property
    def JobName(self) -> typing.Optional[str]:
        """
        
            Gets or sets the Job Name field for the queue settings.
            
        """
        return None

    @JobName.setter
    def JobName(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the Job Name field for the queue settings.
            
        """
        pass

    @property
    def License(self) -> typing.Optional[str]:
        """
        
            Gets or sets the License field for the queue settings.
            
        """
        return None

    @License.setter
    def License(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the License field for the queue settings.
            
        """
        pass

    @property
    def DCSUrl(self) -> typing.Optional[str]:
        """
        DCSUrl property.
        """
        return None

    @DCSUrl.setter
    def DCSUrl(self, value: typing.Optional[str]) -> None:
        """
        DCSUrl property.
        """
        pass

    @property
    def SolutionExecutionTarget(self) -> typing.Optional[str]:
        """
        SolutionExecutionTarget property.
        """
        return None

    @SolutionExecutionTarget.setter
    def SolutionExecutionTarget(self, value: typing.Optional[str]) -> None:
        """
        SolutionExecutionTarget property.
        """
        pass

    @property
    def DCSUsername(self) -> typing.Optional[str]:
        """
        DCSUsername property.
        """
        return None

    @DCSUsername.setter
    def DCSUsername(self, value: typing.Optional[str]) -> None:
        """
        DCSUsername property.
        """
        pass

    @property
    def DCSPassword(self) -> typing.Optional[str]:
        """
        DCSPassword property.
        """
        return None

    @DCSPassword.setter
    def DCSPassword(self, value: typing.Optional[str]) -> None:
        """
        DCSPassword property.
        """
        pass

    @property
    def CloudAccounts(self) -> typing.Optional[typing.List[str]]:
        """
        
            Gets the list of Cloud Accounts.
            
        """
        return None

    @property
    def SelectedCloudAccount(self) -> typing.Optional[str]:
        """
        
            Gets or sets the Cloud Account.
            
        """
        return None

    @SelectedCloudAccount.setter
    def SelectedCloudAccount(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the Cloud Account.
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.IQueueSettings) -> None:
        """
        CopyTo method.
        """
        pass


class ISolveConfiguration(object):

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the name of the SolveConfiguraiton Object
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the name of the SolveConfiguraiton Object
            
        """
        pass

    @property
    def Default(self) -> typing.Optional[bool]:
        """
        
            Gets whether or not this SolveConfiguration is the default configuration.
            
        """
        return None

    @property
    def Settings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.IQueueSettings]:
        """
        
            Gets the QueueSettings object for the configuration.
            
        """
        return None

    @property
    def SolveProcessSettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolveProcessSettings]:
        """
        
            Gets the SolveProcessSettings for the current object.
            
        """
        return None

    def SetAsDefault(self) -> None:
        """
        
            Sets 'this' to be the default configuration to solve with.
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolveConfiguration) -> None:
        """
        CopyTo method.
        """
        pass


class ISolveProcessSettings(object):

    @property
    def DistributeSolution(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the boolean "Distribute Solution (if possible)" field.
            
        """
        return None

    @DistributeSolution.setter
    def DistributeSolution(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the boolean "Distribute Solution (if possible)" field.
            
        """
        pass

    @property
    def MaxNumberOfCores(self) -> typing.Optional[int]:
        """
        
            Gets or sets the "Maximum number of utilized cores" field.
            
        """
        return None

    @MaxNumberOfCores.setter
    def MaxNumberOfCores(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the "Maximum number of utilized cores" field.
            
        """
        pass

    @property
    def NumberOfGPUDevices(self) -> typing.Optional[int]:
        """
        
            Gets or sets the "Number of utilized GPU devices" field.
            
        """
        return None

    @NumberOfGPUDevices.setter
    def NumberOfGPUDevices(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the "Number of utilized GPU devices" field.
            
        """
        pass

    @property
    def AdditionalCommandLineArguments(self) -> typing.Optional[str]:
        """
        
            Gets or sets the "Additional Command Line Arguments" field.
            
        """
        return None

    @AdditionalCommandLineArguments.setter
    def AdditionalCommandLineArguments(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the "Additional Command Line Arguments" field.
            
        """
        pass

    @property
    def CustomExecutablePath(self) -> typing.Optional[str]:
        """
        
            Gets or sets the "Custom Executable Name (with path)" field.
            
        """
        return None

    @CustomExecutablePath.setter
    def CustomExecutablePath(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the "Custom Executable Name (with path)" field.
            
        """
        pass

    @property
    def UserString(self) -> typing.Optional[str]:
        """
        
            Gets or sets the User String field.
            
        """
        return None

    @UserString.setter
    def UserString(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the User String field.
            
        """
        pass

    @property
    def LicenseQueuing(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the "License Queuing: Wait for Available License" field.
            
        """
        return None

    @LicenseQueuing.setter
    def LicenseQueuing(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the "License Queuing: Wait for Available License" field.
            
        """
        pass

    @property
    def UseSharedLicense(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the "Use Shared License, if possible" field.
            
        """
        return None

    @UseSharedLicense.setter
    def UseSharedLicense(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the "Use Shared License, if possible" field.
            
        """
        pass

    @property
    def SolveInSynchronousMode(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the "Solve in synchronous mode" field.
            
        """
        return None

    @SolveInSynchronousMode.setter
    def SolveInSynchronousMode(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the "Solve in synchronous mode" field.
            
        """
        pass

    @property
    def ManualSolverMemorySettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolverMemorySettings]:
        """
        
            Gets the SolverMemorySettings object for the configuration.
            
        """
        return None

    @property
    def ManualLinuxSettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.ILinuxSettings]:
        """
        
            Gets the LinuxSettings object for the configuration.
            
        """
        return None

    @property
    def HPSCloudBurstComputeRequirements(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.IHPSCloudBurstHPCRequirements]:
        """
        
            Gets the HPC requirements object for HPS and Cloud Burst.
            
        """
        return None

    @property
    def GPUAccelerationDevice(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GPUAccelerationDevicesType]:
        """
        
            Gets or sets the "GPU Acceleration Device" field.
            
        """
        return None

    @GPUAccelerationDevice.setter
    def GPUAccelerationDevice(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GPUAccelerationDevicesType]) -> None:
        """
        
            Gets or sets the "GPU Acceleration Device" field.
            
        """
        pass

    @property
    def HybridParallel(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the boolean "Hybrid Parallel (Mechanical APDL)" field.
            
        """
        return None

    @HybridParallel.setter
    def HybridParallel(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the boolean "Hybrid Parallel (Mechanical APDL)" field.
            
        """
        pass

    @property
    def ThreadsPerProcess(self) -> typing.Optional[int]:
        """
        
            Gets or sets the "Threads per process" field.
            
        """
        return None

    @ThreadsPerProcess.setter
    def ThreadsPerProcess(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the "Threads per process" field.
            
        """
        pass

    @property
    def NumberOfProcesses(self) -> typing.Optional[int]:
        """
        
            Gets or sets the "Number of processes" field.
            
        """
        return None

    @property
    def DCSAutoDownloadResults(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the "DCS Auto Download Results" field.
            
        """
        return None

    @DCSAutoDownloadResults.setter
    def DCSAutoDownloadResults(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the "DCS Auto Download Results" field.
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolveProcessSettings) -> None:
        """
        CopyTo method.
        """
        pass


class ISolverMemorySettings(object):

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        
            Gets or sets whether or not manual memory settings are active in the current configuration.
            
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets whether or not manual memory settings are active in the current configuration.
            
        """
        pass

    @property
    def Workspace(self) -> typing.Optional[int]:
        """
        
            Gets or sets the workspace memory amount (megabytes).
            
        """
        return None

    @Workspace.setter
    def Workspace(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the workspace memory amount (megabytes).
            
        """
        pass

    @property
    def Database(self) -> typing.Optional[int]:
        """
        
            Gets or sets the database memory amount (MB).
            
        """
        return None

    @Database.setter
    def Database(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the database memory amount (MB).
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolverMemorySettings) -> None:
        """
        CopyTo method.
        """
        pass


class SolveConfigurations(object):
    """
    
            The application's collection of solve configurations.
            
    """

    @property
    def DefaultConfiguration(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration]:
        """
        
            Returns the default solve configuration.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            The number of solve configurations in the collection.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        IsReadOnly property.
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def Add(self, item: Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration) -> None:
        """
        
            Adds the given SolveConfiguration object to the collection.
            
        """
        pass

    def Clear(self) -> None:
        """
        
            Clears the collection of all non-defualt SolveConfiguration objects.
            
        """
        pass

    def Contains(self, item: Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration) -> bool:
        """
        
            Returns true if the given SolveConfiguration belongs to the collection.
            
        """
        pass

    def CopyTo(self, array: Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration, arrayIndex: int) -> None:
        """
        CopyTo method.
        """
        pass

    def GetEnumerator(self) -> Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfigurationEnumerator:
        """
        GetEnumerator method.
        """
        pass

    def Remove(self, item: Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration) -> bool:
        """
        
            Removes the given SolveConfiguration from the collection.
            
        """
        pass


class LinuxSettings(object):
    """
    
            The class representing the linux settings portion of the solve process settings.
            
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        
             Whether the linux settings are active.
            
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        
             Whether the linux settings are active.
            
        """
        pass

    @property
    def UserName(self) -> typing.Optional[str]:
        """
        
            The user name.
            
        """
        return None

    @UserName.setter
    def UserName(self, value: typing.Optional[str]) -> None:
        """
        
            The user name.
            
        """
        pass

    @property
    def WorkingFolder(self) -> typing.Optional[str]:
        """
        
            The working folder.
            
        """
        return None

    @WorkingFolder.setter
    def WorkingFolder(self, value: typing.Optional[str]) -> None:
        """
        
            The working folder.
            
        """
        pass

    def __init__(self) -> None:
        """
        
             Creates a LinuxSettings object
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ILinuxSettings) -> None:
        """
        CopyTo method.
        """
        pass


class QueueSettings(object):
    """
    
            The class representing queue settings.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the queue settings.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the queue settings.
            
        """
        pass

    @property
    def JobName(self) -> typing.Optional[str]:
        """
        
            The job name of the queue settings.
            
        """
        return None

    @JobName.setter
    def JobName(self, value: typing.Optional[str]) -> None:
        """
        
            The job name of the queue settings.
            
        """
        pass

    @property
    def Licenses(self) -> typing.Optional[typing.Iterable[str]]:
        """
        Licenses property.
        """
        return None

    @property
    def License(self) -> typing.Optional[str]:
        """
        
            The license of the queue settings.  The setter will throw an exception if the given license is not valid.
            
        """
        return None

    @License.setter
    def License(self, value: typing.Optional[str]) -> None:
        """
        
            The license of the queue settings.  The setter will throw an exception if the given license is not valid.
            
        """
        pass

    @property
    def DCSUrl(self) -> typing.Optional[str]:
        """
        DCSUrl property.
        """
        return None

    @DCSUrl.setter
    def DCSUrl(self, value: typing.Optional[str]) -> None:
        """
        DCSUrl property.
        """
        pass

    @property
    def SolutionExecutionTarget(self) -> typing.Optional[str]:
        """
        SolutionExecutionTarget property.
        """
        return None

    @SolutionExecutionTarget.setter
    def SolutionExecutionTarget(self, value: typing.Optional[str]) -> None:
        """
        SolutionExecutionTarget property.
        """
        pass

    @property
    def DCSUsername(self) -> typing.Optional[str]:
        """
        DCSUsername property.
        """
        return None

    @DCSUsername.setter
    def DCSUsername(self, value: typing.Optional[str]) -> None:
        """
        DCSUsername property.
        """
        pass

    @property
    def DCSPassword(self) -> typing.Optional[str]:
        """
        DCSPassword property.
        """
        return None

    @DCSPassword.setter
    def DCSPassword(self, value: typing.Optional[str]) -> None:
        """
        DCSPassword property.
        """
        pass

    @property
    def CloudAccounts(self) -> typing.Optional[typing.List[str]]:
        """
        CloudAccounts property.
        """
        return None

    @property
    def SelectedCloudAccount(self) -> typing.Optional[str]:
        """
        SelectedCloudAccount property.
        """
        return None

    @SelectedCloudAccount.setter
    def SelectedCloudAccount(self, value: typing.Optional[str]) -> None:
        """
        SelectedCloudAccount property.
        """
        pass

    def __init__(self) -> None:
        """
        
             Creates a QueueSettings object
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.IQueueSettings) -> None:
        """
        CopyTo method.
        """
        pass


class RSMQueue(object):
    """
    
            The class representing an RSM Queue.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the RSM Queue.
            
        """
        return None

    @property
    def HPCConfiguration(self) -> typing.Optional[str]:
        """
        
            The HPC configuration of the RSM Queue.
            
        """
        return None

    @property
    def HPCQueue(self) -> typing.Optional[str]:
        """
        
            The HPC Queue of the RSM Queue.
            
        """
        return None

    @property
    def HPCType(self) -> typing.Optional[str]:
        """
        
            The HPC type of the RSM Queue
            
        """
        return None


class SolveConfiguration(object):
    """
    
            The class representing a solve configuration.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            The name of the solve configuration.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            The name of the solve configuration.
            
        """
        pass

    @property
    def Default(self) -> typing.Optional[bool]:
        """
        
            Whether this solve configuration is the default.
            
        """
        return None

    @property
    def Settings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.QueueSettings]:
        """
        
            Returns the queue settings of this solve configuration.
            
        """
        return None

    @property
    def SolveProcessSettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveProcessSettings]:
        """
        
            Returns the solve process settings of this solve configuration.
            
        """
        return None

    @typing.overload
    def __init__(self, name: str) -> None:
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        
             Creates a SolveConfiguration object with a given name or
             gets the instance of an existing SolveConfiguration with that name.
            
        """
        pass

    def SetAsDefault(self) -> None:
        """
        
            Sets this solve configuration as the default.
            
        """
        pass

    def Equals(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolveConfiguration) -> bool:
        """
        Equals method.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolveConfiguration) -> None:
        """
        CopyTo method.
        """
        pass


class SolverMemorySettings(object):
    """
    
            The class representing the solver memory settings portion of the solve process settings.
            
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        
             Whether the solver memory settings are active.
            
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        
             Whether the solver memory settings are active.
            
        """
        pass

    @property
    def Workspace(self) -> typing.Optional[int]:
        """
        
             Workspace size.
            
        """
        return None

    @Workspace.setter
    def Workspace(self, value: typing.Optional[int]) -> None:
        """
        
             Workspace size.
            
        """
        pass

    @property
    def Database(self) -> typing.Optional[int]:
        """
        
             Database size.
            
        """
        return None

    @Database.setter
    def Database(self, value: typing.Optional[int]) -> None:
        """
        
             Database size.
            
        """
        pass

    def __init__(self) -> None:
        """
        
             Creates a SolverMemorySettings object
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolverMemorySettings) -> None:
        """
        CopyTo method.
        """
        pass


class SolveProcessSettings(object):
    """
    
            The class representing solve process settings.
            
    """

    @property
    def DistributeSolution(self) -> typing.Optional[bool]:
        """
        
            Whether to run the solution in distributed mode.
            
        """
        return None

    @DistributeSolution.setter
    def DistributeSolution(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether to run the solution in distributed mode.
            
        """
        pass

    @property
    def MaxNumberOfCores(self) -> typing.Optional[int]:
        """
        
            The maximum number of cores the solver will use.
            
        """
        return None

    @MaxNumberOfCores.setter
    def MaxNumberOfCores(self, value: typing.Optional[int]) -> None:
        """
        
            The maximum number of cores the solver will use.
            
        """
        pass

    @property
    def NumberOfGPUDevices(self) -> typing.Optional[int]:
        """
        
            The number of GPU devices.
            
        """
        return None

    @NumberOfGPUDevices.setter
    def NumberOfGPUDevices(self, value: typing.Optional[int]) -> None:
        """
        
            The number of GPU devices.
            
        """
        pass

    @property
    def AdditionalCommandLineArguments(self) -> typing.Optional[str]:
        """
        
            Any additional command line arguments to give to the solver.
            
        """
        return None

    @AdditionalCommandLineArguments.setter
    def AdditionalCommandLineArguments(self, value: typing.Optional[str]) -> None:
        """
        
            Any additional command line arguments to give to the solver.
            
        """
        pass

    @property
    def CustomExecutablePath(self) -> typing.Optional[str]:
        """
        
            The custom executable path for user programmable features in the solver.
            
        """
        return None

    @CustomExecutablePath.setter
    def CustomExecutablePath(self, value: typing.Optional[str]) -> None:
        """
        
            The custom executable path for user programmable features in the solver.
            
        """
        pass

    @property
    def UserString(self) -> typing.Optional[str]:
        """
        UserString property.
        """
        return None

    @UserString.setter
    def UserString(self, value: typing.Optional[str]) -> None:
        """
        UserString property.
        """
        pass

    @property
    def LicenseQueuing(self) -> typing.Optional[bool]:
        """
        
            Whether license queueing is active.
            
        """
        return None

    @LicenseQueuing.setter
    def LicenseQueuing(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether license queueing is active.
            
        """
        pass

    @property
    def UseSharedLicense(self) -> typing.Optional[bool]:
        """
        
            Whether the solver will use a shared license.
            
        """
        return None

    @UseSharedLicense.setter
    def UseSharedLicense(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether the solver will use a shared license.
            
        """
        pass

    @property
    def SolveInSynchronousMode(self) -> typing.Optional[bool]:
        """
        
            Whether the solve will be in synchronous mode.
            
        """
        return None

    @SolveInSynchronousMode.setter
    def SolveInSynchronousMode(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether the solve will be in synchronous mode.
            
        """
        pass

    @property
    def ManualSolverMemorySettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.SolverMemorySettings]:
        """
        
            Returns the manual solver memory settings.
            
        """
        return None

    @property
    def ManualLinuxSettings(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.LinuxSettings]:
        """
        
            Returns the manual linux settings.
            
        """
        return None

    @property
    def HPSCloudBurstComputeRequirements(self) -> typing.Optional[Ansys.ACT.Mechanical.Application.SolveProcessSettings.HPSCloudBurstHPCRequirements]:
        """
        HPSCloudBurstComputeRequirements property.
        """
        return None

    @property
    def GPUAccelerationDevice(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GPUAccelerationDevicesType]:
        """
        
            The GPU Acceleration device the solver will use.
            
        """
        return None

    @GPUAccelerationDevice.setter
    def GPUAccelerationDevice(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GPUAccelerationDevicesType]) -> None:
        """
        
            The GPU Acceleration device the solver will use.
            
        """
        pass

    @property
    def HybridParallel(self) -> typing.Optional[bool]:
        """
        
            Whether to run the solution in hybrid parallel.
            
        """
        return None

    @HybridParallel.setter
    def HybridParallel(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether to run the solution in hybrid parallel.
            
        """
        pass

    @property
    def ThreadsPerProcess(self) -> typing.Optional[int]:
        """
        
            The threads per process the solver will use.
            
        """
        return None

    @ThreadsPerProcess.setter
    def ThreadsPerProcess(self, value: typing.Optional[int]) -> None:
        """
        
            The threads per process the solver will use.
            
        """
        pass

    @property
    def NumberOfProcesses(self) -> typing.Optional[int]:
        """
        
            The number of processes the solver will use.
            
        """
        return None

    @property
    def DCSAutoDownloadResults(self) -> typing.Optional[bool]:
        """
        
            Whether results need to be automatically downloaded for DCS job after completion.
            
        """
        return None

    @DCSAutoDownloadResults.setter
    def DCSAutoDownloadResults(self, value: typing.Optional[bool]) -> None:
        """
        
            Whether results need to be automatically downloaded for DCS job after completion.
            
        """
        pass

    def __init__(self) -> None:
        """
        
             Creates a SolveProcessSettings object
            
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Mechanical.Application.SolveProcessSettings.ISolveProcessSettings) -> None:
        """
        CopyTo method.
        """
        pass


