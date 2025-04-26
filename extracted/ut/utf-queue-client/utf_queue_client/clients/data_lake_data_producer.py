import base64
import gzip
import json
import os
from datetime import datetime
from io import BytesIO
from socket import gethostname
from typing import List, Optional, Tuple, Union
from uuid import uuid4

import ndjson
from otel_extensions import instrumented

from ..models import DataLakeData, QueueMessage
from . import Loggable
from .base_producer import BlockingProducer

__all__ = ["DataLakeDataProducer", "DataLakeDataProducerFactory"]


class DataLakeDataProducer:
    def __init__(self, tenant_key: str, url=None, producer_app_id: str = None):
        self.queue_name = "default"
        self.__client = BlockingProducer(url, producer_app_id)
        self.__client.queue_declare(queue=self.queue_name, durable=True)
        self.tenant_key = tenant_key

    @instrumented
    def publish_data_lake_csv_file(self, file_path: str, object_id: str = None):
        with open(file_path, "rb") as f:
            csv_data = f.read()
            self.publish_data_lake_csv(csv_data, object_id=object_id)

    @instrumented
    def publish_data_lake_csv(self, csv_data: bytes, object_id: str = None):
        serialized_data, compression = self._serialize_data(csv_data)
        self.publish_data_lake_data(
            "CSV", serialized_data, compression, object_id=object_id
        )

    @instrumented
    def publish_data_lake_json_file(self, file_path: str, object_id: str = None):
        with open(file_path, "rb") as f:
            json_data = json.load(f)
            self.publish_data_lake_data("JSON", json_data, object_id=object_id)

    @instrumented
    def publish_data_lake_json(self, json_data: dict, object_id: str = None):
        self.publish_data_lake_data("JSON", json_data, object_id=object_id)

    @instrumented
    def publish_data_lake_ndjson_file(self, file_path: str, object_id: str = None):
        with open(file_path) as f:
            ndjson_data = ndjson.load(f)
            self.publish_data_lake_ndjson(ndjson_data, object_id=object_id)

    @instrumented
    def publish_data_lake_ndjson(self, ndjson_data: List[dict], object_id: str = None):
        self.publish_data_lake_data("NDJSON", ndjson_data, object_id=object_id)

    @instrumented
    def publish_data_lake_parquet_file(self, file_path: str, object_id: str = None):
        with open(file_path, "rb") as f:
            serialized_data, compression = self._serialize_data(f.read())
            self.publish_data_lake_data(
                "PARQUET", serialized_data, compression, object_id=object_id
            )

    @instrumented
    def publish_data_lake_data(
        self,
        data_format: str,
        data_lake_data: Union[str, dict, List[dict]],
        compression: Optional[str] = None,
        object_id: str = None,
    ):
        payload = DataLakeData(
            dataFormat=data_format,
            data=data_lake_data,
            compression=compression or "NONE",
        )
        if object_id is not None:
            payload.object_id = object_id
        self._publish_data_lake_data_payload(payload)

    @instrumented
    def _publish_data_lake_data_payload(self, data_lake_payload: DataLakeData):
        queue_message = QueueMessage(
            payload=data_lake_payload,
            recordType="DATALAKE_DATA",
            tenantKey=self.tenant_key,
            recordTimestamp=datetime.now().isoformat(),
            messageId=str(uuid4()),
        )
        self.__client.publish(
            exchange="",
            routing_key=self.queue_name,
            payload=queue_message.as_dict(),
            persistent=True,
        )

    @instrumented
    def _serialize_data(self, data_bytes: bytes) -> Tuple[str, str]:
        compression = None
        serialized_data = data_bytes
        if len(data_bytes) > 128:
            compression = "GZIP"
            compressed_data = BytesIO()
            with gzip.GzipFile(fileobj=compressed_data, mode="w") as gzip_stream:
                gzip_stream.write(serialized_data)
            serialized_data = compressed_data.getvalue()
        serialized_data = base64.b64encode(serialized_data).decode("utf-8")
        return serialized_data, compression


class DataLakeDataProducerFactory(Loggable):
    @classmethod
    def create_producer(cls, tenant_key: str, url=None, producer_app_id: str = None):
        if url is None:
            url = os.environ.get(
                "UTF_QUEUE_SERVER_URL", "amqp://guest:guest@localhost:5672/%2f"
            )
        if producer_app_id is None:
            producer_app_id = os.environ.get(
                "UTF_PRODUCER_APP_ID", f"Local DataLakeDataProducer at {gethostname()}"
            )

        try:
            return DataLakeDataProducer(
                tenant_key=tenant_key,
                url=url,
                producer_app_id=producer_app_id,
            )
        except ConnectionError as e:
            cls.logger.warning(f"Unable to connect to queue server: {repr(e)}")
            raise
