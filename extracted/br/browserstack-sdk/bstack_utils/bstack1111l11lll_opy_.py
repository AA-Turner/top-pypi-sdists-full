# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11l11lll_opy_, bstack11l111l1ll1_opy_, bstack1l11l11ll1_opy_, error_handler, bstack1111l1l1ll1_opy_, bstack1111l111l11_opy_, bstack1111l111lll_opy_, bstack11l1lll11_opy_, bstack11ll11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll1l1111ll_opy_ import bstack1lll1l111lll_opy_
import bstack_utils.bstack11l1l11lll_opy_ as bstack1l11l1l1l1_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
import bstack_utils.accessibility as bstack1lllll111l_opy_
from bstack_utils.bstack1l1lll111l_opy_ import bstack1l1lll111l_opy_
from bstack_utils.bstack11111lll1l_opy_ import bstack11111111l1_opy_
from bstack_utils.constants import bstack1lllll1lll_opy_
bstack1lll111111ll_opy_ = bstack11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ⌤")
logger = logging.getLogger(__name__)
class bstack1ll111l1_opy_:
    bstack1lll1l1111ll_opy_ = None
    bs_config = None
    bstack1l1l1l1l1l_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111ll11l1ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def launch(cls, bs_config, bstack1l1l1l1l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1l1l1l1l_opy_ = bstack1l1l1l1l1l_opy_
        try:
            cls.bstack1ll1lllllll1_opy_()
            bstack11l111l111l_opy_ = bstack11l11l11lll_opy_(bs_config)
            bstack11l111lll11_opy_ = bstack11l111l1ll1_opy_(bs_config)
            data = bstack1l11l1l1l1_opy_.bstack1lll1111111l_opy_(bs_config, bstack1l1l1l1l1l_opy_)
            config = {
                bstack11l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ⌥"): (bstack11l111l111l_opy_, bstack11l111lll11_opy_),
                bstack11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⌦"): cls.default_headers()
            }
            response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠫࡕࡕࡓࡕࠩ⌧"), cls.request_url(bstack11l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ⌨")), data, config)
            if response.status_code != 200:
                bstack11lllll1_opy_ = response.json()
                if bstack11lllll1_opy_[bstack11l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ〈")] == False:
                    cls.bstack1lll1111l11l_opy_(bstack11lllll1_opy_)
                    return
                cls.bstack1ll1llll1l11_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ〉")])
                cls.bstack1ll1llll1l1l_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⌫")])
                return None
            bstack1ll1lllll11l_opy_ = cls.bstack1lll11111ll1_opy_(response)
            return bstack1ll1lllll11l_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ⌬").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111lll11111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def stop(cls, bstack1ll1lllll111_opy_=None):
        if not bstack11l1ll111l_opy_.on() and not bstack1lllll111l_opy_.on():
            return
        if os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⌭")) == bstack11l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⌮") or os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⌯")) == bstack11l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⌰"):
            logger.error(bstack11l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪ⌱"))
            return {
                bstack11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ⌲"): bstack11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⌳"),
                bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⌴"): bstack11l11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩ⌵")
            }
        try:
            cls.bstack1lll1l1111ll_opy_.shutdown()
            data = {
                bstack11l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⌶"): bstack11l1lll11_opy_()
            }
            if not bstack1ll1lllll111_opy_ is None:
                data[bstack11l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ⌷")] = [{
                    bstack11l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ⌸"): bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭⌹"),
                    bstack11l11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩ⌺"): bstack1ll1lllll111_opy_
                }]
            config = {
                bstack11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⌻"): cls.default_headers()
            }
            bstack11l111111ll_opy_ = bstack11l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬ⌼").format(os.environ[bstack11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⌽")])
            bstack1lll11111lll_opy_ = cls.request_url(bstack11l111111ll_opy_)
            response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"࠭ࡐࡖࡖࠪ⌾"), bstack1lll11111lll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l11_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨ⌿"))
        except Exception as error:
            logger.error(bstack11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ⍀") + str(error))
            return {
                bstack11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⍁"): bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⍂"),
                bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⍃"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11111ll1_opy_(cls, response):
        bstack11lllll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1ll1lllll11l_opy_ = {}
        if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠬࡰࡷࡵࠩ⍄")) is None:
            os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⍅")] = bstack11l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⍆")
        else:
            os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⍇")] = bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠩ࡭ࡻࡹ࠭⍈"), bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⍉"))
        os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⍊")] = bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⍋"), bstack11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⍌"))
        logger.info(bstack11l11_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬ⍍") + os.getenv(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⍎")));
        if bstack11l1ll111l_opy_.bstack1ll1llllll11_opy_(cls.bs_config, cls.bstack1l1l1l1l1l_opy_.get(bstack11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⍏"), bstack11l11_opy_ (u"ࠪࠫ⍐"))) is True:
            bstack1lll11lll1l1_opy_, build_hashed_id, bstack1lll11111l11_opy_ = cls.bstack1lll111111l1_opy_(bstack11lllll1_opy_)
            if bstack1lll11lll1l1_opy_ != None and build_hashed_id != None:
                bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⍑")] = {
                    bstack11l11_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨ⍒"): bstack1lll11lll1l1_opy_,
                    bstack11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⍓"): build_hashed_id,
                    bstack11l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⍔"): bstack1lll11111l11_opy_
                }
            else:
                bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⍕")] = {}
        else:
            bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⍖")] = {}
        bstack1lll11111111_opy_, build_hashed_id = cls.bstack1ll1llll11ll_opy_(bstack11lllll1_opy_)
        if bstack1lll11111111_opy_ != None and build_hashed_id != None:
            bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⍗")] = {
                bstack11l11_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨ⍘"): bstack1lll11111111_opy_,
                bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⍙"): build_hashed_id,
            }
        else:
            bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍚")] = {}
        if bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⍛")].get(bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⍜")) != None or bstack1ll1lllll11l_opy_[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⍝")].get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⍞")) != None:
            cls.bstack1ll1lllll1ll_opy_(bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠫ࡯ࡽࡴࠨ⍟")), bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⍠")))
        return bstack1ll1lllll11l_opy_
    @classmethod
    def bstack1lll111111l1_opy_(cls, bstack11lllll1_opy_):
        if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⍡")) == None:
            cls.bstack1ll1llll1l11_opy_()
            return [None, None, None]
        if bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⍢")][bstack11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ⍣")] != True:
            cls.bstack1ll1llll1l11_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⍤")])
            return [None, None, None]
        logger.debug(bstack11l11_opy_ (u"ࠪࡿࢂࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ⍥").format(bstack1lllll1lll_opy_))
        os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ⍦")] = bstack11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ⍧")
        if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"࠭ࡪࡸࡶࠪ⍨")):
            os.environ[bstack11l11_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫ⍩")] = json.dumps({
                bstack11l11_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ⍪"): bstack11l11l11lll_opy_(cls.bs_config),
                bstack11l11_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫ⍫"): bstack11l111l1ll1_opy_(cls.bs_config)
            })
        if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⍬")):
            os.environ[bstack11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ⍭")] = bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⍮")]
        if bstack11lllll1_opy_[bstack11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⍯")].get(bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⍰"), {}).get(bstack11l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⍱")):
            os.environ[bstack11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⍲")] = str(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⍳")][bstack11l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⍴")][bstack11l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⍵")])
        else:
            os.environ[bstack11l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⍶")] = bstack11l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⍷")
        return [bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠨ࡬ࡺࡸࠬ⍸")], bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⍹")], os.environ[bstack11l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⍺")]]
    @classmethod
    def bstack1ll1llll11ll_opy_(cls, bstack11lllll1_opy_):
        if bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⍻")) == None:
            cls.bstack1ll1llll1l1l_opy_()
            return [None, None]
        if bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⍼")][bstack11l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⍽")] != True:
            cls.bstack1ll1llll1l1l_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍾")])
            return [None, None]
        if bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⍿")].get(bstack11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⎀")):
            logger.debug(bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ⎁"))
            parsed = json.loads(os.getenv(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⎂"), bstack11l11_opy_ (u"ࠬࢁࡽࠨ⎃")))
            capabilities = bstack1l11l1l1l1_opy_.bstack1lll11111l1l_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⎄")][bstack11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⎅")][bstack11l11_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ⎆")], bstack11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⎇"), bstack11l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⎈"))
            bstack1lll11111111_opy_ = capabilities[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩ⎉")]
            os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⎊")] = bstack1lll11111111_opy_
            if bstack11l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ⎋") in bstack11lllll1_opy_ and bstack11lllll1_opy_.get(bstack11l11_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ⎌")) is None:
                parsed[bstack11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⎍")] = capabilities[bstack11l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⎎")]
            os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⎏")] = json.dumps(parsed)
            scripts = bstack1l11l1l1l1_opy_.bstack1lll11111l1l_opy_(bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⎐")][bstack11l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⎑")][bstack11l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ⎒")], bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⎓"), bstack11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩ⎔"))
            bstack1l1lll111l_opy_.bstack1l111l111_opy_(scripts)
            commands = bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⎕")][bstack11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⎖")][bstack11l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬ⎗")].get(bstack11l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ⎘"))
            bstack1l1lll111l_opy_.bstack11l1111ll1l_opy_(commands)
            bstack11l111ll11l_opy_ = capabilities.get(bstack11l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ⎙"))
            bstack1l1lll111l_opy_.bstack11l11111lll_opy_(bstack11l111ll11l_opy_)
            bstack1l1lll111l_opy_.store()
        return [bstack1lll11111111_opy_, bstack11lllll1_opy_[bstack11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⎚")]]
    @classmethod
    def bstack1ll1llll1l11_opy_(cls, response=None):
        os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⎛")] = bstack11l11_opy_ (u"ࠩࡱࡹࡱࡲࠧ⎜")
        os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⎝")] = bstack11l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⎞")
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ⎟")] = bstack11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⎠")
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭⎡")] = bstack11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ⎢")
        os.environ[bstack11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⎣")] = bstack11l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⎤")
        cls.bstack1lll1111l11l_opy_(response, bstack11l11_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦ⎥"))
        return [None, None, None]
    @classmethod
    def bstack1ll1llll1l1l_opy_(cls, response=None):
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⎦")] = bstack11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⎧")
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⎨")] = bstack11l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭⎩")
        os.environ[bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⎪")] = bstack11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⎫")
        cls.bstack1lll1111l11l_opy_(response, bstack11l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ⎬"))
        return [None, None, None]
    @classmethod
    def bstack1ll1lllll1ll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⎭")] = jwt
        os.environ[bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⎮")] = build_hashed_id
    @classmethod
    def bstack1lll1111l11l_opy_(cls, response=None, product=bstack11l11_opy_ (u"ࠢࠣ⎯")):
        if response == None or response.get(bstack11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ⎰")) == None:
            logger.error(product + bstack11l11_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦ⎱"))
            return
        for error in response[bstack11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ⎲")]:
            bstack1111ll1l1ll_opy_ = error[bstack11l11_opy_ (u"ࠫࡰ࡫ࡹࠨ⎳")]
            error_message = error[bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⎴")]
            if error_message:
                if bstack1111ll1l1ll_opy_ == bstack11l11_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧ⎵"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l11_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣ⎶") + product + bstack11l11_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ⎷"))
    @classmethod
    def bstack1ll1lllllll1_opy_(cls):
        if cls.bstack1lll1l1111ll_opy_ is not None:
            return
        cls.bstack1lll1l1111ll_opy_ = bstack1lll1l111lll_opy_(cls.bstack1ll1llllll1l_opy_)
        cls.bstack1lll1l1111ll_opy_.start()
    @classmethod
    def bstack11111l1l1l_opy_(cls):
        if cls.bstack1lll1l1111ll_opy_ is None:
            return
        cls.bstack1lll1l1111ll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1llllll1l_opy_(cls, bstack111111ll11_opy_, event_url=bstack11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⎸")):
        config = {
            bstack11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⎹"): cls.default_headers()
        }
        logger.debug(bstack11l11_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦ⎺").format(bstack11l11_opy_ (u"ࠬ࠲ࠠࠨ⎻").join([event[bstack11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⎼")] for event in bstack111111ll11_opy_])))
        response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠧࡑࡑࡖࡘࠬ⎽"), cls.request_url(event_url), bstack111111ll11_opy_, config)
        bstack11l11l11l1l_opy_ = response.json()
    @classmethod
    def bstack11l11lll_opy_(cls, bstack111111ll11_opy_, event_url=bstack11l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⎾")):
        logger.debug(bstack11l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⎿").format(bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⏀")]))
        if not bstack1l11l1l1l1_opy_.bstack1ll1llll111l_opy_(bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⏁")]):
            logger.debug(bstack11l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⏂").format(bstack111111ll11_opy_[bstack11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⏃")]))
            return
        bstack111ll1ll1l_opy_ = bstack1l11l1l1l1_opy_.bstack1ll1llll1ll1_opy_(bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⏄")], bstack111111ll11_opy_.get(bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⏅")))
        if bstack111ll1ll1l_opy_ != None:
            if bstack111111ll11_opy_.get(bstack11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⏆")) != None:
                bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⏇")][bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⏈")] = bstack111ll1ll1l_opy_
            else:
                bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⏉")] = bstack111ll1ll1l_opy_
        if event_url == bstack11l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⏊"):
            cls.bstack1ll1lllllll1_opy_()
            logger.debug(bstack11l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⏋").format(bstack111111ll11_opy_[bstack11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⏌")]))
            cls.bstack1lll1l1111ll_opy_.add(bstack111111ll11_opy_)
        elif event_url == bstack11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⏍"):
            cls.bstack1ll1llllll1l_opy_([bstack111111ll11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1l1l11l_opy_(cls, logs):
        for log in logs:
            bstack1ll1llll11l1_opy_ = {
                bstack11l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⏎"): bstack11l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭⏏"),
                bstack11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⏐"): log[bstack11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⏑")],
                bstack11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⏒"): log[bstack11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⏓")],
                bstack11l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩ⏔"): {},
                bstack11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⏕"): log[bstack11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⏖")],
            }
            if bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⏗") in log:
                bstack1ll1llll11l1_opy_[bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⏘")] = log[bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⏙")]
            elif bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⏚") in log:
                bstack1ll1llll11l1_opy_[bstack11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⏛")] = log[bstack11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⏜")]
            cls.bstack11l11lll_opy_({
                bstack11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⏝"): bstack11l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⏞"),
                bstack11l11_opy_ (u"࠭࡬ࡰࡩࡶࠫ⏟"): [bstack1ll1llll11l1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1lllll1l1_opy_(cls, steps):
        bstack1ll1llllllll_opy_ = []
        for step in steps:
            bstack1ll1llll1111_opy_ = {
                bstack11l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⏠"): bstack11l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫ⏡"),
                bstack11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⏢"): step[bstack11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⏣")],
                bstack11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⏤"): step[bstack11l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⏥")],
                bstack11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⏦"): step[bstack11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⏧")],
                bstack11l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⏨"): step[bstack11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⏩")]
            }
            if bstack11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⏪") in step:
                bstack1ll1llll1111_opy_[bstack11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⏫")] = step[bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⏬")]
            elif bstack11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⏭") in step:
                bstack1ll1llll1111_opy_[bstack11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⏮")] = step[bstack11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⏯")]
            bstack1ll1llllllll_opy_.append(bstack1ll1llll1111_opy_)
        cls.bstack11l11lll_opy_({
            bstack11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⏰"): bstack11l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⏱"),
            bstack11l11_opy_ (u"ࠫࡱࡵࡧࡴࠩ⏲"): bstack1ll1llllllll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1ll111lll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l111111l_opy_(cls, screenshot):
        cls.bstack11l11lll_opy_({
            bstack11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⏳"): bstack11l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⏴"),
            bstack11l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⏵"): [{
                bstack11l11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⏶"): bstack11l11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫ⏷"),
                bstack11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⏸"): datetime.datetime.utcnow().isoformat() + bstack11l11_opy_ (u"ࠫ࡟࠭⏹"),
                bstack11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⏺"): screenshot[bstack11l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬ⏻")],
                bstack11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⏼"): screenshot[bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⏽")]
            }]
        }, event_url=bstack11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⏾"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll1111l11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l11lll_opy_({
            bstack11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⏿"): bstack11l11_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ␀"),
            bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ␁"): {
                bstack11l11_opy_ (u"ࠨࡵࡶ࡫ࡧࠦ␂"): cls.current_test_uuid(),
                bstack11l11_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨ␃"): cls.bstack1111l11l1l_opy_(driver)
            }
        })
    @classmethod
    def bstack1111l11111_opy_(cls, event: str, bstack111111ll11_opy_: bstack11111111l1_opy_):
        bstack11111l1lll_opy_ = {
            bstack11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ␄"): event,
            bstack111111ll11_opy_.bstack1111111lll_opy_(): bstack111111ll11_opy_.bstack1lllllll1l1_opy_(event)
        }
        cls.bstack11l11lll_opy_(bstack11111l1lll_opy_)
        result = getattr(bstack111111ll11_opy_, bstack11l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ␅"), None)
        if event == bstack11l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ␆"):
            threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ␇"): bstack11l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭␈")}
        elif event == bstack11l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ␉"):
            threading.current_thread().bstackTestMeta = {bstack11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ␊"): getattr(result, bstack11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ␋"), bstack11l11_opy_ (u"ࠩࠪ␌"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ␍"), None) is None or os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ␎")] == bstack11l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ␏")) and (os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ␐"), None) is None or os.environ[bstack11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ␑")] == bstack11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ␒")):
            return False
        return True
    @staticmethod
    def bstack1ll1llll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ␓"): bstack11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭␔"),
            bstack11l11_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧ␕"): bstack11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ␖")
        }
        if os.environ.get(bstack11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ␗"), None):
            headers[bstack11l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ␘")] = bstack11l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ␙").format(os.environ[bstack11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨ␚")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ␛").format(bstack1lll111111ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ␜"), None)
    @staticmethod
    def bstack1111l11l1l_opy_(driver):
        return {
            bstack1111l1l1ll1_opy_(): bstack1111l111l11_opy_(driver)
        }
    @staticmethod
    def bstack1lll1111l111_opy_(exception_info, report):
        return [{bstack11l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ␝"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll1l11lll_opy_(typename):
        if bstack11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ␞") in typename:
            return bstack11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ␟")
        return bstack11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ␠")