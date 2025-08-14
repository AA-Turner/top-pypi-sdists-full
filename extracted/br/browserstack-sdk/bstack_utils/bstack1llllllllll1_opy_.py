# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
bstack1lllllllll1l_opy_ = 1000
bstack1llllllll11l_opy_ = 2
class bstack1111111111l_opy_:
    def __init__(self, handler, bstack1lllllll1lll_opy_=bstack1lllllllll1l_opy_, bstack11111111111_opy_=bstack1llllllll11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllllll1lll_opy_ = bstack1lllllll1lll_opy_
        self.bstack11111111111_opy_ = bstack11111111111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack111111l111_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1llllllll1ll_opy_()
    def bstack1llllllll1ll_opy_(self):
        self.bstack111111l111_opy_ = threading.Event()
        def bstack1lllllllllll_opy_():
            self.bstack111111l111_opy_.wait(self.bstack11111111111_opy_)
            if not self.bstack111111l111_opy_.is_set():
                self.bstack1llllllll111_opy_()
        self.timer = threading.Thread(target=bstack1lllllllllll_opy_, daemon=True)
        self.timer.start()
    def bstack1lllllllll11_opy_(self):
        try:
            if self.bstack111111l111_opy_ and not self.bstack111111l111_opy_.is_set():
                self.bstack111111l111_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫᾣ") + (str(e) or bstack1l1l1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤᾤ")))
        finally:
            self.timer = None
    def bstack1llllllll1l1_opy_(self):
        if self.timer:
            self.bstack1lllllllll11_opy_()
        self.bstack1llllllll1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllllll1lll_opy_:
                threading.Thread(target=self.bstack1llllllll111_opy_).start()
    def bstack1llllllll111_opy_(self, source = bstack1l1l1ll_opy_ (u"ࠩࠪᾥ")):
        with self.lock:
            if not self.queue:
                self.bstack1llllllll1l1_opy_()
                return
            data = self.queue[:self.bstack1lllllll1lll_opy_]
            del self.queue[:self.bstack1lllllll1lll_opy_]
        self.handler(data)
        if source != bstack1l1l1ll_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬᾦ"):
            self.bstack1llllllll1l1_opy_()
    def shutdown(self):
        self.bstack1lllllllll11_opy_()
        while self.queue:
            self.bstack1llllllll111_opy_(source=bstack1l1l1ll_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭ᾧ"))