# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11ll111lll1_opy_ import bstack11ll11l1111_opy_
from bstack_utils.constants import *
import json
class bstack11llllllll_opy_:
    def __init__(self, bstack1lll1ll11l_opy_, bstack11ll111l1l1_opy_):
        self.bstack1lll1ll11l_opy_ = bstack1lll1ll11l_opy_
        self.bstack11ll111l1l1_opy_ = bstack11ll111l1l1_opy_
        self.bstack11ll111llll_opy_ = None
    def __call__(self):
        bstack11ll111ll11_opy_ = {}
        while True:
            self.bstack11ll111llll_opy_ = bstack11ll111ll11_opy_.get(
                bstack1111l1l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ᝱"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11ll111ll1l_opy_ = self.bstack11ll111llll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11ll111ll1l_opy_ > 0:
                sleep(bstack11ll111ll1l_opy_ / 1000)
            params = {
                bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᝲ"): self.bstack1lll1ll11l_opy_,
                bstack1111l1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᝳ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11ll11l111l_opy_ = bstack1111l1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᝴") + bstack11ll111l11l_opy_ + bstack1111l1l_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥ᝵")
            if self.bstack11ll111l1l1_opy_.lower() == bstack1111l1l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣ᝶"):
                bstack11ll111ll11_opy_ = bstack11ll11l1111_opy_.results(bstack11ll11l111l_opy_, params)
            else:
                bstack11ll111ll11_opy_ = bstack11ll11l1111_opy_.bstack11ll111l1ll_opy_(bstack11ll11l111l_opy_, params)
            if str(bstack11ll111ll11_opy_.get(bstack1111l1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᝷"), bstack1111l1l_opy_ (u"ࠩ࠵࠴࠵࠭᝸"))) != bstack1111l1l_opy_ (u"ࠪ࠸࠵࠺ࠧ᝹"):
                break
        return bstack11ll111ll11_opy_.get(bstack1111l1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ᝺"), bstack11ll111ll11_opy_)