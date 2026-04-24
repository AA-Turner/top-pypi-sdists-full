# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1ll11llll111_opy_ = 2
class bstack1ll11llllll1_opy_:
    def __init__(self, handler, bstack1ll11llll11l_opy_=BATCH_SIZE, bstack1ll11lllll11_opy_=bstack1ll11llll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll11llll11l_opy_ = bstack1ll11llll11l_opy_
        self.bstack1ll11lllll11_opy_ = bstack1ll11lllll11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1l1lll11ll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll1l1111111_opy_()
    def bstack1ll1l1111111_opy_(self):
        self.bstack1l1lll11ll1_opy_ = threading.Event()
        def bstack1ll11llll1ll_opy_():
            self.bstack1l1lll11ll1_opy_.wait(self.bstack1ll11lllll11_opy_)
            if not self.bstack1l1lll11ll1_opy_.is_set():
                self.bstack1ll11lllllll_opy_()
        self.timer = threading.Thread(target=bstack1ll11llll1ll_opy_, daemon=True)
        self.timer.start()
    def bstack1ll11llll1l1_opy_(self):
        try:
            if self.bstack1l1lll11ll1_opy_ and not self.bstack1l1lll11ll1_opy_.is_set():
                self.bstack1l1lll11ll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack111ll11_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⚚") + (str(e) or bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⚛")))
        finally:
            self.timer = None
    def bstack1ll11lllll1l_opy_(self):
        if self.timer:
            self.bstack1ll11llll1l1_opy_()
        self.bstack1ll1l1111111_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll11llll11l_opy_:
                threading.Thread(target=self.bstack1ll11lllllll_opy_).start()
    def bstack1ll11lllllll_opy_(self, source = bstack111ll11_opy_ (u"ࠧࠨ⚜")):
        with self.lock:
            if not self.queue:
                self.bstack1ll11lllll1l_opy_()
                return
            data = self.queue[:self.bstack1ll11llll11l_opy_]
            del self.queue[:self.bstack1ll11llll11l_opy_]
        self.handler(data)
        if source != bstack111ll11_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⚝"):
            self.bstack1ll11lllll1l_opy_()
    def shutdown(self):
        self.bstack1ll11llll1l1_opy_()
        while self.queue:
            self.bstack1ll11lllllll_opy_(source=bstack111ll11_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⚞"))