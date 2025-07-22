# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll111llll_opy_ import bstack11ll111lll1_opy_
from bstack_utils.constants import *
import json
class bstack11111llll_opy_:
    def __init__(self, bstack1l111111l1_opy_, bstack11ll111ll11_opy_):
        self.bstack1l111111l1_opy_ = bstack1l111111l1_opy_
        self.bstack11ll111ll11_opy_ = bstack11ll111ll11_opy_
        self.bstack11ll11l11l1_opy_ = None
    def __call__(self):
        bstack11ll11l111l_opy_ = {}
        while True:
            self.bstack11ll11l11l1_opy_ = bstack11ll11l111l_opy_.get(
                bstack111l111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᝩ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll11l1111_opy_ = self.bstack11ll11l11l1_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll11l1111_opy_ > 0:
                sleep(bstack11ll11l1111_opy_ / 1000)
            params = {
                bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᝪ"): self.bstack1l111111l1_opy_,
                bstack111l111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᝫ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll111l1ll_opy_ = bstack111l111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᝬ") + bstack11ll111l1l1_opy_ + bstack111l111_opy_ (u"ࠧ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡣࡳ࡭࠴ࡼ࠱࠰ࠤ᝭")
            if self.bstack11ll111ll11_opy_.lower() == bstack111l111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢᝮ"):
                bstack11ll11l111l_opy_ = bstack11ll111lll1_opy_.results(bstack11ll111l1ll_opy_, params)
            else:
                bstack11ll11l111l_opy_ = bstack11ll111lll1_opy_.bstack11ll111ll1l_opy_(bstack11ll111l1ll_opy_, params)
            if str(bstack11ll11l111l_opy_.get(bstack111l111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᝯ"), bstack111l111_opy_ (u"ࠨ࠴࠳࠴ࠬᝰ"))) != bstack111l111_opy_ (u"ࠩ࠷࠴࠹࠭᝱"):
                break
        return bstack11ll11l111l_opy_.get(bstack111l111_opy_ (u"ࠪࡨࡦࡺࡡࠨᝲ"), bstack11ll11l111l_opy_)