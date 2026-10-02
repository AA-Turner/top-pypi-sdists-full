"""Local SDK projections of generated contract introspection metadata."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

from .errors import SuperDocError
from .generated.contract import CONTRACT, OPERATION_INDEX


def describe_contract() -> Dict[str, Any]:
    return deepcopy(CONTRACT['introspection']['overview'])


def describe_contract_operation(params: Dict[str, Any]) -> Dict[str, Any]:
    raw_query = params.get('operationId')
    if raw_query is None:
        raise SuperDocError(
            'Missing required parameter: operationId',
            code='INVALID_ARGUMENT',
        )
    query = str(raw_query)
    if len(query) == 0:
        raise SuperDocError(
            'describe command: missing required input.operationId.',
            code='MISSING_REQUIRED',
            exit_code=1,
        )

    index = CONTRACT['introspection']['lookup'].get(query.strip().lower())
    if index is None:
        raise SuperDocError(
            f'Unknown operation: {query}',
            code='TARGET_NOT_FOUND',
            details={'query': query},
            exit_code=1,
        )

    summary = CONTRACT['introspection']['overview']['operations'][index]
    operation = OPERATION_INDEX[summary['id']]
    detail_params = []
    for param in operation['params']:
        detail = {'name': param['name'], 'kind': param['kind']}
        if 'flag' in param:
            detail['flag'] = param['flag']
        detail['type'] = param['type']
        if 'required' in param:
            detail['required'] = param['required']
        if 'description' in param:
            detail['description'] = param['description']
        if 'schema' in param:
            detail['schema'] = param['schema']
        detail_params.append(detail)

    return deepcopy({
        'contractVersion': CONTRACT['contractVersion'],
        'query': query,
        'operation': {
            **summary,
            'params': detail_params,
            'constraints': operation.get('constraints'),
        },
    })
