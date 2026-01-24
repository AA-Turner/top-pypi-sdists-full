# servicenow_client.py
import json

import httpx
from httpx import HTTPError
from loguru import logger


class RequestSession:
    def __init__(self, url, auth, api_url, httpx_timeout=10):
        client = httpx.Client()
        client.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        if isinstance(auth, str):
            client.headers['x-sn-apikey'] = auth
        else:
            client.auth = auth
        client.timeout = httpx_timeout
        self._base_url = url
        if not api_url:
            self._api_url = url + "/api/now/"
        else:
            self._api_url = url + api_url
        self._request_sesh = client

    def _get(self, path, params=None, use_session=True):
        if use_session:
            self._response = self._request_sesh.get(
                self._api_url + f"{path}", params=params
            )
        else:
            self._request_sesh.get(f"{path}", params=params)
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _post(self, path, payload):
        self._response = self._request_sesh.post(
            self._api_url + f"{path}", json=payload
        )
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _post_files(self, path, parameters, file):
        self._request_sesh.headers.update({"Content-Type": "image/jpeg"})
        self._response = self._request_sesh.post(
            self._api_url + f"{path}", params=parameters, data=file
        )
        self._response.raise_for_status()

    def _put(self, path, payload):
        self._response = self._request_sesh.put(self._api_url + f"{path}", data=payload)
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _patch(self, path, payload):
        self._response = self._request_sesh.patch(
            self._api_url + f"{path}", data=payload
        )
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _delete(self, path):
        self._response = self._request_sesh.delete(self._api_url + f"{path}")
        self._response.raise_for_status()

    def get_all_records(self, table_name, limit=1000):
        all_records = []
        params = None
        if limit:
            params = {"sysparm_limit": limit}
        results = self._get(f"table/{table_name}", params=params)
        total_records = int(self._response.headers["X-Total-Count"])
        all_records.extend(results["result"])

        while len(all_records) < total_records:
            logger.debug(
                f"Total records: {total_records}, current records: {len(all_records)}"
            )
            next_urls = self._response.headers["link"].split(",")
            next_url = None
            for link in next_urls:
                if 'rel="next"' in link:
                    next_url = link.split(";")[0].strip("<>")
                    break
            if not next_url:
                break
            next_results = self._get(next_url, use_session=False)
            all_records.extend(next_results["result"])
        return {"result": all_records}

    def get_record_by_sys_id(self, table_name, sys_id):
        return self._get(f"table/{table_name}/{sys_id}")

    def insert_staging_record(self, table_name, payload):
        return self._post(f"import/{table_name}/insertMultiple", payload=payload)


class Incidents(RequestSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_all(self):
        return self._get("table/incident")

    def get_by_sys_id(self, sysid):
        return self._get(f"table/incident/{sysid}")

    def add_comment_to_inc(self, sysid, comment):
        payload = dict()
        payload["comments"] = comment
        payload = json.dumps(payload)
        return self._put(f"table/incident/{sysid}", payload=payload)

    def create_inc(self, description, comments):
        payload = dict()
        payload["short_description"] = description
        payload["comments"] = comments
        payload = json.dumps(payload)
        return self._post("table/incident", payload=payload)

    def add_attachment_to_inc(self, file_path, filename, sys_id):
        with open(file_path, "rb") as fp:
            params = dict()
            params["table_name"] = "incidents"
            params["table_sys_id"] = sys_id
            params["file_name"] = filename
            return self._post_files(f"attachment/file", parameters=params, file=fp)


class CoreCompany(RequestSession):
    def __int__(self, **kwargs):
        super.__init__(**kwargs)

    def get_all(self):
        return self._get(f"table/core_company")

    def create_vendor(self, vendor_name):
        payload = dict()
        payload["name"] = vendor_name.capitalize()
        payload["manufacturer"] = True
        payload = json.dumps(payload)
        self._post("table/core_company", payload=payload)
        return self._response_json["result"]["sys_id"], vendor_name


class Location(RequestSession):
    def __int__(self, **kwargs):
        super.__init__(**kwargs)

    def get_all(self):
        return self._get(f"table/cmn_location")

    def create_location(self, location_name):
        payload = dict()
        payload["name"] = location_name.capitalize()
        payload = json.dumps(payload)
        try:
            self._post("table/cmn_location", payload=payload)
        except HTTPError:
            return Exception
        return self._response_json["result"]["sys_id"]


class CmdbCi:
    def __init__(self, sesh_dict):
        self._sesh_dict = sesh_dict

    @property
    def net_gear(self):
        return NetGear(**self._sesh_dict)


class CMDB_Table(RequestSession):
    def __init__(self, table_name, **kwargs):
        super().__init__(**kwargs)
        self.table_name = table_name

    def get_all(self):
        return self._get(f"table/{self.table_name}")

    def create_ci(self, device_data):
        device_data = json.dumps(device_data)
        return self._post(f"table/{self.table_name}", payload=device_data)

    def update_ci(self, device_data, ci_sys_id):
        device_data = json.dumps(device_data)
        return self._patch(f"table/{self.table_name}/{ci_sys_id}", payload=device_data)

    def delete_ci(self, ci_sys_id):
        return self._delete(f"table/{self.table_name}/{ci_sys_id}")


class NetGear(CMDB_Table):
    def __init__(self, **kwargs):
        super().__init__("cmdb_ci_netgear", **kwargs)


class Change(RequestSession):
    def __init__(self, **kwargs):
        logger.warning(
            "Change class instantiated, this is still experimental. Use with caution. Not recommended for production."
        )
        kwargs["api_url"] = "/api/sn_chg_rest/"
        super().__init__(**kwargs)

    def get_all(self, params=None):
        return self._get("change", params=params)

    def get_by_sys_id(self, sysid):
        return self._get(f"change/{sysid}")

    def create_change_request(
        self,
        description,
        change_type="Standard",
    ):
        payload = dict()
        payload["chg_model"] = change_type
        payload["short_description"] = description
        payload["description"] = description
        payload["type"] = "Standard"
        payload = json.dumps(payload)
        return self._post("change", payload=payload)

    def get_change_states(self, sysid):
        return self._get(f"change/{sysid}/nextstates")

    def get_standard_change(self, sysid):
        self._get(f"change/standard/{sysid}")

    def update_change_request(self, sysid, payload):
        payload = json.dumps(payload)
        return self._patch(f"change/{sysid}", payload=payload)


class Snow:
    def __init__(self, auth, url, httpx_timeout=10, api_url=None):
        sesh_dict = dict()
        sesh_dict["auth"] = auth
        sesh_dict["url"] = url
        sesh_dict["httpx_timeout"] = httpx_timeout
        sesh_dict["api_url"] = api_url
        self._sesh_dict = sesh_dict

    @property
    def incidents(self):
        return Incidents(**self._sesh_dict)

    @property
    def vendors(self):
        return CoreCompany(**self._sesh_dict)

    @property
    def location(self):
        return Location(**self._sesh_dict)

    @property
    def cmdb(self):
        return CmdbCi(self._sesh_dict)

    @property
    def request_client(self):
        return RequestSession(**self._sesh_dict)

    @property
    def change_client(self):
        return Change(**self._sesh_dict)
