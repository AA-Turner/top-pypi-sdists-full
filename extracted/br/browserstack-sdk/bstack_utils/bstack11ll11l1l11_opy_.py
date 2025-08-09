# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11ll111111l_opy_
logger = logging.getLogger(__name__)
class bstack11ll11l1111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lllllll1111_opy_ = urljoin(builder, bstack11l1_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠭ᾛ"))
        if params:
            bstack1lllllll1111_opy_ += bstack11l1_opy_ (u"ࠢࡀࡽࢀࠦᾜ").format(urlencode({bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾝ"): params.get(bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾞ"))}))
        return bstack11ll11l1111_opy_.bstack1lllllll1lll_opy_(bstack1lllllll1111_opy_)
    @staticmethod
    def bstack11ll11l11ll_opy_(builder,params=None):
        bstack1lllllll1111_opy_ = urljoin(builder, bstack11l1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫᾟ"))
        if params:
            bstack1lllllll1111_opy_ += bstack11l1_opy_ (u"ࠦࡄࢁࡽࠣᾠ").format(urlencode({bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾡ"): params.get(bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾢ"))}))
        return bstack11ll11l1111_opy_.bstack1lllllll1lll_opy_(bstack1lllllll1111_opy_)
    @staticmethod
    def bstack1lllllll1lll_opy_(bstack1lllllll11ll_opy_):
        bstack1lllllll111l_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᾣ"), os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾤ"), bstack11l1_opy_ (u"ࠩࠪᾥ")))
        headers = {bstack11l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᾦ"): bstack11l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧᾧ").format(bstack1lllllll111l_opy_)}
        response = requests.get(bstack1lllllll11ll_opy_, headers=headers)
        bstack1lllllll1ll1_opy_ = {}
        try:
            bstack1lllllll1ll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦᾨ").format(e))
            pass
        if bstack1lllllll1ll1_opy_ is not None:
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᾩ")] = response.headers.get(bstack11l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨᾪ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᾫ")] = response.status_code
        return bstack1lllllll1ll1_opy_
    @staticmethod
    def bstack1llllllll111_opy_(bstack1lllllll11l1_opy_, data):
        logger.debug(bstack11l1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࠦᾬ"))
        return bstack11ll11l1111_opy_.bstack1lllllll1l1l_opy_(bstack11l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᾭ"), bstack1lllllll11l1_opy_, data=data)
    @staticmethod
    def bstack1lllllll1l11_opy_(bstack1lllllll11l1_opy_, data):
        logger.debug(bstack11l1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡧࡦࡶࡗࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡶࠦᾮ"))
        res = bstack11ll11l1111_opy_.bstack1lllllll1l1l_opy_(bstack11l1_opy_ (u"ࠬࡍࡅࡕࠩᾯ"), bstack1lllllll11l1_opy_, data=data)
        return res
    @staticmethod
    def bstack1lllllll1l1l_opy_(method, bstack1lllllll11l1_opy_, data=None, params=None, extra_headers=None):
        bstack1lllllll111l_opy_ = os.environ.get(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᾰ"), bstack11l1_opy_ (u"ࠧࠨᾱ"))
        headers = {
            bstack11l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᾲ"): bstack11l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᾳ").format(bstack1lllllll111l_opy_),
            bstack11l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᾴ"): bstack11l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ᾵"),
            bstack11l1_opy_ (u"ࠬࡇࡣࡤࡧࡳࡸࠬᾶ"): bstack11l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᾷ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11ll111111l_opy_ + bstack11l1_opy_ (u"ࠢ࠰ࠤᾸ") + bstack1lllllll11l1_opy_.lstrip(bstack11l1_opy_ (u"ࠨ࠱ࠪᾹ"))
        try:
            if method == bstack11l1_opy_ (u"ࠩࡊࡉ࡙࠭Ὰ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨΆ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11l1_opy_ (u"ࠫࡕ࡛ࡔࠨᾼ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11l1_opy_ (u"࡛ࠧ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧ᾽").format(method))
            logger.debug(bstack11l1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡮ࡣࡧࡩࠥࡺ࡯ࠡࡗࡕࡐ࠿ࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦι").format(url, method))
            bstack1lllllll1ll1_opy_ = {}
            try:
                bstack1lllllll1ll1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ᾿").format(e, response.text))
            if bstack1lllllll1ll1_opy_ is not None:
                bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ῀")] = response.headers.get(
                    bstack11l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ῁"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪῂ")] = response.status_code
            return bstack1lllllll1ll1_opy_
        except Exception as e:
            logger.error(bstack11l1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢῃ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l1l1lll_opy_(bstack1lllllll11ll_opy_, data):
        bstack11l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡔ࡚࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥῄ")
        bstack1lllllll111l_opy_ = os.environ.get(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ῅"), bstack11l1_opy_ (u"ࠧࠨῆ"))
        headers = {
            bstack11l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨῇ"): bstack11l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬῈ").format(bstack1lllllll111l_opy_),
            bstack11l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩΈ"): bstack11l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧῊ")
        }
        response = requests.put(bstack1lllllll11ll_opy_, headers=headers, json=data)
        bstack1lllllll1ll1_opy_ = {}
        try:
            bstack1lllllll1ll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦΉ").format(e))
            pass
        logger.debug(bstack11l1_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡰࡶࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣῌ").format(bstack1lllllll1ll1_opy_))
        if bstack1lllllll1ll1_opy_ is not None:
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ῍")] = response.headers.get(
                bstack11l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ῎"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ῏")] = response.status_code
        return bstack1lllllll1ll1_opy_
    @staticmethod
    def bstack11l1l1l11ll_opy_(bstack1lllllll11ll_opy_):
        bstack11l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡉࡈࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡪࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣῐ")
        bstack1lllllll111l_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨῑ"), bstack11l1_opy_ (u"ࠬ࠭ῒ"))
        headers = {
            bstack11l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ΐ"): bstack11l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ῔").format(bstack1lllllll111l_opy_),
            bstack11l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ῕"): bstack11l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬῖ")
        }
        response = requests.get(bstack1lllllll11ll_opy_, headers=headers)
        bstack1lllllll1ll1_opy_ = {}
        try:
            bstack1lllllll1ll1_opy_ = response.json()
            logger.debug(bstack11l1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣ࡫ࡪࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧῗ").format(bstack1lllllll1ll1_opy_))
        except Exception as e:
            logger.debug(bstack11l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣῘ").format(e, response.text))
            pass
        if bstack1lllllll1ll1_opy_ is not None:
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ῑ")] = response.headers.get(
                bstack11l1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧῚ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lllllll1ll1_opy_[bstack11l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧΊ")] = response.status_code
        return bstack1lllllll1ll1_opy_
    @staticmethod
    def bstack1111llll111_opy_(bstack11ll11ll11l_opy_, payload):
        bstack11l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡓࡡ࡬ࡧࡶࠤࡦࠦࡐࡐࡕࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧࠣࡅࡕࡏࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡸࡥࡲࡷࡨࡷࡹࠦࡰࡢࡻ࡯ࡳࡦࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡇࡐࡊ࠮ࠣࡳࡷࠦࡎࡰࡰࡨࠤ࡮࡬ࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ῜")
        try:
            url = bstack11l1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽࠣ῝").format(bstack11ll111111l_opy_, bstack11ll11ll11l_opy_)
            bstack1lllllll111l_opy_ = os.environ.get(bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ῞"), bstack11l1_opy_ (u"ࠫࠬ῟"))
            headers = {
                bstack11l1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬῠ"): bstack11l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩῡ").format(bstack1lllllll111l_opy_),
                bstack11l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ῢ"): bstack11l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫΰ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(bstack11l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣ࠱ࠤࡘࡺࡡࡵࡷࡶ࠾ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣῤ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack11l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡸࡺ࡟ࡤࡱ࡯ࡰࡪࡩࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡻࡾࠤῥ").format(e))
            return None