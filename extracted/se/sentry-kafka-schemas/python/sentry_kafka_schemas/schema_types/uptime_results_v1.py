from typing import Required, Union, Any, TypedDict, Literal, List


class Assertion(TypedDict, total=False):
    """
    assertion.

    The root of the uptime assertion
    """

    root: "AssertionOp"
    """
    assertion_op.

    All possible assertion operations

    Aggregation type: anyOf
    """



AssertionOp = Union["AssertionOpAnd", "AssertionOpOr", "AssertionOpNot", "AssertionOpStatusCodeCheck", "AssertionOpJsonpath", "AssertionOpHeaderCheck"]
"""
assertion_op.

All possible assertion operations

Aggregation type: anyOf
"""



class AssertionOpAnd(TypedDict, total=False):
    """
    assertion_op_and.

    The boolean AND operation
    """

    op: Literal['and']
    children: List["AssertionOp"]


AssertionOpComparison = Union[Literal['always'], Literal['never'], Literal['less_than'], Literal['greater_than'], Literal['equals'], Literal['not_equals']]
"""
assertion_op_comparison.

The kind of comparison to make.
"""
ASSERTIONOPCOMPARISON_ALWAYS: Literal['always'] = "always"
"""The values for the 'assertion_op_comparison' enum"""
ASSERTIONOPCOMPARISON_NEVER: Literal['never'] = "never"
"""The values for the 'assertion_op_comparison' enum"""
ASSERTIONOPCOMPARISON_LESS_THAN: Literal['less_than'] = "less_than"
"""The values for the 'assertion_op_comparison' enum"""
ASSERTIONOPCOMPARISON_GREATER_THAN: Literal['greater_than'] = "greater_than"
"""The values for the 'assertion_op_comparison' enum"""
ASSERTIONOPCOMPARISON_EQUALS: Literal['equals'] = "equals"
"""The values for the 'assertion_op_comparison' enum"""
ASSERTIONOPCOMPARISON_NOT_EQUALS: Literal['not_equals'] = "not_equals"
"""The values for the 'assertion_op_comparison' enum"""



class AssertionOpHeaderCheck(TypedDict, total=False):
    """
    assertion_op_header_check.

    The HTTP header (key and value) comparison operation
    """

    key_op: "AssertionOpComparison"
    """
    assertion_op_comparison.

    The kind of comparison to make.
    """

    key_operand: "AssertionOpHeaderOperand"
    """
    assertion_op_header_operand.

    A operand for comparison against HTTP header keys and values

    Aggregation type: anyOf
    """

    value_op: "AssertionOpComparison"
    """
    assertion_op_comparison.

    The kind of comparison to make.
    """

    value_operand: "AssertionOpHeaderOperand"
    """
    assertion_op_header_operand.

    A operand for comparison against HTTP header keys and values

    Aggregation type: anyOf
    """



AssertionOpHeaderOperand = Union["AssertionOpHeaderOperandGlob", "AssertionOpHeaderOperandLiteral", "AssertionOpHeaderOperandNone"]
"""
assertion_op_header_operand.

A operand for comparison against HTTP header keys and values

Aggregation type: anyOf
"""



class AssertionOpHeaderOperandGlob(TypedDict, total=False):
    """
    assertion_op_header_operand_glob.

    A glob pattern for matching
    """

    header_op: Literal['glob']
    pattern: "AssertionOpHeaderOperandGlobPattern"
    """
    assertion_op_header_operand_glob_pattern.

    The actual glob pattern, as a string
    """



class AssertionOpHeaderOperandGlobPattern(TypedDict, total=False):
    """
    assertion_op_header_operand_glob_pattern.

    The actual glob pattern, as a string
    """

    value: str


class AssertionOpHeaderOperandLiteral(TypedDict, total=False):
    """
    assertion_op_header_operand_literal.

    A literal value for comparison
    """

    header_op: Literal['literal']
    value: str


class AssertionOpHeaderOperandNone(TypedDict, total=False):
    """
    assertion_op_header_operand_none.

    A none operand for the comparison
    """

    header_op: Literal['none']


