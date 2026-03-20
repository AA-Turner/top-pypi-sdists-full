# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111llll11l1_opy_, bstack111ll1l1l11_opy_, bstack11l1lll11_opy_, error_handler, bstack1111l1llll1_opy_, bstack1111ll1lll1_opy_, bstack1111l1l1l11_opy_, current_time, bstack111ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11111lll_opy_ import bstack1lll1111111l_opy_
import bstack_utils.bstack11l1l1l11l_opy_ as TestHubUtils
from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.test_data import bstack1llll1l1l1l_opy_
from bstack_utils.constants import bstack1ll11ll11l_opy_
bstack1ll1ll11ll11_opy_ = bstack11lll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ╡")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll11111lll_opy_ = None
    bs_config = None
    bstack1l11l11l1l_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l11l111l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def launch(cls, bs_config, bstack1l11l11l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11l11l1l_opy_ = bstack1l11l11l1l_opy_
        try:
            cls.bstack1ll1l1lll1l1_opy_()
            bstack111ll11lll1_opy_ = bstack111llll11l1_opy_(bs_config)
            bstack111llll111l_opy_ = bstack111ll1l1l11_opy_(bs_config)
            data = TestHubUtils.bstack1ll1ll11l1ll_opy_(bs_config, bstack1l11l11l1l_opy_)
            config = {
                bstack11lll1_opy_ (u"ࠨࡣࡸࡸ࡭࠭╢"): (bstack111ll11lll1_opy_, bstack111llll111l_opy_),
                bstack11lll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ╣"): cls.default_headers()
            }
            response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ╤"), cls.request_url(bstack11lll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ╥")), data, config)
            if response.status_code != 200:
                bstack1l11l1ll_opy_ = response.json()
                if bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭╦")] == False:
                    cls.bstack1ll1ll11111l_opy_(bstack1l11l1ll_opy_)
                    return
                cls.bstack1ll1ll111lll_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭╧")])
                cls.bstack1ll1ll1111l1_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ╨")])
                return None
            bstack1ll1ll11l1l1_opy_ = cls.bstack1ll1l1ll1ll1_opy_(response)
            return bstack1ll1ll11l1l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack11lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ╩").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1l1ll1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def stop(cls, bstack1ll1l1lll11l_opy_=None):
        if not bstack1ll1l1l1l1_opy_.on() and not a11y.on():
            return
        if os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭╪")) == bstack11lll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ╫") or os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ╬")) == bstack11lll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ╭"):
            logger.error(bstack11lll1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ╮"))
            return {
                bstack11lll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ╯"): bstack11lll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ╰"),
                bstack11lll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ╱"): bstack11lll1_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ╲")
            }
        try:
            cls.bstack1lll11111lll_opy_.shutdown()
            data = {
                bstack11lll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ╳"): current_time()
            }
            if not bstack1ll1l1lll11l_opy_ is None:
                data[bstack11lll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ╴")] = [{
                    bstack11lll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭╵"): bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ╶"),
                    bstack11lll1_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ╷"): bstack1ll1l1lll11l_opy_
                }]
            config = {
                bstack11lll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ╸"): cls.default_headers()
            }
            bstack111ll111l1l_opy_ = bstack11lll1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫ╹").format(os.environ[bstack11lll1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ╺")])
            bstack1ll1l1lll1ll_opy_ = cls.request_url(bstack111ll111l1l_opy_)
            response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠬࡖࡕࡕࠩ╻"), bstack1ll1l1lll1ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lll1_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ╼"))
        except Exception as error:
            logger.error(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦ╽") + str(error))
            return {
                bstack11lll1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ╾"): bstack11lll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ╿"),
                bstack11lll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ▀"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1l1ll1ll1_opy_(cls, response):
        bstack1l11l1ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1ll11l1l1_opy_ = {}
        if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠫ࡯ࡽࡴࠨ▁")) is None:
            os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ▂")] = bstack11lll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ▃")
        else:
            os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ▄")] = bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠨ࡬ࡺࡸࠬ▅"), bstack11lll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ▆"))
        os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ▇")] = bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭█"), bstack11lll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ▉"))
        logger.info(bstack11lll1_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ▊") + os.getenv(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ▋")));
        if bstack1ll1l1l1l1_opy_.bstack1ll1l1ll1lll_opy_(cls.bs_config, cls.bstack1l11l11l1l_opy_.get(bstack11lll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ▌"), bstack11lll1_opy_ (u"ࠩࠪ▍"))) is True:
            bstack1ll1lllll1l1_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1ll1111ll_opy_(bstack1l11l1ll_opy_)
            if bstack1ll1lllll1l1_opy_ != None and build_hashed_id != None:
                bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ▎")] = {
                    bstack11lll1_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧ▏"): bstack1ll1lllll1l1_opy_,
                    bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ▐"): build_hashed_id,
                    bstack11lll1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ░"): allow_screenshots
                }
            else:
                bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ▒")] = {}
        else:
            bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ▓")] = {}
        bstack1ll1ll11ll1l_opy_, build_hashed_id = cls.bstack1ll1l1lllll1_opy_(bstack1l11l1ll_opy_)
        if bstack1ll1ll11ll1l_opy_ != None and build_hashed_id != None:
            bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ▔")] = {
                bstack11lll1_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧ▕"): bstack1ll1ll11ll1l_opy_,
                bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭▖"): build_hashed_id,
            }
        else:
            bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ▗")] = {}
        if bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭▘")].get(bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ▙")) != None or bstack1ll1ll11l1l1_opy_[bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ▚")].get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ▛")) != None:
            cls.bstack1ll1ll111ll1_opy_(bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠪ࡮ࡼࡺࠧ▜")), bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭▝")))
        return bstack1ll1ll11l1l1_opy_
    @classmethod
    def bstack1ll1ll1111ll_opy_(cls, bstack1l11l1ll_opy_):
        if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▞")) == None:
            cls.bstack1ll1ll111lll_opy_()
            return [None, None, None]
        if bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭▟")][bstack11lll1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ■")] != True:
            cls.bstack1ll1ll111lll_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ□")])
            return [None, None, None]
        logger.debug(bstack11lll1_opy_ (u"ࠩࡾࢁࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ▢").format(bstack1ll11ll11l_opy_))
        os.environ[bstack11lll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ▣")] = bstack11lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ▤")
        if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠬࡰࡷࡵࠩ▥")):
            os.environ[bstack11lll1_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ▦")] = json.dumps({
                bstack11lll1_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ▧"): bstack111llll11l1_opy_(cls.bs_config),
                bstack11lll1_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ▨"): bstack111ll1l1l11_opy_(cls.bs_config)
            })
        if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ▩")):
            os.environ[bstack11lll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ▪")] = bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭▫")]
        if bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▬")].get(bstack11lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ▭"), {}).get(bstack11lll1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ▮")):
            os.environ[bstack11lll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ▯")] = str(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ▰")][bstack11lll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ▱")][bstack11lll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ▲")])
        else:
            os.environ[bstack11lll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭△")] = bstack11lll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ▴")
        return [bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠧ࡫ࡹࡷࠫ▵")], bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▶")], os.environ[bstack11lll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ▷")]]
    @classmethod
    def bstack1ll1l1lllll1_opy_(cls, bstack1l11l1ll_opy_):
        if bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ▸")) == None:
            cls.bstack1ll1ll1111l1_opy_()
            return [None, None]
        if bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ▹")][bstack11lll1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭►")] != True:
            cls.bstack1ll1ll1111l1_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭▻")])
            return [None, None]
        if bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ▼")].get(bstack11lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ▽")):
            logger.debug(bstack11lll1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭▾"))
            parsed = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ▿"), bstack11lll1_opy_ (u"ࠫࢀࢃࠧ◀")))
            capabilities = TestHubUtils.bstack1ll1ll11l11l_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ◁")][bstack11lll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ◂")][bstack11lll1_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭◃")], bstack11lll1_opy_ (u"ࠨࡰࡤࡱࡪ࠭◄"), bstack11lll1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ◅"))
            bstack1ll1ll11ll1l_opy_ = capabilities[bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ◆")]
            os.environ[bstack11lll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ◇")] = bstack1ll1ll11ll1l_opy_
            if capabilities.get(bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪ◈")):
                os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬ◉")] = str(capabilities[bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ◊")])
            if capabilities.get(bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩ࠭○")):
                os.environ[bstack11lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡆ࡚ࡏࡌࡅࡡࡘ࡙ࡎࡊࠧ◌")] = str(capabilities[bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠨ◍")])
            if bstack11lll1_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ◎") in bstack1l11l1ll_opy_ and bstack1l11l1ll_opy_.get(bstack11lll1_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ●")) is None:
                parsed[bstack11lll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ◐")] = capabilities[bstack11lll1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ◑")]
            os.environ[bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ◒")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll1ll11l11l_opy_(bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ◓")][bstack11lll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ◔")][bstack11lll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ◕")], bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ◖"), bstack11lll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧ◗"))
            accessibility_scripts.bstack11lll1l11_opy_(scripts)
            commands_to_wrap = bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ◘")][bstack11lll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ◙")][bstack11lll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪ◚")]
            commands = commands_to_wrap.get(bstack11lll1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬ◛"))
            accessibility_scripts.bstack111ll1lll11_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack11lll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ࡙ࡵࡒࡶࡰࠪ◜"))
            accessibility_scripts.bstack111ll11l1ll_opy_(scripts_to_run)
            bstack111ll1l1111_opy_ = capabilities.get(bstack11lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ◝"))
            accessibility_scripts.bstack111ll11l1l1_opy_(bstack111ll1l1111_opy_)
            accessibility_scripts.store()
        return [bstack1ll1ll11ll1l_opy_, bstack1l11l1ll_opy_[bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ◞")]]
    @classmethod
    def bstack1ll1ll111lll_opy_(cls, response=None):
        os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ◟")] = bstack11lll1_opy_ (u"ࠨࡰࡸࡰࡱ࠭◠")
        os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭◡")] = bstack11lll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ◢")
        os.environ[bstack11lll1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ◣")] = bstack11lll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ◤")
        os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ◥")] = bstack11lll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ◦")
        os.environ[bstack11lll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ◧")] = bstack11lll1_opy_ (u"ࠤࡱࡹࡱࡲࠢ◨")
        cls.bstack1ll1ll11111l_opy_(response, bstack11lll1_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ◩"))
        return [None, None, None]
    @classmethod
    def bstack1ll1ll1111l1_opy_(cls, response=None):
        os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ◪")] = bstack11lll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ◫")
        os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ◬")] = bstack11lll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ◭")
        os.environ[bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ◮")] = bstack11lll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ◯")
        cls.bstack1ll1ll11111l_opy_(response, bstack11lll1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ◰"))
        return [None, None, None]
    @classmethod
    def bstack1ll1ll111ll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ◱")] = jwt
        os.environ[bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ◲")] = build_hashed_id
    @classmethod
    def bstack1ll1ll11111l_opy_(cls, response=None, product=bstack11lll1_opy_ (u"ࠨࠢ◳")):
        if response == None or response.get(bstack11lll1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ◴")) == None:
            logger.error(product + bstack11lll1_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ◵"))
            return
        for error in response[bstack11lll1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ◶")]:
            bstack11111l1llll_opy_ = error[bstack11lll1_opy_ (u"ࠪ࡯ࡪࡿࠧ◷")]
            error_message = error[bstack11lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ◸")]
            if error_message:
                if bstack11111l1llll_opy_ == bstack11lll1_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ◹"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lll1_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ◺") + product + bstack11lll1_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ◻"))
    @classmethod
    def bstack1ll1l1lll1l1_opy_(cls):
        if cls.bstack1lll11111lll_opy_ is not None:
            return
        cls.bstack1lll11111lll_opy_ = bstack1lll1111111l_opy_(cls.post_data)
        cls.bstack1lll11111lll_opy_.start()
    @classmethod
    def bstack1llll1l11l1_opy_(cls):
        if cls.bstack1lll11111lll_opy_ is None:
            return
        cls.bstack1lll11111lll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1llll111lll_opy_, event_url=bstack11lll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ◼")):
        config = {
            bstack11lll1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ◽"): cls.default_headers()
        }
        logger.debug(bstack11lll1_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ◾").format(bstack11lll1_opy_ (u"ࠫ࠱ࠦࠧ◿").join([event[bstack11lll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ☀")] for event in bstack1llll111lll_opy_])))
        response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"࠭ࡐࡐࡕࡗࠫ☁"), cls.request_url(event_url), bstack1llll111lll_opy_, config)
        bstack111llll1l11_opy_ = response.json()
    @classmethod
    def bstack1l1llll1l_opy_(cls, bstack1llll111lll_opy_, event_url=bstack11lll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭☂")):
        logger.debug(bstack11lll1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ☃").format(bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭☄")]))
        if not TestHubUtils.bstack1ll1l1llll1l_opy_(bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ★")]):
            logger.debug(bstack11lll1_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ☆").format(bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ☇")]))
            return
        bstack1ll11l1l11_opy_ = TestHubUtils.bstack1ll1ll111111_opy_(bstack1llll111lll_opy_[bstack11lll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ☈")], bstack1llll111lll_opy_.get(bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ☉")))
        if bstack1ll11l1l11_opy_ != None:
            if bstack1llll111lll_opy_.get(bstack11lll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ☊")) != None:
                bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ☋")][bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ☌")] = bstack1ll11l1l11_opy_
            else:
                bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ☍")] = bstack1ll11l1l11_opy_
        if event_url == bstack11lll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ☎"):
            cls.bstack1ll1l1lll1l1_opy_()
            logger.debug(bstack11lll1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ☏").format(bstack1llll111lll_opy_[bstack11lll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ☐")]))
            cls.bstack1lll11111lll_opy_.add(bstack1llll111lll_opy_)
        elif event_url == bstack11lll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭☑"):
            cls.post_data([bstack1llll111lll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1111l1ll_opy_(cls, logs):
        for log in logs:
            bstack1ll1l1llllll_opy_ = {
                bstack11lll1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ☒"): bstack11lll1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ☓"),
                bstack11lll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ☔"): log[bstack11lll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ☕")],
                bstack11lll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ☖"): log[bstack11lll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ☗")],
                bstack11lll1_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ☘"): {},
                bstack11lll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ☙"): log[bstack11lll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ☚")],
            }
            if bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☛") in log:
                bstack1ll1l1llllll_opy_[bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☜")] = log[bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☝")]
            elif bstack11lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ☞") in log:
                bstack1ll1l1llllll_opy_[bstack11lll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☟")] = log[bstack11lll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☠")]
            cls.bstack1l1llll1l_opy_({
                bstack11lll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ☡"): bstack11lll1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ☢"),
                bstack11lll1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ☣"): [bstack1ll1l1llllll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1ll111l11_opy_(cls, steps):
        bstack1ll1l1llll11_opy_ = []
        for step in steps:
            bstack1ll1l1lll111_opy_ = {
                bstack11lll1_opy_ (u"࠭࡫ࡪࡰࡧࠫ☤"): bstack11lll1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ☥"),
                bstack11lll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ☦"): step[bstack11lll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ☧")],
                bstack11lll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭☨"): step[bstack11lll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ☩")],
                bstack11lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭☪"): step[bstack11lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ☫")],
                bstack11lll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ☬"): step[bstack11lll1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ☭")]
            }
            if bstack11lll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☮") in step:
                bstack1ll1l1lll111_opy_[bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☯")] = step[bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☰")]
            elif bstack11lll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☱") in step:
                bstack1ll1l1lll111_opy_[bstack11lll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☲")] = step[bstack11lll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ☳")]
            bstack1ll1l1llll11_opy_.append(bstack1ll1l1lll111_opy_)
        cls.bstack1l1llll1l_opy_({
            bstack11lll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ☴"): bstack11lll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭☵"),
            bstack11lll1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ☶"): bstack1ll1l1llll11_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l1ll1l1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11lll11_opy_(cls, screenshot):
        cls.bstack1l1llll1l_opy_({
            bstack11lll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☷"): bstack11lll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ☸"),
            bstack11lll1_opy_ (u"࠭࡬ࡰࡩࡶࠫ☹"): [{
                bstack11lll1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ☺"): bstack11lll1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ☻"),
                bstack11lll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ☼"): datetime.datetime.utcnow().isoformat() + bstack11lll1_opy_ (u"ࠪ࡞ࠬ☽"),
                bstack11lll1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ☾"): screenshot[bstack11lll1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ☿")],
                bstack11lll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭♀"): screenshot[bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ♁")]
            }]
        }, event_url=bstack11lll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭♂"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1llll1l_opy_({
            bstack11lll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭♃"): bstack11lll1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ♄"),
            bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭♅"): {
                bstack11lll1_opy_ (u"ࠧࡻࡵࡪࡦࠥ♆"): cls.current_test_uuid(),
                bstack11lll1_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ♇"): cls.bstack1llllll1ll1_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1llll111lll_opy_: bstack1llll1l1l1l_opy_):
        bstack1llll11ll11_opy_ = {
            bstack11lll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ♈"): event,
            bstack1llll111lll_opy_.bstack1llll1l1ll1_opy_(): bstack1llll111lll_opy_.bstack1llll11l1ll_opy_(event)
        }
        cls.bstack1l1llll1l_opy_(bstack1llll11ll11_opy_)
        result = getattr(bstack1llll111lll_opy_, bstack11lll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ♉"), None)
        if event == bstack11lll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ♊"):
            threading.current_thread().bstackTestMeta = {bstack11lll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ♋"): bstack11lll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ♌")}
        elif event == bstack11lll1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ♍"):
            threading.current_thread().bstackTestMeta = {bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭♎"): getattr(result, bstack11lll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ♏"), bstack11lll1_opy_ (u"ࠨࠩ♐"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭♑"), None) is None or os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ♒")] == bstack11lll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ♓")) and (os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ♔"), None) is None or os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ♕")] == bstack11lll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ♖")):
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
            bstack11lll1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ♗"): bstack11lll1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ♘"),
            bstack11lll1_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭♙"): bstack11lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩ♚")
        }
        if os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ♛"), None):
            headers[bstack11lll1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭♜")] = bstack11lll1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ♝").format(os.environ[bstack11lll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ♞")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11lll1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ♟").format(bstack1ll1ll11ll11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ♠"), None)
    @staticmethod
    def bstack1llllll1ll1_opy_(driver):
        return {
            bstack1111l1llll1_opy_(): bstack1111ll1lll1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1ll111l1l_opy_(exception_info, report):
        return [{bstack11lll1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ♡"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll1lllll11_opy_(typename):
        if bstack11lll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ♢") in typename:
            return bstack11lll1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ♣")
        return bstack11lll1_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ♤")