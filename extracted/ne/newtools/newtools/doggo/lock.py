import logging

from .fs import DoggoFileSystem
from time import sleep, time
from random import random

from newtools.optional_imports import boto3, botocore


class DoggoWait:
    """

    A generic wait and timeout function. Raises TimeoutError() if the requested task doesn't occur in the period.

    .. code-block:: python

        dw = DoggoWait()
        dw.start_timeout()
        while not check_my_condition():
            self.dw.check_timeout()

    """

    def __init__(self, wait_period, time_out_seconds):
        """
        :param wait_period: the period to wait for between iterations
        :param time_out_seconds: the time after which a TimeoutError is raised
        """
        self.time_out_seconds = time_out_seconds
        self.wait_period = wait_period
        self._timeout = None

    def wait(self):
        """
        Waits for the defined period
        """
        sleep(self.wait_period)

    def start_timeout(self):
        """
        Starts a time out
        """
        self._timeout = time() + self.time_out_seconds

    def timed_out(self):
        """
        Checks for a time out

        :return: true if the timer has timed out, otherwise false
        """
        if self._timeout is not None:
            return time() > self._timeout
        else:
            raise ValueError("Someone has tried to call timed_out() before calling start_timeout()")

    def check_timeout(self):
        """
        Waits, and raises an exception if the timer has timed out
        """
        self.wait()
        if self.timed_out():
            raise TimeoutError("Timed out waiting for completion")


