import queue
from itertools import cycle

import pytest

from eumdac.customisation import CustomisationError
from eumdac.errors import EumdacError
from eumdac.job_id import JobIdentifier
from eumdac.tailor_app import (
    ExceedingNumberOfCustomisationsEumdacError,
    FatalTailorError,
    InvalidStateTransitionError,
    StateQueryFutureFunc,
    TailorApp,
    WaitForDoneCustomisationFutureFunc,
)
from tests.base import FakeCustomisation, FakeProduct, FakeStore, FakeTailor
from tests.test_order import products, tailor_order


class MockOrder:
    def __init__(self):
        self._no_warning_logs = True
        pass

    def initialize(self, chain, products, output_dir, no_warning_logs):
        pass

    def __str__(self):
        return "test"

    def deserialize(self):
        return {"max_workers": 3}

    def serialize(self, d):
        pass

    def update(self, customisation_id, product_id, status=None, download_states=None):
        pass

    def resolve_product_num(self, p_id):
        return -1, -1


valid_transitions = [
    ["RUNNING", "DONE"],
    ["QUEUED", "RUNNING", "DONE"],
    ["QUEUED", "QUEUED", "QUEUED", "RUNNING", "DONE"],
    ["QUEUED", "QUEUED", "QUEUED", "RUNNING", "RUNNING", "RUNNING", "DONE", "DONE"],
]


@pytest.mark.parametrize("transitions", valid_transitions)
def test_valid_transitions(transitions):
    def add_func(product):
        return FakeCustomisation(states_to_return=transitions)

    WaitForDoneCustomisationFutureFunc(
        customization_add_func=add_func,
        order=MockOrder(),
        polling_interval=0,
        job_identificator=JobIdentifier(total_jobs=1),
        customisation_blackboard=queue.Queue(),
    )(FakeProduct())


invalid_transitions = [
    ["RUNNING", "QUEUED"],
]


@pytest.mark.parametrize("transitions", invalid_transitions)
def test_invalid_transitions(transitions):
    with pytest.raises(InvalidStateTransitionError):

        def add_func(product):
            return FakeCustomisation(states_to_return=transitions)

        WaitForDoneCustomisationFutureFunc(
            customization_add_func=add_func,
            order=MockOrder(),
            polling_interval=0,
            job_identificator=JobIdentifier(total_jobs=1),
            customisation_blackboard=queue.Queue(),
        )(FakeProduct())


timeout_transitions = [
    cycle(["QUEUED"]),
    cycle(["RUNNING"]),
]


@pytest.mark.parametrize("transitions", timeout_transitions)
def test_timeout_raised(transitions):
    with pytest.raises(FatalTailorError):

        def mock_add_func(product):
            return FakeCustomisation(transitions)

        WaitForDoneCustomisationFutureFunc(
            customization_add_func=mock_add_func,
            order=MockOrder(),
            timeout=0.001,
            job_identificator=JobIdentifier(total_jobs=1),
            customisation_blackboard=queue.Queue(),
        )(FakeProduct())


inactive_transitions = [
    cycle(["RUNNING", "INACTIVE"]),
    cycle(["QUEUED", "INACTIVE"]),
]


@pytest.mark.parametrize("transitions", inactive_transitions)
def test_inactive_transitions(transitions):
    with pytest.raises(EumdacError):

        def mock_add_func(product):
            return FakeCustomisation(transitions)

        fut = WaitForDoneCustomisationFutureFunc(
            customization_add_func=mock_add_func,
            order=MockOrder(),
            timeout=1000,
            job_identificator=JobIdentifier(total_jobs=1),
            customisation_blackboard=queue.Queue(),
        )(FakeProduct())
        assert fut.state.name == "INACTIVE"


class FakeAdd:
    def __init__(self):
        self.exception_cnt = 0

    def func(self, product):
        if isinstance(product, tuple):
            exc, max_cnt = product
            if self.exception_cnt >= max_cnt:
                return FakeCustomisation([])
            self.exception_cnt += 1
            raise CustomisationError("Could not add customisation")
        return FakeCustomisation([])


eumdac_error_descriptions = [
    {
        "status": 400,
        "title": "invalid value for parameter",
        "description": "PNG (RGB) driver doesn't support 11 bands.  Must be 1 (grey) or 3 (rgb) bands",
    },
    {
        "status": 400,
        "title": "invalid value for parameter",
        "description": "The roi value can not be a list",
    },
]


