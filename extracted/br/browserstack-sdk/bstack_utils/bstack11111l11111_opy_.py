# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack11111l1l111_opy_ = 1000
bstack11111l1111l_opy_ = 2
class bstack111111lllll_opy_:
    def __init__(self, handler, bstack11111l11lll_opy_=bstack11111l1l111_opy_, bstack111111llll1_opy_=bstack11111l1111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11111l11lll_opy_ = bstack11111l11lll_opy_
        self.bstack111111llll1_opy_ = bstack111111llll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111ll11_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack11111l11ll1_opy_()
    def bstack11111l11ll1_opy_(self):
        self.bstack111111ll11_opy_ = threading.Event()
        def bstack11111l11l11_opy_():
            self.bstack111111ll11_opy_.wait(self.bstack111111llll1_opy_)
            if not self.bstack111111ll11_opy_.is_set():
                self.bstack11111l111ll_opy_()
        self.timer = threading.Thread(target=bstack11111l11l11_opy_, daemon=True)
        self.timer.start()
    def bstack11111l11l1l_opy_(self):
        try:
            if self.bstack111111ll11_opy_ and not self.bstack111111ll11_opy_.is_set():
                self.bstack111111ll11_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨẲ") + (str(e) or bstack1l1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨẳ")))
        finally:
            self.timer = None
    def bstack11111l111l1_opy_(self):
        if self.timer:
            self.bstack11111l11l1l_opy_()
        self.bstack11111l11ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11111l11lll_opy_:
                threading.Thread(target=self.bstack11111l111ll_opy_).start()
    def bstack11111l111ll_opy_(self, source = bstack1l1l1l1_opy_ (u"࠭ࠧẴ")):
        with self.lock:
            if not self.queue:
                self.bstack11111l111l1_opy_()
                return
            data = self.queue[:self.bstack11111l11lll_opy_]
            del self.queue[:self.bstack11111l11lll_opy_]
        self.handler(data)
        if source != bstack1l1l1l1_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩẵ"):
            self.bstack11111l111l1_opy_()
    def shutdown(self):
        self.bstack11111l11l1l_opy_()
        while self.queue:
            self.bstack11111l111ll_opy_(source=bstack1l1l1l1_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪẶ"))