class LockBase:
    def __init__(self, file,
                 wait_period=0.1,
                 time_out_seconds=1800,
                 maximum_age=3600,
                 logger=logging.getLogger("newtools.doggo.baselock")):
        """
        Locks a file across multiple process and clients. On creating the lock we

        1. Check to see if anyone already has a lock
        2. If they don't, attempt to create a lock and wait for wait_period.
        3. If two processes have attempted to get the lock then the one with the earlier lock gets it.
        4. When the lock is released the lock class deletes the lock and other processes can proceed

        Locks only last for maximum_age seconds, and any request to get a lock will time out after time_out_seconds

        Includes waits for eventual consistency

        :param file: the file to lock
        :param wait_period: the period to wait before confirming file lock
        :param time_out_seconds: the time out to stop waiting after
        :param maximum_age: the maximum age of lock files to respect
        :param logger: the logger to use for this class and any newtools classes created by this class
        """
        self.file = file
        self.dw = DoggoWait(wait_period, time_out_seconds)
        self.maximum_age = maximum_age
        self._logger = logger

    def __enter__(self):
        self._logger.info(f"Getting lock on {self.file}")
        self.acquire()
        self._logger.info(f"Acquired lock on {self.file}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        self._logger.info(f"Released lock on {self.file}")


class DoggoLock(LockBase):
    """
    Implements locking using an additional file on the file system. Works for local files and for S3.

    For file systems that are only eventually consistent, use a longer wait_period to wait for consistency when
    multiple clients are reading at the same time.

    Locks a file across multiple process and clients using an additional file on the file system.

        The lock file has the following format:
        ".lock-{file}.{timestamp}-{random}"

        where:

        * file - is the file being locked
        * timestamp - is the timestamp the lock was requested
        * random - is a random number
    """

    def __init__(self, file,
                 wait_period=30,
                 time_out_seconds=1800,
                 maximum_age=3600,
                 logger=logging.getLogger("newtools.doggo.lock")
                 ):
        super(DoggoLock, self).__init__(file, wait_period, time_out_seconds, maximum_age, logger)

        self.dfs = DoggoFileSystem()
        self.file = file
        self.lock_file = None
        self.lock_file_glob = self._get_lock_path(get_glob=True)

    def acquire(self):
        # If the file is locked then wait for it to be unlocked
        self.dw.start_timeout()
        while len(self._get_lock_files()) > 0:
            self.dw.check_timeout()

        # create a lock file and wait to avoid contention
        self._create_lock_file()
        self.dw.wait()

        # wait until we are the earliest lock file
        self.dw.start_timeout()
        while self.lock_file != self._get_first_lock_file():  # pragma: no cover
            self.dw.check_timeout()  # this is only covered by the multiprocessing tests which coverage doesn't see

    def release(self):
        if self.lock_file is not None:
            self.dfs.rm(self.lock_file)
        self.lock_file = None

    def _timestamp_is_valid(self, lock_file):
        timestamp = float(lock_file.split(".")[-1].split('-')[0])

        return timestamp > time() - self.maximum_age

    def _generate_lock_files(self):
        for file in sorted(self.dfs.glob(self.lock_file_glob)):
            if self._timestamp_is_valid(file):
                yield file

    def _get_lock_files(self):
        return [a for a in self._generate_lock_files()]

    def _get_first_lock_file(self):
        for a in self._generate_lock_files():
            return a

    def _get_lock_path(self, get_glob=False):
        file_path = self.dfs.split(self.file)
        if get_glob:
            return self.dfs.join(
                file_path[0],
                ".lock-{file}**".format(
                    file=file_path[1]))
        else:
            return self.dfs.join(
                file_path[0],
                ".lock-{file}.{timestamp}-{random}".format(
                    file=file_path[1],
                    timestamp=str(time()).replace(".", "-"),
                    random=str(random()).replace(".", "-")))

    def _create_lock_file(self):
        if self.lock_file is None:
            self.lock_file = self._get_lock_path()

        with self.dfs.open(self.lock_file, mode="wb") as f:
            f.write(b"woof!")

        self._logger.debug(f"Created {self.lock_file}")


class DynamoDogLock(LockBase):
    """
    Implements a lock using a table in DynamoDB.

    By default uses the region us-east-1 but this can be specified as an optional parameter when requesting the lock.

    The table in dynamo DB is called newtools.dynamo.doggo.lock
    """
    _table_name = "newtools.dynamo.doggo.lock"
    __table = None

    def __init__(self,
                 file,
                 wait_period=0.1,
                 time_out_seconds=1800,
                 maximum_age=3600,
                 logger=logging.getLogger("newtools.doggo.dynamolock"),
                 region="us-east-1"
                 ):

        super(DynamoDogLock, self).__init__(file, wait_period, time_out_seconds, maximum_age, logger)
        self._ddb_client = boto3.client("dynamodb", region_name=region)
        self._ddb_resource = boto3.resource("dynamodb", region_name=region)

    @property
    def _table(self):

        if self._table_name in self._ddb_client.list_tables()['TableNames']:
            self.__table = self._ddb_resource.Table(self._table_name)

            # check the table exists...
            self.__table.item_count
        else:
            self.__table = self._ddb_resource.create_table(
                AttributeDefinitions=[{"AttributeName": "file", "AttributeType": "S"}],
                KeySchema=[{"AttributeName": "file", "KeyType": "HASH"}],
                TableName=self._table_name,
                BillingMode="PAY_PER_REQUEST"
            )
            waiter = self._ddb_client.get_waiter('table_exists')
            waiter.wait(TableName=self._table_name,
                        WaiterConfig={'Delay': 2, 'MaxAttempts': 120})
        return self.__table

    def _get_lock(self):
        epoch_time = round(time())
        try:
            self._table.update_item(
                Key={"file": self.file},
                UpdateExpression="SET locked_time = :current_time",
                ConditionExpression='attribute_not_exists(locked_time) OR locked_time < :expiry_time',
                ExpressionAttributeValues={':current_time': epoch_time,
                                           ':expiry_time': epoch_time - self.maximum_age}
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            else:  # pragma: nocover - this should never occur
                raise e

        return True

    def acquire(self):
        # If the file is locked then wait for it to be unlocked
        self.dw.start_timeout()
        while not self._get_lock():
            self.dw.check_timeout()

    def release(self):
        self._table.delete_item(Key={"file": self.file})
