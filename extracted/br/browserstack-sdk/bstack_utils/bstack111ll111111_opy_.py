# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111l11l1l1l_opy_
logger = logging.getLogger(__name__)
class bstack111l1llll11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1lllll11l_opy_ = urljoin(builder, bstack11lll1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪ⑚"))
        if params:
            bstack1ll1lllll11l_opy_ += bstack11lll1_opy_ (u"ࠦࡄࢁࡽࠣ⑛").format(urlencode({bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⑜"): params.get(bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⑝"))}))
        return bstack111l1llll11_opy_.bstack1ll1llll1ll1_opy_(bstack1ll1lllll11l_opy_)
    @staticmethod
    def bstack111ll1111ll_opy_(builder,params=None):
        bstack1ll1lllll11l_opy_ = urljoin(builder, bstack11lll1_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ⑞"))
        if params:
            bstack1ll1lllll11l_opy_ += bstack11lll1_opy_ (u"ࠣࡁࡾࢁࠧ⑟").format(urlencode({bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ①"): params.get(bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ②"))}))
        return bstack111l1llll11_opy_.bstack1ll1llll1ll1_opy_(bstack1ll1lllll11l_opy_)
    @staticmethod
    def bstack1ll1llll1ll1_opy_(bstack1ll1llllll1l_opy_):
        bstack1ll1lllll1l1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ③"), os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ④"), bstack11lll1_opy_ (u"࠭ࠧ⑤")))
        headers = {bstack11lll1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⑥"): bstack11lll1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⑦").format(bstack1ll1lllll1l1_opy_)}
        response = requests.get(bstack1ll1llllll1l_opy_, headers=headers)
        bstack1ll1llllllll_opy_ = {}
        try:
            bstack1ll1llllllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⑧").format(e))
            pass
        if bstack1ll1llllllll_opy_ is not None:
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⑨")] = response.headers.get(bstack11lll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⑩"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⑪")] = response.status_code
        return bstack1ll1llllllll_opy_
    @staticmethod
    def bstack1ll1lllll111_opy_(bstack1ll1lllllll1_opy_, data):
        logger.debug(bstack11lll1_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࠣ⑫"))
        return bstack111l1llll11_opy_.bstack1ll1llllll11_opy_(bstack11lll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ⑬"), bstack1ll1lllllll1_opy_, data=data)
    @staticmethod
    def bstack1ll1lllll1ll_opy_(bstack1ll1lllllll1_opy_, data):
        logger.debug(bstack11lll1_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣ࡫ࡪࡺࡔࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡳࠣ⑭"))
        res = bstack111l1llll11_opy_.bstack1ll1llllll11_opy_(bstack11lll1_opy_ (u"ࠩࡊࡉ࡙࠭⑮"), bstack1ll1lllllll1_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1llllll11_opy_(method, bstack1ll1lllllll1_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1lllll1l1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⑯"), bstack11lll1_opy_ (u"ࠫࠬ⑰"))
        headers = {
            bstack11lll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⑱"): bstack11lll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⑲").format(bstack1ll1lllll1l1_opy_),
            bstack11lll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⑳"): bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⑴"),
            bstack11lll1_opy_ (u"ࠩࡄࡧࡨ࡫ࡰࡵࠩ⑵"): bstack11lll1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⑶")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111l11l1l1l_opy_ + bstack11lll1_opy_ (u"ࠦ࠴ࠨ⑷") + bstack1ll1lllllll1_opy_.lstrip(bstack11lll1_opy_ (u"ࠬ࠵ࠧ⑸"))
        try:
            if method == bstack11lll1_opy_ (u"࠭ࡇࡆࡖࠪ⑹"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11lll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ⑺"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11lll1_opy_ (u"ࠨࡒࡘࡘࠬ⑻"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11lll1_opy_ (u"ࠤࡘࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤ⑼").format(method))
            logger.debug(bstack11lll1_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡲࡧࡤࡦࠢࡷࡳ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ⑽").format(url, method))
            bstack1ll1llllllll_opy_ = {}
            try:
                bstack1ll1llllllll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11lll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣ⑾").format(e, response.text))
            if bstack1ll1llllllll_opy_ is not None:
                bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⑿")] = response.headers.get(
                    bstack11lll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⒀"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⒁")] = response.status_code
            return bstack1ll1llllllll_opy_
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ⒂").format(e, url))
            return None
    @staticmethod
    def bstack1111lllll1l_opy_(bstack1ll1llllll1l_opy_, data):
        bstack11lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⒃")
        bstack1ll1lllll1l1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⒄"), bstack11lll1_opy_ (u"ࠫࠬ⒅"))
        headers = {
            bstack11lll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⒆"): bstack11lll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⒇").format(bstack1ll1lllll1l1_opy_),
            bstack11lll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⒈"): bstack11lll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⒉")
        }
        response = requests.put(bstack1ll1llllll1l_opy_, headers=headers, json=data)
        bstack1ll1llllllll_opy_ = {}
        try:
            bstack1ll1llllllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⒊").format(e))
            pass
        logger.debug(bstack11lll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⒋").format(bstack1ll1llllllll_opy_))
        if bstack1ll1llllllll_opy_ is not None:
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⒌")] = response.headers.get(
                bstack11lll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⒍"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⒎")] = response.status_code
        return bstack1ll1llllllll_opy_
    @staticmethod
    def bstack1111llll1ll_opy_(bstack1ll1llllll1l_opy_):
        bstack11lll1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ⒏")
        bstack1ll1lllll1l1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⒐"), bstack11lll1_opy_ (u"ࠩࠪ⒑"))
        headers = {
            bstack11lll1_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ⒒"): bstack11lll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ⒓").format(bstack1ll1lllll1l1_opy_),
            bstack11lll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⒔"): bstack11lll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⒕")
        }
        response = requests.get(bstack1ll1llllll1l_opy_, headers=headers)
        bstack1ll1llllllll_opy_ = {}
        try:
            bstack1ll1llllllll_opy_ = response.json()
            logger.debug(bstack11lll1_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ⒖").format(bstack1ll1llllllll_opy_))
        except Exception as e:
            logger.debug(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ⒗").format(e, response.text))
            pass
        if bstack1ll1llllllll_opy_ is not None:
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒘")] = response.headers.get(
                bstack11lll1_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⒙"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1llllllll_opy_[bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⒚")] = response.status_code
        return bstack1ll1llllllll_opy_
    @staticmethod
    def bstack1llll1l1l1l1_opy_(bstack111ll111l1l_opy_, payload):
        bstack11lll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡰ࡫ࡳࠡࡣࠣࡔࡔ࡙ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡂࡒࡌࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡵࡩࡶࡻࡥࡴࡶࠣࡴࡦࡿ࡬ࡰࡣࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡄࡔࡎ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⒛")
        try:
            url = bstack11lll1_opy_ (u"ࠨࡻࡾ࠱ࡾࢁࠧ⒜").format(bstack111l11l1l1l_opy_, bstack111ll111l1l_opy_)
            bstack1ll1lllll1l1_opy_ = os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⒝"), bstack11lll1_opy_ (u"ࠨࠩ⒞"))
            headers = {
                bstack11lll1_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⒟"): bstack11lll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⒠").format(bstack1ll1lllll1l1_opy_),
                bstack11lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒡"): bstack11lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⒢")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1llll1lll_opy_ = [200, 202]
            if response.status_code in bstack1ll1llll1lll_opy_:
                return response.json()
            else:
                logger.error(bstack11lll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧ࠮ࠡࡕࡷࡥࡹࡻࡳ࠻ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ⒣").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡵࡷࡣࡨࡵ࡬࡭ࡧࡦࡸࡤࡨࡵࡪ࡮ࡧࡣࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ⒤").format(e))
            return None