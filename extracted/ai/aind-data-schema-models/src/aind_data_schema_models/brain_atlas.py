"""Brain atlases"""

from pydantic import BaseModel, ConfigDict


class BrainStructureModel(BaseModel):
    """Base model for brain strutures"""

    model_config = ConfigDict(frozen=True)
    atlas: str
    name: str
    acronym: str
    id: str


class CCFv3:
    """CCFv3"""

    VI = BrainStructureModel(
        atlas="CCFv3",
        name="Abducens nucleus",
        acronym="VI",
        id="653",
    )
    ACVII = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory facial motor nucleus",
        acronym="ACVII",
        id="576",
    )
    AOB = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory olfactory bulb",
        acronym="AOB",
        id="151",
    )
    AOBGL = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory olfactory bulb, glomerular layer",
        acronym="AOBgl",
        id="188",
    )
    AOBGR = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory olfactory bulb, granular layer",
        acronym="AOBgr",
        id="196",
    )
    AOBMI = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory olfactory bulb, mitral layer",
        acronym="AOBmi",
        id="204",
    )
    ASO = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory supraoptic group",
        acronym="ASO",
        id="332",
    )
    ACS5 = BrainStructureModel(
        atlas="CCFv3",
        name="Accessory trigeminal nucleus",
        acronym="Acs5",
        id="549009219",
    )
    AI = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area",
        acronym="AI",
        id="95",
    )
    AID = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part",
        acronym="AId",
        id="104",
    )
    AID1 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part, layer 1",
        acronym="AId1",
        id="996",
    )
    AID2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part, layer 2/3",
        acronym="AId2/3",
        id="328",
    )
    AID5 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part, layer 5",
        acronym="AId5",
        id="1101",
    )
    AID6A = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part, layer 6a",
        acronym="AId6a",
        id="783",
    )
    AID6B = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, dorsal part, layer 6b",
        acronym="AId6b",
        id="831",
    )
    AIP = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part",
        acronym="AIp",
        id="111",
    )
    AIP1 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part, layer 1",
        acronym="AIp1",
        id="120",
    )
    AIP2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part, layer 2/3",
        acronym="AIp2/3",
        id="163",
    )
    AIP5 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part, layer 5",
        acronym="AIp5",
        id="344",
    )
    AIP6A = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part, layer 6a",
        acronym="AIp6a",
        id="314",
    )
    AIP6B = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, posterior part, layer 6b",
        acronym="AIp6b",
        id="355",
    )
    AIV = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part",
        acronym="AIv",
        id="119",
    )
    AIV1 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part, layer 1",
        acronym="AIv1",
        id="704",
    )
    AIV2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part, layer 2/3",
        acronym="AIv2/3",
        id="694",
    )
    AIV5 = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part, layer 5",
        acronym="AIv5",
        id="800",
    )
    AIV6A = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part, layer 6a",
        acronym="AIv6a",
        id="675",
    )
    AIV6B = BrainStructureModel(
        atlas="CCFv3",
        name="Agranular insular area, ventral part, layer 6b",
        acronym="AIv6b",
        id="699",
    )
    CA = BrainStructureModel(
        atlas="CCFv3",
        name="Ammon's horn",
        acronym="CA",
        id="375",
    )
    AN = BrainStructureModel(
        atlas="CCFv3",
        name="Ansiform lobule",
        acronym="AN",
        id="1017",
    )
    AAA = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior amygdalar area",
        acronym="AAA",
        id="23",
    )
    VISA = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area",
        acronym="VISa",
        id="312782546",
    )
    VISA1 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 1",
        acronym="VISa1",
        id="312782550",
    )
    VISA2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 2/3",
        acronym="VISa2/3",
        id="312782554",
    )
    VISA4 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 4",
        acronym="VISa4",
        id="312782558",
    )
    VISA5 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 5",
        acronym="VISa5",
        id="312782562",
    )
    VISA6A = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 6a",
        acronym="VISa6a",
        id="312782566",
    )
    VISA6B = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior area, layer 6b",
        acronym="VISa6b",
        id="312782570",
    )
    ACA = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area",
        acronym="ACA",
        id="31",
    )
    ACAD = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part",
        acronym="ACAd",
        id="39",
    )
    ACAD1 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part, layer 1",
        acronym="ACAd1",
        id="935",
    )
    ACAD2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part, layer 2/3",
        acronym="ACAd2/3",
        id="211",
    )
    ACAD5 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part, layer 5",
        acronym="ACAd5",
        id="1015",
    )
    ACAD6A = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part, layer 6a",
        acronym="ACAd6a",
        id="919",
    )
    ACAD6B = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, dorsal part, layer 6b",
        acronym="ACAd6b",
        id="927",
    )
    ACAV = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part",
        acronym="ACAv",
        id="48",
    )
    ACAV6A = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part, 6a",
        acronym="ACAv6a",
        id="810",
    )
    ACAV6B = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part, 6b",
        acronym="ACAv6b",
        id="819",
    )
    ACAV1 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part, layer 1",
        acronym="ACAv1",
        id="588",
    )
    ACAV2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part, layer 2/3",
        acronym="ACAv2/3",
        id="296",
    )
    ACAV5 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior cingulate area, ventral part, layer 5",
        acronym="ACAv5",
        id="772",
    )
    ATN = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior group of the dorsal thalamus",
        acronym="ATN",
        id="239",
    )
    AHN = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior hypothalamic nucleus",
        acronym="AHN",
        id="88",
    )
    AON = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior olfactory nucleus",
        acronym="AON",
        id="159",
    )
    APN = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior pretectal nucleus",
        acronym="APN",
        id="215",
    )
    AT = BrainStructureModel(
        atlas="CCFv3",
        name="Anterior tegmental nucleus",
        acronym="AT",
        id="231",
    )
    AD = BrainStructureModel(
        atlas="CCFv3",
        name="Anterodorsal nucleus",
        acronym="AD",
        id="64",
    )
    ADP = BrainStructureModel(
        atlas="CCFv3",
        name="Anterodorsal preoptic nucleus",
        acronym="ADP",
        id="72",
    )
    VISAL = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area",
        acronym="VISal",
        id="402",
    )
    VISAL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 1",
        acronym="VISal1",
        id="1074",
    )
    VISAL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 2/3",
        acronym="VISal2/3",
        id="905",
    )
    VISAL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 4",
        acronym="VISal4",
        id="1114",
    )
    VISAL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 5",
        acronym="VISal5",
        id="233",
    )
    VISAL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 6a",
        acronym="VISal6a",
        id="601",
    )
    VISAL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Anterolateral visual area, layer 6b",
        acronym="VISal6b",
        id="649",
    )
    AM = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial nucleus",
        acronym="AM",
        id="127",
    )
    AMD = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial nucleus, dorsal part",
        acronym="AMd",
        id="1096",
    )
    AMV = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial nucleus, ventral part",
        acronym="AMv",
        id="1104",
    )
    VISAM = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area",
        acronym="VISam",
        id="394",
    )
    VISAM1 = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 1",
        acronym="VISam1",
        id="281",
    )
    VISAM2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 2/3",
        acronym="VISam2/3",
        id="1066",
    )
    VISAM4 = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 4",
        acronym="VISam4",
        id="401",
    )
    VISAM5 = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 5",
        acronym="VISam5",
        id="433",
    )
    VISAM6A = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 6a",
        acronym="VISam6a",
        id="1046",
    )
    VISAM6B = BrainStructureModel(
        atlas="CCFv3",
        name="Anteromedial visual area, layer 6b",
        acronym="VISam6b",
        id="441",
    )
    AV = BrainStructureModel(
        atlas="CCFv3",
        name="Anteroventral nucleus of thalamus",
        acronym="AV",
        id="255",
    )
    AVPV = BrainStructureModel(
        atlas="CCFv3",
        name="Anteroventral periventricular nucleus",
        acronym="AVPV",
        id="272",
    )
    AVP = BrainStructureModel(
        atlas="CCFv3",
        name="Anteroventral preoptic nucleus",
        acronym="AVP",
        id="263",
    )
    ARH = BrainStructureModel(
        atlas="CCFv3",
        name="Arcuate hypothalamic nucleus",
        acronym="ARH",
        id="223",
    )
    AP = BrainStructureModel(
        atlas="CCFv3",
        name="Area postrema",
        acronym="AP",
        id="207",
    )
    APR = BrainStructureModel(
        atlas="CCFv3",
        name="Area prostriata",
        acronym="APr",
        id="484682508",
    )
    AUD = BrainStructureModel(
        atlas="CCFv3",
        name="Auditory areas",
        acronym="AUD",
        id="247",
    )
    B = BrainStructureModel(
        atlas="CCFv3",
        name="Barrington's nucleus",
        acronym="B",
        id="280",
    )
    GREY = BrainStructureModel(
        atlas="CCFv3",
        name="Basic cell groups and regions",
        acronym="grey",
        id="8",
    )
    BLA = BrainStructureModel(
        atlas="CCFv3",
        name="Basolateral amygdalar nucleus",
        acronym="BLA",
        id="295",
    )
    BLAA = BrainStructureModel(
        atlas="CCFv3",
        name="Basolateral amygdalar nucleus, anterior part",
        acronym="BLAa",
        id="303",
    )
    BLAP = BrainStructureModel(
        atlas="CCFv3",
        name="Basolateral amygdalar nucleus, posterior part",
        acronym="BLAp",
        id="311",
    )
    BLAV = BrainStructureModel(
        atlas="CCFv3",
        name="Basolateral amygdalar nucleus, ventral part",
        acronym="BLAv",
        id="451",
    )
    BMA = BrainStructureModel(
        atlas="CCFv3",
        name="Basomedial amygdalar nucleus",
        acronym="BMA",
        id="319",
    )
    BMAA = BrainStructureModel(
        atlas="CCFv3",
        name="Basomedial amygdalar nucleus, anterior part",
        acronym="BMAa",
        id="327",
    )
    BMAP = BrainStructureModel(
        atlas="CCFv3",
        name="Basomedial amygdalar nucleus, posterior part",
        acronym="BMAp",
        id="334",
    )
    BST = BrainStructureModel(
        atlas="CCFv3",
        name="Bed nuclei of the stria terminalis",
        acronym="BST",
        id="351",
    )
    BA = BrainStructureModel(
        atlas="CCFv3",
        name="Bed nucleus of the accessory olfactory tract",
        acronym="BA",
        id="292",
    )
    BAC = BrainStructureModel(
        atlas="CCFv3",
        name="Bed nucleus of the anterior commissure",
        acronym="BAC",
        id="287",
    )
    BS = BrainStructureModel(
        atlas="CCFv3",
        name="Brain stem",
        acronym="BS",
        id="343",
    )
    CP = BrainStructureModel(
        atlas="CCFv3",
        name="Caudoputamen",
        acronym="CP",
        id="672",
    )
    CEA = BrainStructureModel(
        atlas="CCFv3",
        name="Central amygdalar nucleus",
        acronym="CEA",
        id="536",
    )
    CEAC = BrainStructureModel(
        atlas="CCFv3",
        name="Central amygdalar nucleus, capsular part",
        acronym="CEAc",
        id="544",
    )
    CEAL = BrainStructureModel(
        atlas="CCFv3",
        name="Central amygdalar nucleus, lateral part",
        acronym="CEAl",
        id="551",
    )
    CEAM = BrainStructureModel(
        atlas="CCFv3",
        name="Central amygdalar nucleus, medial part",
        acronym="CEAm",
        id="559",
    )
    CL = BrainStructureModel(
        atlas="CCFv3",
        name="Central lateral nucleus of the thalamus",
        acronym="CL",
        id="575",
    )
    CLI = BrainStructureModel(
        atlas="CCFv3",
        name="Central linear nucleus raphe",
        acronym="CLI",
        id="591",
    )
    CENT = BrainStructureModel(
        atlas="CCFv3",
        name="Central lobule",
        acronym="CENT",
        id="920",
    )
    CM = BrainStructureModel(
        atlas="CCFv3",
        name="Central medial nucleus of the thalamus",
        acronym="CM",
        id="599",
    )
    CBX = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebellar cortex",
        acronym="CBX",
        id="528",
    )
    CBN = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebellar nuclei",
        acronym="CBN",
        id="519",
    )
    CB = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebellum",
        acronym="CB",
        id="512",
    )
    CTX = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebral cortex",
        acronym="CTX",
        id="688",
    )
    CNU = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebral nuclei",
        acronym="CNU",
        id="623",
    )
    CH = BrainStructureModel(
        atlas="CCFv3",
        name="Cerebrum",
        acronym="CH",
        id="567",
    )
    CLA = BrainStructureModel(
        atlas="CCFv3",
        name="Claustrum",
        acronym="CLA",
        id="583",
    )
    CN = BrainStructureModel(
        atlas="CCFv3",
        name="Cochlear nuclei",
        acronym="CN",
        id="607",
    )
    COPY = BrainStructureModel(
        atlas="CCFv3",
        name="Copula pyramidis",
        acronym="COPY",
        id="1033",
    )
    COA = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical amygdalar area",
        acronym="COA",
        id="631",
    )
    COAA = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical amygdalar area, anterior part",
        acronym="COAa",
        id="639",
    )
    COAP = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical amygdalar area, posterior part",
        acronym="COAp",
        id="647",
    )
    COAPL = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical amygdalar area, posterior part, lateral zone",
        acronym="COApl",
        id="655",
    )
    COAPM = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical amygdalar area, posterior part, medial zone",
        acronym="COApm",
        id="663",
    )
    CTXPL = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical plate",
        acronym="CTXpl",
        id="695",
    )
    CTXSP = BrainStructureModel(
        atlas="CCFv3",
        name="Cortical subplate",
        acronym="CTXsp",
        id="703",
    )
    ANCR1 = BrainStructureModel(
        atlas="CCFv3",
        name="Crus 1",
        acronym="ANcr1",
        id="1056",
    )
    ANCR2 = BrainStructureModel(
        atlas="CCFv3",
        name="Crus 2",
        acronym="ANcr2",
        id="1064",
    )
    CUL = BrainStructureModel(
        atlas="CCFv3",
        name="Culmen",
        acronym="CUL",
        id="928",
    )
    CU = BrainStructureModel(
        atlas="CCFv3",
        name="Cuneate nucleus",
        acronym="CU",
        id="711",
    )
    CUN = BrainStructureModel(
        atlas="CCFv3",
        name="Cuneiform nucleus",
        acronym="CUN",
        id="616",
    )
    DEC = BrainStructureModel(
        atlas="CCFv3",
        name="Declive (VI)",
        acronym="DEC",
        id="936",
    )
    DG = BrainStructureModel(
        atlas="CCFv3",
        name="Dentate gyrus",
        acronym="DG",
        id="726",
    )
    DG_SG = BrainStructureModel(
        atlas="CCFv3",
        name="Dentate gyrus, granule cell layer",
        acronym="DG-sg",
        id="632",
    )
    DG_MO = BrainStructureModel(
        atlas="CCFv3",
        name="Dentate gyrus, molecular layer",
        acronym="DG-mo",
        id="10703",
    )
    DG_PO = BrainStructureModel(
        atlas="CCFv3",
        name="Dentate gyrus, polymorph layer",
        acronym="DG-po",
        id="10704",
    )
    DN = BrainStructureModel(
        atlas="CCFv3",
        name="Dentate nucleus",
        acronym="DN",
        id="846",
    )
    NDB = BrainStructureModel(
        atlas="CCFv3",
        name="Diagonal band nucleus",
        acronym="NDB",
        id="596",
    )
    AUDD = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area",
        acronym="AUDd",
        id="1011",
    )
    AUDD1 = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 1",
        acronym="AUDd1",
        id="527",
    )
    AUDD2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 2/3",
        acronym="AUDd2/3",
        id="600",
    )
    AUDD4 = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 4",
        acronym="AUDd4",
        id="678",
    )
    AUDD5 = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 5",
        acronym="AUDd5",
        id="252",
    )
    AUDD6A = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 6a",
        acronym="AUDd6a",
        id="156",
    )
    AUDD6B = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal auditory area, layer 6b",
        acronym="AUDd6b",
        id="243",
    )
    DCO = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal cochlear nucleus",
        acronym="DCO",
        id="96",
    )
    DCN = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal column nuclei",
        acronym="DCN",
        id="720",
    )
    DMX = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal motor nucleus of the vagus nerve",
        acronym="DMX",
        id="839",
    )
    DR = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal nucleus raphe",
        acronym="DR",
        id="872",
    )
    LGD = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal part of the lateral geniculate complex",
        acronym="LGd",
        id="170",
    )
    LGD_CO = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal part of the lateral geniculate complex, core",
        acronym="LGd-co",
        id="496345668",
    )
    LGD_IP = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal part of the lateral geniculate complex, ipsilateral zone",
        acronym="LGd-ip",
        id="496345672",
    )
    LGD_SH = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal part of the lateral geniculate complex, shell",
        acronym="LGd-sh",
        id="496345664",
    )
    DP = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal peduncular area",
        acronym="DP",
        id="814",
    )
    PMD = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal premammillary nucleus",
        acronym="PMd",
        id="980",
    )
    DTN = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal tegmental nucleus",
        acronym="DTN",
        id="880",
    )
    DT = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsal terminal nucleus of the accessory optic tract",
        acronym="DT",
        id="75",
    )
    DMH = BrainStructureModel(
        atlas="CCFv3",
        name="Dorsomedial nucleus of the hypothalamus",
        acronym="DMH",
        id="830",
    )
    ECT = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area",
        acronym="ECT",
        id="895",
    )
    ECT1 = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area/Layer 1",
        acronym="ECT1",
        id="836",
    )
    ECT2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area/Layer 2/3",
        acronym="ECT2/3",
        id="427",
    )
    ECT5 = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area/Layer 5",
        acronym="ECT5",
        id="988",
    )
    ECT6A = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area/Layer 6a",
        acronym="ECT6a",
        id="977",
    )
    ECT6B = BrainStructureModel(
        atlas="CCFv3",
        name="Ectorhinal area/Layer 6b",
        acronym="ECT6b",
        id="1045",
    )
    EW = BrainStructureModel(
        atlas="CCFv3",
        name="Edinger-Westphal nucleus",
        acronym="EW",
        id="975",
    )
    EP = BrainStructureModel(
        atlas="CCFv3",
        name="Endopiriform nucleus",
        acronym="EP",
        id="942",
    )
    EPD = BrainStructureModel(
        atlas="CCFv3",
        name="Endopiriform nucleus, dorsal part",
        acronym="EPd",
        id="952",
    )
    EPV = BrainStructureModel(
        atlas="CCFv3",
        name="Endopiriform nucleus, ventral part",
        acronym="EPv",
        id="966",
    )
    ENT = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area",
        acronym="ENT",
        id="909",
    )
    ENTL = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part",
        acronym="ENTl",
        id="918",
    )
    ENTL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part, layer 1",
        acronym="ENTl1",
        id="1121",
    )
    ENTL2 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part, layer 2",
        acronym="ENTl2",
        id="20",
    )
    ENTL3 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part, layer 3",
        acronym="ENTl3",
        id="52",
    )
    ENTL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part, layer 5",
        acronym="ENTl5",
        id="139",
    )
    ENTL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, lateral part, layer 6a",
        acronym="ENTl6a",
        id="28",
    )
    ENTM = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone",
        acronym="ENTm",
        id="926",
    )
    ENTM1 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone, layer 1",
        acronym="ENTm1",
        id="526",
    )
    ENTM2 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone, layer 2",
        acronym="ENTm2",
        id="543",
    )
    ENTM3 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone, layer 3",
        acronym="ENTm3",
        id="664",
    )
    ENTM5 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone, layer 5",
        acronym="ENTm5",
        id="727",
    )
    ENTM6 = BrainStructureModel(
        atlas="CCFv3",
        name="Entorhinal area, medial part, dorsal zone, layer 6",
        acronym="ENTm6",
        id="743",
    )
    EPI = BrainStructureModel(
        atlas="CCFv3",
        name="Epithalamus",
        acronym="EPI",
        id="958",
    )
    ETH = BrainStructureModel(
        atlas="CCFv3",
        name="Ethmoid nucleus of the thalamus",
        acronym="Eth",
        id="560581551",
    )
    ECU = BrainStructureModel(
        atlas="CCFv3",
        name="External cuneate nucleus",
        acronym="ECU",
        id="903",
    )
    VII = BrainStructureModel(
        atlas="CCFv3",
        name="Facial motor nucleus",
        acronym="VII",
        id="661",
    )
    FC = BrainStructureModel(
        atlas="CCFv3",
        name="Fasciola cinerea",
        acronym="FC",
        id="982",
    )
    FN = BrainStructureModel(
        atlas="CCFv3",
        name="Fastigial nucleus",
        acronym="FN",
        id="989",
    )
    CA1 = BrainStructureModel(
        atlas="CCFv3",
        name="Field CA1",
        acronym="CA1",
        id="382",
    )
    CA2 = BrainStructureModel(
        atlas="CCFv3",
        name="Field CA2",
        acronym="CA2",
        id="423",
    )
    CA3 = BrainStructureModel(
        atlas="CCFv3",
        name="Field CA3",
        acronym="CA3",
        id="463",
    )
    FF = BrainStructureModel(
        atlas="CCFv3",
        name="Fields of Forel",
        acronym="FF",
        id="804",
    )
    FL = BrainStructureModel(
        atlas="CCFv3",
        name="Flocculus",
        acronym="FL",
        id="1049",
    )
    FOTU = BrainStructureModel(
        atlas="CCFv3",
        name="Folium-tuber vermis (VII)",
        acronym="FOTU",
        id="944",
    )
    FRP = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, cerebral cortex",
        acronym="FRP",
        id="184",
    )
    FRP1 = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, layer 1",
        acronym="FRP1",
        id="68",
    )
    FRP2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, layer 2/3",
        acronym="FRP2/3",
        id="667",
    )
    FRP5 = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, layer 5",
        acronym="FRP5",
        id="526157192",
    )
    FRP6A = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, layer 6a",
        acronym="FRP6a",
        id="526157196",
    )
    FRP6B = BrainStructureModel(
        atlas="CCFv3",
        name="Frontal pole, layer 6b",
        acronym="FRP6b",
        id="526322264",
    )
    FS = BrainStructureModel(
        atlas="CCFv3",
        name="Fundus of striatum",
        acronym="FS",
        id="998",
    )
    GEND = BrainStructureModel(
        atlas="CCFv3",
        name="Geniculate group, dorsal thalamus",
        acronym="GENd",
        id="1008",
    )
    GENV = BrainStructureModel(
        atlas="CCFv3",
        name="Geniculate group, ventral thalamus",
        acronym="GENv",
        id="1014",
    )
    GRN = BrainStructureModel(
        atlas="CCFv3",
        name="Gigantocellular reticular nucleus",
        acronym="GRN",
        id="1048",
    )
    GPE = BrainStructureModel(
        atlas="CCFv3",
        name="Globus pallidus, external segment",
        acronym="GPe",
        id="1022",
    )
    GPI = BrainStructureModel(
        atlas="CCFv3",
        name="Globus pallidus, internal segment",
        acronym="GPi",
        id="1031",
    )
    GR = BrainStructureModel(
        atlas="CCFv3",
        name="Gracile nucleus",
        acronym="GR",
        id="1039",
    )
    GU = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas",
        acronym="GU",
        id="1057",
    )
    GU1 = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 1",
        acronym="GU1",
        id="36",
    )
    GU2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 2/3",
        acronym="GU2/3",
        id="180",
    )
    GU4 = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 4",
        acronym="GU4",
        id="148",
    )
    GU5 = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 5",
        acronym="GU5",
        id="187",
    )
    GU6A = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 6a",
        acronym="GU6a",
        id="638",
    )
    GU6B = BrainStructureModel(
        atlas="CCFv3",
        name="Gustatory areas, layer 6b",
        acronym="GU6b",
        id="662",
    )
    HEM = BrainStructureModel(
        atlas="CCFv3",
        name="Hemispheric regions",
        acronym="HEM",
        id="1073",
    )
    HB = BrainStructureModel(
        atlas="CCFv3",
        name="Hindbrain",
        acronym="HB",
        id="1065",
    )
    HPF = BrainStructureModel(
        atlas="CCFv3",
        name="Hippocampal formation",
        acronym="HPF",
        id="1089",
    )
    HIP = BrainStructureModel(
        atlas="CCFv3",
        name="Hippocampal region",
        acronym="HIP",
        id="1080",
    )
    HATA = BrainStructureModel(
        atlas="CCFv3",
        name="Hippocampo-amygdalar transition area",
        acronym="HATA",
        id="589508447",
    )
    XII = BrainStructureModel(
        atlas="CCFv3",
        name="Hypoglossal nucleus",
        acronym="XII",
        id="773",
    )
    LZ = BrainStructureModel(
        atlas="CCFv3",
        name="Hypothalamic lateral zone",
        acronym="LZ",
        id="290",
    )
    MEZ = BrainStructureModel(
        atlas="CCFv3",
        name="Hypothalamic medial zone",
        acronym="MEZ",
        id="467",
    )
    HY = BrainStructureModel(
        atlas="CCFv3",
        name="Hypothalamus",
        acronym="HY",
        id="1097",
    )
    IG = BrainStructureModel(
        atlas="CCFv3",
        name="Induseum griseum",
        acronym="IG",
        id="19",
    )
    IC = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior colliculus",
        acronym="IC",
        id="4",
    )
    ICC = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior colliculus, central nucleus",
        acronym="ICc",
        id="811",
    )
    ICD = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior colliculus, dorsal nucleus",
        acronym="ICd",
        id="820",
    )
    ICE = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior colliculus, external nucleus",
        acronym="ICe",
        id="828",
    )
    IO = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior olivary complex",
        acronym="IO",
        id="83",
    )
    ISN = BrainStructureModel(
        atlas="CCFv3",
        name="Inferior salivatory nucleus",
        acronym="ISN",
        id="106",
    )
    ICB = BrainStructureModel(
        atlas="CCFv3",
        name="Infracerebellar nucleus",
        acronym="ICB",
        id="372",
    )
    ILA = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area",
        acronym="ILA",
        id="44",
    )
    ILA1 = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area, layer 1",
        acronym="ILA1",
        id="707",
    )
    ILA2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area, layer 2/3",
        acronym="ILA2/3",
        id="556",
    )
    ILA5 = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area, layer 5",
        acronym="ILA5",
        id="827",
    )
    ILA6A = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area, layer 6a",
        acronym="ILA6a",
        id="1054",
    )
    ILA6B = BrainStructureModel(
        atlas="CCFv3",
        name="Infralimbic area, layer 6b",
        acronym="ILA6b",
        id="1081",
    )
    IAD = BrainStructureModel(
        atlas="CCFv3",
        name="Interanterodorsal nucleus of the thalamus",
        acronym="IAD",
        id="1113",
    )
    IAM = BrainStructureModel(
        atlas="CCFv3",
        name="Interanteromedial nucleus of the thalamus",
        acronym="IAM",
        id="1120",
    )
    IB = BrainStructureModel(
        atlas="CCFv3",
        name="Interbrain",
        acronym="IB",
        id="1129",
    )
    IA = BrainStructureModel(
        atlas="CCFv3",
        name="Intercalated amygdalar nucleus",
        acronym="IA",
        id="1105",
    )
    IF = BrainStructureModel(
        atlas="CCFv3",
        name="Interfascicular nucleus raphe",
        acronym="IF",
        id="12",
    )
    IGL = BrainStructureModel(
        atlas="CCFv3",
        name="Intergeniculate leaflet of the lateral geniculate complex",
        acronym="IGL",
        id="27",
    )
    INTG = BrainStructureModel(
        atlas="CCFv3",
        name="Intermediate geniculate nucleus",
        acronym="IntG",
        id="563807439",
    )
    IRN = BrainStructureModel(
        atlas="CCFv3",
        name="Intermediate reticular nucleus",
        acronym="IRN",
        id="136",
    )
    IMD = BrainStructureModel(
        atlas="CCFv3",
        name="Intermediodorsal nucleus of the thalamus",
        acronym="IMD",
        id="59",
    )
    IPN = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus",
        acronym="IPN",
        id="100",
    )
    IPA = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, apical",
        acronym="IPA",
        id="607344842",
    )
    IPC = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, caudal",
        acronym="IPC",
        id="607344838",
    )
    IPDL = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, dorsolateral",
        acronym="IPDL",
        id="607344858",
    )
    IPDM = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, dorsomedial",
        acronym="IPDM",
        id="607344854",
    )
    IPI = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, intermediate",
        acronym="IPI",
        id="607344850",
    )
    IPL = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, lateral",
        acronym="IPL",
        id="607344846",
    )
    IPR = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, rostral",
        acronym="IPR",
        id="607344834",
    )
    IPRL = BrainStructureModel(
        atlas="CCFv3",
        name="Interpeduncular nucleus, rostrolateral",
        acronym="IPRL",
        id="607344862",
    )
    IP = BrainStructureModel(
        atlas="CCFv3",
        name="Interposed nucleus",
        acronym="IP",
        id="91",
    )
    INC = BrainStructureModel(
        atlas="CCFv3",
        name="Interstitial nucleus of Cajal",
        acronym="INC",
        id="67",
    )
    I5 = BrainStructureModel(
        atlas="CCFv3",
        name="Intertrigeminal nucleus",
        acronym="I5",
        id="549009227",
    )
    ILM = BrainStructureModel(
        atlas="CCFv3",
        name="Intralaminar nuclei of the dorsal thalamus",
        acronym="ILM",
        id="51",
    )
    ISOCORTEX = BrainStructureModel(
        atlas="CCFv3",
        name="Isocortex",
        acronym="Isocortex",
        id="315",
    )
    KF = BrainStructureModel(
        atlas="CCFv3",
        name="Koelliker-Fuse subnucleus",
        acronym="KF",
        id="123",
    )
    LA = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral amygdalar nucleus",
        acronym="LA",
        id="131",
    )
    LD = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral dorsal nucleus of thalamus",
        acronym="LD",
        id="155",
    )
    LAT = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral group of the dorsal thalamus",
        acronym="LAT",
        id="138",
    )
    LH = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral habenula",
        acronym="LH",
        id="186",
    )
    LHA = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral hypothalamic area",
        acronym="LHA",
        id="194",
    )
    LM = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral mammillary nucleus",
        acronym="LM",
        id="210",
    )
    LP = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral posterior nucleus of the thalamus",
        acronym="LP",
        id="218",
    )
    LPO = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral preoptic area",
        acronym="LPO",
        id="226",
    )
    LRN = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral reticular nucleus",
        acronym="LRN",
        id="235",
    )
    LRNM = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral reticular nucleus, magnocellular part",
        acronym="LRNm",
        id="955",
    )
    LRNP = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral reticular nucleus, parvicellular part",
        acronym="LRNp",
        id="963",
    )
    LSX = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral septal complex",
        acronym="LSX",
        id="275",
    )
    LS = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral septal nucleus",
        acronym="LS",
        id="242",
    )
    LSC = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral septal nucleus, caudal (caudodorsal) part",
        acronym="LSc",
        id="250",
    )
    LSR = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral septal nucleus, rostral (rostroventral) part",
        acronym="LSr",
        id="258",
    )
    LSV = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral septal nucleus, ventral part",
        acronym="LSv",
        id="266",
    )
    LT = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral terminal nucleus of the accessory optic tract",
        acronym="LT",
        id="66",
    )
    LAV = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral vestibular nucleus",
        acronym="LAV",
        id="209",
    )
    VISL = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area",
        acronym="VISl",
        id="409",
    )
    VISL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 1",
        acronym="VISl1",
        id="421",
    )
    VISL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 2/3",
        acronym="VISl2/3",
        id="973",
    )
    VISL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 4",
        acronym="VISl4",
        id="573",
    )
    VISL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 5",
        acronym="VISl5",
        id="613",
    )
    VISL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 6a",
        acronym="VISl6a",
        id="74",
    )
    VISL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Lateral visual area, layer 6b",
        acronym="VISl6b",
        id="121",
    )
    LDT = BrainStructureModel(
        atlas="CCFv3",
        name="Laterodorsal tegmental nucleus",
        acronym="LDT",
        id="162",
    )
    VISLI = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area",
        acronym="VISli",
        id="312782574",
    )
    VISLI1 = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 1",
        acronym="VISli1",
        id="312782578",
    )
    VISLI2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 2/3",
        acronym="VISli2/3",
        id="312782582",
    )
    VISLI4 = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 4",
        acronym="VISli4",
        id="312782586",
    )
    VISLI5 = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 5",
        acronym="VISli5",
        id="312782590",
    )
    VISLI6A = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 6a",
        acronym="VISli6a",
        id="312782594",
    )
    VISLI6B = BrainStructureModel(
        atlas="CCFv3",
        name="Laterointermediate area, layer 6b",
        acronym="VISli6b",
        id="312782598",
    )
    LIN = BrainStructureModel(
        atlas="CCFv3",
        name="Linear nucleus of the medulla",
        acronym="LIN",
        id="203",
    )
    LING = BrainStructureModel(
        atlas="CCFv3",
        name="Lingula (I)",
        acronym="LING",
        id="912",
    )
    CENT2 = BrainStructureModel(
        atlas="CCFv3",
        name="Lobule II",
        acronym="CENT2",
        id="976",
    )
    CENT3 = BrainStructureModel(
        atlas="CCFv3",
        name="Lobule III",
        acronym="CENT3",
        id="984",
    )
    CUL4__5 = BrainStructureModel(
        atlas="CCFv3",
        name="Lobules IV-V",
        acronym="CUL4, 5",
        id="1091",
    )
    LC = BrainStructureModel(
        atlas="CCFv3",
        name="Locus ceruleus",
        acronym="LC",
        id="147",
    )
    MA = BrainStructureModel(
        atlas="CCFv3",
        name="Magnocellular nucleus",
        acronym="MA",
        id="298",
    )
    MARN = BrainStructureModel(
        atlas="CCFv3",
        name="Magnocellular reticular nucleus",
        acronym="MARN",
        id="307",
    )
    MOB = BrainStructureModel(
        atlas="CCFv3",
        name="Main olfactory bulb",
        acronym="MOB",
        id="507",
    )
    MBO = BrainStructureModel(
        atlas="CCFv3",
        name="Mammillary body",
        acronym="MBO",
        id="331",
    )
    MA3 = BrainStructureModel(
        atlas="CCFv3",
        name="Medial accesory oculomotor nucleus",
        acronym="MA3",
        id="549009211",
    )
    MEA = BrainStructureModel(
        atlas="CCFv3",
        name="Medial amygdalar nucleus",
        acronym="MEA",
        id="403",
    )
    MG = BrainStructureModel(
        atlas="CCFv3",
        name="Medial geniculate complex",
        acronym="MG",
        id="475",
    )
    MGD = BrainStructureModel(
        atlas="CCFv3",
        name="Medial geniculate complex, dorsal part",
        acronym="MGd",
        id="1072",
    )
    MGM = BrainStructureModel(
        atlas="CCFv3",
        name="Medial geniculate complex, medial part",
        acronym="MGm",
        id="1088",
    )
    MGV = BrainStructureModel(
        atlas="CCFv3",
        name="Medial geniculate complex, ventral part",
        acronym="MGv",
        id="1079",
    )
    MED = BrainStructureModel(
        atlas="CCFv3",
        name="Medial group of the dorsal thalamus",
        acronym="MED",
        id="444",
    )
    MH = BrainStructureModel(
        atlas="CCFv3",
        name="Medial habenula",
        acronym="MH",
        id="483",
    )
    MM = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus",
        acronym="MM",
        id="491",
    )
    MMD = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus, dorsal part",
        acronym="MMd",
        id="606826659",
    )
    MML = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus, lateral part",
        acronym="MMl",
        id="606826647",
    )
    MMM = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus, medial part",
        acronym="MMm",
        id="606826651",
    )
    MMME = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus, median part",
        acronym="MMme",
        id="732",
    )
    MMP = BrainStructureModel(
        atlas="CCFv3",
        name="Medial mammillary nucleus, posterior part",
        acronym="MMp",
        id="606826655",
    )
    MPO = BrainStructureModel(
        atlas="CCFv3",
        name="Medial preoptic area",
        acronym="MPO",
        id="523",
    )
    MPN = BrainStructureModel(
        atlas="CCFv3",
        name="Medial preoptic nucleus",
        acronym="MPN",
        id="515",
    )
    MPT = BrainStructureModel(
        atlas="CCFv3",
        name="Medial pretectal area",
        acronym="MPT",
        id="531",
    )
    MSC = BrainStructureModel(
        atlas="CCFv3",
        name="Medial septal complex",
        acronym="MSC",
        id="904",
    )
    MS = BrainStructureModel(
        atlas="CCFv3",
        name="Medial septal nucleus",
        acronym="MS",
        id="564",
    )
    MT = BrainStructureModel(
        atlas="CCFv3",
        name="Medial terminal nucleus of the accessory optic tract",
        acronym="MT",
        id="58",
    )
    MV = BrainStructureModel(
        atlas="CCFv3",
        name="Medial vestibular nucleus",
        acronym="MV",
        id="202",
    )
    ME = BrainStructureModel(
        atlas="CCFv3",
        name="Median eminence",
        acronym="ME",
        id="10671",
    )
    MEPO = BrainStructureModel(
        atlas="CCFv3",
        name="Median preoptic nucleus",
        acronym="MEPO",
        id="452",
    )
    MD = BrainStructureModel(
        atlas="CCFv3",
        name="Mediodorsal nucleus of thalamus",
        acronym="MD",
        id="362",
    )
    MY = BrainStructureModel(
        atlas="CCFv3",
        name="Medulla",
        acronym="MY",
        id="354",
    )
    MY_SAT = BrainStructureModel(
        atlas="CCFv3",
        name="Medulla, behavioral state related",
        acronym="MY-sat",
        id="379",
    )
    MY_MOT = BrainStructureModel(
        atlas="CCFv3",
        name="Medulla, motor related",
        acronym="MY-mot",
        id="370",
    )
    MY_SEN = BrainStructureModel(
        atlas="CCFv3",
        name="Medulla, sensory related",
        acronym="MY-sen",
        id="386",
    )
    MDRN = BrainStructureModel(
        atlas="CCFv3",
        name="Medullary reticular nucleus",
        acronym="MDRN",
        id="395",
    )
    MDRND = BrainStructureModel(
        atlas="CCFv3",
        name="Medullary reticular nucleus, dorsal part",
        acronym="MDRNd",
        id="1098",
    )
    MDRNV = BrainStructureModel(
        atlas="CCFv3",
        name="Medullary reticular nucleus, ventral part",
        acronym="MDRNv",
        id="1107",
    )
    MB = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain",
        acronym="MB",
        id="313",
    )
    RAMB = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain raphe nuclei",
        acronym="RAmb",
        id="165",
    )
    MRN = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain reticular nucleus",
        acronym="MRN",
        id="128",
    )
    RR = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain reticular nucleus, retrorubral area",
        acronym="RR",
        id="246",
    )
    MEV = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain trigeminal nucleus",
        acronym="MEV",
        id="460",
    )
    MBSTA = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain, behavioral state related",
        acronym="MBsta",
        id="348",
    )
    MBMOT = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain, motor related",
        acronym="MBmot",
        id="323",
    )
    MBSEN = BrainStructureModel(
        atlas="CCFv3",
        name="Midbrain, sensory related",
        acronym="MBsen",
        id="339",
    )
    MTN = BrainStructureModel(
        atlas="CCFv3",
        name="Midline group of the dorsal thalamus",
        acronym="MTN",
        id="571",
    )
    V = BrainStructureModel(
        atlas="CCFv3",
        name="Motor nucleus of trigeminal",
        acronym="V",
        id="621",
    )
    NOD = BrainStructureModel(
        atlas="CCFv3",
        name="Nodulus (X)",
        acronym="NOD",
        id="968",
    )
    ACB = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus accumbens",
        acronym="ACB",
        id="56",
    )
    AMB = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus ambiguus",
        acronym="AMB",
        id="135",
    )
    AMBD = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus ambiguus, dorsal division",
        acronym="AMBd",
        id="939",
    )
    AMBV = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus ambiguus, ventral division",
        acronym="AMBv",
        id="143",
    )
    NI = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus incertus",
        acronym="NI",
        id="604",
    )
    ND = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of Darkschewitsch",
        acronym="ND",
        id="587",
    )
    NR = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of Roller",
        acronym="NR",
        id="177",
    )
    RE = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of reuniens",
        acronym="RE",
        id="181",
    )
    NB = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the brachium of the inferior colliculus",
        acronym="NB",
        id="580",
    )
    NLL = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the lateral lemniscus",
        acronym="NLL",
        id="612",
    )
    NLOT = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the lateral olfactory tract",
        acronym="NLOT",
        id="619",
    )
    NLOT3 = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the lateral olfactory tract, layer 3",
        acronym="NLOT3",
        id="1139",
    )
    NLOT1 = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the lateral olfactory tract, molecular layer",
        acronym="NLOT1",
        id="260",
    )
    NLOT2 = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the lateral olfactory tract, pyramidal layer",
        acronym="NLOT2",
        id="268",
    )
    NOT = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the optic tract",
        acronym="NOT",
        id="628",
    )
    NPC = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the posterior commissure",
        acronym="NPC",
        id="634",
    )
    NTS = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the solitary tract",
        acronym="NTS",
        id="651",
    )
    NTB = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus of the trapezoid body",
        acronym="NTB",
        id="642",
    )
    PRP = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus prepositus",
        acronym="PRP",
        id="169",
    )
    RM = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus raphe magnus",
        acronym="RM",
        id="206",
    )
    RO = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus raphe obscurus",
        acronym="RO",
        id="222",
    )
    RPA = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus raphe pallidus",
        acronym="RPA",
        id="230",
    )
    RPO = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus raphe pontis",
        acronym="RPO",
        id="238",
    )
    SAG = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus sagulum",
        acronym="SAG",
        id="271",
    )
    X = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus x",
        acronym="x",
        id="765",
    )
    Y = BrainStructureModel(
        atlas="CCFv3",
        name="Nucleus y",
        acronym="y",
        id="781",
    )
    III = BrainStructureModel(
        atlas="CCFv3",
        name="Oculomotor nucleus",
        acronym="III",
        id="35",
    )
    OLF = BrainStructureModel(
        atlas="CCFv3",
        name="Olfactory areas",
        acronym="OLF",
        id="698",
    )
    OT = BrainStructureModel(
        atlas="CCFv3",
        name="Olfactory tubercle",
        acronym="OT",
        id="754",
    )
    OP = BrainStructureModel(
        atlas="CCFv3",
        name="Olivary pretectal nucleus",
        acronym="OP",
        id="706",
    )
    ORB = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area",
        acronym="ORB",
        id="714",
    )
    ORBL = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part",
        acronym="ORBl",
        id="723",
    )
    ORBL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part, layer 1",
        acronym="ORBl1",
        id="448",
    )
    ORBL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part, layer 2/3",
        acronym="ORBl2/3",
        id="412",
    )
    ORBL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part, layer 5",
        acronym="ORBl5",
        id="630",
    )
    ORBL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part, layer 6a",
        acronym="ORBl6a",
        id="440",
    )
    ORBL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, lateral part, layer 6b",
        acronym="ORBl6b",
        id="488",
    )
    ORBM = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part",
        acronym="ORBm",
        id="731",
    )
    ORBM1 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part, layer 1",
        acronym="ORBm1",
        id="484",
    )
    ORBM2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part, layer 2/3",
        acronym="ORBm2/3",
        id="582",
    )
    ORBM5 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part, layer 5",
        acronym="ORBm5",
        id="620",
    )
    ORBM6A = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part, layer 6a",
        acronym="ORBm6a",
        id="910",
    )
    ORBM6B = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, medial part, layer 6b",
        acronym="ORBm6b",
        id="527696977",
    )
    ORBVL = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part",
        acronym="ORBvl",
        id="746",
    )
    ORBVL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part, layer 1",
        acronym="ORBvl1",
        id="969",
    )
    ORBVL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part, layer 2/3",
        acronym="ORBvl2/3",
        id="288",
    )
    ORBVL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part, layer 5",
        acronym="ORBvl5",
        id="1125",
    )
    ORBVL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part, layer 6a",
        acronym="ORBvl6a",
        id="608",
    )
    ORBVL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Orbital area, ventrolateral part, layer 6b",
        acronym="ORBvl6b",
        id="680",
    )
    PAL = BrainStructureModel(
        atlas="CCFv3",
        name="Pallidum",
        acronym="PAL",
        id="803",
    )
    PALC = BrainStructureModel(
        atlas="CCFv3",
        name="Pallidum, caudal region",
        acronym="PALc",
        id="809",
    )
    PALD = BrainStructureModel(
        atlas="CCFv3",
        name="Pallidum, dorsal region",
        acronym="PALd",
        id="818",
    )
    PALM = BrainStructureModel(
        atlas="CCFv3",
        name="Pallidum, medial region",
        acronym="PALm",
        id="826",
    )
    PALV = BrainStructureModel(
        atlas="CCFv3",
        name="Pallidum, ventral region",
        acronym="PALv",
        id="835",
    )
    PBG = BrainStructureModel(
        atlas="CCFv3",
        name="Parabigeminal nucleus",
        acronym="PBG",
        id="874",
    )
    PB = BrainStructureModel(
        atlas="CCFv3",
        name="Parabrachial nucleus",
        acronym="PB",
        id="867",
    )
    PCN = BrainStructureModel(
        atlas="CCFv3",
        name="Paracentral nucleus",
        acronym="PCN",
        id="907",
    )
    PF = BrainStructureModel(
        atlas="CCFv3",
        name="Parafascicular nucleus",
        acronym="PF",
        id="930",
    )
    PFL = BrainStructureModel(
        atlas="CCFv3",
        name="Paraflocculus",
        acronym="PFL",
        id="1041",
    )
    PGRN = BrainStructureModel(
        atlas="CCFv3",
        name="Paragigantocellular reticular nucleus",
        acronym="PGRN",
        id="938",
    )
    PGRND = BrainStructureModel(
        atlas="CCFv3",
        name="Paragigantocellular reticular nucleus, dorsal part",
        acronym="PGRNd",
        id="970",
    )
    PGRNL = BrainStructureModel(
        atlas="CCFv3",
        name="Paragigantocellular reticular nucleus, lateral part",
        acronym="PGRNl",
        id="978",
    )
    PRM = BrainStructureModel(
        atlas="CCFv3",
        name="Paramedian lobule",
        acronym="PRM",
        id="1025",
    )
    PN = BrainStructureModel(
        atlas="CCFv3",
        name="Paranigral nucleus",
        acronym="PN",
        id="607344830",
    )
    PPY = BrainStructureModel(
        atlas="CCFv3",
        name="Parapyramidal nucleus",
        acronym="PPY",
        id="1069",
    )
    PAS = BrainStructureModel(
        atlas="CCFv3",
        name="Parasolitary nucleus",
        acronym="PAS",
        id="859",
    )
    PS = BrainStructureModel(
        atlas="CCFv3",
        name="Parastrial nucleus",
        acronym="PS",
        id="1109",
    )
    PAR = BrainStructureModel(
        atlas="CCFv3",
        name="Parasubiculum",
        acronym="PAR",
        id="843",
    )
    PSTN = BrainStructureModel(
        atlas="CCFv3",
        name="Parasubthalamic nucleus",
        acronym="PSTN",
        id="364",
    )
    PT = BrainStructureModel(
        atlas="CCFv3",
        name="Parataenial nucleus",
        acronym="PT",
        id="15",
    )
    PA5 = BrainStructureModel(
        atlas="CCFv3",
        name="Paratrigeminal nucleus",
        acronym="Pa5",
        id="589508451",
    )
    PA4 = BrainStructureModel(
        atlas="CCFv3",
        name="Paratrochlear nucleus",
        acronym="Pa4",
        id="606826663",
    )
    PVH = BrainStructureModel(
        atlas="CCFv3",
        name="Paraventricular hypothalamic nucleus",
        acronym="PVH",
        id="38",
    )
    PVHD = BrainStructureModel(
        atlas="CCFv3",
        name="Paraventricular hypothalamic nucleus, descending division",
        acronym="PVHd",
        id="63",
    )
    PVT = BrainStructureModel(
        atlas="CCFv3",
        name="Paraventricular nucleus of the thalamus",
        acronym="PVT",
        id="149",
    )
    PC5 = BrainStructureModel(
        atlas="CCFv3",
        name="Parvicellular motor 5 nucleus",
        acronym="PC5",
        id="549009223",
    )
    PARN = BrainStructureModel(
        atlas="CCFv3",
        name="Parvicellular reticular nucleus",
        acronym="PARN",
        id="852",
    )
    PPN = BrainStructureModel(
        atlas="CCFv3",
        name="Pedunculopontine nucleus",
        acronym="PPN",
        id="1052",
    )
    PAG = BrainStructureModel(
        atlas="CCFv3",
        name="Periaqueductal gray",
        acronym="PAG",
        id="795",
    )
    PEF = BrainStructureModel(
        atlas="CCFv3",
        name="Perifornical nucleus",
        acronym="PeF",
        id="576073704",
    )
    PHY = BrainStructureModel(
        atlas="CCFv3",
        name="Perihypoglossal nuclei",
        acronym="PHY",
        id="154",
    )
    PP = BrainStructureModel(
        atlas="CCFv3",
        name="Peripeduncular nucleus",
        acronym="PP",
        id="1044",
    )
    PR = BrainStructureModel(
        atlas="CCFv3",
        name="Perireunensis nucleus",
        acronym="PR",
        id="1077",
    )
    PERI = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area",
        acronym="PERI",
        id="922",
    )
    PERI1 = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area, layer 1",
        acronym="PERI1",
        id="540",
    )
    PERI2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area, layer 2/3",
        acronym="PERI2/3",
        id="888",
    )
    PERI5 = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area, layer 5",
        acronym="PERI5",
        id="692",
    )
    PERI6A = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area, layer 6a",
        acronym="PERI6a",
        id="335",
    )
    PERI6B = BrainStructureModel(
        atlas="CCFv3",
        name="Perirhinal area, layer 6b",
        acronym="PERI6b",
        id="368",
    )
    P5 = BrainStructureModel(
        atlas="CCFv3",
        name="Peritrigeminal zone",
        acronym="P5",
        id="549009215",
    )
    PVA = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular hypothalamic nucleus, anterior part",
        acronym="PVa",
        id="30",
    )
    PVI = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular hypothalamic nucleus, intermediate part",
        acronym="PVi",
        id="118",
    )
    PVP = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular hypothalamic nucleus, posterior part",
        acronym="PVp",
        id="126",
    )
    PVPO = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular hypothalamic nucleus, preoptic part",
        acronym="PVpo",
        id="133",
    )
    PVR = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular region",
        acronym="PVR",
        id="141",
    )
    PVZ = BrainStructureModel(
        atlas="CCFv3",
        name="Periventricular zone",
        acronym="PVZ",
        id="157",
    )
    PIR = BrainStructureModel(
        atlas="CCFv3",
        name="Piriform area",
        acronym="PIR",
        id="961",
    )
    PAA = BrainStructureModel(
        atlas="CCFv3",
        name="Piriform-amygdalar area",
        acronym="PAA",
        id="788",
    )
    P = BrainStructureModel(
        atlas="CCFv3",
        name="Pons",
        acronym="P",
        id="771",
    )
    P_SAT = BrainStructureModel(
        atlas="CCFv3",
        name="Pons, behavioral state related",
        acronym="P-sat",
        id="1117",
    )
    P_MOT = BrainStructureModel(
        atlas="CCFv3",
        name="Pons, motor related",
        acronym="P-mot",
        id="987",
    )
    P_SEN = BrainStructureModel(
        atlas="CCFv3",
        name="Pons, sensory related",
        acronym="P-sen",
        id="1132",
    )
    PCG = BrainStructureModel(
        atlas="CCFv3",
        name="Pontine central gray",
        acronym="PCG",
        id="898",
    )
    PG = BrainStructureModel(
        atlas="CCFv3",
        name="Pontine gray",
        acronym="PG",
        id="931",
    )
    PRNR = BrainStructureModel(
        atlas="CCFv3",
        name="Pontine reticular nucleus",
        acronym="PRNr",
        id="146",
    )
    PRNC = BrainStructureModel(
        atlas="CCFv3",
        name="Pontine reticular nucleus, caudal part",
        acronym="PRNc",
        id="1093",
    )
    PA = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior amygdalar nucleus",
        acronym="PA",
        id="780",
    )
    AUDPO = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area",
        acronym="AUDpo",
        id="1027",
    )
    AUDPO1 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 1",
        acronym="AUDpo1",
        id="696",
    )
    AUDPO2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 2/3",
        acronym="AUDpo2/3",
        id="643",
    )
    AUDPO4 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 4",
        acronym="AUDpo4",
        id="759",
    )
    AUDPO5 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 5",
        acronym="AUDpo5",
        id="791",
    )
    AUDPO6A = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 6a",
        acronym="AUDpo6a",
        id="249",
    )
    AUDPO6B = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior auditory area, layer 6b",
        acronym="AUDpo6b",
        id="456",
    )
    PO = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior complex of the thalamus",
        acronym="PO",
        id="1020",
    )
    PH = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior hypothalamic nucleus",
        acronym="PH",
        id="946",
    )
    PIL = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior intralaminar thalamic nucleus",
        acronym="PIL",
        id="560581563",
    )
    POL = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior limiting nucleus of the thalamus",
        acronym="POL",
        id="1029",
    )
    PTLP = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior parietal association areas",
        acronym="PTLp",
        id="22",
    )
    PPT = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior pretectal nucleus",
        acronym="PPT",
        id="1061",
    )
    POT = BrainStructureModel(
        atlas="CCFv3",
        name="Posterior triangular thalamic nucleus",
        acronym="PoT",
        id="563807435",
    )
    PD = BrainStructureModel(
        atlas="CCFv3",
        name="Posterodorsal preoptic nucleus",
        acronym="PD",
        id="914",
    )
    PDTG = BrainStructureModel(
        atlas="CCFv3",
        name="Posterodorsal tegmental nucleus",
        acronym="PDTg",
        id="599626927",
    )
    VISPL = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area",
        acronym="VISpl",
        id="425",
    )
    VISPL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 1",
        acronym="VISpl1",
        id="750",
    )
    VISPL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 2/3",
        acronym="VISpl2/3",
        id="269",
    )
    VISPL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 4",
        acronym="VISpl4",
        id="869",
    )
    VISPL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 5",
        acronym="VISpl5",
        id="902",
    )
    VISPL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 6a",
        acronym="VISpl6a",
        id="377",
    )
    VISPL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Posterolateral visual area, layer 6b",
        acronym="VISpl6b",
        id="393",
    )
    TR = BrainStructureModel(
        atlas="CCFv3",
        name="Postpiriform transition area",
        acronym="TR",
        id="566",
    )
    VISPOR = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area",
        acronym="VISpor",
        id="312782628",
    )
    VISPOR1 = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 1",
        acronym="VISpor1",
        id="312782632",
    )
    VISPOR2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 2/3",
        acronym="VISpor2/3",
        id="312782636",
    )
    VISPOR4 = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 4",
        acronym="VISpor4",
        id="312782640",
    )
    VISPOR5 = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 5",
        acronym="VISpor5",
        id="312782644",
    )
    VISPOR6A = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 6a",
        acronym="VISpor6a",
        id="312782648",
    )
    VISPOR6B = BrainStructureModel(
        atlas="CCFv3",
        name="Postrhinal area, layer 6b",
        acronym="VISpor6b",
        id="312782652",
    )
    POST = BrainStructureModel(
        atlas="CCFv3",
        name="Postsubiculum",
        acronym="POST",
        id="1037",
    )
    PRC = BrainStructureModel(
        atlas="CCFv3",
        name="Precommissural nucleus",
        acronym="PRC",
        id="50",
    )
    PL = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area",
        acronym="PL",
        id="972",
    )
    PL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area, layer 1",
        acronym="PL1",
        id="171",
    )
    PL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area, layer 2/3",
        acronym="PL2/3",
        id="304",
    )
    PL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area, layer 5",
        acronym="PL5",
        id="363",
    )
    PL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area, layer 6a",
        acronym="PL6a",
        id="84",
    )
    PL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Prelimbic area, layer 6b",
        acronym="PL6b",
        id="132",
    )
    PST = BrainStructureModel(
        atlas="CCFv3",
        name="Preparasubthalamic nucleus",
        acronym="PST",
        id="356",
    )
    PRE = BrainStructureModel(
        atlas="CCFv3",
        name="Presubiculum",
        acronym="PRE",
        id="1084",
    )
    PRT = BrainStructureModel(
        atlas="CCFv3",
        name="Pretectal region",
        acronym="PRT",
        id="1100",
    )
    AUDP = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area",
        acronym="AUDp",
        id="1002",
    )
    AUDP1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 1",
        acronym="AUDp1",
        id="735",
    )
    AUDP2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 2/3",
        acronym="AUDp2/3",
        id="251",
    )
    AUDP4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 4",
        acronym="AUDp4",
        id="816",
    )
    AUDP5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 5",
        acronym="AUDp5",
        id="847",
    )
    AUDP6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 6a",
        acronym="AUDp6a",
        id="954",
    )
    AUDP6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary auditory area, layer 6b",
        acronym="AUDp6b",
        id="1005",
    )
    MOP = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area",
        acronym="MOp",
        id="985",
    )
    MOP1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area, Layer 1",
        acronym="MOp1",
        id="320",
    )
    MOP2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area, Layer 2/3",
        acronym="MOp2/3",
        id="943",
    )
    MOP5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area, Layer 5",
        acronym="MOp5",
        id="648",
    )
    MOP6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area, Layer 6a",
        acronym="MOp6a",
        id="844",
    )
    MOP6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary motor area, Layer 6b",
        acronym="MOp6b",
        id="882",
    )
    SSP = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area",
        acronym="SSp",
        id="322",
    )
    SSP_BFD = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field",
        acronym="SSp-bfd",
        id="329",
    )
    SSP_BFD1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 1",
        acronym="SSp-bfd1",
        id="981",
    )
    SSP_BFD2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 2/3",
        acronym="SSp-bfd2/3",
        id="201",
    )
    SSP_BFD4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 4",
        acronym="SSp-bfd4",
        id="1047",
    )
    SSP_BFD5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 5",
        acronym="SSp-bfd5",
        id="1070",
    )
    SSP_BFD6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 6a",
        acronym="SSp-bfd6a",
        id="1038",
    )
    SSP_BFD6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, barrel field, layer 6b",
        acronym="SSp-bfd6b",
        id="1062",
    )
    SSP_LL = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb",
        acronym="SSp-ll",
        id="337",
    )
    SSP_LL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 1",
        acronym="SSp-ll1",
        id="1030",
    )
    SSP_LL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 2/3",
        acronym="SSp-ll2/3",
        id="113",
    )
    SSP_LL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 4",
        acronym="SSp-ll4",
        id="1094",
    )
    SSP_LL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 5",
        acronym="SSp-ll5",
        id="1128",
    )
    SSP_LL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 6a",
        acronym="SSp-ll6a",
        id="478",
    )
    SSP_LL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, lower limb, layer 6b",
        acronym="SSp-ll6b",
        id="510",
    )
    SSP_M = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth",
        acronym="SSp-m",
        id="345",
    )
    SSP_M1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 1",
        acronym="SSp-m1",
        id="878",
    )
    SSP_M2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 2/3",
        acronym="SSp-m2/3",
        id="657",
    )
    SSP_M4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 4",
        acronym="SSp-m4",
        id="950",
    )
    SSP_M5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 5",
        acronym="SSp-m5",
        id="974",
    )
    SSP_M6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 6a",
        acronym="SSp-m6a",
        id="1102",
    )
    SSP_M6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, mouth, layer 6b",
        acronym="SSp-m6b",
        id="2",
    )
    SSP_N = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose",
        acronym="SSp-n",
        id="353",
    )
    SSP_N1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 1",
        acronym="SSp-n1",
        id="558",
    )
    SSP_N2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 2/3",
        acronym="SSp-n2/3",
        id="838",
    )
    SSP_N4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 4",
        acronym="SSp-n4",
        id="654",
    )
    SSP_N5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 5",
        acronym="SSp-n5",
        id="702",
    )
    SSP_N6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 6a",
        acronym="SSp-n6a",
        id="889",
    )
    SSP_N6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, nose, layer 6b",
        acronym="SSp-n6b",
        id="929",
    )
    SSP_TR = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk",
        acronym="SSp-tr",
        id="361",
    )
    SSP_TR1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 1",
        acronym="SSp-tr1",
        id="1006",
    )
    SSP_TR2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 2/3",
        acronym="SSp-tr2/3",
        id="670",
    )
    SSP_TR4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 4",
        acronym="SSp-tr4",
        id="1086",
    )
    SSP_TR5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 5",
        acronym="SSp-tr5",
        id="1111",
    )
    SSP_TR6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 6a",
        acronym="SSp-tr6a",
        id="9",
    )
    SSP_TR6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, trunk, layer 6b",
        acronym="SSp-tr6b",
        id="461",
    )
    SSP_UN = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned",
        acronym="SSp-un",
        id="182305689",
    )
    SSP_UN1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 1",
        acronym="SSp-un1",
        id="182305693",
    )
    SSP_UN2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 2/3",
        acronym="SSp-un2/3",
        id="182305697",
    )
    SSP_UN4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 4",
        acronym="SSp-un4",
        id="182305701",
    )
    SSP_UN5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 5",
        acronym="SSp-un5",
        id="182305705",
    )
    SSP_UN6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 6a",
        acronym="SSp-un6a",
        id="182305709",
    )
    SSP_UN6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, unassigned, layer 6b",
        acronym="SSp-un6b",
        id="182305713",
    )
    SSP_UL = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb",
        acronym="SSp-ul",
        id="369",
    )
    SSP_UL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 1",
        acronym="SSp-ul1",
        id="450",
    )
    SSP_UL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 2/3",
        acronym="SSp-ul2/3",
        id="854",
    )
    SSP_UL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 4",
        acronym="SSp-ul4",
        id="577",
    )
    SSP_UL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 5",
        acronym="SSp-ul5",
        id="625",
    )
    SSP_UL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 6a",
        acronym="SSp-ul6a",
        id="945",
    )
    SSP_UL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary somatosensory area, upper limb, layer 6b",
        acronym="SSp-ul6b",
        id="1026",
    )
    VISP = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area",
        acronym="VISp",
        id="385",
    )
    VISP1 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 1",
        acronym="VISp1",
        id="593",
    )
    VISP2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 2/3",
        acronym="VISp2/3",
        id="821",
    )
    VISP4 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 4",
        acronym="VISp4",
        id="721",
    )
    VISP5 = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 5",
        acronym="VISp5",
        id="778",
    )
    VISP6A = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 6a",
        acronym="VISp6a",
        id="33",
    )
    VISP6B = BrainStructureModel(
        atlas="CCFv3",
        name="Primary visual area, layer 6b",
        acronym="VISp6b",
        id="305",
    )
    PSV = BrainStructureModel(
        atlas="CCFv3",
        name="Principal sensory nucleus of the trigeminal",
        acronym="PSV",
        id="7",
    )
    PROS = BrainStructureModel(
        atlas="CCFv3",
        name="Prosubiculum",
        acronym="ProS",
        id="484682470",
    )
    PYR = BrainStructureModel(
        atlas="CCFv3",
        name="Pyramus (VIII)",
        acronym="PYR",
        id="951",
    )
    RN = BrainStructureModel(
        atlas="CCFv3",
        name="Red nucleus",
        acronym="RN",
        id="214",
    )
    RT = BrainStructureModel(
        atlas="CCFv3",
        name="Reticular nucleus of the thalamus",
        acronym="RT",
        id="262",
    )
    RCH = BrainStructureModel(
        atlas="CCFv3",
        name="Retrochiasmatic area",
        acronym="RCH",
        id="173",
    )
    RHP = BrainStructureModel(
        atlas="CCFv3",
        name="Retrohippocampal region",
        acronym="RHP",
        id="822",
    )
    RPF = BrainStructureModel(
        atlas="CCFv3",
        name="Retroparafascicular nucleus",
        acronym="RPF",
        id="549009203",
    )
    RSP = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area",
        acronym="RSP",
        id="254",
    )
    RSPD = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part",
        acronym="RSPd",
        id="879",
    )
    RSPD1 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 1",
        acronym="RSPd1",
        id="442",
    )
    RSPD2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 2/3",
        acronym="RSPd2/3",
        id="434",
    )
    RSPD4 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 4",
        acronym="RSPd4",
        id="545",
    )
    RSPD5 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 5",
        acronym="RSPd5",
        id="610",
    )
    RSPD6A = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 6a",
        acronym="RSPd6a",
        id="274",
    )
    RSPD6B = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, dorsal part, layer 6b",
        acronym="RSPd6b",
        id="330",
    )
    RSPAGL = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part",
        acronym="RSPagl",
        id="894",
    )
    RSPAGL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part, layer 1",
        acronym="RSPagl1",
        id="671",
    )
    RSPAGL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part, layer 2/3",
        acronym="RSPagl2/3",
        id="965",
    )
    RSPAGL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part, layer 5",
        acronym="RSPagl5",
        id="774",
    )
    RSPAGL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part, layer 6a",
        acronym="RSPagl6a",
        id="906",
    )
    RSPAGL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, lateral agranular part, layer 6b",
        acronym="RSPagl6b",
        id="279",
    )
    RSPV = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part",
        acronym="RSPv",
        id="886",
    )
    RSPV1 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part, layer 1",
        acronym="RSPv1",
        id="542",
    )
    RSPV2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part, layer 2/3",
        acronym="RSPv2/3",
        id="430",
    )
    RSPV5 = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part, layer 5",
        acronym="RSPv5",
        id="687",
    )
    RSPV6A = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part, layer 6a",
        acronym="RSPv6a",
        id="590",
    )
    RSPV6B = BrainStructureModel(
        atlas="CCFv3",
        name="Retrosplenial area, ventral part, layer 6b",
        acronym="RSPv6b",
        id="622",
    )
    RH = BrainStructureModel(
        atlas="CCFv3",
        name="Rhomboid nucleus",
        acronym="RH",
        id="189",
    )
    RL = BrainStructureModel(
        atlas="CCFv3",
        name="Rostral linear nucleus raphe",
        acronym="RL",
        id="197",
    )
    VISRL1 = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 1",
        acronym="VISrl1",
        id="312782604",
    )
    VISRL2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 2/3",
        acronym="VISrl2/3",
        id="312782608",
    )
    VISRL4 = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 4",
        acronym="VISrl4",
        id="312782612",
    )
    VISRL5 = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 5",
        acronym="VISrl5",
        id="312782616",
    )
    VISRL6A = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 6a",
        acronym="VISrl6a",
        id="312782620",
    )
    VISRL6B = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral area, layer 6b",
        acronym="VISrl6b",
        id="312782624",
    )
    VISRL = BrainStructureModel(
        atlas="CCFv3",
        name="Rostrolateral visual area",
        acronym="VISrl",
        id="417",
    )
    MOS = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area",
        acronym="MOs",
        id="993",
    )
    MOS1 = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area, layer 1",
        acronym="MOs1",
        id="656",
    )
    MOS2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area, layer 2/3",
        acronym="MOs2/3",
        id="962",
    )
    MOS5 = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area, layer 5",
        acronym="MOs5",
        id="767",
    )
    MOS6A = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area, layer 6a",
        acronym="MOs6a",
        id="1021",
    )
    MOS6B = BrainStructureModel(
        atlas="CCFv3",
        name="Secondary motor area, layer 6b",
        acronym="MOs6b",
        id="1085",
    )
    SF = BrainStructureModel(
        atlas="CCFv3",
        name="Septofimbrial nucleus",
        acronym="SF",
        id="310",
    )
    SH = BrainStructureModel(
        atlas="CCFv3",
        name="Septohippocampal nucleus",
        acronym="SH",
        id="333",
    )
    SIM = BrainStructureModel(
        atlas="CCFv3",
        name="Simple lobule",
        acronym="SIM",
        id="1007",
    )
    MO = BrainStructureModel(
        atlas="CCFv3",
        name="Somatomotor areas",
        acronym="MO",
        id="500",
    )
    SS = BrainStructureModel(
        atlas="CCFv3",
        name="Somatosensory areas",
        acronym="SS",
        id="453",
    )
    SPVC = BrainStructureModel(
        atlas="CCFv3",
        name="Spinal nucleus of the trigeminal, caudal part",
        acronym="SPVC",
        id="429",
    )
    SPVI = BrainStructureModel(
        atlas="CCFv3",
        name="Spinal nucleus of the trigeminal, interpolar part",
        acronym="SPVI",
        id="437",
    )
    SPVO = BrainStructureModel(
        atlas="CCFv3",
        name="Spinal nucleus of the trigeminal, oral part",
        acronym="SPVO",
        id="445",
    )
    SPIV = BrainStructureModel(
        atlas="CCFv3",
        name="Spinal vestibular nucleus",
        acronym="SPIV",
        id="225",
    )
    STR = BrainStructureModel(
        atlas="CCFv3",
        name="Striatum",
        acronym="STR",
        id="477",
    )
    STRD = BrainStructureModel(
        atlas="CCFv3",
        name="Striatum dorsal region",
        acronym="STRd",
        id="485",
    )
    STRV = BrainStructureModel(
        atlas="CCFv3",
        name="Striatum ventral region",
        acronym="STRv",
        id="493",
    )
    SAMY = BrainStructureModel(
        atlas="CCFv3",
        name="Striatum-like amygdalar nuclei",
        acronym="sAMY",
        id="278",
    )
    SLC = BrainStructureModel(
        atlas="CCFv3",
        name="Subceruleus nucleus",
        acronym="SLC",
        id="350",
    )
    SCO = BrainStructureModel(
        atlas="CCFv3",
        name="Subcommissural organ",
        acronym="SCO",
        id="599626923",
    )
    SFO = BrainStructureModel(
        atlas="CCFv3",
        name="Subfornical organ",
        acronym="SFO",
        id="338",
    )
    SUBG = BrainStructureModel(
        atlas="CCFv3",
        name="Subgeniculate nucleus",
        acronym="SubG",
        id="321",
    )
    SUB = BrainStructureModel(
        atlas="CCFv3",
        name="Subiculum",
        acronym="SUB",
        id="502",
    )
    SLD = BrainStructureModel(
        atlas="CCFv3",
        name="Sublaterodorsal nucleus",
        acronym="SLD",
        id="358",
    )
    SMT = BrainStructureModel(
        atlas="CCFv3",
        name="Submedial nucleus of the thalamus",
        acronym="SMT",
        id="366",
    )
    SPA = BrainStructureModel(
        atlas="CCFv3",
        name="Subparafascicular area",
        acronym="SPA",
        id="609",
    )
    SPF = BrainStructureModel(
        atlas="CCFv3",
        name="Subparafascicular nucleus",
        acronym="SPF",
        id="406",
    )
    SPFM = BrainStructureModel(
        atlas="CCFv3",
        name="Subparafascicular nucleus, magnocellular part",
        acronym="SPFm",
        id="414",
    )
    SPFP = BrainStructureModel(
        atlas="CCFv3",
        name="Subparafascicular nucleus, parvicellular part",
        acronym="SPFp",
        id="422",
    )
    SBPV = BrainStructureModel(
        atlas="CCFv3",
        name="Subparaventricular zone",
        acronym="SBPV",
        id="347",
    )
    SI = BrainStructureModel(
        atlas="CCFv3",
        name="Substantia innominata",
        acronym="SI",
        id="342",
    )
    SNC = BrainStructureModel(
        atlas="CCFv3",
        name="Substantia nigra, compact part",
        acronym="SNc",
        id="374",
    )
    SNR = BrainStructureModel(
        atlas="CCFv3",
        name="Substantia nigra, reticular part",
        acronym="SNr",
        id="381",
    )
    STN = BrainStructureModel(
        atlas="CCFv3",
        name="Subthalamic nucleus",
        acronym="STN",
        id="470",
    )
    CS = BrainStructureModel(
        atlas="CCFv3",
        name="Superior central nucleus raphe",
        acronym="CS",
        id="679",
    )
    SCM = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, motor related",
        acronym="SCm",
        id="294",
    )
    SCDG = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, motor related, deep gray layer",
        acronym="SCdg",
        id="26",
    )
    SCDW = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, motor related, deep white layer",
        acronym="SCdw",
        id="42",
    )
    SCIG = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, motor related, intermediate gray layer",
        acronym="SCig",
        id="10",
    )
    SCIW = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, motor related, intermediate white layer",
        acronym="SCiw",
        id="17",
    )
    SCOP = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, optic layer",
        acronym="SCop",
        id="851",
    )
    SCS = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, sensory related",
        acronym="SCs",
        id="302",
    )
    SCSG = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, superficial gray layer",
        acronym="SCsg",
        id="842",
    )
    SCZO = BrainStructureModel(
        atlas="CCFv3",
        name="Superior colliculus, zonal layer",
        acronym="SCzo",
        id="834",
    )
    SOC = BrainStructureModel(
        atlas="CCFv3",
        name="Superior olivary complex",
        acronym="SOC",
        id="398",
    )
    SOCL = BrainStructureModel(
        atlas="CCFv3",
        name="Superior olivary complex, lateral part",
        acronym="SOCl",
        id="114",
    )
    SOCM = BrainStructureModel(
        atlas="CCFv3",
        name="Superior olivary complex, medial part",
        acronym="SOCm",
        id="105",
    )
    POR = BrainStructureModel(
        atlas="CCFv3",
        name="Superior olivary complex, periolivary region",
        acronym="POR",
        id="122",
    )
    SUV = BrainStructureModel(
        atlas="CCFv3",
        name="Superior vestibular nucleus",
        acronym="SUV",
        id="217",
    )
    SSS = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area",
        acronym="SSs",
        id="378",
    )
    SSS1 = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 1",
        acronym="SSs1",
        id="873",
    )
    SSS2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 2/3",
        acronym="SSs2/3",
        id="806",
    )
    SSS4 = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 4",
        acronym="SSs4",
        id="1035",
    )
    SSS5 = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 5",
        acronym="SSs5",
        id="1090",
    )
    SSS6A = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 6a",
        acronym="SSs6a",
        id="862",
    )
    SSS6B = BrainStructureModel(
        atlas="CCFv3",
        name="Supplemental somatosensory area, layer 6b",
        acronym="SSs6b",
        id="893",
    )
    SCH = BrainStructureModel(
        atlas="CCFv3",
        name="Suprachiasmatic nucleus",
        acronym="SCH",
        id="286",
    )
    SGN = BrainStructureModel(
        atlas="CCFv3",
        name="Suprageniculate nucleus",
        acronym="SGN",
        id="325",
    )
    SG = BrainStructureModel(
        atlas="CCFv3",
        name="Supragenual nucleus",
        acronym="SG",
        id="318",
    )
    SUM = BrainStructureModel(
        atlas="CCFv3",
        name="Supramammillary nucleus",
        acronym="SUM",
        id="525",
    )
    SU3 = BrainStructureModel(
        atlas="CCFv3",
        name="Supraoculomotor periaqueductal gray",
        acronym="Su3",
        id="614454277",
    )
    SO = BrainStructureModel(
        atlas="CCFv3",
        name="Supraoptic nucleus",
        acronym="SO",
        id="390",
    )
    SUT = BrainStructureModel(
        atlas="CCFv3",
        name="Supratrigeminal nucleus",
        acronym="SUT",
        id="534",
    )
    TT = BrainStructureModel(
        atlas="CCFv3",
        name="Taenia tecta",
        acronym="TT",
        id="589",
    )
    TTD = BrainStructureModel(
        atlas="CCFv3",
        name="Taenia tecta, dorsal part",
        acronym="TTd",
        id="597",
    )
    TTV = BrainStructureModel(
        atlas="CCFv3",
        name="Taenia tecta, ventral part",
        acronym="TTv",
        id="605",
    )
    TRN = BrainStructureModel(
        atlas="CCFv3",
        name="Tegmental reticular nucleus",
        acronym="TRN",
        id="574",
    )
    TEA = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas",
        acronym="TEa",
        id="541",
    )
    TEA1 = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 1",
        acronym="TEa1",
        id="97",
    )
    TEA2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 2/3",
        acronym="TEa2/3",
        id="1127",
    )
    TEA4 = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 4",
        acronym="TEa4",
        id="234",
    )
    TEA5 = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 5",
        acronym="TEa5",
        id="289",
    )
    TEA6A = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 6a",
        acronym="TEa6a",
        id="729",
    )
    TEA6B = BrainStructureModel(
        atlas="CCFv3",
        name="Temporal association areas, layer 6b",
        acronym="TEa6b",
        id="786",
    )
    TH = BrainStructureModel(
        atlas="CCFv3",
        name="Thalamus",
        acronym="TH",
        id="549",
    )
    DORPM = BrainStructureModel(
        atlas="CCFv3",
        name="Thalamus, polymodal association cortex related",
        acronym="DORpm",
        id="856",
    )
    DORSM = BrainStructureModel(
        atlas="CCFv3",
        name="Thalamus, sensory-motor cortex related",
        acronym="DORsm",
        id="864",
    )
    TRS = BrainStructureModel(
        atlas="CCFv3",
        name="Triangular nucleus of septum",
        acronym="TRS",
        id="581",
    )
    IV = BrainStructureModel(
        atlas="CCFv3",
        name="Trochlear nucleus",
        acronym="IV",
        id="115",
    )
    TU = BrainStructureModel(
        atlas="CCFv3",
        name="Tuberal nucleus",
        acronym="TU",
        id="614",
    )
    TM = BrainStructureModel(
        atlas="CCFv3",
        name="Tuberomammillary nucleus",
        acronym="TM",
        id="557",
    )
    TMD = BrainStructureModel(
        atlas="CCFv3",
        name="Tuberomammillary nucleus, dorsal part",
        acronym="TMd",
        id="1126",
    )
    TMV = BrainStructureModel(
        atlas="CCFv3",
        name="Tuberomammillary nucleus, ventral part",
        acronym="TMv",
        id="1",
    )
    UVU = BrainStructureModel(
        atlas="CCFv3",
        name="Uvula (IX)",
        acronym="UVU",
        id="957",
    )
    OV = BrainStructureModel(
        atlas="CCFv3",
        name="Vascular organ of the lamina terminalis",
        acronym="OV",
        id="763",
    )
    VAL = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral anterior-lateral complex of the thalamus",
        acronym="VAL",
        id="629",
    )
    AUDV = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area",
        acronym="AUDv",
        id="1018",
    )
    AUDV1 = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 1",
        acronym="AUDv1",
        id="959",
    )
    AUDV2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 2/3",
        acronym="AUDv2/3",
        id="755",
    )
    AUDV4 = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 4",
        acronym="AUDv4",
        id="990",
    )
    AUDV5 = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 5",
        acronym="AUDv5",
        id="1023",
    )
    AUDV6A = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 6a",
        acronym="AUDv6a",
        id="520",
    )
    AUDV6B = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral auditory area, layer 6b",
        acronym="AUDv6b",
        id="598",
    )
    VCO = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral cochlear nucleus",
        acronym="VCO",
        id="101",
    )
    VENT = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral group of the dorsal thalamus",
        acronym="VENT",
        id="637",
    )
    VM = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral medial nucleus of the thalamus",
        acronym="VM",
        id="685",
    )
    LGV = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral part of the lateral geniculate complex",
        acronym="LGv",
        id="178",
    )
    VP = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral posterior complex of the thalamus",
        acronym="VP",
        id="709",
    )
    VPL = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral posterolateral nucleus of the thalamus",
        acronym="VPL",
        id="718",
    )
    VPLPC = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral posterolateral nucleus of the thalamus, parvicellular part",
        acronym="VPLpc",
        id="725",
    )
    VPM = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral posteromedial nucleus of the thalamus",
        acronym="VPM",
        id="733",
    )
    VPMPC = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral posteromedial nucleus of the thalamus, parvicellular part",
        acronym="VPMpc",
        id="741",
    )
    PMV = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral premammillary nucleus",
        acronym="PMv",
        id="1004",
    )
    VTA = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral tegmental area",
        acronym="VTA",
        id="749",
    )
    VTN = BrainStructureModel(
        atlas="CCFv3",
        name="Ventral tegmental nucleus",
        acronym="VTN",
        id="757",
    )
    VLPO = BrainStructureModel(
        atlas="CCFv3",
        name="Ventrolateral preoptic nucleus",
        acronym="VLPO",
        id="689",
    )
    VMH = BrainStructureModel(
        atlas="CCFv3",
        name="Ventromedial hypothalamic nucleus",
        acronym="VMH",
        id="693",
    )
    VMPO = BrainStructureModel(
        atlas="CCFv3",
        name="Ventromedial preoptic nucleus",
        acronym="VMPO",
        id="576073699",
    )
    VERM = BrainStructureModel(
        atlas="CCFv3",
        name="Vermal regions",
        acronym="VERM",
        id="645",
    )
    VNC = BrainStructureModel(
        atlas="CCFv3",
        name="Vestibular nuclei",
        acronym="VNC",
        id="701",
    )
    VECB = BrainStructureModel(
        atlas="CCFv3",
        name="Vestibulocerebellar nucleus",
        acronym="VeCB",
        id="589508455",
    )
    VISC = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area",
        acronym="VISC",
        id="677",
    )
    VISC1 = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 1",
        acronym="VISC1",
        id="897",
    )
    VISC2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 2/3",
        acronym="VISC2/3",
        id="1106",
    )
    VISC4 = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 4",
        acronym="VISC4",
        id="1010",
    )
    VISC5 = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 5",
        acronym="VISC5",
        id="1058",
    )
    VISC6A = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 6a",
        acronym="VISC6a",
        id="857",
    )
    VISC6B = BrainStructureModel(
        atlas="CCFv3",
        name="Visceral area, layer 6b",
        acronym="VISC6b",
        id="849",
    )
    VIS = BrainStructureModel(
        atlas="CCFv3",
        name="Visual areas",
        acronym="VIS",
        id="669",
    )
    XI = BrainStructureModel(
        atlas="CCFv3",
        name="Xiphoid thalamic nucleus",
        acronym="Xi",
        id="560581559",
    )
    ZI = BrainStructureModel(
        atlas="CCFv3",
        name="Zona incerta",
        acronym="ZI",
        id="797",
    )
    ALV = BrainStructureModel(
        atlas="CCFv3",
        name="alveus",
        acronym="alv",
        id="466",
    )
    AMC = BrainStructureModel(
        atlas="CCFv3",
        name="amygdalar capsule",
        acronym="amc",
        id="884",
    )
    ACO = BrainStructureModel(
        atlas="CCFv3",
        name="anterior commissure, olfactory limb",
        acronym="aco",
        id="900",
    )
    ACT = BrainStructureModel(
        atlas="CCFv3",
        name="anterior commissure, temporal limb",
        acronym="act",
        id="908",
    )
    ARB = BrainStructureModel(
        atlas="CCFv3",
        name="arbor vitae",
        acronym="arb",
        id="728",
    )
    AR = BrainStructureModel(
        atlas="CCFv3",
        name="auditory radiation",
        acronym="ar",
        id="484682524",
    )
    BIC = BrainStructureModel(
        atlas="CCFv3",
        name="brachium of the inferior colliculus",
        acronym="bic",
        id="482",
    )
    BSC = BrainStructureModel(
        atlas="CCFv3",
        name="brachium of the superior colliculus",
        acronym="bsc",
        id="916",
    )
    C = BrainStructureModel(
        atlas="CCFv3",
        name="central canal, spinal cord/medulla",
        acronym="c",
        id="164",
    )
    CPD = BrainStructureModel(
        atlas="CCFv3",
        name="cerebal peduncle",
        acronym="cpd",
        id="924",
    )
    CBC = BrainStructureModel(
        atlas="CCFv3",
        name="cerebellar commissure",
        acronym="cbc",
        id="744",
    )
    CBP = BrainStructureModel(
        atlas="CCFv3",
        name="cerebellar peduncles",
        acronym="cbp",
        id="752",
    )
    CBF = BrainStructureModel(
        atlas="CCFv3",
        name="cerebellum related fiber tracts",
        acronym="cbf",
        id="960",
    )
    AQ = BrainStructureModel(
        atlas="CCFv3",
        name="cerebral aqueduct",
        acronym="AQ",
        id="140",
    )
    EPSC = BrainStructureModel(
        atlas="CCFv3",
        name="cerebral nuclei related",
        acronym="epsc",
        id="760",
    )
    MFBC = BrainStructureModel(
        atlas="CCFv3",
        name="cerebrum related",
        acronym="mfbc",
        id="768",
    )
    CETT = BrainStructureModel(
        atlas="CCFv3",
        name="cervicothalamic tract",
        acronym="cett",
        id="932",
    )
    CHPL = BrainStructureModel(
        atlas="CCFv3",
        name="choroid plexus",
        acronym="chpl",
        id="108",
    )
    CING = BrainStructureModel(
        atlas="CCFv3",
        name="cingulum bundle",
        acronym="cing",
        id="940",
    )
    CVIIIN = BrainStructureModel(
        atlas="CCFv3",
        name="cochlear nerve",
        acronym="cVIIIn",
        id="948",
    )
    FX = BrainStructureModel(
        atlas="CCFv3",
        name="columns of the fornix",
        acronym="fx",
        id="436",
    )
    STC = BrainStructureModel(
        atlas="CCFv3",
        name="commissural branch of stria terminalis",
        acronym="stc",
        id="484682528",
    )
    CC = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum",
        acronym="cc",
        id="776",
    )
    FA = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum, anterior forceps",
        acronym="fa",
        id="956",
    )
    CCB = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum, body",
        acronym="ccb",
        id="484682516",
    )
    EE = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum, extreme capsule",
        acronym="ee",
        id="964",
    )
    FP = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum, posterior forceps",
        acronym="fp",
        id="971",
    )
    CCS = BrainStructureModel(
        atlas="CCFv3",
        name="corpus callosum, splenium",
        acronym="ccs",
        id="986",
    )
    CST = BrainStructureModel(
        atlas="CCFv3",
        name="corticospinal tract",
        acronym="cst",
        id="784",
    )
    CNE = BrainStructureModel(
        atlas="CCFv3",
        name="cranial nerves",
        acronym="cne",
        id="967",
    )
    TSPC = BrainStructureModel(
        atlas="CCFv3",
        name="crossed tectospinal pathway",
        acronym="tspc",
        id="1043",
    )
    CUF = BrainStructureModel(
        atlas="CCFv3",
        name="cuneate fascicle",
        acronym="cuf",
        id="380",
    )
    TSPD = BrainStructureModel(
        atlas="CCFv3",
        name="direct tectospinal pathway",
        acronym="tspd",
        id="1051",
    )
    DTD = BrainStructureModel(
        atlas="CCFv3",
        name="doral tegmental decussation",
        acronym="dtd",
        id="1060",
    )
    DAS = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal acoustic stria",
        acronym="das",
        id="506",
    )
    DC = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal column",
        acronym="dc",
        id="514",
    )
    DF = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal fornix",
        acronym="df",
        id="530",
    )
    DHC = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal hippocampal commissure",
        acronym="dhc",
        id="443",
    )
    LOTD = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal limb",
        acronym="lotd",
        id="538",
    )
    DRT = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal roots",
        acronym="drt",
        id="792",
    )
    SCTD = BrainStructureModel(
        atlas="CCFv3",
        name="dorsal spinocerebellar tract",
        acronym="sctd",
        id="553",
    )
    MFBSE = BrainStructureModel(
        atlas="CCFv3",
        name="epithalamus related",
        acronym="mfbse",
        id="1083",
    )
    EC = BrainStructureModel(
        atlas="CCFv3",
        name="external capsule",
        acronym="ec",
        id="579",
    )
    EM = BrainStructureModel(
        atlas="CCFv3",
        name="external medullary lamina of the thalamus",
        acronym="em",
        id="1092",
    )
    EPS = BrainStructureModel(
        atlas="CCFv3",
        name="extrapyramidal fiber systems",
        acronym="eps",
        id="1000",
    )
    VIIN = BrainStructureModel(
        atlas="CCFv3",
        name="facial nerve",
        acronym="VIIn",
        id="798",
    )
    FR = BrainStructureModel(
        atlas="CCFv3",
        name="fasciculus retroflexus",
        acronym="fr",
        id="595",
    )
    FIBER_TRACTS = BrainStructureModel(
        atlas="CCFv3",
        name="fiber tracts",
        acronym="fiber tracts",
        id="1009",
    )
    FI = BrainStructureModel(
        atlas="CCFv3",
        name="fimbria",
        acronym="fi",
        id="603",
    )
    FXS = BrainStructureModel(
        atlas="CCFv3",
        name="fornix system",
        acronym="fxs",
        id="1099",
    )
    V4 = BrainStructureModel(
        atlas="CCFv3",
        name="fourth ventricle",
        acronym="V4",
        id="145",
    )
    CCG = BrainStructureModel(
        atlas="CCFv3",
        name="genu of corpus callosum",
        acronym="ccg",
        id="1108",
    )
    GVIIN = BrainStructureModel(
        atlas="CCFv3",
        name="genu of the facial nerve",
        acronym="gVIIn",
        id="1116",
    )
    HBC = BrainStructureModel(
        atlas="CCFv3",
        name="habenular commissure",
        acronym="hbc",
        id="611",
    )
    HC = BrainStructureModel(
        atlas="CCFv3",
        name="hippocampal commissures",
        acronym="hc",
        id="618",
    )
    MFSBSHY = BrainStructureModel(
        atlas="CCFv3",
        name="hypothalamus related",
        acronym="mfsbshy",
        id="824",
    )
    ICP = BrainStructureModel(
        atlas="CCFv3",
        name="inferior cerebellar peduncle",
        acronym="icp",
        id="1123",
    )
    CIC = BrainStructureModel(
        atlas="CCFv3",
        name="inferior colliculus commissure",
        acronym="cic",
        id="633",
    )
    INT = BrainStructureModel(
        atlas="CCFv3",
        name="internal capsule",
        acronym="int",
        id="6",
    )
    LFBS = BrainStructureModel(
        atlas="CCFv3",
        name="lateral forebrain bundle system",
        acronym="lfbs",
        id="983",
    )
    LL = BrainStructureModel(
        atlas="CCFv3",
        name="lateral lemniscus",
        acronym="ll",
        id="658",
    )
    LOT = BrainStructureModel(
        atlas="CCFv3",
        name="lateral olfactory tract, body",
        acronym="lot",
        id="665",
    )
    LOTG = BrainStructureModel(
        atlas="CCFv3",
        name="lateral olfactory tract, general",
        acronym="lotg",
        id="21",
    )
    V4R = BrainStructureModel(
        atlas="CCFv3",
        name="lateral recess",
        acronym="V4r",
        id="153",
    )
    VL = BrainStructureModel(
        atlas="CCFv3",
        name="lateral ventricle",
        acronym="VL",
        id="81",
    )
    MP = BrainStructureModel(
        atlas="CCFv3",
        name="mammillary peduncle",
        acronym="mp",
        id="673",
    )
    MFBSMA = BrainStructureModel(
        atlas="CCFv3",
        name="mammillary related",
        acronym="mfbsma",
        id="46",
    )
    MTG = BrainStructureModel(
        atlas="CCFv3",
        name="mammillotegmental tract",
        acronym="mtg",
        id="681",
    )
    MTT = BrainStructureModel(
        atlas="CCFv3",
        name="mammillothalamic tract",
        acronym="mtt",
        id="690",
    )
    MCT = BrainStructureModel(
        atlas="CCFv3",
        name="medial corticohypothalamic tract",
        acronym="mct",
        id="428",
    )
    MFB = BrainStructureModel(
        atlas="CCFv3",
        name="medial forebrain bundle",
        acronym="mfb",
        id="54",
    )
    MFBS = BrainStructureModel(
        atlas="CCFv3",
        name="medial forebrain bundle system",
        acronym="mfbs",
        id="991",
    )
    ML = BrainStructureModel(
        atlas="CCFv3",
        name="medial lemniscus",
        acronym="ml",
        id="697",
    )
    MLF = BrainStructureModel(
        atlas="CCFv3",
        name="medial longitudinal fascicle",
        acronym="mlf",
        id="62",
    )
    MCP = BrainStructureModel(
        atlas="CCFv3",
        name="middle cerebellar peduncle",
        acronym="mcp",
        id="78",
    )
    MOV = BrainStructureModel(
        atlas="CCFv3",
        name="motor root of the trigeminal nerve",
        acronym="moV",
        id="93",
    )
    NST = BrainStructureModel(
        atlas="CCFv3",
        name="nigrostriatal tract",
        acronym="nst",
        id="102",
    )
    IIIN = BrainStructureModel(
        atlas="CCFv3",
        name="oculomotor nerve",
        acronym="IIIn",
        id="832",
    )
    IN = BrainStructureModel(
        atlas="CCFv3",
        name="olfactory nerve",
        acronym="In",
        id="840",
    )
    ONL = BrainStructureModel(
        atlas="CCFv3",
        name="olfactory nerve layer of main olfactory bulb",
        acronym="onl",
        id="1016",
    )
    OCH = BrainStructureModel(
        atlas="CCFv3",
        name="optic chiasm",
        acronym="och",
        id="117",
    )
    IIN = BrainStructureModel(
        atlas="CCFv3",
        name="optic nerve",
        acronym="IIn",
        id="848",
    )
    OR = BrainStructureModel(
        atlas="CCFv3",
        name="optic radiation",
        acronym="or",
        id="484682520",
    )
    OPT = BrainStructureModel(
        atlas="CCFv3",
        name="optic tract",
        acronym="opt",
        id="125",
    )
    FXPO = BrainStructureModel(
        atlas="CCFv3",
        name="postcommissural fornix",
        acronym="fxpo",
        id="737",
    )
    PC = BrainStructureModel(
        atlas="CCFv3",
        name="posterior commissure",
        acronym="pc",
        id="158",
    )
    VISPM = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area",
        acronym="VISpm",
        id="533",
    )
    VISPM1 = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 1",
        acronym="VISpm1",
        id="805",
    )
    VISPM2_3 = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 2/3",
        acronym="VISpm2/3",
        id="41",
    )
    VISPM4 = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 4",
        acronym="VISpm4",
        id="501",
    )
    VISPM5 = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 5",
        acronym="VISpm5",
        id="565",
    )
    VISPM6A = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 6a",
        acronym="VISpm6a",
        id="257",
    )
    VISPM6B = BrainStructureModel(
        atlas="CCFv3",
        name="posteromedial visual area, layer 6b",
        acronym="VISpm6b",
        id="469",
    )
    PM = BrainStructureModel(
        atlas="CCFv3",
        name="principal mammillary tract",
        acronym="pm",
        id="753",
    )
    PY = BrainStructureModel(
        atlas="CCFv3",
        name="pyramid",
        acronym="py",
        id="190",
    )
    PYD = BrainStructureModel(
        atlas="CCFv3",
        name="pyramidal decussation",
        acronym="pyd",
        id="198",
    )
    ROOT = BrainStructureModel(
        atlas="CCFv3",
        name="root",
        acronym="root",
        id="997",
    )
    RUST = BrainStructureModel(
        atlas="CCFv3",
        name="rubrospinal tract",
        acronym="rust",
        id="863",
    )
    SV = BrainStructureModel(
        atlas="CCFv3",
        name="sensory root of the trigeminal nerve",
        acronym="sV",
        id="229",
    )
    TS = BrainStructureModel(
        atlas="CCFv3",
        name="solitary tract",
        acronym="ts",
        id="237",
    )
    SPTV = BrainStructureModel(
        atlas="CCFv3",
        name="spinal tract of the trigeminal nerve",
        acronym="sptV",
        id="794",
    )
    SM = BrainStructureModel(
        atlas="CCFv3",
        name="stria medullaris",
        acronym="sm",
        id="802",
    )
    ST = BrainStructureModel(
        atlas="CCFv3",
        name="stria terminalis",
        acronym="st",
        id="301",
    )
    SEZ = BrainStructureModel(
        atlas="CCFv3",
        name="subependymal zone",
        acronym="SEZ",
        id="98",
    )
    SCP = BrainStructureModel(
        atlas="CCFv3",
        name="superior cerebelar peduncles",
        acronym="scp",
        id="326",
    )
    DSCP = BrainStructureModel(
        atlas="CCFv3",
        name="superior cerebellar peduncle decussation",
        acronym="dscp",
        id="812",
    )
    CSC = BrainStructureModel(
        atlas="CCFv3",
        name="superior colliculus commissure",
        acronym="csc",
        id="336",
    )
    SCWM = BrainStructureModel(
        atlas="CCFv3",
        name="supra-callosal cerebral white matter",
        acronym="scwm",
        id="484682512",
    )
    SUP = BrainStructureModel(
        atlas="CCFv3",
        name="supraoptic commissures",
        acronym="sup",
        id="349",
    )
    TSP = BrainStructureModel(
        atlas="CCFv3",
        name="tectospinal pathway",
        acronym="tsp",
        id="877",
    )
    LFBST = BrainStructureModel(
        atlas="CCFv3",
        name="thalamus related",
        acronym="lfbst",
        id="896",
    )
    V3 = BrainStructureModel(
        atlas="CCFv3",
        name="third ventricle",
        acronym="V3",
        id="129",
    )
    TB = BrainStructureModel(
        atlas="CCFv3",
        name="trapezoid body",
        acronym="tb",
        id="841",
    )
    VN = BrainStructureModel(
        atlas="CCFv3",
        name="trigeminal nerve",
        acronym="Vn",
        id="901",
    )
    IVN = BrainStructureModel(
        atlas="CCFv3",
        name="trochlear nerve",
        acronym="IVn",
        id="911",
    )
    UF = BrainStructureModel(
        atlas="CCFv3",
        name="uncinate fascicle",
        acronym="uf",
        id="850",
    )
    XN = BrainStructureModel(
        atlas="CCFv3",
        name="vagus nerve",
        acronym="Xn",
        id="917",
    )
    VHC = BrainStructureModel(
        atlas="CCFv3",
        name="ventral hippocampal commissure",
        acronym="vhc",
        id="449",
    )
    SCTV = BrainStructureModel(
        atlas="CCFv3",
        name="ventral spinocerebellar tract",
        acronym="sctv",
        id="866",
    )
    VTD = BrainStructureModel(
        atlas="CCFv3",
        name="ventral tegmental decussation",
        acronym="vtd",
        id="397",
    )
    VS = BrainStructureModel(
        atlas="CCFv3",
        name="ventricular systems",
        acronym="VS",
        id="73",
    )
    VVIIIN = BrainStructureModel(
        atlas="CCFv3",
        name="vestibular nerve",
        acronym="vVIIIn",
        id="413",
    )
    VIIIN = BrainStructureModel(
        atlas="CCFv3",
        name="vestibulocochlear nerve",
        acronym="VIIIn",
        id="933",
    )
    VON = BrainStructureModel(
        atlas="CCFv3",
        name="vomeronasal nerve",
        acronym="von",
        id="949",
    )

    @classmethod
    def from_id(cls, id: str):
        """Get structure by ID"""
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, BrainStructureModel) and attr.id == id:
                return attr
        raise ValueError(f"Structure with ID {id} not found.")

    @classmethod
    def by_name(cls, name: str):
        """Get structure by name"""
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, BrainStructureModel) and attr.name == name:
                return attr
        raise ValueError(f"Structure with name '{name}' not found.")

    @classmethod
    def by_acronym(cls, acronym: str):
        """Get structure by acronym"""
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, BrainStructureModel) and attr.acronym == acronym:
                return attr
        raise ValueError(f"Structure with acronym '{acronym}' not found.")
