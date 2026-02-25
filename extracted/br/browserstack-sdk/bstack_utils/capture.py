# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import builtins
import logging
class bstack1111l1lll1_opy_:
    def __init__(self, handler):
        self._11l11111l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l1111l111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᥴ"), bstack11l1l11_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭᥵"), bstack11l1l11_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩ᥶"), bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᥷")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l11111ll1_opy_
        self._11l1111l11l_opy_()
    def _11l11111ll1_opy_(self, *args, **kwargs):
        self._11l11111l1l_opy_(*args, **kwargs)
        message = bstack11l1l11_opy_ (u"ࠪࠤࠬ᥸").join(map(str, args)) + bstack11l1l11_opy_ (u"ࠫࡡࡴࠧ᥹")
        self._11l11111lll_opy_(bstack11l1l11_opy_ (u"ࠬࡏࡎࡇࡑࠪ᥺"), message)
    def _11l11111lll_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ᥻"): level, bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᥼"): msg})
    def _11l1111l11l_opy_(self):
        for level, bstack11l111111ll_opy_ in self._11l1111l111_opy_.items():
            setattr(logging, level, self._11l11111l11_opy_(level, bstack11l111111ll_opy_))
    def _11l11111l11_opy_(self, level, bstack11l111111ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l111111ll_opy_(msg, *args, **kwargs)
            self._11l11111lll_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l11111l1l_opy_
        for level, bstack11l111111ll_opy_ in self._11l1111l111_opy_.items():
            setattr(logging, level, bstack11l111111ll_opy_)