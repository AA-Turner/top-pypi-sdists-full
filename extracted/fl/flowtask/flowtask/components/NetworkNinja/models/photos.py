from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from urllib.parse import urlparse, ParseResult
from datamodel import Field
from .abstract import AbstractPayload
from .account import Account


class PhotoCategory(AbstractPayload):
    """
    Photo Category Model.

    Represents a photo category in the system.

    Example:
        {
            "category_id": 53,
            "name": "TEST Category",
            "client_id": 61,
            "enabled": false,
            "orgid": 71,
            "client_name": "TRO Walmart Assembly"
        }
    """
    category_id: int = Field(primary_key=True, required=True)
    name: str = Field(alias='category_name')
    client_id: int = Field(alias="category_client_id")
    enabled: bool = Field(default=True)
    orgid: int = Field(alias="category_orgid")
    client_name: str = Field(alias="category_client_name")

    class Meta:
        strict = True
        as_objects = True
        name = 'photo_categories'
        schema: str = 'networkninja'

class Document(AbstractPayload):
    """
    Document Model.

    Represents a document in the system.

    Example:
        {
            "document_id": 1,
            "document_name": "Test Document",
            "document_path": "https://www.example.com/test.pdf",
            "description": "Test Document Description",
            "created_on": "2025-02-01T00:00:00-06:00",
            "store_number": "12345",
            "account_id": 1,
            "account_name": "Test Account",
            "question_name": "Test Question",
            "url_parts": "https://www.example.com/test.pdf"
        }
    """
    document_id: int = Field(primary_key=True, required=True)
    document_name: str
    document_path: str
    description: str
    created_on: datetime
    store_number: str
    account_id: Optional[Account]
    account_name: str
    question_name: str
    url_parts: str

    class Meta:
        strict = True
        as_objects = True
        name = 'documents'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        # split the document_path into parts:
        if self.document_path is not None:
            self.url_parts = urlparse(self.document_path)


class Photo(AbstractPayload):
    photo_id: int = Field(primary_key=True, required=True)
    form_id: int
    formid: Optional[int]
    event_id: int
    description: str
    filename: str
    created_on: datetime
    store_number: Optional[int] = Field(alias='store_id')
    account_id: Account
    account_name: Optional[str]
    column_name: Union[str, int]
    column_id: Optional[int]
    question_name: Optional[str]
    url_parts: Optional[dict]
    photo_path: str
    client_id: int
    client_name: str
    categories: Optional[List[PhotoCategory]]
    is_deleted: bool = Field(default=False)
    is_archived: bool = Field(default=False)

    class Meta:
        strict = True
        as_objects = True
        name = 'stores_photos'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        self.filename = self.description
        # split the photo_path into parts:
        if self.photo_path is not None:
            # Iterate over all parts and convert into a dictionary of strings:
            parts = urlparse(self.photo_path)
            self.url_parts = {
                'scheme': parts.scheme,
                'netloc': parts.netloc,
                'path': parts.path,
                'params': parts.params,
                'query': parts.query,
                'fragment': parts.fragment,
            }
        if self.account_id:
            self.account_id.account_name = self.account_name
