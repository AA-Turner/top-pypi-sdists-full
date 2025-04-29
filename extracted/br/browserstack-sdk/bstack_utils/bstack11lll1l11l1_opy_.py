# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l111l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1111_opy_ = urljoin(builder, bstack1llllll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩᵼ"))
        if params:
            bstack111l11l1111_opy_ += bstack1llllll_opy_ (u"ࠥࡃࢀࢃࠢᵽ").format(urlencode({bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵾ"): params.get(bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵿ"))}))
        return bstack11lll1l111l_opy_.bstack111l11l11ll_opy_(bstack111l11l1111_opy_)
    @staticmethod
    def bstack11lll11ll1l_opy_(builder,params=None):
        bstack111l11l1111_opy_ = urljoin(builder, bstack1llllll_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧᶀ"))
        if params:
            bstack111l11l1111_opy_ += bstack1llllll_opy_ (u"ࠢࡀࡽࢀࠦᶁ").format(urlencode({bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᶂ"): params.get(bstack1llllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶃ"))}))
        return bstack11lll1l111l_opy_.bstack111l11l11ll_opy_(bstack111l11l1111_opy_)
    @staticmethod
    def bstack111l11l11ll_opy_(bstack111l11l111l_opy_):
        bstack111l11l11l1_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᶄ"), os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᶅ"), bstack1llllll_opy_ (u"ࠬ࠭ᶆ")))
        headers = {bstack1llllll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᶇ"): bstack1llllll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪᶈ").format(bstack111l11l11l1_opy_)}
        response = requests.get(bstack111l11l111l_opy_, headers=headers)
        bstack111l11l1l11_opy_ = {}
        try:
            bstack111l11l1l11_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢᶉ").format(e))
            pass
        if bstack111l11l1l11_opy_ is not None:
            bstack111l11l1l11_opy_[bstack1llllll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᶊ")] = response.headers.get(bstack1llllll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᶋ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1l11_opy_[bstack1llllll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᶌ")] = response.status_code
        return bstack111l11l1l11_opy_