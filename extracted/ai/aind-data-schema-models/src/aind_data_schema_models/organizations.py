"""Organizations"""

from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from aind_data_schema_models.registries import Registry
from aind_data_schema_models.utils import one_of_instance


class OrganizationModel(BaseModel):
    """Base model for organizations"""

    model_config = ConfigDict(frozen=True)
    name: str
    abbreviation: str
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Aa_Opto_Electronic(OrganizationModel):
    """Model AA Opto Electronic"""

    name: Literal["AA Opto Electronic"] = "AA Opto Electronic"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Asus(OrganizationModel):
    """Model ASUS"""

    name: Literal["ASUS"] = "ASUS"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00bxkz165")


class _Abcam(OrganizationModel):
    """Model Abcam"""

    name: Literal["Abcam"] = "Abcam"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02e1wjw63")


class _Addgene(OrganizationModel):
    """Model Addgene"""

    name: Literal["Addgene"] = "Addgene"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01nn1pw54")


class _Ailipu_Technology_Co(OrganizationModel):
    """Model Ailipu Technology Co"""

    name: Literal["Ailipu Technology Co"] = "Ailipu Technology Co"
    abbreviation: Literal["Ailipu"] = "Ailipu"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Allen_Institute(OrganizationModel):
    """Model Allen Institute"""

    name: Literal["Allen Institute"] = "Allen Institute"
    abbreviation: Literal["AI"] = "AI"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03cpe7c52")


class _Allen_Institute_For_Brain_Science(OrganizationModel):
    """Model Allen Institute for Brain Science"""

    name: Literal["Allen Institute for Brain Science"] = "Allen Institute for Brain Science"
    abbreviation: Literal["AIBS"] = "AIBS"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00dcv1019")


class _Allen_Institute_For_Neural_Dynamics(OrganizationModel):
    """Model Allen Institute for Neural Dynamics"""

    name: Literal["Allen Institute for Neural Dynamics"] = "Allen Institute for Neural Dynamics"
    abbreviation: Literal["AIND"] = "AIND"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="04szwah67")


class _Allied(OrganizationModel):
    """Model Allied"""

    name: Literal["Allied"] = "Allied"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Applied_Scientific_Instrumentation(OrganizationModel):
    """Model Applied Scientific Instrumentation"""

    name: Literal["Applied Scientific Instrumentation"] = "Applied Scientific Instrumentation"
    abbreviation: Literal["ASI"] = "ASI"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Arecont_Vision_Costar(OrganizationModel):
    """Model Arecont Vision Costar"""

    name: Literal["Arecont Vision Costar"] = "Arecont Vision Costar"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Basler(OrganizationModel):
    """Model Basler"""

    name: Literal["Basler"] = "Basler"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Baylor_College_Of_Medicine(OrganizationModel):
    """Model Baylor College of Medicine"""

    name: Literal["Baylor College of Medicine"] = "Baylor College of Medicine"
    abbreviation: Literal["BCM"] = "BCM"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02pttbw34")


class _Boston_University(OrganizationModel):
    """Model Boston University"""

    name: Literal["Boston University"] = "Boston University"
    abbreviation: Literal["BU"] = "BU"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="05qwgg493")


class _Cajal_Neuroscience(OrganizationModel):
    """Model Cajal Neuroscience"""

    name: Literal["Cajal Neuroscience"] = "Cajal Neuroscience"
    abbreviation: Literal["Cajal"] = "Cajal"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="05pdc0q70")


class _Cambridge_Technology(OrganizationModel):
    """Model Cambridge Technology"""

    name: Literal["Cambridge Technology"] = "Cambridge Technology"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Carl_Zeiss(OrganizationModel):
    """Model Carl Zeiss"""

    name: Literal["Carl Zeiss"] = "Carl Zeiss"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01xk5xs43")


class _Champalimaud_Foundation(OrganizationModel):
    """Model Champalimaud Foundation"""

    name: Literal["Champalimaud Foundation"] = "Champalimaud Foundation"
    abbreviation: Literal["Champalimaud"] = "Champalimaud"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03g001n57")


