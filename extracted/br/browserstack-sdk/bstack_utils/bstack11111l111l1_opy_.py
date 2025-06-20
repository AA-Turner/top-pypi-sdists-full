# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack11111l11lll_opy_ = 1000
bstack11111l111ll_opy_ = 2
class bstack11111l11111_opy_:
    def __init__(self, handler, bstack111111lllll_opy_=bstack11111l11lll_opy_, bstack11111l1111l_opy_=bstack11111l111ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111111lllll_opy_ = bstack111111lllll_opy_
        self.bstack11111l1111l_opy_ = bstack11111l1111l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111lll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111111llll1_opy_()
    def bstack111111llll1_opy_(self):
        self.bstack111111lll1_opy_ = threading.Event()
        def bstack11111l11l1l_opy_():
            self.bstack111111lll1_opy_.wait(self.bstack11111l1111l_opy_)
            if not self.bstack111111lll1_opy_.is_set():
                self.bstack11111l1l111_opy_()
        self.timer = threading.Thread(target=bstack11111l11l1l_opy_, daemon=True)
        self.timer.start()
    def bstack11111l11l11_opy_(self):
        try:
            if self.bstack111111lll1_opy_ and not self.bstack111111lll1_opy_.is_set():
                self.bstack111111lll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠪ࡟ࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࡲ࡞ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࠧằ") + (str(e) or bstack11ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡣࡰࡰࡹࡩࡷࡺࡥࡥࠢࡷࡳࠥࡹࡴࡳ࡫ࡱ࡫ࠧẲ")))
        finally:
            self.timer = None
    def bstack11111l11ll1_opy_(self):
        if self.timer:
            self.bstack11111l11l11_opy_()
        self.bstack111111llll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111111lllll_opy_:
                threading.Thread(target=self.bstack11111l1l111_opy_).start()
    def bstack11111l1l111_opy_(self, source = bstack11ll11_opy_ (u"ࠬ࠭ẳ")):
        with self.lock:
            if not self.queue:
                self.bstack11111l11ll1_opy_()
                return
            data = self.queue[:self.bstack111111lllll_opy_]
            del self.queue[:self.bstack111111lllll_opy_]
        self.handler(data)
        if source != bstack11ll11_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨẴ"):
            self.bstack11111l11ll1_opy_()
    def shutdown(self):
        self.bstack11111l11l11_opy_()
        while self.queue:
            self.bstack11111l1l111_opy_(source=bstack11ll11_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩẵ"))