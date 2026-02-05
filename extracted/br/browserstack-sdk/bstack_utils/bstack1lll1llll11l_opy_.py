# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1lll1lllllll_opy_ = 1000
bstack1lll1lll1lll_opy_ = 2
class bstack1lll1lllll11_opy_:
    def __init__(self, handler, bstack1lll1lllll1l_opy_=bstack1lll1lllllll_opy_, bstack1lll1llll1l1_opy_=bstack1lll1lll1lll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll1lllll1l_opy_ = bstack1lll1lllll1l_opy_
        self.bstack1lll1llll1l1_opy_ = bstack1lll1llll1l1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1lll1llllll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll1llll1ll_opy_()
    def bstack1lll1llll1ll_opy_(self):
        self.bstack1lll1llllll_opy_ = threading.Event()
        def bstack1llll1111111_opy_():
            self.bstack1lll1llllll_opy_.wait(self.bstack1lll1llll1l1_opy_)
            if not self.bstack1lll1llllll_opy_.is_set():
                self.bstack1lll1llll111_opy_()
        self.timer = threading.Thread(target=bstack1llll1111111_opy_, daemon=True)
        self.timer.start()
    def bstack1llll111111l_opy_(self):
        try:
            if self.bstack1lll1llllll_opy_ and not self.bstack1lll1llllll_opy_.is_set():
                self.bstack1lll1llllll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡝ࡶࡸࡴࡶ࡟ࡵ࡫ࡰࡩࡷࡣࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࠬℬ") + (str(e) or bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡨࡵ࡮ࡷࡧࡵࡸࡪࡪࠠࡵࡱࠣࡷࡹࡸࡩ࡯ࡩࠥℭ")))
        finally:
            self.timer = None
    def bstack1lll1llllll1_opy_(self):
        if self.timer:
            self.bstack1llll111111l_opy_()
        self.bstack1lll1llll1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll1lllll1l_opy_:
                threading.Thread(target=self.bstack1lll1llll111_opy_).start()
    def bstack1lll1llll111_opy_(self, source = bstack11l1ll1_opy_ (u"ࠪࠫ℮")):
        with self.lock:
            if not self.queue:
                self.bstack1lll1llllll1_opy_()
                return
            data = self.queue[:self.bstack1lll1lllll1l_opy_]
            del self.queue[:self.bstack1lll1lllll1l_opy_]
        self.handler(data)
        if source != bstack11l1ll1_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ℯ"):
            self.bstack1lll1llllll1_opy_()
    def shutdown(self):
        self.bstack1llll111111l_opy_()
        while self.queue:
            self.bstack1lll1llll111_opy_(source=bstack11l1ll1_opy_ (u"ࠬࡹࡨࡶࡶࡧࡳࡼࡴࠧℰ"))