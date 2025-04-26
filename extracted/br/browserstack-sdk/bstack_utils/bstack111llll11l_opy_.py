# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll1ll1l1_opy_, bstack11lllll1111_opy_, bstack1l1lll11l_opy_, bstack111l1ll1ll_opy_, bstack11l1lll1111_opy_, bstack11l1ll11ll1_opy_, bstack11l1l1l111l_opy_, bstack11lll111l1_opy_, bstack11l11l1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11lll11_opy_ import bstack111l11lllll_opy_
import bstack_utils.bstack1l1l1ll1ll_opy_ as bstack1l1ll1ll11_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111l1llll_opy_
import bstack_utils.accessibility as bstack11ll1l1ll1_opy_
from bstack_utils.bstack11l111l11_opy_ import bstack11l111l11_opy_
from bstack_utils.bstack11l1111l11_opy_ import bstack111l1l11ll_opy_
bstack1111lll11ll_opy_ = bstack1l11lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨḀ")
logger = logging.getLogger(__name__)
class bstack111ll1ll1_opy_:
    bstack111l11lll11_opy_ = None
    bs_config = None
    bstack1l111111ll_opy_ = None
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1llll1l_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def launch(cls, bs_config, bstack1l111111ll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l111111ll_opy_ = bstack1l111111ll_opy_
        try:
            cls.bstack1111lll1l11_opy_()
            bstack11llll1lll1_opy_ = bstack11lll1ll1l1_opy_(bs_config)
            bstack11lllll111l_opy_ = bstack11lllll1111_opy_(bs_config)
            data = bstack1l1ll1ll11_opy_.bstack1111ll1l111_opy_(bs_config, bstack1l111111ll_opy_)
            config = {
                bstack1l11lll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧḁ"): (bstack11llll1lll1_opy_, bstack11lllll111l_opy_),
                bstack1l11lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫḂ"): cls.default_headers()
            }
            response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"ࠫࡕࡕࡓࡕࠩḃ"), cls.request_url(bstack1l11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬḄ")), data, config)
            if response.status_code != 200:
                bstack1l1lll111l_opy_ = response.json()
                if bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧḅ")] == False:
                    cls.bstack1111lll1111_opy_(bstack1l1lll111l_opy_)
                    return
                cls.bstack1111ll11111_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḆ")])
                cls.bstack1111ll1l1ll_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḇ")])
                return None
            bstack1111ll11l1l_opy_ = cls.bstack1111ll11lll_opy_(response)
            return bstack1111ll11l1l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢḈ").format(str(error)))
            return None
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def stop(cls, bstack1111l1lll11_opy_=None):
        if not bstack111l1llll_opy_.on() and not bstack11ll1l1ll1_opy_.on():
            return
        if os.environ.get(bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḉ")) == bstack1l11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤḊ") or os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḋ")) == bstack1l11lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦḌ"):
            logger.error(bstack1l11lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪḍ"))
            return {
                bstack1l11lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨḎ"): bstack1l11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨḏ"),
                bstack1l11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫḐ"): bstack1l11lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩḑ")
            }
        try:
            cls.bstack111l11lll11_opy_.shutdown()
            data = {
                bstack1l11lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪḒ"): bstack11lll111l1_opy_()
            }
            if not bstack1111l1lll11_opy_ is None:
                data[bstack1l11lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪḓ")] = [{
                    bstack1l11lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧḔ"): bstack1l11lll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ḕ"),
                    bstack1l11lll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩḖ"): bstack1111l1lll11_opy_
                }]
            config = {
                bstack1l11lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫḗ"): cls.default_headers()
            }
            bstack11l1ll11111_opy_ = bstack1l11lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬḘ").format(os.environ[bstack1l11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥḙ")])
            bstack1111l1lllll_opy_ = cls.request_url(bstack11l1ll11111_opy_)
            response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"࠭ࡐࡖࡖࠪḚ"), bstack1111l1lllll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l11lll_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨḛ"))
        except Exception as error:
            logger.error(bstack1l11lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧḜ") + str(error))
            return {
                bstack1l11lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩḝ"): bstack1l11lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩḞ"),
                bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬḟ"): str(error)
            }
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def bstack1111ll11lll_opy_(cls, response):
        bstack1l1lll111l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll11l1l_opy_ = {}
        if bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠬࡰࡷࡵࠩḠ")) is None:
            os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪḡ")] = bstack1l11lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬḢ")
        else:
            os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬḣ")] = bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠩ࡭ࡻࡹ࠭Ḥ"), bstack1l11lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨḥ"))
        os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḦ")] = bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḧ"), bstack1l11lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫḨ"))
        logger.info(bstack1l11lll_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬḩ") + os.getenv(bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ḫ")));
        if bstack111l1llll_opy_.bstack1111lll11l1_opy_(cls.bs_config, cls.bstack1l111111ll_opy_.get(bstack1l11lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪḫ"), bstack1l11lll_opy_ (u"ࠪࠫḬ"))) is True:
            bstack111l11l1l11_opy_, build_hashed_id, bstack1111ll111l1_opy_ = cls.bstack1111l1lll1l_opy_(bstack1l1lll111l_opy_)
            if bstack111l11l1l11_opy_ != None and build_hashed_id != None:
                bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḭ")] = {
                    bstack1l11lll_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨḮ"): bstack111l11l1l11_opy_,
                    bstack1l11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḯ"): build_hashed_id,
                    bstack1l11lll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫḰ"): bstack1111ll111l1_opy_
                }
            else:
                bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḱ")] = {}
        else:
            bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḲ")] = {}
        bstack1111ll1l11l_opy_, build_hashed_id = cls.bstack1111ll1l1l1_opy_(bstack1l1lll111l_opy_)
        if bstack1111ll1l11l_opy_ != None and build_hashed_id != None:
            bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪḳ")] = {
                bstack1l11lll_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨḴ"): bstack1111ll1l11l_opy_,
                bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḵ"): build_hashed_id,
            }
        else:
            bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ḷ")] = {}
        if bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḷ")].get(bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḸ")) != None or bstack1111ll11l1l_opy_[bstack1l11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩḹ")].get(bstack1l11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḺ")) != None:
            cls.bstack1111ll1ll1l_opy_(bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠫ࡯ࡽࡴࠨḻ")), bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḼ")))
        return bstack1111ll11l1l_opy_
    @classmethod
    def bstack1111l1lll1l_opy_(cls, bstack1l1lll111l_opy_):
        if bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḽ")) == None:
            cls.bstack1111ll11111_opy_()
            return [None, None, None]
        if bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḾ")][bstack1l11lll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩḿ")] != True:
            cls.bstack1111ll11111_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṀ")])
            return [None, None, None]
        logger.debug(bstack1l11lll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧṁ"))
        os.environ[bstack1l11lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪṂ")] = bstack1l11lll_opy_ (u"ࠬࡺࡲࡶࡧࠪṃ")
        if bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"࠭ࡪࡸࡶࠪṄ")):
            os.environ[bstack1l11lll_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫṅ")] = json.dumps({
                bstack1l11lll_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪṆ"): bstack11lll1ll1l1_opy_(cls.bs_config),
                bstack1l11lll_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫṇ"): bstack11lllll1111_opy_(cls.bs_config)
            })
        if bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬṈ")):
            os.environ[bstack1l11lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪṉ")] = bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṊ")]
        if bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ṋ")].get(bstack1l11lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṌ"), {}).get(bstack1l11lll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬṍ")):
            os.environ[bstack1l11lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪṎ")] = str(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṏ")][bstack1l11lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṐ")][bstack1l11lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩṑ")])
        else:
            os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧṒ")] = bstack1l11lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧṓ")
        return [bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠨ࡬ࡺࡸࠬṔ")], bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṕ")], os.environ[bstack1l11lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫṖ")]]
    @classmethod
    def bstack1111ll1l1l1_opy_(cls, bstack1l1lll111l_opy_):
        if bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṗ")) == None:
            cls.bstack1111ll1l1ll_opy_()
            return [None, None]
        if bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṘ")][bstack1l11lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧṙ")] != True:
            cls.bstack1111ll1l1ll_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṚ")])
            return [None, None]
        if bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṛ")].get(bstack1l11lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṜ")):
            logger.debug(bstack1l11lll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧṝ"))
            parsed = json.loads(os.getenv(bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬṞ"), bstack1l11lll_opy_ (u"ࠬࢁࡽࠨṟ")))
            capabilities = bstack1l1ll1ll11_opy_.bstack1111l1llll1_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṡ")][bstack1l11lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṡ")][bstack1l11lll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧṢ")], bstack1l11lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧṣ"), bstack1l11lll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩṤ"))
            bstack1111ll1l11l_opy_ = capabilities[bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩṥ")]
            os.environ[bstack1l11lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪṦ")] = bstack1111ll1l11l_opy_
            if bstack1l11lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣṧ") in bstack1l1lll111l_opy_ and bstack1l1lll111l_opy_.get(bstack1l11lll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨṨ")) is None:
                parsed[bstack1l11lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṩ")] = capabilities[bstack1l11lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪṪ")]
            os.environ[bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫṫ")] = json.dumps(parsed)
            scripts = bstack1l1ll1ll11_opy_.bstack1111l1llll1_opy_(bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṬ")][bstack1l11lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ṭ")][bstack1l11lll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧṮ")], bstack1l11lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṯ"), bstack1l11lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩṰ"))
            bstack11l111l11_opy_.bstack1l11lll11l_opy_(scripts)
            commands = bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṱ")][bstack1l11lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṲ")][bstack1l11lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬṳ")].get(bstack1l11lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧṴ"))
            bstack11l111l11_opy_.bstack11lllll1ll1_opy_(commands)
            bstack11l111l11_opy_.store()
        return [bstack1111ll1l11l_opy_, bstack1l1lll111l_opy_[bstack1l11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨṵ")]]
    @classmethod
    def bstack1111ll11111_opy_(cls, response=None):
        os.environ[bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬṶ")] = bstack1l11lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ṷ")
        os.environ[bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ṹ")] = bstack1l11lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṹ")
        os.environ[bstack1l11lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪṺ")] = bstack1l11lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫṻ")
        os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬṼ")] = bstack1l11lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧṽ")
        os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩṾ")] = bstack1l11lll_opy_ (u"ࠤࡱࡹࡱࡲࠢṿ")
        cls.bstack1111lll1111_opy_(response, bstack1l11lll_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥẀ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1l1ll_opy_(cls, response=None):
        os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩẁ")] = bstack1l11lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪẂ")
        os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫẃ")] = bstack1l11lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬẄ")
        os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẅ")] = bstack1l11lll_opy_ (u"ࠩࡱࡹࡱࡲࠧẆ")
        cls.bstack1111lll1111_opy_(response, bstack1l11lll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥẇ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1ll1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẈ")] = jwt
        os.environ[bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪẉ")] = build_hashed_id
    @classmethod
    def bstack1111lll1111_opy_(cls, response=None, product=bstack1l11lll_opy_ (u"ࠨࠢẊ")):
        if response == None or response.get(bstack1l11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧẋ")) == None:
            logger.error(product + bstack1l11lll_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥẌ"))
            return
        for error in response[bstack1l11lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩẍ")]:
            bstack11l1lllll11_opy_ = error[bstack1l11lll_opy_ (u"ࠪ࡯ࡪࡿࠧẎ")]
            error_message = error[bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẏ")]
            if error_message:
                if bstack11l1lllll11_opy_ == bstack1l11lll_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦẐ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l11lll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢẑ") + product + bstack1l11lll_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧẒ"))
    @classmethod
    def bstack1111lll1l11_opy_(cls):
        if cls.bstack111l11lll11_opy_ is not None:
            return
        cls.bstack111l11lll11_opy_ = bstack111l11lllll_opy_(cls.bstack1111ll1llll_opy_)
        cls.bstack111l11lll11_opy_.start()
    @classmethod
    def bstack111l11ll1l_opy_(cls):
        if cls.bstack111l11lll11_opy_ is None:
            return
        cls.bstack111l11lll11_opy_.shutdown()
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def bstack1111ll1llll_opy_(cls, bstack111ll11l11_opy_, event_url=bstack1l11lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧẓ")):
        config = {
            bstack1l11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪẔ"): cls.default_headers()
        }
        logger.debug(bstack1l11lll_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥẕ").format(bstack1l11lll_opy_ (u"ࠫ࠱ࠦࠧẖ").join([event[bstack1l11lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẗ")] for event in bstack111ll11l11_opy_])))
        response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"࠭ࡐࡐࡕࡗࠫẘ"), cls.request_url(event_url), bstack111ll11l11_opy_, config)
        bstack11llll1llll_opy_ = response.json()
    @classmethod
    def bstack11lllll1l_opy_(cls, bstack111ll11l11_opy_, event_url=bstack1l11lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ẙ")):
        logger.debug(bstack1l11lll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣẚ").format(bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ẛ")]))
        if not bstack1l1ll1ll11_opy_.bstack1111lll111l_opy_(bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẜ")]):
            logger.debug(bstack1l11lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤẝ").format(bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẞ")]))
            return
        bstack1ll1111l_opy_ = bstack1l1ll1ll11_opy_.bstack1111l1ll1ll_opy_(bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẟ")], bstack111ll11l11_opy_.get(bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩẠ")))
        if bstack1ll1111l_opy_ != None:
            if bstack111ll11l11_opy_.get(bstack1l11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪạ")) != None:
                bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫẢ")][bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨả")] = bstack1ll1111l_opy_
            else:
                bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩẤ")] = bstack1ll1111l_opy_
        if event_url == bstack1l11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫấ"):
            cls.bstack1111lll1l11_opy_()
            logger.debug(bstack1l11lll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤẦ").format(bstack111ll11l11_opy_[bstack1l11lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫầ")]))
            cls.bstack111l11lll11_opy_.add(bstack111ll11l11_opy_)
        elif event_url == bstack1l11lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ẩ"):
            cls.bstack1111ll1llll_opy_([bstack111ll11l11_opy_], event_url)
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def bstack1l1l111ll_opy_(cls, logs):
        bstack1111lll1l1l_opy_ = []
        for log in logs:
            bstack1111ll1111l_opy_ = {
                bstack1l11lll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧẩ"): bstack1l11lll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬẪ"),
                bstack1l11lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẫ"): log[bstack1l11lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫẬ")],
                bstack1l11lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩậ"): log[bstack1l11lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪẮ")],
                bstack1l11lll_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨắ"): {},
                bstack1l11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẰ"): log[bstack1l11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫằ")],
            }
            if bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẲ") in log:
                bstack1111ll1111l_opy_[bstack1l11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẳ")] = log[bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ẵ")]
            elif bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẵ") in log:
                bstack1111ll1111l_opy_[bstack1l11lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẶ")] = log[bstack1l11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩặ")]
            bstack1111lll1l1l_opy_.append(bstack1111ll1111l_opy_)
        cls.bstack11lllll1l_opy_({
            bstack1l11lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẸ"): bstack1l11lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨẹ"),
            bstack1l11lll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪẺ"): bstack1111lll1l1l_opy_
        })
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def bstack1111ll11ll1_opy_(cls, steps):
        bstack1111ll1lll1_opy_ = []
        for step in steps:
            bstack1111ll1ll11_opy_ = {
                bstack1l11lll_opy_ (u"࠭࡫ࡪࡰࡧࠫẻ"): bstack1l11lll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪẼ"),
                bstack1l11lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧẽ"): step[bstack1l11lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨẾ")],
                bstack1l11lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ế"): step[bstack1l11lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧỀ")],
                bstack1l11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ề"): step[bstack1l11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧỂ")],
                bstack1l11lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩể"): step[bstack1l11lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪỄ")]
            }
            if bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩễ") in step:
                bstack1111ll1ll11_opy_[bstack1l11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỆ")] = step[bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫệ")]
            elif bstack1l11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬỈ") in step:
                bstack1111ll1ll11_opy_[bstack1l11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ỉ")] = step[bstack1l11lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧỊ")]
            bstack1111ll1lll1_opy_.append(bstack1111ll1ll11_opy_)
        cls.bstack11lllll1l_opy_({
            bstack1l11lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬị"): bstack1l11lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ọ"),
            bstack1l11lll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨọ"): bstack1111ll1lll1_opy_
        })
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11lll1ll1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack11ll1ll111_opy_(cls, screenshot):
        cls.bstack11lllll1l_opy_({
            bstack1l11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨỎ"): bstack1l11lll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩỏ"),
            bstack1l11lll_opy_ (u"࠭࡬ࡰࡩࡶࠫỐ"): [{
                bstack1l11lll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬố"): bstack1l11lll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪỒ"),
                bstack1l11lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬồ"): datetime.datetime.utcnow().isoformat() + bstack1l11lll_opy_ (u"ࠪ࡞ࠬỔ"),
                bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬổ"): screenshot[bstack1l11lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫỖ")],
                bstack1l11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ỗ"): screenshot[bstack1l11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧỘ")]
            }]
        }, event_url=bstack1l11lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ộ"))
    @classmethod
    @bstack111l1ll1ll_opy_(class_method=True)
    def bstack1ll1l1l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11lllll1l_opy_({
            bstack1l11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ớ"): bstack1l11lll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧớ"),
            bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ờ"): {
                bstack1l11lll_opy_ (u"ࠧࡻࡵࡪࡦࠥờ"): cls.current_test_uuid(),
                bstack1l11lll_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧỞ"): cls.bstack11l1111lll_opy_(driver)
            }
        })
    @classmethod
    def bstack11l111l11l_opy_(cls, event: str, bstack111ll11l11_opy_: bstack111l1l11ll_opy_):
        bstack111lll1l11_opy_ = {
            bstack1l11lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫở"): event,
            bstack111ll11l11_opy_.bstack111l1l11l1_opy_(): bstack111ll11l11_opy_.bstack111l11l1l1_opy_(event)
        }
        cls.bstack11lllll1l_opy_(bstack111lll1l11_opy_)
        result = getattr(bstack111ll11l11_opy_, bstack1l11lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨỠ"), None)
        if event == bstack1l11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪỡ"):
            threading.current_thread().bstackTestMeta = {bstack1l11lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỢ"): bstack1l11lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬợ")}
        elif event == bstack1l11lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧỤ"):
            threading.current_thread().bstackTestMeta = {bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ụ"): getattr(result, bstack1l11lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧỦ"), bstack1l11lll_opy_ (u"ࠨࠩủ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ứ"), None) is None or os.environ[bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧứ")] == bstack1l11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤỪ")) and (os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪừ"), None) is None or os.environ[bstack1l11lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫỬ")] == bstack1l11lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧử")):
            return False
        return True
    @staticmethod
    def bstack1111ll11l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111ll1ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l11lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧỮ"): bstack1l11lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬữ"),
            bstack1l11lll_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭Ự"): bstack1l11lll_opy_ (u"ࠫࡹࡸࡵࡦࠩự")
        }
        if os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩỲ"), None):
            headers[bstack1l11lll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ỳ")] = bstack1l11lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪỴ").format(os.environ[bstack1l11lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧỵ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l11lll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨỶ").format(bstack1111lll11ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l11lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧỷ"), None)
    @staticmethod
    def bstack11l1111lll_opy_(driver):
        return {
            bstack11l1lll1111_opy_(): bstack11l1ll11ll1_opy_(driver)
        }
    @staticmethod
    def bstack1111ll111ll_opy_(exception_info, report):
        return [{bstack1l11lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧỸ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack1l11lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣỹ") in typename:
            return bstack1l11lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢỺ")
        return bstack1l11lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣỻ")