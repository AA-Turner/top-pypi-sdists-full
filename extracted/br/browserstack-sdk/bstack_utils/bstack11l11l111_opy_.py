# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l11l1l1_opy_ import bstack1111l11l1ll_opy_
from bstack_utils.constants import *
import json
class bstack111ll1111_opy_:
    def __init__(self, bstack111l1l11_opy_, bstack1111l11l11l_opy_):
        self.bstack111l1l11_opy_ = bstack111l1l11_opy_
        self.bstack1111l11l11l_opy_ = bstack1111l11l11l_opy_
        self.bstack1111l11l111_opy_ = None
    def __call__(self):
        bstack1111l111lll_opy_ = {}
        while True:
            self.bstack1111l11l111_opy_ = bstack1111l111lll_opy_.get(
                bstack11ll11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᶇ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l111ll1_opy_ = self.bstack1111l11l111_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l111ll1_opy_ > 0:
                sleep(bstack1111l111ll1_opy_ / 1000)
            params = {
                bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶈ"): self.bstack111l1l11_opy_,
                bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᶉ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᶊ") + bstack1111l11ll1l_opy_ + bstack11ll11_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᶋ")
            if self.bstack1111l11l11l_opy_.lower() == bstack11ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᶌ"):
                bstack1111l111lll_opy_ = bstack1111l11l1ll_opy_.results(base_url, params)
            else:
                bstack1111l111lll_opy_ = bstack1111l11l1ll_opy_.bstack1111l11ll11_opy_(base_url, params)
            if str(bstack1111l111lll_opy_.get(bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶍ"), bstack11ll11_opy_ (u"࠭࠲࠱࠲ࠪᶎ"))) != bstack11ll11_opy_ (u"ࠧ࠵࠲࠷ࠫᶏ"):
                break
        return bstack1111l111lll_opy_.get(bstack11ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᶐ"), bstack1111l111lll_opy_)