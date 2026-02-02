"""Blob store backed by a relational database."""

from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import re
import urllib.parse
from collections.abc import Iterator
from typing import Any, Literal

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm


class ORMBase(sa_orm.DeclarativeBase):
    """Base class for all ORMs in this module."""


class ORMBucket(ORMBase):
    """Blobs exist inside of buckets."""

    __tablename__ = "bucket"

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, primary_key=True)
    blobs: sa_orm.Mapped[list[ORMBlob]] = sa_orm.relationship(
        back_populates="bucket", cascade="all, delete-orphan"
    )


class ORMBlob(ORMBase):
    """Blobs are binary data with metadata."""

    __tablename__ = "blob"

    bucket_name: sa_orm.Mapped[str] = sa_orm.mapped_column(
        sa.ForeignKey("bucket.name", ondelete="CASCADE"), primary_key=True
    )
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, primary_key=True)
    data: sa_orm.Mapped[bytes] = sa_orm.mapped_column(sa.LargeBinary)
    content_type: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    meta_data: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.String)
    md5: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.CHAR(32))
    size: sa_orm.Mapped[int] = sa_orm.mapped_column()
    bucket: sa_orm.Mapped[ORMBucket] = sa_orm.relationship(back_populates="blobs")


def _url_to_bucket_obj_name(url: str) -> tuple[str, str]:
    match = re.match(r"gs://([^/]+)/(.*)", url)
    if not match:
        raise ValueError("URL was malformed")

    if not match.group(1):
        raise ValueError("Bucket cannot be empty")

    if not match.group(2):
        raise ValueError("Object name cannot be empty")

    bucket = match.group(1)
    obj_name = match.group(2)

    return bucket, obj_name


class RDBMSBlob:
    """Maps the blob interface to the RDBMS."""

    _bucket: RDBMSBucket
    _name: str
    _metadata: dict[str, Any]
    _content_type: str
    _md5_hash: str | None
    _size: int | None

    def __init__(self, bucket: RDBMSBucket, name: str):
        self._bucket = bucket
        self._name = name
        self._metadata = {}
        self._content_type = ""
        self._md5_hash = None
        self._size = None

    @property
    def client(self):
        return self._bucket.client

    @property
    def name(self) -> str:
        return self._name

    @property
    def physical_name(self) -> str:
        return self._name

    @property
    def bucket(self):
        return self._bucket

    @property
    def size(self) -> int | None:
        return self._size

    @property
    def md5_hash(self) -> str | None:
        return self._md5_hash

    def _to_orm(self, session: sa_orm.Session) -> ORMBlob | None:
        return session.get(ORMBlob, (self._bucket.name, self.name))

    def _dump_metadata(self) -> str:
        return json.dumps(self._metadata or {})

    def _load_metadata(self, serialized: str) -> None:
        self._metadata = json.loads(serialized) or {}

    @property
    def metadata(self) -> dict[str, Any]:
        return copy.deepcopy(self._metadata)

    @metadata.setter
    def metadata(self, value: dict[str, Any]) -> None:
        self._metadata.update(value)

    @property
    def content_type(self) -> str:
        return self._content_type

    @content_type.setter
    def content_type(self, value: str) -> None:
        self._content_type = value

    def patch(self) -> None:
        new_metadata = self.metadata
        with self.client.db_session() as session:
            orm_self = self._to_orm(session)
            if not orm_self:
                raise ValueError("object was not found")
            if new_metadata:
                old_metadata = json.loads(orm_self.meta_data) or dict[str, Any]()
                old_metadata.update(new_metadata)
                orm_self.meta_data = json.dumps(old_metadata)
            if self.content_type:
                orm_self.content_type = self.content_type
            orm_self.content_type = self._content_type
            session.commit()

    def reload(self) -> None:
        with self.client.db_session() as session:
            orm_self = self._to_orm(session)
            if orm_self:
                self._load_metadata(orm_self.meta_data)
                self._content_type = orm_self.content_type
                self._md5_hash = orm_self.md5
                self._size = orm_self.size
            else:
                raise ValueError("object was not found")

    def exists(self) -> bool:
        with self.client.db_session() as new_session:
            return bool(self._to_orm(new_session))

    def create_resumable_upload_session(
        self, content_type: str, origin: str | None = None, size: int | None = None
    ) -> str:
        if content_type:
            self._content_type = content_type

        with self.client.db_session() as session:
            self._set_content(new_content=b"", session=session)
            session.commit()
            return self.client.bucket_blob_to_upload_url(self._bucket.name, self.name)

    @property
    def url(self) -> str:
        return f"gs://{self._bucket.name}/{self.name}"

    def _get_content(self, session: sa_orm.Session) -> bytes:
        orm_self = self._to_orm(session)
        if orm_self:
            return orm_self.data
        raise ValueError("object was not found")

    def _set_content(self, new_content: bytes, session: sa_orm.Session) -> None:
        orm_self = self._to_orm(session)
        if not orm_self:
            orm_self = ORMBlob(
                bucket_name=self._bucket.name,
                name=self.name,
                meta_data=self._dump_metadata(),
            )
            session.add(orm_self)
        orm_self.data = new_content
        orm_self.content_type = self.content_type
        orm_self.md5 = hashlib.md5(new_content).hexdigest()
        orm_self.size = len(new_content)

    @contextlib.contextmanager
    def open(
        self, mode: Literal["rb", "wb"] = "rb", **kwargs: Any
    ) -> Iterator[io.BytesIO]:
        """Unlike the google.cloud.storage this *must* be used in a with clause."""
        with self.client.db_session() as session:
            if not self._bucket.exists_impl(session=session):
                raise ValueError("bucket does not exist")

            content_type = kwargs.get("content_type", "")

            match mode:
                case "rb":
                    if content_type:
                        raise ValueError("cannot set content_type on read operation")
                    yield io.BytesIO(self._get_content(session=session))
                case "wb":
                    stream = io.BytesIO()
                    self._content_type = content_type
                    yield stream
                    self._set_content(stream.getvalue(), session=session)
            session.commit()

    def delete(self) -> None:
        with self.client.db_session() as session:
            orm_self = self._to_orm(session)
            if not orm_self:
                raise ValueError("blob does not exist")
            session.delete(orm_self)
            session.commit()

    def upload_from_string(
        self, data: bytes | str, content_type: str = "text/plain"
    ) -> None:
        if isinstance(data, str):
            data = data.encode("utf-8")

        with self.open("wb", content_type=content_type) as stream:
            stream.write(data)

    def generate_signed_url(self, expiration: int) -> str:
        return f"http://{self._bucket.name}/{self.name}"


