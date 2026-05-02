"""FileService DB Model.

Database Object Model for FileServices.
"""
import os
from datetime import datetime
import uuid
from asyncdb.models import Column, Model

def auto_now_add(*args, **kwargs):
    return uuid.uuid4()


class FileModel(Model):
    file_id: int = Column(required=False, primary_key=True, db_default='auto')
    file_uid: uuid.UUID = Column(default=auto_now_add, required=True, primary_key=True, db_default='uuid_generate_v4()')
    file_slug: str = Column(required=True)
    program_id: int = Column(required=True, default=6)
    program_slug: str = Column(required=True, default=os.environ.get('APP_PROGRAM_SLUG', 'troc'))
    mimetype: str = Column(required=True, default='text/csv')
    description: str = Column(required=False)
    filename: dict = Column(required=False, default_factory=lambda: {"name": "", "pattern": ""})
    attributes: dict = Column(
        required=False,
        default_factory=lambda: {"overwrite": True, "create_dir": True, "show_preview": True}
    )
    params: dict = Column(required=False, default_factory=dict)
    fields: list = Column(required=False, default_factory=lambda: [])
    task_enabled: bool = Column(required=True, default=False)
    active: bool = Column(required=True, default=False)
    uploaded_at: datetime = Column(required=False, default=datetime.now())
    created_at: datetime = Column(required=False)

    class Meta:
        name = 'files'
        schema = os.environ.get('DB_SCHEMA', 'troc')
        strict = False
        frozen = False
