# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import builtins
import logging
class bstack1llll11111l_opy_:
    def __init__(self, handler):
        self._11111ll1lll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11111ll11ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111ll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᷔ"), bstack111ll_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᷕ"), bstack111ll_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᷖ"), bstack111ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᷗ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11111lll111_opy_
        self._11111ll1l11_opy_()
    def _11111lll111_opy_(self, *args, **kwargs):
        self._11111ll1lll_opy_(*args, **kwargs)
        message = bstack111ll_opy_ (u"ࠪࠤࠬᷘ").join(map(str, args)) + bstack111ll_opy_ (u"ࠫࡡࡴࠧᷙ")
        self._11111ll11l1_opy_(bstack111ll_opy_ (u"ࠬࡏࡎࡇࡑࠪᷚ"), message)
    def _11111ll11l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᷛ"): level, bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᷜ"): msg})
    def _11111ll1l11_opy_(self):
        for level, bstack11111ll1ll1_opy_ in self._11111ll11ll_opy_.items():
            setattr(logging, level, self._11111ll1l1l_opy_(level, bstack11111ll1ll1_opy_))
    def _11111ll1l1l_opy_(self, level, bstack11111ll1ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11111ll1ll1_opy_(msg, *args, **kwargs)
            self._11111ll11l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11111ll1lll_opy_
        for level, bstack11111ll1ll1_opy_ in self._11111ll11ll_opy_.items():
            setattr(logging, level, bstack11111ll1ll1_opy_)