# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111ll1l1ll1_opy_ import bstack111ll1ll1ll_opy_
from bstack_utils.constants import *
import json
class bstack1l11lll1_opy_:
    def __init__(self, bstack111lll1111_opy_, bstack111ll1l1l1l_opy_):
        self.bstack111lll1111_opy_ = bstack111lll1111_opy_
        self.bstack111ll1l1l1l_opy_ = bstack111ll1l1l1l_opy_
        self.bstack111ll1ll11l_opy_ = None
    def __call__(self):
        bstack111ll1l1lll_opy_ = {}
        while True:
            self.bstack111ll1ll11l_opy_ = bstack111ll1l1lll_opy_.get(
                bstack1111l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᬾ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111ll1ll1l1_opy_ = self.bstack111ll1ll11l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111ll1ll1l1_opy_ > 0:
                sleep(bstack111ll1ll1l1_opy_ / 1000)
            params = {
                bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᬿ"): self.bstack111lll1111_opy_,
                bstack1111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᭀ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1111l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᭁ") + bstack111ll1ll111_opy_ + bstack1111l_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᭂ")
            if self.bstack111ll1l1l1l_opy_.lower() == bstack1111l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᭃ"):
                bstack111ll1l1lll_opy_ = bstack111ll1ll1ll_opy_.results(base_url, params)
            else:
                bstack111ll1l1lll_opy_ = bstack111ll1ll1ll_opy_.bstack111ll1lll11_opy_(base_url, params)
            if str(bstack111ll1l1lll_opy_.get(bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᭄"), bstack1111l_opy_ (u"ࠩ࠵࠴࠵࠭ᭅ"))) != bstack1111l_opy_ (u"ࠪ࠸࠵࠺ࠧᭆ"):
                break
        return bstack111ll1l1lll_opy_.get(bstack1111l_opy_ (u"ࠫࡩࡧࡴࡢࠩᭇ"), bstack111ll1l1lll_opy_)