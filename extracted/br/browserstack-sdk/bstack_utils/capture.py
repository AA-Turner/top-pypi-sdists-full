# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import builtins
import logging
class bstack111l1111ll_opy_:
    def __init__(self, handler):
        self._11l11ll1ll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l11ll11l1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1l1111_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᢚ"), bstack1l1111_opy_ (u"࠭ࡤࡦࡤࡸ࡫ࠬᢛ"), bstack1l1111_opy_ (u"ࠧࡸࡣࡵࡲ࡮ࡴࡧࠨᢜ"), bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᢝ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l11ll1l11_opy_
        self._11l11ll111l_opy_()
    def _11l11ll1l11_opy_(self, *args, **kwargs):
        self._11l11ll1ll1_opy_(*args, **kwargs)
        message = bstack1l1111_opy_ (u"ࠩࠣࠫᢞ").join(map(str, args)) + bstack1l1111_opy_ (u"ࠪࡠࡳ࠭ᢟ")
        self._11l11ll1l1l_opy_(bstack1l1111_opy_ (u"ࠫࡎࡔࡆࡐࠩᢠ"), message)
    def _11l11ll1l1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᢡ"): level, bstack1l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᢢ"): msg})
    def _11l11ll111l_opy_(self):
        for level, bstack11l11ll11ll_opy_ in self._11l11ll11l1_opy_.items():
            setattr(logging, level, self._11l11ll1111_opy_(level, bstack11l11ll11ll_opy_))
    def _11l11ll1111_opy_(self, level, bstack11l11ll11ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l11ll11ll_opy_(msg, *args, **kwargs)
            self._11l11ll1l1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l11ll1ll1_opy_
        for level, bstack11l11ll11ll_opy_ in self._11l11ll11l1_opy_.items():
            setattr(logging, level, bstack11l11ll11ll_opy_)