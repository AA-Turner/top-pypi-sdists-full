# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11111l1l1l1_opy_
logger = logging.getLogger(__name__)
class bstack11111llllll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll11ll1l1l1_opy_ = urljoin(builder, bstack111ll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩ⛫"))
        if params:
            bstack1ll11ll1l1l1_opy_ += bstack111ll_opy_ (u"ࠥࡃࢀࢃࠢ⛬").format(urlencode({bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⛭"): params.get(bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⛮"))}))
        return bstack11111llllll_opy_.bstack1ll11ll1ll11_opy_(bstack1ll11ll1l1l1_opy_)
    @staticmethod
    def bstack11111llll1l_opy_(builder,params=None):
        bstack1ll11ll1l1l1_opy_ = urljoin(builder, bstack111ll_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧ⛯"))
        if params:
            bstack1ll11ll1l1l1_opy_ += bstack111ll_opy_ (u"ࠢࡀࡽࢀࠦ⛰").format(urlencode({bstack111ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⛱"): params.get(bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⛲"))}))
        return bstack11111llllll_opy_.bstack1ll11ll1ll11_opy_(bstack1ll11ll1l1l1_opy_)
    @staticmethod
    def bstack1ll11ll1ll11_opy_(bstack1ll11ll1l11l_opy_):
        bstack1ll11ll1l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⛳"), os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⛴"), bstack111ll_opy_ (u"ࠬ࠭⛵")))
        headers = {bstack111ll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⛶"): bstack111ll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⛷").format(bstack1ll11ll1l1ll_opy_)}
        response = requests.get(bstack1ll11ll1l11l_opy_, headers=headers)
        bstack1ll11lll11l1_opy_ = {}
        try:
            bstack1ll11lll11l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⛸").format(e))
            pass
        if bstack1ll11lll11l1_opy_ is not None:
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⛹")] = response.headers.get(bstack111ll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⛺"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⛻")] = response.status_code
        return bstack1ll11lll11l1_opy_
    @staticmethod
    def bstack1ll11lll1111_opy_(bstack1ll11lll111l_opy_, data):
        logger.debug(bstack111ll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢ⛼"))
        return bstack11111llllll_opy_.bstack1ll11ll1ll1l_opy_(bstack111ll_opy_ (u"࠭ࡐࡐࡕࡗࠫ⛽"), bstack1ll11lll111l_opy_, data=data)
    @staticmethod
    def bstack1ll11ll1lll1_opy_(bstack1ll11lll111l_opy_, data):
        logger.debug(bstack111ll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢ⛾"))
        res = bstack11111llllll_opy_.bstack1ll11ll1ll1l_opy_(bstack111ll_opy_ (u"ࠨࡉࡈࡘࠬ⛿"), bstack1ll11lll111l_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll11ll1ll1l_opy_(method, bstack1ll11lll111l_opy_, data=None, params=None, extra_headers=None):
        bstack1ll11ll1l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭✀"), bstack111ll_opy_ (u"ࠪࠫ✁"))
        headers = {
            bstack111ll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ✂"): bstack111ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ✃").format(bstack1ll11ll1l1ll_opy_),
            bstack111ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ✄"): bstack111ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ✅"),
            bstack111ll_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨ✆"): bstack111ll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ✇")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11111l1l1l1_opy_ + bstack111ll_opy_ (u"ࠥ࠳ࠧ✈") + bstack1ll11lll111l_opy_.lstrip(bstack111ll_opy_ (u"ࠫ࠴࠭✉"))
        try:
            if method == bstack111ll_opy_ (u"ࠬࡍࡅࡕࠩ✊"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack111ll_opy_ (u"࠭ࡐࡐࡕࡗࠫ✋"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack111ll_opy_ (u"ࠧࡑࡗࡗࠫ✌"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack111ll_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ✍").format(method))
            logger.debug(bstack111ll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ✎").format(url, method))
            bstack1ll11lll11l1_opy_ = {}
            try:
                bstack1ll11lll11l1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack111ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ✏").format(e, response.text))
            if bstack1ll11lll11l1_opy_ is not None:
                bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ✐")] = response.headers.get(
                    bstack111ll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭✑"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭✒")] = response.status_code
            return bstack1ll11lll11l1_opy_
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ✓").format(e, url))
            return None
    @staticmethod
    def bstack1lllllll1ll1_opy_(bstack1ll11ll1l11l_opy_, data):
        bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ✔")
        bstack1ll11ll1l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭✕"), bstack111ll_opy_ (u"ࠪࠫ✖"))
        headers = {
            bstack111ll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ✗"): bstack111ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ✘").format(bstack1ll11ll1l1ll_opy_),
            bstack111ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ✙"): bstack111ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ✚")
        }
        response = requests.put(bstack1ll11ll1l11l_opy_, headers=headers, json=data)
        bstack1ll11lll11l1_opy_ = {}
        try:
            bstack1ll11lll11l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ✛").format(e))
            pass
        logger.debug(bstack111ll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ✜").format(bstack1ll11lll11l1_opy_))
        if bstack1ll11lll11l1_opy_ is not None:
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ✝")] = response.headers.get(
                bstack111ll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ✞"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ✟")] = response.status_code
        return bstack1ll11lll11l1_opy_
    @staticmethod
    def bstack1llllllll11l_opy_(bstack1ll11ll1l11l_opy_):
        bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ✠")
        bstack1ll11ll1l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ✡"), bstack111ll_opy_ (u"ࠨࠩ✢"))
        headers = {
            bstack111ll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ✣"): bstack111ll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭✤").format(bstack1ll11ll1l1ll_opy_),
            bstack111ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ✥"): bstack111ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ✦")
        }
        response = requests.get(bstack1ll11ll1l11l_opy_, headers=headers)
        bstack1ll11lll11l1_opy_ = {}
        try:
            bstack1ll11lll11l1_opy_ = response.json()
            logger.debug(bstack111ll_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ✧").format(bstack1ll11lll11l1_opy_))
        except Exception as e:
            logger.debug(bstack111ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ✨").format(e, response.text))
            pass
        if bstack1ll11lll11l1_opy_ is not None:
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ✩")] = response.headers.get(
                bstack111ll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ✪"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11lll11l1_opy_[bstack111ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ✫")] = response.status_code
        return bstack1ll11lll11l1_opy_
    @staticmethod
    def bstack1ll1llll1111_opy_(bstack1111l1111l1_opy_, payload):
        bstack111ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡏࡤ࡯ࡪࡹࠠࡢࠢࡓࡓࡘ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡁࡑࡋࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࠬࡩ࡯ࡣࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡳࡥࡾࡲ࡯ࡢࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡃࡓࡍ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ✬")
        try:
            url = bstack111ll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀࠦ✭").format(bstack11111l1l1l1_opy_, bstack1111l1111l1_opy_)
            bstack1ll11ll1l1ll_opy_ = os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ✮"), bstack111ll_opy_ (u"ࠧࠨ✯"))
            headers = {
                bstack111ll_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ✰"): bstack111ll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ✱").format(bstack1ll11ll1l1ll_opy_),
                bstack111ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ✲"): bstack111ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ✳")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll11ll1llll_opy_ = [200, 202]
            if response.status_code in bstack1ll11ll1llll_opy_:
                return response.json()
            else:
                logger.error(bstack111ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦ࠴ࠠࡔࡶࡤࡸࡺࡹ࠺ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ✴").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡴࡶࡢࡧࡴࡲ࡬ࡦࡥࡷࡣࡧࡻࡩ࡭ࡦࡢࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ✵").format(e))
            return None