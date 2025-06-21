# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import builtins
import logging
class bstack111llll11l_opy_:
    def __init__(self, handler):
        self._11ll11ll11l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll11l1l1l_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ᜚"), bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭᜛"), bstack1l1l1l1_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩ᜜"), bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᜝")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll11l1lll_opy_
        self._11ll11l1l11_opy_()
    def _11ll11l1lll_opy_(self, *args, **kwargs):
        self._11ll11ll11l_opy_(*args, **kwargs)
        message = bstack1l1l1l1_opy_ (u"ࠪࠤࠬ᜞").join(map(str, args)) + bstack1l1l1l1_opy_ (u"ࠫࡡࡴࠧᜟ")
        self._log_message(bstack1l1l1l1_opy_ (u"ࠬࡏࡎࡇࡑࠪᜠ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1l1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᜡ"): level, bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᜢ"): msg})
    def _11ll11l1l11_opy_(self):
        for level, bstack11ll11ll111_opy_ in self._11ll11l1l1l_opy_.items():
            setattr(logging, level, self._11ll11l1ll1_opy_(level, bstack11ll11ll111_opy_))
    def _11ll11l1ll1_opy_(self, level, bstack11ll11ll111_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll11ll111_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll11ll11l_opy_
        for level, bstack11ll11ll111_opy_ in self._11ll11l1l1l_opy_.items():
            setattr(logging, level, bstack11ll11ll111_opy_)