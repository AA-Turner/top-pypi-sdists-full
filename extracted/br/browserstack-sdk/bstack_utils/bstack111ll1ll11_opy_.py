# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll11ll1l1_opy_, bstack11ll1ll11l1_opy_, bstack1l1ll1ll1l_opy_, error_handler, bstack111ll1ll1l1_opy_, bstack11l11lll1l1_opy_, bstack111ll1l1ll1_opy_, bstack1ll11l1ll1_opy_, bstack1l11111ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llllll1llll_opy_ import bstack1lllllll1111_opy_
import bstack_utils.bstack11l111llll_opy_ as bstack1ll111ll_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack11llllllll_opy_
import bstack_utils.accessibility as bstack11lll1ll1l_opy_
from bstack_utils.bstack1l11l11l_opy_ import bstack1l11l11l_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack1111lllll1_opy_
from bstack_utils.constants import bstack1l111l111l_opy_
bstack1llll11lllll_opy_ = bstack1l11ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫₜ")
logger = logging.getLogger(__name__)
class bstack1l111111l1_opy_:
    bstack1llllll1llll_opy_ = None
    bs_config = None
    bstack11l1ll1l1l_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1ll11111_opy_, stage=STAGE.bstack11lllll111_opy_)
    def launch(cls, bs_config, bstack11l1ll1l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1ll1l1l_opy_ = bstack11l1ll1l1l_opy_
        try:
            cls.bstack1llll1ll1111_opy_()
            bstack11ll1lll111_opy_ = bstack11ll11ll1l1_opy_(bs_config)
            bstack11ll1l111ll_opy_ = bstack11ll1ll11l1_opy_(bs_config)
            data = bstack1ll111ll_opy_.bstack1llll1ll11ll_opy_(bs_config, bstack11l1ll1l1l_opy_)
            config = {
                bstack1l11ll1_opy_ (u"ࠬࡧࡵࡵࡪࠪ₝"): (bstack11ll1lll111_opy_, bstack11ll1l111ll_opy_),
                bstack1l11ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ₞"): cls.default_headers()
            }
            response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ₟"), cls.request_url(bstack1l11ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨ₠")), data, config)
            if response.status_code != 200:
                bstack1lll111ll_opy_ = response.json()
                if bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ₡")] == False:
                    cls.bstack1llll1l1l1l1_opy_(bstack1lll111ll_opy_)
                    return
                cls.bstack1llll1l1ll1l_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ₢")])
                cls.bstack1llll1ll1l11_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ₣")])
                return None
            bstack1llll11llll1_opy_ = cls.bstack1llll1ll111l_opy_(response)
            return bstack1llll11llll1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l11ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥ₤").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1llll1l11lll_opy_=None):
        if not bstack11llllllll_opy_.on() and not bstack11lll1ll1l_opy_.on():
            return
        if os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₥")) == bstack1l11ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ₦") or os.environ.get(bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭₧")) == bstack1l11ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢ₨"):
            logger.error(bstack1l11ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭₩"))
            return {
                bstack1l11ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ₪"): bstack1l11ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ₫"),
                bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ€"): bstack1l11ll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬ₭")
            }
        try:
            cls.bstack1llllll1llll_opy_.shutdown()
            data = {
                bstack1l11ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭₮"): bstack1ll11l1ll1_opy_()
            }
            if not bstack1llll1l11lll_opy_ is None:
                data[bstack1l11ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭₯")] = [{
                    bstack1l11ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ₰"): bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ₱"),
                    bstack1l11ll1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ₲"): bstack1llll1l11lll_opy_
                }]
            config = {
                bstack1l11ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ₳"): cls.default_headers()
            }
            bstack11ll11l111l_opy_ = bstack1l11ll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨ₴").format(os.environ[bstack1l11ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ₵")])
            bstack1llll1l11ll1_opy_ = cls.request_url(bstack11ll11l111l_opy_)
            response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠩࡓ࡙࡙࠭₶"), bstack1llll1l11ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l11ll1_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤ₷"))
        except Exception as error:
            logger.error(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣ₸") + str(error))
            return {
                bstack1l11ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ₹"): bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ₺"),
                bstack1l11ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ₻"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll111l_opy_(cls, response):
        bstack1lll111ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll11llll1_opy_ = {}
        if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠨ࡬ࡺࡸࠬ₼")) is None:
            os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭₽")] = bstack1l11ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ₾")
        else:
            os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ₿")] = bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠬࡰࡷࡵࠩ⃀"), bstack1l11ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⃁"))
        os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⃂")] = bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⃃"), bstack1l11ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ⃄"))
        logger.info(bstack1l11ll1_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ⃅") + os.getenv(bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⃆")));
        if bstack11llllllll_opy_.bstack1llll11lll1l_opy_(cls.bs_config, cls.bstack11l1ll1l1l_opy_.get(bstack1l11ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭⃇"), bstack1l11ll1_opy_ (u"࠭ࠧ⃈"))) is True:
            bstack1llllll111ll_opy_, build_hashed_id, bstack1llll1l1l111_opy_ = cls.bstack1llll1l1llll_opy_(bstack1lll111ll_opy_)
            if bstack1llllll111ll_opy_ != None and build_hashed_id != None:
                bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃉")] = {
                    bstack1l11ll1_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫ⃊"): bstack1llllll111ll_opy_,
                    bstack1l11ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⃋"): build_hashed_id,
                    bstack1l11ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⃌"): bstack1llll1l1l111_opy_
                }
            else:
                bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃍")] = {}
        else:
            bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃎")] = {}
        bstack1llll1l1111l_opy_, build_hashed_id = cls.bstack1llll1l11111_opy_(bstack1lll111ll_opy_)
        if bstack1llll1l1111l_opy_ != None and build_hashed_id != None:
            bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃏")] = {
                bstack1l11ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ⃐"): bstack1llll1l1111l_opy_,
                bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⃑"): build_hashed_id,
            }
        else:
            bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ⃒ࠩ")] = {}
        if bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃓ࠪ")].get(bstack1l11ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⃔")) != None or bstack1llll11llll1_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃕")].get(bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃖")) != None:
            cls.bstack1llll1l1ll11_opy_(bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠧ࡫ࡹࡷࠫ⃗")), bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ⃘ࠪ")))
        return bstack1llll11llll1_opy_
    @classmethod
    def bstack1llll1l1llll_opy_(cls, bstack1lll111ll_opy_):
        if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ⃙ࠩ")) == None:
            cls.bstack1llll1l1ll1l_opy_()
            return [None, None, None]
        if bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃚ࠪ")][bstack1l11ll1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⃛")] != True:
            cls.bstack1llll1l1ll1l_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃜")])
            return [None, None, None]
        logger.debug(bstack1l11ll1_opy_ (u"࠭ࡻࡾࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲࠡࠨ⃝").format(bstack1l111l111l_opy_))
        os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭⃞")] = bstack1l11ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭⃟")
        if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠩ࡭ࡻࡹ࠭⃠")):
            os.environ[bstack1l11ll1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ⃡")] = json.dumps({
                bstack1l11ll1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭⃢"): bstack11ll11ll1l1_opy_(cls.bs_config),
                bstack1l11ll1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ⃣"): bstack11ll1ll11l1_opy_(cls.bs_config)
            })
        if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃤")):
            os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ⃥࠭")] = bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦ⃦ࠪ")]
        if bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃧")].get(bstack1l11ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶ⃨ࠫ"), {}).get(bstack1l11ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⃩")):
            os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ⃪࠭")] = str(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ⃫࠭")][bstack1l11ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃬")][bstack1l11ll1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷ⃭ࠬ")])
        else:
            os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕ⃮ࠪ")] = bstack1l11ll1_opy_ (u"ࠥࡲࡺࡲ࡬⃯ࠣ")
        return [bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠫ࡯ࡽࡴࠨ⃰")], bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃱")], os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⃲")]]
    @classmethod
    def bstack1llll1l11111_opy_(cls, bstack1lll111ll_opy_):
        if bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃳")) == None:
            cls.bstack1llll1ll1l11_opy_()
            return [None, None]
        if bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃴")][bstack1l11ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ⃵")] != True:
            cls.bstack1llll1ll1l11_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⃶")])
            return [None, None]
        if bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃷")].get(bstack1l11ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⃸")):
            logger.debug(bstack1l11ll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⃹"))
            parsed = json.loads(os.getenv(bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⃺"), bstack1l11ll1_opy_ (u"ࠨࡽࢀࠫ⃻")))
            capabilities = bstack1ll111ll_opy_.bstack1llll1l11l11_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃼")][bstack1l11ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⃽")][bstack1l11ll1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⃾")], bstack1l11ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⃿"), bstack1l11ll1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ℀"))
            bstack1llll1l1111l_opy_ = capabilities[bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ℁")]
            os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ℂ")] = bstack1llll1l1111l_opy_
            if bstack1l11ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ℃") in bstack1lll111ll_opy_ and bstack1lll111ll_opy_.get(bstack1l11ll1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤ℄")) is None:
                parsed[bstack1l11ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ℅")] = capabilities[bstack1l11ll1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭℆")]
            os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧℇ")] = json.dumps(parsed)
            scripts = bstack1ll111ll_opy_.bstack1llll1l11l11_opy_(bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ℈")][bstack1l11ll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ℉")][bstack1l11ll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪℊ")], bstack1l11ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨℋ"), bstack1l11ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬℌ"))
            bstack1l11l11l_opy_.bstack1lll1l1l11_opy_(scripts)
            commands = bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬℍ")][bstack1l11ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧℎ")][bstack1l11ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨℏ")].get(bstack1l11ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪℐ"))
            bstack1l11l11l_opy_.bstack11ll1l1llll_opy_(commands)
            bstack11ll1ll11ll_opy_ = capabilities.get(bstack1l11ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧℑ"))
            bstack1l11l11l_opy_.bstack11ll11l1l11_opy_(bstack11ll1ll11ll_opy_)
            bstack1l11l11l_opy_.store()
        return [bstack1llll1l1111l_opy_, bstack1lll111ll_opy_[bstack1l11ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬℒ")]]
    @classmethod
    def bstack1llll1l1ll1l_opy_(cls, response=None):
        os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩℓ")] = bstack1l11ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ℔")
        os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪℕ")] = bstack1l11ll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ№")
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ℗")] = bstack1l11ll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ℘")
        os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩℙ")] = bstack1l11ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤℚ")
        os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ℛ")] = bstack1l11ll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦℜ")
        cls.bstack1llll1l1l1l1_opy_(response, bstack1l11ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢℝ"))
        return [None, None, None]
    @classmethod
    def bstack1llll1ll1l11_opy_(cls, response=None):
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭℞")] = bstack1l11ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ℟")
        os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ℠")] = bstack1l11ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ℡")
        os.environ[bstack1l11ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ™")] = bstack1l11ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ℣")
        cls.bstack1llll1l1l1l1_opy_(response, bstack1l11ll1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢℤ"))
        return [None, None, None]
    @classmethod
    def bstack1llll1l1ll11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l11ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ℥")] = jwt
        os.environ[bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧΩ")] = build_hashed_id
    @classmethod
    def bstack1llll1l1l1l1_opy_(cls, response=None, product=bstack1l11ll1_opy_ (u"ࠥࠦ℧")):
        if response == None or response.get(bstack1l11ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫℨ")) == None:
            logger.error(product + bstack1l11ll1_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ℩"))
            return
        for error in response[bstack1l11ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭K")]:
            bstack11l111l11ll_opy_ = error[bstack1l11ll1_opy_ (u"ࠧ࡬ࡧࡼࠫÅ")]
            error_message = error[bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩℬ")]
            if error_message:
                if bstack11l111l11ll_opy_ == bstack1l11ll1_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣℭ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l11ll1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ℮") + product + bstack1l11ll1_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤℯ"))
    @classmethod
    def bstack1llll1ll1111_opy_(cls):
        if cls.bstack1llllll1llll_opy_ is not None:
            return
        cls.bstack1llllll1llll_opy_ = bstack1lllllll1111_opy_(cls.bstack1llll1ll11l1_opy_)
        cls.bstack1llllll1llll_opy_.start()
    @classmethod
    def bstack111l11ll11_opy_(cls):
        if cls.bstack1llllll1llll_opy_ is None:
            return
        cls.bstack1llllll1llll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll11l1_opy_(cls, bstack111l1111l1_opy_, event_url=bstack1l11ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫℰ")):
        config = {
            bstack1l11ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧℱ"): cls.default_headers()
        }
        logger.debug(bstack1l11ll1_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢℲ").format(bstack1l11ll1_opy_ (u"ࠨ࠮ࠣࠫℳ").join([event[bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ℴ")] for event in bstack111l1111l1_opy_])))
        response = bstack1l1ll1ll1l_opy_(bstack1l11ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨℵ"), cls.request_url(event_url), bstack111l1111l1_opy_, config)
        bstack11ll11lll1l_opy_ = response.json()
    @classmethod
    def bstack1l111ll1l1_opy_(cls, bstack111l1111l1_opy_, event_url=bstack1l11ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪℶ")):
        logger.debug(bstack1l11ll1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧℷ").format(bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪℸ")]))
        if not bstack1ll111ll_opy_.bstack1llll1l11l1l_opy_(bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫℹ")]):
            logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ℺").format(bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭℻")]))
            return
        bstack1ll1ll1111_opy_ = bstack1ll111ll_opy_.bstack1llll1l1lll1_opy_(bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧℼ")], bstack111l1111l1_opy_.get(bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ℽ")))
        if bstack1ll1ll1111_opy_ != None:
            if bstack111l1111l1_opy_.get(bstack1l11ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧℾ")) != None:
                bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨℿ")][bstack1l11ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⅀")] = bstack1ll1ll1111_opy_
            else:
                bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⅁")] = bstack1ll1ll1111_opy_
        if event_url == bstack1l11ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⅂"):
            cls.bstack1llll1ll1111_opy_()
            logger.debug(bstack1l11ll1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⅃").format(bstack111l1111l1_opy_[bstack1l11ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⅄")]))
            cls.bstack1llllll1llll_opy_.add(bstack111l1111l1_opy_)
        elif event_url == bstack1l11ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪⅅ"):
            cls.bstack1llll1ll11l1_opy_([bstack111l1111l1_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1l1lll1l1_opy_(cls, logs):
        for log in logs:
            bstack1llll1ll1ll1_opy_ = {
                bstack1l11ll1_opy_ (u"࠭࡫ࡪࡰࡧࠫⅆ"): bstack1l11ll1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩⅇ"),
                bstack1l11ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧⅈ"): log[bstack1l11ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨⅉ")],
                bstack1l11ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⅊"): log[bstack1l11ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⅋")],
                bstack1l11ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ⅌"): {},
                bstack1l11ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⅍"): log[bstack1l11ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨⅎ")],
            }
            if bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⅏") in log:
                bstack1llll1ll1ll1_opy_[bstack1l11ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅐")] = log[bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅑")]
            elif bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⅒") in log:
                bstack1llll1ll1ll1_opy_[bstack1l11ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅓")] = log[bstack1l11ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅔")]
            cls.bstack1l111ll1l1_opy_({
                bstack1l11ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⅕"): bstack1l11ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⅖"),
                bstack1l11ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⅗"): [bstack1llll1ll1ll1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1l111l1_opy_(cls, steps):
        bstack1llll1l1l1ll_opy_ = []
        for step in steps:
            bstack1llll1ll1l1l_opy_ = {
                bstack1l11ll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⅘"): bstack1l11ll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ⅙"),
                bstack1l11ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⅚"): step[bstack1l11ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⅛")],
                bstack1l11ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⅜"): step[bstack1l11ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⅝")],
                bstack1l11ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⅞"): step[bstack1l11ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅟")],
                bstack1l11ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭Ⅰ"): step[bstack1l11ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧⅡ")]
            }
            if bstack1l11ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⅲ") in step:
                bstack1llll1ll1l1l_opy_[bstack1l11ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ")] = step[bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅤ")]
            elif bstack1l11ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⅥ") in step:
                bstack1llll1ll1l1l_opy_[bstack1l11ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⅦ")] = step[bstack1l11ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅧ")]
            bstack1llll1l1l1ll_opy_.append(bstack1llll1ll1l1l_opy_)
        cls.bstack1l111ll1l1_opy_({
            bstack1l11ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅨ"): bstack1l11ll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪⅩ"),
            bstack1l11ll1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬⅪ"): bstack1llll1l1l1ll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1ll11l1ll_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l1l1111ll_opy_(cls, screenshot):
        cls.bstack1l111ll1l1_opy_({
            bstack1l11ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬⅫ"): bstack1l11ll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ⅼ"),
            bstack1l11ll1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨⅭ"): [{
                bstack1l11ll1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩⅮ"): bstack1l11ll1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧⅯ"),
                bstack1l11ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩⅰ"): datetime.datetime.utcnow().isoformat() + bstack1l11ll1_opy_ (u"࡛ࠧࠩⅱ"),
                bstack1l11ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩⅲ"): screenshot[bstack1l11ll1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨⅳ")],
                bstack1l11ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⅴ"): screenshot[bstack1l11ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅵ")]
            }]
        }, event_url=bstack1l11ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪⅶ"))
    @classmethod
    @error_handler(class_method=True)
    def bstack111llllll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111ll1l1_opy_({
            bstack1l11ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅷ"): bstack1l11ll1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫⅸ"),
            bstack1l11ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪⅹ"): {
                bstack1l11ll1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢⅺ"): cls.current_test_uuid(),
                bstack1l11ll1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤⅻ"): cls.bstack111ll1111l_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll11lll_opy_(cls, event: str, bstack111l1111l1_opy_: bstack1111lllll1_opy_):
        bstack1111llll1l_opy_ = {
            bstack1l11ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⅼ"): event,
            bstack111l1111l1_opy_.bstack111l1ll11l_opy_(): bstack111l1111l1_opy_.bstack1111l1ll1l_opy_(event)
        }
        cls.bstack1l111ll1l1_opy_(bstack1111llll1l_opy_)
        result = getattr(bstack111l1111l1_opy_, bstack1l11ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬⅽ"), None)
        if event == bstack1l11ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧⅾ"):
            threading.current_thread().bstackTestMeta = {bstack1l11ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⅿ"): bstack1l11ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩↀ")}
        elif event == bstack1l11ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫↁ"):
            threading.current_thread().bstackTestMeta = {bstack1l11ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪↂ"): getattr(result, bstack1l11ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫↃ"), bstack1l11ll1_opy_ (u"ࠬ࠭ↄ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪↅ"), None) is None or os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫↆ")] == bstack1l11ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨↇ")) and (os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧↈ"), None) is None or os.environ[bstack1l11ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ↉")] == bstack1l11ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ↊")):
            return False
        return True
    @staticmethod
    def bstack1llll1l1l11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l111111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l11ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ↋"): bstack1l11ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ↌"),
            bstack1l11ll1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ↍"): bstack1l11ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭↎")
        }
        if os.environ.get(bstack1l11ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭↏"), None):
            headers[bstack1l11ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ←")] = bstack1l11ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ↑").format(os.environ[bstack1l11ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ→")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l11ll1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ↓").format(bstack1llll11lllll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l11ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ↔"), None)
    @staticmethod
    def bstack111ll1111l_opy_(driver):
        return {
            bstack111ll1ll1l1_opy_(): bstack11l11lll1l1_opy_(driver)
        }
    @staticmethod
    def bstack1llll1l111ll_opy_(exception_info, report):
        return [{bstack1l11ll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ↕"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111l1l1_opy_(typename):
        if bstack1l11ll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ↖") in typename:
            return bstack1l11ll1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ↗")
        return bstack1l11ll1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ↘")