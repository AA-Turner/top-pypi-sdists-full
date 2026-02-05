# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1lll1llll1l_opy_:
    timeout: int
    bstack1lll1lll1ll_opy_: Union[None, Callable]
    bstack1llll111111_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1lll1lllll1_opy_=None, bstack1lll1lll1ll_opy_=None, bstack1llll111111_opy_=None):
        if bstack1lll1lllll1_opy_ is None:
            bstack1lll1lllll1_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1lll1lllll1_opy_ = bstack1lll1lllll1_opy_
        self.bstack1lll1lll1ll_opy_ = bstack1lll1lll1ll_opy_
        self.bstack1llll111111_opy_ = bstack1llll111111_opy_
        self.queue = queue.Queue()
        self.bstack1lll1llllll_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack11l1ll1_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢ࡭ࡳࡧࡀࠠࠣᄻ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1lll1lllll1_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1lll1llllll_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1lll1llllll_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1lll1lll1ll_opy_):
                        self.bstack1lll1lll1ll_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1llll111111_opy_):
                    self.bstack1llll111111_opy_(e)