# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1l1l1l1_opy_, bstack11ll1l11111_opy_, bstack1l11lllll_opy_, bstack111l1l1l11_opy_, bstack111ll1l11l1_opy_, bstack11l11ll1l11_opy_, bstack111llll1l11_opy_, bstack1ll11ll11l_opy_, bstack1l111ll111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llllllll1ll_opy_ import bstack1llllllll111_opy_
import bstack_utils.bstack1111l1l1l_opy_ as bstack11111l1l_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1lllll1l_opy_
import bstack_utils.accessibility as bstack1ll1ll1l11_opy_
from bstack_utils.bstack11l1ll111l_opy_ import bstack11l1ll111l_opy_
from bstack_utils.bstack111ll1llll_opy_ import bstack1111lll1ll_opy_
bstack1llll1ll111l_opy_ = bstack1l11l11_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨₙ")
logger = logging.getLogger(__name__)
class bstack11ll111ll1_opy_:
    bstack1llllllll1ll_opy_ = None
    bs_config = None
    bstack11llll11ll_opy_ = None
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1l1lll11_opy_, stage=STAGE.bstack1lll11l1_opy_)
    def launch(cls, bs_config, bstack11llll11ll_opy_):
        cls.bs_config = bs_config
        cls.bstack11llll11ll_opy_ = bstack11llll11ll_opy_
        try:
            cls.bstack1llll1llll11_opy_()
            bstack11ll1l1l111_opy_ = bstack11ll1l1l1l1_opy_(bs_config)
            bstack11ll1ll1111_opy_ = bstack11ll1l11111_opy_(bs_config)
            data = bstack11111l1l_opy_.bstack1llll1l1ll1l_opy_(bs_config, bstack11llll11ll_opy_)
            config = {
                bstack1l11l11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧₚ"): (bstack11ll1l1l111_opy_, bstack11ll1ll1111_opy_),
                bstack1l11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫₛ"): cls.default_headers()
            }
            response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠫࡕࡕࡓࡕࠩₜ"), cls.request_url(bstack1l11l11_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ₝")), data, config)
            if response.status_code != 200:
                bstack1ll1l11l1l_opy_ = response.json()
                if bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ₞")] == False:
                    cls.bstack1llll1lll1l1_opy_(bstack1ll1l11l1l_opy_)
                    return
                cls.bstack1lllll1111ll_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ₟")])
                cls.bstack1llll1llllll_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ₠")])
                return None
            bstack1llll1ll1l11_opy_ = cls.bstack1llll1l1lll1_opy_(response)
            return bstack1llll1ll1l11_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ₡").format(str(error)))
            return None
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def stop(cls, bstack1llll1lll11l_opy_=None):
        if not bstack1l1lllll1l_opy_.on() and not bstack1ll1ll1l11_opy_.on():
            return
        if os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ₢")) == bstack1l11l11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₣") or os.environ.get(bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ₤")) == bstack1l11l11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ₥"):
            logger.error(bstack1l11l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪ₦"))
            return {
                bstack1l11l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ₧"): bstack1l11l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ₨"),
                bstack1l11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ₩"): bstack1l11l11_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩ₪")
            }
        try:
            cls.bstack1llllllll1ll_opy_.shutdown()
            data = {
                bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₫"): bstack1ll11ll11l_opy_()
            }
            if not bstack1llll1lll11l_opy_ is None:
                data[bstack1l11l11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ€")] = [{
                    bstack1l11l11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ₭"): bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭₮"),
                    bstack1l11l11_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩ₯"): bstack1llll1lll11l_opy_
                }]
            config = {
                bstack1l11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ₰"): cls.default_headers()
            }
            bstack11ll11l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬ₱").format(os.environ[bstack1l11l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ₲")])
            bstack1lllll111111_opy_ = cls.request_url(bstack11ll11l1l1l_opy_)
            response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"࠭ࡐࡖࡖࠪ₳"), bstack1lllll111111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l11l11_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨ₴"))
        except Exception as error:
            logger.error(bstack1l11l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ₵") + str(error))
            return {
                bstack1l11l11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ₶"): bstack1l11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ₷"),
                bstack1l11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ₸"): str(error)
            }
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def bstack1llll1l1lll1_opy_(cls, response):
        bstack1ll1l11l1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll1ll1l11_opy_ = {}
        if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠬࡰࡷࡵࠩ₹")) is None:
            os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₺")] = bstack1l11l11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ₻")
        else:
            os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ₼")] = bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠩ࡭ࡻࡹ࠭₽"), bstack1l11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ₾"))
        os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ₿")] = bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃀"), bstack1l11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⃁"))
        logger.info(bstack1l11l11_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬ⃂") + os.getenv(bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⃃")));
        if bstack1l1lllll1l_opy_.bstack1llll1lll1ll_opy_(cls.bs_config, cls.bstack11llll11ll_opy_.get(bstack1l11l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⃄"), bstack1l11l11_opy_ (u"ࠪࠫ⃅"))) is True:
            bstack1lllllll11l1_opy_, build_hashed_id, bstack1llll1ll1111_opy_ = cls.bstack1lllll111l11_opy_(bstack1ll1l11l1l_opy_)
            if bstack1lllllll11l1_opy_ != None and build_hashed_id != None:
                bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃆")] = {
                    bstack1l11l11_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨ⃇"): bstack1lllllll11l1_opy_,
                    bstack1l11l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃈"): build_hashed_id,
                    bstack1l11l11_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⃉"): bstack1llll1ll1111_opy_
                }
            else:
                bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃊")] = {}
        else:
            bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃋")] = {}
        bstack1llll1ll1l1l_opy_, build_hashed_id = cls.bstack1llll1lllll1_opy_(bstack1ll1l11l1l_opy_)
        if bstack1llll1ll1l1l_opy_ != None and build_hashed_id != None:
            bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⃌")] = {
                bstack1l11l11_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨ⃍"): bstack1llll1ll1l1l_opy_,
                bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃎"): build_hashed_id,
            }
        else:
            bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃏")] = {}
        if bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃐")].get(bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⃑")) != None or bstack1llll1ll1l11_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ⃒ࠩ")].get(bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃓ࠬ")) != None:
            cls.bstack1llll1ll1lll_opy_(bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠫ࡯ࡽࡴࠨ⃔")), bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃕")))
        return bstack1llll1ll1l11_opy_
    @classmethod
    def bstack1lllll111l11_opy_(cls, bstack1ll1l11l1l_opy_):
        if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃖")) == None:
            cls.bstack1lllll1111ll_opy_()
            return [None, None, None]
        if bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃗")][bstack1l11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴ⃘ࠩ")] != True:
            cls.bstack1lllll1111ll_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ⃙ࠩ")])
            return [None, None, None]
        logger.debug(bstack1l11l11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱ⃚ࠧࠧ"))
        os.environ[bstack1l11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ⃛")] = bstack1l11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ⃜")
        if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"࠭ࡪࡸࡶࠪ⃝")):
            os.environ[bstack1l11l11_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫ⃞")] = json.dumps({
                bstack1l11l11_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ⃟"): bstack11ll1l1l1l1_opy_(cls.bs_config),
                bstack1l11l11_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫ⃠"): bstack11ll1l11111_opy_(cls.bs_config)
            })
        if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⃡")):
            os.environ[bstack1l11l11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ⃢")] = bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃣")]
        if bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃤")].get(bstack1l11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃥"), {}).get(bstack1l11l11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷ⃦ࠬ")):
            os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⃧")] = str(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃨ࠪ")][bstack1l11l11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⃩")][bstack1l11l11_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴ⃪ࠩ")])
        else:
            os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ⃫࡙࡙ࠧ")] = bstack1l11l11_opy_ (u"ࠢ࡯ࡷ࡯ࡰ⃬ࠧ")
        return [bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠨ࡬ࡺࡸ⃭ࠬ")], bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ⃮ࠫ")], os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖ⃯ࠫ")]]
    @classmethod
    def bstack1llll1lllll1_opy_(cls, bstack1ll1l11l1l_opy_):
        if bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃰")) == None:
            cls.bstack1llll1llllll_opy_()
            return [None, None]
        if bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃱")][bstack1l11l11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⃲")] != True:
            cls.bstack1llll1llllll_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃳")])
            return [None, None]
        if bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃴")].get(bstack1l11l11_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⃵")):
            logger.debug(bstack1l11l11_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ⃶"))
            parsed = json.loads(os.getenv(bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⃷"), bstack1l11l11_opy_ (u"ࠬࢁࡽࠨ⃸")))
            capabilities = bstack11111l1l_opy_.bstack1lllll111l1l_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃹")][bstack1l11l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃺")][bstack1l11l11_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ⃻")], bstack1l11l11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⃼"), bstack1l11l11_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩ⃽"))
            bstack1llll1ll1l1l_opy_ = capabilities[bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩ⃾")]
            os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⃿")] = bstack1llll1ll1l1l_opy_
            if bstack1l11l11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣ℀") in bstack1ll1l11l1l_opy_ and bstack1ll1l11l1l_opy_.get(bstack1l11l11_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ℁")) is None:
                parsed[bstack1l11l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩℂ")] = capabilities[bstack1l11l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ℃")]
            os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ℄")] = json.dumps(parsed)
            scripts = bstack11111l1l_opy_.bstack1lllll111l1l_opy_(bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ℅")][bstack1l11l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭℆")][bstack1l11l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧℇ")], bstack1l11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ℈"), bstack1l11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩ℉"))
            bstack11l1ll111l_opy_.bstack1llll1111l_opy_(scripts)
            commands = bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩℊ")][bstack1l11l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫℋ")][bstack1l11l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬℌ")].get(bstack1l11l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧℍ"))
            bstack11l1ll111l_opy_.bstack11lll11111l_opy_(commands)
            bstack11lll111l11_opy_ = capabilities.get(bstack1l11l11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫℎ"))
            bstack11l1ll111l_opy_.bstack11ll11l1lll_opy_(bstack11lll111l11_opy_)
            bstack11l1ll111l_opy_.store()
        return [bstack1llll1ll1l1l_opy_, bstack1ll1l11l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩℏ")]]
    @classmethod
    def bstack1lllll1111ll_opy_(cls, response=None):
        os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ℐ")] = bstack1l11l11_opy_ (u"ࠩࡱࡹࡱࡲࠧℑ")
        os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧℒ")] = bstack1l11l11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩℓ")
        os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ℔")] = bstack1l11l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬℕ")
        os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭№")] = bstack1l11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨ℗")
        os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ℘")] = bstack1l11l11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣℙ")
        cls.bstack1llll1lll1l1_opy_(response, bstack1l11l11_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦℚ"))
        return [None, None, None]
    @classmethod
    def bstack1llll1llllll_opy_(cls, response=None):
        os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪℛ")] = bstack1l11l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫℜ")
        os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬℝ")] = bstack1l11l11_opy_ (u"ࠨࡰࡸࡰࡱ࠭℞")
        os.environ[bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭℟")] = bstack1l11l11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ℠")
        cls.bstack1llll1lll1l1_opy_(response, bstack1l11l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦ℡"))
        return [None, None, None]
    @classmethod
    def bstack1llll1ll1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ™")] = jwt
        os.environ[bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ℣")] = build_hashed_id
    @classmethod
    def bstack1llll1lll1l1_opy_(cls, response=None, product=bstack1l11l11_opy_ (u"ࠢࠣℤ")):
        if response == None or response.get(bstack1l11l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ℥")) == None:
            logger.error(product + bstack1l11l11_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦΩ"))
            return
        for error in response[bstack1l11l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ℧")]:
            bstack11l11ll1l1l_opy_ = error[bstack1l11l11_opy_ (u"ࠫࡰ࡫ࡹࠨℨ")]
            error_message = error[bstack1l11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭℩")]
            if error_message:
                if bstack11l11ll1l1l_opy_ == bstack1l11l11_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧK"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l11l11_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣÅ") + product + bstack1l11l11_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨℬ"))
    @classmethod
    def bstack1llll1llll11_opy_(cls):
        if cls.bstack1llllllll1ll_opy_ is not None:
            return
        cls.bstack1llllllll1ll_opy_ = bstack1llllllll111_opy_(cls.bstack1lllll11111l_opy_)
        cls.bstack1llllllll1ll_opy_.start()
    @classmethod
    def bstack1111lll1l1_opy_(cls):
        if cls.bstack1llllllll1ll_opy_ is None:
            return
        cls.bstack1llllllll1ll_opy_.shutdown()
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def bstack1lllll11111l_opy_(cls, bstack1111lll111_opy_, event_url=bstack1l11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨℭ")):
        config = {
            bstack1l11l11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ℮"): cls.default_headers()
        }
        logger.debug(bstack1l11l11_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦℯ").format(bstack1l11l11_opy_ (u"ࠬ࠲ࠠࠨℰ").join([event[bstack1l11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪℱ")] for event in bstack1111lll111_opy_])))
        response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠧࡑࡑࡖࡘࠬℲ"), cls.request_url(event_url), bstack1111lll111_opy_, config)
        bstack11ll1l1lll1_opy_ = response.json()
    @classmethod
    def bstack1ll11l1ll_opy_(cls, bstack1111lll111_opy_, event_url=bstack1l11l11_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧℳ")):
        logger.debug(bstack1l11l11_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤℴ").format(bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧℵ")]))
        if not bstack11111l1l_opy_.bstack1lllll1111l1_opy_(bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨℶ")]):
            logger.debug(bstack1l11l11_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥℷ").format(bstack1111lll111_opy_[bstack1l11l11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪℸ")]))
            return
        bstack1lll11l111_opy_ = bstack11111l1l_opy_.bstack1llll1l1ll11_opy_(bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫℹ")], bstack1111lll111_opy_.get(bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ℺")))
        if bstack1lll11l111_opy_ != None:
            if bstack1111lll111_opy_.get(bstack1l11l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ℻")) != None:
                bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬℼ")][bstack1l11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩℽ")] = bstack1lll11l111_opy_
            else:
                bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪℾ")] = bstack1lll11l111_opy_
        if event_url == bstack1l11l11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬℿ"):
            cls.bstack1llll1llll11_opy_()
            logger.debug(bstack1l11l11_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥ⅀").format(bstack1111lll111_opy_[bstack1l11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⅁")]))
            cls.bstack1llllllll1ll_opy_.add(bstack1111lll111_opy_)
        elif event_url == bstack1l11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⅂"):
            cls.bstack1lllll11111l_opy_([bstack1111lll111_opy_], event_url)
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def bstack1l11lll1l1_opy_(cls, logs):
        for log in logs:
            bstack1llll1ll11ll_opy_ = {
                bstack1l11l11_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⅃"): bstack1l11l11_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭⅄"),
                bstack1l11l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫⅅ"): log[bstack1l11l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬⅆ")],
                bstack1l11l11_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪⅇ"): log[bstack1l11l11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫⅈ")],
                bstack1l11l11_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩⅉ"): {},
                bstack1l11l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅊"): log[bstack1l11l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⅋")],
            }
            if bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅌") in log:
                bstack1llll1ll11ll_opy_[bstack1l11l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅍")] = log[bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅎ")]
            elif bstack1l11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⅏") in log:
                bstack1llll1ll11ll_opy_[bstack1l11l11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅐")] = log[bstack1l11l11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅑")]
            cls.bstack1ll11l1ll_opy_({
                bstack1l11l11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⅒"): bstack1l11l11_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⅓"),
                bstack1l11l11_opy_ (u"࠭࡬ࡰࡩࡶࠫ⅔"): [bstack1llll1ll11ll_opy_]
            })
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def bstack1llll1ll1ll1_opy_(cls, steps):
        bstack1llll1llll1l_opy_ = []
        for step in steps:
            bstack1llll1l1llll_opy_ = {
                bstack1l11l11_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⅕"): bstack1l11l11_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫ⅖"),
                bstack1l11l11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⅗"): step[bstack1l11l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⅘")],
                bstack1l11l11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⅙"): step[bstack1l11l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⅚")],
                bstack1l11l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⅛"): step[bstack1l11l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⅜")],
                bstack1l11l11_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⅝"): step[bstack1l11l11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫ⅞")]
            }
            if bstack1l11l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅟") in step:
                bstack1llll1l1llll_opy_[bstack1l11l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅠ")] = step[bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅡ")]
            elif bstack1l11l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ⅲ") in step:
                bstack1llll1l1llll_opy_[bstack1l11l11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ")] = step[bstack1l11l11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅤ")]
            bstack1llll1llll1l_opy_.append(bstack1llll1l1llll_opy_)
        cls.bstack1ll11l1ll_opy_({
            bstack1l11l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ⅵ"): bstack1l11l11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧⅦ"),
            bstack1l11l11_opy_ (u"ࠫࡱࡵࡧࡴࠩⅧ"): bstack1llll1llll1l_opy_
        })
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l1l1111_opy_, stage=STAGE.bstack1lll11l1_opy_)
    def bstack11ll1lll11_opy_(cls, screenshot):
        cls.bstack1ll11l1ll_opy_({
            bstack1l11l11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅨ"): bstack1l11l11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪⅩ"),
            bstack1l11l11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬⅪ"): [{
                bstack1l11l11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ⅻ"): bstack1l11l11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫⅬ"),
                bstack1l11l11_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ⅽ"): datetime.datetime.utcnow().isoformat() + bstack1l11l11_opy_ (u"ࠫ࡟࠭Ⅾ"),
                bstack1l11l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ⅿ"): screenshot[bstack1l11l11_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬⅰ")],
                bstack1l11l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅱ"): screenshot[bstack1l11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅲ")]
            }]
        }, event_url=bstack1l11l11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧⅳ"))
    @classmethod
    @bstack111l1l1l11_opy_(class_method=True)
    def bstack11ll1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll11l1ll_opy_({
            bstack1l11l11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧⅴ"): bstack1l11l11_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨⅵ"),
            bstack1l11l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧⅶ"): {
                bstack1l11l11_opy_ (u"ࠨࡵࡶ࡫ࡧࠦⅷ"): cls.current_test_uuid(),
                bstack1l11l11_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨⅸ"): cls.bstack111ll11l1l_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1l111_opy_(cls, event: str, bstack1111lll111_opy_: bstack1111lll1ll_opy_):
        bstack111l1l1111_opy_ = {
            bstack1l11l11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬⅹ"): event,
            bstack1111lll111_opy_.bstack1111ll1l1l_opy_(): bstack1111lll111_opy_.bstack1111ll1lll_opy_(event)
        }
        cls.bstack1ll11l1ll_opy_(bstack111l1l1111_opy_)
        result = getattr(bstack1111lll111_opy_, bstack1l11l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩⅺ"), None)
        if event == bstack1l11l11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫⅻ"):
            threading.current_thread().bstackTestMeta = {bstack1l11l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫⅼ"): bstack1l11l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ⅽ")}
        elif event == bstack1l11l11_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨⅾ"):
            threading.current_thread().bstackTestMeta = {bstack1l11l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧⅿ"): getattr(result, bstack1l11l11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨↀ"), bstack1l11l11_opy_ (u"ࠩࠪↁ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧↂ"), None) is None or os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨↃ")] == bstack1l11l11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥↄ")) and (os.environ.get(bstack1l11l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫↅ"), None) is None or os.environ[bstack1l11l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬↆ")] == bstack1l11l11_opy_ (u"ࠣࡰࡸࡰࡱࠨↇ")):
            return False
        return True
    @staticmethod
    def bstack1llll1ll11l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11ll111ll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l11l11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨↈ"): bstack1l11l11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭↉"),
            bstack1l11l11_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧ↊"): bstack1l11l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ↋")
        }
        if os.environ.get(bstack1l11l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ↌"), None):
            headers[bstack1l11l11_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ↍")] = bstack1l11l11_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ↎").format(os.environ[bstack1l11l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨ↏")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l11l11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ←").format(bstack1llll1ll111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l11l11_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ↑"), None)
    @staticmethod
    def bstack111ll11l1l_opy_(driver):
        return {
            bstack111ll1l11l1_opy_(): bstack11l11ll1l11_opy_(driver)
        }
    @staticmethod
    def bstack1llll1lll111_opy_(exception_info, report):
        return [{bstack1l11l11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ→"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1l11l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ↓") in typename:
            return bstack1l11l11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ↔")
        return bstack1l11l11_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ↕")