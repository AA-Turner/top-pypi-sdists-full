import socket
import errno
import select
import websocket
import threading
import time

from rook.com_ws.agent_com_impel.agent_com_base import AgentComBase, FlushMessagesEvent
from rook.com_ws.envelope_wrappers.basic_envelope_wrapper import BasicEnvelopeWrapper
from rook.config import AgentComConfiguration

from rook.logger import logger
from six.moves.queue import Queue, Empty
import rook.protobuf.envelope_pb2 as envelope_pb


class ExitThreadSentinel(object):
    pass


class MultiThreadAgentCom(AgentComBase):

    def __init__(self, agent_id, host, port, proxy, token, labels, tags, debug, print_on_initial_connection):
        super(MultiThreadAgentCom, self).__init__(agent_id, host, port, proxy, token, labels, tags, debug,
                                                  print_on_initial_connection)

        # Queue hold outgoing messages wrapped with IEnvelopeWrapper
        self._queue = Queue()

    def await_message(self, message_name):
        event = threading.Event()
        self.once(message_name, lambda _: event.set())

        return event

    def _create_run_connection_thread(self):
        stop_socket_incoming, incoming_client_socket = socket.socketpair()
        outgoing_exit_sentinel = ExitThreadSentinel()

        def signal_stop_incoming_thread():
            # Logging is not safe here, interpreter might be shutting down
            try:
                stop_socket_incoming.send(b'1')
            except socket.error as socket_error:
                if socket_error.errno == errno.EPIPE:
                    return

                logger.debug("Failed to signal stop", exc_info=1)
            except Exception:
                logger.debug("Failed to signal stop", exc_info=1)
            finally:
                try:
                    stop_socket_incoming.close()
                except:  # lgtm[py/catch-base-exception]
                    pass

        def signal_stop_outgoing_thread():
            # Logging is not safe here, interpreter might be shutting down
            try:
                incoming_client_socket.close()
            except:  # Nothing to do as we are already closing
                pass

            try:
                self._queue.put(BasicEnvelopeWrapper(outgoing_exit_sentinel))
            except Exception:
                logger.debug("Failed to signal stop", exc_info=1)

        routines = [threading.Thread(name="rookout-incoming-thread", target=self._incoming,
                                     args=(incoming_client_socket, signal_stop_outgoing_thread)),
                    threading.Thread(name="rookout-outgoing-thread", target=self._outgoing,
                                     args=(outgoing_exit_sentinel, signal_stop_incoming_thread))]
        for routine in routines:
            routine.daemon = True
            routine.start()
        logger.info("Finished initialization")
        for routine in routines:
            routine.join()

    def _outgoing(self, outgoing_exit_sentinel, on_exit):
        try:
            last_ping = time.time()
            self._connection.ping()

            while self._running:
                envelope_wrapper = None
                if (time.time() - last_ping) >= AgentComConfiguration.PING_INTERVAL:
                    last_ping = time.time()
                    self._connection.ping()

                try:
                    envelope_wrapper = self._queue.get(timeout=AgentComConfiguration.PING_INTERVAL)
                    if envelope_wrapper is None:
                        break
                    msg = envelope_wrapper.get_buffer()
                    if isinstance(msg, ExitThreadSentinel):
                        if msg is outgoing_exit_sentinel:
                            break
                        continue  # if it's an ExitThreadSentinel but not from this specific thread, just skip it
                    if isinstance(msg, FlushMessagesEvent):
                        msg.event.set()
                        continue
                    self._send(msg)
                except Empty:
                    continue
                except (socket.error, websocket.WebSocketConnectionClosedException):
                    if envelope_wrapper is not None:
                        self._queue.put(envelope_wrapper)
                    break

                if envelope_wrapper is not None:
                    self._queue_messages_length -= len(envelope_wrapper)

        except:  # lgtm[py/catch-base-exception]
            try:
                logger.exception("Outgoing thread failed")
            except:  # lgtm[py/catch-base-exception]
                pass
        finally:
            on_exit()

    def _incoming(self, stop_socket, on_exit):
        try:
            while self._running:
                try:
                    # Poll has no file_descriptor limit (on linux) if available - use it
                    if self.poll_available():
                        if self.wait_for_event_poll(stop_socket):
                            break
                    else:
                        if self.wait_for_event_select(stop_socket):
                            break

                    # it wasn't stop_socket, so it's self._connection -> we can read. we have to read including
                    # control frames, otherwise select might return and recv() wouldn't actually return anything
                    code, msg = self._connection.recv_data(control_frame=True)
                    if code != websocket.ABNF.OPCODE_BINARY:
                        continue

                    if msg is None:
                        # socket disconnected
                        logger.debug("Incoming thread - socket disconnected")
                        break

                    if len(msg) > AgentComConfiguration.AGENT_COM_INCOMING_MAX_MESSAGE_SIZE:
                        logger.error("message length (%d) exceed max size", msg)
                        continue

                    envelope = envelope_pb.Envelope()
                    envelope.ParseFromString(msg)
                    self._handle_incoming_message(envelope)
                except (socket.error, websocket.WebSocketConnectionClosedException):
                    logger.debug("Incoming thread - socket disconnected")
                    break
        except:  # lgtm[py/catch-base-exception]
            try:
                logger.exception("Incoming thread failed")
            except:  # lgtm[py/catch-base-exception]
                pass
        finally:
            on_exit()

    def wait_for_event_poll(self, stop_socket):
        poller = select.poll()

        exception_flags = select.POLLHUP | select.POLLERR
        read_only_flags = select.POLLIN | select.POLLPRI | exception_flags

        # Registering all input close and exception types
        poller.register(self._connection, read_only_flags)
        poller.register(stop_socket, read_only_flags)

        events = poller.poll(AgentComConfiguration.PING_TIMEOUT * 1000)

        try:
            for fd, flag in events:
                if fd == stop_socket.fileno():
                    return True  # signaled to stop
                elif fd == self._connection.fileno() and flag \
                        and flag & exception_flags:  # Checking these flags explicitly (ignore input data)
                    return True
        except AttributeError:  # happens when the socket is already None (and fileno() will fail)
            return True  # Should stop

        if len(events) == 0:
            logger.debug("Incoming thread - ping timeout")
            return True  # select timed out - ping timeout

        # Every thing is ok
        return False

    def wait_for_event_select(self, stop_socket):
        rlist, _, xlist = select.select([self._connection, stop_socket],
                                        [],
                                        [self._connection, stop_socket],
                                        AgentComConfiguration.PING_TIMEOUT)
        if stop_socket in rlist or stop_socket in xlist or self._connection in xlist:
            return True  # signaled to stop

        if len(rlist) == 0 and len(xlist) == 0:
            logger.debug("Incoming thread - ping timeout")
            return True  # select timed out - ping timeout
        return False