class _Chan_Zuckerberg_Initiative(OrganizationModel):
    """Model Chan Zuckerberg Initiative"""

    name: Literal["Chan Zuckerberg Initiative"] = "Chan Zuckerberg Initiative"
    abbreviation: Literal["CZI"] = "CZI"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02qenvm24")


class _Charles_River_Laboratories(OrganizationModel):
    """Model Charles River Laboratories"""

    name: Literal["Charles River Laboratories"] = "Charles River Laboratories"
    abbreviation: Literal["CRL"] = "CRL"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03ndmsg87")


class _Chroma(OrganizationModel):
    """Model Chroma"""

    name: Literal["Chroma"] = "Chroma"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Coherent_Scientific(OrganizationModel):
    """Model Coherent Scientific"""

    name: Literal["Coherent Scientific"] = "Coherent Scientific"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="031tysd23")


class _Columbia_University(OrganizationModel):
    """Model Columbia University"""

    name: Literal["Columbia University"] = "Columbia University"
    abbreviation: Literal["Columbia"] = "Columbia"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00hj8s172")


class _Computar(OrganizationModel):
    """Model Computar"""

    name: Literal["Computar"] = "Computar"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Conoptics(OrganizationModel):
    """Model Conoptics"""

    name: Literal["Conoptics"] = "Conoptics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Custom(OrganizationModel):
    """Model Custom"""

    name: Literal["Custom"] = "Custom"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Digikey(OrganizationModel):
    """Model DigiKey"""

    name: Literal["DigiKey"] = "DigiKey"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Dodotronic(OrganizationModel):
    """Model Dodotronic"""

    name: Literal["Dodotronic"] = "Dodotronic"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Doric(OrganizationModel):
    """Model Doric"""

    name: Literal["Doric"] = "Doric"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="059n53q30")


class _Ealing(OrganizationModel):
    """Model Ealing"""

    name: Literal["Ealing"] = "Ealing"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Edmund_Optics(OrganizationModel):
    """Model Edmund Optics"""

    name: Literal["Edmund Optics"] = "Edmund Optics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01j1gwp17")


class _Emory_University(OrganizationModel):
    """Model Emory University"""

    name: Literal["Emory University"] = "Emory University"
    abbreviation: Literal["Emory"] = "Emory"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03czfpz43")


class _Euresys(OrganizationModel):
    """Model Euresys"""

    name: Literal["Euresys"] = "Euresys"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Fujinon(OrganizationModel):
    """Model Fujinon"""

    name: Literal["Fujinon"] = "Fujinon"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Hamamatsu(OrganizationModel):
    """Model Hamamatsu"""

    name: Literal["Hamamatsu"] = "Hamamatsu"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03natb733")


class _Hamilton(OrganizationModel):
    """Model Hamilton"""

    name: Literal["Hamilton"] = "Hamilton"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Huazhong_University_Of_Science_And_Technology(OrganizationModel):
    """Model Huazhong University of Science and Technology"""

    name: Literal["Huazhong University of Science and Technology"] = "Huazhong University of Science and Technology"
    abbreviation: Literal["HUST"] = "HUST"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00p991c53")


class _Ir_Robot_Co(OrganizationModel):
    """Model IR Robot Co"""

    name: Literal["IR Robot Co"] = "IR Robot Co"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Isl_Products_International(OrganizationModel):
    """Model ISL Products International"""

    name: Literal["ISL Products International"] = "ISL Products International"
    abbreviation: Literal["ISL"] = "ISL"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Infinity_Photo_Optical(OrganizationModel):
    """Model Infinity Photo-Optical"""

    name: Literal["Infinity Photo-Optical"] = "Infinity Photo-Optical"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Integrated_Dna_Technologies(OrganizationModel):
    """Model Integrated DNA Technologies"""

    name: Literal["Integrated DNA Technologies"] = "Integrated DNA Technologies"
    abbreviation: Literal["IDT"] = "IDT"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="009jvpf03")


