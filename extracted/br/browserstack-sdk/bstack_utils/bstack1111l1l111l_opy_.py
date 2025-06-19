# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1111l1l11l1_opy_ = 1000
bstack1111l1l1lll_opy_ = 2
class bstack1111l1l11ll_opy_:
    def __init__(self, handler, bstack1111l1l1l1l_opy_=bstack1111l1l11l1_opy_, bstack1111l1l1111_opy_=bstack1111l1l1lll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111l1l1l1l_opy_ = bstack1111l1l1l1l_opy_
        self.bstack1111l1l1111_opy_ = bstack1111l1l1111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack11111lll1l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1111l11llll_opy_()
    def bstack1111l11llll_opy_(self):
        self.bstack11111lll1l_opy_ = threading.Event()
        def bstack1111l1ll111_opy_():
            self.bstack11111lll1l_opy_.wait(self.bstack1111l1l1111_opy_)
            if not self.bstack11111lll1l_opy_.is_set():
                self.bstack1111l11lll1_opy_()
        self.timer = threading.Thread(target=bstack1111l1ll111_opy_, daemon=True)
        self.timer.start()
    def bstack1111l1l1ll1_opy_(self):
        try:
            if self.bstack11111lll1l_opy_ and not self.bstack11111lll1l_opy_.is_set():
                self.bstack11111lll1l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠩ࡞ࡷࡹࡵࡰࡠࡶ࡬ࡱࡪࡸ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥ࠭Ẇ") + (str(e) or bstack111lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡫ࡤࠡࡶࡲࠤࡸࡺࡲࡪࡰࡪࠦẇ")))
        finally:
            self.timer = None
    def bstack1111l1l1l11_opy_(self):
        if self.timer:
            self.bstack1111l1l1ll1_opy_()
        self.bstack1111l11llll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111l1l1l1l_opy_:
                threading.Thread(target=self.bstack1111l11lll1_opy_).start()
    def bstack1111l11lll1_opy_(self, source = bstack111lll_opy_ (u"ࠫࠬẈ")):
        with self.lock:
            if not self.queue:
                self.bstack1111l1l1l11_opy_()
                return
            data = self.queue[:self.bstack1111l1l1l1l_opy_]
            del self.queue[:self.bstack1111l1l1l1l_opy_]
        self.handler(data)
        if source != bstack111lll_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧẉ"):
            self.bstack1111l1l1l11_opy_()
    def shutdown(self):
        self.bstack1111l1l1ll1_opy_()
        while self.queue:
            self.bstack1111l11lll1_opy_(source=bstack111lll_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨẊ"))