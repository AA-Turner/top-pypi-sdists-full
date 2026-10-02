"""Pure projection between generated SDK operations and document-host RPC."""

from __future__ import annotations

from typing import Any, Dict, Optional, Set, Tuple
from uuid import uuid4

from .errors import HOST_PROTOCOL_ERROR, SuperDocError
from .protocol import apply_operation_param_aliases

DOCUMENT_RPC_FEATURES = (
    'document.open',
    'document.invoke',
    'document.save',
    'document.close',
)
DOCUMENT_RPC_DEFAULT_CHANGE_MODE_FEATURE = 'document.open.defaultChangeMode'
DOCUMENT_RPC_REQUEST_TIMEOUT_FEATURE = 'host.request.timeoutMs'
DOCUMENT_RPC_SOURCE_SAVE_FEATURE = 'document.save.source'

_OPEN_FIELDS = {'doc', 'sessionId', 'runtime'}
_INVOKE_OPTION_FIELDS = {'expectedRevision', 'changeMode', 'dryRun', 'supportCheck'}
_REVISION_PREFLIGHT_OPERATIONS = {
    'doc.history.redo',
    'doc.history.undo',
    'doc.plan.execute',
}


def _unsupported(message: str, operation_id: Optional[str] = None) -> SuperDocError:
    return SuperDocError(
        message,
        code='DOCUMENT_RPC_INPUT_UNSUPPORTED',
        details=None if operation_id is None else {'operationId': operation_id},
    )


