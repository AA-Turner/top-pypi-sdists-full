# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1lllll1l_opy_
logger = logging.getLogger(__name__)
class bstack11ll111lll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111111l1ll_opy_ = urljoin(builder, bstack111l111_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠭Ἕ"))
        if params:
            bstack1111111l1ll_opy_ += bstack111l111_opy_ (u"ࠢࡀࡽࢀࠦ἞").format(urlencode({bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ἟"): params.get(bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩἠ"))}))
        return bstack11ll111lll1_opy_.bstack111111l1111_opy_(bstack1111111l1ll_opy_)
    @staticmethod
    def bstack11ll111ll1l_opy_(builder,params=None):
        bstack1111111l1ll_opy_ = urljoin(builder, bstack111l111_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫἡ"))
        if params:
            bstack1111111l1ll_opy_ += bstack111l111_opy_ (u"ࠦࡄࢁࡽࠣἢ").format(urlencode({bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬἣ"): params.get(bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ἤ"))}))
        return bstack11ll111lll1_opy_.bstack111111l1111_opy_(bstack1111111l1ll_opy_)
    @staticmethod
    def bstack111111l1111_opy_(bstack1111111ll1l_opy_):
        bstack1111111l11l_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬἥ"), os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬἦ"), bstack111l111_opy_ (u"ࠩࠪἧ")))
        headers = {bstack111l111_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪἨ"): bstack111l111_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧἩ").format(bstack1111111l11l_opy_)}
        response = requests.get(bstack1111111ll1l_opy_, headers=headers)
        bstack1111111l111_opy_ = {}
        try:
            bstack1111111l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦἪ").format(e))
            pass
        if bstack1111111l111_opy_ is not None:
            bstack1111111l111_opy_[bstack111l111_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧἫ")] = response.headers.get(bstack111l111_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨἬ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨἭ")] = response.status_code
        return bstack1111111l111_opy_
    @staticmethod
    def bstack1111111l1l1_opy_(bstack1111111llll_opy_, data):
        logger.debug(bstack111l111_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࠦἮ"))
        return bstack11ll111lll1_opy_.bstack1111111lll1_opy_(bstack111l111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨἯ"), bstack1111111llll_opy_, data=data)
    @staticmethod
    def bstack1111111ll11_opy_(bstack1111111llll_opy_, data):
        logger.debug(bstack111l111_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡧࡦࡶࡗࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡶࠦἰ"))
        res = bstack11ll111lll1_opy_.bstack1111111lll1_opy_(bstack111l111_opy_ (u"ࠬࡍࡅࡕࠩἱ"), bstack1111111llll_opy_, data=data)
        return res
    @staticmethod
    def bstack1111111lll1_opy_(method, bstack1111111llll_opy_, data=None, params=None, extra_headers=None):
        bstack1111111l11l_opy_ = os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪἲ"), bstack111l111_opy_ (u"ࠧࠨἳ"))
        headers = {
            bstack111l111_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨἴ"): bstack111l111_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬἵ").format(bstack1111111l11l_opy_),
            bstack111l111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩἶ"): bstack111l111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧἷ"),
            bstack111l111_opy_ (u"ࠬࡇࡣࡤࡧࡳࡸࠬἸ"): bstack111l111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩἹ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1lllll1l_opy_ + bstack111l111_opy_ (u"ࠢ࠰ࠤἺ") + bstack1111111llll_opy_.lstrip(bstack111l111_opy_ (u"ࠨ࠱ࠪἻ"))
        try:
            if method == bstack111l111_opy_ (u"ࠩࡊࡉ࡙࠭Ἴ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack111l111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨἽ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack111l111_opy_ (u"ࠫࡕ࡛ࡔࠨἾ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack111l111_opy_ (u"࡛ࠧ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧἿ").format(method))
            logger.debug(bstack111l111_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡮ࡣࡧࡩࠥࡺ࡯ࠡࡗࡕࡐ࠿ࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦὀ").format(url, method))
            bstack1111111l111_opy_ = {}
            try:
                bstack1111111l111_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack111l111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦὁ").format(e, response.text))
            if bstack1111111l111_opy_ is not None:
                bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩὂ")] = response.headers.get(
                    bstack111l111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪὃ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪὄ")] = response.status_code
            return bstack1111111l111_opy_
        except Exception as e:
            logger.error(bstack111l111_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢὅ").format(e, url))
            return None
    @staticmethod
    def bstack11l1l1l1111_opy_(bstack1111111ll1l_opy_, data):
        bstack111l111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡔ࡚࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ὆")
        bstack1111111l11l_opy_ = os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ὇"), bstack111l111_opy_ (u"ࠧࠨὈ"))
        headers = {
            bstack111l111_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨὉ"): bstack111l111_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬὊ").format(bstack1111111l11l_opy_),
            bstack111l111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩὋ"): bstack111l111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧὌ")
        }
        response = requests.put(bstack1111111ll1l_opy_, headers=headers, json=data)
        bstack1111111l111_opy_ = {}
        try:
            bstack1111111l111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦὍ").format(e))
            pass
        logger.debug(bstack111l111_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡰࡶࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ὎").format(bstack1111111l111_opy_))
        if bstack1111111l111_opy_ is not None:
            bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ὏")] = response.headers.get(
                bstack111l111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩὐ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩὑ")] = response.status_code
        return bstack1111111l111_opy_
    @staticmethod
    def bstack11l1l11llll_opy_(bstack1111111ll1l_opy_):
        bstack111l111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡉࡈࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡪࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣὒ")
        bstack1111111l11l_opy_ = os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨὓ"), bstack111l111_opy_ (u"ࠬ࠭ὔ"))
        headers = {
            bstack111l111_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ὕ"): bstack111l111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪὖ").format(bstack1111111l11l_opy_),
            bstack111l111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧὗ"): bstack111l111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ὘")
        }
        response = requests.get(bstack1111111ll1l_opy_, headers=headers)
        bstack1111111l111_opy_ = {}
        try:
            bstack1111111l111_opy_ = response.json()
            logger.debug(bstack111l111_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣ࡫ࡪࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧὙ").format(bstack1111111l111_opy_))
        except Exception as e:
            logger.debug(bstack111l111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ὚").format(e, response.text))
            pass
        if bstack1111111l111_opy_ is not None:
            bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ὓ")] = response.headers.get(
                bstack111l111_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ὜"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111l111_opy_[bstack111l111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧὝ")] = response.status_code
        return bstack1111111l111_opy_