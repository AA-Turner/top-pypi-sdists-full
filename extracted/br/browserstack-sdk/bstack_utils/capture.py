# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import builtins
import logging
class bstack1llll11llll_opy_:
    def __init__(self, handler):
        self._11111llll11_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11111lll111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111ll11_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᶷ"), bstack111ll11_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᶸ"), bstack111ll11_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᶹ"), bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᶺ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11111lll1ll_opy_
        self._11111lllll1_opy_()
    def _11111lll1ll_opy_(self, *args, **kwargs):
        self._11111llll11_opy_(*args, **kwargs)
        message = bstack111ll11_opy_ (u"ࠩࠣࠫᶻ").join(map(str, args)) + bstack111ll11_opy_ (u"ࠪࡠࡳ࠭ᶼ")
        self._11111llll1l_opy_(bstack111ll11_opy_ (u"ࠫࡎࡔࡆࡐࠩᶽ"), message)
    def _11111llll1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᶾ"): level, bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᶿ"): msg})
    def _11111lllll1_opy_(self):
        for level, bstack11111lll1l1_opy_ in self._11111lll111_opy_.items():
            setattr(logging, level, self._11111lll11l_opy_(level, bstack11111lll1l1_opy_))
    def _11111lll11l_opy_(self, level, bstack11111lll1l1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11111lll1l1_opy_(msg, *args, **kwargs)
            self._11111llll1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11111llll11_opy_
        for level, bstack11111lll1l1_opy_ in self._11111lll111_opy_.items():
            setattr(logging, level, bstack11111lll1l1_opy_)