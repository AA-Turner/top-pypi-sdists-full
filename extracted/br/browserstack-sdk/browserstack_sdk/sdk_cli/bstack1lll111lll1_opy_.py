# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import threading
import queue
from typing import Callable, Union
class bstack1lll11l111l_opy_:
    timeout: int
    bstack1lll111ll1l_opy_: Union[None, Callable]
    bstack1lll11l1111_opy_: Union[None, Callable]
    def __init__(self, timeout=10, bstack1lll111ll11_opy_=None, bstack1lll111ll1l_opy_=None, bstack1lll11l1111_opy_=None):
        if bstack1lll111ll11_opy_ is None:
            bstack1lll111ll11_opy_ = min(os.cpu_count() or 2, 8)
        self.timeout = timeout
        self.bstack1lll111ll11_opy_ = bstack1lll111ll11_opy_
        self.bstack1lll111ll1l_opy_ = bstack1lll111ll1l_opy_
        self.bstack1lll11l1111_opy_ = bstack1lll11l1111_opy_
        self.queue = queue.Queue()
        self.bstack1lll111llll_opy_ = threading.Event()
        self.threads = []
    def enqueue(self, job: Callable):
        if not callable(job):
            raise ValueError(bstack11l11_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢ࡭ࡳࡧࡀࠠࠣᇎ") + type(job))
        self.queue.put(job)
    def start(self):
        if self.threads:
            return
        self.threads = [threading.Thread(target=self.worker, daemon=True) for _ in range(self.bstack1lll111ll11_opy_)]
        for thread in self.threads:
            thread.start()
    def stop(self):
        if not self.threads:
            return
        if not self.queue.empty():
            self.queue.join()
        self.bstack1lll111llll_opy_.set()
        for _ in self.threads:
            self.queue.put(None)
        for thread in self.threads:
            thread.join()
        self.threads.clear()
    def worker(self):
        while not self.bstack1lll111llll_opy_.is_set():
            try:
                job = self.queue.get(block=True, timeout=self.timeout)
                if job is None:
                    break
                try:
                    job()
                except Exception as e:
                    if callable(self.bstack1lll111ll1l_opy_):
                        self.bstack1lll111ll1l_opy_(e, job)
                finally:
                    self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                if callable(self.bstack1lll11l1111_opy_):
                    self.bstack1lll11l1111_opy_(e)