# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1ll111l1lll1_opy_ = 2
class bstack1ll111l1ll11_opy_:
    def __init__(self, handler, bstack1ll111l1l111_opy_=BATCH_SIZE, bstack1ll111l11lll_opy_=bstack1ll111l1lll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll111l1l111_opy_ = bstack1ll111l1l111_opy_
        self.bstack1ll111l11lll_opy_ = bstack1ll111l11lll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1l11lllll11_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll111ll1111_opy_()
    def bstack1ll111ll1111_opy_(self):
        self.bstack1l11lllll11_opy_ = threading.Event()
        def bstack1ll111l1l1l1_opy_():
            self.bstack1l11lllll11_opy_.wait(self.bstack1ll111l11lll_opy_)
            if not self.bstack1l11lllll11_opy_.is_set():
                self.bstack1ll111l1llll_opy_()
        self.timer = threading.Thread(target=bstack1ll111l1l1l1_opy_, daemon=True)
        self.timer.start()
    def bstack1ll111l1l11l_opy_(self):
        try:
            if self.bstack1l11lllll11_opy_ and not self.bstack1l11lllll11_opy_.is_set():
                self.bstack1l11lllll11_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⨡") + (str(e) or bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⨢")))
        finally:
            self.timer = None
    def bstack1ll111l1l1ll_opy_(self):
        if self.timer:
            self.bstack1ll111l1l11l_opy_()
        self.bstack1ll111ll1111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll111l1l111_opy_:
                threading.Thread(target=self.bstack1ll111l1llll_opy_).start()
    def bstack1ll111l1llll_opy_(self, source = bstack1l1llll_opy_ (u"ࠧࠨ⨣")):
        with self.lock:
            if not self.queue:
                self.bstack1ll111l1l1ll_opy_()
                return
            data = self.queue[:self.bstack1ll111l1l111_opy_]
            del self.queue[:self.bstack1ll111l1l111_opy_]
        self.handler(data)
        if source != bstack1l1llll_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⨤"):
            self.bstack1ll111l1l1ll_opy_()
    def shutdown(self):
        self.bstack1ll111l1l11l_opy_()
        while self.queue:
            self.bstack1ll111l1llll_opy_(source=bstack1l1llll_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⨥"))