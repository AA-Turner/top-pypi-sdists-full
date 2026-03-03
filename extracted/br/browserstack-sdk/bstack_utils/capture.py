# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import builtins
import logging
class bstack1111ll1l11_opy_:
    def __init__(self, handler):
        self._11l11111l11_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11l11111ll1_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll111_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᥱ"), bstack11ll111_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᥲ"), bstack11ll111_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᥳ"), bstack11ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᥴ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11l11111lll_opy_
        self._11l111111l1_opy_()
    def _11l11111lll_opy_(self, *args, **kwargs):
        self._11l11111l11_opy_(*args, **kwargs)
        message = bstack11ll111_opy_ (u"ࠧࠡࠩ᥵").join(map(str, args)) + bstack11ll111_opy_ (u"ࠨ࡞ࡱࠫ᥶")
        self._11l11111l1l_opy_(bstack11ll111_opy_ (u"ࠩࡌࡒࡋࡕࠧ᥷"), message)
    def _11l11111l1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᥸"): level, bstack11ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᥹"): msg})
    def _11l111111l1_opy_(self):
        for level, bstack11l111111ll_opy_ in self._11l11111ll1_opy_.items():
            setattr(logging, level, self._11l1111l111_opy_(level, bstack11l111111ll_opy_))
    def _11l1111l111_opy_(self, level, bstack11l111111ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11l111111ll_opy_(msg, *args, **kwargs)
            self._11l11111l1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11l11111l11_opy_
        for level, bstack11l111111ll_opy_ in self._11l11111ll1_opy_.items():
            setattr(logging, level, bstack11l111111ll_opy_)