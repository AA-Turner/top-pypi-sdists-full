# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111lll1l11l_opy_ import bstack111lll1lll1_opy_
from bstack_utils.constants import *
import json
class bstack11lllll1l1_opy_:
    def __init__(self, bstack1ll111ll1l_opy_, bstack111lll1ll11_opy_):
        self.bstack1ll111ll1l_opy_ = bstack1ll111ll1l_opy_
        self.bstack111lll1ll11_opy_ = bstack111lll1ll11_opy_
        self.bstack111lll1l1ll_opy_ = None
    def __call__(self):
        bstack111lll1l1l1_opy_ = {}
        while True:
            self.bstack111lll1l1ll_opy_ = bstack111lll1l1l1_opy_.get(
                bstack1111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ᪉"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack111llll1111_opy_ = self.bstack111lll1l1ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack111llll1111_opy_ > 0:
                sleep(bstack111llll1111_opy_ / 1000)
            params = {
                bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᪊"): self.bstack1ll111ll1l_opy_,
                bstack1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᪋"): int(datetime.now().timestamp() * 1000)
            }
            bstack111lll1ll1l_opy_ = bstack1111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ᪌") + bstack111lll1l111_opy_ + bstack1111_opy_ (u"ࠢ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࠦ᪍")
            if self.bstack111lll1ll11_opy_.lower() == bstack1111_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤ᪎"):
                bstack111lll1l1l1_opy_ = bstack111lll1lll1_opy_.results(bstack111lll1ll1l_opy_, params)
            else:
                bstack111lll1l1l1_opy_ = bstack111lll1lll1_opy_.bstack111lll1llll_opy_(bstack111lll1ll1l_opy_, params)
            if str(bstack111lll1l1l1_opy_.get(bstack1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᪏"), bstack1111_opy_ (u"ࠪ࠶࠵࠶ࠧ᪐"))) != bstack1111_opy_ (u"ࠫ࠹࠶࠴ࠨ᪑"):
                break
        return bstack111lll1l1l1_opy_.get(bstack1111_opy_ (u"ࠬࡪࡡࡵࡣࠪ᪒"), bstack111lll1l1l1_opy_)