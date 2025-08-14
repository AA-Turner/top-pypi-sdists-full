# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11l1ll1_opy_ import bstack11ll11l1l1l_opy_
from bstack_utils.constants import *
import json
class bstack111111111_opy_:
    def __init__(self, bstack1llllllll1_opy_, bstack11ll11l11ll_opy_):
        self.bstack1llllllll1_opy_ = bstack1llllllll1_opy_
        self.bstack11ll11l11ll_opy_ = bstack11ll11l11ll_opy_
        self.bstack11ll11l11l1_opy_ = None
    def __call__(self):
        bstack11ll11l1111_opy_ = {}
        while True:
            self.bstack11ll11l11l1_opy_ = bstack11ll11l1111_opy_.get(
                bstack1l1l1ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᝬ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll111llll_opy_ = self.bstack11ll11l11l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll111llll_opy_ > 0:
                sleep(bstack11ll111llll_opy_ / 1000)
            params = {
                bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᝭"): self.bstack1llllllll1_opy_,
                bstack1l1l1ll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᝮ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll111lll1_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᝯ") + bstack11ll11l1l11_opy_ + bstack1l1l1ll_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᝰ")
            if self.bstack11ll11l11ll_opy_.lower() == bstack1l1l1ll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥ᝱"):
                bstack11ll11l1111_opy_ = bstack11ll11l1l1l_opy_.results(bstack11ll111lll1_opy_, params)
            else:
                bstack11ll11l1111_opy_ = bstack11ll11l1l1l_opy_.bstack11ll11l111l_opy_(bstack11ll111lll1_opy_, params)
            if str(bstack11ll11l1111_opy_.get(bstack1l1l1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝲ"), bstack1l1l1ll_opy_ (u"ࠫ࠷࠶࠰ࠨᝳ"))) != bstack1l1l1ll_opy_ (u"ࠬ࠺࠰࠵ࠩ᝴"):
                break
        return bstack11ll11l1111_opy_.get(bstack1l1l1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ᝵"), bstack11ll11l1111_opy_)