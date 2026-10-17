"""Pure stateless helpers for JSON-RPC 2.0 protocol and CLI argv construction.

This module has NO I/O and NO state — all functions are pure and trivially testable.
"""

from __future__ import annotations

import base64
import json
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .errors import (
    HOST_HANDSHAKE_FAILED,
    HOST_PROTOCOL_ERROR,
    JSON_RPC_TIMEOUT_CODE,
    SuperDocError,
)
from .sdk_policy import SDK_POLICY

ChangeMode = Literal['direct', 'tracked']

HOST_PROTOCOL_VERSION = SDK_POLICY['protocolVersion']
REQUIRED_FEATURES = tuple(SDK_POLICY['cliRequiredFeatures'])
COLLABORATION_AUTH_PER_OPEN_FEATURE = SDK_POLICY['features']['collaborationAuthPerOpen']
WATCHDOG_HEADROOM_MS = SDK_POLICY['watchdogHeadroomMs']


# ---------------------------------------------------------------------------
# JSON-RPC message types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class JsonRpcResponse:
    id: int
    result: Any


@dataclass(frozen=True)
class JsonRpcError:
    id: int
    error: Dict[str, Any]


@dataclass(frozen=True)
class JsonRpcNotification:
    method: str
    params: Any


@dataclass(frozen=True)
class InvalidFrame:
    raw: str


ParsedMessage = Union[JsonRpcResponse, JsonRpcError, JsonRpcNotification, InvalidFrame]


# ---------------------------------------------------------------------------
# JSON-RPC encoding / decoding
# ---------------------------------------------------------------------------

def encode_jsonrpc_request(
    request_id: int,
    method: str,
    params: Any = None,
    *,
    request_timeout_ms: Optional[int] = None,
) -> str:
    """Serialize a JSON-RPC 2.0 request as a newline-terminated string."""
    payload = {'jsonrpc': '2.0', 'id': request_id, 'method': method}
    if params is not None:
        payload['params'] = params
    if request_timeout_ms is not None:
        payload['requestTimeoutMs'] = request_timeout_ms
    return json.dumps(payload, separators=(',', ':')) + '\n'


def parse_jsonrpc_line(line: str) -> ParsedMessage:
    """Parse a single line of JSON-RPC stdout into a typed message."""
    stripped = line.strip()
    if not stripped:
        return InvalidFrame(raw=line)

    try:
        parsed = json.loads(stripped)
    except (json.JSONDecodeError, ValueError):
        return InvalidFrame(raw=line)

    if not isinstance(parsed, dict) or parsed.get('jsonrpc') != '2.0':
        return InvalidFrame(raw=line)

    # Notification: has method but no id.
    if 'method' in parsed and 'id' not in parsed:
        return JsonRpcNotification(method=parsed['method'], params=parsed.get('params'))

    raw_id = parsed.get('id')
    if not isinstance(raw_id, int):
        return InvalidFrame(raw=line)

    if 'error' in parsed:
        return JsonRpcError(id=raw_id, error=parsed['error'])

    return JsonRpcResponse(id=raw_id, result=parsed.get('result'))


# ---------------------------------------------------------------------------
# Error mapping
# ---------------------------------------------------------------------------

def map_jsonrpc_error(raw_error: Dict[str, Any]) -> SuperDocError:
    """Normalize a JSON-RPC error object into a SuperDocError.

    Mirrors the Node SDK's mapJsonRpcError precedence: CLI codes first,
    document-host domain codes second, then transport timeout and generic
    command failures.
    """
    if not isinstance(raw_error, dict):
        return SuperDocError(
            'Host returned an unknown JSON-RPC error.',
            code=HOST_PROTOCOL_ERROR,
            details={'error': raw_error},
        )

    data = raw_error.get('data')
    if isinstance(data, dict):
        cli_code = data.get('cliCode')
        domain_code = data.get('domainCode')
        cli_message = data.get('message')
        exit_code = data.get('exitCode')

        if isinstance(cli_code, str):
            return SuperDocError(
                cli_message if isinstance(cli_message, str) else raw_error.get('message', 'Command failed.'),
                code=cli_code,
                details=data.get('details'),
                exit_code=exit_code if isinstance(exit_code, int) else None,
            )

        if isinstance(domain_code, str):
            details: Dict[str, Any] = {}
            if 'details' in data:
                details['domainDetails'] = data['details']
            if 'stage' in data:
                details['stage'] = data['stage']
            if 'byteLength' in data:
                details['byteLength'] = data['byteLength']
            return SuperDocError(
                raw_error.get('message', 'Document operation failed.'),
                code=domain_code,
                details=details,
            )

    error_code = raw_error.get('code')
    message = raw_error.get('message', 'Unknown JSON-RPC error.')

    if error_code == JSON_RPC_TIMEOUT_CODE:
        return SuperDocError(message, code='TIMEOUT', details=data)

    return SuperDocError(message, code='COMMAND_FAILED', details=data)


# ---------------------------------------------------------------------------
# Capability handshake validation
# ---------------------------------------------------------------------------

