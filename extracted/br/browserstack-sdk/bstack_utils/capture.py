# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import builtins
import logging
class bstack1111ll1l1l_opy_:
    def __init__(self, handler):
        self._11l11l11lll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l11l1ll11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11lllll_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᣀ"), bstack11lllll_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨᣁ"), bstack11lllll_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᣂ"), bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᣃ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l11l1l1ll_opy_
        self._11l11l1l1l1_opy_()
    def _11l11l1l1ll_opy_(self, *args, **kwargs):
        self._11l11l11lll_opy_(*args, **kwargs)
        message = bstack11lllll_opy_ (u"ࠬࠦࠧᣄ").join(map(str, args)) + bstack11lllll_opy_ (u"࠭࡜࡯ࠩᣅ")
        self._11l11l1l111_opy_(bstack11lllll_opy_ (u"ࠧࡊࡐࡉࡓࠬᣆ"), message)
    def _11l11l1l111_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᣇ"): level, bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᣈ"): msg})
    def _11l11l1l1l1_opy_(self):
        for level, bstack11l11l11ll1_opy_ in self._11l11l1ll11_opy_.items():
            setattr(logging, level, self._11l11l1l11l_opy_(level, bstack11l11l11ll1_opy_))
    def _11l11l1l11l_opy_(self, level, bstack11l11l11ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l11l11ll1_opy_(msg, *args, **kwargs)
            self._11l11l1l111_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l11l11lll_opy_
        for level, bstack11l11l11ll1_opy_ in self._11l11l1ll11_opy_.items():
            setattr(logging, level, bstack11l11l11ll1_opy_)