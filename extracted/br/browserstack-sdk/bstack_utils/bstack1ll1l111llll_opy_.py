# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1ll1l11l1l11_opy_ = 2
class bstack1ll1l11l1111_opy_:
    def __init__(self, handler, bstack1ll1l111lll1_opy_=BATCH_SIZE, bstack1ll1l111l1ll_opy_=bstack1ll1l11l1l11_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1ll1l111lll1_opy_ = bstack1ll1l111lll1_opy_
        self.bstack1ll1l111l1ll_opy_ = bstack1ll1l111l1ll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1l1l11l1lll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1ll1l111ll11_opy_()
    def bstack1ll1l111ll11_opy_(self):
        self.bstack1l1l11l1lll_opy_ = threading.Event()
        def bstack1ll1l11l11l1_opy_():
            self.bstack1l1l11l1lll_opy_.wait(self.bstack1ll1l111l1ll_opy_)
            if not self.bstack1l1l11l1lll_opy_.is_set():
                self.bstack1ll1l11l11ll_opy_()
        self.timer = threading.Thread(target=bstack1ll1l11l11l1_opy_, daemon=True)
        self.timer.start()
    def bstack1ll1l111ll1l_opy_(self):
        try:
            if self.bstack1l1l11l1lll_opy_ and not self.bstack1l1l11l1lll_opy_.is_set():
                self.bstack1l1l11l1lll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"࡛࠭ࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࡵࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࠪ♣") + (str(e) or bstack111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡦࡳࡳࡼࡥࡳࡶࡨࡨࠥࡺ࡯ࠡࡵࡷࡶ࡮ࡴࡧࠣ♤")))
        finally:
            self.timer = None
    def bstack1ll1l11l111l_opy_(self):
        if self.timer:
            self.bstack1ll1l111ll1l_opy_()
        self.bstack1ll1l111ll11_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1ll1l111lll1_opy_:
                threading.Thread(target=self.bstack1ll1l11l11ll_opy_).start()
    def bstack1ll1l11l11ll_opy_(self, source = bstack111l_opy_ (u"ࠨࠩ♥")):
        with self.lock:
            if not self.queue:
                self.bstack1ll1l11l111l_opy_()
                return
            data = self.queue[:self.bstack1ll1l111lll1_opy_]
            del self.queue[:self.bstack1ll1l111lll1_opy_]
        self.handler(data)
        if source != bstack111l_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ♦"):
            self.bstack1ll1l11l111l_opy_()
    def shutdown(self):
        self.bstack1ll1l111ll1l_opy_()
        while self.queue:
            self.bstack1ll1l11l11ll_opy_(source=bstack111l_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ♧"))