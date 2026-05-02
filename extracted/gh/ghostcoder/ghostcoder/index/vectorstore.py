import json
import logging
from pathlib import Path
from typing import List

from pydantic import Field, BaseModel

from ghostcoder import FileRepository
from ghostcoder.codeblocks import CodeBlock, CodeBlockType

logger = logging.getLogger(__name__)


class SearchHit(BaseModel):
    type: CodeBlockType = Field(description="Type of code block")
    file_path: str = Field(description="File path")
    block_path: List[str] = Field(description="Block path")
    contents: str = Field(description="Contents of the code block")
    score: float = Field(default=None, description="Score of the search hit")


class VectorStore:

    def __init__(self,
                 repository: str,
                 url: str):
        import weaviate

        auth_config = weaviate.AuthApiKey(api_key="YOUR-WEAVIATE-API-KEY")

        self._client = weaviate.Client(
            url=url,
            # auth_client_secret=auth_config,
            additional_headers={
                "X-OpenAI-Api-Key": "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",
            }
        )

        self._repository = repository

        # self._initiate_schema()

    def _initiate_schema(self):
        class_obj = {
            "class": "CodeBlock",
            "description": "A code block.",
            "vectorizer": "text2vec-openai",
            "properties": [
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "Type of code block",
                    "name": "type"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "Repository name",
                    "name": "repository"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "File path",
                    "name": "filePath"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "File extension",
                    "name": "fileExtension"
                },
                {
                    "dataType": [
                        "text[]"
                    ],
                    "description": "Block path",
                    "name": "blockPath"
                },
                {
                    "dataType": [
                        "text"
                    ],
                    "description": "Programming language",
                    "name": "programmingLanguage"
                }
            ]
        }

        self._client.schema.delete_all()
        self._client.schema.create_class(class_obj)

    def reset(self):
        result = self._client.batch.delete_objects(
            class_name="CodeBlock",
            where={
                "path": ["repository"],
                "operator": "Equal",
                "valueText": self._repository,
            },
        )

        logger.info(f"Deleted codeblocks from repository '{self._repository}' {result.get('results', {})}")

    def insert_blocks(self, blocks: List[CodeBlock]):
        with self._client.batch as batch:
            batch.configure(
                batch_size=50,
            )
            for block in blocks:
                contents = block.to_context_string(show_commented_out_code_comment=False)

                if contents.strip():
                    batch.add_data_object(
                        class_name="CodeBlock",
                        data_object={
                            "type": block.type,
                            "repository": self._repository,
                            "filePath": block.root().file_path,
                            "blockPath": block.full_path(),
                            "contents": contents,
                        }
                    )
            result = batch.create_objects()

            logger.info(f"Inserted {len(result)} codeblocks into repository '{self._repository}'")

    def search(self, query: str, limit: int = 10):
        response = (
            self._client.query.get("CodeBlock", ["type", "filePath", "blockPath", "contents"])
            .with_near_text({
                "concepts": [query]
            })
            .with_additional(["distance", "score"])
            .with_limit(limit)
            .with_where({
                "path": ["repository"],
                "operator": "Equal",
                "valueText": self._repository,
            })
            .do()
        )

        hits = []
        for result in response["data"]["Get"]["CodeBlock"]:
            print(result)
            hits.append(SearchHit(
                type=result["type"],
                file_path=result["filePath"],
                block_path=result["blockPath"],
                contents=result["contents"]
            ))

        return hits


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('httpx').setLevel(logging.WARN)
    logging.getLogger('openai').setLevel(logging.INFO)
    logging.getLogger('httpcore').setLevel(logging.INFO)
    repository = FileRepository(Path("/home/albert/repos/albert/bulletproof-react"), include_dirs=["src"])

    vector_store = VectorStore(
        url="https://ghostcoder-test-da9zaphm.weaviate.network", repository=repository.identifier)

    vector_store.search("find the user object")