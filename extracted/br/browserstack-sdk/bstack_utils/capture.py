# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import builtins
import logging
class bstack11111l1l11_opy_:
    def __init__(self, handler):
        self._111ll1l11ll_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111ll11llll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack1111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭᭒"), bstack1111l_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ᭓"), bstack1111l_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫ᭔"), bstack1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᭕")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111ll1l111l_opy_
        self._111ll1l1111_opy_()
    def _111ll1l111l_opy_(self, *args, **kwargs):
        self._111ll1l11ll_opy_(*args, **kwargs)
        message = bstack1111l_opy_ (u"ࠬࠦࠧ᭖").join(map(str, args)) + bstack1111l_opy_ (u"࠭࡜࡯ࠩ᭗")
        self._111ll1l11l1_opy_(bstack1111l_opy_ (u"ࠧࡊࡐࡉࡓࠬ᭘"), message)
    def _111ll1l11l1_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack1111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᭙"): level, bstack1111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᭚"): msg})
    def _111ll1l1111_opy_(self):
        for level, bstack111ll1l1l11_opy_ in self._111ll11llll_opy_.items():
            setattr(logging, level, self._111ll11lll1_opy_(level, bstack111ll1l1l11_opy_))
    def _111ll11lll1_opy_(self, level, bstack111ll1l1l11_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111ll1l1l11_opy_(msg, *args, **kwargs)
            self._111ll1l11l1_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111ll1l11ll_opy_
        for level, bstack111ll1l1l11_opy_ in self._111ll11llll_opy_.items():
            setattr(logging, level, bstack111ll1l1l11_opy_)