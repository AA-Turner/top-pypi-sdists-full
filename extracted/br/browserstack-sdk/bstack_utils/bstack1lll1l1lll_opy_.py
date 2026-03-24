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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111l1lll11l_opy_ import bstack111l1llll11_opy_
from bstack_utils.constants import *
import json
class bstack11l1l1ll11_opy_:
    def __init__(self, bstack11l1l11l1_opy_, bstack111l1lll1l1_opy_):
        self.bstack11l1l11l1_opy_ = bstack11l1l11l1_opy_
        self.bstack111l1lll1l1_opy_ = bstack111l1lll1l1_opy_
        self.bstack111ll111111_opy_ = None
    def __call__(self):
        bstack111l1lll1ll_opy_ = {}
        while True:
            self.bstack111ll111111_opy_ = bstack111l1lll1ll_opy_.get(
                bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᮉ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111l1llllll_opy_ = self.bstack111ll111111_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111l1llllll_opy_ > 0:
                sleep(bstack111l1llllll_opy_ / 1000)
            params = {
                bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᮊ"): self.bstack11l1l11l1_opy_,
                bstack1ll1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᮋ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᮌ") + bstack111l1llll1l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᮍ")
            if self.bstack111l1lll1l1_opy_.lower() == bstack1ll1lll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨᮎ"):
                bstack111l1lll1ll_opy_ = bstack111l1llll11_opy_.results(base_url, params)
            else:
                bstack111l1lll1ll_opy_ = bstack111l1llll11_opy_.bstack111l1lllll1_opy_(base_url, params)
            if str(bstack111l1lll1ll_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᮏ"), bstack1ll1lll_opy_ (u"ࠧ࠳࠲࠳ࠫᮐ"))) != bstack1ll1lll_opy_ (u"ࠨ࠶࠳࠸ࠬᮑ"):
                break
        return bstack111l1lll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᮒ"), bstack111l1lll1ll_opy_)