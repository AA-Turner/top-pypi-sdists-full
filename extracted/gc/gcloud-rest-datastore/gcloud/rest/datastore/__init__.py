"""
This library implements various methods for working with the Google Datastore
APIs.

Installation
------------

.. code-block:: console

    $ pip install --upgrade gcloud-rest-datastore

Usage
-----

We're still working on documentation; for now, this should help get you
started:

.. code-block:: python

    from gcloud.rest.datastore import Datastore
    from gcloud.rest.datastore import Direction
    from gcloud.rest.datastore import Filter
    from gcloud.rest.datastore import GQLQuery
    from gcloud.rest.datastore import Key
    from gcloud.rest.datastore import PathElement
    from gcloud.rest.datastore import PropertyFilter
    from gcloud.rest.datastore import PropertyFilterOperator
    from gcloud.rest.datastore import PropertyOrder
    from gcloud.rest.datastore import Query
    from gcloud.rest.datastore import Value

    ds = Datastore('my-gcloud-project', '/path/to/creds.json')
    key1 = Key('my-gcloud-project', [PathElement('Kind', 'entityname')])
    key2 = Key('my-gcloud-project', [PathElement('Kind', 'entityname2')])

    # batched lookups
    entities = ds.lookup([key1, key2])

    # convenience functions for any datastore mutations
    ds.insert(key1, {'a_boolean': True, 'meaning_of_life': 41})
    ds.update(key1, {'a_boolean': True, 'meaning_of_life': 42})
    ds.upsert(key1, {'animal': 'aardvark'})
    ds.delete(key1)

    # or build your own mutation sequences with full transaction support
    transaction = ds.beginTransaction()
    try:
        mutations = [
            ds.make_mutation(Operation.INSERT, key1,
                             properties={'animal': 'sloth'}),
            ds.make_mutation(Operation.UPSERT, key1,
                             properties={'animal': 'aardvark'}),
            ds.make_mutation(Operation.INSERT, key2,
                             properties={'animal': 'aardvark'}),
        ]
        ds.commit(transaction, mutations=mutations)
    except Exception:
        ds.rollback(transaction)

    # support for partial keys
    partial_key = Key('my-gcloud-project', [PathElement('Kind')])
    # and ID allocation or reservation
    allocated_keys = ds.allocateIds([partial_key])
    ds.reserveIds(allocated_keys)

    # query support
    property_filter = PropertyFilter(prop='answer',
                                     operator=PropertyFilterOperator.EQUAL,
                                     value=Value(42))
    property_order = PropertyOrder(prop='length',
                                   direction=Direction.DESCENDING)
    query = Query(kind='the_meaning_of_life',
                  query_filter=Filter(property_filter),
                  order=property_order)
    results = ds.runQuery(query, session=s)

    # alternatively, query support using GQL
    gql_query = GQLQuery(
        'SELECT * FROM meaning_of_life WHERE answer = @answer',
        named_bindings={'answer': 42})
    results = ds.runQuery(gql_query, session=s)

    # close the HTTP session
    # Note that other options include:
    # * providing your own session: `Datastore(.., session=session)`
    # * using a context manager: `with Datastore(..) as ds:`
    ds.close()

Custom Subclasses
-----------------

``gcloud-rest-datastore`` provides class interfaces mirroring all official
Google API types, ie. ``Key`` and ``PathElement``, ``Entity`` and
``EntityResult``, ``QueryResultBatch``, and ``Value``. These types will be
returned from arbitrary Datastore operations, for example
``Datastore.allocateIds(...)`` will return a list of ``Key`` entities.

For advanced usage, all of these datatypes may be overloaded. A common use-case
may be to deserialize entities into more specific classes. For example, given a
custom entity class such as:

.. code-block:: python

    class MyEntityKind(gcloud.rest.datastore.Entity):
        def __init__(self, key, properties = None) -> None:
            self.key = key
            self.is_an_aardvark = (properties or {}).get('aardvark', False)

        def __repr__(self):
            return "I'm an aardvark!" if self.is_an_aardvark else "Sorry, nope"

We can then configure ``gcloud-rest-datastore`` to serialize/deserialize from
this custom entity class with:

.. code-block:: python

    class MyCustomDatastore(gcloud.rest.datastore.Datastore):
        entity_result_kind.entity_kind = MyEntityKind

The full list of classes which may be overridden in this way is:

.. code-block:: python

    class MyVeryCustomDatastore(gcloud.rest.datastore.Datastore):
        datastore_operation_kind = DatastoreOperation
        entity_result_kind = EntityResult
        entity_result_kind.entity_kind = Entity
        entity_result_kind.entity_kind.key_kind = Key
        key_kind = Key
        key_kind.path_element_kind = PathElement
        mutation_result_kind = MutationResult
        mutation_result_kind.key_kind = Key
        query_result_batch_kind = QueryResultBatch
        query_result_batch_kind.entity_result_kind = EntityResult
        value_kind = Value
        value_kind.key_kind = Key

    class MyVeryCustomQuery(gcloud.rest.datastore.Query):
        value_kind = Value

    class MyVeryCustomGQLQuery(gcloud.rest.datastore.GQLQuery):
        value_kind = Value

You can then drop-in the ``MyVeryCustomDatastore`` class anywhere where you
previously used ``Datastore`` and do the same for ``Query`` and ``GQLQuery``.

To override any sub-key, you'll need to override any parents which use it. For
example, if you want to use a custom ``Key`` kind and be able to use queries
with it, you will need to implement your own ``Value``, ``Query``, and
``GQLQuery`` classes and wire them up to the rest of the custom classes:

.. code-block:: python

    class MyKey(gcloud.rest.datastore.Key):
        pass

    class MyValue(gcloud.rest.datastore.Value):
        key_kind = MyKey

    class MyEntity(gcloud.rest.datastore.Entity):
        key_kind = MyKey
        value_kind = MyValue

    class MyEntityResult(gcloud.rest.datastore.EntityResult):
        entity_kind = MyEntity

    class MyQueryResultBatch(gcloud.rest.datastore.QueryResultBatch):
        entity_result_kind = MyEntityResult

    class MyDatastore(gcloud.rest.datastore.Datastore):
        key_kind = MyKey
        entity_result_kind = MyEntityResult
        query_result_batch = MyQueryResultBatch
        value_kind = MyValue

    class MyQuery(gcloud.rest.datastore.Query):
        value_kind = MyValue

    class MyGQLQuery(gcloud.rest.datastore.GQLQuery):
        value_kind = MyValue
"""
import importlib.metadata

