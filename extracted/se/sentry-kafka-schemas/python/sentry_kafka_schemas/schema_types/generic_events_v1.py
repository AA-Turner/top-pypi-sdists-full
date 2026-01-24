from typing import Required, Union, Any, TypedDict, Literal, List, Dict, Tuple


ClientSdkInfo = Union["_ClientSdkInfoAnyof0"]
"""
client_sdk_info.

 The SDK Interface describes the Sentry SDK and its configuration used to capture and transmit an event.

Aggregation type: anyOf
"""



GenericEvent = Union[Tuple[Literal[2], Literal['insert'], "InsertEvent", "_GroupInformation"]]
"""
generic_event.

Issue platform event

Aggregation type: anyOf
"""



class InsertEvent(TypedDict, total=False):
    """ insert_event. """

    data: Required["SentryEvent"]
    """
    sentry_event.

    The sentry v7 event structure.

    Required property
    """

    datetime: Required[str]
    """ Required property """

    event_id: Required["_EventId"]
    """
     Wrapper around a UUID with slightly different formatting.

    Aggregation type: anyOf

    Required property
    """

    group_id: Required[int]
    """ Required property """

    group_ids: List[int]
    message: Required[str]
    """ Required property """

    organization_id: int
    platform: Required[str]
    """ Required property """

    primary_hash: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    retention_days: Union[int, None]
    occurrence_id: Required[str]
    """ Required property """

    occurrence_data: Required["_InsertEventOccurrenceData"]
    """ Required property """



class SentryEvent(TypedDict, total=False):
    """
    sentry_event.

    The sentry v7 event structure.
    """

    type: "_SentryEventType"
    """
     Type of the event. Defaults to `default`.

     The event type determines how Sentry handles the event and has an impact on processing, rate
     limiting, and quotas. There are three fundamental classes of event types:

      - **Error monitoring events**: Processed and grouped into unique issues based on their
        exception stack traces and error messages.
      - **Security events**: Derived from Browser security violation reports and grouped into
        unique issues based on the endpoint and violation. SDKs do not send such events.
      - **Transaction events** (`transaction`): Contain operation spans and collected into traces
        for performance monitoring.

     Transactions must explicitly specify the `"transaction"` event type. In all other cases,
     Sentry infers the appropriate event type from the payload and overrides the stated type.
     SDKs should not send an event type other than for transactions.

     Example:

     ```json
     {
       "type": "transaction",
       "spans": []
     }
     ```

    Aggregation type: anyOf
    """

    contexts: "_SentryEventContexts"
    """
     Contexts describing the environment (e.g. device, os or browser).

    Aggregation type: anyOf
    """

    culprit: Union[str, None]
    """
     Custom culprit of the event.

     This field is deprecated and shall not be set by client SDKs.
    """

    dist: Union[str, None]
    """
     Program's distribution identifier.

     The distribution of the application.

     Distributions are used to disambiguate build or deployment variants of the same release of
     an application. For example, the dist can be the build number of an XCode build or the
     version code of an Android build.
    """

    environment: Union[str, None]
    """
     The environment name, such as `production` or `staging`.

     ```json
     { "environment": "production" }
     ```
    """

    errors: Union[List["_SentryEventErrorsArrayItem"], None]
    """
     Errors encountered during processing. Intended to be phased out in favor of
     annotation/metadata system.

    default: None
    items:
      anyOf:
      - $ref: '#/definitions/EventProcessingError'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """

    event_id: "_SentryEventEventId"
    """
     Unique identifier of this event.

     Hexadecimal string representing a uuid4 value. The length is exactly 32 characters. Dashes
     are not allowed. Has to be lowercase.

     Even though this field is backfilled on the server with a new uuid4, it is strongly
     recommended to generate that uuid4 clientside. There are some features like user feedback
     which are easier to implement that way, and debugging in case events get lost in your
     Sentry installation is also easier.

     Example:

     ```json
     {
       "event_id": "fc6d8c0c43fc4630ad850ee518f1b9d0"
     }
     ```

    Aggregation type: anyOf
    """

    exception: "_SentryEventException"
    """ Aggregation type: anyOf """

    threads: "_SentryEventThreads"
    """ Aggregation type: anyOf """

    extra: Union[Dict[str, Any], None]
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

    fingerprint: "_SentryEventFingerprint"
    """
     Manual fingerprint override.

     A list of strings used to dictate how this event is supposed to be grouped with other
     events into issues. For more information about overriding grouping see [Customize Grouping
     with Fingerprints](https://docs.sentry.io/data-management/event-grouping/).

     ```json
     {
         "fingerprint": ["myrpc", "POST", "/foo.bar"]
     }

    Aggregation type: anyOf
    """

    level: "_SentryEventLevel"
    """
     Severity level of the event. Defaults to `error`.

     Example:

     ```json
     {"level": "warning"}
     ```

    Aggregation type: anyOf
    """

    logentry: "_SentryEventLogentry"
    """
     Custom parameterized message for this event.

    Aggregation type: anyOf
    """

    logger: Union[str, None]
    """  Logger that created the event. """

    modules: Union[Dict[str, Union[str, None]], None]
    """
     Name and versions of all installed modules/packages/dependencies in the current
     environment/application.

     ```json
     { "django": "3.0.0", "celery": "4.2.1" }
     ```

     In Python this is a list of installed packages as reported by `pkg_resources` together with
     their reported version string.

     This is primarily used for suggesting to enable certain SDK integrations from within the UI
     and for making informed decisions on which frameworks to support in future development
     efforts.

    additionalProperties:
      type:
      - string
      - 'null'
    """

    platform: Union[str, None]
    """
     Platform identifier of this event (defaults to "other").

     A string representing the platform the SDK is submitting from. This will be used by the
     Sentry interface to customize various components in the interface, but also to enter or
     skip stacktrace processing.

     Acceptable values are: `as3`, `c`, `cfml`, `cocoa`, `csharp`, `elixir`, `haskell`, `go`,
     `groovy`, `java`, `javascript`, `native`, `node`, `objc`, `other`, `perl`, `php`, `python`,
     `ruby`
    """

    received: Required["_Timestamp"]
    """
    Can be a ISO-8601 formatted string or a unix timestamp in seconds (floating point values allowed).

    Must be UTC.

    Aggregation type: anyOf

    Required property
    """

    release: Union[str, None]
    """
     The release version of the application.

     **Release versions must be unique across all projects in your organization.** This value
     can be the git SHA for the given project, or a product identifier with a semantic version.
    """

    request: "_SentryEventRequest"
    """
     Information about a web request that occurred during the event.

    Aggregation type: anyOf
    """

    sdk: "_SentryEventSdk"
    """
     Information about the Sentry SDK that generated this event.

    Aggregation type: anyOf
    """

    server_name: Union[str, None]
    """
     Server or device name the event was generated on.

     This is supposed to be a hostname.
    """

    stacktrace: "_SentryEventStacktrace"
    """
     Event stacktrace.

     DEPRECATED: Prefer `threads` or `exception` depending on which is more appropriate.

    Aggregation type: anyOf
    """

    tags: "_SentryEventTags"
    """
     Custom tags for this event.

     A map or list of tags for this event. Each tag must be less than 200 characters.

    Aggregation type: anyOf
    """

    time_spent: Union[int, None]
    """
     Time since the start of the transaction until the error occurred.

    minimum: 0
    """

    timestamp: "_SentryEventTimestamp"
    """
     Timestamp when the event was created.

     Indicates when the event was created in the Sentry SDK. The format is either a string as
     defined in [RFC 3339](https://tools.ietf.org/html/rfc3339) or a numeric (integer or float)
     value representing the number of seconds that have elapsed since the [Unix
     epoch](https://en.wikipedia.org/wiki/Unix_time).

     Timezone is assumed to be UTC if missing.

     Sub-microsecond precision is not preserved with numeric values due to precision
     limitations with floats (at least in our systems). With that caveat in mind, just send
     whatever is easiest to produce.

     All timestamps in the event protocol are formatted this way.

     # Example

     All of these are the same date:

     ```json
     { "timestamp": "2011-05-02T17:41:36Z" }
     { "timestamp": "2011-05-02T17:41:36" }
     { "timestamp": "2011-05-02T17:41:36.000" }
     { "timestamp": 1304358096.0 }
     ```

    Aggregation type: anyOf
    """

    transaction: Union[str, None]
    """
     Transaction name of the event.

     For example, in a web app, this might be the route name (`"/users/<username>/"` or
     `UserView`), in a task queue it might be the function + module name.
    """

    transaction_info: "_SentryEventTransactionInfo"
    """
     Additional information about the name of the transaction.

    Aggregation type: anyOf
    """

    user: "_SentryEventUser"
    """
     Information about the user who triggered this event.

    Aggregation type: anyOf
    """

    version: Union[str, None]
    """  Version """



