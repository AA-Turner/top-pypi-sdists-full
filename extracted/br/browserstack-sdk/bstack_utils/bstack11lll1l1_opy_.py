# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1l111l1_opy_ import bstack11ll11lllll_opy_
from bstack_utils.constants import *
import json
class bstack1lll111ll_opy_:
    def __init__(self, bstack1l1ll11ll_opy_, bstack11ll11lll11_opy_):
        self.bstack1l1ll11ll_opy_ = bstack1l1ll11ll_opy_
        self.bstack11ll11lll11_opy_ = bstack11ll11lll11_opy_
        self.bstack11ll11ll1ll_opy_ = None
    def __call__(self):
        bstack11ll1l1111l_opy_ = {}
        while True:
            self.bstack11ll11ll1ll_opy_ = bstack11ll1l1111l_opy_.get(
                bstack1l1l1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᜇ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll1l11111_opy_ = self.bstack11ll11ll1ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll1l11111_opy_ > 0:
                sleep(bstack11ll1l11111_opy_ / 1000)
            params = {
                bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜈ"): self.bstack1l1ll11ll_opy_,
                bstack1l1l1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᜉ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11ll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᜊ") + bstack11ll11llll1_opy_ + bstack1l1l1l1_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤᜋ")
            if self.bstack11ll11lll11_opy_.lower() == bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢᜌ"):
                bstack11ll1l1111l_opy_ = bstack11ll11lllll_opy_.results(bstack11ll11ll1l1_opy_, params)
            else:
                bstack11ll1l1111l_opy_ = bstack11ll11lllll_opy_.bstack11ll11lll1l_opy_(bstack11ll11ll1l1_opy_, params)
            if str(bstack11ll1l1111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᜍ"), bstack1l1l1l1_opy_ (u"ࠨ࠴࠳࠴ࠬᜎ"))) != bstack1l1l1l1_opy_ (u"ࠩ࠷࠴࠹࠭ᜏ"):
                break
        return bstack11ll1l1111l_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᜐ"), bstack11ll1l1111l_opy_)