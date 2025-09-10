# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll1111l11_opy_ import bstack11ll11111l1_opy_
from bstack_utils.constants import *
import json
class bstack11ll11lll1_opy_:
    def __init__(self, bstack1lllllllll_opy_, bstack11l1llllll1_opy_):
        self.bstack1lllllllll_opy_ = bstack1lllllllll_opy_
        self.bstack11l1llllll1_opy_ = bstack11l1llllll1_opy_
        self.bstack11ll1111l1l_opy_ = None
    def __call__(self):
        bstack11ll1111111_opy_ = {}
        while True:
            self.bstack11ll1111l1l_opy_ = bstack11ll1111111_opy_.get(
                bstack1ll11ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ᝵"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11111ll_opy_ = self.bstack11ll1111l1l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11111ll_opy_ > 0:
                sleep(bstack11ll11111ll_opy_ / 1000)
            params = {
                bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᝶"): self.bstack1lllllllll_opy_,
                bstack1ll11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᝷"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l1lllll1l_opy_ = bstack1ll11ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᝸") + bstack11ll111111l_opy_ + bstack1ll11ll_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢ᝹")
            if self.bstack11l1llllll1_opy_.lower() == bstack1ll11ll_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧ᝺"):
                bstack11ll1111111_opy_ = bstack11ll11111l1_opy_.results(bstack11l1lllll1l_opy_, params)
            else:
                bstack11ll1111111_opy_ = bstack11ll11111l1_opy_.bstack11l1lllllll_opy_(bstack11l1lllll1l_opy_, params)
            if str(bstack11ll1111111_opy_.get(bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᝻"), bstack1ll11ll_opy_ (u"࠭࠲࠱࠲ࠪ᝼"))) != bstack1ll11ll_opy_ (u"ࠧ࠵࠲࠷ࠫ᝽"):
                break
        return bstack11ll1111111_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭᝾"), bstack11ll1111111_opy_)