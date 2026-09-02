import threading
import time

import six

from rook import utils
from rook.com_ws.envelope_wrappers.basic_envelope_wrapper import BasicEnvelopeWrapper
from rook.com_ws.envelope_wrappers.basic_serialized_envelope_wrapper import BasicSerializedEnvelopeWrapper
from rook.com_ws.envelope_wrappers.protobuf_2_envelope_wrapper import Protobuf2EnvelopeWrapper
from six.moves.urllib.parse import urlparse
import select
import certifi
import ssl
import re
import os
import websocket

from rook.exceptions import RookCommunicationException, RookInvalidToken, RookDependencyConflict, \
    RookMissingToken, RookOutputQueueFull, RookWebSocketError
import rook.com_ws.socketpair_compat  # do not remove - adds socket.socketpair on Windows lgtm[py/unused-import]

try:
    from websocket import \
        WebSocketBadStatusException  # This is used to make sure we have the right version lgtm[py/unused-import]
except ImportError:
    raise RookDependencyConflict('websocket')

# Python < 2.7.9 is missing important SSL features for websocket
# (unless supplied by CentOS etc)
if not websocket._ssl_compat.HAVE_SSL:
    try:
        import backports.ssl
        import backports.ssl_match_hostname

        websocket._http.ssl = backports.ssl
        websocket._http.HAVE_SSL = True
        websocket._http.HAVE_CONTEXT_CHECK_HOSTNAME = True
    except ImportError:
        six.print_('[Rookout] Python is missing modern SSL features. To rectify, please run:\n'
                          '  pip install rook[ssl_backport]')

from rook.com_ws import information
from rook.logger import logger
import rook.protobuf.messages_pb2 as messages_pb
import rook.protobuf.envelope_pb2 as envelope_pb
from rook.config import AgentComConfiguration, VersionConfiguration


def wrap_in_envelope(message):
    envelope = envelope_pb.Envelope()
    envelope.timestamp.GetCurrentTime()
    envelope.msg.Pack(message)

    return envelope.SerializeToString()


class FlushMessagesEvent(object):
    def __init__(self):
        self.event = threading.Event()


class MessageCallback(object):
    def __init__(self, cb, persistent):
        self.cb = cb
        self.persistent = persistent


