# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll11111_opy_
logger = logging.getLogger(__name__)
class bstack11ll11l1ll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llllll11ll1_opy_ = urljoin(builder, bstack1111lll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧᾕ"))
        if params:
            bstack1llllll11ll1_opy_ += bstack1111lll_opy_ (u"ࠣࡁࡾࢁࠧᾖ").format(urlencode({bstack1111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾗ"): params.get(bstack1111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾘ"))}))
        return bstack11ll11l1ll1_opy_.bstack1llllll1l1ll_opy_(bstack1llllll11ll1_opy_)
    @staticmethod
    def bstack11ll111lll1_opy_(builder,params=None):
        bstack1llllll11ll1_opy_ = urljoin(builder, bstack1111lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬᾙ"))
        if params:
            bstack1llllll11ll1_opy_ += bstack1111lll_opy_ (u"ࠧࡅࡻࡾࠤᾚ").format(urlencode({bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾛ"): params.get(bstack1111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾜ"))}))
        return bstack11ll11l1ll1_opy_.bstack1llllll1l1ll_opy_(bstack1llllll11ll1_opy_)
    @staticmethod
    def bstack1llllll1l1ll_opy_(bstack1llllll1ll1l_opy_):
        bstack1llllll1l11l_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᾝ"), os.environ.get(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᾞ"), bstack1111lll_opy_ (u"ࠪࠫᾟ")))
        headers = {bstack1111lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᾠ"): bstack1111lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨᾡ").format(bstack1llllll1l11l_opy_)}
        response = requests.get(bstack1llllll1ll1l_opy_, headers=headers)
        bstack1llllll11lll_opy_ = {}
        try:
            bstack1llllll11lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧᾢ").format(e))
            pass
        if bstack1llllll11lll_opy_ is not None:
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᾣ")] = response.headers.get(bstack1111lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᾤ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᾥ")] = response.status_code
        return bstack1llllll11lll_opy_
    @staticmethod
    def bstack1llllll11l1l_opy_(bstack1llllll1ll11_opy_, data):
        logger.debug(bstack1111lll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࠧᾦ"))
        return bstack11ll11l1ll1_opy_.bstack1llllll1l111_opy_(bstack1111lll_opy_ (u"ࠫࡕࡕࡓࡕࠩᾧ"), bstack1llllll1ll11_opy_, data=data)
    @staticmethod
    def bstack1llllll1l1l1_opy_(bstack1llllll1ll11_opy_, data):
        logger.debug(bstack1111lll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡨࡧࡷࡘࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡷࠧᾨ"))
        res = bstack11ll11l1ll1_opy_.bstack1llllll1l111_opy_(bstack1111lll_opy_ (u"࠭ࡇࡆࡖࠪᾩ"), bstack1llllll1ll11_opy_, data=data)
        return res
    @staticmethod
    def bstack1llllll1l111_opy_(method, bstack1llllll1ll11_opy_, data=None, params=None, extra_headers=None):
        bstack1llllll1l11l_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᾪ"), bstack1111lll_opy_ (u"ࠨࠩᾫ"))
        headers = {
            bstack1111lll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᾬ"): bstack1111lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᾭ").format(bstack1llllll1l11l_opy_),
            bstack1111lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᾮ"): bstack1111lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᾯ"),
            bstack1111lll_opy_ (u"࠭ࡁࡤࡥࡨࡴࡹ࠭ᾰ"): bstack1111lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᾱ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll11111_opy_ + bstack1111lll_opy_ (u"ࠣ࠱ࠥᾲ") + bstack1llllll1ll11_opy_.lstrip(bstack1111lll_opy_ (u"ࠩ࠲ࠫᾳ"))
        try:
            if method == bstack1111lll_opy_ (u"ࠪࡋࡊ࡚ࠧᾴ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1111lll_opy_ (u"ࠫࡕࡕࡓࡕࠩ᾵"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1111lll_opy_ (u"ࠬࡖࡕࡕࠩᾶ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1111lll_opy_ (u"ࠨࡕ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨᾷ").format(method))
            logger.debug(bstack1111lll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡ࡯ࡤࡨࡪࠦࡴࡰࠢࡘࡖࡑࡀࠠࡼࡿࠣࡻ࡮ࡺࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧᾸ").format(url, method))
            bstack1llllll11lll_opy_ = {}
            try:
                bstack1llllll11lll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1111lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧᾹ").format(e, response.text))
            if bstack1llllll11lll_opy_ is not None:
                bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᾺ")] = response.headers.get(
                    bstack1111lll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫΆ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᾼ")] = response.status_code
            return bstack1llllll11lll_opy_
        except Exception as e:
            logger.error(bstack1111lll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ᾽").format(e, url))
            return None
    @staticmethod
    def bstack11l1l111lll_opy_(bstack1llllll1ll1l_opy_, data):
        bstack1111lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡕ࡛ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦι")
        bstack1llllll1l11l_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᾿"), bstack1111lll_opy_ (u"ࠨࠩ῀"))
        headers = {
            bstack1111lll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ῁"): bstack1111lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ῂ").format(bstack1llllll1l11l_opy_),
            bstack1111lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪῃ"): bstack1111lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨῄ")
        }
        response = requests.put(bstack1llllll1ll1l_opy_, headers=headers, json=data)
        bstack1llllll11lll_opy_ = {}
        try:
            bstack1llllll11lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ῅").format(e))
            pass
        logger.debug(bstack1111lll_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡱࡷࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤῆ").format(bstack1llllll11lll_opy_))
        if bstack1llllll11lll_opy_ is not None:
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩῇ")] = response.headers.get(
                bstack1111lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪῈ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪΈ")] = response.status_code
        return bstack1llllll11lll_opy_
    @staticmethod
    def bstack11l1l1l1lll_opy_(bstack1llllll1ll1l_opy_):
        bstack1111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡊࡉ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣ࡫ࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῊ")
        bstack1llllll1l11l_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩΉ"), bstack1111lll_opy_ (u"࠭ࠧῌ"))
        headers = {
            bstack1111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ῍"): bstack1111lll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ῎").format(bstack1llllll1l11l_opy_),
            bstack1111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ῏"): bstack1111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ῐ")
        }
        response = requests.get(bstack1llllll1ll1l_opy_, headers=headers)
        bstack1llllll11lll_opy_ = {}
        try:
            bstack1llllll11lll_opy_ = response.json()
            logger.debug(bstack1111lll_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤ࡬࡫ࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨῑ").format(bstack1llllll11lll_opy_))
        except Exception as e:
            logger.debug(bstack1111lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤῒ").format(e, response.text))
            pass
        if bstack1llllll11lll_opy_ is not None:
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧΐ")] = response.headers.get(
                bstack1111lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ῔"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll11lll_opy_[bstack1111lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῕")] = response.status_code
        return bstack1llllll11lll_opy_
    @staticmethod
    def bstack1111lll111l_opy_(bstack11ll11ll111_opy_, payload):
        bstack1111lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡍࡢ࡭ࡨࡷࠥࡧࠠࡑࡑࡖࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤࡆࡖࡉࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡼࡰࡴࡧࡤࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡲࡦࡳࡸࡩࡸࡺࠠࡱࡣࡼࡰࡴࡧࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡁࡑࡋ࠯ࠤࡴࡸࠠࡏࡱࡱࡩࠥ࡯ࡦࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨῖ")
        try:
            url = bstack1111lll_opy_ (u"ࠥࡿࢂ࠵ࡻࡾࠤῗ").format(bstack11l1ll11111_opy_, bstack11ll11ll111_opy_)
            bstack1llllll1l11l_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨῘ"), bstack1111lll_opy_ (u"ࠬ࠭Ῑ"))
            headers = {
                bstack1111lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ὶ"): bstack1111lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪΊ").format(bstack1llllll1l11l_opy_),
                bstack1111lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ῜"): bstack1111lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ῝")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200 or response.status_code == 202:
                return response.json()
            else:
                logger.error(bstack1111lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤ࠲࡙ࠥࡴࡢࡶࡸࡷ࠿ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ῞").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡹࡴࡠࡥࡲࡰࡱ࡫ࡣࡵࡡࡥࡹ࡮ࡲࡤࡠࡦࡤࡸࡦࡀࠠࡼࡿࠥ῟").format(e))
            return None