from typing import List, Union, Optional, Any
from dataclasses import fields, is_dataclass
import asyncio
from pathlib import Path, PurePath
from fastavro import writer, reader, parse_schema
from pymilvus import (
    MilvusClient,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    connections,
    db
)
from pymilvus.exceptions import MilvusException
from langchain_milvus import Milvus  # pylint: disable=import-error, E0611
from langchain.schema import Document
from ..credentials import CredentialsInterface
from ...conf import (
    MILVUS_URL,
    MILVUS_HOST,
    MILVUS_PORT,
    MILVUS_DATABASE,
    MILVUS_PROTOCOL,
    MILVUS_USER,
    MILVUS_PASSWORD,
    MILVUS_TOKEN,
    MILVUS_SECURE,
    MILVUS_SERVER_NAME,
    MILVUS_CA_CERT,
    MILVUS_SERVER_CERT,
    MILVUS_SERVER_KEY,
    MILVUS_USE_TLSv2
)
from .abstract import AbstractStore


class MilvusStore(AbstractStore, CredentialsInterface):
    """
    Interface for managing document storage in Milvus using LangChain.
    """
    _credentials: dict = {
        "uri": str,
        "host": str,
        "port": int,
        "user": str,
        "password": str,
        "token": str,
        "db_name": str,
        "collection_name": str,
    }

    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop("host", MILVUS_HOST)
        self.port = kwargs.pop("port", MILVUS_PORT)
        self.protocol = kwargs.pop("protocol", MILVUS_PROTOCOL)
        self._secure: bool = kwargs.pop('secure', MILVUS_SECURE)
        self.create_database: bool = kwargs.pop('create_database', True)
        self.collection_name = kwargs.pop('collection_name', None)
        self.consistency_level: str = kwargs.pop('consistency_level', 'Session')
        super().__init__(*args, **kwargs)

    def processing_credentials(self):
        super().processing_credentials()
        self.url = self.credentials.get('uri', MILVUS_URL)
        if not self.url:
            self.url = MILVUS_URL
        self.host = self.credentials.get('host', self.host)
        self.protocol = self.credentials.pop('protocol', self.protocol)
        self.port = self.credentials.get('port', self.port)
        self.collection_name = self.credentials.pop('collection_name', self.collection_name)
        if not self.url:
            self.url = f"{self.protocol}://{self.host}:{self.port}"
            self.credentials['uri'] = self.url
        else:
            # Extract host and port from URL
            if not self.host:
                self.host = self.url.split("://")[-1].split(":")[0]
            if not self.port:
                self.port = int(self.url.split(":")[-1])
        self.token = self.credentials.pop("token", MILVUS_TOKEN)
        # user and password (if required)
        self.user = self.credentials.pop("user", MILVUS_USER)
        self.password = self.credentials.pop("password", MILVUS_PASSWORD)
        # Database:
        self.database = self.credentials.get('db_name', MILVUS_DATABASE)
        # SSL/TLS
        self._server_name: str = self.credentials.get('server_name', MILVUS_SERVER_NAME)
        self._cert: str = self.credentials.pop('server_pem_path', MILVUS_SERVER_CERT)
        self._ca_cert: str = self.credentials.pop('ca_pem_path', MILVUS_CA_CERT)
        self._cert_key: str = self.credentials.pop('client_key_path', MILVUS_SERVER_KEY)

        if self.token:
            self.credentials['token'] = self.token
        if self.user:
            self.credentials['token'] = f"{self.user}:{self.password}"
        if self._secure is True:
            args = {
                "secure": self._secure,
                "server_name": self._server_name
            }
            if self._cert:
                if MILVUS_USE_TLSv2 is True:
                    args['client_pem_path'] = self._cert
                    args['client_key_path'] = self._cert_key
                else:
                    args["server_pem_path"] = self._cert
            if self._ca_cert:
                args['ca_pem_path'] = self._ca_cert
            self.credentials = {**self.credentials, **args}

    async def connect(self, alias: str = None) -> "MilvusStore":
        """Connects to the Milvus database."""
        if not alias:
            self._client_id = 'default'
        else:
            self._client_id = alias
        _ = connections.connect(
            alias=self._client_id,
            **self.credentials
        )
        if self.database:
            self.use_database(
                self.database,
                alias=self._client_id,
                create=self.create_database
            )
        self._connection = MilvusClient(
            **self.credentials
        )

    async def disconnect(self, alias: str = 'default'):
        try:
            connections.disconnect(alias=alias)
            self._connection.close()
        except AttributeError:
            pass
        finally:
            self._connection = None

    def use_database(
        self,
        db_name: str,
        alias: str = 'default',
        create: bool = False
    ) -> None:
        try:
            conn = connections.connect(alias, **self.credentials)
        except MilvusException as exc:
            if "database not found" in exc.message:
                args = self.credentials.copy()
                del args['db_name']
                self.create_database(db_name, alias=alias, **args)
        # re-connect:
        try:
            _ = connections.connect(alias, **self.credentials)
            if db_name not in db.list_database(using=alias):
                if self.create_database is True or create is True:
                    try:
                        db.create_database(db_name, using=alias, timeout=10)
                        self.logger.notice(
                            f"Database {db_name} created successfully."
                        )
                    except Exception as e:
                        raise ValueError(
                            f"Error creating database: {e}"
                        )
                else:
                    raise ValueError(
                        f"Database {db_name} does not exist."
                    )
        finally:
            connections.disconnect(alias=alias)

    def create_database(self, db_name: str, alias: str = 'default', **kwargs) -> bool:
        args = {
            "uri": self.url,
            "host": self.host,
            "port": self.port,
            **kwargs
        }
        try:
            conn = connections.connect(alias, **args)
            db.create_database(db_name)
            self.logger.notice(
                f"Database {db_name} created successfully."
            )
        except Exception as e:
            raise ValueError(
                f"Error creating database: {e}"
            )
        finally:
            connections.disconnect(alias=alias)

    async def delete_documents_by_attr(
        self,
        collection_name: str,
        attribute_name: str,
        attribute_value: str
    ):
        """
        Deletes documents in the Milvus collection that match a specific attribute.

        This asynchronous method removes documents from a specified Milvus collection
        where the given attribute matches the provided value.

        Args:
            collection_name (str): The name of the Milvus collection to delete from.
            attribute_name (str): The name of the attribute to filter on.
            attribute_value (str): The value of the attribute to match for deletion.

        Raises:
            Exception: If the deletion operation fails, the error is logged and re-raised.

        Returns:
            None

        Note:
            The method logs a notice with the number of deleted documents upon successful deletion.
        """
        try:
            async with self:
                if self._connection is None:
                    print("Error: Not connected to Milvus. Please call connect() first.")
                    return
                deleted = self._connection.delete(
                    collection_name=collection_name,
                    filter=f'{attribute_name} == "{attribute_value}"'
                )
                self.logger.notice(
                    f"Documents with {attribute_name} = {attribute_value} deleted: {deleted}"
                )
        except Exception as e:
            self.logger.error(f"Failed to delete documents: {e}")
            raise

    async def load_documents(
        self,
        documents: List[Document],
        upsert: Optional[bool] = True,
        collection: str = None,
        pk: str = 'source_type',
        dimension: int = 768,
        index_type: str = 'HNSW',
        metric_type: str = 'L2',
        **kwargs
    ):
        """
        Loads LangChain documents into the Milvus collection.

        Args:
            documents (List[Document]): List of LangChain Document objects.
            upsert (bool): If True, delete existing documents with matching attributes before inserting.
            pk: str: If upsert True, Key to be used for deleting documents before inserting.
            collection (str): Name of the collection.
        """
        if not self._connection:
            await self.connect()

        if not collection:
            collection = self.collection

        # Add posibility of creating the Collection
        # Ensure the collection exists before attempting deletes or inserts
        if not await self.collection_exists(collection):
            # Attempt to create the collection
            await self.create_default_collection(
                collection_name=collection,
                dimension=dimension,
                index_type=index_type,
                metric_type=metric_type
            )

        if upsert is True:
            # Delete documents with matching `category`
            for doc in documents:
                category = doc.metadata.get(pk)
                if category:
                    await self.delete_documents_by_attr(collection, pk, category)

        # Insert documents asynchronously
        async with self:
            if self._connection is None:
                print("Error: Not connected to Milvus. Please call connect() first.")
                return
            print('Inserting documents  ', documents[0])
            docstore = await Milvus.afrom_documents(
                documents,
                embedding=self._embed_,
                connection_args={**self.credentials},
                collection_name=collection,
                drop_old=False,
                consistency_level=self.consistency_level,
                primary_field='pk',
                text_field=self.text_field,
                vector_field=self.vector_field,
                **kwargs
            )
        self.logger.info(
            f"{len(documents)} Docs loaded into Milvus collection '{collection}': {docstore}"
        )
        return docstore, documents

    async def collection_exists(self, collection_name: str) -> bool:
        async with self:
            collections = self._connection.list_collections()
            return collection_name in collections

    def check_state(self, collection_name: str) -> dict:
        return self._connection.get_load_state(collection_name=collection_name)

    async def delete_collection(self, collection: str = None) -> dict:
        self._connection.drop_collection(
            collection_name=collection
        )

    async def create_default_collection(
        self,
        collection_name: str,
        document: Any = None,
        dimension: int = 768,
        index_type: str = None,
        metric_type: str = None,
        schema_type: str = 'default',
        database: Optional[str] = None,
        metadata_field: str = None,
        **kwargs
    ) -> dict:
        """create_collection.

        Create a Schema (Milvus Collection) on the Current Database.

        Args:
            collection_name (str): Collection Name.
            document (Any): List of Documents.
            dimension (int, optional): Vector Dimension. Defaults to 768.
            index_type (str, optional): Default index type of Vector Field. Defaults to "HNSW".
            metric_type (str, optional): Default Metric for Vector Index. Defaults to "L2".
            schema_type (str, optional): Description of Model. Defaults to 'default'.

        Returns:
            dict: _description_
        """
        # Check if collection exists:
        if await self.collection_exists(collection_name):
            self.logger.warning(
                f"Collection {collection_name} already exists."
            )
            return None

        if not database:
            database = self.database
        idx_params = {}
        if not index_type:
            index_type = self._index_type
        if index_type == 'HNSW':
            idx_params = {
                "M": 36,
                "efConstruction": 1024
            }
        elif index_type in ('IVF_FLAT', 'SCANN', 'IVF_SQ8'):
            idx_params = {
                "nlist": 1024
            }
        elif index_type in ('IVF_PQ'):
            idx_params = {
                "nlist": 1024,
                "m": 16
            }
        if not metric_type:
            metric_type = self._metric_type  # default metric type
        # print('::::::::::: HERE > ', index_type, idx_params, metric_type)
        async with self:
            if schema_type == 'default':
                # Default Collection for all loaders:
                schema = MilvusClient.create_schema(
                    auto_id=False,
                    enable_dynamic_field=True,
                    description=collection_name
                )
                schema.add_field(
                    field_name="pk",
                    datatype=DataType.INT64,
                    is_primary=True,
                    auto_id=True,
                    max_length=100
                )
                schema.add_field(
                    field_name="url",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="source",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="filename",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="question",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="answer",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="source_type",
                    datatype=DataType.VARCHAR,
                    max_length=128
                )
                schema.add_field(
                    field_name="type",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="category",
                    datatype=DataType.VARCHAR,
                    max_length=65535
                )
                schema.add_field(
                    field_name="text",
                    datatype=DataType.VARCHAR,
                    description="Text",
                    max_length=65535
                )
                schema.add_field(
                    field_name="summary",
                    datatype=DataType.VARCHAR,
                    description="Summary (refine resume)",
                    max_length=65535
                )
                schema.add_field(
                    field_name="vector",
                    datatype=DataType.FLOAT_VECTOR,
                    dim=dimension,
                    description="vector"
                )
                schema.add_field(
                    field_name="document_meta",
                    datatype=DataType.JSON,
                    description="Custom Metadata information"
                )
                index_params = self._connection.prepare_index_params()
                index_params.add_index(
                    field_name="pk",
                    index_type="STL_SORT"
                )
                index_params.add_index(
                    field_name="text",
                    index_type="marisa-trie"
                )
                index_params.add_index(
                    field_name="summary",
                    index_type="marisa-trie"
                )
                index_params.add_index(
                    field_name="vector",
                    index_type=index_type,
                    metric_type=metric_type,
                    params=idx_params
                )
                self._connection.create_collection(
                    collection_name=collection_name,
                    schema=schema,
                    index_params=index_params,
                    num_shards=2
                )
                await asyncio.sleep(2)
                self._connection.get_load_state(
                    collection_name=collection_name
                )
                return None
            else:
                # Create a Collection based on a Document
                self._connection.create_collection(
                    collection_name=collection_name,
                    dimension=dimension
                )
                if metadata_field:
                    kwargs['metadata_field'] = metadata_field
                # Here using drop_old=True to force recreate based on the first document
                docstore = Milvus.from_documents(
                    [document],  # Only the first document
                    self._embed_,
                    connection_args={**self.kwargs},
                    collection_name=collection_name,
                    drop_old=True,
                    consistency_level='Session',
                    primary_field='pk',
                    text_field='text',
                    vector_field='vector',
                    **kwargs
                )
                return docstore

    def _minimal_schema(self, dimension: int) -> List[FieldSchema]:
        """Defines a minimal schema with basic fields."""
        return [
            FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source_type", dtype=DataType.VARCHAR, max_length=128),
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=128),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dimension),
        ]

    async def create_collection(
        self,
        collection_name: str,
        origin: Union[str, Path, Any] = None,
        dimension: int = 768,
        index_type: str = "HNSW",
        metric_type: str = "L2",
        **kwargs
    ) -> dict:
        """
        Create a Milvus collection based on an origin.

        Args:
            collection_name (str): Name of the Milvus collection.
            origin (Union[str, Path, Any]): None for minimal schema, Path for Avro file, or dataclass for schema.
            dimension (int, optional): Dimension of the vector field. Defaults to 768.
            index_type (str, optional): Index type for vector field. Defaults to "HNSW".
            metric_type (str, optional): Metric type for vector index. Defaults to "L2".

        Returns:
            dict: Result of the collection creation.
        """
        if await self.collection_exists(collection_name):
            self.logger.warning(
                f"Collection {collection_name} already exists."
            )
            return None
        idx_params = {}
        if not index_type:
            index_type = self._index_type
        if index_type == 'HNSW':
            idx_params = {
                "M": 36,
                "efConstruction": 1024
            }
        elif index_type in ('IVF_FLAT', 'SCANN', 'IVF_SQ8'):
            idx_params = {
                "nlist": 1024
            }
        elif index_type in ('IVF_PQ'):
            idx_params = {
                "nlist": 1024,
                "m": 16
            }

        _fields = []

        if origin is None:
            # Define minimal schema with basic fields
            _fields = self._minimal_schema(dimension)
        elif is_dataclass(origin):
            # Define schema based on dataclass fields
            _fields = self._as_dataclass_schema(origin)
        elif isinstance(origin, (PurePath, str)):
            if isinstance(origin, str):
                origin = Path(origin).resolve()
            _fields = self._as_avro_schema(origin)

        # Create the collection schema and collection
        schema = CollectionSchema(
            _fields,
            description=f"Schema for {collection_name}"
        )
        await self._create_milvus_collection(
            collection_name,
            schema, index_type, metric_type, idx_params)
        return {
            "collection_name": collection_name,
            "status": "created"
        }

    def _as_dataclass_schema(self, dataclass_type: Any) -> List[FieldSchema]:
        """Defines fields for a Milvus collection based on dataclass attributes."""
        _fields = []
        for field in fields(dataclass_type):
            field_name = field.name
            field_type = field.type
            if field_type == str:
                size = getattr(field, 'metadata', {}).get('size', 65535)
                _fields.append(
                    FieldSchema(name=field_name, dtype=DataType.VARCHAR, max_length=size)
                )
            elif field_type == int:
                _fields.append(
                    FieldSchema(name=field_name, dtype=DataType.INT64)
                )
            elif field_type == float:
                _fields.append(FieldSchema(name=field_name, dtype=DataType.FLOAT))
            elif field_type == bytes:
                # Assume bytes field indicates a vector; specify dimension in metadata
                dim = getattr(field, 'metadata', {}).get('dim', 768)
                _fields.append(
                    FieldSchema(name=field_name, dtype=DataType.FLOAT_VECTOR, dim=dim)
                )
            elif field_type == bool:
                _fields.append(
                    FieldSchema(name=field_name, dtype=DataType.BOOL)
                )
            else:
                print(
                    f"Unsupported field type for dataclass field {field_name}: {field_type}"
                )
        return _fields

    async def _parse_avro_schema(self, avro_file: Path, dimension: int) -> List[FieldSchema]:
        """Parses an Avro schema file to define Milvus collection fields."""
        fields = []
        try:
            schema = parse_schema(open(avro_file, "r").read())
            for field in schema.fields:
                field_name = field.name
                field_type = field.type
                if field_type == "string":
                    fields.append(FieldSchema(name=field_name, dtype=DataType.VARCHAR, max_length=65535))
                elif field_type == "int" or field_type == "long":
                    fields.append(FieldSchema(name=field_name, dtype=DataType.INT64))
                elif field_type == "float" or field_type == "double":
                    fields.append(FieldSchema(name=field_name, dtype=DataType.FLOAT))
                elif field_type == "bytes":
                    fields.append(FieldSchema(name=field_name, dtype=DataType.FLOAT_VECTOR, dim=dimension))
                elif field_type == "boolean":
                    fields.append(FieldSchema(name=field_name, dtype=DataType.BOOL))
                else:
                    print(f"Unsupported field type: {field_type}")
        except Exception as e:
            print(f"Failed to parse Avro schema: {e}")
        return fields

    async def _create_milvus_collection(
        self,
        collection_name: str,
        schema: CollectionSchema,
        index_type: str,
        metric_type: str,
        idx_params: dict
    ):
        """Creates a collection with the given schema in Milvus."""
        index_params = {
            "index_type": index_type,
            "metric_type": metric_type,
            "params": idx_params
        }
        try:
            collection = Collection(
                name=collection_name,
                schema=schema,
                num_shards=2
            )
            collection.create_index(field_name="vector", index_params=index_params)
            self.logger.debug(
                f"Created collection '{collection_name}' with schema: {schema}"
            )
        except Exception as e:
            self.logger.error(
                f"Failed to create collection '{collection_name}': {e}"
            )
