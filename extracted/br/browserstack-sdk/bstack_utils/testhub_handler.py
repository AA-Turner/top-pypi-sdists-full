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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll11l11l_opy_, bstack111lll1llll_opy_, bstack111l1l111l_opy_, error_handler, bstack11111llll11_opy_, bstack1111l1ll1ll_opy_, bstack1llllllll1ll_opy_, current_time, bstack111l1lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1llllllll_opy_ import bstack1lll11111111_opy_
import bstack_utils.bstack1l1l1ll11_opy_ as TestHubUtils
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.test_data import bstack1llll1l11l1_opy_
from bstack_utils.constants import bstack11l11lll11_opy_
bstack1ll1l1llll11_opy_ = bstack1ll1lll_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭╧")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1ll1llllllll_opy_ = None
    bs_config = None
    bstack1l1ll11l11_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1l11ll1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def launch(cls, bs_config, bstack1l1ll11l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1ll11l11_opy_ = bstack1l1ll11l11_opy_
        try:
            cls.bstack1ll1ll11111l_opy_()
            bstack111lll11l1l_opy_ = bstack111ll11l11l_opy_(bs_config)
            bstack111llll111l_opy_ = bstack111lll1llll_opy_(bs_config)
            data = TestHubUtils.bstack1ll1ll111l1l_opy_(bs_config, bstack1l1ll11l11_opy_)
            config = {
                bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ╨"): (bstack111lll11l1l_opy_, bstack111llll111l_opy_),
                bstack1ll1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ╩"): cls.default_headers()
            }
            response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ╪"), cls.request_url(bstack1ll1lll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪ╫")), data, config)
            if response.status_code != 200:
                bstack11lll11l1l_opy_ = response.json()
                if bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ╬")] == False:
                    cls.bstack1ll1l1llll1l_opy_(bstack11lll11l1l_opy_)
                    return
                cls.bstack1ll1l1lll11l_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ╭")])
                cls.bstack1ll1l1lllll1_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭╮")])
                return None
            bstack1ll1ll11l1l1_opy_ = cls.bstack1ll1ll1111l1_opy_(response)
            return bstack1ll1ll11l1l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧ╯").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l11l11l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def stop(cls, bstack1ll1l1llllll_opy_=None):
        if not bstack11lll1l11_opy_.on() and not a11y.on():
            return
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ╰")) == bstack1ll1lll_opy_ (u"ࠤࡱࡹࡱࡲࠢ╱") or os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ╲")) == bstack1ll1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ╳"):
            logger.error(bstack1ll1lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ╴"))
            return {
                bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭╵"): bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭╶"),
                bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ╷"): bstack1ll1lll_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧ╸")
            }
        try:
            cls.bstack1ll1llllllll_opy_.shutdown()
            data = {
                bstack1ll1lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ╹"): current_time()
            }
            if not bstack1ll1l1llllll_opy_ is None:
                data[bstack1ll1lll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ╺")] = [{
                    bstack1ll1lll_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ╻"): bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ╼"),
                    bstack1ll1lll_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ╽"): bstack1ll1l1llllll_opy_
                }]
            config = {
                bstack1ll1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ╾"): cls.default_headers()
            }
            bstack111ll1111l1_opy_ = bstack1ll1lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ╿").format(os.environ[bstack1ll1lll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ▀")])
            bstack1ll1l1lll1l1_opy_ = cls.request_url(bstack111ll1111l1_opy_)
            response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠫࡕ࡛ࡔࠨ▁"), bstack1ll1l1lll1l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll1lll_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦ▂"))
        except Exception as error:
            logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ▃") + str(error))
            return {
                bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ▄"): bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ▅"),
                bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ▆"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1ll1111l1_opy_(cls, response):
        bstack11lll11l1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1ll11l1l1_opy_ = {}
        if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪ࡮ࡼࡺࠧ▇")) is None:
            os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ█")] = bstack1ll1lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ▉")
        else:
            os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ▊")] = bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠧ࡫ࡹࡷࠫ▋"), bstack1ll1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭▌"))
        os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ▍")] = bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ▎"), bstack1ll1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ▏"))
        logger.info(bstack1ll1lll_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ▐") + os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ░")));
        if bstack11lll1l11_opy_.bstack1ll1l1lll111_opy_(cls.bs_config, cls.bstack1l1ll11l11_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ▒"), bstack1ll1lll_opy_ (u"ࠨࠩ▓"))) is True:
            bstack1ll1llll11ll_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1l1ll1ll1_opy_(bstack11lll11l1l_opy_)
            if bstack1ll1llll11ll_opy_ != None and build_hashed_id != None:
                bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ▔")] = {
                    bstack1ll1lll_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭▕"): bstack1ll1llll11ll_opy_,
                    bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭▖"): build_hashed_id,
                    bstack1ll1lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ▗"): allow_screenshots
                }
            else:
                bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭▘")] = {}
        else:
            bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ▙")] = {}
        bstack1ll1ll1111ll_opy_, build_hashed_id = cls.bstack1ll1ll111lll_opy_(bstack11lll11l1l_opy_)
        if bstack1ll1ll1111ll_opy_ != None and build_hashed_id != None:
            bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ▚")] = {
                bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭▛"): bstack1ll1ll1111ll_opy_,
                bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ▜"): build_hashed_id,
            }
        else:
            bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ▝")] = {}
        if bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▞")].get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ▟")) != None or bstack1ll1ll11l1l1_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ■")].get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ□")) != None:
            cls.bstack1ll1l1ll1lll_opy_(bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠩ࡭ࡻࡹ࠭▢")), bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ▣")))
        return bstack1ll1ll11l1l1_opy_
    @classmethod
    def bstack1ll1l1ll1ll1_opy_(cls, bstack11lll11l1l_opy_):
        if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ▤")) == None:
            cls.bstack1ll1l1lll11l_opy_()
            return [None, None, None]
        if bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▥")][bstack1ll1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ▦")] != True:
            cls.bstack1ll1l1lll11l_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ▧")])
            return [None, None, None]
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ▨").format(bstack11l11lll11_opy_))
        os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ▩")] = bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ▪")
        if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫ࡯ࡽࡴࠨ▫")):
            os.environ[bstack1ll1lll_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ▬")] = json.dumps({
                bstack1ll1lll_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ▭"): bstack111ll11l11l_opy_(cls.bs_config),
                bstack1ll1lll_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ▮"): bstack111lll1llll_opy_(cls.bs_config)
            })
        if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▯")):
            os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ▰")] = bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ▱")]
        if bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ▲")].get(bstack1ll1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭△"), {}).get(bstack1ll1lll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ▴")):
            os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ▵")] = str(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ▶")][bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ▷")][bstack1ll1lll_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ▸")])
        else:
            os.environ[bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ▹")] = bstack1ll1lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ►")
        return [bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡪࡸࡶࠪ▻")], bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ▼")], os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ▽")]]
    @classmethod
    def bstack1ll1ll111lll_opy_(cls, bstack11lll11l1l_opy_):
        if bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ▾")) == None:
            cls.bstack1ll1l1lllll1_opy_()
            return [None, None]
        if bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ▿")][bstack1ll1lll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ◀")] != True:
            cls.bstack1ll1l1lllll1_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ◁")])
            return [None, None]
        if bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭◂")].get(bstack1ll1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ◃")):
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ◄"))
            parsed = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ◅"), bstack1ll1lll_opy_ (u"ࠪࡿࢂ࠭◆")))
            capabilities = TestHubUtils.bstack1ll1ll111l11_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ◇")][bstack1ll1lll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭◈")][bstack1ll1lll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ◉")], bstack1ll1lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ◊"), bstack1ll1lll_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧ○"))
            bstack1ll1ll1111ll_opy_ = capabilities[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ◌")]
            os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ◍")] = bstack1ll1ll1111ll_opy_
            if capabilities.get(bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ◎")):
                os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡔࡆࡕࡗࡣࡗ࡛ࡎࡠࡋࡇࠫ●")] = str(capabilities[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫ◐")])
            if capabilities.get(bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠬ◑")):
                os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉ࠭◒")] = str(capabilities[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠧ◓")])
            if bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ◔") in bstack11lll11l1l_opy_ and bstack11lll11l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ◕")) is None:
                parsed[bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭◖")] = capabilities[bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ◗")]
            os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ◘")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll1ll111l11_opy_(bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ◙")][bstack1ll1lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ◚")][bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ◛")], bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ◜"), bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭◝"))
            accessibility_scripts.bstack11lll1ll_opy_(scripts)
            commands_to_wrap = bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭◞")][bstack1ll1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ◟")][bstack1ll1lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ◠")]
            commands = commands_to_wrap.get(bstack1ll1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ◡"))
            accessibility_scripts.bstack111ll1ll1l1_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠩ◢"))
            accessibility_scripts.bstack111ll111l1l_opy_(scripts_to_run)
            bstack111ll1lll11_opy_ = capabilities.get(bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ◣"))
            accessibility_scripts.bstack111ll1111ll_opy_(bstack111ll1lll11_opy_)
            accessibility_scripts.store()
        return [bstack1ll1ll1111ll_opy_, bstack11lll11l1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ◤")]]
    @classmethod
    def bstack1ll1l1lll11l_opy_(cls, response=None):
        os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ◥")] = bstack1ll1lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ◦")
        os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ◧")] = bstack1ll1lll_opy_ (u"ࠩࡱࡹࡱࡲࠧ◨")
        os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ◩")] = bstack1ll1lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ◪")
        os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ◫")] = bstack1ll1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ◬")
        os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ◭")] = bstack1ll1lll_opy_ (u"ࠣࡰࡸࡰࡱࠨ◮")
        cls.bstack1ll1l1llll1l_opy_(response, bstack1ll1lll_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ◯"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1lllll1_opy_(cls, response=None):
        os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ◰")] = bstack1ll1lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ◱")
        os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ◲")] = bstack1ll1lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ◳")
        os.environ[bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ◴")] = bstack1ll1lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭◵")
        cls.bstack1ll1l1llll1l_opy_(response, bstack1ll1lll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ◶"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1ll1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ◷")] = jwt
        os.environ[bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ◸")] = build_hashed_id
    @classmethod
    def bstack1ll1l1llll1l_opy_(cls, response=None, product=bstack1ll1lll_opy_ (u"ࠧࠨ◹")):
        if response == None or response.get(bstack1ll1lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭◺")) == None:
            logger.error(product + bstack1ll1lll_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤ◻"))
            return
        for error in response[bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ◼")]:
            bstack111111l1l1l_opy_ = error[bstack1ll1lll_opy_ (u"ࠩ࡮ࡩࡾ࠭◽")]
            error_message = error[bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ◾")]
            if error_message:
                if bstack111111l1l1l_opy_ == bstack1ll1lll_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥ◿"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll1lll_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨ☀") + product + bstack1ll1lll_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ☁"))
    @classmethod
    def bstack1ll1ll11111l_opy_(cls):
        if cls.bstack1ll1llllllll_opy_ is not None:
            return
        cls.bstack1ll1llllllll_opy_ = bstack1lll11111111_opy_(cls.post_data)
        cls.bstack1ll1llllllll_opy_.start()
    @classmethod
    def bstack1llll1l1l11_opy_(cls):
        if cls.bstack1ll1llllllll_opy_ is None:
            return
        cls.bstack1ll1llllllll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1llll1lll11_opy_, event_url=bstack1ll1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭☂")):
        config = {
            bstack1ll1lll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ☃"): cls.default_headers()
        }
        logger.debug(bstack1ll1lll_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ☄").format(bstack1ll1lll_opy_ (u"ࠪ࠰ࠥ࠭★").join([event[bstack1ll1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☆")] for event in bstack1llll1lll11_opy_])))
        response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠬࡖࡏࡔࡖࠪ☇"), cls.request_url(event_url), bstack1llll1lll11_opy_, config)
        bstack111ll11ll1l_opy_ = response.json()
    @classmethod
    def bstack11l1ll111l_opy_(cls, bstack1llll1lll11_opy_, event_url=bstack1ll1lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ☈")):
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ☉").format(bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ☊")]))
        if not TestHubUtils.bstack1ll1l1ll1l11_opy_(bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭☋")]):
            logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ☌").format(bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☍")]))
            return
        bstack11l11l111l_opy_ = TestHubUtils.bstack1ll1ll11l11l_opy_(bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ☎")], bstack1llll1lll11_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ☏")))
        if bstack11l11l111l_opy_ != None:
            if bstack1llll1lll11_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ☐")) != None:
                bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ☑")][bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ☒")] = bstack11l11l111l_opy_
            else:
                bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ☓")] = bstack11l11l111l_opy_
        if event_url == bstack1ll1lll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ☔"):
            cls.bstack1ll1ll11111l_opy_()
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ☕").format(bstack1llll1lll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ☖")]))
            cls.bstack1ll1llllllll_opy_.add(bstack1llll1lll11_opy_)
        elif event_url == bstack1ll1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ☗"):
            cls.post_data([bstack1llll1lll11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11lllll111_opy_(cls, logs):
        for log in logs:
            bstack1ll1ll111ll1_opy_ = {
                bstack1ll1lll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭☘"): bstack1ll1lll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ☙"),
                bstack1ll1lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ☚"): log[bstack1ll1lll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ☛")],
                bstack1ll1lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ☜"): log[bstack1ll1lll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ☝")],
                bstack1ll1lll_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ☞"): {},
                bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ☟"): log[bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ☠")],
            }
            if bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☡") in log:
                bstack1ll1ll111ll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☢")] = log[bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☣")]
            elif bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☤") in log:
                bstack1ll1ll111ll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ☥")] = log[bstack1ll1lll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☦")]
            cls.bstack11l1ll111l_opy_({
                bstack1ll1lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭☧"): bstack1ll1lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ☨"),
                bstack1ll1lll_opy_ (u"ࠫࡱࡵࡧࡴࠩ☩"): [bstack1ll1ll111ll1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1l1ll1l1l_opy_(cls, steps):
        bstack1ll1l1ll11ll_opy_ = []
        for step in steps:
            bstack1ll1ll111111_opy_ = {
                bstack1ll1lll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ☪"): bstack1ll1lll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ☫"),
                bstack1ll1lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭☬"): step[bstack1ll1lll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ☭")],
                bstack1ll1lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ☮"): step[bstack1ll1lll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭☯")],
                bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ☰"): step[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭☱")],
                bstack1ll1lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ☲"): step[bstack1ll1lll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ☳")]
            }
            if bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☴") in step:
                bstack1ll1ll111111_opy_[bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☵")] = step[bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☶")]
            elif bstack1ll1lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☷") in step:
                bstack1ll1ll111111_opy_[bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☸")] = step[bstack1ll1lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☹")]
            bstack1ll1l1ll11ll_opy_.append(bstack1ll1ll111111_opy_)
        cls.bstack11l1ll111l_opy_({
            bstack1ll1lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ☺"): bstack1ll1lll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ☻"),
            bstack1ll1lll_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ☼"): bstack1ll1l1ll11ll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111111ll_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack11lll1l11l_opy_(cls, screenshot):
        cls.bstack11l1ll111l_opy_({
            bstack1ll1lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ☽"): bstack1ll1lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ☾"),
            bstack1ll1lll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ☿"): [{
                bstack1ll1lll_opy_ (u"࠭࡫ࡪࡰࡧࠫ♀"): bstack1ll1lll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ♁"),
                bstack1ll1lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ♂"): datetime.datetime.utcnow().isoformat() + bstack1ll1lll_opy_ (u"ࠩ࡝ࠫ♃"),
                bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ♄"): screenshot[bstack1ll1lll_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ♅")],
                bstack1ll1lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ♆"): screenshot[bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭♇")]
            }]
        }, event_url=bstack1ll1lll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ♈"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1ll111l_opy_({
            bstack1ll1lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ♉"): bstack1ll1lll_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭♊"),
            bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ♋"): {
                bstack1ll1lll_opy_ (u"ࠦࡺࡻࡩࡥࠤ♌"): cls.current_test_uuid(),
                bstack1ll1lll_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ♍"): cls.bstack1llllllll11_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1llll1lll11_opy_: bstack1llll1l11l1_opy_):
        bstack1lllll11ll1_opy_ = {
            bstack1ll1lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ♎"): event,
            bstack1llll1lll11_opy_.bstack1lllll1l111_opy_(): bstack1llll1lll11_opy_.bstack1lll1llll11_opy_(event)
        }
        cls.bstack11l1ll111l_opy_(bstack1lllll11ll1_opy_)
        result = getattr(bstack1llll1lll11_opy_, bstack1ll1lll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ♏"), None)
        if event == bstack1ll1lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ♐"):
            threading.current_thread().bstackTestMeta = {bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ♑"): bstack1ll1lll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ♒")}
        elif event == bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭♓"):
            threading.current_thread().bstackTestMeta = {bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ♔"): getattr(result, bstack1ll1lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭♕"), bstack1ll1lll_opy_ (u"ࠧࠨ♖"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ♗"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭♘")] == bstack1ll1lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ♙")) and (os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ♚"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ♛")] == bstack1ll1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ♜")):
            return False
        return True
    @staticmethod
    def bstack1ll1ll11l111_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll1lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭♝"): bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ♞"),
            bstack1ll1lll_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬ♟"): bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ♠")
        }
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ♡"), None):
            headers[bstack1ll1lll_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ♢")] = bstack1ll1lll_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ♣").format(os.environ[bstack1ll1lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ♤")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll1lll_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ♥").format(bstack1ll1l1llll11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭♦"), None)
    @staticmethod
    def bstack1llllllll11_opy_(driver):
        return {
            bstack11111llll11_opy_(): bstack1111l1ll1ll_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l1lll1ll_opy_(exception_info, report):
        return [{bstack1ll1lll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭♧"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll1llll1ll_opy_(typename):
        if bstack1ll1lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ♨") in typename:
            return bstack1ll1lll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ♩")
        return bstack1ll1lll_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ♪")