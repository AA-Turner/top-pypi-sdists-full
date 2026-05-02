import json
import logging
import uuid
from typing import List

from azure.cosmos import CosmosClient, PartitionKey

from ghostcoder.codeblocks import CodeBlock
from ghostcoder.codeblocks.parser.python import PythonParser

logger = logging.getLogger(__name__)

class DocumentStore:

    def __init__(self,
                 endpoint: str,
                 key: str,
                 repository: str,
                 database_name: str = "ghostcoder"):
        client = CosmosClient(endpoint, key)

        container_name = "codeblocks"

        self._repository = repository

        indexing_policy = {
            "indexingMode": "consistent",
            "automatic": True,
            "includedPaths": [
                {
                    "path": "/repository/?"
                },
                {
                    "path": "/file_path/?"
                },
                {
                    "path": "/*"
                }
            ]
        }

        database = client.create_database_if_not_exists(id=database_name, offer_throughput=1000)
        self._container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/repository"),
            indexing_policy=indexing_policy
        )

    def upsert_codeblock(self, codeblock: CodeBlock):
        if not codeblock.file_path:
            logger.error(f"Codeblock missing file_path: {codeblock}")
            return

        logger.debug(f"Upsert codeblock [{self._repository}:{codeblock.file_path}]")

        query = f"SELECT c.id FROM c WHERE c.repository = '{self._repository}' AND c.file_path = '{codeblock.file_path}'"
        items = list(self._container.query_items(query=query))
        codeblock_dict = codeblock.dict()
        codeblock_dict["repository"] = self._repository
        codeblock_dict["file_path"] = codeblock.file_path

        if items:
            existing_id = items[0]['id']
            codeblock_dict = codeblock.dict()
            codeblock_dict["id"] = existing_id
            self._container.upsert_item(codeblock_dict)
            logger.debug(f"Codeblock with ID {codeblock_dict['id']} updated")
        else:
            codeblock_dict["id"] = str(uuid.uuid4())
            self._container.create_item(codeblock_dict)
            logger.debug(f"Codeblock with ID {codeblock_dict['id']} created")

    def read_codeblock(self, file_path: str) -> CodeBlock:
        query = f"SELECT * FROM c WHERE c.repository = '{self._repository}' AND c.file_path = '{file_path}'"
        items = list(self._container.query_items(query=query))

        if not items:
            logger.error(f"No codeblock found for {file_path}")
            return None

        codeblock_dict = items[0]
        return CodeBlock(**codeblock_dict)

    def read_all_codeblocks(self) -> List[CodeBlock]:
        query = f"SELECT * FROM c WHERE c.repository = '{self._repository}'"
        items = self._container.query_items(query=query)
        return [CodeBlock(**item) for item in items]

    def reset(self):
        query = f"SELECT * FROM c WHERE c.repository = '{self._repository}'"
        items = list(self._container.query_items(query=query))

        for item in items:
            self._container.delete_item(item, partition_key=item['repository'])
            logger.debug(f"Deleted codeblock with ID {item['id']} from repository '{self._repository}'")

        logger.info(f"Deleted {len(items)} codeblocks from repository '{self._repository}'")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('httpx').setLevel(logging.WARN)
    logging.getLogger('openai').setLevel(logging.INFO)
    logging.getLogger('httpcore').setLevel(logging.INFO)
    logging.getLogger('neo4j').setLevel(logging.INFO)

    _doc_store = DocumentStore(
        endpoint="https://ghostcoder-dev.documents.azure.com:443/",
        key="HFKwl1DL4tmc4zIEGxJHJrbdX3pNodCw9GNhkHewKgDs6YM17P9XMLAiXbnMTANdpouOfOr6KpcPACDbskVG6g==",
        repository="test"
    )

    parser = PythonParser()
    with open("documentstore.py", "r") as f:
        codeblock = parser.parse(f.read())
        _doc_store.upsert_codeblock("documentstore.py", codeblock)
