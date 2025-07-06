"""Modalities"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.pid_names import BaseName


class ModalityModel(BaseName):
    """Base model for modality"""

    model_config = ConfigDict(frozen=True)
    name: str
    abbreviation: str


class _Behavior(ModalityModel):
    """Model behavior"""

    name: Literal["Behavior"] = "Behavior"
    abbreviation: Literal["behavior"] = "behavior"


class _Behavior_Videos(ModalityModel):
    """Model behavior-videos"""

    name: Literal["Behavior videos"] = "Behavior videos"
    abbreviation: Literal["behavior-videos"] = "behavior-videos"


class _Confocal(ModalityModel):
    """Model confocal"""

    name: Literal["Confocal microscopy"] = "Confocal microscopy"
    abbreviation: Literal["confocal"] = "confocal"


class _Emg(ModalityModel):
    """Model EMG"""

    name: Literal["Electromyography"] = "Electromyography"
    abbreviation: Literal["EMG"] = "EMG"


class _Ecephys(ModalityModel):
    """Model ecephys"""

    name: Literal["Extracellular electrophysiology"] = "Extracellular electrophysiology"
    abbreviation: Literal["ecephys"] = "ecephys"


class _Fib(ModalityModel):
    """Model fib"""

    name: Literal["Fiber photometry"] = "Fiber photometry"
    abbreviation: Literal["fib"] = "fib"


class _Fmost(ModalityModel):
    """Model fMOST"""

    name: Literal["Fluorescence micro-optical sectioning tomography"] = (
        "Fluorescence micro-optical sectioning tomography"
    )
    abbreviation: Literal["fMOST"] = "fMOST"


class _Icephys(ModalityModel):
    """Model icephys"""

    name: Literal["Intracellular electrophysiology"] = "Intracellular electrophysiology"
    abbreviation: Literal["icephys"] = "icephys"


class _Isi(ModalityModel):
    """Model ISI"""

    name: Literal["Intrinsic signal imaging"] = "Intrinsic signal imaging"
    abbreviation: Literal["ISI"] = "ISI"


class _Mri(ModalityModel):
    """Model MRI"""

    name: Literal["Magnetic resonance imaging"] = "Magnetic resonance imaging"
    abbreviation: Literal["MRI"] = "MRI"


class _Merfish(ModalityModel):
    """Model merfish"""

    name: Literal["Multiplexed error-robust fluorescence in situ hybridization"] = (
        "Multiplexed error-robust fluorescence in situ hybridization"
    )
    abbreviation: Literal["merfish"] = "merfish"


class _Pophys(ModalityModel):
    """Model pophys"""

    name: Literal["Planar optical physiology"] = "Planar optical physiology"
    abbreviation: Literal["pophys"] = "pophys"


class _Slap(ModalityModel):
    """Model slap"""

    name: Literal["Scanned line projection imaging"] = "Scanned line projection imaging"
    abbreviation: Literal["slap"] = "slap"


class _Spim(ModalityModel):
    """Model SPIM"""

    name: Literal["Selective plane illumination microscopy"] = "Selective plane illumination microscopy"
    abbreviation: Literal["SPIM"] = "SPIM"


class Modality:
    """Modalities"""

    BEHAVIOR = _Behavior()
    BEHAVIOR_VIDEOS = _Behavior_Videos()
    CONFOCAL = _Confocal()
    EMG = _Emg()
    ECEPHYS = _Ecephys()
    FIB = _Fib()
    FMOST = _Fmost()
    ICEPHYS = _Icephys()
    ISI = _Isi()
    MRI = _Mri()
    MERFISH = _Merfish()
    POPHYS = _Pophys()
    SLAP = _Slap()
    SPIM = _Spim()

    ALL = tuple(ModalityModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(ModalityModel.__subclasses__())], Field(discriminator="abbreviation")]

    abbreviation_map = {m().abbreviation: m() for m in ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get modality from abbreviation"""
        return cls.abbreviation_map.get(abbreviation, None)
