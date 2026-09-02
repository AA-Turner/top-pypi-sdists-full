# type: ignore
"""Fake DataStore, DataTailor and Product that will be used when adding the --test
option in favour of the real implementations. Only useful for unittests."""

import io
from contextlib import contextmanager
from typing import Any, List


class FakeDataStore:
    """Fake DataStore for testing."""

    def get_collection(self, collection_id):
        """Return a FakeCollection with `collection_id`."""
        return FakeCollection(collection_id)

    def get_product(self, collection_id, product_id):
        """Return a FakeProduct with `product_id` from `collection_id`."""
        return FakeProduct(collection_id, product_id)


class FakeProduct:
    """FakeProduct for testing."""

    def __init__(self, collection_id, product_id):
        """Init from `collection_id` and `product_id`."""
        self._id = product_id
        self.collection = FakeCollection(collection_id)
        self.entries = ["entry1.nc", "entry2.nc"]

    def __str__(self):
        """Return the id as str representation"""
        return str(self._id)

    def open(self, entry=None, chunk=None, custom_headers=None):
        """Return a fake stream as the contents of the product."""
        if entry:
            return FakeStream(f"{self._id}-{entry}")

        return FakeStream(self._id)

    @property
    def md5(self):
        """Return the md5 of the fake stream returned on open."""
        import hashlib

        with self.open(None) as f:
            return hashlib.md5(f.read()).hexdigest()


class FakeStream:
    def __init__(self, name):
        self.decode_content = True
        self.name = name
        self.content = io.BytesIO(b"Content")

    def getheader(self, header):
        if header == "Content-Length":
            # Return a fixed length (7) for 'Content-Length' header.
            return 7
        return None

    def read(self, num=None):
        return self.content.read(num)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class FakeCollection:
    """Fake Collection for testing."""

    def __init__(self, collection_id):
        """Init from `collection_id`."""
        self._id = collection_id

    def __str__(self):
        """Return id as the str representation."""
        return str(self._id)

    def search(self, **query):
        """Return fake search results."""
        dtstart = query["dtstart"]
        dtend = query["dtend"]
        return [
            FakeProduct(self._id, f"prod_{dtstart.isoformat().strip().replace(':', '-')}"),
            FakeProduct(self._id, f"prod_{dtend.isoformat().strip().replace(':', '-')}"),
        ]


class FakeDataTailor:
    """Fake DataTailor for testing."""

    pass


class FakeInnerClient:
    def __init__(self, callbacks: List[Any], data: Any):
        self.data = data
        self.callbacks = callbacks

    def loop_forever(self) -> None:
        for d in self.data:
            for c in self.callbacks:
                c(self, None, d, None)


class FakeMessage:
    def __init__(self, payload: Any):
        self.payload = payload
        self.topic = None


class FakeMQTTClient:
    def __init__(self) -> None:
        self.data = [
            FakeMessage(
                '{"id": "9cd08674-38c6-4ec1-9ebc-5ba6fa5a6a5c", "version": "v04", "type": "Feature", "geometry": null, "properties": {"pubtime": "2025-03-24T17:35:48.345Z", "data_id": "EXTERNAL-MONITOR-INGEST-PRIORITY-0100-0100-20210401164500", "start_datetime": "2021-04-01T16:45:00Z", "end_datetime": "2021-04-01T16:45:00Z"}, "links": [{"href": "https://user.eumetsat.int/api-definitions/data-store-download-api", "rel": "canonical", "type": "text/html"}, {"href": "https://api.edl.ope.dac.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3A0655/products/EXTERNAL-MONITOR-INGEST-PRIORITY-0100-0100-20210401164500", "rel": "service", "type": "application/zip", "length": 119}, {"href": "https://api.edl.ope.dac.eumetsat.int/data/browse/1.0.0/collections/EO%3AEUM%3ADAT%3A0655/products/EXTERNAL-MONITOR-INGEST-PRIORITY-0100-0100-20210401164500?format=json", "rel": "related", "type": "application/json"}], "_eumetsat_product_information": {"parentIdentifier": "EO:EUM:DAT:0655", "platform": "MSG3", "productType": "MSGCLMK"}}'.encode()
            ),
            FakeMessage(
                '{"id": "c805c030-5f7b-4e3d-ade2-5ff831353d69", "version": "v04", "type": "Feature", "geometry": null, "properties": {"pubtime": "2025-03-24T17:35:48.462Z", "data_id": "EXTERNAL-MONITOR-INGEST-NORMAL-0100-0100-20210401164500", "start_datetime": "2021-04-01T16:45:00Z", "end_datetime": "2021-04-01T16:45:00Z"}, "links": [{"href": "https://user.eumetsat.int/api-definitions/data-store-download-api", "rel": "canonical", "type": "text/html"}, {"href": "https://api.edl.ope.dac.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3A0655/products/EXTERNAL-MONITOR-INGEST-NORMAL-0100-0100-20210401164500", "rel": "service", "type": "application/zip", "length": 119}, {"href": "https://api.edl.ope.dac.eumetsat.int/data/browse/1.0.0/collections/EO%3AEUM%3ADAT%3A0655/products/EXTERNAL-MONITOR-INGEST-NORMAL-0100-0100-20210401164500?format=json", "rel": "related", "type": "application/json"}], "_eumetsat_product_information": {"parentIdentifier": "EO:EUM:DAT:0655", "platform": "MSG3", "productType": "MSGCLMK"}}'.encode()
            ),
        ]
        self.callbacks: List[Any] = []

    def add_subscription(self, topic: str, qos: int) -> None:
        print(f"FakeMQTTClient add_subscription({topic}, {qos})")

    def connect(self) -> None:
        print("FakeMQTTClient connect()")

    def add_on_msg_callback(self, func: Any) -> None:
        self.callbacks.append(func)

    @property
    def client(self) -> FakeInnerClient:
        return FakeInnerClient(self.callbacks, self.data)
