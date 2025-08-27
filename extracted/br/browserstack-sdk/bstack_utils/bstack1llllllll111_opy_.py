# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1lllllll1ll1_opy_ = 1000
bstack1lllllll1111_opy_ = 2
class bstack1llllll1lll1_opy_:
    def __init__(self, handler, bstack1lllllll11l1_opy_=bstack1lllllll1ll1_opy_, bstack1lllllll111l_opy_=bstack1lllllll1111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllllll11l1_opy_ = bstack1lllllll11l1_opy_
        self.bstack1lllllll111l_opy_ = bstack1lllllll111l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111l11l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lllllll11ll_opy_()
    def bstack1lllllll11ll_opy_(self):
        self.bstack111111l11l_opy_ = threading.Event()
        def bstack1lllllll1lll_opy_():
            self.bstack111111l11l_opy_.wait(self.bstack1lllllll111l_opy_)
            if not self.bstack111111l11l_opy_.is_set():
                self.bstack1llllll1llll_opy_()
        self.timer = threading.Thread(target=bstack1lllllll1lll_opy_, daemon=True)
        self.timer.start()
    def bstack1lllllll1l11_opy_(self):
        try:
            if self.bstack111111l11l_opy_ and not self.bstack111111l11l_opy_.is_set():
                self.bstack111111l11l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠩ࡞ࡷࡹࡵࡰࡠࡶ࡬ࡱࡪࡸ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥ࠭ᾐ") + (str(e) or bstack1111lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡫ࡤࠡࡶࡲࠤࡸࡺࡲࡪࡰࡪࠦᾑ")))
        finally:
            self.timer = None
    def bstack1lllllll1l1l_opy_(self):
        if self.timer:
            self.bstack1lllllll1l11_opy_()
        self.bstack1lllllll11ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllllll11l1_opy_:
                threading.Thread(target=self.bstack1llllll1llll_opy_).start()
    def bstack1llllll1llll_opy_(self, source = bstack1111lll_opy_ (u"ࠫࠬᾒ")):
        with self.lock:
            if not self.queue:
                self.bstack1lllllll1l1l_opy_()
                return
            data = self.queue[:self.bstack1lllllll11l1_opy_]
            del self.queue[:self.bstack1lllllll11l1_opy_]
        self.handler(data)
        if source != bstack1111lll_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧᾓ"):
            self.bstack1lllllll1l1l_opy_()
    def shutdown(self):
        self.bstack1lllllll1l11_opy_()
        while self.queue:
            self.bstack1llllll1llll_opy_(source=bstack1111lll_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨᾔ"))