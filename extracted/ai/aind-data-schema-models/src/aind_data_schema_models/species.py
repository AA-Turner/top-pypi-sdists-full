"""Species"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.registries import Registry


class StrainModel(BaseModel):
    """Base model for a strain"""

    model_config = ConfigDict(frozen=True)
    name: str
    species: str
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _C57Bl_6J(StrainModel):
    """Model C57BL/6J"""

    name: Literal["C57BL/6J"] = "C57BL/6J"
    species: Literal["Mus musculus"] = "Mus musculus"
    registry: Optional[Registry] = Field(default=Registry.MGI)
    registry_identifier: Optional[str] = Field(default="MGI:3028467")


class _Balb_C(StrainModel):
    """Model BALB/c"""

    name: Literal["BALB/c"] = "BALB/c"
    species: Literal["Mus musculus"] = "Mus musculus"
    registry: Optional[Registry] = Field(default=Registry.MGI)
    registry_identifier: Optional[str] = Field(default="MGI:2159737")


class _Unknown(StrainModel):
    """Model Unknown"""

    name: Literal["Unknown"] = "Unknown"
    species: Literal["Mus musculus"] = "Mus musculus"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class Strain:
    """Strain"""

    C57BL_6J = _C57Bl_6J()

    BALB_C = _Balb_C()

    UNKNOWN = _Unknown()

    ALL = tuple(StrainModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(StrainModel.__subclasses__())], Field(discriminator="name")]


class SpeciesModel(BaseModel):
    """Base model for species"""

    model_config = ConfigDict(frozen=True)
    name: str
    common_name: str
    registry: Registry
    registry_identifier: str


class _Callithrix_Jacchus(SpeciesModel):
    """Model Callithrix jacchus"""

    name: Literal["Callithrix jacchus"] = "Callithrix jacchus"
    common_name: Literal["Common marmoset"] = "Common marmoset"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9483"] = "NCBI:txid9483"


class _Carpa_Hircus(SpeciesModel):
    """Model Carpa hircus"""

    name: Literal["Carpa hircus"] = "Carpa hircus"
    common_name: Literal["Goat"] = "Goat"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9925"] = "NCBI:txid9925"


class _Cavia_Porcellus(SpeciesModel):
    """Model Cavia porcellus"""

    name: Literal["Cavia porcellus"] = "Cavia porcellus"
    common_name: Literal["Guinea pig"] = "Guinea pig"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid10141"] = "NCBI:txid10141"


class _Equus_Asinus(SpeciesModel):
    """Model Equus asinus"""

    name: Literal["Equus asinus"] = "Equus asinus"
    common_name: Literal["Donkey"] = "Donkey"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9793"] = "NCBI:txid9793"


class _Gallus_Gallus(SpeciesModel):
    """Model Gallus gallus"""

    name: Literal["Gallus gallus"] = "Gallus gallus"
    common_name: Literal["Chicken"] = "Chicken"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9031"] = "NCBI:txid9031"


class _Homo_Sapiens(SpeciesModel):
    """Model Homo sapiens"""

    name: Literal["Homo sapiens"] = "Homo sapiens"
    common_name: Literal["Human"] = "Human"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9606"] = "NCBI:txid9606"


class _Lama_Glama(SpeciesModel):
    """Model Lama glama"""

    name: Literal["Lama glama"] = "Lama glama"
    common_name: Literal["Llama"] = "Llama"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9844"] = "NCBI:txid9844"


class _Macaca_Mulatta(SpeciesModel):
    """Model Macaca mulatta"""

    name: Literal["Macaca mulatta"] = "Macaca mulatta"
    common_name: Literal["Rhesus macaque"] = "Rhesus macaque"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9544"] = "NCBI:txid9544"


class _Mus_Musculus(SpeciesModel):
    """Model Mus musculus"""

    name: Literal["Mus musculus"] = "Mus musculus"
    common_name: Literal["House mouse"] = "House mouse"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid10090"] = "NCBI:txid10090"


class _Oryctolagus_Cuniculus(SpeciesModel):
    """Model Oryctolagus cuniculus"""

    name: Literal["Oryctolagus cuniculus"] = "Oryctolagus cuniculus"
    common_name: Literal["European rabbit"] = "European rabbit"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid9986"] = "NCBI:txid9986"


class _Rattus_Norvegicus(SpeciesModel):
    """Model Rattus norvegicus"""

    name: Literal["Rattus norvegicus"] = "Rattus norvegicus"
    common_name: Literal["Norway rat"] = "Norway rat"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid10116"] = "NCBI:txid10116"


class _Vicuna_Pacos(SpeciesModel):
    """Model Vicuna pacos"""

    name: Literal["Vicuna pacos"] = "Vicuna pacos"
    common_name: Literal["Alpaca"] = "Alpaca"
    registry: Registry = Registry.NCBI
    registry_identifier: Literal["NCBI:txid30538"] = "NCBI:txid30538"


class Species:
    """Species"""

    COMMON_MARMOSET = _Callithrix_Jacchus()
    GOAT = _Carpa_Hircus()
    GUINEA_PIG = _Cavia_Porcellus()
    DONKEY = _Equus_Asinus()
    CHICKEN = _Gallus_Gallus()
    HUMAN = _Homo_Sapiens()
    LLAMA = _Lama_Glama()
    RHESUS_MACAQUE = _Macaca_Mulatta()
    HOUSE_MOUSE = _Mus_Musculus()
    EUROPEAN_RABBIT = _Oryctolagus_Cuniculus()
    NORWAY_RAT = _Rattus_Norvegicus()
    ALPACA = _Vicuna_Pacos()

    ALL = tuple(SpeciesModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(SpeciesModel.__subclasses__())], Field(discriminator="name")]

    name_map = {m().name: m() for m in ALL}
    common_name_map = {m().common_name: m() for m in ALL}

    @classmethod
    def from_name(cls, name: str):
        """Get SpeciesModel from name"""
        return cls.name_map.get(name, None)

    @classmethod
    def from_common_name(cls, common_name: str):
        """Get SpeciesModel from common_name"""
        return cls.common_name_map.get(common_name, None)
