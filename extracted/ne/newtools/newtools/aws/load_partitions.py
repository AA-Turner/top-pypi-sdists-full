from newtools.optional_imports import boto3
from newtools.aws import S3Location
from newtools.doggo.doggo import FileDoggo
import os


class S3List:

    def __init__(self, bucket, s3_client=None, request_payer='bucketowner'):
        """
        From newtools 2.1.0 onwards, the list_folders method returns a set rather than a list.
        :param bucket: The s3 bucket to look for data in
        :param s3_client: optional pass in of a pre created boto3 s3 client
        """
        self.s3_client = s3_client if s3_client else boto3.client('s3')
        self.bucket = bucket
        self.request_payer = request_payer

    def list_folders(self, prefix=''):
        """
        :param prefix: prefix the data is stored under if empty string will scan at highest level of bucket
        :return: returns a set of the folders at that level (changed from list in 2.1.0 onwards)
        """
        result_list = set()

        # force prefix end with "/"
        if prefix != '' and not prefix.endswith("/"):
            prefix = prefix + "/"

        paginator = self.s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket,
                                   Delimiter='/',
                                   Prefix=prefix,
                                   RequestPayer=self.request_payer)

        for page in pages:
            if page.get('CommonPrefixes'):
                for i in page['CommonPrefixes']:
                    result_list.add(i['Prefix'])

        return result_list


class LoadPartitions:
    """
    The LoadPartitions class will recurse to a specified depth in S3 and create SQL to add all partitions
    to a table in Athena. This is significantly faster than using ``MSCK REPAIR TABLE`` as it only searches
    to the specified depth.

    """

    def __init__(self, bucket, s3_client=None, request_payer='bucketowner'):
        """
        :param bucket: S3 bucket where the data is stored
        :param s3_client: optional param of pre initialised s3 client
        """

        self.s3_client = s3_client
        self.s3_bucket = bucket
        self.request_payer = request_payer

    def list_partitions(self, table=None, partition_depth=None, s3_path=None):
        """
        :param table: The athena table partitions are being loaded for, either this or s3_path has to be specified
        :param partition_depth: The number of partition levels to look for, optional param should be specified if known significant performance impact
        :param s3_path: The prefix for where the data is stored, can be set to blank string to look at top level
                        of the bucket
        :return: A list of all the full paths of the partitions
        """
        partition_depth = partition_depth or 10

        if s3_path is None:

            if table is None:
                raise ValueError('Either table or s3_path must be set both can not be None')

            s3_path = table

        list_files = S3List(self.s3_bucket, self.s3_client, self.request_payer)

        partitions_list = list_files.list_folders(s3_path)
        partitions_tracked = 0

        while partitions_tracked < partition_depth:
            temp_part_list = set()
            for partition in partitions_list:
                partitions_path_temp = list_files.list_folders(partition)
                """
                For each partition in the partition_list we check if there is any more depth, once we reach filename
                `list_files.list_folders(partition)` will return an empty set we check for this and break from
                checking the rest of the partitions, as all partitions have the same depth.
                """
                if not partitions_path_temp:
                    break
                else:
                    temp_part_list.update(partitions_path_temp)

            # If temp_part_list is still empty, no further partitions have been found so we break out of the while loop.

            if temp_part_list:
                partitions_list = temp_part_list
            else:
                break
            partitions_tracked += 1
        return partitions_list

    def generate_sql(self, table, partitions_list, s3_path=None, athena_client=None, output_location=None,
                     athena_s3_client=None):
        """
                :param table: The athena table partitions are being loaded for
                :param partitions_list: The list of all the partitions to generate the alter table query for
                :param s3_path: The prefix for where the data is stored, optional, can also be empty string to look at
                                the toplevel of the bucket
                :param athena_client: The current Athena Client, optional, will be used to list partitions already loaded
                :param output_location: Output location of queries parsed into athena_client
                :param athena_s3_client: The s3 client that matches with the athena client passed in to be able to
                access the queries produced by it if in different account to default
                :return: A list of queries that can be run to add all partitions
                """

        s3_path = table if s3_path is None else s3_path

        if athena_client is not None:
            if output_location is None:
                raise ValueError('output_location must be set to use athena_client')

            query = athena_client.add_query("SHOW PARTITIONS {0}".format(table),
                                            name="show_partitions_athena",
                                            output_location=output_location)

            athena_client.wait_for_completion()
            fm = FileDoggo(os.path.join(query.arguments["output_location"], "{}.txt".format(query.id)), mode='rb',
                           compression=None, client=athena_s3_client, request_payer=self.request_payer)
            with fm as f:
                athena_list = f.read().decode().splitlines()
            athena_list = {'{table}/{partition}/'.format(table=s3_path, partition=partition) for partition in
                           athena_list}
            partitions_list = partitions_list - athena_list

        partition_string_list = []
        for i in partitions_list:
            partition_string = i
            location = S3Location(bucket=self.s3_bucket, key=partition_string, ignore_double_slash=True)
            partition_string = partition_string.replace(s3_path, "")
            partition_string = partition_string.rstrip('/')

            partitions_string_list = [
                '{key}=\'{value}\''.format(key=partition.split('=')[0], value=partition.split('=')[1]) for partition in
                partition_string.split('/') if '=' in partition]

            partition_string = ",".join(partitions_string_list)

            partition_string_formatted = ' PARTITION({}) LOCATION \'{}\''.format(partition_string, location)

            partition_string_list.append(partition_string_formatted)

        query_string_base = "ALTER TABLE {table} ADD IF NOT EXISTS".format(table=table)

        full_query_string_list = []
        temp_string_build = ''
        for count, string in enumerate(partition_string_list):
            temp_string_build += string
            if len(temp_string_build.encode('utf-8')) >= 250000 or (count + 1) == len(partition_string_list):
                query_string_build = query_string_base + temp_string_build
                full_query_string_list.append(query_string_build)
                temp_string_build = ''

        return full_query_string_list

    def get_sql(self, table, partition_depth=None, s3_path=None, athena_client=None, output_location=None,
                athena_s3_client=None):
        """
        :param table: The athena table partitions are being loaded for
        :param partition_depth: The number of partition levels to look for, optional param should be specified if
                                known as will yield best performance.
        :param s3_path: The prefix for where the data is stored, optional, can also be empty string to look at the top
                        level of the bucket
        :param athena_client: The current Athena Client, optional, will be used to list partitions already loaded
        :param output_location: Output location of queries parsed into athena_client
        :param athena_s3_client: The s3 client that matches with the athena client passed in to be able to
                access the queries produced by it if in different account to default
        :return: A list of queries that can be run to add all partitions, each query is limited to 10 partitions
        """

        partitions_list = self.list_partitions(table, partition_depth, s3_path)

        return self.generate_sql(table, partitions_list, s3_path, athena_client, output_location, athena_s3_client)

    def get_sql_from_file_names(self, table, file_names, s3_path=None, athena_client=None, output_location=None,
                                athena_s3_client=None):
        """
        Adds functionality to get the load partitions sql from the output of save_partitioned (PandasDoggo).
        All other params are the same as in get_sql (with removal of partition_depth as we do not use list_partitions).

        :param file_names: Full file names (as output from PandasDoggo.save_partitioned)
        """

        partitions_list = [S3Location(file).prefix for file in file_names]

        return self.generate_sql(table, partitions_list, s3_path, athena_client, output_location, athena_s3_client)
