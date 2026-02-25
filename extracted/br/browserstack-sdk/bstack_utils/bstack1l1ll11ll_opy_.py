# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l1111ll1l_opy_ import bstack11l1111l1ll_opy_
from bstack_utils.constants import *
import json
class bstack11l111lll_opy_:
    def __init__(self, bstack111ll111ll_opy_, bstack11l1111l1l1_opy_):
        self.bstack111ll111ll_opy_ = bstack111ll111ll_opy_
        self.bstack11l1111l1l1_opy_ = bstack11l1111l1l1_opy_
        self.bstack11l111l1111_opy_ = None
    def __call__(self):
        bstack11l111l111l_opy_ = {}
        while True:
            self.bstack11l111l1111_opy_ = bstack11l111l111l_opy_.get(
                bstack11l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᥡ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l1111llll_opy_ = self.bstack11l111l1111_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l1111llll_opy_ > 0:
                sleep(bstack11l1111llll_opy_ / 1000)
            params = {
                bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᥢ"): self.bstack111ll111ll_opy_,
                bstack11l1l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᥣ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l111l11l1_opy_ = bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᥤ") + bstack11l1111lll1_opy_ + bstack11l1l11_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤᥥ")
            if self.bstack11l1111l1l1_opy_.lower() == bstack11l1l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢᥦ"):
                bstack11l111l111l_opy_ = bstack11l1111l1ll_opy_.results(bstack11l111l11l1_opy_, params)
            else:
                bstack11l111l111l_opy_ = bstack11l1111l1ll_opy_.bstack11l1111ll11_opy_(bstack11l111l11l1_opy_, params)
            if str(bstack11l111l111l_opy_.get(bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᥧ"), bstack11l1l11_opy_ (u"ࠨ࠴࠳࠴ࠬᥨ"))) != bstack11l1l11_opy_ (u"ࠩ࠷࠴࠹࠭ᥩ"):
                break
        return bstack11l111l111l_opy_.get(bstack11l1l11_opy_ (u"ࠪࡨࡦࡺࡡࠨᥪ"), bstack11l111l111l_opy_)