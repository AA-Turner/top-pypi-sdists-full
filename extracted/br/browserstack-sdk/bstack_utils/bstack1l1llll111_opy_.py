# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l11ll1l_opy_ import bstack1111l11l11l_opy_
from bstack_utils.constants import *
import json
class bstack1l1l1llll1_opy_:
    def __init__(self, bstack1l1l1l1l_opy_, bstack1111l11l111_opy_):
        self.bstack1l1l1l1l_opy_ = bstack1l1l1l1l_opy_
        self.bstack1111l11l111_opy_ = bstack1111l11l111_opy_
        self.bstack1111l111lll_opy_ = None
    def __call__(self):
        bstack1111l11lll1_opy_ = {}
        while True:
            self.bstack1111l111lll_opy_ = bstack1111l11lll1_opy_.get(
                bstack1ll1l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᶆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l11l1l1_opy_ = self.bstack1111l111lll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l11l1l1_opy_ > 0:
                sleep(bstack1111l11l1l1_opy_ / 1000)
            params = {
                bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶇ"): self.bstack1l1l1l1l_opy_,
                bstack1ll1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᶈ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᶉ") + bstack1111l11ll11_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᶊ")
            if self.bstack1111l11l111_opy_.lower() == bstack1ll1l11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᶋ"):
                bstack1111l11lll1_opy_ = bstack1111l11l11l_opy_.results(base_url, params)
            else:
                bstack1111l11lll1_opy_ = bstack1111l11l11l_opy_.bstack1111l11l1ll_opy_(base_url, params)
            if str(bstack1111l11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᶌ"), bstack1ll1l11_opy_ (u"ࠬ࠸࠰࠱ࠩᶍ"))) != bstack1ll1l11_opy_ (u"࠭࠴࠱࠶ࠪᶎ"):
                break
        return bstack1111l11lll1_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᶏ"), bstack1111l11lll1_opy_)