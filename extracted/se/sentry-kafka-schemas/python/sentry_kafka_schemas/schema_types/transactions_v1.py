from typing import Required, Union, Any, TypedDict, Literal, List, Dict, Tuple


ClientSdkInfo = Union["_ClientSdkInfoAnyof0"]
"""
client_sdk_info.

 The SDK Interface describes the Sentry SDK and its configuration used to capture and transmit an event.

Aggregation type: anyOf
"""



class TransactionEvent(TypedDict, total=False):
    """ transaction_event. """

    group_id: None
    group_ids: List[int]
    event_id: str
    organization_id: int
    project_id: int
    message: str
    platform: str
    datetime: str
    """ format: date-time """

    data: Required["_Data"]
    """ Required property """

    primary_hash: Union[str, None]
    retention_days: Union[int, None]
    occurrence_id: None
    occurrence_data: Dict[str, Any]
    is_new: bool
    is_regression: bool
    is_new_group_environment: bool
    queue: str
    skip_consume: bool
    group_states: None


_AppContext = Union["_AppContextAnyof0"]
"""
 Application information.

 App context describes the application. As opposed to the runtime, this is the actual
 application that was running and carries metadata about the current session.

Aggregation type: anyOf
"""



class _AppContextAnyof0(TypedDict, total=False):
    app_build: Union[str, None]
    """  Internal build ID as it appears on the platform. """

    app_identifier: Union[str, None]
    """  Version-independent application identifier, often a dotted bundle ID. """

    app_memory: Union[int, None]
    """
     Amount of memory used by the application in bytes.

    minimum: 0
    """

    app_name: Union[str, None]
    """  Application name as it appears on the platform. """

    app_start_time: Union[str, None]
    """
     Start time of the app.

     Formatted UTC timestamp when the user started the application.
    """

    app_version: Union[str, None]
    """  Application version as it appears on the platform. """

    build_type: Union[str, None]
    """  String identifying the kind of build. For example, `testflight`. """

    device_app_hash: Union[str, None]
    """  Application-specific device identifier. """

    in_foreground: Union[bool, None]
    """  A flag indicating whether the app is in foreground or not. An app is in foreground when it's visible to the user. """



class _Breakdowns(TypedDict, total=False):
    span_ops: Required[Dict[str, "_NumOfSpans"]]
    """ Required property """



_BrowserContext = Union["_BrowserContextAnyof0"]
"""
 Web browser information.

Aggregation type: anyOf
"""



class _BrowserContextAnyof0(TypedDict, total=False):
    name: Union[str, None]
    """  Display name of the browser application. """

    version: Union[str, None]
    """  Version string of the browser. """



class _ClientSdkInfoAnyof0(TypedDict, total=False):
    integrations: Union[List[Union[str, None]], None]
    """
     List of integrations that are enabled in the SDK. _Optional._

     The list should have all enabled integrations, including default integrations. Default
     integrations are included because different SDK releases may contain different default
     integrations.

    items:
      type:
      - string
      - 'null'
    """

    name: Required[Union[str, None]]
    """
     Unique SDK name. _Required._

     The name of the SDK. The format is `entity.ecosystem[.flavor]` where entity identifies the
     developer of the SDK, ecosystem refers to the programming language or platform where the
     SDK is to be used and the optional flavor is used to identify standalone SDKs that are part
     of a major ecosystem.

     Official Sentry SDKs use the entity `sentry`, as in `sentry.python` or
     `sentry.javascript.react-native`. Please use a different entity for your own SDKs.

    Required property
    """

    version: Required[Union[str, None]]
    """
     The version of the SDK. _Required._

     It should have the [Semantic Versioning](https://semver.org/) format `MAJOR.MINOR.PATCH`,
     without any prefix (no `v` or anything else in front of the major version number).

     Examples: `0.1.0`, `1.0.0`, `4.3.12`

    Required property
    """



