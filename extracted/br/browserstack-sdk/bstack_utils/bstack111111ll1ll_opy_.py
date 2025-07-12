# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack111111lll11_opy_ = 1000
bstack111111l11ll_opy_ = 2
class bstack111111lll1l_opy_:
    def __init__(self, handler, bstack111111l1l1l_opy_=bstack111111lll11_opy_, bstack111111ll11l_opy_=bstack111111l11ll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111111l1l1l_opy_ = bstack111111l1l1l_opy_
        self.bstack111111ll11l_opy_ = bstack111111ll11l_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1l1l1111l11_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111111l1ll1_opy_()
    def bstack111111l1ll1_opy_(self):
        self.bstack1l1l1111l11_opy_ = threading.Event()
        def bstack111111l1lll_opy_():
            self.bstack1l1l1111l11_opy_.wait(self.bstack111111ll11l_opy_)
            if not self.bstack1l1l1111l11_opy_.is_set():
                self.bstack111111ll1l1_opy_()
        self.timer = threading.Thread(target=bstack111111l1lll_opy_, daemon=True)
        self.timer.start()
    def bstack111111ll111_opy_(self):
        try:
            if self.bstack1l1l1111l11_opy_ and not self.bstack1l1l1111l11_opy_.is_set():
                self.bstack1l1l1111l11_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠫࡠࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࡳ࡟ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࠨἔ") + (str(e) or bstack11l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡦࡦࠣࡸࡴࠦࡳࡵࡴ࡬ࡲ࡬ࠨἕ")))
        finally:
            self.timer = None
    def bstack111111l1l11_opy_(self):
        if self.timer:
            self.bstack111111ll111_opy_()
        self.bstack111111l1ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111111l1l1l_opy_:
                threading.Thread(target=self.bstack111111ll1l1_opy_).start()
    def bstack111111ll1l1_opy_(self, source = bstack11l1111_opy_ (u"࠭ࠧ἖")):
        with self.lock:
            if not self.queue:
                self.bstack111111l1l11_opy_()
                return
            data = self.queue[:self.bstack111111l1l1l_opy_]
            del self.queue[:self.bstack111111l1l1l_opy_]
        self.handler(data)
        if source != bstack11l1111_opy_ (u"ࠧࡴࡪࡸࡸࡩࡵࡷ࡯ࠩ἗"):
            self.bstack111111l1l11_opy_()
    def shutdown(self):
        self.bstack111111ll111_opy_()
        while self.queue:
            self.bstack111111ll1l1_opy_(source=bstack11l1111_opy_ (u"ࠨࡵ࡫ࡹࡹࡪ࡯ࡸࡰࠪἘ"))