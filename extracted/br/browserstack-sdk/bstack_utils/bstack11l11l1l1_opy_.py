# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll11l1l11_opy_ import bstack11ll11l11ll_opy_
from bstack_utils.constants import *
import json
class bstack1ll111lll_opy_:
    def __init__(self, bstack1ll1l1ll1_opy_, bstack11ll111ll11_opy_):
        self.bstack1ll1l1ll1_opy_ = bstack1ll1l1ll1_opy_
        self.bstack11ll111ll11_opy_ = bstack11ll111ll11_opy_
        self.bstack11ll111lll1_opy_ = None
    def __call__(self):
        bstack11ll11l111l_opy_ = {}
        while True:
            self.bstack11ll111lll1_opy_ = bstack11ll11l111l_opy_.get(
                bstackl_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᝥ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11l11l1_opy_ = self.bstack11ll111lll1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11l11l1_opy_ > 0:
                sleep(bstack11ll11l11l1_opy_ / 1000)
            params = {
                bstackl_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᝦ"): self.bstack1ll1l1ll1_opy_,
                bstackl_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᝧ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll111llll_opy_ = bstackl_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᝨ") + bstack11ll11l1111_opy_ + bstackl_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᝩ")
            if self.bstack11ll111ll11_opy_.lower() == bstackl_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᝪ"):
                bstack11ll11l111l_opy_ = bstack11ll11l11ll_opy_.results(bstack11ll111llll_opy_, params)
            else:
                bstack11ll11l111l_opy_ = bstack11ll11l11ll_opy_.bstack11ll111ll1l_opy_(bstack11ll111llll_opy_, params)
            if str(bstack11ll11l111l_opy_.get(bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝫ"), bstackl_opy_ (u"ࠫ࠷࠶࠰ࠨᝬ"))) != bstackl_opy_ (u"ࠬ࠺࠰࠵ࠩ᝭"):
                break
        return bstack11ll11l111l_opy_.get(bstackl_opy_ (u"࠭ࡤࡢࡶࡤࠫᝮ"), bstack11ll11l111l_opy_)