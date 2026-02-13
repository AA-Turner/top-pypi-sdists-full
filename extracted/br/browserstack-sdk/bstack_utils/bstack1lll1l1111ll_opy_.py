# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll1l111l1l_opy_ = 2
class bstack1lll1l111lll_opy_:
    def __init__(self, handler, bstack1lll1l111ll1_opy_=BATCH_SIZE, bstack1lll11llllll_opy_=bstack1lll1l111l1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1l111ll1_opy_ = bstack1lll1l111ll1_opy_
        self.bstack1lll11llllll_opy_ = bstack1lll11llllll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll111llll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll1l1111l1_opy_()
    def bstack1lll1l1111l1_opy_(self):
        self.bstack1lll111llll_opy_ = threading.Event()
        def bstack1lll1l11111l_opy_():
            self.bstack1lll111llll_opy_.wait(self.bstack1lll11llllll_opy_)
            if not self.bstack1lll111llll_opy_.is_set():
                self.bstack1lll11lllll1_opy_()
        self.timer = threading.Thread(target=bstack1lll1l11111l_opy_, daemon=True)
        self.timer.start()
    def bstack1lll1l111l11_opy_(self):
        try:
            if self.bstack1lll111llll_opy_ and not self.bstack1lll111llll_opy_.is_set():
                self.bstack1lll111llll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l11_opy_ (u"࡛࠭ࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࡵࡡࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࠪ∘") + (str(e) or bstack11l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡦࡳࡳࡼࡥࡳࡶࡨࡨࠥࡺ࡯ࠡࡵࡷࡶ࡮ࡴࡧࠣ∙")))
        finally:
            self.timer = None
    def bstack1lll1l111111_opy_(self):
        if self.timer:
            self.bstack1lll1l111l11_opy_()
        self.bstack1lll1l1111l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1l111ll1_opy_:
                threading.Thread(target=self.bstack1lll11lllll1_opy_).start()
    def bstack1lll11lllll1_opy_(self, source = bstack11l11_opy_ (u"ࠨࠩ√")):
        with self.lock:
            if not self.queue:
                self.bstack1lll1l111111_opy_()
                return
            data = self.queue[:self.bstack1lll1l111ll1_opy_]
            del self.queue[:self.bstack1lll1l111ll1_opy_]
        self.handler(data)
        if source != bstack11l11_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ∛"):
            self.bstack1lll1l111111_opy_()
    def shutdown(self):
        self.bstack1lll1l111l11_opy_()
        while self.queue:
            self.bstack1lll11lllll1_opy_(source=bstack11l11_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ∜"))