def validate_capabilities(
    response: Any,
    required_features: Tuple[str, ...] = REQUIRED_FEATURES,
) -> None:
    """Validate a host.capabilities response. Raises SuperDocError on failure."""
    if not isinstance(response, dict):
        raise SuperDocError(
            'Host capabilities response is invalid.',
            code=HOST_HANDSHAKE_FAILED,
            details={'response': response},
        )

    protocol_version = response.get('protocolVersion')
    if protocol_version != HOST_PROTOCOL_VERSION:
        raise SuperDocError(
            'Host protocol version is unsupported.',
            code=HOST_HANDSHAKE_FAILED,
            details={'expected': HOST_PROTOCOL_VERSION, 'actual': protocol_version},
        )

    features = response.get('features')
    if not isinstance(features, list) or not all(isinstance(f, str) for f in features):
        raise SuperDocError(
            'Host capabilities.features must be a string array.',
            code=HOST_HANDSHAKE_FAILED,
            details={'features': features},
        )

    for required in required_features:
        if required not in features:
            raise SuperDocError(
                f'Host does not support required feature: {required}',
                code=HOST_HANDSHAKE_FAILED,
                details={'features': features},
            )


# ---------------------------------------------------------------------------
# CLI argv construction
# ---------------------------------------------------------------------------

def _encode_param(args: List[str], spec: Dict[str, Any], value: Any) -> None:
    """Encode a single operation parameter into CLI argv flags."""
    if value is None:
        if spec.get('required'):
            raise SuperDocError(f"Missing required parameter: {spec['name']}", code='INVALID_ARGUMENT')
        return

    kind = spec['kind']
    param_type = spec['type']

    if kind == 'doc':
        args.append(str(value))
        return

    flag = f"--{spec.get('flag') or spec['name']}"

    if param_type == 'boolean':
        args.extend([flag, 'true' if value else 'false'])
        return

    if param_type == 'string[]':
        if not isinstance(value, list):
            raise SuperDocError(f"Parameter {spec['name']} must be a list.", code='INVALID_ARGUMENT')
        for item in value:
            args.extend([flag, str(item)])
        return

    if param_type == 'json':
        args.extend([flag, json.dumps(value)])
        return

    args.extend([flag, str(value)])


def normalize_default_change_mode(default_change_mode: Optional[str]) -> Optional[ChangeMode]:
    """Validate and normalize the default_change_mode option."""
    if default_change_mode is None:
        return None
    if default_change_mode in ('direct', 'tracked'):
        return default_change_mode  # type: ignore[return-value]
    raise SuperDocError(
        'default_change_mode must be "direct" or "tracked".',
        code='INVALID_ARGUMENT',
        details={'defaultChangeMode': default_change_mode},
    )


def apply_default_change_mode(
    operation: Dict[str, Any], payload: Dict[str, Any], default_change_mode: Optional[ChangeMode]
) -> Dict[str, Any]:
    """Inject default change mode into params if applicable."""
    if default_change_mode is None:
        return payload
    if payload.get('changeMode') is not None:
        return payload
    supports = any(spec.get('name') == 'changeMode' for spec in operation.get('params', []))
    if not supports:
        return payload
    return {**payload, 'changeMode': default_change_mode}


def apply_default_user(
    operation: Dict[str, Any], payload: Dict[str, Any], user: Optional[Dict[str, str]]
) -> Dict[str, Any]:
    """Inject default user identity into params for doc.open when not already specified."""
    if user is None:
        return payload
    if operation.get('operationId') != 'doc.open':
        return payload
    result = dict(payload)
    if result.get('userName') is None and user.get('name'):
        result['userName'] = user['name']
    if result.get('userEmail') is None and user.get('email'):
        result['userEmail'] = user['email']
    return result


def apply_operation_param_aliases(
    operation: Dict[str, Any], params: Dict[str, Any]
) -> Dict[str, Any]:
    """Normalize compatibility parameter names to their generated contract names."""
    payload = dict(params)
    operation_id = operation.get('operationId', '')
    aliases = SDK_POLICY['operationParamAliases'].get(operation_id, {})
    for canonical, names in aliases.items():
        for alias in names:
            if alias not in payload:
                continue
            if canonical in payload and payload[canonical] != payload[alias]:
                label = operation_id.removeprefix('doc.')
                raise SuperDocError(
                    f'{label}: cannot provide both {canonical} and {alias} with different values.',
                    code='INVALID_ARGUMENT',
                )
            payload[canonical] = payload.pop(alias)
    return payload


def build_operation_argv(
    operation: Dict[str, Any],
    params: Dict[str, Any],
    timeout_ms: Optional[int] = None,
    default_change_mode: Optional[ChangeMode] = None,
    user: Optional[Dict[str, str]] = None,
) -> List[str]:
    """Build the CLI argument vector for an operation invocation."""
    payload = apply_default_change_mode(operation, params, default_change_mode)
    payload = apply_default_user(operation, payload, user)
    payload = apply_operation_param_aliases(operation, payload)
    argv: List[str] = list(operation['commandTokens'])
    for spec in operation['params']:
        _encode_param(argv, spec, payload.get(spec['name']))
    if timeout_ms is not None:
        argv.extend(['--timeout-ms', str(timeout_ms)])
    argv.extend(['--output', 'json'])
    return argv


