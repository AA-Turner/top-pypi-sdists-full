# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll11lll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1111_opy_ = urljoin(builder, bstack1l11lll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧᵺ"))
        if params:
            bstack111l11l1111_opy_ += bstack1l11lll_opy_ (u"ࠣࡁࡾࢁࠧᵻ").format(urlencode({bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᵼ"): params.get(bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵽ"))}))
        return bstack11lll11lll1_opy_.bstack111l11l11l1_opy_(bstack111l11l1111_opy_)
    @staticmethod
    def bstack11lll1l1l11_opy_(builder,params=None):
        bstack111l11l1111_opy_ = urljoin(builder, bstack1l11lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬᵾ"))
        if params:
            bstack111l11l1111_opy_ += bstack1l11lll_opy_ (u"ࠧࡅࡻࡾࠤᵿ").format(urlencode({bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶀ"): params.get(bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶁ"))}))
        return bstack11lll11lll1_opy_.bstack111l11l11l1_opy_(bstack111l11l1111_opy_)
    @staticmethod
    def bstack111l11l11l1_opy_(bstack111l11l111l_opy_):
        bstack111l11l1l11_opy_ = os.environ.get(bstack1l11lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᶂ"), os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᶃ"), bstack1l11lll_opy_ (u"ࠪࠫᶄ")))
        headers = {bstack1l11lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᶅ"): bstack1l11lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᶆ").format(bstack111l11l1l11_opy_)}
        response = requests.get(bstack111l11l111l_opy_, headers=headers)
        bstack111l11l11ll_opy_ = {}
        try:
            bstack111l11l11ll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧᶇ").format(e))
            pass
        if bstack111l11l11ll_opy_ is not None:
            bstack111l11l11ll_opy_[bstack1l11lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᶈ")] = response.headers.get(bstack1l11lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᶉ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l11ll_opy_[bstack1l11lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᶊ")] = response.status_code
        return bstack111l11l11ll_opy_