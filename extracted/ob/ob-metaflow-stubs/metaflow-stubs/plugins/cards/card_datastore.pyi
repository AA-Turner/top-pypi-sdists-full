######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.914567                                                            #
######################################################################################################

from __future__ import annotations


from ... import metaflow_config as metaflow_config
from .exception import CardNotPresentException as CardNotPresentException

CARD_S3ROOT: None

CARD_LOCALROOT: None

DATASTORE_LOCAL_DIR: str

CARD_SUFFIX: str

CARD_AZUREROOT: None

CARD_GSROOT: None

SKIP_CARD_DUALWRITE: bool

TEMP_DIR_NAME: str

NUM_SHORT_HASH_CHARS: int

class CardInfo(tuple, metaclass=type):
    """
    CardInfo(type, hash, id, filename)
    """
    @staticmethod
    def __new__(_cls, type, hash, id, filename):
        """
        Create new instance of CardInfo(type, hash, id, filename)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class CardNameSuffix(object, metaclass=type):
    ...

class CardPathSuffix(object, metaclass=type):
    ...

def path_spec_resolver(pathspec):
    ...

def is_file_present(path):
    ...

class CardDatastore(object, metaclass=type):
    @classmethod
    def get_storage_root(cls, storage_type):
        ...
    def __init__(self, flow_datastore, pathspec = None):
        ...
    @classmethod
    def get_card_location(cls, base_path, card_name, uuid, card_id = None, suffix = 'html'):
        ...
    @staticmethod
    def info_from_path(path, suffix = 'html'):
        """
        Args:
            path (str): The path to the card
        
        Raises:
            Exception: When the card_path is invalid
        
        Returns:
            CardInfo
        """
        ...
    def save_data(self, uuid, card_type, json_data, card_id = None):
        ...
    def save_card(self, uuid, card_type, card_html, card_id = None, overwrite = True):
        ...
    def create_full_path(self, card_path):
        ...
    def get_card_names(self, card_paths):
        ...
    def get_card_html(self, path):
        ...
    def get_card_data(self, path):
        ...
    def cache_locally(self, path, save_path = None):
        """
        Saves the data present in the `path` the `metaflow_card_cache` directory or to the `save_path`.
        """
        ...
    def extract_data_paths(self, card_type = None, card_hash = None, card_id = None):
        ...
    def extract_card_paths(self, card_type = None, card_hash = None, card_id = None):
        ...
    ...