class SentryExceptionChain(TypedDict, total=False):
    """
    sentry_exception_chain.

     One or multiple chained (nested) exceptions.
    """

    values: Union[None, List["_SentryExceptionChainValuesArrayItem"]]
    """
    items:
      anyOf:
      - $ref: '#/definitions/Exception'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



SentryRequest = Union["_SentryRequestAnyof0"]
"""
sentry_request.

 Http request information.

 The Request interface contains information on a HTTP request related to the event. In client
 SDKs, this can be an outgoing request, or the request that rendered the current web page. On
 server SDKs, this could be the incoming web request that is being handled.

 The data variable should only contain the request body (not the query string). It can either be
 a dictionary (for standard HTTP requests) or a raw request body.

 ### Ordered Maps

 In the Request interface, several attributes can either be declared as string, object, or list
 of tuples. Sentry attempts to parse structured information from the string representation in
 such cases.

 Sometimes, keys can be declared multiple times, or the order of elements matters. In such
 cases, use the tuple representation over a plain object.

 Example of request headers as object:

 ```json
 {
   "content-type": "application/json",
   "accept": "application/json, application/xml"
 }
 ```

 Example of the same headers as list of tuples:

 ```json
 [
   ["content-type", "application/json"],
   ["accept", "application/json"],
   ["accept", "application/xml"]
 ]
 ```

 Example of a fully populated request object:

 ```json
 {
   "request": {
     "method": "POST",
     "url": "http://absolute.uri/foo",
     "query_string": "query=foobar&page=2",
     "data": {
       "foo": "bar"
     },
     "cookies": "PHPSESSID=298zf09hf012fh2; csrftoken=u32t4o3tb3gg43; _gat=1;",
     "headers": {
       "content-type": "text/html"
     },
     "env": {
       "REMOTE_ADDR": "192.168.0.1"
     }
   }
 }
 ```

