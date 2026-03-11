# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11111l11l11_opy_ import bstack111111ll111_opy_
from bstack_utils.constants import *
import json
class bstack111l1l11l1_opy_:
    def __init__(self, bstack11ll11ll1_opy_, bstack1ll1llll11l1_opy_):
        self.bstack11ll11ll1_opy_ = bstack11ll11ll1_opy_
        self.bstack1ll1llll11l1_opy_ = bstack1ll1llll11l1_opy_
        self.bstack1ll1lll1llll_opy_ = None
    def __call__(self):
        bstack1ll1llll11ll_opy_ = {}
        while True:
            self.bstack1ll1lll1llll_opy_ = bstack1ll1llll11ll_opy_.get(
                bstack1ll111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ≓"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1ll1llll111l_opy_ = self.bstack1ll1lll1llll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1ll1llll111l_opy_ > 0:
                sleep(bstack1ll1llll111l_opy_ / 1000)
            params = {
                bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ≔"): self.bstack11ll11ll1_opy_,
                bstack1ll111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ≕"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ≖") + bstack1ll1llll1111_opy_ + bstack1ll111_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥ≗")
            if self.bstack1ll1llll11l1_opy_.lower() == bstack1ll111_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣ≘"):
                bstack1ll1llll11ll_opy_ = bstack111111ll111_opy_.results(base_url, params)
            else:
                bstack1ll1llll11ll_opy_ = bstack111111ll111_opy_.bstack1lll1lll1lll_opy_(base_url, params)
            if str(bstack1ll1llll11ll_opy_.get(bstack1ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ≙"), bstack1ll111_opy_ (u"ࠩ࠵࠴࠵࠭≚"))) != bstack1ll111_opy_ (u"ࠪ࠸࠵࠺ࠧ≛"):
                break
        return bstack1ll1llll11ll_opy_.get(bstack1ll111_opy_ (u"ࠫࡩࡧࡴࡢࠩ≜"), bstack1ll1llll11ll_opy_)