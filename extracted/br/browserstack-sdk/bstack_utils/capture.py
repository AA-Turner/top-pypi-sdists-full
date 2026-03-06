# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import builtins
import logging
class bstack1111l111ll_opy_:
    def __init__(self, handler):
        self._111lll11ll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111lll11lll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1111_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭᪜"), bstack1111_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ᪝"), bstack1111_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫ᪞"), bstack1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᪟")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111lll11l11_opy_
        self._111lll111l1_opy_()
    def _111lll11l11_opy_(self, *args, **kwargs):
        self._111lll11ll1_opy_(*args, **kwargs)
        message = bstack1111_opy_ (u"ࠬࠦࠧ᪠").join(map(str, args)) + bstack1111_opy_ (u"࠭࡜࡯ࠩ᪡")
        self._111lll11l1l_opy_(bstack1111_opy_ (u"ࠧࡊࡐࡉࡓࠬ᪢"), message)
    def _111lll11l1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᪣"): level, bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᪤"): msg})
    def _111lll111l1_opy_(self):
        for level, bstack111lll111ll_opy_ in self._111lll11lll_opy_.items():
            setattr(logging, level, self._111lll1111l_opy_(level, bstack111lll111ll_opy_))
    def _111lll1111l_opy_(self, level, bstack111lll111ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111lll111ll_opy_(msg, *args, **kwargs)
            self._111lll11l1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111lll11ll1_opy_
        for level, bstack111lll111ll_opy_ in self._111lll11lll_opy_.items():
            setattr(logging, level, bstack111lll111ll_opy_)