import json
import logging
import os
import traceback
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_NONE
from typing import List, Optional, Dict, Tuple

import pymongo
import weaviate
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from llama_index import ServiceContext, StorageContext, load_index_from_storage, VectorStoreIndex, Document, \
    get_response_synthesizer, KnowledgeGraphIndex
from llama_index.constants import TYPE_KEY, DATA_KEY
from llama_index.indices.knowledge_graph import KGTableRetriever
from llama_index.indices.knowledge_graph.retrievers import KGRetrieverMode
from llama_index.ingestion import run_transformations
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import ResponseMode
from llama_index.schema import TextNode, MetadataMode, NodeRelationship
from llama_index.storage.docstore import SimpleDocumentStore, DocumentStore, MongoDocumentStore, BaseDocumentStore
from llama_index.storage.docstore.utils import json_to_doc
from llama_index.utils import get_tqdm_iterable
from llama_index.vector_stores import ChromaVectorStore, AzureCosmosDBMongoDBVectorSearch, CassandraVectorStore, \
    WeaviateVectorStore, SimpleVectorStore
from llama_index.vector_stores.types import VectorStore, ExactMatchFilter, MetadataFilters
from pydantic import BaseModel, Field

from ghostcoder.codeblocks import create_parser, CodeBlock
from ghostcoder.codeblocks.codeblocks import Relationship, ReferenceScope, CodeBlockType
from ghostcoder.filerepository import FileRepository
from ghostcoder.index.node_parser import CodeNodeParser
from ghostcoder.index.schema import CodeDocument, CodeNode
from ghostcoder.schema import FileItem, Folder
from ghostcoder.utils import count_tokens


class BlockSearchHit(BaseModel):
    score: float = Field(default=0, description="The similarity score of the block.")
    identifier: str = Field(default=None, description="The identifier of the block.")
    content: str = Field(description="The content of the block.")


class FileSearchHit(BaseModel):
    path: str = Field(description="The path of the file.")
    content_type: str = Field(description="The type of the document.")
    blocks: List[BlockSearchHit] = Field(description="The blocks of the file.")


def create_default_vector_store(index_dir: str):
    import chromadb
    from chromadb.config import Settings

    db = chromadb.PersistentClient(path=index_dir + "/.chroma_db", settings=Settings(anonymized_telemetry=False))
    chroma_collection = db.get_or_create_collection("code-index")
    return ChromaVectorStore(chroma_collection=chroma_collection)


def insert_into_tree(node, path):
    if not path:
        return
    if path[0] not in node:
        node[path[0]] = {}
    insert_into_tree(node[path[0]], path[1:])


def build_tree(tree: dict, references: List[Relationship], default_external_path: str):

    for ref in references:
        if ref is None:
            continue

        if ref.scope == ReferenceScope.EXTERNAL:
            external_path = "/".join(ref.external_path)
        else:
            external_path = default_external_path

        if external_path not in tree:
            tree[external_path] = {}
        insert_into_tree(tree[external_path], ref.path)

    return tree


def deep_merge(dict1, dict2):
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                deep_merge(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]

