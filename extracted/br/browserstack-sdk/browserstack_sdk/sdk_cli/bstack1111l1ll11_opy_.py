# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import threading
import queue
from typing import Callable, Union
class bstack1111l1l1ll_opy_:
    timeout: int
    bstack1111l1l1l1_opy_: Union[None, Callable]
    bstack1111l1l11l_opy_: Union[None, Callable]
    def __init__(self, timeout=1, bstack1111l1ll1l_opy_=1, bstack1111l1l1l1_opy_=None, bstack1111l1l11l_opy_=None):
        self.timeout = timeout
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
        self.bstack1111l1l1l1_opy_ = bstack1111l1l1l1_opy_
        self.bstack1111l1l11l_opy_ = bstack1111l1l11l_opy_
        self.queue = queue.Queue()
        self.bstack1111l1l111_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack1llllll_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤ࡯ࡵࡢ࠻ࠢࠥဗ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1111l1ll1l_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1111l1l111_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1111l1l111_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1111l1l1l1_opy_):
                        self.bstack1111l1l1l1_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1111l1l11l_opy_):
                    self.bstack1111l1l11l_opy_(e)