import json
import logging
import os
from typing import Any
from typing import AnyStr
from typing import IO

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
from .query import QueryResult
from .query import QueryResultBatch
from .query_explain import ExplainOptions
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

LookUpResult = dict[str, str | list[EntityResult | Key]]


def init_api_root(
        api_root: str | None, api_is_dev: bool | None,
) -> tuple[bool, str]:
    if api_root:
        return api_is_dev is None or api_is_dev, api_root

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
    query_result_kind = QueryResult
    value_kind = Value

    _project: str | None
    _api_root: str
    _api_is_dev: bool

    def __init__(
            self, project: str | None = None,
            service_file: str | IO[AnyStr] | None = None,
            namespace: str = '',
            session: Session | None = None,
            token: Token | None = None,
            api_root: str | None = None,
            api_is_dev: bool | None = None,
    ) -> None:
        self._api_is_dev, self._api_root = init_api_root(api_root, api_is_dev)
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
        mutations: list[dict[str, Any]],
        transaction: str | None = None,
        mode: Mode = Mode.TRANSACTIONAL,
    ) -> dict[str, Any]:
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

    def headers(self) -> dict[str, str]:
        if self._api_is_dev:
            return {}

        token = self.token.get()
        return {
            'Authorization': f'Bearer {token}',
        }

    def _post(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        *,
        additional_request_fields: dict[str, Any] | None = None,
        session: Session | None = None,
        timeout: float = 10.,
    ) -> Any:
        merged: dict[str, Any] = {
            **(body or {}), **(additional_request_fields or {}),
        }
        headers = self.headers()
        headers['Content-Type'] = 'application/json'
        s = SyncSession(session) if session else self.session
        if merged:
            payload = json.dumps(merged).encode('utf-8')
            headers['Content-Length'] = str(len(payload))
            return s.post(
                url, data=payload, headers=headers, timeout=timeout,
            )
        headers['Content-Length'] = '0'
        return s.post(url, headers=headers, timeout=timeout)

    # TODO: support mutations w version specifiers, return new version (commit)
    @classmethod
    def make_mutation(
            cls, operation: Operation, key: Key,
            properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
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
        self, keys: list[Key],
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> list[Key]:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:allocateIds'
        resp = self._post(
            url, {'keys': [k.to_repr() for k in keys]},
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data = resp.json()
        return [self.key_kind.from_repr(k) for k in data['keys']]

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/beginTransaction
    # TODO: support readwrite vs readonly transaction types
    def beginTransaction(
        self, session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> str:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:beginTransaction'
        resp = self._post(
            url,
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data = resp.json()
        transaction: str = data['transaction']
        return transaction

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/commit
    def commit(
        self, mutations: list[dict[str, Any]],
        transaction: str | None = None,
        mode: Mode = Mode.TRANSACTIONAL,
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:commit'
        body = self._make_commit_body(
            mutations, transaction=transaction, mode=mode)
        resp = self._post(
            url, body,
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data: dict[str, Any] = resp.json()
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
        kinds: list[str] | None = None,
        namespaces: list[str] | None = None,
        labels: dict[str, str] | None = None,
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> DatastoreOperation:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:export'
        body: dict[str, Any] = {
            'entityFilter': {
                'kinds': kinds or [],
                'namespaceIds': namespaces or [],
            },
            'labels': labels or {},
            'outputUrlPrefix': f'gs://{output_bucket_prefix}',
        }
        resp = self._post(
            url, body,
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data: dict[str, Any] = resp.json()
        return self.datastore_operation_kind.from_repr(data)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects.operations/get
    def get_datastore_operation(
        self, name: str,
        session: Session | None = None,
        timeout: float = 10.,
    ) -> DatastoreOperation:
        url = f'{self._api_root}/{name}'

        headers = self.headers()
        headers.update({
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout)
        data: dict[str, Any] = resp.json()

        return self.datastore_operation_kind.from_repr(data)

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/lookup
    def lookup(
            self, keys: list[Key],
            transaction: str | None = None,
            newTransaction: TransactionOptions | None = None,
            consistency: Consistency = Consistency.STRONG,
            read_time: str | None = None,
            session: Session | None = None, timeout: float = 10.,
            additional_request_fields: dict[str, Any] | None = None,
    ) -> LookUpResult:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:lookup'
        read_options = self._build_read_options(
            consistency, newTransaction, transaction, read_time,
        )
        resp = self._post(
            url,
            {'keys': [k.to_repr() for k in keys], 'readOptions': read_options},
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data: dict[str, Any] = resp.json()
        return self._build_lookup_result(data)

    def _build_lookup_result(self, data: dict[str, Any]) -> LookUpResult:
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
        if 'readTime' in data:
            read_time: str = data['readTime']
            result['readTime'] = read_time
        return result

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/ReadOptions
    def _build_read_options(
            self, consistency: Consistency,
            newTransaction: TransactionOptions | None,
            transaction: str | None, read_time: str | None,
    ) -> dict[str, Any]:
        # TODO: expose ReadOptions directly to users
        if transaction:
            return {'transaction': transaction}

        if newTransaction:
            return {'newTransaction': newTransaction.to_repr()}

        if read_time:
            return {'readTime': read_time}

        return {'readConsistency': consistency.value}

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/reserveIds
    def reserveIds(
        self, keys: list[Key], database_id: str = '',
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> None:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:reserveIds'
        self._post(
            url,
            {'databaseId': database_id, 'keys': [k.to_repr() for k in keys]},
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/rollback
    def rollback(
        self, transaction: str,
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> None:
        project = self.project()
        url = f'{self._api_root}/projects/{project}:rollback'
        self._post(
            url, {'transaction': transaction},
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )

    # https://cloud.google.com/datastore/docs/reference/data/rest/v1/projects/runQuery
    def runQuery(
        self, query: BaseQuery,
        explain_options: ExplainOptions | None = None,
        transaction: str | None = None,
        newTransaction: TransactionOptions | None = None,
        consistency: Consistency = Consistency.EVENTUAL,
        read_time: str | None = None,
        session: Session | None = None,
        timeout: float = 10.,
        additional_request_fields: dict[str, Any] | None = None,
    ) -> QueryResult:
        # pylint: disable=too-many-locals
        project = self.project()
        url = f'{self._api_root}/projects/{project}:runQuery'
        read_options = self._build_read_options(
            consistency, newTransaction, transaction, read_time,
        )
        body: dict[str, Any] = {
            'partitionId': {
                'projectId': project,
                'namespaceId': self.namespace,
            },
            query.json_key: query.to_repr(),
            'readOptions': read_options,
        }
        if explain_options:
            body['explainOptions'] = explain_options.to_repr()
        resp = self._post(
            url, body,
            additional_request_fields=additional_request_fields,
            session=session, timeout=timeout,
        )
        data: dict[str, Any] = resp.json()
        return self.query_result_kind.from_repr(data)

    def delete(
        self, key: Key,
        session: Session | None = None,
    ) -> dict[str, Any]:
        return self.operate(Operation.DELETE, key, session=session)

    def insert(
        self, key: Key, properties: dict[str, Any],
        session: Session | None = None,
    ) -> dict[str, Any]:
        return self.operate(
            Operation.INSERT, key, properties,
            session=session,
        )

    def update(
        self, key: Key, properties: dict[str, Any],
        session: Session | None = None,
    ) -> dict[str, Any]:
        return self.operate(
            Operation.UPDATE, key, properties,
            session=session,
        )

    def upsert(
        self, key: Key, properties: dict[str, Any],
        session: Session | None = None,
    ) -> dict[str, Any]:
        return self.operate(
            Operation.UPSERT, key, properties,
            session=session,
        )

    # TODO: accept Entity rather than key/properties?
    def operate(
        self, operation: Operation, key: Key,
        properties: dict[str, Any] | None = None,
        session: Session | None = None,
    ) -> dict[str, Any]:
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
