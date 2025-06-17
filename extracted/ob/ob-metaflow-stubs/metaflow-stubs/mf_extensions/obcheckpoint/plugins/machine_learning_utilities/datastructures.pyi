######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.878251                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures

from .exceptions import KeyNotCompatibleWithObjectException as KeyNotCompatibleWithObjectException
from .exceptions import KeyNotCompatibleException as KeyNotCompatibleException
from .exceptions import IncompatibleObjectTypeException as IncompatibleObjectTypeException
from .datastore.task_utils import init_datastorage_object as init_datastorage_object

class MetaflowDataArtifactReference(object, metaclass=type):
    @property
    def size(self):
        ...
    @property
    def url(self):
        ...
    @property
    def key(self):
        ...
    @property
    def pathspec(self):
        ...
    @property
    def attempt(self):
        ...
    @property
    def created_on(self):
        ...
    @property
    def metadata(self):
        ...
    def __init__(self, **kwargs):
        ...
    def validate(self, data):
        ...
    @classmethod
    def from_dict(cls, data) -> typing.Union["ModelArtifact", "CheckpointArtifact"]:
        ...
    @classmethod
    def hydrate(cls, data: typing.Union["ModelArtifact", "CheckpointArtifact", dict]):
        ...
    def to_dict(self):
        ...
    ...

class ModelArtifact(MetaflowDataArtifactReference, metaclass=type):
    def __init__(self, **kwargs):
        ...
    @property
    def blob(self):
        ...
    @property
    def uuid(self):
        ...
    @property
    def serializer(self):
        ...
    @property
    def source(self):
        ...
    @property
    def storage_format(self):
        ...
    @classmethod
    def create(cls, pathspec = None, attempt = None, key = None, url = None, model_uuid = None, metadata = None, storage_format = None, source = None, serializer = None, label = None):
        ...
    ...

class CheckpointArtifact(MetaflowDataArtifactReference, metaclass=type):
    @property
    def storage_format(self):
        ...
    @property
    def version_id(self):
        ...
    @property
    def name(self):
        ...
    def __init__(self, **kwargs):
        ...
    ...

class Factory(object, metaclass=type):
    @classmethod
    def hydrate(cls, data):
        ...
    @classmethod
    def from_dict(cls, data):
        ...
    @classmethod
    def load(cls, data, local_path, storage_backend):
        ...
    @classmethod
    def object_type_from_key(cls, reference_key):
        ...
    @classmethod
    def load_from_key(cls, key_object, local_path, storage_backend):
        ...
    @classmethod
    def load_metadata_from_key(cls, key_object, storage_backend) -> typing.Union[metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.ModelArtifact]:
        ...
    ...

def load_model(reference: typing.Union[str, metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.MetaflowDataArtifactReference, dict], path: str):
    ...

