# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1l1ll11l_opy_
logger = logging.getLogger(__name__)
class bstack11ll11111l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llllll11l11_opy_ = urljoin(builder, bstack1ll11ll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶࠫᾙ"))
        if params:
            bstack1llllll11l11_opy_ += bstack1ll11ll_opy_ (u"ࠧࡅࡻࡾࠤᾚ").format(urlencode({bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾛ"): params.get(bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾜ"))}))
        return bstack11ll11111l1_opy_.bstack1lllll1lllll_opy_(bstack1llllll11l11_opy_)
    @staticmethod
    def bstack11l1lllllll_opy_(builder,params=None):
        bstack1llllll11l11_opy_ = urljoin(builder, bstack1ll11ll_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩᾝ"))
        if params:
            bstack1llllll11l11_opy_ += bstack1ll11ll_opy_ (u"ࠤࡂࡿࢂࠨᾞ").format(urlencode({bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾟ"): params.get(bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾠ"))}))
        return bstack11ll11111l1_opy_.bstack1lllll1lllll_opy_(bstack1llllll11l11_opy_)
    @staticmethod
    def bstack1lllll1lllll_opy_(bstack1llllll11l1l_opy_):
        bstack1llllll11ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᾡ"), os.environ.get(bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᾢ"), bstack1ll11ll_opy_ (u"ࠧࠨᾣ")))
        headers = {bstack1ll11ll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᾤ"): bstack1ll11ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᾥ").format(bstack1llllll11ll1_opy_)}
        response = requests.get(bstack1llllll11l1l_opy_, headers=headers)
        bstack1llllll111ll_opy_ = {}
        try:
            bstack1llllll111ll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤᾦ").format(e))
            pass
        if bstack1llllll111ll_opy_ is not None:
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᾧ")] = response.headers.get(bstack1ll11ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᾨ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᾩ")] = response.status_code
        return bstack1llllll111ll_opy_
    @staticmethod
    def bstack1llllll11lll_opy_(bstack1llllll111l1_opy_, data):
        logger.debug(bstack1ll11ll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࠤᾪ"))
        return bstack11ll11111l1_opy_.bstack1llllll11111_opy_(bstack1ll11ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᾫ"), bstack1llllll111l1_opy_, data=data)
    @staticmethod
    def bstack1llllll1111l_opy_(bstack1llllll111l1_opy_, data):
        logger.debug(bstack1ll11ll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤ࡬࡫ࡴࡕࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡴࠤᾬ"))
        res = bstack11ll11111l1_opy_.bstack1llllll11111_opy_(bstack1ll11ll_opy_ (u"ࠪࡋࡊ࡚ࠧᾭ"), bstack1llllll111l1_opy_, data=data)
        return res
    @staticmethod
    def bstack1llllll11111_opy_(method, bstack1llllll111l1_opy_, data=None, params=None, extra_headers=None):
        bstack1llllll11ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᾮ"), bstack1ll11ll_opy_ (u"ࠬ࠭ᾯ"))
        headers = {
            bstack1ll11ll_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᾰ"): bstack1ll11ll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪᾱ").format(bstack1llllll11ll1_opy_),
            bstack1ll11ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᾲ"): bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᾳ"),
            bstack1ll11ll_opy_ (u"ࠪࡅࡨࡩࡥࡱࡶࠪᾴ"): bstack1ll11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ᾵")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1l1ll11l_opy_ + bstack1ll11ll_opy_ (u"ࠧ࠵ࠢᾶ") + bstack1llllll111l1_opy_.lstrip(bstack1ll11ll_opy_ (u"࠭࠯ࠨᾷ"))
        try:
            if method == bstack1ll11ll_opy_ (u"ࠧࡈࡇࡗࠫᾸ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll11ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭Ᾱ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll11ll_opy_ (u"ࠩࡓ࡙࡙࠭Ὰ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll11ll_opy_ (u"࡙ࠥࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡊࡗࡘࡕࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥΆ").format(method))
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡳࡡࡥࡧࠣࡸࡴࠦࡕࡓࡎ࠽ࠤࢀࢃࠠࡸ࡫ࡷ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤᾼ").format(url, method))
            bstack1llllll111ll_opy_ = {}
            try:
                bstack1llllll111ll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll11ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ᾽").format(e, response.text))
            if bstack1llllll111ll_opy_ is not None:
                bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧι")] = response.headers.get(
                    bstack1ll11ll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ᾿"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῀")] = response.status_code
            return bstack1llllll111ll_opy_
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ῁").format(e, url))
            return None
    @staticmethod
    def bstack11l1l11l1l1_opy_(bstack1llllll11l1l_opy_, data):
        bstack1ll11ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡒࡘࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣῂ")
        bstack1llllll11ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨῃ"), bstack1ll11ll_opy_ (u"ࠬ࠭ῄ"))
        headers = {
            bstack1ll11ll_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭῅"): bstack1ll11ll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪῆ").format(bstack1llllll11ll1_opy_),
            bstack1ll11ll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧῇ"): bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬῈ")
        }
        response = requests.put(bstack1llllll11l1l_opy_, headers=headers, json=data)
        bstack1llllll111ll_opy_ = {}
        try:
            bstack1llllll111ll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤΈ").format(e))
            pass
        logger.debug(bstack1ll11ll_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤࡵࡻࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨῊ").format(bstack1llllll111ll_opy_))
        if bstack1llllll111ll_opy_ is not None:
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ή")] = response.headers.get(
                bstack1ll11ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧῌ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ῍")] = response.status_code
        return bstack1llllll111ll_opy_
    @staticmethod
    def bstack11l1l111lll_opy_(bstack1llllll11l1l_opy_):
        bstack1ll11ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡇࡆࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡨࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ῎")
        bstack1llllll11ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭῏"), bstack1ll11ll_opy_ (u"ࠪࠫῐ"))
        headers = {
            bstack1ll11ll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫῑ"): bstack1ll11ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨῒ").format(bstack1llllll11ll1_opy_),
            bstack1ll11ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬΐ"): bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ῔")
        }
        response = requests.get(bstack1llllll11l1l_opy_, headers=headers)
        bstack1llllll111ll_opy_ = {}
        try:
            bstack1llllll111ll_opy_ = response.json()
            logger.debug(bstack1ll11ll_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡩࡨࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ῕").format(bstack1llllll111ll_opy_))
        except Exception as e:
            logger.debug(bstack1ll11ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨῖ").format(e, response.text))
            pass
        if bstack1llllll111ll_opy_ is not None:
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫῗ")] = response.headers.get(
                bstack1ll11ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬῘ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬῙ")] = response.status_code
        return bstack1llllll111ll_opy_
    @staticmethod
    def bstack1111llll1ll_opy_(bstack11ll1111ll1_opy_, payload):
        bstack1ll11ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡑࡦࡱࡥࡴࠢࡤࠤࡕࡕࡓࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤ࠭ࡹࡴࡳࠫ࠽ࠤ࡙࡮ࡥࠡࡃࡓࡍࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࠮ࡤࡪࡥࡷ࠭࠿ࠦࡔࡩࡧࠣࡶࡪࡷࡵࡦࡵࡷࠤࡵࡧࡹ࡭ࡱࡤࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡅࡕࡏࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥῚ")
        try:
            url = bstack1ll11ll_opy_ (u"ࠢࡼࡿ࠲ࡿࢂࠨΊ").format(bstack11l1l1ll11l_opy_, bstack11ll1111ll1_opy_)
            bstack1llllll11ll1_opy_ = os.environ.get(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ῜"), bstack1ll11ll_opy_ (u"ࠩࠪ῝"))
            headers = {
                bstack1ll11ll_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ῞"): bstack1ll11ll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ῟").format(bstack1llllll11ll1_opy_),
                bstack1ll11ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫῠ"): bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩῡ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200 or response.status_code == 202:
                return response.json()
            else:
                logger.error(bstack1ll11ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡ࠯ࠢࡖࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨῢ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll11ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡶࡸࡤࡩ࡯࡭࡮ࡨࡧࡹࡥࡢࡶ࡫࡯ࡨࡤࡪࡡࡵࡣ࠽ࠤࢀࢃࠢΰ").format(e))
            return None