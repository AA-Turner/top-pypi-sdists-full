# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1ll1llll11ll_opy_ = 2
class bstack1ll1lllll111_opy_:
    def __init__(self, handler, bstack1ll1lllll1l1_opy_=BATCH_SIZE, bstack1ll1llll1l11_opy_=bstack1ll1llll11ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1lllll1l1_opy_ = bstack1ll1lllll1l1_opy_
        self.bstack1ll1llll1l11_opy_ = bstack1ll1llll1l11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll11lllll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll1lllll11l_opy_()
    def bstack1ll1lllll11l_opy_(self):
        self.bstack1ll11lllll1_opy_ = threading.Event()
        def bstack1ll1llll1lll_opy_():
            self.bstack1ll11lllll1_opy_.wait(self.bstack1ll1llll1l11_opy_)
            if not self.bstack1ll11lllll1_opy_.is_set():
                self.bstack1ll1llll1l1l_opy_()
        self.timer = threading.Thread(target=bstack1ll1llll1lll_opy_, daemon=True)
        self.timer.start()
    def bstack1ll1llll1ll1_opy_(self):
        try:
            if self.bstack1ll11lllll1_opy_ and not self.bstack1ll11lllll1_opy_.is_set():
                self.bstack1ll11lllll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⒍") + (str(e) or bstack1ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⒎")))
        finally:
            self.timer = None
    def bstack1ll1llll11l1_opy_(self):
        if self.timer:
            self.bstack1ll1llll1ll1_opy_()
        self.bstack1ll1lllll11l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1lllll1l1_opy_:
                threading.Thread(target=self.bstack1ll1llll1l1l_opy_).start()
    def bstack1ll1llll1l1l_opy_(self, source = bstack1ll11_opy_ (u"ࠧࠨ⒏")):
        with self.lock:
            if not self.queue:
                self.bstack1ll1llll11l1_opy_()
                return
            data = self.queue[:self.bstack1ll1lllll1l1_opy_]
            del self.queue[:self.bstack1ll1lllll1l1_opy_]
        self.handler(data)
        if source != bstack1ll11_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⒐"):
            self.bstack1ll1llll11l1_opy_()
    def shutdown(self):
        self.bstack1ll1llll1ll1_opy_()
        while self.queue:
            self.bstack1ll1llll1l1l_opy_(source=bstack1ll11_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⒑"))