# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1lll11l_opy_, bstack11lll111111_opy_, bstack1l11l1l1l1_opy_, error_handler, bstack11l11l11ll1_opy_, bstack111ll1lll11_opy_, bstack111llll1l11_opy_, bstack1l1l11lll_opy_, bstack1ll11l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lllllllll11_opy_ import bstack111111111l1_opy_
import bstack_utils.bstack1111l111l_opy_ as bstack1ll1l11ll1_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack11l1l1111_opy_
import bstack_utils.accessibility as bstack1ll1ll1111_opy_
from bstack_utils.bstack1l11l1l111_opy_ import bstack1l11l1l111_opy_
from bstack_utils.bstack111lll11ll_opy_ import bstack111l11ll1l_opy_
bstack1llll1ll11ll_opy_ = bstack11l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩₚ")
logger = logging.getLogger(__name__)
class bstack1lllllllll_opy_:
    bstack1lllllllll11_opy_ = None
    bs_config = None
    bstack111ll1ll_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1l1l_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def launch(cls, bs_config, bstack111ll1ll_opy_):
        cls.bs_config = bs_config
        cls.bstack111ll1ll_opy_ = bstack111ll1ll_opy_
        try:
            cls.bstack1lllll1111l1_opy_()
            bstack11ll1l1l1l1_opy_ = bstack11ll1lll11l_opy_(bs_config)
            bstack11ll1l11lll_opy_ = bstack11lll111111_opy_(bs_config)
            data = bstack1ll1l11ll1_opy_.bstack1llll1lll11l_opy_(bs_config, bstack111ll1ll_opy_)
            config = {
                bstack11l1_opy_ (u"ࠪࡥࡺࡺࡨࠨₛ"): (bstack11ll1l1l1l1_opy_, bstack11ll1l11lll_opy_),
                bstack11l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬₜ"): cls.default_headers()
            }
            response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡖࡏࡔࡖࠪ₝"), cls.request_url(bstack11l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭₞")), data, config)
            if response.status_code != 200:
                bstack1l111llll1_opy_ = response.json()
                if bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ₟")] == False:
                    cls.bstack1lllll1111ll_opy_(bstack1l111llll1_opy_)
                    return
                cls.bstack1llll1llll11_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ₠")])
                cls.bstack1lllll111l11_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ₡")])
                return None
            bstack1llll1ll1111_opy_ = cls.bstack1lllll111lll_opy_(response)
            return bstack1llll1ll1111_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣ₢").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1llll1ll1l1l_opy_=None):
        if not bstack11l1l1111_opy_.on() and not bstack1ll1ll1111_opy_.on():
            return
        if os.environ.get(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ₣")) == bstack11l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ₤") or os.environ.get(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ₥")) == bstack11l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ₦"):
            logger.error(bstack11l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ₧"))
            return {
                bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ₨"): bstack11l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ₩"),
                bstack11l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ₪"): bstack11l1_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪ₫")
            }
        try:
            cls.bstack1lllllllll11_opy_.shutdown()
            data = {
                bstack11l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ€"): bstack1l1l11lll_opy_()
            }
            if not bstack1llll1ll1l1l_opy_ is None:
                data[bstack11l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫ₭")] = [{
                    bstack11l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ₮"): bstack11l1_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪࠧ₯"),
                    bstack11l1_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪ₰"): bstack1llll1ll1l1l_opy_
                }]
            config = {
                bstack11l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ₱"): cls.default_headers()
            }
            bstack11ll11ll11l_opy_ = bstack11l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭₲").format(os.environ[bstack11l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ₳")])
            bstack1llll1ll1l11_opy_ = cls.request_url(bstack11ll11ll11l_opy_)
            response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠧࡑࡗࡗࠫ₴"), bstack1llll1ll1l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢ₵"))
        except Exception as error:
            logger.error(bstack11l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨ₶") + str(error))
            return {
                bstack11l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₷"): bstack11l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ₸"),
                bstack11l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭₹"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lllll111lll_opy_(cls, response):
        bstack1l111llll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll1ll1111_opy_ = {}
        if bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"࠭ࡪࡸࡶࠪ₺")) is None:
            os.environ[bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ₻")] = bstack11l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭₼")
        else:
            os.environ[bstack11l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭₽")] = bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠪ࡮ࡼࡺࠧ₾"), bstack11l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ₿"))
        os.environ[bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⃀")] = bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃁"), bstack11l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⃂"))
        logger.info(bstack11l1_opy_ (u"ࠨࡖࡨࡷࡹ࡮ࡵࡣࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭⃃") + os.getenv(bstack11l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⃄")));
        if bstack11l1l1111_opy_.bstack1llll1lll1l1_opy_(cls.bs_config, cls.bstack111ll1ll_opy_.get(bstack11l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ⃅"), bstack11l1_opy_ (u"ࠫࠬ⃆"))) is True:
            bstack1lllllll111l_opy_, build_hashed_id, bstack1lllll111l1l_opy_ = cls.bstack1llll1llll1l_opy_(bstack1l111llll1_opy_)
            if bstack1lllllll111l_opy_ != None and build_hashed_id != None:
                bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃇")] = {
                    bstack11l1_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩ⃈"): bstack1lllllll111l_opy_,
                    bstack11l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⃉"): build_hashed_id,
                    bstack11l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⃊"): bstack1lllll111l1l_opy_
                }
            else:
                bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃋")] = {}
        else:
            bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⃌")] = {}
        bstack1llll1lll1ll_opy_, build_hashed_id = cls.bstack1llll1lll111_opy_(bstack1l111llll1_opy_)
        if bstack1llll1lll1ll_opy_ != None and build_hashed_id != None:
            bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃍")] = {
                bstack11l1_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩ⃎"): bstack1llll1lll1ll_opy_,
                bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃏"): build_hashed_id,
            }
        else:
            bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃐")] = {}
        if bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃑")].get(bstack11l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ⃒ࠫ")) != None or bstack1llll1ll1111_opy_[bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ⃓ࠪ")].get(bstack11l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⃔")) != None:
            cls.bstack1llll1llllll_opy_(bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠬࡰࡷࡵࠩ⃕")), bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃖")))
        return bstack1llll1ll1111_opy_
    @classmethod
    def bstack1llll1llll1l_opy_(cls, bstack1l111llll1_opy_):
        if bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃗")) == None:
            cls.bstack1llll1llll11_opy_()
            return [None, None, None]
        if bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃘")][bstack11l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵ⃙ࠪ")] != True:
            cls.bstack1llll1llll11_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃚ࠪ")])
            return [None, None, None]
        logger.debug(bstack11l1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ⃛"))
        os.environ[bstack11l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ⃜")] = bstack11l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ⃝")
        if bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠧ࡫ࡹࡷࠫ⃞")):
            os.environ[bstack11l1_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬ⃟")] = json.dumps({
                bstack11l1_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ⃠"): bstack11ll1lll11l_opy_(cls.bs_config),
                bstack11l1_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬ⃡"): bstack11lll111111_opy_(cls.bs_config)
            })
        if bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⃢")):
            os.environ[bstack11l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ⃣")] = bstack1l111llll1_opy_[bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃤")]
        if bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ⃥ࠧ")].get(bstack11l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴ⃦ࠩ"), {}).get(bstack11l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⃧")):
            os.environ[bstack11l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖ⃨ࠫ")] = str(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃩")][bstack11l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ⃪࠭")][bstack11l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵ⃫ࠪ")])
        else:
            os.environ[bstack11l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⃬")] = bstack11l1_opy_ (u"ࠣࡰࡸࡰࡱࠨ⃭")
        return [bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠩ࡭ࡻࡹ⃮࠭")], bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃯ࠬ")], os.environ[bstack11l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⃰")]]
    @classmethod
    def bstack1llll1lll111_opy_(cls, bstack1l111llll1_opy_):
        if bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃱")) == None:
            cls.bstack1lllll111l11_opy_()
            return [None, None]
        if bstack1l111llll1_opy_[bstack11l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃲")][bstack11l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⃳")] != True:
            cls.bstack1lllll111l11_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃴")])
            return [None, None]
        if bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃵")].get(bstack11l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⃶")):
            logger.debug(bstack11l1_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ⃷"))
            parsed = json.loads(os.getenv(bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⃸"), bstack11l1_opy_ (u"࠭ࡻࡾࠩ⃹")))
            capabilities = bstack1ll1l11ll1_opy_.bstack1lllll11l11l_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃺")][bstack11l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⃻")][bstack11l1_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⃼")], bstack11l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⃽"), bstack11l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ⃾"))
            bstack1llll1lll1ll_opy_ = capabilities[bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪ⃿")]
            os.environ[bstack11l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ℀")] = bstack1llll1lll1ll_opy_
            if bstack11l1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ℁") in bstack1l111llll1_opy_ and bstack1l111llll1_opy_.get(bstack11l1_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢℂ")) is None:
                parsed[bstack11l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ℃")] = capabilities[bstack11l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ℄")]
            os.environ[bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ℅")] = json.dumps(parsed)
            scripts = bstack1ll1l11ll1_opy_.bstack1lllll11l11l_opy_(bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ℆")][bstack11l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧℇ")][bstack11l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ℈")], bstack11l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭℉"), bstack11l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࠪℊ"))
            bstack1l11l1l111_opy_.bstack1llll11111_opy_(scripts)
            commands = bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪℋ")][bstack11l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬℌ")][bstack11l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵ࠭ℍ")].get(bstack11l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨℎ"))
            bstack1l11l1l111_opy_.bstack11ll1l11l11_opy_(commands)
            bstack11ll1lll111_opy_ = capabilities.get(bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬℏ"))
            bstack1l11l1l111_opy_.bstack11ll11lllll_opy_(bstack11ll1lll111_opy_)
            bstack1l11l1l111_opy_.store()
        return [bstack1llll1lll1ll_opy_, bstack1l111llll1_opy_[bstack11l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪℐ")]]
    @classmethod
    def bstack1llll1llll11_opy_(cls, response=None):
        os.environ[bstack11l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧℑ")] = bstack11l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨℒ")
        os.environ[bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨℓ")] = bstack11l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ℔")
        os.environ[bstack11l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬℕ")] = bstack11l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭№")
        os.environ[bstack11l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ℗")] = bstack11l1_opy_ (u"ࠤࡱࡹࡱࡲࠢ℘")
        os.environ[bstack11l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫℙ")] = bstack11l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤℚ")
        cls.bstack1lllll1111ll_opy_(response, bstack11l1_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧℛ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll111l11_opy_(cls, response=None):
        os.environ[bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℜ")] = bstack11l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬℝ")
        os.environ[bstack11l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭℞")] = bstack11l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ℟")
        os.environ[bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ℠")] = bstack11l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ℡")
        cls.bstack1lllll1111ll_opy_(response, bstack11l1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧ™"))
        return [None, None, None]
    @classmethod
    def bstack1llll1llllll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ℣")] = jwt
        os.environ[bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬℤ")] = build_hashed_id
    @classmethod
    def bstack1lllll1111ll_opy_(cls, response=None, product=bstack11l1_opy_ (u"ࠣࠤ℥")):
        if response == None or response.get(bstack11l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩΩ")) == None:
            logger.error(product + bstack11l1_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧ℧"))
            return
        for error in response[bstack11l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫℨ")]:
            bstack111lll111ll_opy_ = error[bstack11l1_opy_ (u"ࠬࡱࡥࡺࠩ℩")]
            error_message = error[bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧK")]
            if error_message:
                if bstack111lll111ll_opy_ == bstack11l1_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨÅ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤℬ") + product + bstack11l1_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢℭ"))
    @classmethod
    def bstack1lllll1111l1_opy_(cls):
        if cls.bstack1lllllllll11_opy_ is not None:
            return
        cls.bstack1lllllllll11_opy_ = bstack111111111l1_opy_(cls.bstack1llll1ll111l_opy_)
        cls.bstack1lllllllll11_opy_.start()
    @classmethod
    def bstack111l1llll1_opy_(cls):
        if cls.bstack1lllllllll11_opy_ is None:
            return
        cls.bstack1lllllllll11_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll111l_opy_(cls, bstack111l11l11l_opy_, event_url=bstack11l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ℮")):
        config = {
            bstack11l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬℯ"): cls.default_headers()
        }
        logger.debug(bstack11l1_opy_ (u"ࠧࡶ࡯ࡴࡶࡢࡨࡦࡺࡡ࠻ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡴࠢࡾࢁࠧℰ").format(bstack11l1_opy_ (u"࠭ࠬࠡࠩℱ").join([event[bstack11l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫℲ")] for event in bstack111l11l11l_opy_])))
        response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ℳ"), cls.request_url(event_url), bstack111l11l11l_opy_, config)
        bstack11lll11l111_opy_ = response.json()
    @classmethod
    def bstack111l1lll_opy_(cls, bstack111l11l11l_opy_, event_url=bstack11l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨℴ")):
        logger.debug(bstack11l1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡢࡦࡧࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥℵ").format(bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨℶ")]))
        if not bstack1ll1l11ll1_opy_.bstack1lllll111111_opy_(bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩℷ")]):
            logger.debug(bstack11l1_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡒࡴࡺࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦℸ").format(bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫℹ")]))
            return
        bstack1llll1111l_opy_ = bstack1ll1l11ll1_opy_.bstack1lllll11111l_opy_(bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ℺")], bstack111l11l11l_opy_.get(bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ℻")))
        if bstack1llll1111l_opy_ != None:
            if bstack111l11l11l_opy_.get(bstack11l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬℼ")) != None:
                bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ℽ")][bstack11l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪℾ")] = bstack1llll1111l_opy_
            else:
                bstack111l11l11l_opy_[bstack11l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫℿ")] = bstack1llll1111l_opy_
        if event_url == bstack11l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⅀"):
            cls.bstack1lllll1111l1_opy_()
            logger.debug(bstack11l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦ⅁").format(bstack111l11l11l_opy_[bstack11l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⅂")]))
            cls.bstack1lllllllll11_opy_.add(bstack111l11l11l_opy_)
        elif event_url == bstack11l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⅃"):
            cls.bstack1llll1ll111l_opy_([bstack111l11l11l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11l11l111_opy_(cls, logs):
        for log in logs:
            bstack1llll1ll11l1_opy_ = {
                bstack11l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⅄"): bstack11l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧⅅ"),
                bstack11l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬⅆ"): log[bstack11l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ⅇ")],
                bstack11l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫⅈ"): log[bstack11l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬⅉ")],
                bstack11l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪ⅊"): {},
                bstack11l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⅋"): log[bstack11l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⅌")],
            }
            if bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅍") in log:
                bstack1llll1ll11l1_opy_[bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅎ")] = log[bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⅏")]
            elif bstack11l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅐") in log:
                bstack1llll1ll11l1_opy_[bstack11l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅑")] = log[bstack11l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⅒")]
            cls.bstack111l1lll_opy_({
                bstack11l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⅓"): bstack11l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⅔"),
                bstack11l1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⅕"): [bstack1llll1ll11l1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll1ll1_opy_(cls, steps):
        bstack1llll1lllll1_opy_ = []
        for step in steps:
            bstack1lllll11l111_opy_ = {
                bstack11l1_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭⅖"): bstack11l1_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬ⅗"),
                bstack11l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⅘"): step[bstack11l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⅙")],
                bstack11l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⅚"): step[bstack11l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⅛")],
                bstack11l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⅜"): step[bstack11l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⅝")],
                bstack11l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⅞"): step[bstack11l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬ⅟")]
            }
            if bstack11l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅠ") in step:
                bstack1lllll11l111_opy_[bstack11l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅡ")] = step[bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⅲ")]
            elif bstack11l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ") in step:
                bstack1lllll11l111_opy_[bstack11l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅤ")] = step[bstack11l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⅥ")]
            bstack1llll1lllll1_opy_.append(bstack1lllll11l111_opy_)
        cls.bstack111l1lll_opy_({
            bstack11l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧⅦ"): bstack11l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨⅧ"),
            bstack11l1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪⅨ"): bstack1llll1lllll1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack111111l1l_opy_, stage=STAGE.bstack11lll1l1_opy_)
    def bstack11l11ll1l_opy_(cls, screenshot):
        cls.bstack111l1lll_opy_({
            bstack11l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅩ"): bstack11l1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫⅪ"),
            bstack11l1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ⅻ"): [{
                bstack11l1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧⅬ"): bstack11l1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬⅭ"),
                bstack11l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧⅮ"): datetime.datetime.utcnow().isoformat() + bstack11l1_opy_ (u"ࠬࡠࠧⅯ"),
                bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧⅰ"): screenshot[bstack11l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ⅱ")],
                bstack11l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅲ"): screenshot[bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⅳ")]
            }]
        }, event_url=bstack11l1_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨⅴ"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1ll11ll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111l1lll_opy_({
            bstack11l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⅵ"): bstack11l1_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩⅶ"),
            bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨⅷ"): {
                bstack11l1_opy_ (u"ࠢࡶࡷ࡬ࡨࠧⅸ"): cls.current_test_uuid(),
                bstack11l1_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢⅹ"): cls.bstack111ll1l111_opy_(driver)
            }
        })
    @classmethod
    def bstack111lll1ll1_opy_(cls, event: str, bstack111l11l11l_opy_: bstack111l11ll1l_opy_):
        bstack1111ll1l1l_opy_ = {
            bstack11l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ⅺ"): event,
            bstack111l11l11l_opy_.bstack1111ll1ll1_opy_(): bstack111l11l11l_opy_.bstack111l111lll_opy_(event)
        }
        cls.bstack111l1lll_opy_(bstack1111ll1l1l_opy_)
        result = getattr(bstack111l11l11l_opy_, bstack11l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪⅻ"), None)
        if event == bstack11l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬⅼ"):
            threading.current_thread().bstackTestMeta = {bstack11l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬⅽ"): bstack11l1_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧⅾ")}
        elif event == bstack11l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩⅿ"):
            threading.current_thread().bstackTestMeta = {bstack11l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨↀ"): getattr(result, bstack11l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩↁ"), bstack11l1_opy_ (u"ࠪࠫↂ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨↃ"), None) is None or os.environ[bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩↄ")] == bstack11l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦↅ")) and (os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬↆ"), None) is None or os.environ[bstack11l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ↇ")] == bstack11l1_opy_ (u"ࠤࡱࡹࡱࡲࠢↈ")):
            return False
        return True
    @staticmethod
    def bstack1lllll111ll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lllllllll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ↉"): bstack11l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ↊"),
            bstack11l1_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨ↋"): bstack11l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ↌")
        }
        if os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ↍"), None):
            headers[bstack11l1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨ↎")] = bstack11l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬ↏").format(os.environ[bstack11l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢ←")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ↑").format(bstack1llll1ll11ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ→"), None)
    @staticmethod
    def bstack111ll1l111_opy_(driver):
        return {
            bstack11l11l11ll1_opy_(): bstack111ll1lll11_opy_(driver)
        }
    @staticmethod
    def bstack1llll1ll1lll_opy_(exception_info, report):
        return [{bstack11l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ↓"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111l111l_opy_(typename):
        if bstack11l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥ↔") in typename:
            return bstack11l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ↕")
        return bstack11l1_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ↖")