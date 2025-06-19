# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11ll1l1lll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111l11l1ll_opy_ = urljoin(builder, bstack111lll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧẋ"))
        if params:
            bstack1111l11l1ll_opy_ += bstack111lll_opy_ (u"ࠣࡁࡾࢁࠧẌ").format(urlencode({bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẍ"): params.get(bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẎ"))}))
        return bstack11ll1l1lll1_opy_.bstack1111l111lll_opy_(bstack1111l11l1ll_opy_)
    @staticmethod
    def bstack11ll1l1l1ll_opy_(builder,params=None):
        bstack1111l11l1ll_opy_ = urljoin(builder, bstack111lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬẏ"))
        if params:
            bstack1111l11l1ll_opy_ += bstack111lll_opy_ (u"ࠧࡅࡻࡾࠤẐ").format(urlencode({bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẑ"): params.get(bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẒ"))}))
        return bstack11ll1l1lll1_opy_.bstack1111l111lll_opy_(bstack1111l11l1ll_opy_)
    @staticmethod
    def bstack1111l111lll_opy_(bstack1111l11ll11_opy_):
        bstack1111l11ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ẓ"), os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ẕ"), bstack111lll_opy_ (u"ࠪࠫẕ")))
        headers = {bstack111lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫẖ"): bstack111lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨẗ").format(bstack1111l11ll1l_opy_)}
        response = requests.get(bstack1111l11ll11_opy_, headers=headers)
        bstack1111l11l111_opy_ = {}
        try:
            bstack1111l11l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧẘ").format(e))
            pass
        if bstack1111l11l111_opy_ is not None:
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨẙ")] = response.headers.get(bstack111lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩẚ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩẛ")] = response.status_code
        return bstack1111l11l111_opy_
    @staticmethod
    def bstack1111l11l11l_opy_(bstack1111l11ll11_opy_, data):
        bstack111lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡹࡰ࡭࡫ࡷࠤࡹ࡫ࡳࡵࡵࠣࡅࡕࡏ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧẜ")
        bstack1111l11ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẝ"), bstack111lll_opy_ (u"ࠬ࠭ẞ"))
        headers = {
            bstack111lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ẟ"): bstack111lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪẠ").format(bstack1111l11ll1l_opy_),
            bstack111lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧạ"): bstack111lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬẢ")
        }
        response = requests.post(bstack1111l11ll11_opy_, headers=headers, json=data)
        bstack1111l11l111_opy_ = {}
        try:
            bstack1111l11l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤả").format(e))
            pass
        if bstack1111l11l111_opy_ is not None:
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬẤ")] = response.headers.get(
                bstack111lll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ấ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ầ")] = response.status_code
        return bstack1111l11l111_opy_
    @staticmethod
    def bstack1111l11l1l1_opy_(bstack1111l11ll11_opy_, data):
        bstack111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡱࡵࡨࡪࡸࡥࡥࠢࡷࡩࡸࡺࡳࠡࡃࡓࡍ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥầ")
        bstack1111l11ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẨ"), bstack111lll_opy_ (u"ࠩࠪẩ"))
        headers = {
            bstack111lll_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪẪ"): bstack111lll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧẫ").format(bstack1111l11ll1l_opy_),
            bstack111lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫẬ"): bstack111lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩậ")
        }
        response = requests.get(bstack1111l11ll11_opy_, headers=headers, json=data)
        bstack1111l11l111_opy_ = {}
        try:
            bstack1111l11l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨẮ").format(e))
            pass
        if bstack1111l11l111_opy_ is not None:
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩắ")] = response.headers.get(
                bstack111lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪẰ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪằ")] = response.status_code
        return bstack1111l11l111_opy_
    @staticmethod
    def bstack11l1ll1l111_opy_(bstack1111l11ll11_opy_, data):
        bstack111lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡓ࡙࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤẲ")
        bstack1111l11ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩẳ"), bstack111lll_opy_ (u"࠭ࠧẴ"))
        headers = {
            bstack111lll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧẵ"): bstack111lll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫẶ").format(bstack1111l11ll1l_opy_),
            bstack111lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨặ"): bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ẹ")
        }
        response = requests.put(bstack1111l11ll11_opy_, headers=headers, json=data)
        bstack1111l11l111_opy_ = {}
        try:
            bstack1111l11l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥẹ").format(e))
            pass
        logger.debug(bstack111lll_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥࡶࡵࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢẺ").format(bstack1111l11l111_opy_))
        if bstack1111l11l111_opy_ is not None:
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧẻ")] = response.headers.get(
                bstack111lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨẼ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨẽ")] = response.status_code
        return bstack1111l11l111_opy_
    @staticmethod
    def bstack11l1lll1l11_opy_(bstack1111l11ll11_opy_):
        bstack111lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡈࡇࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡩࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢẾ")
        bstack1111l11ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧế"), bstack111lll_opy_ (u"ࠫࠬỀ"))
        headers = {
            bstack111lll_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬề"): bstack111lll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩỂ").format(bstack1111l11ll1l_opy_),
            bstack111lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ể"): bstack111lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫỄ")
        }
        response = requests.get(bstack1111l11ll11_opy_, headers=headers)
        bstack1111l11l111_opy_ = {}
        try:
            bstack1111l11l111_opy_ = response.json()
            logger.debug(bstack111lll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡪࡩࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦễ").format(bstack1111l11l111_opy_))
        except Exception as e:
            logger.debug(bstack111lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢỆ").format(e, response.text))
            pass
        if bstack1111l11l111_opy_ is not None:
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬệ")] = response.headers.get(
                bstack111lll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ỉ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111l11l111_opy_[bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ỉ")] = response.status_code
        return bstack1111l11l111_opy_