class _Interuniversity_Microelectronics_Center(OrganizationModel):
    """Model Interuniversity Microelectronics Center"""

    name: Literal["Interuniversity Microelectronics Center"] = "Interuniversity Microelectronics Center"
    abbreviation: Literal["IMEC"] = "IMEC"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02kcbn207")


class _Invitrogen(OrganizationModel):
    """Model Invitrogen"""

    name: Literal["Invitrogen"] = "Invitrogen"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03x1ewr52")


class _Item(OrganizationModel):
    """Model Item"""

    name: Literal["Item"] = "Item"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Jackson_Laboratory(OrganizationModel):
    """Model Jackson Laboratory"""

    name: Literal["Jackson Laboratory"] = "Jackson Laboratory"
    abbreviation: Literal["JAX"] = "JAX"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="021sy4w91")


class _Janelia_Research_Campus(OrganizationModel):
    """Model Janelia Research Campus"""

    name: Literal["Janelia Research Campus"] = "Janelia Research Campus"
    abbreviation: Literal["Janelia"] = "Janelia"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="013sk6x84")


class _Jenoptik(OrganizationModel):
    """Model Jenoptik"""

    name: Literal["Jenoptik"] = "Jenoptik"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="05g7t5c49")


class _Johns_Hopkins_University(OrganizationModel):
    """Model Johns Hopkins University"""

    name: Literal["Johns Hopkins University"] = "Johns Hopkins University"
    abbreviation: Literal["JHU"] = "JHU"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00za53h95")


class _Julabo(OrganizationModel):
    """Model Julabo"""

    name: Literal["Julabo"] = "Julabo"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Kowa(OrganizationModel):
    """Model Kowa"""

    name: Literal["Kowa"] = "Kowa"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03zbwg482")


class _Lasos_Lasertechnik(OrganizationModel):
    """Model LASOS Lasertechnik"""

    name: Literal["LASOS Lasertechnik"] = "LASOS Lasertechnik"
    abbreviation: Literal["LASOS"] = "LASOS"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Lg(OrganizationModel):
    """Model LG"""

    name: Literal["LG"] = "LG"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02b948n83")


class _Leica(OrganizationModel):
    """Model Leica"""

    name: Literal["Leica"] = "Leica"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Lifecanvas(OrganizationModel):
    """Model LifeCanvas"""

    name: Literal["LifeCanvas"] = "LifeCanvas"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Lumen_Dynamics(OrganizationModel):
    """Model Lumen Dynamics"""

    name: Literal["Lumen Dynamics"] = "Lumen Dynamics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Mbf_Bioscience(OrganizationModel):
    """Model MBF Bioscience"""

    name: Literal["MBF Bioscience"] = "MBF Bioscience"
    abbreviation: Literal["MBF"] = "MBF"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02zynam48")


class _Mit_Department_Of_Brain_And_Cognitive_Sciences(OrganizationModel):
    """Model MIT Department of Brain and Cognitive Sciences"""

    name: Literal["MIT Department of Brain and Cognitive Sciences"] = "MIT Department of Brain and Cognitive Sciences"
    abbreviation: Literal["MIT-BCS"] = "MIT-BCS"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Mks_Newport(OrganizationModel):
    """Model MKS Newport"""

    name: Literal["MKS Newport"] = "MKS Newport"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00k17f049")


class _Mpi(OrganizationModel):
    """Model MPI"""

    name: Literal["MPI"] = "MPI"
    abbreviation: Literal["MPI"] = "MPI"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Massachusetts_Institute_Of_Technology(OrganizationModel):
    """Model Massachusetts Institute of Technology"""

    name: Literal["Massachusetts Institute of Technology"] = "Massachusetts Institute of Technology"
    abbreviation: Literal["MIT"] = "MIT"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="042nb2s44")


