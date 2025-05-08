# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack111l11ll1ll_opy_ = 1000
bstack111l11ll1l1_opy_ = 2
class bstack111l11ll111_opy_:
    def __init__(self, handler, bstack111l11lllll_opy_=bstack111l11ll1ll_opy_, bstack111l11l1l1l_opy_=bstack111l11ll1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111l11lllll_opy_ = bstack111l11lllll_opy_
        self.bstack111l11l1l1l_opy_ = bstack111l11l1l1l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111l1ll1l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111l11lll1l_opy_()
    def bstack111l11lll1l_opy_(self):
        self.bstack1111l1ll1l_opy_ = threading.Event()
        def bstack111l11llll1_opy_():
            self.bstack1111l1ll1l_opy_.wait(self.bstack111l11l1l1l_opy_)
            if not self.bstack1111l1ll1l_opy_.is_set():
                self.bstack111l11ll11l_opy_()
        self.timer = threading.Thread(target=bstack111l11llll1_opy_, daemon=True)
        self.timer.start()
    def bstack111l11l1lll_opy_(self):
        try:
            if self.bstack1111l1ll1l_opy_ and not self.bstack1111l1ll1l_opy_.is_set():
                self.bstack1111l1ll1l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠩ࡞ࡷࡹࡵࡰࡠࡶ࡬ࡱࡪࡸ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥ࠭ᵼ") + (str(e) or bstack1l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡫ࡤࠡࡶࡲࠤࡸࡺࡲࡪࡰࡪࠦᵽ")))
        finally:
            self.timer = None
    def bstack111l11lll11_opy_(self):
        if self.timer:
            self.bstack111l11l1lll_opy_()
        self.bstack111l11lll1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111l11lllll_opy_:
                threading.Thread(target=self.bstack111l11ll11l_opy_).start()
    def bstack111l11ll11l_opy_(self, source = bstack1l1lll_opy_ (u"ࠫࠬᵾ")):
        with self.lock:
            if not self.queue:
                self.bstack111l11lll11_opy_()
                return
            data = self.queue[:self.bstack111l11lllll_opy_]
            del self.queue[:self.bstack111l11lllll_opy_]
        self.handler(data)
        if source != bstack1l1lll_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᵿ"):
            self.bstack111l11lll11_opy_()
    def shutdown(self):
        self.bstack111l11l1lll_opy_()
        while self.queue:
            self.bstack111l11ll11l_opy_(source=bstack1l1lll_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨᶀ"))