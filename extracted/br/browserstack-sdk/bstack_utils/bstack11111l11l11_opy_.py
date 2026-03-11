# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack1lll1lll1l11_opy_
logger = logging.getLogger(__name__)
class bstack111111ll111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lll1lllll1l_opy_ = urljoin(builder, bstack1ll111_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩṿ"))
        if params:
            bstack1lll1lllll1l_opy_ += bstack1ll111_opy_ (u"ࠥࡃࢀࢃࠢẀ").format(urlencode({bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẁ"): params.get(bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẂ"))}))
        return bstack111111ll111_opy_.bstack1lll1lll11ll_opy_(bstack1lll1lllll1l_opy_)
    @staticmethod
    def bstack1lll1lll1lll_opy_(builder,params=None):
        bstack1lll1lllll1l_opy_ = urljoin(builder, bstack1ll111_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧẃ"))
        if params:
            bstack1lll1lllll1l_opy_ += bstack1ll111_opy_ (u"ࠢࡀࡽࢀࠦẄ").format(urlencode({bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẅ"): params.get(bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẆ"))}))
        return bstack111111ll111_opy_.bstack1lll1lll11ll_opy_(bstack1lll1lllll1l_opy_)
    @staticmethod
    def bstack1lll1lll11ll_opy_(bstack1lll1lll1ll1_opy_):
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨẇ"), os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẈ"), bstack1ll111_opy_ (u"ࠬ࠭ẉ")))
        headers = {bstack1ll111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ẋ"): bstack1ll111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪẋ").format(bstack1lll1llll1l1_opy_)}
        response = requests.get(bstack1lll1lll1ll1_opy_, headers=headers)
        bstack1lll1lllllll_opy_ = {}
        try:
            bstack1lll1lllllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢẌ").format(e))
            pass
        if bstack1lll1lllllll_opy_ is not None:
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪẍ")] = response.headers.get(bstack1ll111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫẎ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫẏ")] = response.status_code
        return bstack1lll1lllllll_opy_
    @staticmethod
    def bstack1lll1llll11l_opy_(bstack1lll1lllll11_opy_, data):
        logger.debug(bstack1ll111_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢẐ"))
        return bstack111111ll111_opy_.bstack1lll1llll1ll_opy_(bstack1ll111_opy_ (u"࠭ࡐࡐࡕࡗࠫẑ"), bstack1lll1lllll11_opy_, data=data)
    @staticmethod
    def bstack1lll1llll111_opy_(bstack1lll1lllll11_opy_, data):
        logger.debug(bstack1ll111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢẒ"))
        res = bstack111111ll111_opy_.bstack1lll1llll1ll_opy_(bstack1ll111_opy_ (u"ࠨࡉࡈࡘࠬẓ"), bstack1lll1lllll11_opy_, data=data)
        return res
    @staticmethod
    def bstack1lll1llll1ll_opy_(method, bstack1lll1lllll11_opy_, data=None, params=None, extra_headers=None):
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ẕ"), bstack1ll111_opy_ (u"ࠪࠫẕ"))
        headers = {
            bstack1ll111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫẖ"): bstack1ll111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨẗ").format(bstack1lll1llll1l1_opy_),
            bstack1ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬẘ"): bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪẙ"),
            bstack1ll111_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨẚ"): bstack1ll111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬẛ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack1lll1lll1l11_opy_ + bstack1ll111_opy_ (u"ࠥ࠳ࠧẜ") + bstack1lll1lllll11_opy_.lstrip(bstack1ll111_opy_ (u"ࠫ࠴࠭ẝ"))
        try:
            if method == bstack1ll111_opy_ (u"ࠬࡍࡅࡕࠩẞ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll111_opy_ (u"࠭ࡐࡐࡕࡗࠫẟ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll111_opy_ (u"ࠧࡑࡗࡗࠫẠ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll111_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣạ").format(method))
            logger.debug(bstack1ll111_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢẢ").format(url, method))
            bstack1lll1lllllll_opy_ = {}
            try:
                bstack1lll1lllllll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢả").format(e, response.text))
            if bstack1lll1lllllll_opy_ is not None:
                bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬẤ")] = response.headers.get(
                    bstack1ll111_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ấ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ầ")] = response.status_code
            return bstack1lll1lllllll_opy_
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥầ").format(e, url))
            return None
    @staticmethod
    def bstack1lll1lll1l1l_opy_(bstack1lll1lll1ll1_opy_, data):
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨẨ")
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ẩ"), bstack1ll111_opy_ (u"ࠪࠫẪ"))
        headers = {
            bstack1ll111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫẫ"): bstack1ll111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨẬ").format(bstack1lll1llll1l1_opy_),
            bstack1ll111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬậ"): bstack1ll111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪẮ")
        }
        response = requests.put(bstack1lll1lll1ll1_opy_, headers=headers, json=data)
        bstack1lll1lllllll_opy_ = {}
        try:
            bstack1lll1lllllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢắ").format(e))
            pass
        logger.debug(bstack1ll111_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦẰ").format(bstack1lll1lllllll_opy_))
        if bstack1lll1lllllll_opy_ is not None:
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫằ")] = response.headers.get(
                bstack1ll111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬẲ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬẳ")] = response.status_code
        return bstack1lll1lllllll_opy_
    @staticmethod
    def bstack1llll1111111_opy_(bstack1lll1lll1ll1_opy_):
        bstack1ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦẴ")
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫẵ"), bstack1ll111_opy_ (u"ࠨࠩẶ"))
        headers = {
            bstack1ll111_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩặ"): bstack1ll111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭Ẹ").format(bstack1lll1llll1l1_opy_),
            bstack1ll111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪẹ"): bstack1ll111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨẺ")
        }
        response = requests.get(bstack1lll1lll1ll1_opy_, headers=headers)
        bstack1lll1lllllll_opy_ = {}
        try:
            bstack1lll1lllllll_opy_ = response.json()
            logger.debug(bstack1ll111_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣẻ").format(bstack1lll1lllllll_opy_))
        except Exception as e:
            logger.debug(bstack1ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦẼ").format(e, response.text))
            pass
        if bstack1lll1lllllll_opy_ is not None:
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩẽ")] = response.headers.get(
                bstack1ll111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪẾ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lllllll_opy_[bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪế")] = response.status_code
        return bstack1lll1lllllll_opy_
    @staticmethod
    def bstack11111lll11l_opy_(bstack11111llllll_opy_, payload):
        bstack1ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡏࡤ࡯ࡪࡹࠠࡢࠢࡓࡓࡘ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡁࡑࡋࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࠬࡩ࡯ࡣࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡳࡥࡾࡲ࡯ࡢࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡃࡓࡍ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣỀ")
        try:
            url = bstack1ll111_opy_ (u"ࠧࢁࡽ࠰ࡽࢀࠦề").format(bstack1lll1lll1l11_opy_, bstack11111llllll_opy_)
            bstack1lll1llll1l1_opy_ = os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỂ"), bstack1ll111_opy_ (u"ࠧࠨể"))
            headers = {
                bstack1ll111_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨỄ"): bstack1ll111_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬễ").format(bstack1lll1llll1l1_opy_),
                bstack1ll111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỆ"): bstack1ll111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧệ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1lll1llllll1_opy_ = [200, 202]
            if response.status_code in bstack1lll1llllll1_opy_:
                return response.json()
            else:
                logger.error(bstack1ll111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦ࠴ࠠࡔࡶࡤࡸࡺࡹ࠺ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦỈ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡴࡶࡢࡧࡴࡲ࡬ࡦࡥࡷࡣࡧࡻࡩ࡭ࡦࡢࡨࡦࡺࡡ࠻ࠢࡾࢁࠧỉ").format(e))
            return None