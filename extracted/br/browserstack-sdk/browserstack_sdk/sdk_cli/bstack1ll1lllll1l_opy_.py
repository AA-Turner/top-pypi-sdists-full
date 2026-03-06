# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1lll1111111_opy_:
    timeout: int
    bstack1ll1lllll11_opy_: Union[None, Callable]
    bstack1ll1llll1ll_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1ll1lllllll_opy_=None, bstack1ll1lllll11_opy_=None, bstack1ll1llll1ll_opy_=None):
        if bstack1ll1lllllll_opy_ is None:
            bstack1ll1lllllll_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1ll1lllllll_opy_ = bstack1ll1lllllll_opy_
        self.bstack1ll1lllll11_opy_ = bstack1ll1lllll11_opy_
        self.bstack1ll1llll1ll_opy_ = bstack1ll1llll1ll_opy_
        self.queue = queue.Queue()
        self.bstack1ll1llllll1_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack1111_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡪࡰࡤ࠽ࠤࠧቐ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1ll1lllllll_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1ll1llllll1_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1ll1llllll1_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1ll1lllll11_opy_):
                        self.bstack1ll1lllll11_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1ll1llll1ll_opy_):
                    self.bstack1ll1llll1ll_opy_(e)