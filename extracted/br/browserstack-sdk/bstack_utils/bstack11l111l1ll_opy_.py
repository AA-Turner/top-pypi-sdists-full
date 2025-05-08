# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lllll1lll_opy_, bstack11llll1l1ll_opy_, bstack11ll1l111l_opy_, bstack111ll1ll1l_opy_, bstack11l1l1l1l1l_opy_, bstack11l1l1ll1ll_opy_, bstack11l1l1l111l_opy_, bstack1l1ll1ll_opy_, bstack1l111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11l1ll1_opy_ import bstack111l11ll111_opy_
import bstack_utils.bstack1l11l1lll1_opy_ as bstack11l1lllll1_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack1l11ll11ll_opy_
import bstack_utils.accessibility as bstack1l1l1l11l_opy_
from bstack_utils.bstack11ll11ll11_opy_ import bstack11ll11ll11_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack111l1l1lll_opy_
bstack1111ll111ll_opy_ = bstack1l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨḇ")
logger = logging.getLogger(__name__)
class bstack111ll11l_opy_:
    bstack111l11l1ll1_opy_ = None
    bs_config = None
    bstack1l11111l_opy_ = None
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1llllll_opy_, stage=STAGE.bstack1111lll1_opy_)
    def launch(cls, bs_config, bstack1l11111l_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11111l_opy_ = bstack1l11111l_opy_
        try:
            cls.bstack1111lll1l1l_opy_()
            bstack11llll11l11_opy_ = bstack11lllll1lll_opy_(bs_config)
            bstack11llll1ll1l_opy_ = bstack11llll1l1ll_opy_(bs_config)
            data = bstack11l1lllll1_opy_.bstack1111lll11ll_opy_(bs_config, bstack1l11111l_opy_)
            config = {
                bstack1l1lll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧḈ"): (bstack11llll11l11_opy_, bstack11llll1ll1l_opy_),
                bstack1l1lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫḉ"): cls.default_headers()
            }
            response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"ࠫࡕࡕࡓࡕࠩḊ"), cls.request_url(bstack1l1lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬḋ")), data, config)
            if response.status_code != 200:
                bstack1lllll1111_opy_ = response.json()
                if bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧḌ")] == False:
                    cls.bstack1111ll11lll_opy_(bstack1lllll1111_opy_)
                    return
                cls.bstack1111ll1llll_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḍ")])
                cls.bstack1111ll1lll1_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḎ")])
                return None
            bstack1111ll11111_opy_ = cls.bstack1111lll111l_opy_(response)
            return bstack1111ll11111_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢḏ").format(str(error)))
            return None
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def stop(cls, bstack1111ll1111l_opy_=None):
        if not bstack1l11ll11ll_opy_.on() and not bstack1l1l1l11l_opy_.on():
            return
        if os.environ.get(bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḐ")) == bstack1l1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤḑ") or os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḒ")) == bstack1l1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦḓ"):
            logger.error(bstack1l1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪḔ"))
            return {
                bstack1l1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨḕ"): bstack1l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨḖ"),
                bstack1l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫḗ"): bstack1l1lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩḘ")
            }
        try:
            cls.bstack111l11l1ll1_opy_.shutdown()
            data = {
                bstack1l1lll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪḙ"): bstack1l1ll1ll_opy_()
            }
            if not bstack1111ll1111l_opy_ is None:
                data[bstack1l1lll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪḚ")] = [{
                    bstack1l1lll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧḛ"): bstack1l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭Ḝ"),
                    bstack1l1lll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩḝ"): bstack1111ll1111l_opy_
                }]
            config = {
                bstack1l1lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫḞ"): cls.default_headers()
            }
            bstack11ll111ll1l_opy_ = bstack1l1lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬḟ").format(os.environ[bstack1l1lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥḠ")])
            bstack1111ll1l1ll_opy_ = cls.request_url(bstack11ll111ll1l_opy_)
            response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"࠭ࡐࡖࡖࠪḡ"), bstack1111ll1l1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1lll_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨḢ"))
        except Exception as error:
            logger.error(bstack1l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧḣ") + str(error))
            return {
                bstack1l1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩḤ"): bstack1l1lll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩḥ"),
                bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬḦ"): str(error)
            }
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def bstack1111lll111l_opy_(cls, response):
        bstack1lllll1111_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll11111_opy_ = {}
        if bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠬࡰࡷࡵࠩḧ")) is None:
            os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪḨ")] = bstack1l1lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬḩ")
        else:
            os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬḪ")] = bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠩ࡭ࡻࡹ࠭ḫ"), bstack1l1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨḬ"))
        os.environ[bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḭ")] = bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḮ"), bstack1l1lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫḯ"))
        logger.info(bstack1l1lll_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬḰ") + os.getenv(bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ḱ")));
        if bstack1l11ll11ll_opy_.bstack1111lll11l1_opy_(cls.bs_config, cls.bstack1l11111l_opy_.get(bstack1l1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪḲ"), bstack1l1lll_opy_ (u"ࠪࠫḳ"))) is True:
            bstack111l11l1l11_opy_, build_hashed_id, bstack1111ll1l111_opy_ = cls.bstack1111ll1l1l1_opy_(bstack1lllll1111_opy_)
            if bstack111l11l1l11_opy_ != None and build_hashed_id != None:
                bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḴ")] = {
                    bstack1l1lll_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨḵ"): bstack111l11l1l11_opy_,
                    bstack1l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḶ"): build_hashed_id,
                    bstack1l1lll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫḷ"): bstack1111ll1l111_opy_
                }
            else:
                bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḸ")] = {}
        else:
            bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḹ")] = {}
        bstack1111lll1l11_opy_, build_hashed_id = cls.bstack1111ll11l1l_opy_(bstack1lllll1111_opy_)
        if bstack1111lll1l11_opy_ != None and build_hashed_id != None:
            bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪḺ")] = {
                bstack1l1lll_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨḻ"): bstack1111lll1l11_opy_,
                bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḼ"): build_hashed_id,
            }
        else:
            bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ḽ")] = {}
        if bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḾ")].get(bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḿ")) != None or bstack1111ll11111_opy_[bstack1l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṀ")].get(bstack1l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬṁ")) != None:
            cls.bstack1111ll11ll1_opy_(bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠫ࡯ࡽࡴࠨṂ")), bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṃ")))
        return bstack1111ll11111_opy_
    @classmethod
    def bstack1111ll1l1l1_opy_(cls, bstack1lllll1111_opy_):
        if bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")) == None:
            cls.bstack1111ll1llll_opy_()
            return [None, None, None]
        if bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧṅ")][bstack1l1lll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩṆ")] != True:
            cls.bstack1111ll1llll_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṇ")])
            return [None, None, None]
        logger.debug(bstack1l1lll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧṈ"))
        os.environ[bstack1l1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪṉ")] = bstack1l1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪṊ")
        if bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"࠭ࡪࡸࡶࠪṋ")):
            os.environ[bstack1l1lll_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫṌ")] = json.dumps({
                bstack1l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪṍ"): bstack11lllll1lll_opy_(cls.bs_config),
                bstack1l1lll_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫṎ"): bstack11llll1l1ll_opy_(cls.bs_config)
            })
        if bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬṏ")):
            os.environ[bstack1l1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪṐ")] = bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṑ")]
        if bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ṓ")].get(bstack1l1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṓ"), {}).get(bstack1l1lll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬṔ")):
            os.environ[bstack1l1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪṕ")] = str(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṖ")][bstack1l1lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṗ")][bstack1l1lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩṘ")])
        else:
            os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧṙ")] = bstack1l1lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧṚ")
        return [bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠨ࡬ࡺࡸࠬṛ")], bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṜ")], os.environ[bstack1l1lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫṝ")]]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, bstack1lllll1111_opy_):
        if bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṞ")) == None:
            cls.bstack1111ll1lll1_opy_()
            return [None, None]
        if bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṟ")][bstack1l1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧṠ")] != True:
            cls.bstack1111ll1lll1_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṡ")])
            return [None, None]
        if bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṢ")].get(bstack1l1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṣ")):
            logger.debug(bstack1l1lll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧṤ"))
            parsed = json.loads(os.getenv(bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬṥ"), bstack1l1lll_opy_ (u"ࠬࢁࡽࠨṦ")))
            capabilities = bstack11l1lllll1_opy_.bstack1111ll1ll11_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṧ")][bstack1l1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṨ")][bstack1l1lll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧṩ")], bstack1l1lll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧṪ"), bstack1l1lll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩṫ"))
            bstack1111lll1l11_opy_ = capabilities[bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩṬ")]
            os.environ[bstack1l1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪṭ")] = bstack1111lll1l11_opy_
            if bstack1l1lll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣṮ") in bstack1lllll1111_opy_ and bstack1lllll1111_opy_.get(bstack1l1lll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨṯ")) is None:
                parsed[bstack1l1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṰ")] = capabilities[bstack1l1lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪṱ")]
            os.environ[bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫṲ")] = json.dumps(parsed)
            scripts = bstack11l1lllll1_opy_.bstack1111ll1ll11_opy_(bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṳ")][bstack1l1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ṵ")][bstack1l1lll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧṵ")], bstack1l1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṶ"), bstack1l1lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩṷ"))
            bstack11ll11ll11_opy_.bstack111llll11_opy_(scripts)
            commands = bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṸ")][bstack1l1lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṹ")][bstack1l1lll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬṺ")].get(bstack1l1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧṻ"))
            bstack11ll11ll11_opy_.bstack11llll11l1l_opy_(commands)
            bstack11ll11ll11_opy_.store()
        return [bstack1111lll1l11_opy_, bstack1lllll1111_opy_[bstack1l1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨṼ")]]
    @classmethod
    def bstack1111ll1llll_opy_(cls, response=None):
        os.environ[bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬṽ")] = bstack1l1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ṿ")
        os.environ[bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ṿ")] = bstack1l1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨẀ")
        os.environ[bstack1l1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪẁ")] = bstack1l1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫẂ")
        os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬẃ")] = bstack1l1lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧẄ")
        os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩẅ")] = bstack1l1lll_opy_ (u"ࠤࡱࡹࡱࡲࠢẆ")
        cls.bstack1111ll11lll_opy_(response, bstack1l1lll_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥẇ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1lll1_opy_(cls, response=None):
        os.environ[bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩẈ")] = bstack1l1lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪẉ")
        os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫẊ")] = bstack1l1lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬẋ")
        os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẌ")] = bstack1l1lll_opy_ (u"ࠩࡱࡹࡱࡲࠧẍ")
        cls.bstack1111ll11lll_opy_(response, bstack1l1lll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥẎ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll11ll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨẏ")] = jwt
        os.environ[bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪẐ")] = build_hashed_id
    @classmethod
    def bstack1111ll11lll_opy_(cls, response=None, product=bstack1l1lll_opy_ (u"ࠨࠢẑ")):
        if response == None or response.get(bstack1l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧẒ")) == None:
            logger.error(product + bstack1l1lll_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥẓ"))
            return
        for error in response[bstack1l1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩẔ")]:
            bstack11ll11111l1_opy_ = error[bstack1l1lll_opy_ (u"ࠪ࡯ࡪࡿࠧẕ")]
            error_message = error[bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẖ")]
            if error_message:
                if bstack11ll11111l1_opy_ == bstack1l1lll_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦẗ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1lll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢẘ") + product + bstack1l1lll_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧẙ"))
    @classmethod
    def bstack1111lll1l1l_opy_(cls):
        if cls.bstack111l11l1ll1_opy_ is not None:
            return
        cls.bstack111l11l1ll1_opy_ = bstack111l11ll111_opy_(cls.bstack1111l1lll1l_opy_)
        cls.bstack111l11l1ll1_opy_.start()
    @classmethod
    def bstack111ll111ll_opy_(cls):
        if cls.bstack111l11l1ll1_opy_ is None:
            return
        cls.bstack111l11l1ll1_opy_.shutdown()
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def bstack1111l1lll1l_opy_(cls, bstack111l1l11l1_opy_, event_url=bstack1l1lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧẚ")):
        config = {
            bstack1l1lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪẛ"): cls.default_headers()
        }
        logger.debug(bstack1l1lll_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥẜ").format(bstack1l1lll_opy_ (u"ࠫ࠱ࠦࠧẝ").join([event[bstack1l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẞ")] for event in bstack111l1l11l1_opy_])))
        response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"࠭ࡐࡐࡕࡗࠫẟ"), cls.request_url(event_url), bstack111l1l11l1_opy_, config)
        bstack11llll111l1_opy_ = response.json()
    @classmethod
    def bstack11l1llll1_opy_(cls, bstack111l1l11l1_opy_, event_url=bstack1l1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭Ạ")):
        logger.debug(bstack1l1lll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣạ").format(bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ả")]))
        if not bstack11l1lllll1_opy_.bstack1111l1ll1ll_opy_(bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧả")]):
            logger.debug(bstack1l1lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤẤ").format(bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩấ")]))
            return
        bstack1ll1l11ll_opy_ = bstack11l1lllll1_opy_.bstack1111l1lllll_opy_(bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẦ")], bstack111l1l11l1_opy_.get(bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩầ")))
        if bstack1ll1l11ll_opy_ != None:
            if bstack111l1l11l1_opy_.get(bstack1l1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪẨ")) != None:
                bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫẩ")][bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨẪ")] = bstack1ll1l11ll_opy_
            else:
                bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩẫ")] = bstack1ll1l11ll_opy_
        if event_url == bstack1l1lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫẬ"):
            cls.bstack1111lll1l1l_opy_()
            logger.debug(bstack1l1lll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤậ").format(bstack111l1l11l1_opy_[bstack1l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẮ")]))
            cls.bstack111l11l1ll1_opy_.add(bstack111l1l11l1_opy_)
        elif event_url == bstack1l1lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ắ"):
            cls.bstack1111l1lll1l_opy_([bstack111l1l11l1_opy_], event_url)
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def bstack11lll11111_opy_(cls, logs):
        bstack1111ll11l11_opy_ = []
        for log in logs:
            bstack1111lll1111_opy_ = {
                bstack1l1lll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧẰ"): bstack1l1lll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬằ"),
                bstack1l1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẲ"): log[bstack1l1lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫẳ")],
                bstack1l1lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩẴ"): log[bstack1l1lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪẵ")],
                bstack1l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨẶ"): {},
                bstack1l1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪặ"): log[bstack1l1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫẸ")],
            }
            if bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẹ") in log:
                bstack1111lll1111_opy_[bstack1l1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẺ")] = log[bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẻ")]
            elif bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẼ") in log:
                bstack1111lll1111_opy_[bstack1l1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ")] = log[bstack1l1lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẾ")]
            bstack1111ll11l11_opy_.append(bstack1111lll1111_opy_)
        cls.bstack11l1llll1_opy_({
            bstack1l1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧế"): bstack1l1lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨỀ"),
            bstack1l1lll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪề"): bstack1111ll11l11_opy_
        })
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def bstack1111ll111l1_opy_(cls, steps):
        bstack1111ll1ll1l_opy_ = []
        for step in steps:
            bstack1111l1llll1_opy_ = {
                bstack1l1lll_opy_ (u"࠭࡫ࡪࡰࡧࠫỂ"): bstack1l1lll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪể"),
                bstack1l1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧỄ"): step[bstack1l1lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨễ")],
                bstack1l1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ệ"): step[bstack1l1lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧệ")],
                bstack1l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ỉ"): step[bstack1l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧỉ")],
                bstack1l1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩỊ"): step[bstack1l1lll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪị")]
            }
            if bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩỌ") in step:
                bstack1111l1llll1_opy_[bstack1l1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪọ")] = step[bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỎ")]
            elif bstack1l1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬỏ") in step:
                bstack1111l1llll1_opy_[bstack1l1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ố")] = step[bstack1l1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧố")]
            bstack1111ll1ll1l_opy_.append(bstack1111l1llll1_opy_)
        cls.bstack11l1llll1_opy_({
            bstack1l1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬỒ"): bstack1l1lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ồ"),
            bstack1l1lll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨỔ"): bstack1111ll1ll1l_opy_
        })
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lllll111l_opy_, stage=STAGE.bstack1111lll1_opy_)
    def bstack1l1ll11l11_opy_(cls, screenshot):
        cls.bstack11l1llll1_opy_({
            bstack1l1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨổ"): bstack1l1lll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩỖ"),
            bstack1l1lll_opy_ (u"࠭࡬ࡰࡩࡶࠫỗ"): [{
                bstack1l1lll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬỘ"): bstack1l1lll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪộ"),
                bstack1l1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬỚ"): datetime.datetime.utcnow().isoformat() + bstack1l1lll_opy_ (u"ࠪ࡞ࠬớ"),
                bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬỜ"): screenshot[bstack1l1lll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫờ")],
                bstack1l1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ở"): screenshot[bstack1l1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧở")]
            }]
        }, event_url=bstack1l1lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ỡ"))
    @classmethod
    @bstack111ll1ll1l_opy_(class_method=True)
    def bstack1l1ll111l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1llll1_opy_({
            bstack1l1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ỡ"): bstack1l1lll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧỢ"),
            bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ợ"): {
                bstack1l1lll_opy_ (u"ࠧࡻࡵࡪࡦࠥỤ"): cls.current_test_uuid(),
                bstack1l1lll_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧụ"): cls.bstack11l111111l_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1111ll1_opy_(cls, event: str, bstack111l1l11l1_opy_: bstack111l1l1lll_opy_):
        bstack111ll11l11_opy_ = {
            bstack1l1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫỦ"): event,
            bstack111l1l11l1_opy_.bstack111ll11l1l_opy_(): bstack111l1l11l1_opy_.bstack111lll1l1l_opy_(event)
        }
        cls.bstack11l1llll1_opy_(bstack111ll11l11_opy_)
        result = getattr(bstack111l1l11l1_opy_, bstack1l1lll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨủ"), None)
        if event == bstack1l1lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪỨ"):
            threading.current_thread().bstackTestMeta = {bstack1l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪứ"): bstack1l1lll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬỪ")}
        elif event == bstack1l1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧừ"):
            threading.current_thread().bstackTestMeta = {bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ử"): getattr(result, bstack1l1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧử"), bstack1l1lll_opy_ (u"ࠨࠩỮ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ữ"), None) is None or os.environ[bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧỰ")] == bstack1l1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤự")) and (os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪỲ"), None) is None or os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫỳ")] == bstack1l1lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧỴ")):
            return False
        return True
    @staticmethod
    def bstack1111l1lll11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111ll11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧỵ"): bstack1l1lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬỶ"),
            bstack1l1lll_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭ỷ"): bstack1l1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩỸ")
        }
        if os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩỹ"), None):
            headers[bstack1l1lll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭Ỻ")] = bstack1l1lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪỻ").format(os.environ[bstack1l1lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧỼ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1lll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨỽ").format(bstack1111ll111ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1lll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧỾ"), None)
    @staticmethod
    def bstack11l111111l_opy_(driver):
        return {
            bstack11l1l1l1l1l_opy_(): bstack11l1l1ll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1111ll1l11l_opy_(exception_info, report):
        return [{bstack1l1lll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧỿ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll1111_opy_(typename):
        if bstack1l1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣἀ") in typename:
            return bstack1l1lll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢἁ")
        return bstack1l1lll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣἂ")