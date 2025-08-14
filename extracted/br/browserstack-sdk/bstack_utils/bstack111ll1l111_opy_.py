# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1l111ll_opy_, bstack11lll111lll_opy_, bstack1llll11ll1_opy_, error_handler, bstack111lll11l1l_opy_, bstack11l111l11ll_opy_, bstack111ll1lll1l_opy_, bstack11lllll1_opy_, bstack1l111l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llllllllll1_opy_ import bstack1111111111l_opy_
import bstack_utils.bstack1ll1l1ll1_opy_ as bstack111lllll1l_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll1l11l_opy_
import bstack_utils.accessibility as bstack1lll11l1ll_opy_
from bstack_utils.bstack1lll11l1l1_opy_ import bstack1lll11l1l1_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack111l1111ll_opy_
from bstack_utils.constants import bstack1l11l11111_opy_
bstack1llll1llll1l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨ₧")
logger = logging.getLogger(__name__)
class bstack1llllll11l_opy_:
    bstack1llllllllll1_opy_ = None
    bs_config = None
    bstack11ll11111_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1lll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def launch(cls, bs_config, bstack11ll11111_opy_):
        cls.bs_config = bs_config
        cls.bstack11ll11111_opy_ = bstack11ll11111_opy_
        try:
            cls.bstack1llll1lll11l_opy_()
            bstack11ll1l1l1ll_opy_ = bstack11ll1l111ll_opy_(bs_config)
            bstack11ll1l111l1_opy_ = bstack11lll111lll_opy_(bs_config)
            data = bstack111lllll1l_opy_.bstack1lllll111111_opy_(bs_config, bstack11ll11111_opy_)
            config = {
                bstack1l1l1ll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ₨"): (bstack11ll1l1l1ll_opy_, bstack11ll1l111l1_opy_),
                bstack1l1l1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ₩"): cls.default_headers()
            }
            response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡕࡕࡓࡕࠩ₪"), cls.request_url(bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬ₫")), data, config)
            if response.status_code != 200:
                bstack1111l1lll_opy_ = response.json()
                if bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ€")] == False:
                    cls.bstack1llll1lll1l1_opy_(bstack1111l1lll_opy_)
                    return
                cls.bstack1llll1lll1ll_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ₭")])
                cls.bstack1lllll1111l1_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ₮")])
                return None
            bstack1llll1ll11l1_opy_ = cls.bstack1llll1ll1111_opy_(response)
            return bstack1llll1ll11l1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢ₯").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1llll1ll111l_opy_=None):
        if not bstack1l1ll1l11l_opy_.on() and not bstack1lll11l1ll_opy_.on():
            return
        if os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ₰")) == bstack1l1l1ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₱") or os.environ.get(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ₲")) == bstack1l1l1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ₳"):
            logger.error(bstack1l1l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪ₴"))
            return {
                bstack1l1l1ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ₵"): bstack1l1l1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ₶"),
                bstack1l1l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ₷"): bstack1l1l1ll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩ₸")
            }
        try:
            cls.bstack1llllllllll1_opy_.shutdown()
            data = {
                bstack1l1l1ll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ₹"): bstack11lllll1_opy_()
            }
            if not bstack1llll1ll111l_opy_ is None:
                data[bstack1l1l1ll_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ₺")] = [{
                    bstack1l1l1ll_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ₻"): bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭₼"),
                    bstack1l1l1ll_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩ₽"): bstack1llll1ll111l_opy_
                }]
            config = {
                bstack1l1l1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ₾"): cls.default_headers()
            }
            bstack11ll11ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬ₿").format(os.environ[bstack1l1l1ll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥ⃀")])
            bstack1lllll111l1l_opy_ = cls.request_url(bstack11ll11ll111_opy_)
            response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"࠭ࡐࡖࡖࠪ⃁"), bstack1lllll111l1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1l1ll_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨ⃂"))
        except Exception as error:
            logger.error(bstack1l1l1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧ⃃") + str(error))
            return {
                bstack1l1l1ll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⃄"): bstack1l1l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⃅"),
                bstack1l1l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃆"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll1111_opy_(cls, response):
        bstack1111l1lll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll1ll11l1_opy_ = {}
        if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠬࡰࡷࡵࠩ⃇")) is None:
            os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃈")] = bstack1l1l1ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⃉")
        else:
            os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⃊")] = bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠩ࡭ࡻࡹ࠭⃋"), bstack1l1l1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⃌"))
        os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⃍")] = bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃎"), bstack1l1l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⃏"))
        logger.info(bstack1l1l1ll_opy_ (u"ࠧࡕࡧࡶࡸ࡭ࡻࡢࠡࡵࡷࡥࡷࡺࡥࡥࠢࡺ࡭ࡹ࡮ࠠࡪࡦ࠽ࠤࠬ⃐") + os.getenv(bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⃑")));
        if bstack1l1ll1l11l_opy_.bstack1llll1ll1l1l_opy_(cls.bs_config, cls.bstack11ll11111_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦ⃒ࠪ"), bstack1l1l1ll_opy_ (u"⃓ࠪࠫ"))) is True:
            bstack1lllllll1l1l_opy_, build_hashed_id, bstack1lllll111l11_opy_ = cls.bstack1llll1l1llll_opy_(bstack1111l1lll_opy_)
            if bstack1lllllll1l1l_opy_ != None and build_hashed_id != None:
                bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃔")] = {
                    bstack1l1l1ll_opy_ (u"ࠬࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠨ⃕"): bstack1lllllll1l1l_opy_,
                    bstack1l1l1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃖"): build_hashed_id,
                    bstack1l1l1ll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⃗"): bstack1lllll111l11_opy_
                }
            else:
                bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃘")] = {}
        else:
            bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ⃙ࠩ")] = {}
        bstack1llll1ll1l11_opy_, build_hashed_id = cls.bstack1lllll11111l_opy_(bstack1111l1lll_opy_)
        if bstack1llll1ll1l11_opy_ != None and build_hashed_id != None:
            bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ⃚ࠪ")] = {
                bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡩࡡࡷࡳࡰ࡫࡮ࠨ⃛"): bstack1llll1ll1l11_opy_,
                bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃜"): build_hashed_id,
            }
        else:
            bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃝")] = {}
        if bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃞")].get(bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⃟")) != None or bstack1llll1ll11l1_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃠")].get(bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⃡")) != None:
            cls.bstack1llll1llllll_opy_(bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠫ࡯ࡽࡴࠨ⃢")), bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃣")))
        return bstack1llll1ll11l1_opy_
    @classmethod
    def bstack1llll1l1llll_opy_(cls, bstack1111l1lll_opy_):
        if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃤")) == None:
            cls.bstack1llll1lll1ll_opy_()
            return [None, None, None]
        if bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ⃥ࠧ")][bstack1l1l1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴ⃦ࠩ")] != True:
            cls.bstack1llll1lll1ll_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⃧")])
            return [None, None, None]
        logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡿࢂࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯⃨ࠥࠬ").format(bstack1l11l11111_opy_))
        os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ⃩")] = bstack1l1l1ll_opy_ (u"ࠬࡺࡲࡶࡧ⃪ࠪ")
        if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"࠭ࡪࡸࡶ⃫ࠪ")):
            os.environ[bstack1l1l1ll_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊ⃬ࠫ")] = json.dumps({
                bstack1l1l1ll_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧ⃭ࠪ"): bstack11ll1l111ll_opy_(cls.bs_config),
                bstack1l1l1ll_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧ⃮ࠫ"): bstack11lll111lll_opy_(cls.bs_config)
            })
        if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨ⃯ࠬ")):
            os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪ⃰")] = bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃱")]
        if bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃲")].get(bstack1l1l1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⃳"), {}).get(bstack1l1l1ll_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⃴")):
            os.environ[bstack1l1l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⃵")] = str(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⃶")][bstack1l1l1ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⃷")][bstack1l1l1ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ⃸")])
        else:
            os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⃹")] = bstack1l1l1ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⃺")
        return [bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠨ࡬ࡺࡸࠬ⃻")], bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⃼")], os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫ⃽")]]
    @classmethod
    def bstack1lllll11111l_opy_(cls, bstack1111l1lll_opy_):
        if bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃾")) == None:
            cls.bstack1lllll1111l1_opy_()
            return [None, None]
        if bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃿")][bstack1l1l1ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ℀")] != True:
            cls.bstack1lllll1111l1_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ℁")])
            return [None, None]
        if bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨℂ")].get(bstack1l1l1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ℃")):
            logger.debug(bstack1l1l1ll_opy_ (u"ࠪࡘࡪࡹࡴࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࠧࠧ℄"))
            parsed = json.loads(os.getenv(bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ℅"), bstack1l1l1ll_opy_ (u"ࠬࢁࡽࠨ℆")))
            capabilities = bstack111lllll1l_opy_.bstack1llll1lll111_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ℇ")][bstack1l1l1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ℈")][bstack1l1l1ll_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ℉")], bstack1l1l1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧℊ"), bstack1l1l1ll_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩℋ"))
            bstack1llll1ll1l11_opy_ = capabilities[bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩℌ")]
            os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪℍ")] = bstack1llll1ll1l11_opy_
            if bstack1l1l1ll_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡥࠣℎ") in bstack1111l1lll_opy_ and bstack1111l1lll_opy_.get(bstack1l1l1ll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨℏ")) is None:
                parsed[bstack1l1l1ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩℐ")] = capabilities[bstack1l1l1ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪℑ")]
            os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫℒ")] = json.dumps(parsed)
            scripts = bstack111lllll1l_opy_.bstack1llll1lll111_opy_(bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫℓ")][bstack1l1l1ll_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭℔")][bstack1l1l1ll_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧℕ")], bstack1l1l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ№"), bstack1l1l1ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࠩ℗"))
            bstack1lll11l1l1_opy_.bstack1l111l1111_opy_(scripts)
            commands = bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ℘")][bstack1l1l1ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫℙ")][bstack1l1l1ll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࡚࡯ࡘࡴࡤࡴࠬℚ")].get(bstack1l1l1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧℛ"))
            bstack1lll11l1l1_opy_.bstack11ll1l11l1l_opy_(commands)
            bstack11ll1l11111_opy_ = capabilities.get(bstack1l1l1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫℜ"))
            bstack1lll11l1l1_opy_.bstack11ll11ll1ll_opy_(bstack11ll1l11111_opy_)
            bstack1lll11l1l1_opy_.store()
        return [bstack1llll1ll1l11_opy_, bstack1111l1lll_opy_[bstack1l1l1ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩℝ")]]
    @classmethod
    def bstack1llll1lll1ll_opy_(cls, response=None):
        os.environ[bstack1l1l1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭℞")] = bstack1l1l1ll_opy_ (u"ࠩࡱࡹࡱࡲࠧ℟")
        os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ℠")] = bstack1l1l1ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ℡")
        os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ™")] = bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ℣")
        os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ℤ")] = bstack1l1l1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ℥")
        os.environ[bstack1l1l1ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪΩ")] = bstack1l1l1ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ℧")
        cls.bstack1llll1lll1l1_opy_(response, bstack1l1l1ll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦℨ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1111l1_opy_(cls, response=None):
        os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ℩")] = bstack1l1l1ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫK")
        os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬÅ")] = bstack1l1l1ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ℬ")
        os.environ[bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ℭ")] = bstack1l1l1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ℮")
        cls.bstack1llll1lll1l1_opy_(response, bstack1l1l1ll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦℯ"))
        return [None, None, None]
    @classmethod
    def bstack1llll1llllll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩℰ")] = jwt
        os.environ[bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫℱ")] = build_hashed_id
    @classmethod
    def bstack1llll1lll1l1_opy_(cls, response=None, product=bstack1l1l1ll_opy_ (u"ࠢࠣℲ")):
        if response == None or response.get(bstack1l1l1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨℳ")) == None:
            logger.error(product + bstack1l1l1ll_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦℴ"))
            return
        for error in response[bstack1l1l1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪℵ")]:
            bstack111ll1ll1ll_opy_ = error[bstack1l1l1ll_opy_ (u"ࠫࡰ࡫ࡹࠨℶ")]
            error_message = error[bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ℷ")]
            if error_message:
                if bstack111ll1ll1ll_opy_ == bstack1l1l1ll_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧℸ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1l1ll_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣℹ") + product + bstack1l1l1ll_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ℺"))
    @classmethod
    def bstack1llll1lll11l_opy_(cls):
        if cls.bstack1llllllllll1_opy_ is not None:
            return
        cls.bstack1llllllllll1_opy_ = bstack1111111111l_opy_(cls.bstack1llll1lllll1_opy_)
        cls.bstack1llllllllll1_opy_.start()
    @classmethod
    def bstack111l1111l1_opy_(cls):
        if cls.bstack1llllllllll1_opy_ is None:
            return
        cls.bstack1llllllllll1_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1lllll1_opy_(cls, bstack111l111l11_opy_, event_url=bstack1l1l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ℻")):
        config = {
            bstack1l1l1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫℼ"): cls.default_headers()
        }
        logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦℽ").format(bstack1l1l1ll_opy_ (u"ࠬ࠲ࠠࠨℾ").join([event[bstack1l1l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪℿ")] for event in bstack111l111l11_opy_])))
        response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠧࡑࡑࡖࡘࠬ⅀"), cls.request_url(event_url), bstack111l111l11_opy_, config)
        bstack11lll1111ll_opy_ = response.json()
    @classmethod
    def bstack11ll11l1ll_opy_(cls, bstack111l111l11_opy_, event_url=bstack1l1l1ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⅁")):
        logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⅂").format(bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⅃")]))
        if not bstack111lllll1l_opy_.bstack1llll1ll1ll1_opy_(bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⅄")]):
            logger.debug(bstack1l1l1ll_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥⅅ").format(bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅆ")]))
            return
        bstack1lll1l1lll_opy_ = bstack111lllll1l_opy_.bstack1llll1ll11ll_opy_(bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫⅇ")], bstack111l111l11_opy_.get(bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪⅈ")))
        if bstack1lll1l1lll_opy_ != None:
            if bstack111l111l11_opy_.get(bstack1l1l1ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫⅉ")) != None:
                bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⅊")][bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⅋")] = bstack1lll1l1lll_opy_
            else:
                bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⅌")] = bstack1lll1l1lll_opy_
        if event_url == bstack1l1l1ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ⅍"):
            cls.bstack1llll1lll11l_opy_()
            logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥⅎ").format(bstack111l111l11_opy_[bstack1l1l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⅏")]))
            cls.bstack1llllllllll1_opy_.add(bstack111l111l11_opy_)
        elif event_url == bstack1l1l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⅐"):
            cls.bstack1llll1lllll1_opy_([bstack111l111l11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1ll11l_opy_(cls, logs):
        for log in logs:
            bstack1lllll111lll_opy_ = {
                bstack1l1l1ll_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⅑"): bstack1l1l1ll_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭⅒"),
                bstack1l1l1ll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⅓"): log[bstack1l1l1ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⅔")],
                bstack1l1l1ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⅕"): log[bstack1l1l1ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⅖")],
                bstack1l1l1ll_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩ⅗"): {},
                bstack1l1l1ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅘"): log[bstack1l1l1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⅙")],
            }
            if bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅚") in log:
                bstack1lllll111lll_opy_[bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅛")] = log[bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⅜")]
            elif bstack1l1l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⅝") in log:
                bstack1lllll111lll_opy_[bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅞")] = log[bstack1l1l1ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅟")]
            cls.bstack11ll11l1ll_opy_({
                bstack1l1l1ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨⅠ"): bstack1l1l1ll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩⅡ"),
                bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡩࡶࠫⅢ"): [bstack1lllll111lll_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lllll1111ll_opy_(cls, steps):
        bstack1lllll111ll1_opy_ = []
        for step in steps:
            bstack1llll1llll11_opy_ = {
                bstack1l1l1ll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬⅣ"): bstack1l1l1ll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫⅤ"),
                bstack1l1l1ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨⅥ"): step[bstack1l1l1ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩⅦ")],
                bstack1l1l1ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧⅧ"): step[bstack1l1l1ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨⅨ")],
                bstack1l1l1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧⅩ"): step[bstack1l1l1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨⅪ")],
                bstack1l1l1ll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪⅫ"): step[bstack1l1l1ll_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫⅬ")]
            }
            if bstack1l1l1ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⅭ") in step:
                bstack1llll1llll11_opy_[bstack1l1l1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅮ")] = step[bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅯ")]
            elif bstack1l1l1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ⅰ") in step:
                bstack1llll1llll11_opy_[bstack1l1l1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅱ")] = step[bstack1l1l1ll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅲ")]
            bstack1lllll111ll1_opy_.append(bstack1llll1llll11_opy_)
        cls.bstack11ll11l1ll_opy_({
            bstack1l1l1ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ⅳ"): bstack1l1l1ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧⅴ"),
            bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡧࡴࠩⅵ"): bstack1lllll111ll1_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l11l1111l_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
    def bstack1111l111l_opy_(cls, screenshot):
        cls.bstack11ll11l1ll_opy_({
            bstack1l1l1ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅶ"): bstack1l1l1ll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪⅷ"),
            bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡪࡷࠬⅸ"): [{
                bstack1l1l1ll_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ⅹ"): bstack1l1l1ll_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫⅺ"),
                bstack1l1l1ll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ⅻ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1ll_opy_ (u"ࠫ࡟࠭ⅼ"),
                bstack1l1l1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ⅽ"): screenshot[bstack1l1l1ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬⅾ")],
                bstack1l1l1ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅿ"): screenshot[bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨↀ")]
            }]
        }, event_url=bstack1l1l1ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧↁ"))
    @classmethod
    @error_handler(class_method=True)
    def bstack11l1l1111l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll11l1ll_opy_({
            bstack1l1l1ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧↂ"): bstack1l1l1ll_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨↃ"),
            bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧↄ"): {
                bstack1l1l1ll_opy_ (u"ࠨࡵࡶ࡫ࡧࠦↅ"): cls.current_test_uuid(),
                bstack1l1l1ll_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨↆ"): cls.bstack111lll1l11_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1llll_opy_(cls, event: str, bstack111l111l11_opy_: bstack111l1111ll_opy_):
        bstack111l1l1l11_opy_ = {
            bstack1l1l1ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬↇ"): event,
            bstack111l111l11_opy_.bstack1111llllll_opy_(): bstack111l111l11_opy_.bstack1111lllll1_opy_(event)
        }
        cls.bstack11ll11l1ll_opy_(bstack111l1l1l11_opy_)
        result = getattr(bstack111l111l11_opy_, bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩↈ"), None)
        if event == bstack1l1l1ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ↉"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ↊"): bstack1l1l1ll_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭↋")}
        elif event == bstack1l1l1ll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ↌"):
            threading.current_thread().bstackTestMeta = {bstack1l1l1ll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ↍"): getattr(result, bstack1l1l1ll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ↎"), bstack1l1l1ll_opy_ (u"ࠩࠪ↏"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ←"), None) is None or os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ↑")] == bstack1l1l1ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ→")) and (os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ↓"), None) is None or os.environ[bstack1l1l1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ↔")] == bstack1l1l1ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ↕")):
            return False
        return True
    @staticmethod
    def bstack1llll1ll1lll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llllll11l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1l1ll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ↖"): bstack1l1l1ll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭↗"),
            bstack1l1l1ll_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧ↘"): bstack1l1l1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ↙")
        }
        if os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ↚"), None):
            headers[bstack1l1l1ll_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧ↛")] = bstack1l1l1ll_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫ↜").format(os.environ[bstack1l1l1ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨ↝")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1l1ll_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ↞").format(bstack1llll1llll1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ↟"), None)
    @staticmethod
    def bstack111lll1l11_opy_(driver):
        return {
            bstack111lll11l1l_opy_(): bstack11l111l11ll_opy_(driver)
        }
    @staticmethod
    def bstack1llll1l1lll1_opy_(exception_info, report):
        return [{bstack1l1l1ll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ↠"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111ll1l_opy_(typename):
        if bstack1l1l1ll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤ↡") in typename:
            return bstack1l1l1ll_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣ↢")
        return bstack1l1l1ll_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤ↣")