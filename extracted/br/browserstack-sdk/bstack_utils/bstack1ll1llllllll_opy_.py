# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll1111111l_opy_ = 2
class bstack1lll11111111_opy_:
    def __init__(self, handler, bstack1ll1llllll1l_opy_=BATCH_SIZE, bstack1lll111111l1_opy_=bstack1lll1111111l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1llllll1l_opy_ = bstack1ll1llllll1l_opy_
        self.bstack1lll111111l1_opy_ = bstack1lll111111l1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll1l11l11l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll11111ll1_opy_()
    def bstack1lll11111ll1_opy_(self):
        self.bstack1ll1l11l11l_opy_ = threading.Event()
        def bstack1lll11111l11_opy_():
            self.bstack1ll1l11l11l_opy_.wait(self.bstack1lll111111l1_opy_)
            if not self.bstack1ll1l11l11l_opy_.is_set():
                self.bstack1lll11111l1l_opy_()
        self.timer = threading.Thread(target=bstack1lll11111l11_opy_, daemon=True)
        self.timer.start()
    def bstack1ll1lllllll1_opy_(self):
        try:
            if self.bstack1ll1l11l11l_opy_ and not self.bstack1ll1l11l11l_opy_.is_set():
                self.bstack1ll1l11l11l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨ⑛") + (str(e) or bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨ⑜")))
        finally:
            self.timer = None
    def bstack1lll111111ll_opy_(self):
        if self.timer:
            self.bstack1ll1lllllll1_opy_()
        self.bstack1lll11111ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1llllll1l_opy_:
                threading.Thread(target=self.bstack1lll11111l1l_opy_).start()
    def bstack1lll11111l1l_opy_(self, source = bstack1ll1lll_opy_ (u"࠭ࠧ⑝")):
        with self.lock:
            if not self.queue:
                self.bstack1lll111111ll_opy_()
                return
            data = self.queue[:self.bstack1ll1llllll1l_opy_]
            del self.queue[:self.bstack1ll1llllll1l_opy_]
        self.handler(data)
        if source != bstack1ll1lll_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩ⑞"):
            self.bstack1lll111111ll_opy_()
    def shutdown(self):
        self.bstack1ll1lllllll1_opy_()
        while self.queue:
            self.bstack1lll11111l1l_opy_(source=bstack1ll1lll_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⑟"))