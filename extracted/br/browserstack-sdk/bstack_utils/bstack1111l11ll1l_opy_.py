# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111111lllll_opy_
logger = logging.getLogger(__name__)
class bstack1111l11l11l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1l111l111_opy_ = urljoin(builder, bstack1ll1l11_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨ♥"))
        if params:
            bstack1ll1l111l111_opy_ += bstack1ll1l11_opy_ (u"ࠤࡂࡿࢂࠨ♦").format(urlencode({bstack1ll1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ♧"): params.get(bstack1ll1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ♨"))}))
        return bstack1111l11l11l_opy_.bstack1ll1l11111ll_opy_(bstack1ll1l111l111_opy_)
    @staticmethod
    def bstack1111l11l1ll_opy_(builder,params=None):
        bstack1ll1l111l111_opy_ = urljoin(builder, bstack1ll1l11_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭♩"))
        if params:
            bstack1ll1l111l111_opy_ += bstack1ll1l11_opy_ (u"ࠨ࠿ࡼࡿࠥ♪").format(urlencode({bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ♫"): params.get(bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ♬"))}))
        return bstack1111l11l11l_opy_.bstack1ll1l11111ll_opy_(bstack1ll1l111l111_opy_)
    @staticmethod
    def bstack1ll1l11111ll_opy_(bstack1ll1l1111l11_opy_):
        bstack1ll1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ♭"), os.environ.get(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ♮"), bstack1ll1l11_opy_ (u"ࠫࠬ♯")))
        headers = {bstack1ll1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ♰"): bstack1ll1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ♱").format(bstack1ll1l111l11l_opy_)}
        response = requests.get(bstack1ll1l1111l11_opy_, headers=headers)
        bstack1ll1l1111l1l_opy_ = {}
        try:
            bstack1ll1l1111l1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ♲").format(e))
            pass
        if bstack1ll1l1111l1l_opy_ is not None:
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ♳")] = response.headers.get(bstack1ll1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ♴"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ♵")] = response.status_code
        return bstack1ll1l1111l1l_opy_
    @staticmethod
    def bstack1ll1l111l1ll_opy_(bstack1ll1l1111lll_opy_, data):
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡴࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡖࡴࡱ࡯ࡴࡕࡧࡶࡸࡸࠨ♶"))
        return bstack1111l11l11l_opy_.bstack1ll1l111ll11_opy_(bstack1ll1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪ♷"), bstack1ll1l1111lll_opy_, data=data)
    @staticmethod
    def bstack1ll1l1111ll1_opy_(bstack1ll1l1111lll_opy_, data):
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡩࡨࡸ࡙࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡐࡴࡧࡩࡷ࡫ࡤࡕࡧࡶࡸࡸࠨ♸"))
        res = bstack1111l11l11l_opy_.bstack1ll1l111ll11_opy_(bstack1ll1l11_opy_ (u"ࠧࡈࡇࡗࠫ♹"), bstack1ll1l1111lll_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1l111ll11_opy_(method, bstack1ll1l1111lll_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ♺"), bstack1ll1l11_opy_ (u"ࠩࠪ♻"))
        headers = {
            bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ♼"): bstack1ll1l11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ♽").format(bstack1ll1l111l11l_opy_),
            bstack1ll1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ♾"): bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ♿"),
            bstack1ll1l11_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧ⚀"): bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⚁")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111111lllll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠲ࠦ⚂") + bstack1ll1l1111lll_opy_.lstrip(bstack1ll1l11_opy_ (u"ࠪ࠳ࠬ⚃"))
        try:
            if method == bstack1ll1l11_opy_ (u"ࠫࡌࡋࡔࠨ⚄"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll1l11_opy_ (u"ࠬࡖࡏࡔࡖࠪ⚅"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll1l11_opy_ (u"࠭ࡐࡖࡖࠪ⚆"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⚇").format(method))
            logger.debug(bstack1ll1l11_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡰࡥࡩ࡫ࠠࡵࡱ࡙ࠣࡗࡒ࠺ࠡࡽࢀࠤࡼ࡯ࡴࡩࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⚈").format(url, method))
            bstack1ll1l1111l1l_opy_ = {}
            try:
                bstack1ll1l1111l1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⚉").format(e, response.text))
            if bstack1ll1l1111l1l_opy_ is not None:
                bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⚊")] = response.headers.get(
                    bstack1ll1l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⚋"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⚌")] = response.status_code
            return bstack1ll1l1111l1l_opy_
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⚍").format(e, url))
            return None
    @staticmethod
    def bstack1111111ll1l_opy_(bstack1ll1l1111l11_opy_, data):
        bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡖࡕࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⚎")
        bstack1ll1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⚏"), bstack1ll1l11_opy_ (u"ࠩࠪ⚐"))
        headers = {
            bstack1ll1l11_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⚑"): bstack1ll1l11_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⚒").format(bstack1ll1l111l11l_opy_),
            bstack1ll1l11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⚓"): bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⚔")
        }
        response = requests.put(bstack1ll1l1111l11_opy_, headers=headers, json=data)
        bstack1ll1l1111l1l_opy_ = {}
        try:
            bstack1ll1l1111l1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⚕").format(e))
            pass
        logger.debug(bstack1ll1l11_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡲࡸࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚖").format(bstack1ll1l1111l1l_opy_))
        if bstack1ll1l1111l1l_opy_ is not None:
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⚗")] = response.headers.get(
                bstack1ll1l11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⚘"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⚙")] = response.status_code
        return bstack1ll1l1111l1l_opy_
    @staticmethod
    def bstack111111l1111_opy_(bstack1ll1l1111l11_opy_):
        bstack1ll1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡋࡊ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡬࡫ࡴࠡࡶ࡫ࡩࠥࡩ࡯ࡶࡰࡷࠤࡴ࡬ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⚚")
        bstack1ll1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⚛"), bstack1ll1l11_opy_ (u"ࠧࠨ⚜"))
        headers = {
            bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⚝"): bstack1ll1l11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⚞").format(bstack1ll1l111l11l_opy_),
            bstack1ll1l11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⚟"): bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⚠")
        }
        response = requests.get(bstack1ll1l1111l11_opy_, headers=headers)
        bstack1ll1l1111l1l_opy_ = {}
        try:
            bstack1ll1l1111l1l_opy_ = response.json()
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥ࡭ࡥࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⚡").format(bstack1ll1l1111l1l_opy_))
        except Exception as e:
            logger.debug(bstack1ll1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⚢").format(e, response.text))
            pass
        if bstack1ll1l1111l1l_opy_ is not None:
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⚣")] = response.headers.get(
                bstack1ll1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⚤"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1l1111l1l_opy_[bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⚥")] = response.status_code
        return bstack1ll1l1111l1l_opy_
    @staticmethod
    def bstack1lll11lll111_opy_(bstack1111l1l1111_opy_, payload):
        bstack1ll1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡎࡣ࡮ࡩࡸࠦࡡࠡࡒࡒࡗ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡸ࡭࡫ࠠࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡤࡸ࡭ࡱࡪ࠭ࡥࡣࡷࡥࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࠪࡶࡸࡷ࠯࠺ࠡࡖ࡫ࡩࠥࡇࡐࡊࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡽࡱࡵࡡࡥࠢࠫࡨ࡮ࡩࡴࠪ࠼ࠣࡘ࡭࡫ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡲࡤࡽࡱࡵࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡂࡒࡌ࠰ࠥࡵࡲࠡࡐࡲࡲࡪࠦࡩࡧࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⚦")
        try:
            url = bstack1ll1l11_opy_ (u"ࠦࢀࢃ࠯ࡼࡿࠥ⚧").format(bstack111111lllll_opy_, bstack1111l1l1111_opy_)
            bstack1ll1l111l11l_opy_ = os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⚨"), bstack1ll1l11_opy_ (u"࠭ࠧ⚩"))
            headers = {
                bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⚪"): bstack1ll1l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⚫").format(bstack1ll1l111l11l_opy_),
                bstack1ll1l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⚬"): bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⚭")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1l111l1l1_opy_ = [200, 202]
            if response.status_code in bstack1ll1l111l1l1_opy_:
                return response.json()
            else:
                logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡱ࡯ࡰࡪࡩࡴࠡࡤࡸ࡭ࡱࡪࠠࡥࡣࡷࡥ࠳ࠦࡓࡵࡣࡷࡹࡸࡀࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚮").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡳࡵࡡࡦࡳࡱࡲࡥࡤࡶࡢࡦࡺ࡯࡬ࡥࡡࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ⚯").format(e))
            return None