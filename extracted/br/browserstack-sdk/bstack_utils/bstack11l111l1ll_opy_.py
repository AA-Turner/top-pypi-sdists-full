# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll1ll111_opy_, bstack11llll11ll1_opy_, bstack1lll1ll11l_opy_, bstack111l11l1ll_opy_, bstack11l1lll1l11_opy_, bstack11l1llll11l_opy_, bstack11l11ll1ll1_opy_, bstack11ll11l1ll_opy_, bstack1llll11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11ll1l1_opy_ import bstack111l11lll11_opy_
import bstack_utils.bstack1lll11llll_opy_ as bstack11l1ll11l_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack1llll1ll1l_opy_
import bstack_utils.accessibility as bstack11l1lll11_opy_
from bstack_utils.bstack1l1111l1_opy_ import bstack1l1111l1_opy_
from bstack_utils.bstack11l111l111_opy_ import bstack111l11l1l1_opy_
bstack1111ll1l1ll_opy_ = bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬḋ")
logger = logging.getLogger(__name__)
class bstack11l1lll1ll_opy_:
    bstack111l11ll1l1_opy_ = None
    bs_config = None
    bstack11l11llll_opy_ = None
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1ll11l1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def launch(cls, bs_config, bstack11l11llll_opy_):
        cls.bs_config = bs_config
        cls.bstack11l11llll_opy_ = bstack11l11llll_opy_
        try:
            cls.bstack1111ll1lll1_opy_()
            bstack11lllll1l11_opy_ = bstack11lll1ll111_opy_(bs_config)
            bstack11llll1ll11_opy_ = bstack11llll11ll1_opy_(bs_config)
            data = bstack11l1ll11l_opy_.bstack1111ll1l11l_opy_(bs_config, bstack11l11llll_opy_)
            config = {
                bstack11lll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫḌ"): (bstack11lllll1l11_opy_, bstack11llll1ll11_opy_),
                bstack11lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨḍ"): cls.default_headers()
            }
            response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠨࡒࡒࡗ࡙࠭Ḏ"), cls.request_url(bstack11lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩḏ")), data, config)
            if response.status_code != 200:
                bstack1ll1llll11_opy_ = response.json()
                if bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫḐ")] == False:
                    cls.bstack1111lll11ll_opy_(bstack1ll1llll11_opy_)
                    return
                cls.bstack1111ll1l111_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḑ")])
                cls.bstack1111ll11l11_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḒ")])
                return None
            bstack1111lll11l1_opy_ = cls.bstack1111lll111l_opy_(response)
            return bstack1111lll11l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦḓ").format(str(error)))
            return None
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def stop(cls, bstack1111l1ll1l1_opy_=None):
        if not bstack1llll1ll1l_opy_.on() and not bstack11l1lll11_opy_.on():
            return
        if os.environ.get(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫḔ")) == bstack11lll_opy_ (u"ࠣࡰࡸࡰࡱࠨḕ") or os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧḖ")) == bstack11lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣḗ"):
            logger.error(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧḘ"))
            return {
                bstack11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬḙ"): bstack11lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬḚ"),
                bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨḛ"): bstack11lll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭Ḝ")
            }
        try:
            cls.bstack111l11ll1l1_opy_.shutdown()
            data = {
                bstack11lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧḝ"): bstack11ll11l1ll_opy_()
            }
            if not bstack1111l1ll1l1_opy_ is None:
                data[bstack11lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧḞ")] = [{
                    bstack11lll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫḟ"): bstack11lll_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪḠ"),
                    bstack11lll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ḡ"): bstack1111l1ll1l1_opy_
                }]
            config = {
                bstack11lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨḢ"): cls.default_headers()
            }
            bstack11ll1111l1l_opy_ = bstack11lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩḣ").format(os.environ[bstack11lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢḤ")])
            bstack1111l1llll1_opy_ = cls.request_url(bstack11ll1111l1l_opy_)
            response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠪࡔ࡚࡚ࠧḥ"), bstack1111l1llll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lll_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥḦ"))
        except Exception as error:
            logger.error(bstack11lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤḧ") + str(error))
            return {
                bstack11lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ḩ"): bstack11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ḩ"),
                bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩḪ"): str(error)
            }
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def bstack1111lll111l_opy_(cls, response):
        bstack1ll1llll11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111lll11l1_opy_ = {}
        if bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠩ࡭ࡻࡹ࠭ḫ")) is None:
            os.environ[bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḬ")] = bstack11lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩḭ")
        else:
            os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩḮ")] = bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"࠭ࡪࡸࡶࠪḯ"), bstack11lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬḰ"))
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ḱ")] = bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫḲ"), bstack11lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨḳ"))
        logger.info(bstack11lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩḴ") + os.getenv(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḵ")));
        if bstack1llll1ll1l_opy_.bstack1111ll1111l_opy_(cls.bs_config, cls.bstack11l11llll_opy_.get(bstack11lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧḶ"), bstack11lll_opy_ (u"ࠧࠨḷ"))) is True:
            bstack111l11l1111_opy_, build_hashed_id, bstack1111l1ll11l_opy_ = cls.bstack1111ll11lll_opy_(bstack1ll1llll11_opy_)
            if bstack111l11l1111_opy_ != None and build_hashed_id != None:
                bstack1111lll11l1_opy_[bstack11lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḸ")] = {
                    bstack11lll_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬḹ"): bstack111l11l1111_opy_,
                    bstack11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḺ"): build_hashed_id,
                    bstack11lll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨḻ"): bstack1111l1ll11l_opy_
                }
            else:
                bstack1111lll11l1_opy_[bstack11lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḼ")] = {}
        else:
            bstack1111lll11l1_opy_[bstack11lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḽ")] = {}
        bstack1111ll111ll_opy_, build_hashed_id = cls.bstack1111lll1111_opy_(bstack1ll1llll11_opy_)
        if bstack1111ll111ll_opy_ != None and build_hashed_id != None:
            bstack1111lll11l1_opy_[bstack11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḾ")] = {
                bstack11lll_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬḿ"): bstack1111ll111ll_opy_,
                bstack11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṀ"): build_hashed_id,
            }
        else:
            bstack1111lll11l1_opy_[bstack11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṁ")] = {}
        if bstack1111lll11l1_opy_[bstack11lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṂ")].get(bstack11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧṃ")) != None or bstack1111lll11l1_opy_[bstack11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")].get(bstack11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩṅ")) != None:
            cls.bstack1111l1lll11_opy_(bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠨ࡬ࡺࡸࠬṆ")), bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṇ")))
        return bstack1111lll11l1_opy_
    @classmethod
    def bstack1111ll11lll_opy_(cls, bstack1ll1llll11_opy_):
        if bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṈ")) == None:
            cls.bstack1111ll1l111_opy_()
            return [None, None, None]
        if bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫṉ")][bstack11lll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭Ṋ")] != True:
            cls.bstack1111ll1l111_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ṋ")])
            return [None, None, None]
        logger.debug(bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫṌ"))
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧṍ")] = bstack11lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧṎ")
        if bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠪ࡮ࡼࡺࠧṏ")):
            os.environ[bstack11lll_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨṐ")] = json.dumps({
                bstack11lll_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧṑ"): bstack11lll1ll111_opy_(cls.bs_config),
                bstack11lll_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨṒ"): bstack11llll11ll1_opy_(cls.bs_config)
            })
        if bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩṓ")):
            os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧṔ")] = bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṕ")]
        if bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪṖ")].get(bstack11lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṗ"), {}).get(bstack11lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩṘ")):
            os.environ[bstack11lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧṙ")] = str(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧṚ")][bstack11lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩṛ")][bstack11lll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ṝ")])
        else:
            os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫṝ")] = bstack11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤṞ")
        return [bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠬࡰࡷࡵࠩṟ")], bstack1ll1llll11_opy_[bstack11lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨṠ")], os.environ[bstack11lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨṡ")]]
    @classmethod
    def bstack1111lll1111_opy_(cls, bstack1ll1llll11_opy_):
        if bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṢ")) == None:
            cls.bstack1111ll11l11_opy_()
            return [None, None]
        if bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṣ")][bstack11lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫṤ")] != True:
            cls.bstack1111ll11l11_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṥ")])
            return [None, None]
        if bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṦ")].get(bstack11lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṧ")):
            logger.debug(bstack11lll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫṨ"))
            parsed = json.loads(os.getenv(bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩṩ"), bstack11lll_opy_ (u"ࠩࡾࢁࠬṪ")))
            capabilities = bstack11l1ll11l_opy_.bstack1111l1ll1ll_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṫ")][bstack11lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṬ")][bstack11lll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫṭ")], bstack11lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫṮ"), bstack11lll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ṯ"))
            bstack1111ll111ll_opy_ = capabilities[bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭Ṱ")]
            os.environ[bstack11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧṱ")] = bstack1111ll111ll_opy_
            if bstack11lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧṲ") in bstack1ll1llll11_opy_ and bstack1ll1llll11_opy_.get(bstack11lll_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥṳ")) is None:
                parsed[bstack11lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ṵ")] = capabilities[bstack11lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧṵ")]
            os.environ[bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨṶ")] = json.dumps(parsed)
            scripts = bstack11l1ll11l_opy_.bstack1111l1ll1ll_opy_(bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṷ")][bstack11lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṸ")][bstack11lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫṹ")], bstack11lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩṺ"), bstack11lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ṻ"))
            bstack1l1111l1_opy_.bstack11ll11llll_opy_(scripts)
            commands = bstack1ll1llll11_opy_[bstack11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṽ")][bstack11lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṽ")][bstack11lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩṾ")].get(bstack11lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫṿ"))
            bstack1l1111l1_opy_.bstack11llll1ll1l_opy_(commands)
            bstack1l1111l1_opy_.store()
        return [bstack1111ll111ll_opy_, bstack1ll1llll11_opy_[bstack11lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬẀ")]]
    @classmethod
    def bstack1111ll1l111_opy_(cls, response=None):
        os.environ[bstack11lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩẁ")] = bstack11lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪẂ")
        os.environ[bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪẃ")] = bstack11lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬẄ")
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧẅ")] = bstack11lll_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨẆ")
        os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩẇ")] = bstack11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤẈ")
        os.environ[bstack11lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ẉ")] = bstack11lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦẊ")
        cls.bstack1111lll11ll_opy_(response, bstack11lll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢẋ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll11l11_opy_(cls, response=None):
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ẍ")] = bstack11lll_opy_ (u"ࠩࡱࡹࡱࡲࠧẍ")
        os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨẎ")] = bstack11lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩẏ")
        os.environ[bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩẐ")] = bstack11lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫẑ")
        cls.bstack1111lll11ll_opy_(response, bstack11lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢẒ"))
        return [None, None, None]
    @classmethod
    def bstack1111l1lll11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẓ")] = jwt
        os.environ[bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧẔ")] = build_hashed_id
    @classmethod
    def bstack1111lll11ll_opy_(cls, response=None, product=bstack11lll_opy_ (u"ࠥࠦẕ")):
        if response == None or response.get(bstack11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫẖ")) == None:
            logger.error(product + bstack11lll_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢẗ"))
            return
        for error in response[bstack11lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ẘ")]:
            bstack11l11lll111_opy_ = error[bstack11lll_opy_ (u"ࠧ࡬ࡧࡼࠫẙ")]
            error_message = error[bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẚ")]
            if error_message:
                if bstack11l11lll111_opy_ == bstack11lll_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣẛ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lll_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦẜ") + product + bstack11lll_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤẝ"))
    @classmethod
    def bstack1111ll1lll1_opy_(cls):
        if cls.bstack111l11ll1l1_opy_ is not None:
            return
        cls.bstack111l11ll1l1_opy_ = bstack111l11lll11_opy_(cls.bstack1111ll11ll1_opy_)
        cls.bstack111l11ll1l1_opy_.start()
    @classmethod
    def bstack111ll1l1ll_opy_(cls):
        if cls.bstack111l11ll1l1_opy_ is None:
            return
        cls.bstack111l11ll1l1_opy_.shutdown()
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def bstack1111ll11ll1_opy_(cls, bstack111ll1ll11_opy_, event_url=bstack11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫẞ")):
        config = {
            bstack11lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧẟ"): cls.default_headers()
        }
        logger.debug(bstack11lll_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢẠ").format(bstack11lll_opy_ (u"ࠨ࠮ࠣࠫạ").join([event[bstack11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ả")] for event in bstack111ll1ll11_opy_])))
        response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨả"), cls.request_url(event_url), bstack111ll1ll11_opy_, config)
        bstack11lll1llll1_opy_ = response.json()
    @classmethod
    def bstack11111111_opy_(cls, bstack111ll1ll11_opy_, event_url=bstack11lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪẤ")):
        logger.debug(bstack11lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧấ").format(bstack111ll1ll11_opy_[bstack11lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẦ")]))
        if not bstack11l1ll11l_opy_.bstack1111ll1ll11_opy_(bstack111ll1ll11_opy_[bstack11lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫầ")]):
            logger.debug(bstack11lll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨẨ").format(bstack111ll1ll11_opy_[bstack11lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ẩ")]))
            return
        bstack1l11lll1l_opy_ = bstack11l1ll11l_opy_.bstack1111ll1llll_opy_(bstack111ll1ll11_opy_[bstack11lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẪ")], bstack111ll1ll11_opy_.get(bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ẫ")))
        if bstack1l11lll1l_opy_ != None:
            if bstack111ll1ll11_opy_.get(bstack11lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧẬ")) != None:
                bstack111ll1ll11_opy_[bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨậ")][bstack11lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬẮ")] = bstack1l11lll1l_opy_
            else:
                bstack111ll1ll11_opy_[bstack11lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ắ")] = bstack1l11lll1l_opy_
        if event_url == bstack11lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨẰ"):
            cls.bstack1111ll1lll1_opy_()
            logger.debug(bstack11lll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨằ").format(bstack111ll1ll11_opy_[bstack11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẲ")]))
            cls.bstack111l11ll1l1_opy_.add(bstack111ll1ll11_opy_)
        elif event_url == bstack11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪẳ"):
            cls.bstack1111ll11ll1_opy_([bstack111ll1ll11_opy_], event_url)
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def bstack11l1l1ll11_opy_(cls, logs):
        bstack1111ll11111_opy_ = []
        for log in logs:
            bstack1111ll1ll1l_opy_ = {
                bstack11lll_opy_ (u"࠭࡫ࡪࡰࡧࠫẴ"): bstack11lll_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩẵ"),
                bstack11lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧẶ"): log[bstack11lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨặ")],
                bstack11lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ẹ"): log[bstack11lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧẹ")],
                bstack11lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬẺ"): {},
                bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẻ"): log[bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨẼ")],
            }
            if bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ") in log:
                bstack1111ll1ll1l_opy_[bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẾ")] = log[bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪế")]
            elif bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỀ") in log:
                bstack1111ll1ll1l_opy_[bstack11lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬề")] = log[bstack11lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ể")]
            bstack1111ll11111_opy_.append(bstack1111ll1ll1l_opy_)
        cls.bstack11111111_opy_({
            bstack11lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫể"): bstack11lll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬỄ"),
            bstack11lll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧễ"): bstack1111ll11111_opy_
        })
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def bstack1111l1lll1l_opy_(cls, steps):
        bstack1111ll11l1l_opy_ = []
        for step in steps:
            bstack1111ll111l1_opy_ = {
                bstack11lll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨỆ"): bstack11lll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧệ"),
                bstack11lll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫỈ"): step[bstack11lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬỉ")],
                bstack11lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪỊ"): step[bstack11lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫị")],
                bstack11lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪỌ"): step[bstack11lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫọ")],
                bstack11lll_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Ỏ"): step[bstack11lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧỏ")]
            }
            if bstack11lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ố") in step:
                bstack1111ll111l1_opy_[bstack11lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧố")] = step[bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨỒ")]
            elif bstack11lll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩồ") in step:
                bstack1111ll111l1_opy_[bstack11lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỔ")] = step[bstack11lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫổ")]
            bstack1111ll11l1l_opy_.append(bstack1111ll111l1_opy_)
        cls.bstack11111111_opy_({
            bstack11lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩỖ"): bstack11lll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪỗ"),
            bstack11lll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬỘ"): bstack1111ll11l1l_opy_
        })
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11lllll1_opy_, stage=STAGE.bstack11l111ll_opy_)
    def bstack1l1llll11_opy_(cls, screenshot):
        cls.bstack11111111_opy_({
            bstack11lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬộ"): bstack11lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ớ"),
            bstack11lll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨớ"): [{
                bstack11lll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩỜ"): bstack11lll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧờ"),
                bstack11lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩỞ"): datetime.datetime.utcnow().isoformat() + bstack11lll_opy_ (u"࡛ࠧࠩở"),
                bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩỠ"): screenshot[bstack11lll_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨỡ")],
                bstack11lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỢ"): screenshot[bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫợ")]
            }]
        }, event_url=bstack11lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪỤ"))
    @classmethod
    @bstack111l11l1ll_opy_(class_method=True)
    def bstack1ll11l1l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11111111_opy_({
            bstack11lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪụ"): bstack11lll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫỦ"),
            bstack11lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪủ"): {
                bstack11lll_opy_ (u"ࠤࡸࡹ࡮ࡪࠢỨ"): cls.current_test_uuid(),
                bstack11lll_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤứ"): cls.bstack11l11111ll_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1111l11_opy_(cls, event: str, bstack111ll1ll11_opy_: bstack111l11l1l1_opy_):
        bstack111l11ll1l_opy_ = {
            bstack11lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨỪ"): event,
            bstack111ll1ll11_opy_.bstack111l11l111_opy_(): bstack111ll1ll11_opy_.bstack111ll11lll_opy_(event)
        }
        cls.bstack11111111_opy_(bstack111l11ll1l_opy_)
        result = getattr(bstack111ll1ll11_opy_, bstack11lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬừ"), None)
        if event == bstack11lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧỬ"):
            threading.current_thread().bstackTestMeta = {bstack11lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧử"): bstack11lll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩỮ")}
        elif event == bstack11lll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫữ"):
            threading.current_thread().bstackTestMeta = {bstack11lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪỰ"): getattr(result, bstack11lll_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫự"), bstack11lll_opy_ (u"ࠬ࠭Ỳ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỳ"), None) is None or os.environ[bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫỴ")] == bstack11lll_opy_ (u"ࠣࡰࡸࡰࡱࠨỵ")) and (os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧỶ"), None) is None or os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨỷ")] == bstack11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤỸ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1lll1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫỹ"): bstack11lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩỺ"),
            bstack11lll_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪỻ"): bstack11lll_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ỽ")
        }
        if os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ỽ"), None):
            headers[bstack11lll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪỾ")] = bstack11lll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧỿ").format(os.environ[bstack11lll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤἀ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11lll_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬἁ").format(bstack1111ll1l1ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lll_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫἂ"), None)
    @staticmethod
    def bstack11l11111ll_opy_(driver):
        return {
            bstack11l1lll1l11_opy_(): bstack11l1llll11l_opy_(driver)
        }
    @staticmethod
    def bstack1111l1lllll_opy_(exception_info, report):
        return [{bstack11lll_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫἃ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111l1llll_opy_(typename):
        if bstack11lll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧἄ") in typename:
            return bstack11lll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦἅ")
        return bstack11lll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧἆ")