# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack11111111111_opy_ = 1000
bstack1111111111l_opy_ = 2
class bstack111111111l1_opy_:
    def __init__(self, handler, bstack1llllllllll1_opy_=bstack11111111111_opy_, bstack1lllllllllll_opy_=bstack1111111111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llllllllll1_opy_ = bstack1llllllllll1_opy_
        self.bstack1lllllllllll_opy_ = bstack1lllllllllll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111lll1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llllllll11l_opy_()
    def bstack1llllllll11l_opy_(self):
        self.bstack111111lll1_opy_ = threading.Event()
        def bstack1llllllll1l1_opy_():
            self.bstack111111lll1_opy_.wait(self.bstack1lllllllllll_opy_)
            if not self.bstack111111lll1_opy_.is_set():
                self.bstack111111111ll_opy_()
        self.timer = threading.Thread(target=bstack1llllllll1l1_opy_, daemon=True)
        self.timer.start()
    def bstack1llllllll1ll_opy_(self):
        try:
            if self.bstack111111lll1_opy_ and not self.bstack111111lll1_opy_.is_set():
                self.bstack111111lll1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠨ࡝ࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࡷࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࠬᾖ") + (str(e) or bstack11l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡨࡵ࡮ࡷࡧࡵࡸࡪࡪࠠࡵࡱࠣࡷࡹࡸࡩ࡯ࡩࠥᾗ")))
        finally:
            self.timer = None
    def bstack1lllllllll1l_opy_(self):
        if self.timer:
            self.bstack1llllllll1ll_opy_()
        self.bstack1llllllll11l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llllllllll1_opy_:
                threading.Thread(target=self.bstack111111111ll_opy_).start()
    def bstack111111111ll_opy_(self, source = bstack11l1_opy_ (u"ࠪࠫᾘ")):
        with self.lock:
            if not self.queue:
                self.bstack1lllllllll1l_opy_()
                return
            data = self.queue[:self.bstack1llllllllll1_opy_]
            del self.queue[:self.bstack1llllllllll1_opy_]
        self.handler(data)
        if source != bstack11l1_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᾙ"):
            self.bstack1lllllllll1l_opy_()
    def shutdown(self):
        self.bstack1llllllll1ll_opy_()
        while self.queue:
            self.bstack111111111ll_opy_(source=bstack11l1_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᾚ"))