# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111l1l1l_opy_, bstack11l1111l1l1_opy_, bstack1llll1l1ll_opy_, error_handler, bstack1111l1111l1_opy_, bstack1111l1lll11_opy_, bstack1111l1111ll_opy_, current_time, bstack1lll11lll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll11l1llll_opy_ import bstack1lll11ll111l_opy_
import bstack_utils.bstack1ll111111l_opy_ as bstack1l111l1l_opy_
from bstack_utils.bstack1111l1l1l1_opy_ import bstack11l111ll11_opy_
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.test_data import bstack111111l111_opy_
from bstack_utils.constants import bstack1lll11l111_opy_
bstack1ll1lll11lll_opy_ = bstack1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ⑗")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll11l1llll_opy_ = None
    bs_config = None
    bstack11l1llll11_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1ll11ll_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def launch(cls, bs_config, bstack11l1llll11_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1llll11_opy_ = bstack11l1llll11_opy_
        try:
            cls.bstack1ll1lll1lll1_opy_()
            bstack11l111l11ll_opy_ = bstack11l111l1l1l_opy_(bs_config)
            bstack11l111l1l11_opy_ = bstack11l1111l1l1_opy_(bs_config)
            data = bstack1l111l1l_opy_.bstack1ll1lllll1l1_opy_(bs_config, bstack11l1llll11_opy_)
            config = {
                bstack1111_opy_ (u"ࠨࡣࡸࡸ࡭࠭⑘"): (bstack11l111l11ll_opy_, bstack11l111l1l11_opy_),
                bstack1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⑙"): cls.default_headers()
            }
            response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⑚"), cls.request_url(bstack1111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ⑛")), data, config)
            if response.status_code != 200:
                bstack1llll1lll1_opy_ = response.json()
                if bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⑜")] == False:
                    cls.bstack1ll1lllll111_opy_(bstack1llll1lll1_opy_)
                    return
                cls.bstack1ll1lll1l11l_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⑝")])
                cls.bstack1ll1lll1l111_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⑞")])
                return None
            bstack1ll1llll1l1l_opy_ = cls.bstack1ll1llll1lll_opy_(response)
            return bstack1ll1llll1l1l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ⑟").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll1ll1ll_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def stop(cls, bstack1ll1llll1ll1_opy_=None):
        if not bstack11l111ll11_opy_.on() and not bstack11l1111111_opy_.on():
            return
        if os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭①")) == bstack1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ②") or os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ③")) == bstack1111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ④"):
            logger.error(bstack1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ⑤"))
            return {
                bstack1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⑥"): bstack1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⑦"),
                bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⑧"): bstack1111_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ⑨")
            }
        try:
            cls.bstack1lll11l1llll_opy_.shutdown()
            data = {
                bstack1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⑩"): current_time()
            }
            if not bstack1ll1llll1ll1_opy_ is None:
                data[bstack1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ⑪")] = [{
                    bstack1111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭⑫"): bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ⑬"),
                    bstack1111_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ⑭"): bstack1ll1llll1ll1_opy_
                }]
            config = {
                bstack1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⑮"): cls.default_headers()
            }
            bstack111llll11l1_opy_ = bstack1111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫ⑯").format(os.environ[bstack1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ⑰")])
            bstack1ll1lll111ll_opy_ = cls.request_url(bstack111llll11l1_opy_)
            response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"ࠬࡖࡕࡕࠩ⑱"), bstack1ll1lll111ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ⑲"))
        except Exception as error:
            logger.error(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦ⑳") + str(error))
            return {
                bstack1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⑴"): bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⑵"),
                bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⑶"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1llll1lll_opy_(cls, response):
        bstack1llll1lll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1llll1l1l_opy_ = {}
        if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠫ࡯ࡽࡴࠨ⑷")) is None:
            os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⑸")] = bstack1111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⑹")
        else:
            os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⑺")] = bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠨ࡬ࡺࡸࠬ⑻"), bstack1111_opy_ (u"ࠩࡱࡹࡱࡲࠧ⑼"))
        os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⑽")] = bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⑾"), bstack1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⑿"))
        logger.info(bstack1111_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ⒀") + os.getenv(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⒁")));
        if bstack11l111ll11_opy_.bstack1ll1llll111l_opy_(cls.bs_config, cls.bstack11l1llll11_opy_.get(bstack1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⒂"), bstack1111_opy_ (u"ࠩࠪ⒃"))) is True:
            bstack1lll11l1l1l1_opy_, build_hashed_id, allow_screenshots = cls.bstack1ll1llll11ll_opy_(bstack1llll1lll1_opy_)
            if bstack1lll11l1l1l1_opy_ != None and build_hashed_id != None:
                bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⒄")] = {
                    bstack1111_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧ⒅"): bstack1lll11l1l1l1_opy_,
                    bstack1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⒆"): build_hashed_id,
                    bstack1111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⒇"): allow_screenshots
                }
            else:
                bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⒈")] = {}
        else:
            bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⒉")] = {}
        bstack1ll1lll11l11_opy_, build_hashed_id = cls.bstack1ll1lll1ll1l_opy_(bstack1llll1lll1_opy_)
        if bstack1ll1lll11l11_opy_ != None and build_hashed_id != None:
            bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⒊")] = {
                bstack1111_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧ⒋"): bstack1ll1lll11l11_opy_,
                bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⒌"): build_hashed_id,
            }
        else:
            bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⒍")] = {}
        if bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⒎")].get(bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⒏")) != None or bstack1ll1llll1l1l_opy_[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⒐")].get(bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⒑")) != None:
            cls.bstack1ll1lllll11l_opy_(bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠪ࡮ࡼࡺࠧ⒒")), bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⒓")))
        return bstack1ll1llll1l1l_opy_
    @classmethod
    def bstack1ll1llll11ll_opy_(cls, bstack1llll1lll1_opy_):
        if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⒔")) == None:
            cls.bstack1ll1lll1l11l_opy_()
            return [None, None, None]
        if bstack1llll1lll1_opy_[bstack1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⒕")][bstack1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⒖")] != True:
            cls.bstack1ll1lll1l11l_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⒗")])
            return [None, None, None]
        logger.debug(bstack1111_opy_ (u"ࠩࡾࢁࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⒘").format(bstack1lll11l111_opy_))
        os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ⒙")] = bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩ⒚")
        if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠬࡰࡷࡵࠩ⒛")):
            os.environ[bstack1111_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ⒜")] = json.dumps({
                bstack1111_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ⒝"): bstack11l111l1l1l_opy_(cls.bs_config),
                bstack1111_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ⒞"): bstack11l1111l1l1_opy_(cls.bs_config)
            })
        if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⒟")):
            os.environ[bstack1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⒠")] = bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⒡")]
        if bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⒢")].get(bstack1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⒣"), {}).get(bstack1111_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⒤")):
            os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⒥")] = str(bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⒦")][bstack1111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⒧")][bstack1111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⒨")])
        else:
            os.environ[bstack1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⒩")] = bstack1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⒪")
        return [bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠧ࡫ࡹࡷࠫ⒫")], bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⒬")], os.environ[bstack1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⒭")]]
    @classmethod
    def bstack1ll1lll1ll1l_opy_(cls, bstack1llll1lll1_opy_):
        if bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⒮")) == None:
            cls.bstack1ll1lll1l111_opy_()
            return [None, None]
        if bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⒯")][bstack1111_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⒰")] != True:
            cls.bstack1ll1lll1l111_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⒱")])
            return [None, None]
        if bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⒲")].get(bstack1111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⒳")):
            logger.debug(bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭⒴"))
            parsed = json.loads(os.getenv(bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⒵"), bstack1111_opy_ (u"ࠫࢀࢃࠧⒶ")))
            capabilities = bstack1l111l1l_opy_.bstack1ll1lll11ll1_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬⒷ")][bstack1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧⒸ")][bstack1111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭Ⓓ")], bstack1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ⓔ"), bstack1111_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨⒻ"))
            bstack1ll1lll11l11_opy_ = capabilities[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨⒼ")]
            os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩⒽ")] = bstack1ll1lll11l11_opy_
            if bstack1111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢⒾ") in bstack1llll1lll1_opy_ and bstack1llll1lll1_opy_.get(bstack1111_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧⒿ")) is None:
                parsed[bstack1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨⓀ")] = capabilities[bstack1111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩⓁ")]
            os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪⓂ")] = json.dumps(parsed)
            scripts = bstack1l111l1l_opy_.bstack1ll1lll11ll1_opy_(bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪⓃ")][bstack1111_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬⓄ")][bstack1111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭Ⓟ")], bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫⓆ"), bstack1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨⓇ"))
            bstack1l111l111_opy_.bstack11ll1111l_opy_(scripts)
            commands = bstack1llll1lll1_opy_[bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨⓈ")][bstack1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪⓉ")][bstack1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫⓊ")].get(bstack1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭Ⓥ"))
            bstack1l111l111_opy_.bstack11l1111l11l_opy_(commands)
            bstack11l1111l111_opy_ = capabilities.get(bstack1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪⓌ"))
            bstack1l111l111_opy_.bstack111llll11ll_opy_(bstack11l1111l111_opy_)
            bstack1l111l111_opy_.store()
        return [bstack1ll1lll11l11_opy_, bstack1llll1lll1_opy_[bstack1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨⓍ")]]
    @classmethod
    def bstack1ll1lll1l11l_opy_(cls, response=None):
        os.environ[bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⓎ")] = bstack1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ⓩ")
        os.environ[bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ⓐ")] = bstack1111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨⓑ")
        os.environ[bstack1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪⓒ")] = bstack1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫⓓ")
        os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬⓔ")] = bstack1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧⓕ")
        os.environ[bstack1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩⓖ")] = bstack1111_opy_ (u"ࠤࡱࡹࡱࡲࠢⓗ")
        cls.bstack1ll1lllll111_opy_(response, bstack1111_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥⓘ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1lll1l111_opy_(cls, response=None):
        os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩⓙ")] = bstack1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪⓚ")
        os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫⓛ")] = bstack1111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬⓜ")
        os.environ[bstack1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬⓝ")] = bstack1111_opy_ (u"ࠩࡱࡹࡱࡲࠧⓞ")
        cls.bstack1ll1lllll111_opy_(response, bstack1111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥⓟ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1lllll11l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨⓠ")] = jwt
        os.environ[bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪⓡ")] = build_hashed_id
    @classmethod
    def bstack1ll1lllll111_opy_(cls, response=None, product=bstack1111_opy_ (u"ࠨࠢⓢ")):
        if response == None or response.get(bstack1111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧⓣ")) == None:
            logger.error(product + bstack1111_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥⓤ"))
            return
        for error in response[bstack1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩⓥ")]:
            bstack1111l1l1l1l_opy_ = error[bstack1111_opy_ (u"ࠪ࡯ࡪࡿࠧⓦ")]
            error_message = error[bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬⓧ")]
            if error_message:
                if bstack1111l1l1l1l_opy_ == bstack1111_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦⓨ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢⓩ") + product + bstack1111_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ⓪"))
    @classmethod
    def bstack1ll1lll1lll1_opy_(cls):
        if cls.bstack1lll11l1llll_opy_ is not None:
            return
        cls.bstack1lll11l1llll_opy_ = bstack1lll11ll111l_opy_(cls.bstack1ll1llll1111_opy_)
        cls.bstack1lll11l1llll_opy_.start()
    @classmethod
    def bstack1llllll111l_opy_(cls):
        if cls.bstack1lll11l1llll_opy_ is None:
            return
        cls.bstack1lll11l1llll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1llll1111_opy_(cls, bstack11111l11l1_opy_, event_url=bstack1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⓫")):
        config = {
            bstack1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⓬"): cls.default_headers()
        }
        logger.debug(bstack1111_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ⓭").format(bstack1111_opy_ (u"ࠫ࠱ࠦࠧ⓮").join([event[bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⓯")] for event in bstack11111l11l1_opy_])))
        response = bstack1llll1l1ll_opy_(bstack1111_opy_ (u"࠭ࡐࡐࡕࡗࠫ⓰"), cls.request_url(event_url), bstack11111l11l1_opy_, config)
        bstack11l11l1111l_opy_ = response.json()
    @classmethod
    def bstack1111lll11_opy_(cls, bstack11111l11l1_opy_, event_url=bstack1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⓱")):
        logger.debug(bstack1111_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⓲").format(bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⓳")]))
        if not bstack1l111l1l_opy_.bstack1ll1lll1ll11_opy_(bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⓴")]):
            logger.debug(bstack1111_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⓵").format(bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⓶")]))
            return
        bstack1ll11ll1_opy_ = bstack1l111l1l_opy_.bstack1ll1lll111l1_opy_(bstack11111l11l1_opy_[bstack1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⓷")], bstack11111l11l1_opy_.get(bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⓸")))
        if bstack1ll11ll1_opy_ != None:
            if bstack11111l11l1_opy_.get(bstack1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⓹")) != None:
                bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⓺")][bstack1111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⓻")] = bstack1ll11ll1_opy_
            else:
                bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⓼")] = bstack1ll11ll1_opy_
        if event_url == bstack1111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⓽"):
            cls.bstack1ll1lll1lll1_opy_()
            logger.debug(bstack1111_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⓾").format(bstack11111l11l1_opy_[bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⓿")]))
            cls.bstack1lll11l1llll_opy_.add(bstack11111l11l1_opy_)
        elif event_url == bstack1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭─"):
            cls.bstack1ll1llll1111_opy_([bstack11111l11l1_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1111l11_opy_(cls, logs):
        for log in logs:
            bstack1ll1lll11l1l_opy_ = {
                bstack1111_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ━"): bstack1111_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ│"),
                bstack1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ┃"): log[bstack1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ┄")],
                bstack1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ┅"): log[bstack1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ┆")],
                bstack1111_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ┇"): {},
                bstack1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ┈"): log[bstack1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ┉")],
            }
            if bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┊") in log:
                bstack1ll1lll11l1l_opy_[bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┋")] = log[bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┌")]
            elif bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ┍") in log:
                bstack1ll1lll11l1l_opy_[bstack1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ┎")] = log[bstack1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ┏")]
            cls.bstack1111lll11_opy_({
                bstack1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ┐"): bstack1111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ┑"),
                bstack1111_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ┒"): [bstack1ll1lll11l1l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1lll1l1ll_opy_(cls, steps):
        bstack1ll1lll1llll_opy_ = []
        for step in steps:
            bstack1ll1lll1l1l1_opy_ = {
                bstack1111_opy_ (u"࠭࡫ࡪࡰࡧࠫ┓"): bstack1111_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ└"),
                bstack1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ┕"): step[bstack1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ┖")],
                bstack1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭┗"): step[bstack1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ┘")],
                bstack1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭┙"): step[bstack1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ┚")],
                bstack1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ┛"): step[bstack1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ├")]
            }
            if bstack1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ┝") in step:
                bstack1ll1lll1l1l1_opy_[bstack1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ┞")] = step[bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ┟")]
            elif bstack1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ┠") in step:
                bstack1ll1lll1l1l1_opy_[bstack1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┡")] = step[bstack1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ┢")]
            bstack1ll1lll1llll_opy_.append(bstack1ll1lll1l1l1_opy_)
        cls.bstack1111lll11_opy_({
            bstack1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ┣"): bstack1111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭┤"),
            bstack1111_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ┥"): bstack1ll1lll1llll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111l1l11l1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l11l1l1l_opy_(cls, screenshot):
        cls.bstack1111lll11_opy_({
            bstack1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ┦"): bstack1111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ┧"),
            bstack1111_opy_ (u"࠭࡬ࡰࡩࡶࠫ┨"): [{
                bstack1111_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ┩"): bstack1111_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ┪"),
                bstack1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ┫"): datetime.datetime.utcnow().isoformat() + bstack1111_opy_ (u"ࠪ࡞ࠬ┬"),
                bstack1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ┭"): screenshot[bstack1111_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ┮")],
                bstack1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭┯"): screenshot[bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ┰")]
            }]
        }, event_url=bstack1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭┱"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1l11l1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1111lll11_opy_({
            bstack1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭┲"): bstack1111_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ┳"),
            bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭┴"): {
                bstack1111_opy_ (u"ࠧࡻࡵࡪࡦࠥ┵"): cls.current_test_uuid(),
                bstack1111_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ┶"): cls.bstack11111lllll_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack11111l11l1_opy_: bstack111111l111_opy_):
        bstack1llllll1l11_opy_ = {
            bstack1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ┷"): event,
            bstack11111l11l1_opy_.bstack1111111111_opy_(): bstack11111l11l1_opy_.bstack1llllll1lll_opy_(event)
        }
        cls.bstack1111lll11_opy_(bstack1llllll1l11_opy_)
        result = getattr(bstack11111l11l1_opy_, bstack1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ┸"), None)
        if event == bstack1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ┹"):
            threading.current_thread().bstackTestMeta = {bstack1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ┺"): bstack1111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ┻")}
        elif event == bstack1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ┼"):
            threading.current_thread().bstackTestMeta = {bstack1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭┽"): getattr(result, bstack1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ┾"), bstack1111_opy_ (u"ࠨࠩ┿"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭╀"), None) is None or os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ╁")] == bstack1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ╂")) and (os.environ.get(bstack1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ╃"), None) is None or os.environ[bstack1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ╄")] == bstack1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ╅")):
            return False
        return True
    @staticmethod
    def bstack1ll1llll11l1_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ╆"): bstack1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ╇"),
            bstack1111_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭╈"): bstack1111_opy_ (u"ࠫࡹࡸࡵࡦࠩ╉")
        }
        if os.environ.get(bstack1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ╊"), None):
            headers[bstack1111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭╋")] = bstack1111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ╌").format(os.environ[bstack1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ╍")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1111_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ╎").format(bstack1ll1lll11lll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ╏"), None)
    @staticmethod
    def bstack11111lllll_opy_(driver):
        return {
            bstack1111l1111l1_opy_(): bstack1111l1lll11_opy_(driver)
        }
    @staticmethod
    def bstack1ll1llll1l11_opy_(exception_info, report):
        return [{bstack1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ═"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll1ll1111_opy_(typename):
        if bstack1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ║") in typename:
            return bstack1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ╒")
        return bstack1111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ╓")