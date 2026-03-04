# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll11ll111l_opy_ = 2
class bstack1lll11lll111_opy_:
    def __init__(self, handler, bstack1lll11ll1lll_opy_=BATCH_SIZE, bstack1lll11lll11l_opy_=bstack1lll11ll111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll11ll1lll_opy_ = bstack1lll11ll1lll_opy_
        self.bstack1lll11lll11l_opy_ = bstack1lll11lll11l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll11111l1_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll11ll1l1l_opy_()
    def bstack1lll11ll1l1l_opy_(self):
        self.bstack1lll11111l1_opy_ = threading.Event()
        def bstack1lll11ll1l11_opy_():
            self.bstack1lll11111l1_opy_.wait(self.bstack1lll11lll11l_opy_)
            if not self.bstack1lll11111l1_opy_.is_set():
                self.bstack1lll11ll11ll_opy_()
        self.timer = threading.Thread(target=bstack1lll11ll1l11_opy_, daemon=True)
        self.timer.start()
    def bstack1lll11ll1ll1_opy_(self):
        try:
            if self.bstack1lll11111l1_opy_ and not self.bstack1lll11111l1_opy_.is_set():
                self.bstack1lll11111l1_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1lll1l_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨ⍊") + (str(e) or bstack1lll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨ⍋")))
        finally:
            self.timer = None
    def bstack1lll11ll1111_opy_(self):
        if self.timer:
            self.bstack1lll11ll1ll1_opy_()
        self.bstack1lll11ll1l1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll11ll1lll_opy_:
                threading.Thread(target=self.bstack1lll11ll11ll_opy_).start()
    def bstack1lll11ll11ll_opy_(self, source = bstack1lll1l_opy_ (u"࠭ࠧ⍌")):
        with self.lock:
            if not self.queue:
                self.bstack1lll11ll1111_opy_()
                return
            data = self.queue[:self.bstack1lll11ll1lll_opy_]
            del self.queue[:self.bstack1lll11ll1lll_opy_]
        self.handler(data)
        if source != bstack1lll1l_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩ⍍"):
            self.bstack1lll11ll1111_opy_()
    def shutdown(self):
        self.bstack1lll11ll1ll1_opy_()
        while self.queue:
            self.bstack1lll11ll11ll_opy_(source=bstack1lll1l_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⍎"))