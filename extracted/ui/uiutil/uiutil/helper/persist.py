# encoding: utf-8

from stateutil.persist import Persist, JSONPersistentStore
from configurationutil import Configuration
from conversionutil.dx import dx
from conversionutil.ex import ex

global_ui_persistence_store = None

# TODO: Need to document this, and maybe move some of it into stateutil


class UIPersistentStore(object):
    def __init__(self,
                 persistent_store):
        """

        :param persistent_store: class that implements __getitem__ and __setitem__.
        """
        self.persistent_store = persistent_store

    @staticmethod
    def key(key):
        """
        Override if the key must be modified to access the store
        :param key: key into the store
        :return: modifier key
        """
        return key


def json_persistent_store_factory(root_folder):
    return UIPersistentStore(
               JSONPersistentStore(
                   root_folder=root_folder))


def set_global_ui_persistence_store(store):
    global global_ui_persistence_store
    global_ui_persistence_store = store


def get_global_ui_persistence_store():
    global global_ui_persistence_store
    if not global_ui_persistence_store:
        raise ValueError(u'set_global_ui_persistence_store has not been called.')
    return global_ui_persistence_store


def get_default_global_ui_persistence_store():
    try:
        get_global_ui_persistence_store()
    except ValueError:
        set_global_ui_persistence_store(
            json_persistent_store_factory(
                root_folder=u'{r}/ui_persistence'.format(r=Configuration().data_path_unversioned)))


class PersistentField(Persist):

    def __init__(self,
                 key,
                 store=None,
                 *args,
                 **kwargs):
        if store is None:
            store = get_global_ui_persistence_store()
            key = store.key(key)
        super(PersistentField, self).__init__(persistent_store=store.persistent_store,
                                              key=key,
                                              stack_level=3,
                                              *args,
                                              **kwargs)


class ObscuredPersistentField(PersistentField):
    """
    Used instead of PersistentField if you want
    the value stored with some noddy encoding
    """
    @staticmethod
    def encode(value):
        return ex(value)

    @staticmethod
    def decode(value):
        return dx(value)
