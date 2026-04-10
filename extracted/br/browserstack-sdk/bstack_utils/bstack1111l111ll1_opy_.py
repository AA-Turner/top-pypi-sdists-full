# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11111ll1111_opy_
logger = logging.getLogger(__name__)
class bstack1111l111l1l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll11lllllll_opy_ = urljoin(builder, bstack1ll_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ♬"))
        if params:
            bstack1ll11lllllll_opy_ += bstack1ll_opy_ (u"ࠤࡂࡿࢂࠨ♭").format(urlencode({bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ♮"): params.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ♯"))}))
        return bstack1111l111l1l_opy_.bstack1ll11llll1ll_opy_(bstack1ll11lllllll_opy_)
    @staticmethod
    def bstack1111l111lll_opy_(builder,params=None):
        bstack1ll11lllllll_opy_ = urljoin(builder, bstack1ll_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭♰"))
        if params:
            bstack1ll11lllllll_opy_ += bstack1ll_opy_ (u"ࠨ࠿ࡼࡿࠥ♱").format(urlencode({bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ♲"): params.get(bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ♳"))}))
        return bstack1111l111l1l_opy_.bstack1ll11llll1ll_opy_(bstack1ll11lllllll_opy_)
    @staticmethod
    def bstack1ll11llll1ll_opy_(bstack1ll1l11111ll_opy_):
        bstack1ll1l1111l11_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ♴"), os.environ.get(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ♵"), bstack1ll_opy_ (u"ࠫࠬ♶")))
        headers = {bstack1ll_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ♷"): bstack1ll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ♸").format(bstack1ll1l1111l11_opy_)}
        response = requests.get(bstack1ll1l11111ll_opy_, headers=headers)
        bstack1ll11lllll11_opy_ = {}
        try:
            bstack1ll11lllll11_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ♹").format(e))
            pass
        if bstack1ll11lllll11_opy_ is not None:
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ♺")] = response.headers.get(bstack1ll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ♻"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ♼")] = response.status_code
        return bstack1ll11lllll11_opy_
    @staticmethod
    def bstack1ll11llllll1_opy_(bstack1ll1l111111l_opy_, data):
        logger.debug(bstack1ll_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨ♽"))
        return bstack1111l111l1l_opy_.bstack1ll1l11111l1_opy_(bstack1ll_opy_ (u"ࠬࡖࡏࡔࡖࠪ♾"), bstack1ll1l111111l_opy_, data=data)
    @staticmethod
    def bstack1ll1l1111111_opy_(bstack1ll1l111111l_opy_, data):
        logger.debug(bstack1ll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨ♿"))
        res = bstack1111l111l1l_opy_.bstack1ll1l11111l1_opy_(bstack1ll_opy_ (u"ࠧࡈࡇࡗࠫ⚀"), bstack1ll1l111111l_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1l11111l1_opy_(method, bstack1ll1l111111l_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1l1111l11_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⚁"), bstack1ll_opy_ (u"ࠩࠪ⚂"))
        headers = {
            bstack1ll_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⚃"): bstack1ll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⚄").format(bstack1ll1l1111l11_opy_),
            bstack1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⚅"): bstack1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⚆"),
            bstack1ll_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧ⚇"): bstack1ll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⚈")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11111ll1111_opy_ + bstack1ll_opy_ (u"ࠤ࠲ࠦ⚉") + bstack1ll1l111111l_opy_.lstrip(bstack1ll_opy_ (u"ࠪ࠳ࠬ⚊"))
        try:
            if method == bstack1ll_opy_ (u"ࠫࡌࡋࡔࠨ⚋"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll_opy_ (u"ࠬࡖࡏࡔࡖࠪ⚌"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll_opy_ (u"࠭ࡐࡖࡖࠪ⚍"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⚎").format(method))
            logger.debug(bstack1ll_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⚏").format(url, method))
            bstack1ll11lllll11_opy_ = {}
            try:
                bstack1ll11lllll11_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⚐").format(e, response.text))
            if bstack1ll11lllll11_opy_ is not None:
                bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⚑")] = response.headers.get(
                    bstack1ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⚒"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⚓")] = response.status_code
            return bstack1ll11lllll11_opy_
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⚔").format(e, url))
            return None
    @staticmethod
    def bstack1lllllll1ll1_opy_(bstack1ll1l11111ll_opy_, data):
        bstack1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⚕")
        bstack1ll1l1111l11_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⚖"), bstack1ll_opy_ (u"ࠩࠪ⚗"))
        headers = {
            bstack1ll_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⚘"): bstack1ll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⚙").format(bstack1ll1l1111l11_opy_),
            bstack1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⚚"): bstack1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⚛")
        }
        response = requests.put(bstack1ll1l11111ll_opy_, headers=headers, json=data)
        bstack1ll11lllll11_opy_ = {}
        try:
            bstack1ll11lllll11_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⚜").format(e))
            pass
        logger.debug(bstack1ll_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚝").format(bstack1ll11lllll11_opy_))
        if bstack1ll11lllll11_opy_ is not None:
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⚞")] = response.headers.get(
                bstack1ll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⚟"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⚠")] = response.status_code
        return bstack1ll11lllll11_opy_
    @staticmethod
    def bstack1111111l11l_opy_(bstack1ll1l11111ll_opy_):
        bstack1ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⚡")
        bstack1ll1l1111l11_opy_ = os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⚢"), bstack1ll_opy_ (u"ࠧࠨ⚣"))
        headers = {
            bstack1ll_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⚤"): bstack1ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⚥").format(bstack1ll1l1111l11_opy_),
            bstack1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⚦"): bstack1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⚧")
        }
        response = requests.get(bstack1ll1l11111ll_opy_, headers=headers)
        bstack1ll11lllll11_opy_ = {}
        try:
            bstack1ll11lllll11_opy_ = response.json()
            logger.debug(bstack1ll_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⚨").format(bstack1ll11lllll11_opy_))
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⚩").format(e, response.text))
            pass
        if bstack1ll11lllll11_opy_ is not None:
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⚪")] = response.headers.get(
                bstack1ll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⚫"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11lllll11_opy_[bstack1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⚬")] = response.status_code
        return bstack1ll11lllll11_opy_
    @staticmethod
    def bstack1lll11l1ll1l_opy_(bstack1111l11l11l_opy_, payload):
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣ࡮ࡩࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩࠥࡇࡐࡊࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡽࡱࡵࡡࡥࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡲࡤࡽࡱࡵࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡂࡒࡌ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⚭")
        try:
            url = bstack1ll_opy_ (u"ࠦࢀࢃ࠯ࡼࡿࠥ⚮").format(bstack11111ll1111_opy_, bstack1111l11l11l_opy_)
            bstack1ll1l1111l11_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⚯"), bstack1ll_opy_ (u"࠭ࠧ⚰"))
            headers = {
                bstack1ll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⚱"): bstack1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⚲").format(bstack1ll1l1111l11_opy_),
                bstack1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⚳"): bstack1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⚴")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll11lllll1l_opy_ = [200, 202]
            if response.status_code in bstack1ll11lllll1l_opy_:
                return response.json()
            else:
                logger.error(bstack1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥ࠳ࠦࡓࡵࡣࡷࡹࡸࡀࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚵").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡳࡵࡡࡦࡳࡱࡲࡥࡤࡶࡢࡦࡺ࡯࡬ࡥࡡࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⚶").format(e))
            return None