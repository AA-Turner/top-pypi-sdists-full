# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1llll11111l1_opy_ = 1000
bstack1llll111l111_opy_ = 2
class bstack1llll1111lll_opy_:
    def __init__(self, handler, bstack1llll1111l1l_opy_=bstack1llll11111l1_opy_, bstack1lll1lllllll_opy_=bstack1llll111l111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llll1111l1l_opy_ = bstack1llll1111l1l_opy_
        self.bstack1lll1lllllll_opy_ = bstack1lll1lllllll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll1llll11_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llll11111ll_opy_()
    def bstack1llll11111ll_opy_(self):
        self.bstack1lll1llll11_opy_ = threading.Event()
        def bstack1llll1111111_opy_():
            self.bstack1lll1llll11_opy_.wait(self.bstack1lll1lllllll_opy_)
            if not self.bstack1lll1llll11_opy_.is_set():
                self.bstack1llll111111l_opy_()
        self.timer = threading.Thread(target=bstack1llll1111111_opy_, daemon=True)
        self.timer.start()
    def bstack1lll1llllll1_opy_(self):
        try:
            if self.bstack1lll1llll11_opy_ and not self.bstack1lll1llll11_opy_.is_set():
                self.bstack1lll1llll11_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨℨ") + (str(e) or bstack1l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨ℩")))
        finally:
            self.timer = None
    def bstack1llll1111ll1_opy_(self):
        if self.timer:
            self.bstack1lll1llllll1_opy_()
        self.bstack1llll11111ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llll1111l1l_opy_:
                threading.Thread(target=self.bstack1llll111111l_opy_).start()
    def bstack1llll111111l_opy_(self, source = bstack1l1111_opy_ (u"࠭ࠧK")):
        with self.lock:
            if not self.queue:
                self.bstack1llll1111ll1_opy_()
                return
            data = self.queue[:self.bstack1llll1111l1l_opy_]
            del self.queue[:self.bstack1llll1111l1l_opy_]
        self.handler(data)
        if source != bstack1l1111_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩÅ"):
            self.bstack1llll1111ll1_opy_()
    def shutdown(self):
        self.bstack1lll1llllll1_opy_()
        while self.queue:
            self.bstack1llll111111l_opy_(source=bstack1l1111_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪℬ"))