class RDBMSBucket:
    """Maps the bucket interface to the RDBMS."""

    _client: RDBMSBlobClient
    _name: str

    def __init__(self, client: RDBMSBlobClient, name: str):
        self._client = client
        self._name = name

    def _to_orm(self, session: sa_orm.Session) -> ORMBucket | None:
        return session.get(ORMBucket, self._name)

    @property
    def client(self):
        return self._client

    @property
    def name(self) -> str:
        return self._name

    def blob(self, name: str) -> RDBMSBlob:
        return RDBMSBlob(name=name, bucket=self)

    def exists_impl(self, session: sa_orm.Session) -> bool:
        return bool(self._to_orm(session))

    def exists(self) -> bool:
        with self._client.db_session() as session:
            return self.exists_impl(session)

    def create(self) -> None:
        with self._client.db_session() as session:
            session.add(ORMBucket(name=self._name))
            session.commit()

    def list_blobs(self) -> Iterator[RDBMSBlob]:
        def get_blobs():
            with self._client.db_session() as session:
                orm_self = self._to_orm(session)
                if not orm_self:
                    raise ValueError("bucket does not exist")
                for blob in orm_self.blobs:
                    yield RDBMSBlob(self, blob.name)

        return iter(list(get_blobs()))


class RDBMSBlobClient:
    """Maps the client interface to the RDBMS."""

    _engine: sa.Engine

    def __init__(self, engine: sa.Engine):
        ORMBase.metadata.create_all(engine)
        self._engine = engine

    @staticmethod
    def upload_url_to_bucket_blob(url: str) -> tuple[str, str]:
        match = re.match(r"https?://([^/]+)/(.*)", url)
        if not match:
            raise ValueError("upload url was malformed")
        return match.group(1), urllib.parse.unquote_plus(match.group(2))

    def blob_from_signed_url(self, url: str) -> RDBMSBlob:
        match = re.match(r"https?://([^/]+)/(.*)", url)
        if not match:
            raise ValueError("signed url was malformed")
        return self.bucket(match.group(1)).blob(
            urllib.parse.unquote_plus(match.group(2))
        )

    @staticmethod
    def bucket_blob_to_upload_url(bucket: str, blob: str) -> str:
        return f"http://{bucket}/{urllib.parse.quote_plus(blob)}"

    def http_put(self, url: str, content: bytes) -> None:
        bucket, blob = self.upload_url_to_bucket_blob(url)

        with self.db_session() as session:
            upload_record = session.get(ORMBlob, (bucket, blob))

            if not upload_record:
                raise ValueError("no upload record found")
            upload_record.data = content
            upload_record.size = len(content)
            upload_record.md5 = hashlib.md5(content).hexdigest()
            session.commit()

    @contextlib.contextmanager
    def db_session(self) -> Iterator[sa_orm.Session]:
        with sa_orm.Session(self._engine) as session:
            yield session

    def blob_from_url(self, url: str) -> RDBMSBlob:
        bucket_name, blob_name = _url_to_bucket_obj_name(url)
        bucket = self.bucket(bucket_name)
        return bucket.blob(blob_name)

    def bucket(self, name: str) -> RDBMSBucket:
        return RDBMSBucket(client=self, name=name)
