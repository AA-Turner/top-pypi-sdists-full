# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1ll1111_opy_ import bstack11ll1l1lll1_opy_
from bstack_utils.constants import *
import json
class bstack11ll111l_opy_:
    def __init__(self, bstack1ll1ll1111_opy_, bstack11ll1ll111l_opy_):
        self.bstack1ll1ll1111_opy_ = bstack1ll1ll1111_opy_
        self.bstack11ll1ll111l_opy_ = bstack11ll1ll111l_opy_
        self.bstack11ll1l1ll11_opy_ = None
    def __call__(self):
        bstack11ll1l1ll1l_opy_ = {}
        while True:
            self.bstack11ll1l1ll11_opy_ = bstack11ll1l1ll1l_opy_.get(
                bstack111lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᛸ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1l1llll_opy_ = self.bstack11ll1l1ll11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1l1llll_opy_ > 0:
                sleep(bstack11ll1l1llll_opy_ / 1000)
            params = {
                bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᛹"): self.bstack1ll1ll1111_opy_,
                bstack111lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᛺"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll1l1l1l1_opy_ = bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᛻") + bstack11ll1l1l11l_opy_ + bstack111lll_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣ᛼")
            if self.bstack11ll1ll111l_opy_.lower() == bstack111lll_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ᛽"):
                bstack11ll1l1ll1l_opy_ = bstack11ll1l1lll1_opy_.results(bstack11ll1l1l1l1_opy_, params)
            else:
                bstack11ll1l1ll1l_opy_ = bstack11ll1l1lll1_opy_.bstack11ll1l1l1ll_opy_(bstack11ll1l1l1l1_opy_, params)
            if str(bstack11ll1l1ll1l_opy_.get(bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᛾"), bstack111lll_opy_ (u"ࠧ࠳࠲࠳ࠫ᛿"))) != bstack111lll_opy_ (u"ࠨ࠶࠳࠸ࠬᜀ"):
                break
        return bstack11ll1l1ll1l_opy_.get(bstack111lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᜁ"), bstack11ll1l1ll1l_opy_)