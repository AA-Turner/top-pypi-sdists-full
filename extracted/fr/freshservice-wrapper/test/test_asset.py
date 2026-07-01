# Copyright 2018 eGym GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from unittest import TestCase

from freshservice.api import API, AssetAPI


TEST_DOMAIN = 'flamunda'


class TestAsset(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = API(os.environ['FRESHSERVICE_API_KEY'], TEST_DOMAIN)
        cls.asset_api = AssetAPI(cls.api)

    def test_asset_get(self):
        asset = self.asset_api.get(1)
        self.assertEqual(asset.description, 'Test')
        self.assertEqual(asset.user_id, None)
        self.assertEqual(asset.warranty, 0)
        self.assertEqual(asset.os, 'Mac')
        self.assertEqual(asset.screen_width, '13')
        self.assertEqual(asset.hostname, 'pc-657')

    def test_asset_search(self):
        assets = self.asset_api.search('name', 'pc-657')
        self.assertEqual(assets[0].hostname, 'pc-657')
        assets = self.asset_api.search('serial_number', 'SN_XYZ')
        self.assertEqual(assets[0].serial_number, 'SN_XYZ')

    def test_asset_get_all(self):
        assets = self.asset_api.get_all()
        print('We have %d assets in our inventory!' % len(assets))
        for asset in assets:
            if hasattr(asset, 'hostname'):
                if asset.hostname == 'pc-657':
                    self.assertEqual(asset.serial_number, 'SN_XYZ')
                    break

    def test_asset_update(self):
        asset = self.asset_api.update(1, screen_width='15', impact='1',
                                      mac_address='AA:AA:AA:AA:AA:AA')
        self.assertEqual(asset.impact, 1)
        self.assertEqual(asset.screen_width, '15')
        self.assertEqual(asset.mac_address, 'AA:AA:AA:AA:AA:AA')

        asset = self.asset_api.update(1, screen_width='13', impact='2',
                                      mac_address='')
        self.assertEqual(asset.impact, 2)
        self.assertEqual(asset.screen_width, '13')
        self.assertEqual(asset.mac_address, None)
