# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll11ll1111_opy_ = 2
class bstack1lll11ll111l_opy_:
    def __init__(self, handler, bstack1lll11ll1l1l_opy_=BATCH_SIZE, bstack1lll11ll11l1_opy_=bstack1lll11ll1111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll11ll1l1l_opy_ = bstack1lll11ll1l1l_opy_
        self.bstack1lll11ll11l1_opy_ = bstack1lll11ll11l1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll1llllll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll11ll1l11_opy_()
    def bstack1lll11ll1l11_opy_(self):
        self.bstack1ll1llllll1_opy_ = threading.Event()
        def bstack1lll11ll1ll1_opy_():
            self.bstack1ll1llllll1_opy_.wait(self.bstack1lll11ll11l1_opy_)
            if not self.bstack1ll1llllll1_opy_.is_set():
                self.bstack1lll11ll11ll_opy_()
        self.timer = threading.Thread(target=bstack1lll11ll1ll1_opy_, daemon=True)
        self.timer.start()
    def bstack1lll11ll1lll_opy_(self):
        try:
            if self.bstack1ll1llllll1_opy_ and not self.bstack1ll1llllll1_opy_.is_set():
                self.bstack1ll1llllll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1111_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⍋") + (str(e) or bstack1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⍌")))
        finally:
            self.timer = None
    def bstack1lll11l1lll1_opy_(self):
        if self.timer:
            self.bstack1lll11ll1lll_opy_()
        self.bstack1lll11ll1l11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll11ll1l1l_opy_:
                threading.Thread(target=self.bstack1lll11ll11ll_opy_).start()
    def bstack1lll11ll11ll_opy_(self, source = bstack1111_opy_ (u"ࠧࠨ⍍")):
        with self.lock:
            if not self.queue:
                self.bstack1lll11l1lll1_opy_()
                return
            data = self.queue[:self.bstack1lll11ll1l1l_opy_]
            del self.queue[:self.bstack1lll11ll1l1l_opy_]
        self.handler(data)
        if source != bstack1111_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⍎"):
            self.bstack1lll11l1lll1_opy_()
    def shutdown(self):
        self.bstack1lll11ll1lll_opy_()
        while self.queue:
            self.bstack1lll11ll11ll_opy_(source=bstack1111_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⍏"))