class _Mcgovern_Institute_For_Brain_Research(OrganizationModel):
    """Model McGovern Institute for Brain Research"""

    name: Literal["McGovern Institute for Brain Research"] = "McGovern Institute for Brain Research"
    abbreviation: Literal["MIBR"] = "MIBR"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="05ymca674")


class _Meadowlark_Optics(OrganizationModel):
    """Model Meadowlark Optics"""

    name: Literal["Meadowlark Optics"] = "Meadowlark Optics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00n8qbq54")


class _Michael_J_Fox_Foundation_For_Parkinson_S_Research(OrganizationModel):
    """Model Michael J. Fox Foundation for Parkinson's Research"""

    name: Literal["Michael J. Fox Foundation for Parkinson's Research"] = (
        "Michael J. Fox Foundation for Parkinson's Research"
    )
    abbreviation: Literal["MJFF"] = "MJFF"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03arq3225")


class _Midwest_Optical_Systems_Inc_(OrganizationModel):
    """Model Midwest Optical Systems, Inc."""

    name: Literal["Midwest Optical Systems, Inc."] = "Midwest Optical Systems, Inc."
    abbreviation: Literal["MidOpt"] = "MidOpt"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Mitutuyo(OrganizationModel):
    """Model Mitutuyo"""

    name: Literal["Mitutuyo"] = "Mitutuyo"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Nresearch_Inc(OrganizationModel):
    """Model NResearch Inc"""

    name: Literal["NResearch Inc"] = "NResearch Inc"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _National_Center_For_Complementary_And_Integrative_Health(OrganizationModel):
    """Model National Center for Complementary and Integrative Health"""

    name: Literal["National Center for Complementary and Integrative Health"] = (
        "National Center for Complementary and Integrative Health"
    )
    abbreviation: Literal["NCCIH"] = "NCCIH"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00190t495")


class _National_Institute_Of_Mental_Health(OrganizationModel):
    """Model National Institute of Mental Health"""

    name: Literal["National Institute of Mental Health"] = "National Institute of Mental Health"
    abbreviation: Literal["NIMH"] = "NIMH"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="04xeg9z08")


class _National_Institute_Of_Neurological_Disorders_And_Stroke(OrganizationModel):
    """Model National Institute of Neurological Disorders and Stroke"""

    name: Literal["National Institute of Neurological Disorders and Stroke"] = (
        "National Institute of Neurological Disorders and Stroke"
    )
    abbreviation: Literal["NINDS"] = "NINDS"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01s5ya894")


class _National_Instruments(OrganizationModel):
    """Model National Instruments"""

    name: Literal["National Instruments"] = "National Instruments"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="026exqw73")


class _Navitar(OrganizationModel):
    """Model Navitar"""

    name: Literal["Navitar"] = "Navitar"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Neuralynx(OrganizationModel):
    """Model NeuraLynx"""

    name: Literal["NeuraLynx"] = "NeuraLynx"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Neurophotometrics(OrganizationModel):
    """Model Neurophotometrics"""

    name: Literal["Neurophotometrics"] = "Neurophotometrics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _New_Scale_Technologies(OrganizationModel):
    """Model New Scale Technologies"""

    name: Literal["New Scale Technologies"] = "New Scale Technologies"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _New_York_University(OrganizationModel):
    """Model New York University"""

    name: Literal["New York University"] = "New York University"
    abbreviation: Literal["NYU"] = "NYU"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="0190ak572")


class _Nikon(OrganizationModel):
    """Model Nikon"""

    name: Literal["Nikon"] = "Nikon"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="0280y9h11")


class _Olympus(OrganizationModel):
    """Model Olympus"""

    name: Literal["Olympus"] = "Olympus"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02vcdte90")


class _Open_Ephys_Production_Site(OrganizationModel):
    """Model Open Ephys Production Site"""

    name: Literal["Open Ephys Production Site"] = "Open Ephys Production Site"
    abbreviation: Literal["OEPS"] = "OEPS"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="007rkz355")