class CodeIndex:

    def __init__(self,
                 repository: FileRepository,
                 index_dir: str = None,
                 docstore: Optional[BaseDocumentStore] = None,
                 vector_store: Optional[VectorStore] = None):
        self.repository = repository
        self.index_dir = index_dir or str(self.repository.repo_path / ".index")
        self.docstore = docstore or SimpleDocumentStore()
        self.vector_store = vector_store or SimpleVectorStore()

        node_parser = CodeNodeParser.from_defaults(include_metadata=False)
        self.service_context = ServiceContext.from_defaults(node_parser=node_parser)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store, docstore=self.docstore)

        self._vector_index = VectorStoreIndex(nodes=[],
                                              service_context=self.service_context,
                                              storage_context=self.storage_context,
                                              show_progress=True)

    def initiate_index(self):
        documents = self._read_documents(parse_block=True)

        logging.info(f"Creating new index with {len(documents)} documents...")

        if not self.docstore:
            self.docstore = SimpleDocumentStore()

        storage_context = StorageContext.from_defaults(vector_store=self.vector_store, docstore=self.docstore)

        self.docstore.add_documents(documents)

        nodes = run_transformations(
            documents,  # type: ignore
            self.service_context.transformations,
            show_progress=True
        )

        self._vector_index = VectorStoreIndex(nodes=nodes,
                                              service_context=self.service_context,
                                              storage_context=storage_context,
                                              show_progress=True)

        #self._knowledge_graph = CodeKnowledgeGraph(nodes=nodes,
        #                                           service_context=self.service_context,
        #                                           storage_context=storage_context,
        #                                           show_progress=True)

        if self.index_dir:
            self._vector_index.storage_context.persist(persist_dir=self.index_dir)
            logging.info("New index created and persisted to storage.")

    def refresh(self):
        documents = self._read_documents()

        docs_to_refresh = []
        for document in documents:
            existing_doc = self.get_code_document(document.get_doc_id())
            if existing_doc is None:
                logging.debug(f"Will add document {document.get_doc_id()}")
                docs_to_refresh.append((existing_doc, document))
            elif existing_doc.hash != document.hash:
                logging.debug(f"Will refreshing document {document.get_doc_id()}, "
                              f"new hash {document.hash} != existing hash {existing_doc.hash}")
                docs_to_refresh.append((existing_doc, document))

        docs_with_progress = get_tqdm_iterable(
            docs_to_refresh, True, "Refreshing documents"
        )

        for (existing_doc, document) in docs_with_progress:
            codeblock = self.create_block(document.get_doc_id(), document.text, document.metadata.get("language"))
            if codeblock:
                document = CodeDocument(text=document.text, codeblock=codeblock, metadata=document.metadata, id_=document.id_)

            if existing_doc:
                self._vector_index.update_ref_doc(document)
            else:
                self._vector_index.insert(document)

            self.docstore.add_documents([document])

    def _index_documents(self):
        filetree = self.repository.file_tree()

    def traverse(self, folder: Folder):
        files = []

        for node in folder.children:
            if node.type == "folder":



                files.extend(node.traverse())
            else:
                files.append(node)
        return files


    def _read_documents(self, parse_block: bool = False):
        documents = []

        files = self.repository.file_tree().traverse()

        files_with_progress = get_tqdm_iterable(
            files, True, "Read documents"
        )

        for file in files_with_progress:
            file_item = self.repository.get_file(file.path)
            file_split = file_item.file_path.split("/")[-1].split(".")
            if len(file_split) > 1:
                file_extension = file_split[-1]
            else:
                file_extension = ""
            metadata = {
                "repository": self.repository.identifier,
                "file_path": file.path,
                "file_extension": file_extension
            }

            if file.language:
                metadata["language"] = file.language

            codeblock = None
            if parse_block:
                codeblock = self.create_block(file.path, file_item.content, file.language)

            doc_id = f"{self.repository.identifier}:{file.path}"

            if codeblock:
                doc = CodeDocument(id_=doc_id, text=file_item.content, codeblock=codeblock, metadata=metadata)
            else:
                doc = Document(id_=doc_id, text=file_item.content, metadata=metadata)

            documents.append(doc)

        return documents

    def add_to_index(self, sub_tree: dict, path: List[str], codeblock: CodeBlock):
        if len(path) == 1:
            sub_tree[path[0]] = codeblock
        elif len(path) > 1:
            if path[0] not in sub_tree:
                sub_tree[path[0]] = {}

            self.add_to_index(sub_tree[path[0]], path[1:], codeblock)

    def create_block(self, file_path: str, contents: str, language: Optional[str]) -> Optional[CodeBlock]:
        if not language:
            return None

        try:
            parser = create_parser(language)
        except Exception as e:
            logging.warning(
                f"Could not get parser for language {language}. "
                f"Will not parse document {file_path}. Error: {e}")
            return None

        try:
            return parser.parse(contents, file_path)
        except Exception as e:
            traceback.print_exc()
            logging.warning(
                f"Failed to parse {file_path}. Error: {e}")
            return None

    def search(self, query: str, filter_values: dict = {}, limit: int = 20):
        logging.debug(f"Searching for {query}...")

        filters = []
        for key, sub_tree in filter_values.items():
            filters.append(ExactMatchFilter(key=key, value=sub_tree))

        filters.append(ExactMatchFilter(key="repository", value=self.repository.identifier))

        vector_retriever = self._vector_index.as_retriever(similarity_top_k=limit, filters=MetadataFilters(filters=filters))
        #kg_retriever = KGTableRetriever(
        #    index=self._knowledge_graph, retriever_mode=KGRetrieverMode.KEYWORD, include_text=False)

        nodes = vector_retriever.retrieve(query)
        #kg_nodes = kg_retriever.retrieve(query)

        #vector_ids = {n.node.node_id for n in vector_nodes}
        #kg_ids = {n.node.node_id for n in kg_nodes}

        #combined_dict = {n.node.node_id: n for n in vector_nodes}
        #combined_dict.update({n.node.node_id: n for n in kg_nodes})

        #retrieve_ids = vector_ids.union(kg_ids)
        #nodes = [combined_dict[rid] for rid in retrieve_ids]

        logging.info(f"Got {len(nodes)} hits")

        hits = self.generate_response(nodes)

        return hits

    def generate_response(self, nodes: List, depth: int = 0) -> List[FileItem]:
        items: Dict[str, Tuple[CodeBlock, Dict, int, FileItem]] = {}
        exclude_types = [CodeBlockType.FUNCTION, CodeBlockType.CLASS, CodeBlockType.TEST_SUITE, CodeBlockType.TEST_CASE]

        for node in nodes:
            source = node.node.source_node
            if not source:
                continue

            if source.node_id not in items:
                codedoc = self.get_code_document(source.node_id)
                if codedoc is None or not isinstance(codedoc, CodeDocument):
                    continue
                items[source.node_id] = (codedoc.codeblock, {}, 0, None)

            if node.node.metadata.get("block_path"):
                block_path = node.node.metadata.get("block_path").split("/")  # TODO: Change "/" to "."
                insert_into_tree(items[source.node_id][1], block_path)

            content = items[source.node_id][0]._to_context_string(path_tree=items[source.node_id][1], exclude_types=exclude_types)

            tokens = count_tokens(content)
            items[source.node_id] = (items[source.node_id][0], items[source.node_id][1], tokens, FileItem(path=node.node.metadata.get("file_path"), content=content))

            sum_tokens = sum([item[2] for item in items.values()])
            print(f"add {codedoc.id_} {block_path}, {items[source.node_id][1]} sum_tokens: {sum_tokens}")

        for node in nodes:
            source = node.node.source_node
            if not source:
                continue

            if not node.node.metadata.get("block_path"):
                logging.warning(f"Node {node.node_id} in {source.node_id} has no block_path.")
                continue

            block_path = node.node.metadata.get("block_path").split("/")  # TODO: Change "/" to "."
            codeblock = items[source.node_id][0].find_by_path(block_path)

            path_tree = codeblock.build_reference_tree()
            deep_merge(items[source.node_id][1], path_tree)
            print(items[source.node_id][1])

            content = items[source.node_id][0]._to_context_string(path_tree=items[source.node_id][1], exclude_types=exclude_types)

            tokens = count_tokens(content)
            items[source.node_id] = (items[source.node_id][0], items[source.node_id][1], tokens, FileItem(path=node.node.metadata.get("file_path"), content=content))

            sum_tokens = sum([item[2] for item in items.values()])
            print(f"update {block_path}, sum_tokens: {sum_tokens}")

        return [item[3] for item in items.values()]

    def ask(self, query: str):
        #template = QuestionAnswerPrompt(DEFAULT_TEXT_QA_PROMPT_TMPL)
        response_synthesizer = get_response_synthesizer(
            response_mode=ResponseMode.COMPACT,
            #text_qa_template=template
        )
        retriever = self._vector_index.as_retriever(similarity_top_k=20)

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
         #   node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        )
        #query_engine = self._index.as_query_engine()
        response = query_engine.query(query)
        return response

    # TODO: Move to extended llamaindex
    def get_code_document(self, doc_id: str):
        json = self.docstore._kvstore.get(doc_id, collection="docstore")
        if json is None:
            logging.warning(f"doc_id {doc_id} not found.")
            return None

        doc_type = json[TYPE_KEY]
        data_dict = json[DATA_KEY]
        if doc_type == CodeDocument.get_type():
            return CodeDocument.parse_obj(data_dict)

        return json_to_doc(json)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('httpx').setLevel(logging.WARN)
    logging.getLogger('openai').setLevel(logging.INFO)
    logging.getLogger('httpcore').setLevel(logging.INFO)

    repository = FileRepository(Path("/home/albert/repos/albert/ghostcoder"), exclude_dirs=["tests", "playground", "benchmark"])
    uri = "mongodb://ghostcoder:CK5tVOlRJlltB4XRKpZ8CJTsDHQyQ5DatY49qljpBqWLOWzS30ZDsHScD9VhK38JSnZ1wl5YZ0B8ACDbpW9XXQ==@ghostcoder.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ghostcoder@"

    docstore = MongoDocumentStore.from_uri(uri, "ghostcoder-dev", "docstore")
    docstore._node_collection = "docstore"
    docstore._metadata_collection = "metadata"

    auth_config = weaviate.AuthApiKey(api_key="YOUR-WEAVIATE-API-KEY")

    client = weaviate.Client(
        url="https://ghostcoder-test-da9zaphm.weaviate.network",
        #auth_client_secret=auth_config
    )

    result = client.batch.delete_objects(
        class_name="LlamaIndex",
        where={
            "path": ["repository"],
            "operator": "Equal",
            "valueText": repository.identifier
        },
    )

    #print(result)

    vector_store = WeaviateVectorStore(
        weaviate_client=client, index_name="LlamaIndex"
    )

    index = CodeIndex(repository=repository,
                      index_dir="/home/albert/repos/albert/ghostcoder/.index",
                      vector_store=vector_store,
                      docstore=docstore)

    index.initiate_index()

    hits = index.search("Update all parsers with a new field?")

    for hit in hits:
        print("Filepath: ", hit.file_path)
        print(hit.content)
