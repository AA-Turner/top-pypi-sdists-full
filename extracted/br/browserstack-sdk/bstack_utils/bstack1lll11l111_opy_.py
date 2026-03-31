# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111l1ll11l1_opy_ import bstack111l1ll1111_opy_
from bstack_utils.constants import *
import json
class bstack11l1l1ll1_opy_:
    def __init__(self, bstack1l11ll111l_opy_, bstack111l1ll11ll_opy_):
        self.bstack1l11ll111l_opy_ = bstack1l11ll111l_opy_
        self.bstack111l1ll11ll_opy_ = bstack111l1ll11ll_opy_
        self.bstack111l1l1llll_opy_ = None
    def __call__(self):
        bstack111l1l1lll1_opy_ = {}
        while True:
            self.bstack111l1l1llll_opy_ = bstack111l1l1lll1_opy_.get(
                bstack1ll11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ᮷"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111l1ll111l_opy_ = self.bstack111l1l1llll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111l1ll111l_opy_ > 0:
                sleep(bstack111l1ll111l_opy_ / 1000)
            params = {
                bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᮸"): self.bstack1l11ll111l_opy_,
                bstack1ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ᮹"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᮺ") + bstack111l1ll1l11_opy_ + bstack1ll11_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᮻ")
            if self.bstack111l1ll11ll_opy_.lower() == bstack1ll11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᮼ"):
                bstack111l1l1lll1_opy_ = bstack111l1ll1111_opy_.results(base_url, params)
            else:
                bstack111l1l1lll1_opy_ = bstack111l1ll1111_opy_.bstack111l1ll1l1l_opy_(base_url, params)
            if str(bstack111l1l1lll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᮽ"), bstack1ll11_opy_ (u"ࠫ࠷࠶࠰ࠨᮾ"))) != bstack1ll11_opy_ (u"ࠬ࠺࠰࠵ࠩᮿ"):
                break
        return bstack111l1l1lll1_opy_.get(bstack1ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᯀ"), bstack111l1l1lll1_opy_)