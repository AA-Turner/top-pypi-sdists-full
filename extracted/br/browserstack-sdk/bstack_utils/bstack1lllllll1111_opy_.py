# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1llllll1l11l_opy_ = 1000
bstack1llllll1ll1l_opy_ = 2
class bstack1lllllll11l1_opy_:
    def __init__(self, handler, bstack1llllll1l1ll_opy_=bstack1llllll1l11l_opy_, bstack1llllll1l1l1_opy_=bstack1llllll1ll1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1llllll1l1ll_opy_ = bstack1llllll1l1ll_opy_
        self.bstack1llllll1l1l1_opy_ = bstack1llllll1l1l1_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack11111111ll_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lllllll111l_opy_()
    def bstack1lllllll111l_opy_(self):
        self.bstack11111111ll_opy_ = threading.Event()
        def bstack1lllllll11ll_opy_():
            self.bstack11111111ll_opy_.wait(self.bstack1llllll1l1l1_opy_)
            if not self.bstack11111111ll_opy_.is_set():
                self.bstack1llllll1llll_opy_()
        self.timer = threading.Thread(target=bstack1lllllll11ll_opy_, daemon=True)
        self.timer.start()
    def bstack1llllll1lll1_opy_(self):
        try:
            if self.bstack11111111ll_opy_ and not self.bstack11111111ll_opy_.is_set():
                self.bstack11111111ll_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1111l1l_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫᾕ") + (str(e) or bstack1111l1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤᾖ")))
        finally:
            self.timer = None
    def bstack1llllll1ll11_opy_(self):
        if self.timer:
            self.bstack1llllll1lll1_opy_()
        self.bstack1lllllll111l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1llllll1l1ll_opy_:
                threading.Thread(target=self.bstack1llllll1llll_opy_).start()
    def bstack1llllll1llll_opy_(self, source = bstack1111l1l_opy_ (u"ࠩࠪᾗ")):
        with self.lock:
            if not self.queue:
                self.bstack1llllll1ll11_opy_()
                return
            data = self.queue[:self.bstack1llllll1l1ll_opy_]
            del self.queue[:self.bstack1llllll1l1ll_opy_]
        self.handler(data)
        if source != bstack1111l1l_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬᾘ"):
            self.bstack1llllll1ll11_opy_()
    def shutdown(self):
        self.bstack1llllll1lll1_opy_()
        while self.queue:
            self.bstack1llllll1llll_opy_(source=bstack1111l1l_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᾙ"))