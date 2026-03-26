# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111l1ll11ll_opy_ import bstack111l1ll11l1_opy_
from bstack_utils.constants import *
import json
class bstack11ll111lll_opy_:
    def __init__(self, bstack1lll1l1l1l_opy_, bstack111l1ll111l_opy_):
        self.bstack1lll1l1l1l_opy_ = bstack1lll1l1l1l_opy_
        self.bstack111l1ll111l_opy_ = bstack111l1ll111l_opy_
        self.bstack111l1ll1ll1_opy_ = None
    def __call__(self):
        bstack111l1ll1111_opy_ = {}
        while True:
            self.bstack111l1ll1ll1_opy_ = bstack111l1ll1111_opy_.get(
                bstack1ll1lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᮦ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111l1ll1l1l_opy_ = self.bstack111l1ll1ll1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111l1ll1l1l_opy_ > 0:
                sleep(bstack111l1ll1l1l_opy_ / 1000)
            params = {
                bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᮧ"): self.bstack1lll1l1l1l_opy_,
                bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᮨ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᮩ") + bstack111l1ll1lll_opy_ + bstack1ll1lll_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤ᮪")
            if self.bstack111l1ll111l_opy_.lower() == bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹ᮫ࠢ"):
                bstack111l1ll1111_opy_ = bstack111l1ll11l1_opy_.results(base_url, params)
            else:
                bstack111l1ll1111_opy_ = bstack111l1ll11l1_opy_.bstack111l1ll1l11_opy_(base_url, params)
            if str(bstack111l1ll1111_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᮬ"), bstack1ll1lll_opy_ (u"ࠨ࠴࠳࠴ࠬᮭ"))) != bstack1ll1lll_opy_ (u"ࠩ࠷࠴࠹࠭ᮮ"):
                break
        return bstack111l1ll1111_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᮯ"), bstack111l1ll1111_opy_)