class _Optotune(OrganizationModel):
    """Model Optotune"""

    name: Literal["Optotune"] = "Optotune"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Other(OrganizationModel):
    """Model Other"""

    name: Literal["Other"] = "Other"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Oxxius(OrganizationModel):
    """Model Oxxius"""

    name: Literal["Oxxius"] = "Oxxius"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Placid_Industries(OrganizationModel):
    """Model Placid Industries"""

    name: Literal["Placid Industries"] = "Placid Industries"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Prizmatix(OrganizationModel):
    """Model Prizmatix"""

    name: Literal["Prizmatix"] = "Prizmatix"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Quantifi(OrganizationModel):
    """Model Quantifi"""

    name: Literal["Quantifi"] = "Quantifi"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Raspberry_Pi(OrganizationModel):
    """Model Raspberry Pi"""

    name: Literal["Raspberry Pi"] = "Raspberry Pi"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Sicgen(OrganizationModel):
    """Model SICGEN"""

    name: Literal["SICGEN"] = "SICGEN"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Same_Sky(OrganizationModel):
    """Model Same Sky"""

    name: Literal["Same Sky"] = "Same Sky"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Schneider_Kreuznach(OrganizationModel):
    """Model Schneider-Kreuznach"""

    name: Literal["Schneider-Kreuznach"] = "Schneider-Kreuznach"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Second_Order_Effects(OrganizationModel):
    """Model Second Order Effects"""

    name: Literal["Second Order Effects"] = "Second Order Effects"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Semrock(OrganizationModel):
    """Model Semrock"""

    name: Literal["Semrock"] = "Semrock"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Sigma_Aldrich(OrganizationModel):
    """Model Sigma-Aldrich"""

    name: Literal["Sigma-Aldrich"] = "Sigma-Aldrich"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Simons_Foundation(OrganizationModel):
    """Model Simons Foundation"""

    name: Literal["Simons Foundation"] = "Simons Foundation"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01cmst727")


class _Spectra_Physics(OrganizationModel):
    """Model Spectra-Physics"""

    name: Literal["Spectra-Physics"] = "Spectra-Physics"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="02ad9kp97")


class _Spinnaker(OrganizationModel):
    """Model Spinnaker"""

    name: Literal["Spinnaker"] = "Spinnaker"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Tamron(OrganizationModel):
    """Model Tamron"""

    name: Literal["Tamron"] = "Tamron"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Technical_Manufacturing_Corporation(OrganizationModel):
    """Model Technical Manufacturing Corporation"""

    name: Literal["Technical Manufacturing Corporation"] = "Technical Manufacturing Corporation"
    abbreviation: Literal["TMC"] = "TMC"
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Teledyne_Flir(OrganizationModel):
    """Model Teledyne FLIR"""

    name: Literal["Teledyne FLIR"] = "Teledyne FLIR"
    abbreviation: Literal["FLIR"] = "FLIR"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="01j1gwp17")


class _Templeton_World_Charity_Foundation(OrganizationModel):
    """Model Templeton World Charity Foundation"""

    name: Literal["Templeton World Charity Foundation"] = "Templeton World Charity Foundation"
    abbreviation: Literal["TWCF"] = "TWCF"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00x0z1472")


class _The_Imaging_Source(OrganizationModel):
    """Model The Imaging Source"""

    name: Literal["The Imaging Source"] = "The Imaging Source"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _The_Lee_Company(OrganizationModel):
    """Model The Lee Company"""

    name: Literal["The Lee Company"] = "The Lee Company"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Thermo_Fisher_Scientific(OrganizationModel):
    """Model Thermo Fisher Scientific"""

    name: Literal["Thermo Fisher Scientific"] = "Thermo Fisher Scientific"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="03x1ewr52")


class _Thorlabs(OrganizationModel):
    """Model Thorlabs"""

    name: Literal["Thorlabs"] = "Thorlabs"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="04gsnvb07")


