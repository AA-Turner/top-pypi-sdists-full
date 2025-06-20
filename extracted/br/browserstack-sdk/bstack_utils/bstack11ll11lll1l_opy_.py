# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll1ll11_opy_
logger = logging.getLogger(__name__)
class bstack11ll1l11111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111111l1l1l_opy_ = urljoin(builder, bstack11ll11_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨẶ"))
        if params:
            bstack111111l1l1l_opy_ += bstack11ll11_opy_ (u"ࠤࡂࡿࢂࠨặ").format(urlencode({bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẸ"): params.get(bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẹ"))}))
        return bstack11ll1l11111_opy_.bstack111111lll11_opy_(bstack111111l1l1l_opy_)
    @staticmethod
    def bstack11ll11lll11_opy_(builder,params=None):
        bstack111111l1l1l_opy_ = urljoin(builder, bstack11ll11_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭Ẻ"))
        if params:
            bstack111111l1l1l_opy_ += bstack11ll11_opy_ (u"ࠨ࠿ࡼࡿࠥẻ").format(urlencode({bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẼ"): params.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ"))}))
        return bstack11ll1l11111_opy_.bstack111111lll11_opy_(bstack111111l1l1l_opy_)
    @staticmethod
    def bstack111111lll11_opy_(bstack111111ll1l1_opy_):
        bstack111111l1ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧẾ"), os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧế"), bstack11ll11_opy_ (u"ࠫࠬỀ")))
        headers = {bstack11ll11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬề"): bstack11ll11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩỂ").format(bstack111111l1ll1_opy_)}
        response = requests.get(bstack111111ll1l1_opy_, headers=headers)
        bstack111111lll1l_opy_ = {}
        try:
            bstack111111lll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨể").format(e))
            pass
        if bstack111111lll1l_opy_ is not None:
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩỄ")] = response.headers.get(bstack11ll11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪễ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỆ")] = response.status_code
        return bstack111111lll1l_opy_
    @staticmethod
    def bstack111111l1lll_opy_(bstack111111ll11l_opy_, data):
        logger.debug(bstack11ll11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨệ"))
        return bstack11ll1l11111_opy_.bstack111111ll111_opy_(bstack11ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪỈ"), bstack111111ll11l_opy_, data=data)
    @staticmethod
    def bstack111111ll1ll_opy_(bstack111111ll11l_opy_, data):
        logger.debug(bstack11ll11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨỉ"))
        res = bstack11ll1l11111_opy_.bstack111111ll111_opy_(bstack11ll11_opy_ (u"ࠧࡈࡇࡗࠫỊ"), bstack111111ll11l_opy_, data=data)
        return res
    @staticmethod
    def bstack111111ll111_opy_(method, bstack111111ll11l_opy_, data=None, params=None, extra_headers=None):
        bstack111111l1ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬị"), bstack11ll11_opy_ (u"ࠩࠪỌ"))
        headers = {
            bstack11ll11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪọ"): bstack11ll11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧỎ").format(bstack111111l1ll1_opy_),
            bstack11ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫỏ"): bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩỐ"),
            bstack11ll11_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧố"): bstack11ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫỒ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll1ll11_opy_ + bstack11ll11_opy_ (u"ࠤ࠲ࠦồ") + bstack111111ll11l_opy_.lstrip(bstack11ll11_opy_ (u"ࠪ࠳ࠬỔ"))
        try:
            if method == bstack11ll11_opy_ (u"ࠫࡌࡋࡔࠨổ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪỖ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11ll11_opy_ (u"࠭ࡐࡖࡖࠪỗ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11ll11_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢỘ").format(method))
            logger.debug(bstack11ll11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨộ").format(url, method))
            bstack111111lll1l_opy_ = {}
            try:
                bstack111111lll1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨỚ").format(e, response.text))
            if bstack111111lll1l_opy_ is not None:
                bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫớ")] = response.headers.get(
                    bstack11ll11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬỜ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬờ")] = response.status_code
            return bstack111111lll1l_opy_
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤỞ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l1l1l1l_opy_(bstack111111ll1l1_opy_, data):
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧở")
        bstack111111l1ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬỠ"), bstack11ll11_opy_ (u"ࠩࠪỡ"))
        headers = {
            bstack11ll11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪỢ"): bstack11ll11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧợ").format(bstack111111l1ll1_opy_),
            bstack11ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫỤ"): bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩụ")
        }
        response = requests.put(bstack111111ll1l1_opy_, headers=headers, json=data)
        bstack111111lll1l_opy_ = {}
        try:
            bstack111111lll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨỦ").format(e))
            pass
        logger.debug(bstack11ll11_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥủ").format(bstack111111lll1l_opy_))
        if bstack111111lll1l_opy_ is not None:
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪỨ")] = response.headers.get(
                bstack11ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫứ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫỪ")] = response.status_code
        return bstack111111lll1l_opy_
    @staticmethod
    def bstack11l1ll111ll_opy_(bstack111111ll1l1_opy_):
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥừ")
        bstack111111l1ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỬ"), bstack11ll11_opy_ (u"ࠧࠨử"))
        headers = {
            bstack11ll11_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨỮ"): bstack11ll11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬữ").format(bstack111111l1ll1_opy_),
            bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỰ"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧự")
        }
        response = requests.get(bstack111111ll1l1_opy_, headers=headers)
        bstack111111lll1l_opy_ = {}
        try:
            bstack111111lll1l_opy_ = response.json()
            logger.debug(bstack11ll11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢỲ").format(bstack111111lll1l_opy_))
        except Exception as e:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥỳ").format(e, response.text))
            pass
        if bstack111111lll1l_opy_ is not None:
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨỴ")] = response.headers.get(
                bstack11ll11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩỵ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111lll1l_opy_[bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩỶ")] = response.status_code
        return bstack111111lll1l_opy_