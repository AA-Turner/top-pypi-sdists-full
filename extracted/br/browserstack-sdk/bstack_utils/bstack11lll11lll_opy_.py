# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11l111l1111_opy_ import bstack11l1111lll1_opy_
from bstack_utils.constants import *
import json
class bstack11l1ll111l_opy_:
    def __init__(self, bstack11ll11l1ll_opy_, bstack11l111l111l_opy_):
        self.bstack11ll11l1ll_opy_ = bstack11ll11l1ll_opy_
        self.bstack11l111l111l_opy_ = bstack11l111l111l_opy_
        self.bstack11l1111l1ll_opy_ = None
    def __call__(self):
        bstack11l1111ll11_opy_ = {}
        while True:
            self.bstack11l1111l1ll_opy_ = bstack11l1111ll11_opy_.get(
                bstack11ll111_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᥞ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11l1111ll1l_opy_ = self.bstack11l1111l1ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11l1111ll1l_opy_ > 0:
                sleep(bstack11l1111ll1l_opy_ / 1000)
            params = {
                bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᥟ"): self.bstack11ll11l1ll_opy_,
                bstack11ll111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᥠ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11l1111llll_opy_ = bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᥡ") + bstack11l1111l11l_opy_ + bstack11ll111_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨᥢ")
            if self.bstack11l111l111l_opy_.lower() == bstack11ll111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦᥣ"):
                bstack11l1111ll11_opy_ = bstack11l1111lll1_opy_.results(bstack11l1111llll_opy_, params)
            else:
                bstack11l1111ll11_opy_ = bstack11l1111lll1_opy_.bstack11l1111l1l1_opy_(bstack11l1111llll_opy_, params)
            if str(bstack11l1111ll11_opy_.get(bstack11ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᥤ"), bstack11ll111_opy_ (u"ࠬ࠸࠰࠱ࠩᥥ"))) != bstack11ll111_opy_ (u"࠭࠴࠱࠶ࠪᥦ"):
                break
        return bstack11l1111ll11_opy_.get(bstack11ll111_opy_ (u"ࠧࡥࡣࡷࡥࠬᥧ"), bstack11l1111ll11_opy_)