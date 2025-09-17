# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1l1ll1ll_opy_
logger = logging.getLogger(__name__)
class bstack11ll111l1ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llllll11111_opy_ = urljoin(builder, bstack1l11ll1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪᾘ"))
        if params:
            bstack1llllll11111_opy_ += bstack1l11ll1_opy_ (u"ࠦࡄࢁࡽࠣᾙ").format(urlencode({bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾚ"): params.get(bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᾛ"))}))
        return bstack11ll111l1ll_opy_.bstack1llllll11l1l_opy_(bstack1llllll11111_opy_)
    @staticmethod
    def bstack11ll111lll1_opy_(builder,params=None):
        bstack1llllll11111_opy_ = urljoin(builder, bstack1l11ll1_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨᾜ"))
        if params:
            bstack1llllll11111_opy_ += bstack1l11ll1_opy_ (u"ࠣࡁࡾࢁࠧᾝ").format(urlencode({bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᾞ"): params.get(bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᾟ"))}))
        return bstack11ll111l1ll_opy_.bstack1llllll11l1l_opy_(bstack1llllll11111_opy_)
    @staticmethod
    def bstack1llllll11l1l_opy_(bstack1lllll1lllll_opy_):
        bstack1llllll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᾠ"), os.environ.get(bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᾡ"), bstack1l11ll1_opy_ (u"࠭ࠧᾢ")))
        headers = {bstack1l11ll1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᾣ"): bstack1l11ll1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᾤ").format(bstack1llllll111ll_opy_)}
        response = requests.get(bstack1lllll1lllll_opy_, headers=headers)
        bstack1llllll111l1_opy_ = {}
        try:
            bstack1llllll111l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣᾥ").format(e))
            pass
        if bstack1llllll111l1_opy_ is not None:
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᾦ")] = response.headers.get(bstack1l11ll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᾧ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᾨ")] = response.status_code
        return bstack1llllll111l1_opy_
    @staticmethod
    def bstack1llllll11ll1_opy_(bstack1llllll11lll_opy_, data):
        logger.debug(bstack1l11ll1_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࠣᾩ"))
        return bstack11ll111l1ll_opy_.bstack1llllll11l11_opy_(bstack1l11ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᾪ"), bstack1llllll11lll_opy_, data=data)
    @staticmethod
    def bstack1llllll1111l_opy_(bstack1llllll11lll_opy_, data):
        logger.debug(bstack1l11ll1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣ࡫ࡪࡺࡔࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡳࠣᾫ"))
        res = bstack11ll111l1ll_opy_.bstack1llllll11l11_opy_(bstack1l11ll1_opy_ (u"ࠩࡊࡉ࡙࠭ᾬ"), bstack1llllll11lll_opy_, data=data)
        return res
    @staticmethod
    def bstack1llllll11l11_opy_(method, bstack1llllll11lll_opy_, data=None, params=None, extra_headers=None):
        bstack1llllll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᾭ"), bstack1l11ll1_opy_ (u"ࠫࠬᾮ"))
        headers = {
            bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᾯ"): bstack1l11ll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᾰ").format(bstack1llllll111ll_opy_),
            bstack1l11ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᾱ"): bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᾲ"),
            bstack1l11ll1_opy_ (u"ࠩࡄࡧࡨ࡫ࡰࡵࠩᾳ"): bstack1l11ll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᾴ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1l1ll1ll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠴ࠨ᾵") + bstack1llllll11lll_opy_.lstrip(bstack1l11ll1_opy_ (u"ࠬ࠵ࠧᾶ"))
        try:
            if method == bstack1l11ll1_opy_ (u"࠭ࡇࡆࡖࠪᾷ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l11ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬᾸ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l11ll1_opy_ (u"ࠨࡒࡘࡘࠬᾹ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l11ll1_opy_ (u"ࠤࡘࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤᾺ").format(method))
            logger.debug(bstack1l11ll1_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡲࡧࡤࡦࠢࡷࡳ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣΆ").format(url, method))
            bstack1llllll111l1_opy_ = {}
            try:
                bstack1llllll111l1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l11ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣᾼ").format(e, response.text))
            if bstack1llllll111l1_opy_ is not None:
                bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭᾽")] = response.headers.get(
                    bstack1l11ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧι"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᾿")] = response.status_code
            return bstack1llllll111l1_opy_
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ῀").format(e, url))
            return None
    @staticmethod
    def bstack11l1l111ll1_opy_(bstack1lllll1lllll_opy_, data):
        bstack1l11ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ῁")
        bstack1llllll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧῂ"), bstack1l11ll1_opy_ (u"ࠫࠬῃ"))
        headers = {
            bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬῄ"): bstack1l11ll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ῅").format(bstack1llllll111ll_opy_),
            bstack1l11ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ῆ"): bstack1l11ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫῇ")
        }
        response = requests.put(bstack1lllll1lllll_opy_, headers=headers, json=data)
        bstack1llllll111l1_opy_ = {}
        try:
            bstack1llllll111l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣῈ").format(e))
            pass
        logger.debug(bstack1l11ll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧΈ").format(bstack1llllll111l1_opy_))
        if bstack1llllll111l1_opy_ is not None:
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬῊ")] = response.headers.get(
                bstack1l11ll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ή"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ῌ")] = response.status_code
        return bstack1llllll111l1_opy_
    @staticmethod
    def bstack11l1l1l1111_opy_(bstack1lllll1lllll_opy_):
        bstack1l11ll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ῍")
        bstack1llllll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ῎"), bstack1l11ll1_opy_ (u"ࠩࠪ῏"))
        headers = {
            bstack1l11ll1_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪῐ"): bstack1l11ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧῑ").format(bstack1llllll111ll_opy_),
            bstack1l11ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫῒ"): bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩΐ")
        }
        response = requests.get(bstack1lllll1lllll_opy_, headers=headers)
        bstack1llllll111l1_opy_ = {}
        try:
            bstack1llllll111l1_opy_ = response.json()
            logger.debug(bstack1l11ll1_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ῔").format(bstack1llllll111l1_opy_))
        except Exception as e:
            logger.debug(bstack1l11ll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ῕").format(e, response.text))
            pass
        if bstack1llllll111l1_opy_ is not None:
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪῖ")] = response.headers.get(
                bstack1l11ll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫῗ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll111l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫῘ")] = response.status_code
        return bstack1llllll111l1_opy_
    @staticmethod
    def bstack1111ll1lll1_opy_(bstack11ll11l111l_opy_, payload):
        bstack1l11ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡰ࡫ࡳࠡࡣࠣࡔࡔ࡙ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡂࡒࡌࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡵࡩࡶࡻࡥࡴࡶࠣࡴࡦࡿ࡬ࡰࡣࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡄࡔࡎ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῙ")
        try:
            url = bstack1l11ll1_opy_ (u"ࠨࡻࡾ࠱ࡾࢁࠧῚ").format(bstack11l1l1ll1ll_opy_, bstack11ll11l111l_opy_)
            bstack1llllll111ll_opy_ = os.environ.get(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫΊ"), bstack1l11ll1_opy_ (u"ࠨࠩ῜"))
            headers = {
                bstack1l11ll1_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ῝"): bstack1l11ll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭῞").format(bstack1llllll111ll_opy_),
                bstack1l11ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ῟"): bstack1l11ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨῠ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200 or response.status_code == 202:
                return response.json()
            else:
                logger.error(bstack1l11ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧ࠮ࠡࡕࡷࡥࡹࡻࡳ࠻ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧῡ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l11ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡵࡷࡣࡨࡵ࡬࡭ࡧࡦࡸࡤࡨࡵࡪ࡮ࡧࡣࡩࡧࡴࡢ࠼ࠣࡿࢂࠨῢ").format(e))
            return None