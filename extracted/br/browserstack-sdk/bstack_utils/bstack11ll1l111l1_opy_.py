# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll1ll11_opy_
logger = logging.getLogger(__name__)
class bstack11ll11lllll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111111l1lll_opy_ = urljoin(builder, bstack1l1l1l1_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩặ"))
        if params:
            bstack111111l1lll_opy_ += bstack1l1l1l1_opy_ (u"ࠥࡃࢀࢃࠢẸ").format(urlencode({bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẹ"): params.get(bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẺ"))}))
        return bstack11ll11lllll_opy_.bstack111111ll11l_opy_(bstack111111l1lll_opy_)
    @staticmethod
    def bstack11ll11lll1l_opy_(builder,params=None):
        bstack111111l1lll_opy_ = urljoin(builder, bstack1l1l1l1_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧẻ"))
        if params:
            bstack111111l1lll_opy_ += bstack1l1l1l1_opy_ (u"ࠢࡀࡽࢀࠦẼ").format(urlencode({bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ"): params.get(bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẾ"))}))
        return bstack11ll11lllll_opy_.bstack111111ll11l_opy_(bstack111111l1lll_opy_)
    @staticmethod
    def bstack111111ll11l_opy_(bstack111111l1l1l_opy_):
        bstack111111l1ll1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨế"), os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỀ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ề")))
        headers = {bstack1l1l1l1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ể"): bstack1l1l1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪể").format(bstack111111l1ll1_opy_)}
        response = requests.get(bstack111111l1l1l_opy_, headers=headers)
        bstack111111ll111_opy_ = {}
        try:
            bstack111111ll111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢỄ").format(e))
            pass
        if bstack111111ll111_opy_ is not None:
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪễ")] = response.headers.get(bstack1l1l1l1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫỆ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫệ")] = response.status_code
        return bstack111111ll111_opy_
    @staticmethod
    def bstack111111ll1l1_opy_(bstack111111lll1l_opy_, data):
        logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢỈ"))
        return bstack11ll11lllll_opy_.bstack111111ll1ll_opy_(bstack1l1l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫỉ"), bstack111111lll1l_opy_, data=data)
    @staticmethod
    def bstack111111lll11_opy_(bstack111111lll1l_opy_, data):
        logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢỊ"))
        res = bstack11ll11lllll_opy_.bstack111111ll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡉࡈࡘࠬị"), bstack111111lll1l_opy_, data=data)
        return res
    @staticmethod
    def bstack111111ll1ll_opy_(method, bstack111111lll1l_opy_, data=None, params=None, extra_headers=None):
        bstack111111l1ll1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ọ"), bstack1l1l1l1_opy_ (u"ࠪࠫọ"))
        headers = {
            bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫỎ"): bstack1l1l1l1_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨỏ").format(bstack111111l1ll1_opy_),
            bstack1l1l1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬỐ"): bstack1l1l1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪố"),
            bstack1l1l1l1_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨỒ"): bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬồ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll1ll11_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠳ࠧỔ") + bstack111111lll1l_opy_.lstrip(bstack1l1l1l1_opy_ (u"ࠫ࠴࠭ổ"))
        try:
            if method == bstack1l1l1l1_opy_ (u"ࠬࡍࡅࡕࠩỖ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫỗ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1l1l1_opy_ (u"ࠧࡑࡗࡗࠫỘ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣộ").format(method))
            logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢỚ").format(url, method))
            bstack111111ll111_opy_ = {}
            try:
                bstack111111ll111_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢớ").format(e, response.text))
            if bstack111111ll111_opy_ is not None:
                bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬỜ")] = response.headers.get(
                    bstack1l1l1l1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ờ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ở")] = response.status_code
            return bstack111111ll111_opy_
        except Exception as e:
            logger.error(bstack1l1l1l1_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥở").format(e, url))
            return None
    @staticmethod
    def bstack11l1l1l11ll_opy_(bstack111111l1l1l_opy_, data):
        bstack1l1l1l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨỠ")
        bstack111111l1ll1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ỡ"), bstack1l1l1l1_opy_ (u"ࠪࠫỢ"))
        headers = {
            bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫợ"): bstack1l1l1l1_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨỤ").format(bstack111111l1ll1_opy_),
            bstack1l1l1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬụ"): bstack1l1l1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪỦ")
        }
        response = requests.put(bstack111111l1l1l_opy_, headers=headers, json=data)
        bstack111111ll111_opy_ = {}
        try:
            bstack111111ll111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢủ").format(e))
            pass
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦỨ").format(bstack111111ll111_opy_))
        if bstack111111ll111_opy_ is not None:
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫứ")] = response.headers.get(
                bstack1l1l1l1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬỪ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬừ")] = response.status_code
        return bstack111111ll111_opy_
    @staticmethod
    def bstack11l1ll11lll_opy_(bstack111111l1l1l_opy_):
        bstack1l1l1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦỬ")
        bstack111111l1ll1_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫử"), bstack1l1l1l1_opy_ (u"ࠨࠩỮ"))
        headers = {
            bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩữ"): bstack1l1l1l1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭Ự").format(bstack111111l1ll1_opy_),
            bstack1l1l1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪự"): bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨỲ")
        }
        response = requests.get(bstack111111l1l1l_opy_, headers=headers)
        bstack111111ll111_opy_ = {}
        try:
            bstack111111ll111_opy_ = response.json()
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣỳ").format(bstack111111ll111_opy_))
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦỴ").format(e, response.text))
            pass
        if bstack111111ll111_opy_ is not None:
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩỵ")] = response.headers.get(
                bstack1l1l1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪỶ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack111111ll111_opy_[bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỷ")] = response.status_code
        return bstack111111ll111_opy_