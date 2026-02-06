# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l1l1ll111_opy_, bstack11l1l1ll1ll_opy_, bstack111ll111_opy_, error_handler, bstack111ll111l11_opy_, bstack111ll1llll1_opy_, bstack1111lllll1l_opy_, bstack1lll11lll1_opy_, bstack1l1ll1ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1lll1lll1lll_opy_ import bstack1lll1lll1l1l_opy_
import bstack_utils.bstack111ll1ll1l_opy_ as bstack1llll1111_opy_
from bstack_utils.bstack1111l1lll1_opy_ import bstack1l1l11llll_opy_
import bstack_utils.accessibility as bstack11l1llll11_opy_
from bstack_utils.bstack1ll1111l1l_opy_ import bstack1ll1111l1l_opy_
from bstack_utils.bstack1111llllll_opy_ import bstack111111llll_opy_
from bstack_utils.constants import bstack11ll11lll1_opy_
bstack1lll11l11ll1_opy_ = bstack11lllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ≘")
logger = logging.getLogger(__name__)
class bstack11lll1111l_opy_:
    bstack1lll1lll1lll_opy_ = None
    bs_config = None
    bstack1l1l111111_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l11111111_opy_, stage=STAGE.bstack1llll11111_opy_)
    def launch(cls, bs_config, bstack1l1l111111_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1l111111_opy_ = bstack1l1l111111_opy_
        try:
            cls.bstack1lll11l1ll1l_opy_()
            bstack11l11llllll_opy_ = bstack11l1l1ll111_opy_(bs_config)
            bstack11l1l1111l1_opy_ = bstack11l1l1ll1ll_opy_(bs_config)
            data = bstack1llll1111_opy_.bstack1lll11l1l111_opy_(bs_config, bstack1l1l111111_opy_)
            config = {
                bstack11lllll_opy_ (u"ࠨࡣࡸࡸ࡭࠭≙"): (bstack11l11llllll_opy_, bstack11l1l1111l1_opy_),
                bstack11lllll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ≚"): cls.default_headers()
            }
            response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ≛"), cls.request_url(bstack11lllll_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ≜")), data, config)
            if response.status_code != 200:
                bstack1l1ll11l1_opy_ = response.json()
                if bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭≝")] == False:
                    cls.bstack1lll11l11l11_opy_(bstack1l1ll11l1_opy_)
                    return
                cls.bstack1lll11ll1ll1_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭≞")])
                cls.bstack1lll11l1llll_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ≟")])
                return None
            bstack1lll11ll1lll_opy_ = cls.bstack1lll11l111ll_opy_(response)
            return bstack1lll11ll1lll_opy_, response.json()
        except Exception as error:
            logger.error(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ≠").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l111l11ll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def stop(cls, bstack1lll11ll1l1l_opy_=None):
        if not bstack1l1l11llll_opy_.on() and not bstack11l1llll11_opy_.on():
            return
        if os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭≡")) == bstack11lllll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ≢") or os.environ.get(bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ≣")) == bstack11lllll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ≤"):
            logger.error(bstack11lllll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ≥"))
            return {
                bstack11lllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ≦"): bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ≧"),
                bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ≨"): bstack11lllll_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ≩")
            }
        try:
            cls.bstack1lll1lll1lll_opy_.shutdown()
            data = {
                bstack11lllll_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ≪"): bstack1lll11lll1_opy_()
            }
            if not bstack1lll11ll1l1l_opy_ is None:
                data[bstack11lllll_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ≫")] = [{
                    bstack11lllll_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭≬"): bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ≭"),
                    bstack11lllll_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ≮"): bstack1lll11ll1l1l_opy_
                }]
            config = {
                bstack11lllll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ≯"): cls.default_headers()
            }
            bstack11l11ll1ll1_opy_ = bstack11lllll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫ≰").format(os.environ[bstack11lllll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ≱")])
            bstack1lll11llll11_opy_ = cls.request_url(bstack11l11ll1ll1_opy_)
            response = bstack111ll111_opy_(bstack11lllll_opy_ (u"ࠬࡖࡕࡕࠩ≲"), bstack1lll11llll11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11lllll_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ≳"))
        except Exception as error:
            logger.error(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦ≴") + str(error))
            return {
                bstack11lllll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ≵"): bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ≶"),
                bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ≷"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11l111ll_opy_(cls, response):
        bstack1l1ll11l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll11ll1lll_opy_ = {}
        if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠫ࡯ࡽࡴࠨ≸")) is None:
            os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ≹")] = bstack11lllll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ≺")
        else:
            os.environ[bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ≻")] = bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠨ࡬ࡺࡸࠬ≼"), bstack11lllll_opy_ (u"ࠩࡱࡹࡱࡲࠧ≽"))
        os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ≾")] = bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭≿"), bstack11lllll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⊀"))
        logger.info(bstack11lllll_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ⊁") + os.getenv(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⊂")));
        if bstack1l1l11llll_opy_.bstack1lll11lll11l_opy_(cls.bs_config, cls.bstack1l1l111111_opy_.get(bstack11lllll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⊃"), bstack11lllll_opy_ (u"ࠩࠪ⊄"))) is True:
            bstack1lll1ll1l111_opy_, build_hashed_id, bstack1lll11l1l1ll_opy_ = cls.bstack1lll11l1lll1_opy_(bstack1l1ll11l1_opy_)
            if bstack1lll1ll1l111_opy_ != None and build_hashed_id != None:
                bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⊅")] = {
                    bstack11lllll_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧ⊆"): bstack1lll1ll1l111_opy_,
                    bstack11lllll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⊇"): build_hashed_id,
                    bstack11lllll_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⊈"): bstack1lll11l1l1ll_opy_
                }
            else:
                bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⊉")] = {}
        else:
            bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⊊")] = {}
        bstack1lll11ll11l1_opy_, build_hashed_id = cls.bstack1lll11l1ll11_opy_(bstack1l1ll11l1_opy_)
        if bstack1lll11ll11l1_opy_ != None and build_hashed_id != None:
            bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⊋")] = {
                bstack11lllll_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧ⊌"): bstack1lll11ll11l1_opy_,
                bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⊍"): build_hashed_id,
            }
        else:
            bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⊎")] = {}
        if bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⊏")].get(bstack11lllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⊐")) != None or bstack1lll11ll1lll_opy_[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⊑")].get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⊒")) != None:
            cls.bstack1lll11l1l11l_opy_(bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠪ࡮ࡼࡺࠧ⊓")), bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⊔")))
        return bstack1lll11ll1lll_opy_
    @classmethod
    def bstack1lll11l1lll1_opy_(cls, bstack1l1ll11l1_opy_):
        if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⊕")) == None:
            cls.bstack1lll11ll1ll1_opy_()
            return [None, None, None]
        if bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⊖")][bstack11lllll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⊗")] != True:
            cls.bstack1lll11ll1ll1_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⊘")])
            return [None, None, None]
        logger.debug(bstack11lllll_opy_ (u"ࠩࡾࢁࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫ⊙").format(bstack11ll11lll1_opy_))
        os.environ[bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ⊚")] = bstack11lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩ⊛")
        if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠬࡰࡷࡵࠩ⊜")):
            os.environ[bstack11lllll_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ⊝")] = json.dumps({
                bstack11lllll_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ⊞"): bstack11l1l1ll111_opy_(cls.bs_config),
                bstack11lllll_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ⊟"): bstack11l1l1ll1ll_opy_(cls.bs_config)
            })
        if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⊠")):
            os.environ[bstack11lllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⊡")] = bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⊢")]
        if bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⊣")].get(bstack11lllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⊤"), {}).get(bstack11lllll_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⊥")):
            os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⊦")] = str(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⊧")][bstack11lllll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⊨")][bstack11lllll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⊩")])
        else:
            os.environ[bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⊪")] = bstack11lllll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⊫")
        return [bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠧ࡫ࡹࡷࠫ⊬")], bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⊭")], os.environ[bstack11lllll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⊮")]]
    @classmethod
    def bstack1lll11l1ll11_opy_(cls, bstack1l1ll11l1_opy_):
        if bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⊯")) == None:
            cls.bstack1lll11l1llll_opy_()
            return [None, None]
        if bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⊰")][bstack11lllll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⊱")] != True:
            cls.bstack1lll11l1llll_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⊲")])
            return [None, None]
        if bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⊳")].get(bstack11lllll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⊴")):
            logger.debug(bstack11lllll_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭⊵"))
            parsed = json.loads(os.getenv(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⊶"), bstack11lllll_opy_ (u"ࠫࢀࢃࠧ⊷")))
            capabilities = bstack1llll1111_opy_.bstack1lll11ll1l11_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⊸")][bstack11lllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⊹")][bstack11lllll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭⊺")], bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⊻"), bstack11lllll_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ⊼"))
            bstack1lll11ll11l1_opy_ = capabilities[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ⊽")]
            os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⊾")] = bstack1lll11ll11l1_opy_
            if bstack11lllll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ⊿") in bstack1l1ll11l1_opy_ and bstack1l1ll11l1_opy_.get(bstack11lllll_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⋀")) is None:
                parsed[bstack11lllll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⋁")] = capabilities[bstack11lllll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⋂")]
            os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⋃")] = json.dumps(parsed)
            scripts = bstack1llll1111_opy_.bstack1lll11ll1l11_opy_(bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⋄")][bstack11lllll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⋅")][bstack11lllll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⋆")], bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⋇"), bstack11lllll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨ⋈"))
            bstack1ll1111l1l_opy_.bstack1l11l11ll1_opy_(scripts)
            commands = bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⋉")][bstack11lllll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⋊")][bstack11lllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫ⋋")].get(bstack11lllll_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭⋌"))
            bstack1ll1111l1l_opy_.bstack11l1ll111l1_opy_(commands)
            bstack11l1l1l111l_opy_ = capabilities.get(bstack11lllll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⋍"))
            bstack1ll1111l1l_opy_.bstack11l11lll1l1_opy_(bstack11l1l1l111l_opy_)
            bstack1ll1111l1l_opy_.store()
        return [bstack1lll11ll11l1_opy_, bstack1l1ll11l1_opy_[bstack11lllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⋎")]]
    @classmethod
    def bstack1lll11ll1ll1_opy_(cls, response=None):
        os.environ[bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ⋏")] = bstack11lllll_opy_ (u"ࠨࡰࡸࡰࡱ࠭⋐")
        os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⋑")] = bstack11lllll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ⋒")
        os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ⋓")] = bstack11lllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ⋔")
        os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ⋕")] = bstack11lllll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⋖")
        os.environ[bstack11lllll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⋗")] = bstack11lllll_opy_ (u"ࠤࡱࡹࡱࡲࠢ⋘")
        cls.bstack1lll11l11l11_opy_(response, bstack11lllll_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ⋙"))
        return [None, None, None]
    @classmethod
    def bstack1lll11l1llll_opy_(cls, response=None):
        os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⋚")] = bstack11lllll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⋛")
        os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⋜")] = bstack11lllll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⋝")
        os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⋞")] = bstack11lllll_opy_ (u"ࠩࡱࡹࡱࡲࠧ⋟")
        cls.bstack1lll11l11l11_opy_(response, bstack11lllll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ⋠"))
        return [None, None, None]
    @classmethod
    def bstack1lll11l1l11l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11lllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⋡")] = jwt
        os.environ[bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⋢")] = build_hashed_id
    @classmethod
    def bstack1lll11l11l11_opy_(cls, response=None, product=bstack11lllll_opy_ (u"ࠨࠢ⋣")):
        if response == None or response.get(bstack11lllll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ⋤")) == None:
            logger.error(product + bstack11lllll_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥ⋥"))
            return
        for error in response[bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ⋦")]:
            bstack111ll1ll1ll_opy_ = error[bstack11lllll_opy_ (u"ࠪ࡯ࡪࡿࠧ⋧")]
            error_message = error[bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⋨")]
            if error_message:
                if bstack111ll1ll1ll_opy_ == bstack11lllll_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ⋩"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11lllll_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ⋪") + product + bstack11lllll_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ⋫"))
    @classmethod
    def bstack1lll11l1ll1l_opy_(cls):
        if cls.bstack1lll1lll1lll_opy_ is not None:
            return
        cls.bstack1lll1lll1lll_opy_ = bstack1lll1lll1l1l_opy_(cls.bstack1lll11lll1l1_opy_)
        cls.bstack1lll1lll1lll_opy_.start()
    @classmethod
    def bstack1111l1l11l_opy_(cls):
        if cls.bstack1lll1lll1lll_opy_ is None:
            return
        cls.bstack1lll1lll1lll_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11lll1l1_opy_(cls, bstack1111111l1l_opy_, event_url=bstack11lllll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ⋬")):
        config = {
            bstack11lllll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ⋭"): cls.default_headers()
        }
        logger.debug(bstack11lllll_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ⋮").format(bstack11lllll_opy_ (u"ࠫ࠱ࠦࠧ⋯").join([event[bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⋰")] for event in bstack1111111l1l_opy_])))
        response = bstack111ll111_opy_(bstack11lllll_opy_ (u"࠭ࡐࡐࡕࡗࠫ⋱"), cls.request_url(event_url), bstack1111111l1l_opy_, config)
        bstack11l1l1lllll_opy_ = response.json()
    @classmethod
    def bstack11ll1llll1_opy_(cls, bstack1111111l1l_opy_, event_url=bstack11lllll_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭⋲")):
        logger.debug(bstack11lllll_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ⋳").format(bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⋴")]))
        if not bstack1llll1111_opy_.bstack1lll11ll1111_opy_(bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⋵")]):
            logger.debug(bstack11lllll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⋶").format(bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⋷")]))
            return
        bstack1l1l111ll1_opy_ = bstack1llll1111_opy_.bstack1lll11l11l1l_opy_(bstack1111111l1l_opy_[bstack11lllll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⋸")], bstack1111111l1l_opy_.get(bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ⋹")))
        if bstack1l1l111ll1_opy_ != None:
            if bstack1111111l1l_opy_.get(bstack11lllll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ⋺")) != None:
                bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ⋻")][bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⋼")] = bstack1l1l111ll1_opy_
            else:
                bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⋽")] = bstack1l1l111ll1_opy_
        if event_url == bstack11lllll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⋾"):
            cls.bstack1lll11l1ll1l_opy_()
            logger.debug(bstack11lllll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ⋿").format(bstack1111111l1l_opy_[bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⌀")]))
            cls.bstack1lll1lll1lll_opy_.add(bstack1111111l1l_opy_)
        elif event_url == bstack11lllll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⌁"):
            cls.bstack1lll11lll1l1_opy_([bstack1111111l1l_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack1ll111l1ll_opy_(cls, logs):
        for log in logs:
            bstack1lll11l1l1l1_opy_ = {
                bstack11lllll_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ⌂"): bstack11lllll_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ⌃"),
                bstack11lllll_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ⌄"): log[bstack11lllll_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⌅")],
                bstack11lllll_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⌆"): log[bstack11lllll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⌇")],
                bstack11lllll_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ⌈"): {},
                bstack11lllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⌉"): log[bstack11lllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⌊")],
            }
            if bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⌋") in log:
                bstack1lll11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⌌")] = log[bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌍")]
            elif bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌎") in log:
                bstack1lll11l1l1l1_opy_[bstack11lllll_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⌏")] = log[bstack11lllll_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌐")]
            cls.bstack11ll1llll1_opy_({
                bstack11lllll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⌑"): bstack11lllll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⌒"),
                bstack11lllll_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⌓"): [bstack1lll11l1l1l1_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11lll1ll_opy_(cls, steps):
        bstack1lll11l11lll_opy_ = []
        for step in steps:
            bstack1lll11ll111l_opy_ = {
                bstack11lllll_opy_ (u"࠭࡫ࡪࡰࡧࠫ⌔"): bstack11lllll_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ⌕"),
                bstack11lllll_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⌖"): step[bstack11lllll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⌗")],
                bstack11lllll_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⌘"): step[bstack11lllll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⌙")],
                bstack11lllll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⌚"): step[bstack11lllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⌛")],
                bstack11lllll_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⌜"): step[bstack11lllll_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⌝")]
            }
            if bstack11lllll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⌞") in step:
                bstack1lll11ll111l_opy_[bstack11lllll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⌟")] = step[bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⌠")]
            elif bstack11lllll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⌡") in step:
                bstack1lll11ll111l_opy_[bstack11lllll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌢")] = step[bstack11lllll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌣")]
            bstack1lll11l11lll_opy_.append(bstack1lll11ll111l_opy_)
        cls.bstack11ll1llll1_opy_({
            bstack11lllll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⌤"): bstack11lllll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⌥"),
            bstack11lllll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⌦"): bstack1lll11l11lll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack11l1ll11ll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l11l111ll_opy_(cls, screenshot):
        cls.bstack11ll1llll1_opy_({
            bstack11lllll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⌧"): bstack11lllll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⌨"),
            bstack11lllll_opy_ (u"࠭࡬ࡰࡩࡶࠫ〈"): [{
                bstack11lllll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ〉"): bstack11lllll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ⌫"),
                bstack11lllll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⌬"): datetime.datetime.utcnow().isoformat() + bstack11lllll_opy_ (u"ࠪ࡞ࠬ⌭"),
                bstack11lllll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⌮"): screenshot[bstack11lllll_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⌯")],
                bstack11lllll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⌰"): screenshot[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⌱")]
            }]
        }, event_url=bstack11lllll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭⌲"))
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll111lll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll1llll1_opy_({
            bstack11lllll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⌳"): bstack11lllll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⌴"),
            bstack11lllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⌵"): {
                bstack11lllll_opy_ (u"ࠧࡻࡵࡪࡦࠥ⌶"): cls.current_test_uuid(),
                bstack11lllll_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ⌷"): cls.bstack1111lll1ll_opy_(driver)
            }
        })
    @classmethod
    def bstack111l111111_opy_(cls, event: str, bstack1111111l1l_opy_: bstack111111llll_opy_):
        bstack1111l11l1l_opy_ = {
            bstack11lllll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⌸"): event,
            bstack1111111l1l_opy_.bstack11111111l1_opy_(): bstack1111111l1l_opy_.bstack11111l11ll_opy_(event)
        }
        cls.bstack11ll1llll1_opy_(bstack1111l11l1l_opy_)
        result = getattr(bstack1111111l1l_opy_, bstack11lllll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⌹"), None)
        if event == bstack11lllll_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⌺"):
            threading.current_thread().bstackTestMeta = {bstack11lllll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⌻"): bstack11lllll_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⌼")}
        elif event == bstack11lllll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⌽"):
            threading.current_thread().bstackTestMeta = {bstack11lllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⌾"): getattr(result, bstack11lllll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⌿"), bstack11lllll_opy_ (u"ࠨࠩ⍀"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⍁"), None) is None or os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⍂")] == bstack11lllll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⍃")) and (os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⍄"), None) is None or os.environ[bstack11lllll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⍅")] == bstack11lllll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⍆")):
            return False
        return True
    @staticmethod
    def bstack1lll11ll11ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11lll1111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11lllll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⍇"): bstack11lllll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⍈"),
            bstack11lllll_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭⍉"): bstack11lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩ⍊")
        }
        if os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⍋"), None):
            headers[bstack11lllll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⍌")] = bstack11lllll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ⍍").format(os.environ[bstack11lllll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧ⍎")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11lllll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ⍏").format(bstack1lll11l11ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11lllll_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ⍐"), None)
    @staticmethod
    def bstack1111lll1ll_opy_(driver):
        return {
            bstack111ll111l11_opy_(): bstack111ll1llll1_opy_(driver)
        }
    @staticmethod
    def bstack1lll11lll111_opy_(exception_info, report):
        return [{bstack11lllll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ⍑"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1llll1111ll_opy_(typename):
        if bstack11lllll_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ⍒") in typename:
            return bstack11lllll_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ⍓")
        return bstack11lllll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ⍔")