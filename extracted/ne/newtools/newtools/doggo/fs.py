# (c) 2012-2020 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""

Cross-platform supports for reading, writing, copying, deleting, etc... files from S3 or local

.. parsed-literal::

             ,--._______,-.
           ,','  ,    .  ,_`-.
          / /  ,' , _` ``. |  )       `-..
         (,';'""`/ '"`-._ ` `/ ______    \\
           : ,o.-`- ,o.  )`` -'      `---.))
           : , d8b ^-.   '|   `.      `    `.
           |/ __:_     `. |  ,  `       `    \
           | ( ,-.`-.    ;'  ;   `       :    ;
           | |  ,   `.      /     ;      :    \
           ;-'`:::._,`.__),'             :     ;
          / ,  `-   `--                  ;     |
         /  `                   `       ,      |
        (    `     :              :    ,`      |
         `   `.    :     :        :  ,'  `    :
          `    `|-- `     ` ,'    ,-'     :-.-';
          :     |`--.______;     |        :    :
           :    /           |    |         |   \
           |    ;           ;    ;        /     ;
         _/--' |   -hrr-   :`-- /         `_:_:_|
       ,',','  |           |___ \
       `^._,--'           / , , .)
                          `-._,-'
"""
import shutil
import os
import gzip
from io import BytesIO
from glob import glob
from newtools.optional_imports import s3fs, boto3, botocore
from newtools.aws import S3Location
from newtools.log import log_to_stdout
from newtools.optional_imports import AWSRetry
from newtools.optional_imports import boto3

import fnmatch
logger = log_to_stdout('Deductive - DoggoFileSystem')

def _gzip_wrapped(func):
    def gzip_open(self, *args, **kwargs):
        if self.compression == 'gzip':
            f = func(self, *args, **kwargs)
            self._to_close.append(f)
            return gzip.open(f, self.mode)
        return func(self, *args, **kwargs)

    return gzip_open

class FileDoggo:
    """

He fetches the things you want. Tv remotes, slippers, newspapers, files. Mostly files though.

.. code-block:: python

    from newtools import FileDoggo
    import boto3

    path = 's3 or local path'
    s3_client = boto3.Session().client('s3')
    with FileDoggo(path, mode='rb', client=s3_client) as f:
        f.read()

This is written to treat local paths and s3 paths the same, returning a file like object for either.

"""
    _connection = None

    def __init__(self, path, mode='rb', is_s3=None, client=None, compression=None, request_payer='bucketowner'):
        """
        Creates the class

        :param path: path to file to connect to. s3 or local path
        :type path: str or S3Location
        :param mode: opening mode for file, note s3 only allows 'rb' or 'wb'
        :param is_s3: force Doggo to treat path as an S3Location, otherwise autodetects if beings with "s3://"
        :type is_s3: bool
        :param client: optional `boto3.Session().Client('s3')` instance to use for s3 operations
        :param compression: None, 'gzip' or 'snappy'.
        :param request_payer: either 'bucketowner' or 'requester' - who incurs the cost of said operation
        """

        self.buffer = BytesIO()
        self.mode = mode

        self.is_s3 = is_s3 or path.startswith('s3://')
        if self.is_s3:
            # allows you to specify s3 for paths that don't begin with s3:// for whatever reason you might want
            self.path = S3Location(path)
        else:
            self.path = path

        self.request_payer = request_payer

        self._client = client
        if compression in [None, 'gzip', 'snappy']:
            self.compression = compression
        else:
            raise NotImplementedError(f"Compression {compression} is not supported in FileDoggo")
        self._to_close = []

    @property
    def connection(self):
        if not self._connection:
            self._connection = self._connect()
        return self._connection

    @property
    def client(self):
        if not self._client:
            self._client = boto3.Session().client('s3')
        return self._client

    def close(self):

        if self._connection:
            for c in [self._connection] + self._to_close:
                if not c.closed:
                    c.close()

    def __enter__(self):
        return self.connection

    def __exit__(self, etype, value, traceback):
        # ¯\_(ツ)_/¯
        if self.is_s3 and 'w' in self.mode:
            self._write_s3()

        self.close()

    @_gzip_wrapped
    def _connect(self):

        if self.is_s3:
            if self.mode == 'rb':
                return self._read_s3()
            elif self.mode == 'wb':
                # check s3 exists? meh, writing to a buffer is so fast i think the overhead isn't worth
                return self.buffer  # write to this buffer and we'll upload later
            else:
                raise ValueError(f'mode {self.mode} is not supported')

        else:

            return open(self.path, self.mode)

    @AWSRetry.backoff(tries=5, delay=1, backoff=1, added_exceptions=['404'])
    def _read_s3(self):

        self.client.download_fileobj(Bucket=self.path.bucket, Key=self.path.key, Fileobj=self.buffer,
                                     ExtraArgs={'RequestPayer': self.request_payer})
        self.buffer.seek(0)
        return self.buffer

    def _write_s3(self):

        if self.compression == 'gzip':
            self.connection.close()  # flushes writing to gzip

        self.buffer.seek(0)
        self.client.upload_fileobj(Bucket=self.path.bucket, Key=self.path.key, Fileobj=self.buffer,
                                   ExtraArgs={'RequestPayer': self.request_payer})


class DoggoFileSystem:
    """
    Implements common file operations using either S3 or local file system depending on whether the path
    begins "s3://"

    """
    __s3fs = None

    def __init__(self, session=None, boto3_session=None):
        s3fs.S3FileSystem.read_timeout = 600
        self.__s3fs = s3fs.S3FileSystem(session=session)

        self.s3_session = boto3_session if boto3_session else boto3.session.Session()
        self.s3_client = self.s3_session.client('s3')

    @property
    def _s3fs(self):
        """
        S3FS caching does not respect other applications updating S3 so therefore we invalidate
        the cache before using

        :return: the S3FS File system
        """
        self.__s3fs.invalidate_cache()
        return self.__s3fs

    def is_s3(self, path1, path2=None):
        """
        Returns true if the passed path is on S3

        :param path1: the first path to check
        :param path2: the second path to check
        :raises NotImplementedError: if only one of the two paths in on S3
        :return: True if both are S3, False if neither are, and raises an exception for mixed types
        """
        p1_is_s3 = path1.startswith("s3://")
        p2_is_s3 = p1_is_s3 if path2 is None else path2.startswith("s3://")

        if path2 is not None:
            return p1_is_s3 and p2_is_s3
        else:
            return p1_is_s3

    def _check_folders(self, path):
        if not self.is_s3(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def cp(self, source, destination):
        """
        Copies a file or folder, per shutil copy() or shutil.copytree() depending on
        if source is a /folder/ or a /file.extension

        :param source: source path, folders must be specified by trailing '/'
        :param destination: destination path, folders must be specified by trailing '/'
        """

        if not self.exists(source):
            raise FileNotFoundError('The specified source file/folder cannot be located')

        is_directory = source.endswith('/')

        if self.is_s3(source, destination):
            return self._s3fs.cp(source, destination, recursive=True)

        elif not self.is_s3(source) and self.is_s3(destination):
            return self._s3fs.put(lpath=source,
                                  rpath=destination,
                                  recursive=True)

        elif self.is_s3(source) and not self.is_s3(destination):
            return self._s3fs.get(lpath=destination,
                                  rpath=source,
                                  recursive=is_directory)

        else:
            if is_directory:
                return shutil.copytree(source, destination)
            else:
                self._check_folders(destination)
                return shutil.copy(source, destination)

    def mv(self, source, destination):
        """
        Moves a file per shutil.move() except that it does not copy WITHIN.
        i.e. /location/folderA/ >> /destination/folderA/
        rather than
        i.e. /location/folderA/ >> /destination/folderA/folderA/

        :param source: source path, folders must be specified by trailing '/'
        :param destination: destination path, folders must be specified by trailing '/'
        """

        if not self.exists(source):
            raise FileNotFoundError('The specified source file/folder cannot be located')

        is_directory = source.endswith('/')

        if self.is_s3(source, destination):
            return self._s3fs.mv(source, destination)

        elif not self.is_s3(source) and self.is_s3(destination):
            self._s3fs.put(lpath=source,
                           rpath=destination,
                           recursive=True)
            if is_directory:
                return shutil.rmtree(source)
            else:
                return os.remove(source)

        elif self.is_s3(source) and not self.is_s3(destination):
            self._s3fs.get(lpath=destination,
                           rpath=source,
                           recursive=is_directory)
            return self._s3fs.rm(source, recursive=is_directory)

        else:
            if is_directory:
                shutil.copytree(source, destination)
                return shutil.rmtree(source)

            else:
                self._check_folders(destination)
                shutil.copy(source, destination)
                return os.remove(source)

    def exists(self, path):
        """
        Returns true if a path exists, per os.path.exists()

        :param path: the path to check
        :return: True if the path exists, otherwise False
        """
        if self.is_s3(path):
            return self._s3fs.exists(path)
        else:
            return os.path.exists(path)

    def size(self, path):
        """
        Returns the size of a file per os.path.getsize()

        :param path: the path to check
        :return: the size of the file at this path
        """
        if self.is_s3(path):
            return self._s3fs.size(path)
        else:
            return os.path.getsize(path)

    def rm(self, path, **kwargs):
        """
        Removes a file, per os.remove()

        :param path: the file to remove
        """
        if self.is_s3(path):
            return self._s3fs.rm(path, **kwargs)
        else:
            return os.remove(path)

    def ls(self, location: str, recursive: bool = False):
        """
        returns the list of contents of a directory. If directory is empty or doesnt exist, returns an empty list

        if recursive = False, returns contents of specified directory, including folders
        if recursive = True, returns all files including full paths that are below the specified location,
        and no directories
        """
        if self.is_s3(location) and not recursive:
            return [S3Location(item) for item in self._s3fs.glob(location)] if location.endswith('/') else [
                S3Location(item) for item in self._s3fs.glob(location + '/')]

        elif self.is_s3(location) and recursive:
            bucket = S3Location(location).bucket
            prefix = S3Location(location).key
            try:
                if prefix is None:
                    files = self._list_files(bucket=bucket)
                else:
                    files = self._list_files(bucket=bucket, prefix=prefix)
                return [S3Location(bucket).join(file) for file in files]
            except (self.s3_client.exceptions.ClientError, botocore.exceptions.NoCredentialsError) as e:
                logger.error(e)
                return[]

        elif recursive:
            file_list = []
            for item in os.walk(location):
                file_list.extend([os.path.join(item[0], file_name) for file_name in item[2] if
                                  os.path.isfile(os.path.join(item[0], file_name))])
            return file_list
        else:
            try:
                return [os.path.join(location, item) for item in os.listdir(location)]
            except (FileNotFoundError, NotADirectoryError) as e:
                logger.error(e)
                return[]

    def glob(self, glob_string):
        """
        Searched for a file per glob.glob(recursive=True)


        :param glob_string: the path to search
        :return:
        """
        if self.is_s3(glob_string):
            return [S3Location(a) for a in self._s3fs.glob(glob_string)]
        else:
            return glob(glob_string, recursive=True)

    def open(self, path, mode, *args, **kwargs):
        """
        Opens a file, per open()

        :param path: the path to open
        :param mode: the mode to open in
        :param args: any arguments in the FileDoggo class
        :param kwargs: any keyword arguments for the FileDoggo class
        :return: a file handle
        """
        if "w" in mode:
            self._check_folders(path)
        return FileDoggo(path, mode, *args, **kwargs)

    def join(self, path, *paths):
        """
        Joins to paths per os.path.join()
        :param path: the first path
        :param paths: the paths to joins
        :return:
        """
        if self.is_s3(path):
            return S3Location(path).join(*paths)
        else:
            return os.path.join(path, *paths)

    def split(self, path):
        """
        Splits a path into prefix and file, per os.path.split()
        :param path:
        :return:
        """
        if self.is_s3(path):
            loc = S3Location(path)
            if loc.prefix is not None:
                return S3Location(loc.bucket).join(loc.prefix), loc.file
            else:
                return S3Location(loc.bucket), loc.file
        else:
            return os.path.split(path)

    def _files_within(self, directory_path, pattern):
        """
        Returns generator containing all the files in a directory
        """
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for file_name in fnmatch.filter(filenames, pattern):
                yield os.path.join(dirpath, file_name)

    def _put_folder(self, source, bucket, destination="", file_format="*"):
        """
       Copies files from a directory on local system to s3
      +        :param source: Folder on local filesystem that must be copied to s3
      +        :param bucket: s3 bucket in which files have to be copied
      +        :param destination: Location on s3 bucket to which files have to be copied
      +        :param file_format: pattern for files to be transferred
      +        :return: None
              """
        if os.path.isdir(source):
            file_list = list(self._files_within(source, file_format))
            for each_file in file_list:
                part_key = os.path.relpath(each_file, source)
                key = os.path.join(destination, part_key)
                self.s3_client.upload_file(each_file, bucket, key)
        else:
            raise ValueError("Source must be a valid directory path")

    def _generate_keys(self, bucket, prefix, suffix="", start_after=None):

        if start_after is None:
            s3_objects = self.s3_client.list_objects_v2(Bucket=bucket,
                                                        Prefix=prefix,
                                                        MaxKeys=1000)
        else:
            s3_objects = self.s3_client.list_objects_v2(Bucket=bucket,
                                                        Prefix=prefix,
                                                        MaxKeys=1000,
                                                        StartAfter=start_after)

        if 'Contents' in s3_objects:
            for key in s3_objects["Contents"]:
                if key['Key'].endswith(suffix):
                    yield key['Key']

            # get the next keys
            yield from self._generate_keys(bucket, prefix, suffix, s3_objects["Contents"][-1]['Key'])

    def _delete(self, path, suffix=""):
        loc = S3Location(path)
        keys = []
        for key in self._generate_keys(loc.bucket, loc.path, suffix):
            keys.append({'Key': key})
            if len(keys) == 1000:
                self.s3_client.delete_objects(Bucket=loc.bucket,
                                              Delete={"Objects": keys})
                keys = []

        if len(keys) > 0:
            self.s3_client.delete_objects(Bucket=loc.bucket,
                                          Delete={"Objects": keys})

    def _delete_files(self, bucket, prefix, suffix=""):
        return self._delete("s3://{0}/{1}".format(bucket, prefix), suffix)

    def _list_files(self, bucket, prefix="", suffix=None, remove_prefix=False):
        return self._list("s3://{0}/{1}".format(bucket, prefix), suffix, remove_prefix)

    def _list(self, path, suffix=None, remove_prefix=False):
        return [key['key'] for key in self._list_dict(path, suffix, remove_prefix)]

    def _list_dict(self, path, suffix=None, remove_prefix=False):
        """
            Return details of files with particular prefix/suffix stored on S3

            ## Parameters
            - bucket: S3 bucket in which files are stored
            - prefix: Prefix filter for files on S3
            - suffix: Suffix filter for files on S3
        """

        loc = S3Location(path)

        response = self.s3_client.list_objects_v2(Bucket=loc.bucket,
                                                  Prefix=loc.path if loc.path else "")
        while True:
            if response and 'Contents' in response:
                for key in response['Contents']:
                    if not suffix or key['Key'].endswith(suffix):
                        yield {
                            'key': key['Key'].replace(loc.path, '') if loc.path and remove_prefix else key['Key'],
                            'last_modified': key['LastModified'],
                            'size': key['Size']
                        }

                # Do we need to carry on?
                if response['IsTruncated'] and 'NextContinuationToken' in response:
                    response = self.s3_client.list_objects_v2(Bucket=loc.bucket,
                                                              Prefix=loc.path if loc.path else "",
                                                              ContinuationToken=response['NextContinuationToken'])
                else:
                    break
            else:
                break
