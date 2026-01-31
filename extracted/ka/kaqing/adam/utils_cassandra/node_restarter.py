from copy import copy
from datetime import datetime
import threading
import time
import traceback

from adam.config import Config
from adam.repl_state import ReplState
from adam.utils_cassandra.cassandra import Cassandra
from adam.utils_cassandra.node_restartable import NodeRestartable
from adam.utils_context import Context
from adam.utils_k8s.pods import Pods

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def key(pod: str, namespace: str):
    return f'{pod}@{namespace}'

class NodeRestarter:
    lock = threading.Lock()
    nodes_thread: threading.Thread = None
    _ctx: Context = None

    _queue: dict[tuple[str, str], float] = {}
    _in_restartings: dict[tuple[str, str], float] = {}
    _completed: dict[tuple[str, str], float] = {}
    _waiting_ons: dict[tuple[str, str], str] = {}

    def schedule(state: ReplState, pod: str, ctx: Context):
        NodeRestarter.start(state, ctx)

        NodeRestarter._ctx.log2(f'[{ts()}] Restart requested for {pod}@{state.namespace}.')
        with NodeRestarter.lock:
            NodeRestarter._queue[(pod, state.namespace)] = time.time()

    def start(state: ReplState, ctx: Context):
        with NodeRestarter.lock:
            if not NodeRestarter.nodes_thread:
                ctx = ctx.copy(background=True, bg_init_msg='[{job_id}] Use :?? to get job scheduling status.')

                NodeRestarter._ctx = ctx
                NodeRestarter.nodes_thread = threading.Thread(target=NodeRestarter.loop, args=(state, ctx,), daemon=True)
                NodeRestarter.nodes_thread.start()

    def done(pod: tuple[str, str], ctx: Context):
        ctx.log2(f'[{ts()}] Restarted {pod}.')

        if pod in NodeRestarter._in_restartings:
            del NodeRestarter._in_restartings[pod]
        NodeRestarter._completed[pod] = time.time()

    def pending():
        with NodeRestarter.lock:
            return copy(NodeRestarter._queue)

    def completed():
        with NodeRestarter.lock:
            return copy(NodeRestarter._completed)

    def restart_node(pod: str, namespace: str, ctx: Context):
        with NodeRestarter.lock:
            key = (pod, namespace)
            if key in NodeRestarter._queue:
                del NodeRestarter._queue[key]
            NodeRestarter._in_restartings[key] = time.time()

        Pods.delete(pod, namespace)

    def restartings(timeout: int = 0, ctx: Context = Context.NULL):
        if not timeout:
            timeout = Config().get('cassandra.restart.grace-period-in-seconds', 5 * 60)

        with NodeRestarter.lock:
            for pod, t in list(NodeRestarter._in_restartings.items()):
                if (secs := int(time.time() - t)) >= timeout:
                    NodeRestarter._ctx.log2(f'[{ts()}] {int(secs)} seconds have been passed since restart of {pod[0]}@{pod[1]}. Removing from in_restart queue...')
                    NodeRestarter.done(pod, NodeRestarter._ctx)

            return NodeRestarter._in_restartings

    def waiting_ons():
        return copy(NodeRestarter._waiting_ons)

    # DEBUG kubectl exec cs-a7b13e29bd-cs-a7b13e29bd-default-sts-0 -c cassandra -n azops88 -- /bin/sh -c "nodetool -u cs-a7b13e29bd-superuser -pw ... status"
    # c:cs-a7b13e29bd-default-sts>
    # nodetool: Failed to connect to '127.0.0.1:7199' - FailedLoginException: 'Unable to perform authentication: Operation timed out - received only 1 responses.'.
    # Reason: Handshake status 500 Internal Server Error -+-+- {'content-length': '33', 'content-type': 'text/plain; charset=utf-8', 'date': 'Thu, 29 Jan 2026 20:40:20 GMT', 'connection': 'close'} -+-+- b'container not found ("cassandra")'

    # single queue pattern
    def loop(state: ReplState, ctx: Context = Context.NULL):
        while True:
            try:
                while (pods := NodeRestarter.pending().keys()):
                    restarted = 0
                    for pod, namespace in pods:
                        in_restartings = NodeRestarter.restartings(ctx=ctx)
                        ir = ''
                        if in_restartings:
                            ir = f', in_restarting:[{", ".join([f"{r[0]}@{r[1]}" for r in in_restartings])}]'

                        node: NodeRestartable = Cassandra.restartable(state.with_namespace(namespace), pod, in_restartings=in_restartings, ctx=ctx.copy(show_out=False, background=False))
                        if node.restartable():
                            ctx.log2(f'[{ts()}] Restarting {pod}@{namespace}{ir}.')
                            NodeRestarter.restart_node(pod, namespace, ctx)

                            restarted += 1

                            with NodeRestarter.lock:
                                if (pod, namespace) in NodeRestarter._waiting_ons:
                                    del NodeRestarter._waiting_ons[(pod, namespace)]
                        else:
                            with NodeRestarter.lock:
                                NodeRestarter._waiting_ons[(pod, namespace)] = node.waiting_on()
                            ctx.log2(f'[{ts()}] {pod}@{namespace} is not restartable{ir}.')

                    if not restarted:
                        # ctx.log2(f'[{ts()}] Did not find any restartable pods.')
                        time.sleep(5)

                # trigger cleaning up of restartings
                NodeRestarter.restartings(ctx=ctx)

                time.sleep(5)
            except:
                traceback.print_exc()