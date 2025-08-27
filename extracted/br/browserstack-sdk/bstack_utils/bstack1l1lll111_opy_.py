# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll11l1ll1_opy_
from bstack_utils.constants import *
import json
class bstack1l11l111_opy_:
    def __init__(self, bstack11ll1111_opy_, bstack11ll11l1111_opy_):
        self.bstack11ll1111_opy_ = bstack11ll1111_opy_
        self.bstack11ll11l1111_opy_ = bstack11ll11l1111_opy_
        self.bstack11ll11l1l1l_opy_ = None
    def __call__(self):
        bstack11ll11l11l1_opy_ = {}
        while True:
            self.bstack11ll11l1l1l_opy_ = bstack11ll11l11l1_opy_.get(
                bstack1111lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᝬ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11l11ll_opy_ = self.bstack11ll11l1l1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11l11ll_opy_ > 0:
                sleep(bstack11ll11l11ll_opy_ / 1000)
            params = {
                bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝭"): self.bstack11ll1111_opy_,
                bstack1111lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᝮ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l111l_opy_ = bstack1111lll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᝯ") + bstack11ll11l1l11_opy_ + bstack1111lll_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᝰ")
            if self.bstack11ll11l1111_opy_.lower() == bstack1111lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥ᝱"):
                bstack11ll11l11l1_opy_ = bstack11ll11l1ll1_opy_.results(bstack11ll11l111l_opy_, params)
            else:
                bstack11ll11l11l1_opy_ = bstack11ll11l1ll1_opy_.bstack11ll111lll1_opy_(bstack11ll11l111l_opy_, params)
            if str(bstack11ll11l11l1_opy_.get(bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝲ"), bstack1111lll_opy_ (u"ࠫ࠷࠶࠰ࠨᝳ"))) != bstack1111lll_opy_ (u"ࠬ࠺࠰࠵ࠩ᝴"):
                break
        return bstack11ll11l11l1_opy_.get(bstack1111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫ᝵"), bstack11ll11l11l1_opy_)