from concurrent.futures import as_completed, Future, ThreadPoolExecutor
import functools
import threading
from typing import Callable, Iterator, TypeVar
import sys
import time

from adam.config_holder import ConfigHolder
from adam.utils import elapsed_time
from adam.utils_log import debug, log_exc, log_timing
from adam.utils_error import ErrorAware

T = TypeVar('T')

class ThreadPool:
    pools: dict[str, 'ThreadPool'] = {}
    thread_lock = threading.Lock()

    def create(name: str, workers: int):
        with ThreadPool.thread_lock:
            if name in ThreadPool.pools:
                return ThreadPool.pools[name]

            pool = ThreadPool(name, workers)
            ThreadPool.pools[name] = pool

            return pool

    def __init__(self, name: str, workers: int):
        self.name = name
        self.workers = workers
        self.dispatched = 0
        self.completed = 0
        self.concurrency = 0
        self.max_concurrency = 0

        self.lock = threading.Lock()
        self._executor: ThreadPoolExecutor = None

    def executor(self):
        with ThreadPool.thread_lock:
            if not self._executor:
                self._executor = ThreadPoolExecutor(max_workers=self.workers, thread_name_prefix=self.name)

            return self._executor

    def metrics(self, f: Callable[..., T], /, *args, **kwargs):
        try:
            with self.lock:
                self.dispatched += 1
                self.concurrency += 1
                if self.concurrency > self.max_concurrency:
                    self.max_concurrency = self.concurrency

            return f(*args, **kwargs)
        finally:
            with self.lock:
                self.completed += 1
                self.concurrency -= 1

DEFAULT: ThreadPool = ThreadPool.create('default', 200)

class ParallelService:
    def __init__(self, handler: 'ParallelHandler'):
        self.handler = handler
        self.collection = handler.collection
        self.pool = handler.pool
        self.name = handler.pool.name

    def as_completed(self, fn: Callable[..., T]) -> Iterator[T]:
        collection = self.collection
        if not collection:
            return iter([])

        pool = self.handler.pool
        self.handler.print_begin()

        with log_timing(f'parallel.as_completed(size={len(collection)}, pool={self.name})'):
            futures = [pool.executor().submit(functools.partial(pool.metrics, fn, t)) for t in collection]
            for t in as_completed(futures):
                yield t.result()

    def map(self, fn: Callable[..., T]) -> Iterator[T]:
        collection = self.collection
        if not collection:
            return iter([])

        pool = self.handler.pool
        self.handler.print_begin()

        with log_timing(f'parallel.map(size={len(collection)}, pool={self.name})'):
            return pool.executor().map(functools.partial(pool.metrics, fn), collection)

    def collect(self, fn: Callable[..., T]) -> list[T]:
        # the same as join() only to have better semantics by callers
        return self.join(fn, f_name='collect')

    def join(self, fn: Callable[..., T], f_name = 'join') -> list[T]:
        collection = self.collection
        if not collection:
            return []

        pool = self.handler.pool
        self.handler.print_begin()

        with log_timing(f'parallel.{f_name}(size={len(collection)}, pool={self.name})'):
            return list(pool.executor().map(functools.partial(pool.metrics, fn), collection))

    def sample(self, fn: Callable[..., T], samples = 3) -> list[T]:
        collection = self.collection
        if not collection:
            return []

        pool = self.handler.pool

        name = self.name
        if samples > len(collection):
            samples = len(collection)

        # allow one down node
        if samples == len(collection) and samples > 2:
            samples -= 1

        self.handler.samples = samples
        self.handler.print_begin()

        # 1. If 3 samples are requested out of 96 nodes, first 9 pods are examined concurrently.
        # 2. If at least 3 samples are acquired, the method returns with the first 3 samples.
        # 3. If not all 3 samples are acquired, the next 9 pods are examined concurrently, and so on.
        # 4. After all 96 nodes are examined, if the number of samples is less than 3, the samples are returned.
        batch_size = min(len(collection), samples * 3)

        # emulate pod failure with more than one batch
        # collection = ['cs-a7b13e29bd-cs-a7b13e29bd-default-sts-9', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-0', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-1', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-2']
        # batch_size = 3

        batch = collection[:batch_size]
        collection = collection[batch_size:]

        results: list[T] = []

        batch_no = 0
        while samples and batch:
            with log_timing(f'parallel.sample(samples={samples}, batch_no={batch_no}, batch_size={len(batch)}, pool={name})'):
                futures = [pool.executor().submit(functools.partial(pool.metrics, fn, e)) for e in batch]
                for f in as_completed(futures):
                    with log_exc():
                        r = f.result()
                        if isinstance(r, ErrorAware):
                            if not r.has_error():
                                results.append(r)
                                samples -= 1
                        else:
                            results.append(r)
                            samples -= 1

                        if not samples:
                            break

            if samples:
                if batch_size < len(collection):
                    batch = collection[:batch_size]
                    collection = collection[batch_size:]
                else:
                    batch = collection
                    collection = []

                batch_no += 1

        return results

