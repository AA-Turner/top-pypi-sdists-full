# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11l1lll_opy_ import bstack11ll11ll11l_opy_
from bstack_utils.constants import *
import json
class bstack11ll11l111_opy_:
    def __init__(self, bstack1l11l11l1_opy_, bstack11ll11ll111_opy_):
        self.bstack1l11l11l1_opy_ = bstack1l11l11l1_opy_
        self.bstack11ll11ll111_opy_ = bstack11ll11ll111_opy_
        self.bstack11ll11l1ll1_opy_ = None
    def __call__(self):
        bstack11ll11l1l11_opy_ = {}
        while True:
            self.bstack11ll11l1ll1_opy_ = bstack11ll11l1l11_opy_.get(
                bstack1l1ll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᜧ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11lll11_opy_ = self.bstack11ll11l1ll1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11lll11_opy_ > 0:
                sleep(bstack11ll11lll11_opy_ / 1000)
            params = {
                bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜨ"): self.bstack1l11l11l1_opy_,
                bstack1l1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᜩ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l1l1l_opy_ = bstack1l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᜪ") + bstack11ll11ll1ll_opy_ + bstack1l1ll1_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᜫ")
            if self.bstack11ll11ll111_opy_.lower() == bstack1l1ll1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᜬ"):
                bstack11ll11l1l11_opy_ = bstack11ll11ll11l_opy_.results(bstack11ll11l1l1l_opy_, params)
            else:
                bstack11ll11l1l11_opy_ = bstack11ll11ll11l_opy_.bstack11ll11ll1l1_opy_(bstack11ll11l1l1l_opy_, params)
            if str(bstack11ll11l1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᜭ"), bstack1l1ll1_opy_ (u"ࠬ࠸࠰࠱ࠩᜮ"))) != bstack1l1ll1_opy_ (u"࠭࠴࠱࠶ࠪᜯ"):
                break
        return bstack11ll11l1l11_opy_.get(bstack1l1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬᜰ"), bstack11ll11l1l11_opy_)