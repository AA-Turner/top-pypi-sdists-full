from typing import Optional, Type
import hashlib
import json
from urllib.parse import urlparse, quote
from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger, storage_accounts

storage_account = storage_accounts.get("main") if storage_accounts else None
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class SourceDocument:
    def __init__(
        self,
        content: str,
        source: str,
        id: Optional[str] = None,
        title: Optional[str] = None,
        chunk: Optional[int] = None,
        offset: Optional[int] = None,
        page_number: Optional[int] = None,
        chunk_id: Optional[str] = None,
    ):
        self.id = id
        self.content = content
        self.source = source
        self.title = title
        self.chunk = chunk
        self.offset = offset
        self.page_number = page_number
        self.chunk_id = chunk_id
        logger.debug(
            f"SourceDocument initialized with id: {self.id}, source: {self.source}"
        )

    def __str__(self):
        return f"SourceDocument(id={self.id}, title={self.title}, source={self.source}, chunk={self.chunk}, offset={self.offset}, page_number={self.page_number}, chunk_id={self.chunk_id})"

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.id == other.id
                and self.content == other.content
                and self.source == other.source
                and self.title == other.title
                and self.chunk == other.chunk
                and self.offset == other.offset
                and self.page_number == other.page_number
                and self.chunk_id == other.chunk_id
            )
        return False

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def to_json(self):
        json_string = json.dumps(self, cls=SourceDocumentEncoder)
        logger.debug(f"Serialized SourceDocument to JSON: {json_string}")
        return json_string

    @classmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def from_json(cls, json_string):
        source_document = json.loads(json_string, cls=SourceDocumentDecoder)
        return source_document

    @classmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def from_dict(cls, dict_obj):
        logger.debug(f"Creating SourceDocument from dict: {dict_obj}")
        return cls(
            dict_obj["id"],
            dict_obj["content"],
            dict_obj["source"],
            dict_obj["title"],
            dict_obj["chunk"],
            dict_obj["offset"],
            dict_obj["page_number"],
            dict_obj["chunk_id"],
        )

    @classmethod
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def from_metadata(
        cls: Type["SourceDocument"],
        content: str,
        metadata: dict,
        document_url: Optional[str],
        idx: Optional[int],
    ) -> "SourceDocument":
        logger.debug(
            f"Creating SourceDocument from metadata. document_url:{document_url}, metadata:{metadata}"
        )
        parsed_url = urlparse(document_url)
        file_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        filename = parsed_url.path
        hash_key = hashlib.sha1(f"{file_url}_{idx}".encode("utf-8")).hexdigest()
        hash_key = f"doc_{hash_key}"
        sas_placeholder = (
            "_SAS_TOKEN_PLACEHOLDER_"
            if parsed_url.netloc
            and parsed_url.netloc.endswith(".blob.core.windows.net")
            else ""
        )
        source_document = cls(
            id=metadata.get("id", hash_key),
            content=content,
            source=metadata.get("source", f"{file_url}{sas_placeholder}"),
            title=metadata.get("title", filename),
            chunk=metadata.get("chunk", idx),
            offset=metadata.get("offset"),
            page_number=metadata.get("page_number"),
            chunk_id=metadata.get("chunk_id"),
        )
        return source_document

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_filename(self, include_path=False):
        filename = self.source.replace("_SAS_TOKEN_PLACEHOLDER_", "").replace(
            "http://", ""
        )
        if include_path:
            filename = filename.split("/")[-1]
        else:
            filename = filename.split("/")[-1].split(".")[0]
        logger.debug(
            f"Extracted filename: {filename}, include_path: {include_path}"
        )
        return filename

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_markdown_url(self):
        url = quote(self.source, safe=":/")
        if "_SAS_TOKEN_PLACEHOLDER_" in url:
            if not storage_account:
                logger.warning("Storage account not configured. Cannot generate container SAS for markdown URL.")
                container_sas = ""
            else:
                try:
                    # Generate container SAS using storage_account from mgmt_config
                    container_sas = "?" + storage_account.get_container_sas(
                        container_name=env_helper.AZURE_BLOB_CONTAINER_NAME,
                        permission="r"
                    )
                except Exception as e:
                    logger.error(f"Failed to generate container SAS: {e}")
                    container_sas = ""
            url = url.replace("_SAS_TOKEN_PLACEHOLDER_", container_sas)
        logger.debug(f"Generated markdown URL: {url}")
        return f"[{self.title}]({url})"


class SourceDocumentEncoder(json.JSONEncoder):
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def default(self, obj):
        if isinstance(obj, SourceDocument):
            logger.debug(f"Encoding SourceDocument: {obj}")
            return {
                "id": obj.id,
                "content": obj.content,
                "source": obj.source,
                "title": obj.title,
                "chunk": obj.chunk,
                "offset": obj.offset,
                "page_number": obj.page_number,
                "chunk_id": obj.chunk_id,
            }
        return super().default(obj)


class SourceDocumentDecoder(json.JSONDecoder):
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def decode(self, s, **kwargs):
        logger.debug(f"Decoding JSON string: {s}")
        obj = super().decode(s, **kwargs)
        source_document = SourceDocument(
            id=obj["id"],
            content=obj["content"],
            source=obj["source"],
            title=obj["title"],
            chunk=obj["chunk"],
            offset=obj["offset"],
            page_number=obj["page_number"],
            chunk_id=obj["chunk_id"],
        )
        return source_document
