# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l11ll1l1l_opy_ import bstack11l11lll1l1_opy_
from bstack_utils.constants import *
import json
class bstack11l11111l_opy_:
    def __init__(self, bstack111lllll1l_opy_, bstack11l11ll1l11_opy_):
        self.bstack111lllll1l_opy_ = bstack111lllll1l_opy_
        self.bstack11l11ll1l11_opy_ = bstack11l11ll1l11_opy_
        self.bstack11l11ll1lll_opy_ = None
    def __call__(self):
        bstack11l11ll1ll1_opy_ = {}
        while True:
            self.bstack11l11ll1lll_opy_ = bstack11l11ll1ll1_opy_.get(
                bstack11l1ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᢍ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l11llll11_opy_ = self.bstack11l11ll1lll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l11llll11_opy_ > 0:
                sleep(bstack11l11llll11_opy_ / 1000)
            params = {
                bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᢎ"): self.bstack111lllll1l_opy_,
                bstack11l1ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᢏ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l11lll11l_opy_ = bstack11l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᢐ") + bstack11l11lll1ll_opy_ + bstack11l1ll1_opy_ (u"ࠥ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡡࡱ࡫࠲ࡺ࠶࠵ࠢᢑ")
            if self.bstack11l11ll1l11_opy_.lower() == bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࡷࠧᢒ"):
                bstack11l11ll1ll1_opy_ = bstack11l11lll1l1_opy_.results(bstack11l11lll11l_opy_, params)
            else:
                bstack11l11ll1ll1_opy_ = bstack11l11lll1l1_opy_.bstack11l11lll111_opy_(bstack11l11lll11l_opy_, params)
            if str(bstack11l11ll1ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᢓ"), bstack11l1ll1_opy_ (u"࠭࠲࠱࠲ࠪᢔ"))) != bstack11l1ll1_opy_ (u"ࠧ࠵࠲࠷ࠫᢕ"):
                break
        return bstack11l11ll1ll1_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᢖ"), bstack11l11ll1ll1_opy_)