_CloudResourceContext = Union["_CloudResourceContextAnyof0"]
"""
 Cloud Resource Context.

 This context describes the cloud resource the event originated from.

 Example:

 ```json
 "cloud_resource": {
     "cloud.account.id": "499517922981",
     "cloud.provider": "aws",
     "cloud.platform": "aws_ec2",
     "cloud.region": "us-east-1",
     "cloud.vavailability_zone": "us-east-1e",
     "host.id": "i-07d3301208fe0a55a",
     "host.type": "t2.large"
 }
 ```

Aggregation type: anyOf
"""



_CloudResourceContextAnyof0 = TypedDict('_CloudResourceContextAnyof0', {
    #  The cloud account ID the resource is assigned to.
    'cloud.account.id': Union[str, None],
    #  The zone where the resource is running.
    'cloud.availability_zone': Union[str, None],
    #  The cloud platform in use.
    #  The prefix of the service SHOULD match the one specified in cloud_provider.
    'cloud.platform': Union[str, None],
    #  Name of the cloud provider.
    'cloud.provider': Union[str, None],
    #  The geographical region the resource is running.
    'cloud.region': Union[str, None],
    #  Unique host ID.
    'host.id': Union[str, None],
    #  Machine type of the host.
    'host.type': Union[str, None],
}, total=False)


_Context = Union["_DeviceContext", "_OsContext", "_RuntimeContext", "_AppContext", "_BrowserContext", "_GpuContext", "_TraceContext", "_ProfileContext", "_MonitorContext", "_ResponseContext", "_OtelContext", "_CloudResourceContext", Dict[str, Any]]
"""
 A context describes environment info (e.g. device, os or browser).

Aggregation type: anyOf
"""



_Contexts = Union[Dict[str, "_ContextsAnyof0Additionalproperties"]]
"""
 The Contexts Interface provides additional context data. Typically, this is data related to the
 current user and the environment. For example, the device or application version. Its canonical
 name is `contexts`.

 The `contexts` type can be used to define arbitrary contextual data on the event. It accepts an
 object of key/value pairs. The key is the “alias” of the context and can be freely chosen.
 However, as per policy, it should match the type of the context unless there are two values for
 a type. You can omit `type` if the key name is the type.

 Unknown data for the contexts is rendered as a key/value list.

 For more details about sending additional data with your event, see the [full documentation on
 Additional Data](https://docs.sentry.io/enriching-error-data/additional-data/).

Aggregation type: anyOf
"""



_ContextsAnyof0Additionalproperties = Union["_Context", None]
""" Aggregation type: anyOf """



_Cookies = Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
"""
 A map holding cookies.

anyOf:
  - anyOf:
    - additionalProperties:
        type:
        - string
        - 'null'
      type: object
    - items:
        items:
        - type:
          - string
          - 'null'
        - type:
          - string
          - 'null'
        maxItems: 2
        minItems: 2
        type:
        - array
        - 'null'
      type: array
"""



