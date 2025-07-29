# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1ll1111l_opy_
logger = logging.getLogger(__name__)
class bstack11ll11l11ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111111ll11_opy_ = urljoin(builder, bstackl_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧ἞"))
        if params:
            bstack1111111ll11_opy_ += bstackl_opy_ (u"ࠣࡁࡾࢁࠧ἟").format(urlencode({bstackl_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩἠ"): params.get(bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪἡ"))}))
        return bstack11ll11l11ll_opy_.bstack1111111l1ll_opy_(bstack1111111ll11_opy_)
    @staticmethod
    def bstack11ll111ll1l_opy_(builder,params=None):
        bstack1111111ll11_opy_ = urljoin(builder, bstackl_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬἢ"))
        if params:
            bstack1111111ll11_opy_ += bstackl_opy_ (u"ࠧࡅࡻࡾࠤἣ").format(urlencode({bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ἤ"): params.get(bstackl_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧἥ"))}))
        return bstack11ll11l11ll_opy_.bstack1111111l1ll_opy_(bstack1111111ll11_opy_)
    @staticmethod
    def bstack1111111l1ll_opy_(bstack1111111l1l1_opy_):
        bstack11111111lll_opy_ = os.environ.get(bstackl_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ἦ"), os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ἧ"), bstackl_opy_ (u"ࠪࠫἨ")))
        headers = {bstackl_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫἩ"): bstackl_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨἪ").format(bstack11111111lll_opy_)}
        response = requests.get(bstack1111111l1l1_opy_, headers=headers)
        bstack1111111lll1_opy_ = {}
        try:
            bstack1111111lll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧἫ").format(e))
            pass
        if bstack1111111lll1_opy_ is not None:
            bstack1111111lll1_opy_[bstackl_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨἬ")] = response.headers.get(bstackl_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩἭ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111111lll1_opy_[bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩἮ")] = response.status_code
        return bstack1111111lll1_opy_
    @staticmethod
    def bstack1111111ll1l_opy_(bstack1111111l111_opy_, data):
        logger.debug(bstackl_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࠧἯ"))
        return bstack11ll11l11ll_opy_.bstack1111111l11l_opy_(bstackl_opy_ (u"ࠫࡕࡕࡓࡕࠩἰ"), bstack1111111l111_opy_, data=data)
    @staticmethod
    def bstack1111111llll_opy_(bstack1111111l111_opy_, data):
        logger.debug(bstackl_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡨࡧࡷࡘࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡷࠧἱ"))
        res = bstack11ll11l11ll_opy_.bstack1111111l11l_opy_(bstackl_opy_ (u"࠭ࡇࡆࡖࠪἲ"), bstack1111111l111_opy_, data=data)
        return res
    @staticmethod
    def bstack1111111l11l_opy_(method, bstack1111111l111_opy_, data=None, params=None, extra_headers=None):
        bstack11111111lll_opy_ = os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫἳ"), bstackl_opy_ (u"ࠨࠩἴ"))
        headers = {
            bstackl_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩἵ"): bstackl_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ἶ").format(bstack11111111lll_opy_),
            bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪἷ"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨἸ"),
            bstackl_opy_ (u"࠭ࡁࡤࡥࡨࡴࡹ࠭Ἱ"): bstackl_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪἺ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1ll1111l_opy_ + bstackl_opy_ (u"ࠣ࠱ࠥἻ") + bstack1111111l111_opy_.lstrip(bstackl_opy_ (u"ࠩ࠲ࠫἼ"))
        try:
            if method == bstackl_opy_ (u"ࠪࡋࡊ࡚ࠧἽ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstackl_opy_ (u"ࠫࡕࡕࡓࡕࠩἾ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstackl_opy_ (u"ࠬࡖࡕࡕࠩἿ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstackl_opy_ (u"ࠨࡕ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨὀ").format(method))
            logger.debug(bstackl_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡ࡯ࡤࡨࡪࠦࡴࡰࠢࡘࡖࡑࡀࠠࡼࡿࠣࡻ࡮ࡺࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧὁ").format(url, method))
            bstack1111111lll1_opy_ = {}
            try:
                bstack1111111lll1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstackl_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧὂ").format(e, response.text))
            if bstack1111111lll1_opy_ is not None:
                bstack1111111lll1_opy_[bstackl_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪὃ")] = response.headers.get(
                    bstackl_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫὄ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1111111lll1_opy_[bstackl_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫὅ")] = response.status_code
            return bstack1111111lll1_opy_
        except Exception as e:
            logger.error(bstackl_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ὆").format(e, url))
            return None
    @staticmethod
    def bstack11l1l11ll1l_opy_(bstack1111111l1l1_opy_, data):
        bstackl_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡕ࡛ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ὇")
        bstack11111111lll_opy_ = os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫὈ"), bstackl_opy_ (u"ࠨࠩὉ"))
        headers = {
            bstackl_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩὊ"): bstackl_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭Ὃ").format(bstack11111111lll_opy_),
            bstackl_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪὌ"): bstackl_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨὍ")
        }
        response = requests.put(bstack1111111l1l1_opy_, headers=headers, json=data)
        bstack1111111lll1_opy_ = {}
        try:
            bstack1111111lll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ὎").format(e))
            pass
        logger.debug(bstackl_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡱࡷࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ὏").format(bstack1111111lll1_opy_))
        if bstack1111111lll1_opy_ is not None:
            bstack1111111lll1_opy_[bstackl_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩὐ")] = response.headers.get(
                bstackl_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪὑ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111lll1_opy_[bstackl_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪὒ")] = response.status_code
        return bstack1111111lll1_opy_
    @staticmethod
    def bstack11l1l1ll1l1_opy_(bstack1111111l1l1_opy_):
        bstackl_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡊࡉ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣ࡫ࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤὓ")
        bstack11111111lll_opy_ = os.environ.get(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩὔ"), bstackl_opy_ (u"࠭ࠧὕ"))
        headers = {
            bstackl_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧὖ"): bstackl_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫὗ").format(bstack11111111lll_opy_),
            bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ὘"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ὑ")
        }
        response = requests.get(bstack1111111l1l1_opy_, headers=headers)
        bstack1111111lll1_opy_ = {}
        try:
            bstack1111111lll1_opy_ = response.json()
            logger.debug(bstackl_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤ࡬࡫ࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ὚").format(bstack1111111lll1_opy_))
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤὛ").format(e, response.text))
            pass
        if bstack1111111lll1_opy_ is not None:
            bstack1111111lll1_opy_[bstackl_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ὜")] = response.headers.get(
                bstackl_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨὝ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111lll1_opy_[bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ὞")] = response.status_code
        return bstack1111111lll1_opy_