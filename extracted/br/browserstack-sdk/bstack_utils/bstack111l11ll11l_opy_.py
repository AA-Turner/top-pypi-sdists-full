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
import logging
logger = logging.getLogger(__name__)
bstack111l11ll1l1_opy_ = 1000
bstack111l11l1ll1_opy_ = 2
class bstack111l11l1lll_opy_:
    def __init__(self, handler, bstack111l11ll1ll_opy_=bstack111l11ll1l1_opy_, bstack111l11ll111_opy_=bstack111l11l1ll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l11ll1ll_opy_ = bstack111l11ll1ll_opy_
        self.bstack111l11ll111_opy_ = bstack111l11ll111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111l1l111_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111l11lll1l_opy_()
    def bstack111l11lll1l_opy_(self):
        self.bstack1111l1l111_opy_ = threading.Event()
        def bstack111l11llll1_opy_():
            self.bstack1111l1l111_opy_.wait(self.bstack111l11ll111_opy_)
            if not self.bstack1111l1l111_opy_.is_set():
                self.bstack111l11l1l1l_opy_()
        self.timer = threading.Thread(target=bstack111l11llll1_opy_, daemon=True)
        self.timer.start()
    def bstack111l11lll11_opy_(self):
        try:
            if self.bstack1111l1l111_opy_ and not self.bstack1111l1l111_opy_.is_set():
                self.bstack1111l1l111_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨᵷ") + (str(e) or bstack1llllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨᵸ")))
        finally:
            self.timer = None
    def bstack111l11lllll_opy_(self):
        if self.timer:
            self.bstack111l11lll11_opy_()
        self.bstack111l11lll1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l11ll1ll_opy_:
                threading.Thread(target=self.bstack111l11l1l1l_opy_).start()
    def bstack111l11l1l1l_opy_(self, source = bstack1llllll_opy_ (u"࠭ࠧᵹ")):
        with self.lock:
            if not self.queue:
                self.bstack111l11lllll_opy_()
                return
            data = self.queue[:self.bstack111l11ll1ll_opy_]
            del self.queue[:self.bstack111l11ll1ll_opy_]
        self.handler(data)
        if source != bstack1llllll_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩᵺ"):
            self.bstack111l11lllll_opy_()
    def shutdown(self):
        self.bstack111l11lll11_opy_()
        while self.queue:
            self.bstack111l11l1l1l_opy_(source=bstack1llllll_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪᵻ"))