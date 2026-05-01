# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11111lll1ll_opy_ import bstack11111llllll_opy_
from bstack_utils.constants import *
import json
class bstack1l1l111l1l_opy_:
    def __init__(self, bstack1lllllllll_opy_, bstack11111llll11_opy_):
        self.bstack1lllllllll_opy_ = bstack1lllllllll_opy_
        self.bstack11111llll11_opy_ = bstack11111llll11_opy_
        self.bstack11111lll11l_opy_ = None
    def __call__(self):
        bstack11111lllll1_opy_ = {}
        while True:
            self.bstack11111lll11l_opy_ = bstack11111lllll1_opy_.get(
                bstack111ll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ᷀"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l111111_opy_ = self.bstack11111lll11l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l111111_opy_ > 0:
                sleep(bstack1111l111111_opy_ / 1000)
            params = {
                bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᷁"): self.bstack1lllllllll_opy_,
                bstack111ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴ᷂ࠬ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack111ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᷃") + bstack11111lll1l1_opy_ + bstack111ll_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣ᷄")
            if self.bstack11111llll11_opy_.lower() == bstack111ll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ᷅"):
                bstack11111lllll1_opy_ = bstack11111llllll_opy_.results(base_url, params)
            else:
                bstack11111lllll1_opy_ = bstack11111llllll_opy_.bstack11111llll1l_opy_(base_url, params)
            if str(bstack11111lllll1_opy_.get(bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᷆"), bstack111ll_opy_ (u"ࠧ࠳࠲࠳ࠫ᷇"))) != bstack111ll_opy_ (u"ࠨ࠶࠳࠸ࠬ᷈"):
                break
        return bstack11111lllll1_opy_.get(bstack111ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ᷉"), bstack11111lllll1_opy_)