"""Device enums for data schema"""

from enum import Enum


class ImagingDeviceType(str, Enum):
    """Imaginge device type name"""

    BEAM_EXPANDER = "Beam expander"
    SAMPLE_CHAMBER = "Sample Chamber"
    DIFFUSER = "Diffuser"
    GALVO = "Galvo"
    LASER_COMBINER = "Laser combiner"
    LASER_COUPLER = "Laser coupler"
    PRISM = "Prism"
    OBJECTIVE = "Objective"
    ROTATION_MOUNT = "Rotation mount"
    SLIT = "Slit"
    SLM = "Spatial light modulator"
    TUNABLE_LENS = "Tunable lens"
    OTHER = "Other"


class StageAxisDirection(str, Enum):
    """Direction of motion for motorized stage"""

    DETECTION_AXIS = "Detection axis"
    ILLUMINATION_AXIS = "Illumination axis"
    PERPENDICULAR_AXIS = "Perpendicular axis"


class DeviceDriver(str, Enum):
    """DeviceDriver name"""

    OPENGL = "OpenGL"
    VIMBA = "Vimba"
    NVIDIA = "Nvidia Graphics"


class Coupling(str, Enum):
    """Laser coupling type"""

    FREE_SPACE = "Free-space"
    MMF = "Multi-mode fiber"
    SMF = "Single-mode fiber"
    OTHER = "Other"


class DataInterface(str, Enum):
    """Connection between a device and a PC"""

    CAMERALINK = "CameraLink"
    COAX = "Coax"
    ETH = "Ethernet"
    PCIE = "PCIe"
    PXI = "PXI"
    USB = "USB"
    OTHER = "Other"


class FilterType(str, Enum):
    """Filter type"""

    BANDPASS = "Band pass"
    DICHROIC = "Dichroic"
    LONGPASS = "Long pass"
    MULTIBAND = "Multiband"
    ND = "Neutral density"
    NOTCH = "Notch"
    MULTI_NOTCH = "Multi notch"
    SHORTPASS = "Short pass"


class CameraChroma(str, Enum):
    """Color vs. black & white"""

    COLOR = "Color"
    BW = "Monochrome"


class DaqChannelType(str, Enum):
    """DAQ Channel type"""

    AI = "Analog Input"
    AO = "Analog Output"
    DI = "Digital Input"
    DO = "Digital Output"


class ImmersionMedium(str, Enum):
    """Immersion medium name"""

    AIR = "air"
    MULTI = "multi"
    OIL = "oil"
    PBS = "PBS"
    WATER = "water"
    OTHER = "other"
    EASYINDEX = "easy index"
    ECI = "ethyl cinnimate"
    ACB = "aqueous clearing buffer"


class ObjectiveType(str, Enum):
    """Objective type for Slap2"""

    REMOTE = "Remote"
    PRIMARY = "Primary"


class CameraTarget(str, Enum):
    """Target of camera"""

    BODY = "Body"
    BRAIN = "Brain"
    EYE = "Eye"
    FACE = "Face"
    TONGUE = "Tongue"
    OTHER = "Other"


class ProbeModel(str, Enum):
    """Probe model name"""

    MI_ULED_PROBE = "Michigan uLED Probe (Version 1)"
    MP_PHOTONIC_V1 = "MPI Photonic Probe (Version 1)"
    NP_OPTO_DEMONSTRATOR = "Neuropixels Opto (Demonstrator)"
    NP_UHD_FIXED = "Neuropixels UHD (Fixed)"
    NP_UHD_SWITCHABLE = "Neuropixels UHD (Switchable)"
    NP1 = "Neuropixels 1.0"
    NP2_SINGLE_SHANK = "Neuropixels 2.0 (Single Shank)"
    NP2_MULTI_SHANK = "Neuropixels 2.0 (Multi Shank)"
    NP2_QUAD_BASE = "Neuropixels 2.0 (Quad Base)"
    CUSTOM = "Custom"


class DetectorType(str, Enum):
    """Detector type name"""

    CAMERA = "Camera"
    PMT = "Photomultiplier Tube"
    OTHER = "Other"


class Cooling(str, Enum):
    """Cooling medium name"""

    AIR = "Air"
    WATER = "Water"
    NO_COOLING = "No cooling"


class BinMode(str, Enum):
    """Detector binning mode"""

    ADDITIVE = "Additive"
    AVERAGE = "Average"
    NO_BINNING = "No binning"


class FerruleMaterial(str, Enum):
    """Fiber probe ferrule material type name"""

    CERAMIC = "Ceramic"
    STAINLESS_STEEL = "Stainless steel"


class LickSensorType(str, Enum):
    """Type of lick sensor"""

    CAPACITIVE = "Capacitive"
    CONDUCTIVE = "Conductive"
    PIEZOELECTIC = "Piezoelectric"


class MyomatrixArrayType(str, Enum):
    """Type of Myomatrix array"""

    INJECTED = "Injected"
    SUTURED = "Sutured"
