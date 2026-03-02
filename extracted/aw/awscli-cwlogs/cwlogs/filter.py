#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Amazon Software License (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/asl/
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from threading import Event
from datetime import datetime
import logging
from dateutil.tz import tzlocal
from six.moves import queue as Queue

from awscli.errorhandler import ServerError
from awscli.customizations.commands import BasicCommand
import cwlogs
from cwlogs import utils
from cwlogs.utils import print_stdout
from cwlogs.utils import print_stderr
from cwlogs.retry import ExponentialBackoff
from cwlogs.threads import BaseThread, ExitChecker
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def initialize(cli):
    """
    The entry point for CloudWatch Logs filter command.
    """
    cli.register('building-command-table.logs', inject_commands)


def inject_commands(command_table, session, **kwargs):
    """
    Called when the CloudWatch Logs command table is being built.
    Used to inject new high level commands into the command list.
    These high level commands must not collide with existing
    low-level API call names.
    """
    command_table['filter'] = LogsFilterCommand(session)


class LogsFilterCommand(BasicCommand):
    """
    """
    NAME = 'filter'
    DESCRIPTION = 'Filters log events that match a filter pattern.'
    SYNOPSIS = ''
    EXAMPLES = BasicCommand.FROM_FILE('logs', 'filter.rst', root_module=cwlogs)

    ARG_TABLE = [
        {'name': 'log-group-name', 'required': True,
         'help_text': 'Specifies the log group.'},
        {'name': 'log-stream-names',
         'schema': {'type': 'array', 'items': {'type': 'string'}},
         'help_text': 'Specifies the log streams to search within the group. '
                       'All the streams in the group are searched by default. '
                       'Syntax is: "streamName1" "streamName2" "streamName3" ...'},
        {'name': 'filter-pattern',
         'help_text': 'The filter pattern to filter for.'},
        {'name': 'interleaved',
          'action': 'store_true',
         'help_text': 'Whether or not these events are interleaved.'},
        {'name': 'start-time',
         'help_text': 'Optional value to specify start time of log events. '
                      'The value has to be in ISO8601 format '
                      '(YYYY-MM-DDThh:mm:ssZ). e.g. 2013-12-23T14:01:00Z'},
        {'name': 'end-time',
         'help_text': 'Optional value to specify end time of log events. '
                      'The value has to be in ISO8601 format '
                      '(YYYY-MM-DDThh:mm:ssZ). e.g. 2013-12-23T14:01:00Z'},
        {'name': 'output-format', 'default': '{logStreamName} {timestamp} {message}',
         'help_text': 'Optional value to specify the output format '
                      'of log events. Defaults to "{logStreamName} {timestamp} {message}". '
                      'Valid keys are logStreamName, timestamp, message and ingestionTime.'},
    ]

    UPDATE = False

    QUEUE_SIZE = 10

    def _run_main(self, args, parsed_globals):
        logging.basicConfig(level=logging.INFO)
        for handler in logging.root.handlers:
            handler.addFilter(logging.Filter(__name__))

        client_args = {
            'region_name': None,
            'verify': None
        }
        if parsed_globals.region is not None:
            client_args['region_name'] = parsed_globals.region
        if parsed_globals.verify_ssl is not None:
            client_args['verify'] = parsed_globals.verify_ssl
        if parsed_globals.endpoint_url is not None:
            client_args['endpoint_url'] = parsed_globals.endpoint_url
        # Initialize services and append cwlogs version to user agent
        self._session.user_agent_extra += 'cwlogs/' + cwlogs.__version__
        self.logs = self._session.create_client('logs', **client_args)
        # This unregister call will go away once the client switchover
        # is done, but for now we're relying on Logs catching a ClientError
        # when we check if a bucket exists, so we need to ensure the
        # botocore ClientError is raised instead of the CLI's error handler.
        self.logs.meta.events.unregister('after-call', unique_id='awscli-error-handler')
        # Run the command and report success
        self._call(args, parsed_globals)

        return 0

    def _call(self, options, parsed_globals):
        if options.start_time:
            try:
                start_time_in_ms = utils.iso8601_to_epoch(options.start_time)
            except ValueError as e:
                raise ValueError('%s. You must pass a valid start time to '
                                 ' --start-time' % e)
        else:
            start_time_in_ms = None

        if options.end_time:
            try:
                end_time_in_ms = utils.iso8601_to_epoch(options.end_time)
            except ValueError as e:
                raise ValueError('%s. You must pass a valid end time to '
                                 ' --end-time' % e)
        else:
            end_time_in_ms = None

        interleaved = True if options.interleaved is not None and options.interleaved is True else False

        logger.debug('Going to start event puller...')
        threads = []
        stop_flag = Event()
        queue = Queue.Queue(self.QUEUE_SIZE)
        puller = EventsPuller(stop_flag, queue,
                              self.logs,
                              options.log_group_name,
                              options.log_stream_names,
                              options.filter_pattern,
                              start_time_in_ms,
                              end_time_in_ms,
                              interleaved)
        puller.start()
        threads.append(puller)
        logger.debug('Going to start event renderer...')
        renderer = EventsRenderer(stop_flag, queue,
                                  options.output_format)
        renderer.start()
        threads.append(renderer)

        self._wait_on_exit(stop_flag)
        for thread in threads:
            try:
                thread.join()
            except:
                pass

    def _wait_on_exit(self, stop_flag):
        exit_checker = ExitChecker(stop_flag)
        exit_checker.start()
        try:
            while exit_checker.is_alive() and not stop_flag.is_set():
                exit_checker.join(5)
        except KeyboardInterrupt:
            pass
        logger.debug('Shutting down...')
        stop_flag.set()
        exit_checker.join()


