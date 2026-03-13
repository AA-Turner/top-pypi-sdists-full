# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import threading
import logging
logger = logging.getLogger(__name__)
BATCH_SIZE = 1000
bstack1lll111ll11l_opy_ = 2
class bstack1lll111llll1_opy_:
    def __init__(self, handler, bstack1lll11l1111l_opy_=BATCH_SIZE, bstack1lll11l11111_opy_=bstack1lll111ll11l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll11l1111l_opy_ = bstack1lll11l1111l_opy_
        self.bstack1lll11l11111_opy_ = bstack1lll11l11111_opy_
        self.lock = threading.Lock()
        self.timer = None
        self.bstack1ll1ll1l111_opy_ = None
    def start(self):
        if not (self.timer and self.timer.is_alive()):
            self.bstack1lll111ll1ll_opy_()
    def bstack1lll111ll1ll_opy_(self):
        self.bstack1ll1ll1l111_opy_ = threading.Event()
        def bstack1lll111ll1l1_opy_():
            self.bstack1ll1ll1l111_opy_.wait(self.bstack1lll11l11111_opy_)
            if not self.bstack1ll1ll1l111_opy_.is_set():
                self.bstack1lll111lllll_opy_()
        self.timer = threading.Thread(target=bstack1lll111ll1l1_opy_, daemon=True)
        self.timer.start()
    def bstack1lll111lll11_opy_(self):
        try:
            if self.bstack1ll1ll1l111_opy_ and not self.bstack1ll1ll1l111_opy_.is_set():
                self.bstack1ll1ll1l111_opy_.set()
            if self.timer and self.timer.is_alive() and self.timer != threading.current_thread():
                self.timer.join()
        except Exception as e:
            logger.debug(bstack1111l_opy_ (u"ࠧ࡜ࡵࡷࡳࡵࡥࡴࡪ࡯ࡨࡶࡢࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࠫ␊") + (str(e) or bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡧࡴࡴࡶࡦࡴࡷࡩࡩࠦࡴࡰࠢࡶࡸࡷ࡯࡮ࡨࠤ␋")))
        finally:
            self.timer = None
    def bstack1lll111lll1l_opy_(self):
        if self.timer:
            self.bstack1lll111lll11_opy_()
        self.bstack1lll111ll1ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll11l1111l_opy_:
                threading.Thread(target=self.bstack1lll111lllll_opy_).start()
    def bstack1lll111lllll_opy_(self, source = bstack1111l_opy_ (u"ࠩࠪ␌")):
        with self.lock:
            if not self.queue:
                self.bstack1lll111lll1l_opy_()
                return
            data = self.queue[:self.bstack1lll11l1111l_opy_]
            del self.queue[:self.bstack1lll11l1111l_opy_]
        self.handler(data)
        if source != bstack1111l_opy_ (u"ࠪࡷ࡭ࡻࡴࡥࡱࡺࡲࠬ␍"):
            self.bstack1lll111lll1l_opy_()
    def shutdown(self):
        self.bstack1lll111lll11_opy_()
        while self.queue:
            self.bstack1lll111lllll_opy_(source=bstack1111l_opy_ (u"ࠫࡸ࡮ࡵࡵࡦࡲࡻࡳ࠭␎"))