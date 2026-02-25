# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1lll11llll1_opy_:
    timeout: int
    bstack1lll11lll1l_opy_: Union[None, Callable]
    bstack1lll11lllll_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1lll11lll11_opy_=None, bstack1lll11lll1l_opy_=None, bstack1lll11lllll_opy_=None):
        if bstack1lll11lll11_opy_ is None:
            bstack1lll11lll11_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1lll11lll11_opy_ = bstack1lll11lll11_opy_
        self.bstack1lll11lll1l_opy_ = bstack1lll11lll1l_opy_
        self.bstack1lll11lllll_opy_ = bstack1lll11lllll_opy_
        self.queue = queue.Queue()
        self.bstack1lll11ll1ll_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack11l1l11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤ࡯ࡵࡢ࠻ࠢࠥᇗ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1lll11lll11_opy_)]
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
                    if callable(self.bstack1lll11lll1l_opy_):
                        self.bstack1lll11lll1l_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1lll11lllll_opy_):
                    self.bstack1lll11lllll_opy_(e)