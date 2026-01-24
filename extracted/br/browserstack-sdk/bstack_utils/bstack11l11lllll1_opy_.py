# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l11111lll_opy_
logger = logging.getLogger(__name__)
class bstack11l11lll11l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1lll1llll1ll_opy_ = urljoin(builder, bstack1l1111_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩℭ"))
        if params:
            bstack1lll1llll1ll_opy_ += bstack1l1111_opy_ (u"ࠥࡃࢀࢃࠢ℮").format(urlencode({bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫℯ"): params.get(bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬℰ"))}))
        return bstack11l11lll11l_opy_.bstack1lll1llll11l_opy_(bstack1lll1llll1ll_opy_)
    @staticmethod
    def bstack11l11llll1l_opy_(builder,params=None):
        bstack1lll1llll1ll_opy_ = urljoin(builder, bstack1l1111_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧℱ"))
        if params:
            bstack1lll1llll1ll_opy_ += bstack1l1111_opy_ (u"ࠢࡀࡽࢀࠦℲ").format(urlencode({bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨℳ"): params.get(bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩℴ"))}))
        return bstack11l11lll11l_opy_.bstack1lll1llll11l_opy_(bstack1lll1llll1ll_opy_)
    @staticmethod
    def bstack1lll1llll11l_opy_(bstack1lll1lllll11_opy_):
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨℵ"), os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨℶ"), bstack1l1111_opy_ (u"ࠬ࠭ℷ")))
        headers = {bstack1l1111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ℸ"): bstack1l1111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪℹ").format(bstack1lll1llll1l1_opy_)}
        response = requests.get(bstack1lll1lllll11_opy_, headers=headers)
        bstack1lll1lll1ll1_opy_ = {}
        try:
            bstack1lll1lll1ll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ℺").format(e))
            pass
        if bstack1lll1lll1ll1_opy_ is not None:
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ℻")] = response.headers.get(bstack1l1111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫℼ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫℽ")] = response.status_code
        return bstack1lll1lll1ll1_opy_
    @staticmethod
    def bstack1lll1llll111_opy_(bstack1lll1lllll1l_opy_, data):
        logger.debug(bstack1l1111_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢℾ"))
        return bstack11l11lll11l_opy_.bstack1lll1lll1lll_opy_(bstack1l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫℿ"), bstack1lll1lllll1l_opy_, data=data)
    @staticmethod
    def bstack1lll1lll1l11_opy_(bstack1lll1lllll1l_opy_, data):
        logger.debug(bstack1l1111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢ⅀"))
        res = bstack11l11lll11l_opy_.bstack1lll1lll1lll_opy_(bstack1l1111_opy_ (u"ࠨࡉࡈࡘࠬ⅁"), bstack1lll1lllll1l_opy_, data=data)
        return res
    @staticmethod
    def bstack1lll1lll1lll_opy_(method, bstack1lll1lllll1l_opy_, data=None, params=None, extra_headers=None):
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⅂"), bstack1l1111_opy_ (u"ࠪࠫ⅃"))
        headers = {
            bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⅄"): bstack1l1111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨⅅ").format(bstack1lll1llll1l1_opy_),
            bstack1l1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬⅆ"): bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪⅇ"),
            bstack1l1111_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨⅈ"): bstack1l1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬⅉ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l11111lll_opy_ + bstack1l1111_opy_ (u"ࠥ࠳ࠧ⅊") + bstack1lll1lllll1l_opy_.lstrip(bstack1l1111_opy_ (u"ࠫ࠴࠭⅋"))
        try:
            if method == bstack1l1111_opy_ (u"ࠬࡍࡅࡕࠩ⅌"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫ⅍"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1l1111_opy_ (u"ࠧࡑࡗࡗࠫⅎ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1l1111_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ⅏").format(method))
            logger.debug(bstack1l1111_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⅐").format(url, method))
            bstack1lll1lll1ll1_opy_ = {}
            try:
                bstack1lll1lll1ll1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⅑").format(e, response.text))
            if bstack1lll1lll1ll1_opy_ is not None:
                bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⅒")] = response.headers.get(
                    bstack1l1111_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⅓"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⅔")] = response.status_code
            return bstack1lll1lll1ll1_opy_
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⅕").format(e, url))
            return None
    @staticmethod
    def bstack111llllll1l_opy_(bstack1lll1lllll11_opy_, data):
        bstack1l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⅖")
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⅗"), bstack1l1111_opy_ (u"ࠪࠫ⅘"))
        headers = {
            bstack1l1111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⅙"): bstack1l1111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⅚").format(bstack1lll1llll1l1_opy_),
            bstack1l1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⅛"): bstack1l1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⅜")
        }
        response = requests.put(bstack1lll1lllll11_opy_, headers=headers, json=data)
        bstack1lll1lll1ll1_opy_ = {}
        try:
            bstack1lll1lll1ll1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⅝").format(e))
            pass
        logger.debug(bstack1l1111_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⅞").format(bstack1lll1lll1ll1_opy_))
        if bstack1lll1lll1ll1_opy_ is not None:
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⅟")] = response.headers.get(
                bstack1l1111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬⅠ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⅡ")] = response.status_code
        return bstack1lll1lll1ll1_opy_
    @staticmethod
    def bstack11l111111ll_opy_(bstack1lll1lllll11_opy_):
        bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦⅢ")
        bstack1lll1llll1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫⅣ"), bstack1l1111_opy_ (u"ࠨࠩⅤ"))
        headers = {
            bstack1l1111_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩⅥ"): bstack1l1111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭Ⅶ").format(bstack1lll1llll1l1_opy_),
            bstack1l1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪⅧ"): bstack1l1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨⅨ")
        }
        response = requests.get(bstack1lll1lllll11_opy_, headers=headers)
        bstack1lll1lll1ll1_opy_ = {}
        try:
            bstack1lll1lll1ll1_opy_ = response.json()
            logger.debug(bstack1l1111_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣⅩ").format(bstack1lll1lll1ll1_opy_))
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦⅪ").format(e, response.text))
            pass
        if bstack1lll1lll1ll1_opy_ is not None:
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩⅫ")] = response.headers.get(
                bstack1l1111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪⅬ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1lll1lll1ll1_opy_[bstack1l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪⅭ")] = response.status_code
        return bstack1lll1lll1ll1_opy_
    @staticmethod
    def bstack11111111111_opy_(bstack11l1l11111l_opy_, payload):
        bstack1l1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡏࡤ࡯ࡪࡹࠠࡢࠢࡓࡓࡘ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡁࡑࡋࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࠬࡩ࡯ࡣࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡳࡥࡾࡲ࡯ࡢࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡃࡓࡍ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣⅮ")
        try:
            url = bstack1l1111_opy_ (u"ࠧࢁࡽ࠰ࡽࢀࠦⅯ").format(bstack11l11111lll_opy_, bstack11l1l11111l_opy_)
            bstack1lll1llll1l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪⅰ"), bstack1l1111_opy_ (u"ࠧࠨⅱ"))
            headers = {
                bstack1l1111_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨⅲ"): bstack1l1111_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬⅳ").format(bstack1lll1llll1l1_opy_),
                bstack1l1111_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩⅴ"): bstack1l1111_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧⅵ")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1lll1lll1l1l_opy_ = [200, 202]
            if response.status_code in bstack1lll1lll1l1l_opy_:
                return response.json()
            else:
                logger.error(bstack1l1111_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦ࠴ࠠࡔࡶࡤࡸࡺࡹ࠺ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦⅶ").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡴࡶࡢࡧࡴࡲ࡬ࡦࡥࡷࡣࡧࡻࡩ࡭ࡦࡢࡨࡦࡺࡡ࠻ࠢࡾࢁࠧⅷ").format(e))
            return None