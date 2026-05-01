import json
import os
import uuid

import ndjson
import pytest

from utf_queue_client.clients.data_lake_data_producer import (
    DataLakeDataProducer,
    DataLakeDataProducerFactory,
)


def test_data_lake_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = DataLakeDataProducer("dummy tenant")


@pytest.mark.parametrize("use_object_id", [True, False])
def test_data_lake_producer_central_queue(
    request,
    data_lake_tenant_key,
    csv_file_path,
    json_file_path,
    parquet_file_path,
    ndjson_file_path,
    amqp_url,
    queue_consumer,
    use_object_id,
):
    os.environ["UTF_PRODUCER_APP_ID"] = request.node.name
    producer = DataLakeDataProducerFactory.create_producer(
        data_lake_tenant_key, amqp_url
    )
    producer.publish_data_lake_csv_file(
        csv_file_path, object_id=str(uuid.uuid4()) if use_object_id else None
    )
    queue_consumer.expect_messages(1)
    producer.publish_data_lake_json_file(
        json_file_path, object_id=str(uuid.uuid4()) if use_object_id else None
    )
    queue_consumer.expect_messages(2)
    with open(json_file_path, "rb") as f:
        producer.publish_data_lake_json(json.load(f))
    producer.publish_data_lake_parquet_file(
        parquet_file_path, object_id=str(uuid.uuid4()) if use_object_id else None
    )
    queue_consumer.expect_messages(3)
    producer.publish_data_lake_ndjson_file(
        ndjson_file_path, object_id=str(uuid.uuid4()) if use_object_id else None
    )
    queue_consumer.expect_messages(4)
    with open(ndjson_file_path) as f:
        data = ndjson.load(f)
        producer.publish_data_lake_ndjson(
            data, object_id=str(uuid.uuid4()) if use_object_id else None
        )
    queue_consumer.expect_messages(5)