class AssertionOpJsonpath(TypedDict, total=False):
    """
    assertion_op_jsonpath.

    The JSONPath query operation
    """

    op: Literal['json_path']
    value: str


class AssertionOpNot(TypedDict, total=False):
    """
    assertion_op_not.

    The negation operation
    """

    op: Literal['not']
    operand: "AssertionOp"
    """
    assertion_op.

    All possible assertion operations

    Aggregation type: anyOf
    """



class AssertionOpOr(TypedDict, total=False):
    """
    assertion_op_or.

    The boolean OR operation
    """

    op: Literal['or']
    children: List["AssertionOp"]


class AssertionOpStatusCodeCheck(TypedDict, total=False):
    """
    assertion_op_status_code_check.

    The HTTP status code comparison operation
    """

    value: int
    operator: "AssertionOpComparison"
    """
    assertion_op_comparison.

    The kind of comparison to make.
    """



class CheckResult(TypedDict, total=False):
    """
    check_result.

    A message containing the result of the uptime check.
    """

    guid: Required[str]
    """
    Unique identifier of the uptime check

    Required property
    """

    subscription_id: Required[str]
    """
    Identifier of the subscription that this check was run for

    Required property
    """

    status: Required["CheckStatus"]
    """
    check_status.

    The status of the check

    Required property
    """

    status_reason: Required[Union["CheckStatusReason", None]]
    """
    Aggregation type: oneOf

    Required property
    """

    trace_id: Required[str]
    """
    Trace ID associated with the check-in made

    Required property
    """

    span_id: Required[str]
    """
    Span ID associated with the check-in made. This is a phantom span generated by the uptime-checker, no real span is ingested.

    Required property
    """

    scheduled_check_time_ms: Required[Union[int, float]]
    """
    Timestamp in milliseconds of when the check was schedule to run

    Required property
    """

    actual_check_time_ms: Required[Union[int, float]]
    """
    Timestamp in milliseconds of when the check was actually ran

    Required property
    """

    duration_ms: Required[Union[Union[int, float], None]]
    """
    Duration of the check in ms. Will be null when the status is missed_window

    Required property
    """

    request_info: Required[Union["RequestInfo", None]]
    """
    Aggregation type: oneOf

    Required property
    """

    request_info_list: List["RequestInfo"]
    """ List of all request attempts, in order of execution """

    region: str
    """ The region that this check was performed in """

    assertion_failure_data: Union["Assertion", None]
    """ Aggregation type: oneOf """



CheckStatus = Union[Literal['success'], Literal['failure'], Literal['missed_window'], Literal['disallowed_by_robots']]
"""
check_status.

The status of the check
"""
CHECKSTATUS_SUCCESS: Literal['success'] = "success"
"""The values for the 'check_status' enum"""
CHECKSTATUS_FAILURE: Literal['failure'] = "failure"
"""The values for the 'check_status' enum"""
CHECKSTATUS_MISSED_WINDOW: Literal['missed_window'] = "missed_window"
"""The values for the 'check_status' enum"""
CHECKSTATUS_DISALLOWED_BY_ROBOTS: Literal['disallowed_by_robots'] = "disallowed_by_robots"
"""The values for the 'check_status' enum"""



class CheckStatusReason(TypedDict, total=False):
    """
    check_status_reason.

    Reason for the status, primarily used for failure
    """

    type: Required["CheckStatusReasonType"]
    """
    check_status_reason_type.

    The type of the status reason

    Required property
    """

    description: Required[str]
    """
    A human readable description of the status reason

    Required property
    """



