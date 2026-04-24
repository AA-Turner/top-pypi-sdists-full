# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack1111l1ll1ll_opy_, bstack1111ll1l1l1_opy_, bstack111l1l1ll1_opy_, error_handler, bstack1llll11lll11_opy_, bstack1ll1lll1lll_opy_, bstack1llll1ll111l_opy_, bstack1llllll1l11_opy_, bstack111lll1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1l111111l_opy_ import bstack1ll11llllll1_opy_
import bstack_utils.bstack111l111lll_opy_ as TestHubUtils
from bstack_utils.bstack11lll111_opy_ import bstack1lll1l11l_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.bstack1llll1l11ll_opy_ import bstack1lll1ll11l1_opy_
from bstack_utils.constants import bstack1l11l11l1_opy_
bstack1ll111lll111_opy_ = bstack111ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ➦")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll1l111111l_opy_ = None
    bs_config = None
    bstack111ll1111l_opy_ = None
    _1ll111llll11_opy_ = False
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l1l111_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def launch(cls, bs_config, bstack111ll1111l_opy_):
        cls._1ll111llll11_opy_ = True
        cls.bs_config = bs_config
        cls.bstack111ll1111l_opy_ = bstack111ll1111l_opy_
        try:
            cls.bstack1ll111ll1111_opy_()
            bstack1111ll11lll_opy_ = bstack1111l1ll1ll_opy_(bs_config)
            bstack1111ll111l1_opy_ = bstack1111ll1l1l1_opy_(bs_config)
            data = TestHubUtils.bstack1ll111ll111l_opy_(bs_config, bstack111ll1111l_opy_)
            config = {
                bstack111ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭➧"): (bstack1111ll11lll_opy_, bstack1111ll111l1_opy_),
                bstack111ll11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ➨"): cls.default_headers()
            }
            response = bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ➩"), cls.request_url(bstack111ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ➪")), data, config)
            if response.status_code != 200:
                bstack1l111l1l1_opy_ = response.json()
                if bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭➫")] == False:
                    cls.bstack1ll11l111ll1_opy_(bstack1l111l1l1_opy_)
                    return
                cls.bstack1ll11l1111ll_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭➬")])
                cls.bstack1ll11l111l1l_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ➭")])
                return None
            bstack1ll111l1llll_opy_ = cls.bstack1ll111ll1l1l_opy_(response)
            return bstack1ll111l1llll_opy_, response.json()
        except Exception as error:
            logger.error(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ➮").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11111l11l1l_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def stop(cls, bstack1ll111lll1ll_opy_=None):
        if not bstack1lll1l11l_opy_.on() and not a11y.on():
            return
        if not cls._1ll111llll11_opy_:
            logger.info(bstack111ll11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࠡ࡫ࡶࠤࡈࡒࡉ࠮࡯ࡤࡲࡦ࡭ࡥࡥࠢࠫࡰࡦࡻ࡮ࡤࡪࠣࡲࡴࡺࠠࡤࡣ࡯ࡰࡪࡪࠠࡣࡻࠣࡗࡉࡑࠩࠡ࠯ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡹࡴࡰࡲࠣࡅࡕࡏࠠࡳࡧࡴࡹࡪࡹࡴࠣ➯"))
            if cls.bstack1ll1l111111l_opy_ is not None:
                logger.info(bstack111ll11_opy_ (u"ࠥࡗ࡭ࡻࡴࡵ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰࠣࡶࡪࡷࡵࡦࡵࡷࠤࡶࡻࡥࡶࡧࠥ➰"))
                cls.bstack1ll1l111111l_opy_.shutdown()
            else:
                logger.info(bstack111ll11_opy_ (u"ࠦࡓࡵࠠࡳࡧࡴࡹࡪࡹࡴࠡࡳࡸࡩࡺ࡫ࠠࡵࡱࠣࡷ࡭ࡻࡴࡥࡱࡺࡲࠧ➱"))
            return
        if os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ➲")) == bstack111ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ➳") or os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ➴")) == bstack111ll11_opy_ (u"ࠣࡰࡸࡰࡱࠨ➵"):
            logger.error(bstack111ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬ➶"))
            return {
                bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ➷"): bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ➸"),
                bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭➹"): bstack111ll11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫ➺")
            }
        try:
            cls.bstack1ll1l111111l_opy_.shutdown()
            data = {
                bstack111ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ➻"): bstack1llllll1l11_opy_()
            }
            if not bstack1ll111lll1ll_opy_ is None:
                data[bstack111ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬ➼")] = [{
                    bstack111ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ➽"): bstack111ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ➾"),
                    bstack111ll11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫ➿"): bstack1ll111lll1ll_opy_
                }]
            config = {
                bstack111ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭⟀"): cls.default_headers()
            }
            bstack1111l11l111_opy_ = bstack111ll11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧ⟁").format(os.environ[bstack111ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠧ⟂")])
            bstack1ll111ll11ll_opy_ = cls.request_url(bstack1111l11l111_opy_)
            response = bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠨࡒࡘࡘࠬ⟃"), bstack1ll111ll11ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111ll11_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣ⟄"))
        except Exception as error:
            logger.error(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢ⟅") + str(error))
            return {
                bstack111ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⟆"): bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⟇"),
                bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⟈"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111ll1l1l_opy_(cls, response):
        bstack1l111l1l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll111l1llll_opy_ = {}
        if bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠧ࡫ࡹࡷࠫ⟉")) is None:
            os.environ[bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⟊")] = bstack111ll11_opy_ (u"ࠩࡱࡹࡱࡲࠧ⟋")
        else:
            os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⟌")] = bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠫ࡯ࡽࡴࠨ⟍"), bstack111ll11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⟎"))
        os.environ[bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⟏")] = bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⟐"), bstack111ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭⟑"))
        logger.info(bstack111ll11_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧ⟒") + os.getenv(bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⟓")));
        if bstack1lll1l11l_opy_.bstack1ll11l111l11_opy_(cls.bs_config, cls.bstack111ll1111l_opy_.get(bstack111ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ⟔"), bstack111ll11_opy_ (u"ࠬ࠭⟕"))) is True:
            bstack1ll11lll1l11_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll11l11111l_opy_(bstack1l111l1l1_opy_)
            if bstack1ll11lll1l11_opy_ != None and build_hashed_id != None:
                bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⟖")] = {
                    bstack111ll11_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪ⟗"): bstack1ll11lll1l11_opy_,
                    bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⟘"): build_hashed_id,
                    bstack111ll11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⟙"): allow_screenshots
                }
            else:
                bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⟚")] = {}
        else:
            bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⟛")] = {}
        bstack1ll111llll1l_opy_, build_hashed_id = cls.bstack1ll111lll11l_opy_(bstack1l111l1l1_opy_)
        if bstack1ll111llll1l_opy_ != None and build_hashed_id != None:
            bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⟜")] = {
                bstack111ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪ⟝"): bstack1ll111llll1l_opy_,
                bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⟞"): build_hashed_id,
            }
        else:
            bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⟟")] = {}
        if bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⟠")].get(bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⟡")) != None or bstack1ll111l1llll_opy_[bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⟢")].get(bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⟣")) != None:
            cls.bstack1ll111ll1lll_opy_(bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"࠭ࡪࡸࡶࠪ⟤")), bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⟥")))
        return bstack1ll111l1llll_opy_
    @classmethod
    def bstack1ll11l11111l_opy_(cls, bstack1l111l1l1_opy_):
        if bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⟦")) == None:
            cls.bstack1ll11l1111ll_opy_()
            return [None, None, None]
        if bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⟧")][bstack111ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⟨")] != True:
            cls.bstack1ll11l1111ll_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⟩")])
            return [None, None, None]
        logger.debug(bstack111ll11_opy_ (u"ࠬࢁࡽࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ⟪").format(bstack1l11l11l1_opy_))
        os.environ[bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ⟫")] = bstack111ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ⟬")
        if bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠨ࡬ࡺࡸࠬ⟭")):
            os.environ[bstack111ll11_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭⟮")] = json.dumps({
                bstack111ll11_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ⟯"): bstack1111l1ll1ll_opy_(cls.bs_config),
                bstack111ll11_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭⟰"): bstack1111ll1l1l1_opy_(cls.bs_config)
            })
        if bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⟱")):
            os.environ[bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ⟲")] = bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⟳")]
        if bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⟴")].get(bstack111ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⟵"), {}).get(bstack111ll11_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⟶")):
            os.environ[bstack111ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⟷")] = str(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⟸")][bstack111ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⟹")][bstack111ll11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⟺")])
        else:
            os.environ[bstack111ll11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⟻")] = bstack111ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢ⟼")
        return [bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠪ࡮ࡼࡺࠧ⟽")], bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⟾")], os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⟿")]]
    @classmethod
    def bstack1ll111lll11l_opy_(cls, bstack1l111l1l1_opy_):
        if bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⠀")) == None:
            cls.bstack1ll11l111l1l_opy_()
            return [None, None]
        if bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⠁")][bstack111ll11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ⠂")] != True:
            cls.bstack1ll11l111l1l_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⠃")])
            return [None, None]
        if bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⠄")].get(bstack111ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⠅")):
            logger.debug(bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩ⠆"))
            parsed = json.loads(os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⠇"), bstack111ll11_opy_ (u"ࠧࡼࡿࠪ⠈")))
            capabilities = TestHubUtils.bstack1ll111lll1l1_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⠉")][bstack111ll11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⠊")][bstack111ll11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ⠋")], bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⠌"), bstack111ll11_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫ⠍"))
            bstack1ll111llll1l_opy_ = capabilities[bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ⠎")]
            os.environ[bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⠏")] = bstack1ll111llll1l_opy_
            if capabilities.get(bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭⠐")):
                os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ⠑")] = str(capabilities[bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ⠒")])
            if capabilities.get(bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠩ⠓")):
                os.environ[bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠪ⠔")] = str(capabilities[bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠫ⠕")])
            if bstack111ll11_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ⠖") in bstack1l111l1l1_opy_ and bstack1l111l1l1_opy_.get(bstack111ll11_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ⠗")) is None:
                parsed[bstack111ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⠘")] = capabilities[bstack111ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ⠙")]
            os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⠚")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll111lll1l1_opy_(bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⠛")][bstack111ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⠜")][bstack111ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ⠝")], bstack111ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭⠞"), bstack111ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪ⠟"))
            accessibility_scripts.bstack1l1l1l1l11_opy_(scripts)
            commands_to_wrap = bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⠠")][bstack111ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⠡")][bstack111ll11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭⠢")]
            commands = commands_to_wrap.get(bstack111ll11_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ⠣"))
            accessibility_scripts.bstack1l11lll11ll_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack111ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳ࠭⠤"))
            accessibility_scripts.bstack1111l11l1l1_opy_(scripts_to_run)
            bstack1111l1llll1_opy_ = capabilities.get(bstack111ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭⠥"))
            accessibility_scripts.bstack1111l11ll11_opy_(bstack1111l1llll1_opy_)
            accessibility_scripts.store()
        return [bstack1ll111llll1l_opy_, bstack1l111l1l1_opy_[bstack111ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⠦")]]
    @classmethod
    def bstack1ll11l1111ll_opy_(cls, response=None):
        os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⠧")] = bstack111ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⠨")
        os.environ[bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⠩")] = bstack111ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⠪")
        os.environ[bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭⠫")] = bstack111ll11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ⠬")
        os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⠭")] = bstack111ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⠮")
        os.environ[bstack111ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⠯")] = bstack111ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⠰")
        cls.bstack1ll11l111ll1_opy_(response, bstack111ll11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨ⠱"))
        return [None, None, None]
    @classmethod
    def bstack1ll11l111l1l_opy_(cls, response=None):
        os.environ[bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⠲")] = bstack111ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭⠳")
        os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⠴")] = bstack111ll11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⠵")
        os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⠶")] = bstack111ll11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⠷")
        cls.bstack1ll11l111ll1_opy_(response, bstack111ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨ⠸"))
        return [None, None, None]
    @classmethod
    def bstack1ll111ll1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⠹")] = jwt
        os.environ[bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⠺")] = build_hashed_id
    @classmethod
    def bstack1ll11l111ll1_opy_(cls, response=None, product=bstack111ll11_opy_ (u"ࠤࠥ⠻")):
        if response == None or response.get(bstack111ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ⠼")) == None:
            logger.error(product + bstack111ll11_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨ⠽"))
            return
        for error in response[bstack111ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ⠾")]:
            bstack1llll1l1ll1l_opy_ = error[bstack111ll11_opy_ (u"࠭࡫ࡦࡻࠪ⠿")]
            error_message = error[bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⡀")]
            if error_message:
                if bstack1llll1l1ll1l_opy_ == bstack111ll11_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢ⡁"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111ll11_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥ⡂") + product + bstack111ll11_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ⡃"))
    @classmethod
    def bstack1ll111ll1111_opy_(cls):
        if cls.bstack1ll1l111111l_opy_ is not None:
            return
        cls.bstack1ll1l111111l_opy_ = bstack1ll11llllll1_opy_(cls.post_data)
        cls.bstack1ll1l111111l_opy_.start()
    @classmethod
    def bstack1lll1lll111_opy_(cls):
        if cls.bstack1ll1l111111l_opy_ is None:
            return
        cls.bstack1ll1l111111l_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lll11lllll_opy_, event_url=bstack111ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⡄")):
        config = {
            bstack111ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭⡅"): cls.default_headers()
        }
        logger.debug(bstack111ll11_opy_ (u"ࠨࡰࡰࡵࡷࡣࡩࡧࡴࡢ࠼ࠣࡗࡪࡴࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡺࡥࡴࡶ࡫ࡹࡧࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵࡵࠣࡿࢂࠨ⡆").format(bstack111ll11_opy_ (u"ࠧ࠭ࠢࠪ⡇").join([event[bstack111ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⡈")] for event in bstack1lll11lllll_opy_])))
        response = bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⡉"), cls.request_url(event_url), bstack1lll11lllll_opy_, config)
        bstack1111lll1lll_opy_ = response.json()
    @classmethod
    def bstack1l1lll11_opy_(cls, bstack1lll11lllll_opy_, event_url=bstack111ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ⡊")):
        logger.debug(bstack111ll11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡷࡸࡪࡳࡰࡵ࡫ࡱ࡫ࠥࡺ࡯ࠡࡣࡧࡨࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ⡋").format(bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⡌")]))
        if not TestHubUtils.bstack1ll11l1111l1_opy_(bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⡍")]):
            logger.debug(bstack111ll11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡓࡵࡴࠡࡣࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⡎").format(bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⡏")]))
            return
        bstack11l11l11ll_opy_ = TestHubUtils.bstack1ll11l111111_opy_(bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⡐")], bstack1lll11lllll_opy_.get(bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⡑")))
        if bstack11l11l11ll_opy_ != None:
            if bstack1lll11lllll_opy_.get(bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⡒")) != None:
                bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⡓")][bstack111ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ⡔")] = bstack11l11l11ll_opy_
            else:
                bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⡕")] = bstack11l11l11ll_opy_
        if event_url == bstack111ll11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⡖"):
            cls.bstack1ll111ll1111_opy_()
            logger.debug(bstack111ll11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⡗").format(bstack1lll11lllll_opy_[bstack111ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⡘")]))
            cls.bstack1ll1l111111l_opy_.add(bstack1lll11lllll_opy_)
        elif event_url == bstack111ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⡙"):
            cls.post_data([bstack1lll11lllll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack111ll11lll_opy_(cls, logs):
        for log in logs:
            bstack1ll111ll1ll1_opy_ = {
                bstack111ll11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⡚"): bstack111ll11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨ⡛"),
                bstack111ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⡜"): log[bstack111ll11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⡝")],
                bstack111ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⡞"): log[bstack111ll11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⡟")],
                bstack111ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫ⡠"): {},
                bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⡡"): log[bstack111ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⡢")],
            }
            if bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡣") in log:
                bstack1ll111ll1ll1_opy_[bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⡤")] = log[bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⡥")]
            elif bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⡦") in log:
                bstack1ll111ll1ll1_opy_[bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⡧")] = log[bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⡨")]
            cls.bstack1l1lll11_opy_({
                bstack111ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⡩"): bstack111ll11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⡪"),
                bstack111ll11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⡫"): [bstack1ll111ll1ll1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111llllll_opy_(cls, steps):
        bstack1ll111l1lll1_opy_ = []
        for step in steps:
            bstack1ll111ll11l1_opy_ = {
                bstack111ll11_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⡬"): bstack111ll11_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭⡭"),
                bstack111ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⡮"): step[bstack111ll11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⡯")],
                bstack111ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⡰"): step[bstack111ll11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⡱")],
                bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⡲"): step[bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⡳")],
                bstack111ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⡴"): step[bstack111ll11_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⡵")]
            }
            if bstack111ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⡶") in step:
                bstack1ll111ll11l1_opy_[bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⡷")] = step[bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⡸")]
            elif bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⡹") in step:
                bstack1ll111ll11l1_opy_[bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⡺")] = step[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⡻")]
            bstack1ll111l1lll1_opy_.append(bstack1ll111ll11l1_opy_)
        cls.bstack1l1lll11_opy_({
            bstack111ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⡼"): bstack111ll11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⡽"),
            bstack111ll11_opy_ (u"࠭࡬ࡰࡩࡶࠫ⡾"): bstack1ll111l1lll1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l111l1l_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack111111ll_opy_(cls, screenshot):
        cls.bstack1l1lll11_opy_({
            bstack111ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⡿"): bstack111ll11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⢀"),
            bstack111ll11_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⢁"): [{
                bstack111ll11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⢂"): bstack111ll11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭⢃"),
                bstack111ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⢄"): datetime.datetime.utcnow().isoformat() + bstack111ll11_opy_ (u"࡚࠭ࠨ⢅"),
                bstack111ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⢆"): screenshot[bstack111ll11_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧ⢇")],
                bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⢈"): screenshot[bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⢉")]
            }]
        }, event_url=bstack111ll11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⢊"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1lll11_opy_({
            bstack111ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⢋"): bstack111ll11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⢌"),
            bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⢍"): {
                bstack111ll11_opy_ (u"ࠣࡷࡸ࡭ࡩࠨ⢎"): cls.current_test_uuid(),
                bstack111ll11_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣ⢏"): cls.bstack1llll111l1l_opy_(driver)
            }
        })
    @classmethod
    def bstack1llll1l11l1_opy_(cls, event: str, bstack1lll11lllll_opy_: bstack1lll1ll11l1_opy_):
        bstack1lll1l1l1ll_opy_ = {
            bstack111ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⢐"): event,
            bstack1lll11lllll_opy_.bstack1lll1ll1lll_opy_(): bstack1lll11lllll_opy_.bstack1lll1l11l1l_opy_(event)
        }
        cls.bstack1l1lll11_opy_(bstack1lll1l1l1ll_opy_)
        result = getattr(bstack1lll11lllll_opy_, bstack111ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⢑"), None)
        if event == bstack111ll11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⢒"):
            threading.current_thread().bstackTestMeta = {bstack111ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⢓"): bstack111ll11_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⢔")}
        elif event == bstack111ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⢕"):
            threading.current_thread().bstackTestMeta = {bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⢖"): getattr(result, bstack111ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⢗"), bstack111ll11_opy_ (u"ࠫࠬ⢘"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⢙"), None) is None or os.environ[bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⢚")] == bstack111ll11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⢛")) and (os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⢜"), None) is None or os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⢝")] == bstack111ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⢞")):
            return False
        return True
    @staticmethod
    def bstack1ll111ll1l11_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111ll11_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ⢟"): bstack111ll11_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ⢠"),
            bstack111ll11_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩ⢡"): bstack111ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬ⢢")
        }
        if os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⢣"), None):
            headers[bstack111ll11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ⢤")] = bstack111ll11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭⢥").format(os.environ[bstack111ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣ⢦")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111ll11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫ⢧").format(bstack1ll111lll111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111ll11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ⢨"), None)
    @staticmethod
    def bstack1llll111l1l_opy_(driver):
        return {
            bstack1llll11lll11_opy_(): bstack1ll1lll1lll_opy_(driver)
        }
    @staticmethod
    def bstack1ll111lllll1_opy_(exception_info, report):
        return [{bstack111ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪ⢩"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll111l1l1l_opy_(typename):
        if bstack111ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ⢪") in typename:
            return bstack111ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ⢫")
        return bstack111ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ⢬")