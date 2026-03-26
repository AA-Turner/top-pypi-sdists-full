# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111l11l11ll_opy_
logger = logging.getLogger(__name__)
class bstack111l1ll11l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1lll1l1ll_opy_ = urljoin(builder, bstack1ll1lll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧ⒁"))
        if params:
            bstack1ll1lll1l1ll_opy_ += bstack1ll1lll_opy_ (u"ࠣࡁࡾࢁࠧ⒂").format(urlencode({bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⒃"): params.get(bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⒄"))}))
        return bstack111l1ll11l1_opy_.bstack1ll1llll1111_opy_(bstack1ll1lll1l1ll_opy_)
    @staticmethod
    def bstack111l1ll1l11_opy_(builder,params=None):
        bstack1ll1lll1l1ll_opy_ = urljoin(builder, bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬ⒅"))
        if params:
            bstack1ll1lll1l1ll_opy_ += bstack1ll1lll_opy_ (u"ࠧࡅࡻࡾࠤ⒆").format(urlencode({bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⒇"): params.get(bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⒈"))}))
        return bstack111l1ll11l1_opy_.bstack1ll1llll1111_opy_(bstack1ll1lll1l1ll_opy_)
    @staticmethod
    def bstack1ll1llll1111_opy_(bstack1ll1lll1ll1l_opy_):
        bstack1ll1lll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⒉"), os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⒊"), bstack1ll1lll_opy_ (u"ࠪࠫ⒋")))
        headers = {bstack1ll1lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⒌"): bstack1ll1lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⒍").format(bstack1ll1lll1lll1_opy_)}
        response = requests.get(bstack1ll1lll1ll1l_opy_, headers=headers)
        bstack1ll1lll1llll_opy_ = {}
        try:
            bstack1ll1lll1llll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⒎").format(e))
            pass
        if bstack1ll1lll1llll_opy_ is not None:
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⒏")] = response.headers.get(bstack1ll1lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⒐"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⒑")] = response.status_code
        return bstack1ll1lll1llll_opy_
    @staticmethod
    def bstack1ll1llll11l1_opy_(bstack1ll1lll1l1l1_opy_, data):
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࠧ⒒"))
        return bstack111l1ll11l1_opy_.bstack1ll1llll111l_opy_(bstack1ll1lll_opy_ (u"ࠫࡕࡕࡓࡕࠩ⒓"), bstack1ll1lll1l1l1_opy_, data=data)
    @staticmethod
    def bstack1ll1lll1ll11_opy_(bstack1ll1lll1l1l1_opy_, data):
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡨࡧࡷࡘࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡷࠧ⒔"))
        res = bstack111l1ll11l1_opy_.bstack1ll1llll111l_opy_(bstack1ll1lll_opy_ (u"࠭ࡇࡆࡖࠪ⒕"), bstack1ll1lll1l1l1_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1llll111l_opy_(method, bstack1ll1lll1l1l1_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1lll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⒖"), bstack1ll1lll_opy_ (u"ࠨࠩ⒗"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⒘"): bstack1ll1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⒙").format(bstack1ll1lll1lll1_opy_),
            bstack1ll1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒚"): bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⒛"),
            bstack1ll1lll_opy_ (u"࠭ࡁࡤࡥࡨࡴࡹ࠭⒜"): bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⒝")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111l11l11ll_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠱ࠥ⒞") + bstack1ll1lll1l1l1_opy_.lstrip(bstack1ll1lll_opy_ (u"ࠩ࠲ࠫ⒟"))
        try:
            if method == bstack1ll1lll_opy_ (u"ࠪࡋࡊ࡚ࠧ⒠"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll1lll_opy_ (u"ࠫࡕࡕࡓࡕࠩ⒡"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll1lll_opy_ (u"ࠬࡖࡕࡕࠩ⒢"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⒣").format(method))
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡ࡯ࡤࡨࡪࠦࡴࡰࠢࡘࡖࡑࡀࠠࡼࡿࠣࡻ࡮ࡺࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧ⒤").format(url, method))
            bstack1ll1lll1llll_opy_ = {}
            try:
                bstack1ll1lll1llll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ⒥").format(e, response.text))
            if bstack1ll1lll1llll_opy_ is not None:
                bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒦")] = response.headers.get(
                    bstack1ll1lll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⒧"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⒨")] = response.status_code
            return bstack1ll1lll1llll_opy_
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ⒩").format(e, url))
            return None
    @staticmethod
    def bstack1111lll111l_opy_(bstack1ll1lll1ll1l_opy_, data):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡕ࡛ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⒪")
        bstack1ll1lll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⒫"), bstack1ll1lll_opy_ (u"ࠨࠩ⒬"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⒭"): bstack1ll1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⒮").format(bstack1ll1lll1lll1_opy_),
            bstack1ll1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒯"): bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⒰")
        }
        response = requests.put(bstack1ll1lll1ll1l_opy_, headers=headers, json=data)
        bstack1ll1lll1llll_opy_ = {}
        try:
            bstack1ll1lll1llll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⒱").format(e))
            pass
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡱࡷࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⒲").format(bstack1ll1lll1llll_opy_))
        if bstack1ll1lll1llll_opy_ is not None:
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⒳")] = response.headers.get(
                bstack1ll1lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒴"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⒵")] = response.status_code
        return bstack1ll1lll1llll_opy_
    @staticmethod
    def bstack1111ll1ll1l_opy_(bstack1ll1lll1ll1l_opy_):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡊࡉ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣ࡫ࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤⒶ")
        bstack1ll1lll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩⒷ"), bstack1ll1lll_opy_ (u"࠭ࠧⒸ"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧⒹ"): bstack1ll1lll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫⒺ").format(bstack1ll1lll1lll1_opy_),
            bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨⒻ"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ⓖ")
        }
        response = requests.get(bstack1ll1lll1ll1l_opy_, headers=headers)
        bstack1ll1lll1llll_opy_ = {}
        try:
            bstack1ll1lll1llll_opy_ = response.json()
            logger.debug(bstack1ll1lll_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤ࡬࡫ࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨⒽ").format(bstack1ll1lll1llll_opy_))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤⒾ").format(e, response.text))
            pass
        if bstack1ll1lll1llll_opy_ is not None:
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧⒿ")] = response.headers.get(
                bstack1ll1lll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨⓀ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lll1llll_opy_[bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨⓁ")] = response.status_code
        return bstack1ll1lll1llll_opy_
    @staticmethod
    def bstack1llll1111l1l_opy_(bstack111l1lll111_opy_, payload):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡍࡢ࡭ࡨࡷࠥࡧࠠࡑࡑࡖࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤࡆࡖࡉࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡼࡰࡴࡧࡤࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡲࡦࡳࡸࡩࡸࡺࠠࡱࡣࡼࡰࡴࡧࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡁࡑࡋ࠯ࠤࡴࡸࠠࡏࡱࡱࡩࠥ࡯ࡦࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨⓂ")
        try:
            url = bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠵ࡻࡾࠤⓃ").format(bstack111l11l11ll_opy_, bstack111l1lll111_opy_)
            bstack1ll1lll1lll1_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨⓄ"), bstack1ll1lll_opy_ (u"ࠬ࠭Ⓟ"))
            headers = {
                bstack1ll1lll_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ⓠ"): bstack1ll1lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪⓇ").format(bstack1ll1lll1lll1_opy_),
                bstack1ll1lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧⓈ"): bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬⓉ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1llll11ll_opy_ = [200, 202]
            if response.status_code in bstack1ll1llll11ll_opy_:
                return response.json()
            else:
                logger.error(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤ࠲࡙ࠥࡴࡢࡶࡸࡷ࠿ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤⓊ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡹࡴࡠࡥࡲࡰࡱ࡫ࡣࡵࡡࡥࡹ࡮ࡲࡤࡠࡦࡤࡸࡦࡀࠠࡼࡿࠥⓋ").format(e))
            return None