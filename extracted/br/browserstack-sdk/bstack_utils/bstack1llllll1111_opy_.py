# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l11l111_opy_ import bstack1111l111lll_opy_
from bstack_utils.constants import *
import json
class bstack1l11l11ll1_opy_:
    def __init__(self, bstack1ll1l1l11l_opy_, bstack1111l11l11l_opy_):
        self.bstack1ll1l1l11l_opy_ = bstack1ll1l1l11l_opy_
        self.bstack1111l11l11l_opy_ = bstack1111l11l11l_opy_
        self.bstack1111l11l1ll_opy_ = None
    def __call__(self):
        bstack1111l11ll11_opy_ = {}
        while True:
            self.bstack1111l11l1ll_opy_ = bstack1111l11ll11_opy_.get(
                bstack111l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᶆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l11l1l1_opy_ = self.bstack1111l11l1ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l11l1l1_opy_ > 0:
                sleep(bstack1111l11l1l1_opy_ / 1000)
            params = {
                bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶇ"): self.bstack1ll1l1l11l_opy_,
                bstack111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᶈ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᶉ") + bstack1111l11ll1l_opy_ + bstack111l_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᶊ")
            if self.bstack1111l11l11l_opy_.lower() == bstack111l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᶋ"):
                bstack1111l11ll11_opy_ = bstack1111l111lll_opy_.results(base_url, params)
            else:
                bstack1111l11ll11_opy_ = bstack1111l111lll_opy_.bstack1111l11lll1_opy_(base_url, params)
            if str(bstack1111l11ll11_opy_.get(bstack111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᶌ"), bstack111l_opy_ (u"ࠬ࠸࠰࠱ࠩᶍ"))) != bstack111l_opy_ (u"࠭࠴࠱࠶ࠪᶎ"):
                break
        return bstack1111l11ll11_opy_.get(bstack111l_opy_ (u"ࠧࡥࡣࡷࡥࠬᶏ"), bstack1111l11ll11_opy_)