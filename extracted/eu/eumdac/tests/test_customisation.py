import fnmatch
import io
import time
import shutil
import unittest
from datetime import datetime

from pytest import skip

from eumdac.token import AccessToken
from eumdac.datastore import DataStore
from eumdac.tailor_models import Chain
from eumdac.datatailor import DataTailor
from eumdac.customisation import Customisation, AlreadyDeletedCustomisationError

from .base import DataServiceTestCase, INTEGRATION_TESTING


class TestCustomisation(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datatailor = DataTailor(self.token)

    @unittest.skip("Temporarily skipping")
    def test_full_customisation_process(self):
        # format conversion
        chain_config = Chain(product="HRSEVIRI", format="netcdf4", quicklook="hrseviri_png")
        # search for the last product in June 2020
        datastore = DataStore(self.token)
        hrseviri = datastore.get_collection("EO:EUM:DAT:MSG:HRSEVIRI")
        product = hrseviri.search(dtend=datetime(2020, 7, 1)).first()
        # use context manager, to automatically delete customisations at the end even
        # if an error occurs
        with self.datatailor.new_customisation(product, chain_config) as customisation:
            if not INTEGRATION_TESTING:
                customisation.update_margin = 0
            timeout = 900  # needed to increase to 12 minutes, overstrained DT...
            tic = time.time()
            while time.time() - tic < timeout:
                if INTEGRATION_TESTING:
                    time.sleep(5)
                if customisation.status == "DONE":
                    break
            else:
                raise TimeoutError(f"Cutomisation took longer than {timeout}s")
            # test streaming
            (png_aux_xml,) = fnmatch.filter(customisation.outputs, "*.png.aux.xml")
            with customisation.stream_output(png_aux_xml) as stream:
                file = io.BytesIO()
                shutil.copyfileobj(stream, file)
            # check properties
            self.assertIsInstance(customisation.creation_time, datetime)
            self.assertIsInstance(customisation.backend, str)
            self.assertIsInstance(customisation.product_type, str)
            self.assertIsInstance(customisation.processing_steps, list)
            self.assertIsInstance(customisation.status, str)
            self.assertIsInstance(customisation.progress, int)
            self.assertIsInstance(customisation.duration, int)
            self.assertIsInstance(customisation.outputs, list)
            self.assertIsInstance(customisation.logfile, str)

        expected_xml_length = 870
        self.assertEqual(file.tell(), expected_xml_length)

        # check that customisation has been removed
        delete_url = self.datatailor.urls.get("tailor", "delete")
        self.requests_mock.assert_call_count(delete_url, 1)

    @unittest.skipIf(INTEGRATION_TESTING, "Integration already covered!")
    def test_properties_cache(self):
        customisation_id = "abcdef123"
        url = self.datatailor.urls.get(
            "tailor", "customisation", vars={"customisation_id": customisation_id}
        )
        self.requests_mock.add(
            "GET",
            url,
            json={
                customisation_id: {
                    "creation_time": datetime.now().strftime(Customisation._creation_time_format),
                    "backend_id": "backend-id",
                    "product_id": "product-id",
                    "required_processing_steps": ["a", "b", "c"],
                    "status": "DONE",
                    "progress": 100,
                    "processing_duration": 123,
                    "output_products": ["file.nc", "file.xml", "file.png"],
                }
            },
        )
        self.token._expiration = time.time() + 1000
        self.token._access_token = "token"
        customisation = Customisation(customisation_id, self.datatailor)

        creation_time = customisation.creation_time
        backend = customisation.backend
        self.assertIsInstance(creation_time, datetime)
        self.assertIsInstance(backend, str)
        self.requests_mock.assert_call_count(url, 1)

        # force reload
        customisation.update_margin = 0
        status = customisation.status
        self.assertIsInstance(status, str)
        self.requests_mock.assert_call_count(url, 2)

    @unittest.skipIf(INTEGRATION_TESTING, "Integration already covered!")
    def test_string_representation(self):
        customisation_id = "abcdef123"
        customisation = Customisation(customisation_id, self.datatailor)
        self.assertEqual(customisation_id, str(customisation))
        self.assertIn(customisation_id, repr(customisation))

    @unittest.skipIf(INTEGRATION_TESTING, "Test Failure")
    def test_cannot_fails_when_deleted(self):
        self.requests_mock.add("PATCH", self.datatailor.urls.get("tailor", "delete"))
        self.token._expiration = time.time() + 1000
        self.token._access_token = "token"
        customisation_id = "abcdef123"
        customisation = Customisation(customisation_id, self.datatailor)
        customisation.delete()

        message = "Customisation already deleted."
        with self.assertRaisesRegex(AlreadyDeletedCustomisationError, message):
            customisation.status

        with self.assertRaisesRegex(AlreadyDeletedCustomisationError, message):
            customisation.logfile

        with self.assertRaisesRegex(AlreadyDeletedCustomisationError, message):
            with customisation.stream_output("file.dat") as stream:
                data = stream.read()
                del data

    @unittest.skipIf(INTEGRATION_TESTING, "Test Failure")
    def test_fail_on_unknown_stream_output(self):
        customisation_id = "abcdef123"
        url = self.datatailor.urls.get(
            "tailor", "customisation", vars={"customisation_id": customisation_id}
        )
        self.requests_mock.add(
            "GET",
            url,
            json={customisation_id: {"output_products": ["file.nc", "file.xml", "file.png"]}},
        )
        self.token._expiration = time.time() + 1000
        self.token._access_token = "token"
        customisation_id = "abcdef123"
        customisation = Customisation(customisation_id, self.datatailor)
        message = r"file\.dat not in "
        with self.assertRaisesRegex(ValueError, message):
            with customisation.stream_output("file.dat") as stream:
                data = stream.read()
                del data

    @classmethod
    def prepare_integration_test(cls):
        prepare_test_customisation(cls.credentials)


def prepare_test_customisation(credentials):
    """delete all existing customisations"""
    token = AccessToken(credentials)
    datatailor = DataTailor(token)
    for customisation in datatailor.customisations:
        try:
            customisation.delete()
        except:
            pass
