# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1ll1ll11l11_opy_:
    timeout: int
    bstack1ll1ll111ll_opy_: Union[None, Callable]
    bstack1ll1ll11ll1_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1ll1ll11l1l_opy_=None, bstack1ll1ll111ll_opy_=None, bstack1ll1ll11ll1_opy_=None):
        if bstack1ll1ll11l1l_opy_ is None:
            bstack1ll1ll11l1l_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1ll1ll11l1l_opy_ = bstack1ll1ll11l1l_opy_
        self.bstack1ll1ll111ll_opy_ = bstack1ll1ll111ll_opy_
        self.bstack1ll1ll11ll1_opy_ = bstack1ll1ll11ll1_opy_
        self.queue = queue.Queue()
        self.bstack1ll1ll1l111_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack1111l_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣ࡮ࡴࡨ࠺ࠡࠤዮ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1ll1ll11l1l_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1ll1ll1l111_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1ll1ll1l111_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1ll1ll111ll_opy_):
                        self.bstack1ll1ll111ll_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1ll1ll11ll1_opy_):
                    self.bstack1ll1ll11ll1_opy_(e)