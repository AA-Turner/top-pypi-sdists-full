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
import threading
import logging
logger = logging.getLogger(__name__)
bstack1lll1lll11l1_opy_ = 1000
bstack1lll1lll1ll1_opy_ = 2
class bstack1lll1lll1l1l_opy_:
    def __init__(self, handler, bstack1lll1lll11ll_opy_=bstack1lll1lll11l1_opy_, bstack1lll1lll1l11_opy_=bstack1lll1lll1ll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1lll11ll_opy_ = bstack1lll1lll11ll_opy_
        self.bstack1lll1lll1l11_opy_ = bstack1lll1lll1l11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll11ll1ll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll1llll1l1_opy_()
    def bstack1lll1llll1l1_opy_(self):
        self.bstack1lll11ll1ll_opy_ = threading.Event()
        def bstack1lll1llll1ll_opy_():
            self.bstack1lll11ll1ll_opy_.wait(self.bstack1lll1lll1l11_opy_)
            if not self.bstack1lll11ll1ll_opy_.is_set():
                self.bstack1lll1llll111_opy_()
        self.timer = threading.Thread(target=bstack1lll1llll1ll_opy_, daemon=True)
        self.timer.start()
    def bstack1lll1llll11l_opy_(self):
        try:
            if self.bstack1lll11ll1ll_opy_ and not self.bstack1lll11ll1ll_opy_.is_set():
                self.bstack1lll11ll1ll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⅌") + (str(e) or bstack11lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⅍")))
        finally:
            self.timer = None
    def bstack1lll1lll111l_opy_(self):
        if self.timer:
            self.bstack1lll1llll11l_opy_()
        self.bstack1lll1llll1l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1lll11ll_opy_:
                threading.Thread(target=self.bstack1lll1llll111_opy_).start()
    def bstack1lll1llll111_opy_(self, source = bstack11lllll_opy_ (u"ࠧࠨⅎ")):
        with self.lock:
            if not self.queue:
                self.bstack1lll1lll111l_opy_()
                return
            data = self.queue[:self.bstack1lll1lll11ll_opy_]
            del self.queue[:self.bstack1lll1lll11ll_opy_]
        self.handler(data)
        if source != bstack11lllll_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⅏"):
            self.bstack1lll1lll111l_opy_()
    def shutdown(self):
        self.bstack1lll1llll11l_opy_()
        while self.queue:
            self.bstack1lll1llll111_opy_(source=bstack11lllll_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⅐"))