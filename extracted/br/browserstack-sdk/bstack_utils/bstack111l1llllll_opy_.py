# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111l111l111_opy_
logger = logging.getLogger(__name__)
class bstack111l1lllll1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1llll11ll_opy_ = urljoin(builder, bstack1l1_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹࠧ⑥"))
        if params:
            bstack1ll1llll11ll_opy_ += bstack1l1_opy_ (u"ࠣࡁࡾࢁࠧ⑦").format(urlencode({bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⑧"): params.get(bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⑨"))}))
        return bstack111l1lllll1_opy_.bstack1ll1llll1l1l_opy_(bstack1ll1llll11ll_opy_)
    @staticmethod
    def bstack111l1lll1l1_opy_(builder,params=None):
        bstack1ll1llll11ll_opy_ = urljoin(builder, bstack1l1_opy_ (u"ࠫ࡮ࡹࡳࡶࡧࡶ࠱ࡸࡻ࡭࡮ࡣࡵࡽࠬ⑩"))
        if params:
            bstack1ll1llll11ll_opy_ += bstack1l1_opy_ (u"ࠧࡅࡻࡾࠤ⑪").format(urlencode({bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⑫"): params.get(bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⑬"))}))
        return bstack111l1lllll1_opy_.bstack1ll1llll1l1l_opy_(bstack1ll1llll11ll_opy_)
    @staticmethod
    def bstack1ll1llll1l1l_opy_(bstack1ll1lllll1l1_opy_):
        bstack1ll1lllll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⑭"), os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⑮"), bstack1l1_opy_ (u"ࠪࠫ⑯")))
        headers = {bstack1l1_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⑰"): bstack1l1_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⑱").format(bstack1ll1lllll111_opy_)}
        response = requests.get(bstack1ll1lllll1l1_opy_, headers=headers)
        bstack1ll1llll11l1_opy_ = {}
        try:
            bstack1ll1llll11l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⑲").format(e))
            pass
        if bstack1ll1llll11l1_opy_ is not None:
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⑳")] = response.headers.get(bstack1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⑴"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⑵")] = response.status_code
        return bstack1ll1llll11l1_opy_
    @staticmethod
    def bstack1ll1llll1l11_opy_(bstack1ll1lllll11l_opy_, data):
        logger.debug(bstack1l1_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥࡺࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡕࡳࡰ࡮ࡺࡔࡦࡵࡷࡷࠧ⑶"))
        return bstack111l1lllll1_opy_.bstack1ll1lllll1ll_opy_(bstack1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩ⑷"), bstack1ll1lllll11l_opy_, data=data)
    @staticmethod
    def bstack1ll1llll1lll_opy_(bstack1ll1lllll11l_opy_, data):
        logger.debug(bstack1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡨࡧࡷࡘࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡏࡳࡦࡨࡶࡪࡪࡔࡦࡵࡷࡷࠧ⑸"))
        res = bstack111l1lllll1_opy_.bstack1ll1lllll1ll_opy_(bstack1l1_opy_ (u"࠭ࡇࡆࡖࠪ⑹"), bstack1ll1lllll11l_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1lllll1ll_opy_(method, bstack1ll1lllll11l_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1lllll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⑺"), bstack1l1_opy_ (u"ࠨࠩ⑻"))
        headers = {
            bstack1l1_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⑼"): bstack1l1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⑽").format(bstack1ll1lllll111_opy_),
            bstack1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⑾"): bstack1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⑿"),
            bstack1l1_opy_ (u"࠭ࡁࡤࡥࡨࡴࡹ࠭⒀"): bstack1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⒁")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111l111l111_opy_ + bstack1l1_opy_ (u"ࠣ࠱ࠥ⒂") + bstack1ll1lllll11l_opy_.lstrip(bstack1l1_opy_ (u"ࠩ࠲ࠫ⒃"))
        try:
            if method == bstack1l1_opy_ (u"ࠪࡋࡊ࡚ࠧ⒄"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩ⒅"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1_opy_ (u"ࠬࡖࡕࡕࠩ⒆"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1_opy_ (u"ࠨࡕ࡯ࡵࡸࡴࡵࡵࡲࡵࡧࡧࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࡿࢂࠨ⒇").format(method))
            logger.debug(bstack1l1_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡ࡯ࡤࡨࡪࠦࡴࡰࠢࡘࡖࡑࡀࠠࡼࡿࠣࡻ࡮ࡺࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧ⒈").format(url, method))
            bstack1ll1llll11l1_opy_ = {}
            try:
                bstack1ll1llll11l1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ⒉").format(e, response.text))
            if bstack1ll1llll11l1_opy_ is not None:
                bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒊")] = response.headers.get(
                    bstack1l1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⒋"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⒌")] = response.status_code
            return bstack1ll1llll11l1_opy_
        except Exception as e:
            logger.error(bstack1l1_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ⒍").format(e, url))
            return None
    @staticmethod
    def bstack1111lll11l1_opy_(bstack1ll1lllll1l1_opy_, data):
        bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡕ࡛ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡹ࡮ࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⒎")
        bstack1ll1lllll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⒏"), bstack1l1_opy_ (u"ࠨࠩ⒐"))
        headers = {
            bstack1l1_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⒑"): bstack1l1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⒒").format(bstack1ll1lllll111_opy_),
            bstack1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒓"): bstack1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⒔")
        }
        response = requests.put(bstack1ll1lllll1l1_opy_, headers=headers, json=data)
        bstack1ll1llll11l1_opy_ = {}
        try:
            bstack1ll1llll11l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⒕").format(e))
            pass
        logger.debug(bstack1l1_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡱࡷࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⒖").format(bstack1ll1llll11l1_opy_))
        if bstack1ll1llll11l1_opy_ is not None:
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⒗")] = response.headers.get(
                bstack1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒘"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⒙")] = response.status_code
        return bstack1ll1llll11l1_opy_
    @staticmethod
    def bstack1111lllll11_opy_(bstack1ll1lllll1l1_opy_):
        bstack1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡊࡉ࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣ࡫ࡪࡺࠠࡵࡪࡨࠤࡨࡵࡵ࡯ࡶࠣࡳ࡫ࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⒚")
        bstack1ll1lllll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⒛"), bstack1l1_opy_ (u"࠭ࠧ⒜"))
        headers = {
            bstack1l1_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⒝"): bstack1l1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⒞").format(bstack1ll1lllll111_opy_),
            bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⒟"): bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⒠")
        }
        response = requests.get(bstack1ll1lllll1l1_opy_, headers=headers)
        bstack1ll1llll11l1_opy_ = {}
        try:
            bstack1ll1llll11l1_opy_ = response.json()
            logger.debug(bstack1l1_opy_ (u"ࠦࡗ࡫ࡱࡶࡧࡶࡸ࡚ࡺࡩ࡭ࡵ࠽ࠤ࡬࡫ࡴࡠࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨ⒡").format(bstack1ll1llll11l1_opy_))
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠤ࠲ࠦࡻࡾࠤ⒢").format(e, response.text))
            pass
        if bstack1ll1llll11l1_opy_ is not None:
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⒣")] = response.headers.get(
                bstack1l1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⒤"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1llll11l1_opy_[bstack1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⒥")] = response.status_code
        return bstack1ll1llll11l1_opy_
    @staticmethod
    def bstack1llll1111ll1_opy_(bstack111ll111111_opy_, payload):
        bstack1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡍࡢ࡭ࡨࡷࠥࡧࠠࡑࡑࡖࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡷ࡬ࡪࠦࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡣࡷ࡬ࡰࡩ࠳ࡤࡢࡶࡤࠤࡪࡴࡤࡱࡱ࡬ࡲࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡫࡮ࡥࡲࡲ࡭ࡳࡺࠠࠩࡵࡷࡶ࠮ࡀࠠࡕࡪࡨࠤࡆࡖࡉࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡱࡣࡼࡰࡴࡧࡤࠡࠪࡧ࡭ࡨࡺࠩ࠻ࠢࡗ࡬ࡪࠦࡲࡦࡳࡸࡩࡸࡺࠠࡱࡣࡼࡰࡴࡧࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡨ࡮ࡩࡴ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡁࡑࡋ࠯ࠤࡴࡸࠠࡏࡱࡱࡩࠥ࡯ࡦࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⒦")
        try:
            url = bstack1l1_opy_ (u"ࠥࡿࢂ࠵ࡻࡾࠤ⒧").format(bstack111l111l111_opy_, bstack111ll111111_opy_)
            bstack1ll1lllll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⒨"), bstack1l1_opy_ (u"ࠬ࠭⒩"))
            headers = {
                bstack1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⒪"): bstack1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⒫").format(bstack1ll1lllll111_opy_),
                bstack1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⒬"): bstack1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⒭")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1llll1ll1_opy_ = [200, 202]
            if response.status_code in bstack1ll1llll1ll1_opy_:
                return response.json()
            else:
                logger.error(bstack1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡣࡷ࡬ࡰࡩࠦࡤࡢࡶࡤ࠲࡙ࠥࡴࡢࡶࡸࡷ࠿ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⒮").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡹࡴࡠࡥࡲࡰࡱ࡫ࡣࡵࡡࡥࡹ࡮ࡲࡤࡠࡦࡤࡸࡦࡀࠠࡼࡿࠥ⒯").format(e))
            return None