# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import builtins
import logging
class bstack1111l1l11l_opy_:
    def __init__(self, handler):
        self._111lll11l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111lll1l11l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1lll1l_opy_ (u"ࠧࡪࡰࡩࡳࠬ᪛"), bstack1lll1l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ᪜"), bstack1lll1l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪ᪝"), bstack1lll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ᪞")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111lll11l11_opy_
        self._111lll11lll_opy_()
    def _111lll11l11_opy_(self, *args, **kwargs):
        self._111lll11l1l_opy_(*args, **kwargs)
        message = bstack1lll1l_opy_ (u"ࠫࠥ࠭᪟").join(map(str, args)) + bstack1lll1l_opy_ (u"ࠬࡢ࡮ࠨ᪠")
        self._111lll111ll_opy_(bstack1lll1l_opy_ (u"࠭ࡉࡏࡈࡒࠫ᪡"), message)
    def _111lll111ll_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᪢"): level, bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪣"): msg})
    def _111lll11lll_opy_(self):
        for level, bstack111lll11ll1_opy_ in self._111lll1l11l_opy_.items():
            setattr(logging, level, self._111lll1l111_opy_(level, bstack111lll11ll1_opy_))
    def _111lll1l111_opy_(self, level, bstack111lll11ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111lll11ll1_opy_(msg, *args, **kwargs)
            self._111lll111ll_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111lll11l1l_opy_
        for level, bstack111lll11ll1_opy_ in self._111lll1l11l_opy_.items():
            setattr(logging, level, bstack111lll11ll1_opy_)