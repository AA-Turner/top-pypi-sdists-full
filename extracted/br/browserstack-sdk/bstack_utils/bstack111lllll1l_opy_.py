# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1l1ll1l_opy_, bstack11ll1ll11ll_opy_, bstack1llll1ll_opy_, bstack111l1lll11_opy_, bstack111llll11l1_opy_, bstack111llll1lll_opy_, bstack11l11ll11l1_opy_, bstack1l11l11ll_opy_, bstack111ll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11111l111l1_opy_ import bstack11111l11111_opy_
import bstack_utils.bstack11l1lll11l_opy_ as bstack1l1ll1lll1_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
import bstack_utils.accessibility as bstack11l11lll11_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack11llll1l1l_opy_
from bstack_utils.bstack111lll1ll1_opy_ import bstack111l111lll_opy_
bstack1llllll1l111_opy_ = bstack11ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᾩ")
logger = logging.getLogger(__name__)
class bstack1l1l1l1ll_opy_:
    bstack11111l111l1_opy_ = None
    bs_config = None
    bstack1l1llll11l_opy_ = None
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1111lll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def launch(cls, bs_config, bstack1l1llll11l_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1llll11l_opy_ = bstack1l1llll11l_opy_
        try:
            cls.bstack1llllll1ll1l_opy_()
            bstack11ll1lll11l_opy_ = bstack11ll1l1ll1l_opy_(bs_config)
            bstack11ll1ll111l_opy_ = bstack11ll1ll11ll_opy_(bs_config)
            data = bstack1l1ll1lll1_opy_.bstack1lllll1llll1_opy_(bs_config, bstack1l1llll11l_opy_)
            config = {
                bstack11ll11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᾪ"): (bstack11ll1lll11l_opy_, bstack11ll1ll111l_opy_),
                bstack11ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᾫ"): cls.default_headers()
            }
            response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᾬ"), cls.request_url(bstack11ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᾭ")), data, config)
            if response.status_code != 200:
                bstack1ll111lll_opy_ = response.json()
                if bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᾮ")] == False:
                    cls.bstack1lllll1lll1l_opy_(bstack1ll111lll_opy_)
                    return
                cls.bstack1lllll1l1l1l_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᾯ")])
                cls.bstack1lllll1l1lll_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᾰ")])
                return None
            bstack1lllll1l1ll1_opy_ = cls.bstack1llllll11111_opy_(response)
            return bstack1lllll1l1ll1_opy_, response.json()
        except Exception as error:
            logger.error(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᾱ").format(str(error)))
            return None
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def stop(cls, bstack1llllll11ll1_opy_=None):
        if not bstack11l1ll11_opy_.on() and not bstack11l11lll11_opy_.on():
            return
        if os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾲ")) == bstack11ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢᾳ") or os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᾴ")) == bstack11ll11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ᾵"):
            logger.error(bstack11ll11_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᾶ"))
            return {
                bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᾷ"): bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ᾰ"),
                bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᾹ"): bstack11ll11_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᾺ")
            }
        try:
            cls.bstack11111l111l1_opy_.shutdown()
            data = {
                bstack11ll11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨΆ"): bstack1l11l11ll_opy_()
            }
            if not bstack1llllll11ll1_opy_ is None:
                data[bstack11ll11_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᾼ")] = [{
                    bstack11ll11_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ᾽"): bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫι"),
                    bstack11ll11_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ᾿"): bstack1llllll11ll1_opy_
                }]
            config = {
                bstack11ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ῀"): cls.default_headers()
            }
            bstack11ll1l11l11_opy_ = bstack11ll11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ῁").format(os.environ[bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣῂ")])
            bstack1lllll1l11ll_opy_ = cls.request_url(bstack11ll1l11l11_opy_)
            response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠫࡕ࡛ࡔࠨῃ"), bstack1lllll1l11ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll11_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦῄ"))
        except Exception as error:
            logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ῅") + str(error))
            return {
                bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧῆ"): bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧῇ"),
                bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪῈ"): str(error)
            }
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1llllll11111_opy_(cls, response):
        bstack1ll111lll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll1l1ll1_opy_ = {}
        if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠪ࡮ࡼࡺࠧΈ")) is None:
            os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨῊ")] = bstack11ll11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪΉ")
        else:
            os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪῌ")] = bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠧ࡫ࡹࡷࠫ῍"), bstack11ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭῎"))
        os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ῏")] = bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬῐ"), bstack11ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩῑ"))
        logger.info(bstack11ll11_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪῒ") + os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫΐ")));
        if bstack11l1ll11_opy_.bstack1lllll1ll1ll_opy_(cls.bs_config, cls.bstack1l1llll11l_opy_.get(bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ῔"), bstack11ll11_opy_ (u"ࠨࠩ῕"))) is True:
            bstack111111l1ll1_opy_, build_hashed_id, bstack1llllll1111l_opy_ = cls.bstack1llllll1l11l_opy_(bstack1ll111lll_opy_)
            if bstack111111l1ll1_opy_ != None and build_hashed_id != None:
                bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩῖ")] = {
                    bstack11ll11_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭ῗ"): bstack111111l1ll1_opy_,
                    bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ῐ"): build_hashed_id,
                    bstack11ll11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩῙ"): bstack1llllll1111l_opy_
                }
            else:
                bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ὶ")] = {}
        else:
            bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧΊ")] = {}
        bstack1lllll1lllll_opy_, build_hashed_id = cls.bstack1llllll1ll11_opy_(bstack1ll111lll_opy_)
        if bstack1lllll1lllll_opy_ != None and build_hashed_id != None:
            bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ῜")] = {
                bstack11ll11_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭῝"): bstack1lllll1lllll_opy_,
                bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ῞"): build_hashed_id,
            }
        else:
            bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ῟")] = {}
        if bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῠ")].get(bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨῡ")) != None or bstack1lllll1l1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧῢ")].get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪΰ")) != None:
            cls.bstack1lllll1l1l11_opy_(bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠩ࡭ࡻࡹ࠭ῤ")), bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬῥ")))
        return bstack1lllll1l1ll1_opy_
    @classmethod
    def bstack1llllll1l11l_opy_(cls, bstack1ll111lll_opy_):
        if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫῦ")) == None:
            cls.bstack1lllll1l1l1l_opy_()
            return [None, None, None]
        if bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῧ")][bstack11ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧῨ")] != True:
            cls.bstack1lllll1l1l1l_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῩ")])
            return [None, None, None]
        logger.debug(bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬῪ"))
        os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨΎ")] = bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨῬ")
        if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠫ࡯ࡽࡴࠨ῭")):
            os.environ[bstack11ll11_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ΅")] = json.dumps({
                bstack11ll11_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ`"): bstack11ll1l1ll1l_opy_(cls.bs_config),
                bstack11ll11_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ῰"): bstack11ll1ll11ll_opy_(cls.bs_config)
            })
        if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῱")):
            os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨῲ")] = bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬῳ")]
        if bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫῴ")].get(bstack11ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭῵"), {}).get(bstack11ll11_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪῶ")):
            os.environ[bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨῷ")] = str(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨῸ")][bstack11ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪΌ")][bstack11ll11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧῺ")])
        else:
            os.environ[bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬΏ")] = bstack11ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥῼ")
        return [bstack1ll111lll_opy_[bstack11ll11_opy_ (u"࠭ࡪࡸࡶࠪ´")], bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ῾")], os.environ[bstack11ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ῿")]]
    @classmethod
    def bstack1llllll1ll11_opy_(cls, bstack1ll111lll_opy_):
        if bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ ")) == None:
            cls.bstack1lllll1l1lll_opy_()
            return [None, None]
        if bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ ")][bstack11ll11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ ")] != True:
            cls.bstack1lllll1l1lll_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ ")])
            return [None, None]
        if bstack1ll111lll_opy_[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ ")].get(bstack11ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ ")):
            logger.debug(bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ "))
            parsed = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ "), bstack11ll11_opy_ (u"ࠪࡿࢂ࠭ ")))
            capabilities = bstack1l1ll1lll1_opy_.bstack1llllll111l1_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ ")][bstack11ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ ")][bstack11ll11_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ​")], bstack11ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ‌"), bstack11ll11_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ‍"))
            bstack1lllll1lllll_opy_ = capabilities[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ‎")]
            os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ‏")] = bstack1lllll1lllll_opy_
            if bstack11ll11_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ‐") in bstack1ll111lll_opy_ and bstack1ll111lll_opy_.get(bstack11ll11_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ‑")) is None:
                parsed[bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ‒")] = capabilities[bstack11ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ–")]
            os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ—")] = json.dumps(parsed)
            scripts = bstack1l1ll1lll1_opy_.bstack1llllll111l1_opy_(bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ―")][bstack11ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‖")][bstack11ll11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ‗")], bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‘"), bstack11ll11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧ’"))
            bstack11llll1l1l_opy_.bstack11ll1ll1ll_opy_(scripts)
            commands = bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ‚")][bstack11ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‛")][bstack11ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪ“")].get(bstack11ll11_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ”"))
            bstack11llll1l1l_opy_.bstack11lll111lll_opy_(commands)
            bstack11lll1l1ll1_opy_ = capabilities.get(bstack11ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ„"))
            bstack11llll1l1l_opy_.bstack11ll1l1l11l_opy_(bstack11lll1l1ll1_opy_)
            bstack11llll1l1l_opy_.store()
        return [bstack1lllll1lllll_opy_, bstack1ll111lll_opy_[bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ‟")]]
    @classmethod
    def bstack1lllll1l1l1l_opy_(cls, response=None):
        os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ†")] = bstack11ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ‡")
        os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ•")] = bstack11ll11_opy_ (u"ࠩࡱࡹࡱࡲࠧ‣")
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ․")] = bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ‥")
        os.environ[bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ…")] = bstack11ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ‧")
        os.environ[bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ ")] = bstack11ll11_opy_ (u"ࠣࡰࡸࡰࡱࠨ ")
        cls.bstack1lllll1lll1l_opy_(response, bstack11ll11_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ‪"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1l1lll_opy_(cls, response=None):
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ‫")] = bstack11ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ‬")
        os.environ[bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ‭")] = bstack11ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ‮")
        os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ ")] = bstack11ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭‰")
        cls.bstack1lllll1lll1l_opy_(response, bstack11ll11_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ‱"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1l1l11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ′")] = jwt
        os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ″")] = build_hashed_id
    @classmethod
    def bstack1lllll1lll1l_opy_(cls, response=None, product=bstack11ll11_opy_ (u"ࠧࠨ‴")):
        if response == None or response.get(bstack11ll11_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭‵")) == None:
            logger.error(product + bstack11ll11_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤ‶"))
            return
        for error in response[bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ‷")]:
            bstack11l11lll111_opy_ = error[bstack11ll11_opy_ (u"ࠩ࡮ࡩࡾ࠭‸")]
            error_message = error[bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ‹")]
            if error_message:
                if bstack11l11lll111_opy_ == bstack11ll11_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥ›"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll11_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨ※") + product + bstack11ll11_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ‼"))
    @classmethod
    def bstack1llllll1ll1l_opy_(cls):
        if cls.bstack11111l111l1_opy_ is not None:
            return
        cls.bstack11111l111l1_opy_ = bstack11111l11111_opy_(cls.bstack1llllll111ll_opy_)
        cls.bstack11111l111l1_opy_.start()
    @classmethod
    def bstack111l111111_opy_(cls):
        if cls.bstack11111l111l1_opy_ is None:
            return
        cls.bstack11111l111l1_opy_.shutdown()
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1llllll111ll_opy_(cls, bstack111l1l111l_opy_, event_url=bstack11ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭‽")):
        config = {
            bstack11ll11_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ‾"): cls.default_headers()
        }
        logger.debug(bstack11ll11_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ‿").format(bstack11ll11_opy_ (u"ࠪ࠰ࠥ࠭⁀").join([event[bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⁁")] for event in bstack111l1l111l_opy_])))
        response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠬࡖࡏࡔࡖࠪ⁂"), cls.request_url(event_url), bstack111l1l111l_opy_, config)
        bstack11lll11111l_opy_ = response.json()
    @classmethod
    def bstack1l1l11lll1_opy_(cls, bstack111l1l111l_opy_, event_url=bstack11ll11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⁃")):
        logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⁄").format(bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⁅")]))
        if not bstack1l1ll1lll1_opy_.bstack1llllll1l1l1_opy_(bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁆")]):
            logger.debug(bstack11ll11_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⁇").format(bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⁈")]))
            return
        bstack1l11111111_opy_ = bstack1l1ll1lll1_opy_.bstack1lllll1ll1l1_opy_(bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⁉")], bstack111l1l111l_opy_.get(bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⁊")))
        if bstack1l11111111_opy_ != None:
            if bstack111l1l111l_opy_.get(bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⁋")) != None:
                bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⁌")][bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⁍")] = bstack1l11111111_opy_
            else:
                bstack111l1l111l_opy_[bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⁎")] = bstack1l11111111_opy_
        if event_url == bstack11ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⁏"):
            cls.bstack1llllll1ll1l_opy_()
            logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⁐").format(bstack111l1l111l_opy_[bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⁑")]))
            cls.bstack11111l111l1_opy_.add(bstack111l1l111l_opy_)
        elif event_url == bstack11ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⁒"):
            cls.bstack1llllll111ll_opy_([bstack111l1l111l_opy_], event_url)
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack11ll1lllll_opy_(cls, logs):
        bstack1llllll11l11_opy_ = []
        for log in logs:
            bstack1llllll1l1ll_opy_ = {
                bstack11ll11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⁓"): bstack11ll11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ⁔"),
                bstack11ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⁕"): log[bstack11ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⁖")],
                bstack11ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⁗"): log[bstack11ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⁘")],
                bstack11ll11_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ⁙"): {},
                bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⁚"): log[bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⁛")],
            }
            if bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⁜") in log:
                bstack1llllll1l1ll_opy_[bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁝")] = log[bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁞")]
            elif bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ ") in log:
                bstack1llllll1l1ll_opy_[bstack11ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⁠")] = log[bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁡")]
            bstack1llllll11l11_opy_.append(bstack1llllll1l1ll_opy_)
        cls.bstack1l1l11lll1_opy_({
            bstack11ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁢"): bstack11ll11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⁣"),
            bstack11ll11_opy_ (u"ࠫࡱࡵࡧࡴࠩ⁤"): bstack1llllll11l11_opy_
        })
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1lllll1ll111_opy_(cls, steps):
        bstack1lllll1lll11_opy_ = []
        for step in steps:
            bstack1llllll11l1l_opy_ = {
                bstack11ll11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⁥"): bstack11ll11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ⁦"),
                bstack11ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⁧"): step[bstack11ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⁨")],
                bstack11ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⁩"): step[bstack11ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⁪")],
                bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⁫"): step[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⁬")],
                bstack11ll11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⁭"): step[bstack11ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⁮")]
            }
            if bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁯") in step:
                bstack1llllll11l1l_opy_[bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁰")] = step[bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁱ")]
            elif bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁲") in step:
                bstack1llllll11l1l_opy_[bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁳")] = step[bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⁴")]
            bstack1lllll1lll11_opy_.append(bstack1llllll11l1l_opy_)
        cls.bstack1l1l11lll1_opy_({
            bstack11ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⁵"): bstack11ll11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⁶"),
            bstack11ll11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⁷"): bstack1lllll1lll11_opy_
        })
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l11llll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack111lll11l_opy_(cls, screenshot):
        cls.bstack1l1l11lll1_opy_({
            bstack11ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁸"): bstack11ll11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⁹"),
            bstack11ll11_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⁺"): [{
                bstack11ll11_opy_ (u"࠭࡫ࡪࡰࡧࠫ⁻"): bstack11ll11_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ⁼"),
                bstack11ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⁽"): datetime.datetime.utcnow().isoformat() + bstack11ll11_opy_ (u"ࠩ࡝ࠫ⁾"),
                bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⁿ"): screenshot[bstack11ll11_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ₀")],
                bstack11ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ₁"): screenshot[bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭₂")]
            }]
        }, event_url=bstack11ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ₃"))
    @classmethod
    @bstack111l1lll11_opy_(class_method=True)
    def bstack1l1l111ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l11lll1_opy_({
            bstack11ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ₄"): bstack11ll11_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭₅"),
            bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ₆"): {
                bstack11ll11_opy_ (u"ࠦࡺࡻࡩࡥࠤ₇"): cls.current_test_uuid(),
                bstack11ll11_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ₈"): cls.bstack111ll1l111_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1l11l_opy_(cls, event: str, bstack111l1l111l_opy_: bstack111l111lll_opy_):
        bstack111l1l1ll1_opy_ = {
            bstack11ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ₉"): event,
            bstack111l1l111l_opy_.bstack111l1ll11l_opy_(): bstack111l1l111l_opy_.bstack111l1l11ll_opy_(event)
        }
        cls.bstack1l1l11lll1_opy_(bstack111l1l1ll1_opy_)
        result = getattr(bstack111l1l111l_opy_, bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₊"), None)
        if event == bstack11ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ₋"):
            threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ₌"): bstack11ll11_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ₍")}
        elif event == bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭₎"):
            threading.current_thread().bstackTestMeta = {bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ₏"): getattr(result, bstack11ll11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ₐ"), bstack11ll11_opy_ (u"ࠧࠨₑ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬₒ"), None) is None or os.environ[bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ₓ")] == bstack11ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣₔ")) and (os.environ.get(bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩₕ"), None) is None or os.environ[bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪₖ")] == bstack11ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦₗ")):
            return False
        return True
    @staticmethod
    def bstack1lllll1ll11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1l1l1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ₘ"): bstack11ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫₙ"),
            bstack11ll11_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬₚ"): bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨₛ")
        }
        if os.environ.get(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨₜ"), None):
            headers[bstack11ll11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ₝")] = bstack11ll11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ₞").format(os.environ[bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ₟")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11ll11_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ₠").format(bstack1llllll1l111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭₡"), None)
    @staticmethod
    def bstack111ll1l111_opy_(driver):
        return {
            bstack111llll11l1_opy_(): bstack111llll1lll_opy_(driver)
        }
    @staticmethod
    def bstack1llllll11lll_opy_(exception_info, report):
        return [{bstack11ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭₢"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111l111l_opy_(typename):
        if bstack11ll11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ₣") in typename:
            return bstack11ll11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ₤")
        return bstack11ll11_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ₥")