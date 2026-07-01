# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import builtins
import logging
class bstack111ll1l1_opy_:
    def __init__(self, handler):
        self._111111ll111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111111l1lll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ₀"), bstack1l1llll_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ₁"), bstack1l1llll_opy_ (u"࠭ࡷࡢࡴࡱ࡭ࡳ࡭ࠧ₂"), bstack1l1llll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭₃")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111111ll1ll_opy_
        self._111111ll1l1_opy_()
    def _111111ll1ll_opy_(self, *args, **kwargs):
        self._111111ll111_opy_(*args, **kwargs)
        message = bstack1l1llll_opy_ (u"ࠨࠢࠪ₄").join(map(str, args)) + bstack1l1llll_opy_ (u"ࠩ࡟ࡲࠬ₅")
        self._111111lll11_opy_(bstack1l1llll_opy_ (u"ࠪࡍࡓࡌࡏࠨ₆"), message)
    def _111111lll11_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1llll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ₇"): level, bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭₈"): msg})
    def _111111ll1l1_opy_(self):
        for level, bstack111111lll1l_opy_ in self._111111l1lll_opy_.items():
            setattr(logging, level, self._111111ll11l_opy_(level, bstack111111lll1l_opy_))
    def _111111ll11l_opy_(self, level, bstack111111lll1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111111lll1l_opy_(msg, *args, **kwargs)
            self._111111lll11_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111111ll111_opy_
        for level, bstack111111lll1l_opy_ in self._111111l1lll_opy_.items():
            setattr(logging, level, bstack111111lll1l_opy_)