# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack111111lllll_opy_ import bstack11111l111ll_opy_
from bstack_utils.constants import *
import json
class bstack11l1ll1l1l_opy_:
    def __init__(self, test_run_uuid, bstack11111l11111_opy_):
        self.test_run_uuid = test_run_uuid
        self.bstack11111l11111_opy_ = bstack11111l11111_opy_
        self.bstack11111l1111l_opy_ = None
    def __call__(self):
        bstack11111l11l11_opy_ = {}
        while True:
            self.bstack11111l1111l_opy_ = bstack11111l11l11_opy_.get(
                bstack1l1llll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⁬"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11111l11l1l_opy_ = self.bstack11111l1111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11111l11l1l_opy_ > 0:
                sleep(bstack11111l11l1l_opy_ / 1000)
            params = {
                bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⁭"): self.test_run_uuid,
                bstack1l1llll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⁮"): int(datetime.now().timestamp() * 1000)
            }
            base_url = bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ⁯") + bstack11111l111l1_opy_ + bstack1l1llll_opy_ (u"ࠤ࠲ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡧࡰࡪ࠱ࡹ࠵࠴ࠨ⁰")
            if self.bstack11111l11111_opy_.lower() == bstack1l1llll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࡶࠦⁱ"):
                bstack11111l11l11_opy_ = bstack11111l111ll_opy_.results(base_url, params)
            else:
                bstack11111l11l11_opy_ = bstack11111l111ll_opy_.bstack111111llll1_opy_(base_url, params)
            if str(bstack11111l11l11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⁲"), bstack1l1llll_opy_ (u"ࠬ࠸࠰࠱ࠩ⁳"))) != bstack1l1llll_opy_ (u"࠭࠴࠱࠶ࠪ⁴"):
                break
        return bstack11111l11l11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡥࡣࡷࡥࠬ⁵"), bstack11111l11l11_opy_)