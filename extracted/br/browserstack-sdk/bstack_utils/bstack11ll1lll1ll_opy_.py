# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack11ll1llll1l_opy_ = 1000
bstack11ll1lll1l1_opy_ = 2
class bstack11ll1llllll_opy_:
    def __init__(self, handler, bstack11lll1111l1_opy_=bstack11ll1llll1l_opy_, bstack11ll1lll111_opy_=bstack11ll1lll1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11lll1111l1_opy_ = bstack11lll1111l1_opy_
        self.bstack11ll1lll111_opy_ = bstack11ll1lll111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111111l11_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack11lll11111l_opy_()
    def bstack11lll11111l_opy_(self):
        self.bstack1111111l11_opy_ = threading.Event()
        def bstack11ll1llll11_opy_():
            self.bstack1111111l11_opy_.wait(self.bstack11ll1lll111_opy_)
            if not self.bstack1111111l11_opy_.is_set():
                self.bstack11lll111111_opy_()
        self.timer = threading.Thread(target=bstack11ll1llll11_opy_, daemon=True)
        self.timer.start()
    def bstack11ll1lll11l_opy_(self):
        try:
            if self.bstack1111111l11_opy_ and not self.bstack1111111l11_opy_.is_set():
                self.bstack1111111l11_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡝ࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࡷࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࠬᘙ") + (str(e) or bstack1ll11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡨࡵ࡮ࡷࡧࡵࡸࡪࡪࠠࡵࡱࠣࡷࡹࡸࡩ࡯ࡩࠥᘚ")))
        finally:
            self.timer = None
    def bstack11ll1lllll1_opy_(self):
        if self.timer:
            self.bstack11ll1lll11l_opy_()
        self.bstack11lll11111l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11lll1111l1_opy_:
                threading.Thread(target=self.bstack11lll111111_opy_).start()
    def bstack11lll111111_opy_(self, source = bstack1ll11ll_opy_ (u"ࠪࠫᘛ")):
        with self.lock:
            if not self.queue:
                self.bstack11ll1lllll1_opy_()
                return
            data = self.queue[:self.bstack11lll1111l1_opy_]
            del self.queue[:self.bstack11lll1111l1_opy_]
        self.handler(data)
        if source != bstack1ll11ll_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᘜ"):
            self.bstack11ll1lllll1_opy_()
    def shutdown(self):
        self.bstack11ll1lll11l_opy_()
        while self.queue:
            self.bstack11lll111111_opy_(source=bstack1ll11ll_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᘝ"))