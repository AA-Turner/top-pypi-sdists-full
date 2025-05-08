# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l11l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l111l_opy_ = urljoin(builder, bstack1l1lll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧᶁ"))
        if params:
            bstack111l11l111l_opy_ += bstack1l1lll_opy_ (u"ࠣࡁࡾࢁࠧᶂ").format(urlencode({bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᶃ"): params.get(bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶄ"))}))
        return bstack11lll1l11l1_opy_.bstack111l11l1111_opy_(bstack111l11l111l_opy_)
    @staticmethod
    def bstack11lll11ll1l_opy_(builder,params=None):
        bstack111l11l111l_opy_ = urljoin(builder, bstack1l1lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬᶅ"))
        if params:
            bstack111l11l111l_opy_ += bstack1l1lll_opy_ (u"ࠧࡅࡻࡾࠤᶆ").format(urlencode({bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶇ"): params.get(bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶈ"))}))
        return bstack11lll1l11l1_opy_.bstack111l11l1111_opy_(bstack111l11l111l_opy_)
    @staticmethod
    def bstack111l11l1111_opy_(bstack111l11l11ll_opy_):
        bstack111l11l1l11_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᶉ"), os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᶊ"), bstack1l1lll_opy_ (u"ࠪࠫᶋ")))
        headers = {bstack1l1lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᶌ"): bstack1l1lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᶍ").format(bstack111l11l1l11_opy_)}
        response = requests.get(bstack111l11l11ll_opy_, headers=headers)
        bstack111l11l11l1_opy_ = {}
        try:
            bstack111l11l11l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧᶎ").format(e))
            pass
        if bstack111l11l11l1_opy_ is not None:
            bstack111l11l11l1_opy_[bstack1l1lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᶏ")] = response.headers.get(bstack1l1lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᶐ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l11l1_opy_[bstack1l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᶑ")] = response.status_code
        return bstack111l11l11l1_opy_