@pytest.mark.parametrize("description", eumdac_error_descriptions)
def test_concurrent_download_fail_400(description):
    def mock_add_func(product):
        raise EumdacError("Test", description)

    with pytest.raises(FatalTailorError):
        WaitForDoneCustomisationFutureFunc(
            customization_add_func=mock_add_func,
            order=MockOrder(),
            job_identificator=JobIdentifier(total_jobs=1),
            customisation_blackboard=queue.Queue(),
        )(FakeProduct())


class FakeFailCustomisation(FakeCustomisation):
    def __init__(self, logfile, cid=None):
        self.states_to_return = iter(["QUEUED", "RUNNING", "FAILED"])
        self.logfile = logfile
        self._id = cid or "foo"
        self.deleted = False


class FakeFailCustomisationProduct:
    def __init__(self, customisation, product):
        self.customisation = customisation
        self.product = product


eumdac_error_logs = [
    """
    2022-07-14 07:37:52 - PROCESSING.chain_runner[270] - INFO - Start process "fb6bdb44"
    2022-07-14 07:37:52 - PROCESSING.chain_runner[231] - INFO - WORKER: tcp://10.0.3.141:40353
    2022-07-14 07:37:52 - PROCESSING.chain_runner[232] - INFO - PID: 26
    2022-07-14 07:37:52 - PROCESSING.chain_runner[233] - INFO - backend: epct_gis_hrit
    2022-07-14 07:37:52 - PROCESSING.chain_runner[234] - INFO - user: delahoz
    2022-07-14 07:38:04 - PROCESSING.preprocessing[56] - INFO - download from https://api.eumetsat.int/data/download/collections/EO%3AEUM%3ADAT%3AMSG%3AHRSEVIRI/products/MSG4-SEVI-MSG15-0100-NA-20220601004243.155000000Z-NA is finished
    2022-07-14 07:38:07 - PROCESSING.chain_runner[401] - INFO - customisation time: 14 - process: fb6bdb44
    2022-07-14 07:38:07 - PROCESSING.chain_runner[403] - ERROR - error at preprocessing.initialise_processing[516] while initializing the customization for product(s) [MSG4-SEVI-MSG15-0100-NA-20220601004243.155000000Z-NA] and for configuration {'product': 'HRSEVIRI_HRIT', 'format': 'png_rgb'}: invalid HRIT file name: '/var/dtws/users/delahoz/workspace/EPCT_HRSEVIRI_HRIT_fb6bdb44/decompressed_data/MSG4-SEVI-MSG15-0100-NA-20220601004243.155000000Z-NA.nat'
    """,
    """
    2022-07-14 08:14:19 - PROCESSING.api[403] - INFO - Submitted process 53a71aea - FUTURE: run_chain_async-e24f66fb1ab913b7761f9ac62b4ee281
    2022-07-14 08:14:21 - PROCESSING.chain_runner[270] - INFO - Start process "53a71aea"
    2022-07-14 08:14:21 - PROCESSING.chain_runner[231] - INFO - WORKER: tcp://10.0.3.151:33526
    2022-07-14 08:14:21 - PROCESSING.chain_runner[232] - INFO - PID: 26
    2022-07-14 08:14:21 - PROCESSING.chain_runner[233] - INFO - backend: epct_gis_eps_grib2
    2022-07-14 08:14:21 - PROCESSING.chain_runner[234] - INFO - user: delahoz
    2022-07-14 08:14:39 - PROCESSING.preprocessing[56] - INFO - download from https://api.eumetsat.int/data/download/collections/EO%3AEUM%3ADAT%3AMETOP%3AAVHRRL1/products/AVHR_xxx_1B_M03_20220709215503Z_20220709233703Z_N_O_20220709233331Z is finished
    2022-07-14 08:14:50 - PROCESSING.preprocessing[523] - INFO - Processing details - product: AVHRRL1 chain-name: None chain-details: -product: AVHRRL1 -format: GRIB-2 -compression: Internal compression (HDF5 or NetCDF4)
    2022-07-14 08:14:50 - PROCESSING.preprocessing[530] - INFO - Input products: AVHR_xxx_1B_M03_20220709215503Z_20220709233703Z_N_O_20220709233331Z.nat
    2022-07-14 08:14:51 - PROCESSING.epct_gis[991] - INFO - Expected steps: ['import', 'format']
    2022-07-14 08:14:51 - PROCESSING.epct_gis[994] - INFO - Starting step "IMPORT" 1/2 ...
    2022-07-14 08:14:54 - PROCESSING.vrt[94] - INFO - Command line and its output ...
    2022-07-14 08:14:54 - PROCESSING.epct_gis[998] - INFO - ... step "IMPORT" finished!
    2022-07-14 08:14:54 - PROCESSING.epct_gis[1006] - INFO - Starting step "FORMAT" 2/2 ...
    2022-07-14 08:14:54 - PROCESSING.vrt[94] - INFO - Command line and its output ...
    2022-07-14 08:15:05 - PROCESSING.epct_gis[802] - INFO - ... step "FORMAT" finished!
    2022-07-14 08:15:05 - PROCESSING.vrt[94] - INFO - Command line and its output ...
    ERROR 6: Source dataset must have a geotransform
    2022-07-14 08:15:05 - PROCESSING.vrt[94] - INFO - Command line and its output ...
    ERROR 6: Source dataset must have a geotransform
    2022-07-14 08:15:05 - PROCESSING.chain_runner[401] - INFO - customisation time: None - process: 53a71aea
    2022-07-14 08:15:05 - PROCESSING.chain_runner[403] - ERROR - error at epct_gis.run_chain[1014] while performing the customization for product(s) [AVHR_xxx_1B_M03_20220709215503Z_20220709233703Z_N_O_20220709233331Z.nat] and for configuration {'product': 'AVHRRL1', 'format': 'grib2', 'compression': 'internal'}: INTERNAL ERROR: see Log file
    """,
]


