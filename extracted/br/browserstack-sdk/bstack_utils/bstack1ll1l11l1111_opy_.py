# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1ll1l111l1ll_opy_ = 2
class bstack1ll1l111ll1l_opy_:
    def __init__(self, handler, bstack1ll1l111llll_opy_=BATCH_SIZE, bstack1ll1l111lll1_opy_=bstack1ll1l111l1ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1l111llll_opy_ = bstack1ll1l111llll_opy_
        self.bstack1ll1l111lll1_opy_ = bstack1ll1l111lll1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1l1lll11lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll1l11l111l_opy_()
    def bstack1ll1l11l111l_opy_(self):
        self.bstack1l1lll11lll_opy_ = threading.Event()
        def bstack1ll1l111l1l1_opy_():
            self.bstack1l1lll11lll_opy_.wait(self.bstack1ll1l111lll1_opy_)
            if not self.bstack1l1lll11lll_opy_.is_set():
                self.bstack1ll1l11l11ll_opy_()
        self.timer = threading.Thread(target=bstack1ll1l111l1l1_opy_, daemon=True)
        self.timer.start()
    def bstack1ll1l11l11l1_opy_(self):
        try:
            if self.bstack1l1lll11lll_opy_ and not self.bstack1l1lll11lll_opy_.is_set():
                self.bstack1l1lll11lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫ♤") + (str(e) or bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤ♥")))
        finally:
            self.timer = None
    def bstack1ll1l111ll11_opy_(self):
        if self.timer:
            self.bstack1ll1l11l11l1_opy_()
        self.bstack1ll1l11l111l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1l111llll_opy_:
                threading.Thread(target=self.bstack1ll1l11l11ll_opy_).start()
    def bstack1ll1l11l11ll_opy_(self, source = bstack11ll11_opy_ (u"ࠩࠪ♦")):
        with self.lock:
            if not self.queue:
                self.bstack1ll1l111ll11_opy_()
                return
            data = self.queue[:self.bstack1ll1l111llll_opy_]
            del self.queue[:self.bstack1ll1l111llll_opy_]
        self.handler(data)
        if source != bstack11ll11_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ♧"):
            self.bstack1ll1l111ll11_opy_()
    def shutdown(self):
        self.bstack1ll1l11l11l1_opy_()
        while self.queue:
            self.bstack1ll1l11l11ll_opy_(source=bstack11ll11_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭♨"))