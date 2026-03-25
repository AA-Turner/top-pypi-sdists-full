# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111ll1ll111_opy_, bstack111ll1lll1l_opy_, bstack1l111l1111_opy_, error_handler, bstack1111l1ll1ll_opy_, bstack111111ll11l_opy_, bstack11111l1111l_opy_, current_time, bstack1l1lll111l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11111l11_opy_ import bstack1lll11111l1l_opy_
import bstack_utils.bstack111111111_opy_ as TestHubUtils
from bstack_utils.bstack1llll11lll_opy_ import bstack1111l1lll1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.test_data import bstack1llll1ll111_opy_
from bstack_utils.constants import bstack1ll1l111_opy_
bstack1ll1ll111l1l_opy_ = bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ╬")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll11111l11_opy_ = None
    bs_config = None
    bstack11lll11l11_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1l11l1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def launch(cls, bs_config, bstack11lll11l11_opy_):
        cls.bs_config = bs_config
        cls.bstack11lll11l11_opy_ = bstack11lll11l11_opy_
        try:
            cls.bstack1ll1ll1111ll_opy_()
            bstack111ll1ll1l1_opy_ = bstack111ll1ll111_opy_(bs_config)
            bstack111ll1lll11_opy_ = bstack111ll1lll1l_opy_(bs_config)
            data = TestHubUtils.bstack1ll1ll111111_opy_(bs_config, bstack11lll11l11_opy_)
            config = {
                bstack1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪ╭"): (bstack111ll1ll1l1_opy_, bstack111ll1lll11_opy_),
                bstack1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ╮"): cls.default_headers()
            }
            response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠧࡑࡑࡖࡘࠬ╯"), cls.request_url(bstack1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨ╰")), data, config)
            if response.status_code != 200:
                bstack111l1llll_opy_ = response.json()
                if bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ╱")] == False:
                    cls.bstack1ll1l1llllll_opy_(bstack111l1llll_opy_)
                    return
                cls.bstack1ll1l1ll1ll1_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ╲")])
                cls.bstack1ll1l1lll11l_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ╳")])
                return None
            bstack1ll1ll11l111_opy_ = cls.bstack1ll1l1ll11l1_opy_(response)
            return bstack1ll1ll11l111_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥ╴").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l11lll1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def stop(cls, bstack1ll1ll111lll_opy_=None):
        if not bstack1111l1lll1_opy_.on() and not a11y.on():
            return
        if os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ╵")) == bstack1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ╶") or os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭╷")) == bstack1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ╸"):
            logger.error(bstack1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭╹"))
            return {
                bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ╺"): bstack1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ╻"),
                bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ╼"): bstack1l1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬ╽")
            }
        try:
            cls.bstack1lll11111l11_opy_.shutdown()
            data = {
                bstack1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭╾"): current_time()
            }
            if not bstack1ll1ll111lll_opy_ is None:
                data[bstack1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭╿")] = [{
                    bstack1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ▀"): bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ▁"),
                    bstack1l1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ▂"): bstack1ll1ll111lll_opy_
                }]
            config = {
                bstack1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ▃"): cls.default_headers()
            }
            bstack111ll111111_opy_ = bstack1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨ▄").format(os.environ[bstack1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ▅")])
            bstack1ll1ll11l11l_opy_ = cls.request_url(bstack111ll111111_opy_)
            response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠩࡓ࡙࡙࠭▆"), bstack1ll1ll11l11l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤ▇"))
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣ█") + str(error))
            return {
                bstack1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ▉"): bstack1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ▊"),
                bstack1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ▋"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1l1ll11l1_opy_(cls, response):
        bstack111l1llll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1ll11l111_opy_ = {}
        if bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠨ࡬ࡺࡸࠬ▌")) is None:
            os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭▍")] = bstack1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ▎")
        else:
            os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ▏")] = bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠬࡰࡷࡵࠩ▐"), bstack1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ░"))
        os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ▒")] = bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▓"), bstack1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ▔"))
        logger.info(bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ▕") + os.getenv(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ▖")));
        if bstack1111l1lll1_opy_.bstack1ll1ll1111l1_opy_(cls.bs_config, cls.bstack11lll11l11_opy_.get(bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭▗"), bstack1l1_opy_ (u"࠭ࠧ▘"))) is True:
            bstack1ll1lllll111_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1ll111ll1_opy_(bstack111l1llll_opy_)
            if bstack1ll1lllll111_opy_ != None and build_hashed_id != None:
                bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ▙")] = {
                    bstack1l1_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫ▚"): bstack1ll1lllll111_opy_,
                    bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ▛"): build_hashed_id,
                    bstack1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ▜"): allow_screenshots
                }
            else:
                bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ▝")] = {}
        else:
            bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▞")] = {}
        bstack1ll1l1lll1l1_opy_, build_hashed_id = cls.bstack1ll1l1ll1l1l_opy_(bstack111l1llll_opy_)
        if bstack1ll1l1lll1l1_opy_ != None and build_hashed_id != None:
            bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭▟")] = {
                bstack1l1_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ■"): bstack1ll1l1lll1l1_opy_,
                bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ□"): build_hashed_id,
            }
        else:
            bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ▢")] = {}
        if bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ▣")].get(bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭▤")) != None or bstack1ll1ll11l111_opy_[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ▥")].get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ▦")) != None:
            cls.bstack1ll1l1lll111_opy_(bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠧ࡫ࡹࡷࠫ▧")), bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▨")))
        return bstack1ll1ll11l111_opy_
    @classmethod
    def bstack1ll1ll111ll1_opy_(cls, bstack111l1llll_opy_):
        if bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ▩")) == None:
            cls.bstack1ll1l1ll1ll1_opy_()
            return [None, None, None]
        if bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ▪")][bstack1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ▫")] != True:
            cls.bstack1ll1l1ll1ll1_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▬")])
            return [None, None, None]
        logger.debug(bstack1l1_opy_ (u"࠭ࡻࡾࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ▭").format(bstack1ll1l111_opy_))
        os.environ[bstack1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭▮")] = bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭▯")
        if bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭▰")):
            os.environ[bstack1l1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ▱")] = json.dumps({
                bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭▲"): bstack111ll1ll111_opy_(cls.bs_config),
                bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ△"): bstack111ll1lll1l_opy_(cls.bs_config)
            })
        if bstack111l1llll_opy_.get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ▴")):
            os.environ[bstack1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭▵")] = bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▶")]
        if bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ▷")].get(bstack1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ▸"), {}).get(bstack1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ▹")):
            os.environ[bstack1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭►")] = str(bstack111l1llll_opy_[bstack1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭▻")][bstack1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ▼")][bstack1l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ▽")])
        else:
            os.environ[bstack1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ▾")] = bstack1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ▿")
        return [bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠫ࡯ࡽࡴࠨ◀")], bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ◁")], os.environ[bstack1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ◂")]]
    @classmethod
    def bstack1ll1l1ll1l1l_opy_(cls, bstack111l1llll_opy_):
        if bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ◃")) == None:
            cls.bstack1ll1l1lll11l_opy_()
            return [None, None]
        if bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ◄")][bstack1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ◅")] != True:
            cls.bstack1ll1l1lll11l_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ◆")])
            return [None, None]
        if bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ◇")].get(bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭◈")):
            logger.debug(bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ◉"))
            parsed = json.loads(os.getenv(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ◊"), bstack1l1_opy_ (u"ࠨࡽࢀࠫ○")))
            capabilities = TestHubUtils.bstack1ll1l1ll1l11_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ◌")][bstack1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ◍")][bstack1l1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ◎")], bstack1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ●"), bstack1l1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ◐"))
            bstack1ll1l1lll1l1_opy_ = capabilities[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ◑")]
            os.environ[bstack1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭◒")] = bstack1ll1l1lll1l1_opy_
            if capabilities.get(bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ◓")):
                os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣ࡙ࡋࡓࡕࡡࡕ࡙ࡓࡥࡉࡅࠩ◔")] = str(capabilities[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩ◕")])
            if capabilities.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠪ◖")):
                os.environ[bstack1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠫ◗")] = str(capabilities[bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠬ◘")])
            if bstack1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ◙") in bstack111l1llll_opy_ and bstack111l1llll_opy_.get(bstack1l1_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ◚")) is None:
                parsed[bstack1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ◛")] = capabilities[bstack1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ◜")]
            os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭◝")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll1l1ll1l11_opy_(bstack111l1llll_opy_[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭◞")][bstack1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ◟")][bstack1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ◠")], bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ◡"), bstack1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫ◢"))
            accessibility_scripts.bstack1llll11ll_opy_(scripts)
            commands_to_wrap = bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ◣")][bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭◤")][bstack1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧ◥")]
            commands = commands_to_wrap.get(bstack1l1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ◦"))
            accessibility_scripts.bstack111llll11l1_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧ◧"))
            accessibility_scripts.bstack111ll1111ll_opy_(scripts_to_run)
            bstack111lll1l1ll_opy_ = capabilities.get(bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ◨"))
            accessibility_scripts.bstack111ll111l11_opy_(bstack111lll1l1ll_opy_)
            accessibility_scripts.store()
        return [bstack1ll1l1lll1l1_opy_, bstack111l1llll_opy_[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ◩")]]
    @classmethod
    def bstack1ll1l1ll1ll1_opy_(cls, response=None):
        os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ◪")] = bstack1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ◫")
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ◬")] = bstack1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ◭")
        os.environ[bstack1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ◮")] = bstack1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ◯")
        os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ◰")] = bstack1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ◱")
        os.environ[bstack1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭◲")] = bstack1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ◳")
        cls.bstack1ll1l1llllll_opy_(response, bstack1l1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ◴"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1lll11l_opy_(cls, response=None):
        os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭◵")] = bstack1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ◶")
        os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ◷")] = bstack1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ◸")
        os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ◹")] = bstack1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ◺")
        cls.bstack1ll1l1llllll_opy_(response, bstack1l1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ◻"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1lll111_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ◼")] = jwt
        os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ◽")] = build_hashed_id
    @classmethod
    def bstack1ll1l1llllll_opy_(cls, response=None, product=bstack1l1_opy_ (u"ࠥࠦ◾")):
        if response == None or response.get(bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ◿")) == None:
            logger.error(product + bstack1l1_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ☀"))
            return
        for error in response[bstack1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭☁")]:
            bstack11111l11l11_opy_ = error[bstack1l1_opy_ (u"ࠧ࡬ࡧࡼࠫ☂")]
            error_message = error[bstack1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ☃")]
            if error_message:
                if bstack11111l11l11_opy_ == bstack1l1_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣ☄"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ★") + product + bstack1l1_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ☆"))
    @classmethod
    def bstack1ll1ll1111ll_opy_(cls):
        if cls.bstack1lll11111l11_opy_ is not None:
            return
        cls.bstack1lll11111l11_opy_ = bstack1lll11111l1l_opy_(cls.post_data)
        cls.bstack1lll11111l11_opy_.start()
    @classmethod
    def bstack1llll1l11l1_opy_(cls):
        if cls.bstack1lll11111l11_opy_ is None:
            return
        cls.bstack1lll11111l11_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1llll11llll_opy_, event_url=bstack1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ☇")):
        config = {
            bstack1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ☈"): cls.default_headers()
        }
        logger.debug(bstack1l1_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢ☉").format(bstack1l1_opy_ (u"ࠨ࠮ࠣࠫ☊").join([event[bstack1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭☋")] for event in bstack1llll11llll_opy_])))
        response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ☌"), cls.request_url(event_url), bstack1llll11llll_opy_, config)
        bstack111ll1l111l_opy_ = response.json()
    @classmethod
    def bstack11ll1l11ll_opy_(cls, bstack1llll11llll_opy_, event_url=bstack1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ☍")):
        logger.debug(bstack1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ☎").format(bstack1llll11llll_opy_[bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ☏")]))
        if not TestHubUtils.bstack1ll1l1lll1ll_opy_(bstack1llll11llll_opy_[bstack1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ☐")]):
            logger.debug(bstack1l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ☑").format(bstack1llll11llll_opy_[bstack1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭☒")]))
            return
        bstack1l1ll111l_opy_ = TestHubUtils.bstack1ll1ll111l11_opy_(bstack1llll11llll_opy_[bstack1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ☓")], bstack1llll11llll_opy_.get(bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭☔")))
        if bstack1l1ll111l_opy_ != None:
            if bstack1llll11llll_opy_.get(bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ☕")) != None:
                bstack1llll11llll_opy_[bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ☖")][bstack1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ☗")] = bstack1l1ll111l_opy_
            else:
                bstack1llll11llll_opy_[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭☘")] = bstack1l1ll111l_opy_
        if event_url == bstack1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ☙"):
            cls.bstack1ll1ll1111ll_opy_()
            logger.debug(bstack1l1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ☚").format(bstack1llll11llll_opy_[bstack1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ☛")]))
            cls.bstack1lll11111l11_opy_.add(bstack1llll11llll_opy_)
        elif event_url == bstack1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ☜"):
            cls.post_data([bstack1llll11llll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1llllll1l1_opy_(cls, logs):
        for log in logs:
            bstack1ll1l1ll1lll_opy_ = {
                bstack1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫ☝"): bstack1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ☞"),
                bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ☟"): log[bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ☠")],
                bstack1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭☡"): log[bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ☢")],
                bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ☣"): {},
                bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ☤"): log[bstack1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ☥")],
            }
            if bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☦") in log:
                bstack1ll1l1ll1lll_opy_[bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☧")] = log[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☨")]
            elif bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☩") in log:
                bstack1ll1l1ll1lll_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ☪")] = log[bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☫")]
            cls.bstack11ll1l11ll_opy_({
                bstack1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ☬"): bstack1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ☭"),
                bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ☮"): [bstack1ll1l1ll1lll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1l1ll11ll_opy_(cls, steps):
        bstack1ll1l1llll11_opy_ = []
        for step in steps:
            bstack1ll1l1llll1l_opy_ = {
                bstack1l1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ☯"): bstack1l1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ☰"),
                bstack1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ☱"): step[bstack1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ☲")],
                bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ☳"): step[bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ☴")],
                bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ☵"): step[bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ☶")],
                bstack1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭☷"): step[bstack1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ☸")]
            }
            if bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭☹") in step:
                bstack1ll1l1llll1l_opy_[bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ☺")] = step[bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ☻")]
            elif bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ☼") in step:
                bstack1ll1l1llll1l_opy_[bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ☽")] = step[bstack1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ☾")]
            bstack1ll1l1llll11_opy_.append(bstack1ll1l1llll1l_opy_)
        cls.bstack11ll1l11ll_opy_({
            bstack1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ☿"): bstack1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ♀"),
            bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ♁"): bstack1ll1l1llll11_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l1111l1_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l1llll11_opy_(cls, screenshot):
        cls.bstack11ll1l11ll_opy_({
            bstack1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ♂"): bstack1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭♃"),
            bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ♄"): [{
                bstack1l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ♅"): bstack1l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧ♆"),
                bstack1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ♇"): datetime.datetime.utcnow().isoformat() + bstack1l1_opy_ (u"࡛ࠧࠩ♈"),
                bstack1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ♉"): screenshot[bstack1l1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ♊")],
                bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ♋"): screenshot[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ♌")]
            }]
        }, event_url=bstack1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ♍"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1l11ll_opy_({
            bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ♎"): bstack1l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ♏"),
            bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ♐"): {
                bstack1l1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ♑"): cls.current_test_uuid(),
                bstack1l1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ♒"): cls.bstack1llllllllll_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1llll11llll_opy_: bstack1llll1ll111_opy_):
        bstack1lllll1l1l1_opy_ = {
            bstack1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ♓"): event,
            bstack1llll11llll_opy_.bstack1lll1llll11_opy_(): bstack1llll11llll_opy_.bstack1llll1l1111_opy_(event)
        }
        cls.bstack11ll1l11ll_opy_(bstack1lllll1l1l1_opy_)
        result = getattr(bstack1llll11llll_opy_, bstack1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ♔"), None)
        if event == bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ♕"):
            threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ♖"): bstack1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ♗")}
        elif event == bstack1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ♘"):
            threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ♙"): getattr(result, bstack1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ♚"), bstack1l1_opy_ (u"ࠬ࠭♛"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ♜"), None) is None or os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ♝")] == bstack1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨ♞")) and (os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ♟"), None) is None or os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ♠")] == bstack1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ♡")):
            return False
        return True
    @staticmethod
    def bstack1ll1ll11111l_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ♢"): bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ♣"),
            bstack1l1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ♤"): bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭♥")
        }
        if os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭♦"), None):
            headers[bstack1l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ♧")] = bstack1l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ♨").format(os.environ[bstack1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ♩")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ♪").format(bstack1ll1ll111l1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ♫"), None)
    @staticmethod
    def bstack1llllllllll_opy_(driver):
        return {
            bstack1111l1ll1ll_opy_(): bstack111111ll11l_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l1lllll1_opy_(exception_info, report):
        return [{bstack1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ♬"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1ll1llll1ll_opy_(typename):
        if bstack1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ♭") in typename:
            return bstack1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ♮")
        return bstack1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ♯")