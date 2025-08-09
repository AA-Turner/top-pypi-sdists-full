# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import *
import json
class bstack1lll1l1lll_opy_:
    def __init__(self, bstack1llll1lll1_opy_, bstack11ll11l11l1_opy_):
        self.bstack1llll1lll1_opy_ = bstack1llll1lll1_opy_
        self.bstack11ll11l11l1_opy_ = bstack11ll11l11l1_opy_
        self.bstack11ll11l1lll_opy_ = None
    def __call__(self):
        bstack11ll11ll111_opy_ = {}
        while True:
            self.bstack11ll11l1lll_opy_ = bstack11ll11ll111_opy_.get(
                bstack11l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᝦ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11l1ll1_opy_ = self.bstack11ll11l1lll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11l1ll1_opy_ > 0:
                sleep(bstack11ll11l1ll1_opy_ / 1000)
            params = {
                bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᝧ"): self.bstack1llll1lll1_opy_,
                bstack11l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᝨ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l111l_opy_ = bstack11l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᝩ") + bstack11ll11l1l1l_opy_ + bstack11l1_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᝪ")
            if self.bstack11ll11l11l1_opy_.lower() == bstack11l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᝫ"):
                bstack11ll11ll111_opy_ = bstack11ll11l1111_opy_.results(bstack11ll11l111l_opy_, params)
            else:
                bstack11ll11ll111_opy_ = bstack11ll11l1111_opy_.bstack11ll11l11ll_opy_(bstack11ll11l111l_opy_, params)
            if str(bstack11ll11ll111_opy_.get(bstack11l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᝬ"), bstack11l1_opy_ (u"ࠬ࠸࠰࠱ࠩ᝭"))) != bstack11l1_opy_ (u"࠭࠴࠱࠶ࠪᝮ"):
                break
        return bstack11ll11ll111_opy_.get(bstack11l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᝯ"), bstack11ll11ll111_opy_)