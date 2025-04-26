import json
import logging
import os
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

from .constants import Consistency
from .constants import Mode
from .constants import Operation
from .datastore_operation import DatastoreOperation
from .entity import EntityResult
from .key import Key
from .mutation import MutationResult
from .query import BaseQuery
from .query import QueryResultBatch
from .transaction_options import TransactionOptions
from .value import Value

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]


# TODO: is cloud-platform needed?
SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
]

log = logging.getLogger(__name__)

LookUpResult = Dict[str, Union[str, List[Union[EntityResult, Key]]]]


def init_api_root(api_root: Optional[str]) -> Tuple[bool, str]:
    if api_root:
        return True, api_root

    host = os.environ.get('DATASTORE_EMULATOR_HOST')
    if host:
        return True, f'http://{host}/v1'

    return False, 'https://datastore.googleapis.com/v1'


class Datastore:
    datastore_operation_kind = DatastoreOperation
    entity_result_kind = EntityResult
    key_kind = Key
    mutation_result_kind = MutationResult
    query_result_batch_kind = QueryResultBatch
    value_kind = Value

    _project: Optional[str]
    _api_root: str
    _api_is_dev: bool

    def __init__(
            self, project: Optional[str] = None,
            service_file: Optional[Union[str, IO[AnyStr]]] = None,
            namespace: str = '', session: Optional[Session] = None,
            token: Optional[Token] = None, api_root: Optional[str] = None,
    ) -> None:
        self._api_is_dev, self._api_root = init_api_root(api_root)
        self.namespace = namespace
        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

        self._project = project
        if self._api_is_dev and not project:
            self._project = (
                os.environ.get('DATASTORE_PROJECT_ID')
                or os.environ.get('GOOGLE_CLOUD_PROJECT')
                or 'dev'
            )

    def project(self) -> str:
        if self._project:
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    @staticmethod
    def _make_commit_body(
        mutations: List[Dict[str, Any]],
        transaction: Optional[str] = None,
        mode: Mode = Mode.TRANSACTIONAL,
    ) -> Dict[str, Any]:
        if not mutations:
            raise Exception('at least one mutation record is required')

        if transaction is None and mode != Mode.NON_TRANSACTIONAL:
            raise Exception(
                'a transaction ID must be provided when mode is '
                'transactional',
            )

        data = {
            'mode': mode.value,
            'mutations': mutations,
        }
        if transaction is not None:
            data['transaction'] = transaction
        return data

    def headers(self) -> Dict[str, str]:
        if self._api_is_dev:
            return {}

        token = self.token.get()
        return {
            'Authorization': f'Bearer {token}',
        }

    # TODO: support mutations w version specifiers, return new version (commit)
    @classmethod
    def make_mutation(
            cls, operation: Operation, key: Key,
            properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if operation == Operation.DELETE:
            return {operation.value: key.to_repr()}

        mutation_properties = {}
        for k, v in (properties or {}).items():
            value = v if isinstance(v, cls.value_kind) else cls.value_kind(v)
            mutation_properties[k] = value.to_repr()

        return {
            operation.value: {
                'key': key.to_repr(),
                'properties': mutation_properties,
            },
        }

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/allocateIds
    def allocateIds(
        self, keys: List[Key],
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> List[Key]:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:allocateIds'

        payload = json.dumps({
            'keys': [k.to_repr() for k in keys],
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(
            url, data=payload, headers=headers,
            timeout=timeout,
        )
        data = resp.json()

        return [self.key_kind.from_repr(k) for k in data['keys']]

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/beginTransaction
    # TODO: support readwrite vs readonly transaction types
    def beginTransaction(
        self, session: Optional[Session] = None,
        timeout: int = 10,
    ) -> str:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:beginTransaction'
        headers = self.headers()
        headers.update({
            'Content-Length': '0',
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, timeout=timeout)
        data = resp.json()

        transaction: str = data['transaction']
        return transaction

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/commit
    def commit(
        self, mutations: List[Dict[str, Any]],
        transaction: Optional[str] = None,
        mode: Mode = Mode.TRANSACTIONAL,
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:commit'

        body = self._make_commit_body(
            mutations, transaction=transaction,
            mode=mode,
        )
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(
            url, data=payload, headers=headers,
            timeout=timeout,
        )
        data: Dict[str, Any] = resp.json()

        return {
            'mutationResults': [
                self.mutation_result_kind.from_repr(r)
                for r in data.get('mutationResults', [])
            ],
            'indexUpdates': data.get('indexUpdates', 0),
        }

    # https://cloud.google.com/datastore/docs/reference/admin/rest/v1/projects/export
    def export(
        self, output_bucket_prefix: str,
        kinds: Optional[List[str]] = None,
        namespaces: Optional[List[str]] = None,
        labels: Optional[Dict[str, str]] = None,
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> DatastoreOperation:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:export'

        payload = json.dumps({
            'entityFilter': {
                'kinds': kinds or [],
                'namespaceIds': namespaces or [],
            },
            'labels': labels or {},
            'outputUrlPrefix': f'gs://{output_bucket_prefix}',
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(
            url, data=payload, headers=headers,
            timeout=timeout,
        )
        data: Dict[str, Any] = resp.json()

        return self.datastore_operation_kind.from_repr(data)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects.operations/get
    def get_datastore_operation(
        self, name: str,
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> DatastoreOperation:
        url = f'{self._api_root}/{name}'

        headers = self.headers()
        headers.update({
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        data: Dict[str, Any] = resp.json()

        return self.datastore_operation_kind.from_repr(data)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/lookup
    def lookup(
            self, keys: List[Key],
            transaction: Optional[str] = None,
            newTransaction: Optional[TransactionOptions] = None,
            consistency: Consistency = Consistency.STRONG,
            session: Optional[Session] = None, timeout: int = 10,
    ) -> LookUpResult:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:lookup'

        read_options = self._build_read_options(
            consistency, newTransaction, transaction)

        payload = json.dumps({
            'keys': [k.to_repr() for k in keys],
            'readOptions': read_options,
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(
            url, data=payload, headers=headers,
            timeout=timeout,
        )

        data: Dict[str, Any] = resp.json()

        return self._build_lookup_result(data)

    def _build_lookup_result(self, data: Dict[str, Any]) -> LookUpResult:
        result: LookUpResult = {
            'found': [
                self.entity_result_kind.from_repr(e)
                for e in data.get('found', [])
            ],
            'missing': [
                self.entity_result_kind.from_repr(e)
                for e in data.get('missing', [])
            ],
            'deferred': [
                self.key_kind.from_repr(k)
                for k in data.get('deferred', [])
            ],
        }
        if 'transaction' in data:
            new_transaction: str = data['transaction']
            result['transaction'] = new_transaction
        return result

    def _build_read_options(self,
                            consistency: Consistency,
                            newTransaction: Optional[TransactionOptions],
                            transaction: Optional[str]) -> Dict[str, Any]:
        # TODO: expose ReadOptions directly to users
        # See
        # https://cloud.google.com/datastore/docs/reference/data/rest/v1/ReadOptions
        if transaction:
            return {'transaction': transaction}

        if newTransaction:
            return {'newTransaction': newTransaction.to_repr()}

        return {'readConsistency': consistency.value}

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/reserveIds
    def reserveIds(
        self, keys: List[Key], database_id: str = '',
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> None:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:reserveIds'

        payload = json.dumps({
            'databaseId': database_id,
            'keys': [k.to_repr() for k in keys],
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        s.post(url, data=payload, headers=headers, timeout=timeout)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/rollback
    def rollback(
        self, transaction: str,
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> None:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:rollback'

        payload = json.dumps({
            'transaction': transaction,
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        s.post(url, data=payload, headers=headers, timeout=timeout)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/runQuery
    def runQuery(
        self, query: BaseQuery,
        transaction: Optional[str] = None,
        consistency: Consistency = Consistency.EVENTUAL,
        session: Optional[Session] = None,
        timeout: int = 10,
    ) -> QueryResultBatch:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:runQuery'

        if transaction:
            options = {'transaction': transaction}
        else:
            options = {'readConsistency': consistency.value}
        payload = json.dumps({
            'partitionId': {
                'projectId': project,
                'namespaceId': self.namespace,
            },
            query.json_key: query.to_repr(),
            'readOptions': options,
        }).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(
            url, data=payload, headers=headers,
            timeout=timeout,
        )

        data: Dict[str, Any] = resp.json()
        return self.query_result_batch_kind.from_repr(data['batch'])

    def delete(
        self, key: Key,
        session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        return self.operate(Operation.DELETE, key, session=session)

    def insert(
        self, key: Key, properties: Dict[str, Any],
        session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        return self.operate(
            Operation.INSERT, key, properties,
            session=session,
        )

    def update(
        self, key: Key, properties: Dict[str, Any],
        session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        return self.operate(
            Operation.UPDATE, key, properties,
            session=session,
        )

    def upsert(
        self, key: Key, properties: Dict[str, Any],
        session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        return self.operate(
            Operation.UPSERT, key, properties,
            session=session,
        )

    # TODO: accept Entity rather than key/properties?
    def operate(
        self, operation: Operation, key: Key,
        properties: Optional[Dict[str, Any]] = None,
        session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        transaction = self.beginTransaction(session=session)
        mutation = self.make_mutation(operation, key, properties=properties)
        return self.commit(
            [mutation], transaction=transaction,
            session=session,
        )

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> 'Datastore':
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
