# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111ll111111_opy_ import bstack111l1llll11_opy_
from bstack_utils.constants import *
import json
class bstack1llll1ll1_opy_:
    def __init__(self, bstack1l11l1lll_opy_, bstack111ll1111l1_opy_):
        self.bstack1l11l1lll_opy_ = bstack1l11l1lll_opy_
        self.bstack111ll1111l1_opy_ = bstack111ll1111l1_opy_
        self.bstack111ll11111l_opy_ = None
    def __call__(self):
        bstack111l1llll1l_opy_ = {}
        while True:
            self.bstack111ll11111l_opy_ = bstack111l1llll1l_opy_.get(
                bstack11lll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᮆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111l1llllll_opy_ = self.bstack111ll11111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111l1llllll_opy_ > 0:
                sleep(bstack111l1llllll_opy_ / 1000)
            params = {
                bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᮇ"): self.bstack1l11l1lll_opy_,
                bstack11lll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᮈ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack11lll1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᮉ") + bstack111l1lllll1_opy_ + bstack11lll1_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᮊ")
            if self.bstack111ll1111l1_opy_.lower() == bstack11lll1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᮋ"):
                bstack111l1llll1l_opy_ = bstack111l1llll11_opy_.results(base_url, params)
            else:
                bstack111l1llll1l_opy_ = bstack111l1llll11_opy_.bstack111ll1111ll_opy_(base_url, params)
            if str(bstack111l1llll1l_opy_.get(bstack11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᮌ"), bstack11lll1_opy_ (u"ࠫ࠷࠶࠰ࠨᮍ"))) != bstack11lll1_opy_ (u"ࠬ࠺࠰࠵ࠩᮎ"):
                break
        return bstack111l1llll1l_opy_.get(bstack11lll1_opy_ (u"࠭ࡤࡢࡶࡤࠫᮏ"), bstack111l1llll1l_opy_)