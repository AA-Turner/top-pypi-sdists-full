# Copyright 2025 Lenovo Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pyghmi.redfish.oem.generic as generic
import pyghmi.util.webclient as webclient
from urllib.parse import urlencode
import pyghmi.exceptions as pygexc


class OEMHandler(generic.OEMHandler):

    def __init__(self, sysinfo, sysurl, webclient, cache, gpool=None):
        super(OEMHandler, self).__init__(sysinfo, sysurl, webclient, cache,
                                         gpool)
        if sysurl is None:
            systems, status = webclient.grab_json_response_with_status('/redfish/v1/Systems')
            if status == 200:
                for system in systems.get('Members', []):
                    if system.get('@odata.id', '').endswith('/Self') or system.get('@odata.id', '').endswith('/System_0'):
                        sysurl = system['@odata.id']
                        break
            self._varsysurl = sysurl
        self._wc = None
        self.bmc = webclient.thehost
        self._certverify = webclient._certverify

    def reseat_bay(self, bay):
        if bay != -1:
            raise pygexc.UnsupportedFunctionality(
                'This is not an enclosure manager')
        
        self._do_web_request('/redfish/v1/Chassis/Chassis_0/Actions/Oem/NvidiaChassis.AuxPowerReset', {
            "ResetType": "AuxPowerCycle"
        })

    def format_messages(self, response):
        msgs = response.get('Messages', [])
        msgents = []
        for msg in msgs:
            msgents.append(self.format_message(msg))
        for msg in response.get('Oem', {}).get('Ami', {}).get('HMCMessages', []):
            msgents.append(self.format_messages(msg))
        return ';'.join(msgents)

    def update_firmware(self, filename, data=None, progress=None, bank=None, otherfields=()):
        self._do_web_request('/redfish/v1/UpdateService', {
            "Oem": {
                "AMIUpdateService": {
                "@odata.type": "#AMIUpdateService.v1_0_0.AMIUpdateService",
                "PreserveConfiguration": {
                    "Syslog": True,
                    "NTP": True,
                    "Network": True,
                    "Authentication": True,
                    "EXTLOG": True,
                    "FRU": True,
                    "IPMI": True,
                    "KVM": True,
                    "REDFISH": True,
                    "SDR": False,
                    "SEL": True,
                    "SNMP": True,
                    "SSH": True,
                    "WEB": True
            }
            }}}, method='PATCH', etag='*')
        return super(OEMHandler, self).update_firmware(filename, data=data, progress=progress, bank=bank, otherfields=otherfields)

    @property
    def wc(self):
        self.fwid = None
        if self._wc:
            rsp, status = self._wc.grab_json_response_with_status(
                '/api/chassis-status')
            if status == 200:
                return self._wc
        authdata = {
            'username': self.username,
            'password': self.password,
        }
        wc = webclient.SecureHTTPConnection(self.bmc, 443,
                                            verifycallback=self._certverify,
                                            timeout=180)
        wc.set_header('Content-Type', 'application/x-www-form-urlencoded')
        rsp, status = wc.grab_json_response_with_status(
            '/api/session', urlencode(authdata))

        if status < 200 or status >= 300:
            raise Exception('Error establishing web session')
        if 'CSRFToken' in rsp:
            self.csrftok = rsp['CSRFToken']
            wc.set_header('X-CSRFTOKEN', self.csrftok)
        self._wc = wc
        return wc


