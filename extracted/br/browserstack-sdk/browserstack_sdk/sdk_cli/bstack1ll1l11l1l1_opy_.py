# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1ll1l111lll_opy_:
    timeout: int
    bstack1ll1l111ll1_opy_: Union[None, Callable]
    bstack1ll1l11l1ll_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1ll1l11l111_opy_=None, bstack1ll1l111ll1_opy_=None, bstack1ll1l11l1ll_opy_=None):
        if bstack1ll1l11l111_opy_ is None:
            bstack1ll1l11l111_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1ll1l11l111_opy_ = bstack1ll1l11l111_opy_
        self.bstack1ll1l111ll1_opy_ = bstack1ll1l111ll1_opy_
        self.bstack1ll1l11l1ll_opy_ = bstack1ll1l11l1ll_opy_
        self.queue = queue.Queue()
        self.bstack1ll1l11l11l_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack1ll1lll_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤ࡯ࡵࡢ࠻ࠢࠥጙ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1ll1l11l111_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1ll1l11l11l_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1ll1l11l11l_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1ll1l111ll1_opy_):
                        self.bstack1ll1l111ll1_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1ll1l11l1ll_opy_):
                    self.bstack1ll1l11l1ll_opy_(e)