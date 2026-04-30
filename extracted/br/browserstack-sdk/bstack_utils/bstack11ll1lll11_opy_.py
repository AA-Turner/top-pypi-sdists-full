# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l11111l_opy_ import bstack1111l111111_opy_
from bstack_utils.constants import *
import json
class bstack1l1l1l1l1_opy_:
    def __init__(self, bstack11l1l111ll_opy_, bstack11111llllll_opy_):
        self.bstack11l1l111ll_opy_ = bstack11l1l111ll_opy_
        self.bstack11111llllll_opy_ = bstack11111llllll_opy_
        self.bstack1111l111l11_opy_ = None
    def __call__(self):
        bstack1111l1111l1_opy_ = {}
        while True:
            self.bstack1111l111l11_opy_ = bstack1111l1111l1_opy_.get(
                bstack1l1111l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᶥ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11111llll1l_opy_ = self.bstack1111l111l11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11111llll1l_opy_ > 0:
                sleep(bstack11111llll1l_opy_ / 1000)
            params = {
                bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶦ"): self.bstack11l1l111ll_opy_,
                bstack1l1111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᶧ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1l1111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᶨ") + bstack11111lllll1_opy_ + bstack1l1111l_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤᶩ")
            if self.bstack11111llllll_opy_.lower() == bstack1l1111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢᶪ"):
                bstack1111l1111l1_opy_ = bstack1111l111111_opy_.results(base_url, params)
            else:
                bstack1111l1111l1_opy_ = bstack1111l111111_opy_.bstack1111l1111ll_opy_(base_url, params)
            if str(bstack1111l1111l1_opy_.get(bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᶫ"), bstack1l1111l_opy_ (u"ࠨ࠴࠳࠴ࠬᶬ"))) != bstack1l1111l_opy_ (u"ࠩ࠷࠴࠹࠭ᶭ"):
                break
        return bstack1111l1111l1_opy_.get(bstack1l1111l_opy_ (u"ࠪࡨࡦࡺࡡࠨᶮ"), bstack1111l1111l1_opy_)