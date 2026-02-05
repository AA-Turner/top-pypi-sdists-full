# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l1111ll1l_opy_
logger = logging.getLogger(__name__)
class bstack11l11lll1l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lll1lll1l11_opy_ = urljoin(builder, bstack11l1ll1_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠭ℱ"))
        if params:
            bstack1lll1lll1l11_opy_ += bstack11l1ll1_opy_ (u"ࠢࡀࡽࢀࠦℲ").format(urlencode({bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨℳ"): params.get(bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩℴ"))}))
        return bstack11l11lll1l1_opy_.bstack1lll1lll11ll_opy_(bstack1lll1lll1l11_opy_)
    @staticmethod
    def bstack11l11lll111_opy_(builder,params=None):
        bstack1lll1lll1l11_opy_ = urljoin(builder, bstack11l1ll1_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵ࠰ࡷࡺࡳ࡭ࡢࡴࡼࠫℵ"))
        if params:
            bstack1lll1lll1l11_opy_ += bstack11l1ll1_opy_ (u"ࠦࡄࢁࡽࠣℶ").format(urlencode({bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬℷ"): params.get(bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ℸ"))}))
        return bstack11l11lll1l1_opy_.bstack1lll1lll11ll_opy_(bstack1lll1lll1l11_opy_)
    @staticmethod
    def bstack1lll1lll11ll_opy_(bstack1lll1lll11l1_opy_):
        bstack1lll1lll1ll1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬℹ"), os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ℺"), bstack11l1ll1_opy_ (u"ࠩࠪ℻")))
        headers = {bstack11l1ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪℼ"): bstack11l1ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧℽ").format(bstack1lll1lll1ll1_opy_)}
        response = requests.get(bstack1lll1lll11l1_opy_, headers=headers)
        bstack1lll1lll1111_opy_ = {}
        try:
            bstack1lll1lll1111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦℾ").format(e))
            pass
        if bstack1lll1lll1111_opy_ is not None:
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧℿ")] = response.headers.get(bstack11l1ll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⅀"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⅁")] = response.status_code
        return bstack1lll1lll1111_opy_
    @staticmethod
    def bstack1lll1lll111l_opy_(bstack1lll1lll1l1l_opy_, data):
        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࡔࡲ࡯࡭ࡹ࡚ࡥࡴࡶࡶࠦ⅂"))
        return bstack11l11lll1l1_opy_.bstack1lll1ll1ll1l_opy_(bstack11l1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⅃"), bstack1lll1lll1l1l_opy_, data=data)
    @staticmethod
    def bstack1lll1ll1llll_opy_(bstack1lll1lll1l1l_opy_, data):
        logger.debug(bstack11l1ll1_opy_ (u"ࠦࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡩࡳࡷࠦࡧࡦࡶࡗࡩࡸࡺࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࡕࡲࡥࡧࡵࡩࡩ࡚ࡥࡴࡶࡶࠦ⅄"))
        res = bstack11l11lll1l1_opy_.bstack1lll1ll1ll1l_opy_(bstack11l1ll1_opy_ (u"ࠬࡍࡅࡕࠩⅅ"), bstack1lll1lll1l1l_opy_, data=data)
        return res
    @staticmethod
    def bstack1lll1ll1ll1l_opy_(method, bstack1lll1lll1l1l_opy_, data=None, params=None, extra_headers=None):
        bstack1lll1lll1ll1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪⅆ"), bstack11l1ll1_opy_ (u"ࠧࠨⅇ"))
        headers = {
            bstack11l1ll1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨⅈ"): bstack11l1ll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬⅉ").format(bstack1lll1lll1ll1_opy_),
            bstack11l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⅊"): bstack11l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⅋"),
            bstack11l1ll1_opy_ (u"ࠬࡇࡣࡤࡧࡳࡸࠬ⅌"): bstack11l1ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ⅍")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l1111ll1l_opy_ + bstack11l1ll1_opy_ (u"ࠢ࠰ࠤⅎ") + bstack1lll1lll1l1l_opy_.lstrip(bstack11l1ll1_opy_ (u"ࠨ࠱ࠪ⅏"))
        try:
            if method == bstack11l1ll1_opy_ (u"ࠩࡊࡉ࡙࠭⅐"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11l1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⅑"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11l1ll1_opy_ (u"ࠫࡕ࡛ࡔࠨ⅒"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11l1ll1_opy_ (u"࡛ࠧ࡮ࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡌ࡙࡚ࡐࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࡾࢁࠧ⅓").format(method))
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡏࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡮ࡣࡧࡩࠥࡺ࡯ࠡࡗࡕࡐ࠿ࠦࡻࡾࠢࡺ࡭ࡹ࡮ࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦ⅔").format(url, method))
            bstack1lll1lll1111_opy_ = {}
            try:
                bstack1lll1lll1111_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ⅕").format(e, response.text))
            if bstack1lll1lll1111_opy_ is not None:
                bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⅖")] = response.headers.get(
                    bstack11l1ll1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⅗"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⅘")] = response.status_code
            return bstack1lll1lll1111_opy_
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠦࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶࡧࡶࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⅙").format(e, url))
            return None
    @staticmethod
    def bstack111llll1l1l_opy_(bstack1lll1lll11l1_opy_, data):
        bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡩࡳࡪࡳࠡࡣࠣࡔ࡚࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡸ࡭࡫ࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ⅚")
        bstack1lll1lll1ll1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⅛"), bstack11l1ll1_opy_ (u"ࠧࠨ⅜"))
        headers = {
            bstack11l1ll1_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⅝"): bstack11l1ll1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⅞").format(bstack1lll1lll1ll1_opy_),
            bstack11l1ll1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⅟"): bstack11l1ll1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧⅠ")
        }
        response = requests.put(bstack1lll1lll11l1_opy_, headers=headers, json=data)
        bstack1lll1lll1111_opy_ = {}
        try:
            bstack1lll1lll1111_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡋࡕࡒࡒࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦⅡ").format(e))
            pass
        logger.debug(bstack11l1ll1_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡰࡶࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣⅢ").format(bstack1lll1lll1111_opy_))
        if bstack1lll1lll1111_opy_ is not None:
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨⅣ")] = response.headers.get(
                bstack11l1ll1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩⅤ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩⅥ")] = response.status_code
        return bstack1lll1lll1111_opy_
    @staticmethod
    def bstack111llll1l11_opy_(bstack1lll1lll11l1_opy_):
        bstack11l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡔࡧࡱࡨࡸࠦࡡࠡࡉࡈࡘࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡪࡩࡹࠦࡴࡩࡧࠣࡧࡴࡻ࡮ࡵࠢࡲࡪࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣⅦ")
        bstack1lll1lll1ll1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨⅧ"), bstack11l1ll1_opy_ (u"ࠬ࠭Ⅸ"))
        headers = {
            bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ⅹ"): bstack11l1ll1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪⅪ").format(bstack1lll1lll1ll1_opy_),
            bstack11l1ll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧⅫ"): bstack11l1ll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬⅬ")
        }
        response = requests.get(bstack1lll1lll11l1_opy_, headers=headers)
        bstack1lll1lll1111_opy_ = {}
        try:
            bstack1lll1lll1111_opy_ = response.json()
            logger.debug(bstack11l1ll1_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣ࡫ࡪࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧⅭ").format(bstack1lll1lll1111_opy_))
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣⅮ").format(e, response.text))
            pass
        if bstack1lll1lll1111_opy_ is not None:
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ⅿ")] = response.headers.get(
                bstack11l1ll1_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧⅰ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lll1111_opy_[bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⅱ")] = response.status_code
        return bstack1lll1lll1111_opy_
    @staticmethod
    def bstack11111l111ll_opy_(bstack11l11lllll1_opy_, payload):
        bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡓࡡ࡬ࡧࡶࠤࡦࠦࡐࡐࡕࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡶ࡫ࡩࠥࡩ࡯࡭࡮ࡨࡧࡹ࠳ࡢࡶ࡫࡯ࡨ࠲ࡪࡡࡵࡣࠣࡩࡳࡪࡰࡰ࡫ࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࠨࡴࡶࡵ࠭࠿ࠦࡔࡩࡧࠣࡅࡕࡏࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࠩࡦ࡬ࡧࡹ࠯࠺ࠡࡖ࡫ࡩࠥࡸࡥࡲࡷࡨࡷࡹࠦࡰࡢࡻ࡯ࡳࡦࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡇࡐࡊ࠮ࠣࡳࡷࠦࡎࡰࡰࡨࠤ࡮࡬ࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧⅲ")
        try:
            url = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠴ࢁࡽࠣⅳ").format(bstack11l1111ll1l_opy_, bstack11l11lllll1_opy_)
            bstack1lll1lll1ll1_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⅴ"), bstack11l1ll1_opy_ (u"ࠫࠬⅵ"))
            headers = {
                bstack11l1ll1_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬⅶ"): bstack11l1ll1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩⅷ").format(bstack1lll1lll1ll1_opy_),
                bstack11l1ll1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ⅸ"): bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫⅹ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1lll1ll1lll1_opy_ = [200, 202]
            if response.status_code in bstack1lll1ll1lll1_opy_:
                return response.json()
            else:
                logger.error(bstack11l1ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩ࡯࡭࡮ࡨࡧࡹࠦࡢࡶ࡫࡯ࡨࠥࡪࡡࡵࡣ࠱ࠤࡘࡺࡡࡵࡷࡶ࠾ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣⅺ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡸࡺ࡟ࡤࡱ࡯ࡰࡪࡩࡴࡠࡤࡸ࡭ࡱࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡻࡾࠤⅻ").format(e))
            return None