def _document_author(user: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
    if user is None:
        return None
    if not isinstance(user, dict):
        raise SuperDocError(
            'user must be an object with a non-empty name.',
            code='INVALID_ARGUMENT',
        )
    name = user.get('name')
    email = user.get('email')
    if not isinstance(name, str) or not name.strip():
        raise SuperDocError(
            'user.name must be a non-empty string.',
            code='INVALID_ARGUMENT',
        )
    if email is not None and not isinstance(email, str):
        raise SuperDocError('user.email must be a string.', code='INVALID_ARGUMENT')
    return {'name': name, **({} if email is None else {'email': email})}


def build_document_open_params(
    params: Dict[str, Any],
    user: Optional[Dict[str, str]] = None,
    *,
    stdin_bytes: Optional[bytes] = None,
    default_change_mode: Optional[str] = None,
) -> Tuple[str, Dict[str, Any]]:
    if stdin_bytes is not None:
        raise _unsupported('Structured document RPC does not support stdinBytes.', 'doc.open')

    unsupported_field = next(
        (name for name, value in params.items() if value is not None and name not in _OPEN_FIELDS),
        None,
    )
    if unsupported_field is not None:
        raise _unsupported(
            f'Structured document RPC does not support doc.open field {unsupported_field}.',
            'doc.open',
        )

    path = params.get('doc')
    if not isinstance(path, str) or not path.strip() or path == '-':
        raise _unsupported(
            'Structured document RPC v0 requires doc.open({"doc": path}).',
            'doc.open',
        )
    runtime = params.get('runtime')
    if runtime is not None and runtime != 'v2':
        raise _unsupported('Structured document RPC v0 only supports runtime="v2".', 'doc.open')

    requested_session_id = params.get('sessionId')
    if requested_session_id is not None and (
        not isinstance(requested_session_id, str) or not requested_session_id
    ):
        raise SuperDocError('sessionId must be a non-empty string.', code='INVALID_ARGUMENT')
    session_id = requested_session_id or str(uuid4())
    author = _document_author(user)
    return session_id, {
        'sessionId': session_id,
        'path': path,
        **({} if author is None else {'author': author}),
        **({} if default_change_mode is None else {
            'defaultChangeMode': default_change_mode,
        }),
    }


def _document_invoke_payload(
    operation: Dict[str, Any],
    params: Dict[str, Any],
    *,
    stdin_bytes: Optional[bytes],
) -> Dict[str, Any]:
    operation_id = operation.get('operationId')
    normalized_params = apply_operation_param_aliases(operation, params)
    if stdin_bytes is not None:
        raise _unsupported('Structured document RPC does not support stdinBytes.', operation_id)
    if normalized_params.get('out') is not None:
        raise _unsupported(
            'Structured document RPC does not support per-operation output paths.', operation_id,
        )
    force = normalized_params.get('force')
    if force is not None and force is not False:
        raise _unsupported('Structured document RPC does not support per-operation force.', operation_id)

    input_payload: Dict[str, Any] = {}
    options_payload: Dict[str, Any] = {}
    params_by_name = {param['name']: param for param in operation.get('params', [])}

    for name, value in normalized_params.items():
        if value is None or name in {'doc', 'sessionId', 'out', 'force'}:
            continue
        param = params_by_name.get(name)
        if param is None:
            raise _unsupported(
                f'Structured document RPC does not support {operation_id} field {name}.',
                operation_id,
            )
        input_name = param.get('documentApiInputName')
        if isinstance(input_name, str) and input_name:
            input_payload[input_name] = value
        elif name in _INVOKE_OPTION_FIELDS:
            options_payload[name] = value
        else:
            raise _unsupported(
                f'Structured document RPC does not support {operation_id} field {name}.',
                operation_id,
            )

    if 'changeMode' in options_payload and not (
        operation.get('supportsTrackedMode') is True
        or operation.get('supportsConditionalTrackedMode') is True
    ):
        if options_payload['changeMode'] == 'tracked':
            raise _unsupported(
                f'Structured document RPC does not support tracked mode for {operation_id}.',
                operation_id,
            )
        if options_payload['changeMode'] != 'direct':
            raise _unsupported(
                f'Structured document RPC received an invalid change mode for {operation_id}.',
                operation_id,
            )
        del options_payload['changeMode']

    if 'dryRun' in options_payload and operation.get('supportsDryRun') is not True:
        if options_payload['dryRun'] is True:
            raise _unsupported(
                f'Structured document RPC does not support dry run for {operation_id}.',
                operation_id,
            )
        del options_payload['dryRun']

    if 'expectedRevision' in options_payload and operation_id in _REVISION_PREFLIGHT_OPERATIONS:
        raise _unsupported(
            f'Structured document RPC does not yet support expectedRevision for {operation_id}.',
            operation_id,
        )
    if 'expectedRevision' in options_payload and operation.get('mutates') is not True:
        raise _unsupported(
            f'Structured document RPC does not support expectedRevision for {operation_id}.',
            operation_id,
        )

    return {
        'input': input_payload,
        **({} if not options_payload else {'options': options_payload}),
    }


def build_document_invoke_request(
    session_id: str,
    operation: Dict[str, Any],
    params: Dict[str, Any],
    *,
    stdin_bytes: Optional[bytes] = None,
    host_features: Optional[Set[str]] = None,
) -> Tuple[str, Dict[str, Any]]:
    operation_id = operation.get('operationId')

    if operation_id == 'doc.save':
        if stdin_bytes is not None:
            raise _unsupported(
                'Structured document RPC does not support document.save stdinBytes.', operation_id,
            )
        path = params.get('out')
        if params.get('inPlace') is not None and not isinstance(params['inPlace'], bool):
            raise _unsupported(
                'Structured document RPC requires inPlace to be a boolean.', operation_id,
            )
        if params.get('inPlace') is True and path is not None:
            raise _unsupported(
                'Structured document RPC requires either inPlace or out, not both.',
                operation_id,
            )
        if path is not None and (not isinstance(path, str) or not path):
            raise _unsupported(
                'Structured document RPC requires out to be a non-empty path.', operation_id,
            )
        allowed = {'sessionId', 'out', 'force', 'mode', 'inPlace'}
        unknown = next(
            (name for name, value in params.items() if value is not None and name not in allowed),
            None,
        )
        if unknown is not None:
            raise _unsupported(
                f'Structured document RPC does not support doc.save field {unknown}.', operation_id,
            )
        if path is None and (
            host_features is None or DOCUMENT_RPC_SOURCE_SAVE_FEATURE not in host_features
        ):
            raise _unsupported(
                'Structured document RPC host does not support source saves.', operation_id,
            )
        return 'document.save', {
            'sessionId': session_id,
            **({} if path is None else {'path': path}),
            **({} if params.get('force') is not True else {'overwrite': True}),
            **({} if params.get('mode') is None else {'mode': params['mode']}),
        }

    if operation_id == 'doc.close':
        if stdin_bytes is not None:
            raise _unsupported(
                'Structured document RPC does not support document.close stdinBytes.', operation_id,
            )
        allowed = {'sessionId', 'discard'}
        unknown = next(
            (name for name, value in params.items() if value is not None and name not in allowed),
            None,
        )
        if unknown is not None:
            raise _unsupported(
                f'Structured document RPC does not support doc.close field {unknown}.', operation_id,
            )
        return 'document.close', {
            'sessionId': session_id,
            **({} if params.get('discard') is None else {'discard': params['discard']}),
        }

    document_operation_id = operation.get('documentApiOperationId')
    if not isinstance(document_operation_id, str) or not document_operation_id:
        raise _unsupported(
            f'Structured document RPC does not support {operation_id}.', operation_id,
        )
    payload = _document_invoke_payload(operation, params, stdin_bytes=stdin_bytes)
    return 'document.invoke', {
        'sessionId': session_id,
        'operationId': document_operation_id,
        'input': payload['input'],
        **({} if 'options' not in payload else {'options': payload['options']}),
    }


def document_rpc_request_supports_response_timeout(
    operation: Dict[str, Any], method: str, params: Dict[str, Any],
) -> bool:
    if method == 'document.save':
        return False
    if method != 'document.invoke':
        return True

    options = params.get('options')
    if isinstance(options, dict) and options.get('dryRun') is True:
        return True
    if operation.get('mutates') is False:
        return True
    return operation.get('idempotency') == 'idempotent'


def map_document_open_result(
    response: Any,
    session_id: str,
    path: str,
) -> Dict[str, Any]:
    if not isinstance(response, dict):
        raise SuperDocError(
            'Host returned invalid document.open result.',
            code=HOST_PROTOCOL_ERROR,
            details={'result': response},
        )
    byte_length = response.get('byteLength')
    if (
        response.get('sessionId') != session_id
        or isinstance(byte_length, bool)
        or not isinstance(byte_length, (int, float))
    ):
        raise SuperDocError(
            'Host returned invalid document.open session metadata.',
            code=HOST_PROTOCOL_ERROR,
            details={'result': response},
        )
    return {
        'active': True,
        'contextId': session_id,
        'runtime': 'v2',
        'sessionType': 'local',
        'document': {
            'path': path,
            'source': 'path',
            'byteLength': byte_length,
            'revision': 0,
        },
        'dirty': False,
    }


def map_document_lifecycle_result(
    operation_id: str,
    response: Any,
    session_id: str,
    expected_in_place: Optional[bool] = None,
) -> Any:
    if operation_id not in {'doc.save', 'doc.close'}:
        return response
    if not isinstance(response, dict):
        label = operation_id.removeprefix('doc.')
        raise SuperDocError(
            f'Host returned invalid {label} result.',
            code=HOST_PROTOCOL_ERROR,
            details={'result': response},
        )
    if response.get('sessionId') != session_id:
        raise SuperDocError(
            'Host returned a result for the wrong document session.',
            code=HOST_PROTOCOL_ERROR,
            details={'expectedSessionId': session_id, 'result': response},
        )
    if operation_id == 'doc.close':
        if response.get('closed') is not True or not isinstance(response.get('discarded'), bool):
            raise SuperDocError(
                'Host returned invalid document.close result.',
                code=HOST_PROTOCOL_ERROR,
                details={'result': response},
            )
        return {
            'contextId': session_id,
            'runtime': 'v2',
            'closed': True,
            'saved': False,
            'discarded': response['discarded'],
            'defaultSessionCleared': False,
        }

    output = response.get('output')
    if (
        response.get('saved') is not True
        or (
            not isinstance(response.get('inPlace'), bool)
            and not ('inPlace' not in response and expected_in_place is False)
        )
        or not isinstance(output, dict)
        or not isinstance(output.get('path'), str)
        or isinstance(output.get('byteLength'), bool)
        or not isinstance(output.get('byteLength'), (int, float))
    ):
        raise SuperDocError(
            'Host returned invalid document.save result.',
            code=HOST_PROTOCOL_ERROR,
            details={'result': response},
        )
    return {
        'contextId': session_id,
        'runtime': 'v2',
        'saved': True,
        'inPlace': response.get('inPlace', False),
        'mode': response.get('mode'),
        'output': output,
        'report': response.get('report'),
    }
