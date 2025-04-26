from abc import ABC, abstractmethod

from tinybird_cdk import utils

DEFAULT_TTL_FOR_PUBLIC_URLS_S = 3600

class Client(ABC):
    '''
    Abstract class with interface all cloud storage clients must implement.

    The API is restricted to what connectors need, strictly. If new requirements
    arise, more methods can be added, but there has to be a real use case.
    '''

    @abstractmethod
    def uri(self, bucket, key):
        '''
        Returns a string with the URI for the given bucket and key in the
        corresponding cloud storage service. For example, the GCS client would
        return something like this::

            client.uri('bucket', 'tinybird/random-file-name.csv')
            # => 'gs://bucket/tinybird/random-file-name.csv'
        '''

    @abstractmethod
    def ls(self, bucket, directory=None):
        '''
        Returns a list of strings with the keys in the given bucket, prefixed by
        the given directory, if any. This list can be empty::

            client.ls('bucket', 'tinybird')
            # => ['tinybird/foo.csv', 'tinybird/bar.csv']
        '''

    @abstractmethod
    def public_url(self, bucket, key, expires_in_s=DEFAULT_TTL_FOR_PUBLIC_URLS_S):
        '''Returns a string with a publicly accessible URL for the given object.'''

    @abstractmethod
    def rm(self, bucket, key):
        '''Removes the object from the cloud storage service.'''

    @abstractmethod
    def rmtree(self, bucket, directory):
        '''
        Removes all objects below the given bucket and directory in the cloud
        storage service.
        '''

    @abstractmethod
    def cat(self, bucket, directory):
        '''
        Concatenates all the objects in the given directory into one single object.
        The resulting object is stored in the same directory, and its key returned.

        If the directory is empty or non-existing, the method returns ``None``.
        '''

    def cat_key(self, directory):
        return f'{directory}/{utils.random_filename("cdk")}'
