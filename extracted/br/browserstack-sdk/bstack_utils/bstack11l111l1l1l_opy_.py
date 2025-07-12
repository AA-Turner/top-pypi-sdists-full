# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack11l11111lll_opy_
logger = logging.getLogger(__name__)
class bstack11l111ll111_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1111111l1ll_opy_ = urljoin(builder, bstack11l1111_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩἙ"))
        if params:
            bstack1111111l1ll_opy_ += bstack11l1111_opy_ (u"ࠥࡃࢀࢃࠢἚ").format(urlencode({bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫἛ"): params.get(bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬἜ"))}))
        return bstack11l111ll111_opy_.bstack111111l111l_opy_(bstack1111111l1ll_opy_)
    @staticmethod
    def bstack11l111lll11_opy_(builder,params=None):
        bstack1111111l1ll_opy_ = urljoin(builder, bstack11l1111_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧἝ"))
        if params:
            bstack1111111l1ll_opy_ += bstack11l1111_opy_ (u"ࠢࡀࡽࢀࠦ἞").format(urlencode({bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ἟"): params.get(bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩἠ"))}))
        return bstack11l111ll111_opy_.bstack111111l111l_opy_(bstack1111111l1ll_opy_)
    @staticmethod
    def bstack111111l111l_opy_(bstack1111111l1l1_opy_):
        bstack1111111lll1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨἡ"), os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨἢ"), bstack11l1111_opy_ (u"ࠬ࠭ἣ")))
        headers = {bstack11l1111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ἤ"): bstack11l1111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪἥ").format(bstack1111111lll1_opy_)}
        response = requests.get(bstack1111111l1l1_opy_, headers=headers)
        bstack1111111ll1l_opy_ = {}
        try:
            bstack1111111ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢἦ").format(e))
            pass
        if bstack1111111ll1l_opy_ is not None:
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪἧ")] = response.headers.get(bstack11l1111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫἨ"), str(int(datetime.now().timestamp() * 1000)))
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫἩ")] = response.status_code
        return bstack1111111ll1l_opy_
    @staticmethod
    def bstack1111111llll_opy_(bstack111111l1111_opy_, data):
        logger.debug(bstack11l1111_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢἪ"))
        return bstack11l111ll111_opy_.bstack111111l11l1_opy_(bstack11l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫἫ"), bstack111111l1111_opy_, data=data)
    @staticmethod
    def bstack1111111ll11_opy_(bstack111111l1111_opy_, data):
        logger.debug(bstack11l1111_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢἬ"))
        res = bstack11l111ll111_opy_.bstack111111l11l1_opy_(bstack11l1111_opy_ (u"ࠨࡉࡈࡘࠬἭ"), bstack111111l1111_opy_, data=data)
        return res
    @staticmethod
    def bstack111111l11l1_opy_(method, bstack111111l1111_opy_, data=None, params=None, extra_headers=None):
        bstack1111111lll1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ἦ"), bstack11l1111_opy_ (u"ࠪࠫἯ"))
        headers = {
            bstack11l1111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫἰ"): bstack11l1111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨἱ").format(bstack1111111lll1_opy_),
            bstack11l1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬἲ"): bstack11l1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪἳ"),
            bstack11l1111_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨἴ"): bstack11l1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬἵ")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack11l11111lll_opy_ + bstack11l1111_opy_ (u"ࠥ࠳ࠧἶ") + bstack111111l1111_opy_.lstrip(bstack11l1111_opy_ (u"ࠫ࠴࠭ἷ"))
        try:
            if method == bstack11l1111_opy_ (u"ࠬࡍࡅࡕࠩἸ"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack11l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫἹ"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack11l1111_opy_ (u"ࠧࡑࡗࡗࠫἺ"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack11l1111_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣἻ").format(method))
            logger.debug(bstack11l1111_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢἼ").format(url, method))
            bstack1111111ll1l_opy_ = {}
            try:
                bstack1111111ll1l_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack11l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢἽ").format(e, response.text))
            if bstack1111111ll1l_opy_ is not None:
                bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬἾ")] = response.headers.get(
                    bstack11l1111_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭Ἷ"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ὀ")] = response.status_code
            return bstack1111111ll1l_opy_
        except Exception as e:
            logger.error(bstack11l1111_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥὁ").format(e, url))
            return None
    @staticmethod
    def bstack111lll11lll_opy_(bstack1111111l1l1_opy_, data):
        bstack11l1111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨὂ")
        bstack1111111lll1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ὃ"), bstack11l1111_opy_ (u"ࠪࠫὄ"))
        headers = {
            bstack11l1111_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫὅ"): bstack11l1111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ὆").format(bstack1111111lll1_opy_),
            bstack11l1111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ὇"): bstack11l1111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪὈ")
        }
        response = requests.put(bstack1111111l1l1_opy_, headers=headers, json=data)
        bstack1111111ll1l_opy_ = {}
        try:
            bstack1111111ll1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢὉ").format(e))
            pass
        logger.debug(bstack11l1111_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦὊ").format(bstack1111111ll1l_opy_))
        if bstack1111111ll1l_opy_ is not None:
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫὋ")] = response.headers.get(
                bstack11l1111_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬὌ"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬὍ")] = response.status_code
        return bstack1111111ll1l_opy_
    @staticmethod
    def bstack111ll1ll1l1_opy_(bstack1111111l1l1_opy_):
        bstack11l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ὎")
        bstack1111111lll1_opy_ = os.environ.get(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ὏"), bstack11l1111_opy_ (u"ࠨࠩὐ"))
        headers = {
            bstack11l1111_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩὑ"): bstack11l1111_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ὒ").format(bstack1111111lll1_opy_),
            bstack11l1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪὓ"): bstack11l1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨὔ")
        }
        response = requests.get(bstack1111111l1l1_opy_, headers=headers)
        bstack1111111ll1l_opy_ = {}
        try:
            bstack1111111ll1l_opy_ = response.json()
            logger.debug(bstack11l1111_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣὕ").format(bstack1111111ll1l_opy_))
        except Exception as e:
            logger.debug(bstack11l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦὖ").format(e, response.text))
            pass
        if bstack1111111ll1l_opy_ is not None:
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩὗ")] = response.headers.get(
                bstack11l1111_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ὘"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1111111ll1l_opy_[bstack11l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪὙ")] = response.status_code
        return bstack1111111ll1l_opy_