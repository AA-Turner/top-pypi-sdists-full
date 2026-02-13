# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import builtins
import logging
class bstack11111llll1_opy_:
    def __init__(self, handler):
        self._111llll1ll1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111lllll111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11l11_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᥪ"), bstack11l11_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᥫ"), bstack11l11_opy_ (u"ࠬࡽࡡࡳࡰ࡬ࡲ࡬࠭ᥬ"), bstack11l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᥭ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111llll1l11_opy_
        self._111llll1lll_opy_()
    def _111llll1l11_opy_(self, *args, **kwargs):
        self._111llll1ll1_opy_(*args, **kwargs)
        message = bstack11l11_opy_ (u"ࠧࠡࠩ᥮").join(map(str, args)) + bstack11l11_opy_ (u"ࠨ࡞ࡱࠫ᥯")
        self._111llll1l1l_opy_(bstack11l11_opy_ (u"ࠩࡌࡒࡋࡕࠧᥰ"), message)
    def _111llll1l1l_opy_(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᥱ"): level, bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᥲ"): msg})
    def _111llll1lll_opy_(self):
        for level, bstack111llll11ll_opy_ in self._111lllll111_opy_.items():
            setattr(logging, level, self._111lllll11l_opy_(level, bstack111llll11ll_opy_))
    def _111lllll11l_opy_(self, level, bstack111llll11ll_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111llll11ll_opy_(msg, *args, **kwargs)
            self._111llll1l1l_opy_(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111llll1ll1_opy_
        for level, bstack111llll11ll_opy_ in self._111lllll111_opy_.items():
            setattr(logging, level, bstack111llll11ll_opy_)