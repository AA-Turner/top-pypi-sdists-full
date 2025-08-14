# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll11l11_opy_
logger = logging.getLogger(__name__)
class bstack11ll11l1l1l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lllllll11ll_opy_ = urljoin(builder, bstack1l1l1ll_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬᾨ"))
        if params:
            bstack1lllllll11ll_opy_ += bstack1l1l1ll_opy_ (u"ࠨ࠿ࡼࡿࠥᾩ").format(urlencode({bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᾪ"): params.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᾫ"))}))
        return bstack11ll11l1l1l_opy_.bstack1lllllll1ll1_opy_(bstack1lllllll11ll_opy_)
    @staticmethod
    def bstack11ll11l111l_opy_(builder,params=None):
        bstack1lllllll11ll_opy_ = urljoin(builder, bstack1l1l1ll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪᾬ"))
        if params:
            bstack1lllllll11ll_opy_ += bstack1l1l1ll_opy_ (u"ࠥࡃࢀࢃࠢᾭ").format(urlencode({bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᾮ"): params.get(bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᾯ"))}))
        return bstack11ll11l1l1l_opy_.bstack1lllllll1ll1_opy_(bstack1lllllll11ll_opy_)
    @staticmethod
    def bstack1lllllll1ll1_opy_(bstack1lllllll1l11_opy_):
        bstack1lllllll1l1l_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᾰ"), os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᾱ"), bstack1l1l1ll_opy_ (u"ࠨࠩᾲ")))
        headers = {bstack1l1l1ll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᾳ"): bstack1l1l1ll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᾴ").format(bstack1lllllll1l1l_opy_)}
        response = requests.get(bstack1lllllll1l11_opy_, headers=headers)
        bstack1lllllll111l_opy_ = {}
        try:
            bstack1lllllll111l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ᾵").format(e))
            pass
        if bstack1lllllll111l_opy_ is not None:
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ᾶ")] = response.headers.get(bstack1l1l1ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧᾷ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᾸ")] = response.status_code
        return bstack1lllllll111l_opy_
    @staticmethod
    def bstack1llllll1llll_opy_(bstack1llllll1lll1_opy_, data):
        logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࠥᾹ"))
        return bstack11ll11l1l1l_opy_.bstack1lllllll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᾺ"), bstack1llllll1lll1_opy_, data=data)
    @staticmethod
    def bstack1lllllll1111_opy_(bstack1llllll1lll1_opy_, data):
        logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥ࡭ࡥࡵࡖࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡵࠥΆ"))
        res = bstack11ll11l1l1l_opy_.bstack1lllllll11l1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡌࡋࡔࠨᾼ"), bstack1llllll1lll1_opy_, data=data)
        return res
    @staticmethod
    def bstack1lllllll11l1_opy_(method, bstack1llllll1lll1_opy_, data=None, params=None, extra_headers=None):
        bstack1lllllll1l1l_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᾽"), bstack1l1l1ll_opy_ (u"࠭ࠧι"))
        headers = {
            bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ᾿"): bstack1l1l1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ῀").format(bstack1lllllll1l1l_opy_),
            bstack1l1l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ῁"): bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ῂ"),
            bstack1l1l1ll_opy_ (u"ࠫࡆࡩࡣࡦࡲࡷࠫῃ"): bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨῄ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll11l11_opy_ + bstack1l1l1ll_opy_ (u"ࠨ࠯ࠣ῅") + bstack1llllll1lll1_opy_.lstrip(bstack1l1l1ll_opy_ (u"ࠧ࠰ࠩῆ"))
        try:
            if method == bstack1l1l1ll_opy_ (u"ࠨࡉࡈࡘࠬῇ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1l1ll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧῈ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1l1ll_opy_ (u"ࠪࡔ࡚࡚ࠧΈ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1l1ll_opy_ (u"࡚ࠦࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦῊ").format(method))
            logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡭ࡢࡦࡨࠤࡹࡵࠠࡖࡔࡏ࠾ࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥΉ").format(url, method))
            bstack1lllllll111l_opy_ = {}
            try:
                bstack1lllllll111l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥῌ").format(e, response.text))
            if bstack1lllllll111l_opy_ is not None:
                bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ῍")] = response.headers.get(
                    bstack1l1l1ll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ῎"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ῏")] = response.status_code
            return bstack1lllllll111l_opy_
        except Exception as e:
            logger.error(bstack1l1l1ll_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨῐ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l111lll_opy_(bstack1lllllll1l11_opy_, data):
        bstack1l1l1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡓ࡙࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤῑ")
        bstack1lllllll1l1l_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩῒ"), bstack1l1l1ll_opy_ (u"࠭ࠧΐ"))
        headers = {
            bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ῔"): bstack1l1l1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ῕").format(bstack1lllllll1l1l_opy_),
            bstack1l1l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨῖ"): bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ῗ")
        }
        response = requests.put(bstack1lllllll1l11_opy_, headers=headers, json=data)
        bstack1lllllll111l_opy_ = {}
        try:
            bstack1lllllll111l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥῘ").format(e))
            pass
        logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥࡶࡵࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢῙ").format(bstack1lllllll111l_opy_))
        if bstack1lllllll111l_opy_ is not None:
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧῚ")] = response.headers.get(
                bstack1l1l1ll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨΊ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ῜")] = response.status_code
        return bstack1lllllll111l_opy_
    @staticmethod
    def bstack11l1l11l11l_opy_(bstack1lllllll1l11_opy_):
        bstack1l1l1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡈࡇࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡩࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ῝")
        bstack1lllllll1l1l_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ῞"), bstack1l1l1ll_opy_ (u"ࠫࠬ῟"))
        headers = {
            bstack1l1l1ll_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬῠ"): bstack1l1l1ll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩῡ").format(bstack1lllllll1l1l_opy_),
            bstack1l1l1ll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ῢ"): bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫΰ")
        }
        response = requests.get(bstack1lllllll1l11_opy_, headers=headers)
        bstack1lllllll111l_opy_ = {}
        try:
            bstack1lllllll111l_opy_ = response.json()
            logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡪࡩࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦῤ").format(bstack1lllllll111l_opy_))
        except Exception as e:
            logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢῥ").format(e, response.text))
            pass
        if bstack1lllllll111l_opy_ is not None:
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬῦ")] = response.headers.get(
                bstack1l1l1ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ῧ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lllllll111l_opy_[bstack1l1l1ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ῠ")] = response.status_code
        return bstack1lllllll111l_opy_
    @staticmethod
    def bstack111l1111111_opy_(bstack11ll11ll111_opy_, payload):
        bstack1l1l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡧ࡫ࡦࡵࠣࡥࠥࡖࡏࡔࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥ࠮ࡳࡵࡴࠬ࠾࡚ࠥࡨࡦࠢࡄࡔࡎࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡶࡡࡺ࡮ࡲࡥࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡆࡖࡉ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦῩ")
        try:
            url = bstack1l1l1ll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃࠢῪ").format(bstack11l1ll11l11_opy_, bstack11ll11ll111_opy_)
            bstack1lllllll1l1l_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ύ"), bstack1l1l1ll_opy_ (u"ࠪࠫῬ"))
            headers = {
                bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ῭"): bstack1l1l1ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ΅").format(bstack1lllllll1l1l_opy_),
                bstack1l1l1ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ`"): bstack1l1l1ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ῰")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(bstack1l1l1ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢ࠰ࠣࡗࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ῱").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡷࡹࡥࡣࡰ࡮࡯ࡩࡨࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡤࡢࡶࡤ࠾ࠥࢁࡽࠣῲ").format(e))
            return None