class ParallelHandler:
    def __init__(self, collection: list, msg: str = None, pool = DEFAULT):
        self.collection = collection
        self.msg = msg
        if msg and msg.startswith('d`'):
            if ConfigHolder().config.is_debug():
                self.msg = msg.replace('d`', '', 1)
            else:
                self.msg = None
        self.pool = pool

        self.samples = sys.maxsize
        self.begin = []
        self.end = []
        self.start_time = None

    def __enter__(self) -> ParallelService:
        self.start_time = time.time()

        self.pool.executor().__enter__()

        return ParallelService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # do not shut down executor until kaqing exits
        # if self.executor:
        #     self.executor.__exit__(exc_type, exc_val, exc_tb)

        self.print_end()

        return False

    def size(self):
        if not self.collection:
            return 0

        return len(self.collection)

    def print_begin(self):
        if not self.msg:
            return

        self.begin = []
        self.end = []
        size = self.size()
        offloaded = False
        sampling = False
        if size == 0:
            offloaded = True
            msg = self.msg.replace('{size}', '1')
        elif size > 1 and self.samples == sys.maxsize:
            msg = self.msg.replace('{size}', f'{size}')
        elif self.samples < sys.maxsize:
            sampling = True
            samples = self.samples
            if self.samples > size:
                samples = size
            msg = self.msg.replace('{size}', f'{samples}/{size} sample')
        else:
            msg = self.msg.replace('{size}', f'{size}')

        for token in msg.split(' '):
            if '|' in token:
                self.begin.append(token.split('|')[0])
                if not sampling and not offloaded:
                    self.end.append(token.split('|')[1])
            else:
                self.begin.append(token)
                if not sampling and not offloaded:
                    self.end.append(token)

        if offloaded:
            self.ctx.debug(f'{" ".join(self.begin)} offloaded...')
        else:
            debug(f'{" ".join(self.begin)} with {self.pool.workers} workers...')

    def print_end(self):
        if self.end:
            debug(f'{" ".join(self.end)} in {elapsed_time(self.start_time)}.')

def parallelize(collection: list, msg: str = None, pool = DEFAULT):
    return ParallelHandler(collection, msg=msg, pool=pool)

class OffloadHandler(ParallelHandler):
    def __init__(self, do_offload = True, msg: str = None, pool = DEFAULT):
        super().__init__(None, msg=msg, pool=pool)
        self.do_offload = do_offload

    def __enter__(self):
        self.start_time = time.time()

        if self.do_offload:
            self.pool.executor().__enter__()

        return self.submit

    def __exit__(self, exc_type, exc_val, exc_tb):
        # do not shut down executor until kaqing exits
        # if self.executor:
        #     self.executor.__exit__(exc_type, exc_val, exc_tb)

        self.print_end()

        return False

    def submit(self, fn: Callable[..., T], /, *args, **kwargs) -> Future[T]:
        if self.do_offload:
            pool = self.pool
            self.print_begin()

            return pool.executor().submit(functools.partial(pool.metrics, fn, *args, **kwargs))

        # foreground
        future = Future()
        future.set_result(fn(*args, **kwargs))

        return future

def offload(do_offload = True, msg: str = None, pool = DEFAULT):
    return OffloadHandler(do_offload=do_offload, msg=msg, pool=pool)