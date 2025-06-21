# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1lll11l_opy_, bstack11ll1l1llll_opy_, bstack1l1llll1ll_opy_, bstack111ll11111_opy_, bstack11l11lll1ll_opy_, bstack111llll1lll_opy_, bstack11l1l11l1ll_opy_, bstack1lllll1l1l_opy_, bstack111l1ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11111l11111_opy_ import bstack111111lllll_opy_
import bstack_utils.bstack1l11111111_opy_ as bstack1l1l11111_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack11l1l1l1ll_opy_
import bstack_utils.accessibility as bstack1ll1l11ll_opy_
from bstack_utils.bstack1111ll1l1_opy_ import bstack1111ll1l1_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack111l11l111_opy_
bstack1llllll11111_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧᾪ")
logger = logging.getLogger(__name__)
class bstack111llllll_opy_:
    bstack11111l11111_opy_ = None
    bs_config = None
    bstack11l1111l11_opy_ = None
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1llll11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def launch(cls, bs_config, bstack11l1111l11_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1111l11_opy_ = bstack11l1111l11_opy_
        try:
            cls.bstack1llllll1ll1l_opy_()
            bstack11ll1l1lll1_opy_ = bstack11ll1lll11l_opy_(bs_config)
            bstack11ll1llllll_opy_ = bstack11ll1l1llll_opy_(bs_config)
            data = bstack1l1l11111_opy_.bstack1lllll1llll1_opy_(bs_config, bstack11l1111l11_opy_)
            config = {
                bstack1l1l1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᾫ"): (bstack11ll1l1lll1_opy_, bstack11ll1llllll_opy_),
                bstack1l1l1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᾬ"): cls.default_headers()
            }
            response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨᾭ"), cls.request_url(bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫᾮ")), data, config)
            if response.status_code != 200:
                bstack11l1l111ll_opy_ = response.json()
                if bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᾯ")] == False:
                    cls.bstack1lllll1ll111_opy_(bstack11l1l111ll_opy_)
                    return
                cls.bstack1llllll11ll1_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᾰ")])
                cls.bstack1llllll1l11l_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᾱ")])
                return None
            bstack1lllll1l1lll_opy_ = cls.bstack1llllll1l111_opy_(response)
            return bstack1lllll1l1lll_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨᾲ").format(str(error)))
            return None
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def stop(cls, bstack1llllll11lll_opy_=None):
        if not bstack11l1l1l1ll_opy_.on() and not bstack1ll1l11ll_opy_.on():
            return
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᾳ")) == bstack1l1l1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᾴ") or os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᾵")) == bstack1l1l1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᾶ"):
            logger.error(bstack1l1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᾷ"))
            return {
                bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᾸ"): bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᾹ"),
                bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾺ"): bstack1l1l1l1_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨΆ")
            }
        try:
            cls.bstack11111l11111_opy_.shutdown()
            data = {
                bstack1l1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᾼ"): bstack1lllll1l1l_opy_()
            }
            if not bstack1llllll11lll_opy_ is None:
                data[bstack1l1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ᾽")] = [{
                    bstack1l1l1l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ι"): bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ᾿"),
                    bstack1l1l1l1_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ῀"): bstack1llllll11lll_opy_
                }]
            config = {
                bstack1l1l1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ῁"): cls.default_headers()
            }
            bstack11ll1l11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫῂ").format(os.environ[bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤῃ")])
            bstack1lllll1l1l11_opy_ = cls.request_url(bstack11ll1l11l11_opy_)
            response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠬࡖࡕࡕࠩῄ"), bstack1lllll1l1l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l1l1_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ῅"))
        except Exception as error:
            logger.error(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦῆ") + str(error))
            return {
                bstack1l1l1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨῇ"): bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨῈ"),
                bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫΈ"): str(error)
            }
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def bstack1llllll1l111_opy_(cls, response):
        bstack11l1l111ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll1l1lll_opy_ = {}
        if bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡯ࡽࡴࠨῊ")) is None:
            os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩΉ")] = bstack1l1l1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫῌ")
        else:
            os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ῍")] = bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡺࡸࠬ῎"), bstack1l1l1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ῏"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨῐ")] = bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ῑ"), bstack1l1l1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪῒ"))
        logger.info(bstack1l1l1l1_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫΐ") + os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ῔")));
        if bstack11l1l1l1ll_opy_.bstack1llllll1l1l1_opy_(cls.bs_config, cls.bstack11l1111l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ῕"), bstack1l1l1l1_opy_ (u"ࠩࠪῖ"))) is True:
            bstack111111l1ll1_opy_, build_hashed_id, bstack1llllll111l1_opy_ = cls.bstack1llllll111ll_opy_(bstack11l1l111ll_opy_)
            if bstack111111l1ll1_opy_ != None and build_hashed_id != None:
                bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪῗ")] = {
                    bstack1l1l1l1_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧῘ"): bstack111111l1ll1_opy_,
                    bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧῙ"): build_hashed_id,
                    bstack1l1l1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪῚ"): bstack1llllll111l1_opy_
                }
            else:
                bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧΊ")] = {}
        else:
            bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ῜")] = {}
        bstack1lllll1lllll_opy_, build_hashed_id = cls.bstack1llllll1ll11_opy_(bstack11l1l111ll_opy_)
        if bstack1lllll1lllll_opy_ != None and build_hashed_id != None:
            bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ῝")] = {
                bstack1l1l1l1_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧ῞"): bstack1lllll1lllll_opy_,
                bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭῟"): build_hashed_id,
            }
        else:
            bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬῠ")] = {}
        if bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ῡ")].get(bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩῢ")) != None or bstack1lllll1l1lll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨΰ")].get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫῤ")) != None:
            cls.bstack1llllll11l11_opy_(bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠪ࡮ࡼࡺࠧῥ")), bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ῦ")))
        return bstack1lllll1l1lll_opy_
    @classmethod
    def bstack1llllll111ll_opy_(cls, bstack11l1l111ll_opy_):
        if bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῧ")) == None:
            cls.bstack1llllll11ll1_opy_()
            return [None, None, None]
        if bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ῠ")][bstack1l1l1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨῩ")] != True:
            cls.bstack1llllll11ll1_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨῪ")])
            return [None, None, None]
        logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭Ύ"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩῬ")] = bstack1l1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ῭")
        if bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡰࡷࡵࠩ΅")):
            os.environ[bstack1l1l1l1_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ`")] = json.dumps({
                bstack1l1l1l1_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ῰"): bstack11ll1lll11l_opy_(cls.bs_config),
                bstack1l1l1l1_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ῱"): bstack11ll1l1llll_opy_(cls.bs_config)
            })
        if bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫῲ")):
            os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩῳ")] = bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ῴ")]
        if bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ῵")].get(bstack1l1l1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧῶ"), {}).get(bstack1l1l1l1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫῷ")):
            os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩῸ")] = str(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩΌ")][bstack1l1l1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫῺ")][bstack1l1l1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨΏ")])
        else:
            os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ῼ")] = bstack1l1l1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ´")
        return [bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡫ࡹࡷࠫ῾")], bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῿")], os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ ")]]
    @classmethod
    def bstack1llllll1ll11_opy_(cls, bstack11l1l111ll_opy_):
        if bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ ")) == None:
            cls.bstack1llllll1l11l_opy_()
            return [None, None]
        if bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ ")][bstack1l1l1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ ")] != True:
            cls.bstack1llllll1l11l_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ ")])
            return [None, None]
        if bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ ")].get(bstack1l1l1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ ")):
            logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ "))
            parsed = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ "), bstack1l1l1l1_opy_ (u"ࠫࢀࢃࠧ ")))
            capabilities = bstack1l1l11111_opy_.bstack1llllll1111l_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ ")][bstack1l1l1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ​")][bstack1l1l1l1_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭‌")], bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭‍"), bstack1l1l1l1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ‎"))
            bstack1lllll1lllll_opy_ = capabilities[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ‏")]
            os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ‐")] = bstack1lllll1lllll_opy_
            if bstack1l1l1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ‑") in bstack11l1l111ll_opy_ and bstack11l1l111ll_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ‒")) is None:
                parsed[bstack1l1l1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ–")] = capabilities[bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ—")]
            os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ―")] = json.dumps(parsed)
            scripts = bstack1l1l11111_opy_.bstack1llllll1111l_opy_(bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ‖")][bstack1l1l1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ‗")][bstack1l1l1l1_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭‘")], bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ’"), bstack1l1l1l1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨ‚"))
            bstack1111ll1l1_opy_.bstack11ll111ll1_opy_(scripts)
            commands = bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ‛")][bstack1l1l1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ“")][bstack1l1l1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫ”")].get(bstack1l1l1l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭„"))
            bstack1111ll1l1_opy_.bstack11lll111ll1_opy_(commands)
            bstack11lll1l11l1_opy_ = capabilities.get(bstack1l1l1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‟"))
            bstack1111ll1l1_opy_.bstack11ll1l11lll_opy_(bstack11lll1l11l1_opy_)
            bstack1111ll1l1_opy_.store()
        return [bstack1lllll1lllll_opy_, bstack11l1l111ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ†")]]
    @classmethod
    def bstack1llllll11ll1_opy_(cls, response=None):
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ‡")] = bstack1l1l1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭•")
        os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭‣")] = bstack1l1l1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ․")
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ‥")] = bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ…")
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ‧")] = bstack1l1l1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ ")] = bstack1l1l1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ‪")
        cls.bstack1lllll1ll111_opy_(response, bstack1l1l1l1_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ‫"))
        return [None, None, None]
    @classmethod
    def bstack1llllll1l11l_opy_(cls, response=None):
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ‬")] = bstack1l1l1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ‭")
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ‮")] = bstack1l1l1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ ")
        os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ‰")] = bstack1l1l1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ‱")
        cls.bstack1lllll1ll111_opy_(response, bstack1l1l1l1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ′"))
        return [None, None, None]
    @classmethod
    def bstack1llllll11l11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ″")] = jwt
        os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ‴")] = build_hashed_id
    @classmethod
    def bstack1lllll1ll111_opy_(cls, response=None, product=bstack1l1l1l1_opy_ (u"ࠨࠢ‵")):
        if response == None or response.get(bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ‶")) == None:
            logger.error(product + bstack1l1l1l1_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ‷"))
            return
        for error in response[bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ‸")]:
            bstack111llllll11_opy_ = error[bstack1l1l1l1_opy_ (u"ࠪ࡯ࡪࡿࠧ‹")]
            error_message = error[bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ›")]
            if error_message:
                if bstack111llllll11_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ※"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l1l1_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ‼") + product + bstack1l1l1l1_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ‽"))
    @classmethod
    def bstack1llllll1ll1l_opy_(cls):
        if cls.bstack11111l11111_opy_ is not None:
            return
        cls.bstack11111l11111_opy_ = bstack111111lllll_opy_(cls.bstack1lllll1ll11l_opy_)
        cls.bstack11111l11111_opy_.start()
    @classmethod
    def bstack111l1lllll_opy_(cls):
        if cls.bstack11111l11111_opy_ is None:
            return
        cls.bstack11111l11111_opy_.shutdown()
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def bstack1lllll1ll11l_opy_(cls, bstack1111lll1l1_opy_, event_url=bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ‾")):
        config = {
            bstack1l1l1l1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ‿"): cls.default_headers()
        }
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ⁀").format(bstack1l1l1l1_opy_ (u"ࠫ࠱ࠦࠧ⁁").join([event[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⁂")] for event in bstack1111lll1l1_opy_])))
        response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"࠭ࡐࡐࡕࡗࠫ⁃"), cls.request_url(event_url), bstack1111lll1l1_opy_, config)
        bstack11lll111l11_opy_ = response.json()
    @classmethod
    def bstack11111111l_opy_(cls, bstack1111lll1l1_opy_, event_url=bstack1l1l1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⁄")):
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⁅").format(bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁆")]))
        if not bstack1l1l11111_opy_.bstack1llllll1l1ll_opy_(bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁇")]):
            logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⁈").format(bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⁉")]))
            return
        bstack11l111l1_opy_ = bstack1l1l11111_opy_.bstack1lllll1l1l1l_opy_(bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⁊")], bstack1111lll1l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⁋")))
        if bstack11l111l1_opy_ != None:
            if bstack1111lll1l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⁌")) != None:
                bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⁍")][bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⁎")] = bstack11l111l1_opy_
            else:
                bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⁏")] = bstack11l111l1_opy_
        if event_url == bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⁐"):
            cls.bstack1llllll1ll1l_opy_()
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⁑").format(bstack1111lll1l1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⁒")]))
            cls.bstack11111l11111_opy_.add(bstack1111lll1l1_opy_)
        elif event_url == bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⁓"):
            cls.bstack1lllll1ll11l_opy_([bstack1111lll1l1_opy_], event_url)
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def bstack1111l1111_opy_(cls, logs):
        bstack1lllll1ll1ll_opy_ = []
        for log in logs:
            bstack1lllll1lll1l_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⁔"): bstack1l1l1l1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ⁕"),
                bstack1l1l1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⁖"): log[bstack1l1l1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⁗")],
                bstack1l1l1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⁘"): log[bstack1l1l1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⁙")],
                bstack1l1l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ⁚"): {},
                bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⁛"): log[bstack1l1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⁜")],
            }
            if bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁝") in log:
                bstack1lllll1lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁞")] = log[bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ ")]
            elif bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁠") in log:
                bstack1lllll1lll1l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁡")] = log[bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁢")]
            bstack1lllll1ll1ll_opy_.append(bstack1lllll1lll1l_opy_)
        cls.bstack11111111l_opy_({
            bstack1l1l1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁣"): bstack1l1l1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⁤"),
            bstack1l1l1l1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⁥"): bstack1lllll1ll1ll_opy_
        })
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def bstack1llllll11l1l_opy_(cls, steps):
        bstack1lllll1l1ll1_opy_ = []
        for step in steps:
            bstack1lllll1l11ll_opy_ = {
                bstack1l1l1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫ⁦"): bstack1l1l1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ⁧"),
                bstack1l1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⁨"): step[bstack1l1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⁩")],
                bstack1l1l1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⁪"): step[bstack1l1l1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⁫")],
                bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⁬"): step[bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⁭")],
                bstack1l1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⁮"): step[bstack1l1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⁯")]
            }
            if bstack1l1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁰") in step:
                bstack1lllll1l11ll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁱ")] = step[bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁲")]
            elif bstack1l1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁳") in step:
                bstack1lllll1l11ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⁴")] = step[bstack1l1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁵")]
            bstack1lllll1l1ll1_opy_.append(bstack1lllll1l11ll_opy_)
        cls.bstack11111111l_opy_({
            bstack1l1l1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⁶"): bstack1l1l1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⁷"),
            bstack1l1l1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⁸"): bstack1lllll1l1ll1_opy_
        })
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l111111l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack11llll1111_opy_(cls, screenshot):
        cls.bstack11111111l_opy_({
            bstack1l1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⁹"): bstack1l1l1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⁺"),
            bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡩࡶࠫ⁻"): [{
                bstack1l1l1l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⁼"): bstack1l1l1l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ⁽"),
                bstack1l1l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⁾"): datetime.datetime.utcnow().isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬⁿ"),
                bstack1l1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ₀"): screenshot[bstack1l1l1l1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ₁")],
                bstack1l1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭₂"): screenshot[bstack1l1l1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ₃")]
            }]
        }, event_url=bstack1l1l1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭₄"))
    @classmethod
    @bstack111ll11111_opy_(class_method=True)
    def bstack1ll111l1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11111111l_opy_({
            bstack1l1l1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭₅"): bstack1l1l1l1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ₆"),
            bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭₇"): {
                bstack1l1l1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥ₈"): cls.current_test_uuid(),
                bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ₉"): cls.bstack111lll1l11_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1ll1l_opy_(cls, event: str, bstack1111lll1l1_opy_: bstack111l11l111_opy_):
        bstack1111lll111_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₊"): event,
            bstack1111lll1l1_opy_.bstack1111ll1ll1_opy_(): bstack1111lll1l1_opy_.bstack111l11111l_opy_(event)
        }
        cls.bstack11111111l_opy_(bstack1111lll111_opy_)
        result = getattr(bstack1111lll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ₋"), None)
        if event == bstack1l1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ₌"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₍"): bstack1l1l1l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ₎")}
        elif event == bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ₏"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ₐ"): getattr(result, bstack1l1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧₑ"), bstack1l1l1l1_opy_ (u"ࠨࠩₒ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ₓ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧₔ")] == bstack1l1l1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤₕ")) and (os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪₖ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫₗ")] == bstack1l1l1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧₘ")):
            return False
        return True
    @staticmethod
    def bstack1lllll1lll11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111llllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧₙ"): bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬₚ"),
            bstack1l1l1l1_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ₛ"): bstack1l1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩₜ")
        }
        if os.environ.get(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ₝"), None):
            headers[bstack1l1l1l1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭₞")] = bstack1l1l1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ₟").format(os.environ[bstack1l1l1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ₠")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1l1l1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ₡").format(bstack1llllll11111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ₢"), None)
    @staticmethod
    def bstack111lll1l11_opy_(driver):
        return {
            bstack11l11lll1ll_opy_(): bstack111llll1lll_opy_(driver)
        }
    @staticmethod
    def bstack1lllll1ll1l1_opy_(exception_info, report):
        return [{bstack1l1l1l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ₣"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111l11ll_opy_(typename):
        if bstack1l1l1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ₤") in typename:
            return bstack1l1l1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ₥")
        return bstack1l1l1l1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ₦")