Aggregation type: anyOf
"""



class SentryThreadChain(TypedDict, total=False):
    """
    sentry_thread_chain.

     One or multiple threads.
    """

    values: Required[Union[None, List["_SentryThreadChainValuesArrayItem"]]]
    """
    items:
      anyOf:
      - $ref: '#/definitions/Thread'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null

    Required property
    """



SentryUser = Union["_SentryUserAnyof0"]
"""
sentry_user.

 Information about the user who triggered an event.

 ```json
 {
   "user": {
     "id": "unique_id",
     "username": "my_user",
     "email": "foo@example.com",
     "ip_address": "127.0.0.1",
     "subscription": "basic"
   }
 }
 ```

Aggregation type: anyOf
"""



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



_EVENT_PROCESSING_ERROR_ANYOF0_NAME_DEFAULT = None
""" Default value of the field path 'event processing error anyof0 name' """



_EVENT_PROCESSING_ERROR_ANYOF0_VALUE_DEFAULT = None
""" Default value of the field path 'event processing error anyof0 value' """



_EventId = Union[str]
"""
 Wrapper around a UUID with slightly different formatting.

Aggregation type: anyOf
"""



_EventProcessingError = Union["_EventProcessingErrorAnyof0"]
"""
 An event processing error.

Aggregation type: anyOf
"""



class _EventProcessingErrorAnyof0(TypedDict, total=False):
    name: Union[str, None]
    """
     Affected key or deep path.

    default: None
    """

    type: Required[Union[str, None]]
    """
     The error kind.

    Required property
    """

    value: Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
    """
     The original value causing this error.

    default: None
    """



_EventType = Union[Literal['error'], Literal['csp'], Literal['hpkp'], Literal['expectct'], Literal['expectstaple'], Literal['transaction'], Literal['nel'], Literal['default'], Literal['generic'], Literal['feedback']]
"""
The type of an event.

The event type determines how Sentry handles the event and has an impact on processing, rate limiting, and quotas. There are three fundamental classes of event types:

