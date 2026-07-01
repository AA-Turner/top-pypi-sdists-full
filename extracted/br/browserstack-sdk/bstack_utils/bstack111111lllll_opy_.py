# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack1111111l1ll_opy_
from bstack_utils.helper import get_ca_cert_path
logger = logging.getLogger(__name__)
def _1ll111l11111_opy_():
    bstack1l1llll_opy_ (u"࡙ࠥࠦࠧࡄࡌ࠯࠸࠼࠶࠼࠺ࠡࡲࡵࡳࡽࡿࡃࡢࡅࡨࡶࡹ࡯ࡦࡪࡥࡤࡸࡪࠦ࡫ࡸࡣࡵ࡫ࡸࠦࡦࡰࡴࠣࡳࡺࡺࡢࡰࡷࡱࡨࠥࡸࡥࡲࡷࡨࡷࡹࡹ࠮ࠋࠢࠣࠤࠥࡘࡥࡢࡦࡶࠤࡥࡶࡲࡰࡺࡼࡇࡦࡉࡥࡳࡶ࡬ࡪ࡮ࡩࡡࡵࡧࡣࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡓࡅࡍࠣࡇࡔࡔࡆࡊࡉࠣࠬࡵࡧࡲࡴࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠫ࠱ࠤࡑࡧࡺࡺ࠯࡬ࡱࡵࡵࡲࡵࡵࠣࡇࡔࡔࡆࡊࡉࠣࡸࡴࠦࡡࡷࡱ࡬ࡨࠥࡺࡨࡦࠢࡦ࡭ࡷࡩࡵ࡭ࡣࡵࠤ࡮ࡳࡰࡰࡴࡷࠎࠥࠦࠠࠡࡣࡷࠤࡲࡵࡤࡶ࡮ࡨࠤࡱࡵࡡࡥࠢࡷ࡭ࡲ࡫ࠠࠩࡴࡨࡵࡺ࡫ࡳࡵࡡࡸࡸ࡮ࡲࡳࠡ࡫ࡶࠤ࡮ࡳࡰࡰࡴࡷࡩࡩࠦࡢࡺࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠏࠦࠠࠡࠢ࡬ࡲ࡮ࡺࠠࡣࡧࡩࡳࡷ࡫ࠠࡄࡑࡑࡊࡎࡍࠠࡪࡵࠣࡴࡴࡶࡵ࡭ࡣࡷࡩࡩ࠯࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⨦")
    cert_path = get_ca_cert_path(None)
    return {bstack1l1llll_opy_ (u"ࠫࡻ࡫ࡲࡪࡨࡼࠫ⨧"): cert_path} if cert_path else {}
