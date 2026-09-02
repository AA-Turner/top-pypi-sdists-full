import unittest
import time
from unittest import mock

from requests.exceptions import HTTPError

from eumdac.errors import EumdacError
from eumdac.token import AccessToken
from eumdac.datatailor import DataTailor
from eumdac.customisation import Customisation
from eumdac.tailor_models import Chain, Filter, RegionOfInterest, Quicklook

from .base import DataServiceTestCase, INTEGRATION_TESTING


# @pytest.mark.skip("Temporarily skipping")
class TestDataTailor(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datatailor = DataTailor(self.token)

    @unittest.skipIf(INTEGRATION_TESTING, "Tested in unit testing phase")
    def test_property_customisations(self):
        token_url = self.token.urls.get("token", "token")
        self.requests_mock.add(
            "POST",
            token_url,
            json={
                "access_token": "b070adda-00c8-36cd-bb8f-4f6a2d6661ce",
                "scope": "am_application_scope default",
                "token_type": "Bearer",
                "expires_in": 970,
            },
        )
        customisations_url = self.datatailor.urls.get("tailor", "customisations")
        self.requests_mock.add(
            "GET",
            customisations_url,
            json={
                "data": [
                    {
                        "user_id": "ABC",
                        "creation_time": "20210810T142328Z",
                        "backend_id": "epct_gis_msg",
                        "product_id": "HRSEVIRI",
                        "required_processing_steps": ["format"],
                        "status": "DONE",
                        "progress": 100,
                        "processing_duration": 47,
                        "output_products": ["output.file"],
                        "id": "abcdef",
                    }
                ]
            },
        )
        customisations = self.datatailor.customisations
        self.assertIsInstance(customisations, list)
        self.assertIsInstance(customisations[0], Customisation)

    def test_properties(self):
        info = self.datatailor.info
        self.assertIn("epct_version", info)

        user_info = self.datatailor.user_info
        self.assertIsInstance(user_info["username"], str)

        quota = self.datatailor.quota
        self.assertIsInstance(quota, dict)

    @unittest.skipIf(INTEGRATION_TESTING, "Only checking the interface.")
    def test_create_customisation(self):
        self.token._access_token = "b070adda-00c8-36cd-bb8f-4f6a2d6661ce"
        self.token._expiration = time.time() + 1000
        self.requests_mock.add(
            "POST",
            self.datatailor.urls.get("tailor", "customisations"),
            json={"total": 1, "data": ["63f53c99"]},
        )
        chain_name = "MyChain"
        mock_product = mock.MagicMock(name="product")
        mock_product._id = "MY-PRODUCT-ID"
        mock_product.collection._id = "MY-COLLECTION-ID"
        customisation = self.datatailor.new_customisation(mock_product, chain_name)
        self.assertIsInstance(customisation, Customisation)

    def test_chain_crud(self):
        url = self.datatailor.chains.url
        chain = Chain(
            id="hrseviri_native_to_netcdf4",
            name="Native to netCDF4",
            description="Convert a SEVIRI Native product to netCDF4",
            product="HRSEVIRI",
            format="netcdf4",
        )
        # create
        self.datatailor.chains.create(chain)
        self.requests_mock.assert_call_count(url, 1)

        # read
        chain_ = self.datatailor.chains.read(chain.id)
        self.assertEqual(chain_, chain)
        chains = self.datatailor.chains.search(product="HRSEVIRI")
        self.assertIn(chain, chains)
        self.assertIsInstance(chains[0], Chain)

        # update
        chain.description = "convert a SEVIRI native product to netCDF4"
        self.datatailor.chains.update(chain)
        chain_ = self.datatailor.chains.read(chain.id)
        self.assertEqual(chain_, chain)

        # delete
        self.datatailor.chains.delete(chain)
        self.requests_mock.assert_call_count(url + f"/{chain.id}", 4)

    def test_filter_crud(self):
        url = self.datatailor.filters.url
        fltr = Filter(
            id="hrseviri_water_vapour",
            product="HRSEVIRI",
            bands=["channel_9", "channel_10"],
            name="Water Vapour",
        )
        # create
        self.datatailor.filters.create(fltr)
        self.requests_mock.assert_call_count(url, 1)

        # read
        fltr_ = self.datatailor.filters.read(fltr.id)
        self.assertEqual(fltr_, fltr)
        fltrs = self.datatailor.filters.search(product="HRSEVIRI")
        self.assertIn(fltr, fltrs)
        self.assertIsInstance(fltrs[0], Filter)

        # update
        fltr.bands = ["channel_9"]
        self.datatailor.filters.update(fltr)
        fltr_ = self.datatailor.filters.read(fltr.id)
        self.assertEqual(fltr_, fltr)

        # delete
        self.datatailor.filters.delete(fltr)
        self.requests_mock.assert_call_count(url + f"/{fltr.id}", 4)

    def test_roi_crud(self):
        url = self.datatailor.rois.url
        roi = RegionOfInterest(
            id="deutschland", name="Deutschland", NSWE=[54.983104, 47.302488, 5.988658, 15.016996]
        )
        # create
        self.datatailor.rois.create(roi)
        self.requests_mock.assert_call_count(url, 1)

        # read
        roi_ = self.datatailor.rois.read(roi.id)
        self.assertEqual(roi_, roi)

        # delete
        self.datatailor.rois.delete(roi)
        self.requests_mock.assert_call_count(url + f"/{roi.id}", 2)

    def test_quicklook_crud(self):
        url = self.datatailor.quicklooks.url
        quicklook = Quicklook(
            id="hrseviri_wv_jpeg",
            name="HRSEVIRI Water Vapour",
            resample_method="cubic",
            stretch_method="min_max",
            product="HRSEVIRI",
            format="jpeg_rgb",
            filter=Filter(bands=["channel_11", "channel_10", "channel_9"]),
        )
        # create
        self.datatailor.quicklooks.create(quicklook)
        self.requests_mock.assert_call_count(url, 1)

        # read
        quicklook_ = self.datatailor.quicklooks.read(quicklook.id)
        self.assertEqual(quicklook_, quicklook)
        quicklooks = self.datatailor.quicklooks.search(product="HRSEVIRI")
        self.assertIn(quicklook, quicklooks)
        self.assertIsInstance(quicklooks[0], Quicklook)

        # update
        quicklook.resample_method = "bilinear"
        self.datatailor.quicklooks.update(quicklook)
        quicklook_ = self.datatailor.quicklooks.read(quicklook.id)
        self.assertEqual(quicklook_, quicklook)

        # delete (using string)
        self.datatailor.quicklooks.delete(quicklook.id)
        self.requests_mock.assert_call_count(url + f"/{quicklook.id}", 4)

    @classmethod
    def prepare_integration_test(cls):
        prepare_test_datatailor(cls.credentials)


def prepare_test_datatailor(credentials):
    """delete any resource that will be created during the test"""
    token = AccessToken(credentials)
    datatailor = DataTailor(token)
    crud_resources = [
        (datatailor.chains, "hrseviri_native_to_netcdf4"),
        (datatailor.filters, "hrseviri_water_vapour"),
        (datatailor.rois, "deutschland"),
        (datatailor.quicklooks, "hrseviri_wv_jpeg"),
    ]
    for api, resource_id in crud_resources:
        try:
            api.delete(resource_id)
        except:
            # Resources may or may not be there and DTWS won't send 40X error codes
            # when deleting not-found resources, so the fastest way is to try
            # deleting and ignore errors
            pass