- **Error monitoring events** (`default`, `error`): Processed and grouped into unique issues based on their exception stack traces and error messages. - **Security events** (`csp`, `hpkp`, `expectct`, `expectstaple`): Derived from Browser security violation reports and grouped into unique issues based on the endpoint and violation. SDKs do not send such events. - **Transaction events** (`transaction`): Contain operation spans and collected into traces for performance monitoring. - **Feedback events** (`feedback`): Contains user feedback messages.
"""
_EVENTTYPE_ERROR: Literal['error'] = "error"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_CSP: Literal['csp'] = "csp"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_HPKP: Literal['hpkp'] = "hpkp"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_EXPECTCT: Literal['expectct'] = "expectct"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_EXPECTSTAPLE: Literal['expectstaple'] = "expectstaple"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_TRANSACTION: Literal['transaction'] = "transaction"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_NEL: Literal['nel'] = "nel"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_DEFAULT: Literal['default'] = "default"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_GENERIC: Literal['generic'] = "generic"
"""The values for the 'The type of an event' enum"""
_EVENTTYPE_FEEDBACK: Literal['feedback'] = "feedback"
"""The values for the 'The type of an event' enum"""



_Exception = Union["_ExceptionAnyof0"]
"""
 A single exception.

 Multiple values inside of an [event](#typedef-Event) represent chained exceptions and should be sorted oldest to newest. For example, consider this Python code snippet:

 ```python
 try:
     raise Exception("random boring invariant was not met!")
 except Exception as e:
     raise ValueError("something went wrong, help!") from e
 ```

 `Exception` would be described first in the values list, followed by a description of `ValueError`:

 ```json
 {
   "exception": {
     "values": [
       {"type": "Exception": "value": "random boring invariant was not met!"},
       {"type": "ValueError", "value": "something went wrong, help!"},
     ]
   }
 }
 ```

Aggregation type: anyOf
"""



class _ExceptionAnyof0(TypedDict, total=False):
    mechanism: "_ExceptionAnyof0Mechanism"
    """
     Mechanism by which this exception was generated and handled.

    Aggregation type: anyOf
    """

    module: Union[str, None]
    """  The optional module, or package which the exception type lives in. """

    stacktrace: "_ExceptionAnyof0Stacktrace"
    """
     Stack trace containing frames of this exception.

    Aggregation type: anyOf
    """

    raw_stacktrace: "_ExceptionAnyof0RawStacktrace"
    """
     Stack trace containing frames of this exception.

    Aggregation type: anyOf
    """

    thread_id: "_ExceptionAnyof0ThreadId"
    """
     An optional value that refers to a [thread](#typedef-Thread).

    Aggregation type: anyOf
    """

    type: Union[str, None]
    """
     Exception type, e.g. `ValueError`.

     At least one of `type` or `value` is required, otherwise the exception is discarded.
    """

    value: "_ExceptionAnyof0Value"
    """
     Human readable display value.

     At least one of `type` or `value` is required, otherwise the exception is discarded.

    Aggregation type: anyOf
    """



_ExceptionAnyof0Mechanism = Union["_Mechanism", None]
"""
 Mechanism by which this exception was generated and handled.

Aggregation type: anyOf
"""



_ExceptionAnyof0RawStacktrace = Union["_RawStacktrace", None]
"""
 Stack trace containing frames of this exception.

Aggregation type: anyOf
"""



_ExceptionAnyof0Stacktrace = Union["_RawStacktrace", None]
"""
 Stack trace containing frames of this exception.

Aggregation type: anyOf
"""



_ExceptionAnyof0ThreadId = Union["_ThreadId", None]
"""
 An optional value that refers to a [thread](#typedef-Thread).

Aggregation type: anyOf
"""



_ExceptionAnyof0Value = Union["_JsonLenientString", None]
"""
 Human readable display value.

 At least one of `type` or `value` is required, otherwise the exception is discarded.

Aggregation type: anyOf
"""



_Fingerprint = Union[List[str]]
"""
 A fingerprint value.

Aggregation type: anyOf
"""



_Frame = Union["_FrameAnyof0"]
"""
 Holds information about a single stacktrace frame.

 Each object should contain **at least** a `filename`, `function` or `instruction_addr`
 attribute. All values are optional, but recommended.

Aggregation type: anyOf
"""



class _FrameAnyof0(TypedDict, total=False):
    abs_path: "_FrameAnyof0AbsPath"
    """
     Absolute path to the source file.

    Aggregation type: anyOf
    """

    addr_mode: Union[str, None]
    """
     Defines the addressing mode for addresses.

     This can be:
     - `"abs"` (the default): `instruction_addr` is absolute.
     - `"rel:$idx"`: `instruction_addr` is relative to the `debug_meta.image` identified by its index in the list.
     - `"rel:$uuid"`: `instruction_addr` is relative to the `debug_meta.image` identified by its `debug_id`.

     If one of the `"rel:XXX"` variants is given together with `function_id`, the `instruction_addr` is relative
     to the uniquely identified function in the references `debug_meta.image`.
    """

    colno: Union[int, None]
    """
     Column number within the source file, starting at 1.

    minimum: 0
    """

    context_line: Union[str, None]
    """  Source code of the current line (`lineno`). """

    filename: "_FrameAnyof0Filename"
    """
     The source file name (basename only).

    Aggregation type: anyOf
    """

    function: Union[str, None]
    """
     Name of the frame's function. This might include the name of a class.

     This function name may be shortened or demangled. If not, Sentry will demangle and shorten
     it for some platforms. The original function name will be stored in `raw_function`.
    """

    function_id: "_FrameAnyof0FunctionId"
    """
     (.NET) The function id / index that uniquely identifies a function inside a module.

     This is the `MetadataToken` of a .NET `MethodBase`.

    Aggregation type: anyOf
    """

    image_addr: "_FrameAnyof0ImageAddr"
    """
     (C/C++/Native) Start address of the containing code module (image).

    Aggregation type: anyOf
    """

    in_app: Union[bool, None]
    """
     Override whether this frame should be considered part of application code, or part of
     libraries/frameworks/dependencies.

     Setting this attribute to `false` causes the frame to be hidden/collapsed by default and
     mostly ignored during issue grouping.
    """

    instruction_addr: "_FrameAnyof0InstructionAddr"
    """
     (C/C++/Native) An optional instruction address for symbolication.

     This should be a string with a hexadecimal number that includes a 0x prefix.
     If this is set and a known image is defined in the
     [Debug Meta Interface]({%- link _documentation/development/sdk-dev/event-payloads/debugmeta.md -%}),
     then symbolication can take place.

    Aggregation type: anyOf
    """

    lineno: Union[int, None]
    """
     Line number within the source file, starting at 1.

    minimum: 0
    """

    module: Union[str, None]
    """
     Name of the module the frame is contained in.

     Note that this might also include a class name if that is something the
     language natively considers to be part of the stack (for instance in Java).
    """

    package: Union[str, None]
    """
     Name of the package that contains the frame.

     For instance this can be a dylib for native languages, the name of the jar
     or .NET assembly.
    """

    platform: Union[str, None]
    """
     Which platform this frame is from.

     This can override the platform for a single frame. Otherwise, the platform of the event is
     assumed. This can be used for multi-platform stack traces, such as in React Native.
    """

    post_context: Union[List[Union[str, None]], None]
    """
     Source code of the lines after `lineno`.

    items:
      type:
      - string
      - 'null'
    """

    pre_context: Union[List[Union[str, None]], None]
    """
     Source code leading up to `lineno`.

    items:
      type:
      - string
      - 'null'
    """

    raw_function: Union[str, None]
    """
     A raw (but potentially truncated) function value.

     The original function name, if the function name is shortened or demangled. Sentry shows the
     raw function when clicking on the shortened one in the UI.

     If this has the same value as `function` it's best to be omitted.  This exists because on
     many platforms the function itself contains additional information like overload specifies
     or a lot of generics which can make it exceed the maximum limit we provide for the field.
     In those cases then we cannot reliably trim down the function any more at a later point
     because the more valuable information has been removed.

     The logic to be applied is that an intelligently trimmed function name should be stored in
     `function` and the value before trimming is stored in this field instead.  However also this
     field will be capped at 256 characters at the moment which often means that not the entire
     original value can be stored.
    """

    stack_start: Union[bool, None]
    """
     Marks this frame as the bottom of a chained stack trace.

     Stack traces from asynchronous code consist of several sub traces that are chained together
     into one large list. This flag indicates the root function of a chained stack trace.
     Depending on the runtime and thread, this is either the `main` function or a thread base
     stub.

     This field should only be specified when true.
    """

    symbol: Union[str, None]
    """
     Potentially mangled name of the symbol as it appears in an executable.

     This is different from a function name by generally being the mangled
     name that appears natively in the binary.  This is relevant for languages
     like Swift, C++ or Rust.
    """

    symbol_addr: "_FrameAnyof0SymbolAddr"
    """
     (C/C++/Native) Start address of the frame's function.

     We use the instruction address for symbolication, but this can be used to calculate
     an instruction offset automatically.

    Aggregation type: anyOf
    """

    vars: "_FrameAnyof0Vars"
    """
     Mapping of local variables and expression names that were available in this frame.

    Aggregation type: anyOf
    """



_FrameAnyof0AbsPath = Union[str, None]
"""
 Absolute path to the source file.

Aggregation type: anyOf
"""



_FrameAnyof0Filename = Union[str, None]
"""
 The source file name (basename only).

Aggregation type: anyOf
"""



_FrameAnyof0FunctionId = Union[str, None]
"""
 (.NET) The function id / index that uniquely identifies a function inside a module.

 This is the `MetadataToken` of a .NET `MethodBase`.

Aggregation type: anyOf
"""



_FrameAnyof0ImageAddr = Union[str, None]
"""
 (C/C++/Native) Start address of the containing code module (image).

Aggregation type: anyOf
"""



_FrameAnyof0InstructionAddr = Union[str, None]
"""
 (C/C++/Native) An optional instruction address for symbolication.

 This should be a string with a hexadecimal number that includes a 0x prefix.
 If this is set and a known image is defined in the
 [Debug Meta Interface]({%- link _documentation/development/sdk-dev/event-payloads/debugmeta.md -%}),
 then symbolication can take place.

Aggregation type: anyOf
"""



_FrameAnyof0SymbolAddr = Union[str, None]
"""
 (C/C++/Native) Start address of the frame's function.

 We use the instruction address for symbolication, but this can be used to calculate
 an instruction offset automatically.

Aggregation type: anyOf
"""



_FrameAnyof0Vars = Union["_FrameVars", None]
"""
 Mapping of local variables and expression names that were available in this frame.

Aggregation type: anyOf
"""



_FrameVars = Union[Dict[str, Any]]
"""
 Frame local variables.

Aggregation type: anyOf
"""



_Geo = Union["_GeoAnyof0"]
"""
 Geographical location of the end user or device.

Aggregation type: anyOf
"""



class _GeoAnyof0(TypedDict, total=False):
    city: Union[str, None]
    """  Human readable city name. """

    country_code: Union[str, None]
    """  Two-letter country code (ISO 3166-1 alpha-2). """

    region: Union[str, None]
    """  Human readable region name or code. """

    subdivision: Union[str, None]
    """  Human readable subdivision name. """



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



class _GroupInformation(TypedDict, total=False):
    group_states: List["_GroupState"]
    is_new: bool
    is_new_group_environment: bool
    is_regression: bool
    queue: str
    skip_consume: bool


class _GroupState(TypedDict, total=False):
    id: Union[str, int]
    """ $comment: yes, we have seen both types in prod, not sure where they come from """

    is_new: bool
    is_new_group_environment: bool
    is_regression: bool


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



class _InsertEventOccurrenceData(TypedDict, total=False):
    detection_time: Required[Union[int, float]]
    """ Required property """

    fingerprint: Required[List[str]]
    """ Required property """

    issue_title: Required[str]
    """ Required property """

    subtitle: Union[str, None]
    culprit: Union[str, None]
    level: Union[str, None]
    resource_id: Union[str, None]
    id: Required[str]
    """ Required property """

    type: Required[int]
    """ Required property """



_InstructionAddrAdjustment = Union[Literal['auto'], Literal['all_but_first'], Literal['all'], Literal['none']]
"""
Controls the mechanism by which the `instruction_addr` of a [`Stacktrace`] [`Frame`] is adjusted.

The adjustment tries to transform *return addresses* to *call addresses* for symbolication. Typically, this adjustment needs to be done for all frames but the first, as the first frame is usually taken directly from the cpu context of a hardware exception or a suspended thread and the stack trace is created from that.

When the stack walking implementation truncates frames from the top, `"all"` frames should be adjusted. In case the stack walking implementation already does the adjustment when producing stack frames, `"none"` should be used here.
"""
_INSTRUCTIONADDRADJUSTMENT_AUTO: Literal['auto'] = "auto"
"""The values for the 'Controls the mechanism by which the `instruction_addr` of a [`Stacktrace`] [`Frame`] is adjusted' enum"""
_INSTRUCTIONADDRADJUSTMENT_ALL_BUT_FIRST: Literal['all_but_first'] = "all_but_first"
"""The values for the 'Controls the mechanism by which the `instruction_addr` of a [`Stacktrace`] [`Frame`] is adjusted' enum"""
_INSTRUCTIONADDRADJUSTMENT_ALL: Literal['all'] = "all"
"""The values for the 'Controls the mechanism by which the `instruction_addr` of a [`Stacktrace`] [`Frame`] is adjusted' enum"""
_INSTRUCTIONADDRADJUSTMENT_NONE: Literal['none'] = "none"
"""The values for the 'Controls the mechanism by which the `instruction_addr` of a [`Stacktrace`] [`Frame`] is adjusted' enum"""



_JsonLenientString = Union[str]
"""
 A "into-string" type of value. All non-string values are serialized as JSON.

Aggregation type: anyOf
"""



_Level = Union[Literal['debug'], Literal['info'], Literal['warning'], Literal['error'], Literal['fatal']]
""" Severity level of an event or breadcrumb. """
_LEVEL_DEBUG: Literal['debug'] = "debug"
"""The values for the 'Severity level of an event or breadcrumb' enum"""
_LEVEL_INFO: Literal['info'] = "info"
"""The values for the 'Severity level of an event or breadcrumb' enum"""
_LEVEL_WARNING: Literal['warning'] = "warning"
"""The values for the 'Severity level of an event or breadcrumb' enum"""
_LEVEL_ERROR: Literal['error'] = "error"
"""The values for the 'Severity level of an event or breadcrumb' enum"""
_LEVEL_FATAL: Literal['fatal'] = "fatal"
"""The values for the 'Severity level of an event or breadcrumb' enum"""



_LogEntry = Union["_LogEntryAnyof0"]
"""
 A log entry message.

 A log message is similar to the `message` attribute on the event itself but
 can additionally hold optional parameters.

 ```json
 {
   "message": {
     "message": "My raw message with interpreted strings like %s",
     "params": ["this"]
   }
 }
 ```

 ```json
 {
   "message": {
     "message": "My raw message with interpreted strings like {foo}",
     "params": {"foo": "this"}
   }
 }
 ```

Aggregation type: anyOf
"""



class _LogEntryAnyof0(TypedDict, total=False):
    formatted: "_LogEntryAnyof0Formatted"
    """
     The formatted message. If `message` and `params` are given, Sentry
     will attempt to backfill `formatted` if empty.

     It must not exceed 8192 characters. Longer messages will be truncated.

    Aggregation type: anyOf
    """

    message: "_LogEntryAnyof0Message"
    """
     The log message with parameter placeholders.

     This attribute is primarily used for grouping related events together into issues.
     Therefore this really should just be a string template, i.e. `Sending %d requests` instead
     of `Sending 9999 requests`. The latter is much better at home in `formatted`.

     It must not exceed 8192 characters. Longer messages will be truncated.

    Aggregation type: anyOf
    """

    params: Union[Dict[str, Any], List[Any], None]
    """
     Parameters to be interpolated into the log message. This can be an array of positional
     parameters as well as a mapping of named arguments to their values.
    """



_LogEntryAnyof0Formatted = Union["_Message", None]
"""
 The formatted message. If `message` and `params` are given, Sentry
 will attempt to backfill `formatted` if empty.

 It must not exceed 8192 characters. Longer messages will be truncated.

Aggregation type: anyOf
"""



_LogEntryAnyof0Message = Union["_Message", None]
"""
 The log message with parameter placeholders.

 This attribute is primarily used for grouping related events together into issues.
 Therefore this really should just be a string template, i.e. `Sending %d requests` instead
 of `Sending 9999 requests`. The latter is much better at home in `formatted`.

 It must not exceed 8192 characters. Longer messages will be truncated.

Aggregation type: anyOf
"""



_Mechanism = Union["_MechanismAnyof0"]
"""
 The mechanism by which an exception was generated and handled.

 The exception mechanism is an optional field residing in the [exception](#typedef-Exception).
 It carries additional information about the way the exception was created on the target system.
 This includes general exception values obtained from the operating system or runtime APIs, as
 well as mechanism-specific values.

Aggregation type: anyOf
"""



class _MechanismAnyof0(TypedDict, total=False):
    handled: Union[bool, None]
    """
     Flag indicating whether this exception was handled.

     This is a best-effort guess at whether the exception was handled by user code or not. For
     example:

     - Exceptions leading to a 500 Internal Server Error or to a hard process crash are
       `handled=false`, as the SDK typically has an integration that automatically captures the
       error.

     - Exceptions captured using `capture_exception` (called from user code) are `handled=true`
       as the user explicitly captured the exception (and therefore kind of handled it)
    """

    type: Required[Union[str, None]]
    """
     Mechanism type (required).

     Required unique identifier of this mechanism determining rendering and processing of the
     mechanism data.

     In the Python SDK this is merely the name of the framework integration that produced the
     exception, while for native it is e.g. `"minidump"` or `"applecrashreport"`.

    Required property
    """



_Message = Union[str]
""" Aggregation type: anyOf """



_MonitorContext = Union[Dict[str, Any]]
"""
 Monitor information.

Aggregation type: anyOf
"""



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



class _RawStacktrace(TypedDict, total=False):
    """
     A stack trace of a single thread.

     A stack trace contains a list of frames, each with various bits (most optional) describing the
     context of that frame. Frames should be sorted from oldest to newest.

     For the given example program written in Python:

     ```python
     def foo():
         my_var = 'foo'
         raise ValueError()

     def main():
         foo()
     ```

     A minimalistic stack trace for the above program in the correct order:

     ```json
     {
       "frames": [
         {"function": "main"},
         {"function": "foo"}
       ]
     }
     ```

     The top frame fully symbolicated with five lines of source context:

     ```json
     {
       "frames": [{
         "in_app": true,
         "function": "myfunction",
         "abs_path": "/real/file/name.py",
         "filename": "file/name.py",
         "lineno": 3,
         "vars": {
           "my_var": "'value'"
         },
         "pre_context": [
           "def foo():",
           "  my_var = 'foo'",
         ],
         "context_line": "  raise ValueError()",
         "post_context": [
           "",
           "def main():"
         ],
       }]
     }
     ```

     A minimal native stack trace with register values. Note that the `package` event attribute must
     be "native" for these frames to be symbolicated.

     ```json
     {
       "frames": [
         {"instruction_addr": "0x7fff5bf3456c"},
         {"instruction_addr": "0x7fff5bf346c0"},
       ],
       "registers": {
         "rip": "0x00007ff6eef54be2",
         "rsp": "0x0000003b710cd9e0"
       }
     }
     ```
    """

    frames: Required[Union[List["_RawStacktraceFramesArrayItem"], None]]
    """
     Required. A non-empty list of stack frames. The list is ordered from caller to callee, or
     oldest to youngest. The last frame is the one creating the exception.

    items:
      anyOf:
      - $ref: '#/definitions/Frame'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null

    Required property
    """

    instruction_addr_adjustment: "_RawStacktraceInstructionAddrAdjustment"
    """
     Optional. A flag that indicates if, and how, `instruction_addr` values need to be adjusted
     before they are symbolicated.

    Aggregation type: anyOf
    """

    lang: Union[str, None]
    """  The language of the stacktrace. """

    registers: Union[Dict[str, "_RawStacktraceRegistersObjectAdditionalproperties"], None]
    """
     Register values of the thread (top frame).

     A map of register names and their values. The values should contain the actual register
     values of the thread, thus mapping to the last frame in the list.

    additionalProperties:
      anyOf:
      - $ref: '#/definitions/RegVal'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """

    snapshot: Union[bool, None]
    """
     Indicates that this stack trace is a snapshot triggered by an external signal.

     If this field is `false`, then the stack trace points to the code that caused this stack
     trace to be created. This can be the location of a raised exception, as well as an exception
     or signal handler.

     If this field is `true`, then the stack trace was captured as part of creating an unrelated
     event. For example, a thread other than the crashing thread, or a stack trace computed as a
     result of an external kill signal.
    """



_RawStacktraceFramesArrayItem = Union["_Frame", None]
""" Aggregation type: anyOf """



_RawStacktraceInstructionAddrAdjustment = Union["_InstructionAddrAdjustment", None]
"""
 Optional. A flag that indicates if, and how, `instruction_addr` values need to be adjusted
 before they are symbolicated.

Aggregation type: anyOf
"""



_RawStacktraceRegistersObjectAdditionalproperties = Union[str, None]
""" Aggregation type: anyOf """



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



_SENTRY_EVENT_ERRORS_DEFAULT = None
""" Default value of the field path 'sentry_event errors' """



_SentryEventContexts = Union["_Contexts", None]
"""
 Contexts describing the environment (e.g. device, os or browser).

Aggregation type: anyOf
"""



_SentryEventErrorsArrayItem = Union["_EventProcessingError", None]
""" Aggregation type: anyOf """



_SentryEventEventId = Union["_EventId", None]
"""
 Unique identifier of this event.

 Hexadecimal string representing a uuid4 value. The length is exactly 32 characters. Dashes
 are not allowed. Has to be lowercase.

 Even though this field is backfilled on the server with a new uuid4, it is strongly
 recommended to generate that uuid4 clientside. There are some features like user feedback
 which are easier to implement that way, and debugging in case events get lost in your
 Sentry installation is also easier.

 Example:

 ```json
 {
   "event_id": "fc6d8c0c43fc4630ad850ee518f1b9d0"
 }
 ```

Aggregation type: anyOf
"""



_SentryEventException = Union["SentryExceptionChain", None]
""" Aggregation type: anyOf """



_SentryEventFingerprint = Union["_Fingerprint", None]
"""
 Manual fingerprint override.

 A list of strings used to dictate how this event is supposed to be grouped with other
 events into issues. For more information about overriding grouping see [Customize Grouping
 with Fingerprints](https://docs.sentry.io/data-management/event-grouping/).

 ```json
 {
     "fingerprint": ["myrpc", "POST", "/foo.bar"]
 }

Aggregation type: anyOf
"""



_SentryEventLevel = Union["_Level", None]
"""
 Severity level of the event. Defaults to `error`.

 Example:

 ```json
 {"level": "warning"}
 ```

Aggregation type: anyOf
"""



_SentryEventLogentry = Union["_LogEntry", None]
"""
 Custom parameterized message for this event.

Aggregation type: anyOf
"""



_SentryEventRequest = Union["SentryRequest", None]
"""
 Information about a web request that occurred during the event.

Aggregation type: anyOf
"""



_SentryEventSdk = Union["ClientSdkInfo", None]
"""
 Information about the Sentry SDK that generated this event.

Aggregation type: anyOf
"""



_SentryEventStacktrace = Union["_RawStacktrace", None]
"""
 Event stacktrace.

 DEPRECATED: Prefer `threads` or `exception` depending on which is more appropriate.

Aggregation type: anyOf
"""



_SentryEventTags = Union["_Tags", None]
"""
 Custom tags for this event.

 A map or list of tags for this event. Each tag must be less than 200 characters.

Aggregation type: anyOf
"""



_SentryEventThreads = Union["SentryThreadChain", None]
""" Aggregation type: anyOf """



_SentryEventTimestamp = Union["_Timestamp", None]
"""
 Timestamp when the event was created.

 Indicates when the event was created in the Sentry SDK. The format is either a string as
 defined in [RFC 3339](https://tools.ietf.org/html/rfc3339) or a numeric (integer or float)
 value representing the number of seconds that have elapsed since the [Unix
 epoch](https://en.wikipedia.org/wiki/Unix_time).

 Timezone is assumed to be UTC if missing.

 Sub-microsecond precision is not preserved with numeric values due to precision
 limitations with floats (at least in our systems). With that caveat in mind, just send
 whatever is easiest to produce.

 All timestamps in the event protocol are formatted this way.

 # Example

 All of these are the same date:

 ```json
 { "timestamp": "2011-05-02T17:41:36Z" }
 { "timestamp": "2011-05-02T17:41:36" }
 { "timestamp": "2011-05-02T17:41:36.000" }
 { "timestamp": 1304358096.0 }
 ```

Aggregation type: anyOf
"""



_SentryEventTransactionInfo = Union["_TransactionInfo", None]
"""
 Additional information about the name of the transaction.

Aggregation type: anyOf
"""



_SentryEventType = Union["_EventType", None]
"""
 Type of the event. Defaults to `default`.

 The event type determines how Sentry handles the event and has an impact on processing, rate
 limiting, and quotas. There are three fundamental classes of event types:

  - **Error monitoring events**: Processed and grouped into unique issues based on their
    exception stack traces and error messages.
  - **Security events**: Derived from Browser security violation reports and grouped into
    unique issues based on the endpoint and violation. SDKs do not send such events.
  - **Transaction events** (`transaction`): Contain operation spans and collected into traces
    for performance monitoring.

 Transactions must explicitly specify the `"transaction"` event type. In all other cases,
 Sentry infers the appropriate event type from the payload and overrides the stated type.
 SDKs should not send an event type other than for transactions.

 Example:

 ```json
 {
   "type": "transaction",
   "spans": []
 }
 ```

Aggregation type: anyOf
"""



_SentryEventUser = Union["SentryUser", None]
"""
 Information about the user who triggered this event.

Aggregation type: anyOf
"""



_SentryExceptionChainValuesArrayItem = Union["_Exception", None]
""" Aggregation type: anyOf """



class _SentryRequestAnyof0(TypedDict, total=False):
    headers: "_SentryRequestAnyof0Headers"
    """
     A dictionary of submitted headers.

     If a header appears multiple times it, needs to be merged according to the HTTP standard
     for header merging. Header names are treated case-insensitively by Sentry.

    Aggregation type: anyOf
    """

    method: Union[str, None]
    """  HTTP request method. """

    url: Union[str, None]
    """
     The URL of the request if available.

    The query string can be declared either as part of the `url`, or separately in `query_string`.
    """



_SentryRequestAnyof0Headers = Union["_Headers", None]
"""
 A dictionary of submitted headers.

 If a header appears multiple times it, needs to be merged according to the HTTP standard
 for header merging. Header names are treated case-insensitively by Sentry.

Aggregation type: anyOf
"""



_SentryThreadChainValuesArrayItem = Union["_Thread", None]
""" Aggregation type: anyOf """



class _SentryUserAnyof0(TypedDict, total=False):
    data: Union[Dict[str, Any], None]
    """
     Additional arbitrary fields, as stored in the database (and sometimes as sent by clients).
     All data from `self.other` should end up here after store normalization.

    additionalProperties: True
    """

    email: Union[str, None]
    """  Email address of the user. """

    geo: "_SentryUserAnyof0Geo"
    """
     Approximate geographical location of the end user or device.

    Aggregation type: anyOf
    """

    id: Union[str, None]
    """  Unique identifier of the user. """

    ip_address: "_SentryUserAnyof0IpAddress"
    """
     Remote IP address of the user. Defaults to "{{auto}}".

    Aggregation type: anyOf
    """

    name: Union[str, None]
    """  Human readable name of the user. """

    segment: Union[str, None]
    """  The user segment, for apps that divide users in user segments. """

    username: Union[str, None]
    """  Username of the user. """



_SentryUserAnyof0Geo = Union["_Geo", None]
"""
 Approximate geographical location of the end user or device.

Aggregation type: anyOf
"""



_SentryUserAnyof0IpAddress = Union[str, None]
"""
 Remote IP address of the user. Defaults to "{{auto}}".

Aggregation type: anyOf
"""



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



_Thread = Union["_ThreadAnyof0"]
"""
 A single thread.

 The Threads Interface specifies threads that were running at the time an event happened.
 These threads can also contain stack traces.

Aggregation type: anyOf
"""



class _ThreadAnyof0(TypedDict, total=False):
    id: "_ThreadAnyof0Id"
    """
     An optional value that refers to a [thread](#typedef-Thread).

    Aggregation type: anyOf
    """

    main: Union[bool, None]
    """
     If applicable, a flag indicating whether the thread was responsible for rendering the user interface.

     On mobile platforms this is oftentimes referred to as the `main thread` or `ui thread`.
    """



_ThreadAnyof0Id = Union["_ThreadId", None]
"""
 An optional value that refers to a [thread](#typedef-Thread).

Aggregation type: anyOf
"""



_ThreadId = Union["_ThreadIdAnyof0", str]
"""
 Represents a thread id.

Aggregation type: anyOf
"""



_ThreadIdAnyof0 = int
""" minimum: 0 """



_Timestamp = Union[Union[int, float]]
"""
Can be a ISO-8601 formatted string or a unix timestamp in seconds (floating point values allowed).

Must be UTC.

Aggregation type: anyOf
"""



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

    sampled: Union[bool, None]
    """  Whether the trace connected to the event has been sampled as part of dynamic sampling """



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

