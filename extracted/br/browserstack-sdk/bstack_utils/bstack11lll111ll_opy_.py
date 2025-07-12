# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l111l1l1l_opy_ import bstack11l111ll111_opy_
from bstack_utils.constants import *
import json
class bstack1lll1llll_opy_:
    def __init__(self, bstack1l1111111_opy_, bstack11l111ll1ll_opy_):
        self.bstack1l1111111_opy_ = bstack1l1111111_opy_
        self.bstack11l111ll1ll_opy_ = bstack11l111ll1ll_opy_
        self.bstack11l111ll11l_opy_ = None
    def __call__(self):
        bstack11l111ll1l1_opy_ = {}
        while True:
            self.bstack11l111ll11l_opy_ = bstack11l111ll1l1_opy_.get(
                bstack11l1111_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ᠝"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l111l1l11_opy_ = self.bstack11l111ll11l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l111l1l11_opy_ > 0:
                sleep(bstack11l111l1l11_opy_ / 1000)
            params = {
                bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᠞"): self.bstack1l1111111_opy_,
                bstack11l1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᠟"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l111l1lll_opy_ = bstack11l1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᠠ") + bstack11l111l1ll1_opy_ + bstack11l1111_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᠡ")
            if self.bstack11l111ll1ll_opy_.lower() == bstack11l1111_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᠢ"):
                bstack11l111ll1l1_opy_ = bstack11l111ll111_opy_.results(bstack11l111l1lll_opy_, params)
            else:
                bstack11l111ll1l1_opy_ = bstack11l111ll111_opy_.bstack11l111lll11_opy_(bstack11l111l1lll_opy_, params)
            if str(bstack11l111ll1l1_opy_.get(bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᠣ"), bstack11l1111_opy_ (u"࠭࠲࠱࠲ࠪᠤ"))) != bstack11l1111_opy_ (u"ࠧ࠵࠲࠷ࠫᠥ"):
                break
        return bstack11l111ll1l1_opy_.get(bstack11l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᠦ"), bstack11l111ll1l1_opy_)