def normalize_collaboration_auth(value: Any) -> Dict[str, str]:
    """Validate request-scoped collaboration authentication without exposing its token."""
    if not isinstance(value, dict):
        raise SuperDocError('collaboration_auth must be a dictionary.', code='INVALID_ARGUMENT')
    unknown_fields = set(value) - {'type', 'token'}
    if unknown_fields:
        field = sorted(unknown_fields)[0]
        raise SuperDocError(f'collaboration_auth.{field} is not supported.', code='INVALID_ARGUMENT')
    if value.get('type') != 'token':
        raise SuperDocError('collaboration_auth.type must be "token".', code='INVALID_ARGUMENT')
    token = value.get('token')
    if not isinstance(token, str) or len(token) == 0:
        raise SuperDocError('collaboration_auth.token must be a non-empty string.', code='INVALID_ARGUMENT')
    return {'type': 'token', 'token': token}


def build_cli_invoke_payload(
    argv: List[str],
    stdin_bytes: Optional[bytes] = None,
    collaboration_auth: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Build the params dict for a cli.invoke JSON-RPC request."""
    payload: Dict[str, Any] = {'argv': argv}
    payload['stdinBase64'] = base64.b64encode(stdin_bytes).decode('ascii') if stdin_bytes else ''
    if collaboration_auth is not None:
        payload['collaborationAuth'] = normalize_collaboration_auth(collaboration_auth)
    return payload


def build_structured_read_input(
    operation: Dict[str, Any], params: Dict[str, Any],
    stdin_bytes: Optional[bytes] = None,
    collaboration_auth: Optional[Dict[str, str]] = None,
    encoded_argv: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
    if type(params) is not dict:
        return None
    if (
        operation['operationId'] not in ('doc.info', 'doc.blocks.list', 'doc.query.match')
        or not isinstance(params.get('sessionId'), str) or not params['sessionId']
        or params.get('doc') is not None
        or stdin_bytes is not None or collaboration_auth is not None
    ):
        return None
    if encoded_argv is None:
        return None
    flags = {f"--{spec.get('flag') or spec['name']}": spec for spec in operation['params'] if spec['kind'] != 'doc'}
    encoded: Dict[str, List[str]] = {}
    # Preserve the completed encoding even if a later serializer mutated params.
    for index in range(len(operation['commandTokens']), len(encoded_argv), 2):
        if index + 1 >= len(encoded_argv):
            return None
        flag, token = encoded_argv[index:index + 2]
        if not isinstance(token, str):
            return None
        if flag in ('--output', '--timeout-ms'):
            continue
        spec = flags.get(flag)
        if spec is None or (spec['kind'] != 'jsonFlag' and token.startswith('-')):
            return None
        encoded.setdefault(spec['name'], []).append(token)
    result: Dict[str, Any] = {}
    for spec in operation['params']:
        value = params.get(spec['name'])
        tokens = encoded.get(spec['name'])
        if tokens is None:
            if spec.get('required'):
                return None
            continue
        if spec['type'] != 'string[]' and len(tokens) != 1:
            return None
        token = tokens[0]
        if spec['kind'] == 'jsonFlag':
            try:
                result[spec['name']] = json.loads(token)
            except (ValueError, TypeError, IndexError):
                return None
            continue
        kind = spec['type']
        if kind == 'number':
            if type(value) not in (int, float):
                return None
            try:
                number = float(token)
                if not math.isfinite(value) or value < 0 or not math.isfinite(number) or number < 0:
                    return None
            except (OverflowError, ValueError):
                return None
            result[spec['name']] = number
        elif kind == 'boolean':
            if type(value) is not bool or token not in ('true', 'false'):
                return None
            result[spec['name']] = token == 'true'
        elif kind == 'string[]':
            if any(not item or item.strip() != item for item in tokens):
                return None
            result[spec['name']] = tokens
        else:
            if type(value) is not str or not token or token.strip() != token:
                return None
            result[spec['name']] = token
    try:
        json.dumps(result, allow_nan=False)
    except (ValueError, TypeError):
        return None
    return result


def resolve_watchdog_timeout(
    watchdog_timeout_ms: int,
    timeout_ms_override: Optional[int] = None,
    request_timeout_ms: Optional[int] = None,
) -> int:
    """Compute the effective watchdog timeout for a single request."""
    if timeout_ms_override is not None:
        return max(watchdog_timeout_ms, timeout_ms_override + WATCHDOG_HEADROOM_MS)
    if request_timeout_ms is not None:
        return max(watchdog_timeout_ms, request_timeout_ms + WATCHDOG_HEADROOM_MS)
    return watchdog_timeout_ms


def resolve_invocation(cli_bin: str) -> Tuple[str, List[str]]:
    """Determine how to invoke the CLI binary (bare, via node, via bun)."""
    lower = cli_bin.lower()
    if lower.endswith('.js'):
        return 'node', [cli_bin]
    if lower.endswith('.ts'):
        return 'bun', [cli_bin]
    return cli_bin, []
