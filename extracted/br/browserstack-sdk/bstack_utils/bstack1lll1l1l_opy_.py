# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111llll11l1_opy_ import bstack111lll1ll1l_opy_
from bstack_utils.constants import *
import json
class bstack11111l111_opy_:
    def __init__(self, bstack1ll11lllll_opy_, bstack111lll1l1ll_opy_):
        self.bstack1ll11lllll_opy_ = bstack1ll11lllll_opy_
        self.bstack111lll1l1ll_opy_ = bstack111lll1l1ll_opy_
        self.bstack111llll111l_opy_ = None
    def __call__(self):
        bstack111lll1ll11_opy_ = {}
        while True:
            self.bstack111llll111l_opy_ = bstack111lll1ll11_opy_.get(
                bstack1lll1l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ᪈"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111lll1l1l1_opy_ = self.bstack111llll111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111lll1l1l1_opy_ > 0:
                sleep(bstack111lll1l1l1_opy_ / 1000)
            params = {
                bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᪉"): self.bstack1ll11lllll_opy_,
                bstack1lll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ᪊"): int(datetime.now().timestamp() * 1000)
            }
            bstack111lll1lll1_opy_ = bstack1lll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᪋") + bstack111llll1111_opy_ + bstack1lll1l_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥ᪌")
            if self.bstack111lll1l1ll_opy_.lower() == bstack1lll1l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣ᪍"):
                bstack111lll1ll11_opy_ = bstack111lll1ll1l_opy_.results(bstack111lll1lll1_opy_, params)
            else:
                bstack111lll1ll11_opy_ = bstack111lll1ll1l_opy_.bstack111lll1llll_opy_(bstack111lll1lll1_opy_, params)
            if str(bstack111lll1ll11_opy_.get(bstack1lll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᪎"), bstack1lll1l_opy_ (u"ࠩ࠵࠴࠵࠭᪏"))) != bstack1lll1l_opy_ (u"ࠪ࠸࠵࠺ࠧ᪐"):
                break
        return bstack111lll1ll11_opy_.get(bstack1lll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ᪑"), bstack111lll1ll11_opy_)