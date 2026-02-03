# pylint: disable=C0301
"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.
This file has been automatically generated based on the ONTAP REST API documentation.
## Overview
You can use this endpoint to upload the DCN software image from the local system to the ONTAP cluster.
### Uploading a software package
The following example shows how to upload a DCN software package.
```python
import json
from netapp_ontap import HostConnection
from netapp_ontap.resources import DcnClusterSoftwareUpload
with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = DcnClusterSoftwareUpload()
    response = resource.upload(file_path="/path/to/image.tgz")
    print(json.dumps(response.http_response.json()), indent=4)
```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
{
    "uuid": "f0ce5ac2-3347-4fa9-9335-ff8f2212bdad",
    "state": "processing",
    "create_time": "2025-07-09T13:27:09-04:00"
}
```
"""
import os
import logging
from typing import Optional
from requests_toolbelt import MultipartEncoder  # type: ignore
from netapp_ontap import utils, HostConnection
from netapp_ontap.error import NetAppRestError
from netapp_ontap.resource import Resource
from netapp_ontap.response import NetAppResponse
LOGGER = logging.getLogger(__name__)
class DcnClusterSoftwareUpload(Resource):
    """Allows interaction with DcnClusterSoftwarePackage objects on the host"""
    _path = "/api/dcn/cluster/software/upload"
    @utils.api
    def upload(
        self, file_path, connection: Optional[HostConnection] = None, **kwargs
    ) -> NetAppResponse:
        """Upload this file to the host.
        Args:
            file_path: The path to the file to upload
            connection: The `netapp_ontap.host_connection.HostConnection` object
                to use for this API call. If unset, tries to use the connection
                which is set globally for the library or from the current context.
            **kwargs: Any key/value pairs passed will normally be sent as query parameters
                to the host. If any of these pairs are parameters that are sent as formdata then
                only parameters of that type will be accepted and all others will be discarded.
        Returns:
            A `netapp_ontap.response.NetAppResponse` object containing the
            details of the HTTP response.
        Raises:
            `netapp_ontap.error.NetAppRestError`: If the API call returned a status
                code >= 400
        """
        if not isinstance(file_path, str):
            raise NetAppRestError(
                f"file_path must be a string, got {type(file_path).__name__}"
            )
        if not os.path.exists(file_path):
            raise NetAppRestError(f"The file at {file_path} does not exist.")
        my_connection = connection if connection is not None else self.get_connection()
        with open(file_path, "rb") as f:
            file_name = os.path.basename(file_path)
            me = MultipartEncoder(
                fields={"file": (file_name, f, "application/octet-stream")}
            )
            url = f"{my_connection.origin}{self._location}"
            response = my_connection.session.post(
                url,
                data=me,
                params=kwargs,
                headers={"Content-Type": me.content_type},
            )
            self._last_response = NetAppResponse(response, connection=my_connection)
            return self._last_response