class _Transducer_Techniques(OrganizationModel):
    """Model Transducer Techniques"""

    name: Literal["Transducer Techniques"] = "Transducer Techniques"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Tymphany(OrganizationModel):
    """Model Tymphany"""

    name: Literal["Tymphany"] = "Tymphany"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _University_Of_California_San_Diego(OrganizationModel):
    """Model University of California, San Diego"""

    name: Literal["University of California, San Diego"] = "University of California, San Diego"
    abbreviation: Literal["UCSD"] = "UCSD"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="0168r3w48")


class _University_Of_Pennsylvania(OrganizationModel):
    """Model University of Pennsylvania"""

    name: Literal["University of Pennsylvania"] = "University of Pennsylvania"
    abbreviation: Literal["UPENN"] = "UPENN"
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="00b30xv10")


class _Vieworks(OrganizationModel):
    """Model Vieworks"""

    name: Literal["Vieworks"] = "Vieworks"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Vortran(OrganizationModel):
    """Model Vortran"""

    name: Literal["Vortran"] = "Vortran"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=None)
    registry_identifier: Optional[str] = Field(default=None)


class _Ams_Osram(OrganizationModel):
    """Model ams OSRAM"""

    name: Literal["ams OSRAM"] = "ams OSRAM"
    abbreviation: Literal[None] = None
    registry: Optional[Registry] = Field(default=Registry.ROR)
    registry_identifier: Optional[str] = Field(default="045d0h266")


