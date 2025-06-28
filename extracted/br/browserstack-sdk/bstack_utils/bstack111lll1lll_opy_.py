# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1ll1111_opy_, bstack11ll1l1l1l1_opy_, bstack1l1ll1ll1l_opy_, bstack111l1111ll_opy_, bstack11l11lll1l1_opy_, bstack111llll1l11_opy_, bstack11l11ll11ll_opy_, bstack1llllll1l_opy_, bstack11l1ll11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11111l11111_opy_ import bstack111111lllll_opy_
import bstack_utils.bstack11l11lllll_opy_ as bstack1lllll11_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack111l1ll1l_opy_
import bstack_utils.accessibility as bstack1l11ll1lll_opy_
from bstack_utils.bstack1ll1l1l1l_opy_ import bstack1ll1l1l1l_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack111l11ll11_opy_
bstack1llllll1l111_opy_ = bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫῊ")
logger = logging.getLogger(__name__)
class bstack1l1lll1l_opy_:
    bstack11111l11111_opy_ = None
    bs_config = None
    bstack1lll11111l_opy_ = None
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1lll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def launch(cls, bs_config, bstack1lll11111l_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll11111l_opy_ = bstack1lll11111l_opy_
        try:
            cls.bstack1lllll1lll1l_opy_()
            bstack11ll1ll11ll_opy_ = bstack11ll1ll1111_opy_(bs_config)
            bstack11ll1llllll_opy_ = bstack11ll1l1l1l1_opy_(bs_config)
            data = bstack1lllll11_opy_.bstack1lllll1ll1l1_opy_(bs_config, bstack1lll11111l_opy_)
            config = {
                bstack1l1ll1_opy_ (u"ࠬࡧࡵࡵࡪࠪΉ"): (bstack11ll1ll11ll_opy_, bstack11ll1llllll_opy_),
                bstack1l1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧῌ"): cls.default_headers()
            }
            response = bstack1l1ll1ll1l_opy_(bstack1l1ll1_opy_ (u"ࠧࡑࡑࡖࡘࠬ῍"), cls.request_url(bstack1l1ll1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨ῎")), data, config)
            if response.status_code != 200:
                bstack111lll1l_opy_ = response.json()
                if bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ῏")] == False:
                    cls.bstack1llllll11lll_opy_(bstack111lll1l_opy_)
                    return
                cls.bstack1llllll11111_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪῐ")])
                cls.bstack1lllll1l11l1_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫῑ")])
                return None
            bstack1lllll1l1lll_opy_ = cls.bstack1lllll1ll11l_opy_(response)
            return bstack1lllll1l1lll_opy_, response.json()
        except Exception as error:
            logger.error(bstack1l1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥῒ").format(str(error)))
            return None
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def stop(cls, bstack1lllll1llll1_opy_=None):
        if not bstack111l1ll1l_opy_.on() and not bstack1l11ll1lll_opy_.on():
            return
        if os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪΐ")) == bstack1l1ll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ῔") or os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭῕")) == bstack1l1ll1_opy_ (u"ࠤࡱࡹࡱࡲࠢῖ"):
            logger.error(bstack1l1ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ῗ"))
            return {
                bstack1l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫῘ"): bstack1l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫῙ"),
                bstack1l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧῚ"): bstack1l1ll1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬΊ")
            }
        try:
            cls.bstack11111l11111_opy_.shutdown()
            data = {
                bstack1l1ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭῜"): bstack1llllll1l_opy_()
            }
            if not bstack1lllll1llll1_opy_ is None:
                data[bstack1l1ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭῝")] = [{
                    bstack1l1ll1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ῞"): bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ῟"),
                    bstack1l1ll1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬῠ"): bstack1lllll1llll1_opy_
                }]
            config = {
                bstack1l1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧῡ"): cls.default_headers()
            }
            bstack11ll11llll1_opy_ = bstack1l1ll1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨῢ").format(os.environ[bstack1l1ll1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨΰ")])
            bstack1llllll11ll1_opy_ = cls.request_url(bstack11ll11llll1_opy_)
            response = bstack1l1ll1ll1l_opy_(bstack1l1ll1_opy_ (u"ࠩࡓ࡙࡙࠭ῤ"), bstack1llllll11ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1ll1_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤῥ"))
        except Exception as error:
            logger.error(bstack1l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣῦ") + str(error))
            return {
                bstack1l1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬῧ"): bstack1l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬῨ"),
                bstack1l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨῩ"): str(error)
            }
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def bstack1lllll1ll11l_opy_(cls, response):
        bstack111lll1l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll1l1lll_opy_ = {}
        if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠨ࡬ࡺࡸࠬῪ")) is None:
            os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ύ")] = bstack1l1ll1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨῬ")
        else:
            os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ῭")] = bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠬࡰࡷࡵࠩ΅"), bstack1l1ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ`"))
        os.environ[bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ῰")] = bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῱"), bstack1l1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧῲ"))
        logger.info(bstack1l1ll1_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨῳ") + os.getenv(bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩῴ")));
        if bstack111l1ll1l_opy_.bstack1lllll1l1ll1_opy_(cls.bs_config, cls.bstack1lll11111l_opy_.get(bstack1l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭῵"), bstack1l1ll1_opy_ (u"࠭ࠧῶ"))) is True:
            bstack111111l11l1_opy_, build_hashed_id, bstack1lllll1l11ll_opy_ = cls.bstack1llllll111ll_opy_(bstack111lll1l_opy_)
            if bstack111111l11l1_opy_ != None and build_hashed_id != None:
                bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῷ")] = {
                    bstack1l1ll1_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫῸ"): bstack111111l11l1_opy_,
                    bstack1l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫΌ"): build_hashed_id,
                    bstack1l1ll1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧῺ"): bstack1lllll1l11ll_opy_
                }
            else:
                bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫΏ")] = {}
        else:
            bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῼ")] = {}
        bstack1llllll11l11_opy_, build_hashed_id = cls.bstack1lllll11lll1_opy_(bstack111lll1l_opy_)
        if bstack1llllll11l11_opy_ != None and build_hashed_id != None:
            bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭´")] = {
                bstack1l1ll1_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ῾"): bstack1llllll11l11_opy_,
                bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῿"): build_hashed_id,
            }
        else:
            bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ ")] = {}
        if bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ ")].get(bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ ")) != None or bstack1lllll1l1lll_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ ")].get(bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ ")) != None:
            cls.bstack1lllll11llll_opy_(bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠧ࡫ࡹࡷࠫ ")), bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ ")))
        return bstack1lllll1l1lll_opy_
    @classmethod
    def bstack1llllll111ll_opy_(cls, bstack111lll1l_opy_):
        if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ ")) == None:
            cls.bstack1llllll11111_opy_()
            return [None, None, None]
        if bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ ")][bstack1l1ll1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ ")] != True:
            cls.bstack1llllll11111_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ ")])
            return [None, None, None]
        logger.debug(bstack1l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ​"))
        os.environ[bstack1l1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭‌")] = bstack1l1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭‍")
        if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠩ࡭ࡻࡹ࠭‎")):
            os.environ[bstack1l1ll1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ‏")] = json.dumps({
                bstack1l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭‐"): bstack11ll1ll1111_opy_(cls.bs_config),
                bstack1l1ll1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ‑"): bstack11ll1l1l1l1_opy_(cls.bs_config)
            })
        if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ‒")):
            os.environ[bstack1l1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭–")] = bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ—")]
        if bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ―")].get(bstack1l1ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‖"), {}).get(bstack1l1ll1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ‗")):
            os.environ[bstack1l1ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭‘")] = str(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭’")][bstack1l1ll1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ‚")][bstack1l1ll1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ‛")])
        else:
            os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ“")] = bstack1l1ll1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ”")
        return [bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠫ࡯ࡽࡴࠨ„")], bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ‟")], os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ†")]]
    @classmethod
    def bstack1lllll11lll1_opy_(cls, bstack111lll1l_opy_):
        if bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ‡")) == None:
            cls.bstack1lllll1l11l1_opy_()
            return [None, None]
        if bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ•")][bstack1l1ll1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ‣")] != True:
            cls.bstack1lllll1l11l1_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ․")])
            return [None, None]
        if bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ‥")].get(bstack1l1ll1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭…")):
            logger.debug(bstack1l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ‧"))
            parsed = json.loads(os.getenv(bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ "), bstack1l1ll1_opy_ (u"ࠨࡽࢀࠫ ")))
            capabilities = bstack1lllll11_opy_.bstack1lllll1lll11_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ‪")][bstack1l1ll1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‫")][bstack1l1ll1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ‬")], bstack1l1ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‭"), bstack1l1ll1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ‮"))
            bstack1llllll11l11_opy_ = capabilities[bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ ")]
            os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭‰")] = bstack1llllll11l11_opy_
            if bstack1l1ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ‱") in bstack111lll1l_opy_ and bstack111lll1l_opy_.get(bstack1l1ll1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤ′")) is None:
                parsed[bstack1l1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ″")] = capabilities[bstack1l1ll1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭‴")]
            os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ‵")] = json.dumps(parsed)
            scripts = bstack1lllll11_opy_.bstack1lllll1lll11_opy_(bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ‶")][bstack1l1ll1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‷")][bstack1l1ll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ‸")], bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ‹"), bstack1l1ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬ›"))
            bstack1ll1l1l1l_opy_.bstack1l11lll111_opy_(scripts)
            commands = bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ※")][bstack1l1ll1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ‼")][bstack1l1ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨ‽")].get(bstack1l1ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ‾"))
            bstack1ll1l1l1l_opy_.bstack11lll11l1l1_opy_(commands)
            bstack11ll1l11ll1_opy_ = capabilities.get(bstack1l1ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ‿"))
            bstack1ll1l1l1l_opy_.bstack11ll11lllll_opy_(bstack11ll1l11ll1_opy_)
            bstack1ll1l1l1l_opy_.store()
        return [bstack1llllll11l11_opy_, bstack111lll1l_opy_[bstack1l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⁀")]]
    @classmethod
    def bstack1llllll11111_opy_(cls, response=None):
        os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⁁")] = bstack1l1ll1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⁂")
        os.environ[bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⁃")] = bstack1l1ll1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⁄")
        os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⁅")] = bstack1l1ll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⁆")
        os.environ[bstack1l1ll1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⁇")] = bstack1l1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⁈")
        os.environ[bstack1l1ll1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⁉")] = bstack1l1ll1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⁊")
        cls.bstack1llllll11lll_opy_(response, bstack1l1ll1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ⁋"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1l11l1_opy_(cls, response=None):
        os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⁌")] = bstack1l1ll1_opy_ (u"ࠩࡱࡹࡱࡲࠧ⁍")
        os.environ[bstack1l1ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⁎")] = bstack1l1ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⁏")
        os.environ[bstack1l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⁐")] = bstack1l1ll1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⁑")
        cls.bstack1llllll11lll_opy_(response, bstack1l1ll1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ⁒"))
        return [None, None, None]
    @classmethod
    def bstack1lllll11llll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⁓")] = jwt
        os.environ[bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⁔")] = build_hashed_id
    @classmethod
    def bstack1llllll11lll_opy_(cls, response=None, product=bstack1l1ll1_opy_ (u"ࠥࠦ⁕")):
        if response == None or response.get(bstack1l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ⁖")) == None:
            logger.error(product + bstack1l1ll1_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ⁗"))
            return
        for error in response[bstack1l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭⁘")]:
            bstack11l11ll1ll1_opy_ = error[bstack1l1ll1_opy_ (u"ࠧ࡬ࡧࡼࠫ⁙")]
            error_message = error[bstack1l1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⁚")]
            if error_message:
                if bstack11l11ll1ll1_opy_ == bstack1l1ll1_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣ⁛"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ⁜") + product + bstack1l1ll1_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ⁝"))
    @classmethod
    def bstack1lllll1lll1l_opy_(cls):
        if cls.bstack11111l11111_opy_ is not None:
            return
        cls.bstack11111l11111_opy_ = bstack111111lllll_opy_(cls.bstack1lllll1l1l1l_opy_)
        cls.bstack11111l11111_opy_.start()
    @classmethod
    def bstack111ll11l1l_opy_(cls):
        if cls.bstack11111l11111_opy_ is None:
            return
        cls.bstack11111l11111_opy_.shutdown()
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def bstack1lllll1l1l1l_opy_(cls, bstack111l1111l1_opy_, event_url=bstack1l1ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⁞")):
        config = {
            bstack1l1ll1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ "): cls.default_headers()
        }
        logger.debug(bstack1l1ll1_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢ⁠").format(bstack1l1ll1_opy_ (u"ࠨ࠮ࠣࠫ⁡").join([event[bstack1l1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁢")] for event in bstack111l1111l1_opy_])))
        response = bstack1l1ll1ll1l_opy_(bstack1l1ll1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⁣"), cls.request_url(event_url), bstack111l1111l1_opy_, config)
        bstack11lll1111ll_opy_ = response.json()
    @classmethod
    def bstack11l1111l_opy_(cls, bstack111l1111l1_opy_, event_url=bstack1l1ll1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⁤")):
        logger.debug(bstack1l1ll1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⁥").format(bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⁦")]))
        if not bstack1lllll11_opy_.bstack1lllll1l1l11_opy_(bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⁧")]):
            logger.debug(bstack1l1ll1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⁨").format(bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁩")]))
            return
        bstack1lll1l1l11_opy_ = bstack1lllll11_opy_.bstack1llllll1111l_opy_(bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁪")], bstack111l1111l1_opy_.get(bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⁫")))
        if bstack1lll1l1l11_opy_ != None:
            if bstack111l1111l1_opy_.get(bstack1l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⁬")) != None:
                bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⁭")][bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⁮")] = bstack1lll1l1l11_opy_
            else:
                bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⁯")] = bstack1lll1l1l11_opy_
        if event_url == bstack1l1ll1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⁰"):
            cls.bstack1lllll1lll1l_opy_()
            logger.debug(bstack1l1ll1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨⁱ").format(bstack111l1111l1_opy_[bstack1l1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⁲")]))
            cls.bstack11111l11111_opy_.add(bstack111l1111l1_opy_)
        elif event_url == bstack1l1ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⁳"):
            cls.bstack1lllll1l1l1l_opy_([bstack111l1111l1_opy_], event_url)
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def bstack11llll1l1_opy_(cls, logs):
        bstack1lllll1l1111_opy_ = []
        for log in logs:
            bstack1lllll1ll111_opy_ = {
                bstack1l1ll1_opy_ (u"࠭࡫ࡪࡰࡧࠫ⁴"): bstack1l1ll1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ⁵"),
                bstack1l1ll1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⁶"): log[bstack1l1ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⁷")],
                bstack1l1ll1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⁸"): log[bstack1l1ll1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⁹")],
                bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ⁺"): {},
                bstack1l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⁻"): log[bstack1l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⁼")],
            }
            if bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁽") in log:
                bstack1lllll1ll111_opy_[bstack1l1ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁾")] = log[bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁿ")]
            elif bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₀") in log:
                bstack1lllll1ll111_opy_[bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ₁")] = log[bstack1l1ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭₂")]
            bstack1lllll1l1111_opy_.append(bstack1lllll1ll111_opy_)
        cls.bstack11l1111l_opy_({
            bstack1l1ll1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₃"): bstack1l1ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ₄"),
            bstack1l1ll1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ₅"): bstack1lllll1l1111_opy_
        })
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def bstack1lllll1ll1ll_opy_(cls, steps):
        bstack1lllll1l111l_opy_ = []
        for step in steps:
            bstack1llllll11l1l_opy_ = {
                bstack1l1ll1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ₆"): bstack1l1ll1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ₇"),
                bstack1l1ll1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ₈"): step[bstack1l1ll1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ₉")],
                bstack1l1ll1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ₊"): step[bstack1l1ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ₋")],
                bstack1l1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ₌"): step[bstack1l1ll1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ₍")],
                bstack1l1ll1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭₎"): step[bstack1l1ll1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ₏")]
            }
            if bstack1l1ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ₐ") in step:
                bstack1llllll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧₑ")] = step[bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨₒ")]
            elif bstack1l1ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩₓ") in step:
                bstack1llllll11l1l_opy_[bstack1l1ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪₔ")] = step[bstack1l1ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫₕ")]
            bstack1lllll1l111l_opy_.append(bstack1llllll11l1l_opy_)
        cls.bstack11l1111l_opy_({
            bstack1l1ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩₖ"): bstack1l1ll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪₗ"),
            bstack1l1ll1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬₘ"): bstack1lllll1l111l_opy_
        })
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1lll11llll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1l1l1111ll_opy_(cls, screenshot):
        cls.bstack11l1111l_opy_({
            bstack1l1ll1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬₙ"): bstack1l1ll1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ₚ"),
            bstack1l1ll1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨₛ"): [{
                bstack1l1ll1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩₜ"): bstack1l1ll1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧ₝"),
                bstack1l1ll1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ₞"): datetime.datetime.utcnow().isoformat() + bstack1l1ll1_opy_ (u"࡛ࠧࠩ₟"),
                bstack1l1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ₠"): screenshot[bstack1l1ll1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ₡")],
                bstack1l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ₢"): screenshot[bstack1l1ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₣")]
            }]
        }, event_url=bstack1l1ll1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ₤"))
    @classmethod
    @bstack111l1111ll_opy_(class_method=True)
    def bstack11l11l1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1111l_opy_({
            bstack1l1ll1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ₥"): bstack1l1ll1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ₦"),
            bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ₧"): {
                bstack1l1ll1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ₨"): cls.current_test_uuid(),
                bstack1l1ll1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ₩"): cls.bstack111ll11ll1_opy_(driver)
            }
        })
    @classmethod
    def bstack111llll111_opy_(cls, event: str, bstack111l1111l1_opy_: bstack111l11ll11_opy_):
        bstack1111ll1lll_opy_ = {
            bstack1l1ll1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ₪"): event,
            bstack111l1111l1_opy_.bstack111l11llll_opy_(): bstack111l1111l1_opy_.bstack111l1l11ll_opy_(event)
        }
        cls.bstack11l1111l_opy_(bstack1111ll1lll_opy_)
        result = getattr(bstack111l1111l1_opy_, bstack1l1ll1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₫"), None)
        if event == bstack1l1ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ€"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ₭"): bstack1l1ll1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ₮")}
        elif event == bstack1l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ₯"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₰"): getattr(result, bstack1l1ll1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₱"), bstack1l1ll1_opy_ (u"ࠬ࠭₲"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₳"), None) is None or os.environ[bstack1l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ₴")] == bstack1l1ll1_opy_ (u"ࠣࡰࡸࡰࡱࠨ₵")) and (os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ₶"), None) is None or os.environ[bstack1l1ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ₷")] == bstack1l1ll1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₸")):
            return False
        return True
    @staticmethod
    def bstack1lllll1lllll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1ll1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ₹"): bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ₺"),
            bstack1l1ll1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ₻"): bstack1l1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭₼")
        }
        if os.environ.get(bstack1l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭₽"), None):
            headers[bstack1l1ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ₾")] = bstack1l1ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ₿").format(os.environ[bstack1l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ⃀")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1ll1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ⃁").format(bstack1llllll1l111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⃂"), None)
    @staticmethod
    def bstack111ll11ll1_opy_(driver):
        return {
            bstack11l11lll1l1_opy_(): bstack111llll1l11_opy_(driver)
        }
    @staticmethod
    def bstack1llllll111l1_opy_(exception_info, report):
        return [{bstack1l1ll1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⃃"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111l11l1_opy_(typename):
        if bstack1l1ll1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ⃄") in typename:
            return bstack1l1ll1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ⃅")
        return bstack1l1ll1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ⃆")