# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1ll11l1_opy_, bstack11lll11111l_opy_, bstack1ll111l111_opy_, error_handler, bstack11l1111ll1l_opy_, bstack111ll1ll111_opy_, bstack11l11l1l1ll_opy_, bstack1ll111ll1l_opy_, bstack1l11l1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lllllll1111_opy_ import bstack1lllllll11l1_opy_
import bstack_utils.bstack1l111ll11_opy_ as bstack1l11ll1l1l_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
import bstack_utils.accessibility as bstack1lll1111l1_opy_
from bstack_utils.bstack1ll1ll1ll1_opy_ import bstack1ll1ll1ll1_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack111l111l1l_opy_
from bstack_utils.constants import bstack11l1l1111l_opy_
bstack1llll1ll1l1l_opy_ = bstack1111l1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭₞")
logger = logging.getLogger(__name__)
class bstack11l1lllll1_opy_:
    bstack1lllllll1111_opy_ = None
    bs_config = None
    bstack1l1ll1l1_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1ll1lll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def launch(cls, bs_config, bstack1l1ll1l1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1ll1l1_opy_ = bstack1l1ll1l1_opy_
        try:
            cls.bstack1llll1l1l111_opy_()
            bstack11ll1lll111_opy_ = bstack11ll1ll11l1_opy_(bs_config)
            bstack11ll1ll11ll_opy_ = bstack11lll11111l_opy_(bs_config)
            data = bstack1l11ll1l1l_opy_.bstack1llll1ll1ll1_opy_(bs_config, bstack1l1ll1l1_opy_)
            config = {
                bstack1111l1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ₟"): (bstack11ll1lll111_opy_, bstack11ll1ll11ll_opy_),
                bstack1111l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ₠"): cls.default_headers()
            }
            response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ₡"), cls.request_url(bstack1111l1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪ₢")), data, config)
            if response.status_code != 200:
                bstack11ll11ll11_opy_ = response.json()
                if bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ₣")] == False:
                    cls.bstack1llll1ll1lll_opy_(bstack11ll11ll11_opy_)
                    return
                cls.bstack1llll1l1l1l1_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ₤")])
                cls.bstack1llll1ll111l_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭₥")])
                return None
            bstack1llll1l1l11l_opy_ = cls.bstack1llll1l1ll1l_opy_(response)
            return bstack1llll1l1l11l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1111l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧ₦").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1llll1l11l1l_opy_=None):
        if not bstack1ll11lll1_opy_.on() and not bstack1lll1111l1_opy_.on():
            return
        if os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ₧")) == bstack1111l1l_opy_ (u"ࠤࡱࡹࡱࡲࠢ₨") or os.environ.get(bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ₩")) == bstack1111l1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₪"):
            logger.error(bstack1111l1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨ₫"))
            return {
                bstack1111l1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭€"): bstack1111l1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭₭"),
                bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ₮"): bstack1111l1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧ₯")
            }
        try:
            cls.bstack1lllllll1111_opy_.shutdown()
            data = {
                bstack1111l1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₰"): bstack1ll111ll1l_opy_()
            }
            if not bstack1llll1l11l1l_opy_ is None:
                data[bstack1111l1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨ₱")] = [{
                    bstack1111l1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ₲"): bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫ₳"),
                    bstack1111l1l_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧ₴"): bstack1llll1l11l1l_opy_
                }]
            config = {
                bstack1111l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ₵"): cls.default_headers()
            }
            bstack11ll11l11l1_opy_ = bstack1111l1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ₶").format(os.environ[bstack1111l1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣ₷")])
            bstack1llll1ll11l1_opy_ = cls.request_url(bstack11ll11l11l1_opy_)
            response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠫࡕ࡛ࡔࠨ₸"), bstack1llll1ll11l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1111l1l_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦ₹"))
        except Exception as error:
            logger.error(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥ₺") + str(error))
            return {
                bstack1111l1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ₻"): bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ₼"),
                bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ₽"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1l1ll1l_opy_(cls, response):
        bstack11ll11ll11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll1l1l11l_opy_ = {}
        if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠪ࡮ࡼࡺࠧ₾")) is None:
            os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ₿")] = bstack1111l1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⃀")
        else:
            os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃁")] = bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠧ࡫ࡹࡷࠫ⃂"), bstack1111l1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭⃃"))
        os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⃄")] = bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⃅"), bstack1111l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⃆"))
        logger.info(bstack1111l1l_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪ⃇") + os.getenv(bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ⃈")));
        if bstack1ll11lll1_opy_.bstack1llll1l1111l_opy_(cls.bs_config, cls.bstack1l1ll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ⃉"), bstack1111l1l_opy_ (u"ࠨࠩ⃊"))) is True:
            bstack1llllll111l1_opy_, build_hashed_id, bstack1llll1l1llll_opy_ = cls.bstack1llll11llll1_opy_(bstack11ll11ll11_opy_)
            if bstack1llllll111l1_opy_ != None and build_hashed_id != None:
                bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃋")] = {
                    bstack1111l1l_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭⃌"): bstack1llllll111l1_opy_,
                    bstack1111l1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⃍"): build_hashed_id,
                    bstack1111l1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⃎"): bstack1llll1l1llll_opy_
                }
            else:
                bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃏")] = {}
        else:
            bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃐")] = {}
        bstack1llll1l111ll_opy_, build_hashed_id = cls.bstack1llll1l11l11_opy_(bstack11ll11ll11_opy_)
        if bstack1llll1l111ll_opy_ != None and build_hashed_id != None:
            bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃑")] = {
                bstack1111l1l_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ⃒࠭"): bstack1llll1l111ll_opy_,
                bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃓ࠬ"): build_hashed_id,
            }
        else:
            bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃔")] = {}
        if bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃕")].get(bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃖")) != None or bstack1llll1l1l11l_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃗")].get(bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ⃘ࠪ")) != None:
            cls.bstack1llll1l1lll1_opy_(bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠩ࡭ࡻࡹ⃙࠭")), bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃚ࠬ")))
        return bstack1llll1l1l11l_opy_
    @classmethod
    def bstack1llll11llll1_opy_(cls, bstack11ll11ll11_opy_):
        if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃛")) == None:
            cls.bstack1llll1l1l1l1_opy_()
            return [None, None, None]
        if bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃜")][bstack1111l1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⃝")] != True:
            cls.bstack1llll1l1l1l1_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃞")])
            return [None, None, None]
        logger.debug(bstack1111l1l_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⃟").format(bstack11l1l1111l_opy_))
        os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ⃠")] = bstack1111l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ⃡")
        if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠫ࡯ࡽࡴࠨ⃢")):
            os.environ[bstack1111l1l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩ⃣")] = json.dumps({
                bstack1111l1l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨ⃤"): bstack11ll1ll11l1_opy_(cls.bs_config),
                bstack1111l1l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥ⃥ࠩ"): bstack11lll11111l_opy_(cls.bs_config)
            })
        if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ⃦ࠪ")):
            os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ⃧")] = bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃨ࠬ")]
        if bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃩")].get(bstack1111l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ⃪࠭"), {}).get(bstack1111l1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵ⃫ࠪ")):
            os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⃬")] = str(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃭")][bstack1111l1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵ⃮ࠪ")][bstack1111l1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹ⃯ࠧ")])
        else:
            os.environ[bstack1111l1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬ⃰")] = bstack1111l1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ⃱")
        return [bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"࠭ࡪࡸࡶࠪ⃲")], bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⃳")], os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⃴")]]
    @classmethod
    def bstack1llll1l11l11_opy_(cls, bstack11ll11ll11_opy_):
        if bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃵")) == None:
            cls.bstack1llll1ll111l_opy_()
            return [None, None]
        if bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⃶")][bstack1111l1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⃷")] != True:
            cls.bstack1llll1ll111l_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃸")])
            return [None, None]
        if bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃹")].get(bstack1111l1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃺")):
            logger.debug(bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬ⃻"))
            parsed = json.loads(os.getenv(bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⃼"), bstack1111l1l_opy_ (u"ࠪࡿࢂ࠭⃽")))
            capabilities = bstack1l11ll1l1l_opy_.bstack1llll1ll11ll_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃾")][bstack1111l1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⃿")][bstack1111l1l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ℀")], bstack1111l1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ℁"), bstack1111l1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧℂ"))
            bstack1llll1l111ll_opy_ = capabilities[bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ℃")]
            os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ℄")] = bstack1llll1l111ll_opy_
            if bstack1111l1l_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ℅") in bstack11ll11ll11_opy_ and bstack11ll11ll11_opy_.get(bstack1111l1l_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ℆")) is None:
                parsed[bstack1111l1l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧℇ")] = capabilities[bstack1111l1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ℈")]
            os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ℉")] = json.dumps(parsed)
            scripts = bstack1l11ll1l1l_opy_.bstack1llll1ll11ll_opy_(bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩℊ")][bstack1111l1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫℋ")][bstack1111l1l_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬℌ")], bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪℍ"), bstack1111l1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧℎ"))
            bstack1ll1ll1ll1_opy_.bstack1l11l1ll_opy_(scripts)
            commands = bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧℏ")][bstack1111l1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩℐ")][bstack1111l1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪℑ")].get(bstack1111l1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬℒ"))
            bstack1ll1ll1ll1_opy_.bstack11ll1l1l11l_opy_(commands)
            bstack11ll1ll1l1l_opy_ = capabilities.get(bstack1111l1l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩℓ"))
            bstack1ll1ll1ll1_opy_.bstack11ll11ll111_opy_(bstack11ll1ll1l1l_opy_)
            bstack1ll1ll1ll1_opy_.store()
        return [bstack1llll1l111ll_opy_, bstack11ll11ll11_opy_[bstack1111l1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ℔")]]
    @classmethod
    def bstack1llll1l1l1l1_opy_(cls, response=None):
        os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℕ")] = bstack1111l1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ№")
        os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ℗")] = bstack1111l1l_opy_ (u"ࠩࡱࡹࡱࡲࠧ℘")
        os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩℙ")] = bstack1111l1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪℚ")
        os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫℛ")] = bstack1111l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦℜ")
        os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨℝ")] = bstack1111l1l_opy_ (u"ࠣࡰࡸࡰࡱࠨ℞")
        cls.bstack1llll1ll1lll_opy_(response, bstack1111l1l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ℟"))
        return [None, None, None]
    @classmethod
    def bstack1llll1ll111l_opy_(cls, response=None):
        os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ℠")] = bstack1111l1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ℡")
        os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ™")] = bstack1111l1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ℣")
        os.environ[bstack1111l1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫℤ")] = bstack1111l1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭℥")
        cls.bstack1llll1ll1lll_opy_(response, bstack1111l1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤΩ"))
        return [None, None, None]
    @classmethod
    def bstack1llll1l1lll1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ℧")] = jwt
        os.environ[bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩℨ")] = build_hashed_id
    @classmethod
    def bstack1llll1ll1lll_opy_(cls, response=None, product=bstack1111l1l_opy_ (u"ࠧࠨ℩")):
        if response == None or response.get(bstack1111l1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭K")) == None:
            logger.error(product + bstack1111l1l_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤÅ"))
            return
        for error in response[bstack1111l1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨℬ")]:
            bstack11l111l1111_opy_ = error[bstack1111l1l_opy_ (u"ࠩ࡮ࡩࡾ࠭ℭ")]
            error_message = error[bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ℮")]
            if error_message:
                if bstack11l111l1111_opy_ == bstack1111l1l_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥℯ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1111l1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨℰ") + product + bstack1111l1l_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦℱ"))
    @classmethod
    def bstack1llll1l1l111_opy_(cls):
        if cls.bstack1lllllll1111_opy_ is not None:
            return
        cls.bstack1lllllll1111_opy_ = bstack1lllllll11l1_opy_(cls.bstack1llll11lllll_opy_)
        cls.bstack1lllllll1111_opy_.start()
    @classmethod
    def bstack111l1l11ll_opy_(cls):
        if cls.bstack1lllllll1111_opy_ is None:
            return
        cls.bstack1lllllll1111_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll11lllll_opy_(cls, bstack111l1l111l_opy_, event_url=bstack1111l1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭Ⅎ")):
        config = {
            bstack1111l1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩℳ"): cls.default_headers()
        }
        logger.debug(bstack1111l1l_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤℴ").format(bstack1111l1l_opy_ (u"ࠪ࠰ࠥ࠭ℵ").join([event[bstack1111l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨℶ")] for event in bstack111l1l111l_opy_])))
        response = bstack1ll111l111_opy_(bstack1111l1l_opy_ (u"ࠬࡖࡏࡔࡖࠪℷ"), cls.request_url(event_url), bstack111l1l111l_opy_, config)
        bstack11lll1111ll_opy_ = response.json()
    @classmethod
    def bstack111lll1l_opy_(cls, bstack111l1l111l_opy_, event_url=bstack1111l1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬℸ")):
        logger.debug(bstack1111l1l_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢℹ").format(bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ℺")]))
        if not bstack1l11ll1l1l_opy_.bstack1llll1l111l1_opy_(bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭℻")]):
            logger.debug(bstack1111l1l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣℼ").format(bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨℽ")]))
            return
        bstack1l1lllll_opy_ = bstack1l11ll1l1l_opy_.bstack1llll1ll1l11_opy_(bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩℾ")], bstack111l1l111l_opy_.get(bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨℿ")))
        if bstack1l1lllll_opy_ != None:
            if bstack111l1l111l_opy_.get(bstack1111l1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⅀")) != None:
                bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⅁")][bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⅂")] = bstack1l1lllll_opy_
            else:
                bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⅃")] = bstack1l1lllll_opy_
        if event_url == bstack1111l1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⅄"):
            cls.bstack1llll1l1l111_opy_()
            logger.debug(bstack1111l1l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣⅅ").format(bstack111l1l111l_opy_[bstack1111l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅆ")]))
            cls.bstack1lllllll1111_opy_.add(bstack111l1l111l_opy_)
        elif event_url == bstack1111l1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬⅇ"):
            cls.bstack1llll11lllll_opy_([bstack111l1l111l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11l11l1l1l_opy_(cls, logs):
        for log in logs:
            bstack1llll1l1ll11_opy_ = {
                bstack1111l1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ⅈ"): bstack1111l1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫⅉ"),
                bstack1111l1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⅊"): log[bstack1111l1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⅋")],
                bstack1111l1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⅌"): log[bstack1111l1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⅍")],
                bstack1111l1l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧⅎ"): {},
                bstack1111l1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⅏"): log[bstack1111l1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⅐")],
            }
            if bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅑") in log:
                bstack1llll1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⅒")] = log[bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅓")]
            elif bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅔") in log:
                bstack1llll1l1ll11_opy_[bstack1111l1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⅕")] = log[bstack1111l1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⅖")]
            cls.bstack111lll1l_opy_({
                bstack1111l1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⅗"): bstack1111l1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⅘"),
                bstack1111l1l_opy_ (u"ࠫࡱࡵࡧࡴࠩ⅙"): [bstack1llll1l1ll11_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1l11lll_opy_(cls, steps):
        bstack1llll1l11ll1_opy_ = []
        for step in steps:
            bstack1llll1ll1111_opy_ = {
                bstack1111l1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⅚"): bstack1111l1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ⅛"),
                bstack1111l1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⅜"): step[bstack1111l1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⅝")],
                bstack1111l1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⅞"): step[bstack1111l1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⅟")],
                bstack1111l1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬⅠ"): step[bstack1111l1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⅱ")],
                bstack1111l1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨⅢ"): step[bstack1111l1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩⅣ")]
            }
            if bstack1111l1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅤ") in step:
                bstack1llll1ll1111_opy_[bstack1111l1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⅥ")] = step[bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⅦ")]
            elif bstack1111l1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅧ") in step:
                bstack1llll1ll1111_opy_[bstack1111l1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅨ")] = step[bstack1111l1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⅹ")]
            bstack1llll1l11ll1_opy_.append(bstack1llll1ll1111_opy_)
        cls.bstack111lll1l_opy_({
            bstack1111l1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫⅪ"): bstack1111l1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬⅫ"),
            bstack1111l1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧⅬ"): bstack1llll1l11ll1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1llll1l11_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1111l1ll_opy_(cls, screenshot):
        cls.bstack111lll1l_opy_({
            bstack1111l1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧⅭ"): bstack1111l1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨⅮ"),
            bstack1111l1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪⅯ"): [{
                bstack1111l1l_opy_ (u"࠭࡫ࡪࡰࡧࠫⅰ"): bstack1111l1l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩⅱ"),
                bstack1111l1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫⅲ"): datetime.datetime.utcnow().isoformat() + bstack1111l1l_opy_ (u"ࠩ࡝ࠫⅳ"),
                bstack1111l1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫⅴ"): screenshot[bstack1111l1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪⅵ")],
                bstack1111l1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅶ"): screenshot[bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ⅷ")]
            }]
        }, event_url=bstack1111l1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬⅸ"))
    @classmethod
    @error_handler(class_method=True)
    def bstack111lll1ll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111lll1l_opy_({
            bstack1111l1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬⅹ"): bstack1111l1l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ⅺ"),
            bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬⅻ"): {
                bstack1111l1l_opy_ (u"ࠦࡺࡻࡩࡥࠤⅼ"): cls.current_test_uuid(),
                bstack1111l1l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦⅽ"): cls.bstack111ll11ll1_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll11111_opy_(cls, event: str, bstack111l1l111l_opy_: bstack111l111l1l_opy_):
        bstack111l1ll111_opy_ = {
            bstack1111l1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅾ"): event,
            bstack111l1l111l_opy_.bstack1111ll1111_opy_(): bstack111l1l111l_opy_.bstack1111lll1l1_opy_(event)
        }
        cls.bstack111lll1l_opy_(bstack111l1ll111_opy_)
        result = getattr(bstack111l1l111l_opy_, bstack1111l1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧⅿ"), None)
        if event == bstack1111l1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩↀ"):
            threading.current_thread().bstackTestMeta = {bstack1111l1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩↁ"): bstack1111l1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫↂ")}
        elif event == bstack1111l1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ↄ"):
            threading.current_thread().bstackTestMeta = {bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬↄ"): getattr(result, bstack1111l1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ↅ"), bstack1111l1l_opy_ (u"ࠧࠨↆ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬↇ"), None) is None or os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ↈ")] == bstack1111l1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ↉")) and (os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ↊"), None) is None or os.environ[bstack1111l1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ↋")] == bstack1111l1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ↌")):
            return False
        return True
    @staticmethod
    def bstack1llll1l1l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11l1lllll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1111l1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭↍"): bstack1111l1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ↎"),
            bstack1111l1l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬ↏"): bstack1111l1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ←")
        }
        if os.environ.get(bstack1111l1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ↑"), None):
            headers[bstack1111l1l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ→")] = bstack1111l1l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ↓").format(os.environ[bstack1111l1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ↔")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1111l1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ↕").format(bstack1llll1ll1l1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1111l1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭↖"), None)
    @staticmethod
    def bstack111ll11ll1_opy_(driver):
        return {
            bstack11l1111ll1l_opy_(): bstack111ll1ll111_opy_(driver)
        }
    @staticmethod
    def bstack1llll1l11111_opy_(exception_info, report):
        return [{bstack1111l1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭↗"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111l1ll_opy_(typename):
        if bstack1111l1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ↘") in typename:
            return bstack1111l1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ↙")
        return bstack1111l1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ↚")