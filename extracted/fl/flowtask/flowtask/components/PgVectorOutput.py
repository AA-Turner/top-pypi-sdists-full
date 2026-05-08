from collections.abc import Callable
import asyncio
from typing import List
from sqlalchemy import text
from parrot.stores.postgres import PgVectorStore
from parrot.stores.models import Document
from .flow import FlowComponent
from ..exceptions import DataNotFound, ComponentError, ConfigError
from ..conf import default_sqlalchemy_pg
from ..interfaces.credentials import CredentialsInterface


class PgVectorOutput(CredentialsInterface, FlowComponent):
    """
    Saving Parrot Documents on a Postgres Database using PgVector.

    This component is designed to save documents into a PostgreSQL database using PgVector extension
    with Parrot's vector store implementation (no Langchain dependency).

    Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PgVectorOutput:
          credentials:
          dsn:
          table: lg_products
          schema: lg
          embedding_model:
          model: thenlper/gte-base
          model_type: transformers
          id_column: "id"
          embedding_column: 'embedding'
          pk: source_type
          create_table: true
          upsert: true
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {
        "dsn": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.upsert: bool = kwargs.pop('upsert', True)
        pk = kwargs.pop('pk', 'source_type')
        self.pk: List[str] = pk if isinstance(pk, list) else [pk]
        self._embedding_model: dict = kwargs.get('embedding_model', None)
        self.embedding_column: str = kwargs.pop('embedding_column', kwargs.pop('vector_column', 'embedding'))
        self.table: str = kwargs.pop('table', 'documents')
        self.schema: str = kwargs.pop('schema', 'public')
        self.id_column: str = kwargs.pop('id_column', 'id')
        self.dimension: int = kwargs.pop('dimension', 768)
        self.create_table: bool = kwargs.pop('create_table', False)
        self.prepare_columns: bool = kwargs.pop('prepare_columns', True)
        self.document_column: str = kwargs.pop('document_column', 'document')
        self.metadata_column: str = kwargs.pop('metadata_column', 'cmetadata')
        self.text_column: str = kwargs.pop('text_column', 'text')
        # FEAT-127: contextual embedding headers (opt-in, per-store)
        self.contextual_embedding: bool = kwargs.pop('contextual_embedding', False)
        self.contextual_template = kwargs.pop('contextual_template', None)
        self.contextual_max_header_tokens: int = kwargs.pop(
            'contextual_max_header_tokens', 100
        )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        await super().start(**kwargs)
        self.processing_credentials()
        # DSN
        if not self.credentials:
            self._dsn = default_sqlalchemy_pg
        else:
            self._dsn = self.credentials.get('dsn', default_sqlalchemy_pg)
        if not self.data:
            raise DataNotFound(
                "List of Documents is Empty."
            )
        if not isinstance(self.data, list):
            raise ComponentError(
                f"Incompatible kind of data received, expected a *list* of documents, receives {type(self.data)}"
            )
        return True

    async def close(self):
        pass

    def _sanitize_documents(self, documents: List[Document]) -> List[Document]:
        """Strip null bytes from document content and metadata for PostgreSQL compatibility."""
        for doc in documents:
            if doc.page_content:
                doc.page_content = doc.page_content.replace('\x00', '')
            if doc.metadata:
                for key, value in doc.metadata.items():
                    if isinstance(value, str):
                        doc.metadata[key] = value.replace('\x00', '')
        return documents

    async def _create_collection(self, store: PgVectorStore):
        """
        Create the collection (table) in the PostgreSQL database using Parrot's method.
        """
        if not self.create_table:
            return
            
        if not await store.collection_exists(table=self.table, schema=self.schema):
            print(f"Creating collection {self.schema}.{self.table}...")
            
            # Use Parrot's create_collection method
            await store.create_collection(
                table=self.table,
                schema=self.schema,
                dimension=self.dimension,
                id_column=self.id_column,
                embedding_column=self.embedding_column,
                document_column=self.document_column,
                metadata_column=self.metadata_column
            )
            print(f"✅ Collection {self.schema}.{self.table} created successfully")

    _DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

    def _get_embedding_model_name(self, store: PgVectorStore) -> str:
        """Resolve the embedding model name from the store configuration."""
        if store.embedding_model and isinstance(store.embedding_model, dict):
            return store.embedding_model.get('model_name', self._DEFAULT_EMBEDDING_MODEL)
        # Fallback: check if the embed callable has a model name
        if store._embed_ and hasattr(store._embed_, 'model_name'):
            return store._embed_.model_name
        return self._DEFAULT_EMBEDDING_MODEL

    async def _ensure_embedding_model_column(self, store: PgVectorStore):
        """Add embedding_model column to the table if it doesn't exist."""
        async with store.session() as session:
            await session.execute(text(
                f"ALTER TABLE {self.schema}.{self.table} "
                f"ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(255)"
            ))

    async def _prepare_embedding_table(self, store: PgVectorStore):
        """
        Prepare the embedding table using Parrot's prepare_embedding_table method.
        """
        if not self.prepare_columns:
            return
            
        print(f"Preparing embedding table {self.schema}.{self.table}...")
        
        # Use Parrot's connection to prepare the table
        async with store.session() as session:
            await store.prepare_embedding_table(
                table=self.table,
                schema=self.schema,
                conn=session,
                embedding_column=self.embedding_column,
                document_column=self.document_column,
                metadata_column=self.metadata_column,
                text_column=self.text_column,
                id_column=self.id_column,
                dimension=self.dimension,
                create_all_indexes=True
            )
        print(f"✅ Embedding table {self.schema}.{self.table} prepared successfully")

    async def run(self):
        """
        Saving Parrot Documents on a Postgres Database using PgVector.
        """
        # Connecting to PostgreSQL using Parrot's PgVectorStore:
        store_kwargs = {
            "table": self.table,
            "schema": self.schema,
            "id_column": self.id_column,
            "embedding_column": self.embedding_column,
            "document_column": self.document_column,
            "text_column": self.text_column,
            "dsn": self._dsn,
            "dimension": self.dimension,
            "auto_initialize": True,
        }
        if self._embedding_model is not None:
            store_kwargs["embedding_model"] = self._embedding_model
        # FEAT-127: forward contextual-header config to the store so
        # add_documents() prepends the metadata-driven header before embed.
        if self.contextual_embedding:
            store_kwargs["contextual_embedding"] = True
            store_kwargs["contextual_max_header_tokens"] = (
                self.contextual_max_header_tokens
            )
            if self.contextual_template is not None:
                store_kwargs["contextual_template"] = self.contextual_template
        _store = PgVectorStore(**store_kwargs)
        
        self._result = None
        async with _store as store:
            print(f'Connecting to PostgreSQL... {store.is_connected()}')
            print(f"Processing table {self.schema}.{self.table}...")
            
            # Create collection if needed
            if self.create_table:
                await self._create_collection(store)
            
            # Prepare embedding columns if needed
            if self.prepare_columns:
                await self._prepare_embedding_table(store)
            
            # Resolve the embedding model name
            model_name = self._get_embedding_model_name(store)
            print(f"Embedding model: {model_name}")

            # Verify collection exists
            if await store.collection_exists(table=self.table, schema=self.schema):
                # Ensure embedding_model column exists
                await self._ensure_embedding_model_column(store)

                # If upsert: delete existing documents matching all pk fields
                if self.upsert and self.pk:
                    # Build filter from unique metadata values across all pk fields
                    filter_dict = {}
                    for key in self.pk:
                        values = list({
                            doc.metadata[key]
                            for doc in self.data
                            if doc.metadata and key in doc.metadata
                        })
                        if values:
                            filter_dict[key] = values if len(values) > 1 else values[0]
                    if filter_dict:
                        print(f"Upserting: deleting existing documents matching {filter_dict}")
                        deleted_count = await store.delete_documents_by_filter(
                            filter_dict=filter_dict,
                            table=self.table,
                            schema=self.schema,
                            metadata_column=self.metadata_column
                        )
                        print(f"Deleted {deleted_count} existing documents")

                # Sanitize null bytes before inserting
                self.data = self._sanitize_documents(self.data)
                # Add documents to the store
                print(f"Adding {len(self.data)} documents to vector store...")
                await store.add_documents(
                    documents=self.data,
                    table=self.table,
                    schema=self.schema,
                    embedding_column=self.embedding_column,
                    content_column=self.document_column,
                    metadata_column=self.metadata_column
                )

                # Stamp rows that have no embedding_model with the current model name
                async with store.session() as session:
                    await session.execute(
                        text(
                            f"UPDATE {self.schema}.{self.table} "
                            f"SET embedding_model = :model_name "
                            f"WHERE embedding_model IS NULL"
                        ),
                        {"model_name": model_name}
                    )

                result = {
                    "vectorstore": f"{store!r}",
                    "table": f"{self.schema}.{self.table}",
                    "documents_added": len(self.data),
                    "embedding_model": model_name,
                    "embedding_column": self.embedding_column,
                    "schema": self.schema
                }
                print(f"✅ Successfully added {len(self.data)} documents to {self.schema}.{self.table}")
            else:
                raise DataNotFound(
                    f"Collection {self.schema}.{self.table} does not exist and could not be created."
                )
            
            self._result = result
        
        self.add_metric('DOCUMENTS_LOADED', len(self.data))
        return result
