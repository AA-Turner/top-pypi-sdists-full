# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import builtins
import logging
class bstack1llll11l11l_opy_:
    def __init__(self, handler):
        self._11111llllll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11111lll1ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᶞ"), bstack1ll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨᶟ"), bstack1ll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᶠ"), bstack1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᶡ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11111lll1l1_opy_
        self._11111llll11_opy_()
    def _11111lll1l1_opy_(self, *args, **kwargs):
        self._11111llllll_opy_(*args, **kwargs)
        message = bstack1ll_opy_ (u"ࠬࠦࠧᶢ").join(map(str, args)) + bstack1ll_opy_ (u"࠭࡜࡯ࠩᶣ")
        self._11111llll1l_opy_(bstack1ll_opy_ (u"ࠧࡊࡐࡉࡓࠬᶤ"), message)
    def _11111llll1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᶥ"): level, bstack1ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᶦ"): msg})
    def _11111llll11_opy_(self):
        for level, bstack11111lllll1_opy_ in self._11111lll1ll_opy_.items():
            setattr(logging, level, self._1111l111111_opy_(level, bstack11111lllll1_opy_))
    def _1111l111111_opy_(self, level, bstack11111lllll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11111lllll1_opy_(msg, *args, **kwargs)
            self._11111llll1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11111llllll_opy_
        for level, bstack11111lllll1_opy_ in self._11111lll1ll_opy_.items():
            setattr(logging, level, bstack11111lllll1_opy_)