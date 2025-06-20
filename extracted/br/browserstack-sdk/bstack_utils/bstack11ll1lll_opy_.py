# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11lll1l_opy_ import bstack11ll1l11111_opy_
from bstack_utils.constants import *
import json
class bstack1lll11111_opy_:
    def __init__(self, bstack1l1llll1l_opy_, bstack11ll11llll1_opy_):
        self.bstack1l1llll1l_opy_ = bstack1l1llll1l_opy_
        self.bstack11ll11llll1_opy_ = bstack11ll11llll1_opy_
        self.bstack11ll11ll1l1_opy_ = None
    def __call__(self):
        bstack11ll11lllll_opy_ = {}
        while True:
            self.bstack11ll11ll1l1_opy_ = bstack11ll11lllll_opy_.get(
                bstack11ll11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᜆ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1l1111l_opy_ = self.bstack11ll11ll1l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1l1111l_opy_ > 0:
                sleep(bstack11ll1l1111l_opy_ / 1000)
            params = {
                bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜇ"): self.bstack1l1llll1l_opy_,
                bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᜈ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11ll1ll_opy_ = bstack11ll11_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᜉ") + bstack11ll1l111l1_opy_ + bstack11ll11_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᜊ")
            if self.bstack11ll11llll1_opy_.lower() == bstack11ll11_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨᜋ"):
                bstack11ll11lllll_opy_ = bstack11ll1l11111_opy_.results(bstack11ll11ll1ll_opy_, params)
            else:
                bstack11ll11lllll_opy_ = bstack11ll1l11111_opy_.bstack11ll11lll11_opy_(bstack11ll11ll1ll_opy_, params)
            if str(bstack11ll11lllll_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᜌ"), bstack11ll11_opy_ (u"ࠧ࠳࠲࠳ࠫᜍ"))) != bstack11ll11_opy_ (u"ࠨ࠶࠳࠸ࠬᜎ"):
                break
        return bstack11ll11lllll_opy_.get(bstack11ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧᜏ"), bstack11ll11lllll_opy_)