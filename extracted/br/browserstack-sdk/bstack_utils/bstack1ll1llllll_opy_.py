# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111l1llllll_opy_ import bstack111l1lllll1_opy_
from bstack_utils.constants import *
import json
class bstack1l1111l1l_opy_:
    def __init__(self, bstack1l11lllll1_opy_, bstack111l1llll11_opy_):
        self.bstack1l11lllll1_opy_ = bstack1l11lllll1_opy_
        self.bstack111l1llll11_opy_ = bstack111l1llll11_opy_
        self.bstack111l1lll11l_opy_ = None
    def __call__(self):
        bstack111l1llll1l_opy_ = {}
        while True:
            self.bstack111l1lll11l_opy_ = bstack111l1llll1l_opy_.get(
                bstack1l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᮎ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111l1lll111_opy_ = self.bstack111l1lll11l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111l1lll111_opy_ > 0:
                sleep(bstack111l1lll111_opy_ / 1000)
            params = {
                bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᮏ"): self.bstack1l11lllll1_opy_,
                bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᮐ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᮑ") + bstack111l1lll1ll_opy_ + bstack1l1_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᮒ")
            if self.bstack111l1llll11_opy_.lower() == bstack1l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᮓ"):
                bstack111l1llll1l_opy_ = bstack111l1lllll1_opy_.results(base_url, params)
            else:
                bstack111l1llll1l_opy_ = bstack111l1lllll1_opy_.bstack111l1lll1l1_opy_(base_url, params)
            if str(bstack111l1llll1l_opy_.get(bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᮔ"), bstack1l1_opy_ (u"ࠬ࠸࠰࠱ࠩᮕ"))) != bstack1l1_opy_ (u"࠭࠴࠱࠶ࠪᮖ"):
                break
        return bstack111l1llll1l_opy_.get(bstack1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᮗ"), bstack111l1llll1l_opy_)