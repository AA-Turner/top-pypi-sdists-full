# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111ll1lllll_opy_
logger = logging.getLogger(__name__)
class bstack11l1111l1ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lll1l11l111_opy_ = urljoin(builder, bstack11l1l11_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ∨"))
        if params:
            bstack1lll1l11l111_opy_ += bstack11l1l11_opy_ (u"ࠤࡂࡿࢂࠨ∩").format(urlencode({bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ∪"): params.get(bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ∫"))}))
        return bstack11l1111l1ll_opy_.bstack1lll1l111ll1_opy_(bstack1lll1l11l111_opy_)
    @staticmethod
    def bstack11l1111ll11_opy_(builder,params=None):
        bstack1lll1l11l111_opy_ = urljoin(builder, bstack11l1l11_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭∬"))
        if params:
            bstack1lll1l11l111_opy_ += bstack11l1l11_opy_ (u"ࠨ࠿ࡼࡿࠥ∭").format(urlencode({bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ∮"): params.get(bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ∯"))}))
        return bstack11l1111l1ll_opy_.bstack1lll1l111ll1_opy_(bstack1lll1l11l111_opy_)
    @staticmethod
    def bstack1lll1l111ll1_opy_(bstack1lll1l11ll11_opy_):
        bstack1lll1l11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ∰"), os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ∱"), bstack11l1l11_opy_ (u"ࠫࠬ∲")))
        headers = {bstack11l1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ∳"): bstack11l1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ∴").format(bstack1lll1l11l1l1_opy_)}
        response = requests.get(bstack1lll1l11ll11_opy_, headers=headers)
        bstack1lll1l11l11l_opy_ = {}
        try:
            bstack1lll1l11l11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ∵").format(e))
            pass
        if bstack1lll1l11l11l_opy_ is not None:
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ∶")] = response.headers.get(bstack11l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ∷"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ∸")] = response.status_code
        return bstack1lll1l11l11l_opy_
    @staticmethod
    def bstack1lll1l11lll1_opy_(bstack1lll1l11ll1l_opy_, data):
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨ∹"))
        return bstack11l1111l1ll_opy_.bstack1lll1l111l1l_opy_(bstack11l1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪ∺"), bstack1lll1l11ll1l_opy_, data=data)
    @staticmethod
    def bstack1lll1l111lll_opy_(bstack1lll1l11ll1l_opy_, data):
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨ∻"))
        res = bstack11l1111l1ll_opy_.bstack1lll1l111l1l_opy_(bstack11l1l11_opy_ (u"ࠧࡈࡇࡗࠫ∼"), bstack1lll1l11ll1l_opy_, data=data)
        return res
    @staticmethod
    def bstack1lll1l111l1l_opy_(method, bstack1lll1l11ll1l_opy_, data=None, params=None, extra_headers=None):
        bstack1lll1l11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ∽"), bstack11l1l11_opy_ (u"ࠩࠪ∾"))
        headers = {
            bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ∿"): bstack11l1l11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ≀").format(bstack1lll1l11l1l1_opy_),
            bstack11l1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ≁"): bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ≂"),
            bstack11l1l11_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧ≃"): bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ≄")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111ll1lllll_opy_ + bstack11l1l11_opy_ (u"ࠤ࠲ࠦ≅") + bstack1lll1l11ll1l_opy_.lstrip(bstack11l1l11_opy_ (u"ࠪ࠳ࠬ≆"))
        try:
            if method == bstack11l1l11_opy_ (u"ࠫࡌࡋࡔࠨ≇"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11l1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪ≈"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11l1l11_opy_ (u"࠭ࡐࡖࡖࠪ≉"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11l1l11_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ≊").format(method))
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ≋").format(url, method))
            bstack1lll1l11l11l_opy_ = {}
            try:
                bstack1lll1l11l11l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11l1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ≌").format(e, response.text))
            if bstack1lll1l11l11l_opy_ is not None:
                bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ≍")] = response.headers.get(
                    bstack11l1l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ≎"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ≏")] = response.status_code
            return bstack1lll1l11l11l_opy_
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ≐").format(e, url))
            return None
    @staticmethod
    def bstack111ll111111_opy_(bstack1lll1l11ll11_opy_, data):
        bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ≑")
        bstack1lll1l11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ≒"), bstack11l1l11_opy_ (u"ࠩࠪ≓"))
        headers = {
            bstack11l1l11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ≔"): bstack11l1l11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ≕").format(bstack1lll1l11l1l1_opy_),
            bstack11l1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ≖"): bstack11l1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ≗")
        }
        response = requests.put(bstack1lll1l11ll11_opy_, headers=headers, json=data)
        bstack1lll1l11l11l_opy_ = {}
        try:
            bstack1lll1l11l11l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ≘").format(e))
            pass
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ≙").format(bstack1lll1l11l11l_opy_))
        if bstack1lll1l11l11l_opy_ is not None:
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ≚")] = response.headers.get(
                bstack11l1l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ≛"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ≜")] = response.status_code
        return bstack1lll1l11l11l_opy_
    @staticmethod
    def bstack111ll1l111l_opy_(bstack1lll1l11ll11_opy_):
        bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ≝")
        bstack1lll1l11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ≞"), bstack11l1l11_opy_ (u"ࠧࠨ≟"))
        headers = {
            bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ≠"): bstack11l1l11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ≡").format(bstack1lll1l11l1l1_opy_),
            bstack11l1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ≢"): bstack11l1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ≣")
        }
        response = requests.get(bstack1lll1l11ll11_opy_, headers=headers)
        bstack1lll1l11l11l_opy_ = {}
        try:
            bstack1lll1l11l11l_opy_ = response.json()
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ≤").format(bstack1lll1l11l11l_opy_))
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ≥").format(e, response.text))
            pass
        if bstack1lll1l11l11l_opy_ is not None:
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ≦")] = response.headers.get(
                bstack11l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ≧"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1l11l11l_opy_[bstack11l1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ≨")] = response.status_code
        return bstack1lll1l11l11l_opy_
    @staticmethod
    def bstack1llllll11l1l_opy_(bstack11l111l11ll_opy_, payload):
        bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣ࡮ࡩࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩࠥࡇࡐࡊࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡽࡱࡵࡡࡥࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡲࡤࡽࡱࡵࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡂࡒࡌ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ≩")
        try:
            url = bstack11l1l11_opy_ (u"ࠦࢀࢃ࠯ࡼࡿࠥ≪").format(bstack111ll1lllll_opy_, bstack11l111l11ll_opy_)
            bstack1lll1l11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ≫"), bstack11l1l11_opy_ (u"࠭ࠧ≬"))
            headers = {
                bstack11l1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ≭"): bstack11l1l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ≮").format(bstack1lll1l11l1l1_opy_),
                bstack11l1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ≯"): bstack11l1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭≰")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1lll1l11l1ll_opy_ = [200, 202]
            if response.status_code in bstack1lll1l11l1ll_opy_:
                return response.json()
            else:
                logger.error(bstack11l1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥ࠳ࠦࡓࡵࡣࡷࡹࡸࡀࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ≱").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡳࡵࡡࡦࡳࡱࡲࡥࡤࡶࡢࡦࡺ࡯࡬ࡥࡡࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ≲").format(e))
            return None