# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import builtins
import logging
class bstack111lll111l_opy_:
    def __init__(self, handler):
        self._11ll1111l1l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11ll1111l11_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack111l111_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ᝼"), bstack111l111_opy_ (u"ࠧࡥࡧࡥࡹ࡬࠭᝽"), bstack111l111_opy_ (u"ࠨࡹࡤࡶࡳ࡯࡮ࡨࠩ᝾"), bstack111l111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᝿")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11ll1111lll_opy_
        self._11ll111l111_opy_()
    def _11ll1111lll_opy_(self, *args, **kwargs):
        self._11ll1111l1l_opy_(*args, **kwargs)
        message = bstack111l111_opy_ (u"ࠪࠤࠬក").join(map(str, args)) + bstack111l111_opy_ (u"ࠫࡡࡴࠧខ")
        self._log_message(bstack111l111_opy_ (u"ࠬࡏࡎࡇࡑࠪគ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack111l111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬឃ"): level, bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨង"): msg})
    def _11ll111l111_opy_(self):
        for level, bstack11ll111l11l_opy_ in self._11ll1111l11_opy_.items():
            setattr(logging, level, self._11ll1111ll1_opy_(level, bstack11ll111l11l_opy_))
    def _11ll1111ll1_opy_(self, level, bstack11ll111l11l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11ll111l11l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11ll1111l1l_opy_
        for level, bstack11ll111l11l_opy_ in self._11ll1111l11_opy_.items():
            setattr(logging, level, bstack11ll111l11l_opy_)