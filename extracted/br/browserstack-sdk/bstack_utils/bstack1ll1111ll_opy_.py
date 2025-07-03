# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11l11l1_opy_ import bstack11ll11l1l1l_opy_
from bstack_utils.constants import *
import json
class bstack1l11lll1ll_opy_:
    def __init__(self, bstack1l1111ll11_opy_, bstack11ll11l1l11_opy_):
        self.bstack1l1111ll11_opy_ = bstack1l1111ll11_opy_
        self.bstack11ll11l1l11_opy_ = bstack11ll11l1l11_opy_
        self.bstack11ll11l111l_opy_ = None
    def __call__(self):
        bstack11ll11l11ll_opy_ = {}
        while True:
            self.bstack11ll11l111l_opy_ = bstack11ll11l11ll_opy_.get(
                bstack1l1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ᝞"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11l1lll_opy_ = self.bstack11ll11l111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11l1lll_opy_ > 0:
                sleep(bstack11ll11l1lll_opy_ / 1000)
            params = {
                bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝟"): self.bstack1l1111ll11_opy_,
                bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᝠ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l1111_opy_ = bstack1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᝡ") + bstack11ll11l1ll1_opy_ + bstack1l1_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᝢ")
            if self.bstack11ll11l1l11_opy_.lower() == bstack1l1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᝣ"):
                bstack11ll11l11ll_opy_ = bstack11ll11l1l1l_opy_.results(bstack11ll11l1111_opy_, params)
            else:
                bstack11ll11l11ll_opy_ = bstack11ll11l1l1l_opy_.bstack11ll111llll_opy_(bstack11ll11l1111_opy_, params)
            if str(bstack11ll11l11ll_opy_.get(bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝤ"), bstack1l1_opy_ (u"ࠫ࠷࠶࠰ࠨᝥ"))) != bstack1l1_opy_ (u"ࠬ࠺࠰࠵ࠩᝦ"):
                break
        return bstack11ll11l11ll_opy_.get(bstack1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᝧ"), bstack11ll11l11ll_opy_)