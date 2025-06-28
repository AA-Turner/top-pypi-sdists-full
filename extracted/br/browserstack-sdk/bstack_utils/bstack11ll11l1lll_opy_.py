# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11ll1111lll_opy_
logger = logging.getLogger(__name__)
class bstack11ll11ll11l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111111l1111_opy_ = urljoin(builder, bstack1l1ll1_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠭ỗ"))
        if params:
            bstack111111l1111_opy_ += bstack1l1ll1_opy_ (u"ࠢࡀࡽࢀࠦỘ").format(urlencode({bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨộ"): params.get(bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỚ"))}))
        return bstack11ll11ll11l_opy_.bstack111111l111l_opy_(bstack111111l1111_opy_)
    @staticmethod
    def bstack11ll11ll1l1_opy_(builder,params=None):
        bstack111111l1111_opy_ = urljoin(builder, bstack1l1ll1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫớ"))
        if params:
            bstack111111l1111_opy_ += bstack1l1ll1_opy_ (u"ࠦࡄࢁࡽࠣỜ").format(urlencode({bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬờ"): params.get(bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ở"))}))
        return bstack11ll11ll11l_opy_.bstack111111l111l_opy_(bstack111111l1111_opy_)
    @staticmethod
    def bstack111111l111l_opy_(bstack111111l1ll1_opy_):
        bstack111111l11l1_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬở"), os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬỠ"), bstack1l1ll1_opy_ (u"ࠩࠪỡ")))
        headers = {bstack1l1ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪỢ"): bstack1l1ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧợ").format(bstack111111l11l1_opy_)}
        response = requests.get(bstack111111l1ll1_opy_, headers=headers)
        bstack111111l1l1l_opy_ = {}
        try:
            bstack111111l1l1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦỤ").format(e))
            pass
        if bstack111111l1l1l_opy_ is not None:
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧụ")] = response.headers.get(bstack1l1ll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨỦ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨủ")] = response.status_code
        return bstack111111l1l1l_opy_
    @staticmethod
    def bstack111111l11ll_opy_(bstack1111111llll_opy_, data):
        logger.debug(bstack1l1ll1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࠦỨ"))
        return bstack11ll11ll11l_opy_.bstack111111l1l11_opy_(bstack1l1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨứ"), bstack1111111llll_opy_, data=data)
    @staticmethod
    def bstack111111l1lll_opy_(bstack1111111llll_opy_, data):
        logger.debug(bstack1l1ll1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡧࡦࡶࡗࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡶࠦỪ"))
        res = bstack11ll11ll11l_opy_.bstack111111l1l11_opy_(bstack1l1ll1_opy_ (u"ࠬࡍࡅࡕࠩừ"), bstack1111111llll_opy_, data=data)
        return res
    @staticmethod
    def bstack111111l1l11_opy_(method, bstack1111111llll_opy_, data=None, params=None, extra_headers=None):
        bstack111111l11l1_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỬ"), bstack1l1ll1_opy_ (u"ࠧࠨử"))
        headers = {
            bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨỮ"): bstack1l1ll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬữ").format(bstack111111l11l1_opy_),
            bstack1l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỰ"): bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧự"),
            bstack1l1ll1_opy_ (u"ࠬࡇࡣࡤࡧࡳࡸࠬỲ"): bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩỳ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11ll1111lll_opy_ + bstack1l1ll1_opy_ (u"ࠢ࠰ࠤỴ") + bstack1111111llll_opy_.lstrip(bstack1l1ll1_opy_ (u"ࠨ࠱ࠪỵ"))
        try:
            if method == bstack1l1ll1_opy_ (u"ࠩࡊࡉ࡙࠭Ỷ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨỷ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1ll1_opy_ (u"ࠫࡕ࡛ࡔࠨỸ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1ll1_opy_ (u"࡛ࠧ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧỹ").format(method))
            logger.debug(bstack1l1ll1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡮ࡣࡧࡩࠥࡺ࡯ࠡࡗࡕࡐ࠿ࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦỺ").format(url, method))
            bstack111111l1l1l_opy_ = {}
            try:
                bstack111111l1l1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦỻ").format(e, response.text))
            if bstack111111l1l1l_opy_ is not None:
                bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩỼ")] = response.headers.get(
                    bstack1l1ll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪỽ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỾ")] = response.status_code
            return bstack111111l1l1l_opy_
        except Exception as e:
            logger.error(bstack1l1ll1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢỿ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l1l1l11_opy_(bstack111111l1ll1_opy_, data):
        bstack1l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡔ࡚࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥἀ")
        bstack111111l11l1_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἁ"), bstack1l1ll1_opy_ (u"ࠧࠨἂ"))
        headers = {
            bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨἃ"): bstack1l1ll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬἄ").format(bstack111111l11l1_opy_),
            bstack1l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩἅ"): bstack1l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧἆ")
        }
        response = requests.put(bstack111111l1ll1_opy_, headers=headers, json=data)
        bstack111111l1l1l_opy_ = {}
        try:
            bstack111111l1l1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦἇ").format(e))
            pass
        logger.debug(bstack1l1ll1_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡰࡶࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣἈ").format(bstack111111l1l1l_opy_))
        if bstack111111l1l1l_opy_ is not None:
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨἉ")] = response.headers.get(
                bstack1l1ll1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩἊ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩἋ")] = response.status_code
        return bstack111111l1l1l_opy_
    @staticmethod
    def bstack11l1l11ll1l_opy_(bstack111111l1ll1_opy_):
        bstack1l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡉࡈࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡪࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣἌ")
        bstack111111l11l1_opy_ = os.environ.get(bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨἍ"), bstack1l1ll1_opy_ (u"ࠬ࠭Ἆ"))
        headers = {
            bstack1l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ἇ"): bstack1l1ll1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪἐ").format(bstack111111l11l1_opy_),
            bstack1l1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧἑ"): bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬἒ")
        }
        response = requests.get(bstack111111l1ll1_opy_, headers=headers)
        bstack111111l1l1l_opy_ = {}
        try:
            bstack111111l1l1l_opy_ = response.json()
            logger.debug(bstack1l1ll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣ࡫ࡪࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧἓ").format(bstack111111l1l1l_opy_))
        except Exception as e:
            logger.debug(bstack1l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣἔ").format(e, response.text))
            pass
        if bstack111111l1l1l_opy_ is not None:
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ἕ")] = response.headers.get(
                bstack1l1ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ἖"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111l1l1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ἗")] = response.status_code
        return bstack111111l1l1l_opy_