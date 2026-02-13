# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111llllll1l_opy_ import bstack111lllll1ll_opy_
from bstack_utils.constants import *
import json
class bstack1lll1l1ll1_opy_:
    def __init__(self, bstack1ll1l1111l_opy_, bstack11l1111111l_opy_):
        self.bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_
        self.bstack11l1111111l_opy_ = bstack11l1111111l_opy_
        self.bstack111lllllll1_opy_ = None
    def __call__(self):
        bstack111llllll11_opy_ = {}
        while True:
            self.bstack111lllllll1_opy_ = bstack111llllll11_opy_.get(
                bstack11l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᥗ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l111111l1_opy_ = self.bstack111lllllll1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l111111l1_opy_ > 0:
                sleep(bstack11l111111l1_opy_ / 1000)
            params = {
                bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᥘ"): self.bstack1ll1l1111l_opy_,
                bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᥙ"): int(datetime.now().timestamp() * 1000)
            }
            bstack111lllll1l1_opy_ = bstack11l11_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᥚ") + bstack11l11111111_opy_ + bstack11l11_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᥛ")
            if self.bstack11l1111111l_opy_.lower() == bstack11l11_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᥜ"):
                bstack111llllll11_opy_ = bstack111lllll1ll_opy_.results(bstack111lllll1l1_opy_, params)
            else:
                bstack111llllll11_opy_ = bstack111lllll1ll_opy_.bstack111llllllll_opy_(bstack111lllll1l1_opy_, params)
            if str(bstack111llllll11_opy_.get(bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᥝ"), bstack11l11_opy_ (u"ࠬ࠸࠰࠱ࠩᥞ"))) != bstack11l11_opy_ (u"࠭࠴࠱࠶ࠪᥟ"):
                break
        return bstack111llllll11_opy_.get(bstack11l11_opy_ (u"ࠧࡥࡣࡷࡥࠬᥠ"), bstack111llllll11_opy_)