class _Data(TypedDict, total=False):
    type: Required[str]
    """ Required property """

    transaction: Union[str, None]
    """
     Transaction name of the event.

     For example, in a web app, this might be the route name (`"/users/<username>/"` or
     `UserView`), in a task queue it might be the function + module name.
    """

    transaction_info: "_TransactionInfo"
    """
     Additional information about the name of the transaction.

    Aggregation type: anyOf
    """

    timestamp: Required[Union[int, float]]
    """ Required property """

    start_timestamp: Required[Union[int, float]]
    """ Required property """

    received: Required[Union[int, float]]
    """ Required property """

    release: Union[str, None]
    """
     The release version of the application.

     **Release versions must be unique across all projects in your organization.** This value
     can be the git SHA for the given project, or a product identifier with a semantic version.
    """

    environment: Union[str, None]
    """
     The environment name, such as `production` or `staging`.

     ```json
     { "environment": "production" }
     ```
    """

    contexts: Required["_Contexts"]
    """
     The Contexts Interface provides additional context data. Typically, this is data related to the
     current user and the environment. For example, the device or application version. Its canonical
     name is `contexts`.

     The `contexts` type can be used to define arbitrary contextual data on the event. It accepts an
     object of key/value pairs. The key is the “alias” of the context and can be freely chosen.
     However, as per policy, it should match the type of the context unless there are two values for
     a type. You can omit `type` if the key name is the type.

     Unknown data for the contexts is rendered as a key/value list.

     For more details about sending additional data with your event, see the [full documentation on
     Additional Data](https://docs.sentry.io/enriching-error-data/additional-data/).

    Aggregation type: anyOf

    Required property
    """

    tags: "_DataTags"
    """
     Custom tags for this event.

     A map or list of tags for this event. Each tag must be less than 200 characters.

    Aggregation type: anyOf
    """

    extra: "_Extra"
    """
     Arbitrary extra information set by the user.

     ```json
     {
         "extra": {
             "my_key": 1,
             "some_other_value": "foo bar"
         }
     }```

    additionalProperties: True
    """

    sdk: "ClientSdkInfo"
    """
    client_sdk_info.

     The SDK Interface describes the Sentry SDK and its configuration used to capture and transmit an event.

    Aggregation type: anyOf
    """

    project: int
    spans: Required[List["_Span"]]
    """ Required property """

    measurements: "_Measurements"
    breakdowns: "_Breakdowns"
    culprit: str
    title: str
    location: str


_DataTags = Union["_Tags", None]
"""
 Custom tags for this event.

 A map or list of tags for this event. Each tag must be less than 200 characters.

Aggregation type: anyOf
"""



_DeviceContext = Union["_DeviceContextAnyof0"]
"""
 Device information.

 Device context describes the device that caused the event. This is most appropriate for mobile
 applications.

Aggregation type: anyOf
"""



class _DeviceContextAnyof0(TypedDict, total=False):
    arch: Union[str, None]
    """  Native cpu architecture of the device. """

    battery_level: Union[Union[int, float], None]
    """
     Current battery level in %.

     If the device has a battery, this can be a floating point value defining the battery level
     (in the range 0-100).
    """

    battery_status: Union[str, None]
    """
     Status of the device's battery.

     For example, `Unknown`, `Charging`, `Discharging`, `NotCharging`, `Full`.
    """

    boot_time: Union[str, None]
    """  Indicator when the device was booted. """

    brand: Union[str, None]
    """  Brand of the device. """

    charging: Union[bool, None]
    """  Whether the device was charging or not. """

    cpu_description: Union[str, None]
    """
     CPU description.

     For example, Intel(R) Core(TM)2 Quad CPU Q6600 @ 2.40GHz.
    """

    device_type: Union[str, None]
    """
     Kind of device the application is running on.

     For example, `Unknown`, `Handheld`, `Console`, `Desktop`.
    """

    device_unique_identifier: Union[str, None]
    """  Unique device identifier. """

    external_free_storage: Union[int, None]
    """
     Free size of the attached external storage in bytes (eg: android SDK card).

    minimum: 0
    """

    external_storage_size: Union[int, None]
    """
     Total size of the attached external storage in bytes (eg: android SDK card).

    minimum: 0
    """

    family: Union[str, None]
    """
     Family of the device model.

     This is usually the common part of model names across generations. For instance, `iPhone`
     would be a reasonable family, so would be `Samsung Galaxy`.
    """

    free_memory: Union[int, None]
    """
     How much memory is still available in bytes.

    minimum: 0
    """

    free_storage: Union[int, None]
    """
     How much storage is free in bytes.

    minimum: 0
    """

    low_memory: Union[bool, None]
    """  Whether the device was low on memory. """

    manufacturer: Union[str, None]
    """  Manufacturer of the device. """

    memory_size: Union[int, None]
    """
     Total memory available in bytes.

    minimum: 0
    """

    model: Union[str, None]
    """
     Device model.

     This, for example, can be `Samsung Galaxy S3`.
    """

    model_id: Union[str, None]
    """
     Device model (internal identifier).

     An internal hardware revision to identify the device exactly.
    """

    name: Union[str, None]
    """  Name of the device. """

    online: Union[bool, None]
    """  Whether the device was online or not. """

    orientation: Union[str, None]
    """
     Current screen orientation.

     This can be a string `portrait` or `landscape` to define the orientation of a device.
    """

    processor_count: Union[int, None]
    """
     Number of "logical processors".

     For example, 8.

    minimum: 0
    """

    processor_frequency: Union[int, None]
    """
     Processor frequency in MHz.

     Note that the actual CPU frequency might vary depending on current load and
     power conditions, especially on low-powered devices like phones and laptops.

    minimum: 0
    """

    screen_density: Union[Union[int, float], None]
    """  Device screen density. """

    screen_dpi: Union[int, None]
    """
     Screen density as dots-per-inch.

    minimum: 0
    """

    screen_resolution: Union[str, None]
    """
     Device screen resolution.

     (e.g.: 800x600, 3040x1444)
    """

    simulator: Union[bool, None]
    """  Simulator/prod indicator. """

    storage_size: Union[int, None]
    """
     Total storage size of the device in bytes.

    minimum: 0
    """

    supports_accelerometer: Union[bool, None]
    """  Whether the accelerometer is available on the device. """

    supports_audio: Union[bool, None]
    """  Whether audio is available on the device. """

    supports_gyroscope: Union[bool, None]
    """  Whether the gyroscope is available on the device. """

    supports_location_service: Union[bool, None]
    """  Whether location support is available on the device. """

    supports_vibration: Union[bool, None]
    """  Whether vibration is available on the device. """

    timezone: Union[str, None]
    """  Timezone of the device. """

    usable_memory: Union[int, None]
    """
     How much memory is usable for the app in bytes.

    minimum: 0
    """



