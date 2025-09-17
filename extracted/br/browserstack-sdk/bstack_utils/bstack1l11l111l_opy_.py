# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll111ll1l_opy_ import bstack11ll111l1ll_opy_
from bstack_utils.constants import *
import json
class bstack11lll111l1_opy_:
    def __init__(self, bstack111ll11l_opy_, bstack11ll11l1111_opy_):
        self.bstack111ll11l_opy_ = bstack111ll11l_opy_
        self.bstack11ll11l1111_opy_ = bstack11ll11l1111_opy_
        self.bstack11ll111l11l_opy_ = None
    def __call__(self):
        bstack11ll111ll11_opy_ = {}
        while True:
            self.bstack11ll111l11l_opy_ = bstack11ll111ll11_opy_.get(
                bstack1l11ll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᝯ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll111l111_opy_ = self.bstack11ll111l11l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll111l111_opy_ > 0:
                sleep(bstack11ll111l111_opy_ / 1000)
            params = {
                bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᝰ"): self.bstack111ll11l_opy_,
                bstack1l11ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ᝱"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll111l1l1_opy_ = bstack1l11ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᝲ") + bstack11ll111llll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡢࡲ࡬࠳ࡻ࠷࠯ࠣᝳ")
            if self.bstack11ll11l1111_opy_.lower() == bstack1l11ll1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࡸࠨ᝴"):
                bstack11ll111ll11_opy_ = bstack11ll111l1ll_opy_.results(bstack11ll111l1l1_opy_, params)
            else:
                bstack11ll111ll11_opy_ = bstack11ll111l1ll_opy_.bstack11ll111lll1_opy_(bstack11ll111l1l1_opy_, params)
            if str(bstack11ll111ll11_opy_.get(bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᝵"), bstack1l11ll1_opy_ (u"ࠧ࠳࠲࠳ࠫ᝶"))) != bstack1l11ll1_opy_ (u"ࠨ࠶࠳࠸ࠬ᝷"):
                break
        return bstack11ll111ll11_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧ᝸"), bstack11ll111ll11_opy_)