class bstack11111l111ll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll111l111ll_opy_ = urljoin(builder, bstack1l1llll_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷࠬ⨨"))
        if params:
            bstack1ll111l111ll_opy_ += bstack1l1llll_opy_ (u"ࠨ࠿ࡼࡿࠥ⨩").format(urlencode({bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⨪"): params.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⨫"))}))
        return bstack11111l111ll_opy_.bstack1ll1111lll1l_opy_(bstack1ll111l111ll_opy_)
    @staticmethod
    def bstack111111llll1_opy_(builder,params=None):
        bstack1ll111l111ll_opy_ = urljoin(builder, bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴ࠯ࡶࡹࡲࡳࡡࡳࡻࠪ⨬"))
        if params:
            bstack1ll111l111ll_opy_ += bstack1l1llll_opy_ (u"ࠥࡃࢀࢃࠢ⨭").format(urlencode({bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⨮"): params.get(bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⨯"))}))
        return bstack11111l111ll_opy_.bstack1ll1111lll1l_opy_(bstack1ll111l111ll_opy_)
    @staticmethod
    def bstack1ll1111lll1l_opy_(bstack1ll111l1111l_opy_):
        bstack1ll111l11ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⨰"), os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⨱"), bstack1l1llll_opy_ (u"ࠨࠩ⨲")))
        headers = {bstack1l1llll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⨳"): bstack1l1llll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⨴").format(bstack1ll111l11ll1_opy_)}
        response = requests.get(bstack1ll111l1111l_opy_, headers=headers, **_1ll111l11111_opy_())
        bstack1ll1111lllll_opy_ = {}
        try:
            bstack1ll1111lllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⨵").format(e))
            pass
        if bstack1ll1111lllll_opy_ is not None:
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⨶")] = response.headers.get(bstack1l1llll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⨷"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⨸")] = response.status_code
        return bstack1ll1111lllll_opy_
    @staticmethod
    def bstack1ll1111llll1_opy_(bstack1ll111l11l11_opy_, data):
        logger.debug(bstack1l1llll_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡦࡰࡴࠣࡸࡪࡹࡴࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࡓࡱ࡮࡬ࡸ࡙࡫ࡳࡵࡵࠥ⨹"))
        return bstack11111l111ll_opy_.bstack1ll1111ll1ll_opy_(bstack1l1llll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⨺"), bstack1ll111l11l11_opy_, data=data)
    @staticmethod
    def bstack1ll111l111l1_opy_(bstack1ll111l11l11_opy_, data):
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡓࡧࡴࡹࡪࡹࡴࠡࡨࡲࡶࠥ࡭ࡥࡵࡖࡨࡷࡹࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࡔࡸࡤࡦࡴࡨࡨ࡙࡫ࡳࡵࡵࠥ⨻"))
        res = bstack11111l111ll_opy_.bstack1ll1111ll1ll_opy_(bstack1l1llll_opy_ (u"ࠫࡌࡋࡔࠨ⨼"), bstack1ll111l11l11_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1111ll1ll_opy_(method, bstack1ll111l11l11_opy_, data=None, params=None, extra_headers=None):
        bstack1ll111l11ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⨽"), bstack1l1llll_opy_ (u"࠭ࠧ⨾"))
        headers = {
            bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⨿"): bstack1l1llll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⩀").format(bstack1ll111l11ll1_opy_),
            bstack1l1llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⩁"): bstack1l1llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⩂"),
            bstack1l1llll_opy_ (u"ࠫࡆࡩࡣࡦࡲࡷࠫ⩃"): bstack1l1llll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⩄")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack1111111l1ll_opy_ + bstack1l1llll_opy_ (u"ࠨ࠯ࠣ⩅") + bstack1ll111l11l11_opy_.lstrip(bstack1l1llll_opy_ (u"ࠧ࠰ࠩ⩆"))
        try:
            bstack1ll1111lll11_opy_ = _1ll111l11111_opy_()
            if method == bstack1l1llll_opy_ (u"ࠨࡉࡈࡘࠬ⩇"):
                response = requests.get(url, headers=headers, params=params, json=data, **bstack1ll1111lll11_opy_)
            elif method == bstack1l1llll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⩈"):
                response = requests.post(url, headers=headers, json=data, **bstack1ll1111lll11_opy_)
            elif method == bstack1l1llll_opy_ (u"ࠪࡔ࡚࡚ࠧ⩉"):
                response = requests.put(url, headers=headers, json=data, **bstack1ll1111lll11_opy_)
            else:
                raise ValueError(bstack1l1llll_opy_ (u"࡚ࠦࡴࡳࡶࡲࡳࡳࡷࡺࡥࡥࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪ࠺ࠡࡽࢀࠦ⩊").format(method))
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡕࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡭ࡢࡦࡨࠤࡹࡵࠠࡖࡔࡏ࠾ࠥࢁࡽࠡࡹ࡬ࡸ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࡼࡿࠥ⩋").format(url, method))
            bstack1ll1111lllll_opy_ = {}
            try:
                bstack1ll1111lllll_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1llll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡌࡖࡓࡓࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⩌").format(e, response.text))
            if bstack1ll1111lllll_opy_ is not None:
                bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⩍")] = response.headers.get(
                    bstack1l1llll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⩎"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⩏")] = response.status_code
            return bstack1ll1111lllll_opy_
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠥࡓࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ⩐").format(e, url))
            return None
    @staticmethod
    def bstack1llllll11ll1_opy_(bstack1ll111l1111l_opy_, data):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡨࡲࡩࡹࠠࡢࠢࡓ࡙࡙ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡷ࡬ࡪࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ⩑")
        bstack1ll111l11ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⩒"), bstack1l1llll_opy_ (u"࠭ࠧ⩓"))
        headers = {
            bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ⩔"): bstack1l1llll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ⩕").format(bstack1ll111l11ll1_opy_),
            bstack1l1llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⩖"): bstack1l1llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⩗")
        }
        response = requests.put(bstack1ll111l1111l_opy_, headers=headers, json=data, **_1ll111l11111_opy_())
        bstack1ll1111lllll_opy_ = {}
        try:
            bstack1ll1111lllll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡊࡔࡑࡑࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡼࡿࠥ⩘").format(e))
            pass
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹ࡛ࡴࡪ࡮ࡶ࠾ࠥࡶࡵࡵࡡࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⩙").format(bstack1ll1111lllll_opy_))
        if bstack1ll1111lllll_opy_ is not None:
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"࠭࡮ࡦࡺࡷࡣࡵࡵ࡬࡭ࡡࡷ࡭ࡲ࡫ࠧ⩚")] = response.headers.get(
                bstack1l1llll_opy_ (u"ࠧ࡯ࡧࡻࡸࡤࡶ࡯࡭࡮ࡢࡸ࡮ࡳࡥࠨ⩛"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⩜")] = response.status_code
        return bstack1ll1111lllll_opy_
    @staticmethod
    def bstack1lllll1ll1l1_opy_(bstack1ll111l1111l_opy_):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡦࡰࡧࡷࠥࡧࠠࡈࡇࡗࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡩࡨࡸࠥࡺࡨࡦࠢࡦࡳࡺࡴࡴࠡࡱࡩࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢ⩝")
        bstack1ll111l11ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⩞"), bstack1l1llll_opy_ (u"ࠫࠬ⩟"))
        headers = {
            bstack1l1llll_opy_ (u"ࠬࡧࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⩠"): bstack1l1llll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⩡").format(bstack1ll111l11ll1_opy_),
            bstack1l1llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⩢"): bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⩣")
        }
        response = requests.get(bstack1ll111l1111l_opy_, headers=headers, **_1ll111l11111_opy_())
        bstack1ll1111lllll_opy_ = {}
        try:
            bstack1ll1111lllll_opy_ = response.json()
            logger.debug(bstack1l1llll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡪࡩࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⩤").format(bstack1ll1111lllll_opy_))
        except Exception as e:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⩥").format(e, response.text))
            pass
        if bstack1ll1111lllll_opy_ is not None:
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⩦")] = response.headers.get(
                bstack1l1llll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⩧"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1111lllll_opy_[bstack1l1llll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⩨")] = response.status_code
        return bstack1ll1111lllll_opy_
    @staticmethod
    def bstack1ll1ll1l11l1_opy_(bstack11111l11lll_opy_, payload):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒࡧ࡫ࡦࡵࠣࡥࠥࡖࡏࡔࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡵࡪࡨࠤࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡨࡵࡪ࡮ࡧ࠱ࡩࡧࡴࡢࠢࡨࡲࡩࡶ࡯ࡪࡰࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥ࠮ࡳࡵࡴࠬ࠾࡚ࠥࡨࡦࠢࡄࡔࡎࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࠨࡥ࡫ࡦࡸ࠮ࡀࠠࡕࡪࡨࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡶࡡࡺ࡮ࡲࡥࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡆࡖࡉ࠭ࠢࡲࡶࠥࡔ࡯࡯ࡧࠣ࡭࡫ࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⩩")
        try:
            url = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠳ࢀࢃࠢ⩪").format(bstack1111111l1ll_opy_, bstack11111l11lll_opy_)
            bstack1ll111l11ll1_opy_ = os.environ.get(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⩫"), bstack1l1llll_opy_ (u"ࠪࠫ⩬"))
            headers = {
                bstack1l1llll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⩭"): bstack1l1llll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⩮").format(bstack1ll111l11ll1_opy_),
                bstack1l1llll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⩯"): bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⩰")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30, **_1ll111l11111_opy_())
            bstack1ll111l11l1l_opy_ = [200, 202]
            if response.status_code in bstack1ll111l11l1l_opy_:
                return response.json()
            else:
                logger.error(bstack1l1llll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡨࡵ࡬࡭ࡧࡦࡸࠥࡨࡵࡪ࡮ࡧࠤࡩࡧࡴࡢ࠰ࠣࡗࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⩱").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡷࡹࡥࡣࡰ࡮࡯ࡩࡨࡺ࡟ࡣࡷ࡬ࡰࡩࡥࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ⩲").format(e))
            return None