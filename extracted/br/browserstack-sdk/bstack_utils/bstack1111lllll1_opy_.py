# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l1l111l_opy_, bstack11l1ll11111_opy_, bstack111l11l1ll_opy_, error_handler, bstack111l111111l_opy_, bstack111l11lll11_opy_, bstack111l1l11l11_opy_, bstack1ll1llll11_opy_, bstack111ll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll1llll11l_opy_ import bstack1lll1lllll11_opy_
import bstack_utils.bstack1111ll1l1_opy_ as bstack1l1ll1111_opy_
from bstack_utils.bstack1111llll11_opy_ import bstack1ll11l1l1l_opy_
import bstack_utils.accessibility as bstack1l11l1l1l_opy_
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_
from bstack_utils.bstack1111ll11ll_opy_ import bstack1111l11ll1_opy_
from bstack_utils.constants import bstack1l1llll11_opy_
bstack1lll1l11111l_opy_ = bstack11l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ∸")
logger = logging.getLogger(__name__)
class bstack1l11111l1l_opy_:
    bstack1lll1llll11l_opy_ = None
    bs_config = None
    bstack1l11llll_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l11111ll1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def launch(cls, bs_config, bstack1l11llll_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11llll_opy_ = bstack1l11llll_opy_
        try:
            cls.bstack1lll11llllll_opy_()
            bstack11l1ll1ll1l_opy_ = bstack11l1l1l111l_opy_(bs_config)
            bstack11l1l11ll1l_opy_ = bstack11l1ll11111_opy_(bs_config)
            data = bstack1l1ll1111_opy_.bstack1lll11ll1l1l_opy_(bs_config, bstack1l11llll_opy_)
            config = {
                bstack11l1ll1_opy_ (u"ࠫࡦࡻࡴࡩࠩ∹"): (bstack11l1ll1ll1l_opy_, bstack11l1l11ll1l_opy_),
                bstack11l1ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭∺"): cls.default_headers()
            }
            response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"࠭ࡐࡐࡕࡗࠫ∻"), cls.request_url(bstack11l1ll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧ∼")), data, config)
            if response.status_code != 200:
                bstack111l1l11l1_opy_ = response.json()
                if bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ∽")] == False:
                    cls.bstack1lll11l1l11l_opy_(bstack111l1l11l1_opy_)
                    return
                cls.bstack1lll11ll1l11_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ∾")])
                cls.bstack1lll11lll111_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ∿")])
                return None
            bstack1lll11ll1lll_opy_ = cls.bstack1lll11ll1111_opy_(response)
            return bstack1lll11ll1lll_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤ≀").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1111ll11_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def stop(cls, bstack1lll11ll11ll_opy_=None):
        if not bstack1ll11l1l1l_opy_.on() and not bstack1l11l1l1l_opy_.on():
            return
        if os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ≁")) == bstack11l1ll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ≂") or os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ≃")) == bstack11l1ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨ≄"):
            logger.error(bstack11l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ≅"))
            return {
                bstack11l1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ≆"): bstack11l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ≇"),
                bstack11l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭≈"): bstack11l1ll1_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫ≉")
            }
        try:
            cls.bstack1lll1llll11l_opy_.shutdown()
            data = {
                bstack11l1ll1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ≊"): bstack1ll1llll11_opy_()
            }
            if not bstack1lll11ll11ll_opy_ is None:
                data[bstack11l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬ≋")] = [{
                    bstack11l1ll1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ≌"): bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ≍"),
                    bstack11l1ll1_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫ≎"): bstack1lll11ll11ll_opy_
                }]
            config = {
                bstack11l1ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭≏"): cls.default_headers()
            }
            bstack11l11lllll1_opy_ = bstack11l1ll1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧ≐").format(os.environ[bstack11l1ll1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ≑")])
            bstack1lll1l1111l1_opy_ = cls.request_url(bstack11l11lllll1_opy_)
            response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"ࠨࡒࡘࡘࠬ≒"), bstack1lll1l1111l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1ll1_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣ≓"))
        except Exception as error:
            logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢ≔") + str(error))
            return {
                bstack11l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ≕"): bstack11l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ≖"),
                bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ≗"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11ll1111_opy_(cls, response):
        bstack111l1l11l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll11ll1lll_opy_ = {}
        if bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠧ࡫ࡹࡷࠫ≘")) is None:
            os.environ[bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ≙")] = bstack11l1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ≚")
        else:
            os.environ[bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ≛")] = bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠫ࡯ࡽࡴࠨ≜"), bstack11l1ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ≝"))
        os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ≞")] = bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ≟"), bstack11l1ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭≠"))
        logger.info(bstack11l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧ≡") + os.getenv(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ≢")));
        if bstack1ll11l1l1l_opy_.bstack1lll11l1l1ll_opy_(cls.bs_config, cls.bstack1l11llll_opy_.get(bstack11l1ll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ≣"), bstack11l1ll1_opy_ (u"ࠬ࠭≤"))) is True:
            bstack1lll1lll1ll1_opy_, build_hashed_id, bstack1lll11l1l1l1_opy_ = cls.bstack1lll11ll11l1_opy_(bstack111l1l11l1_opy_)
            if bstack1lll1lll1ll1_opy_ != None and build_hashed_id != None:
                bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭≥")] = {
                    bstack11l1ll1_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪ≦"): bstack1lll1lll1ll1_opy_,
                    bstack11l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ≧"): build_hashed_id,
                    bstack11l1ll1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭≨"): bstack1lll11l1l1l1_opy_
                }
            else:
                bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ≩")] = {}
        else:
            bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ≪")] = {}
        bstack1lll11lllll1_opy_, build_hashed_id = cls.bstack1lll11lll1l1_opy_(bstack111l1l11l1_opy_)
        if bstack1lll11lllll1_opy_ != None and build_hashed_id != None:
            bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ≫")] = {
                bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪ≬"): bstack1lll11lllll1_opy_,
                bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ≭"): build_hashed_id,
            }
        else:
            bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ≮")] = {}
        if bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ≯")].get(bstack11l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ≰")) != None or bstack1lll11ll1lll_opy_[bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ≱")].get(bstack11l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ≲")) != None:
            cls.bstack1lll1l111111_opy_(bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡪࡸࡶࠪ≳")), bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ≴")))
        return bstack1lll11ll1lll_opy_
    @classmethod
    def bstack1lll11ll11l1_opy_(cls, bstack111l1l11l1_opy_):
        if bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ≵")) == None:
            cls.bstack1lll11ll1l11_opy_()
            return [None, None, None]
        if bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ≶")][bstack11l1ll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ≷")] != True:
            cls.bstack1lll11ll1l11_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ≸")])
            return [None, None, None]
        logger.debug(bstack11l1ll1_opy_ (u"ࠬࢁࡽࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ≹").format(bstack1l1llll11_opy_))
        os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ≺")] = bstack11l1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ≻")
        if bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠨ࡬ࡺࡸࠬ≼")):
            os.environ[bstack11l1ll1_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭≽")] = json.dumps({
                bstack11l1ll1_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ≾"): bstack11l1l1l111l_opy_(cls.bs_config),
                bstack11l1ll1_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭≿"): bstack11l1ll11111_opy_(cls.bs_config)
            })
        if bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⊀")):
            os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ⊁")] = bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⊂")]
        if bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⊃")].get(bstack11l1ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⊄"), {}).get(bstack11l1ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⊅")):
            os.environ[bstack11l1ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⊆")] = str(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⊇")][bstack11l1ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⊈")][bstack11l1ll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⊉")])
        else:
            os.environ[bstack11l1ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⊊")] = bstack11l1ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢ⊋")
        return [bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠪ࡮ࡼࡺࠧ⊌")], bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⊍")], os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⊎")]]
    @classmethod
    def bstack1lll11lll1l1_opy_(cls, bstack111l1l11l1_opy_):
        if bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⊏")) == None:
            cls.bstack1lll11lll111_opy_()
            return [None, None]
        if bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⊐")][bstack11l1ll1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ⊑")] != True:
            cls.bstack1lll11lll111_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⊒")])
            return [None, None]
        if bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⊓")].get(bstack11l1ll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⊔")):
            logger.debug(bstack11l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩ⊕"))
            parsed = json.loads(os.getenv(bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⊖"), bstack11l1ll1_opy_ (u"ࠧࡼࡿࠪ⊗")))
            capabilities = bstack1l1ll1111_opy_.bstack1lll11lll11l_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⊘")][bstack11l1ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⊙")][bstack11l1ll1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ⊚")], bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⊛"), bstack11l1ll1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⊜"))
            bstack1lll11lllll1_opy_ = capabilities[bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ⊝")]
            os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⊞")] = bstack1lll11lllll1_opy_
            if bstack11l1ll1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ⊟") in bstack111l1l11l1_opy_ and bstack111l1l11l1_opy_.get(bstack11l1ll1_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ⊠")) is None:
                parsed[bstack11l1ll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⊡")] = capabilities[bstack11l1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⊢")]
            os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⊣")] = json.dumps(parsed)
            scripts = bstack1l1ll1111_opy_.bstack1lll11lll11l_opy_(bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⊤")][bstack11l1ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⊥")][bstack11l1ll1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ⊦")], bstack11l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⊧"), bstack11l1ll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫ⊨"))
            bstack1lll1ll11l_opy_.bstack11ll11l11l_opy_(scripts)
            commands = bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⊩")][bstack11l1ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⊪")][bstack11l1ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ⊫")].get(bstack11l1ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ⊬"))
            bstack1lll1ll11l_opy_.bstack11l1l111ll1_opy_(commands)
            bstack11l1ll1l111_opy_ = capabilities.get(bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⊭"))
            bstack1lll1ll11l_opy_.bstack11l1l1111l1_opy_(bstack11l1ll1l111_opy_)
            bstack1lll1ll11l_opy_.store()
        return [bstack1lll11lllll1_opy_, bstack111l1l11l1_opy_[bstack11l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⊮")]]
    @classmethod
    def bstack1lll11ll1l11_opy_(cls, response=None):
        os.environ[bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⊯")] = bstack11l1ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⊰")
        os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⊱")] = bstack11l1ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⊲")
        os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭⊳")] = bstack11l1ll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⊴")
        os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⊵")] = bstack11l1ll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⊶")
        os.environ[bstack11l1ll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⊷")] = bstack11l1ll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⊸")
        cls.bstack1lll11l1l11l_opy_(response, bstack11l1ll1_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨ⊹"))
        return [None, None, None]
    @classmethod
    def bstack1lll11lll111_opy_(cls, response=None):
        os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⊺")] = bstack11l1ll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭⊻")
        os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⊼")] = bstack11l1ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⊽")
        os.environ[bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⊾")] = bstack11l1ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⊿")
        cls.bstack1lll11l1l11l_opy_(response, bstack11l1ll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨ⋀"))
        return [None, None, None]
    @classmethod
    def bstack1lll1l111111_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⋁")] = jwt
        os.environ[bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⋂")] = build_hashed_id
    @classmethod
    def bstack1lll11l1l11l_opy_(cls, response=None, product=bstack11l1ll1_opy_ (u"ࠤࠥ⋃")):
        if response == None or response.get(bstack11l1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ⋄")) == None:
            logger.error(product + bstack11l1ll1_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨ⋅"))
            return
        for error in response[bstack11l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ⋆")]:
            bstack1111llll1l1_opy_ = error[bstack11l1ll1_opy_ (u"࠭࡫ࡦࡻࠪ⋇")]
            error_message = error[bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⋈")]
            if error_message:
                if bstack1111llll1l1_opy_ == bstack11l1ll1_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢ⋉"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1ll1_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥ⋊") + product + bstack11l1ll1_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ⋋"))
    @classmethod
    def bstack1lll11llllll_opy_(cls):
        if cls.bstack1lll1llll11l_opy_ is not None:
            return
        cls.bstack1lll1llll11l_opy_ = bstack1lll1lllll11_opy_(cls.bstack1lll11l1ll11_opy_)
        cls.bstack1lll1llll11l_opy_.start()
    @classmethod
    def bstack111111llll_opy_(cls):
        if cls.bstack1lll1llll11l_opy_ is None:
            return
        cls.bstack1lll1llll11l_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11l1ll11_opy_(cls, bstack11111l1lll_opy_, event_url=bstack11l1ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⋌")):
        config = {
            bstack11l1ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭⋍"): cls.default_headers()
        }
        logger.debug(bstack11l1ll1_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨ⋎").format(bstack11l1ll1_opy_ (u"ࠧ࠭ࠢࠪ⋏").join([event[bstack11l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋐")] for event in bstack11111l1lll_opy_])))
        response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⋑"), cls.request_url(event_url), bstack11111l1lll_opy_, config)
        bstack11l1ll1ll11_opy_ = response.json()
    @classmethod
    def bstack1111l11ll_opy_(cls, bstack11111l1lll_opy_, event_url=bstack11l1ll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ⋒")):
        logger.debug(bstack11l1ll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ⋓").format(bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⋔")]))
        if not bstack1l1ll1111_opy_.bstack1lll11ll1ll1_opy_(bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⋕")]):
            logger.debug(bstack11l1ll1_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⋖").format(bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⋗")]))
            return
        bstack1l1l11l11_opy_ = bstack1l1ll1111_opy_.bstack1lll11l1llll_opy_(bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⋘")], bstack11111l1lll_opy_.get(bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⋙")))
        if bstack1l1l11l11_opy_ != None:
            if bstack11111l1lll_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⋚")) != None:
                bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⋛")][bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ⋜")] = bstack1l1l11l11_opy_
            else:
                bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⋝")] = bstack1l1l11l11_opy_
        if event_url == bstack11l1ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⋞"):
            cls.bstack1lll11llllll_opy_()
            logger.debug(bstack11l1ll1_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⋟").format(bstack11111l1lll_opy_[bstack11l1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⋠")]))
            cls.bstack1lll1llll11l_opy_.add(bstack11111l1lll_opy_)
        elif event_url == bstack11l1ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⋡"):
            cls.bstack1lll11l1ll11_opy_([bstack11111l1lll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1111llll1_opy_(cls, logs):
        for log in logs:
            bstack1lll11ll111l_opy_ = {
                bstack11l1ll1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⋢"): bstack11l1ll1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨ⋣"),
                bstack11l1ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⋤"): log[bstack11l1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⋥")],
                bstack11l1ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⋦"): log[bstack11l1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⋧")],
                bstack11l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫ⋨"): {},
                bstack11l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⋩"): log[bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⋪")],
            }
            if bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⋫") in log:
                bstack1lll11ll111l_opy_[bstack11l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⋬")] = log[bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⋭")]
            elif bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⋮") in log:
                bstack1lll11ll111l_opy_[bstack11l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⋯")] = log[bstack11l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋰")]
            cls.bstack1111l11ll_opy_({
                bstack11l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⋱"): bstack11l1ll1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⋲"),
                bstack11l1ll1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⋳"): [bstack1lll11ll111l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11llll11_opy_(cls, steps):
        bstack1lll11llll1l_opy_ = []
        for step in steps:
            bstack1lll11lll1ll_opy_ = {
                bstack11l1ll1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⋴"): bstack11l1ll1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭⋵"),
                bstack11l1ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⋶"): step[bstack11l1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⋷")],
                bstack11l1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⋸"): step[bstack11l1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⋹")],
                bstack11l1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⋺"): step[bstack11l1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⋻")],
                bstack11l1ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⋼"): step[bstack11l1ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⋽")]
            }
            if bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⋾") in step:
                bstack1lll11lll1ll_opy_[bstack11l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⋿")] = step[bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌀")]
            elif bstack11l1ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⌁") in step:
                bstack1lll11lll1ll_opy_[bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌂")] = step[bstack11l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⌃")]
            bstack1lll11llll1l_opy_.append(bstack1lll11lll1ll_opy_)
        cls.bstack1111l11ll_opy_({
            bstack11l1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⌄"): bstack11l1ll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⌅"),
            bstack11l1ll1_opy_ (u"࠭࡬ࡰࡩࡶࠫ⌆"): bstack1lll11llll1l_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1ll111ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1111l111_opy_(cls, screenshot):
        cls.bstack1111l11ll_opy_({
            bstack11l1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⌇"): bstack11l1ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⌈"),
            bstack11l1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⌉"): [{
                bstack11l1ll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⌊"): bstack11l1ll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭⌋"),
                bstack11l1ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⌌"): datetime.datetime.utcnow().isoformat() + bstack11l1ll1_opy_ (u"࡚࠭ࠨ⌍"),
                bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⌎"): screenshot[bstack11l1ll1_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ⌏")],
                bstack11l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌐"): screenshot[bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⌑")]
            }]
        }, event_url=bstack11l1ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⌒"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1l11l1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1111l11ll_opy_({
            bstack11l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⌓"): bstack11l1ll1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⌔"),
            bstack11l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⌕"): {
                bstack11l1ll1_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ⌖"): cls.current_test_uuid(),
                bstack11l1ll1_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣ⌗"): cls.bstack1111ll1l11_opy_(driver)
            }
        })
    @classmethod
    def bstack1111ll111l_opy_(cls, event: str, bstack11111l1lll_opy_: bstack1111l11ll1_opy_):
        bstack11111l1l11_opy_ = {
            bstack11l1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⌘"): event,
            bstack11111l1lll_opy_.bstack11111lll1l_opy_(): bstack11111l1lll_opy_.bstack1111l11lll_opy_(event)
        }
        cls.bstack1111l11ll_opy_(bstack11111l1l11_opy_)
        result = getattr(bstack11111l1lll_opy_, bstack11l1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⌙"), None)
        if event == bstack11l1ll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⌚"):
            threading.current_thread().bstackTestMeta = {bstack11l1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⌛"): bstack11l1ll1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⌜")}
        elif event == bstack11l1ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⌝"):
            threading.current_thread().bstackTestMeta = {bstack11l1ll1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⌞"): getattr(result, bstack11l1ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⌟"), bstack11l1ll1_opy_ (u"ࠫࠬ⌠"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⌡"), None) is None or os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⌢")] == bstack11l1ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⌣")) and (os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⌤"), None) is None or os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⌥")] == bstack11l1ll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⌦")):
            return False
        return True
    @staticmethod
    def bstack1lll11l1lll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11111l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⌧"): bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⌨"),
            bstack11l1ll1_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩ〈"): bstack11l1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ〉")
        }
        if os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⌫"), None):
            headers[bstack11l1ll1_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⌬")] = bstack11l1ll1_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⌭").format(os.environ[bstack11l1ll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣ⌮")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1ll1_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ⌯").format(bstack1lll1l11111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1ll1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⌰"), None)
    @staticmethod
    def bstack1111ll1l11_opy_(driver):
        return {
            bstack111l111111l_opy_(): bstack111l11lll11_opy_(driver)
        }
    @staticmethod
    def bstack1lll11l1ll1l_opy_(exception_info, report):
        return [{bstack11l1ll1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⌱"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1llll11111l_opy_(typename):
        if bstack11l1ll1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ⌲") in typename:
            return bstack11l1ll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ⌳")
        return bstack11l1ll1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ⌴")