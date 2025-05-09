# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll11llll_opy_ import bstack11lll1l1111_opy_
from bstack_utils.constants import *
import json
class bstack1ll111lll_opy_:
    def __init__(self, bstack1l11ll1111_opy_, bstack11lll11l1ll_opy_):
        self.bstack1l11ll1111_opy_ = bstack1l11ll1111_opy_
        self.bstack11lll11l1ll_opy_ = bstack11lll11l1ll_opy_
        self.bstack11lll11ll1l_opy_ = None
    def __call__(self):
        bstack11lll1l11l1_opy_ = {}
        while True:
            self.bstack11lll11ll1l_opy_ = bstack11lll1l11l1_opy_.get(
                bstack11lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᙗ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l111l_opy_ = self.bstack11lll11ll1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l111l_opy_ > 0:
                sleep(bstack11lll1l111l_opy_ / 1000)
            params = {
                bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᙘ"): self.bstack1l11ll1111_opy_,
                bstack11lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᙙ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll11lll1_opy_ = bstack11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᙚ") + bstack11lll11ll11_opy_ + bstack11lll_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᙛ")
            if self.bstack11lll11l1ll_opy_.lower() == bstack11lll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨᙜ"):
                bstack11lll1l11l1_opy_ = bstack11lll1l1111_opy_.results(bstack11lll11lll1_opy_, params)
            else:
                bstack11lll1l11l1_opy_ = bstack11lll1l1111_opy_.bstack11lll11l1l1_opy_(bstack11lll11lll1_opy_, params)
            if str(bstack11lll1l11l1_opy_.get(bstack11lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙝ"), bstack11lll_opy_ (u"ࠧ࠳࠲࠳ࠫᙞ"))) != bstack11lll_opy_ (u"ࠨ࠶࠳࠸ࠬᙟ"):
                break
        return bstack11lll1l11l1_opy_.get(bstack11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᙠ"), bstack11lll1l11l1_opy_)