"""AWS CloudWatch Utilities.

This module contains a set of classes used to record information
about the exection of a process into AWS CloudWatch

"""

from datetime import datetime
import time
import boto3


def get_next_expected_sequence_token(message):
    next_expected_sequence_token = message.split("sequenceToken is:", 1)[1].strip()
    return next_expected_sequence_token


class Logger:
    """Class used to record logs in AWS CloudWatch"""

    def __init__(self, arg1, arg2=None, arg3=None):
      """Logger( [credentials], log_group_name, [region] )
         If credentials are supplied they should the result from AssumeRole.
         If credentials are not supplied then we use the default (computer's role)
         If region is not supplied, it defaults to us-east-1
         
         E.g.
         Logger( "myloggroup" )
         Logger( "myloggroup", "us-west-2" )
         Logger( boto3.client('sts').assume_role(RoleArn=ROLE, RoleSessionName='TestJob')['Credentials'], "myloggroup" )
      """
         
      if isinstance(arg1, dict):
        credentials = { "aws_access_key_id":arg1['AccessKeyId'], "aws_secret_access_key":arg1['SecretAccessKey'], "aws_session_token":arg1['SessionToken'] }
        log_group_name = arg2
        region = arg3
      else:
        credentials = {}
        log_group_name = arg1
        region = arg2
      if region == None:
        region = 'us-east-1'
      self.__do_init(credentials, log_group_name, region) 
                                    
    def __do_init(self, credentials, log_group_name, region):
        """Creates a new Logger object

        Args:
            credentials (dict): AWS Credentials used to access CloudWatch.
            log_group_name (str): Name of the AWS Log Groupself.
                Must be the name of the job being executed.
            region (str, optional): AWS region where logs are recorded.
                If not specified us-east-1 is assumed as default.

        """
        self.sequence_token = None
        self.region = region
        self.logs = boto3.client('logs', region_name=self.region, **credentials)

        self.log_stream_name = str(datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        self.log_group_name = log_group_name
        if len( \
            self.logs.describe_log_groups(logGroupNamePrefix=self.log_group_name)['logGroups'] \
              ) == 0:
            self.logs.create_log_group(logGroupName=self.log_group_name)
        self.logs.create_log_stream(logGroupName=self.log_group_name, \
                                    logStreamName=self.log_stream_name)

    def log(self, message):
        """Writes the passed argument into the AWS CloudWatch log

        The same message is also printed on standard output.

        Args:
            message (str): The actual message to be logged.

        """
        print(str(datetime.utcnow()) + ' : ' + message)
        try:
            if self.sequence_token is None:
                response = self.logs.put_log_events( \
                    logGroupName=self.log_group_name, \
                    logStreamName=self.log_stream_name, \
                    logEvents=[
                        {
                            'timestamp': int(round(time.time() * 1000)),
                            'message': message
                        },
                        ] \
                    )
            else:
                response = self.logs.put_log_events( \
                    logGroupName=self.log_group_name, \
                    logStreamName=self.log_stream_name, \
                    logEvents=[
                        {
                            'timestamp': int(round(time.time() * 1000)),
                            'message': message
                        },
                        ], \
                    sequenceToken=self.sequence_token \
                    )
        except (self.logs.exceptions.InvalidSequenceTokenException,
                self.logs.exceptions.DataAlreadyAcceptedException) as exception:
            error_message = exception.response['Error']['Message']
            next_sequence_token = get_next_expected_sequence_token(error_message)
            if next_sequence_token:
                self.sequence_token = next_sequence_token
                response = self.logs.put_log_events( \
                    logGroupName=self.log_group_name, \
                    logStreamName=self.log_stream_name, \
                    logEvents=[
                        {
                                'timestamp': int(round(time.time() * 1000)),
                                'message': message
                        },
                    ], \
                    sequenceToken=self.sequence_token \
                )
                pass
            else:
                raise exception
        self.sequence_token = response['nextSequenceToken']


class MetricRecorder:
    """Class used to record metrics in AWS CloudWatch"""
    def __init__(self, arg1, arg2=None, arg3=None):
      if isinstance(arg1, dict):
        credentials = { "aws_access_key_id":arg1['AccessKeyId'], "aws_secret_access_key":arg1['SecretAccessKey'], "aws_session_token":arg1['SessionToken'] }
        namespace = arg2
        region = arg3
      else:
        credentials = {}
        namespace = arg1
        region = arg2
      if region == None:
        region = 'us-east-1'
      self.__do_init(credentials, namespace, region)

    def __do_init(self, credentials, namespace, region):
        """Creates a new MetricRecorder object

        Args:
            credentials (dict): AWS Credentials used to access CloudWatch.
            namespace (str): Name of the AWS Metric Custom Namespace.
            region (str, optional): AWS region where logs are recorded.
                If not specified, us-east-1 is assumed as default.

        """
        self.namespace = namespace
        self.cloudwatch = boto3.client('cloudwatch', region_name=region, **credentials)

    def record(self, metric_name, value, metric_dims=None, metric_unit='Count'):
        """Record a metric value into AWS CloudWatch

        Args:
            metric_name (str): The name of the AWS metric.
            value (str): Actual value of the AWS metric.
            metric_dims (list, optional): A list of dimensions associated wit the data.
                each dimension is a dict Name - Value
                If not specified, empty list [] is assumed as default.
            metric_unit (str, optional): Unit of the AWS metric.
                If not specified, Count is assumed as default.

        """

        metric_dims = metric_dims or []
        # See https://nedbatchelder.com/blog/200806/pylint.html
        # for details on why not to use [] in the method declaration.
        if len(metric_dims) > 0:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Dimensions': metric_dims,
                        'Value': value,
                        'Unit': metric_unit
                    }
                ]
            )
        else:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Value': value,
                        'Unit': metric_unit
                    }
                ]
            )
