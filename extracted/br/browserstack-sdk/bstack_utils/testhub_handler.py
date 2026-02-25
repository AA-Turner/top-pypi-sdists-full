# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11l1111l_opy_, bstack11l11l11l11_opy_, bstack11l11llll_opy_, error_handler, bstack111l1llll1l_opy_, bstack1111lll1l11_opy_, bstack111l1l11ll1_opy_, current_time, bstack11llll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll1l1l1l1l_opy_ import bstack1lll1l1l1111_opy_
import bstack_utils.bstack111l111l11_opy_ as bstack1l11l1l111_opy_
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
import bstack_utils.accessibility as bstack1l111ll111_opy_
from bstack_utils.bstack111llllll1_opy_ import bstack111llllll1_opy_
from bstack_utils.test_data import bstack1lllllll1ll_opy_
from bstack_utils.constants import bstack1l1l1l11l1_opy_
bstack1lll11111l11_opy_ = bstack11l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ⌯")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1lll1l1l1l1l_opy_ = None
    bs_config = None
    bstack11l1l11l1_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111lll1llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def launch(cls, bs_config, bstack11l1l11l1_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1l11l1_opy_ = bstack11l1l11l1_opy_
        try:
            cls.bstack1lll111l111l_opy_()
            bstack11l11lll1ll_opy_ = bstack11l11l1111l_opy_(bs_config)
            bstack11l11l11111_opy_ = bstack11l11l11l11_opy_(bs_config)
            data = bstack1l11l1l111_opy_.bstack1lll1111l1l1_opy_(bs_config, bstack11l1l11l1_opy_)
            config = {
                bstack11l1l11_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ⌰"): (bstack11l11lll1ll_opy_, bstack11l11l11111_opy_),
                bstack11l1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⌱"): cls.default_headers()
            }
            response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠨࡒࡒࡗ࡙࠭⌲"), cls.request_url(bstack11l1l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ⌳")), data, config)
            if response.status_code != 200:
                bstack1lllllll1l_opy_ = response.json()
                if bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⌴")] == False:
                    cls.bstack1lll111l1l1l_opy_(bstack1lllllll1l_opy_)
                    return
                cls.bstack1lll1111l11l_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⌵")])
                cls.bstack1lll111l1111_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⌶")])
                return None
            bstack1lll111l11ll_opy_ = cls.bstack1lll111l1lll_opy_(response)
            return bstack1lll111l11ll_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ⌷").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111lll1ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def stop(cls, bstack1lll111l1l11_opy_=None):
        if not bstack1l111111_opy_.on() and not bstack1l111ll111_opy_.on():
            return
        if os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⌸")) == bstack11l1l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ⌹") or os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⌺")) == bstack11l1l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⌻"):
            logger.error(bstack11l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ⌼"))
            return {
                bstack11l1l11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⌽"): bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ⌾"),
                bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⌿"): bstack11l1l11_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭⍀")
            }
        try:
            cls.bstack1lll1l1l1l1l_opy_.shutdown()
            data = {
                bstack11l1l11_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ⍁"): current_time()
            }
            if not bstack1lll111l1l11_opy_ is None:
                data[bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ⍂")] = [{
                    bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ⍃"): bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ⍄"),
                    bstack11l1l11_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭⍅"): bstack1lll111l1l11_opy_
                }]
            config = {
                bstack11l1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⍆"): cls.default_headers()
            }
            bstack11l111l11ll_opy_ = bstack11l1l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩ⍇").format(os.environ[bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ⍈")])
            bstack1lll11111ll1_opy_ = cls.request_url(bstack11l111l11ll_opy_)
            response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠪࡔ࡚࡚ࠧ⍉"), bstack1lll11111ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1l11_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ⍊"))
        except Exception as error:
            logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤ⍋") + str(error))
            return {
                bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⍌"): bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭⍍"),
                bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⍎"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll111l1lll_opy_(cls, response):
        bstack1lllllll1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll111l11ll_opy_ = {}
        if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠩ࡭ࡻࡹ࠭⍏")) is None:
            os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⍐")] = bstack11l1l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⍑")
        else:
            os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⍒")] = bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"࠭ࡪࡸࡶࠪ⍓"), bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⍔"))
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⍕")] = bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⍖"), bstack11l1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⍗"))
        logger.info(bstack11l1l11_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩ⍘") + os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⍙")));
        if bstack1l111111_opy_.bstack1lll1111ll1l_opy_(cls.bs_config, cls.bstack11l1l11l1_opy_.get(bstack11l1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ⍚"), bstack11l1l11_opy_ (u"ࠧࠨ⍛"))) is True:
            bstack1lll1l11l1l1_opy_, build_hashed_id, bstack1lll1111lll1_opy_ = cls.bstack1lll1111111l_opy_(bstack1lllllll1l_opy_)
            if bstack1lll1l11l1l1_opy_ != None and build_hashed_id != None:
                bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⍜")] = {
                    bstack11l1l11_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬ⍝"): bstack1lll1l11l1l1_opy_,
                    bstack11l1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⍞"): build_hashed_id,
                    bstack11l1l11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⍟"): bstack1lll1111lll1_opy_
                }
            else:
                bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⍠")] = {}
        else:
            bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⍡")] = {}
        bstack1lll111ll111_opy_, build_hashed_id = cls.bstack1lll1111ll11_opy_(bstack1lllllll1l_opy_)
        if bstack1lll111ll111_opy_ != None and build_hashed_id != None:
            bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍢")] = {
                bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬ⍣"): bstack1lll111ll111_opy_,
                bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⍤"): build_hashed_id,
            }
        else:
            bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⍥")] = {}
        if bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⍦")].get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⍧")) != None or bstack1lll111l11ll_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍨")].get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⍩")) != None:
            cls.bstack1lll11111l1l_opy_(bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡬ࡺࡸࠬ⍪")), bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⍫")))
        return bstack1lll111l11ll_opy_
    @classmethod
    def bstack1lll1111111l_opy_(cls, bstack1lllllll1l_opy_):
        if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⍬")) == None:
            cls.bstack1lll1111l11l_opy_()
            return [None, None, None]
        if bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⍭")][bstack11l1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⍮")] != True:
            cls.bstack1lll1111l11l_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⍯")])
            return [None, None, None]
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡼࡿࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩ⍰").format(bstack1l1l1l11l1_opy_))
        os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⍱")] = bstack11l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⍲")
        if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠪ࡮ࡼࡺࠧ⍳")):
            os.environ[bstack11l1l11_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨ⍴")] = json.dumps({
                bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ⍵"): bstack11l11l1111l_opy_(cls.bs_config),
                bstack11l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨ⍶"): bstack11l11l11l11_opy_(cls.bs_config)
            })
        if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⍷")):
            os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ⍸")] = bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⍹")]
        if bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⍺")].get(bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⍻"), {}).get(bstack11l1l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⍼")):
            os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⍽")] = str(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⍾")][bstack11l1l11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⍿")][bstack11l1l11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⎀")])
        else:
            os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⎁")] = bstack11l1l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⎂")
        return [bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡰࡷࡵࠩ⎃")], bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⎄")], os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⎅")]]
    @classmethod
    def bstack1lll1111ll11_opy_(cls, bstack1lllllll1l_opy_):
        if bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⎆")) == None:
            cls.bstack1lll111l1111_opy_()
            return [None, None]
        if bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⎇")][bstack11l1l11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⎈")] != True:
            cls.bstack1lll111l1111_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎉")])
            return [None, None]
        if bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⎊")].get(bstack11l1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⎋")):
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⎌"))
            parsed = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⎍"), bstack11l1l11_opy_ (u"ࠩࡾࢁࠬ⎎")))
            capabilities = bstack1l11l1l111_opy_.bstack1lll111111l1_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎏")][bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⎐")][bstack11l1l11_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⎑")], bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⎒"), bstack11l1l11_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭⎓"))
            bstack1lll111ll111_opy_ = capabilities[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭⎔")]
            os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⎕")] = bstack1lll111ll111_opy_
            if bstack11l1l11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⎖") in bstack1lllllll1l_opy_ and bstack1lllllll1l_opy_.get(bstack11l1l11_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ⎗")) is None:
                parsed[bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⎘")] = capabilities[bstack11l1l11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⎙")]
            os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⎚")] = json.dumps(parsed)
            scripts = bstack1l11l1l111_opy_.bstack1lll111111l1_opy_(bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⎛")][bstack11l1l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⎜")][bstack11l1l11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ⎝")], bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⎞"), bstack11l1l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭⎟"))
            bstack111llllll1_opy_.bstack11l11l1ll_opy_(scripts)
            commands = bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⎠")][bstack11l1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⎡")][bstack11l1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩ⎢")].get(bstack11l1l11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ⎣"))
            bstack111llllll1_opy_.bstack11l111lllll_opy_(commands)
            bstack11l111lll1l_opy_ = capabilities.get(bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ⎤"))
            bstack111llllll1_opy_.bstack11l111l1ll1_opy_(bstack11l111lll1l_opy_)
            bstack111llllll1_opy_.store()
        return [bstack1lll111ll111_opy_, bstack1lllllll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⎥")]]
    @classmethod
    def bstack1lll1111l11l_opy_(cls, response=None):
        os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⎦")] = bstack11l1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⎧")
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⎨")] = bstack11l1l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭⎩")
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ⎪")] = bstack11l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ⎫")
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ⎬")] = bstack11l1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⎭")
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⎮")] = bstack11l1l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⎯")
        cls.bstack1lll111l1l1l_opy_(response, bstack11l1l11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ⎰"))
        return [None, None, None]
    @classmethod
    def bstack1lll111l1111_opy_(cls, response=None):
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⎱")] = bstack11l1l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⎲")
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⎳")] = bstack11l1l11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⎴")
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⎵")] = bstack11l1l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⎶")
        cls.bstack1lll111l1l1l_opy_(response, bstack11l1l11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ⎷"))
        return [None, None, None]
    @classmethod
    def bstack1lll11111l1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⎸")] = jwt
        os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⎹")] = build_hashed_id
    @classmethod
    def bstack1lll111l1l1l_opy_(cls, response=None, product=bstack11l1l11_opy_ (u"ࠦࠧ⎺")):
        if response == None or response.get(bstack11l1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ⎻")) == None:
            logger.error(product + bstack11l1l11_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣ⎼"))
            return
        for error in response[bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ⎽")]:
            bstack111l11ll1ll_opy_ = error[bstack11l1l11_opy_ (u"ࠨ࡭ࡨࡽࠬ⎾")]
            error_message = error[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⎿")]
            if error_message:
                if bstack111l11ll1ll_opy_ == bstack11l1l11_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ⏀"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1l11_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧ⏁") + product + bstack11l1l11_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ⏂"))
    @classmethod
    def bstack1lll111l111l_opy_(cls):
        if cls.bstack1lll1l1l1l1l_opy_ is not None:
            return
        cls.bstack1lll1l1l1l1l_opy_ = bstack1lll1l1l1111_opy_(cls.bstack1lll11111lll_opy_)
        cls.bstack1lll1l1l1l1l_opy_.start()
    @classmethod
    def bstack1llllllll1l_opy_(cls):
        if cls.bstack1lll1l1l1l1l_opy_ is None:
            return
        cls.bstack1lll1l1l1l1l_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11111lll_opy_(cls, bstack111111ll11_opy_, event_url=bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⏃")):
        config = {
            bstack11l1l11_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ⏄"): cls.default_headers()
        }
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣ⏅").format(bstack11l1l11_opy_ (u"ࠩ࠯ࠤࠬ⏆").join([event[bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⏇")] for event in bstack111111ll11_opy_])))
        response = bstack11l11llll_opy_(bstack11l1l11_opy_ (u"ࠫࡕࡕࡓࡕࠩ⏈"), cls.request_url(event_url), bstack111111ll11_opy_, config)
        bstack11l11l11lll_opy_ = response.json()
    @classmethod
    def bstack1l1ll11lll_opy_(cls, bstack111111ll11_opy_, event_url=bstack11l1l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⏉")):
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⏊").format(bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⏋")]))
        if not bstack1l11l1l111_opy_.bstack1lll111ll1l1_opy_(bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⏌")]):
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⏍").format(bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⏎")]))
            return
        bstack1llll111l_opy_ = bstack1l11l1l111_opy_.bstack1lll1111l1ll_opy_(bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⏏")], bstack111111ll11_opy_.get(bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⏐")))
        if bstack1llll111l_opy_ != None:
            if bstack111111ll11_opy_.get(bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⏑")) != None:
                bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⏒")][bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⏓")] = bstack1llll111l_opy_
            else:
                bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⏔")] = bstack1llll111l_opy_
        if event_url == bstack11l1l11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ⏕"):
            cls.bstack1lll111l111l_opy_()
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⏖").format(bstack111111ll11_opy_[bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⏗")]))
            cls.bstack1lll1l1l1l1l_opy_.add(bstack111111ll11_opy_)
        elif event_url == bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⏘"):
            cls.bstack1lll11111lll_opy_([bstack111111ll11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l111ll1_opy_(cls, logs):
        for log in logs:
            bstack1lll1111llll_opy_ = {
                bstack11l1l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⏙"): bstack11l1l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪ⏚"),
                bstack11l1l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⏛"): log[bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⏜")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⏝"): log[bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⏞")],
                bstack11l1l11_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭⏟"): {},
                bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⏠"): log[bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⏡")],
            }
            if bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⏢") in log:
                bstack1lll1111llll_opy_[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⏣")] = log[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⏤")]
            elif bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⏥") in log:
                bstack1lll1111llll_opy_[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⏦")] = log[bstack11l1l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⏧")]
            cls.bstack1l1ll11lll_opy_({
                bstack11l1l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⏨"): bstack11l1l11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⏩"),
                bstack11l1l11_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⏪"): [bstack1lll1111llll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll111ll11l_opy_(cls, steps):
        bstack1lll1111l111_opy_ = []
        for step in steps:
            bstack1lll111l11l1_opy_ = {
                bstack11l1l11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⏫"): bstack11l1l11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ⏬"),
                bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⏭"): step[bstack11l1l11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⏮")],
                bstack11l1l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⏯"): step[bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⏰")],
                bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⏱"): step[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⏲")],
                bstack11l1l11_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⏳"): step[bstack11l1l11_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⏴")]
            }
            if bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⏵") in step:
                bstack1lll111l11l1_opy_[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⏶")] = step[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⏷")]
            elif bstack11l1l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⏸") in step:
                bstack1lll111l11l1_opy_[bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⏹")] = step[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⏺")]
            bstack1lll1111l111_opy_.append(bstack1lll111l11l1_opy_)
        cls.bstack1l1ll11lll_opy_({
            bstack11l1l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⏻"): bstack11l1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⏼"),
            bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭⏽"): bstack1lll1111l111_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1lll11llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack11l1lllll_opy_(cls, screenshot):
        cls.bstack1l1ll11lll_opy_({
            bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⏾"): bstack11l1l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⏿"),
            bstack11l1l11_opy_ (u"ࠫࡱࡵࡧࡴࠩ␀"): [{
                bstack11l1l11_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ␁"): bstack11l1l11_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ␂"),
                bstack11l1l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ␃"): datetime.datetime.utcnow().isoformat() + bstack11l1l11_opy_ (u"ࠨ࡜ࠪ␄"),
                bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ␅"): screenshot[bstack11l1l11_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ␆")],
                bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ␇"): screenshot[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ␈")]
            }]
        }, event_url=bstack11l1l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ␉"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1lllll1ll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1ll11lll_opy_({
            bstack11l1l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ␊"): bstack11l1l11_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ␋"),
            bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ␌"): {
                bstack11l1l11_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ␍"): cls.current_test_uuid(),
                bstack11l1l11_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥ␎"): cls.bstack1111ll1ll1_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack111111ll11_opy_: bstack1lllllll1ll_opy_):
        bstack111111l1l1_opy_ = {
            bstack11l1l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ␏"): event,
            bstack111111ll11_opy_.bstack1111l11l1l_opy_(): bstack111111ll11_opy_.bstack1llllllll11_opy_(event)
        }
        cls.bstack1l1ll11lll_opy_(bstack111111l1l1_opy_)
        result = getattr(bstack111111ll11_opy_, bstack11l1l11_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭␐"), None)
        if event == bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ␑"):
            threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ␒"): bstack11l1l11_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ␓")}
        elif event == bstack11l1l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ␔"):
            threading.current_thread().bstackTestMeta = {bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ␕"): getattr(result, bstack11l1l11_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ␖"), bstack11l1l11_opy_ (u"࠭ࠧ␗"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ␘"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ␙")] == bstack11l1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢ␚")) and (os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ␛"), None) is None or os.environ[bstack11l1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ␜")] == bstack11l1l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ␝")):
            return False
        return True
    @staticmethod
    def bstack1lll111l1ll1_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ␞"): bstack11l1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ␟"),
            bstack11l1l11_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫ␠"): bstack11l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ␡")
        }
        if os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ␢"), None):
            headers[bstack11l1l11_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ␣")] = bstack11l1l11_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ␤").format(os.environ[bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥ␥")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1l11_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭␦").format(bstack1lll11111l11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ␧"), None)
    @staticmethod
    def bstack1111ll1ll1_opy_(driver):
        return {
            bstack111l1llll1l_opy_(): bstack1111lll1l11_opy_(driver)
        }
    @staticmethod
    def bstack1lll111111ll_opy_(exception_info, report):
        return [{bstack11l1l11_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ␨"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll1ll1l11_opy_(typename):
        if bstack11l1l11_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ␩") in typename:
            return bstack11l1l11_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ␪")
        return bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ␫")