# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l11ll11l1_opy_ import bstack11l11ll1l11_opy_
from bstack_utils.constants import *
import json
class bstack11l11l1lll_opy_:
    def __init__(self, bstack1l1l11l111_opy_, bstack11l11l1lll1_opy_):
        self.bstack1l1l11l111_opy_ = bstack1l1l11l111_opy_
        self.bstack11l11l1lll1_opy_ = bstack11l11l1lll1_opy_
        self.bstack11l11ll1111_opy_ = None
    def __call__(self):
        bstack11l11ll111l_opy_ = {}
        while True:
            self.bstack11l11ll1111_opy_ = bstack11l11ll111l_opy_.get(
                bstack11lllll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ᢭"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l11l1ll1l_opy_ = self.bstack11l11ll1111_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l11l1ll1l_opy_ > 0:
                sleep(bstack11l11l1ll1l_opy_ / 1000)
            params = {
                bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᢮"): self.bstack1l1l11l111_opy_,
                bstack11lllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᢯"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l11l1llll_opy_ = bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᢰ") + bstack11l11ll11ll_opy_ + bstack11lllll_opy_ (u"ࠢ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࠦᢱ")
            if self.bstack11l11l1lll1_opy_.lower() == bstack11lllll_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤᢲ"):
                bstack11l11ll111l_opy_ = bstack11l11ll1l11_opy_.results(bstack11l11l1llll_opy_, params)
            else:
                bstack11l11ll111l_opy_ = bstack11l11ll1l11_opy_.bstack11l11ll1l1l_opy_(bstack11l11l1llll_opy_, params)
            if str(bstack11l11ll111l_opy_.get(bstack11lllll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᢳ"), bstack11lllll_opy_ (u"ࠪ࠶࠵࠶ࠧᢴ"))) != bstack11lllll_opy_ (u"ࠫ࠹࠶࠴ࠨᢵ"):
                break
        return bstack11l11ll111l_opy_.get(bstack11lllll_opy_ (u"ࠬࡪࡡࡵࡣࠪᢶ"), bstack11l11ll111l_opy_)