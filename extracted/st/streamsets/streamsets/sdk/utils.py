# Copyright 2021 StreamSets Inc.

"""Assorted utility functions."""

# fmt: off
import base64
import binascii
import copy
import json
import logging
import os
import random
import re
import string
from collections import OrderedDict, defaultdict
from datetime import datetime
from decimal import Decimal
from time import sleep, time

import inflection
from inflection import camelize
from requests.exceptions import ChunkedEncodingError, ConnectionError, HTTPError

from streamsets.sdk.constants import SDC_DEPLOYMENT_TYPE, TRANSFORMER_DEPLOYMENT_TYPE
from streamsets.sdk.exceptions import InvalidVersionError

from .exceptions import InternalServerError

# fmt: on

logger = logging.getLogger(__name__)

# These are the current modes for transformer and sdc. Assuming there won't be an overlap between the modes for SDC and
# transformer.
TRANSFORMER_EXECUTION_MODES = {'BATCH', 'STREAMING'}
TRANSFORMER_DEFAULT_EXECUTION_MODE = 'BATCH'
# pipelineType is NOT THE SAME THING as executionMode, even though the value happens to also be a value for executionMode
# see patch in SDC-10960 which introduced this parameter name to the backend
TRANSFORMER_PIPELINE_TYPE = 'STREAMING'
SDC_DEFAULT_EXECUTION_MODE = 'STANDALONE'
METERING_METRIC_LOOKUP = {'pipeline_hours': 'pipelineTime', 'clock_hours': 'clockTime', 'total_units': 'units'}

# This is hardcoded in domainserver over here https://git.io/Jecwm
DEFAULT_PROVISIONING_SPEC = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: datacollector-deployment
  namespace: streamsets