CheckStatusReasonType = Union[Literal['timeout'], Literal['dns_error'], Literal['failure'], Literal['tls_error'], Literal['connection_error'], Literal['redirect_error'], Literal['miss_produced'], Literal['miss_backfill'], Literal['assertion_compilation_error'], Literal['assertion_evaluation_error']]
"""
check_status_reason_type.

The type of the status reason
"""
CHECKSTATUSREASONTYPE_TIMEOUT: Literal['timeout'] = "timeout"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_DNS_ERROR: Literal['dns_error'] = "dns_error"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_FAILURE: Literal['failure'] = "failure"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_TLS_ERROR: Literal['tls_error'] = "tls_error"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_CONNECTION_ERROR: Literal['connection_error'] = "connection_error"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_REDIRECT_ERROR: Literal['redirect_error'] = "redirect_error"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_MISS_PRODUCED: Literal['miss_produced'] = "miss_produced"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_MISS_BACKFILL: Literal['miss_backfill'] = "miss_backfill"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_ASSERTION_COMPILATION_ERROR: Literal['assertion_compilation_error'] = "assertion_compilation_error"
"""The values for the 'check_status_reason_type' enum"""
CHECKSTATUSREASONTYPE_ASSERTION_EVALUATION_ERROR: Literal['assertion_evaluation_error'] = "assertion_evaluation_error"
"""The values for the 'check_status_reason_type' enum"""



class RequestDurations(TypedDict, total=False):
    """
    request_durations.

    Durations of each operation in the request
    """

    dns_lookup: "Timing"
    """ timing. """

    tcp_connection: "Timing"
    """ timing. """

    tls_handshake: "Timing"
    """ timing. """

    time_to_first_byte: "Timing"
    """ timing. """

    send_request: "Timing"
    """ timing. """

    receive_response: "Timing"
    """ timing. """



class RequestInfo(TypedDict, total=False):
    """
    request_info.

    Additional information about each request made
    """

    request_type: Required["RequestType"]
    """
    request_type.

    The type of HTTP method used for the check

    Required property
    """

    http_status_code: Required[Union[Union[int, float], None]]
    """
    Status code of the request

    Required property
    """

    url: str
    """ The full URL being requested """

    request_body_size_bytes: Union[int, float]
    """ Size of the request body in bytes (per OTEL). """

    response_body_size_bytes: Union[int, float]
    """ Size of the response body in bytes (per OTEL). """

    request_duration_us: Union[int, float]
    """ Total measured duration for this specific request in microseconds. This is the actual wall clock time and may differ from summing individual timing components. """

    durations: "RequestDurations"
    """
    request_durations.

    Durations of each operation in the request
    """

    response_body: Union[str, None]
    """ Response body content, captured on failure when configured. Base64 encoded. """

    response_headers: Union[List["ResponseHeader"], None]
    """
    Response headers, captured on failure when configured.

    items:
      $ref: '#/definitions/ResponseHeader'
      used: !!set
        $ref: null
    """



RequestType = Union[Literal['GET'], Literal['POST'], Literal['HEAD'], Literal['PUT'], Literal['DELETE'], Literal['PATCH'], Literal['OPTIONS']]
"""
request_type.

The type of HTTP method used for the check
"""
REQUESTTYPE_GET: Literal['GET'] = "GET"
"""The values for the 'request_type' enum"""
REQUESTTYPE_POST: Literal['POST'] = "POST"
"""The values for the 'request_type' enum"""
REQUESTTYPE_HEAD: Literal['HEAD'] = "HEAD"
"""The values for the 'request_type' enum"""
REQUESTTYPE_PUT: Literal['PUT'] = "PUT"
"""The values for the 'request_type' enum"""
REQUESTTYPE_DELETE: Literal['DELETE'] = "DELETE"
"""The values for the 'request_type' enum"""
REQUESTTYPE_PATCH: Literal['PATCH'] = "PATCH"
"""The values for the 'request_type' enum"""
REQUESTTYPE_OPTIONS: Literal['OPTIONS'] = "OPTIONS"
"""The values for the 'request_type' enum"""



ResponseHeader = List[Any]
"""
response_header.

A response header, consisting of a name and value as a tuple.

prefixItems:
  - title: header_name
    type: string
  - title: header_value
    type: string
"""



class Timing(TypedDict, total=False):
    """ timing. """

    start_us: Required[Union[int, float]]
    """
    Start of the timing, timestamp in microseconds.

    Required property
    """

    duration_us: Required[Union[int, float]]
    """
    Duration of the timing, in microseconds

    Required property
    """