_EventId = Union[str]
"""
 Wrapper around a UUID with slightly different formatting.

Aggregation type: anyOf
"""



_Extra = Union[Dict[str, Any], None]
"""
 Arbitrary extra information set by the user.

 ```json
 {
     "extra": {
         "my_key": 1,
         "some_other_value": "foo bar"
     }
 }```

additionalProperties: True
"""



_GpuContext = Union["_GpuContextAnyof0"]
"""
 GPU information.

 Example:

 ```json
 "gpu": {
   "name": "AMD Radeon Pro 560",
   "vendor_name": "Apple",
   "memory_size": 4096,
   "api_type": "Metal",
   "multi_threaded_rendering": true,
   "version": "Metal",
   "npot_support": "Full"
 }
 ```

Aggregation type: anyOf
"""



class _GpuContextAnyof0(TypedDict, total=False):
    api_type: Union[str, None]
    """
     The device low-level API type.

     Examples: `"Apple Metal"` or `"Direct3D11"`
    """

    graphics_shader_level: Union[str, None]
    """
     Approximate "shader capability" level of the graphics device.

     For Example: Shader Model 2.0, OpenGL ES 3.0, Metal / OpenGL ES 3.1, 27 (unknown)
    """

    id: Union[None, str]
    """  The PCI identifier of the graphics device. """

    max_texture_size: Union[int, None]
    """
     Largest size of a texture that is supported by the graphics hardware.

     For Example: 16384

    minimum: 0
    """

    memory_size: Union[int, None]
    """
     The total GPU memory available in Megabytes.

    minimum: 0
    """

    multi_threaded_rendering: Union[bool, None]
    """  Whether the GPU has multi-threaded rendering or not. """

    name: Union[str, None]
    """  The name of the graphics device. """

    npot_support: Union[str, None]
    """  The Non-Power-Of-Two support. """

    supports_compute_shaders: Union[bool, None]
    """  Whether compute shaders are available on the device. """

    supports_draw_call_instancing: Union[bool, None]
    """  Whether GPU draw call instancing is supported. """

    supports_geometry_shaders: Union[bool, None]
    """  Whether geometry shaders are available on the device. """

    supports_ray_tracing: Union[bool, None]
    """  Whether ray tracing is available on the device. """

    vendor_id: Union[str, None]
    """  The PCI vendor identifier of the graphics device. """

    vendor_name: Union[str, None]
    """  The vendor name as reported by the graphics device. """

    version: Union[str, None]
    """  The Version of the graphics device. """