class EventsPuller(BaseThread):
    def __init__(self, stop_flag, queue, logs_service, log_group_name,
                 log_stream_names, filter_pattern, start_time, end_time, interleaved):
        super(EventsPuller, self).__init__(stop_flag)
        self.queue = queue
        self.logs_service = logs_service
        self.log_group_name = log_group_name
        self.log_stream_names = log_stream_names
        self.filter_pattern = filter_pattern
        self.start_time = start_time
        self.end_time = end_time
        self.next_token = None
        self.interleaved = interleaved

    def on_run_failed(self, exception):
        self.stop_flag.set()
        logger.error("FilterLogEvents request failed")

    @ExponentialBackoff(logger=logger, exception=ClientError)
    def _run(self):
        params = dict(logGroupName=self.log_group_name,
                      interleaved=self.interleaved)

        if self.log_stream_names:
            params['logStreamNames'] = self.log_stream_names

        if self.filter_pattern is not None:
            params['filterPattern'] = self.filter_pattern

        while True:
            if self.stop_flag.is_set():
                logger.debug('Puller is leaving...')
                break

            logger.debug('Filtering log events with [%s] [%s] [%s] [%s]' %
                         (self.log_group_name,
                          self.log_stream_names,
                          self.filter_pattern,
                          self.next_token))

            if self.next_token:
                params['nextToken'] = self.next_token
            if self.start_time:
                params['startTime'] = self.start_time
            if self.end_time:
                params['endTime'] = self.end_time
            log_events_response = self.logs_service.filter_log_events(**params)
            if log_events_response:
                logger.debug('Adding %d log events to the queue' %
                             len(log_events_response.get('events')))
                self.next_token = log_events_response.get('nextToken')
                self.queue.put(EventBatch(self.log_group_name,
                                          self.log_stream_names,
                                          log_events_response.get('events'),
                                          log_events_response.get('searchedLogStreams')))
            if log_events_response.get('nextToken') is None:
                logger.debug('Filter complete.')
                self.stop_flag.set()
            else:
                logger.debug('Polling again.')
                self.stop_flag.wait(1/1000.0)


class EventsRenderer(BaseThread):
    def __init__(self, stop_flag, queue, output_format):
        super(EventsRenderer, self).__init__(stop_flag)
        self.queue = queue
        self.output_format = u''.join(output_format)

    def _run(self):
        total_searched_streams = set()
        while True:
            try:
                event_batch = self.queue.get(False)
                for event in event_batch.events:
                    revised_event = event.copy()
                    if event.get('timestamp') is not None:
                        revised_event['timestamp'] = \
                            datetime.fromtimestamp(event['timestamp']/1000.0,
                                                   tzlocal())
                    if event.get('ingestionTime') is not None:
                        revised_event['ingestionTime'] = \
                            datetime.fromtimestamp(
                                event['ingestionTime']/1000.0,
                                tzlocal())
                    print_stdout(self.output_format.format(**revised_event))
                if event_batch.searched_log_streams:
                    for searched_log_stream in event_batch.searched_log_streams:
                        total_searched_streams.add(searched_log_stream.get('logStreamName'))
                print_stderr("Searching for more data...")
            except Queue.Empty:
                if self.stop_flag.is_set():
                    print_stderr('{0} log streams searched in log group {1}:'.format(len(total_searched_streams), event_batch.log_group_name))
                    print_stderr(', '.join(sorted(total_searched_streams)))
                    logger.debug('Renderer is leaving...')
                    break
                else:
                    self.stop_flag.wait(0.1)


class EventBatch(object):
    def __init__(self, log_group_name, log_stream_names, events, searched_log_streams):
        self.log_group_name = log_group_name
        self.log_stream_names = log_stream_names
        self.events = events
        self.searched_log_streams = searched_log_streams
