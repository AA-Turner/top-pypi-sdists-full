# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack111111l1l11_opy_ = 1000
bstack111111ll111_opy_ = 2
class bstack111111ll11l_opy_:
    def __init__(self, handler, bstack111111l11ll_opy_=bstack111111l1l11_opy_, bstack111111l1ll1_opy_=bstack111111ll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111111l11ll_opy_ = bstack111111l11ll_opy_
        self.bstack111111l1ll1_opy_ = bstack111111l1ll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1111111lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111111l1lll_opy_()
    def bstack111111l1lll_opy_(self):
        self.bstack1111111lll_opy_ = threading.Event()
        def bstack111111l1l1l_opy_():
            self.bstack1111111lll_opy_.wait(self.bstack111111l1ll1_opy_)
            if not self.bstack1111111lll_opy_.is_set():
                self.bstack111111ll1ll_opy_()
        self.timer = threading.Thread(target=bstack111111l1l1l_opy_, daemon=True)
        self.timer.start()
    def bstack111111lll11_opy_(self):
        try:
            if self.bstack1111111lll_opy_ and not self.bstack1111111lll_opy_.is_set():
                self.bstack1111111lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠩ࡞ࡷࡹࡵࡰࡠࡶ࡬ࡱࡪࡸ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥ࠭ἒ") + (str(e) or bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡫ࡤࠡࡶࡲࠤࡸࡺࡲࡪࡰࡪࠦἓ")))
        finally:
            self.timer = None
    def bstack111111ll1l1_opy_(self):
        if self.timer:
            self.bstack111111lll11_opy_()
        self.bstack111111l1lll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111111l11ll_opy_:
                threading.Thread(target=self.bstack111111ll1ll_opy_).start()
    def bstack111111ll1ll_opy_(self, source = bstack1l1_opy_ (u"ࠫࠬἔ")):
        with self.lock:
            if not self.queue:
                self.bstack111111ll1l1_opy_()
                return
            data = self.queue[:self.bstack111111l11ll_opy_]
            del self.queue[:self.bstack111111l11ll_opy_]
        self.handler(data)
        if source != bstack1l1_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧἕ"):
            self.bstack111111ll1l1_opy_()
    def shutdown(self):
        self.bstack111111lll11_opy_()
        while self.queue:
            self.bstack111111ll1ll_opy_(source=bstack1l1_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨ἖"))