# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111l11ll1ll_opy_
logger = logging.getLogger(__name__)
class bstack111l1ll1111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1lll1l11l_opy_ = urljoin(builder, bstack1ll11_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪ⒒"))
        if params:
            bstack1ll1lll1l11l_opy_ += bstack1ll11_opy_ (u"ࠦࡄࢁࡽࠣ⒓").format(urlencode({bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⒔"): params.get(bstack1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⒕"))}))
        return bstack111l1ll1111_opy_.bstack1ll1llll1111_opy_(bstack1ll1lll1l11l_opy_)
    @staticmethod
    def bstack111l1ll1l1l_opy_(builder,params=None):
        bstack1ll1lll1l11l_opy_ = urljoin(builder, bstack1ll11_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ⒖"))
        if params:
            bstack1ll1lll1l11l_opy_ += bstack1ll11_opy_ (u"ࠣࡁࡾࢁࠧ⒗").format(urlencode({bstack1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⒘"): params.get(bstack1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⒙"))}))
        return bstack111l1ll1111_opy_.bstack1ll1llll1111_opy_(bstack1ll1lll1l11l_opy_)
    @staticmethod
    def bstack1ll1llll1111_opy_(bstack1ll1llll111l_opy_):
        bstack1ll1lll1ll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⒚"), os.environ.get(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⒛"), bstack1ll11_opy_ (u"࠭ࠧ⒜")))
        headers = {bstack1ll11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⒝"): bstack1ll11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⒞").format(bstack1ll1lll1ll11_opy_)}
        response = requests.get(bstack1ll1llll111l_opy_, headers=headers)
        bstack1ll1lll1lll1_opy_ = {}
        try:
            bstack1ll1lll1lll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⒟").format(e))
            pass
        if bstack1ll1lll1lll1_opy_ is not None:
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⒠")] = response.headers.get(bstack1ll11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⒡"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⒢")] = response.status_code
        return bstack1ll1lll1lll1_opy_
    @staticmethod
    def bstack1ll1lll1l1ll_opy_(bstack1ll1lll1l111_opy_, data):
        logger.debug(bstack1ll11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࠣ⒣"))
        return bstack111l1ll1111_opy_.bstack1ll1lll1llll_opy_(bstack1ll11_opy_ (u"ࠧࡑࡑࡖࡘࠬ⒤"), bstack1ll1lll1l111_opy_, data=data)
    @staticmethod
    def bstack1ll1lll1ll1l_opy_(bstack1ll1lll1l111_opy_, data):
        logger.debug(bstack1ll11_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣ࡫ࡪࡺࡔࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡳࠣ⒥"))
        res = bstack111l1ll1111_opy_.bstack1ll1lll1llll_opy_(bstack1ll11_opy_ (u"ࠩࡊࡉ࡙࠭⒦"), bstack1ll1lll1l111_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1lll1llll_opy_(method, bstack1ll1lll1l111_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1lll1ll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⒧"), bstack1ll11_opy_ (u"ࠫࠬ⒨"))
        headers = {
            bstack1ll11_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⒩"): bstack1ll11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⒪").format(bstack1ll1lll1ll11_opy_),
            bstack1ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⒫"): bstack1ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⒬"),
            bstack1ll11_opy_ (u"ࠩࡄࡧࡨ࡫ࡰࡵࠩ⒭"): bstack1ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⒮")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111l11ll1ll_opy_ + bstack1ll11_opy_ (u"ࠦ࠴ࠨ⒯") + bstack1ll1lll1l111_opy_.lstrip(bstack1ll11_opy_ (u"ࠬ࠵ࠧ⒰"))
        try:
            if method == bstack1ll11_opy_ (u"࠭ࡇࡆࡖࠪ⒱"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll11_opy_ (u"ࠧࡑࡑࡖࡘࠬ⒲"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll11_opy_ (u"ࠨࡒࡘࡘࠬ⒳"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll11_opy_ (u"ࠤࡘࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤ⒴").format(method))
            logger.debug(bstack1ll11_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡲࡧࡤࡦࠢࡷࡳ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ⒵").format(url, method))
            bstack1ll1lll1lll1_opy_ = {}
            try:
                bstack1ll1lll1lll1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣⒶ").format(e, response.text))
            if bstack1ll1lll1lll1_opy_ is not None:
                bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ⓑ")] = response.headers.get(
                    bstack1ll11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧⒸ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⒹ")] = response.status_code
            return bstack1ll1lll1lll1_opy_
        except Exception as e:
            logger.error(bstack1ll11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦⒺ").format(e, url))
            return None
    @staticmethod
    def bstack1111ll1ll11_opy_(bstack1ll1llll111l_opy_, data):
        bstack1ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢⒻ")
        bstack1ll1lll1ll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⒼ"), bstack1ll11_opy_ (u"ࠫࠬⒽ"))
        headers = {
            bstack1ll11_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬⒾ"): bstack1ll11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩⒿ").format(bstack1ll1lll1ll11_opy_),
            bstack1ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭Ⓚ"): bstack1ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫⓁ")
        }
        response = requests.put(bstack1ll1llll111l_opy_, headers=headers, json=data)
        bstack1ll1lll1lll1_opy_ = {}
        try:
            bstack1ll1lll1lll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣⓂ").format(e))
            pass
        logger.debug(bstack1ll11_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧⓃ").format(bstack1ll1lll1lll1_opy_))
        if bstack1ll1lll1lll1_opy_ is not None:
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬⓄ")] = response.headers.get(
                bstack1ll11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ⓟ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ⓠ")] = response.status_code
        return bstack1ll1lll1lll1_opy_
    @staticmethod
    def bstack1111lll11ll_opy_(bstack1ll1llll111l_opy_):
        bstack1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧⓇ")
        bstack1ll1lll1ll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬⓈ"), bstack1ll11_opy_ (u"ࠩࠪⓉ"))
        headers = {
            bstack1ll11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪⓊ"): bstack1ll11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧⓋ").format(bstack1ll1lll1ll11_opy_),
            bstack1ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫⓌ"): bstack1ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩⓍ")
        }
        response = requests.get(bstack1ll1llll111l_opy_, headers=headers)
        bstack1ll1lll1lll1_opy_ = {}
        try:
            bstack1ll1lll1lll1_opy_ = response.json()
            logger.debug(bstack1ll11_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤⓎ").format(bstack1ll1lll1lll1_opy_))
        except Exception as e:
            logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧⓏ").format(e, response.text))
            pass
        if bstack1ll1lll1lll1_opy_ is not None:
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪⓐ")] = response.headers.get(
                bstack1ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫⓑ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lll1lll1_opy_[bstack1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫⓒ")] = response.status_code
        return bstack1ll1lll1lll1_opy_
    @staticmethod
    def bstack1llll1l1111l_opy_(bstack111l1ll1lll_opy_, payload):
        bstack1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡰ࡫ࡳࠡࡣࠣࡔࡔ࡙ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡂࡒࡌࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡵࡩࡶࡻࡥࡴࡶࠣࡴࡦࡿ࡬ࡰࡣࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡄࡔࡎ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤⓓ")
        try:
            url = bstack1ll11_opy_ (u"ࠨࡻࡾ࠱ࡾࢁࠧⓔ").format(bstack111l11ll1ll_opy_, bstack111l1ll1lll_opy_)
            bstack1ll1lll1ll11_opy_ = os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫⓕ"), bstack1ll11_opy_ (u"ࠨࠩⓖ"))
            headers = {
                bstack1ll11_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩⓗ"): bstack1ll11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ⓘ").format(bstack1ll1lll1ll11_opy_),
                bstack1ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪⓙ"): bstack1ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨⓚ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1lll1l1l1_opy_ = [200, 202]
            if response.status_code in bstack1ll1lll1l1l1_opy_:
                return response.json()
            else:
                logger.error(bstack1ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧ࠮ࠡࡕࡷࡥࡹࡻࡳ࠻ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧⓛ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡵࡷࡣࡨࡵ࡬࡭ࡧࡦࡸࡤࡨࡵࡪ࡮ࡧࡣࡩࡧࡴࡢ࠼ࠣࡿࢂࠨⓜ").format(e))
            return None