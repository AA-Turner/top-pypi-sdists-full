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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l11l1ll_opy_, bstack11l1l11ll11_opy_, bstack1l1ll11111_opy_, error_handler, bstack111l1llll1l_opy_, bstack111l1l11l1l_opy_, bstack111ll11l111_opy_, bstack1111l11l1_opy_, bstack111111lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llll1111l11_opy_ import bstack1llll1111lll_opy_
import bstack_utils.bstack111ll1llll_opy_ as bstack11l11ll111_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1lll11ll11_opy_
import bstack_utils.accessibility as bstack1l11l1l111_opy_
from bstack_utils.bstack1l1111l1ll_opy_ import bstack1l1111l1ll_opy_
from bstack_utils.bstack1111ll1lll_opy_ import bstack111111111l_opy_
from bstack_utils.constants import bstack1ll1lll111_opy_
bstack1lll11ll1l11_opy_ = bstack1l1111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭∴")
logger = logging.getLogger(__name__)
class bstack11l11111l_opy_:
    bstack1llll1111l11_opy_ = None
    bs_config = None
    bstack11ll111ll_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l111lll1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def launch(cls, bs_config, bstack11ll111ll_opy_):
        cls.bs_config = bs_config
        cls.bstack11ll111ll_opy_ = bstack11ll111ll_opy_
        try:
            cls.bstack1lll11lll1l1_opy_()
            bstack11l1l1ll1ll_opy_ = bstack11l1l11l1ll_opy_(bs_config)
            bstack11l1l1l111l_opy_ = bstack11l1l11ll11_opy_(bs_config)
            data = bstack11l11ll111_opy_.bstack1lll1l111l11_opy_(bs_config, bstack11ll111ll_opy_)
            config = {
                bstack1l1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ∵"): (bstack11l1l1ll1ll_opy_, bstack11l1l1l111l_opy_),
                bstack1l1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ∶"): cls.default_headers()
            }
            response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ∷"), cls.request_url(bstack1l1111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪ∸")), data, config)
            if response.status_code != 200:
                bstack1ll11l1l1_opy_ = response.json()
                if bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ∹")] == False:
                    cls.bstack1lll1l111ll1_opy_(bstack1ll11l1l1_opy_)
                    return
                cls.bstack1lll1l11111l_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ∺")])
                cls.bstack1lll11lll11l_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭∻")])
                return None
            bstack1lll11ll111l_opy_ = cls.bstack1lll11llllll_opy_(response)
            return bstack1lll11ll111l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧ∼").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l111l11ll_opy_, stage=STAGE.bstack1111lll11_opy_)
    def stop(cls, bstack1lll11ll1l1l_opy_=None):
        if not bstack1lll11ll11_opy_.on() and not bstack1l11l1l111_opy_.on():
            return
        if os.environ.get(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ∽")) == bstack1l1111_opy_ (u"ࠤࡱࡹࡱࡲࠢ∾") or os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ∿")) == bstack1l1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ≀"):
            logger.error(bstack1l1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ≁"))
            return {
                bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭≂"): bstack1l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭≃"),
                bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ≄"): bstack1l1111_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧ≅")
            }
        try:
            cls.bstack1llll1111l11_opy_.shutdown()
            data = {
                bstack1l1111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ≆"): bstack1111l11l1_opy_()
            }
            if not bstack1lll11ll1l1l_opy_ is None:
                data[bstack1l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ≇")] = [{
                    bstack1l1111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ≈"): bstack1l1111_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ≉"),
                    bstack1l1111_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ≊"): bstack1lll11ll1l1l_opy_
                }]
            config = {
                bstack1l1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ≋"): cls.default_headers()
            }
            bstack11l1l11111l_opy_ = bstack1l1111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ≌").format(os.environ[bstack1l1111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ≍")])
            bstack1lll11ll11l1_opy_ = cls.request_url(bstack11l1l11111l_opy_)
            response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠫࡕ࡛ࡔࠨ≎"), bstack1lll11ll11l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1111_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦ≏"))
        except Exception as error:
            logger.error(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ≐") + str(error))
            return {
                bstack1l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ≑"): bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ≒"),
                bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ≓"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11llllll_opy_(cls, response):
        bstack1ll11l1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll11ll111l_opy_ = {}
        if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠪ࡮ࡼࡺࠧ≔")) is None:
            os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ≕")] = bstack1l1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ≖")
        else:
            os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ≗")] = bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠧ࡫ࡹࡷࠫ≘"), bstack1l1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭≙"))
        os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ≚")] = bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ≛"), bstack1l1111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ≜"))
        logger.info(bstack1l1111_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ≝") + os.getenv(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ≞")));
        if bstack1lll11ll11_opy_.bstack1lll11lllll1_opy_(cls.bs_config, cls.bstack11ll111ll_opy_.get(bstack1l1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ≟"), bstack1l1111_opy_ (u"ࠨࠩ≠"))) is True:
            bstack1lll1llll1l1_opy_, build_hashed_id, bstack1lll1l11l11l_opy_ = cls.bstack1lll11lll111_opy_(bstack1ll11l1l1_opy_)
            if bstack1lll1llll1l1_opy_ != None and build_hashed_id != None:
                bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ≡")] = {
                    bstack1l1111_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭≢"): bstack1lll1llll1l1_opy_,
                    bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭≣"): build_hashed_id,
                    bstack1l1111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ≤"): bstack1lll1l11l11l_opy_
                }
            else:
                bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭≥")] = {}
        else:
            bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ≦")] = {}
        bstack1lll1l111l1l_opy_, build_hashed_id = cls.bstack1lll11ll1111_opy_(bstack1ll11l1l1_opy_)
        if bstack1lll1l111l1l_opy_ != None and build_hashed_id != None:
            bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ≧")] = {
                bstack1l1111_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭≨"): bstack1lll1l111l1l_opy_,
                bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ≩"): build_hashed_id,
            }
        else:
            bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ≪")] = {}
        if bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ≫")].get(bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ≬")) != None or bstack1lll11ll111l_opy_[bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ≭")].get(bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ≮")) != None:
            cls.bstack1lll11ll1ll1_opy_(bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠩ࡭ࡻࡹ࠭≯")), bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ≰")))
        return bstack1lll11ll111l_opy_
    @classmethod
    def bstack1lll11lll111_opy_(cls, bstack1ll11l1l1_opy_):
        if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ≱")) == None:
            cls.bstack1lll1l11111l_opy_()
            return [None, None, None]
        if bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ≲")][bstack1l1111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ≳")] != True:
            cls.bstack1lll1l11111l_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ≴")])
            return [None, None, None]
        logger.debug(bstack1l1111_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ≵").format(bstack1ll1lll111_opy_))
        os.environ[bstack1l1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ≶")] = bstack1l1111_opy_ (u"ࠪࡸࡷࡻࡥࠨ≷")
        if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠫ࡯ࡽࡴࠨ≸")):
            os.environ[bstack1l1111_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ≹")] = json.dumps({
                bstack1l1111_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ≺"): bstack11l1l11l1ll_opy_(cls.bs_config),
                bstack1l1111_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ≻"): bstack11l1l11ll11_opy_(cls.bs_config)
            })
        if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ≼")):
            os.environ[bstack1l1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ≽")] = bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ≾")]
        if bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ≿")].get(bstack1l1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⊀"), {}).get(bstack1l1111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⊁")):
            os.environ[bstack1l1111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⊂")] = str(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⊃")][bstack1l1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⊄")][bstack1l1111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⊅")])
        else:
            os.environ[bstack1l1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⊆")] = bstack1l1111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⊇")
        return [bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"࠭ࡪࡸࡶࠪ⊈")], bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⊉")], os.environ[bstack1l1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⊊")]]
    @classmethod
    def bstack1lll11ll1111_opy_(cls, bstack1ll11l1l1_opy_):
        if bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⊋")) == None:
            cls.bstack1lll11lll11l_opy_()
            return [None, None]
        if bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⊌")][bstack1l1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⊍")] != True:
            cls.bstack1lll11lll11l_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⊎")])
            return [None, None]
        if bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⊏")].get(bstack1l1111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⊐")):
            logger.debug(bstack1l1111_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ⊑"))
            parsed = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⊒"), bstack1l1111_opy_ (u"ࠪࡿࢂ࠭⊓")))
            capabilities = bstack11l11ll111_opy_.bstack1lll11llll11_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⊔")][bstack1l1111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⊕")][bstack1l1111_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ⊖")], bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⊗"), bstack1l1111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ⊘"))
            bstack1lll1l111l1l_opy_ = capabilities[bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ⊙")]
            os.environ[bstack1l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⊚")] = bstack1lll1l111l1l_opy_
            if bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ⊛") in bstack1ll11l1l1_opy_ and bstack1ll11l1l1_opy_.get(bstack1l1111_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ⊜")) is None:
                parsed[bstack1l1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⊝")] = capabilities[bstack1l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⊞")]
            os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⊟")] = json.dumps(parsed)
            scripts = bstack11l11ll111_opy_.bstack1lll11llll11_opy_(bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⊠")][bstack1l1111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⊡")][bstack1l1111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ⊢")], bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⊣"), bstack1l1111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧ⊤"))
            bstack1l1111l1ll_opy_.bstack1l1l11lll1_opy_(scripts)
            commands = bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⊥")][bstack1l1111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⊦")][bstack1l1111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪ⊧")].get(bstack1l1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ⊨"))
            bstack1l1111l1ll_opy_.bstack11l1ll11lll_opy_(commands)
            bstack11l1ll1111l_opy_ = capabilities.get(bstack1l1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⊩"))
            bstack1l1111l1ll_opy_.bstack11l1l1111ll_opy_(bstack11l1ll1111l_opy_)
            bstack1l1111l1ll_opy_.store()
        return [bstack1lll1l111l1l_opy_, bstack1ll11l1l1_opy_[bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⊪")]]
    @classmethod
    def bstack1lll1l11111l_opy_(cls, response=None):
        os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⊫")] = bstack1l1111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⊬")
        os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⊭")] = bstack1l1111_opy_ (u"ࠩࡱࡹࡱࡲࠧ⊮")
        os.environ[bstack1l1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ⊯")] = bstack1l1111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ⊰")
        os.environ[bstack1l1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ⊱")] = bstack1l1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⊲")
        os.environ[bstack1l1111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⊳")] = bstack1l1111_opy_ (u"ࠣࡰࡸࡰࡱࠨ⊴")
        cls.bstack1lll1l111ll1_opy_(response, bstack1l1111_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ⊵"))
        return [None, None, None]
    @classmethod
    def bstack1lll11lll11l_opy_(cls, response=None):
        os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⊶")] = bstack1l1111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⊷")
        os.environ[bstack1l1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⊸")] = bstack1l1111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⊹")
        os.environ[bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⊺")] = bstack1l1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭⊻")
        cls.bstack1lll1l111ll1_opy_(response, bstack1l1111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ⊼"))
        return [None, None, None]
    @classmethod
    def bstack1lll11ll1ll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⊽")] = jwt
        os.environ[bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⊾")] = build_hashed_id
    @classmethod
    def bstack1lll1l111ll1_opy_(cls, response=None, product=bstack1l1111_opy_ (u"ࠧࠨ⊿")):
        if response == None or response.get(bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭⋀")) == None:
            logger.error(product + bstack1l1111_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤ⋁"))
            return
        for error in response[bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ⋂")]:
            bstack1111lll1lll_opy_ = error[bstack1l1111_opy_ (u"ࠩ࡮ࡩࡾ࠭⋃")]
            error_message = error[bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⋄")]
            if error_message:
                if bstack1111lll1lll_opy_ == bstack1l1111_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥ⋅"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1111_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨ⋆") + product + bstack1l1111_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ⋇"))
    @classmethod
    def bstack1lll11lll1l1_opy_(cls):
        if cls.bstack1llll1111l11_opy_ is not None:
            return
        cls.bstack1llll1111l11_opy_ = bstack1llll1111lll_opy_(cls.bstack1lll1l1111ll_opy_)
        cls.bstack1llll1111l11_opy_.start()
    @classmethod
    def bstack1111l111l1_opy_(cls):
        if cls.bstack1llll1111l11_opy_ is None:
            return
        cls.bstack1llll1111l11_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1l1111ll_opy_(cls, bstack11111l11ll_opy_, event_url=bstack1l1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⋈")):
        config = {
            bstack1l1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⋉"): cls.default_headers()
        }
        logger.debug(bstack1l1111_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ⋊").format(bstack1l1111_opy_ (u"ࠪ࠰ࠥ࠭⋋").join([event[bstack1l1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⋌")] for event in bstack11111l11ll_opy_])))
        response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠬࡖࡏࡔࡖࠪ⋍"), cls.request_url(event_url), bstack11111l11ll_opy_, config)
        bstack11l1l1lll1l_opy_ = response.json()
    @classmethod
    def bstack1l11llll1_opy_(cls, bstack11111l11ll_opy_, event_url=bstack1l1111_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⋎")):
        logger.debug(bstack1l1111_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⋏").format(bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋐")]))
        if not bstack11l11ll111_opy_.bstack1lll11ll11ll_opy_(bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⋑")]):
            logger.debug(bstack1l1111_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⋒").format(bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⋓")]))
            return
        bstack1l1111lll_opy_ = bstack11l11ll111_opy_.bstack1lll1l111lll_opy_(bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⋔")], bstack11111l11ll_opy_.get(bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⋕")))
        if bstack1l1111lll_opy_ != None:
            if bstack11111l11ll_opy_.get(bstack1l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⋖")) != None:
                bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⋗")][bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⋘")] = bstack1l1111lll_opy_
            else:
                bstack11111l11ll_opy_[bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⋙")] = bstack1l1111lll_opy_
        if event_url == bstack1l1111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⋚"):
            cls.bstack1lll11lll1l1_opy_()
            logger.debug(bstack1l1111_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⋛").format(bstack11111l11ll_opy_[bstack1l1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⋜")]))
            cls.bstack1llll1111l11_opy_.add(bstack11111l11ll_opy_)
        elif event_url == bstack1l1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⋝"):
            cls.bstack1lll1l1111ll_opy_([bstack11111l11ll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1111ll_opy_(cls, logs):
        for log in logs:
            bstack1lll1l11l111_opy_ = {
                bstack1l1111_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⋞"): bstack1l1111_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ⋟"),
                bstack1l1111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⋠"): log[bstack1l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⋡")],
                bstack1l1111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⋢"): log[bstack1l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⋣")],
                bstack1l1111_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ⋤"): {},
                bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⋥"): log[bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⋦")],
            }
            if bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⋧") in log:
                bstack1lll1l11l111_opy_[bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⋨")] = log[bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋩")]
            elif bstack1l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⋪") in log:
                bstack1lll1l11l111_opy_[bstack1l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⋫")] = log[bstack1l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⋬")]
            cls.bstack1l11llll1_opy_({
                bstack1l1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⋭"): bstack1l1111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⋮"),
                bstack1l1111_opy_ (u"ࠫࡱࡵࡧࡴࠩ⋯"): [bstack1lll1l11l111_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11llll1l_opy_(cls, steps):
        bstack1lll1l1111l1_opy_ = []
        for step in steps:
            bstack1lll11ll1lll_opy_ = {
                bstack1l1111_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⋰"): bstack1l1111_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ⋱"),
                bstack1l1111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⋲"): step[bstack1l1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⋳")],
                bstack1l1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⋴"): step[bstack1l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⋵")],
                bstack1l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⋶"): step[bstack1l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⋷")],
                bstack1l1111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⋸"): step[bstack1l1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⋹")]
            }
            if bstack1l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⋺") in step:
                bstack1lll11ll1lll_opy_[bstack1l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⋻")] = step[bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⋼")]
            elif bstack1l1111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⋽") in step:
                bstack1lll11ll1lll_opy_[bstack1l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋾")] = step[bstack1l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⋿")]
            bstack1lll1l1111l1_opy_.append(bstack1lll11ll1lll_opy_)
        cls.bstack1l11llll1_opy_({
            bstack1l1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⌀"): bstack1l1111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⌁"),
            bstack1l1111_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⌂"): bstack1lll1l1111l1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l11ll1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack11l1l1l1l_opy_(cls, screenshot):
        cls.bstack1l11llll1_opy_({
            bstack1l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⌃"): bstack1l1111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⌄"),
            bstack1l1111_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⌅"): [{
                bstack1l1111_opy_ (u"࠭࡫ࡪࡰࡧࠫ⌆"): bstack1l1111_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ⌇"),
                bstack1l1111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⌈"): datetime.datetime.utcnow().isoformat() + bstack1l1111_opy_ (u"ࠩ࡝ࠫ⌉"),
                bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⌊"): screenshot[bstack1l1111_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⌋")],
                bstack1l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⌌"): screenshot[bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌍")]
            }]
        }, event_url=bstack1l1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⌎"))
    @classmethod
    @error_handler(class_method=True)
    def bstack111lll1ll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l11llll1_opy_({
            bstack1l1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⌏"): bstack1l1111_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⌐"),
            bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⌑"): {
                bstack1l1111_opy_ (u"ࠦࡺࡻࡩࡥࠤ⌒"): cls.current_test_uuid(),
                bstack1l1111_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ⌓"): cls.bstack1111ll111l_opy_(driver)
            }
        })
    @classmethod
    def bstack1111ll1111_opy_(cls, event: str, bstack11111l11ll_opy_: bstack111111111l_opy_):
        bstack1111111ll1_opy_ = {
            bstack1l1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⌔"): event,
            bstack11111l11ll_opy_.bstack11111ll1l1_opy_(): bstack11111l11ll_opy_.bstack111111llll_opy_(event)
        }
        cls.bstack1l11llll1_opy_(bstack1111111ll1_opy_)
        result = getattr(bstack11111l11ll_opy_, bstack1l1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⌕"), None)
        if event == bstack1l1111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⌖"):
            threading.current_thread().bstackTestMeta = {bstack1l1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⌗"): bstack1l1111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⌘")}
        elif event == bstack1l1111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⌙"):
            threading.current_thread().bstackTestMeta = {bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌚"): getattr(result, bstack1l1111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⌛"), bstack1l1111_opy_ (u"ࠧࠨ⌜"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⌝"), None) is None or os.environ[bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⌞")] == bstack1l1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⌟")) and (os.environ.get(bstack1l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⌠"), None) is None or os.environ[bstack1l1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⌡")] == bstack1l1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⌢")):
            return False
        return True
    @staticmethod
    def bstack1lll11lll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l11111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⌣"): bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⌤"),
            bstack1l1111_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬ⌥"): bstack1l1111_opy_ (u"ࠪࡸࡷࡻࡥࠨ⌦")
        }
        if os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⌧"), None):
            headers[bstack1l1111_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⌨")] = bstack1l1111_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ〈").format(os.environ[bstack1l1111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ〉")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1111_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ⌫").format(bstack1lll11ll1l11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⌬"), None)
    @staticmethod
    def bstack1111ll111l_opy_(driver):
        return {
            bstack111l1llll1l_opy_(): bstack111l1l11l1l_opy_(driver)
        }
    @staticmethod
    def bstack1lll1l111111_opy_(exception_info, report):
        return [{bstack1l1111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭⌭"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1llll1111l1_opy_(typename):
        if bstack1l1111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ⌮") in typename:
            return bstack1l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ⌯")
        return bstack1l1111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ⌰")