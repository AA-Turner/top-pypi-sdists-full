import time
import websocket
import socket

from rook.com_ws import poll_select, selectable_event, selectable_queue
from rook.com_ws.agent_com_impel.agent_com_base import AgentComBase, FlushMessagesEvent
from rook.config import AgentComConfiguration

from rook.logger import logger
import rook.protobuf.envelope_pb2 as envelope_pb
from six.moves.queue import Empty


class SingleThreadAgentCom(AgentComBase):

    def __init__(self, agent_id, host, port, proxy, token, labels, tags, debug, print_on_initial_connection):
        super(SingleThreadAgentCom, self).__init__(agent_id, host, port, proxy, token, labels, tags, debug,
                                                   print_on_initial_connection)

        # Queue hold outgoing messages wrapped with IEnvelopeWrapper
        self._queue = selectable_queue.SelectableQueue()

    def await_message(self, message_name):
        event = selectable_event.SelectableEvent()
        self.once(message_name, lambda _: event.set())

        return event

    def _create_run_connection_thread(self):
        logger.dev_debug("Entering _create_run_connection_thread")
        with self.await_message('InitialAugsCommand') as got_initial_augs_event:
            try:
                self.run_until_stopped(got_initial_augs_event)
            except Exception as exc:
                logger.exception("network loop stopped: %s", exc)

    def run_until_stopped(self, got_initial_augs_event):
        logger.dev_debug("Entering run_until_stopped")
        self._connection.ping()
        waiter = poll_select.get_waiter([self._connection, self._queue, got_initial_augs_event], [], [self._connection])
        last_ping_time = 0
        last_read_time = time.time()
        got_initial_augs_started_waiting = time.time()
        got_initial_augs_keep_waiting = True
        while self._running:
            # this is similar to the select API: rlist, wlist, xlist - fds ready to read, ready to write, and errors
            # see official documentation for POSIX select or Python select.select for further info
            logger.dev_debug("Before waiter.wait")
            rlist, _, xlist = waiter.wait(AgentComConfiguration.PING_INTERVAL)
            logger.dev_debug("After waiter.wait")

            # if it's time to send a ping, go ahead and do it now
            if (time.time() - last_ping_time) >= AgentComConfiguration.PING_INTERVAL:
                last_ping_time = time.time()
                logger.debug("Sending ping")
                self._connection.ping()
            # if rlist and xlist are empty -> the wait timed out, so check if we had a ping timeout
            if len(rlist) == 0 and len(xlist) == 0 and (
                    time.time() - last_read_time) >= AgentComConfiguration.PING_TIMEOUT:
                logger.debug("Disconnecting due to ping timeout")
                self._connection.close()
                break

            # got initial augs is ready, so don't wait on it anymore
            if got_initial_augs_event in rlist:
                # don't wait on got_initial_augs_event anymore
                got_initial_augs_keep_waiting = False
                waiter = poll_select.get_waiter([self._connection, self._queue], [], [self._connection])
                logger.info("Finished initialization")
            # still waiting for got initial augs, but reached timeout, don't wait on it anymore
            if got_initial_augs_keep_waiting and (
                    time.time() - got_initial_augs_started_waiting) >= AgentComConfiguration.TIMEOUT:
                got_initial_augs_keep_waiting = False
                waiter = poll_select.get_waiter([self._connection, self._queue], [], [self._connection])
                logger.warning("Timeout waiting for initial augs")
            # connection appeared in xlist, means it was closed
            if self._connection in xlist:
                logger.info("Connection closed")
                break
            # connection appeared in rlist, means there's data to read
            if self._connection in rlist:
                last_read_time = time.time()
                try:
                    logger.dev_debug("Trying to read data from connection")
                    code, msg = self._connection.recv_data(control_frame=True)
                    if code == websocket.ABNF.OPCODE_BINARY:
                        if msg is None:
                            # socket disconnected
                            logger.debug("Reading msg - socket disconnected")
                            break

                        if len(msg) > AgentComConfiguration.AGENT_COM_INCOMING_MAX_MESSAGE_SIZE:
                            logger.error("message length (%d) exceed max size", msg)
                            continue

                        envelope = envelope_pb.Envelope()
                        logger.dev_debug("Trying to parse envelope from string")
                        envelope.ParseFromString(msg)
                        logger.dev_debug("Finished parsing envelope from string")
                        self._handle_incoming_message(envelope)
                    else:
                        logger.dev_debug("Received opcode: %d", code)
                except (socket.error, websocket.WebSocketConnectionClosedException):
                    logger.debug("Reading msg - socket disconnected")
                    break
            # queue appeared in rlist, means there's a new message to send
            if self._queue in rlist:
                logger.dev_debug("queue in rlist")
                wrapped_envelope = None
                try:
                    wrapped_envelope = self._queue.get()
                    msg = wrapped_envelope.get_buffer()
                    if isinstance(msg, FlushMessagesEvent):
                        msg.event.set()
                        continue
                    logger.dev_debug("Trying to send data to connection")
                    self._connection.send_binary(msg)
                except (socket.error, websocket.WebSocketConnectionClosedException):
                    if wrapped_envelope is not None:
                        self._queue.put(wrapped_envelope)
                    logger.info("Got websocket closed exception")
                    break
                except Empty:
                    logger.dev_debug("queue was empty!")
                    continue
                self._queue_messages_length -= len(wrapped_envelope)

        logger.warning("loop stopped running")
