# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
from bstack_utils.constants import bstack111l11ll11l_opy_
logger = logging.getLogger(__name__)
class bstack111l1llll11_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack1ll1llll1lll_opy_ = urljoin(builder, bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩ①"))
        if params:
            bstack1ll1llll1lll_opy_ += bstack1ll1lll_opy_ (u"ࠥࡃࢀࢃࠢ②").format(urlencode({bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ③"): params.get(bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ④"))}))
        return bstack111l1llll11_opy_.bstack1ll1llll1ll1_opy_(bstack1ll1llll1lll_opy_)
    @staticmethod
    def bstack111l1lllll1_opy_(builder,params=None):
        bstack1ll1llll1lll_opy_ = urljoin(builder, bstack1ll1lll_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧ⑤"))
        if params:
            bstack1ll1llll1lll_opy_ += bstack1ll1lll_opy_ (u"ࠢࡀࡽࢀࠦ⑥").format(urlencode({bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⑦"): params.get(bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⑧"))}))
        return bstack111l1llll11_opy_.bstack1ll1llll1ll1_opy_(bstack1ll1llll1lll_opy_)
    @staticmethod
    def bstack1ll1llll1ll1_opy_(bstack1ll1lllll111_opy_):
        bstack1ll1llll11ll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⑨"), os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⑩"), bstack1ll1lll_opy_ (u"ࠬ࠭⑪")))
        headers = {bstack1ll1lll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⑫"): bstack1ll1lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⑬").format(bstack1ll1llll11ll_opy_)}
        response = requests.get(bstack1ll1lllll111_opy_, headers=headers)
        bstack1ll1lllll1l1_opy_ = {}
        try:
            bstack1ll1lllll1l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⑭").format(e))
            pass
        if bstack1ll1lllll1l1_opy_ is not None:
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⑮")] = response.headers.get(bstack1ll1lll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⑯"), str(int(datetime.now().timestamp() * 1000)))
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⑰")] = response.status_code
        return bstack1ll1lllll1l1_opy_
    @staticmethod
    def bstack1ll1llllll11_opy_(bstack1ll1llll1l1l_opy_, data):
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡕࡩࡶࡻࡥࡴࡶࠣࡪࡴࡸࠠࡵࡧࡶࡸࡔࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࡗࡵࡲࡩࡵࡖࡨࡷࡹࡹࠢ⑱"))
        return bstack111l1llll11_opy_.bstack1ll1lllll11l_opy_(bstack1ll1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫ⑲"), bstack1ll1llll1l1l_opy_, data=data)
    @staticmethod
    def bstack1ll1lllll1ll_opy_(bstack1ll1llll1l1l_opy_, data):
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡬࡯ࡳࠢࡪࡩࡹ࡚ࡥࡴࡶࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࡑࡵࡨࡪࡸࡥࡥࡖࡨࡷࡹࡹࠢ⑳"))
        res = bstack111l1llll11_opy_.bstack1ll1lllll11l_opy_(bstack1ll1lll_opy_ (u"ࠨࡉࡈࡘࠬ⑴"), bstack1ll1llll1l1l_opy_, data=data)
        return res
    @staticmethod
    def bstack1ll1lllll11l_opy_(method, bstack1ll1llll1l1l_opy_, data=None, params=None, extra_headers=None):
        bstack1ll1llll11ll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⑵"), bstack1ll1lll_opy_ (u"ࠪࠫ⑶"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⑷"): bstack1ll1lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⑸").format(bstack1ll1llll11ll_opy_),
            bstack1ll1lll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⑹"): bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⑺"),
            bstack1ll1lll_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨ⑻"): bstack1ll1lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⑼")
        }
        if extra_headers:
            headers.update(extra_headers)
        url = bstack111l11ll11l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠳ࠧ⑽") + bstack1ll1llll1l1l_opy_.lstrip(bstack1ll1lll_opy_ (u"ࠫ࠴࠭⑾"))
        try:
            if method == bstack1ll1lll_opy_ (u"ࠬࡍࡅࡕࠩ⑿"):
                response = requests.get(url, headers=headers, params=params, json=data)
            elif method == bstack1ll1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫ⒀"):
                response = requests.post(url, headers=headers, json=data)
            elif method == bstack1ll1lll_opy_ (u"ࠧࡑࡗࡗࠫ⒁"):
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(bstack1ll1lll_opy_ (u"ࠣࡗࡱࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡈࡕࡖࡓࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࢁࡽࠣ⒂").format(method))
            logger.debug(bstack1ll1lll_opy_ (u"ࠤࡒࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶࠣࡱࡦࡪࡥࠡࡶࡲࠤ࡚ࡘࡌ࠻ࠢࡾࢁࠥࡽࡩࡵࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࢀࢃࠢ⒃").format(url, method))
            bstack1ll1lllll1l1_opy_ = {}
            try:
                bstack1ll1lllll1l1_opy_ = response.json()
            except Exception as e:
                logger.debug(bstack1ll1lll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡐࡓࡐࡐࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢ⒄").format(e, response.text))
            if bstack1ll1lllll1l1_opy_ is not None:
                bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⒅")] = response.headers.get(
                    bstack1ll1lll_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡴࡲ࡬ࡠࡶ࡬ࡱࡪ࠭⒆"), str(int(datetime.now().timestamp() * 1000))
                )
                bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⒇")] = response.status_code
            return bstack1ll1lllll1l1_opy_
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠢࡐࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡳࡧࡴࡹࡪࡹࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥ⒈").format(e, url))
            return None
    @staticmethod
    def bstack1111lll1l1l_opy_(bstack1ll1lllll111_opy_, data):
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡥ࡯ࡦࡶࠤࡦࠦࡐࡖࡖࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡴࡩࡧࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ⒉")
        bstack1ll1llll11ll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⒊"), bstack1ll1lll_opy_ (u"ࠪࠫ⒋"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ⒌"): bstack1ll1lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ⒍").format(bstack1ll1llll11ll_opy_),
            bstack1ll1lll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ⒎"): bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ⒏")
        }
        response = requests.put(bstack1ll1lllll111_opy_, headers=headers, json=data)
        bstack1ll1lllll1l1_opy_ = {}
        try:
            bstack1ll1lllll1l1_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢ⒐").format(e))
            pass
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡕࡩࡶࡻࡥࡴࡶࡘࡸ࡮ࡲࡳ࠻ࠢࡳࡹࡹࡥࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࠥࡸࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⒑").format(bstack1ll1lllll1l1_opy_))
        if bstack1ll1lllll1l1_opy_ is not None:
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫ⒒")] = response.headers.get(
                bstack1ll1lll_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬ⒓"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⒔")] = response.status_code
        return bstack1ll1lllll1l1_opy_
    @staticmethod
    def bstack1111lll11ll_opy_(bstack1ll1lllll111_opy_):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡪࡴࡤࡴࠢࡤࠤࡌࡋࡔࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳࠥ࡭ࡥࡵࠢࡷ࡬ࡪࠦࡣࡰࡷࡱࡸࠥࡵࡦࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ⒕")
        bstack1ll1llll11ll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⒖"), bstack1ll1lll_opy_ (u"ࠨࠩ⒗"))
        headers = {
            bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⒘"): bstack1ll1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⒙").format(bstack1ll1llll11ll_opy_),
            bstack1ll1lll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⒚"): bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⒛")
        }
        response = requests.get(bstack1ll1lllll111_opy_, headers=headers)
        bstack1ll1lllll1l1_opy_ = {}
        try:
            bstack1ll1lllll1l1_opy_ = response.json()
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡦࡳࡸࡩࡸࡺࡕࡵ࡫࡯ࡷ࠿ࠦࡧࡦࡶࡢࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ࠾ࠥࢁࡽࠣ⒜").format(bstack1ll1lllll1l1_opy_))
        except Exception as e:
            logger.debug(bstack1ll1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ⒝").format(e, response.text))
            pass
        if bstack1ll1lllll1l1_opy_ is not None:
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩ⒞")] = response.headers.get(
                bstack1ll1lll_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪ⒟"), str(int(datetime.now().timestamp() * 1000))
            )
            bstack1ll1lllll1l1_opy_[bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⒠")] = response.status_code
        return bstack1ll1lllll1l1_opy_
    @staticmethod
    def bstack1lll1llllll1_opy_(bstack111ll1111l1_opy_, payload):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡏࡤ࡯ࡪࡹࠠࡢࠢࡓࡓࡘ࡚ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤࡹ࡮ࡥࠡࡥࡲࡰࡱ࡫ࡣࡵ࠯ࡥࡹ࡮ࡲࡤ࠮ࡦࡤࡸࡦࠦࡥ࡯ࡦࡳࡳ࡮ࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡰࡧࡴࡴ࡯࡮ࡵࠢࠫࡷࡹࡸࠩ࠻ࠢࡗ࡬ࡪࠦࡁࡑࡋࠣࡩࡳࡪࡰࡰ࡫ࡱࡸࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࠬࡩ࡯ࡣࡵࠫ࠽ࠤ࡙࡮ࡥࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡳࡥࡾࡲ࡯ࡢࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡃࡓࡍ࠱ࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠠࡪࡨࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ⒡")
        try:
            url = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀࠦ⒢").format(bstack111l11ll11l_opy_, bstack111ll1111l1_opy_)
            bstack1ll1llll11ll_opy_ = os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⒣"), bstack1ll1lll_opy_ (u"ࠧࠨ⒤"))
            headers = {
                bstack1ll1lll_opy_ (u"ࠨࡣࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ⒥"): bstack1ll1lll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ⒦").format(bstack1ll1llll11ll_opy_),
                bstack1ll1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ⒧"): bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ⒨")
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            bstack1ll1llll1l11_opy_ = [200, 202]
            if response.status_code in bstack1ll1llll1l11_opy_:
                return response.json()
            else:
                logger.error(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡥࡹ࡮ࡲࡤࠡࡦࡤࡸࡦ࠴ࠠࡔࡶࡤࡸࡺࡹ࠺ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫࠺ࠡࡽࢀࠦ⒩").format(
                    response.status_code, response.text))
                return None
        except Exception as e:
            logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡴࡶࡢࡧࡴࡲ࡬ࡦࡥࡷࡣࡧࡻࡩ࡭ࡦࡢࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ⒪").format(e))
            return None