_Headers = Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
"""
 A map holding headers.

anyOf:
  - anyOf:
    - additionalProperties:
        anyOf:
        - $ref: '#/definitions/HeaderValue'
        - type: 'null'
      type: object
    - items:
        items:
        - anyOf:
          - $ref: '#/definitions/HeaderName'
          - type: 'null'
        - anyOf:
          - $ref: '#/definitions/HeaderValue'
          - type: 'null'
        maxItems: 2
        minItems: 2
        type:
        - array
        - 'null'
      type: array
"""



class _Measurements(TypedDict, total=False):
    num_of_spans: "_NumOfSpans"


_MonitorContext = Union[Dict[str, Any]]
"""
 Monitor information.

Aggregation type: anyOf
"""



class _NumOfSpans(TypedDict, total=False):
    value: Required[Union[int, float]]
    """ Required property """

    unit: str


_OsContext = Union["_OsContextAnyof0"]
"""
 Operating system information.

 OS context describes the operating system on which the event was created. In web contexts, this
 is the operating system of the browser (generally pulled from the User-Agent string).

Aggregation type: anyOf
"""



class _OsContextAnyof0(TypedDict, total=False):
    build: Union[str, None]
    """  Internal build number of the operating system. """

    kernel_version: Union[str, None]
    """
     Current kernel version.

     This is typically the entire output of the `uname` syscall.
    """

    name: Union[str, None]
    """  Name of the operating system. """

    raw_description: Union[str, None]
    """
     Unprocessed operating system info.

     An unprocessed description string obtained by the operating system. For some well-known
     runtimes, Sentry will attempt to parse `name` and `version` from this string, if they are
     not explicitly given.
    """

    rooted: Union[bool, None]
    """  Indicator if the OS is rooted (mobile mostly). """

    version: Union[str, None]
    """  Version of the operating system. """



_OtelContext = Union["_OtelContextAnyof0"]
"""
 OpenTelemetry Context

 If an event has this context, it was generated from an OpenTelemetry signal (trace, metric, log).

Aggregation type: anyOf
"""



class _OtelContextAnyof0(TypedDict, total=False):
    attributes: Union[Dict[str, Any], None]
    """
     Attributes of the OpenTelemetry span that maps to a Sentry event.

     <https://github.com/open-telemetry/opentelemetry-proto/blob/724e427879e3d2bae2edc0218fff06e37b9eb46e/opentelemetry/proto/trace/v1/trace.proto#L174-L186>

    additionalProperties: True
    """

    resource: Union[Dict[str, Any], None]
    """
     Information about an OpenTelemetry resource.

     <https://github.com/open-telemetry/opentelemetry-proto/blob/724e427879e3d2bae2edc0218fff06e37b9eb46e/opentelemetry/proto/resource/v1/resource.proto>

    additionalProperties: True
    """



_ProfileContext = Union["_ProfileContextAnyof0"]
"""
 Profile context

Aggregation type: anyOf
"""



class _ProfileContextAnyof0(TypedDict, total=False):
    profile_id: Required["_ProfileContextAnyof0ProfileId"]
    """
     The profile ID.

    Aggregation type: anyOf

    Required property
    """



_ProfileContextAnyof0ProfileId = Union["_EventId", None]
"""
 The profile ID.

Aggregation type: anyOf
"""



_ResponseContext = Union["_ResponseContextAnyof0"]
"""
 Response interface that contains information on a HTTP response related to the event.

Aggregation type: anyOf
"""



