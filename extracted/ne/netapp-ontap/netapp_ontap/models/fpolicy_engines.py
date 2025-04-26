r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FpolicyEngines", "FpolicyEnginesSchema"]
__pdoc__ = {
    "FpolicyEnginesSchema.resource": False,
    "FpolicyEnginesSchema.opts": False,
    "FpolicyEngines": False,
}


class FpolicyEnginesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FpolicyEngines object"""

    buffer_size = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_buffer_size.FpolicyEngineBufferSizeSchema", unknown=EXCLUDE, data_key="buffer_size", allow_none=True)
    r""" Specifies the send and receive buffer size of the connected socket for the FPolicy server. """

    certificate = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_certificate.FpolicyEngineCertificateSchema", unknown=EXCLUDE, data_key="certificate", allow_none=True)
    r""" Provides details about certificate used to authenticate the FPolicy server. """

    format = marshmallow_fields.Str(data_key="format", allow_none=True)
    r""" The format for the notification messages sent to the FPolicy servers.
  The possible values are:

    * xml  - Notifications sent to the FPolicy server will be formatted using the XML schema.
    * protobuf - Notifications sent to the FPolicy server will be formatted using Protobuf schema, which is a binary form.


Valid choices:

* xml
* protobuf """

    keep_alive_interval = marshmallow_fields.Str(data_key="keep_alive_interval", allow_none=True)
    r""" Specifies the ISO-8601 interval time for a storage appliance to send Keep Alive message to an FPolicy server. The allowed range is between 10 to 600 seconds.

Example: PT2M """

    max_server_requests = Size(data_key="max_server_requests", allow_none=True)
    r""" Specifies the maximum number of outstanding requests for the FPolicy server. It is used to specify maximum outstanding requests that will be queued up for the FPolicy server. The value for this field must be between 1 and 10000.  The default values are 500, 1000 or 2000 for Low-end(<64 GB memory), Mid-end(>=64 GB memory) and High-end(>=128 GB memory) Platforms respectively.

Example: 500 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Specifies the name to assign to the external server configuration.

Example: fp_ex_eng """

    port = Size(data_key="port", allow_none=True)
    r""" Port number of the FPolicy server application.

Example: 9876 """

    primary_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="primary_servers", allow_none=True)
    r""" The primary_servers field of the fpolicy_engines.

Example: ["10.132.145.20","10.140.101.109"] """

    request_abort_timeout = marshmallow_fields.Str(data_key="request_abort_timeout", allow_none=True)
    r""" Specifies the ISO-8601 timeout duration for a screen request to be aborted by a storage appliance. The allowed range is between 0 to 200 seconds.

Example: PT40S """

    request_cancel_timeout = marshmallow_fields.Str(data_key="request_cancel_timeout", allow_none=True)
    r""" Specifies the ISO-8601 timeout duration for a screen request to be processed by an FPolicy server. The allowed range is between 0 to 100 seconds.

Example: PT20S """

    resiliency = marshmallow_fields.Nested("netapp_ontap.models.fpolicy_engine_resiliency.FpolicyEngineResiliencySchema", unknown=EXCLUDE, data_key="resiliency", allow_none=True)
    r""" If all primary and secondary servers are down, or if no response is received from the FPolicy servers, file access events are stored inside the storage controller under the specified resiliency-directory-path. """

    secondary_servers = marshmallow_fields.List(marshmallow_fields.Str, data_key="secondary_servers", allow_none=True)
    r""" The secondary_servers field of the fpolicy_engines.

Example: ["10.132.145.20","10.132.145.21"] """

    server_progress_timeout = marshmallow_fields.Str(data_key="server_progress_timeout", allow_none=True)
    r""" Specifies the ISO-8601 timeout duration in which a throttled FPolicy server must complete at least one screen request. If no request is processed within the timeout, connection to the FPolicy server is terminated. The allowed range is between 0 to 100 seconds.

Example: PT1M """

    ssl_option = marshmallow_fields.Str(data_key="ssl_option", allow_none=True)
    r""" Specifies the SSL option for external communication with the FPolicy server. Possible values include the following:

* no_auth       When set to "no_auth", no authentication takes place.
* server_auth   When set to "server_auth", only the FPolicy server is authenticated by the SVM. With this option, before creating the FPolicy external engine, the administrator must install the public certificate of the certificate authority (CA) that signed the FPolicy server certificate.
* mutual_auth   When set to "mutual_auth", mutual authentication takes place between the SVM and the FPolicy server. This means authentication of the FPolicy server by the SVM along with authentication of the SVM by the FPolicy server. With this option, before creating the FPolicy external engine, the administrator must install the public certificate of the certificate authority (CA) that signed the FPolicy server certificate along with the public certificate and key file for authentication of the SVM.


Valid choices:

* no_auth
* server_auth
* mutual_auth """

    status_request_interval = marshmallow_fields.Str(data_key="status_request_interval", allow_none=True)
    r""" Specifies the ISO-8601 interval time for a storage appliance to query a status request from an FPolicy server. The allowed range is between 0 to 50 seconds.

Example: PT10S """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The notification mode determines what ONTAP does after sending notifications to FPolicy servers.
  The possible values are:

    * synchronous  - After sending a notification, wait for a response from the FPolicy server.
    * asynchronous - After sending a notification, file request processing continues.


Valid choices:

* synchronous
* asynchronous """

    @property
    def resource(self):
        return FpolicyEngines

    gettable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "name",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,name,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,type,"""

    patchable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,type,"""

    postable_fields = [
        "buffer_size",
        "certificate",
        "format",
        "keep_alive_interval",
        "max_server_requests",
        "name",
        "port",
        "primary_servers",
        "request_abort_timeout",
        "request_cancel_timeout",
        "resiliency",
        "secondary_servers",
        "server_progress_timeout",
        "ssl_option",
        "status_request_interval",
        "type",
    ]
    """buffer_size,certificate,format,keep_alive_interval,max_server_requests,name,port,primary_servers,request_abort_timeout,request_cancel_timeout,resiliency,secondary_servers,server_progress_timeout,ssl_option,status_request_interval,type,"""


class FpolicyEngines(Resource):

    _schema = FpolicyEnginesSchema
