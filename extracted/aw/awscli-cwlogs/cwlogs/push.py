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

from datetime import datetime, timedelta
import encodings
import glob
import gzip
import hashlib
import io
import logging
import logging.config
import os
import os.path
from operator import itemgetter
import re
import six
from six.moves import queue as Queue
from six.moves import configparser
import socket
from sys import stdin, exc_info
from threading import Event
from io import BytesIO

import requests
from botocore.exceptions import ClientError
from awscli.customizations.commands import BasicCommand
import cwlogs
from cwlogs.parser import DateTimeParser
from cwlogs import utils
from cwlogs.kvstore import KeyValueStore
from cwlogs.utils import get_current_millis, print_stdout, \
    validate_file_readable
from cwlogs.retry import ExponentialBackoff
from cwlogs.threads import BaseThread, ExitChecker

logger = logging.getLogger(__name__)
reader_logger = logging.getLogger(__name__ + '.reader')
publisher_logger = logging.getLogger(__name__ + '.publisher')
event_logger = logging.getLogger(__name__ + '.event')
batch_logger = logging.getLogger(__name__ + '.batch')
stream_logger = logging.getLogger(__name__ + '.stream')
watcher_logger = logging.getLogger(__name__ + '.watcher')

def initialize(cli):
    """
    The entry point for CloudWatch Logs push command.
    """
    cli.register('building-command-table.logs', inject_commands)


def inject_commands(command_table, session, **kwargs):
    """
    Called when the CloudWatch Logs command table is being built.
    Used to inject new high level commands into the command list.
    These high level commands must not collide with existing
    low-level API call names.
    """
    command_table['push'] = LogsPushCommand(session)

##
# A callback that comes on before-sign.logs.PutLogEvents. The intention is to compress the payload
# before going forward to reduce the cost spent in signing and transferring the payload.
##
def compress_request_payload(**kwargs):
    for name, value in kwargs.items():
        # Check for request entry
        if name == 'request':
            # Request has "data" that forms the body of the payload.
            # Compress it if the payload length is more than 1024 bytes.
            payload = value.__dict__['data']
            payload_length = len(payload)
            if payload_length > 1024:
                new_payload = compress_string(payload)
                new_payload_length = str(len(new_payload))
                value.__dict__['data'] = new_payload
                value.__dict__['headers']['Content-Encoding'] = "gzip"
                value.__dict__['headers']['Content-Length'] = new_payload_length
            break

##
# A utility method that gzips a given string
##
def compress_string(string):
    zbuf = BytesIO()
    zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf)
    zfile.write(string)
    zfile.close()
    return zbuf.getvalue()

class LogsPushCommand(BasicCommand):
    """
    """
    NAME = 'push'
    DESCRIPTION = ('Parses log events from standard input or files and puts '
                   'them into log stream(s) based on information specified in '
                   'a configuration file or arguments.')
    SYNOPSIS = ''
    EXAMPLES = BasicCommand.FROM_FILE('logs', 'push.rst', root_module=cwlogs)

    ENCODINGS = '''
        ascii big5 big5hkscs cp037 cp424 cp437 cp500 cp720 cp737 cp775 cp850
        cp852 cp855 cp856 cp857 cp858 cp860 cp861 cp862 cp863 cp864 cp865 cp866
        cp869 cp874 cp875 cp932 cp949 cp950 cp1006 cp1026 cp1140 cp1250 cp1251
        cp1252 cp1253 cp1254 cp1255 cp1256 cp1257 cp1258 euc_jp euc_jis_2004
        euc_jisx0213 euc_kr gb2312 gbk gb18030 hz iso2022_jp iso2022_jp_1
        iso2022_jp_2 iso2022_jp_2004 iso2022_jp_3 iso2022_jp_ext iso2022_kr
        latin_1 iso8859_2 iso8859_3 iso8859_4 iso8859_5 iso8859_6 iso8859_7
        iso8859_8 iso8859_9 iso8859_10 iso8859_13 iso8859_14 iso8859_15
        iso8859_16 johab koi8_r koi8_u mac_cyrillic mac_greek mac_iceland
        mac_latin2 mac_roman mac_turkish ptcp154 shift_jis shift_jis_2004
        shift_jisx0213 utf_32 utf_32_be utf_32_le utf_16 utf_16_be utf_16_le
        utf_7 utf_8 utf_8_sig
    '''

    ARG_TABLE = [
        {'name': 'config-file',
         'help_text': 'Specifies where and how to read the source files and '
                      'where to push the log events. If this is specified, '
                      'other arguments will be ignored except ``--dry-run``.'},
        {'name': 'additional-configs-dir',
         'help_text': 'Specifies a directory where supplemental configurations can '
                      'be added. When files exist in this directory, they will be '
                      'used in addition to the streams in the main config file, `config-file`. '
                      'Only additional stream configurations will be used from the additional '
                      'files in the directory. This parameter s ignored if no main '
                      'configuration file is provided using `config-file` as well.'},
        {'name': 'log-group-name',
         'help_text': 'Specifies the destination log group.'},
        {'name': 'log-stream-name',
         'help_text': 'Specifies the destination log stream.'},
        {'name': 'buffer-duration', 'cli_type_name': 'integer',
         'default': 5000,
         'help_text': 'A batch is buffered for ``--buffer-duration`` amount '
                      'of time. '
                      'Defaults to 5000 ms and its minimum value is 5000 ms.'},
        {'name': 'datetime-format',
         'help_text': 'Specifies how timestamp is extracted from log messages. '
                      'If it is not provided, the current time is used. '
                      'If the timestamp cannot be parsed from a given log message, '
                      'the timestamp from the previous log event is used if '
                      'a previous log event exists and had a timestamp. '
                      'Otherwise the current time is used. If you are using '
                      'stdin as input rather than a log file, the timestamp '
                      'will always fall back to current time if it cannot be'
                      'parsed. Check common formats in below examples '
                      'section.'},
        {'name': 'time-zone',
         'help_text': 'Specifies the time zone of log event timestamp. '
                      'This is used if time zone can\'t be inferred based on '
                      'datetime format. The two supported values are UTC and '
                      'LOCAL. Defaults to LOCAL.'},
        {'name': 'encoding',
         'help_text': 'Specifies the encoding of the source log event '
                      'messages. Defaults to utf_8. Available encodings '
                      'are ' + ', '.join(ENCODINGS.split())},
        {'name': 'dry-run', 'action': 'store_true',
         'help_text': 'Prints log events instead of sending them to '
                      'CloudWatch Logs.'},
        {'name': 'logging-config-file',
         'help_text': 'Configures how this command outputs its own log. '
                      'Supports Python logging config file format.'},
        {'name': 'no-gzip-http-content-encoding',
         'action': 'store_false',
         'dest': 'use_http_compression',
         'help_text': 'When set, explicitly disables gzip http content encoding on sent data, '
                      'which is enabled by default'},
    ]

    UPDATE = False
    # This is for the stdin reader
    QUEUE_SIZE = 10000

    def _run_main(self, args, parsed_globals):
        # enable basic logging initially. This will be overriden if a python logging config
        # file is provided in the agent config.
        logging.basicConfig(
            level=logging.INFO,
            format=('%(asctime)s - %(name)s - %(levelname)s - '
                    '%(process)d - %(threadName)s - %(message)s'))
        for handler in logging.root.handlers:
            handler.addFilter(logging.Filter('cwlogs'))

        # Parse a dummy string to bypass a bug before using strptime in thread
        # https://bugs.launchpad.net/openobject-server/+bug/947231
        datetime.strptime('2012-01-01', '%Y-%m-%d')
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
        # when we check if a stream exists, so we need to ensure the
        # botocore ClientError is raised instead of the CLI's error handler.
        self.logs.meta.events.unregister('after-call', unique_id='awscli-error-handler')
        self._validate_arguments(args)
        # Run the command and report success
        if args.config_file:
            self._call_push_file(args, parsed_globals)
        else:
            self._call_push_stdin(args, parsed_globals)

        return 0

    def _register_compression_handler(self):
        # Register handler for request compression.
        self.logs.meta.events.register('before-sign.{0}.{1}'
            .format('logs', 'PutLogEvents'), compress_request_payload, unique_id='compress_request_payload')


    def _validate_arguments(self, options):
        if options.config_file or (options.log_group_name and
                                   options.log_stream_name):
            return
        raise ValueError('You need to provide either --config-file '
                         'or both --log-group-name and --log-stream-name.')

    def _get_config(self, config_file, configs_dir):
        validate_file_readable(config_file)
        config = configparser.RawConfigParser(StreamConfig.DEFAULT_DICT)
        config.read(config_file)
        if not configs_dir:
            return config

        if os.path.isdir(configs_dir):
            files = os.listdir(configs_dir)
            for file_name in files:
                file_name = os.path.join(configs_dir, file_name)
                if os.path.isfile(file_name):
                    validate_file_readable(file_name)
                    logger.info("Loading additional configs from " + file_name)
                    subconfig = configparser.RawConfigParser(StreamConfig.DEFAULT_DICT)

                    try:
                        subconfig.read(file_name)
                    except Exception as e:
                        logger.warning("Failed to parse additional config file " + file_name + ": " + str(e))
                        continue

                    for section in subconfig.sections():
                        if config.has_section(section) or section == StreamConfig.GENERAL_SECTION:
                            continue
                        for option in subconfig.options(section):
                            if not config.has_section(section):
                                config.add_section(section)

                            config.set(section, option, subconfig.get(section, option))

        return config

    def _call_push_file(self, options, parsed_globals):
        stop_flag = Event()
        config = self._get_config(options.config_file, options.additional_configs_dir)
        state_file = config.get(StreamConfig.GENERAL_SECTION,
                                StreamConfig.STATE_FILE)
        logging_config_file = config.get(StreamConfig.GENERAL_SECTION,
                                         StreamConfig.LOGGING_CONFIG_FILE)
        try:
            use_http_compression = config.getboolean(StreamConfig.GENERAL_SECTION, StreamConfig.USE_HTTP_COMPRESSION)
            if use_http_compression == None:
                use_http_compression = True
        except (configparser.NoOptionError, ValueError):
            logger.info("Missing or invalid value for use_gzip_http_content_encoding config. Defaulting to use gzip encoding.")
            use_http_compression = True
        if use_http_compression:
            self._register_compression_handler()

        try:
            queue_size = config.getint(StreamConfig.GENERAL_SECTION, StreamConfig.QUEUE_SIZE)
            if queue_size is None:
                queue_size = StreamConfig.DEFAULT_QUEUE_SIZE
        except (configparser.NoOptionError, ValueError):
            logger.info('Missing or invalid value for queue_size config. Defaulting to use {0}'.format(
                StreamConfig.DEFAULT_QUEUE_SIZE))
            queue_size = StreamConfig.DEFAULT_QUEUE_SIZE

        self._config_logging(logging_config_file)
        watcher = Watcher(stop_flag, self.logs, state_file, options.dry_run)
        for section in config.sections():
            if section == StreamConfig.GENERAL_SECTION:
                continue
            stream_config = StreamConfig(config, section)
            stream_config.state_file = state_file
            watcher.register(stream_config, queue_size)
        watcher.start()
        self._wait_on_exit(stop_flag)
        watcher.join()

    def _call_push_stdin(self, options, parsed_globals):
        self._config_logging(options.logging_config_file)
        time_zone = options.time_zone
        if time_zone:
            if time_zone not in [StreamConfig.TIME_ZONE_UTC,
                                 StreamConfig.TIME_ZONE_LOCAL]:
                logger.warning('The time zone \'%s\' is unknown, using '
                               'default time zone (%s)' %
                               (time_zone,
                                StreamConfig.TIME_ZONE_LOCAL))
                time_zone = StreamConfig.TIME_ZONE_LOCAL
        else:
            time_zone = StreamConfig.TIME_ZONE_LOCAL
        encoding = options.encoding
        if encoding:
            if encodings.search_function(encoding) is None:
                logger.warning('The encoding \'%s\' is unknown, using '
                               'default encoding (%s)' %
                               (encoding, StreamConfig.DEFAULT_ENCODING))
                encoding = StreamConfig.DEFAULT_ENCODING
        else:
            encoding = StreamConfig.DEFAULT_ENCODING

        use_http_compression = options.use_http_compression
        if use_http_compression:
            self._register_compression_handler()

        threads = []
        queue = Queue.Queue(self.QUEUE_SIZE)
        stop_flag = Event()
        reader = StandardInputEventsReader(stop_flag, queue,
                                           options.datetime_format,
                                           time_zone,
                                           encoding)
        reader.start()
        threads.append(reader)
        publisher = EventsPublisher(stop_flag, queue, self.logs,
                                    options.log_group_name,
                                    options.log_stream_name,
                                    int(options.buffer_duration),
                                    options.dry_run)
        publisher.start()
        threads.append(publisher)
        self._wait_on_exit(stop_flag)
        reader.join()
        publisher.join()

    def _wait_on_exit(self, stop_flag):
        exit_checker = ExitChecker(stop_flag)
        exit_checker.start()
        try:
            while exit_checker.is_alive() and not stop_flag.is_set():
                exit_checker.join(5)
        except KeyboardInterrupt:
            pass
        logger.info('Shutting down...')
        stop_flag.set()
        exit_checker.join()

    def _config_logging(self, logging_config_file):
        if logging_config_file:
            try:
                logging.config.fileConfig(logging_config_file)
                logger.debug("Loaded logging configurations from file " + logging_config_file)
                return
            except Exception as e:
                logger.warning('Detected wrong logging config: ' + str(e))
        logger.info('Using default logging configuration.')