class _ResponseContextAnyof0(TypedDict, total=False):
    body_size: Union[int, None]
    """
     HTTP response body size.

    minimum: 0
    """

    cookies: "_ResponseContextAnyof0Cookies"
    """
     The cookie values.

     Can be given unparsed as string, as dictionary, or as a list of tuples.

    Aggregation type: anyOf
    """

    headers: "_ResponseContextAnyof0Headers"
    """
     A dictionary of submitted headers.

     If a header appears multiple times it, needs to be merged according to the HTTP standard
     for header merging. Header names are treated case-insensitively by Sentry.

    Aggregation type: anyOf
    """

    status_code: Union[int, None]
    """
     HTTP status code.

    minimum: 0
    """



_ResponseContextAnyof0Cookies = Union["_Cookies", None]
"""
 The cookie values.

 Can be given unparsed as string, as dictionary, or as a list of tuples.

Aggregation type: anyOf
"""



_ResponseContextAnyof0Headers = Union["_Headers", None]
"""
 A dictionary of submitted headers.

 If a header appears multiple times it, needs to be merged according to the HTTP standard
 for header merging. Header names are treated case-insensitively by Sentry.

Aggregation type: anyOf
"""



_RuntimeContext = Union["_RuntimeContextAnyof0"]
"""
 Runtime information.

 Runtime context describes a runtime in more detail. Typically, this context is present in
 `contexts` multiple times if multiple runtimes are involved (for instance, if you have a
 JavaScript application running on top of JVM).

Aggregation type: anyOf
"""



class _RuntimeContextAnyof0(TypedDict, total=False):
    build: Union[str, None]
    """  Application build string, if it is separate from the version. """

    name: Union[str, None]
    """  Runtime name. """

    raw_description: Union[str, None]
    """
     Unprocessed runtime info.

     An unprocessed description string obtained by the runtime. For some well-known runtimes,
     Sentry will attempt to parse `name` and `version` from this string, if they are not
     explicitly given.
    """

    version: Union[str, None]
    """  Runtime version string. """



class _Span(TypedDict, total=False):
    timestamp: Required[Union[int, float]]
    """ Required property """

    start_timestamp: Required[Union[int, float]]
    """ Required property """

    exclusive_time: Union[int, float]
    description: Union[str, None]
    op: str
    span_id: Required[str]
    """ Required property """

    parent_span_id: Union[str, None]
    trace_id: Required[str]
    """ Required property """

    same_process_as_parent: Union[bool, None]
    tags: Required[Union[Dict[str, Any], None]]
    """ Required property """

    data: Required[Union[Dict[str, Any], None]]
    """ Required property """

    hash: str


_SpanId = Union[str]
"""
 A 16-character hex string as described in the W3C trace context spec.

Aggregation type: anyOf
"""



_SpanStatus = Union[Literal['ok'], Literal['cancelled'], Literal['unknown'], Literal['invalid_argument'], Literal['deadline_exceeded'], Literal['not_found'], Literal['already_exists'], Literal['permission_denied'], Literal['resource_exhausted'], Literal['failed_precondition'], Literal['aborted'], Literal['out_of_range'], Literal['unimplemented'], Literal['internal_error'], Literal['unavailable'], Literal['data_loss'], Literal['unauthenticated']]
"""
Trace status.

Values from <https://github.com/open-telemetry/opentelemetry-specification/blob/8fb6c14e4709e75a9aaa64b0dbbdf02a6067682a/specification/api-tracing.md#status> Mapping to HTTP from <https://github.com/open-telemetry/opentelemetry-specification/blob/8fb6c14e4709e75a9aaa64b0dbbdf02a6067682a/specification/data-http.md#status>
"""
_SPANSTATUS_OK: Literal['ok'] = "ok"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_CANCELLED: Literal['cancelled'] = "cancelled"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_UNKNOWN: Literal['unknown'] = "unknown"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_INVALID_ARGUMENT: Literal['invalid_argument'] = "invalid_argument"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_DEADLINE_EXCEEDED: Literal['deadline_exceeded'] = "deadline_exceeded"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_NOT_FOUND: Literal['not_found'] = "not_found"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_ALREADY_EXISTS: Literal['already_exists'] = "already_exists"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_PERMISSION_DENIED: Literal['permission_denied'] = "permission_denied"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_RESOURCE_EXHAUSTED: Literal['resource_exhausted'] = "resource_exhausted"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_FAILED_PRECONDITION: Literal['failed_precondition'] = "failed_precondition"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_ABORTED: Literal['aborted'] = "aborted"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_OUT_OF_RANGE: Literal['out_of_range'] = "out_of_range"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_UNIMPLEMENTED: Literal['unimplemented'] = "unimplemented"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_INTERNAL_ERROR: Literal['internal_error'] = "internal_error"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_UNAVAILABLE: Literal['unavailable'] = "unavailable"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_DATA_LOSS: Literal['data_loss'] = "data_loss"
"""The values for the 'Trace status' enum"""
_SPANSTATUS_UNAUTHENTICATED: Literal['unauthenticated'] = "unauthenticated"
"""The values for the 'Trace status' enum"""



