# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11111ll1l1l_opy_
logger = logging.getLogger(__name__)
class bstack1111l111lll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1l11111ll_opy_ = urljoin(builder, bstack111l_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶࠫ♨"))
        if params:
            bstack1ll1l11111ll_opy_ += bstack111l_opy_ (u"ࠧࡅࡻࡾࠤ♩").format(urlencode({bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭♪"): params.get(bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ♫"))}))
        return bstack1111l111lll_opy_.bstack1ll1l111111l_opy_(bstack1ll1l11111ll_opy_)
    @staticmethod
    def bstack1111l11lll1_opy_(builder,params=None):
        bstack1ll1l11111ll_opy_ = urljoin(builder, bstack111l_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳ࠮ࡵࡸࡱࡲࡧࡲࡺࠩ♬"))
        if params:
            bstack1ll1l11111ll_opy_ += bstack111l_opy_ (u"ࠤࡂࡿࢂࠨ♭").format(urlencode({bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ♮"): params.get(bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ♯"))}))
        return bstack1111l111lll_opy_.bstack1ll1l111111l_opy_(bstack1ll1l11111ll_opy_)
    @staticmethod
    def bstack1ll1l111111l_opy_(bstack1ll1l1111lll_opy_):
        bstack1ll1l111l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ♰"), os.environ.get(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ♱"), bstack111l_opy_ (u"ࠧࠨ♲")))
        headers = {bstack111l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ♳"): bstack111l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ♴").format(bstack1ll1l111l1l1_opy_)}
        response = requests.get(bstack1ll1l1111lll_opy_, headers=headers)
        bstack1ll1l111l111_opy_ = {}
        try:
            bstack1ll1l111l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ♵").format(e))
            pass
        if bstack1ll1l111l111_opy_ is not None:
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ♶")] = response.headers.get(bstack111l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭♷"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭♸")] = response.status_code
        return bstack1ll1l111l111_opy_
    @staticmethod
    def bstack1ll1l1111l1l_opy_(bstack1ll1l1111l11_opy_, data):
        logger.debug(bstack111l_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࡙ࡰ࡭࡫ࡷࡘࡪࡹࡴࡴࠤ♹"))
        return bstack1111l111lll_opy_.bstack1ll1l11111l1_opy_(bstack111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭♺"), bstack1ll1l1111l11_opy_, data=data)
    @staticmethod
    def bstack1ll1l111l11l_opy_(bstack1ll1l1111l11_opy_, data):
        logger.debug(bstack111l_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤ࡬࡫ࡴࡕࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡓࡷࡪࡥࡳࡧࡧࡘࡪࡹࡴࡴࠤ♻"))
        res = bstack1111l111lll_opy_.bstack1ll1l11111l1_opy_(bstack111l_opy_ (u"ࠪࡋࡊ࡚ࠧ♼"), bstack1ll1l1111l11_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1l11111l1_opy_(method, bstack1ll1l1111l11_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1l111l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ♽"), bstack111l_opy_ (u"ࠬ࠭♾"))
        headers = {
            bstack111l_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭♿"): bstack111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⚀").format(bstack1ll1l111l1l1_opy_),
            bstack111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⚁"): bstack111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⚂"),
            bstack111l_opy_ (u"ࠪࡅࡨࡩࡥࡱࡶࠪ⚃"): bstack111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⚄")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11111ll1l1l_opy_ + bstack111l_opy_ (u"ࠧ࠵ࠢ⚅") + bstack1ll1l1111l11_opy_.lstrip(bstack111l_opy_ (u"࠭࠯ࠨ⚆"))
        try:
            if method == bstack111l_opy_ (u"ࠧࡈࡇࡗࠫ⚇"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭⚈"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack111l_opy_ (u"ࠩࡓ࡙࡙࠭⚉"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack111l_opy_ (u"࡙ࠥࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡊࡗࡘࡕࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥ⚊").format(method))
            logger.debug(bstack111l_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡳࡡࡥࡧࠣࡸࡴࠦࡕࡓࡎ࠽ࠤࢀࢃࠠࡸ࡫ࡷ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤ⚋").format(url, method))
            bstack1ll1l111l111_opy_ = {}
            try:
                bstack1ll1l111l111_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⚌").format(e, response.text))
            if bstack1ll1l111l111_opy_ is not None:
                bstack1ll1l111l111_opy_[bstack111l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⚍")] = response.headers.get(
                    bstack111l_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⚎"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⚏")] = response.status_code
            return bstack1ll1l111l111_opy_
        except Exception as e:
            logger.error(bstack111l_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ⚐").format(e, url))
            return None
    @staticmethod
    def bstack1111111lll1_opy_(bstack1ll1l1111lll_opy_, data):
        bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡒࡘࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡶ࡫ࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⚑")
        bstack1ll1l111l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⚒"), bstack111l_opy_ (u"ࠬ࠭⚓"))
        headers = {
            bstack111l_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⚔"): bstack111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⚕").format(bstack1ll1l111l1l1_opy_),
            bstack111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⚖"): bstack111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⚗")
        }
        response = requests.put(bstack1ll1l1111lll_opy_, headers=headers, json=data)
        bstack1ll1l111l111_opy_ = {}
        try:
            bstack1ll1l111l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⚘").format(e))
            pass
        logger.debug(bstack111l_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤࡵࡻࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⚙").format(bstack1ll1l111l111_opy_))
        if bstack1ll1l111l111_opy_ is not None:
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⚚")] = response.headers.get(
                bstack111l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⚛"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⚜")] = response.status_code
        return bstack1ll1l111l111_opy_
    @staticmethod
    def bstack111111l1111_opy_(bstack1ll1l1111lll_opy_):
        bstack111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡇࡆࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡨࡧࡷࠤࡹ࡮ࡥࠡࡥࡲࡹࡳࡺࠠࡰࡨࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⚝")
        bstack1ll1l111l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⚞"), bstack111l_opy_ (u"ࠪࠫ⚟"))
        headers = {
            bstack111l_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⚠"): bstack111l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⚡").format(bstack1ll1l111l1l1_opy_),
            bstack111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⚢"): bstack111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⚣")
        }
        response = requests.get(bstack1ll1l1111lll_opy_, headers=headers)
        bstack1ll1l111l111_opy_ = {}
        try:
            bstack1ll1l111l111_opy_ = response.json()
            logger.debug(bstack111l_opy_ (u"ࠣࡔࡨࡵࡺ࡫ࡳࡵࡗࡷ࡭ࡱࡹ࠺ࠡࡩࡨࡸࡤ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚤").format(bstack1ll1l111l111_opy_))
        except Exception as e:
            logger.debug(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⚥").format(e, response.text))
            pass
        if bstack1ll1l111l111_opy_ is not None:
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⚦")] = response.headers.get(
                bstack111l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⚧"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1l111l111_opy_[bstack111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⚨")] = response.status_code
        return bstack1ll1l111l111_opy_
    @staticmethod
    def bstack1lll1111l1ll_opy_(bstack1111l11llll_opy_, payload):
        bstack111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡑࡦࡱࡥࡴࠢࡤࠤࡕࡕࡓࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡴࡩࡧࠣࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡧࡻࡩ࡭ࡦ࠰ࡨࡦࡺࡡࠡࡧࡱࡨࡵࡵࡩ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡨࡲࡩࡶ࡯ࡪࡰࡷࠤ࠭ࡹࡴࡳࠫ࠽ࠤ࡙࡮ࡥࠡࡃࡓࡍࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࠮ࡤࡪࡥࡷ࠭࠿ࠦࡔࡩࡧࠣࡶࡪࡷࡵࡦࡵࡷࠤࡵࡧࡹ࡭ࡱࡤࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡅࡕࡏࠬࠡࡱࡵࠤࡓࡵ࡮ࡦࠢ࡬ࡪࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⚩")
        try:
            url = bstack111l_opy_ (u"ࠢࡼࡿ࠲ࡿࢂࠨ⚪").format(bstack11111ll1l1l_opy_, bstack1111l11llll_opy_)
            bstack1ll1l111l1l1_opy_ = os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⚫"), bstack111l_opy_ (u"ࠩࠪ⚬"))
            headers = {
                bstack111l_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⚭"): bstack111l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⚮").format(bstack1ll1l111l1l1_opy_),
                bstack111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⚯"): bstack111l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⚰")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1l1111ll1_opy_ = [200, 202]
            if response.status_code in bstack1ll1l1111ll1_opy_:
                return response.json()
            else:
                logger.error(bstack111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧࡴࡲ࡬ࡦࡥࡷࠤࡧࡻࡩ࡭ࡦࠣࡨࡦࡺࡡ࠯ࠢࡖࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⚱").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡶࡸࡤࡩ࡯࡭࡮ࡨࡧࡹࡥࡢࡶ࡫࡯ࡨࡤࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ⚲").format(e))
            return None