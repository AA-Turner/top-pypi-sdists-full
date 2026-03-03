# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll1l1l111l_opy_ = 2
class bstack1lll1l11lll1_opy_:
    def __init__(self, handler, bstack1lll1l1l1l1l_opy_=BATCH_SIZE, bstack1lll1l1l1ll1_opy_=bstack1lll1l1l111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1l1l1l1l_opy_ = bstack1lll1l1l1l1l_opy_
        self.bstack1lll1l1l1ll1_opy_ = bstack1lll1l1l1ll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll11lllll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll1l11llll_opy_()
    def bstack1lll1l11llll_opy_(self):
        self.bstack1lll11lllll_opy_ = threading.Event()
        def bstack1lll1l1l11l1_opy_():
            self.bstack1lll11lllll_opy_.wait(self.bstack1lll1l1l1ll1_opy_)
            if not self.bstack1lll11lllll_opy_.is_set():
                self.bstack1lll1l1l1111_opy_()
        self.timer = threading.Thread(target=bstack1lll1l1l11l1_opy_, daemon=True)
        self.timer.start()
    def bstack1lll1l1l1l11_opy_(self):
        try:
            if self.bstack1lll11lllll_opy_ and not self.bstack1lll11lllll_opy_.is_set():
                self.bstack1lll11lllll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫ∠") + (str(e) or bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤ∡")))
        finally:
            self.timer = None
    def bstack1lll1l1l1lll_opy_(self):
        if self.timer:
            self.bstack1lll1l1l1l11_opy_()
        self.bstack1lll1l11llll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1l1l1l1l_opy_:
                threading.Thread(target=self.bstack1lll1l1l1111_opy_).start()
    def bstack1lll1l1l1111_opy_(self, source = bstack11ll111_opy_ (u"ࠩࠪ∢")):
        with self.lock:
            if not self.queue:
                self.bstack1lll1l1l1lll_opy_()
                return
            data = self.queue[:self.bstack1lll1l1l1l1l_opy_]
            del self.queue[:self.bstack1lll1l1l1l1l_opy_]
        self.handler(data)
        if source != bstack11ll111_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ∣"):
            self.bstack1lll1l1l1lll_opy_()
    def shutdown(self):
        self.bstack1lll1l1l1l11_opy_()
        while self.queue:
            self.bstack1lll1l1l1111_opy_(source=bstack11ll111_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭∤"))