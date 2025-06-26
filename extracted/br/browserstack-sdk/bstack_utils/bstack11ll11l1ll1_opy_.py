# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll1l111_opy_
logger = logging.getLogger(__name__)
class bstack11ll11ll111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111111l11ll_opy_ = urljoin(builder, bstack11ll1l1_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠭ỗ"))
        if params:
            bstack111111l11ll_opy_ += bstack11ll1l1_opy_ (u"ࠢࡀࡽࢀࠦỘ").format(urlencode({bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨộ"): params.get(bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỚ"))}))
        return bstack11ll11ll111_opy_.bstack1111111llll_opy_(bstack111111l11ll_opy_)
    @staticmethod
    def bstack11ll11l1lll_opy_(builder,params=None):
        bstack111111l11ll_opy_ = urljoin(builder, bstack11ll1l1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫớ"))
        if params:
            bstack111111l11ll_opy_ += bstack11ll1l1_opy_ (u"ࠦࡄࢁࡽࠣỜ").format(urlencode({bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬờ"): params.get(bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ở"))}))
        return bstack11ll11ll111_opy_.bstack1111111llll_opy_(bstack111111l11ll_opy_)
    @staticmethod
    def bstack1111111llll_opy_(bstack111111l1l1l_opy_):
        bstack111111l1l11_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬở"), os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬỠ"), bstack11ll1l1_opy_ (u"ࠩࠪỡ")))
        headers = {bstack11ll1l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪỢ"): bstack11ll1l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧợ").format(bstack111111l1l11_opy_)}
        response = requests.get(bstack111111l1l1l_opy_, headers=headers)
        bstack111111l111l_opy_ = {}
        try:
            bstack111111l111l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦỤ").format(e))
            pass
        if bstack111111l111l_opy_ is not None:
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧụ")] = response.headers.get(bstack11ll1l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨỦ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨủ")] = response.status_code
        return bstack111111l111l_opy_
    @staticmethod
    def bstack111111l1ll1_opy_(bstack111111l11l1_opy_, data):
        logger.debug(bstack11ll1l1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࠦỨ"))
        return bstack11ll11ll111_opy_.bstack111111l1111_opy_(bstack11ll1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨứ"), bstack111111l11l1_opy_, data=data)
    @staticmethod
    def bstack1111111lll1_opy_(bstack111111l11l1_opy_, data):
        logger.debug(bstack11ll1l1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡧࡦࡶࡗࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡶࠦỪ"))
        res = bstack11ll11ll111_opy_.bstack111111l1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡍࡅࡕࠩừ"), bstack111111l11l1_opy_, data=data)
        return res
    @staticmethod
    def bstack111111l1111_opy_(method, bstack111111l11l1_opy_, data=None, params=None, extra_headers=None):
        bstack111111l1l11_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỬ"), bstack11ll1l1_opy_ (u"ࠧࠨử"))
        headers = {
            bstack11ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨỮ"): bstack11ll1l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬữ").format(bstack111111l1l11_opy_),
            bstack11ll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỰ"): bstack11ll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧự"),
            bstack11ll1l1_opy_ (u"ࠬࡇࡣࡤࡧࡳࡸࠬỲ"): bstack11ll1l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩỳ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll1l111_opy_ + bstack11ll1l1_opy_ (u"ࠢ࠰ࠤỴ") + bstack111111l11l1_opy_.lstrip(bstack11ll1l1_opy_ (u"ࠨ࠱ࠪỵ"))
        try:
            if method == bstack11ll1l1_opy_ (u"ࠩࡊࡉ࡙࠭Ỷ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11ll1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨỷ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11ll1l1_opy_ (u"ࠫࡕ࡛ࡔࠨỸ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11ll1l1_opy_ (u"࡛ࠧ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧỹ").format(method))
            logger.debug(bstack11ll1l1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡮ࡣࡧࡩࠥࡺ࡯ࠡࡗࡕࡐ࠿ࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦỺ").format(url, method))
            bstack111111l111l_opy_ = {}
            try:
                bstack111111l111l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11ll1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦỻ").format(e, response.text))
            if bstack111111l111l_opy_ is not None:
                bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩỼ")] = response.headers.get(
                    bstack11ll1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪỽ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỾ")] = response.status_code
            return bstack111111l111l_opy_
        except Exception as e:
            logger.error(bstack11ll1l1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢỿ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l11lll1_opy_(bstack111111l1l1l_opy_, data):
        bstack11ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡔ࡚࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥἀ")
        bstack111111l1l11_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἁ"), bstack11ll1l1_opy_ (u"ࠧࠨἂ"))
        headers = {
            bstack11ll1l1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨἃ"): bstack11ll1l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬἄ").format(bstack111111l1l11_opy_),
            bstack11ll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩἅ"): bstack11ll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧἆ")
        }
        response = requests.put(bstack111111l1l1l_opy_, headers=headers, json=data)
        bstack111111l111l_opy_ = {}
        try:
            bstack111111l111l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦἇ").format(e))
            pass
        logger.debug(bstack11ll1l1_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡰࡶࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣἈ").format(bstack111111l111l_opy_))
        if bstack111111l111l_opy_ is not None:
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨἉ")] = response.headers.get(
                bstack11ll1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩἊ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩἋ")] = response.status_code
        return bstack111111l111l_opy_
    @staticmethod
    def bstack11l1l1lll1l_opy_(bstack111111l1l1l_opy_):
        bstack11ll1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡉࡈࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡪࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣἌ")
        bstack111111l1l11_opy_ = os.environ.get(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨἍ"), bstack11ll1l1_opy_ (u"ࠬ࠭Ἆ"))
        headers = {
            bstack11ll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ἇ"): bstack11ll1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪἐ").format(bstack111111l1l11_opy_),
            bstack11ll1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧἑ"): bstack11ll1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬἒ")
        }
        response = requests.get(bstack111111l1l1l_opy_, headers=headers)
        bstack111111l111l_opy_ = {}
        try:
            bstack111111l111l_opy_ = response.json()
            logger.debug(bstack11ll1l1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣ࡫ࡪࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧἓ").format(bstack111111l111l_opy_))
        except Exception as e:
            logger.debug(bstack11ll1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣἔ").format(e, response.text))
            pass
        if bstack111111l111l_opy_ is not None:
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ἕ")] = response.headers.get(
                bstack11ll1l1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ἖"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111l111l_opy_[bstack11ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ἗")] = response.status_code
        return bstack111111l111l_opy_