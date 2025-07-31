# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll111l1ll_opy_ import bstack11ll11l111l_opy_
from bstack_utils.constants import *
import json
class bstack1lll11l1ll_opy_:
    def __init__(self, bstack11l1ll11l_opy_, bstack11ll111lll1_opy_):
        self.bstack11l1ll11l_opy_ = bstack11l1ll11l_opy_
        self.bstack11ll111lll1_opy_ = bstack11ll111lll1_opy_
        self.bstack11ll111ll11_opy_ = None
    def __call__(self):
        bstack11ll111ll1l_opy_ = {}
        while True:
            self.bstack11ll111ll11_opy_ = bstack11ll111ll1l_opy_.get(
                bstack1l11l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᝥ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll111llll_opy_ = self.bstack11ll111ll11_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll111llll_opy_ > 0:
                sleep(bstack11ll111llll_opy_ / 1000)
            params = {
                bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᝦ"): self.bstack11l1ll11l_opy_,
                bstack1l11l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᝧ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l1111_opy_ = bstack1l11l11_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᝨ") + bstack11ll11l11l1_opy_ + bstack1l11l11_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᝩ")
            if self.bstack11ll111lll1_opy_.lower() == bstack1l11l11_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᝪ"):
                bstack11ll111ll1l_opy_ = bstack11ll11l111l_opy_.results(bstack11ll11l1111_opy_, params)
            else:
                bstack11ll111ll1l_opy_ = bstack11ll11l111l_opy_.bstack11ll11l11ll_opy_(bstack11ll11l1111_opy_, params)
            if str(bstack11ll111ll1l_opy_.get(bstack1l11l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᝫ"), bstack1l11l11_opy_ (u"ࠫ࠷࠶࠰ࠨᝬ"))) != bstack1l11l11_opy_ (u"ࠬ࠺࠰࠵ࠩ᝭"):
                break
        return bstack11ll111ll1l_opy_.get(bstack1l11l11_opy_ (u"࠭ࡤࡢࡶࡤࠫᝮ"), bstack11ll111ll1l_opy_)