# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1l1lll11l11_opy_:
    timeout: int
    bstack1l1lll1l111_opy_: Union[None, Callable]
    bstack1l1lll11lll_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1l1lll1l11l_opy_=None, bstack1l1lll1l111_opy_=None, bstack1l1lll11lll_opy_=None):
        if bstack1l1lll1l11l_opy_ is None:
            bstack1l1lll1l11l_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1l1lll1l11l_opy_ = bstack1l1lll1l11l_opy_
        self.bstack1l1lll1l111_opy_ = bstack1l1lll1l111_opy_
        self.bstack1l1lll11lll_opy_ = bstack1l1lll11lll_opy_
        self.queue = queue.Queue()
        self.bstack1l1lll11l1l_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack1ll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣ࡮ࡴࡨ࠺ࠡࠤᑚ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1l1lll1l11l_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1l1lll11l1l_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1l1lll11l1l_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1l1lll1l111_opy_):
                        self.bstack1l1lll1l111_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1l1lll11lll_opy_):
                    self.bstack1l1lll11lll_opy_(e)