# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l111ll1_opy_ import bstack1111l111l1l_opy_
from bstack_utils.constants import *
import json
class bstack11lll1l111_opy_:
    def __init__(self, bstack11ll11l1ll_opy_, bstack1111l11l111_opy_):
        self.bstack11ll11l1ll_opy_ = bstack11ll11l1ll_opy_
        self.bstack1111l11l111_opy_ = bstack1111l11l111_opy_
        self.bstack1111l1111l1_opy_ = None
    def __call__(self):
        bstack1111l1111ll_opy_ = {}
        while True:
            self.bstack1111l1111l1_opy_ = bstack1111l1111ll_opy_.get(
                bstack1ll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᶊ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l111l11_opy_ = self.bstack1111l1111l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l111l11_opy_ > 0:
                sleep(bstack1111l111l11_opy_ / 1000)
            params = {
                bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶋ"): self.bstack11ll11l1ll_opy_,
                bstack1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᶌ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᶍ") + bstack1111l11111l_opy_ + bstack1ll_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᶎ")
            if self.bstack1111l11l111_opy_.lower() == bstack1ll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᶏ"):
                bstack1111l1111ll_opy_ = bstack1111l111l1l_opy_.results(base_url, params)
            else:
                bstack1111l1111ll_opy_ = bstack1111l111l1l_opy_.bstack1111l111lll_opy_(base_url, params)
            if str(bstack1111l1111ll_opy_.get(bstack1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᶐ"), bstack1ll_opy_ (u"ࠩ࠵࠴࠵࠭ᶑ"))) != bstack1ll_opy_ (u"ࠪ࠸࠵࠺ࠧᶒ"):
                break
        return bstack1111l1111ll_opy_.get(bstack1ll_opy_ (u"ࠫࡩࡧࡴࡢࠩᶓ"), bstack1111l1111ll_opy_)