class AgentComBase(object):
    def __init__(self, agent_id, host, port, proxy, token, labels, tags, debug, print_on_initial_connection):
        self._thread = None
        self.id = agent_id

        self._init_connect_thread()

        self._host = host if '://' in host else 'ws://' + host
        self._port = port
        self._proxy = proxy
        self._token = token
        self._token_valid = False
        self._labels = labels or {}
        self._tags = tags or []

        self._loop = None
        self._connection = None

        self._queue = None  # Initiated by child
        self._queue_messages_length = 0

        self._running = False

        self._ready_event = threading.Event()
        self._connection_error = None

        self.debug = debug

        self._callbacks = {}
        self._print_on_initial_connection = print_on_initial_connection

        def set_ready_event(*args):
            self._ready_event.set()

        self.once('InitialAugsCommand', set_ready_event)

    def poll_available(self):
        return hasattr(select, "poll")

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        if not self._running:
            logger.warning("stop while not running")
            return

        self._running = False

        if self._connection is not None:
            self._connection.close(1000)

        self._thread.join()
        self._thread = None

        if self._connection is not None:
            self._connection.close(1000)
            self._connection = None

    def restart(self):
        self.stop()
        self._init_connect_thread()
        self.start()

    def update_info(self, agent_id, tags, labels):
        self.id = agent_id
        self._labels = labels or {}
        self._tags = tags or []

    def send_user_message(self, aug_id, message_id, arguments):
        envelope = Protobuf2EnvelopeWrapper(self.id, aug_id, message_id, arguments)

        self.add_envelope(envelope)

    def add(self, message):
        if self.is_queue_full():
            return

        envelope = BasicSerializedEnvelopeWrapper(message)
        self.add_envelope(envelope)

    def add_envelope(self, envelope):
        if len(envelope) + self._queue_messages_length > AgentComConfiguration.MAX_QUEUE_MESSAGES_LENGTH:
            raise RookOutputQueueFull()

        self._queue_messages_length += len(envelope)
        self._queue.put(envelope)

    def is_queue_full(self):
        return self._queue.qsize() >= AgentComConfiguration.MAX_QUEUED_MESSAGES

    def on(self, message_name, callback):
        self._register_callback(message_name, MessageCallback(callback, True))

    def once(self, message_name, callback):
        self._register_callback(message_name, MessageCallback(callback, False))

    def await_message(self, message_name):
        raise NotImplementedError('AgentComBase')

    def wait_for_ready(self, timeout=None):
        if not self._ready_event.wait(timeout):
            raise RookCommunicationException()
        else:
            if self._connection_error is not None:
                raise self._connection_error

    def _do_connect(self):
        try:
            self._connection = self._create_connection()
            self._register_agent(self.debug)

        except websocket.WebSocketBadStatusException as e:
            if e.status_code == 400:
                self._connection_error = RookWebSocketError(e.status_code)
                self._ready_event.set()
            if not self._token_valid and e.status_code == 403:  # invalid token
                if self._token is None:
                    self._connection_error = RookMissingToken()
                else:
                    self._connection_error = RookInvalidToken(self._token)
                self._ready_event.set()

                logger.error('Connection failed; %s', self._connection_error.get_message())
            raise

    def _run_single_connect_attmept(self):
        success = True
        fail_reason = ""
        try:
            self._do_connect()
        except Exception as e:
            success = False
            if hasattr(e, 'message') and e.message:
                fail_reason = e.message
            else:
                fail_reason = str(e)
        return success, fail_reason

    def _connect(self):
        retry = 0
        backoff = AgentComConfiguration.BACK_OFF
        connected = False
        last_successful_connection = 0
        while self._running:
            sleep_duration_for_reconnect = backoff
            success, fail_reason = self._run_single_connect_attmept()
            if success is False:
                retry += 1
                connected = False
                logger.info('Connection failed; reason = %s, retry = #%d, waiting %.3fs', fail_reason,
                            retry, backoff)
            else:
                connected = True
                last_successful_connection = time.time()
                logger.debug("WebSocket connected successfully")
                self._token_valid = True

                if self._print_on_initial_connection:
                    # So there is no print on reconnect
                    self._print_on_initial_connection = False
                    utils.quiet_print("[Rookout] Successfully connected to controller.")
                    logger.debug("[Rookout] Agent ID is {}".format(self.id))
                self._create_run_connection_thread()  # Blocking until connection thread is finished
                time_after_run_connection = time.time()
                run_connection_duration = time_after_run_connection - last_successful_connection
                sleep_duration_for_reconnect = max(0, backoff - run_connection_duration)  # remaining time until backoff
            if self._running:  # no point in sleeping if exiting the loop
                time.sleep(sleep_duration_for_reconnect)
                backoff = min(backoff * 2, AgentComConfiguration.MAX_SLEEP)
                if connected and time.time() >= last_successful_connection + AgentComConfiguration.RESET_BACKOFF_TIMEOUT:
                    retry = 0
                    backoff = AgentComConfiguration.BACK_OFF
                logger.debug("Reconnecting")

    def _create_run_connection_thread(self):
        raise NotImplementedError('AgentComBase')

    def flush_all_messages(self):
        flush_event = FlushMessagesEvent()
        self._queue.put(BasicEnvelopeWrapper(flush_event))
        flush_event.event.wait(AgentComConfiguration.FLUSH_TIMEOUT)

    def _create_connection(self):
        url = '{}:{}/v1'.format(self._host, self._port)
        headers = {
            'User-Agent': 'RookoutAgent/{}+{}'.format(VersionConfiguration.VERSION, VersionConfiguration.COMMIT)
        }

        if self._token is not None:
            headers["X-Rookout-Token"] = self._token

        proxy_host, proxy_port = self._get_proxy()

        connect_args = (url,)
        connect_kwargs = dict(header=headers,
                              timeout=AgentComConfiguration.TIMEOUT,
                              http_proxy_host=proxy_host,
                              http_proxy_port=proxy_port,
                              enable_multithread=True)

        if os.environ.get('ROOKOUT_NO_HOST_HEADER_PORT') == '1':
            host = re.sub(':\d+$', '', urlparse(url).netloc)
        else:
            host = None

        connect_kwargs['sslopt'] = dict()

        if os.environ.get('ROOKOUT_SKIP_SSL_VERIFY') == '1':
            connect_kwargs['sslopt']['cert_reqs'] = ssl.CERT_NONE

        try:
            # connect using system certificates
            conn = websocket.create_connection(*connect_args, host=host, **connect_kwargs)
        # In some very specific scenario, you cannot
        # reference ssl.CertificateError because it does
        # exist, so instead we get with with getattr
        # (None never matches an exception)
        except (ssl.SSLError, getattr(ssl, 'CertificateError', None)):
            # connect using certifi certificate bundle
            # (Python 2.7.15+ from python.org on macOS rejects our CA, see RK-3383)
            connect_kwargs['sslopt']['ca_certs'] = certifi.where()
            logger.debug("Got SSL error when connecting using system CA cert store, falling back to certifi")
            conn = websocket.create_connection(*connect_args, **connect_kwargs)
        conn.settimeout(None)
        return conn

    def _get_proxy(self):
        if self._proxy is None:
            return None, None

        try:
            if not self._proxy.startswith("http://"):
                self._proxy = "http://" + self._proxy

            url = urlparse(self._proxy, "http://")

            logger.debug("Connecting via proxy: %s", url.netloc)

            return url.hostname, url.port
        except ValueError:
            return None, None

    def _register_agent(self, debug):
        info = information.collect(debug)
        info.agent_id = self.id
        info.labels = self._labels
        info.tags = self._tags

        m = messages_pb.NewAgentMessage()
        m.agent_info.CopyFrom(information.pack_agent_info(info))

        return self._send(wrap_in_envelope(m))

    def _init_connect_thread(self):
        if self._thread is not None:
            raise RuntimeError('Trying to start AgentCom thread twice')

        self._thread = threading.Thread(name="rookout-" + type(self).__name__, target=self._connect)
        self._thread.daemon = True

    AcceptedMessageTypes = [
        messages_pb.InitialAugsCommand,
        messages_pb.AddAugCommand,
        messages_pb.ClearAugsCommand,
        messages_pb.PingMessage,
        messages_pb.RemoveAugCommand
    ]

    def _handle_incoming_message(self, envelope):
        for message_type in self.AcceptedMessageTypes:
            if envelope.msg.Is(message_type.DESCRIPTOR):
                message = message_type()
                envelope.msg.Unpack(message)
                type_name = message.DESCRIPTOR.name

                callbacks = self._callbacks.get(type_name)

                if callbacks:
                    persistent_callbacks = []

                    # Trigger all persistent callbacks first
                    for callback in callbacks:
                        try:
                            if callback.persistent:
                                callback.cb(message)
                        except Exception:  # We ignore errors here, they are high unlikely and the code is too deep
                            pass
                        finally:
                            if callback.persistent:
                                persistent_callbacks.append(callback)

                    # Trigger all non persistent callbacks
                    for callback in callbacks:
                        try:
                            if not callback.persistent:
                                callback.cb(message)
                        except Exception:  # We ignore errors here, they are high unlikely and the code is too deep
                            pass

                    self._callbacks[type_name] = persistent_callbacks

    def _send(self, message):
        return self._connection.send_binary(message)

    def _register_callback(self, message_name, callback):
        self._callbacks.setdefault(message_name, []).append(callback)