class Organization:
    """Organization"""

    AA_OPTO_ELECTRONIC = _Aa_Opto_Electronic()
    ASUS = _Asus()
    ABCAM = _Abcam()
    ADDGENE = _Addgene()
    AILIPU = _Ailipu_Technology_Co()
    AI = _Allen_Institute()
    AIBS = _Allen_Institute_For_Brain_Science()
    AIND = _Allen_Institute_For_Neural_Dynamics()
    ALLIED = _Allied()
    ASI = _Applied_Scientific_Instrumentation()
    ARECONT_VISION_COSTAR = _Arecont_Vision_Costar()
    BASLER = _Basler()
    BCM = _Baylor_College_Of_Medicine()
    BU = _Boston_University()
    CAJAL = _Cajal_Neuroscience()
    CAMBRIDGE_TECHNOLOGY = _Cambridge_Technology()
    CARL_ZEISS = _Carl_Zeiss()
    CHAMPALIMAUD = _Champalimaud_Foundation()
    CZI = _Chan_Zuckerberg_Initiative()
    CRL = _Charles_River_Laboratories()
    CHROMA = _Chroma()
    COHERENT_SCIENTIFIC = _Coherent_Scientific()
    COLUMBIA = _Columbia_University()
    COMPUTAR = _Computar()
    CONOPTICS = _Conoptics()
    CUSTOM = _Custom()
    DIGIKEY = _Digikey()
    DODOTRONIC = _Dodotronic()
    DORIC = _Doric()
    EALING = _Ealing()
    EDMUND_OPTICS = _Edmund_Optics()
    EMORY = _Emory_University()
    EURESYS = _Euresys()
    FUJINON = _Fujinon()
    HAMAMATSU = _Hamamatsu()
    HAMILTON = _Hamilton()
    HUST = _Huazhong_University_Of_Science_And_Technology()
    IR_ROBOT_CO = _Ir_Robot_Co()
    ISL = _Isl_Products_International()
    INFINITY_PHOTO_OPTICAL = _Infinity_Photo_Optical()
    IDT = _Integrated_Dna_Technologies()
    IMEC = _Interuniversity_Microelectronics_Center()
    INVITROGEN = _Invitrogen()
    ITEM = _Item()
    JAX = _Jackson_Laboratory()
    JANELIA = _Janelia_Research_Campus()
    JENOPTIK = _Jenoptik()
    JHU = _Johns_Hopkins_University()
    JULABO = _Julabo()
    KOWA = _Kowa()
    LASOS = _Lasos_Lasertechnik()
    LG = _Lg()
    LEICA = _Leica()
    LIFECANVAS = _Lifecanvas()
    LUMEN_DYNAMICS = _Lumen_Dynamics()
    MBF = _Mbf_Bioscience()
    MIT_BCS = _Mit_Department_Of_Brain_And_Cognitive_Sciences()
    MKS_NEWPORT = _Mks_Newport()
    MPI = _Mpi()
    MIT = _Massachusetts_Institute_Of_Technology()
    MIBR = _Mcgovern_Institute_For_Brain_Research()
    MEADOWLARK_OPTICS = _Meadowlark_Optics()
    MJFF = _Michael_J_Fox_Foundation_For_Parkinson_S_Research()
    MIDOPT = _Midwest_Optical_Systems_Inc_()
    MITUTUYO = _Mitutuyo()
    NRESEARCH_INC = _Nresearch_Inc()
    NCCIH = _National_Center_For_Complementary_And_Integrative_Health()
    NIMH = _National_Institute_Of_Mental_Health()
    NINDS = _National_Institute_Of_Neurological_Disorders_And_Stroke()
    NATIONAL_INSTRUMENTS = _National_Instruments()
    NAVITAR = _Navitar()
    NEURALYNX = _Neuralynx()
    NEUROPHOTOMETRICS = _Neurophotometrics()
    NEW_SCALE_TECHNOLOGIES = _New_Scale_Technologies()
    NYU = _New_York_University()
    NIKON = _Nikon()
    OLYMPUS = _Olympus()
    OEPS = _Open_Ephys_Production_Site()
    OPTOTUNE = _Optotune()
    OTHER = _Other()
    OXXIUS = _Oxxius()
    PLACID_INDUSTRIES = _Placid_Industries()
    PRIZMATIX = _Prizmatix()
    QUANTIFI = _Quantifi()
    RASPBERRY_PI = _Raspberry_Pi()
    SICGEN = _Sicgen()
    SAME_SKY = _Same_Sky()
    SCHNEIDER_KREUZNACH = _Schneider_Kreuznach()
    SECOND_ORDER_EFFECTS = _Second_Order_Effects()
    SEMROCK = _Semrock()
    SIGMA_ALDRICH = _Sigma_Aldrich()
    SIMONS_FOUNDATION = _Simons_Foundation()
    SPECTRA_PHYSICS = _Spectra_Physics()
    SPINNAKER = _Spinnaker()
    TAMRON = _Tamron()
    TMC = _Technical_Manufacturing_Corporation()
    FLIR = _Teledyne_Flir()
    TWCF = _Templeton_World_Charity_Foundation()
    THE_IMAGING_SOURCE = _The_Imaging_Source()
    THE_LEE_COMPANY = _The_Lee_Company()
    THERMO_FISHER_SCIENTIFIC = _Thermo_Fisher_Scientific()
    THORLABS = _Thorlabs()
    TRANSDUCER_TECHNIQUES = _Transducer_Techniques()
    TYMPHANY = _Tymphany()
    UCSD = _University_Of_California_San_Diego()
    UPENN = _University_Of_Pennsylvania()
    VIEWORKS = _Vieworks()
    VORTRAN = _Vortran()
    AMS_OSRAM = _Ams_Osram()

    ALL = tuple(OrganizationModel.__subclasses__())

    ONE_OF = Annotated[Union[tuple(OrganizationModel.__subclasses__())], Field(discriminator="name")]

    abbreviation_map = {m().abbreviation: m() for m in ALL if m().abbreviation is not None}

    @classmethod
    def from_abbreviation(cls, abbreviation: str):
        """Get platform from abbreviation"""
        return cls.abbreviation_map.get(abbreviation, None)

    name_map = {m().name: m() for m in ALL}

    @classmethod
    def from_name(cls, name: str):
        """Get platform from name"""
        return cls.name_map.get(name, None)


Organization.DETECTOR_MANUFACTURERS = one_of_instance(
    [
        Organization.AILIPU,
        Organization.ALLIED,
        Organization.BASLER,
        Organization.DODOTRONIC,
        Organization.EDMUND_OPTICS,
        Organization.HAMAMATSU,
        Organization.SPINNAKER,
        Organization.FLIR,
        Organization.THE_IMAGING_SOURCE,
        Organization.THORLABS,
        Organization.VIEWORKS,
        Organization.OTHER,
    ]
)

