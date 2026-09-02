from eumdac.token import AnonymousAccessToken
from eumdac.datastore import DataStore
from eumdac.product import Product
from eumdac.collection import Collection
from datetime import datetime


# Auxies

TOKEN = AnonymousAccessToken()


def products_setup():
    products = [
        "MSG3-SEVI-MSG15-0100-NA-20240101101243.601000000Z-NA",
        "S3B_OL_2_WFR____20240303T120224_20240303T120321_20240305T045853_0056_090_194_4320_MAR_O_NT_003.SEN3",
        "W_XX-EUMETSAT-Darmstadt,IMG+SAT,MTI1+FCI-1C-RRAD-HRFI-FD--x-x---x_C_EUMT_20251010115303_IDPFI_OPE_20251010115006_20251010115923_N__O_0072_0000",
    ]

    collections = ["EO:EUM:DAT:MSG:HRSEVIRI", "EO:EUM:DAT:0407", "EO:EUM:DAT:0665"]

    # Product ID : Collection ID, Satellite start, Instrument, Size, Timeliness,
    # Orbit related numbers (1->int), Orbit direction ("a"->str), MTG specific (1->int)
    products_setup_dict = {
        products[0]: [collections[0], "MSG", "SEVIRI", 1, "NOMINAL", None, None, None],
        products[1]: [collections[1], "Sentinel", "OLCI", 1, "NT", 1, "a", None],
        products[2]: [collections[2], "MTI1", "FCI", 1.0, "NRT", None, None, "a"],
    }

    return products_setup_dict


def assertions(p_obj, p_setup_list):
    assert str(p_obj.collection) == p_setup_list[0]
    assert isinstance(p_obj.sensing_start, datetime)
    assert isinstance(p_obj.sensing_end, datetime)
    assert p_obj.satellite.startswith(p_setup_list[1])
    print(p_obj.instrument)  # For debugging
    assert p_obj.instrument == p_setup_list[2]
    assert isinstance(p_obj.size, type(p_setup_list[3]))
    assert isinstance(p_obj.metadata, dict)
    assert "properties" in p_obj.metadata
    assert "manifest.xml" in p_obj.entries
    assert isinstance(p_obj.acronym, str)
    assert isinstance(p_obj.product_type, str)
    assert p_obj.product_type == p_obj.acronym
    assert p_obj.timeliness == p_setup_list[4]
    assert isinstance(p_obj.md5, str)
    assert isinstance(p_obj.processingTime, str)
    assert isinstance(p_obj.processorVersion, str)
    assert isinstance(p_obj.format, str)
    assert isinstance(p_obj.qualityStatus, str)
    assert isinstance(p_obj.ingested, datetime)
    assert isinstance(p_obj.orbit_type, str)
    assert isinstance(p_obj.orbit_is_LEO, bool)
    assert isinstance(p_obj.url, str)
    # LEO specific
    assert isinstance(p_obj.orbit_number, type(p_setup_list[5]))
    assert isinstance(p_obj.relative_orbit, type(p_setup_list[5]))
    assert isinstance(p_obj.cycle_number, type(p_setup_list[5]))
    assert isinstance(p_obj.orbit_direction, type(p_setup_list[6]))
    # MTG specific
    assert isinstance(p_obj.is_mtg, bool)
    assert isinstance(p_obj.repeat_cycle, type(p_setup_list[7]))
    assert isinstance(p_obj.region_coverage, type(p_setup_list[7]))
    assert isinstance(p_obj.subregion_identifier, type(p_setup_list[7]))


# TESTS


def test_1_get_product_directly_properties():
    products_setup_dict = products_setup()
    datastore = DataStore(token=TOKEN)

    for p_id in products_setup_dict.keys():
        print(f"Asserting: {p_id}")
        p_obj = Product(products_setup_dict[p_id][0], p_id, datastore)
        assertions(p_obj, products_setup_dict[p_id])


def test_2_get_product_search_properties():
    products_setup_dict = products_setup()
    datastore = DataStore(token=TOKEN)

    for p_id in products_setup_dict.keys():
        print(f"Asserting: {p_id}")
        collection = Collection(products_setup_dict[p_id][0], datastore)
        p_obj = collection.search(title=p_id).first()
        assertions(p_obj, products_setup_dict[p_id])


def test_3_get_product_opensearch_properties():
    products_setup_dict = products_setup()
    datastore = DataStore(token=TOKEN)

    for p_id in products_setup_dict.keys():
        print(f"Asserting: {p_id}")
        p_obj = datastore.opensearch(f"pi={products_setup_dict[p_id][0]}&title={p_id}").first()
        assertions(p_obj, products_setup_dict[p_id])
