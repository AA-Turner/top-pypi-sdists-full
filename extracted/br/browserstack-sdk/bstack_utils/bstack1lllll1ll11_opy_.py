# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l111l11_opy_ import bstack1111l111l1l_opy_
from bstack_utils.constants import *
import json
class bstack1llllllllll_opy_:
    def __init__(self, bstack111l1ll11_opy_, bstack1111l1111ll_opy_):
        self.bstack111l1ll11_opy_ = bstack111l1ll11_opy_
        self.bstack1111l1111ll_opy_ = bstack1111l1111ll_opy_
        self.bstack1111l1111l1_opy_ = None
    def __call__(self):
        bstack1111l11111l_opy_ = {}
        while True:
            self.bstack1111l1111l1_opy_ = bstack1111l11111l_opy_.get(
                bstack1l111l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᶣ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11111llllll_opy_ = self.bstack1111l1111l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11111llllll_opy_ > 0:
                sleep(bstack11111llllll_opy_ / 1000)
            params = {
                bstack1l111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶤ"): self.bstack111l1ll11_opy_,
                bstack1l111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᶥ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1l111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᶦ") + bstack1111l111111_opy_ + bstack1l111l_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᶧ")
            if self.bstack1111l1111ll_opy_.lower() == bstack1l111l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᶨ"):
                bstack1111l11111l_opy_ = bstack1111l111l1l_opy_.results(base_url, params)
            else:
                bstack1111l11111l_opy_ = bstack1111l111l1l_opy_.bstack1111l111ll1_opy_(base_url, params)
            if str(bstack1111l11111l_opy_.get(bstack1l111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶩ"), bstack1l111l_opy_ (u"࠭࠲࠱࠲ࠪᶪ"))) != bstack1l111l_opy_ (u"ࠧ࠵࠲࠷ࠫᶫ"):
                break
        return bstack1111l11111l_opy_.get(bstack1l111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᶬ"), bstack1111l11111l_opy_)