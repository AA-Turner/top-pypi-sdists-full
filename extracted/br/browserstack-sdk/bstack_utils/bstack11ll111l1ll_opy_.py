# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1lllllll_opy_
logger = logging.getLogger(__name__)
class bstack11ll11l111l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1llllll1llll_opy_ = urljoin(builder, bstack1l11l11_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬᾚ"))
        if params:
            bstack1llllll1llll_opy_ += bstack1l11l11_opy_ (u"ࠨ࠿ࡼࡿࠥᾛ").format(urlencode({bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾜ"): params.get(bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾝ"))}))
        return bstack11ll11l111l_opy_.bstack1llllll1ll11_opy_(bstack1llllll1llll_opy_)
    @staticmethod
    def bstack11ll11l11ll_opy_(builder,params=None):
        bstack1llllll1llll_opy_ = urljoin(builder, bstack1l11l11_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᾞ"))
        if params:
            bstack1llllll1llll_opy_ += bstack1l11l11_opy_ (u"ࠥࡃࢀࢃࠢᾟ").format(urlencode({bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾠ"): params.get(bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾡ"))}))
        return bstack11ll11l111l_opy_.bstack1llllll1ll11_opy_(bstack1llllll1llll_opy_)
    @staticmethod
    def bstack1llllll1ll11_opy_(bstack1lllllll1111_opy_):
        bstack1lllllll11l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᾢ"), os.environ.get(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᾣ"), bstack1l11l11_opy_ (u"ࠨࠩᾤ")))
        headers = {bstack1l11l11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᾥ"): bstack1l11l11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᾦ").format(bstack1lllllll11l1_opy_)}
        response = requests.get(bstack1lllllll1111_opy_, headers=headers)
        bstack1llllll1ll1l_opy_ = {}
        try:
            bstack1llllll1ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥᾧ").format(e))
            pass
        if bstack1llllll1ll1l_opy_ is not None:
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᾨ")] = response.headers.get(bstack1l11l11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᾩ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᾪ")] = response.status_code
        return bstack1llllll1ll1l_opy_
    @staticmethod
    def bstack1lllllll1l11_opy_(bstack1lllllll11ll_opy_, data):
        logger.debug(bstack1l11l11_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࠥᾫ"))
        return bstack11ll11l111l_opy_.bstack1llllll1lll1_opy_(bstack1l11l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᾬ"), bstack1lllllll11ll_opy_, data=data)
    @staticmethod
    def bstack1lllllll111l_opy_(bstack1lllllll11ll_opy_, data):
        logger.debug(bstack1l11l11_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥ࡭ࡥࡵࡖࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡵࠥᾭ"))
        res = bstack11ll11l111l_opy_.bstack1llllll1lll1_opy_(bstack1l11l11_opy_ (u"ࠫࡌࡋࡔࠨᾮ"), bstack1lllllll11ll_opy_, data=data)
        return res
    @staticmethod
    def bstack1llllll1lll1_opy_(method, bstack1lllllll11ll_opy_, data=None, params=None, extra_headers=None):
        bstack1lllllll11l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᾯ"), bstack1l11l11_opy_ (u"࠭ࠧᾰ"))
        headers = {
            bstack1l11l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᾱ"): bstack1l11l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᾲ").format(bstack1lllllll11l1_opy_),
            bstack1l11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᾳ"): bstack1l11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᾴ"),
            bstack1l11l11_opy_ (u"ࠫࡆࡩࡣࡦࡲࡷࠫ᾵"): bstack1l11l11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᾶ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1lllllll_opy_ + bstack1l11l11_opy_ (u"ࠨ࠯ࠣᾷ") + bstack1lllllll11ll_opy_.lstrip(bstack1l11l11_opy_ (u"ࠧ࠰ࠩᾸ"))
        try:
            if method == bstack1l11l11_opy_ (u"ࠨࡉࡈࡘࠬᾹ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l11l11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᾺ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l11l11_opy_ (u"ࠪࡔ࡚࡚ࠧΆ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l11l11_opy_ (u"࡚ࠦࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦᾼ").format(method))
            logger.debug(bstack1l11l11_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡭ࡢࡦࡨࠤࡹࡵࠠࡖࡔࡏ࠾ࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥ᾽").format(url, method))
            bstack1llllll1ll1l_opy_ = {}
            try:
                bstack1llllll1ll1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥι").format(e, response.text))
            if bstack1llllll1ll1l_opy_ is not None:
                bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ᾿")] = response.headers.get(
                    bstack1l11l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ῀"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ῁")] = response.status_code
            return bstack1llllll1ll1l_opy_
        except Exception as e:
            logger.error(bstack1l11l11_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨῂ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l11ll1l_opy_(bstack1lllllll1111_opy_, data):
        bstack1l11l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡓ࡙࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῃ")
        bstack1lllllll11l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩῄ"), bstack1l11l11_opy_ (u"࠭ࠧ῅"))
        headers = {
            bstack1l11l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧῆ"): bstack1l11l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫῇ").format(bstack1lllllll11l1_opy_),
            bstack1l11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨῈ"): bstack1l11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Έ")
        }
        response = requests.put(bstack1lllllll1111_opy_, headers=headers, json=data)
        bstack1llllll1ll1l_opy_ = {}
        try:
            bstack1llllll1ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l11l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥῊ").format(e))
            pass
        logger.debug(bstack1l11l11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥࡶࡵࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢΉ").format(bstack1llllll1ll1l_opy_))
        if bstack1llllll1ll1l_opy_ is not None:
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧῌ")] = response.headers.get(
                bstack1l11l11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ῍"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῎")] = response.status_code
        return bstack1llllll1ll1l_opy_
    @staticmethod
    def bstack11l1l1ll111_opy_(bstack1lllllll1111_opy_):
        bstack1l11l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡈࡇࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡩࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ῏")
        bstack1lllllll11l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧῐ"), bstack1l11l11_opy_ (u"ࠫࠬῑ"))
        headers = {
            bstack1l11l11_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬῒ"): bstack1l11l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩΐ").format(bstack1lllllll11l1_opy_),
            bstack1l11l11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭῔"): bstack1l11l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ῕")
        }
        response = requests.get(bstack1lllllll1111_opy_, headers=headers)
        bstack1llllll1ll1l_opy_ = {}
        try:
            bstack1llllll1ll1l_opy_ = response.json()
            logger.debug(bstack1l11l11_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡪࡩࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦῖ").format(bstack1llllll1ll1l_opy_))
        except Exception as e:
            logger.debug(bstack1l11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢῗ").format(e, response.text))
            pass
        if bstack1llllll1ll1l_opy_ is not None:
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬῘ")] = response.headers.get(
                bstack1l11l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ῑ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1llllll1ll1l_opy_[bstack1l11l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ὶ")] = response.status_code
        return bstack1llllll1ll1l_opy_
    @staticmethod
    def bstack111l11111l1_opy_(bstack11ll11l1l1l_opy_, payload):
        bstack1l11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡧ࡫ࡦࡵࠣࡥࠥࡖࡏࡔࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥ࠮ࡳࡵࡴࠬ࠾࡚ࠥࡨࡦࠢࡄࡔࡎࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡶࡡࡺ࡮ࡲࡥࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡆࡖࡉ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦΊ")
        try:
            url = bstack1l11l11_opy_ (u"ࠣࡽࢀ࠳ࢀࢃࠢ῜").format(bstack11l1lllllll_opy_, bstack11ll11l1l1l_opy_)
            bstack1lllllll11l1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭῝"), bstack1l11l11_opy_ (u"ࠪࠫ῞"))
            headers = {
                bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ῟"): bstack1l11l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨῠ").format(bstack1lllllll11l1_opy_),
                bstack1l11l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬῡ"): bstack1l11l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪῢ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(bstack1l11l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢ࠰ࠣࡗࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢΰ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡷࡹࡥࡣࡰ࡮࡯ࡩࡨࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡤࡢࡶࡤ࠾ࠥࢁࡽࠣῤ").format(e))
            return None