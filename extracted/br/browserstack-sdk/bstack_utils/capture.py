# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import builtins
import logging
class bstack1llll111lll_opy_:
    def __init__(self, handler):
        self._11111llll11_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11111ll1lll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1111l_opy_ (u"ࠧࡪࡰࡩࡳࠬᶹ"), bstack1l1111l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᶺ"), bstack1l1111l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᶻ"), bstack1l1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᶼ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11111lll111_opy_
        self._11111lll1l1_opy_()
    def _11111lll111_opy_(self, *args, **kwargs):
        self._11111llll11_opy_(*args, **kwargs)
        message = bstack1l1111l_opy_ (u"ࠫࠥ࠭ᶽ").join(map(str, args)) + bstack1l1111l_opy_ (u"ࠬࡢ࡮ࠨᶾ")
        self._11111lll11l_opy_(bstack1l1111l_opy_ (u"࠭ࡉࡏࡈࡒࠫᶿ"), message)
    def _11111lll11l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᷀"): level, bstack1l1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᷁"): msg})
    def _11111lll1l1_opy_(self):
        for level, bstack11111ll1ll1_opy_ in self._11111ll1lll_opy_.items():
            setattr(logging, level, self._11111lll1ll_opy_(level, bstack11111ll1ll1_opy_))
    def _11111lll1ll_opy_(self, level, bstack11111ll1ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11111ll1ll1_opy_(msg, *args, **kwargs)
            self._11111lll11l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11111llll11_opy_
        for level, bstack11111ll1ll1_opy_ in self._11111ll1lll_opy_.items():
            setattr(logging, level, bstack11111ll1ll1_opy_)