from .array import Array
from .constants import CompositeFilterOperator
from .constants import Consistency
from .constants import Direction
from .constants import Mode
from .constants import MoreResultsType
from .constants import Operation
from .constants import PropertyFilterOperator
from .constants import ResultType
from .datastore import Datastore
from .datastore import SCOPES
from .datastore_operation import DatastoreOperation
from .entity import Entity
from .entity import EntityResult
from .filter import CompositeFilter
from .filter import Filter
from .filter import PropertyFilter
from .key import Key
from .key import PathElement
from .lat_lng import LatLng
from .mutation import MutationResult
from .projection import Projection
from .property_order import PropertyOrder
from .query import GQLCursor
from .query import GQLQuery
from .query import Query
from .query import QueryResultBatch
from .transaction_options import ReadOnly
from .transaction_options import ReadWrite
from .transaction_options import TransactionOptions
from .value import Value


__version__ = importlib.metadata.version('gcloud-rest-datastore')
__all__ = [
    'Array',
    'CompositeFilter',
    'CompositeFilterOperator',
    'Consistency',
    'Datastore',
    'DatastoreOperation',
    'Direction',
    'Entity',
    'EntityResult',
    'Filter',
    'GQLCursor',
    'GQLQuery',
    'Key',
    'LatLng',
    'Mode',
    'MoreResultsType',
    'MutationResult',
    'Operation',
    'PathElement',
    'Projection',
    'PropertyFilter',
    'PropertyFilterOperator',
    'PropertyOrder',
    'Query',
    'QueryResultBatch',
    'ReadOnly',
    'ReadWrite',
    'ResultType',
    'SCOPES',
    'TransactionOptions',
    'Value',
    '__version__',
]
