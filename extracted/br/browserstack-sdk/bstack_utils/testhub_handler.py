# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111l11ll_opy_, bstack11l111l1ll1_opy_, bstack1llll1l111_opy_, error_handler, bstack111l11lll11_opy_, bstack111l111llll_opy_, bstack1111ll1l11l_opy_, current_time, bstack1lll111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11ll11l1_opy_ import bstack1lll11lll111_opy_
import bstack_utils.bstack11l1l1ll1l_opy_ as bstack111ll11ll1_opy_
from bstack_utils.bstack1111ll1111_opy_ import bstack111lllll1_opy_
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.bstack1l11l11l1l_opy_ import bstack1l11l11l1l_opy_
from bstack_utils.test_data import bstack11111llll1_opy_
from bstack_utils.constants import bstack1lllllll11_opy_
bstack1ll1lllll11l_opy_ = bstack1lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭⑖")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll11ll11l1_opy_ = None
    bs_config = None
    bstack11l1l1l1_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll11llll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def launch(cls, bs_config, bstack11l1l1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1l1l1_opy_ = bstack11l1l1l1_opy_
        try:
            cls.bstack1ll1llll11l1_opy_()
            bstack11l11111111_opy_ = bstack11l111l11ll_opy_(bs_config)
            bstack11l11l111l1_opy_ = bstack11l111l1ll1_opy_(bs_config)
            data = bstack111ll11ll1_opy_.bstack1ll1llll1111_opy_(bs_config, bstack11l1l1l1_opy_)
            config = {
                bstack1lll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ⑗"): (bstack11l11111111_opy_, bstack11l11l111l1_opy_),
                bstack1lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⑘"): cls.default_headers()
            }
            response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ⑙"), cls.request_url(bstack1lll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪ⑚")), data, config)
            if response.status_code != 200:
                bstack1l1l1lll1_opy_ = response.json()
                if bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⑛")] == False:
                    cls.bstack1ll1llll1ll1_opy_(bstack1l1l1lll1_opy_)
                    return
                cls.bstack1ll1llll1lll_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⑜")])
                cls.bstack1ll1lll1l1ll_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⑝")])
                return None
            bstack1ll1lllll111_opy_ = cls.bstack1ll1llll1l11_opy_(response)
            return bstack1ll1lllll111_opy_, response.json()
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧ⑞").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll11ll11_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def stop(cls, bstack1ll1llll1l1l_opy_=None):
        if not bstack111lllll1_opy_.on() and not bstack11l1111111_opy_.on():
            return
        if os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⑟")) == bstack1lll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢ①") or os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ②")) == bstack1lll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ③"):
            logger.error(bstack1lll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ④"))
            return {
                bstack1lll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⑤"): bstack1lll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⑥"),
                bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⑦"): bstack1lll1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧ⑧")
            }
        try:
            cls.bstack1lll11ll11l1_opy_.shutdown()
            data = {
                bstack1lll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⑨"): current_time()
            }
            if not bstack1ll1llll1l1l_opy_ is None:
                data[bstack1lll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ⑩")] = [{
                    bstack1lll1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ⑪"): bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ⑫"),
                    bstack1lll1l_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ⑬"): bstack1ll1llll1l1l_opy_
                }]
            config = {
                bstack1lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⑭"): cls.default_headers()
            }
            bstack111llll1l11_opy_ = bstack1lll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ⑮").format(os.environ[bstack1lll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ⑯")])
            bstack1ll1lll1l11l_opy_ = cls.request_url(bstack111llll1l11_opy_)
            response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠫࡕ࡛ࡔࠨ⑰"), bstack1ll1lll1l11l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lll1l_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦ⑱"))
        except Exception as error:
            logger.error(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ⑲") + str(error))
            return {
                bstack1lll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⑳"): bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⑴"),
                bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⑵"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1llll1l11_opy_(cls, response):
        bstack1l1l1lll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1lllll111_opy_ = {}
        if bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠪ࡮ࡼࡺࠧ⑶")) is None:
            os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⑷")] = bstack1lll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⑸")
        else:
            os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⑹")] = bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠧ࡫ࡹࡷࠫ⑺"), bstack1lll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭⑻"))
        os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⑼")] = bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⑽"), bstack1lll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⑾"))
        logger.info(bstack1lll1l_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ⑿") + os.getenv(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⒀")));
        if bstack111lllll1_opy_.bstack1ll1lllll1l1_opy_(cls.bs_config, cls.bstack11l1l1l1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ⒁"), bstack1lll1l_opy_ (u"ࠨࠩ⒂"))) is True:
            bstack1lll11l1l11l_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1lll1ll1l_opy_(bstack1l1l1lll1_opy_)
            if bstack1lll11l1l11l_opy_ != None and build_hashed_id != None:
                bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⒃")] = {
                    bstack1lll1l_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭⒄"): bstack1lll11l1l11l_opy_,
                    bstack1lll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⒅"): build_hashed_id,
                    bstack1lll1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⒆"): allow_screenshots
                }
            else:
                bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⒇")] = {}
        else:
            bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⒈")] = {}
        bstack1ll1lll1l111_opy_, build_hashed_id = cls.bstack1ll1llll111l_opy_(bstack1l1l1lll1_opy_)
        if bstack1ll1lll1l111_opy_ != None and build_hashed_id != None:
            bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⒉")] = {
                bstack1lll1l_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭⒊"): bstack1ll1lll1l111_opy_,
                bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⒋"): build_hashed_id,
            }
        else:
            bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⒌")] = {}
        if bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⒍")].get(bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⒎")) != None or bstack1ll1lllll111_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⒏")].get(bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⒐")) != None:
            cls.bstack1ll1llllll11_opy_(bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠩ࡭ࡻࡹ࠭⒑")), bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⒒")))
        return bstack1ll1lllll111_opy_
    @classmethod
    def bstack1ll1lll1ll1l_opy_(cls, bstack1l1l1lll1_opy_):
        if bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⒓")) == None:
            cls.bstack1ll1llll1lll_opy_()
            return [None, None, None]
        if bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⒔")][bstack1lll1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⒕")] != True:
            cls.bstack1ll1llll1lll_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⒖")])
            return [None, None, None]
        logger.debug(bstack1lll1l_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⒗").format(bstack1lllllll11_opy_))
        os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ⒘")] = bstack1lll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ⒙")
        if bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠫ࡯ࡽࡴࠨ⒚")):
            os.environ[bstack1lll1l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ⒛")] = json.dumps({
                bstack1lll1l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ⒜"): bstack11l111l11ll_opy_(cls.bs_config),
                bstack1lll1l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ⒝"): bstack11l111l1ll1_opy_(cls.bs_config)
            })
        if bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⒞")):
            os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⒟")] = bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⒠")]
        if bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⒡")].get(bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⒢"), {}).get(bstack1lll1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⒣")):
            os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⒤")] = str(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⒥")][bstack1lll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⒦")][bstack1lll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⒧")])
        else:
            os.environ[bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⒨")] = bstack1lll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⒩")
        return [bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"࠭ࡪࡸࡶࠪ⒪")], bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⒫")], os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⒬")]]
    @classmethod
    def bstack1ll1llll111l_opy_(cls, bstack1l1l1lll1_opy_):
        if bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⒭")) == None:
            cls.bstack1ll1lll1l1ll_opy_()
            return [None, None]
        if bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⒮")][bstack1lll1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⒯")] != True:
            cls.bstack1ll1lll1l1ll_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⒰")])
            return [None, None]
        if bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⒱")].get(bstack1lll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⒲")):
            logger.debug(bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ⒳"))
            parsed = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⒴"), bstack1lll1l_opy_ (u"ࠪࡿࢂ࠭⒵")))
            capabilities = bstack111ll11ll1_opy_.bstack1ll1lll11ll1_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫⒶ")][bstack1lll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ⓑ")][bstack1lll1l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬⒸ")], bstack1lll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬⒹ"), bstack1lll1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧⒺ"))
            bstack1ll1lll1l111_opy_ = capabilities[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧⒻ")]
            os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨⒼ")] = bstack1ll1lll1l111_opy_
            if bstack1lll1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨⒽ") in bstack1l1l1lll1_opy_ and bstack1l1l1lll1_opy_.get(bstack1lll1l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦⒾ")) is None:
                parsed[bstack1lll1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧⒿ")] = capabilities[bstack1lll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨⓀ")]
            os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩⓁ")] = json.dumps(parsed)
            scripts = bstack111ll11ll1_opy_.bstack1ll1lll11ll1_opy_(bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩⓂ")][bstack1lll1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫⓃ")][bstack1lll1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬⓄ")], bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪⓅ"), bstack1lll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧⓆ"))
            bstack1l11l11l1l_opy_.bstack11l1l1lll_opy_(scripts)
            commands = bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧⓇ")][bstack1lll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩⓈ")][bstack1lll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪⓉ")].get(bstack1lll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬⓊ"))
            bstack1l11l11l1l_opy_.bstack11l1111ll11_opy_(commands)
            bstack11l111ll111_opy_ = capabilities.get(bstack1lll1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩⓋ"))
            bstack1l11l11l1l_opy_.bstack111llll1l1l_opy_(bstack11l111ll111_opy_)
            bstack1l11l11l1l_opy_.store()
        return [bstack1ll1lll1l111_opy_, bstack1l1l1lll1_opy_[bstack1lll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧⓌ")]]
    @classmethod
    def bstack1ll1llll1lll_opy_(cls, response=None):
        os.environ[bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫⓍ")] = bstack1lll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬⓎ")
        os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬⓏ")] = bstack1lll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧⓐ")
        os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩⓑ")] = bstack1lll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪⓒ")
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫⓓ")] = bstack1lll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦⓔ")
        os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨⓕ")] = bstack1lll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨⓖ")
        cls.bstack1ll1llll1ll1_opy_(response, bstack1lll1l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤⓗ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1lll1l1ll_opy_(cls, response=None):
        os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨⓘ")] = bstack1lll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩⓙ")
        os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪⓚ")] = bstack1lll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫⓛ")
        os.environ[bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫⓜ")] = bstack1lll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ⓝ")
        cls.bstack1ll1llll1ll1_opy_(response, bstack1lll1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤⓞ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1llllll11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧⓟ")] = jwt
        os.environ[bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⓠ")] = build_hashed_id
    @classmethod
    def bstack1ll1llll1ll1_opy_(cls, response=None, product=bstack1lll1l_opy_ (u"ࠧࠨⓡ")):
        if response == None or response.get(bstack1lll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ⓢ")) == None:
            logger.error(product + bstack1lll1l_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤⓣ"))
            return
        for error in response[bstack1lll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨⓤ")]:
            bstack1111llll1ll_opy_ = error[bstack1lll1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ⓥ")]
            error_message = error[bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⓦ")]
            if error_message:
                if bstack1111llll1ll_opy_ == bstack1lll1l_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥⓧ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨⓨ") + product + bstack1lll1l_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦⓩ"))
    @classmethod
    def bstack1ll1llll11l1_opy_(cls):
        if cls.bstack1lll11ll11l1_opy_ is not None:
            return
        cls.bstack1lll11ll11l1_opy_ = bstack1lll11lll111_opy_(cls.bstack1ll1lll11lll_opy_)
        cls.bstack1lll11ll11l1_opy_.start()
    @classmethod
    def bstack11111ll1ll_opy_(cls):
        if cls.bstack1lll11ll11l1_opy_ is None:
            return
        cls.bstack1lll11ll11l1_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1lll11lll_opy_(cls, bstack1111l11111_opy_, event_url=bstack1lll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⓪")):
        config = {
            bstack1lll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ⓫"): cls.default_headers()
        }
        logger.debug(bstack1lll1l_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ⓬").format(bstack1lll1l_opy_ (u"ࠪ࠰ࠥ࠭⓭").join([event[bstack1lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⓮")] for event in bstack1111l11111_opy_])))
        response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠬࡖࡏࡔࡖࠪ⓯"), cls.request_url(event_url), bstack1111l11111_opy_, config)
        bstack111lllll1ll_opy_ = response.json()
    @classmethod
    def bstack11lll111ll_opy_(cls, bstack1111l11111_opy_, event_url=bstack1lll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⓰")):
        logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⓱").format(bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⓲")]))
        if not bstack111ll11ll1_opy_.bstack1ll1lll11l1l_opy_(bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⓳")]):
            logger.debug(bstack1lll1l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⓴").format(bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⓵")]))
            return
        bstack11ll111l11_opy_ = bstack111ll11ll1_opy_.bstack1ll1llll11ll_opy_(bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⓶")], bstack1111l11111_opy_.get(bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⓷")))
        if bstack11ll111l11_opy_ != None:
            if bstack1111l11111_opy_.get(bstack1lll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⓸")) != None:
                bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⓹")][bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⓺")] = bstack11ll111l11_opy_
            else:
                bstack1111l11111_opy_[bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⓻")] = bstack11ll111l11_opy_
        if event_url == bstack1lll1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⓼"):
            cls.bstack1ll1llll11l1_opy_()
            logger.debug(bstack1lll1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⓽").format(bstack1111l11111_opy_[bstack1lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⓾")]))
            cls.bstack1lll11ll11l1_opy_.add(bstack1111l11111_opy_)
        elif event_url == bstack1lll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⓿"):
            cls.bstack1ll1lll11lll_opy_([bstack1111l11111_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11ll1l1l11_opy_(cls, logs):
        for log in logs:
            bstack1ll1lll11l11_opy_ = {
                bstack1lll1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭─"): bstack1lll1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ━"),
                bstack1lll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ│"): log[bstack1lll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ┃")],
                bstack1lll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ┄"): log[bstack1lll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ┅")],
                bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ┆"): {},
                bstack1lll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ┇"): log[bstack1lll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ┈")],
            }
            if bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ┉") in log:
                bstack1ll1lll11l11_opy_[bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┊")] = log[bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┋")]
            elif bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┌") in log:
                bstack1ll1lll11l11_opy_[bstack1lll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ┍")] = log[bstack1lll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ┎")]
            cls.bstack11lll111ll_opy_({
                bstack1lll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭┏"): bstack1lll1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ┐"),
                bstack1lll1l_opy_ (u"ࠫࡱࡵࡧࡴࠩ┑"): [bstack1ll1lll11l11_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1lll1l1l1_opy_(cls, steps):
        bstack1ll1lll1llll_opy_ = []
        for step in steps:
            bstack1ll1lllll1ll_opy_ = {
                bstack1lll1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ┒"): bstack1lll1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ┓"),
                bstack1lll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭└"): step[bstack1lll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ┕")],
                bstack1lll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ┖"): step[bstack1lll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭┗")],
                bstack1lll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ┘"): step[bstack1lll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭┙")],
                bstack1lll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ┚"): step[bstack1lll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ┛")]
            }
            if bstack1lll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ├") in step:
                bstack1ll1lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ┝")] = step[bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ┞")]
            elif bstack1lll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┟") in step:
                bstack1ll1lllll1ll_opy_[bstack1lll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┠")] = step[bstack1lll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┡")]
            bstack1ll1lll1llll_opy_.append(bstack1ll1lllll1ll_opy_)
        cls.bstack11lll111ll_opy_({
            bstack1lll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ┢"): bstack1lll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ┣"),
            bstack1lll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ┤"): bstack1ll1lll1llll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111lll1111_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1ll1l11ll_opy_(cls, screenshot):
        cls.bstack11lll111ll_opy_({
            bstack1lll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ┥"): bstack1lll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ┦"),
            bstack1lll1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ┧"): [{
                bstack1lll1l_opy_ (u"࠭࡫ࡪࡰࡧࠫ┨"): bstack1lll1l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ┩"),
                bstack1lll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ┪"): datetime.datetime.utcnow().isoformat() + bstack1lll1l_opy_ (u"ࠩ࡝ࠫ┫"),
                bstack1lll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ┬"): screenshot[bstack1lll1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ┭")],
                bstack1lll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┮"): screenshot[bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┯")]
            }]
        }, event_url=bstack1lll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ┰"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1ll1lll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11lll111ll_opy_({
            bstack1lll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ┱"): bstack1lll1l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭┲"),
            bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ┳"): {
                bstack1lll1l_opy_ (u"ࠦࡺࡻࡩࡥࠤ┴"): cls.current_test_uuid(),
                bstack1lll1l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ┵"): cls.bstack1111l11ll1_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1111l11111_opy_: bstack11111llll1_opy_):
        bstack1111111l1l_opy_ = {
            bstack1lll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ┶"): event,
            bstack1111l11111_opy_.bstack11111ll111_opy_(): bstack1111l11111_opy_.bstack1lllllll1l1_opy_(event)
        }
        cls.bstack11lll111ll_opy_(bstack1111111l1l_opy_)
        result = getattr(bstack1111l11111_opy_, bstack1lll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ┷"), None)
        if event == bstack1lll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ┸"):
            threading.current_thread().bstackTestMeta = {bstack1lll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ┹"): bstack1lll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ┺")}
        elif event == bstack1lll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭┻"):
            threading.current_thread().bstackTestMeta = {bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ┼"): getattr(result, bstack1lll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭┽"), bstack1lll1l_opy_ (u"ࠧࠨ┾"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ┿"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭╀")] == bstack1lll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ╁")) and (os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ╂"), None) is None or os.environ[bstack1lll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ╃")] == bstack1lll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ╄")):
            return False
        return True
    @staticmethod
    def bstack1ll1lll1lll1_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1lll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭╅"): bstack1lll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ╆"),
            bstack1lll1l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬ╇"): bstack1lll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ╈")
        }
        if os.environ.get(bstack1lll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ╉"), None):
            headers[bstack1lll1l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ╊")] = bstack1lll1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ╋").format(os.environ[bstack1lll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ╌")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1lll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ╍").format(bstack1ll1lllll11l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭╎"), None)
    @staticmethod
    def bstack1111l11ll1_opy_(driver):
        return {
            bstack111l11lll11_opy_(): bstack111l111llll_opy_(driver)
        }
    @staticmethod
    def bstack1ll1lll1ll11_opy_(exception_info, report):
        return [{bstack1lll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭╏"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll1ll111l_opy_(typename):
        if bstack1lll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ═") in typename:
            return bstack1lll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ║")
        return bstack1lll1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ╒")