# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11llll1l11l_opy_, bstack11llll1ll11_opy_, bstack1l1ll1111_opy_, bstack111l1l1111_opy_, bstack11ll11l1111_opy_, bstack11l1l1ll11l_opy_, bstack11l1ll1llll_opy_, bstack1l11l1l11l_opy_, bstack1lll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11ll11l_opy_ import bstack111l11l1lll_opy_
import bstack_utils.bstack111ll11l1_opy_ as bstack11ll1l111l_opy_
from bstack_utils.bstack11l1111ll1_opy_ import bstack1ll1l111l1_opy_
import bstack_utils.accessibility as bstack11111l11l_opy_
from bstack_utils.bstack1l1llll1_opy_ import bstack1l1llll1_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111lll1l11_opy_
bstack1111ll1l111_opy_ = bstack1llllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪḂ")
logger = logging.getLogger(__name__)
class bstack11l11llll_opy_:
    bstack111l11ll11l_opy_ = None
    bs_config = None
    bstack1l1lllllll_opy_ = None
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1llllll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def launch(cls, bs_config, bstack1l1lllllll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1lllllll_opy_ = bstack1l1lllllll_opy_
        try:
            cls.bstack1111ll1ll11_opy_()
            bstack11llll1l111_opy_ = bstack11llll1l11l_opy_(bs_config)
            bstack11lll1ll11l_opy_ = bstack11llll1ll11_opy_(bs_config)
            data = bstack11ll1l111l_opy_.bstack1111ll1l1l1_opy_(bs_config, bstack1l1lllllll_opy_)
            config = {
                bstack1llllll_opy_ (u"ࠫࡦࡻࡴࡩࠩḃ"): (bstack11llll1l111_opy_, bstack11lll1ll11l_opy_),
                bstack1llllll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭Ḅ"): cls.default_headers()
            }
            response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"࠭ࡐࡐࡕࡗࠫḅ"), cls.request_url(bstack1llllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧḆ")), data, config)
            if response.status_code != 200:
                bstack11lll1l1l1_opy_ = response.json()
                if bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩḇ")] == False:
                    cls.bstack1111l1lllll_opy_(bstack11lll1l1l1_opy_)
                    return
                cls.bstack1111lll11l1_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḈ")])
                cls.bstack1111ll11l1l_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪḉ")])
                return None
            bstack1111ll1llll_opy_ = cls.bstack1111ll11l11_opy_(response)
            return bstack1111ll1llll_opy_, response.json()
        except Exception as error:
            logger.error(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤḊ").format(str(error)))
            return None
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def stop(cls, bstack1111l1lll1l_opy_=None):
        if not bstack1ll1l111l1_opy_.on() and not bstack11111l11l_opy_.on():
            return
        if os.environ.get(bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩḋ")) == bstack1llllll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦḌ") or os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬḍ")) == bstack1llllll_opy_ (u"ࠣࡰࡸࡰࡱࠨḎ"):
            logger.error(bstack1llllll_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬḏ"))
            return {
                bstack1llllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪḐ"): bstack1llllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḑ"),
                bstack1llllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ḓ"): bstack1llllll_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫḓ")
            }
        try:
            cls.bstack111l11ll11l_opy_.shutdown()
            data = {
                bstack1llllll_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬḔ"): bstack1l11l1l11l_opy_()
            }
            if not bstack1111l1lll1l_opy_ is None:
                data[bstack1llllll_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬḕ")] = [{
                    bstack1llllll_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩḖ"): bstack1llllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨḗ"),
                    bstack1llllll_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫḘ"): bstack1111l1lll1l_opy_
                }]
            config = {
                bstack1llllll_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ḙ"): cls.default_headers()
            }
            bstack11l1l1ll1l1_opy_ = bstack1llllll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧḚ").format(os.environ[bstack1llllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧḛ")])
            bstack1111ll1l1ll_opy_ = cls.request_url(bstack11l1l1ll1l1_opy_)
            response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠨࡒࡘࡘࠬḜ"), bstack1111ll1l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1llllll_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣḝ"))
        except Exception as error:
            logger.error(bstack1llllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢḞ") + str(error))
            return {
                bstack1llllll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫḟ"): bstack1llllll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḠ"),
                bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧḡ"): str(error)
            }
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111ll11l11_opy_(cls, response):
        bstack11lll1l1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll1llll_opy_ = {}
        if bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠧ࡫ࡹࡷࠫḢ")) is None:
            os.environ[bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬḣ")] = bstack1llllll_opy_ (u"ࠩࡱࡹࡱࡲࠧḤ")
        else:
            os.environ[bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḥ")] = bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠫ࡯ࡽࡴࠨḦ"), bstack1llllll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪḧ"))
        os.environ[bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫḨ")] = bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḩ"), bstack1llllll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ḫ"))
        logger.info(bstack1llllll_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧḫ") + os.getenv(bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨḬ")));
        if bstack1ll1l111l1_opy_.bstack1111ll1111l_opy_(cls.bs_config, cls.bstack1l1lllllll_opy_.get(bstack1llllll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬḭ"), bstack1llllll_opy_ (u"ࠬ࠭Ḯ"))) is True:
            bstack111l11l11l1_opy_, build_hashed_id, bstack1111ll1l11l_opy_ = cls.bstack1111l1lll11_opy_(bstack11lll1l1l1_opy_)
            if bstack111l11l11l1_opy_ != None and build_hashed_id != None:
                bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḯ")] = {
                    bstack1llllll_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪḰ"): bstack111l11l11l1_opy_,
                    bstack1llllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḱ"): build_hashed_id,
                    bstack1llllll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ḳ"): bstack1111ll1l11l_opy_
                }
            else:
                bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḳ")] = {}
        else:
            bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḴ")] = {}
        bstack1111lll11ll_opy_, build_hashed_id = cls.bstack1111ll11111_opy_(bstack11lll1l1l1_opy_)
        if bstack1111lll11ll_opy_ != None and build_hashed_id != None:
            bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḵ")] = {
                bstack1llllll_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪḶ"): bstack1111lll11ll_opy_,
                bstack1llllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḷ"): build_hashed_id,
            }
        else:
            bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḸ")] = {}
        if bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḹ")].get(bstack1llllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḺ")) != None or bstack1111ll1llll_opy_[bstack1llllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḻ")].get(bstack1llllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḼ")) != None:
            cls.bstack1111ll111ll_opy_(bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"࠭ࡪࡸࡶࠪḽ")), bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḾ")))
        return bstack1111ll1llll_opy_
    @classmethod
    def bstack1111l1lll11_opy_(cls, bstack11lll1l1l1_opy_):
        if bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḿ")) == None:
            cls.bstack1111lll11l1_opy_()
            return [None, None, None]
        if bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṀ")][bstack1llllll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫṁ")] != True:
            cls.bstack1111lll11l1_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṂ")])
            return [None, None, None]
        logger.debug(bstack1llllll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩṃ"))
        os.environ[bstack1llllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬṄ")] = bstack1llllll_opy_ (u"ࠧࡵࡴࡸࡩࠬṅ")
        if bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠨ࡬ࡺࡸࠬṆ")):
            os.environ[bstack1llllll_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ṇ")] = json.dumps({
                bstack1llllll_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬṈ"): bstack11llll1l11l_opy_(cls.bs_config),
                bstack1llllll_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ṉ"): bstack11llll1ll11_opy_(cls.bs_config)
            })
        if bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṊ")):
            os.environ[bstack1llllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬṋ")] = bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩṌ")]
        if bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨṍ")].get(bstack1llllll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṎ"), {}).get(bstack1llllll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧṏ")):
            os.environ[bstack1llllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬṐ")] = str(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṑ")][bstack1llllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṒ")][bstack1llllll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫṓ")])
        else:
            os.environ[bstack1llllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩṔ")] = bstack1llllll_opy_ (u"ࠤࡱࡹࡱࡲࠢṕ")
        return [bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠪ࡮ࡼࡺࠧṖ")], bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ṗ")], os.environ[bstack1llllll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭Ṙ")]]
    @classmethod
    def bstack1111ll11111_opy_(cls, bstack11lll1l1l1_opy_):
        if bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṙ")) == None:
            cls.bstack1111ll11l1l_opy_()
            return [None, None]
        if bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṚ")][bstack1llllll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩṛ")] != True:
            cls.bstack1111ll11l1l_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṜ")])
            return [None, None]
        if bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṝ")].get(bstack1llllll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṞ")):
            logger.debug(bstack1llllll_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩṟ"))
            parsed = json.loads(os.getenv(bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧṠ"), bstack1llllll_opy_ (u"ࠧࡼࡿࠪṡ")))
            capabilities = bstack11ll1l111l_opy_.bstack1111ll111l1_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṢ")][bstack1llllll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṣ")][bstack1llllll_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩṤ")], bstack1llllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩṥ"), bstack1llllll_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫṦ"))
            bstack1111lll11ll_opy_ = capabilities[bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫṧ")]
            os.environ[bstack1llllll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬṨ")] = bstack1111lll11ll_opy_
            if bstack1llllll_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥṩ") in bstack11lll1l1l1_opy_ and bstack11lll1l1l1_opy_.get(bstack1llllll_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣṪ")) is None:
                parsed[bstack1llllll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫṫ")] = capabilities[bstack1llllll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬṬ")]
            os.environ[bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ṭ")] = json.dumps(parsed)
            scripts = bstack11ll1l111l_opy_.bstack1111ll111l1_opy_(bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṯ")][bstack1llllll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṯ")][bstack1llllll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩṰ")], bstack1llllll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧṱ"), bstack1llllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫṲ"))
            bstack1l1llll1_opy_.bstack1l11ll1ll_opy_(scripts)
            commands = bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṳ")][bstack1llllll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ṵ")][bstack1llllll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧṵ")].get(bstack1llllll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩṶ"))
            bstack1l1llll1_opy_.bstack11llll1l1ll_opy_(commands)
            bstack1l1llll1_opy_.store()
        return [bstack1111lll11ll_opy_, bstack11lll1l1l1_opy_[bstack1llllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṷ")]]
    @classmethod
    def bstack1111lll11l1_opy_(cls, response=None):
        os.environ[bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧṸ")] = bstack1llllll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṹ")
        os.environ[bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨṺ")] = bstack1llllll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪṻ")
        os.environ[bstack1llllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬṼ")] = bstack1llllll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ṽ")
        os.environ[bstack1llllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧṾ")] = bstack1llllll_opy_ (u"ࠤࡱࡹࡱࡲࠢṿ")
        os.environ[bstack1llllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫẀ")] = bstack1llllll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤẁ")
        cls.bstack1111l1lllll_opy_(response, bstack1llllll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧẂ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, response=None):
        os.environ[bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫẃ")] = bstack1llllll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬẄ")
        os.environ[bstack1llllll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ẅ")] = bstack1llllll_opy_ (u"ࠩࡱࡹࡱࡲࠧẆ")
        os.environ[bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧẇ")] = bstack1llllll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩẈ")
        cls.bstack1111l1lllll_opy_(response, bstack1llllll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧẉ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll111ll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪẊ")] = jwt
        os.environ[bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬẋ")] = build_hashed_id
    @classmethod
    def bstack1111l1lllll_opy_(cls, response=None, product=bstack1llllll_opy_ (u"ࠣࠤẌ")):
        if response == None or response.get(bstack1llllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩẍ")) == None:
            logger.error(product + bstack1llllll_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧẎ"))
            return
        for error in response[bstack1llllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫẏ")]:
            bstack11l1l11ll11_opy_ = error[bstack1llllll_opy_ (u"ࠬࡱࡥࡺࠩẐ")]
            error_message = error[bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẑ")]
            if error_message:
                if bstack11l1l11ll11_opy_ == bstack1llllll_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨẒ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1llllll_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤẓ") + product + bstack1llllll_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢẔ"))
    @classmethod
    def bstack1111ll1ll11_opy_(cls):
        if cls.bstack111l11ll11l_opy_ is not None:
            return
        cls.bstack111l11ll11l_opy_ = bstack111l11l1lll_opy_(cls.bstack1111lll111l_opy_)
        cls.bstack111l11ll11l_opy_.start()
    @classmethod
    def bstack111ll1l1l1_opy_(cls):
        if cls.bstack111l11ll11l_opy_ is None:
            return
        cls.bstack111l11ll11l_opy_.shutdown()
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111lll111l_opy_(cls, bstack111l1l1l1l_opy_, event_url=bstack1llllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩẕ")):
        config = {
            bstack1llllll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬẖ"): cls.default_headers()
        }
        logger.debug(bstack1llllll_opy_ (u"ࠧࡶ࡯ࡴࡶࡢࡨࡦࡺࡡ࠻ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡴࠢࡾࢁࠧẗ").format(bstack1llllll_opy_ (u"࠭ࠬࠡࠩẘ").join([event[bstack1llllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẙ")] for event in bstack111l1l1l1l_opy_])))
        response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ẚ"), cls.request_url(event_url), bstack111l1l1l1l_opy_, config)
        bstack11lll1lllll_opy_ = response.json()
    @classmethod
    def bstack1lll1l1ll_opy_(cls, bstack111l1l1l1l_opy_, event_url=bstack1llllll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨẛ")):
        logger.debug(bstack1llllll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡢࡦࡧࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥẜ").format(bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẝ")]))
        if not bstack11ll1l111l_opy_.bstack1111lll1l11_opy_(bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẞ")]):
            logger.debug(bstack1llllll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡒࡴࡺࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦẟ").format(bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẠ")]))
            return
        bstack1lll1l1l1_opy_ = bstack11ll1l111l_opy_.bstack1111ll11ll1_opy_(bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬạ")], bstack111l1l1l1l_opy_.get(bstack1llllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫẢ")))
        if bstack1lll1l1l1_opy_ != None:
            if bstack111l1l1l1l_opy_.get(bstack1llllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬả")) != None:
                bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ấ")][bstack1llllll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪấ")] = bstack1lll1l1l1_opy_
            else:
                bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫẦ")] = bstack1lll1l1l1_opy_
        if event_url == bstack1llllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ầ"):
            cls.bstack1111ll1ll11_opy_()
            logger.debug(bstack1llllll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦẨ").format(bstack111l1l1l1l_opy_[bstack1llllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ẩ")]))
            cls.bstack111l11ll11l_opy_.add(bstack111l1l1l1l_opy_)
        elif event_url == bstack1llllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨẪ"):
            cls.bstack1111lll111l_opy_([bstack111l1l1l1l_opy_], event_url)
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack11lll11l1l_opy_(cls, logs):
        bstack1111l1ll1ll_opy_ = []
        for log in logs:
            bstack1111lll1l1l_opy_ = {
                bstack1llllll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩẫ"): bstack1llllll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧẬ"),
                bstack1llllll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬậ"): log[bstack1llllll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ắ")],
                bstack1llllll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫắ"): log[bstack1llllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬẰ")],
                bstack1llllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪằ"): {},
                bstack1llllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẲ"): log[bstack1llllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ẳ")],
            }
            if bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ẵ") in log:
                bstack1111lll1l1l_opy_[bstack1llllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẵ")] = log[bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẶ")]
            elif bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩặ") in log:
                bstack1111lll1l1l_opy_[bstack1llllll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẸ")] = log[bstack1llllll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẹ")]
            bstack1111l1ll1ll_opy_.append(bstack1111lll1l1l_opy_)
        cls.bstack1lll1l1ll_opy_({
            bstack1llllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẺ"): bstack1llllll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪẻ"),
            bstack1llllll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬẼ"): bstack1111l1ll1ll_opy_
        })
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack1111l1llll1_opy_(cls, steps):
        bstack1111ll11lll_opy_ = []
        for step in steps:
            bstack1111ll1ll1l_opy_ = {
                bstack1llllll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ẽ"): bstack1llllll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬẾ"),
                bstack1llllll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩế"): step[bstack1llllll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪỀ")],
                bstack1llllll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨề"): step[bstack1llllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩỂ")],
                bstack1llllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨể"): step[bstack1llllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩỄ")],
                bstack1llllll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫễ"): step[bstack1llllll_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬỆ")]
            }
            if bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫệ") in step:
                bstack1111ll1ll1l_opy_[bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬỈ")] = step[bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ỉ")]
            elif bstack1llllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧỊ") in step:
                bstack1111ll1ll1l_opy_[bstack1llllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨị")] = step[bstack1llllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỌ")]
            bstack1111ll11lll_opy_.append(bstack1111ll1ll1l_opy_)
        cls.bstack1lll1l1ll_opy_({
            bstack1llllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧọ"): bstack1llllll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨỎ"),
            bstack1llllll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪỏ"): bstack1111ll11lll_opy_
        })
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l111llll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1lll11ll11_opy_(cls, screenshot):
        cls.bstack1lll1l1ll_opy_({
            bstack1llllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪỐ"): bstack1llllll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫố"),
            bstack1llllll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ồ"): [{
                bstack1llllll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧồ"): bstack1llllll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬỔ"),
                bstack1llllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧổ"): datetime.datetime.utcnow().isoformat() + bstack1llllll_opy_ (u"ࠬࡠࠧỖ"),
                bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧỗ"): screenshot[bstack1llllll_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭Ộ")],
                bstack1llllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨộ"): screenshot[bstack1llllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỚ")]
            }]
        }, event_url=bstack1llllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨớ"))
    @classmethod
    @bstack111l1l1111_opy_(class_method=True)
    def bstack11l111ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1lll1l1ll_opy_({
            bstack1llllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨỜ"): bstack1llllll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩờ"),
            bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨỞ"): {
                bstack1llllll_opy_ (u"ࠢࡶࡷ࡬ࡨࠧở"): cls.current_test_uuid(),
                bstack1llllll_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢỠ"): cls.bstack11l111llll_opy_(driver)
            }
        })
    @classmethod
    def bstack111llllll1_opy_(cls, event: str, bstack111l1l1l1l_opy_: bstack111lll1l11_opy_):
        bstack111lll11ll_opy_ = {
            bstack1llllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ỡ"): event,
            bstack111l1l1l1l_opy_.bstack111l11l11l_opy_(): bstack111l1l1l1l_opy_.bstack111l11l1ll_opy_(event)
        }
        cls.bstack1lll1l1ll_opy_(bstack111lll11ll_opy_)
        result = getattr(bstack111l1l1l1l_opy_, bstack1llllll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪỢ"), None)
        if event == bstack1llllll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬợ"):
            threading.current_thread().bstackTestMeta = {bstack1llllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬỤ"): bstack1llllll_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧụ")}
        elif event == bstack1llllll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩỦ"):
            threading.current_thread().bstackTestMeta = {bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨủ"): getattr(result, bstack1llllll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩỨ"), bstack1llllll_opy_ (u"ࠪࠫứ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỪ"), None) is None or os.environ[bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩừ")] == bstack1llllll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦỬ")) and (os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬử"), None) is None or os.environ[bstack1llllll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ữ")] == bstack1llllll_opy_ (u"ࠤࡱࡹࡱࡲࠢữ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1lll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11llll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1llllll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỰ"): bstack1llllll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧự"),
            bstack1llllll_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨỲ"): bstack1llllll_opy_ (u"࠭ࡴࡳࡷࡨࠫỳ")
        }
        if os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫỴ"), None):
            headers[bstack1llllll_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨỵ")] = bstack1llllll_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬỶ").format(os.environ[bstack1llllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢỷ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1llllll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪỸ").format(bstack1111ll1l111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1llllll_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩỹ"), None)
    @staticmethod
    def bstack11l111llll_opy_(driver):
        return {
            bstack11ll11l1111_opy_(): bstack11l1l1ll11l_opy_(driver)
        }
    @staticmethod
    def bstack1111lll1111_opy_(exception_info, report):
        return [{bstack1llllll_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩỺ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack1llllll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥỻ") in typename:
            return bstack1llllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤỼ")
        return bstack1llllll_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥỽ")