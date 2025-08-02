import random
from io import BytesIO

import pytest

from pymtom_xop import MtomAttachment

FILE_PATH = "documents/python.pdf"
FILE_NAME = "python.pdf"


def test__get_content_type():
    att = MtomAttachment(file=FILE_PATH)
    setattr(att, 'file_name', '')
    with pytest.raises(AttributeError, match="file_name attribute is required"):
        att._MtomAttachment__get_content_type()  # type: ignore

    setattr(att, 'file_name', FILE_NAME)
    att._MtomAttachment__get_content_type()  # type: ignore

    assert att.content_type == 'application/pdf'


def test__generate_mime_headers():
    att = MtomAttachment(file=FILE_PATH)

    headers: bytes = att._MtomAttachment__generate_mime_headers()  # type: ignore

    header_lst = headers.splitlines()
    # remove empty and decode
    header_lst = [h.decode() for h in header_lst if h]

    validate_headers = [
        f'Content-Type: {att.content_type}',
        f'Content-Transfer-Encoding: {att.content_transfer_encoding}',
        f'Content-ID: {att.cid}',
        f'Content-Disposition: {att.content_disposition}; name="{att.file_name}"'
    ]

    assert header_lst == validate_headers


def test_init():
    att = MtomAttachment(FILE_PATH)

    assert att.content_transfer_encoding == 'binary'
    assert att.content_disposition == 'attachment'


def test_get_cid():
    att = MtomAttachment(FILE_PATH)
    cid = att.get_cid()

    assert isinstance(cid, bytes)


def test_init_multiple_unique_mtom_attachments():
    # create list of random attachments
    atts: list[MtomAttachment] = []
    qty = random.randint(3, 7)
    for i in range(qty):
        data = BytesIO(random.randbytes(random.randint(10, 100)))
        new_att = MtomAttachment(file=data, file_name=f"file_{i}.txt")
        atts.append(new_att)

    # check unique filename
    assert len(set([att.file_name for att in atts])) == qty
    # check unique file data
    assert len(set([att.file_data for att in atts])) == qty
    # check unique cid
    assert len(set([att.cid for att in atts])) == qty
    # check unique mime headers
    assert len(set([att.mime_headers for att in atts])) == qty
