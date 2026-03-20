# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll1111l11l_opy_ = 2
class bstack1lll1111111l_opy_:
    def __init__(self, handler, bstack1lll11111111_opy_=BATCH_SIZE, bstack1lll11111l11_opy_=bstack1lll1111l11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll11111111_opy_ = bstack1lll11111111_opy_
        self.bstack1lll11111l11_opy_ = bstack1lll11111l11_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll1l11l11l_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll11111ll1_opy_()
    def bstack1lll11111ll1_opy_(self):
        self.bstack1ll1l11l11l_opy_ = threading.Event()
        def bstack1lll111111ll_opy_():
            self.bstack1ll1l11l11l_opy_.wait(self.bstack1lll11111l11_opy_)
            if not self.bstack1ll1l11l11l_opy_.is_set():
                self.bstack1lll1111l111_opy_()
        self.timer = threading.Thread(target=bstack1lll111111ll_opy_, daemon=True)
        self.timer.start()
    def bstack1lll11111l1l_opy_(self):
        try:
            if self.bstack1ll1l11l11l_opy_ and not self.bstack1ll1l11l11l_opy_.is_set():
                self.bstack1ll1l11l11l_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠬࡡࡳࡵࡱࡳࡣࡹ࡯࡭ࡦࡴࡠࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࠩ⑕") + (str(e) or bstack11lll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡥࡲࡲࡻ࡫ࡲࡵࡧࡧࠤࡹࡵࠠࡴࡶࡵ࡭ࡳ࡭ࠢ⑖")))
        finally:
            self.timer = None
    def bstack1lll111111l1_opy_(self):
        if self.timer:
            self.bstack1lll11111l1l_opy_()
        self.bstack1lll11111ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll11111111_opy_:
                threading.Thread(target=self.bstack1lll1111l111_opy_).start()
    def bstack1lll1111l111_opy_(self, source = bstack11lll1_opy_ (u"ࠧࠨ⑗")):
        with self.lock:
            if not self.queue:
                self.bstack1lll111111l1_opy_()
                return
            data = self.queue[:self.bstack1lll11111111_opy_]
            del self.queue[:self.bstack1lll11111111_opy_]
        self.handler(data)
        if source != bstack11lll1_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪ⑘"):
            self.bstack1lll111111l1_opy_()
    def shutdown(self):
        self.bstack1lll11111l1l_opy_()
        while self.queue:
            self.bstack1lll1111l111_opy_(source=bstack11lll1_opy_ (u"ࠩࡶ࡬ࡺࡺࡤࡰࡹࡱࠫ⑙"))