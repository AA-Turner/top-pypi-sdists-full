# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1lll11l1lll_opy_:
    timeout: int
    bstack1lll11ll11l_opy_: Union[None, Callable]
    bstack1lll11lll11_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1lll11ll1l1_opy_=None, bstack1lll11ll11l_opy_=None, bstack1lll11lll11_opy_=None):
        if bstack1lll11ll1l1_opy_ is None:
            bstack1lll11ll1l1_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1lll11ll1l1_opy_ = bstack1lll11ll1l1_opy_
        self.bstack1lll11ll11l_opy_ = bstack1lll11ll11l_opy_
        self.bstack1lll11lll11_opy_ = bstack1lll11lll11_opy_
        self.queue = queue.Queue()
        self.bstack1lll11ll1ll_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack11lllll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣ࡮ࡴࡨ࠺ࠡࠤᅑ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1lll11ll1l1_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1lll11ll1ll_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1lll11ll1ll_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1lll11ll11l_opy_):
                        self.bstack1lll11ll11l_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1lll11lll11_opy_):
                    self.bstack1lll11lll11_opy_(e)