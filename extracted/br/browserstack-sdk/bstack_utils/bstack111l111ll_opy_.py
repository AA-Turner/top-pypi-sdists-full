# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1l11l1_opy_ import bstack11lll11lll1_opy_
from bstack_utils.constants import *
import json
class bstack1ll1llll1_opy_:
    def __init__(self, bstack1l111l11ll_opy_, bstack11lll11ll11_opy_):
        self.bstack1l111l11ll_opy_ = bstack1l111l11ll_opy_
        self.bstack11lll11ll11_opy_ = bstack11lll11ll11_opy_
        self.bstack11lll11ll1l_opy_ = None
    def __call__(self):
        bstack11lll1l11ll_opy_ = {}
        while True:
            self.bstack11lll11ll1l_opy_ = bstack11lll1l11ll_opy_.get(
                bstack1l11lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᙐ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l111l_opy_ = self.bstack11lll11ll1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l111l_opy_ > 0:
                sleep(bstack11lll1l111l_opy_ / 1000)
            params = {
                bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᙑ"): self.bstack1l111l11ll_opy_,
                bstack1l11lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᙒ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll11llll_opy_ = bstack1l11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᙓ") + bstack11lll1l1111_opy_ + bstack1l11lll_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᙔ")
            if self.bstack11lll11ll11_opy_.lower() == bstack1l11lll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨᙕ"):
                bstack11lll1l11ll_opy_ = bstack11lll11lll1_opy_.results(bstack11lll11llll_opy_, params)
            else:
                bstack11lll1l11ll_opy_ = bstack11lll11lll1_opy_.bstack11lll1l1l11_opy_(bstack11lll11llll_opy_, params)
            if str(bstack11lll1l11ll_opy_.get(bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙖ"), bstack1l11lll_opy_ (u"ࠧ࠳࠲࠳ࠫᙗ"))) != bstack1l11lll_opy_ (u"ࠨ࠶࠳࠸ࠬᙘ"):
                break
        return bstack11lll1l11ll_opy_.get(bstack1l11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᙙ"), bstack11lll1l11ll_opy_)