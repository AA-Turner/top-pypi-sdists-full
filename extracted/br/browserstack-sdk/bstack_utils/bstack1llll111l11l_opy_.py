# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1llll111l1l1_opy_ = 2
class bstack1llll1111lll_opy_:
    def __init__(self, handler, bstack1llll1111l11_opy_=BATCH_SIZE, bstack1llll111111l_opy_=bstack1llll111l1l1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llll1111l11_opy_ = bstack1llll1111l11_opy_
        self.bstack1llll111111l_opy_ = bstack1llll111111l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll1ll1l1ll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llll1111l1l_opy_()
    def bstack1llll1111l1l_opy_(self):
        self.bstack1ll1ll1l1ll_opy_ = threading.Event()
        def bstack1llll111l111_opy_():
            self.bstack1ll1ll1l1ll_opy_.wait(self.bstack1llll111111l_opy_)
            if not self.bstack1ll1ll1l1ll_opy_.is_set():
                self.bstack1llll1111ll1_opy_()
        self.timer = threading.Thread(target=bstack1llll111l111_opy_, daemon=True)
        self.timer.start()
    def bstack1llll11111l1_opy_(self):
        try:
            if self.bstack1ll1ll1l1ll_opy_ and not self.bstack1ll1ll1l1ll_opy_.is_set():
                self.bstack1ll1ll1l1ll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨṺ") + (str(e) or bstack1ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨṻ")))
        finally:
            self.timer = None
    def bstack1llll11111ll_opy_(self):
        if self.timer:
            self.bstack1llll11111l1_opy_()
        self.bstack1llll1111l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llll1111l11_opy_:
                threading.Thread(target=self.bstack1llll1111ll1_opy_).start()
    def bstack1llll1111ll1_opy_(self, source = bstack1ll111_opy_ (u"࠭ࠧṼ")):
        with self.lock:
            if not self.queue:
                self.bstack1llll11111ll_opy_()
                return
            data = self.queue[:self.bstack1llll1111l11_opy_]
            del self.queue[:self.bstack1llll1111l11_opy_]
        self.handler(data)
        if source != bstack1ll111_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩṽ"):
            self.bstack1llll11111ll_opy_()
    def shutdown(self):
        self.bstack1llll11111l1_opy_()
        while self.queue:
            self.bstack1llll1111ll1_opy_(source=bstack1ll111_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪṾ"))