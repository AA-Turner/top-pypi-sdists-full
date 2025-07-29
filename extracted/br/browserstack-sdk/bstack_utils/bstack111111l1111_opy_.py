# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack111111ll11l_opy_ = 1000
bstack111111ll111_opy_ = 2
class bstack111111l1l1l_opy_:
    def __init__(self, handler, bstack111111l11ll_opy_=bstack111111ll11l_opy_, bstack111111l1lll_opy_=bstack111111ll111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack111111l11ll_opy_ = bstack111111l11ll_opy_
        self.bstack111111l1lll_opy_ = bstack111111l1lll_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111l1ll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack111111l111l_opy_()
    def bstack111111l111l_opy_(self):
        self.bstack111111l1ll_opy_ = threading.Event()
        def bstack111111l1l11_opy_():
            self.bstack111111l1ll_opy_.wait(self.bstack111111l1lll_opy_)
            if not self.bstack111111l1ll_opy_.is_set():
                self.bstack111111l11l1_opy_()
        self.timer = threading.Thread(target=bstack111111l1l11_opy_, daemon=True)
        self.timer.start()
    def bstack111111ll1l1_opy_(self):
        try:
            if self.bstack111111l1ll_opy_ and not self.bstack111111l1ll_opy_.is_set():
                self.bstack111111l1ll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠩ࡞ࡷࡹࡵࡰࡠࡶ࡬ࡱࡪࡸ࡝ࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥ࠭Ἑ") + (str(e) or bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡩ࡯࡯ࡸࡨࡶࡹ࡫ࡤࠡࡶࡲࠤࡸࡺࡲࡪࡰࡪࠦἚ")))
        finally:
            self.timer = None
    def bstack111111l1ll1_opy_(self):
        if self.timer:
            self.bstack111111ll1l1_opy_()
        self.bstack111111l111l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack111111l11ll_opy_:
                threading.Thread(target=self.bstack111111l11l1_opy_).start()
    def bstack111111l11l1_opy_(self, source = bstackl_opy_ (u"ࠫࠬἛ")):
        with self.lock:
            if not self.queue:
                self.bstack111111l1ll1_opy_()
                return
            data = self.queue[:self.bstack111111l11ll_opy_]
            del self.queue[:self.bstack111111l11ll_opy_]
        self.handler(data)
        if source != bstackl_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧἜ"):
            self.bstack111111l1ll1_opy_()
    def shutdown(self):
        self.bstack111111ll1l1_opy_()
        while self.queue:
            self.bstack111111l11l1_opy_(source=bstackl_opy_ (u"࠭ࡳࡩࡷࡷࡨࡴࡽ࡮ࠨἝ"))