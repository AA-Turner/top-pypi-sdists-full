# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1ll11l1_opy_, bstack11ll1ll1l11_opy_, bstack1lllll1111_opy_, error_handler, bstack111llll1lll_opy_, bstack11l111l111l_opy_, bstack111llll111l_opy_, bstack11l1l1l1l1_opy_, bstack1111l1l11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11ll1lll1ll_opy_ import bstack11ll1llllll_opy_
import bstack_utils.bstack1l1ll111_opy_ as bstack111llll11l_opy_
from bstack_utils.bstack111ll11111_opy_ import bstack11lllllll1_opy_
import bstack_utils.accessibility as bstack1l1l11l1l1_opy_
from bstack_utils.bstack1llll111_opy_ import bstack1llll111_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1111l1lll1_opy_
from bstack_utils.constants import bstack1l1llll11_opy_
bstack1llll1ll111l_opy_ = bstack1ll11ll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ₝")
logger = logging.getLogger(__name__)
class bstack1l11ll1l_opy_:
    bstack11ll1lll1ll_opy_ = None
    bs_config = None
    bstack1111l1l1l_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1l1l1l11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def launch(cls, bs_config, bstack1111l1l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1111l1l1l_opy_ = bstack1111l1l1l_opy_
        try:
            cls.bstack1llll1l1lll1_opy_()
            bstack11ll1l11lll_opy_ = bstack11ll1ll11l1_opy_(bs_config)
            bstack11ll11ll111_opy_ = bstack11ll1ll1l11_opy_(bs_config)
            data = bstack111llll11l_opy_.bstack1llll1l11l11_opy_(bs_config, bstack1111l1l1l_opy_)
            config = {
                bstack1ll11ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ₞"): (bstack11ll1l11lll_opy_, bstack11ll11ll111_opy_),
                bstack1ll11ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ₟"): cls.default_headers()
            }
            response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭₠"), cls.request_url(bstack1ll11ll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩ₡")), data, config)
            if response.status_code != 200:
                bstack1llll111ll_opy_ = response.json()
                if bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ₢")] == False:
                    cls.bstack1llll1l1l1ll_opy_(bstack1llll111ll_opy_)
                    return
                cls.bstack1llll1ll1111_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ₣")])
                cls.bstack1llll11lllll_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ₤")])
                return None
            bstack1llll1ll1ll1_opy_ = cls.bstack1llll11llll1_opy_(response)
            return bstack1llll1ll1ll1_opy_, response.json()
        except Exception as error:
            logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ₥").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    def stop(cls, bstack1llll1l111ll_opy_=None):
        if not bstack11lllllll1_opy_.on() and not bstack1l1l11l1l1_opy_.on():
            return
        if os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ₦")) == bstack1ll11ll_opy_ (u"ࠣࡰࡸࡰࡱࠨ₧") or os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ₨")) == bstack1ll11ll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ₩"):
            logger.error(bstack1ll11ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧ₪"))
            return {
                bstack1ll11ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ₫"): bstack1ll11ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ€"),
                bstack1ll11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ₭"): bstack1ll11ll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭₮")
            }
        try:
            cls.bstack11ll1lll1ll_opy_.shutdown()
            data = {
                bstack1ll11ll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ₯"): bstack11l1l1l1l1_opy_()
            }
            if not bstack1llll1l111ll_opy_ is None:
                data[bstack1ll11ll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ₰")] = [{
                    bstack1ll11ll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫ₱"): bstack1ll11ll_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ₲"),
                    bstack1ll11ll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭₳"): bstack1llll1l111ll_opy_
                }]
            config = {
                bstack1ll11ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ₴"): cls.default_headers()
            }
            bstack11ll1111ll1_opy_ = bstack1ll11ll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩ₵").format(os.environ[bstack1ll11ll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ₶")])
            bstack1llll11lll1l_opy_ = cls.request_url(bstack11ll1111ll1_opy_)
            response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠪࡔ࡚࡚ࠧ₷"), bstack1llll11lll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll11ll_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ₸"))
        except Exception as error:
            logger.error(bstack1ll11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤ₹") + str(error))
            return {
                bstack1ll11ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭₺"): bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭₻"),
                bstack1ll11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ₼"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll11llll1_opy_(cls, response):
        bstack1llll111ll_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1llll1ll1ll1_opy_ = {}
        if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠩ࡭ࡻࡹ࠭₽")) is None:
            os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ₾")] = bstack1ll11ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ₿")
        else:
            os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⃀")] = bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡪࡸࡶࠪ⃁"), bstack1ll11ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⃂"))
        os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⃃")] = bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⃄"), bstack1ll11ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⃅"))
        logger.info(bstack1ll11ll_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩ⃆") + os.getenv(bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⃇")));
        if bstack11lllllll1_opy_.bstack1llll1ll1l11_opy_(cls.bs_config, cls.bstack1111l1l1l_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ⃈"), bstack1ll11ll_opy_ (u"ࠧࠨ⃉"))) is True:
            bstack1llllll11ll1_opy_, build_hashed_id, bstack1llll1l1l1l1_opy_ = cls.bstack1llll1l11111_opy_(bstack1llll111ll_opy_)
            if bstack1llllll11ll1_opy_ != None and build_hashed_id != None:
                bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⃊")] = {
                    bstack1ll11ll_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬ⃋"): bstack1llllll11ll1_opy_,
                    bstack1ll11ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⃌"): build_hashed_id,
                    bstack1ll11ll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⃍"): bstack1llll1l1l1l1_opy_
                }
            else:
                bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃎")] = {}
        else:
            bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃏")] = {}
        bstack1llll1l1llll_opy_, build_hashed_id = cls.bstack1llll1l1ll11_opy_(bstack1llll111ll_opy_)
        if bstack1llll1l1llll_opy_ != None and build_hashed_id != None:
            bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃐")] = {
                bstack1ll11ll_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬ⃑"): bstack1llll1l1llll_opy_,
                bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ⃒ࠫ"): build_hashed_id,
            }
        else:
            bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻ⃓ࠪ")] = {}
        if bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃔")].get(bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⃕")) != None or bstack1llll1ll1ll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃖")].get(bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⃗")) != None:
            cls.bstack1llll1l11l1l_opy_(bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠨ࡬ࡺࡸ⃘ࠬ")), bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧ⃙ࠫ")))
        return bstack1llll1ll1ll1_opy_
    @classmethod
    def bstack1llll1l11111_opy_(cls, bstack1llll111ll_opy_):
        if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃚ࠪ")) == None:
            cls.bstack1llll1ll1111_opy_()
            return [None, None, None]
        if bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃛")][bstack1ll11ll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⃜")] != True:
            cls.bstack1llll1ll1111_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃝")])
            return [None, None, None]
        logger.debug(bstack1ll11ll_opy_ (u"ࠧࡼࡿࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩ⃞").format(bstack1l1llll11_opy_))
        os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⃟")] = bstack1ll11ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ⃠")
        if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠪ࡮ࡼࡺࠧ⃡")):
            os.environ[bstack1ll11ll_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨ⃢")] = json.dumps({
                bstack1ll11ll_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ⃣"): bstack11ll1ll11l1_opy_(cls.bs_config),
                bstack1ll11ll_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨ⃤"): bstack11ll1ll1l11_opy_(cls.bs_config)
            })
        if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥ⃥ࠩ")):
            os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊ⃦ࠧ")] = bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⃧")]
        if bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃨ࠪ")].get(bstack1ll11ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⃩"), {}).get(bstack1ll11ll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴ⃪ࠩ")):
            os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ⃫࡙࡙ࠧ")] = str(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ⃬ࠧ")][bstack1ll11ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴ⃭ࠩ")][bstack1ll11ll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ⃮࠭")])
        else:
            os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖ⃯ࠫ")] = bstack1ll11ll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⃰")
        return [bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡰࡷࡵࠩ⃱")], bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⃲")], os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ⃳")]]
    @classmethod
    def bstack1llll1l1ll11_opy_(cls, bstack1llll111ll_opy_):
        if bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃴")) == None:
            cls.bstack1llll11lllll_opy_()
            return [None, None]
        if bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃵")][bstack1ll11ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⃶")] != True:
            cls.bstack1llll11lllll_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃷")])
            return [None, None]
        if bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃸")].get(bstack1ll11ll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⃹")):
            logger.debug(bstack1ll11ll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⃺"))
            parsed = json.loads(os.getenv(bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⃻"), bstack1ll11ll_opy_ (u"ࠩࡾࢁࠬ⃼")))
            capabilities = bstack111llll11l_opy_.bstack1llll1ll1l1l_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⃽")][bstack1ll11ll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⃾")][bstack1ll11ll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⃿")], bstack1ll11ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ℀"), bstack1ll11ll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭℁"))
            bstack1llll1l1llll_opy_ = capabilities[bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ℂ")]
            os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ℃")] = bstack1llll1l1llll_opy_
            if bstack1ll11ll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ℄") in bstack1llll111ll_opy_ and bstack1llll111ll_opy_.get(bstack1ll11ll_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ℅")) is None:
                parsed[bstack1ll11ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭℆")] = capabilities[bstack1ll11ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧℇ")]
            os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ℈")] = json.dumps(parsed)
            scripts = bstack111llll11l_opy_.bstack1llll1ll1l1l_opy_(bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ℉")][bstack1ll11ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪℊ")][bstack1ll11ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫℋ")], bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩℌ"), bstack1ll11ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ℍ"))
            bstack1llll111_opy_.bstack1l111l11_opy_(scripts)
            commands = bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ℎ")][bstack1ll11ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨℏ")][bstack1ll11ll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩℐ")].get(bstack1ll11ll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫℑ"))
            bstack1llll111_opy_.bstack11ll11l1l11_opy_(commands)
            bstack11ll1l11l11_opy_ = capabilities.get(bstack1ll11ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨℒ"))
            bstack1llll111_opy_.bstack11ll111l11l_opy_(bstack11ll1l11l11_opy_)
            bstack1llll111_opy_.store()
        return [bstack1llll1l1llll_opy_, bstack1llll111ll_opy_[bstack1ll11ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ℓ")]]
    @classmethod
    def bstack1llll1ll1111_opy_(cls, response=None):
        os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ℔")] = bstack1ll11ll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫℕ")
        os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ№")] = bstack1ll11ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭℗")
        os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨ℘")] = bstack1ll11ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩℙ")
        os.environ[bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪℚ")] = bstack1ll11ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥℛ")
        os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧℜ")] = bstack1ll11ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧℝ")
        cls.bstack1llll1l1l1ll_opy_(response, bstack1ll11ll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ℞"))
        return [None, None, None]
    @classmethod
    def bstack1llll11lllll_opy_(cls, response=None):
        os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ℟")] = bstack1ll11ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ℠")
        os.environ[bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ℡")] = bstack1ll11ll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ™")
        os.environ[bstack1ll11ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ℣")] = bstack1ll11ll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬℤ")
        cls.bstack1llll1l1l1ll_opy_(response, bstack1ll11ll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ℥"))
        return [None, None, None]
    @classmethod
    def bstack1llll1l11l1l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ω")] = jwt
        os.environ[bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ℧")] = build_hashed_id
    @classmethod
    def bstack1llll1l1l1ll_opy_(cls, response=None, product=bstack1ll11ll_opy_ (u"ࠦࠧℨ")):
        if response == None or response.get(bstack1ll11ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬ℩")) == None:
            logger.error(product + bstack1ll11ll_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣK"))
            return
        for error in response[bstack1ll11ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧÅ")]:
            bstack111llll11l1_opy_ = error[bstack1ll11ll_opy_ (u"ࠨ࡭ࡨࡽࠬℬ")]
            error_message = error[bstack1ll11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪℭ")]
            if error_message:
                if bstack111llll11l1_opy_ == bstack1ll11ll_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤ℮"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll11ll_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧℯ") + product + bstack1ll11ll_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥℰ"))
    @classmethod
    def bstack1llll1l1lll1_opy_(cls):
        if cls.bstack11ll1lll1ll_opy_ is not None:
            return
        cls.bstack11ll1lll1ll_opy_ = bstack11ll1llllll_opy_(cls.bstack1llll1ll11l1_opy_)
        cls.bstack11ll1lll1ll_opy_.start()
    @classmethod
    def bstack1111lll111_opy_(cls):
        if cls.bstack11ll1lll1ll_opy_ is None:
            return
        cls.bstack11ll1lll1ll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1ll11l1_opy_(cls, bstack111l11ll11_opy_, event_url=bstack1ll11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬℱ")):
        config = {
            bstack1ll11ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨℲ"): cls.default_headers()
        }
        logger.debug(bstack1ll11ll_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣℳ").format(bstack1ll11ll_opy_ (u"ࠩ࠯ࠤࠬℴ").join([event[bstack1ll11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧℵ")] for event in bstack111l11ll11_opy_])))
        response = bstack1lllll1111_opy_(bstack1ll11ll_opy_ (u"ࠫࡕࡕࡓࡕࠩℶ"), cls.request_url(event_url), bstack111l11ll11_opy_, config)
        bstack11ll11ll1ll_opy_ = response.json()
    @classmethod
    def bstack11l11l1l11_opy_(cls, bstack111l11ll11_opy_, event_url=bstack1ll11ll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫℷ")):
        logger.debug(bstack1ll11ll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨℸ").format(bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫℹ")]))
        if not bstack111llll11l_opy_.bstack1llll1l11lll_opy_(bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ℺")]):
            logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ℻").format(bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧℼ")]))
            return
        bstack1l1l1111l_opy_ = bstack111llll11l_opy_.bstack1llll1l1111l_opy_(bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨℽ")], bstack111l11ll11_opy_.get(bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧℾ")))
        if bstack1l1l1111l_opy_ != None:
            if bstack111l11ll11_opy_.get(bstack1ll11ll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨℿ")) != None:
                bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⅀")][bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⅁")] = bstack1l1l1111l_opy_
            else:
                bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⅂")] = bstack1l1l1111l_opy_
        if event_url == bstack1ll11ll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩ⅃"):
            cls.bstack1llll1l1lll1_opy_()
            logger.debug(bstack1ll11ll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ⅄").format(bstack111l11ll11_opy_[bstack1ll11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅅ")]))
            cls.bstack11ll1lll1ll_opy_.add(bstack111l11ll11_opy_)
        elif event_url == bstack1ll11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫⅆ"):
            cls.bstack1llll1ll11l1_opy_([bstack111l11ll11_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11lllll11l_opy_(cls, logs):
        for log in logs:
            bstack1llll1l11ll1_opy_ = {
                bstack1ll11ll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬⅇ"): bstack1ll11ll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪⅈ"),
                bstack1ll11ll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨⅉ"): log[bstack1ll11ll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ⅊")],
                bstack1ll11ll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⅋"): log[bstack1ll11ll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ⅌")],
                bstack1ll11ll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭⅍"): {},
                bstack1ll11ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨⅎ"): log[bstack1ll11ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⅏")],
            }
            if bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⅐") in log:
                bstack1llll1l11ll1_opy_[bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⅑")] = log[bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⅒")]
            elif bstack1ll11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⅓") in log:
                bstack1llll1l11ll1_opy_[bstack1ll11ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⅔")] = log[bstack1ll11ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⅕")]
            cls.bstack11l11l1l11_opy_({
                bstack1ll11ll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⅖"): bstack1ll11ll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⅗"),
                bstack1ll11ll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⅘"): [bstack1llll1l11ll1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1llll1l111l1_opy_(cls, steps):
        bstack1llll1ll11ll_opy_ = []
        for step in steps:
            bstack1llll1l1l111_opy_ = {
                bstack1ll11ll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⅙"): bstack1ll11ll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨ⅚"),
                bstack1ll11ll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⅛"): step[bstack1ll11ll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⅜")],
                bstack1ll11ll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⅝"): step[bstack1ll11ll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⅞")],
                bstack1ll11ll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅟"): step[bstack1ll11ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬⅠ")],
                bstack1ll11ll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧⅡ"): step[bstack1ll11ll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨⅢ")]
            }
            if bstack1ll11ll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧⅣ") in step:
                bstack1llll1l1l111_opy_[bstack1ll11ll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨⅤ")] = step[bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩⅥ")]
            elif bstack1ll11ll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⅦ") in step:
                bstack1llll1l1l111_opy_[bstack1ll11ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅧ")] = step[bstack1ll11ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅨ")]
            bstack1llll1ll11ll_opy_.append(bstack1llll1l1l111_opy_)
        cls.bstack11l11l1l11_opy_({
            bstack1ll11ll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪⅩ"): bstack1ll11ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫⅪ"),
            bstack1ll11ll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ⅻ"): bstack1llll1ll11ll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1llll1l1l1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1111l1111_opy_(cls, screenshot):
        cls.bstack11l11l1l11_opy_({
            bstack1ll11ll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ⅼ"): bstack1ll11ll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧⅭ"),
            bstack1ll11ll_opy_ (u"ࠫࡱࡵࡧࡴࠩⅮ"): [{
                bstack1ll11ll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪⅯ"): bstack1ll11ll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨⅰ"),
                bstack1ll11ll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪⅱ"): datetime.datetime.utcnow().isoformat() + bstack1ll11ll_opy_ (u"ࠨ࡜ࠪⅲ"),
                bstack1ll11ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪⅳ"): screenshot[bstack1ll11ll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩⅴ")],
                bstack1ll11ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫⅵ"): screenshot[bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬⅶ")]
            }]
        }, event_url=bstack1ll11ll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫⅷ"))
    @classmethod
    @error_handler(class_method=True)
    def bstack111llll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l11l1l11_opy_({
            bstack1ll11ll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫⅸ"): bstack1ll11ll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬⅹ"),
            bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫⅺ"): {
                bstack1ll11ll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣⅻ"): cls.current_test_uuid(),
                bstack1ll11ll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥⅼ"): cls.bstack111ll1ll1l_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1ll11_opy_(cls, event: str, bstack111l11ll11_opy_: bstack1111l1lll1_opy_):
        bstack1111ll1111_opy_ = {
            bstack1ll11ll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩⅽ"): event,
            bstack111l11ll11_opy_.bstack1111ll11ll_opy_(): bstack111l11ll11_opy_.bstack111l111l11_opy_(event)
        }
        cls.bstack11l11l1l11_opy_(bstack1111ll1111_opy_)
        result = getattr(bstack111l11ll11_opy_, bstack1ll11ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ⅾ"), None)
        if event == bstack1ll11ll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅿ"):
            threading.current_thread().bstackTestMeta = {bstack1ll11ll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨↀ"): bstack1ll11ll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪↁ")}
        elif event == bstack1ll11ll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬↂ"):
            threading.current_thread().bstackTestMeta = {bstack1ll11ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫↃ"): getattr(result, bstack1ll11ll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬↄ"), bstack1ll11ll_opy_ (u"࠭ࠧↅ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫↆ"), None) is None or os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬↇ")] == bstack1ll11ll_opy_ (u"ࠤࡱࡹࡱࡲࠢↈ")) and (os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ↉"), None) is None or os.environ[bstack1ll11ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ↊")] == bstack1ll11ll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ↋")):
            return False
        return True
    @staticmethod
    def bstack1llll1l1l11l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l11ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll11ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ↌"): bstack1ll11ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ↍"),
            bstack1ll11ll_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫ↎"): bstack1ll11ll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ↏")
        }
        if os.environ.get(bstack1ll11ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ←"), None):
            headers[bstack1ll11ll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ↑")] = bstack1ll11ll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ→").format(os.environ[bstack1ll11ll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥ↓")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll11ll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭↔").format(bstack1llll1ll111l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ↕"), None)
    @staticmethod
    def bstack111ll1ll1l_opy_(driver):
        return {
            bstack111llll1lll_opy_(): bstack11l111l111l_opy_(driver)
        }
    @staticmethod
    def bstack1llll1l1ll1l_opy_(exception_info, report):
        return [{bstack1ll11ll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ↖"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111l11l_opy_(typename):
        if bstack1ll11ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ↗") in typename:
            return bstack1ll11ll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ↘")
        return bstack1ll11ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ↙")