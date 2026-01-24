# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l11lllll1_opy_ import bstack11l11lll11l_opy_
from bstack_utils.constants import *
import json
class bstack1l11l1ll11_opy_:
    def __init__(self, bstack1l1l11l11l_opy_, bstack11l11lll111_opy_):
        self.bstack1l1l11l11l_opy_ = bstack1l1l11l11l_opy_
        self.bstack11l11lll111_opy_ = bstack11l11lll111_opy_
        self.bstack11l11llll11_opy_ = None
    def __call__(self):
        bstack11l11lll1l1_opy_ = {}
        while True:
            self.bstack11l11llll11_opy_ = bstack11l11lll1l1_opy_.get(
                bstack1l1111_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᢇ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l11llllll_opy_ = self.bstack11l11llll11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l11llllll_opy_ > 0:
                sleep(bstack11l11llllll_opy_ / 1000)
            params = {
                bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᢈ"): self.bstack1l1l11l11l_opy_,
                bstack1l1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᢉ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l11ll1lll_opy_ = bstack1l1111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᢊ") + bstack11l11lll1ll_opy_ + bstack1l1111_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᢋ")
            if self.bstack11l11lll111_opy_.lower() == bstack1l1111_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨᢌ"):
                bstack11l11lll1l1_opy_ = bstack11l11lll11l_opy_.results(bstack11l11ll1lll_opy_, params)
            else:
                bstack11l11lll1l1_opy_ = bstack11l11lll11l_opy_.bstack11l11llll1l_opy_(bstack11l11ll1lll_opy_, params)
            if str(bstack11l11lll1l1_opy_.get(bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᢍ"), bstack1l1111_opy_ (u"ࠧ࠳࠲࠳ࠫᢎ"))) != bstack1l1111_opy_ (u"ࠨ࠶࠳࠸ࠬᢏ"):
                break
        return bstack11l11lll1l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡧࡥࡹࡧࠧᢐ"), bstack11l11lll1l1_opy_)