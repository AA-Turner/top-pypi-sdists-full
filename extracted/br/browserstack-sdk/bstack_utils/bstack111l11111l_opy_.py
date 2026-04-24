# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack1111l111l1l_opy_ import bstack1111l1111ll_opy_
from bstack_utils.constants import *
import json
class bstack1ll111l11l_opy_:
    def __init__(self, bstack1lllllll11_opy_, bstack1111l111111_opy_):
        self.bstack1lllllll11_opy_ = bstack1lllllll11_opy_
        self.bstack1111l111111_opy_ = bstack1111l111111_opy_
        self.bstack1111l11111l_opy_ = None
    def __call__(self):
        bstack11111llllll_opy_ = {}
        while True:
            self.bstack1111l11111l_opy_ = bstack11111llllll_opy_.get(
                bstack111ll11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᶣ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack1111l1111l1_opy_ = self.bstack1111l11111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack1111l1111l1_opy_ > 0:
                sleep(bstack1111l1111l1_opy_ / 1000)
            params = {
                bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶤ"): self.bstack1lllllll11_opy_,
                bstack111ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᶥ"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack111ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᶦ") + bstack1111l111l11_opy_ + bstack111ll11_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᶧ")
            if self.bstack1111l111111_opy_.lower() == bstack111ll11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᶨ"):
                bstack11111llllll_opy_ = bstack1111l1111ll_opy_.results(base_url, params)
            else:
                bstack11111llllll_opy_ = bstack1111l1111ll_opy_.bstack1111l111ll1_opy_(base_url, params)
            if str(bstack11111llllll_opy_.get(bstack111ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᶩ"), bstack111ll11_opy_ (u"࠭࠲࠱࠲ࠪᶪ"))) != bstack111ll11_opy_ (u"ࠧ࠵࠲࠷ࠫᶫ"):
                break
        return bstack11111llllll_opy_.get(bstack111ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᶬ"), bstack11111llllll_opy_)