# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11111ll1111_opy_
logger = logging.getLogger(__name__)
class bstack1111l111111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll11ll1ll11_opy_ = urljoin(builder, bstack1l1111l_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬ⚡"))
        if params:
            bstack1ll11ll1ll11_opy_ += bstack1l1111l_opy_ (u"ࠨ࠿ࡼࡿࠥ⚢").format(urlencode({bstack1l1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⚣"): params.get(bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⚤"))}))
        return bstack1111l111111_opy_.bstack1ll11lll11l1_opy_(bstack1ll11ll1ll11_opy_)
    @staticmethod
    def bstack1111l1111ll_opy_(builder,params=None):
        bstack1ll11ll1ll11_opy_ = urljoin(builder, bstack1l1111l_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪ⚥"))
        if params:
            bstack1ll11ll1ll11_opy_ += bstack1l1111l_opy_ (u"ࠥࡃࢀࢃࠢ⚦").format(urlencode({bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⚧"): params.get(bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⚨"))}))
        return bstack1111l111111_opy_.bstack1ll11lll11l1_opy_(bstack1ll11ll1ll11_opy_)
    @staticmethod
    def bstack1ll11lll11l1_opy_(bstack1ll11lll1111_opy_):
        bstack1ll11lll1l11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⚩"), os.environ.get(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⚪"), bstack1l1111l_opy_ (u"ࠨࠩ⚫")))
        headers = {bstack1l1111l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⚬"): bstack1l1111l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⚭").format(bstack1ll11lll1l11_opy_)}
        response = requests.get(bstack1ll11lll1111_opy_, headers=headers)
        bstack1ll11ll1ll1l_opy_ = {}
        try:
            bstack1ll11ll1ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⚮").format(e))
            pass
        if bstack1ll11ll1ll1l_opy_ is not None:
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⚯")] = response.headers.get(bstack1l1111l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⚰"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⚱")] = response.status_code
        return bstack1ll11ll1ll1l_opy_
    @staticmethod
    def bstack1ll11ll1lll1_opy_(bstack1ll11lll1l1l_opy_, data):
        logger.debug(bstack1l1111l_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࠥ⚲"))
        return bstack1111l111111_opy_.bstack1ll11lll111l_opy_(bstack1l1111l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⚳"), bstack1ll11lll1l1l_opy_, data=data)
    @staticmethod
    def bstack1ll11lll11ll_opy_(bstack1ll11lll1l1l_opy_, data):
        logger.debug(bstack1l1111l_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥ࡭ࡥࡵࡖࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡵࠥ⚴"))
        res = bstack1111l111111_opy_.bstack1ll11lll111l_opy_(bstack1l1111l_opy_ (u"ࠫࡌࡋࡔࠨ⚵"), bstack1ll11lll1l1l_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll11lll111l_opy_(method, bstack1ll11lll1l1l_opy_, data=None, params=None, extra_headers=None):
        bstack1ll11lll1l11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⚶"), bstack1l1111l_opy_ (u"࠭ࠧ⚷"))
        headers = {
            bstack1l1111l_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⚸"): bstack1l1111l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⚹").format(bstack1ll11lll1l11_opy_),
            bstack1l1111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⚺"): bstack1l1111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⚻"),
            bstack1l1111l_opy_ (u"ࠫࡆࡩࡣࡦࡲࡷࠫ⚼"): bstack1l1111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⚽")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11111ll1111_opy_ + bstack1l1111l_opy_ (u"ࠨ࠯ࠣ⚾") + bstack1ll11lll1l1l_opy_.lstrip(bstack1l1111l_opy_ (u"ࠧ࠰ࠩ⚿"))
        try:
            if method == bstack1l1111l_opy_ (u"ࠨࡉࡈࡘࠬ⛀"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1111l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⛁"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1111l_opy_ (u"ࠪࡔ࡚࡚ࠧ⛂"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1111l_opy_ (u"࡚ࠦࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦ⛃").format(method))
            logger.debug(bstack1l1111l_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡭ࡢࡦࡨࠤࡹࡵࠠࡖࡔࡏ࠾ࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥ⛄").format(url, method))
            bstack1ll11ll1ll1l_opy_ = {}
            try:
                bstack1ll11ll1ll1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⛅").format(e, response.text))
            if bstack1ll11ll1ll1l_opy_ is not None:
                bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⛆")] = response.headers.get(
                    bstack1l1111l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⛇"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⛈")] = response.status_code
            return bstack1ll11ll1ll1l_opy_
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⛉").format(e, url))
            return None
    @staticmethod
    def bstack1llllllll1l1_opy_(bstack1ll11lll1111_opy_, data):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡓ࡙࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⛊")
        bstack1ll11lll1l11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⛋"), bstack1l1111l_opy_ (u"࠭ࠧ⛌"))
        headers = {
            bstack1l1111l_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⛍"): bstack1l1111l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⛎").format(bstack1ll11lll1l11_opy_),
            bstack1l1111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⛏"): bstack1l1111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⛐")
        }
        response = requests.put(bstack1ll11lll1111_opy_, headers=headers, json=data)
        bstack1ll11ll1ll1l_opy_ = {}
        try:
            bstack1ll11ll1ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⛑").format(e))
            pass
        logger.debug(bstack1l1111l_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥࡶࡵࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⛒").format(bstack1ll11ll1ll1l_opy_))
        if bstack1ll11ll1ll1l_opy_ is not None:
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⛓")] = response.headers.get(
                bstack1l1111l_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⛔"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⛕")] = response.status_code
        return bstack1ll11ll1ll1l_opy_
    @staticmethod
    def bstack11111111l11_opy_(bstack1ll11lll1111_opy_):
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡈࡇࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡩࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⛖")
        bstack1ll11lll1l11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⛗"), bstack1l1111l_opy_ (u"ࠫࠬ⛘"))
        headers = {
            bstack1l1111l_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⛙"): bstack1l1111l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⛚").format(bstack1ll11lll1l11_opy_),
            bstack1l1111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⛛"): bstack1l1111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⛜")
        }
        response = requests.get(bstack1ll11lll1111_opy_, headers=headers)
        bstack1ll11ll1ll1l_opy_ = {}
        try:
            bstack1ll11ll1ll1l_opy_ = response.json()
            logger.debug(bstack1l1111l_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡪࡩࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⛝").format(bstack1ll11ll1ll1l_opy_))
        except Exception as e:
            logger.debug(bstack1l1111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⛞").format(e, response.text))
            pass
        if bstack1ll11ll1ll1l_opy_ is not None:
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⛟")] = response.headers.get(
                bstack1l1111l_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⛠"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll11ll1ll1l_opy_[bstack1l1111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⛡")] = response.status_code
        return bstack1ll11ll1ll1l_opy_
    @staticmethod
    def bstack1lll1111llll_opy_(bstack1111l111ll1_opy_, payload):
        bstack1l1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡧ࡫ࡦࡵࠣࡥࠥࡖࡏࡔࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥ࠮ࡳࡵࡴࠬ࠾࡚ࠥࡨࡦࠢࡄࡔࡎࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡶࡡࡺ࡮ࡲࡥࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡆࡖࡉ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⛢")
        try:
            url = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠳ࢀࢃࠢ⛣").format(bstack11111ll1111_opy_, bstack1111l111ll1_opy_)
            bstack1ll11lll1l11_opy_ = os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⛤"), bstack1l1111l_opy_ (u"ࠪࠫ⛥"))
            headers = {
                bstack1l1111l_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⛦"): bstack1l1111l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⛧").format(bstack1ll11lll1l11_opy_),
                bstack1l1111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⛨"): bstack1l1111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⛩")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll11ll1llll_opy_ = [200, 202]
            if response.status_code in bstack1ll11ll1llll_opy_:
                return response.json()
            else:
                logger.error(bstack1l1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢ࠰ࠣࡗࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⛪").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡷࡹࡥࡣࡰ࡮࡯ࡩࡨࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ⛫").format(e))
            return None