spec:
  replicas: 1
  selector:
    matchLabels:
      app: datacollector-deployment
  template:
    metadata:
      labels:
        app: datacollector-deployment
    spec:
      containers:
      - name: datacollector
        image: streamsets/datacollector:latest
        ports:
        - containerPort: 18630
        env:
        - name: HOST
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: PORT0
          value: "18630"'''


def get_decoded_jwt(token):
    """Decode JSON web token.

    Args:
        token (:obj:`str`): JSON web token.

    Returns:
        Decoded token as a :py:`dict`.
    """
    if not isinstance(token, str):
        raise TypeError('Token should be of type `str` and not of type {}'.format(type(token)))

    split_token = token.split('.')

    if len(split_token) < 2:
        raise ValueError('Token passed is not valid.')

    # padding is required to decode the token from base64, we can calculate the number of `=` we need to add as padding,
    # but base64 will automatically truncate any extra padding provided. The maximum padding we need at any given point
    # is 2. Explanation on stack overflow: https://publ.cc/BdJhXb
    padding = '=='
    token_payload = split_token[1]

    try:
        decoded_token = base64.b64decode(token_payload + padding)
        decoded_token_dict = json.loads(decoded_token)
    except (binascii.Error, json.decoder.JSONDecodeError) as e:
        logger.error(e, exc_info=True)
        raise ValueError('Error occurred while trying to decode the token.')

    return decoded_token_dict


def get_random_string(characters=string.ascii_letters, length=8):
    """
    Returns a string of the requested length consisting of random combinations of the given
    sequence of string characters.
    """
    return ''.join(random.choice(characters) for _ in range(length))


def get_random_file_path(prefix='/tmp', extension='txt'):
    """Returns a random file path with specified prefix and extension

    Args:
        prefix (:obj:`str`, optional): Prefix path. Default: ``'/tmp'``.
        extension (:obj:`str`, optional): File extension to use. Default: ``'txt'``.
    """
    return os.path.join(prefix, '{}.{}'.format(get_random_string, extension))


def join_url_parts(*parts):
    """
    Join a URL from a list of parts. See http://stackoverflow.com/questions/24814657 for
    examples of why urllib.parse.urljoin is insufficient for what we want to do.
    """
    return '/'.join([piece.strip('/') for piece in parts if piece is not None])


def get_params(parameters, exclusions=None):
    """Get a dictionary of parameters to be passed as requests methods' params argument.

    The typical use of this method is to pass in locals() from a function that wraps a
    REST endpoint. It will then create a dictionary, filtering out any exclusions (e.g.
    path parameters) and unset parameters, and use camelize to convert arguments from
    ``this_style`` to ``thisStyle``.
    """
    # We do this to prevent Python from misusing its magic to change a tuple
    # with a single value into the type of the single value inside the tuple
    exclusions = (exclusions,) if not isinstance(exclusions, tuple) else exclusions

    # we rstrip params so as we can handle names like 'len_'
    return {
        camelize(arg.rstrip('_'), uppercase_first_letter=False): value
        for arg, value in parameters.items()
        if value is not None and arg not in exclusions
    }


class Version:
    """Maven version string abstraction.

    Use this class to enable correct comparison of Maven versioned projects. For our purposes,
    any version is equivalent to any other version that has the same 4-digit version number (i.e.
    3.0.0.0-SNAPSHOT == 3.0.0.0-RC2 == 3.0.0.0).

    Args:
        version (:obj:`str`), (:obj:`int`), (:obj:`float`), or (:obj:`Version`):
            Version string (e.g. '2.5.0.0-SNAPSHOT').
    Raises:
        An instance of :py:class:`sdk.exceptions.InvalidVersionError` if the version input cannot be parsed.
    """

    # pylint: disable=protected-access,too-few-public-methods
    def __init__(self, version):
        if isinstance(version, Version):
            # avoid re-parsing data from a `Version` object
            self.name = version.name
            self.version = version.version
            self.specifier = version.specifier

        else:
            pattern = r'^([a-zA-Z]+)?-?([\d.]+)-?(\w+)?$'
            # name `[a-zA-Z]+` May or may not exist
            # delimiter1 `-?` May or may not exist e.g. `-` or None
            # version `[\d.]+` Version number e.g. `3.8.2`
            # delimiter2 `-?` May or may not exist e.g. `-` or None
            # specifier `\w+` May or may not exist e.g. `RC2`

            try:
                # note: `version` may be an in or float type, convert to a string before further processing
                groups = re.search(pattern, str(version)).groups()
                # Parse the numeric part of versions & add additional 0's to keep a min length of version.
                numeric_version_list = [int(i) for i in groups[1].split('.')]
                if not numeric_version_list:
                    raise InvalidVersionError(version)

            except (ValueError, AttributeError):
                raise InvalidVersionError(version)

            while len(numeric_version_list) < 4:
                numeric_version_list.append(0)

            self.name = groups[0]
            self.version = numeric_version_list
            self.specifier = groups[2]

    def __repr__(self):
        version = ".".join(map(str, self.version))
        return "<Version: {!r}, {}, {!r}>".format(self.name, version, self.specifier)

    def __str__(self):
        version = ".".join(map(str, self.version))
        return "-".join(filter(None, [self.name, version, self.specifier]))

    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version(other)
        return self.name == other.name and self.version == other.version

    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version(other)
        if self.name != other.name:
            raise TypeError('Comparison can only be done between two Version instances with same name.')
        return self.version < other.version

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return other.__ge__(self)


def sdc_value_reader(value):
    """Helper function which can parse SDC Record value (Record JSON in dict format for example)
    and convert to SDC implied Python collection with necessary types being converted from SDC
    to Python.

    Args:
        value: SDC Record value.

    Returns:
        The value.
    """
    # Note: check instance of OrderedDict before dict to avoid superfluous
    # check of OrderedDict getting evaluated for dict
    type_to_function_map = {
        "LIST_MAP": lambda x: sdc_value_reader(OrderedDict([(key, x[key]) for key in range(len(x))])),
        "LIST": lambda x: sdc_value_reader(x),
        "MAP": lambda x: sdc_value_reader(x),
        "SHORT": lambda x: int(x),
        "INTEGER": lambda x: int(x),
        "LONG": lambda x: int(x),
        "CHAR": lambda x: x,
        "STRING": lambda x: x,
        "DATE": lambda x: datetime.utcfromtimestamp(x / 1000),
        "DATETIME": lambda x: datetime.utcfromtimestamp(x / 1000),
        "TIME": lambda x: datetime.utcfromtimestamp(x / 1000),
        "BOOLEAN": lambda x: x,
        "BYTE": lambda x: str(x).encode(),
        "DOUBLE": lambda x: float(x),
        "FLOAT": lambda x: float(x),
        "DECIMAL": lambda x: Decimal(str(x)),
        "BYTE_ARRAY": lambda x: base64.b64decode(x),
    }
    if isinstance(value, OrderedDict):
        return OrderedDict([(value['dqpath'].split('/')[-1], sdc_value_reader(value)) for key, value in value.items()])
    elif isinstance(value, dict):
        if 'type' in value and 'value' in value:
            # value['type'] in some cases could also be a dict
            if (
                value['value'] is None
                or not isinstance(value['type'], str)
                or value['type'] not in type_to_function_map
            ):
                return value['value']
            return type_to_function_map[value['type']](value['value'])
        else:
            return {key: sdc_value_reader(value) for key, value in value.items()}
    elif isinstance(value, list):
        return [sdc_value_reader(item) for item in value]
    else:
        return value['value']


def st_value_reader(value):
    """Helper function which can parse ST Record value (Record JSON in dict format for example)
    and convert to ST implied Python collection with necessary types being converted from ST to Python.

    Args:
        value: ST Record value.

    Returns:
        The value.
    """
    # Note: check instance of OrderedDict before dict to avoid superfluous
    # check of OrderedDict getting evaluated for dict
    type_to_function_map = {
        "LIST_MAP": lambda x: st_value_reader(OrderedDict([(key, x[key]) for key in range(len(x))])),
        "LIST": lambda x: st_value_reader(x),
        "MAP": lambda x: st_value_reader(x),
        "SHORT": lambda x: int(x),
        "INTEGER": lambda x: int(x),
        "LONG": lambda x: int(x),
        "CHAR": lambda x: x,
        "STRING": lambda x: x,
        "DATE": lambda x: datetime.utcfromtimestamp(x / 1000),
        "DATETIME": lambda x: datetime.utcfromtimestamp(x / 1000),
        "TIME": lambda x: datetime.utcfromtimestamp(x / 1000),
        "BOOLEAN": lambda x: x,
        "BYTE": lambda x: str(x).encode(),
        "DOUBLE": lambda x: float(x),
        "FLOAT": lambda x: float(x),
        "DECIMAL": lambda x: Decimal(str(x)),
        "BYTE_ARRAY": lambda x: base64.b64decode(x),
    }
    if isinstance(value, OrderedDict):
        return OrderedDict([(value['dqpath'].split('/')[-1], st_value_reader(value)) for key, value in value.items()])
    elif isinstance(value, dict):
        if 'type' in value and 'value' in value:
            # value['type'] in some cases could also be a dict
            if (
                value['value'] is None
                or not isinstance(value['type'], str)
                or value['type'] not in type_to_function_map
            ):
                return value['value']
            return type_to_function_map[value['type']](value['value'])
        else:
            return {key: st_value_reader(value) for key, value in value.items()}
    elif isinstance(value, list):
        return [st_value_reader(item) for item in value]
    else:
        return value['value']


def pipeline_json_encoder(o):
    """Default method for JSON encoding of custom classes."""
    if hasattr(o, '_data'):
        return o._data
    raise TypeError('{} is not JSON serializable'.format(repr(o)))


def format_log(log_records):
    return '\n'.join(
        [
            (
                '{timestamp} [user:{user}] [pipeline:{entity}] '
                '[runner:{runner}] [thread:{thread}] {severity} '
                '{category} - {message} {exception}'
            ).format(
                timestamp=rec.get('timestamp'),
                user=rec.get('s-user'),
                entity=rec.get('s-entity'),
                runner=rec.get('s-runner'),
                thread=rec.get('thread'),
                severity=rec.get('severity'),
                category=rec.get('category'),
                message=rec.get('message'),
                exception=rec.get('exception'),
            )
            for rec in log_records
        ]
    )


def format_sch_log(log_records):
    return '\n'.join(
        [
            (
                '{timestamp} [requestId:{request_id}] [app:{app}] '
                '[componentId:{component_id}] [user:{user}] [thread:{thread}] '
                '{exception_level} {message}'
            ).format(
                timestamp=rec.get('timestamp'),
                request_id=rec.get('request_id'),
                app=rec.get('app'),
                component_id=rec.get('component_id'),
                user=rec.get('user'),
                thread=rec.get('thread'),
                exception_level=rec.get('exception_level'),
                message=rec.get('message'),
            )
            for rec in log_records
        ]
    )


# The `#:` constructs at the end of assignments are part of Sphinx's autodoc functionality.
DEFAULT_TIME_BETWEEN_CHECKS = 1  #:
DEFAULT_TIMEOUT = 60  #:


def wait_for_condition(
    condition,
    condition_args=None,
    condition_kwargs=None,
    time_between_checks=DEFAULT_TIME_BETWEEN_CHECKS,
    timeout=DEFAULT_TIMEOUT,
    time_to_success=0,
    success=None,
    failure=None,
):
    """Wait until a condition is satisfied (or timeout).

    Args:
        condition: Callable to evaluate.
        condition_args (optional): A list of args to pass to the
            ``condition``. Default: ``None``
        condition_kwargs (optional): A dictionary of kwargs to pass to the
            ``condition``. Default: ``None``
        time_between_checks (:obj:`int`, optional): Seconds between condition checks.
            Default: :py:const:`DEFAULT_TIME_BETWEEN_CHECKS`
        timeout (:obj:`int`, optional): Seconds to wait before timing out.
            Default: :py:const:`DEFAULT_TIMEOUT`
        time_to_success (:obj:`int`, optional): Seconds for the condition to hold true
            before it is considered satisfied. Default: ``0``
        success (optional): Callable to invoke when ``condition`` succeeds. A ``time``
            variable will be passed as an argument, so can be used. Default: ``None``
        failure (optional): Callable to invoke when timeout occurs. ``timeout`` will
            be passed as an argument. Default: ``None``

    Raises:
        :py:obj:`TimeoutError`
    """
    start_time = time()
    stop_time = start_time + timeout

    success_start_time = None

    while time() < stop_time:
        outcome = condition(*condition_args or [], **condition_kwargs or {})
        if outcome:
            success_start_time = success_start_time or time()
            if time() >= success_start_time + time_to_success:
                if success is not None:
                    success(time='{:.3f}'.format(time() - start_time))
                return
        else:
            success_start_time = None
        sleep(time_between_checks)

    if failure is not None:
        failure(timeout=timeout)


def wait_and_retry_on_http_error(func, timeout_sec=300, time_between_calls_sec=2):
    """
    Decorator to retry a function on HTTPError for draft runs and snapshots using tunneling

    Retries the decorated function upon encountering an HTTPError, logging a warning and waiting
    between attempts until the specified timeout is reached.

    Args:
        func (callable): The function to decorate.
        timeout_sec (int): Maximum time to keep retrying (default is 300 seconds).
        time_between_calls_sec (int): Wait time between retry attempts (default is 2 seconds).

    Raises:
        HTTPError: If the function fails after retrying until the timeout is reached.

    Returns:
        An instance of :py:class:`streamsets.sdk.sch_api.Command` if the decorated function if successful.
    """

    def inner(*args, **kwargs):
        end_time = time() + timeout_sec
        error = None
        while time() < end_time:
            try:
                return func(*args, **kwargs)
            except HTTPError as e:
                error = e
                logger.warning("HTTPError occurred: {}. Retrying in {} seconds...".format(e, time_between_calls_sec))
                sleep(time_between_calls_sec)
        raise error

    return inner


def retry_on_connection_error(func):
    """Decorator to retry a function on ConnectionError.

    Args:
        func (callable): Function to decorate, that can throw ConnectionError.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, ChunkedEncodingError) as e:
            # requests sometimes throws ChunkedEncodingError when the underlying exception is a ConnectionError.
            logger.warning("ConnectionError occurred: {}. Retrying once.".format(e))
            return func(*args, **kwargs)

    return inner


class SeekableList(list):
    def get(self, **kwargs):
        """Retrieve the first instance that matches the supplied arguments.

        Args:
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            The first instance from the group that matches the supplied arguments.
        """
        try:
            return next(i for i in self if all(getattr(i, k) == v for k, v in kwargs.items()))
        except StopIteration:
            raise ValueError(
                'Instance ({}) is not in list'.format(', '.join('{}={}'.format(k, v) for k, v in kwargs.items()))
            )

    def get_all(self, **kwargs):
        """Retrieve all instances that match the supplied arguments.

        Args:
            **kwargs: Optional arguments to be passed to filter the results offline.

        Returns:
            A :py:obj:`streamsets.sdk.utils.SeekableList` of results that match the supplied arguments.
        """
        return SeekableList(i for i in self if all(getattr(i, k) == v for k, v in kwargs.items()))


class MutableKwargs:
    """Util class with functions to update kwargs.

    Args:
        defaults (:obj:`dict`): default kwargs for the function.
        actuals (:obj:`dict`): actual kwargs passed to the function.
    """

    def __init__(self, defaults, actuals):
        self._defaults = defaults
        self._actuals = actuals

    def union(self):
        """Unions defaults with actuals.

        Returns:
            A py:obj:`dict` of unioned args.
        """
        unioned_kwargs = dict(self._defaults)
        unioned_kwargs.update(self._actuals)
        return unioned_kwargs

    def subtract(self):
        """Returns the difference between actuals and defaults based on keys.

        Returns:
            A py:obj:`dict` of subtracted kwargs.
        """
        return {key: self._actuals[key] for key in self._actuals.keys() - self._defaults.keys()}


def update_acl_permissions(api_client, resource_type, permission):
    """Util function mapping various api_client functions (update_acl_permissions) to the resource_type.

    Args:
        api_client (py:class:`streamsets.sdk.sch_api.ApiClient`): An instance of API client.
        resource_type (:obj:`str`): Type of resource eg. 'JOB', 'PIPELINE'.
        permission (:py:class:`streamsets.sdk.sch_models.Permission`): A Permission object.
    """
    function_call_mapping = {
        'JOB': api_client.update_job_permissions,
        'PIPELINE': api_client.update_pipeline_permissions,
        'SDC': api_client.update_sdc_permissions,
        'REPORT_DEFINITION': api_client.update_report_definition_permissions,
        'CONNECTION': api_client.update_connection_permissions,
        'TOPOLOGY': api_client.update_topology_permissions,
        'EVENT_SUBSCRIPTION': api_client.update_subscription_permissions,
        'DEPLOYMENT': api_client.update_legacy_deployment_permissions,
        'CSP_DEPLOYMENT': api_client.update_deployment_permissions,
        'CSP_ENVIRONMENT': api_client.update_environment_permissions,
        'SCHEDULER_JOB': api_client.update_scheduled_task_permissions,
        'ALERT': api_client.update_alert_permissions,
    }
    return function_call_mapping[resource_type](permission, permission['resourceId'], permission['subjectId'])


def set_acl(api_client, resource_type, resource_id, acl_json):
    """Util function mapping various api_client functions (set_acl) to the resource_type.

    Args:
        api_client (py:class:`streamsets.sdk.sch_api.ApiClient`): An instance of API client.
        resource_type (:obj:`str`): Type of resource eg. 'JOB', 'PIPELINE'.
        resource_id (:obj:`str`): Id of the resource (pipeline, job etc.).
        acl_json (:py:class:`streamsets.sdk.sch_models.Permission`): A Permission object.
    """
    function_call_mapping = {
        'JOB': api_client.set_job_acl,
        'PIPELINE': api_client.set_pipeline_acl,
        'SDC': api_client.set_engine_acl,
        'REPORT_DEFINITION': api_client.set_report_definition_acl,
        'CONNECTION': api_client.update_connection_acl,
        'TOPOLOGY': api_client.set_topology_acl,
        'EVENT_SUBSCRIPTION': api_client.set_subscription_acl,
        'DEPLOYMENT': api_client.set_provisioning_agent_acl,
        'CSP_DEPLOYMENT': api_client.update_deployment_acl,
        'CSP_ENVIRONMENT': api_client.set_environment_acl,
        'SCHEDULER_JOB': api_client.set_scheduled_task_acl,
        'ALERT': api_client.set_alert_acl,
    }
    return function_call_mapping[resource_type](resource_id, acl_json)


def reversed_dict(forward_dict):
    """Reverse the key: value pairs to value: key pairs.

    Args:
        forward_dict (:obj:`dict`): Original key: value dictionary.

    Returns:
        An instance of (:obj:`dict`) with value: key mapping.
    """
    values = list(forward_dict.values())
    if len(set(values)) < len(values):
        logger.warning('The dictionary provided, is not one-one mapping. This could cause some consistency problems.')
    return dict(reversed(item) for item in forward_dict.items())


def get_open_output_lanes(stages):
    """Util function to get open output lanes from a set of stages.

    Args:
        stages (:py:obj:`streamsets.sdk.utils.SeekableList`) or
               (:obj:`list`): List of :py:class:`streamsets.sdk.sdc_models.Stage` instances.

    Returns:
        A (:obj:`set`) of open output (:obj:`str`) lanes.
    """
    output_lanes = set()
    input_lanes = set()
    for stage in stages:
        output_lanes.update({output_lane for output_lane in stage.output_lanes})
        input_lanes.update({input_lane for input_lane in stage._data['inputLanes']})
    return output_lanes - input_lanes


def determine_fragment_label(stages, number_of_open_output_lanes):
    """Util function to determine Pipeline Fragment Label.

    Args:
        stages (:py:obj:`streamsets.sdk.utils.SeekableList`) or
               (:obj:`list`): List of :py:class:`streamsets.sdk.sdc_models.Stage` instances.
        number_of_open_output_lanes (:obj:`int`): Number of open output lanes.

    Returns:
        An instance of :obj:`str`.
    """
    stage_types = {stage['uiInfo']['stageType'] for stage in stages}
    # Logic taken from: https://git.io/fjlL2
    label = 'Processors'
    if 'SOURCE' in stage_types:
        label = 'Origins'
    if number_of_open_output_lanes == 0:
        label = 'Destinations'
    return label


def build_tag_from_raw_tag(raw_tag, organization):
    """Build tag json from raw tag string.

    Args:
        raw_tag (:obj:`str`): Raw tag
        organization (:obj:`str`): SCH Organization

    Returns:
        An instance of :obj:`dict`
    """
    # Logic as seen at https://git.io/JfPhk
    parent_id = '{}:{}'.format('/'.join(raw_tag.split('/')[:-1]), organization) if raw_tag.split('/')[0:-1] else None
    return {
        'id': '{}:{}'.format(raw_tag, organization),
        'tag': raw_tag.split('/')[-1],
        'parentId': parent_id,
        'organization': organization,
    }


def get_topology_nodes(jobs, pipeline, pipeline_definition, x_pos, y_pos, selected_topology_node=None, postfix=None):
    """Create a topology node for the specified jobs in JSON format, and update any existing nodes as required.

    Instead of calling this method directly, all users should instead use the methods available to the
        :py:class:`streamsets.sdk.sch_models.TopologyBuilder` and :py:class:`streamsets.sdk.sch_models.Topology` classes
        respectively.

    Args:
        jobs (:obj:`list`): A list of jobs, in JSON format, to create topology nodes for.
        pipeline (:obj:`dict`): A Pipeline object, in JSON format, that the jobs are based on.
        pipeline_definition (:obj:`dict`): The definition of the pipeline, in JSON format.
        x_pos (:obj:`int`): An integer representing the position of the node on the X-axis.
        y_pos (:obj:`int`): An integer representing the position of the node on the Y-axis.:
        selected_topology_node (:py:class:`streamsets.sdk.sch_models.TopologyNode`, optional): A TopologyNode object to
            attach the node to. Default: ``None``
        postfix (:obj:`int`, optional): An integer to attach to the postfix datetime. Default: ``None``
    Returns:
        A :obj:`list` of Topology nodes in JSON format.
    """
    # Based off of https://git.io/JBFgn
    topology_node_json = {
        'nodeType': None,
        'instanceName': None,
        'library': None,
        'stageName': None,
        'stageVersion': None,
        'jobId': None,
        'pipelineId': None,
        'pipelineCommitId': None,
        'pipelineVersion': None,
        'inputLanes': [],
        'outputLanes': [],
        'uiInfo': {},
    }
    error_discard_stage_name = 'com_streamsets_pipeline_stage_destination_devnull_ToErrorNullDTarget'
    stats_aggr_null_stage_name = 'com_streamsets_pipeline_stage_destination_devnull_StatsNullDTarget'
    stats_aggr_dpm_stage_name = 'com_streamsets_pipeline_stage_destination_devnull_StatsDpmDirectlyDTarget'
    fragment_source_stage_name = 'com_streamsets_pipeline_stage_origin_fragment_FragmentSource'
    fragment_processor_stage_name = 'com_streamsets_pipeline_stage_processor_fragment_FragmentProcessor'
    fragment_target_stage_name = 'com_streamsets_pipeline_stage_destination_fragment_FragmentTarget'
    topology_nodes = []
    source_system_nodes = []
    job_nodes = []
    stage_instances = pipeline_definition['stages']
    source_stage_instances = [
        source_stage for source_stage in stage_instances if source_stage['uiInfo']['stageType'] == 'SOURCE'
    ]
    target_stage_instances = [
        target_stage
        for target_stage in stage_instances
        if target_stage['uiInfo']['stageType'] == 'TARGET' or target_stage['uiInfo']['stageType'] == 'EXECUTOR'
    ]
    first_job = jobs[0]
    postfix = int((datetime.utcnow().timestamp() * 1000 + postfix) if postfix else datetime.utcnow().timestamp() * 1000)

    if selected_topology_node and selected_topology_node['nodeType'] == 'SYSTEM':
        source_system_nodes = [selected_topology_node]
    else:
        for count, source_stage_instance in enumerate(source_stage_instances):
            source_system_node = copy.deepcopy(topology_node_json)
            source_system_node['nodeType'] = 'SYSTEM'
            source_system_node['instanceName'] = '{}:SYSTEM:{}'.format(source_stage_instance['instanceName'], postfix)
            source_system_node['library'] = source_stage_instance['library']
            source_system_node['stageName'] = source_stage_instance['stageName']
            source_system_node['stageVersion'] = source_stage_instance['stageVersion']
            source_system_node['jobId'] = first_job._data['id']
            source_system_node['pipelineId'] = first_job._data['pipelineId']
            source_system_node['pipelineCommitId'] = first_job._data['pipelineCommitId']
            source_system_node['pipelineVersion'] = pipeline['version']
            source_system_node['outputLanes'] = ['{}:LANE:1{}'.format(source_system_node['instanceName'], postfix)]
            source_system_node['uiInfo']['label'] = source_stage_instance['uiInfo']['label']
            source_system_node['uiInfo']['colorIcon'] = (
                source_stage_instance['uiInfo']['colorIcon'] if 'colorIcon' in source_stage_instance['uiInfo'] else ''
            )
            source_system_node['uiInfo']['xPos'] = x_pos
            source_system_node['uiInfo']['yPos'] = y_pos + (len(jobs) * 150) / 2 + +(count * 175)
            topology_nodes.append(source_system_node)
            source_system_nodes.append(source_system_node)

    for count, job in enumerate(jobs):
        job_node = copy.deepcopy(topology_node_json)
        job_node['nodeType'] = 'JOB'
        job_node['instanceName'] = '{}:JOB:{}{}'.format(source_stage_instances[0]['instanceName'], postfix, count)
        job_node['library'] = source_stage_instances[0]['library']
        job_node['stageName'] = source_stage_instances[0]['stageName']
        job_node['stageVersion'] = source_stage_instances[0]['stageVersion']
        job_node['jobId'] = job._data['id']
        job_node['pipelineId'] = job._data['pipelineId']
        job_node['pipelineCommitId'] = job._data['pipelineCommitId']
        job_node['pipelineVersion'] = pipeline['version']
        job_node['inputLanes'] = [node['outputLanes'][0] for node in source_system_nodes]
        job_node['uiInfo']['label'] = job._data['name']
        job_node['uiInfo']['xPos'] = x_pos + 220
        job_node['uiInfo']['yPos'] = y_pos + (len(target_stage_instances) * 150) / 2 + count * 150
        job_node['uiInfo']['outputStreamLabels'] = []
        job_node['uiInfo']['outputStreamTexts'] = []
        job_node['uiInfo']['statsAggr'] = (
            'statsAggregatorStage' in pipeline_definition
            and pipeline_definition['statsAggregatorStage']['stageName'] != stats_aggr_null_stage_name
            and pipeline_definition['statsAggregatorStage']['stageName'] != stats_aggr_dpm_stage_name
        )
        job_node['uiInfo']['executorType'] = job._data['executorType']
        topology_nodes.append(job_node)
        job_nodes.append(job_node)

    for count, target_stage_instance in enumerate(target_stage_instances):
        target_instance_name = target_stage_instance['instanceName']
        if target_stage_instance['stageName'] in [
            fragment_source_stage_name,
            fragment_processor_stage_name,
            fragment_target_stage_name,
        ]:
            fragment_id = target_stage_instance['uiInfo']['fragmentId']
            fragment_instance_id = target_stage_instance['uiInfo']['fragmentInstanceId']
            selected_fragment = next(
                (
                    fragment
                    for fragment in pipeline_definition['fragments']
                    if fragment['fragmentId'] == fragment_id and fragment['fragmentInstanceId'] == fragment_instance_id
                ),
                None,
            )
            if selected_fragment and 'stages' in selected_fragment and len(selected_fragment['stages']):
                target_instance_name = selected_fragment['stages'][0]['instanceName']
        new_output_lane = '{}:LANE:{}{}'.format(target_instance_name, postfix, count + 1)

        for job_node in job_nodes:
            job_node['outputLanes'].append(new_output_lane)
            job_node['uiInfo']['outputStreamLabels'].append(target_stage_instance['uiInfo']['label'])
            job_node['uiInfo']['outputStreamTexts'].append(target_stage_instance['uiInfo']['label'][0:1])
        target_system_node = copy.deepcopy(topology_node_json)
        target_system_node['nodeType'] = 'SYSTEM'
        target_system_node['instanceName'] = '{}:SYSTEM:{}'.format(target_stage_instance['instanceName'], postfix)
        target_system_node['library'] = target_stage_instance['library']
        target_system_node['stageName'] = target_stage_instance['stageName']
        target_system_node['stageVersion'] = target_stage_instance['stageVersion']
        target_system_node['jobId'] = first_job._data['id']
        target_system_node['pipelineId'] = first_job._data['pipelineId']
        target_system_node['pipelineCommitId'] = first_job._data['pipelineCommitId']
        target_system_node['pipelineVersion'] = pipeline['version']
        target_system_node['inputLanes'] = [new_output_lane]
        target_system_node['outputLanes'] = ['{}OutputLane1{}'.format(target_system_node['instanceName'], postfix)]
        target_system_node['uiInfo']['label'] = target_stage_instance['uiInfo']['label']
        target_system_node['uiInfo']['colorIcon'] = (
            target_stage_instance['uiInfo']['colorIcon'] if 'colorIcon' in target_stage_instance['uiInfo'] else ''
        )
        target_system_node['uiInfo']['xPos'] = x_pos + 500
        target_system_node['uiInfo']['yPos'] = y_pos + count * 175
        topology_nodes.append(target_system_node)

    if pipeline_definition['errorStage']:
        error_stage_instance = pipeline_definition['errorStage']
        new_output_lane = '{}:LANE:{}{}'.format(
            error_stage_instance['instanceName'], postfix, len(target_stage_instances) + 1
        )

        for job_node in job_nodes:
            job_node['outputLanes'].append(new_output_lane)
            job_node['uiInfo']['outputStreamLabels'].append(error_stage_instance['uiInfo']['label'])
            job_node['uiInfo']['outputStreamTexts'].append(error_stage_instance['uiInfo']['label'][0:1])
            job_node['uiInfo']['errorStreamIndex'] = len(target_stage_instances)
        error_system_node = copy.deepcopy(topology_node_json)
        error_system_node['nodeType'] = 'SYSTEM'
        error_system_node['instanceName'] = '{}:SYSTEM:{}'.format(error_stage_instance['instanceName'], postfix)
        error_system_node['library'] = error_stage_instance['library']
        error_system_node['stageName'] = error_stage_instance['stageName']
        error_system_node['stageVersion'] = error_stage_instance['stageVersion']
        error_system_node['jobId'] = first_job._data['id']
        error_system_node['pipelineId'] = first_job._data['pipelineId']
        error_system_node['pipelineCommitId'] = first_job._data['pipelineCommitId']
        error_system_node['pipelineVersion'] = pipeline['version']
        error_system_node['inputLanes'] = [new_output_lane]
        error_system_node['outputLanes'] = (
            ['{}OutputLane1{}'.format(error_system_node['instanceName'], postfix)]
            if error_stage_instance['stageName'] != error_discard_stage_name
            else []
        )
        error_system_node['uiInfo']['label'] = error_stage_instance['uiInfo']['label']
        error_system_node['uiInfo']['xPos'] = x_pos + 500
        error_system_node['uiInfo']['yPos'] = y_pos + len(target_stage_instances) * 175
        topology_nodes.append(error_system_node)

    return topology_nodes


def top_objects_by_metering_metric(metering_data, object_type, metric):
    if metric not in ['pipeline_hours', 'clock_hours', 'total_units']:
        raise ValueError('The metric provided must be pipeline_hours, clock_hours, or total_units.')
    metric_by_object = defaultdict(int)
    metric_index = metering_data['data']['columnNames'].index(METERING_METRIC_LOOKUP[metric])
    object_index = metering_data['data']['columnNames'].index(object_type)
    for item in metering_data['data']['report']:
        object_id = metering_data['data']['aliases'][item[object_index]][0]
        metric_by_object[object_id] += item[metric_index]
    return OrderedDict(
        [(key, value) for key, value in sorted(metric_by_object.items(), key=lambda key: key[1], reverse=True)]
    )


def create_aster_envelope(data):
    return {'data': data, 'version': 2}


def get_library_directory_name(lib, engine_type):
    if engine_type in ['DC', 'COLLECTOR']:
        return 'streamsets-datacollector-{}-lib'.format(lib)
    if engine_type in ['TF', 'TRANSFORMER']:
        return (
            'streamsets-transformer-{}-lib'.format(lib)
            if 'credentialstore' in lib
            else 'streamsets-spark-{}-lib'.format(lib)
        )


def get_attribute(config_definition):
    config_name = config_definition.get('name')
    config_label = config_definition.get('label')

    if config_label:
        replacements = [(r'[\s-]+', '_'), (r'&', 'and'), (r'/sec', '_per_sec'), (r'_\((.+)\)', r'_in_\1')]
        attribute_name = config_label.lower()
        for pattern, replacement in replacements:
            attribute_name = re.sub(pattern, replacement, attribute_name)
    else:
        attribute_name = inflection.underscore(config_definition['fieldName'])

    return attribute_name, config_name


def get_bw_compatibility_map(version, compatibility_maps):
    compatibility_map = {}
    # Scan the versions and add all override maps for versions lower than the current one.
    # This allows backward compatibility for more than one version.
    for map_version, override_dict in compatibility_maps.items():
        if Version(map_version) <= Version(version):
            compatibility_map.update(override_dict)

    return compatibility_map


def get_color_icon_from_stage_definition(stage_definition, stage_types):
    """Create `colorIcon` value from stage definition.
    Flow is mentioned in https://t.ly/xg4un

    E.g: stage_definitions: {'label': 'Dev Data Generator', 'type': 'SOURCE'}
         stage_types: {'origin': 'SOURCE', 'destination': 'TARGET', 'executor': 'EXECUTOR', 'processor': 'PROCESSOR'}
         should give output as: Origin_Dev_Data_Generator.png
                                <stage type>_<underscore joined stage label>.png

    Args:
        stage_definition (:py:obj:`dict`): stage definition from pipeline definitions
        stage_types (:py:obj:`dict`): A dict converting stage type between user and json representation

    Returns:
        A :py:obj:`str` with the file name for the stage's icon.
    """
    reversed_stage_types = reversed_dict(stage_types)

    if stage_definition.get('type') not in reversed_stage_types or not stage_definition.get('label'):
        return ''  # an empty string shows a greyed out image on the UI

    stage_processor_type = reversed_stage_types[stage_definition['type']].capitalize()

    # space or slash should be delimiters
    escaped_stage_labels = re.split(r' |/', stage_definition['label'])
    color_icon_name = '_'.join([stage_processor_type] + escaped_stage_labels) + '.png'

    return color_icon_name


def get_stage_library_display_name_from_library(stage_library_name, deployment_type):
    """Convert internal stage library name to display name.

    E.g: 'streamsets-spark-snowflake-with-no-dependency-lib:4.1.0' -> 'snowflake-with-no-dependency'

    Args:
        stage_library_name (:py:`str`): Stage library as stored in data for API calls/internally.
        deployment_type (:py:`str`): Deployment type that the library belongs to. "DC" or "TF".

    Returns:
        A :py:`str` with the display name of the stage library

    """
    if not isinstance(stage_library_name, str):
        raise TypeError("`stage_library_name` must be of type `str`")

    if not isinstance(deployment_type, str):
        raise TypeError("`deployment_type` must be of type `str`")

    accepted_deployment_types = [SDC_DEPLOYMENT_TYPE, TRANSFORMER_DEPLOYMENT_TYPE]
    if deployment_type not in accepted_deployment_types:
        raise ValueError("`deployment_type` should be in {}".format(accepted_deployment_types))

    try:
        if deployment_type == SDC_DEPLOYMENT_TYPE:
            return re.match(r'streamsets-datacollector-(.+)-lib.*', stage_library_name).group(1)
        else:
            return re.match(r'streamsets-(spark|transformer)-(.+)-lib.*', stage_library_name).group(2)
    except AttributeError:
        # Attribute error is raised when the regex cannot match the library name properly
        # This can occur because the library name is badly formed or because library name and deployment type
        # do not match and we check for an incorrect condition.
        raise ValueError(
            "Invalid `stage_library_name` sent to the function, make sure that it's formatted correctly"
            " and has the correct `deployment_type`"
        )


def get_stage_library_name_from_display_name(
    stage_library_display_name, deployment_type, deployment_engine_version=None
):
    """Convert a stage's display name to a library name used internally.

    E.g: 'aws:2.1.0', 'DC', None -> 'streamsets-datacollector-aws-lib:2.1.0'
         'aws', 'DC', '5.7.1' -> 'streamsets-datacollector-aws-lib:5.7.1'

    Args:
        stage_library_display_name (:py:`str`): Display name of the stage.
        deployment_type (:py:`str`): Deployment type that the library belongs to. "DC" or "TF".
        deployment_engine_version (:py:`str`, optional): Used for the library version when the version is not part of
                                                        the display name. Default: ``None``.

    Returns:
        A :py:`str` with the library name in the format we store internally.

    """
    if not isinstance(stage_library_display_name, str):
        raise TypeError("`stage_library_name` must be of type `str`")

    if not isinstance(deployment_type, str):
        raise TypeError("`deployment_type` must be of type `str`")

    accepted_deployment_types = [SDC_DEPLOYMENT_TYPE, TRANSFORMER_DEPLOYMENT_TYPE]
    if deployment_type not in accepted_deployment_types:
        raise ValueError("`deployment_type` should be in {}".format(accepted_deployment_types))

    parsed_display_name = stage_library_display_name.split(':')
    if len(parsed_display_name) > 1:
        # if the version is provided in the display name then we should use it
        lib_name = parsed_display_name[0]
        lib_version = parsed_display_name[1]

        # verify that version is valid
        Version(lib_version)
    elif not isinstance(deployment_engine_version, str):
        # ensure deployment version is provided
        raise TypeError(
            "`deployment_engine_version` of type `str` should be provided" " for library names without version."
        )
    else:
        # call version to ensure it's a valid version, will raise InvalidVersionError if incorrect
        Version(deployment_engine_version)

        lib_name = parsed_display_name[0]
        lib_version = deployment_engine_version

    if deployment_type == SDC_DEPLOYMENT_TYPE:
        return 'streamsets-datacollector-{}-lib:{}'.format(lib_name, lib_version)
    else:
        return (
            'streamsets-transformer-{}-lib:{}'.format(lib_name, lib_version)
            if 'credentialstore' in stage_library_display_name
            else 'streamsets-spark-{}-lib:{}'.format(lib_name, lib_version)
        )


def validate_pipeline_stages(pipeline):
    try:
        pipeline_builder = pipeline._get_builder()
    except (ValueError, InternalServerError) as e:
        raise ValueError(
            'Editing pipeline {} is not supported when the engine is not accessible,'
            ' please check if the engine is running and try again.'.format(pipeline.pipeline_id)
        ) from e

    pipeline_builder._update_stages_definition()

    engine_libraries = {stage['library'] for stage in pipeline_builder._definitions['stages']}
    for stage in pipeline.stages:
        if stage._data['library'] not in engine_libraries:
            raise ValueError("Stage {} does not exist within Engine Libraries".format(stage.instance_name))