Organization.FILTER_MANUFACTURERS = one_of_instance(
    [
        Organization.CHROMA,
        Organization.EDMUND_OPTICS,
        Organization.MIDOPT,
        Organization.SEMROCK,
        Organization.THORLABS,
        Organization.OTHER,
    ]
)

Organization.LENS_MANUFACTURERS = one_of_instance(
    [
        Organization.COMPUTAR,
        Organization.EDMUND_OPTICS,
        Organization.FUJINON,
        Organization.HAMAMATSU,
        Organization.INFINITY_PHOTO_OPTICAL,
        Organization.KOWA,
        Organization.LEICA,
        Organization.MITUTUYO,
        Organization.NAVITAR,
        Organization.NIKON,
        Organization.OLYMPUS,
        Organization.SCHNEIDER_KREUZNACH,
        Organization.TAMRON,
        Organization.THORLABS,
        Organization.CARL_ZEISS,
        Organization.OTHER,
    ]
)

Organization.DAQ_DEVICE_MANUFACTURERS = one_of_instance(
    [
        Organization.AIND,
        Organization.CHAMPALIMAUD,
        Organization.NATIONAL_INSTRUMENTS,
        Organization.IMEC,
        Organization.OEPS,
        Organization.SECOND_ORDER_EFFECTS,
        Organization.OTHER,
    ]
)

Organization.LASER_MANUFACTURERS = one_of_instance(
    [
        Organization.COHERENT_SCIENTIFIC,
        Organization.HAMAMATSU,
        Organization.LASOS,
        Organization.OXXIUS,
        Organization.QUANTIFI,
        Organization.SPECTRA_PHYSICS,
        Organization.THORLABS,
        Organization.VORTRAN,
        Organization.OTHER,
    ]
)

Organization.LED_MANUFACTURERS = one_of_instance(
    [Organization.AMS_OSRAM, Organization.DORIC, Organization.PRIZMATIX, Organization.THORLABS, Organization.OTHER]
)

Organization.MANIPULATOR_MANUFACTURERS = one_of_instance([Organization.NEW_SCALE_TECHNOLOGIES, Organization.OTHER])

Organization.MONITOR_MANUFACTURERS = one_of_instance([Organization.ASUS, Organization.LG, Organization.OTHER])

Organization.SPEAKER_MANUFACTURERS = one_of_instance(
    [Organization.DIGIKEY, Organization.TYMPHANY, Organization.ISL, Organization.OTHER]
)

Organization.FUNDERS = one_of_instance(
    [
        Organization.AI,
        Organization.CZI,
        Organization.MBF,
        Organization.MJFF,
        Organization.NCCIH,
        Organization.NIMH,
        Organization.NINDS,
        Organization.SIMONS_FOUNDATION,
        Organization.TWCF,
    ]
)

Organization.RESEARCH_INSTITUTIONS = one_of_instance(
    [
        Organization.AIBS,
        Organization.AIND,
        Organization.MIT_BCS,
        Organization.BU,
        Organization.COLUMBIA,
        Organization.HUST,
        Organization.JANELIA,
        Organization.JHU,
        Organization.MIBR,
        Organization.MIT,
        Organization.NYU,
        Organization.UCSD,
        Organization.UPENN,
        Organization.OTHER,
    ]
)

Organization.SUBJECT_SOURCES = one_of_instance(
    [
        Organization.AI,
        Organization.BCM,
        Organization.COLUMBIA,
        Organization.HUST,
        Organization.JANELIA,
        Organization.JAX,
        Organization.NYU,
        Organization.UPENN,
        Organization.OTHER,
    ]
)

Organization.CATHETER_IMPLANT_INSTITUTIONS = one_of_instance(
    [
        Organization.AIND,
        Organization.CRL,
        Organization.JAX,
        Organization.OTHER,
    ]
)
