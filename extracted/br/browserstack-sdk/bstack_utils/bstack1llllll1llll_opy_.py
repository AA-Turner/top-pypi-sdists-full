# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1lllllll111l_opy_ = 1000
bstack1llllll1l111_opy_ = 2
class bstack1lllllll1111_opy_:
    def __init__(self, handler, bstack1llllll1l11l_opy_=bstack1lllllll111l_opy_, bstack1llllll1l1ll_opy_=bstack1llllll1l111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llllll1l11l_opy_ = bstack1llllll1l11l_opy_
        self.bstack1llllll1l1ll_opy_ = bstack1llllll1l1ll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111111l1l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llllll1l1l1_opy_()
    def bstack1llllll1l1l1_opy_(self):
        self.bstack1111111l1l_opy_ = threading.Event()
        def bstack1lllllll11l1_opy_():
            self.bstack1111111l1l_opy_.wait(self.bstack1llllll1l1ll_opy_)
            if not self.bstack1111111l1l_opy_.is_set():
                self.bstack1llllll1lll1_opy_()
        self.timer = threading.Thread(target=bstack1lllllll11l1_opy_, daemon=True)
        self.timer.start()
    def bstack1llllll1ll1l_opy_(self):
        try:
            if self.bstack1111111l1l_opy_ and not self.bstack1111111l1l_opy_.is_set():
                self.bstack1111111l1l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩᾓ") + (str(e) or bstack1l11ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢᾔ")))
        finally:
            self.timer = None
    def bstack1llllll1ll11_opy_(self):
        if self.timer:
            self.bstack1llllll1ll1l_opy_()
        self.bstack1llllll1l1l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llllll1l11l_opy_:
                threading.Thread(target=self.bstack1llllll1lll1_opy_).start()
    def bstack1llllll1lll1_opy_(self, source = bstack1l11ll1_opy_ (u"ࠧࠨᾕ")):
        with self.lock:
            if not self.queue:
                self.bstack1llllll1ll11_opy_()
                return
            data = self.queue[:self.bstack1llllll1l11l_opy_]
            del self.queue[:self.bstack1llllll1l11l_opy_]
        self.handler(data)
        if source != bstack1l11ll1_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪᾖ"):
            self.bstack1llllll1ll11_opy_()
    def shutdown(self):
        self.bstack1llllll1ll1l_opy_()
        while self.queue:
            self.bstack1llllll1lll1_opy_(source=bstack1l11ll1_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫᾗ"))