class StreamConfig(object):
    GENERAL_SECTION = 'general'
    STATE_FILE = 'state_file'
    DEFAULT_STATE_FILE = 'watchstate'
    LOGGING_CONFIG_FILE = 'logging_config_file'
    FILE = 'file'
    LOG_GROUP_NAME = 'log_group_name'
    LOG_STREAM_NAME = 'log_stream_name'
    DATETIME_FORMAT = 'datetime_format'
    USE_HTTP_COMPRESSION = 'use_gzip_http_content_encoding'
    QUEUE_SIZE = 'queue_size'
    DEFAULT_QUEUE_SIZE = 10
    TIME_ZONE = 'time_zone'
    TIME_ZONE_UTC = 'UTC'
    TIME_ZONE_LOCAL = 'LOCAL'
    BUFFER_DURATION = 'buffer_duration'
    DEFAULT_BUFFER_DURATION = 5000
    MIN_BUFFER_DURATION = 5000
    HOSTNAME_PLACEHOLDER = '{hostname}'
    INSTANCE_ID_PLACEHOLDER = '{instance_id}'
    IP_ADDRESS_PLACEHOLDER = '{ip_address}'
    INSTANCE_ID_URL = 'http://169.254.169.254/latest/meta-data/instance-id'
    # where to start to read file
    INITIAL_POSITION = 'initial_position'
    INIT_POS_EOF = 'end_of_file'
    INIT_POS_SOF = 'start_of_file'
    ENCODING = 'encoding'
    DEFAULT_ENCODING = 'utf_8'
    # line number or range, e.g.
    # 2: use 2nd line as file fingerprint
    # 2-4: use 2nd to 4th (inclusive) lines as file fingerprint
    FILE_FINGERPRINT_LINES = 'file_fingerprint_lines'
    DEFAULT_FILE_FINGERPRINT_LINES = '1'
    MULTI_LINE_START_PATTERN = 'multi_line_start_pattern'
    DEFAULT_MULTI_LINE_START_PATTERN = '^[^\s]'
    BATCH_SIZE = 'batch_size'
    MAX_BATCH_SIZE = 1024 * 1024
    DEFAULT_BATCH_SIZE = MAX_BATCH_SIZE
    BATCH_COUNT = 'batch_count'
    MAX_BATCH_COUNT = 10000
    DEFAULT_BATCH_COUNT = MAX_BATCH_COUNT
    DEFAULT_DICT = {
        STATE_FILE: DEFAULT_STATE_FILE,
        LOGGING_CONFIG_FILE: None,
        DATETIME_FORMAT: None,
        ENCODING: DEFAULT_ENCODING,
        INITIAL_POSITION: INIT_POS_SOF,
        BUFFER_DURATION: DEFAULT_BUFFER_DURATION,
        TIME_ZONE: TIME_ZONE_LOCAL,
        FILE_FINGERPRINT_LINES: DEFAULT_FILE_FINGERPRINT_LINES,
        MULTI_LINE_START_PATTERN: DEFAULT_MULTI_LINE_START_PATTERN,
        BATCH_COUNT: DEFAULT_BATCH_COUNT,
        BATCH_SIZE: DEFAULT_BATCH_SIZE
    }

    def __init__(self, config, section):
        self.stream_key = section
        self.state_file = None
        self.path_to_file = config.get(section, self.FILE)
        self.file_fingerprint_lines = config.get(section,
                                                 self.FILE_FINGERPRINT_LINES)
        self.log_group_name = self._normalize(config.get(section,
                                                         self.LOG_GROUP_NAME))
        self.log_stream_name = self._normalize(config.get(section,
                                                          self.LOG_STREAM_NAME))
        self.dt_format = config.get(section, self.DATETIME_FORMAT)
        dt_parser = None
        if self.dt_format:
            try:
                dt_parser = DateTimeParser(self.dt_format)
            except:
                logger.warning('The datetime format (%s) is invalid, '
                               'will use current time.' %
                               self.dt_format)
                self.dt_format = None

        self.time_zone = config.get(section, self.TIME_ZONE)
        if self.time_zone and \
            self.time_zone not in [self.TIME_ZONE_UTC,
                                   self.TIME_ZONE_LOCAL]:
            logger.warning('The time zone \'%s\' is unknown, using '
                           'default time zone (%s)' %
                           (self.time_zone, self.TIME_ZONE_LOCAL))
            self.time_zone = self.TIME_ZONE_LOCAL

        try:
            self.buffer_duration = config.getint(section, self.BUFFER_DURATION)
        except ValueError:
            logger.warning('The buffer duration \'%s\' is invalid, using '
                           'default buffer duration (%d)' %
                           (config.get(section, self.BUFFER_DURATION),
                            self.DEFAULT_BUFFER_DURATION))
            self.buffer_duration = self.DEFAULT_BUFFER_DURATION
        if self.buffer_duration < StreamConfig.MIN_BUFFER_DURATION:
            logger.warning(
                'The buffer_duration is set to MIN_BUFFER_DURATION '
                '(%s)', StreamConfig.MIN_BUFFER_DURATION)
            self.buffer_duration = StreamConfig.MIN_BUFFER_DURATION

        self.init_pos = config.get(section, self.INITIAL_POSITION)
        if self.init_pos not in [self.INIT_POS_EOF, self.INIT_POS_SOF]:
            logger.warning('The initial position \'%s\' is unknown, using '
                           'default initial position (%s)' %
                           (self.init_pos, self.INIT_POS_SOF))
            self.init_pos = self.INIT_POS_SOF

        self.encoding = config.get(section, self.ENCODING)
        if encodings.search_function(self.encoding) is None:
            logger.warning('The encoding \'%s\' is unknown, using '
                           'default encoding (%s)' %
                           (self.encoding, self.DEFAULT_ENCODING))
            self.encoding = self.DEFAULT_ENCODING

        if self.file_fingerprint_lines and \
            re.match(six.u('^[1-9]+[0-9]*-?[0-9]*$'),
                     self.file_fingerprint_lines) is None:
            logger.warning('The file fingerprint lines \'%s\' is invalid, '
                           'using first line to calculate file fingerprint' %
                           (self.file_fingerprint_lines))
            self.file_fingerprint_lines = self.DEFAULT_FILE_FINGERPRINT_LINES

        self.multi_line_start_pattern = config.get(
            section, self.MULTI_LINE_START_PATTERN)
        self.ignore_pattern_case = False
        if self.multi_line_start_pattern == '{datetime_format}':
            if dt_parser:
                self.multi_line_start_pattern = dt_parser.dt_re.pattern
                self.ignore_pattern_case = True
            else:
                logger.warning('The multi-line start pattern uses '
                               '{datetime_format} but datetime_format is '
                               'invalid or not specified.')
                self.multi_line_start_pattern = \
                    self.DEFAULT_MULTI_LINE_START_PATTERN
        elif self.multi_line_start_pattern:
            try:
                re.compile(self.multi_line_start_pattern)
            except:
                logger.warning('The multi-line start pattern \'%s\' is '
                               'invalid, using default pattern (%s)' %
                               (self.multi_line_start_pattern,
                                self.DEFAULT_MULTI_LINE_START_PATTERN))
                self.multi_line_start_pattern = \
                    self.DEFAULT_MULTI_LINE_START_PATTERN
        else:
            self.multi_line_start_pattern = \
                self.DEFAULT_MULTI_LINE_START_PATTERN

        try:
            self.batch_size = config.getint(section, self.BATCH_SIZE)
        except ValueError:
            logger.warning('The batch size \'%s\' is invalid, using '
                           'default batch size (%d)' %
                           (config.get(section, self.BATCH_SIZE),
                            self.DEFAULT_BATCH_SIZE))
            self.batch_size = self.DEFAULT_BATCH_SIZE
        if self.batch_size > StreamConfig.MAX_BATCH_SIZE:
            logger.warning(
                'The batch size is set to MAX_BATCH_SIZE '
                '(%s)', StreamConfig.MAX_BATCH_SIZE)
            self.batch_size = StreamConfig.MAX_BATCH_SIZE

        try:
            self.batch_count = config.getint(section, self.BATCH_COUNT)
        except ValueError:
            logger.warning('The batch count \'%s\' is invalid, using '
                           'default batch count (%d)' %
                           (config.get(section, self.BATCH_COUNT),
                            self.DEFAULT_BATCH_COUNT))
            self.batch_count = self.DEFAULT_BATCH_COUNT
        if self.batch_count > StreamConfig.MAX_BATCH_COUNT:
            logger.warning(
                'The batch size is set to MAX_BATCH_COUNT '
                '(%s)', StreamConfig.MAX_BATCH_COUNT)
            self.batch_count = StreamConfig.MAX_BATCH_COUNT

    def _normalize(self, place_holder_str):
        if re.search(self.INSTANCE_ID_PLACEHOLDER, place_holder_str):
            instance_id = self._instance_id()
            if not instance_id:
                instance_id = (socket.gethostname() or
                               socket.gethostbyname(socket.gethostname()))
                logger.warning('Unable to get instance id, use %s instead.',
                               instance_id)
            place_holder_str = self._sub_placeholder(
                place_holder_str,
                self.INSTANCE_ID_PLACEHOLDER,
                instance_id)
        if re.search(self.HOSTNAME_PLACEHOLDER, place_holder_str):
            hostname = (socket.gethostname() or
                        socket.gethostbyname(socket.gethostname()))
            place_holder_str = self._sub_placeholder(
                place_holder_str,
                self.HOSTNAME_PLACEHOLDER,
                hostname)
        if re.search(self.IP_ADDRESS_PLACEHOLDER, place_holder_str):
            place_holder_str = self._sub_placeholder(
                place_holder_str,
                self.IP_ADDRESS_PLACEHOLDER,
                socket.gethostbyname(socket.gethostname()))
        return place_holder_str

    def _sub_placeholder(self, place_holder_str, placeholder, value):
        if value is None:
            raise ValueError('Substituting %s with empty value is not '
                             'allowed.' % placeholder)
        return place_holder_str.replace(placeholder, value)

    def _instance_id(self):
        try:
            # Times out after 5 seconds
            response = requests.get(self.INSTANCE_ID_URL, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception:
            return None

class Watcher(BaseThread):
    """
    Watch all streams periodically and keep streams alive.
    """

    def __init__(self, stop_flag, logs, state_file, dry_run=False):
        super(Watcher, self).__init__(stop_flag)
        self.streams = []
        self.logs = logs
        self.dry_run = dry_run
        # Create push_state table
        KeyValueStore(db=state_file, table='push_state').close()
        KeyValueStore(db=state_file, table='stream_state').close()

    def register(self, config, queue_size=StreamConfig.DEFAULT_QUEUE_SIZE):
        stream = Stream(config, queue_size)
        stream.stop_flag = self.stop_flag
        stream.logs = self.logs
        stream.dry_run = self.dry_run
        self.streams.append(stream)

    def _run(self):
        while True:
            if self._exit_needed():
                watcher_logger.info('Watcher is leaving...')
                break
            for stream in self.streams:
                try:
                    if stream.validate():
                        stream.refresh()
                except Exception as e:
                    stream.restart_time = (datetime.utcnow() +
                                           timedelta(seconds=60))
                    watcher_logger.error(
                        'Failed to refresh stream: %s, reason: %r.',
                        stream.debug_fields(), e)
            # sleep 5s
            self.stop_flag.wait(5)

        for stream in self.streams:
            stream.join()


class Stream(object):

    def __init__(self, config, queue_size=StreamConfig.DEFAULT_QUEUE_SIZE):
        self.state_file = config.state_file
        self.stream_key = config.stream_key
        self.file = config.path_to_file
        self.file_fingerprint_lines = config.file_fingerprint_lines
        self.multi_line_start_pattern = config.multi_line_start_pattern
        self.ignore_pattern_case = config.ignore_pattern_case
        self.log_group_name = config.log_group_name
        self.log_stream_name = config.log_stream_name
        self.dt_format = config.dt_format
        self.time_zone = config.time_zone
        self.buffer_duration = config.buffer_duration
        self.init_pos = config.init_pos
        self.encoding = config.encoding
        self.batch_count = config.batch_count
        self.batch_size = config.batch_size
        self.queue_size = queue_size
        self.queue = Queue.Queue(queue_size)
        self.group_stop_flag = Event()
        self.readers = dict()
        self.publisher = None
        self.source_id = None
        self.stop_flag = None
        # restart_time is set if refreshing a stream causes exception.
        self.restart_time = None
        self.logs = None
        self.dry_run = None
        self.open = open
        # the state of a file belonging to one stream
        self.state_store = KeyValueStore(db=self.state_file,
                                         table='push_state')
        # the state of a stream
        self.stream_store = KeyValueStore(db=self.state_file,
                                          table='stream_state')
        self.stream_state = self.stream_store.get(self.stream_key)

    def validate(self):
        if not self.log_group_name:
            raise ValueError('The log_group_name can not be blank')
        if not self.log_stream_name:
            raise ValueError('The log_stream_name can not be blank')
        return True

    def refresh(self):
        """
        Keep the stream alive and manage the lifecycle of reader/publisher

        * Handle file rotation
        * Remove dead reader/publisher and start new ones
        """
        if self.restart_time:
            if self.restart_time > datetime.utcnow():
                return
            else:
                self.restart_time = None
        self._clean_up()
        (source_id, source_file) = self._source_file(self.file)
        if source_id is None or source_file is None:
            return
        if self.source_id == source_id:
            return
        if self.group_stop_flag.is_set():
            # do not start reader/publisher while the flag is set.
            # the clean_up method resets this flag once both reader
            # and publisher are cleared.
            return
        if self.publisher is None:
            # there is no publisher yet
            stream_logger.info(
                'Starting publisher for [%s, %s]', source_id, source_file)
            publisher = EventBatchPublisher(self.stop_flag,
                                            self.queue,
                                            self.logs,
                                            self.log_group_name,
                                            self.log_stream_name,
                                            self.dry_run)
            publisher.group_stop_flag = self.group_stop_flag
            publisher.register_publish_callback(
                self._record_state)
            publisher.start()
            self.publisher = publisher
        if self.readers:
            # file has been rotated. Let reader exit.
            stream_logger.info('Detected file rotation, notifying reader')
            reader = self.readers[self.source_id]
            reader.exiting = True
            # do not start a new reader unless the old one has
            # finished reading the old file.
            if reader and reader.is_alive():
                stream_logger.info('Reader is still alive.')
                return
        # set up stream state if this is the first time to process this stream
        if self.stream_state is None:
            with open(source_file, 'rb') as fo:
                if self.init_pos == StreamConfig.INIT_POS_EOF:
                    fo.seek(0, os.SEEK_END)
                self.stream_store.save(self.stream_key,
                                       dict(source_id=source_id,
                                            initial_position=fo.tell()))
            self.stream_state = self.stream_store.get(self.stream_key)
        # the file might be processed before, use last position
        push_state = self.state_store.get(source_id)
        stream_logger.info(
            'Starting reader for [%s, %s]', source_id, source_file)
        reader = FileEventBatchReader(source_id,
                                      self.stop_flag,
                                      self.queue,
                                      self.dt_format,
                                      self.time_zone,
                                      source_file,
                                      push_state,
                                      self.stream_state,
                                      self.encoding,
                                      self.buffer_duration,
                                      self.batch_count,
                                      self.batch_size,
                                      self.multi_line_start_pattern,
                                      self.ignore_pattern_case)
        reader.group_stop_flag = self.group_stop_flag
        reader.start()
        self.readers[source_id] = reader
        self.source_id = source_id

    def _clean_up(self):
        # clean up dead readers
        to_be_deleted = []
        for source_id in self.readers.keys():
            if not self.readers[source_id].is_alive():
                to_be_deleted.append(source_id)
        for source_id in to_be_deleted:
            stream_logger.info(
                'Removing dead reader [%s, %s]',
                source_id, self.readers[source_id].file)
            del self.readers[source_id]
            # TODO: need to clean up old states
        if len(self.readers) > 1:
            stream_logger.warning('Found %d readers running' % len(self.readers))
        # clean up publisher
        if self.publisher and not self.publisher.is_alive():
            stream_logger.info(
                'Removing dead publisher [%s, %s]', self.source_id, self.file)
            self.publisher = None
        # reset stop flag and queue once cleaning up all readers and publisher
        if not self.publisher and not self.readers and \
                self.group_stop_flag.is_set():
            self.source_id = None
            self.group_stop_flag.clear()
            self.queue = Queue.Queue(self.queue_size)

    def join(self):
        for reader in self.readers.values():
            reader.join()
        if self.publisher:
            self.publisher.join()
        self.state_store.close()
        self.stream_store.close()

    def _record_state(self, event_batch, sequence_token):
        state = dict(
            source_id=event_batch.source_id,
            start_position=event_batch.first_event.start_position,
            end_position=event_batch.last_event.end_position,
            batch_timestamp=event_batch.batch_timestamp,
            first_timestamp=event_batch.first_event.timestamp,
            first_timestamp_status=event_batch.first_event.event_timestamp_status,
            sequence_token=sequence_token)
        stream_logger.debug('Saved state: %s', state)
        if not self.dry_run:
            self.state_store.save(event_batch.source_id, state)

    def _source_file(self, path):
        """
        Return source id and source file based on ``path``.

        A file might be rotated in different ways and new data will go to
        different places based on what rotation mechanism is used. This class
        detects the file rotation and starts a reader if needed.
        1) old file is renamed and a new file is created with same file name.
        2) old file is copied and then truncated.
        3) old file remains the same name, and a new file is created.
        Old and new file share a common pattern.
        """
        # sort files by mtime in reverse order
        files = sorted(filter(os.path.isfile, glob.glob(path)),
                       key=os.path.getmtime,
                       reverse=True)
        if not files:
            stream_logger.warning("No file is found with given path '%s'.", path)
            return (None, None)
        for f in files:
            if os.path.splitext(f)[1] in ['.tar', '.gz', '.zip', '.bz2', '.rar']:
                stream_logger.info("Ignoring archived/compressed file '%s'.", f)
            else:
                return (self._calc_file_fingerprint(f), f)
        return (None, None)

    def _calc_file_fingerprint(self, source_file):
        """
        Calculate the file fingerprint based on file content which is specified
        by the file_fingerprint_lines variable.
        Return None if the specified lines are not available.

        Note that the log stream key (section name) is also used to calc
        file fingerprint so one file can be configured in multiple log streams.
        """
        line_ranges = self.file_fingerprint_lines.split('-')
        if len(line_ranges) == 2:
            start_line, end_line = int(line_ranges[0]), int(line_ranges[1])
        elif len(line_ranges) == 1:
            start_line, end_line = int(line_ranges[0]), int(line_ranges[0])

        with self.open(source_file, 'rb') as f:
            line_num = 1
            fingerprint_lines = []
            while line_num <= end_line:
                line = f.readline()
                if line:
                    if line_num >= start_line:
                        fingerprint_lines.append(line)
                else:
                    return None
                line_num += 1
            if fingerprint_lines:
                # scope file by stream key in case a file is configured
                # by multiple streams
                source_id_val = (self.stream_key.encode('utf_8') +
                                 six.b('').join(fingerprint_lines))
                return hashlib.md5(source_id_val).hexdigest()
        return None

    def debug_fields(self):
        return dict(file=self.file, source_id=self.source_id,
                    log_group_name=self.log_group_name,
                    log_stream_name=self.log_stream_name,
                    datetime_format=self.dt_format,
                    time_zone=self.time_zone,
                    buffer_duration=self.buffer_duration,
                    init_pos=self.init_pos,
                    encoding=self.encoding,
                    queue=self.queue and self.queue.qsize())


class FileEventsReader(BaseThread):
    def __init__(self, source_id, stop_flag, queue, dt_format, time_zone,
                 file, push_state, stream_state, encoding,
                 multi_line_start_pattern=None, ignore_pattern_case=False):
        super(FileEventsReader, self).__init__(stop_flag)
        self.source_id = source_id
        self.queue = queue
        if dt_format:
            self.dt_parser = DateTimeParser(dt_format, time_zone)
        else:
            self.dt_parser = None
        validate_file_readable(file)
        self.file = file
        self.push_state = push_state
        self.stream_state = stream_state
        self.encoding = encoding
        self.exiting = False
        self.open = io.open
        self.temp_line = six.b('')
        # Temp event is an event that hasn't been added to the queue.
        self.temp_event = None
        self.prev_event = None
        if multi_line_start_pattern:
            if ignore_pattern_case:
                # Ignore case if the regex is converted from datetime_format
                # because the regex only matches lower case month
                self.multi_line_start_matcher = re.compile(
                    six.b(multi_line_start_pattern), re.IGNORECASE)
            else:
                # Use case sensitive for configured regex
                self.multi_line_start_matcher = re.compile(
                    six.b(multi_line_start_pattern))
        else:
            self.multi_line_start_matcher = re.compile(
                six.b('^[^\s]'))

    def _push_event(self, force=False):
        if self.temp_event is None:
            return
        if not self.temp_event.complete():
            if self.temp_event.event_timestamp_status == \
                    EventTimestampStatus.FALLBACK_CURRENT_TIME:
                reader_logger.warning(
                    'Fall back to current time: %s, reason: %s.',
                    self.temp_event.debug_fields(),
                    'timestamp could not be parsed from message')
            else:
                reader_logger.warning(
                    'Fall back to previous event time: %s, '
                    'previousEventTime: %s, reason: %s.',
                    self.temp_event.debug_fields(),
                    self.temp_event.prev_timestamp,
                    'timestamp could not be parsed from message')
        while True:
            try:
                self.queue.put(self.temp_event, False)
                break
            except Queue.Full:
                if self._exit_needed():
                    return
                else:
                    self.stop_flag.wait(5)
        self.prev_event = self.temp_event
        self.temp_event = None

    def _is_new_entry(self, message):
        return self.multi_line_start_matcher.search(message) is not None

    def _locate_initial_position(self, fo):
        # if push state exists, the source file was processed before
        if self.push_state:
            fo.seek(self.push_state['start_position'])

            # Only the timestamp and the timestamp status is important
            first_timestamp_status = None
            if 'first_timestamp_status' in self.push_state:
                first_timestamp_status = self.push_state['first_timestamp_status']

            self.prev_event = LogEvent(
                timestamp=self.push_state['first_timestamp'],
                event_timestamp_status=first_timestamp_status)
            reader_logger.info(
                'Replay events end at %d.', self.push_state['end_position'])
        # otherwise if stream state exists
        elif self.stream_state:
            # and source id is the same as persisted one,
            # use persisted position
            if self.stream_state['source_id'] == self.source_id:
                fo.seek(self.stream_state['initial_position'])
            # from start of file for following files belonging to this stream
            else:
                fo.seek(0)
        else:
            reader_logger.warning(
                'Both stream state and push state are not available.')
            fo.seek(0)
        reader_logger.info('Start reading file from %d.' % fo.tell())

    def _run(self):

        # Var life cycle: data -> temp_line -> line -> temp_event -> event

        # Opening file in binary mode. Don't use text mode because
        # TextIOWrapper.tell is slow
        # (https://docs.python.org/3.1/library/io.html#id3) and
        # buggy (http://stackoverflow.com/questions/24481276).
        # The drawback is that readline returns lines separated by '\n'
        # so '\r' is not supported.
        with self.open(self.file, mode='rb') as fo:
            self._locate_initial_position(fo)
            temp_line_start_pos = 0
            while True:
                if self._exit_needed():
                    reader_logger.info('Reader is leaving as requested...')
                    self._push_event()
                    break
                curr_position = fo.tell()
                if not self.temp_line:
                    temp_line_start_pos = curr_position
                # Might read partial line
                data = fo.readline()
                if not data:
                    self._push_event()
                    if self.exiting:
                        # force to push batch and leave
                        self._push_event(force=True)
                        reader_logger.info('No data is left. Reader is leaving.')
                        return
                    else:
                        self.stop_flag.wait(1)
                    fo.seek(curr_position)
                elif not data.endswith(six.b('\n')):
                    self.temp_line += data
                    continue
                else:
                    self.temp_line += data
                    # Can't use universal new line when opening file in
                    # binary mode
                    line = self.temp_line.rstrip(six.b('\r\n'))
                    if self.temp_event and not self._is_new_entry(line):
                        self.temp_event.append_message(line)
                        self.temp_event.end_position = fo.tell()
                    else:
                        self._push_event()
                        end_position = fo.tell()
                        self.temp_event = self._create_log_event(
                            line,
                            temp_line_start_pos,
                            end_position)
                    self.temp_line = six.b('')

    def _create_log_event(self, message, start_position, end_position):
        event = LogEvent(
            message=message,
            start_position=start_position,
            end_position=end_position,
            source_id=self.source_id,
            dt_parser=self.dt_parser,
            prev_event=self.prev_event,
            encoding=self.encoding)
        if self.push_state:
            delta = self.push_state['end_position'] - end_position
            if delta >= 0:
                event.is_replay = (delta >= 0)
                event.is_last_replay = (delta == 0)
                event.batch_timestamp = self.push_state['batch_timestamp']
                event.sequence_token = self.push_state['sequence_token']
        return event


class FileEventBatchReader(FileEventsReader):
    def __init__(self, source_id, stop_flag, queue, dt_format, time_zone,
                 file, push_state, stream_state, encoding,
                 buffer_duration, batch_count, batch_size,
                 multi_line_start_pattern=None, ignore_pattern_case=False):
        super(FileEventBatchReader, self).__init__(
                source_id, stop_flag, queue, dt_format, time_zone,
                file, push_state, stream_state, encoding,
                multi_line_start_pattern, ignore_pattern_case)
        self.buffer_duration = buffer_duration
        self.batch_count = batch_count
        self.batch_size = batch_size
        self.event_batch = None

    def _push_event(self, force=False):
        is_batch_full = False
        if self.temp_event:
            if not self.temp_event.complete():
                if self.temp_event.event_timestamp_status == \
                        EventTimestampStatus.FALLBACK_CURRENT_TIME:
                    reader_logger.warning(
                        'Fall back to current time: %s, reason: %s. ',
                        self.temp_event.debug_fields(),
                        'timestamp could not be parsed from message')
                else:
                    reader_logger.warning(
                        'Fall back to previous event time: %s, '
                        'previousEventTime: %s, reason: %s.',
                        self.temp_event.debug_fields(),
                        self.temp_event.prev_timestamp,
                        'timestamp could not be parsed from message')

            if self._add_event(self.temp_event) == 0:
                is_batch_full = True

        if is_batch_full or \
                (self.event_batch and self.event_batch.should_batch_be_published()) or \
                (force and self.event_batch and len(self.event_batch.events) > 0):
            while True:
                try:
                    # every batch in the queue should be published by publisher
                    # so set force_publish to true to skip the check on publisher side
                    self.event_batch.force_publish = True
                    self.queue.put(self.event_batch, False)
                    self.event_batch = None
                    break
                except Queue.Full:
                    if self._exit_needed():
                        return
                    else:
                        self.stop_flag.wait(1)
            if is_batch_full:
                self._add_event(self.temp_event)
                # Push the last event
                if force:
                    self.temp_event = None
                    self._push_event(force=True)
                    return
        if self.temp_event:
            self.prev_event = self.temp_event
            self.temp_event = None

    def _add_event(self, event):
        """
        Add event to batch and start the first batch if it doesn't exist
        """
        if self.event_batch is None:
            self.event_batch = EventBatch(self.buffer_duration, self.batch_count, self.batch_size)
        return self.event_batch.add_event(event)


class StandardInputEventsReader(BaseThread):
    def __init__(self, stop_flag, queue, dt_format, time_zone, encoding):
        super(StandardInputEventsReader, self).__init__(stop_flag)
        self.queue = queue
        if dt_format:
            self.dt_parser = DateTimeParser(dt_format, time_zone)
        else:
            self.dt_parser = None
        self.encoding = encoding
        self.prev_event = None
        self.stdin = stdin

    def _run(self):
        while True:
            line = self.stdin.readline()
            if isinstance(line, six.binary_type):
                message = line.rstrip(b'\r\n')
            else:
                message = line.rstrip('\r\n')
            # the service doesn't allow empty message so exclude it here
            if message:
                event = LogEvent(message=message,
                                 dt_parser=self.dt_parser,
                                 prev_event=self.prev_event,
                                 encoding=self.encoding)
                if not event.complete():
                    reader_logger.warning(
                        'Fall back to current time: %s, reason: %s.',
                        event.debug_fields(),
                        'timestamp could not be parsed from message')
                self.pre_event = event
                self.queue.put(event)
            # Note that 'tail FILE' generates EOF
            # while 'tail -f FILE' doesn't.
            if not line:
                self.stop_flag.set()
                reader_logger.info('Reader reached the end of input.')
            if self._exit_needed():
                reader_logger.info('Reader is leaving...')
                break


class Publisher(BaseThread):
    def __init__(self, stop_flag, queue, logs_service, log_group_name,
                 log_stream_name, dry_run=False):
        super(Publisher, self).__init__(stop_flag)
        self.queue = queue
        self.logs_service = logs_service
        self.log_group_name = log_group_name
        self.log_stream_name = log_stream_name
        self.publish_callback = None
        self.event_batch = None
        self.dry_run = dry_run
        self.last_publish_time = None
        # Sequence token used for publishing events.
        if self.dry_run:
            self.sequence_token = 0
        else:
            self.sequence_token = None

    def register_publish_callback(self, publish_callback):
        """
        The publish_callback is called before making PutLogEvents call
        """
        self.publish_callback = publish_callback


    def _publish_event_batch(self):
        """
        Publish current event batch and start a new event batch
        """
        if not self.event_batch or not \
                self.event_batch.should_batch_be_published():
            return
        # A sequence token is from replay batch, or putLogEvents response
        if self.event_batch.is_replay:
            self.sequence_token = self.event_batch.sequence_token
        if self.publish_callback:
            self.publish_callback(self.event_batch, self.sequence_token)
        # This ensures no put call is made within 200ms from previous call
        if self.last_publish_time:
            self.stop_flag.wait(
                (EventBatch.MIN_PUT_DELAY -
                 (get_current_millis() -
                  self.last_publish_time)) / 1000.0)
        # This time is recorded before making the call so the above delay
        # is between making calls and not including the latency of call.
        publish_time = get_current_millis()
        self.sequence_token = self._put_log_events(self.event_batch)
        self.event_batch = None
        self.last_publish_time = publish_time

    def _put_log_events(self, event_batch):
        operation_aborted_ex = 'OperationAbortedException'
        data_already_accepted_ex = 'DataAlreadyAcceptedException'
        invalid_sequence_token_ex = 'InvalidSequenceTokenException'
        invalid_parameter_ex = 'InvalidParameterException'
        bad_sequence_token_re = "sequenceToken(?:\sis)?: ([^\s]+)"
        resource_not_found_ex = 'ResourceNotFoundException'
        events = []
        for event in event_batch.events:
            events.append({'timestamp': event.timestamp,
                           'message': event.message})
        # In one batch, events should be sorted in ascending order
        events = sorted(events, key=itemgetter('timestamp'))
        params = dict(logGroupName=self.log_group_name,
                      logStreamName=self.log_stream_name,
                      logEvents=events,
                      sequenceToken=None)
        batch_skipped = False
        sequence_token = self.sequence_token
        next_token = None
        while True:
            try:
                if sequence_token:
                    params['sequenceToken'] = sequence_token
                else:
                    if ('sequenceToken' in params.keys()):
                        del params['sequenceToken']
                if self.dry_run:
                    for event in params['logEvents']:
                        print_stdout(event['message'])
                    # Fake sequence token for dry run.
                    fake_sequence_token = str(int(sequence_token) + 1)
                    response = {'nextSequenceToken': fake_sequence_token}
                else:
                    response = self.logs_service.put_log_events(**params)
                next_token = response.get('nextSequenceToken')
                break
            except:
                type, value, traceback = exc_info()
                publisher_logger.warning('Caught exception: %s', value)
                # Skip batch if DataAlreadyAcceptedException happens
                if re.search(data_already_accepted_ex, str(value)):
                    bad_token_match = re.search(bad_sequence_token_re,
                                                str(value))
                    if bad_token_match:
                        sequence_token = bad_token_match.group(1)
                    batch_skipped = True
                    break
                # Retry request if OperationAbortedException happens
                if re.search(operation_aborted_ex, str(value)):
                    continue
                # Resend log events with new sequence token
                # when InvalidSequenceTokenException happens
                if re.search(invalid_sequence_token_ex, str(value)):
                    bad_token_match = re.search(bad_sequence_token_re,
                                                str(value))
                    if bad_token_match:
                        msg = ('Multiple agents might be sending log '
                               'events to log stream (%s %s) with '
                               'sequence token (%s). This could cause '
                               'duplicates and is not recommended.' %
                               (self.log_group_name,
                                self.log_stream_name,
                                sequence_token))
                        publisher_logger.warning(msg)
                        sequence_token = bad_token_match.group(1)
                        # This happens when sending log events with a token to
                        # a stream that doesn't expect a token.
                        if sequence_token == 'null':
                            sequence_token = None
                    else:
                        publisher_logger.error('Failed to get sequence token.')
                    continue

                if re.search(resource_not_found_ex, str(value)):
                    sequence_token = \
                        ExponentialBackoff(
                            max_retries=5,
                            logger=batch_logger,
                            stop_flag=self.stop_flag)(
                            self._setup_resources
                        )()
                    continue

                else:
                    # Even we did the client side validation, it's still
                    # possible to get back InvalidParameterException because
                    # we can't validate everything on client side accurately,
                    # e.g. service uses its own sys time to validate log
                    # events, the retention check.
                    # When this happens, we will just log the error and skip
                    # the batch.
                    if re.search(invalid_parameter_ex, str(value)):
                        batch_skipped = True
                        publisher_logger.warning(
                            'Skip batch: %s, reason: %s.',
                            event_batch.debug_fields(),
                            'invalid parameter exception')
                        break
                    # For any other unknown exceptions, raise the exception
                    # and cause the command exit.
                    raise

        if batch_skipped:
            next_token = sequence_token
        else:
            publisher_logger.info('Log group: %s, log stream: %s, '
                                  'queue size: %d, Publish batch: %s',
                                  self.log_group_name, self.log_stream_name,
                                  self.queue.qsize(), event_batch.debug_fields())
        return next_token

    def _setup_resources(self):
        batch_logger.info('Creating log group %s.', self.log_group_name)
        resource_already_exists_ex = 'ResourceAlreadyExistsException'
        try:
            self.logs_service.create_log_group(
                logGroupName=self.log_group_name)
        except:
            type, value, traceback = exc_info()
            if not re.search(resource_already_exists_ex, str(value)):
                batch_logger.warning("CreateLogGroup failed with exception %s" % value)
                raise
        batch_logger.info('Creating log stream %s.', self.log_stream_name)
        try:
            self.logs_service.create_log_stream(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name)
        except:
            type, value, traceback = exc_info()
            if not re.search(resource_already_exists_ex, str(value)):
                batch_logger.warning("CreateLogStream failed with exception %s" % value)
                raise


class EventsPublisher(Publisher):
    def __init__(self, stop_flag, queue, logs_service, log_group_name,
                 log_stream_name, buffer_duration, dry_run=False):
        super(EventsPublisher, self).__init__(
                stop_flag, queue, logs_service, log_group_name,
                log_stream_name, dry_run)
        if buffer_duration < StreamConfig.MIN_BUFFER_DURATION:
            publisher_logger.warning(
                'buffer_duration is set to MIN_BUFFER_DURATION '
                '(%s)', StreamConfig.MIN_BUFFER_DURATION)
            self.buffer_duration = StreamConfig.MIN_BUFFER_DURATION
        else:
            self.buffer_duration = buffer_duration

    def _run(self):
        while True:
            try:
                event = self.queue.get(False)
                add_status = self._add_event(event)
                if add_status == 0:
                    self._publish_event_batch()
                    self._add_event(event)
            except Queue.Empty:
                if self._exit_needed():
                    if not self.event_batch or not self.event_batch.events:
                        publisher_logger.info('Publisher is leaving as requested...')
                    else:
                        self.event_batch.force_publish = True
                        self._publish_event_batch()
                    break
                else:
                    self.stop_flag.wait(2)
            self._publish_event_batch()

    def _add_event(self, event):
        """
        Add event to batch and start the first batch if it doesn't exist
        """
        if self.event_batch is None:
            self.event_batch = EventBatch(self.buffer_duration)
        return self.event_batch.add_event(event)


class EventBatchPublisher(Publisher):
    def __init__(self, stop_flag, queue, logs_service, log_group_name,
                 log_stream_name, dry_run=False):
        super(EventBatchPublisher, self).__init__(
            stop_flag, queue, logs_service, log_group_name,
            log_stream_name, dry_run)

    def _run(self):
        while True:
            try:
                self.event_batch = self.queue.get(False)
                self._publish_event_batch()
            except Queue.Empty:
                if self._exit_needed():
                    if not self.event_batch or not self.event_batch.events:
                        publisher_logger.info('Publisher is leaving as requested...')
                    else:
                        self.event_batch.force_publish = True
                        self._publish_event_batch()
                    break
                else:
                    self.stop_flag.wait(1)


class EventTimestampStatus(object):
    TIMESTAMP_NOT_EVALUATED_YET = 0
    TIMESTAMP_VALID = 1
    FALLBACK_CURRENT_TIME = 2
    FALLBACK_PREVIOUS_EVENTTIME = 3


class LogEvent(object):
    PER_EVENT_OVERHEAD = 26
    MAX_EVENT_SIZE = 262144 # 256 * 1024

    def __init__(self, timestamp=None, message='',
                 source_id=None, sequence_token=None,
                 start_position=None, end_position=None,
                 is_replay=False, dt_parser=None,
                 prev_event=None, is_last_replay=False,
                 encoding='utf_8', batch_timestamp=None,
                 event_timestamp_status=EventTimestampStatus.TIMESTAMP_NOT_EVALUATED_YET):
        self.timestamp = timestamp
        self.encoding = encoding
        self.size_in_bytes = 0
        self.message = None
        self.source_id = source_id
        self.sequence_token = sequence_token
        self.start_position = start_position
        self.end_position = end_position
        self.is_replay = is_replay
        self.is_last_replay = is_last_replay
        self.dt_parser = dt_parser
        self.prev_timestamp = None
        self.prev_event_timestamp_status = EventTimestampStatus.TIMESTAMP_NOT_EVALUATED_YET
        if prev_event:
            self.prev_timestamp = prev_event.timestamp
            self.prev_event_timestamp_status = prev_event.event_timestamp_status
        self.initialize_event_timestamp_status(event_timestamp_status)
        self.batch_timestamp = batch_timestamp
        self.append_message(message)

    def initialize_event_timestamp_status(self, event_timestamp_status):
        valid_event_timestamp_statuses = range(4)
        if event_timestamp_status is not None \
                and event_timestamp_status in valid_event_timestamp_statuses:
            self.event_timestamp_status = event_timestamp_status
        else:
            self.event_timestamp_status = EventTimestampStatus.TIMESTAMP_NOT_EVALUATED_YET

    def complete(self):
        """
        Complete the event by setting the timestamp field.

        Return False if timestamp can't be parsed from message
        and current / previous event
        time is used, otherwise return True.
        """
        if self.timestamp:
            self.event_timestamp_status = EventTimestampStatus.TIMESTAMP_VALID
            return True
        if self.dt_parser is None:
            self.timestamp = utils.epoch(datetime.utcnow())
        else:
            try:
                curr_datetime = self.dt_parser.parse(self.message)
            except:
                curr_datetime = None
            if curr_datetime:
                self.timestamp = utils.epoch(curr_datetime)
            else:
                if self.prev_timestamp and \
                                self.prev_event_timestamp_status != EventTimestampStatus.FALLBACK_CURRENT_TIME \
                        and self.prev_event_timestamp_status != EventTimestampStatus.TIMESTAMP_NOT_EVALUATED_YET:
                    self.event_timestamp_status = EventTimestampStatus.FALLBACK_PREVIOUS_EVENTTIME
                    self.timestamp = self.prev_timestamp
                else:
                    self.event_timestamp_status = EventTimestampStatus.FALLBACK_CURRENT_TIME
                    self.timestamp = utils.epoch(datetime.utcnow())
                return False
        self.event_timestamp_status = EventTimestampStatus.TIMESTAMP_VALID
        return True

    def append_message(self, message):
        """
        Assign or append the message to event message.

        The message param could be binary type or text (unicode) type.
        This method converts the binary message to text if needed.
        There is a size limit per log event, so this method also checks
        if message (encoded with utf-8) exceeds the limit (number of bytes).
        """
        if isinstance(message, six.text_type):
            encoded_msg = message.encode('utf_8')
            decoded_msg = message
        else:
            decoded_msg = self._decode(message)
            # If encoding is utf_8 compatible, no need to encode message
            if self.encoding in ('utf_8', 'utf-8', 'utf8', 'ascii'):
                encoded_msg = message
            else:
                encoded_msg = decoded_msg.encode('utf_8')
        msg_size = len(encoded_msg)
        # Skip message to simplify the process as slicing text by
        # number of bytes is not easy.
        # the 1 byte is for '\n'
        if ((self.message and self.size_in_bytes + msg_size >
                self.MAX_EVENT_SIZE - 1) or
                (not self.message and self.size_in_bytes + msg_size >
                        self.MAX_EVENT_SIZE - self.PER_EVENT_OVERHEAD)):
            fallback_msg = six.u('[TRUNCATED MESSAGE] %d bytes are '
                                 'truncated.' % msg_size)
            event_logger.warning(
                'Truncate event: %s, reason: %s.', self.debug_fields(),
                'single event exceeds size limit')
            decoded_msg = fallback_msg
            msg_size = len(fallback_msg)
            # Don't append the truncate msg if adding it could exceed the
            # limit
            if (self.message and
                            self.size_in_bytes + msg_size > self.MAX_EVENT_SIZE - 1):
                return

        if self.message:
            self.message += six.u('\n') + decoded_msg
            self.size_in_bytes += msg_size + 1
        else:
            self.message = decoded_msg
            self.size_in_bytes += msg_size + self.PER_EVENT_OVERHEAD

    def _decode(self, message):
        # Only decode message to string if it's binary_type.
        # Since python3 readline returns unicode string,
        # this conversion is for python2 only.
        if isinstance(message, six.binary_type):
            try:
                return message.decode(self.encoding)
            except:
                event_logger.warning(
                    'Decode event with replace: %s, reason: %s.',
                    self.debug_fields(),
                    'unable to decode with %s' % self.encoding)
                return message.decode(self.encoding, 'replace')
        return message

    def debug_fields(self):
        return dict(timestamp=self.timestamp,
                    start_position=self.start_position,
                    end_position=self.end_position)

    def __eq__(self, other):
        return (self.timestamp == other.timestamp and
                self.message == other.message and
                self.source_id == other.source_id and
                self.sequence_token == other.sequence_token and
                self.start_position == other.start_position and
                self.end_position == other.end_position and
                self.is_replay == other.is_replay and
                self.is_last_replay == other.is_last_replay and
                self.batch_timestamp == other.batch_timestamp)


class EventBatch(object):
    # Below are rules enforced by PutLogEvents. Check API doc for details.
    # An extra overhead added to each event besides the message size.
    PER_EVENT_OVERHEAD = 26
    MAX_BATCH_SIZE = 32 * 1024
    MAX_NUM_OF_EVENTS_PER_BATCH = 1000

    MILLIS_PER_HOUR = 60 * 60 * 1000
    MILLIS_PER_DAY = 24 * MILLIS_PER_HOUR

    # All events in a batch must belong to a 24hrs period.
    MAX_TIME_RANGE_PER_BATCH = MILLIS_PER_DAY
    # CWL allows posting events up to two hours in future
    MAX_ALLOWED_INTERVAL_IN_FUTURE = 2 * MILLIS_PER_HOUR
    # CWL doesn't allow backfill more than 14 days in past.
    MAX_ALLOWED_INTERVAL_IN_PAST = 14 * MILLIS_PER_DAY

    # 5 TPS
    MIN_PUT_DELAY = 200

    def __init__(self, buffer_duration,
            max_num_of_events_per_batch=MAX_NUM_OF_EVENTS_PER_BATCH,
            max_batch_size=MAX_BATCH_SIZE):
        # Source fingerprint. It's None for events from stdin.
        self.source_id = None
        # A batch should be published at least buffer_duration ms since the
        # first event is added.
        self.buffer_duration = buffer_duration
        # Batch timestamp is set when the first event is added.
        self.batch_timestamp = None
        # An array holds all events.
        self.events = []
        # First/Last event in the batch
        self.first_event = None
        self.last_event = None
        # Smallest/largest timestamp in batch so the max range can be
        # calculated.
        self.smallest_timestamp_in_batch = None
        self.largest_timestamp_in_batch = None
        # This tracks the size of batch so batch won't exceed the max
        # allowed batch size (MAX_BATCH_SIZE)
        self.batch_size_in_bytes = 0
        # There are certain cases where a batch can't accept the new event
        # but should_batch_be_published rules are not met.
        # Setting this variable forces the publish.
        self.force_publish = False

        # A replay batch contains events whose replay attribute is True.
        # A replay event is an event that's processed before.
        self.is_replay = False
        self.sequence_token = None

        self.skipped_events_count = 0
        self.fallback_events_count = 0
        # Some service restrictions for testing override.
        self.max_num_of_events_per_batch = max_num_of_events_per_batch
        self.max_batch_size = max_batch_size
        self.per_event_overhead = self.PER_EVENT_OVERHEAD
        self.max_time_range_per_batch = self.MAX_TIME_RANGE_PER_BATCH
        self.max_allowed_interval_in_future = \
            self.MAX_ALLOWED_INTERVAL_IN_FUTURE
        self.max_allowed_interval_in_past = self.MAX_ALLOWED_INTERVAL_IN_PAST

    def _can_event_be_added(self, event):
        """
        Check if batch can still accept an event.

        1. A batch can only contain events from the same source so push state
        can be persisted with one record.
        2. A replay event can only be added to a replay batch from same
        source. A non-replay event can only be added to non-replay batch
        from same source.
        3. Batch can't exceed max_batch_size.
        4. Batch can't exceed max_num_of_events_per_batch.
        4. The time range can't exceed max_time_range_per_batch.
        """
        if len(self.events) == 0:
            return True
        if event.source_id != self.source_id:
            return False
        if event.is_replay != self.is_replay:
            return False
        if self.batch_size_in_bytes + event.size_in_bytes > \
                self.max_batch_size:
            return False
        if len(self.events) + 1 > self.max_num_of_events_per_batch:
            return False
        if self.largest_timestamp_in_batch and \
                self.largest_timestamp_in_batch:
            new_time_range = abs(max(self.largest_timestamp_in_batch,
                                     event.timestamp) -
                                 min(self.smallest_timestamp_in_batch,
                                     event.timestamp))
            if new_time_range > self.max_time_range_per_batch:
                return False
        return True

    def add_event(self, event):
        """
        Add event to a batch, and update some batch properties.
        Return 1 if event is successfully added to the batch,
        return -1 if event is invalid, and return 0 if event can't be
        added to this batch, but is good to be added to a new batch.

        Note that when this method returns 0, it also sets
        force_publish to True so batch can be published.
        Some batch properties are derived from first event, such
        as source_id, whether this is a replay batch, the sequence token.
        """
        # Below variables are needed to validate event
        if self.first_event is None:
            self.source_id = event.source_id
            self.batch_timestamp = get_current_millis()
            self.is_replay = event.is_replay
            if self.is_replay:
                self.sequence_token = event.sequence_token
                self.batch_timestamp = event.batch_timestamp
        if not self._validate_event(event):
            self.skipped_events_count += 1
            return -1
        if not self._can_event_be_added(event):
            self.force_publish = True
            return 0
        if event.event_timestamp_status != EventTimestampStatus.TIMESTAMP_VALID:
            self.fallback_events_count += 1
        self.events.append(event)
        self._update_batch_size(event)
        self._update_min_max_timestamp(event)
        if self.first_event is None:
            self.first_event = event
        self.last_event = event
        return 1

    def should_batch_be_published(self):
        """
        Check if a batch should be published.
        Return True if batch should be published, otherwise, return False.
        A batch should be published if it exceeds the buffer duration or
        force publish is true, e.g. thread is leaving, batch can't
        accept more events (see _can_event_be_added for details).
        Note that for replay batch, the buffer duration check is ignored.
        """
        if len(self.events) == 0:
            return False
        if self.is_replay:
            return self.last_event.is_last_replay or self.force_publish
        if self.force_publish:
            return True
        if get_current_millis() - self.batch_timestamp >= self.buffer_duration:
            return True
        return False

    def _validate_event(self, event):
        """
        Return False if event is invalid, otherwise return True

        The client side and server side validation use different system time,
        so this is not 100% accurate, which means, a verified event batch
        might be rejected by server.
        """
        # Ignore blank messages or they'll cause PutLogEvents to fail.
        if event.message.strip() == '':
            return False

        # Skip the event if its too far in future.
        if event.timestamp > (self.batch_timestamp +
                                  self.max_allowed_interval_in_future):
            batch_logger.warning(
                'Skip event: %s, reason: %s.', event.debug_fields(),
                'timestamp is more than 2 hours in future')
            return False

        # Skip the event if its too far in the past.
        if event.timestamp < (self.batch_timestamp -
                                  self.max_allowed_interval_in_past):
            batch_logger.warning(
                'Skip event: %s, reason: %s.', event.debug_fields(),
                'timestamp is more than 14 days in past')
            return False
        return True

    def _update_min_max_timestamp(self, event):
        """
        Track the smallest/largest event timestamps in the batch.
        """
        event_timestamp = event.timestamp
        if self.smallest_timestamp_in_batch is None:
            self.smallest_timestamp_in_batch = event_timestamp
            self.largest_timestamp_in_batch = event_timestamp
        elif self.smallest_timestamp_in_batch > event_timestamp:
            self.smallest_timestamp_in_batch = event_timestamp
        elif self.largest_timestamp_in_batch < event_timestamp:
            self.largest_timestamp_in_batch = event_timestamp

    def _update_batch_size(self, event):
        self.batch_size_in_bytes += event.size_in_bytes

    def debug_fields(self):
        return dict(source_id=self.source_id,
                    num_of_events=len(self.events),
                    skipped_events_count=self.skipped_events_count,
                    fallback_events_count=self.fallback_events_count,
                    batch_size_in_bytes=self.batch_size_in_bytes,
                    first_event=(self.first_event and
                                 self.first_event.debug_fields()),
                    last_event=(self.last_event and
                                self.last_event.debug_fields()))


class ResourceNotFoundException(Exception):
    """
    Raised when log stream or log group is not found
    """
    pass
