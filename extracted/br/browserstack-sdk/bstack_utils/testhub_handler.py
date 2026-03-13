# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack111lll1ll11_opy_, bstack111lll11lll_opy_, bstack1llll1ll1_opy_, error_handler, bstack11111lll1ll_opy_, bstack1111lll1ll1_opy_, bstack1111l111l11_opy_, current_time, bstack1l11l11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11l111l1_opy_ import bstack1lll111llll1_opy_
import bstack_utils.bstack1ll1l111l1_opy_ as TestHubUtils
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.test_data import bstack111111111l_opy_
from bstack_utils.constants import bstack1l1lllll1l_opy_
bstack1ll1ll1llll1_opy_ = bstack1111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩ┖")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll11l111l1_opy_ = None
    bs_config = None
    bstack1ll111l111_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll111ll1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def launch(cls, bs_config, bstack1ll111l111_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll111l111_opy_ = bstack1ll111l111_opy_
        try:
            cls.bstack1ll1lll1111l_opy_()
            bstack111llllll11_opy_ = bstack111lll1ll11_opy_(bs_config)
            bstack111llll1ll1_opy_ = bstack111lll11lll_opy_(bs_config)
            data = TestHubUtils.bstack1ll1lll11111_opy_(bs_config, bstack1ll111l111_opy_)
            config = {
                bstack1111l_opy_ (u"ࠪࡥࡺࡺࡨࠨ┗"): (bstack111llllll11_opy_, bstack111llll1ll1_opy_),
                bstack1111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ┘"): cls.default_headers()
            }
            response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠬࡖࡏࡔࡖࠪ┙"), cls.request_url(bstack1111l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭┚")), data, config)
            if response.status_code != 200:
                bstack11111ll11_opy_ = response.json()
                if bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ┛")] == False:
                    cls.bstack1ll1lll111ll_opy_(bstack11111ll11_opy_)
                    return
                cls.bstack1ll1ll1l1ll1_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ├")])
                cls.bstack1ll1ll1l1l1l_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ┝")])
                return None
            bstack1ll1ll1l11l1_opy_ = cls.bstack1ll1lll11l11_opy_(response)
            return bstack1ll1ll1l11l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣ┞").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1l1l1ll_opy_, stage=STAGE.bstack11lll111l_opy_)
    def stop(cls, bstack1ll1ll1ll111_opy_=None):
        if not bstack11l11ll1l1_opy_.on() and not a11y.on():
            return
        if os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ┟")) == bstack1111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ┠") or os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ┡")) == bstack1111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ┢"):
            logger.error(bstack1111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ┣"))
            return {
                bstack1111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ┤"): bstack1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ┥"),
                bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ┦"): bstack1111l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪ┧")
            }
        try:
            cls.bstack1lll11l111l1_opy_.shutdown()
            data = {
                bstack1111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ┨"): current_time()
            }
            if not bstack1ll1ll1ll111_opy_ is None:
                data[bstack1111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫ┩")] = [{
                    bstack1111l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ┪"): bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧ┫"),
                    bstack1111l_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪ┬"): bstack1ll1ll1ll111_opy_
                }]
            config = {
                bstack1111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ┭"): cls.default_headers()
            }
            bstack111ll1lll1l_opy_ = bstack1111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭┮").format(os.environ[bstack1111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ┯")])
            bstack1ll1ll1lllll_opy_ = cls.request_url(bstack111ll1lll1l_opy_)
            response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠧࡑࡗࡗࠫ┰"), bstack1ll1ll1lllll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111l_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢ┱"))
        except Exception as error:
            logger.error(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨ┲") + str(error))
            return {
                bstack1111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ┳"): bstack1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ┴"),
                bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭┵"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1lll11l11_opy_(cls, response):
        bstack11111ll11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1ll1l11l1_opy_ = {}
        if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"࠭ࡪࡸࡶࠪ┶")) is None:
            os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ┷")] = bstack1111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭┸")
        else:
            os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭┹")] = bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠪ࡮ࡼࡺࠧ┺"), bstack1111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ┻"))
        os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ┼")] = bstack11111ll11_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ┽"), bstack1111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ┾"))
        logger.info(bstack1111l_opy_ (u"ࠨࡖࡨࡷࡹ࡮ࡵࡣࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭┿") + os.getenv(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ╀")));
        if bstack11l11ll1l1_opy_.bstack1ll1lll11ll1_opy_(cls.bs_config, cls.bstack1ll111l111_opy_.get(bstack1111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ╁"), bstack1111l_opy_ (u"ࠫࠬ╂"))) is True:
            bstack1lll111l1l11_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1ll1l11ll_opy_(bstack11111ll11_opy_)
            if bstack1lll111l1l11_opy_ != None and build_hashed_id != None:
                bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ╃")] = {
                    bstack1111l_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩ╄"): bstack1lll111l1l11_opy_,
                    bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ╅"): build_hashed_id,
                    bstack1111l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ╆"): allow_screenshots
                }
            else:
                bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ╇")] = {}
        else:
            bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ╈")] = {}
        bstack1ll1ll1l111l_opy_, build_hashed_id = cls.bstack1ll1ll1lll11_opy_(bstack11111ll11_opy_)
        if bstack1ll1ll1l111l_opy_ != None and build_hashed_id != None:
            bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ╉")] = {
                bstack1111l_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩ╊"): bstack1ll1ll1l111l_opy_,
                bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ╋"): build_hashed_id,
            }
        else:
            bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ╌")] = {}
        if bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ╍")].get(bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ╎")) != None or bstack1ll1ll1l11l1_opy_[bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ╏")].get(bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭═")) != None:
            cls.bstack1ll1ll1l1l11_opy_(bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠬࡰࡷࡵࠩ║")), bstack11111ll11_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ╒")))
        return bstack1ll1ll1l11l1_opy_
    @classmethod
    def bstack1ll1ll1l11ll_opy_(cls, bstack11111ll11_opy_):
        if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ╓")) == None:
            cls.bstack1ll1ll1l1ll1_opy_()
            return [None, None, None]
        if bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ╔")][bstack1111l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ╕")] != True:
            cls.bstack1ll1ll1l1ll1_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ╖")])
            return [None, None, None]
        logger.debug(bstack1111l_opy_ (u"ࠫࢀࢃࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭╗").format(bstack1l1lllll1l_opy_))
        os.environ[bstack1111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ╘")] = bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ╙")
        if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠧ࡫ࡹࡷࠫ╚")):
            os.environ[bstack1111l_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬ╛")] = json.dumps({
                bstack1111l_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ╜"): bstack111lll1ll11_opy_(cls.bs_config),
                bstack1111l_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬ╝"): bstack111lll11lll_opy_(cls.bs_config)
            })
        if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭╞")):
            os.environ[bstack1111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ╟")] = bstack11111ll11_opy_[bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ╠")]
        if bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ╡")].get(bstack1111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ╢"), {}).get(bstack1111l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭╣")):
            os.environ[bstack1111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ╤")] = str(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ╥")][bstack1111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭╦")][bstack1111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ╧")])
        else:
            os.environ[bstack1111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ╨")] = bstack1111l_opy_ (u"ࠣࡰࡸࡰࡱࠨ╩")
        return [bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠩ࡭ࡻࡹ࠭╪")], bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ╫")], os.environ[bstack1111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ╬")]]
    @classmethod
    def bstack1ll1ll1lll11_opy_(cls, bstack11111ll11_opy_):
        if bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ╭")) == None:
            cls.bstack1ll1ll1l1l1l_opy_()
            return [None, None]
        if bstack11111ll11_opy_[bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭╮")][bstack1111l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ╯")] != True:
            cls.bstack1ll1ll1l1l1l_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ╰")])
            return [None, None]
        if bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ╱")].get(bstack1111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ╲")):
            logger.debug(bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ╳"))
            parsed = json.loads(os.getenv(bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭╴"), bstack1111l_opy_ (u"࠭ࡻࡾࠩ╵")))
            capabilities = TestHubUtils.bstack1ll1ll1ll11l_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ╶")][bstack1111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ╷")][bstack1111l_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ╸")], bstack1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ╹"), bstack1111l_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ╺"))
            bstack1ll1ll1l111l_opy_ = capabilities[bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪ╻")]
            os.environ[bstack1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ╼")] = bstack1ll1ll1l111l_opy_
            if capabilities.get(bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬ╽")):
                os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧ╾")] = str(capabilities[bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧ╿")])
            if capabilities.get(bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠨ▀")):
                os.environ[bstack1111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠩ▁")] = str(capabilities[bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠪ▂")])
            if bstack1111l_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ▃") in bstack11111ll11_opy_ and bstack11111ll11_opy_.get(bstack1111l_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ▄")) is None:
                parsed[bstack1111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ▅")] = capabilities[bstack1111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ▆")]
            os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ▇")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1ll1ll1ll11l_opy_(bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ█")][bstack1111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭▉")][bstack1111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ▊")], bstack1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ▋"), bstack1111l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩ▌"))
            accessibility_scripts.bstack1llll11ll1_opy_(scripts)
            commands_to_wrap = bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ▍")][bstack1111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ▎")][bstack1111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬ▏")]
            commands = commands_to_wrap.get(bstack1111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ▐"))
            accessibility_scripts.bstack11l11111l1l_opy_(commands)
            scripts_to_run = commands_to_wrap.get(bstack1111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࡔࡰࡔࡸࡲࠬ░"))
            accessibility_scripts.bstack111lll11l11_opy_(scripts_to_run)
            bstack11l111111ll_opy_ = capabilities.get(bstack1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ▒"))
            accessibility_scripts.bstack111ll1lllll_opy_(bstack11l111111ll_opy_)
            accessibility_scripts.store()
        return [bstack1ll1ll1l111l_opy_, bstack11111ll11_opy_[bstack1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ▓")]]
    @classmethod
    def bstack1ll1ll1l1ll1_opy_(cls, response=None):
        os.environ[bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ▔")] = bstack1111l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ▕")
        os.environ[bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ▖")] = bstack1111l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ▗")
        os.environ[bstack1111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬ▘")] = bstack1111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭▙")
        os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ▚")] = bstack1111l_opy_ (u"ࠤࡱࡹࡱࡲࠢ▛")
        os.environ[bstack1111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ▜")] = bstack1111l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ▝")
        cls.bstack1ll1lll111ll_opy_(response, bstack1111l_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧ▞"))
        return [None, None, None]
    @classmethod
    def bstack1ll1ll1l1l1l_opy_(cls, response=None):
        os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ▟")] = bstack1111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ■")
        os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭□")] = bstack1111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ▢")
        os.environ[bstack1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ▣")] = bstack1111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ▤")
        cls.bstack1ll1lll111ll_opy_(response, bstack1111l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧ▥"))
        return [None, None, None]
    @classmethod
    def bstack1ll1ll1l1l11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ▦")] = jwt
        os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ▧")] = build_hashed_id
    @classmethod
    def bstack1ll1lll111ll_opy_(cls, response=None, product=bstack1111l_opy_ (u"ࠣࠤ▨")):
        if response == None or response.get(bstack1111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ▩")) == None:
            logger.error(product + bstack1111l_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧ▪"))
            return
        for error in response[bstack1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ▫")]:
            bstack111l1111l11_opy_ = error[bstack1111l_opy_ (u"ࠬࡱࡥࡺࠩ▬")]
            error_message = error[bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ▭")]
            if error_message:
                if bstack111l1111l11_opy_ == bstack1111l_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨ▮"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111l_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤ▯") + product + bstack1111l_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ▰"))
    @classmethod
    def bstack1ll1lll1111l_opy_(cls):
        if cls.bstack1lll11l111l1_opy_ is not None:
            return
        cls.bstack1lll11l111l1_opy_ = bstack1lll111llll1_opy_(cls.post_data)
        cls.bstack1lll11l111l1_opy_.start()
    @classmethod
    def bstack11111111ll_opy_(cls):
        if cls.bstack1lll11l111l1_opy_ is None:
            return
        cls.bstack1lll11l111l1_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lllll1l1ll_opy_, event_url=bstack1111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ▱")):
        config = {
            bstack1111l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ▲"): cls.default_headers()
        }
        logger.debug(bstack1111l_opy_ (u"ࠧࡶ࡯ࡴࡶࡢࡨࡦࡺࡡ࠻ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡴࠢࡾࢁࠧ△").format(bstack1111l_opy_ (u"࠭ࠬࠡࠩ▴").join([event[bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ▵")] for event in bstack1lllll1l1ll_opy_])))
        response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭▶"), cls.request_url(event_url), bstack1lllll1l1ll_opy_, config)
        bstack111lllll1l1_opy_ = response.json()
    @classmethod
    def bstack111lllllll_opy_(cls, bstack1lllll1l1ll_opy_, event_url=bstack1111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ▷")):
        logger.debug(bstack1111l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡢࡦࡧࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ▸").format(bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ▹")]))
        if not TestHubUtils.bstack1ll1ll11llll_opy_(bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ►")]):
            logger.debug(bstack1111l_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡒࡴࡺࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ▻").format(bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ▼")]))
            return
        bstack11llll11_opy_ = TestHubUtils.bstack1ll1ll1ll1ll_opy_(bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ▽")], bstack1lllll1l1ll_opy_.get(bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ▾")))
        if bstack11llll11_opy_ != None:
            if bstack1lllll1l1ll_opy_.get(bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ▿")) != None:
                bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭◀")][bstack1111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ◁")] = bstack11llll11_opy_
            else:
                bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ◂")] = bstack11llll11_opy_
        if event_url == bstack1111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭◃"):
            cls.bstack1ll1lll1111l_opy_()
            logger.debug(bstack1111l_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ◄").format(bstack1lllll1l1ll_opy_[bstack1111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭◅")]))
            cls.bstack1lll11l111l1_opy_.add(bstack1lllll1l1ll_opy_)
        elif event_url == bstack1111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ◆"):
            cls.post_data([bstack1lllll1l1ll_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1l1111l_opy_(cls, logs):
        for log in logs:
            bstack1ll1ll1lll1l_opy_ = {
                bstack1111l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ◇"): bstack1111l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧ◈"),
                bstack1111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ◉"): log[bstack1111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭◊")],
                bstack1111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ○"): log[bstack1111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ◌")],
                bstack1111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪ◍"): {},
                bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ◎"): log[bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭●")],
            }
            if bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭◐") in log:
                bstack1ll1ll1lll1l_opy_[bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ◑")] = log[bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ◒")]
            elif bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ◓") in log:
                bstack1ll1ll1lll1l_opy_[bstack1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ◔")] = log[bstack1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ◕")]
            cls.bstack111lllllll_opy_({
                bstack1111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ◖"): bstack1111l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ◗"),
                bstack1111l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ◘"): [bstack1ll1ll1lll1l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1ll1ll1l1_opy_(cls, steps):
        bstack1ll1ll1l1lll_opy_ = []
        for step in steps:
            bstack1ll1lll11l1l_opy_ = {
                bstack1111l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭◙"): bstack1111l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬ◚"),
                bstack1111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ◛"): step[bstack1111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ◜")],
                bstack1111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ◝"): step[bstack1111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ◞")],
                bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ◟"): step[bstack1111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ◠")],
                bstack1111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ◡"): step[bstack1111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ◢")]
            }
            if bstack1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ◣") in step:
                bstack1ll1lll11l1l_opy_[bstack1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ◤")] = step[bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭◥")]
            elif bstack1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ◦") in step:
                bstack1ll1lll11l1l_opy_[bstack1111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ◧")] = step[bstack1111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ◨")]
            bstack1ll1ll1l1lll_opy_.append(bstack1ll1lll11l1l_opy_)
        cls.bstack111lllllll_opy_({
            bstack1111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ◩"): bstack1111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ◪"),
            bstack1111l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ◫"): bstack1ll1ll1l1lll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll1111l_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack11l1lll1l1_opy_(cls, screenshot):
        cls.bstack111lllllll_opy_({
            bstack1111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ◬"): bstack1111l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ◭"),
            bstack1111l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭◮"): [{
                bstack1111l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ◯"): bstack1111l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬ◰"),
                bstack1111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ◱"): datetime.datetime.utcnow().isoformat() + bstack1111l_opy_ (u"ࠬࡠࠧ◲"),
                bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ◳"): screenshot[bstack1111l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭◴")],
                bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ◵"): screenshot[bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ◶")]
            }]
        }, event_url=bstack1111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ◷"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111lllllll_opy_({
            bstack1111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ◸"): bstack1111l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ◹"),
            bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ◺"): {
                bstack1111l_opy_ (u"ࠢࡶࡷ࡬ࡨࠧ◻"): cls.current_test_uuid(),
                bstack1111l_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢ◼"): cls.bstack11111ll1ll_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1lllll1l1ll_opy_: bstack111111111l_opy_):
        bstack1llll1lll1l_opy_ = {
            bstack1111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭◽"): event,
            bstack1lllll1l1ll_opy_.bstack1lllllll1ll_opy_(): bstack1lllll1l1ll_opy_.bstack11111111l1_opy_(event)
        }
        cls.bstack111lllllll_opy_(bstack1llll1lll1l_opy_)
        result = getattr(bstack1lllll1l1ll_opy_, bstack1111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ◾"), None)
        if event == bstack1111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ◿"):
            threading.current_thread().bstackTestMeta = {bstack1111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ☀"): bstack1111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ☁")}
        elif event == bstack1111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ☂"):
            threading.current_thread().bstackTestMeta = {bstack1111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ☃"): getattr(result, bstack1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ☄"), bstack1111l_opy_ (u"ࠪࠫ★"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ☆"), None) is None or os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ☇")] == bstack1111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ☈")) and (os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ☉"), None) is None or os.environ[bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭☊")] == bstack1111l_opy_ (u"ࠤࡱࡹࡱࡲࠢ☋")):
            return False
        return True
    @staticmethod
    def bstack1ll1ll1l1111_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ☌"): bstack1111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ☍"),
            bstack1111l_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨ☎"): bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫ☏")
        }
        if os.environ.get(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ☐"), None):
            headers[bstack1111l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ☑")] = bstack1111l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ☒").format(os.environ[bstack1111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢ☓")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1111l_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ☔").format(bstack1ll1ll1llll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ☕"), None)
    @staticmethod
    def bstack11111ll1ll_opy_(driver):
        return {
            bstack11111lll1ll_opy_(): bstack1111lll1ll1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1lll111l1_opy_(exception_info, report):
        return [{bstack1111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ☖"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll11l1l1l_opy_(typename):
        if bstack1111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ☗") in typename:
            return bstack1111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ☘")
        return bstack1111l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ☙")