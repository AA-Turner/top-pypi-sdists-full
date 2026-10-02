# (c) Deductive 2012-2020, all rights reserved
# This code is licensed under MIT license (see license.txt for details)

from urllib import parse


class S3Location(str):
    """
    Class that parses out an S3 location from a passed string. Subclass of `str`
    so supports most string operations.

    :param s3_str: string representation of s3 location, accepts most common formats
        Also accepts None if using `bucket` and `key` keywords
    :param bucket: ignored if s3_str is not None. can specify only bucket for
        bucket='mybucket' - 's3://mybucket/' or in conjuction with `key`
    :param key: ignored if s3_str is not None. Bucket must be set.
        bucket='mybucket', key='path/to/file'
    :param ignore_double_slash: default False. If true allows s3 locations containing '//'
        these are valid s3 paths, but typically result from mistaken joins

    Examples:

    .. code-block:: python

        loc1 = S3Location('s3://bucket/folder/file.txt')
        loc2 = S3Location('bucket/folder')
        loc3 = S3Location('http://s3*.amazonaws.com/bucket-name/')
        loc4 = S3Location('https://s3*.amazonaws.com/bucket-name/')
        loc5 = S3Location(bucket='bucket', key='path/to/file')


    """

    def __new__(cls, s3_str=None, ignore_double_slash=False, bucket=None, key=None):

        if s3_str is None:
            s3_str = cls._from_kwargs(bucket, key)

        validated_string = cls._validate(s3_str, ignore_double_slash)

        instance = super(S3Location, cls).__new__(cls, validated_string)

        return instance

    def __init__(self, *args, **kwargs):

        super().__init__()

        self._bucket = self.split('/')[2]
        self._key = '/'.join(self.split('/')[3:])

    @staticmethod
    def _from_kwargs(bucket=None, key=None):

        if bucket is None:
            raise ValueError('could not resolve bucket')

        return "s3://{bucket}/{path}".format(bucket=bucket,
                                             path=key or '')

    @classmethod
    def _validate(self, s3_str, ignore_double_slash=False):

        result = parse.urlparse(s3_str)

        if result.port is not None:
            raise ValueError("S3 URLs cannot have a port")

        if result.password is not None:
            raise ValueError("S3 URLs cannot have a password (or username)")

        if result.username is not None:
            raise ValueError("S3 URLs cannot have a username")

        if result.scheme == "":
            if result.path.startswith("/"):
                raise ValueError("S3 URLS must have a prefix or not start with a /, "
                                    "current val: {}".format(s3_str))
            else:
                _bucket = result.path.split("/")[0]
                _key = "/".join(result.path.split("/")[1:])

        elif result.scheme == "s3":
            if result.hostname is None:
                raise ValueError("S3 URL is malformed, "
                                    "current val: {}".format(s3_str))
            _bucket = result.hostname
            _key = result.path[1:]
        elif result.scheme in ["http", "https"]:
            if result.hostname.startswith("s3") and result.hostname.endswith(".amazonaws.com"):
                _bucket = result.path.split("/")[1]
                _key = "/".join(result.path.split("/")[2:])
            else:
                raise ValueError("S3 HTTP URLS must be of the form http[s]://s3*.amazonaws.com/bucket-name/, "
                                    "current val: {}".format(s3_str))
        else:
            raise ValueError("S3 URLs must be either s3://, http://, or https://, "
                                "current val: {}".format(s3_str))

        s3_path = "s3://{bucket}/{path}".format(bucket=_bucket,
                                                path=_key or '')

        if not ignore_double_slash:
            if "//" in "{bucket}/{path}".format(bucket=_bucket,
                                                path=_key or ''):
                raise ValueError("S3 URLs cannot contains a // unless ignore_double_slash is set to True, "
                                    "current val: {}".format(s3_str))

        return s3_path

    @staticmethod
    def _coalesce_empty(s, n):
        if s == "":
            return n
        else:
            return s

    @property
    def file(self):
        """
        File property
        :return: the file name part of the S3 URL
        """
        return self._coalesce_empty(self._key.split("/")[-1], None)

    @property
    def prefix(self):
        """

        :return: the prefix part of the S3 URL
        """
        return self._coalesce_empty("/".join(self._key.split("/")[0:-1]), None)

    @property
    def key(self):
        """

        :return: the key part of the S3 URL
        """
        return self._coalesce_empty(self._key, None)

    @property
    def path(self):
        """

        :return: the path part of the S3 URL (same as the key)
        """
        return self.key

    @property
    def bucket(self):
        """

        :return: the bucket part of the S3 URL (same as the key)
        """
        return self._coalesce_empty(self._bucket, None)

    @property
    def s3_url(self):
        return "s3://{bucket}/{path}".format(bucket=self.bucket,
                                             path=self.key or '')

    def join(self, *other, ignore_double_slash=False):
        """
        Join s3 location to string or list of strings similar to os.path.join
        :param other: nargs to join,
        :param ignore_double_slash: default False. set true to allow '//' in the link, eg 's3://bucket/folder//path/key'
        :return: the new S3Location

        Examples:

        .. code-block:: python

            loc1 = S3Location('s3://bucket/folder/')
            loc2 = loc1.join('file.txt')
            loc3 = loc1.join('path', 'to', 'file')


        """

        to_join = '/'.join(other)

        if self.endswith('/'):
            joined = self.s3_url + to_join
        else:
            joined = self.s3_url + '/' + to_join

        return S3Location(joined, ignore_double_slash)

    def __repr__(self):
        return ('S3Location(\'{}\')'.format(self))

    def __eq__(self, other):
        return self.s3_url == str(other)

    def __contains__(self, item):
        return self.__str__().__contains__(item)

    def __hash__(self):
        return hash(self.__str__())
