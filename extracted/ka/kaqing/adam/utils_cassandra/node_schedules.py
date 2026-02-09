from copy import copy
from datetime import datetime
import threading
import time

from adam.config import Config
from adam.utils_context import Context
from adam.utils_k8s.pods import strip_pod_name

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def key(pod: str, namespace: str):
    return f'{pod}@{namespace}'

class NodeSchedules:
    lock = threading.Lock()

    _queue: dict[tuple[str, str], float] = {}
    _in_restartings: dict[tuple[str, str], float] = {}
    _completed: dict[tuple[str, str], float] = {}
    _waiting_ons: dict[tuple[str, str], str] = {}

    def pending():
        with NodeSchedules.lock:
            return copy(NodeSchedules._queue)

    def completed():
        with NodeSchedules.lock:
            return copy(NodeSchedules._completed)

    def restartings(timeout: int = 0, ctx: Context = Context.NULL):
        if not timeout:
            timeout = Config().get('cassandra.restart.grace-period-in-seconds', 5 * 60)

        with NodeSchedules.lock:
            for pod, t in list(NodeSchedules._in_restartings.items()):
                if (secs := int(time.time() - t)) >= timeout:
                    ctx.log2(f'[{ts()}] {int(secs)} seconds have been passed since restart of {strip_pod_name(pod[0])}@{pod[1]}. Removing from in_restart queue...')
                    NodeSchedules.done(pod, ctx)

            return NodeSchedules._in_restartings

    def waiting_ons():
        return copy(NodeSchedules._waiting_ons)

    def restarts(namespace: str = None, ctx: Context = Context.NULL) -> list[str]:
        pods = set()

        for p in NodeSchedules.pending().keys():
            if not namespace or namespace == p[1]:
                pods.add(p[0])
        for p in NodeSchedules.restartings(ctx=ctx).keys():
            if not namespace or namespace == p[1]:
                pods.add(p[0])

        return sorted(list(pods))

    def done(pod: tuple[str, str], ctx: Context):
        ctx.log2(f'[{ts()}] Restarted {pod}.')

        if pod in NodeSchedules._in_restartings:
            del NodeSchedules._in_restartings[pod]
        NodeSchedules._completed[pod] = time.time()