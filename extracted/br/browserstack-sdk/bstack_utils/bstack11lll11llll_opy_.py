# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l1111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l111lll1_opy_ = urljoin(builder, bstack11lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶࠫᶅ"))
        if params:
            bstack111l111lll1_opy_ += bstack11lll_opy_ (u"ࠧࡅࡻࡾࠤᶆ").format(urlencode({bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᶇ"): params.get(bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶈ"))}))
        return bstack11lll1l1111_opy_.bstack111l11l111l_opy_(bstack111l111lll1_opy_)
    @staticmethod
    def bstack11lll11l1l1_opy_(builder,params=None):
        bstack111l111lll1_opy_ = urljoin(builder, bstack11lll_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩᶉ"))
        if params:
            bstack111l111lll1_opy_ += bstack11lll_opy_ (u"ࠤࡂࡿࢂࠨᶊ").format(urlencode({bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶋ"): params.get(bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶌ"))}))
        return bstack11lll1l1111_opy_.bstack111l11l111l_opy_(bstack111l111lll1_opy_)
    @staticmethod
    def bstack111l11l111l_opy_(bstack111l11l11l1_opy_):
        bstack111l11l1111_opy_ = os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᶍ"), os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᶎ"), bstack11lll_opy_ (u"ࠧࠨᶏ")))
        headers = {bstack11lll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᶐ"): bstack11lll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᶑ").format(bstack111l11l1111_opy_)}
        response = requests.get(bstack111l11l11l1_opy_, headers=headers)
        bstack111l111llll_opy_ = {}
        try:
            bstack111l111llll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤᶒ").format(e))
            pass
        if bstack111l111llll_opy_ is not None:
            bstack111l111llll_opy_[bstack11lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᶓ")] = response.headers.get(bstack11lll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᶔ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l111llll_opy_[bstack11lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᶕ")] = response.status_code
        return bstack111l111llll_opy_