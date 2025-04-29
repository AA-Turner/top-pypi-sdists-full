# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1l11l1_opy_ import bstack11lll1l111l_opy_
from bstack_utils.constants import *
import json
class bstack1llllll11_opy_:
    def __init__(self, bstack1lll1l1111_opy_, bstack11lll11lll1_opy_):
        self.bstack1lll1l1111_opy_ = bstack1lll1l1111_opy_
        self.bstack11lll11lll1_opy_ = bstack11lll11lll1_opy_
        self.bstack11lll11ll11_opy_ = None
    def __call__(self):
        bstack11lll1l1l11_opy_ = {}
        while True:
            self.bstack11lll11ll11_opy_ = bstack11lll1l1l11_opy_.get(
                bstack1llllll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᙒ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll11llll_opy_ = self.bstack11lll11ll11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll11llll_opy_ > 0:
                sleep(bstack11lll11llll_opy_ / 1000)
            params = {
                bstack1llllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᙓ"): self.bstack1lll1l1111_opy_,
                bstack1llllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᙔ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l11ll_opy_ = bstack1llllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᙕ") + bstack11lll1l1111_opy_ + bstack1llllll_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᙖ")
            if self.bstack11lll11lll1_opy_.lower() == bstack1llllll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᙗ"):
                bstack11lll1l1l11_opy_ = bstack11lll1l111l_opy_.results(bstack11lll1l11ll_opy_, params)
            else:
                bstack11lll1l1l11_opy_ = bstack11lll1l111l_opy_.bstack11lll11ll1l_opy_(bstack11lll1l11ll_opy_, params)
            if str(bstack11lll1l1l11_opy_.get(bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙘ"), bstack1llllll_opy_ (u"ࠩ࠵࠴࠵࠭ᙙ"))) != bstack1llllll_opy_ (u"ࠪ࠸࠵࠺ࠧᙚ"):
                break
        return bstack11lll1l1l11_opy_.get(bstack1llllll_opy_ (u"ࠫࡩࡧࡴࡢࠩᙛ"), bstack11lll1l1l11_opy_)