@pytest.mark.parametrize("log", eumdac_error_logs)
def test_wait_for_done_fail(log):
    def mock_add_func(product):
        return FakeFailCustomisation(logfile=log)

    with pytest.raises(FatalTailorError):
        WaitForDoneCustomisationFutureFunc(
            order=MockOrder(),
            customization_add_func=mock_add_func,
            job_identificator=JobIdentifier(total_jobs=1),
            customisation_blackboard=queue.Queue(),
        )(FakeProduct())


def test_state_query():
    collection_id = "coid"
    customisation_id = "cuid"
    product_id = "pid"

    success, customisation, product = StateQueryFutureFunc()(
        product_id,
        {"col_id": collection_id, "customisation": customisation_id},
        FakeTailor(),
        FakeStore(),
    )

    assert success
    assert customisation._id == customisation_id
    assert product._id == product_id
    assert product.collection._id == collection_id


def test_resume(tailor_order):
    ta = TailorApp(tailor_order, FakeStore(), FakeTailor())

    for pi in tailor_order.iter_product_info():
        assert pi.p_dict["server_state"] == "UNSUBMITTED"

    ta.resume()

    for pi in tailor_order.iter_product_info():
        assert pi.p_dict["server_state"] == "DONE"
        for fn, ds in pi.p_dict["download_states"].items():
            assert ds == "DOWNLOADED"


@pytest.mark.parametrize("status_code,message,description", [(200, "test", "test")])
def test_check_nonfatal_error_response(tailor_order, status_code, message, description):
    from eumdac.tailor_app import check_error_response

    extra_info = {"description": description, "status": status_code}

    err = EumdacError(message, extra_info)
    check_error_response(err)


@pytest.mark.parametrize("status_code,message,description", [(400, "test", "test")])
def test_check_fatal_error_response(tailor_order, status_code, message, description):
    from eumdac.tailor_app import check_error_response

    extra_info = {"description": description, "status": status_code}

    err = EumdacError(message, extra_info)
    with pytest.raises(FatalTailorError):
        check_error_response(err)


@pytest.mark.parametrize(
    "status_code,message,description",
    [(500, "test", "You are exceeding your maximum number 123")],
)
def test_check_fatal_error_response2(tailor_order, status_code, message, description):
    from eumdac.tailor_app import check_error_response

    extra_info = {"description": description, "status": status_code}

    err = EumdacError(message, extra_info)
    with pytest.raises(ExceedingNumberOfCustomisationsEumdacError):
        check_error_response(err)
