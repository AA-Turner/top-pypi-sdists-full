# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l111ll1ll_opy_
logger = logging.getLogger(__name__)
class bstack11l11ll1l11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lll1ll1l1l1_opy_ = urljoin(builder, bstack11lllll_opy_ (u"ࠪ࡭ࡸࡹࡵࡦࡵࠪ⅑"))
        if params:
            bstack1lll1ll1l1l1_opy_ += bstack11lllll_opy_ (u"ࠦࡄࢁࡽࠣ⅒").format(urlencode({bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅓"): params.get(bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅔"))}))
        return bstack11l11ll1l11_opy_.bstack1lll1ll1llll_opy_(bstack1lll1ll1l1l1_opy_)
    @staticmethod
    def bstack11l11ll1l1l_opy_(builder,params=None):
        bstack1lll1ll1l1l1_opy_ = urljoin(builder, bstack11lllll_opy_ (u"ࠧࡪࡵࡶࡹࡪࡹ࠭ࡴࡷࡰࡱࡦࡸࡹࠨ⅕"))
        if params:
            bstack1lll1ll1l1l1_opy_ += bstack11lllll_opy_ (u"ࠣࡁࡾࢁࠧ⅖").format(urlencode({bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅗"): params.get(bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅘"))}))
        return bstack11l11ll1l11_opy_.bstack1lll1ll1llll_opy_(bstack1lll1ll1l1l1_opy_)
    @staticmethod
    def bstack1lll1ll1llll_opy_(bstack1lll1lll1111_opy_):
        bstack1lll1ll1l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⅙"), os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⅚"), bstack11lllll_opy_ (u"࠭ࠧ⅛")))
        headers = {bstack11lllll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⅜"): bstack11lllll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⅝").format(bstack1lll1ll1l111_opy_)}
        response = requests.get(bstack1lll1lll1111_opy_, headers=headers)
        bstack1lll1ll11lll_opy_ = {}
        try:
            bstack1lll1ll11lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⅞").format(e))
            pass
        if bstack1lll1ll11lll_opy_ is not None:
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⅟")] = response.headers.get(bstack11lllll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬⅠ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⅡ")] = response.status_code
        return bstack1lll1ll11lll_opy_
    @staticmethod
    def bstack1lll1ll1ll1l_opy_(bstack1lll1ll1l1ll_opy_, data):
        logger.debug(bstack11lllll_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡫ࡵࡲࠡࡶࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡘࡶ࡬ࡪࡶࡗࡩࡸࡺࡳࠣⅢ"))
        return bstack11l11ll1l11_opy_.bstack1lll1ll1l11l_opy_(bstack11lllll_opy_ (u"ࠧࡑࡑࡖࡘࠬⅣ"), bstack1lll1ll1l1ll_opy_, data=data)
    @staticmethod
    def bstack1lll1ll1ll11_opy_(bstack1lll1ll1l1ll_opy_, data):
        logger.debug(bstack11lllll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣ࡫ࡪࡺࡔࡦࡵࡷࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࡒࡶࡩ࡫ࡲࡦࡦࡗࡩࡸࡺࡳࠣⅤ"))
        res = bstack11l11ll1l11_opy_.bstack1lll1ll1l11l_opy_(bstack11lllll_opy_ (u"ࠩࡊࡉ࡙࠭Ⅵ"), bstack1lll1ll1l1ll_opy_, data=data)
        return res
    @staticmethod
    def bstack1lll1ll1l11l_opy_(method, bstack1lll1ll1l1ll_opy_, data=None, params=None, extra_headers=None):
        bstack1lll1ll1l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⅦ"), bstack11lllll_opy_ (u"ࠫࠬⅧ"))
        headers = {
            bstack11lllll_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬⅨ"): bstack11lllll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩⅩ").format(bstack1lll1ll1l111_opy_),
            bstack11lllll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭Ⅺ"): bstack11lllll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫⅫ"),
            bstack11lllll_opy_ (u"ࠩࡄࡧࡨ࡫ࡰࡵࠩⅬ"): bstack11lllll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ⅽ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l111ll1ll_opy_ + bstack11lllll_opy_ (u"ࠦ࠴ࠨⅮ") + bstack1lll1ll1l1ll_opy_.lstrip(bstack11lllll_opy_ (u"ࠬ࠵ࠧⅯ"))
        try:
            if method == bstack11lllll_opy_ (u"࠭ࡇࡆࡖࠪⅰ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11lllll_opy_ (u"ࠧࡑࡑࡖࡘࠬⅱ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11lllll_opy_ (u"ࠨࡒࡘࡘࠬⅲ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11lllll_opy_ (u"ࠤࡘࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡉࡖࡗࡔࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࡻࡾࠤⅳ").format(method))
            logger.debug(bstack11lllll_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡲࡧࡤࡦࠢࡷࡳ࡛ࠥࡒࡍ࠼ࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣⅴ").format(url, method))
            bstack1lll1ll11lll_opy_ = {}
            try:
                bstack1lll1ll11lll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11lllll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠣ࠱ࠥࢁࡽࠣⅵ").format(e, response.text))
            if bstack1lll1ll11lll_opy_ is not None:
                bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ⅶ")] = response.headers.get(
                    bstack11lllll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧⅷ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⅸ")] = response.status_code
            return bstack1lll1ll11lll_opy_
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠣࡑࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦⅹ").format(e, url))
            return None
    @staticmethod
    def bstack111lllll11l_opy_(bstack1lll1lll1111_opy_, data):
        bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡑࡗࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡵࡪࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢⅺ")
        bstack1lll1ll1l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⅻ"), bstack11lllll_opy_ (u"ࠫࠬⅼ"))
        headers = {
            bstack11lllll_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬⅽ"): bstack11lllll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩⅾ").format(bstack1lll1ll1l111_opy_),
            bstack11lllll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ⅿ"): bstack11lllll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫↀ")
        }
        response = requests.put(bstack1lll1lll1111_opy_, headers=headers, json=data)
        bstack1lll1ll11lll_opy_ = {}
        try:
            bstack1lll1ll11lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡏ࡙ࡏࡏࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣↁ").format(e))
            pass
        logger.debug(bstack11lllll_opy_ (u"ࠥࡖࡪࡷࡵࡦࡵࡷ࡙ࡹ࡯࡬ࡴ࠼ࠣࡴࡺࡺ࡟ࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧↂ").format(bstack1lll1ll11lll_opy_))
        if bstack1lll1ll11lll_opy_ is not None:
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬↃ")] = response.headers.get(
                bstack11lllll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭ↄ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ↅ")] = response.status_code
        return bstack1lll1ll11lll_opy_
    @staticmethod
    def bstack111llll11ll_opy_(bstack1lll1lll1111_opy_):
        bstack11lllll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘ࡫࡮ࡥࡵࠣࡥࠥࡍࡅࡕࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡧࡦࡶࠣࡸ࡭࡫ࠠࡤࡱࡸࡲࡹࠦ࡯ࡧࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧↆ")
        bstack1lll1ll1l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬↇ"), bstack11lllll_opy_ (u"ࠩࠪↈ"))
        headers = {
            bstack11lllll_opy_ (u"ࠪࡥࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ↉"): bstack11lllll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ↊").format(bstack1lll1ll1l111_opy_),
            bstack11lllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ↋"): bstack11lllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ↌")
        }
        response = requests.get(bstack1lll1lll1111_opy_, headers=headers)
        bstack1lll1ll11lll_opy_ = {}
        try:
            bstack1lll1ll11lll_opy_ = response.json()
            logger.debug(bstack11lllll_opy_ (u"ࠢࡓࡧࡴࡹࡪࡹࡴࡖࡶ࡬ࡰࡸࡀࠠࡨࡧࡷࡣ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠤ↍").format(bstack1lll1ll11lll_opy_))
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠠ࠮ࠢࡾࢁࠧ↎").format(e, response.text))
            pass
        if bstack1lll1ll11lll_opy_ is not None:
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ↏")] = response.headers.get(
                bstack11lllll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ←"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1ll11lll_opy_[bstack11lllll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ↑")] = response.status_code
        return bstack1lll1ll11lll_opy_
    @staticmethod
    def bstack1lllllll11ll_opy_(bstack11l11ll1ll1_opy_, payload):
        bstack11lllll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡐࡥࡰ࡫ࡳࠡࡣࠣࡔࡔ࡙ࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥࡺࡨࡦࠢࡦࡳࡱࡲࡥࡤࡶ࠰ࡦࡺ࡯࡬ࡥ࠯ࡧࡥࡹࡧࠠࡦࡰࡧࡴࡴ࡯࡮ࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧࡱࡨࡵࡵࡩ࡯ࡶࠣࠬࡸࡺࡲࠪ࠼ࠣࡘ࡭࡫ࠠࡂࡒࡌࠤࡪࡴࡤࡱࡱ࡬ࡲࡹࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࠭ࡪࡩࡤࡶࠬ࠾࡚ࠥࡨࡦࠢࡵࡩࡶࡻࡥࡴࡶࠣࡴࡦࡿ࡬ࡰࡣࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡄࡔࡎ࠲ࠠࡰࡴࠣࡒࡴࡴࡥࠡ࡫ࡩࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ→")
        try:
            url = bstack11lllll_opy_ (u"ࠨࡻࡾ࠱ࡾࢁࠧ↓").format(bstack11l111ll1ll_opy_, bstack11l11ll1ll1_opy_)
            bstack1lll1ll1l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ↔"), bstack11lllll_opy_ (u"ࠨࠩ↕"))
            headers = {
                bstack11lllll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ↖"): bstack11lllll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭↗").format(bstack1lll1ll1l111_opy_),
                bstack11lllll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ↘"): bstack11lllll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ↙")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1lll1ll1lll1_opy_ = [200, 202]
            if response.status_code in bstack1lll1ll1lll1_opy_:
                return response.json()
            else:
                logger.error(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡱࡲࡥࡤࡶࠣࡦࡺ࡯࡬ࡥࠢࡧࡥࡹࡧ࠮ࠡࡕࡷࡥࡹࡻࡳ࠻ࠢࡾࢁ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠧ↚").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡵࡷࡣࡨࡵ࡬࡭ࡧࡦࡸࡤࡨࡵࡪ࡮ࡧࡣࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ↛").format(e))
            return None