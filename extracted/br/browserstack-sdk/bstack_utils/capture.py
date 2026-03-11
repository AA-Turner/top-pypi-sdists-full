# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import builtins
import logging
class bstack111111ll1l_opy_:
    def __init__(self, handler):
        self._1ll1lll1lll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1ll1lll1l1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll111_opy_ (u"ࠧࡪࡰࡩࡳࠬ≦"), bstack1ll111_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧ≧"), bstack1ll111_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪ≨"), bstack1ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ≩")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1ll1lll1l111_opy_
        self._1ll1lll1l1l1_opy_()
    def _1ll1lll1l111_opy_(self, *args, **kwargs):
        self._1ll1lll1lll1_opy_(*args, **kwargs)
        message = bstack1ll111_opy_ (u"ࠫࠥ࠭≪").join(map(str, args)) + bstack1ll111_opy_ (u"ࠬࡢ࡮ࠨ≫")
        self._1ll1lll1ll11_opy_(bstack1ll111_opy_ (u"࠭ࡉࡏࡈࡒࠫ≬"), message)
    def _1ll1lll1ll11_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭≭"): level, bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ≮"): msg})
    def _1ll1lll1l1l1_opy_(self):
        for level, bstack1ll1lll1ll1l_opy_ in self._1ll1lll1l1ll_opy_.items():
            setattr(logging, level, self._1ll1lll1l11l_opy_(level, bstack1ll1lll1ll1l_opy_))
    def _1ll1lll1l11l_opy_(self, level, bstack1ll1lll1ll1l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1ll1lll1ll1l_opy_(msg, *args, **kwargs)
            self._1ll1lll1ll11_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1ll1lll1lll1_opy_
        for level, bstack1ll1lll1ll1l_opy_ in self._1ll1lll1l1ll_opy_.items():
            setattr(logging, level, bstack1ll1lll1ll1l_opy_)