# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import builtins
import logging
class bstack1llll111l1l_opy_:
    def __init__(self, handler):
        self._1111l111111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._1111l111l1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᶛ"), bstack11ll11_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᶜ"), bstack11ll11_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᶝ"), bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᶞ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._1111l11111l_opy_
        self._11111llllll_opy_()
    def _1111l11111l_opy_(self, *args, **kwargs):
        self._1111l111111_opy_(*args, **kwargs)
        message = bstack11ll11_opy_ (u"ࠩࠣࠫᶟ").join(map(str, args)) + bstack11ll11_opy_ (u"ࠪࡠࡳ࠭ᶠ")
        self._1111l1111l1_opy_(bstack11ll11_opy_ (u"ࠫࡎࡔࡆࡐࠩᶡ"), message)
    def _1111l1111l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᶢ"): level, bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᶣ"): msg})
    def _11111llllll_opy_(self):
        for level, bstack1111l1111ll_opy_ in self._1111l111l1l_opy_.items():
            setattr(logging, level, self._1111l111l11_opy_(level, bstack1111l1111ll_opy_))
    def _1111l111l11_opy_(self, level, bstack1111l1111ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack1111l1111ll_opy_(msg, *args, **kwargs)
            self._1111l1111l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._1111l111111_opy_
        for level, bstack1111l1111ll_opy_ in self._1111l111l1l_opy_.items():
            setattr(logging, level, bstack1111l1111ll_opy_)