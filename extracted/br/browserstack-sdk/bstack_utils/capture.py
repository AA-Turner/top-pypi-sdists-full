# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import builtins
import logging
class bstack1lllll1ll1l_opy_:
    def __init__(self, handler):
        self._111l1lll111_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111l1ll1l11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᮝ"), bstack1ll1lll_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭ᮞ"), bstack1ll1lll_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩᮟ"), bstack1ll1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᮠ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111l1ll1l1l_opy_
        self._111l1ll1lll_opy_()
    def _111l1ll1l1l_opy_(self, *args, **kwargs):
        self._111l1lll111_opy_(*args, **kwargs)
        message = bstack1ll1lll_opy_ (u"ࠪࠤࠬᮡ").join(map(str, args)) + bstack1ll1lll_opy_ (u"ࠫࡡࡴࠧᮢ")
        self._111l1ll11l1_opy_(bstack1ll1lll_opy_ (u"ࠬࡏࡎࡇࡑࠪᮣ"), message)
    def _111l1ll11l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1ll1lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᮤ"): level, bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᮥ"): msg})
    def _111l1ll1lll_opy_(self):
        for level, bstack111l1ll11ll_opy_ in self._111l1ll1l11_opy_.items():
            setattr(logging, level, self._111l1ll1ll1_opy_(level, bstack111l1ll11ll_opy_))
    def _111l1ll1ll1_opy_(self, level, bstack111l1ll11ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111l1ll11ll_opy_(msg, *args, **kwargs)
            self._111l1ll11l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111l1lll111_opy_
        for level, bstack111l1ll11ll_opy_ in self._111l1ll1l11_opy_.items():
            setattr(logging, level, bstack111l1ll11ll_opy_)