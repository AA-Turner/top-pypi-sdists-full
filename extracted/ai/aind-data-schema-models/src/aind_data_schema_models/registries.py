"""Registries"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.pid_names import BaseName


class RegistryModel(BaseName):
    """Base model for registries"""

    model_config = ConfigDict(frozen=True)
    name: str
    abbreviation: str


class _Addgene(RegistryModel):
    """Model ADDGENE"""

    name: Literal["Addgene"] = "Addgene"
    abbreviation: Literal["ADDGENE"] = "ADDGENE"


class _Emapa(RegistryModel):
    """Model EMAPA"""

    name: Literal["Edinburgh Mouse Atlas Project"] = "Edinburgh Mouse Atlas Project"
    abbreviation: Literal["EMAPA"] = "EMAPA"


class _Mgi(RegistryModel):
    """Model MGI"""

    name: Literal["Mouse Genome Informatics"] = "Mouse Genome Informatics"
    abbreviation: Literal["MGI"] = "MGI"


class _Ncbi(RegistryModel):
    """Model NCBI"""

    name: Literal["National Center for Biotechnology Information"] = "National Center for Biotechnology Information"
    abbreviation: Literal["NCBI"] = "NCBI"


class _Orcid(RegistryModel):
    """Model ORCID"""

    name: Literal["Open Researcher and Contributor ID"] = "Open Researcher and Contributor ID"
    abbreviation: Literal["ORCID"] = "ORCID"


class _Ror(RegistryModel):
    """Model ROR"""

    name: Literal["Research Organization Registry"] = "Research Organization Registry"
    abbreviation: Literal["ROR"] = "ROR"


class _Rrid(RegistryModel):
    """Model RRID"""

    name: Literal["Research Resource Identifiers"] = "Research Resource Identifiers"
    abbreviation: Literal["RRID"] = "RRID"


class _Uniprot(RegistryModel):
    """Model UNIPROT"""

    name: Literal["Universal Protein Resource"] = "Universal Protein Resource"
    abbreviation: Literal["UNIPROT"] = "UNIPROT"


class Registry:
    """Registries"""

    ADDGENE = _Addgene()
    EMAPA = _Emapa()
    MGI = _Mgi()
    NCBI = _Ncbi()
    ORCID = _Orcid()
    ROR = _Ror()
    RRID = _Rrid()
    UNIPROT = _Uniprot()

    ALL = tuple(RegistryModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(RegistryModel.__subclasses__())], Field(discriminator="abbreviation")]

    abbreviation_map = {m().abbreviation: m() for m in ALL}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get registry from abbreviation"""
        return cls.abbreviation_map.get(abbreviation, None)