_TagEntry = Union["_TagEntryAnyof0", None]
""" Aggregation type: anyOf """



_TagEntryAnyof0 = Tuple[Union[str, None], Union[str, None]]
"""
maxItems: 2
minItems: 2
"""



_Tags = List["_TagEntry"]
"""  Manual key/value tag pairs. """



_TraceContext = Union["_TraceContextAnyof0"]
"""
 Trace context

Aggregation type: anyOf
"""



class _TraceContextAnyof0(TypedDict, total=False):
    client_sample_rate: Union[Union[int, float], None]
    """
     The client-side sample rate as reported in the envelope's `trace.sample_rate` header.

     The server takes this field from envelope headers and writes it back into the event. Clients
     should not ever send this value.
    """

    exclusive_time: Union[Union[int, float], None]
    """
     The amount of time in milliseconds spent in this transaction span,
     excluding its immediate child spans.
    """

    op: Union[str, None]
    """  Span type (see `OperationType` docs). """

    parent_span_id: "_TraceContextAnyof0ParentSpanId"
    """
     The ID of the span enclosing this span.

    Aggregation type: anyOf
    """

    span_id: Required["_TraceContextAnyof0SpanId"]
    """
     The ID of the span.

    Aggregation type: anyOf

    Required property
    """

    status: "_TraceContextAnyof0Status"
    """
     Whether the trace failed or succeeded. Currently only used to indicate status of individual
     transactions.

    Aggregation type: anyOf
    """

    trace_id: Required["_TraceContextAnyof0TraceId"]
    """
     The trace ID.

    Aggregation type: anyOf

    Required property
    """



_TraceContextAnyof0ParentSpanId = Union["_SpanId", None]
"""
 The ID of the span enclosing this span.

Aggregation type: anyOf
"""



_TraceContextAnyof0SpanId = Union["_SpanId", None]
"""
 The ID of the span.

Aggregation type: anyOf
"""



_TraceContextAnyof0Status = Union["_SpanStatus", None]
"""
 Whether the trace failed or succeeded. Currently only used to indicate status of individual
 transactions.

Aggregation type: anyOf
"""



_TraceContextAnyof0TraceId = Union["_TraceId", None]
"""
 The trace ID.

Aggregation type: anyOf
"""



_TraceId = Union[str]
"""
 A 32-character hex string as described in the W3C trace context spec.

Aggregation type: anyOf
"""



_TransactionInfo = Union["_TransactionInfoAnyof0"]
"""
 Additional information about the name of the transaction.

Aggregation type: anyOf
"""



class _TransactionInfoAnyof0(TypedDict, total=False):
    source: Union[str, None]
    """
    Describes how the name of the transaction was determined.

     This will be used by the server to decide whether or not to scrub identifiers from the
     transaction name, or replace the entire name with a placeholder.
    """

